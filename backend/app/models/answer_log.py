"""답안 기록 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.test_attempt import TestAttempt
    from app.models.question import Question


class AnswerLog(Base):
    """답안 기록 모델."""

    __tablename__ = "answer_logs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    attempt_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("test_attempts.id", ondelete="CASCADE"), index=True
    )
    question_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("questions.id"), index=True
    )

    # 답안
    selected_answer: Mapped[str] = mapped_column(String(500))
    is_correct: Mapped[bool] = mapped_column(Boolean)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)

    # 게이미피케이션
    combo_count: Mapped[int] = mapped_column(Integer, default=0)
    points_earned: Mapped[int] = mapped_column(Integer, default=0)

    # 적응형 난이도 스냅샷
    question_difficulty: Mapped[int | None] = mapped_column(Integer, nullable=True)
    question_category: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="문제 카테고리 스냅샷: computation | concept"
    )

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # 관계
    attempt: Mapped["TestAttempt"] = relationship(
        "TestAttempt", back_populates="answer_logs", lazy="raise"
    )
    question: Mapped["Question"] = relationship("Question", lazy="selectin")

    def __repr__(self) -> str:
        return f"<AnswerLog {self.id[:8]}>"
