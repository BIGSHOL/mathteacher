"""Gemini AI 학습 보조 API - 힌트, 유연 채점, 피드백."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from google import genai
from google.genai import types

from app.core.config import settings

router = APIRouter(prefix="/ai", tags=["ai-assist"])

# ─────────────────────────────────────────────
# Gemini 클라이언트 (싱글턴)
# ─────────────────────────────────────────────
_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GEMINI_API_KEY가 설정되지 않았습니다.",
        )
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


# ─────────────────────────────────────────────
# 1. 힌트 생성
# ─────────────────────────────────────────────
class HintRequest(BaseModel):
    question_content: str = Field(..., description="문제 내용")
    question_type: str = Field(..., description="multiple_choice 또는 fill_in_blank")
    options: list[str] | None = Field(None, description="객관식 선지 (MC만)")
    student_grade: str = Field(..., description="학년 (예: middle_1)")
    hint_level: int = Field(1, ge=1, le=3, description="힌트 수준 1~3 (클수록 구체적)")


class HintResponse(BaseModel):
    hint: str
    hint_level: int


@router.post("/hint", response_model=HintResponse)
async def generate_hint(req: HintRequest):
    """학생에게 단계별 힌트를 제공합니다. 정답은 절대 노출하지 않습니다."""
    client = _get_client()

    grade_label = {
        "elementary_3": "초3", "elementary_4": "초4",
        "elementary_5": "초5", "elementary_6": "초6",
        "middle_1": "중1", "middle_2": "중2", "middle_3": "중3",
        "high_1": "고1",
    }.get(req.student_grade, req.student_grade)

    level_desc = {
        1: "풀이 방향만 가볍게 안내. 구체적인 숫자나 공식은 제시하지 마세요.",
        2: "관련 개념과 공식을 알려주되, 핵심 계산 단계는 비워두세요.",
        3: "풀이 과정을 거의 다 안내하되, 마지막 답만 빈칸으로 남기세요.",
    }

    prompt = (
        f"당신은 {grade_label} 학생을 위한 수학 튜터입니다.\n"
        f"학생이 아래 문제를 풀다가 막혔습니다. 힌트 레벨 {req.hint_level}에 맞춰 도움을 주세요.\n\n"
        f"[힌트 레벨 설명]\n{level_desc[req.hint_level]}\n\n"
        f"[문제]\n{req.question_content}\n"
    )
    if req.options:
        prompt += f"[선지] {', '.join(req.options)}\n"
    prompt += "\n절대 정답을 직접 알려주지 마세요. 한국어로 2~4문장, 친절하게 답하세요."

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.4, max_output_tokens=300),
    )

    return HintResponse(hint=response.text.strip(), hint_level=req.hint_level)


# ─────────────────────────────────────────────
# 2. 유연 채점 (빈칸 채우기)
# ─────────────────────────────────────────────
class GradeRequest(BaseModel):
    question_content: str = Field(..., description="문제 내용")
    correct_answer: str = Field(..., description="정답")
    student_answer: str = Field(..., description="학생 답안")
    accept_formats: list[str] | None = Field(None, description="허용 표기 목록")


class GradeResponse(BaseModel):
    is_correct: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str


@router.post("/grade-fill-blank", response_model=GradeResponse)
async def grade_fill_blank(req: GradeRequest):
    """빈칸 채우기 답안을 유연하게 채점합니다. 표기 차이(3/4 vs 0.75)를 허용합니다."""

    # 1단계: 규칙 기반 매칭 (빠름)
    student = req.student_answer.strip().replace(" ", "")
    correct = req.correct_answer.strip().replace(" ", "")

    if student == correct:
        return GradeResponse(is_correct=True, confidence=1.0, reason="정확히 일치")

    accept = [a.strip().replace(" ", "") for a in (req.accept_formats or [])]
    if student in accept:
        return GradeResponse(is_correct=True, confidence=1.0, reason="허용 표기와 일치")

    # 2단계: Gemini 유연 채점
    client = _get_client()

    prompt = (
        "수학 문제의 빈칸 채우기 답안을 채점하세요.\n\n"
        f"[문제] {req.question_content}\n"
        f"[정답] {req.correct_answer}\n"
        f"[학생 답] {req.student_answer}\n\n"
        "다음 기준으로 판단하세요:\n"
        "- 동치인 수학적 표현은 정답 (예: 3/4 = 0.75, -3 = -3.0)\n"
        "- 단위 표기 차이는 정답 (예: 5cm = 5 cm)\n"
        "- 약분/통분 결과가 같으면 정답\n"
        "- 수학적으로 다른 값이면 오답\n\n"
        "반드시 아래 JSON 형식으로만 답하세요:\n"
        '{"is_correct": true/false, "confidence": 0.0~1.0, "reason": "판단 근거"}'
    )

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=200),
    )

    import json
    try:
        text = response.text.strip()
        # JSON 블록 추출
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        result = json.loads(text)
        return GradeResponse(
            is_correct=bool(result.get("is_correct", False)),
            confidence=float(result.get("confidence", 0.5)),
            reason=str(result.get("reason", "")),
        )
    except (json.JSONDecodeError, KeyError, ValueError):
        # 파싱 실패 시 보수적으로 오답 처리
        return GradeResponse(
            is_correct=False,
            confidence=0.3,
            reason="AI 응답 파싱 실패. 수동 확인이 필요합니다.",
        )


# ─────────────────────────────────────────────
# 3. 맞춤 피드백
# ─────────────────────────────────────────────
class FeedbackRequest(BaseModel):
    question_content: str = Field(..., description="문제 내용")
    correct_answer: str = Field(..., description="정답")
    student_answer: str = Field(..., description="학생 답안")
    explanation: str = Field("", description="문제 해설")
    student_grade: str = Field(..., description="학년")


class FeedbackResponse(BaseModel):
    feedback: str
    error_type: str = Field("", description="오류 유형 (예: 부호 오류, 개념 혼동)")
    suggestion: str = Field("", description="학습 제안")


@router.post("/feedback", response_model=FeedbackResponse)
async def generate_feedback(req: FeedbackRequest):
    """학생의 오답에 대해 맞춤 피드백을 생성합니다."""
    client = _get_client()

    grade_label = {
        "elementary_3": "초3", "elementary_4": "초4",
        "elementary_5": "초5", "elementary_6": "초6",
        "middle_1": "중1", "middle_2": "중2", "middle_3": "중3",
        "high_1": "고1",
    }.get(req.student_grade, req.student_grade)

    prompt = (
        f"당신은 {grade_label} 학생의 수학 오답을 분석하는 전문 튜터입니다.\n\n"
        f"[문제] {req.question_content}\n"
        f"[정답] {req.correct_answer}\n"
        f"[학생 답] {req.student_answer}\n"
    )
    if req.explanation:
        prompt += f"[해설] {req.explanation}\n"

    prompt += (
        "\n학생이 왜 틀렸는지 분석하고, 아래 JSON 형식으로 답하세요:\n"
        "{\n"
        '  "feedback": "학생 눈높이에 맞는 친절한 설명 (2~4문장)",\n'
        '  "error_type": "오류 유형 (예: 부호 오류, 계산 실수, 개념 혼동, 문제 이해 부족)",\n'
        '  "suggestion": "보완 학습 제안 (1~2문장)"\n'
        "}\n"
        "반드시 JSON만 출력하세요."
    )

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=400),
    )

    import json
    try:
        text = response.text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        result = json.loads(text)
        return FeedbackResponse(
            feedback=str(result.get("feedback", "")),
            error_type=str(result.get("error_type", "")),
            suggestion=str(result.get("suggestion", "")),
        )
    except (json.JSONDecodeError, KeyError, ValueError):
        return FeedbackResponse(
            feedback=f"정답은 {req.correct_answer}입니다. {req.explanation}",
            error_type="분석 불가",
            suggestion="해설을 다시 읽어보세요.",
        )
