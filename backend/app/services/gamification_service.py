"""게이미피케이션 서비스."""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.user import User


# 레벨별 필요 XP
LEVEL_XP_REQUIREMENTS = {
    1: 0,
    2: 100,
    3: 250,
    4: 450,
    5: 700,
    6: 1000,
    7: 1400,
    8: 1900,
    9: 2500,
    10: 3200,
}

MAX_LEVEL = 10


class GamificationService:
    """게이미피케이션 서비스."""

    def __init__(self, db: Session | None = None):
        self.db = db

    def calculate_xp(
        self,
        score: int,
        max_score: int,
        combo_max: int,
        time_bonus: bool = False,
    ) -> int:
        """XP 계산."""
        # 기본 XP: 점수의 절반
        base_xp = score // 2

        # 정답률 보너스 (90% 이상: +20%, 80% 이상: +10%)
        accuracy = score / max_score if max_score > 0 else 0
        if accuracy >= 0.9:
            base_xp = int(base_xp * 1.2)
        elif accuracy >= 0.8:
            base_xp = int(base_xp * 1.1)

        # 콤보 보너스 (5콤보 이상: +10XP, 10콤보 이상: +25XP)
        if combo_max >= 10:
            base_xp += 25
        elif combo_max >= 5:
            base_xp += 10

        # 시간 보너스
        if time_bonus:
            base_xp = int(base_xp * 1.1)

        return base_xp

    def get_level_for_xp(self, total_xp: int) -> int:
        """XP에 해당하는 레벨 계산."""
        current_level = 1
        for level, required_xp in LEVEL_XP_REQUIREMENTS.items():
            if total_xp >= required_xp:
                current_level = level
            else:
                break
        return min(current_level, MAX_LEVEL)

    def check_level_up(
        self,
        current_level: int,
        current_xp: int,
        xp_earned: int,
    ) -> dict:
        """레벨업 체크."""
        new_total_xp = current_xp + xp_earned
        new_level = self.get_level_for_xp(new_total_xp)

        if new_level > current_level:
            return {
                "level_up": True,
                "new_level": new_level,
                "total_xp": new_total_xp,
            }

        return {
            "level_up": False,
            "new_level": None,
            "total_xp": new_total_xp,
        }

    def update_streak(
        self,
        current_streak: int,
        last_activity_date: str | None,
        today: str,
    ) -> dict:
        """스트릭 업데이트."""
        if not last_activity_date:
            return {"new_streak": 1, "streak_broken": False}

        last_date = datetime.fromisoformat(last_activity_date).date()
        today_date = datetime.fromisoformat(today).date()
        diff = (today_date - last_date).days

        if diff == 0:
            # 같은 날 - 스트릭 유지
            return {"new_streak": current_streak, "streak_broken": False}
        elif diff == 1:
            # 연속 - 스트릭 증가
            return {"new_streak": current_streak + 1, "streak_broken": False}
        else:
            # 끊김 - 스트릭 리셋
            return {"new_streak": 1, "streak_broken": True}

    def update_user_gamification(
        self,
        user: User,
        xp_earned: int,
        today: str,
    ) -> dict:
        """사용자 게이미피케이션 정보 업데이트."""
        if not self.db:
            raise ValueError("Database session required")

        # 레벨업 체크
        level_result = self.check_level_up(
            current_level=user.level,
            current_xp=user.total_xp,
            xp_earned=xp_earned,
        )

        # 스트릭 업데이트
        last_activity = (
            user.last_activity_date.isoformat()
            if user.last_activity_date
            else None
        )
        streak_result = self.update_streak(
            current_streak=user.current_streak,
            last_activity_date=last_activity,
            today=today,
        )

        # 사용자 업데이트
        user.total_xp = level_result["total_xp"]
        if level_result["level_up"]:
            user.level = level_result["new_level"]

        user.current_streak = streak_result["new_streak"]
        user.max_streak = max(user.max_streak, streak_result["new_streak"])
        user.last_activity_date = datetime.fromisoformat(today)

        self.db.commit()

        return {
            "level_up": level_result["level_up"],
            "new_level": level_result["new_level"],
            "total_xp": level_result["total_xp"],
            "current_streak": streak_result["new_streak"],
            "streak_broken": streak_result["streak_broken"],
        }
