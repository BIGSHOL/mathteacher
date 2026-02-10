"""테스트 모델."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.schemas.common import Grade

if TYPE_CHECKING:
    from app.models.test_attempt import TestAttempt


class Test(Base):
    """테스트 모델."""

    __tablename__ = "tests"

    id: Mapped[str] = mapped_column(
        String(100), primary_key=True, default=lambda: str(uuid4())
    )
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    grade: Mapped[str] = mapped_column(String(20), index=True)
    test_type: Mapped[str] = mapped_column(
        String(50), default="concept", comment="테스트 유형: concept, cumulative, semester_final, grade_final"
    )
    category: Mapped[str | None] = mapped_column(
        String(30), nullable=True, index=True,
        comment="문제 카테고리: computation, concept, fill_in_blank, 또는 NULL(종합)"
    )
    semester: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="학기 종합시험의 경우 학기 번호"
    )
    concept_ids: Mapped[list[str]] = mapped_column(JSON)
    question_ids: Mapped[list[str]] = mapped_column(JSON)
    question_count: Mapped[int] = mapped_column(Integer)
    time_limit_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # 적응형
    is_adaptive: Mapped[bool] = mapped_column(Boolean, default=False)
    adaptive_pool_config: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # 문제 풀 설정
    use_question_pool: Mapped[bool] = mapped_column(Boolean, default=False)
    questions_per_attempt: Mapped[int | None] = mapped_column(Integer, nullable=True)
    shuffle_options: Mapped[bool] = mapped_column(Boolean, default=True)

    # 상태
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_placement: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="진단 평가 테스트 여부"
    )

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 관계
    attempts: Mapped[list["TestAttempt"]] = relationship(
        "TestAttempt", back_populates="test", lazy="raise"
    )

    def __repr__(self) -> str:
        return f"<Test {self.title}>"
