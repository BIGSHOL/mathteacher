"""단원(목차) 모델."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Enum as SAEnum, ForeignKey, Integer, JSON, String, Table, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.schemas.common import Grade


# 단원 선수관계 연결 테이블
chapter_prerequisites = Table(
    "chapter_prerequisites",
    Base.metadata,
    Column("chapter_id", String(36), ForeignKey("chapters.id"), primary_key=True),
    Column("prerequisite_id", String(36), ForeignKey("chapters.id"), primary_key=True),
    comment="단원 선수관계. chapter_id를 배우려면 prerequisite_id를 먼저 완료해야 함",
)


class Chapter(Base):
    """단원 모델 (교과서 목차 구조)."""

    __tablename__ = "chapters"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    name: Mapped[str] = mapped_column(
        String(200), index=True, comment="예: 1. 소인수분해"
    )
    grade: Mapped[Grade] = mapped_column(SAEnum(Grade), index=True)
    chapter_number: Mapped[int] = mapped_column(
        Integer, index=True, comment="단원 번호 (1, 2, 3, ...)"
    )
    description: Mapped[str] = mapped_column(Text, default="")

    # 구성 요소
    concept_ids: Mapped[list[str]] = mapped_column(
        JSON, default=list, comment="이 단원에 포함된 개념 ID 목록"
    )
    final_test_id: Mapped[str | None] = mapped_column(
        String(36), nullable=True, comment="단원 종합 테스트 ID"
    )

    # 완료 조건
    mastery_threshold: Mapped[int] = mapped_column(
        Integer, default=80, comment="개념 마스터리 임계값 (%)"
    )
    final_test_pass_score: Mapped[int] = mapped_column(
        Integer, default=70, comment="종합 테스트 통과 점수"
    )
    require_teacher_approval: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="선생님 승인 필요 여부"
    )

    # 상태
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 관계: 선수 단원
    prerequisites: Mapped[list["Chapter"]] = relationship(
        "Chapter",
        secondary=chapter_prerequisites,
        primaryjoin=id == chapter_prerequisites.c.chapter_id,
        secondaryjoin=id == chapter_prerequisites.c.prerequisite_id,
        backref="dependents",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Chapter {self.name}>"
