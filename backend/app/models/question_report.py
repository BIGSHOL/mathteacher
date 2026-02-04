"""문제 신고 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.schemas.common import ReportStatus, ReportType

if TYPE_CHECKING:
    from app.models.question import Question
    from app.models.user import User


class QuestionReport(Base):
    """문제 신고."""

    __tablename__ = "question_reports"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    question_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("questions.id", ondelete="CASCADE"), index=True
    )
    reporter_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    report_type: Mapped[ReportType] = mapped_column(
        Enum(ReportType), index=True
    )
    comment: Mapped[str] = mapped_column(Text)
    status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus), default=ReportStatus.PENDING, index=True
    )
    admin_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolved_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 관계
    question: Mapped["Question"] = relationship("Question", lazy="selectin")
    reporter: Mapped["User"] = relationship(
        "User", foreign_keys=[reporter_id], lazy="selectin"
    )
    reviewer: Mapped["User | None"] = relationship(
        "User", foreign_keys=[resolved_by], lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<QuestionReport {self.id[:8]}>"
