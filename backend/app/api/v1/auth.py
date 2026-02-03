"""인증 API 엔드포인트."""

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.schemas import (
    ApiResponse,
    ErrorResponse,
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    LogoutResponse,
    RegisterAdminRequest,
    RegisterStudentRequest,
    RegisterTeacherRequest,
    RegisterResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
    UserCreate,
    UserResponse,
)
from app.schemas.common import UserRole
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)

# 쿠키 설정 상수
REFRESH_TOKEN_COOKIE_NAME = "refresh_token"
REFRESH_TOKEN_MAX_AGE = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60  # seconds


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """인증 서비스 의존성."""
    return AuthService(db)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """현재 사용자 조회."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "인증이 필요합니다.",
                },
            },
        )

    payload = auth_service.verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "유효하지 않은 토큰입니다.",
                },
            },
        )

    user = auth_service.get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "USER_NOT_FOUND",
                    "message": "사용자를 찾을 수 없습니다.",
                },
            },
        )

    return UserResponse.model_validate(user)


def require_role(*roles: UserRole):
    """역할 권한 검증 의존성."""

    def role_checker(current_user: UserResponse = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "error": {
                        "code": "FORBIDDEN",
                        "message": "권한이 없습니다.",
                    },
                },
            )
        return current_user

    return role_checker


@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(
    request: LoginRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    """로그인."""
    user = auth_service.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "이메일 또는 비밀번호가 올바르지 않습니다.",
                },
            },
        )

    access_token = auth_service.create_access_token(user.id)
    refresh_token = auth_service.create_refresh_token(user.id)

    # 리프레시 토큰 저장
    auth_service.save_refresh_token(user.id, refresh_token)

    # HttpOnly 쿠키로 refresh token 설정 (XSS 방지)
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        max_age=REFRESH_TOKEN_MAX_AGE,
        httponly=True,  # JavaScript 접근 불가
        secure=settings.ENV != "development",  # HTTPS only in production
        samesite="lax",  # CSRF 방지
        path="/api/v1/auth",  # 인증 API 경로에서만 전송
    )

    return ApiResponse(
        data=LoginResponse(
            user=UserResponse.model_validate(user),
            access_token=access_token,
            refresh_token="",  # 쿠키로 전송되므로 응답 body에서 제거
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
    )


@router.post("/refresh", response_model=ApiResponse[TokenRefreshResponse])
async def refresh_token(
    response: Response,
    refresh_token_cookie: str | None = Cookie(default=None, alias=REFRESH_TOKEN_COOKIE_NAME),
    auth_service: AuthService = Depends(get_auth_service),
):
    """토큰 갱신 (HttpOnly 쿠키에서 refresh token 읽기)."""
    # 쿠키에서 refresh token 확인
    if not refresh_token_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "리프레시 토큰이 없습니다.",
                },
            },
        )

    # 기존 토큰 검증
    stored_token = auth_service.get_refresh_token(refresh_token_cookie)
    if not stored_token:
        # 무효한 토큰이면 쿠키 삭제
        response.delete_cookie(key=REFRESH_TOKEN_COOKIE_NAME, path="/api/v1/auth")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "유효하지 않은 토큰입니다.",
                },
            },
        )

    # 토큰 페이로드 검증
    payload = auth_service.verify_token(refresh_token_cookie)
    if not payload:
        response.delete_cookie(key=REFRESH_TOKEN_COOKIE_NAME, path="/api/v1/auth")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "유효하지 않은 토큰입니다.",
                },
            },
        )

    user_id = payload["sub"]

    # 기존 토큰 무효화
    auth_service.revoke_refresh_token(refresh_token_cookie)

    # 새 토큰 발급
    new_access_token = auth_service.create_access_token(user_id)
    new_refresh_token = auth_service.create_refresh_token(user_id)
    auth_service.save_refresh_token(user_id, new_refresh_token)

    # 새 refresh token을 HttpOnly 쿠키로 설정
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=new_refresh_token,
        max_age=REFRESH_TOKEN_MAX_AGE,
        httponly=True,
        secure=settings.ENV != "development",
        samesite="lax",
        path="/api/v1/auth",
    )

    return ApiResponse(
        data=TokenRefreshResponse(
            access_token=new_access_token,
            refresh_token="",  # 쿠키로 전송되므로 응답 body에서 제거
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
    )


@router.post("/logout", response_model=ApiResponse[LogoutResponse])
async def logout(
    response: Response,
    refresh_token_cookie: str | None = Cookie(default=None, alias=REFRESH_TOKEN_COOKIE_NAME),
    current_user: UserResponse = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """로그아웃 (HttpOnly 쿠키에서 refresh token 읽기)."""
    # 쿠키에서 refresh token이 있으면 무효화
    if refresh_token_cookie:
        auth_service.revoke_refresh_token(refresh_token_cookie)

    # 쿠키 삭제
    response.delete_cookie(key=REFRESH_TOKEN_COOKIE_NAME, path="/api/v1/auth")

    return ApiResponse(data=LogoutResponse(message="로그아웃 성공"))


@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """현재 사용자 정보 조회."""
    return ApiResponse(data=current_user)


@router.post(
    "/register",
    response_model=ApiResponse[RegisterResponse],
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterStudentRequest | RegisterTeacherRequest | RegisterAdminRequest,
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN, UserRole.MASTER)),
    auth_service: AuthService = Depends(get_auth_service),
):
    """사용자 등록.

    권한:
    - TEACHER: 학생만 생성 가능
    - ADMIN: 학생, 강사 생성 가능
    - MASTER: 학생, 강사, 관리자 생성 가능
    """
    # 이메일 중복 체크
    existing_user = auth_service.get_user_by_email(request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "EMAIL_ALREADY_EXISTS",
                    "message": "이미 사용 중인 이메일입니다.",
                },
            },
        )

    # 역할 결정 및 권한 검증
    if isinstance(request, RegisterStudentRequest):
        role = UserRole.STUDENT
        user_data = UserCreate(
            email=request.email,
            password=request.password,
            name=request.name,
            role=role,
            grade=request.grade,
            class_id=request.class_id,
        )
    elif isinstance(request, RegisterTeacherRequest):
        # 강사 생성은 ADMIN, MASTER만 가능
        if current_user.role == UserRole.TEACHER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "error": {
                        "code": "FORBIDDEN",
                        "message": "강사 계정 생성 권한이 없습니다.",
                    },
                },
            )
        role = UserRole.TEACHER
        user_data = UserCreate(
            email=request.email,
            password=request.password,
            name=request.name,
            role=role,
        )
    else:  # RegisterAdminRequest
        # 관리자 생성은 MASTER만 가능
        if current_user.role != UserRole.MASTER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "error": {
                        "code": "FORBIDDEN",
                        "message": "관리자 계정 생성 권한이 없습니다. 마스터만 가능합니다.",
                    },
                },
            )
        role = UserRole.ADMIN
        user_data = UserCreate(
            email=request.email,
            password=request.password,
            name=request.name,
            role=role,
        )

    user = auth_service.create_user(user_data)

    return ApiResponse(
        data=RegisterResponse(
            user=UserResponse.model_validate(user),
            message="사용자가 등록되었습니다.",
        )
    )
