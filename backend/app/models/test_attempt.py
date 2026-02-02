"""테스트 시도 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.test import Test
    from app.models.user import User
    from app.models.answer_log import AnswerLog


class TestAttempt(Base):
    """테스트 시도 모델."""

    __tablename__ = "test_attempts"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    test_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tests.id"), index=True
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), index=True
    )

    # 시간
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # 점수
    score: Mapped[int] = mapped_column(Integer, default=0)
    max_score: Mapped[int] = mapped_column(Integer, default=0)
    correct_count: Mapped[int] = mapped_column(Integer, default=0)
    total_count: Mapped[int] = mapped_column(Integer, default=0)

    # 게이미피케이션
    xp_earned: Mapped[int] = mapped_column(Integer, default=0)
    combo_max: Mapped[int] = mapped_column(Integer, default=0)

    # 관계
    test: Mapped["Test"] = relationship("Test", back_populates="attempts")
    student: Mapped["User"] = relationship("User")
    answer_logs: Mapped[list["AnswerLog"]] = relationship(
        "AnswerLog", back_populates="attempt", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<TestAttempt {self.id[:8]}>"
