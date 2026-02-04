"""Gemini AI 학습 보조 API - 힌트, 유연 채점, 피드백."""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from app.core.config import settings
from app.api.v1.auth import get_current_user, limiter
from app.schemas.auth import UserResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai-assist"])

_ai_service = AIService()


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
@limiter.limit("30/minute")
async def generate_hint(
    request: Request,
    req: HintRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """학생에게 단계별 힌트를 제공합니다. 정답은 절대 노출하지 않습니다."""
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI 서비스가 설정되지 않았습니다.",
        )

    result = await _ai_service.generate_hint(
        question_content=req.question_content,
        question_type=req.question_type,
        options=req.options,
        student_grade=req.student_grade,
        hint_level=req.hint_level,
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="힌트 생성에 실패했습니다.",
        )
    return HintResponse(**result)


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
@limiter.limit("20/minute")
async def grade_fill_blank(
    request: Request,
    req: GradeRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """빈칸 채우기 답안을 유연하게 채점합니다. 표기 차이(3/4 vs 0.75)를 허용합니다."""
    result = await _ai_service.grade_fill_blank(
        question_content=req.question_content,
        correct_answer=req.correct_answer,
        student_answer=req.student_answer,
        accept_formats=req.accept_formats,
    )
    if not result:
        return GradeResponse(
            is_correct=False,
            confidence=0.3,
            reason="AI 서비스를 사용할 수 없습니다.",
        )
    return GradeResponse(**result)


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
@limiter.limit("30/minute")
async def generate_feedback(
    request: Request,
    req: FeedbackRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """학생의 오답에 대해 맞춤 피드백을 생성합니다."""
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI 서비스가 설정되지 않았습니다.",
        )

    result = await _ai_service.generate_feedback(
        question_content=req.question_content,
        correct_answer=req.correct_answer,
        student_answer=req.student_answer,
        explanation=req.explanation,
        student_grade=req.student_grade,
    )
    if not result:
        return FeedbackResponse(
            feedback=f"정답은 {req.correct_answer}입니다. {req.explanation}",
            error_type="분석 불가",
            suggestion="해설을 다시 읽어보세요.",
        )
    return FeedbackResponse(**result)
