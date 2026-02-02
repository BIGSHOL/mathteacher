"""문제 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.schemas.common import Difficulty, QuestionType

if TYPE_CHECKING:
    from app.models.concept import Concept


class Question(Base):
    """문제 모델."""

    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    concept_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("concepts.id"), index=True
    )
    question_type: Mapped[QuestionType] = mapped_column(Enum(QuestionType))
    difficulty: Mapped[Difficulty] = mapped_column(Enum(Difficulty), index=True)
    content: Mapped[str] = mapped_column(Text)
    options: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    correct_answer: Mapped[str] = mapped_column(String(500))
    explanation: Mapped[str] = mapped_column(Text, default="")
    points: Mapped[int] = mapped_column(Integer, default=10)

    # 상태
    is_active: Mapped[bool] = mapped_column(default=True)

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 관계
    concept: Mapped["Concept"] = relationship("Concept", back_populates="questions")

    def __repr__(self) -> str:
        return f"<Question {self.id[:8]}>"
