"""테스트 스키마 정의."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from .common import Difficulty, Grade, ProblemPart, QuestionCategory, QuestionType


# ===========================
# 개념 스키마
# ===========================


class ConceptBase(BaseModel):
    """개념 기본 스키마."""

    name: str = Field(..., min_length=1, max_length=200)
    grade: Grade
    category: QuestionCategory = QuestionCategory.CONCEPT
    part: ProblemPart = ProblemPart.CALC
    description: str = ""


class ConceptCreate(ConceptBase):
    """개념 생성 스키마."""

    parent_id: str | None = None


class ConceptResponse(ConceptBase):
    """개념 응답 스키마."""

    id: str
    parent_id: str | None = None
    prerequisite_ids: list[str] = []

    model_config = {"from_attributes": True}


# ===========================
# 문제 스키마
# ===========================


class QuestionOption(BaseModel):
    """문제 선택지."""

    id: str
    label: str  # A, B, C, D
    text: str

    @field_validator("text", mode="before")
    @classmethod
    def coerce_text(cls, v):
        """시드 데이터에서 tuple/list로 저장된 text를 문자열로 변환."""
        if isinstance(v, (list, tuple)):
            return v[0] if v else ""
        return v


class QuestionBase(BaseModel):
    """문제 기본 스키마."""

    category: QuestionCategory
    part: ProblemPart
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
    prerequisite_concept_ids: list[str] | None = None


class QuestionResponse(QuestionBase):
    """문제 응답 스키마 (학생용 - 정답 제외)."""

    id: str
    concept_id: str
    concept_name: str = ""
    grade: str | None = None
    chapter_name: str | None = None
    options: list[QuestionOption] | None = None
    prerequisite_concept_ids: list[str] | None = None
    blank_config: dict | None = None
    correct_answer: str | None = None

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
    category: str | None = None  # computation, concept, fill_in_blank, 또는 None(종합)
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
    is_adaptive: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}


class AvailableTestResponse(TestResponse):
    """풀 수 있는 테스트 응답."""

    is_completed: bool = False
    best_score: int | None = None
    attempt_count: int = 0
    difficulty: int = 5  # 문제 평균 난이도 (1~10)


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
    is_adaptive: bool = False
    current_difficulty: int | None = None

    model_config = {"from_attributes": True}


class StartTestResponse(BaseModel):
    """테스트 시작 응답."""

    attempt_id: str
    test: TestWithQuestionsResponse
    started_at: datetime
    is_adaptive: bool = False
    current_difficulty: int | None = None


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
    next_difficulty: int | None = None
    error_type: str = ""
    suggestion: str = ""
    # 재도전 관련 필드 (일일 테스트용)
    retry_scheduled: bool | None = None  # 재도전 예정 여부
    retry_count: int | None = None  # 이 문제에서 틀린 횟수
    retry_queue_count: int | None = None  # 재도전 대기 문제 수
    hint: dict | None = None  # 재도전 힌트 정보
    moved_to_focus_check: bool | None = None  # 집중 체크로 이동 여부
    focus_check_message: str | None = None  # 집중 체크 안내 메시지


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


class AchievementEarned(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    earned_at: datetime


class CompleteTestResponse(BaseModel):
    """테스트 완료 응답."""

    attempt: TestAttemptResponse
    answers: list[AnswerLogResponse]
    level_up: bool = False
    level_down: bool = False
    new_level: int | None = None
    xp_earned: int
    total_xp: int | None = None
    current_streak: int | None = None
    achievements_earned: list[AchievementEarned] = []
    # 레벨다운 방어 시스템
    level_down_defense: int | None = None
    level_down_action: str | None = None  # none / defense_consumed / defense_restored / level_down


class GetAttemptResponse(BaseModel):
    """시도 결과 조회 응답."""

    attempt: TestAttemptResponse
    answers: list[AnswerLogResponse]
    test: TestWithQuestionsResponse


class WrongQuestionItem(BaseModel):
    """오답 문제 항목."""

    question: QuestionWithAnswer
    wrong_count: int
    last_selected_answer: str
    last_attempted_at: datetime


class ReviewResponse(BaseModel):
    """복습 오답 목록 응답."""

    items: list[WrongQuestionItem]
    total: int


# ===========================
# 적응형 테스트 스키마
# ===========================


class NextQuestionResponse(BaseModel):
    """적응형 다음 문제 응답."""

    question: QuestionResponse | None = None
    current_difficulty: int
    questions_answered: int
    questions_remaining: int
    is_complete: bool = False
