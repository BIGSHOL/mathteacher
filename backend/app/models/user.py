"""사용자 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, JSON, String, func
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
    login_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(
        String(20), default="student"
    )
    grade: Mapped[str | None] = mapped_column(String(20), nullable=True)
    class_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("classes.id"), nullable=True
    )

    # 게이미피케이션
    level: Mapped[int] = mapped_column(Integer, default=1)
    total_xp: Mapped[int] = mapped_column(Integer, default=0)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    max_streak: Mapped[int] = mapped_column(Integer, default=0)
    level_down_defense: Mapped[int] = mapped_column(Integer, default=3)
    last_activity_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_quota_met_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="마지막 할당량 달성 날짜"
    )

    # 상태
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # 관계
    inventory = relationship("UserItem", back_populates="user", cascade="all, delete-orphan")

    # 진단 평가 (Placement Test)
    has_completed_placement: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="진단 평가 완료 여부"
    )
    placement_test_id: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="완료한 진단 평가 시도 ID"
    )
    placement_result: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="진단 평가 결과 (시작 단원, 레벨 등)"
    )

    # 강사 메모
    teacher_memo: Mapped[str | None] = mapped_column(
        String(2000), nullable=True, comment="강사 메모 (학생에 대한 특이사항 등)"
    )

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 관계
    class_: Mapped["Class | None"] = relationship(
        "Class", back_populates="students", foreign_keys=[class_id], lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<User {self.login_id}>"


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
    user: Mapped["User"] = relationship("User", lazy="selectin")

    def __repr__(self) -> str:
        return f"<RefreshToken {self.id}>"
