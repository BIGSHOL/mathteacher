"""공통 스키마 정의."""

from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel


class UserRole(str, Enum):
    """사용자 역할."""

    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


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


class Difficulty(str, Enum):
    """난이도."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


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
