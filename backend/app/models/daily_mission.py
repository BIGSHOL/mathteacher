from datetime import datetime
from uuid import uuid4
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class DailyMission(Base):
    """일일 미션 모델."""

    __tablename__ = "daily_missions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    
    # 미션 타입 (e.g., 'complete_tests', 'solve_questions', 'get_perfect_score')
    type: Mapped[str] = mapped_column(String(50))
    title: Mapped[str] = mapped_column(String(100))
    
    target_count: Mapped[int] = mapped_column(Integer, default=1)
    current_count: Mapped[int] = mapped_column(Integer, default=0)
    
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_claimed: Mapped[bool] = mapped_column(Boolean, default=False, comment="보상 수령 여부")
    
    reward_xp: Mapped[int] = mapped_column(Integer, default=100)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    
    student = relationship("User", backref="daily_missions")
