"""오답 간격 반복 학습 모델."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class WrongAnswerReview(Base):
    """오답 간격 반복 학습 스케줄.

    학생이 틀린 문제를 1일→3일→7일→30일→60일 간격으로 재출제.
    AnswerLog는 건드리지 않고, 이 테이블은 복습 스케줄만 관리.
    """

    __tablename__ = "wrong_answer_reviews"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    question_id: Mapped[str] = mapped_column(
        String(100), ForeignKey("questions.id", ondelete="CASCADE"), index=True
    )

    # 복습 스케줄
    review_stage: Mapped[int] = mapped_column(Integer, default=1)
    next_review_date: Mapped[str] = mapped_column(String(10))  # "YYYY-MM-DD" KST

    # 이력
    wrong_count: Mapped[int] = mapped_column(Integer, default=1)
    correct_streak: Mapped[int] = mapped_column(Integer, default=0)
    last_wrong_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # 상태
    is_graduated: Mapped[bool] = mapped_column(Boolean, default=False)
    graduated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint("student_id", "question_id", name="uq_student_question_review"),
    )

    def __repr__(self) -> str:
        return f"<WrongAnswerReview student={self.student_id[:8]} q={self.question_id} stage={self.review_stage}>"
