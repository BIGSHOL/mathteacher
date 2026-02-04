"""AI 보조 서비스 (Gemini) - 힌트, 유연 채점, 피드백, 문제 동적 생성."""

import json
import logging
import re
from uuid import uuid4

from google import genai
from google.genai import types

from app.core.config import settings

logger = logging.getLogger(__name__)

# 학년 라벨 매핑
GRADE_LABELS: dict[str, str] = {
    "elementary_3": "초3", "elementary_4": "초4",
    "elementary_5": "초5", "elementary_6": "초6",
    "middle_1": "중1", "middle_2": "중2", "middle_3": "중3",
    "high_1": "고1", "high_2": "고2",
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


class AIService:
    """AI 보조 서비스. 모든 메서드는 실패 시 None 반환."""

    async def generate_hint(
        self,
        question_content: str,
        question_type: str,
        options: list[str] | None,
        student_grade: str,
        hint_level: int,
    ) -> dict | None:
        """단계별 힌트 생성. 실패 시 None."""
        client = _get_client()
        if not client:
            return None

        grade_label = GRADE_LABELS.get(student_grade, student_grade)
        level_desc = {
            1: "풀이 방향만 가볍게 안내. 구체적인 숫자나 공식은 제시하지 마세요.",
            2: "관련 개념과 공식을 알려주되, 핵심 계산 단계는 비워두세요.",
            3: "풀이 과정을 거의 다 안내하되, 마지막 답만 빈칸으로 남기세요.",
        }

        prompt = (
            f"당신은 {grade_label} 학생을 위한 수학 튜터입니다.\n"
            f"학생이 아래 문제를 풀다가 막혔습니다. 힌트 레벨 {hint_level}에 맞춰 도움을 주세요.\n\n"
            f"[힌트 레벨 설명]\n{level_desc.get(hint_level, level_desc[1])}\n\n"
            f"[문제]\n{question_content}\n"
        )
        if options:
            prompt += f"[선지] {', '.join(options)}\n"
        prompt += "\n절대 정답을 직접 알려주지 마세요. 한국어로 2~4문장, 친절하게 답하세요."

        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.4, max_output_tokens=300),
            )
            return {"hint": response.text.strip(), "hint_level": hint_level}
        except Exception:
            logger.exception("AI hint generation failed")
            return None

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

        grade_label = GRADE_LABELS.get(grade, grade)
        cat_label = "연산" if category == "computation" else "개념"

        if question_type == "fill_in_blank":
            type_instruction = (
                "빈칸 채우기 문제를 생성하세요.\n"
                '- content: 문제 텍스트 (예: "72를 소인수분해하면?")\n'
                "- options: null\n"
                '- correct_answer: 정답 (예: "2³×3²")\n'
                '- accept_formats: 허용 답안 리스트 (예: ["2^3×3^2", "2^3*3^2"])\n'
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
                "- 오개념을 반영한 매력적인 오답 선지 포함\n"
                "- correct_answer: 정답 라벨 (A/B/C/D 중 하나)\n"
            )
            json_example = (
                '{"content": "24의 약수의 개수는?", '
                '"options": [{"label":"A","text":"4개"},{"label":"B","text":"6개"},'
                '{"label":"C","text":"8개"},{"label":"D","text":"10개"}], '
                '"correct_answer": "C", '
                '"explanation": "24=2³×3이므로 약수의 개수=(3+1)(1+1)=8개", '
                '"difficulty": 5}'
            )

        # 중복 방지: 기존 문제 목록을 프롬프트에 포함
        existing_section = ""
        if existing_contents:
            existing_list = "\n".join(f"- {c}" for c in existing_contents[:20])
            existing_section = (
                f"\n## 이미 존재하는 문제 (중복 금지)\n"
                f"아래 문제들과 동일하거나 숫자만 바꾼 유사 문제는 절대 생성하지 마세요:\n"
                f"{existing_list}\n"
            )

        prompt = (
            f"당신은 2022 개정 교육과정 기반 {grade_label} 수학 문제 출제 전문가입니다.\n\n"
            f"[개념] {concept_name}\n"
            f"[트랙] {cat_label}\n"
            f"[난이도 범위] {difficulty_min}~{difficulty_max} (1=매우 쉬움, 10=매우 어려움)\n"
            f"[생성 개수] {count}개\n\n"
            f"{type_instruction}\n"
            "## 규칙\n"
            "1. 모든 수학 계산은 반드시 정확해야 합니다. 검산을 수행하세요.\n"
            "2. explanation에 풀이 과정을 포함하세요.\n"
            f"3. difficulty는 {difficulty_min}~{difficulty_max} 범위에서 다양하게 분포시키세요.\n"
            "4. 한국어로 작성하세요.\n"
            "5. 각 문제가 서로 다른 유형/소재여야 합니다.\n"
            f"{existing_section}\n"
            f"## 출력 형식 (JSON 배열)\n"
            f"예시: [{json_example}]\n\n"
            f"반드시 {count}개의 문제를 JSON 배열로만 출력하세요. 다른 텍스트는 포함하지 마세요."
        )

        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.5,
                    max_output_tokens=4096,
                ),
            )
            text = response.text.strip()

            # JSON 추출
            if "```" in text:
                match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
                if match:
                    text = match.group(1)

            questions_raw = json.loads(text)
            if not isinstance(questions_raw, list):
                questions_raw = [questions_raw]

            # Question 모델에 맞게 변환
            result = []
            seq = start_seq
            for q in questions_raw[:count]:
                if id_prefix:
                    qid = f"{id_prefix}-{seq:03d}"
                else:
                    qid = f"ai-{uuid4().hex[:12]}"
                seq += 1
                diff = int(q.get("difficulty", 5))
                diff = max(1, min(10, diff))

                question_dict = {
                    "id": qid,
                    "concept_id": concept_id,
                    "category": category,
                    "part": part,
                    "question_type": question_type,
                    "difficulty": diff,
                    "content": q.get("content", ""),
                    "correct_answer": q.get("correct_answer", ""),
                    "explanation": q.get("explanation", ""),
                    "points": 10,
                    "is_active": True,
                }

                if question_type == "multiple_choice":
                    options = q.get("options", [])
                    if options and isinstance(options, list):
                        formatted = []
                        labels = ["A", "B", "C", "D"]
                        for i, opt in enumerate(options[:4]):
                            if isinstance(opt, dict):
                                formatted.append({
                                    "id": str(i + 1),
                                    "label": opt.get("label", labels[i]),
                                    "text": str(opt.get("text", "")),
                                })
                            else:
                                formatted.append({
                                    "id": str(i + 1),
                                    "label": labels[i],
                                    "text": str(opt),
                                })
                        question_dict["options"] = formatted
                    else:
                        question_dict["options"] = None
                else:
                    question_dict["options"] = None
                    accept = q.get("accept_formats", [])
                    question_dict["blank_config"] = {
                        "blank_count": 1,
                        "accept_formats": accept if accept else [q.get("correct_answer", "")],
                    }

                if question_dict["content"]:
                    result.append(question_dict)

            logger.info("AI generated %d questions for concept %s", len(result), concept_name)
            return result

        except Exception:
            logger.exception("AI question generation failed for concept %s", concept_name)
            return None
