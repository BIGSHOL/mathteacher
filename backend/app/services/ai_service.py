"""AI 보조 서비스 (Gemini) - 힌트, 유연 채점, 피드백."""

import json
import logging

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
