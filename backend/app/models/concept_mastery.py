"""개념 숙련도 모델."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ConceptMastery(Base):
    """학생의 개념별 숙련도 추적."""

    __tablename__ = "concept_mastery"
    __table_args__ = (
        UniqueConstraint("student_id", "concept_id", name="uix_student_concept"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    concept_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("concepts.id", ondelete="CASCADE"), index=True
    )
    
    student = relationship("User", backref="concept_masteries")
    concept = relationship("Concept", backref="masteries")

    # 숙련도 메트릭
    mastery_percentage: Mapped[int] = mapped_column(
        Integer, default=0, comment="숙련도 0-100%"
    )
    total_attempts: Mapped[int] = mapped_column(
        Integer, default=0, comment="총 시도 횟수"
    )
    correct_count: Mapped[int] = mapped_column(
        Integer, default=0, comment="정답 횟수"
    )
    average_score: Mapped[float] = mapped_column(
        Float, default=0.0, comment="평균 점수"
    )

    # 잠금/해제
    is_unlocked: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="선수학습 완료 여부"
    )
    unlocked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # 마스터리 달성
    is_mastered: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="80% 이상 달성"
    )
    mastered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # 타임스탬프
    last_practiced: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<ConceptMastery student={self.student_id[:8]} concept={self.concept_id[:8]} mastery={self.mastery_percentage}%>"
