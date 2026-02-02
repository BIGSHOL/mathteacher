"""인증 API 엔드포인트."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
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

    return ApiResponse(
        data=LoginResponse(
            user=UserResponse.model_validate(user),
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
    )


@router.post("/refresh", response_model=ApiResponse[TokenRefreshResponse])
async def refresh_token(
    request: TokenRefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """토큰 갱신."""
    # 기존 토큰 검증
    stored_token = auth_service.get_refresh_token(request.refresh_token)
    if not stored_token:
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
    payload = auth_service.verify_token(request.refresh_token)
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

    user_id = payload["sub"]

    # 기존 토큰 무효화
    auth_service.revoke_refresh_token(request.refresh_token)

    # 새 토큰 발급
    new_access_token = auth_service.create_access_token(user_id)
    new_refresh_token = auth_service.create_refresh_token(user_id)
    auth_service.save_refresh_token(user_id, new_refresh_token)

    return ApiResponse(
        data=TokenRefreshResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
    )


@router.post("/logout", response_model=ApiResponse[LogoutResponse])
async def logout(
    request: LogoutRequest,
    current_user: UserResponse = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """로그아웃."""
    auth_service.revoke_refresh_token(request.refresh_token)

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
    request: RegisterStudentRequest | RegisterTeacherRequest,
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    auth_service: AuthService = Depends(get_auth_service),
):
    """사용자 등록 (강사/관리자 전용)."""
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

    # 역할 결정
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
    else:
        role = UserRole.TEACHER
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
