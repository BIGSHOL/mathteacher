"""반(클래스) 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
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
    grade: Mapped[Grade] = mapped_column(Enum(Grade))
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 관계
    teacher: Mapped["User"] = relationship(
        "User", foreign_keys=[teacher_id], backref="taught_classes"
    )
    students: Mapped[list["User"]] = relationship(
        "User", back_populates="class_", foreign_keys="User.class_id"
    )

    def __repr__(self) -> str:
        return f"<Class {self.name}>"
