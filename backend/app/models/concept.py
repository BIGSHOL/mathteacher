"""개념 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Index, String, Text, func, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.schemas.common import Grade, ProblemPart, QuestionCategory


# 개념 선수관계 연결 테이블 (계통수학)
concept_prerequisites = Table(
    "concept_prerequisites",
    Base.metadata,
    Column("concept_id", String(36), ForeignKey("concepts.id"), primary_key=True),
    Column("prerequisite_id", String(36), ForeignKey("concepts.id"), primary_key=True),
    comment="개념 선수관계 (계통수학 체인). concept_id를 배우려면 prerequisite_id를 먼저 알아야 함",
)

if TYPE_CHECKING:
    from app.models.question import Question


class Concept(Base):
    """수학 개념 모델."""

    __tablename__ = "concepts"
    __table_args__ = (
        Index("ix_concept_grade_name", "grade", "name"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    name: Mapped[str] = mapped_column(String(200), index=True)
    grade: Mapped[Grade] = mapped_column(SAEnum(Grade), index=True)
    category: Mapped[QuestionCategory] = mapped_column(
        SAEnum(QuestionCategory), index=True, default=QuestionCategory.CONCEPT,
        comment="트랙: 연산(computation) / 개념(concept)"
    )
    part: Mapped[ProblemPart] = mapped_column(
        SAEnum(ProblemPart), index=True, default=ProblemPart.CALC,
        comment="파트: calc/algebra/func/geo/data/word"
    )
    description: Mapped[str] = mapped_column(Text, default="")
    parent_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("concepts.id"), nullable=True
    )

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 관계
    parent: Mapped["Concept | None"] = relationship(
        "Concept", remote_side=[id], backref="children", lazy="raise"
    )
    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="concept", lazy="raise"
    )

    # 계통수학: 선수 개념 관계 (이 개념을 배우려면 먼저 알아야 하는 개념들)
    prerequisites: Mapped[list["Concept"]] = relationship(
        "Concept",
        secondary=concept_prerequisites,
        primaryjoin=id == concept_prerequisites.c.concept_id,
        secondaryjoin=id == concept_prerequisites.c.prerequisite_id,
        backref="dependents",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return f"<Concept {self.name}>"
