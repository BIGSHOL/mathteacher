"""공통 스키마 정의."""

from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel


class UserRole(str, Enum):
    """사용자 역할."""

    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    MASTER = "master"


class Grade(str, Enum):
    """학년."""

    ELEMENTARY_1 = "elementary_1"
    ELEMENTARY_2 = "elementary_2"
    ELEMENTARY_3 = "elementary_3"
    ELEMENTARY_4 = "elementary_4"
    ELEMENTARY_5 = "elementary_5"
    ELEMENTARY_6 = "elementary_6"
    MIDDLE_1 = "middle_1"
    MIDDLE_2 = "middle_2"
    MIDDLE_3 = "middle_3"
    HIGH_1 = "high_1"


class QuestionType(str, Enum):
    """문제 유형."""

    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    FILL_IN_BLANK = "fill_in_blank"  # 빈칸 채우기


class QuestionCategory(str, Enum):
    """문제 카테고리 (트랙)."""

    COMPUTATION = "computation"  # 연산
    CONCEPT = "concept"  # 개념
    FILL_IN_BLANK = "fill_in_blank"  # 빈칸


class ConceptMethod(str, Enum):
    """개념 문항 생성 방식 (Sub-type)."""

    GRADUAL_FADING = "gradual_fading"   # TYPE A: 점진적 빈칸 소거
    ERROR_ANALYSIS = "error_analysis"   # TYPE B: 오개념 분석 (틀린 곳 찾기)
    VISUAL_DECODING = "visual_decoding" # TYPE C: 시각적 해체 (확대/강조)
    STANDARD = "standard"               # 일반 개념 문항


class ProblemPart(str, Enum):
    """문제 파트 (6개 영역).

    문제의 내용 영역을 분류합니다.
    각 문제는 하나의 파트에 속하며,
    파트별로 문제 출제/보충/분석이 가능합니다.
    """

    CALC = "calc"          # 계산 (순수 연산)
    ALGEBRA = "algebra"    # 대수 (방정식, 부등식, 문자식)
    FUNC = "func"          # 함수 (함수, 그래프, 좌표)
    GEO = "geo"            # 도형 (기하, 측정, 공간)
    DATA = "data"          # 자료 (통계, 확률, 표/그래프 해석)
    WORD = "word"          # 문장제 (실생활 응용, 서술형)


class Difficulty(int, Enum):
    """난이도 (10단계, 학년 내 상대 난이도).

    각 학년(초1~공통수학1) × 각 트랙(연산/개념) 내에서
    Lv.1(가장 쉬움) ~ Lv.10(가장 어려움)으로 운영.
    """

    LV1 = 1
    LV2 = 2
    LV3 = 3
    LV4 = 4
    LV5 = 5
    LV6 = 6
    LV7 = 7
    LV8 = 8
    LV9 = 9
    LV10 = 10


class ReportType(str, Enum):
    """문제 신고 유형."""

    WRONG_ANSWER = "wrong_answer"      # 정답 오류
    WRONG_OPTIONS = "wrong_options"    # 보기 오류
    QUESTION_ERROR = "question_error"  # 문제 오류
    OTHER = "other"                    # 기타


class ReportStatus(str, Enum):
    """문제 신고 처리 상태."""

    PENDING = "pending"      # 대기
    RESOLVED = "resolved"    # 처리 완료
    DISMISSED = "dismissed"  # 반려


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """API 성공 응답."""

    success: bool = True
    data: T
    message: str | None = None


class ErrorDetail(BaseModel):
    """에러 상세."""

    code: str
    message: str
    details: dict[str, list[str]] | None = None


class ErrorResponse(BaseModel):
    """API 에러 응답."""

    success: bool = False
    error: ErrorDetail


class PaginatedResponse(BaseModel, Generic[T]):
    """페이지네이션 응답."""

    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
