"""집중 체크 모델 - 4회 이상 틀린 문제 저장."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class FocusCheckItem(Base):
    """집중 체크 문제 모델.
    
    4회 이상 틀린 문제를 별도로 저장하여 추후 집중 학습에 활용.
    """

    __tablename__ = "focus_check_items"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), index=True
    )
    question_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("questions.id"), index=True
    )
    
    # 메타 정보
    attempt_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("test_attempts.id"), nullable=True
    )
    wrong_count: Mapped[int] = mapped_column(default=4)  # 틀린 횟수
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)  # 해결 여부
    
    # 시간
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def __repr__(self) -> str:
        return f"<FocusCheckItem {self.id[:8]} q={self.question_id[:8]}>"
