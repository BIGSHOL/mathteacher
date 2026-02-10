"""문제 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Index, Integer, String, Text, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.database import Base
from app.schemas.common import ConceptMethod, ProblemPart, QuestionType

if TYPE_CHECKING:
    from app.models.concept import Concept


class Question(Base):
    """문제 모델."""

    __tablename__ = "questions"
    __table_args__ = (
        CheckConstraint("difficulty >= 1 AND difficulty <= 10", name="ck_question_difficulty_range"),
        Index("ix_question_concept_type_diff_active", "concept_id", "question_type", "difficulty", "is_active"),
        Index("ix_question_active_created", "is_active", "created_at"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    concept_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("concepts.id"), index=True
    )
    category: Mapped[str] = mapped_column(
        String(30), index=True, comment="트랙: computation / concept / application / fill_in_blank"
    )
    part: Mapped[ProblemPart] = mapped_column(
        Enum(ProblemPart), index=True, comment="파트: calc/algebra/func/geo/data/word"
    )
    question_type: Mapped[QuestionType] = mapped_column(Enum(QuestionType))
    difficulty: Mapped[int] = mapped_column(Integer, index=True, comment="학년 내 상대 난이도 1-10")
    content: Mapped[str] = mapped_column(Text)
    options: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    correct_answer: Mapped[str] = mapped_column(String(500))
    explanation: Mapped[str] = mapped_column(Text, default="")
    hint: Mapped[str] = mapped_column(Text, nullable=True, comment="문제 힌트")
    
    # 개념 문항 확장 (Phase 2)
    concept_method: Mapped[ConceptMethod | None] = mapped_column(
        Enum(ConceptMethod), nullable=True, comment="개념 문항 생성 방식 (Gradual Fading 등)"
    )
    fading_level: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="빈칸 레벨 (1~4)"
    )

    points: Mapped[int] = mapped_column(Integer, default=10)

    # 계통수학: 선수 개념 연결
    prerequisite_concept_ids: Mapped[list[str] | None] = mapped_column(
        JSON, nullable=True, default=list,
        comment="선수 개념 ID 목록 (계통수학 체인)"
    )

    # 빈칸 채우기 설정
    blank_config: Mapped[dict | None] = mapped_column(
        JSON, nullable=True,
        comment="빈칸 채우기 설정: 빈칸 가능 위치, 중요도, 회차별 규칙"
    )

    # 상태
    is_active: Mapped[bool] = mapped_column(default=True, index=True)

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 관계
    concept: Mapped["Concept"] = relationship("Concept", back_populates="questions", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Question {self.id[:8]}>"
