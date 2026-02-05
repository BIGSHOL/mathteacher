"""인증 서비스."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from app.models.user import RefreshToken, User
from app.schemas.auth import UserCreate, UserResponse


class AuthService:
    """인증 서비스."""

    def __init__(self, db: AsyncSession | None = None):
        self.db = db

    def hash_password(self, password: str) -> str:
        """비밀번호 해싱."""
        return get_password_hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증."""
        return verify_password(plain_password, hashed_password)

    def create_access_token(self, user_id: str) -> str:
        """액세스 토큰 생성 (user_id만)."""
        return create_access_token(data={"sub": user_id})

    def create_access_token_for_user(self, user) -> str:
        """사용자 정보를 포함한 액세스 토큰 생성 (DB 조회 없이 인증 가능)."""
        return create_access_token(data={
            "sub": user.id,
            "role": user.role.value if hasattr(user.role, "value") else user.role,
            "name": user.name,
            "login_id": user.login_id,
            "grade": user.grade.value if user.grade and hasattr(user.grade, "value") else user.grade,
            "class_id": user.class_id,
        })

    def create_refresh_token(self, user_id: str) -> str:
        """리프레시 토큰 생성."""
        return create_refresh_token(data={"sub": user_id})

    def verify_token(self, token: str) -> dict | None:
        """토큰 검증."""
        return verify_token(token)

    async def get_user_by_login_id(self, login_id: str) -> User | None:
        """로그인 ID로 사용자 조회."""
        if not self.db:
            raise ValueError("Database session required")
        stmt = select(User).where(User.login_id == login_id)
        return await self.db.scalar(stmt)

    async def get_user_by_id(self, user_id: str) -> User | None:
        """ID로 사용자 조회."""
        if not self.db:
            raise ValueError("Database session required")
        return await self.db.get(User, user_id)

    async def authenticate_user(self, login_id: str, password: str) -> User | None:
        """사용자 인증."""
        import logging
        logger = logging.getLogger(__name__)

        user = await self.get_user_by_login_id(login_id)
        if not user:
            logger.warning("Login failed: user '%s' not found", login_id)
            return None
        if not self.verify_password(password, user.hashed_password):
            logger.warning("Login failed: wrong password for user '%s'", login_id)
            return None
        if not user.is_active:
            logger.warning("Login failed: user '%s' is inactive", login_id)
            return None
        logger.info("Login successful for user '%s'", login_id)
        return user

    async def create_user(self, user_data: UserCreate) -> User:
        """사용자 생성."""
        if not self.db:
            raise ValueError("Database session required")

        hashed_password = self.hash_password(user_data.password)
        user = User(
            login_id=user_data.login_id,
            hashed_password=hashed_password,
            name=user_data.name,
            role=user_data.role,
            grade=user_data.grade,
            class_id=user_data.class_id,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def save_refresh_token(self, user_id: str, token: str) -> RefreshToken:
        """리프레시 토큰 저장."""
        if not self.db:
            raise ValueError("Database session required")

        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        self.db.add(refresh_token)
        await self.db.commit()
        return refresh_token

    async def get_refresh_token(self, token: str) -> RefreshToken | None:
        """리프레시 토큰 조회."""
        if not self.db:
            raise ValueError("Database session required")
        stmt = select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.is_revoked == False,  # noqa: E712
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
        return await self.db.scalar(stmt)

    async def revoke_refresh_token(self, token: str) -> bool:
        """리프레시 토큰 무효화."""
        if not self.db:
            raise ValueError("Database session required")
        refresh_token = await self.get_refresh_token(token)
        if not refresh_token:
            return False
        refresh_token.is_revoked = True
        await self.db.commit()
        return True

    async def revoke_all_user_tokens(self, user_id: str) -> None:
        """사용자의 모든 리프레시 토큰 무효화."""
        if not self.db:
            raise ValueError("Database session required")
        stmt = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False,  # noqa: E712
        )
        tokens = (await self.db.scalars(stmt)).all()
        for token in tokens:
            token.is_revoked = True
        await self.db.commit()
