"""개념 문항 생성기 (Type A, B, C)."""

import json
import logging
from uuid import uuid4

from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.common import ConceptMethod, QuestionType, QuestionCategory, ProblemPart

logger = logging.getLogger(__name__)


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


class ConceptGenerator:
    """개념 문항 전용 생성기."""

    async def generate_gradual_fading(
        self,
        concept_name: str,
        concept_id: str,
        grade: str,
        key_summary: str,
        core_concepts: str,
        id_prefix: str = "",
        start_seq: int = 1,
    ) -> list[dict] | None:
        """Type A: 점진적 빈칸 소거 (Gradual Fading) 문항 4단계 생성."""
        client = _get_client()
        if not client:
            return None

        # 핵심 문장이 없으면 코어 컨셉에서 추출 시도
        if not key_summary:
             key_summary_prompt = (
                 f"다음 개념 설명에서 가장 핵심이 되는 정의나 정리 1문장을 추출해줘.\n"
                 f"개념: {core_concepts}\n"
                 f"대상: {grade} 학생\n"
                 "출력: 핵심 문장 1개만 출력 (설명 제외)"
             )
             try:
                 resp = client.models.generate_content(
                     model=settings.GEMINI_MODEL_NAME,
                     contents=key_summary_prompt,
                 )
                 key_summary = resp.text.strip()
             except Exception:
                 logger.error("Failed to extract key summary for %s", concept_name)
                 return None

        prompt = (
            f"당신은 {grade} 수학 개념 교육 전문가입니다.\n"
            f"[개념] {concept_name}\n"
            f"[핵심 문장] {key_summary}\n\n"
            "핵심 문장을 학습하기 위한 '점진적 빈칸 소거(Gradual Fading)' 문제 4단계를 만드세요.\n"
            "각 단계는 동일한 핵심 문장을 기반으로 빈칸의 위치와 개수만 다르게 하여 난이도를 조절합니다.\n\n"
            "## 단계별 지침\n"
            "1. **Level 1 (전체 빈칸)**: 핵심 문장 전체를 쓰게 하거나, 전체에 해당하는 핵심 용어를 묻습니다. (난이도 8)\n"
            "2. **Level 2 (논리 빈칸)**: '왜냐하면', '따라서', '조건' 등 논리적 연결 고리나 인과 관계 부분에 빈칸을 뚫습니다. (난이도 6)\n"
            "3. **Level 3 (용어 빈칸)**: 핵심 수학 용어(명사)에 빈칸을 뚫습니다. (난이도 4)\n"
            "4. **Level 4 (따라쓰기/선택)**: 문장을 거의 다 보여주고 아주 쉬운 조사나 수치를 채우거나, 올바른 문장을 선택하게 합니다. (난이도 2)\n\n"
            "## 출력 형식\n"
            "반드시 아래 JSON 포맷의 **배열**로 출력하세요.\n"
            "[\n"
            "  {\n"
            '    "level": 1,\n'
            '    "question_type": "fill_in_blank",\n'
            '    "content": "문제 지문 (예: 다음 문장을 완성하세요.\\n[핵심문장 변형])",\n'
            '    "correct_answer": "정답",\n'
            '    "explanation": "해설",\n'
            '    "blank_config": {"blank_count": 1, "accept_formats": ["유사답안"]}\n'
            "  },\n"
            "  ... (Level 2, 3, 4)\n"
            "]"
        )

        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2, # 정형화된 출력을 위해 낮음
                    response_mime_type="application/json"
                ),
            )
            
            questions = json.loads(response.text)
            
            result = []
            seq = start_seq
            for q in questions:
                level = q.get("level", 1)
                qid = f"{id_prefix}-fade-L{level}-{seq:03d}" if id_prefix else f"fade-{uuid4().hex[:8]}"
                
                # 난이도 자동 매핑 (L1: 쉬움 -> L4: 어려움)
                # L1(2): 아주 쉬운 조사/수치, L2(4): 용어 빈칸, L3(6): 논리 빈칸, L4(8): 핵심 문장 전체
                difficulty = {1: 2, 2: 4, 3: 6, 4: 8}.get(level, 5)

                q_obj = {
                    "id": qid,
                    "concept_id": concept_id,
                    "category": QuestionCategory.CONCEPT,
                    "part": ProblemPart.CALC, # 임시 (개념에 맞게 수정 필요)
                    "question_type": QuestionType.FILL_IN_BLANK if q.get("question_type") == "fill_in_blank" else QuestionType.MULTIPLE_CHOICE,
                    "difficulty": difficulty,
                    "content": q.get("content", ""),
                    "correct_answer": q.get("correct_answer", ""),
                    "explanation": q.get("explanation", ""),
                    "hint": f"Hint: Level {level} - {key_summary[:10]}...", # 힌트 자동 생성
                    "concept_method": ConceptMethod.GRADUAL_FADING,
                    "fading_level": level,
                    "points": 10,
                    "is_active": True,
                    "options": q.get("options", None),
                    "blank_config": q.get("blank_config", None)
                }
                result.append(q_obj)
                seq += 1

            return result

        except Exception as e:
            logger.exception("Failed to generate gradual fading questions: %s", e)
            return None

    async def generate_error_analysis(
        self,
        concept_name: str,
        concept_id: str,
        grade: str,
        misconceptions: str,
        count: int = 1,
        id_prefix: str = "",
        start_seq: int = 1,
    ) -> list[dict] | None:
        """Type B: 오개념 분석 (Error Analysis) 문항 생성."""
        client = _get_client()
        if not client:
            return None

        prompt = (
            f"당신은 {grade} 수학 교육 전문가입니다.\n"
            f"[개념] {concept_name}\n"
            f"[주요 오개념] {misconceptions}\n\n"
            "학생들이 자주 범하는 오개념을 기반으로 '틀린 풀이 찾기' 또는 '오류 원인 설명하기' 문제를 만드세요.\n"
            "가상의 학생(예: 민수, 지혜)이 문제를 풀다가 실수를 하는 구체적인 상황을 제시하세요.\n\n"
            "## 문제 구성 지침\n"
            "1. **상황 제시**: 어떤 문제를 풀고 있는 상황과, 학생의 잘못된 풀이 과정을 보여즙니다.\n"
            "   - 예: '민수는 32-17을 계산하면서 다음과 같이 풀었습니다.'\n"
            "2. **질문**: 무엇이 잘못되었는지, 왜 그렇게 생각하면 안 되는지를 묻습니다.\n"
            "3. **형식**: 객관식(오류 단계 찾기) 또는 빈칸(올바른 이유 쓰기)으로 출제하세요.\n\n"
            "## 출력 형식\n"
            "반드시 아래 JSON 포맷의 **배열**로 출력하세요.\n"
            "[\n"
            "  {\n"
            '    "question_type": "multiple_choice",\n'
            '    "content": "문제 지문 (잘못된 풀이 포함)",\n'
            '    "options": [{"label":"A", "text":"..."}, ...],\n'
            '    "correct_answer": "A",\n'
            '    "explanation": "해설 (오류 원인 및 올바른 풀이)",\n'
            '    "difficulty": 5\n'
            "  }\n"
            "]"
        )

        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    response_mime_type="application/json"
                ),
            )
            
            questions = json.loads(response.text)
            
            result = []
            seq = start_seq
            for q in questions[:count]:
                qid = f"{id_prefix}-error-{seq:03d}" if id_prefix else f"error-{uuid4().hex[:8]}"
                
                q_obj = {
                    "id": qid,
                    "concept_id": concept_id,
                    "category": QuestionCategory.CONCEPT,
                    "part": ProblemPart.CALC, # 임시
                    "question_type": QuestionType.MULTIPLE_CHOICE if q.get("question_type") == "multiple_choice" else QuestionType.FILL_IN_BLANK,
                    "difficulty": int(q.get("difficulty", 5)),
                    "content": q.get("content", ""),
                    "correct_answer": q.get("correct_answer", ""),
                    "explanation": q.get("explanation", ""),
                    "hint": "Hint: 풀이 과정 중 논리적 비약을 찾아보세요.",
                    "concept_method": ConceptMethod.ERROR_ANALYSIS,
                    "points": 10,
                    "is_active": True,
                    "options": q.get("options", None),
                    "blank_config": q.get("blank_config", None)
                }
                result.append(q_obj)
                seq += 1

            return result

        except Exception as e:
            logger.exception("Failed to generate error analysis questions: %s", e)
            return None

    async def generate_visual_decoding(
        self,
        concept_name: str,
        concept_id: str,
        grade: str,
        core_concepts: str,
        count: int = 1,
        id_prefix: str = "",
        start_seq: int = 1,
    ) -> list[dict] | None:
        """Type C: 시각적 해체 (Visual Decoding) 문항 생성."""
        client = _get_client()
        if not client:
            return None

        prompt = (
            f"당신은 {grade} 수학 교육 전문가입니다.\n"
            f"[개념] {concept_name}\n"
            f"[핵심 내용] {core_concepts}\n\n"
            "복잡한 수식, 그래프, 또는 개념 정의에서 '핵심 부분'을 시각적으로 강조하여 묻는 문제를 만드세요.\n"
            "**강조하고 싶은 부분**은 마크다운 볼드체(**텍스트**)로 감싸주세요.\n"
            "이 강조된 부분은 프론트엔드에서 붉은색이나 하이라이트 처리됩니다.\n\n"
            "## 문제 구성 지침\n"
            "1. **상황 제시**: 공식이나 개념, 도형의 성질 등을 제시합니다.\n"
            "2. **강조**: 핵심이 되는 변수, 연산자, 또는 용어를 **로 감쌉니다.\n"
            "   - 예: '이차방정식 ax^2 + bx + c = 0 에서 **D = b^2 - 4ac**는 무엇을 의미합니까?'\n"
            "3. **질문**: 강조된 부분이 전체 맥락에서 어떤 역할을 하는지 묻습니다.\n"
            "4. **형식**: 객관식(의미 찾기) 또는 빈칸(용어 쓰기).\n\n"
            "## 출력 형식\n"
            "반드시 아래 JSON 포맷의 **배열**로 출력하세요.\n"
            "[\n"
            "  {\n"
            '    "question_type": "multiple_choice",\n'
            '    "content": "문제 지문 (**강조** 포함)",\n'
            '    "options": [{"label":"A", "text":"..."}, ...],\n'
            '    "correct_answer": "A",\n'
            '    "explanation": "해설",\n'
            '    "difficulty": 3\n'
            "  }\n"
            "]"
        )

        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    response_mime_type="application/json"
                ),
            )
            
            questions = json.loads(response.text)
            
            result = []
            seq = start_seq
            for q in questions[:count]:
                qid = f"{id_prefix}-visual-{seq:03d}" if id_prefix else f"visual-{uuid4().hex[:8]}"
                
                q_obj = {
                    "id": qid,
                    "concept_id": concept_id,
                    "category": QuestionCategory.CONCEPT,
                    "part": ProblemPart.CALC, # 임시
                    "question_type": QuestionType.MULTIPLE_CHOICE if q.get("question_type") == "multiple_choice" else QuestionType.FILL_IN_BLANK,
                    "difficulty": int(q.get("difficulty", 3)),
                    "content": q.get("content", ""),
                    "correct_answer": q.get("correct_answer", ""),
                    "explanation": q.get("explanation", ""),
                    "hint": "Hint: 붉게 표시된 부분의 역할에 주목하세요.",
                    "concept_method": ConceptMethod.VISUAL_DECODING,
                    "points": 10,
                    "is_active": True,
                    "options": q.get("options", None),
                    "blank_config": q.get("blank_config", None)
                }
                result.append(q_obj)
                seq += 1

            return result

        except Exception as e:
            logger.exception("Failed to generate visual decoding questions: %s", e)
            return None
