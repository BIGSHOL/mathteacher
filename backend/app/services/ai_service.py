"""AI 보조 서비스 (Gemini) - 힌트, 유연 채점, 피드백, 문제 동적 생성."""

import json
import logging
import re
from uuid import uuid4

from google import genai
from google.genai import types

from app.core.config import settings
from app.services.prompt_context import format_prompt_context, CONCEPT_QUESTION_PROTOCOL, PROMPT_CONTEXTS
from app.services.concept_generator import ConceptGenerator

logger = logging.getLogger(__name__)

# 학년 라벨 매핑
GRADE_LABELS: dict[str, str] = {
    "elementary_3": "초3", "elementary_4": "초4",
    "elementary_5": "초5", "elementary_6": "초6",
    "middle_1": "중1", "middle_2": "중2", "middle_3": "중3",
    "high_1": "고1", "high_2": "고1",
}

# 싱글턴 클라이언트
_client: genai.Client | None = None


def _get_client() -> genai.Client | None:
    """Gemini 클라이언트 반환. API 키 미설정 시 None."""
    global _client
    if not settings.GEMINI_API_KEY:
        return None
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def _cross_validate_answer(q: dict, options: list) -> str | None:
    """객관식 정답 라벨이 해설의 최종 답과 일치하는지 교차검증.

    Returns:
        불일치 시 경고 메시지, 일치 시 None.
        불일치가 자동 수정 가능한 경우 q["correct_answer"]를 직접 수정함.
    """
    correct_label = str(q.get("correct_answer", "")).strip().upper()
    explanation = str(q.get("explanation", ""))

    # 정답 라벨에 해당하는 선지 텍스트 찾기
    label_to_text: dict[str, str] = {}
    for opt in options:
        if isinstance(opt, dict):
            label_to_text[str(opt.get("label", "")).upper()] = str(opt.get("text", ""))

    correct_text = label_to_text.get(correct_label, "")
    if not correct_text:
        return None

    # 해설에서 최종 답 추출: "= 8개", "= 360", "답은 8개이다" 등
    final_answers = re.findall(r"=\s*(\-?[\d,]+(?:\.\d+)?)\s*(개|cm|m|kg|g|원|명|마리|장|번|°)?", explanation)
    if not final_answers:
        return None

    # 마지막으로 나온 최종 답
    final_value = final_answers[-1][0].replace(",", "")
    final_unit = final_answers[-1][1]
    final_str = f"{final_value}{final_unit}" if final_unit else final_value

    # 정답 선지에 최종 답이 포함되어 있는지 확인
    if final_value in correct_text or final_str in correct_text:
        return None  # 일치 → OK

    # 다른 선지에 최종 답이 있으면 자동 수정
    for label, text in label_to_text.items():
        if label != correct_label and (final_value in text or final_str in text):
            logger.warning(
                "정답 라벨 자동 수정: %s(%s) → %s(%s) | 해설 최종답=%s",
                correct_label, correct_text, label, text, final_str,
            )
            q["correct_answer"] = label  # 자동 수정
            return None  # 수정 완료 → 경고 없음 (문제 유지)

    return None


def _validate_generated_question(q: dict, category: str = "") -> list[str]:
    """생성된 문제의 품질 검증. 경고 메시지 목록을 반환."""
    warnings: list[str] = []
    content = str(q.get("content", ""))
    qtype = q.get("question_type", "")

    # 보기 기호가 content에 포함된 경우 (객관식/빈칸 공통)
    if re.search(r"\([ㄱㄴㄷㄹㅁ가나다라]\)", content):
        warnings.append("보기 기호가 문제 내용에 포함됨")

    # 빈칸 전용 검증
    if qtype == "fill_in_blank":
        if re.search(r"고르[시면]|선택|모두 고르", content):
            warnings.append("빈칸 문제에 선택형 표현 사용됨")
        # 빈칸에서 '다음 중/다음 수' 등 외부 참조 차단
        if re.search(r"다음[은의\s]*(수|중|표|식|그림|보기|과정)", content):
            warnings.append("외부 참조 표현 '다음...' 사용됨")
        # '과정이다' + '(가)/(나)' 참조형 빈칸
        if re.search(r"과정이다.*\([가나다라]\)", content):
            warnings.append("참조형 빈칸 문제 - 풀이 과정 참조")
        # 괄호 안 숫자 목록 나열: (2, 4, 9, 11) 패턴
        if re.search(r"\(\s*\d+\s*,\s*\d+\s*,\s*\d+", content):
            warnings.append("빈칸 문제에 숫자 목록 나열됨")
        # 쉼표로 연결된 3개 이상 숫자 나열: "1, 3, 5, 7 중에서"
        if re.search(r"\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+", content):
            warnings.append("빈칸 문제에 쉼표 구분 숫자 나열됨")

    # 객관식인데 options가 없거나 비어있음
    if qtype == "multiple_choice":
        options = q.get("options")
        if not options or not isinstance(options, list) or len(options) < 2:
            warnings.append("객관식인데 보기가 없거나 부족함")
        # 정답 라벨-해설 교차검증: 해설의 최종 답이 정답 선지와 일치하는지
        elif q.get("correct_answer") and q.get("explanation"):
            _check = _cross_validate_answer(q, options)
            if _check:
                warnings.append(_check)

    # 연산 트랙인데 계산 문제가 아닌 경우
    if category == "computation":
        # 용어 빈칸: '___도 아니다', '___라 한다', '___라고 한다'
        if re.search(r"_{2,}[도를이]|_{2,}\s*(라고?\s*한다|이라)", content):
            warnings.append("연산 트랙에 용어 빈칸 문제")
        # 판별형: '예/아니오', '존재하는가', '존재하지 않는다'
        if re.search(r"예\s*/\s*아니오|존재하는가|존재하지\s*않", content):
            warnings.append("연산 트랙에 판별형 문제")
        # '무엇인가?' 형태의 용어 암기형
        if re.search(r"무엇인가\??$|무엇일까\??$", content.strip()):
            warnings.append("연산 트랙에 암기형 문제")

    # 개념 트랙인데 단순 계산 문제인 경우
    if category == "concept":
        # 단순 계산식(숫자와 연산자)이 포함되어 있으면서, 개념적 맥락(의미, 이유 등)이 없는 경우
        is_calc_expr = re.search(r"[\d]+\s*[+\-×÷*/]\s*[\d]+", content)
        has_concept_kwd = re.search(r"정의|성질|옳은|설명|이유|특징|의미|뜻|몇\s*개|개수|과정|원리|잘못|틀린|모두|만족하는", content)
        
        if is_calc_expr and not has_concept_kwd:
             warnings.append("개념 트랙에 단순 연산 의심 (맥락 부족)")

        # [NO CALC] 단순 계산 요구 여부 (구체적 표현 차단)
        if re.search(r"계산하시오|구하시오|값을 구해|얼마인가", content):
            if not re.search(r"왜|이유|설명|의미|과정|원리", content):
                warnings.append("[NO CALC 위반] 단순 계산 요구, 개념 맥락 부족")

        # [WHY] '왜' 질문 포함 여부 (설명 요구 강화)
        has_why = re.search(r"왜|이유|설명|의미|과정|원리|어떻게|무엇을|차이점|같은|다른", content)
        if not has_why:
             warnings.append("[WHY 미충족] 설명/이유를 묻지 않음 (단편적 질문)")

    return warnings


class AIService:
    """AI 보조 서비스. 모든 메서드는 실패 시 None 반환."""

    async def grade_fill_blank(
        self,
        question_content: str,
        correct_answer: str,
        student_answer: str,
        accept_formats: list[str] | None,
    ) -> dict | None:
        """빈칸 채우기 유연 채점. 실패 시 None."""
        # 1단계: 규칙 기반 매칭
        student = student_answer.strip().replace(" ", "")
        correct = correct_answer.strip().replace(" ", "")

        if student == correct:
            return {"is_correct": True, "confidence": 1.0, "reason": "정확히 일치"}

        accept = [a.strip().replace(" ", "") for a in (accept_formats or [])]
        if student in accept:
            return {"is_correct": True, "confidence": 1.0, "reason": "허용 표기와 일치"}

        # 2단계: Gemini 유연 채점
        client = _get_client()
        if not client:
            return None

        prompt = (
            "수학 문제의 빈칸 채우기 답안을 채점하세요.\n\n"
            f"[문제] {question_content}\n"
            f"[정답] {correct_answer}\n"
            f"[학생 답] {student_answer}\n\n"
            "다음 기준으로 판단하세요:\n"
            "- 동치인 수학적 표현은 정답 (예: 3/4 = 0.75, -3 = -3.0)\n"
            "- 단위 표기 차이는 정답 (예: 5cm = 5 cm)\n"
            "- 약분/통분 결과가 같으면 정답\n"
            "- 수학적으로 다른 값이면 오답\n\n"
            "반드시 아래 JSON 형식으로만 답하세요:\n"
            '{"is_correct": true/false, "confidence": 0.0~1.0, "reason": "판단 근거"}'
        )

        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=200),
            )
            text = response.text.strip()
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip()
            result = json.loads(text)
            return {
                "is_correct": bool(result.get("is_correct", False)),
                "confidence": float(result.get("confidence", 0.5)),
                "reason": str(result.get("reason", "")),
            }
        except Exception:
            logger.exception("AI fill-blank grading failed")
            return None

    async def generate_feedback(
        self,
        question_content: str,
        correct_answer: str,
        student_answer: str,
        explanation: str,
        student_grade: str,
    ) -> dict | None:
        """오답 맞춤 피드백 생성. 실패 시 None."""
        client = _get_client()
        if not client:
            return None

        grade_label = GRADE_LABELS.get(student_grade, student_grade)

        prompt = (
            f"당신은 {grade_label} 학생의 수학 오답을 분석하는 전문 튜터입니다.\n\n"
            f"[문제] {question_content}\n"
            f"[정답] {correct_answer}\n"
            f"[학생 답] {student_answer}\n"
        )
        if explanation:
            prompt += f"[해설] {explanation}\n"
        prompt += (
            "\n학생이 왜 틀렸는지 분석하고, 아래 JSON 형식으로 답하세요:\n"
            "{\n"
            '  "feedback": "학생 눈높이에 맞는 친절한 설명 (2~4문장)",\n'
            '  "error_type": "오류 유형 (예: 부호 오류, 계산 실수, 개념 혼동, 문제 이해 부족)",\n'
            '  "suggestion": "보완 학습 제안 (1~2문장)"\n'
            "}\n"
            "반드시 JSON만 출력하세요."
        )

        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=400),
            )
            text = response.text.strip()
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip()
            result = json.loads(text)
            return {
                "feedback": str(result.get("feedback", "")),
                "error_type": str(result.get("error_type", "")),
                "suggestion": str(result.get("suggestion", "")),
            }
        except Exception:
            logger.exception("AI feedback generation failed")
            return None

    async def generate_questions(
        self,
        concept_name: str,
        concept_id: str,
        grade: str,
        category: str,
        part: str,
        question_type: str,
        count: int,
        difficulty_min: int = 1,
        difficulty_max: int = 10,
        existing_contents: list[str] | None = None,
        id_prefix: str = "",
        start_seq: int = 1,
        concept_method: str | None = None,  # 신규 (Phase 2)
        fading_level: int | None = None,    # 신규 (Phase 2)
    ) -> list[dict] | None:
        """Gemini로 문제를 동적 생성. 실패 시 None.

        Args:
            concept_name: 개념 이름 (예: "소인수분해")
            concept_id: 개념 ID
            grade: 학년 (예: "middle_1")
            category: "computation" 또는 "concept"
            part: "calc", "algebra", "func", "geo", "data", "word"
            question_type: "multiple_choice" 또는 "fill_in_blank"
            count: 생성할 문제 수
            difficulty_min: 최소 난이도
            difficulty_max: 최대 난이도
            existing_contents: 기존 문제 content 목록 (중복 방지)
            id_prefix: ID 접두사 (예: "ai-m1-fb") - 비어있으면 자동 생성
            start_seq: 시작 시퀀스 번호

        Returns:
            Question 모델에 바로 넣을 수 있는 dict 리스트
        """
        client = _get_client()
        if not client:
            return None

        # [Phase 3] 점진적 빈칸 소거 (Gradual Fading) 처리
        if concept_method == "gradual_fading":
            generator = ConceptGenerator()
            # PROMPT_CONTEXTS에서 key_summary 등 정보 조회
            ctx = PROMPT_CONTEXTS.get(concept_id, {})
            key_summary = ctx.get("key_summary", "")
            core_concepts = ctx.get("core_concepts", "") if not key_summary else ""

            return await generator.generate_gradual_fading(
                concept_name=concept_name,
                concept_id=concept_id,
                grade=grade,
                key_summary=key_summary,
                core_concepts=core_concepts,
                id_prefix=id_prefix,
                start_seq=start_seq,
            )

        # [Phase 4] 오개념 분석 (Error Analysis) 처리
        if concept_method == "error_analysis":
            generator = ConceptGenerator()
            ctx = PROMPT_CONTEXTS.get(concept_id, {})
            misconceptions = ctx.get("misconceptions", "")
            
            return await generator.generate_error_analysis(
                concept_name=concept_name,
                concept_id=concept_id,
                grade=grade,
                misconceptions=misconceptions,
                count=count,
                id_prefix=id_prefix,
                start_seq=start_seq,
            )

        # [Phase 5] 시각적 해체 (Visual Decoding) 처리
        if concept_method == "visual_decoding":
            generator = ConceptGenerator()
            ctx = PROMPT_CONTEXTS.get(concept_id, {})
            core_concepts = ctx.get("core_concepts", "")
            
            return await generator.generate_visual_decoding(
                concept_name=concept_name,
                concept_id=concept_id,
                grade=grade,
                core_concepts=core_concepts,
                count=count,
                id_prefix=id_prefix,
                start_seq=start_seq,
            )

        grade_label = GRADE_LABELS.get(grade, grade)
        cat_label = "연산" if category == "computation" else "개념"

        # 트랙별 출제 지침
        if category == "computation":
            track_instruction = (
                "\n## 트랙 지침: 연산 (계산 속도 훈련)\n"
                "**이 트랙은 반복 계산으로 속도를 높이는 훈련입니다.**\n"
                "문제의 정답은 반드시 '직접 계산한 숫자/수식'이어야 합니다.\n"
                "\n### 연산 트랙에 적합한 문제 유형\n"
                "- 소인수분해: '72를 소인수분해하면?' → 답: 2³×3²\n"
                "- 최대공약수/최소공배수 계산: '24와 36의 최대공약수는?' → 답: 12\n"
                "- 사칙연산: '(-3)×(-5)+2의 값은?' → 답: 17\n"
                "- 거듭제곱 계산: '2⁴×3의 값은?' → 답: 48\n"
                "- 약수/배수 구하기: '120의 양의 약수의 합은?' → 답: 360\n"
                "- 식의 값: 'x=3일 때, 2x²-5x+1의 값은?' → 답: 4\n"
                "- 방정식 풀기: '3x+6=0의 해는?' → 답: -2\n"
                "\n### 연산 트랙에서 금지되는 문제 유형 (위반 시 삭제)\n"
                "- 용어 암기: '가장 작은 소수는?' (답: 2) → 계산 아닌 암기\n"
                "- 판별형: '12와 35는 서로소인가? (예/아니오)' → 계산 아닌 판별\n"
                "- 용어 빈칸: '1은 소수도 아니고 ___도 아니다' → 용어 채우기\n"
                "- 개수 세기: '1부터 20까지 소수의 개수는?' → 나열 후 세기\n"
                "- 정의 문제: '두 자연수의 최대공약수가 1일 때 이를 ___라 한다' → 용어\n"
                "- 존재 여부: '~인 경우는 존재하는가?' → 판단형\n"
            )
        else:
            track_instruction = (
                "\n## 트랙 지침: 개념 (수학적 이해력 평가)\n"
                "이 트랙은 수학 개념의 이해와 적용을 평가합니다.\n"
                "- 정의, 성질, 판별, 분류, 개수 세기 등 개념 이해 문제를 출제하세요.\n"
                "- 좋은 예: '소수의 정의로 옳은 것은?', '1부터 20까지 소수의 개수는?'\n"
                "- 좋은 예: '서로소인 두 수의 조건은?', '합성수의 특징은?'\n"
            )

        # 객관식/빈칸에 따른 프롬프트 보강
        if question_type == "fill_in_blank":
            type_instruction = (
                "빈칸 채우기 문제를 생성하세요.\n"
                '- content: 문제 텍스트 (예: "72를 소인수분해하면?")\n'
                "- options: null\n"
                '- correct_answer: 정답 (예: "2³×3²")\n'
                '- accept_formats: 허용 답안 리스트 (예: ["2^3×3^2", "2^3*3^2"])\n'
                "\n## 빈칸 채우기 필수 규칙 (매우 중요)\n"
                "1. 학생이 숫자·수식·단어를 직접 입력하는 형식입니다. 보기가 없습니다.\n"
                "2. 정답은 반드시 하나의 명확한 값이어야 합니다.\n"
                "3. **기호 사용 금지**: (ㄱ), (ㄴ), (가), (나) 등 보기용 기호를 절대 사용하지 마세요.\n"
                "   - 대신 `[ ]` 또는 `( )`를 사용하여 빈칸을 표시하세요. 예: '5 + 2 = [ ]'\n"
                "4. '고르시오', '선택하시오', '다음 중' 등 객관식형 표현을 절대 사용하지 마세요.\n"
                "5. **목록 나열 금지**: 후보 숫자 목록(예: 2, 4, 7, 9)을 제시하지 마세요.\n"
            )
            json_example = (
                '{"content": "72를 소인수분해하면?", '
                '"correct_answer": "2³×3²", '
                '"explanation": "72=2×36=2×2×18=2×2×2×9=2³×3²", '
                '"difficulty": 4, '
                '"accept_formats": ["2^3*3^2"]}'
            )
        else:
            type_instruction = (
                "객관식(4지선다) 문제를 생성하세요.\n"
                "- 반드시 선지 4개 (A, B, C, D)\n"
                "- correct_answer: 정답 라벨 (A/B/C/D 중 하나)\n"
                "\n## 객관식 필수 규칙 (매우 중요)\n"
                "1. **기호 사용 금지**: (ㄱ), (ㄴ), (가), (나) 등 기호를 content에 넣지 마세요.\n"
                "   - 만약 문제 내에서 특정 부분을 지칭해야 한다면 [A], [B] 또는 [가], [나] 대신 [ ]를 사용하거나 전체 식을 다시 쓰세요.\n"
                "2. **선지는 options에만**: content에는 문제 텍스트만 넣으세요. 선지 목록을 content에 나열하지 마세요.\n"
                "## 객관식(MC) 지침\n"
                "1. options 배열에 5개의 선택지를 'label'(A-E)과 'text' 형식으로 제공하세요.\n"
                "2. correct_answer는 반드시 'A', 'B', 'C', 'D', 'E' 중 하나여야 합니다.\n"
                "3. (ㄱ), (ㄴ), (가), (나) 등의 기호를 사용하지 마세요.\n"
                "4. [CoT 지시] 문제를 낼 때 먼저 스스로 계산하고, 그 결과가 선지에 있는지 확인한 후 최종 JSON을 구성하세요."
            )
            json_example = (
                '{"content": "24의 약수의 개수는?", '
                '"options": [{"label":"A","text":"4개"},{"label":"B","text":"6개"},'
                '{"label":"C","text":"8개"},{"label":"D","text":"10개"}], '
                '"correct_answer": "C", '
                '"explanation": "24=2³×3이므로 약수의 개수=(3+1)(1+1)=8개", '
                '"difficulty": 5}'
            )

        # 트랙별 지침 (상세 내용 통합)
        if category == "concept":
            track_instruction += (
                "\n\n## [중요] 개념 트랙 금지 사항\n"
                "1. **단순 계산 금지**: '다음 식을 계산하시오', '25 + 36 = ?' 같은 단순 연산 문제는 절대 만들지 마세요.\n"
                "2. **원리 중심**: 계산을 하더라도 '왜 그렇게 되는지', '어떤 성질을 이용했는지'를 묻거나, 과정의 빈칸을 채우게 하세요.\n"
                "3. **개념 키워드 사용**: 정의, 성질, 이유, 설명, 포함 관계, 분류, 개수 등을 묻는 표현을 적극 사용하세요."
            )
            # [Phase 1] 3단 변환 프로토콜 주입
            track_instruction += CONCEPT_QUESTION_PROTOCOL
        else:
            track_instruction += "\n\n## [중요] 연산 트랙 금지 사항: 개념이나 정의를 묻지 말고, 오직 빠르고 정확한 '계산 수행 능력'을 테스트하세요."

        # 중복 방지
        existing_section = ""
        if existing_contents:
            existing_list = "\n".join(f"- {c}" for c in existing_contents[:20])
            existing_section = (
                f"\n## 중복 금지 목록\n"
                f"아래 문제들과 중복되지 않게 하세요:\n"
                f"{existing_list}\n"
            )

        curriculum_context = format_prompt_context(concept_id, grade)
        context_section = f"\n## 교육과정 배경\n{curriculum_context}\n" if curriculum_context else ""

        prompt = (
            f"당신은 {grade_label} 수학 문제 출제 전문가입니다.\n\n"
            f"[개념명] {concept_name} | [트랙] {cat_label}\n"
            f"[난이도] {difficulty_min}~{difficulty_max} | [개수] {count}개\n\n"
            f"{track_instruction}\n\n"
            f"{context_section}\n\n"
            f"{type_instruction}\n\n"
            "## 공통 규칙\n"
            "1. 정확성: 모든 계산은 100% 정확해야 합니다.\n"
            "2. 다양성: 한 개념 내에서도 다양한 상황과 난이도를 구성하세요.\n"
            "3. 기호 사용 금지: (ㄱ), (ㄴ), (가), (나), ①, ② 등은 절대 사용하지 마세요. 대신 [ ] 또는 ( )를 사용하세요.\n"
            "4. LaTeX 제한: LaTeX 문법을 사용할 수 있지만, array, tabular, begin{...} 등 복잡한 환경은 렌더링을 위해 사용하지 마세요.\n"
            f"{existing_section}\n\n"
            f"## 출력 형식: JSON 배열만 출력 (예: [{json_example}])"
        )

        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                response = client.models.generate_content(
                    model=settings.GEMINI_MODEL_NAME,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.4 + (attempt * 0.1),  # 재시도 시 창의성 약간 높임
                        max_output_tokens=4096,
                    ),
                )

                if not response.text:
                    if attempt < max_retries: continue
                    return None

                text = response.text.strip()
                # Markdown 코드 블록 제거
                if "```" in text:
                    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
                    if match:
                        text = match.group(1).strip()
                    else:
                        text = re.sub(r"```(?:json)?|```", "", text).strip()
                
                # 가끔 앞뒤에 붙는 불필요한 텍스트 제거 (최초 [ 와 마지막 ] 찾기)
                start_idx = text.find("[")
                end_idx = text.rfind("]")
                if start_idx != -1 and end_idx != -1:
                    text = text[start_idx:end_idx+1]

                questions_raw = json.loads(text)
                if not isinstance(questions_raw, list):
                    questions_raw = [questions_raw]

                # 결과 가공 및 검증
                result = []
                seq = start_seq
                for q in questions_raw[:count]:
                    qid = f"{id_prefix}-{seq:03d}" if id_prefix else f"ai-{uuid4().hex[:12]}"
                    seq += 1
                    
                    question_dict = {
                        "id": qid,
                        "concept_id": concept_id,
                        "category": category,
                        "part": part,
                        "question_type": question_type,
                        "difficulty": max(1, min(10, int(q.get("difficulty", 5)))),
                        "content": q.get("content", ""),
                        "correct_answer": q.get("correct_answer", ""),
                        "explanation": q.get("explanation", ""),
                        "concept_method": concept_method,  # 신규
                        "fading_level": fading_level,      # 신규
                        "points": 10,
                        "is_active": True,
                    }

                    if question_type == "multiple_choice":
                        options = q.get("options", [])
                        if options and isinstance(options, list):
                            formatted = []
                            labels = ["A", "B", "C", "D"]
                            for i, opt in enumerate(options[:4]):
                                formatted.append({
                                    "id": str(i + 1),
                                    "label": opt.get("label", labels[i]) if isinstance(opt, dict) else labels[i],
                                    "text": str(opt.get("text", opt) if isinstance(opt, dict) else opt),
                                })
                            question_dict["options"] = formatted
                        else:
                            continue # 보기 없는 객관식 제외
                    else:
                        question_dict["options"] = None
                        accept = q.get("accept_formats", [])
                        question_dict["blank_config"] = {
                            "blank_count": 1,
                            "accept_formats": accept if accept else [str(q.get("correct_answer", ""))],
                        }

                    # 품질 검증
                    warnings = _validate_generated_question(question_dict, category)
                    if not warnings:
                        result.append(question_dict)
                    else:
                        logger.warning("AI 문제 제외 (%s): %s", qid, "; ".join(warnings))

                if result:
                    logger.info("AI generated %d questions for %s (attempt %d)", len(result), concept_name, attempt + 1)
                    return result
                
                if attempt < max_retries:
                    logger.info("No valid questions generated for %s, retrying...", concept_name)
                    continue

            except json.JSONDecodeError as e:
                logger.error("JSON 파싱 실패 (시도 %d/%d): %s\nResponse: %s", attempt + 1, max_retries + 1, e, text[:500])
                if attempt < max_retries: continue
            except Exception:
                logger.exception("AI 문제 생성 중 예외 발생 (시도 %d)", attempt + 1)
                if attempt < max_retries: continue

        return None
