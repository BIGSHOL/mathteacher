"""인증 서비스."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

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

    def __init__(self, db: Session | None = None):
        self.db = db

    def hash_password(self, password: str) -> str:
        """비밀번호 해싱."""
        return get_password_hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증."""
        return verify_password(plain_password, hashed_password)

    def create_access_token(self, user_id: str) -> str:
        """액세스 토큰 생성."""
        return create_access_token(data={"sub": user_id})

    def create_refresh_token(self, user_id: str) -> str:
        """리프레시 토큰 생성."""
        return create_refresh_token(data={"sub": user_id})

    def verify_token(self, token: str) -> dict | None:
        """토큰 검증."""
        return verify_token(token)

    def get_user_by_email(self, email: str) -> User | None:
        """이메일로 사용자 조회."""
        if not self.db:
            raise ValueError("Database session required")
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)

    def get_user_by_id(self, user_id: str) -> User | None:
        """ID로 사용자 조회."""
        if not self.db:
            raise ValueError("Database session required")
        return self.db.get(User, user_id)

    def authenticate_user(self, email: str, password: str) -> User | None:
        """사용자 인증."""
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user

    def create_user(self, user_data: UserCreate) -> User:
        """사용자 생성."""
        if not self.db:
            raise ValueError("Database session required")

        hashed_password = self.hash_password(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            name=user_data.name,
            role=user_data.role,
            grade=user_data.grade,
            class_id=user_data.class_id,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def save_refresh_token(self, user_id: str, token: str) -> RefreshToken:
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
        self.db.commit()
        return refresh_token

    def get_refresh_token(self, token: str) -> RefreshToken | None:
        """리프레시 토큰 조회."""
        if not self.db:
            raise ValueError("Database session required")
        stmt = select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.is_revoked == False,  # noqa: E712
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
        return self.db.scalar(stmt)

    def revoke_refresh_token(self, token: str) -> bool:
        """리프레시 토큰 무효화."""
        if not self.db:
            raise ValueError("Database session required")
        refresh_token = self.get_refresh_token(token)
        if not refresh_token:
            return False
        refresh_token.is_revoked = True
        self.db.commit()
        return True

    def revoke_all_user_tokens(self, user_id: str) -> None:
        """사용자의 모든 리프레시 토큰 무효화."""
        if not self.db:
            raise ValueError("Database session required")
        stmt = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False,  # noqa: E712
        )
        tokens = self.db.scalars(stmt).all()
        for token in tokens:
            token.is_revoked = True
        self.db.commit()
