"""반(클래스) 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.schemas.common import Grade

if TYPE_CHECKING:
    from app.models.user import User


class Class(Base):
    """반 모델."""

    __tablename__ = "classes"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    name: Mapped[str] = mapped_column(String(100))
    teacher_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), index=True
    )
    grade: Mapped[str] = mapped_column(String(20))
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # 일일 할당량
    daily_quota: Mapped[int] = mapped_column(
        Integer, default=20, comment="일일 목표 정답 수"
    )
    quota_carry_over: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="미달성 할당량 이월 여부"
    )

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 관계
    teacher: Mapped["User"] = relationship(
        "User", foreign_keys=[teacher_id], backref="taught_classes", lazy="selectin"
    )
    students: Mapped[list["User"]] = relationship(
        "User", back_populates="class_", foreign_keys="User.class_id", lazy="raise"
    )

    def __repr__(self) -> str:
        return f"<Class {self.name}>"
