"""테스트 스키마 정의."""

from datetime import datetime

from pydantic import BaseModel, Field

from .common import Difficulty, Grade, QuestionType


# ===========================
# 개념 스키마
# ===========================


class ConceptBase(BaseModel):
    """개념 기본 스키마."""

    name: str = Field(..., min_length=1, max_length=200)
    grade: Grade
    description: str = ""


class ConceptCreate(ConceptBase):
    """개념 생성 스키마."""

    parent_id: str | None = None


class ConceptResponse(ConceptBase):
    """개념 응답 스키마."""

    id: str
    parent_id: str | None = None

    model_config = {"from_attributes": True}


# ===========================
# 문제 스키마
# ===========================


class QuestionOption(BaseModel):
    """문제 선택지."""

    id: str
    label: str  # A, B, C, D
    text: str


class QuestionBase(BaseModel):
    """문제 기본 스키마."""

    question_type: QuestionType
    difficulty: Difficulty
    content: str = Field(..., min_length=1)
    explanation: str = ""
    points: int = Field(default=10, ge=1, le=100)


class QuestionCreate(QuestionBase):
    """문제 생성 스키마."""

    concept_id: str
    options: list[QuestionOption] | None = None
    correct_answer: str


class QuestionResponse(QuestionBase):
    """문제 응답 스키마 (학생용 - 정답 제외)."""

    id: str
    concept_id: str
    options: list[QuestionOption] | None = None

    model_config = {"from_attributes": True}


class QuestionWithAnswer(QuestionResponse):
    """문제 응답 스키마 (정답 포함)."""

    correct_answer: str


# ===========================
# 테스트 스키마
# ===========================


class TestBase(BaseModel):
    """테스트 기본 스키마."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    grade: Grade
    time_limit_minutes: int | None = None


class TestCreate(TestBase):
    """테스트 생성 스키마."""

    concept_ids: list[str]
    question_ids: list[str]


class TestUpdate(BaseModel):
    """테스트 수정 스키마."""

    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    is_active: bool | None = None
    question_ids: list[str] | None = None


class TestResponse(TestBase):
    """테스트 응답 스키마."""

    id: str
    concept_ids: list[str]
    question_count: int
    is_active: bool = True
    created_at: datetime

    model_config = {"from_attributes": True}


class AvailableTestResponse(TestResponse):
    """풀 수 있는 테스트 응답."""

    is_completed: bool = False
    best_score: int | None = None
    attempt_count: int = 0


class TestWithQuestionsResponse(TestResponse):
    """문제 포함 테스트 응답."""

    questions: list[QuestionResponse]


# ===========================
# 테스트 시도 스키마
# ===========================


class TestAttemptBase(BaseModel):
    """테스트 시도 기본 스키마."""

    test_id: str
    student_id: str


class TestAttemptResponse(TestAttemptBase):
    """테스트 시도 응답."""

    id: str
    started_at: datetime
    completed_at: datetime | None = None
    score: int = 0
    max_score: int = 0
    correct_count: int = 0
    total_count: int = 0
    xp_earned: int = 0
    combo_max: int = 0

    model_config = {"from_attributes": True}


class StartTestResponse(BaseModel):
    """테스트 시작 응답."""

    attempt_id: str
    test: TestWithQuestionsResponse
    started_at: datetime


# ===========================
# 답안 제출 스키마
# ===========================


class SubmitAnswerRequest(BaseModel):
    """답안 제출 요청."""

    question_id: str
    selected_answer: str
    time_spent_seconds: int = Field(..., ge=0)


class SubmitAnswerResponse(BaseModel):
    """답안 제출 응답."""

    is_correct: bool
    correct_answer: str
    explanation: str
    points_earned: int
    combo_count: int
    xp_earned: int
    current_score: int
    questions_remaining: int


class AnswerLogResponse(BaseModel):
    """답안 기록 응답."""

    id: str
    attempt_id: str
    question_id: str
    selected_answer: str
    is_correct: bool
    time_spent_seconds: int
    combo_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# 테스트 완료 스키마
# ===========================


class CompleteTestResponse(BaseModel):
    """테스트 완료 응답."""

    attempt: TestAttemptResponse
    answers: list[AnswerLogResponse]
    level_up: bool = False
    new_level: int | None = None
    xp_earned: int
    achievements_earned: list[str] = []


class GetAttemptResponse(BaseModel):
    """시도 결과 조회 응답."""

    attempt: TestAttemptResponse
    answers: list[AnswerLogResponse]
    test: TestResponse
