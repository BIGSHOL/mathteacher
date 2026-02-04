"""일일 테스트 기록 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.test import Test
    from app.models.test_attempt import TestAttempt
    from app.models.user import User


class DailyTestRecord(Base):
    """일일 테스트 기록 - 학생별/카테고리별/날짜별 테스트 추적."""

    __tablename__ = "daily_test_records"
    __table_args__ = (
        UniqueConstraint(
            "student_id", "date", "category",
            name="uix_student_date_category",
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    date: Mapped[str] = mapped_column(
        String(10), index=True, comment="YYYY-MM-DD (KST)"
    )
    category: Mapped[str] = mapped_column(
        String(20), index=True, comment="concept | computation | fill_in_blank"
    )

    # 기존 Test/TestAttempt 연결
    test_id: Mapped[str] = mapped_column(
        String(100), ForeignKey("tests.id")
    )
    attempt_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("test_attempts.id"), nullable=True
    )

    # 상태 및 결과 (비정규화 - 이력 조회 성능용)
    status: Mapped[str] = mapped_column(
        String(20), default="pending", comment="pending | in_progress | completed"
    )
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    correct_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # 관계
    test: Mapped["Test"] = relationship("Test", lazy="selectin")
    attempt: Mapped["TestAttempt | None"] = relationship("TestAttempt", lazy="selectin")
    student: Mapped["User"] = relationship("User", lazy="selectin")

    def __repr__(self) -> str:
        return f"<DailyTestRecord {self.date} {self.category} {self.status}>"