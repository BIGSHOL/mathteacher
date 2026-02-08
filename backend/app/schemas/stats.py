"""통계 스키마 정의."""

from datetime import datetime

from pydantic import BaseModel, Field

from .common import Grade


# ===========================
# 업적 스키마
# ===========================


class Achievement(BaseModel):
    """획득한 업적."""

    id: str  # achievement_type
    name: str
    description: str
    icon: str
    earned_at: datetime

    earned_at: datetime


# ===========================
# 랭킹 스키마
# ===========================


class RankingItem(BaseModel):
    """랭킹 항목."""

    rank: int
    user_id: str
    name: str
    level: int
    total_xp: int
    grade: str | None


# ===========================
# 개념 통계 스키마
# ===========================


class ConceptStat(BaseModel):
    """개념별 통계."""

    concept_id: str
    concept_name: str
    total_questions: int
    correct_count: int
    accuracy_rate: float


class ConceptDetailStat(ConceptStat):
    """개념 상세 통계."""

    grade: Grade
    student_count: int
    average_time_seconds: float
    difficulty_distribution: dict[str, int]


# ===========================
# 학생 통계 스키마
# ===========================


class TrackStats(BaseModel):
    """트랙별 통계 (연산/개념/유형)."""

    total_questions: int
    correct_answers: int
    accuracy_rate: float
    average_time: float = 0


class ReviewStatsInfo(BaseModel):
    """오답 복습 현황."""

    pending_count: int = 0      # 복습 대기 (오늘 이전)
    in_progress_count: int = 0  # 진행 중 (아직 졸업 안 함)
    graduated_count: int = 0    # 졸업 완료


class QuotaProgress(BaseModel):
    """일일 할당량 진행 상황."""

    daily_quota: int
    correct_today: int
    quota_remaining: int
    accumulated_quota: int
    quota_met: bool
    carry_over: bool


class RecentTest(BaseModel):
    """최근 테스트."""

    test_id: str
    test_title: str
    score: int
    max_score: int
    accuracy_rate: float
    completed_at: datetime


class DailyActivity(BaseModel):
    """일별 활동."""

    date: str
    tests_completed: int
    questions_answered: int
    accuracy_rate: float


class StudentStats(BaseModel):
    """학생 통계."""

    user_id: str
    total_tests: int
    total_questions: int
    correct_answers: int
    accuracy_rate: float
    average_time_per_question: float
    current_streak: int
    max_streak: int
    level: int
    total_xp: int
    today_solved: int
    weak_concepts: list[ConceptStat]
    strong_concepts: list[ConceptStat]
    computation_stats: TrackStats | None = None
    concept_stats: TrackStats | None = None
    type_stats: dict[str, TrackStats] = {}
    daily_activity: list[DailyActivity] = []
    recent_tests: list[RecentTest] = []
    review_stats: ReviewStatsInfo | None = None
    quota: QuotaProgress | None = None


class StudentStatsSummary(BaseModel):
    """학생 통계 요약 (목록용)."""

    user_id: str
    name: str
    grade: Grade
    class_name: str
    level: int
    total_xp: int
    accuracy_rate: float
    tests_completed: int
    current_streak: int
    last_activity_at: datetime | None


class ChapterProgressStat(BaseModel):
    """단원별 진행 통계."""

    chapter_id: str
    chapter_name: str
    chapter_number: int
    is_unlocked: bool = False
    is_completed: bool = False
    overall_progress: int = 0
    concepts_mastery: dict[str, int] = {}  # concept_name → mastery %


class StudentDetailStats(StudentStats):
    """학생 상세 통계."""

    name: str
    login_id: str
    grade: Grade
    class_name: str
    recent_tests: list[RecentTest]
    daily_activity: list[DailyActivity]
    chapter_progress: list[ChapterProgressStat] = []


# ===========================
# 반 통계 스키마
# ===========================


class ClassStats(BaseModel):
    """반 통계."""

    class_id: str
    student_count: int
    average_accuracy: float
    average_level: float
    tests_completed_today: int
    weak_concepts: list[ConceptStat]


class TopStudent(BaseModel):
    """상위 학생."""

    user_id: str
    name: str
    level: int
    accuracy_rate: float


class DailyClassStat(BaseModel):
    """일별 반 통계."""

    date: str
    active_students: int
    tests_completed: int
    average_accuracy: float


class ClassDetailStats(ClassStats):
    """반 상세 통계."""

    class_name: str
    teacher_name: str
    grade: Grade
    top_students: list[TopStudent]
    concept_stats: list[ConceptStat]
    daily_stats: list[DailyClassStat]


# ===========================
# 대시보드 스키마
# ===========================


class TodayStats(BaseModel):
    """오늘 통계."""

    active_students: int
    tests_completed: int
    questions_answered: int
    average_accuracy: float


class WeekStats(BaseModel):
    """이번주 통계."""

    active_students: int
    tests_completed: int
    accuracy_trend: list[float]  # 7일간 정답률


class DashboardAlert(BaseModel):
    """대시보드 알림."""

    type: str  # low_accuracy, inactive, struggling
    student_id: str
    student_name: str
    message: str


class DashboardStats(BaseModel):
    """대시보드 통계."""

    today: TodayStats
    this_week: WeekStats
    alerts: list[DashboardAlert]


# ===========================
# 할당량 설정 스키마
# ===========================


class QuotaUpdateRequest(BaseModel):
    """반 할당량 설정 요청."""

    daily_quota: int = Field(ge=1, le=100, description="일일 목표 정답 수")
    quota_carry_over: bool = Field(description="미달성 할당량 이월 여부")


class StudentQuotaStatus(BaseModel):
    """학생별 할당량 상태 (강사 조회용)."""

    student_id: str
    student_name: str
    correct_today: int
    daily_quota: int
    accumulated_quota: int
    quota_met: bool
