"""사용자 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.schemas.common import Grade, UserRole

if TYPE_CHECKING:
    from app.models.class_ import Class


class User(Base):
    """사용자 모델."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.STUDENT
    )
    grade: Mapped[Grade | None] = mapped_column(Enum(Grade), nullable=True)
    class_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("classes.id"), nullable=True
    )

    # 게이미피케이션
    level: Mapped[int] = mapped_column(Integer, default=1)
    total_xp: Mapped[int] = mapped_column(Integer, default=0)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    max_streak: Mapped[int] = mapped_column(Integer, default=0)
    last_activity_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # 상태
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 관계
    class_: Mapped["Class | None"] = relationship(
        "Class", back_populates="students", foreign_keys=[class_id]
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class RefreshToken(Base):
    """리프레시 토큰 모델."""

    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    token: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # 관계
    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        return f"<RefreshToken {self.id}>"
