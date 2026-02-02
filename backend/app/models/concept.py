"""개념 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.schemas.common import Grade

if TYPE_CHECKING:
    from app.models.question import Question


class Concept(Base):
    """수학 개념 모델."""

    __tablename__ = "concepts"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    name: Mapped[str] = mapped_column(String(200), index=True)
    grade: Mapped[Grade] = mapped_column(Enum(Grade), index=True)
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
        "Concept", remote_side=[id], backref="children"
    )
    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="concept"
    )

    def __repr__(self) -> str:
        return f"<Concept {self.name}>"
