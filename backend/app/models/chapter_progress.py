"""단원 진행 상황 모델."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ChapterProgress(Base):
    """학생의 단원별 진행 상황."""

    __tablename__ = "chapter_progress"
    __table_args__ = (
        UniqueConstraint("student_id", "chapter_id", name="uix_student_chapter"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    chapter_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("chapters.id", ondelete="CASCADE"), index=True
    )

    # 잠금/해제
    is_unlocked: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="단원 해제 여부"
    )
    unlocked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # 개념별 마스터리 (빠른 조회용)
    concepts_mastery: Mapped[dict] = mapped_column(
        JSON, default=dict, comment='{"concept-001": 85, "concept-002": 100}'
    )

    # 종합 테스트
    final_test_attempted: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="종합 테스트 시도 여부"
    )
    final_test_passed: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="종합 테스트 통과"
    )
    final_test_score: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="종합 테스트 점수"
    )
    final_test_attempt_id: Mapped[str | None] = mapped_column(
        String(36), nullable=True, comment="최고 점수 시도 ID"
    )

    # 선생님 승인
    teacher_approved: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="선생님 승인 여부"
    )
    approved_by: Mapped[str | None] = mapped_column(
        String(36), nullable=True, comment="승인한 선생님 ID"
    )
    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    approval_feedback: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="승인 피드백"
    )

    # 완료
    is_completed: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="단원 완료 여부"
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # 진행률 (0-100)
    overall_progress: Mapped[int] = mapped_column(
        Integer, default=0, comment="전체 진행률 %"
    )

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<ChapterProgress student={self.student_id[:8]} chapter={self.chapter_id[:8]} progress={self.overall_progress}%>"
