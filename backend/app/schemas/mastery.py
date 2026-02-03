"""개념 숙련도 및 단원 진행 스키마."""

from datetime import datetime
from pydantic import BaseModel


class ConceptMasteryResponse(BaseModel):
    """개념 숙련도 응답."""

    concept_id: str
    concept_name: str
    mastery_percentage: int
    is_mastered: bool
    is_unlocked: bool
    total_attempts: int
    correct_count: int
    average_score: float
    last_practiced: datetime | None


class ChapterProgressResponse(BaseModel):
    """단원 진행 상황 응답."""

    chapter_id: str
    chapter_number: int
    name: str
    description: str
    is_unlocked: bool
    overall_progress: int
    is_completed: bool
    final_test_score: int | None
    teacher_approved: bool


class ChapterDetailResponse(BaseModel):
    """단원 상세 정보."""

    chapter_id: str
    overall_progress: int
    concepts_mastery: dict[str, int]
    mastered_count: int
    total_concepts: int
    final_test_passed: bool
    final_test_score: int | None
    teacher_approved: bool
    is_completed: bool


class RecommendationResponse(BaseModel):
    """학습 추천."""

    type: str  # "continue" | "next"
    chapter_id: str
    chapter_name: str
    progress: int | None = None
    message: str


class ApprovalRequest(BaseModel):
    """선생님 승인 요청."""

    student_id: str
    feedback: str | None = None
