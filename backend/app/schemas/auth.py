"""인증 스키마 정의."""

from datetime import datetime

from pydantic import BaseModel, Field

from .common import Grade, UserRole


# ===========================
# 사용자 스키마
# ===========================


class UserBase(BaseModel):
    """사용자 기본 스키마."""

    login_id: str = Field(..., min_length=4, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole


class UserCreate(UserBase):
    """사용자 생성 스키마."""

    password: str = Field(..., min_length=6, max_length=100)
    grade: Grade | None = None
    class_id: str | None = None


class UserUpdate(BaseModel):
    """사용자 수정 스키마."""

    name: str | None = Field(None, min_length=1, max_length=100)
    grade: Grade | None = None
    class_id: str | None = None
    is_active: bool | None = None
    teacher_memo: str | None = None


class UserResponse(UserBase):
    """사용자 응답 스키마."""

    id: str
    grade: Grade | None = None
    class_id: str | None = None
    level: int = 1
    total_xp: int = 0
    current_streak: int = 0
    teacher_memo: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===========================
# 로그인 스키마
# ===========================


class LoginRequest(BaseModel):
    """로그인 요청."""

    login_id: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    """로그인 응답."""

    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# ===========================
# 토큰 스키마
# ===========================


class TokenRefreshRequest(BaseModel):
    """토큰 갱신 요청."""

    refresh_token: str


class TokenRefreshResponse(BaseModel):
    """토큰 갱신 응답."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class LogoutRequest(BaseModel):
    """로그아웃 요청."""

    refresh_token: str


class LogoutResponse(BaseModel):
    """로그아웃 응답."""

    message: str


# ===========================
# 회원가입 스키마
# ===========================


class RegisterRequest(BaseModel):
    """계정 등록 요청 (역할 통합)."""

    login_id: str = Field(..., min_length=4, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=6, max_length=100)
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole
    grade: Grade | None = None
    class_id: str | None = None


# 하위호환용 별칭
RegisterStudentRequest = RegisterRequest
RegisterTeacherRequest = RegisterRequest
RegisterAdminRequest = RegisterRequest


class UpdateUserRequest(BaseModel):
    """계정 수정 요청."""

    name: str | None = Field(None, min_length=1, max_length=100)
    password: str | None = Field(None, min_length=6, max_length=100)
    role: UserRole | None = None
    grade: Grade | None = None
    class_id: str | None = None
    is_active: bool | None = None


class RegisterResponse(BaseModel):
    """회원가입 응답."""

    user: UserResponse
    message: str
