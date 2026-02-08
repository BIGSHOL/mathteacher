"""일일 테스트 스키마."""

from datetime import datetime

from pydantic import BaseModel


CATEGORY_LABELS = {
    "concept": "개념",
    "computation": "연산",
    "fill_in_blank": "빈칸",
}


class DailyTestRecordResponse(BaseModel):
    """일일 테스트 기록 응답."""

    id: str
    date: str
    category: str
    category_label: str
    status: str
    test_id: str
    attempt_id: str | None = None
    score: int | None = None
    max_score: int | None = None
    correct_count: int | None = None
    total_count: int | None = None
    completed_at: datetime | None = None
    question_count: int

    model_config = {"from_attributes": True}


class DailyTestTodayResponse(BaseModel):
    """오늘의 일일 테스트 응답."""

    date: str
    tests: list[DailyTestRecordResponse]
    ai_generated_count: int = 0
    weak_concept_count: int = 0


class DailyTestStartResponse(BaseModel):
    """일일 테스트 시작 응답."""

    attempt_id: str
