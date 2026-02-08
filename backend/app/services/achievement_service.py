from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.models.achievement import Achievement
from app.models.user import User
from app.models.test_attempt import TestAttempt

class AchievementService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # 업적 정의
    ACHIEVEMENTS_DEF = {
        "first_test": {"name": "첫 걸음", "description": "첫 번째 테스트 완료", "icon": "🎉"},
        "streak_3": {"name": "작심삼일 탈출", "description": "3일 연속 학습", "icon": "🔥"},
        "streak_7": {"name": "일주일의 기적", "description": "7일 연속 학습", "icon": "📅"},
        "streak_30": {"name": "습관의 힘", "description": "30일 연속 학습", "icon": "🏆"},
        "combo_5": {"name": "콤보의 시작", "description": "5콤보 달성", "icon": "⚡"},
        "combo_10": {"name": "멈출 수 없는", "description": "10콤보 달성", "icon": "🌪️"},
        "perfect_score": {"name": "완벽주의자", "description": "테스트 100점 달성", "icon": "💯"},
        "level_5": {"name": "레벨업 마스터", "description": "레벨 5 달성", "icon": "⭐"},
        "level_10": {"name": "고수의 길", "description": "레벨 10 달성", "icon": "👑"},
        "tests_10": {"name": "성실한 학생", "description": "테스트 10회 완료", "icon": "📝"},
        "tests_50": {"name": "노력의 천재", "description": "테스트 50회 완료", "icon": "📚"},
        "tests_100": {"name": "수학의 신", "description": "테스트 100회 완료", "icon": "🎓"},
    }

    async def get_student_achievements(self, student_id: str) -> list[Achievement]:
        """학생의 획득 업적 목록 조회."""
        result = await self.db.execute(
            select(Achievement).where(Achievement.student_id == student_id)
        )
        return result.scalars().all()

    async def check_achievements(self, student_id: str, attempt: TestAttempt, user: User, completed_count: int) -> list[dict]:
        """테스트 완료 후 업적 달성 여부 체크."""
        
        # 이미 획득한 업적 조회
        existing_achievements = await self.get_student_achievements(student_id)
        existing_types = {a.achievement_type for a in existing_achievements}

        newly_earned = []

        # 체크 대상 및 조건
        checks = {
            "first_test": completed_count >= 1,
            "streak_3": user.current_streak >= 3,
            "streak_7": user.current_streak >= 7,
            "streak_30": user.current_streak >= 30,
            "combo_5": attempt.combo_max >= 5,
            "combo_10": attempt.combo_max >= 10,
            "perfect_score": attempt.score == attempt.max_score and attempt.max_score > 0,
            "level_5": user.level >= 5,
            "level_10": user.level >= 10,
            "tests_10": completed_count >= 10,
            "tests_50": completed_count >= 50,
            "tests_100": completed_count >= 100,
        }

        for ach_type, condition in checks.items():
            if condition and ach_type not in existing_types:
                # 새 업적 달성
                achievement = Achievement(
                    student_id=student_id,
                    achievement_type=ach_type
                )
                self.db.add(achievement)
                newly_earned.append({
                    "id": ach_type,
                    "name": self.ACHIEVEMENTS_DEF[ach_type]["name"],
                    "description": self.ACHIEVEMENTS_DEF[ach_type]["description"],
                    "icon": self.ACHIEVEMENTS_DEF[ach_type]["icon"],
                    "earned_at": datetime.now() # 클라이언트 표시용
                })
        
        if newly_earned:
            await self.db.commit()
            
        return newly_earned
