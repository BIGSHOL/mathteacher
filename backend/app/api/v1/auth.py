"""인증 API 엔드포인트."""

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_token as _verify_jwt

_testing = os.environ.get("TESTING") == "1"

from app.core.config import settings
from app.core.database import get_db
from app.schemas import (
    ApiResponse,
    ErrorResponse,
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    LogoutResponse,
    RegisterRequest,
    RegisterResponse,
    UpdateUserRequest,
    TokenRefreshRequest,
    TokenRefreshResponse,
    UserCreate,
    UserResponse,
)
from app.schemas.common import UserRole
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)

# Rate Limiter 인스턴스
limiter = Limiter(key_func=get_remote_address)

# 쿠키 설정 상수
REFRESH_TOKEN_COOKIE_NAME = "refresh_token"
REFRESH_TOKEN_MAX_AGE = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60  # seconds


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """인증 서비스 의존성."""
    return AuthService(db)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> UserResponse:
    """현재 사용자 조회 (JWT 페이로드에서 직접 반환, DB 조회 없음)."""
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

    payload = _verify_jwt(credentials.credentials)
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

    # JWT 페이로드에 사용자 정보가 있으면 DB 조회 없이 반환
    try:
        now = datetime.now(timezone.utc)
        return UserResponse(
            id=payload["sub"],
            login_id=payload.get("login_id", ""),
            name=payload.get("name", ""),
            role=payload.get("role", "student"),
            grade=payload.get("grade"),
            class_id=payload.get("class_id"),
            level=payload.get("level", 1),
            total_xp=payload.get("total_xp", 0),
            current_streak=payload.get("current_streak", 0),
            created_at=now,
            updated_at=now,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "토큰 데이터가 유효하지 않습니다.",
                },
            },
        )


def require_role(*roles: UserRole):
    """역할 권한 검증 의존성."""

    async def role_checker(current_user: UserResponse = Depends(get_current_user)):
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
@limiter.limit("10000/minute" if _testing else "10/minute")
async def login(
    request: Request,
    login_request: LoginRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    """로그인."""
    user = await auth_service.authenticate_user(login_request.login_id, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "아이디 또는 비밀번호가 올바르지 않습니다.",
                },
            },
        )

    access_token = auth_service.create_access_token_for_user(user)
    refresh_token = auth_service.create_refresh_token(user.id)

    # 리프레시 토큰 저장
    await auth_service.save_refresh_token(user.id, refresh_token)

    # HttpOnly 쿠키로 refresh token 설정 (XSS 방지)
    # 크로스 오리진(Vercel↔Railway)에서는 samesite="none" 필수
    is_production = settings.ENV != "development"
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        max_age=REFRESH_TOKEN_MAX_AGE,
        httponly=True,  # JavaScript 접근 불가
        secure=is_production,  # HTTPS only in production
        samesite="none" if is_production else "lax",  # 크로스 오리진 허용
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
    stored_token = await auth_service.get_refresh_token(refresh_token_cookie)
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
    await auth_service.revoke_refresh_token(refresh_token_cookie)

    # 새 토큰 발급 (사용자 정보 포함)
    user = await auth_service.get_user_by_id(user_id)
    if user:
        new_access_token = auth_service.create_access_token_for_user(user)
    else:
        new_access_token = auth_service.create_access_token(user_id)
    new_refresh_token = auth_service.create_refresh_token(user_id)
    await auth_service.save_refresh_token(user_id, new_refresh_token)

    # 새 refresh token을 HttpOnly 쿠키로 설정
    is_production = settings.ENV != "development"
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE_NAME,
        value=new_refresh_token,
        max_age=REFRESH_TOKEN_MAX_AGE,
        httponly=True,
        secure=is_production,
        samesite="none" if is_production else "lax",
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
        await auth_service.revoke_refresh_token(refresh_token_cookie)

    # 쿠키 삭제
    response.delete_cookie(key=REFRESH_TOKEN_COOKIE_NAME, path="/api/v1/auth")

    return ApiResponse(data=LogoutResponse(message="로그아웃 성공"))


@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """현재 사용자 정보 조회."""
    return ApiResponse(data=current_user)


@router.get("/debug-users")
async def debug_users(auth_service: AuthService = Depends(get_auth_service)):
    """디버그: DB에 있는 사용자 목록 확인 (배포 후 삭제 필요)."""
    from sqlalchemy import select
    from app.models.user import User

    stmt = select(User.id, User.login_id, User.name, User.role, User.is_active)
    result = await auth_service.db.execute(stmt)
    users = result.all()

    return {
        "total_users": len(users),
        "users": [
            {
                "id": u.id,
                "login_id": u.login_id,
                "name": u.name,
                "role": u.role,
                "is_active": u.is_active,
            }
            for u in users
        ],
    }


@router.get("/debug-chapters")
async def debug_chapters(
    grade: str | None = None,
    auth_service: AuthService = Depends(get_auth_service),
):
    """디버그: 챕터 concept_ids 매핑 상태 확인."""
    from sqlalchemy import select
    from app.models.chapter import Chapter
    from app.models.question import Question
    from app.models.daily_test_record import DailyTestRecord

    db = auth_service.db

    # 챕터 조회
    stmt = select(Chapter).order_by(Chapter.grade, Chapter.chapter_number)
    if grade:
        stmt = stmt.where(Chapter.grade == grade)
    chapters = list((await db.scalars(stmt)).all())

    chapter_data = []
    for ch in chapters:
        # 이 concept_ids에 해당하는 문제 수 확인
        q_count = 0
        if ch.concept_ids:
            q_stmt = select(func.count()).select_from(Question).where(
                Question.concept_id.in_(ch.concept_ids),
                Question.is_active == True,  # noqa: E712
            )
            q_count = await db.scalar(q_stmt) or 0

        chapter_data.append({
            "id": ch.id,
            "name": ch.name,
            "grade": ch.grade,
            "chapter_number": ch.chapter_number,
            "concept_ids": ch.concept_ids,
            "question_count": q_count,
        })

    # 오늘의 일일 테스트 현황
    from datetime import datetime, timedelta, timezone as tz
    KST = tz(timedelta(hours=9))
    today = datetime.now(KST).date().isoformat()
    daily_stmt = select(DailyTestRecord).where(DailyTestRecord.date == today)
    daily_records = list((await db.scalars(daily_stmt)).all())

    return {
        "total_chapters": len(chapters),
        "chapters": chapter_data,
        "today_daily_tests": [
            {
                "student_id": r.student_id,
                "category": r.category,
                "test_id": r.test_id,
                "total_count": r.total_count,
                "status": r.status,
            }
            for r in daily_records
        ],
    }


@router.post(
    "/register",
    response_model=ApiResponse[RegisterResponse],
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10000/minute" if _testing else "5/minute")
async def register(
    request: Request,
    register_request: RegisterRequest,
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN, UserRole.MASTER)),
    auth_service: AuthService = Depends(get_auth_service),
):
    """사용자 등록.

    권한:
    - TEACHER: 학생만 생성 가능
    - ADMIN: 학생, 강사 생성 가능
    - MASTER: 학생, 강사, 관리자 생성 가능
    """
    # 아이디 중복 체크
    existing_user = await auth_service.get_user_by_login_id(register_request.login_id)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "LOGIN_ID_ALREADY_EXISTS",
                    "message": "이미 사용 중인 아이디입니다.",
                },
            },
        )

    role = register_request.role

    # 권한 검증
    if role == UserRole.ADMIN and current_user.role != UserRole.MASTER:
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
    if role == UserRole.TEACHER and current_user.role == UserRole.TEACHER:
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
    if role == UserRole.MASTER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "error": {
                    "code": "FORBIDDEN",
                    "message": "마스터 계정은 생성할 수 없습니다.",
                },
            },
        )

    user_data = UserCreate(
        login_id=register_request.login_id,
        password=register_request.password,
        name=register_request.name,
        role=role,
        grade=register_request.grade if role == UserRole.STUDENT else None,
        class_id=register_request.class_id if role == UserRole.STUDENT else None,
    )

    user = await auth_service.create_user(user_data)

    return ApiResponse(
        data=RegisterResponse(
            user=UserResponse.model_validate(user),
            message="사용자가 등록되었습니다.",
        )
    )
