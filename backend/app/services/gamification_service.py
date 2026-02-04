"""게이미피케이션 서비스."""

from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

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
MAX_DEFENSE = 3  # 레벨다운 방어 실드 최대 개수


class GamificationService:
    """게이미피케이션 서비스."""

    def __init__(self, db: AsyncSession | None = None):
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

    def calculate_adaptive_level(
        self,
        current_level: int,
        final_difficulty: int,
        correct_count: int,
        total_count: int,
    ) -> int | None:
        """적응형 테스트 결과로 학생 레벨 산출.

        계획서 섹션 7.3:
          10문제 후 최종 레벨 산출 → 학생의 level 업데이트

        규칙:
          - 정답률 50% 이상이면 final_difficulty를 demonstrated_level로 간주
          - demonstrated_level이 현재 레벨보다 높으면 레벨업
          - 정답률 70% 이상이면 demonstrated_level 그대로
          - 정답률 50~70%이면 demonstrated_level - 1 (약간 보수적)
          - 레벨 하락은 없음 (non-punitive)
        """
        if total_count == 0:
            return None

        accuracy = correct_count / total_count

        if accuracy < 0.5:
            return None  # 정답률 낮으면 레벨 변경 안 함

        if accuracy >= 0.7:
            demonstrated = final_difficulty
        else:
            demonstrated = max(final_difficulty - 1, 1)

        if demonstrated > current_level:
            return min(demonstrated, MAX_LEVEL)

        return None  # 현재 레벨 이하이면 변경 안 함

    def check_level_down(
        self,
        user: User,
        final_difficulty: int,
        correct_count: int,
        total_count: int,
    ) -> dict:
        """레벨다운 체크 (방어 시스템 포함).

        발동 조건 (매우 엄격):
          - 정답률 < 30%
          - 최종 난이도가 현재 레벨보다 2 이상 낮음
          - 현재 레벨이 2 이상 (레벨 1은 다운 불가)

        방어 시스템:
          - 방어 실드 3개 (level_down_defense)
          - 심각한 실패 시 실드 1개 소모
          - 실드 0에서 다시 심각한 실패 → 레벨 1 하락 + 실드 리셋
          - 정답률 >= 60% → 실드 1개 회복 (최대 3)

        Returns:
            {"action": "none"}
            {"action": "defense_restored", "defense_remaining": int}
            {"action": "defense_consumed", "defense_remaining": int}
            {"action": "level_down", "new_level": int, "defense_remaining": int}
        """
        if total_count == 0:
            return {"action": "none"}

        accuracy = correct_count / total_count

        # 실드 회복: 적응형에서 정답률 60% 이상이면 실드 1개 회복
        if accuracy >= 0.6:
            if user.level_down_defense < MAX_DEFENSE:
                user.level_down_defense = min(user.level_down_defense + 1, MAX_DEFENSE)
                return {
                    "action": "defense_restored",
                    "defense_remaining": user.level_down_defense,
                }
            return {"action": "none"}

        # 레벨다운 발동 조건: 정답률 30% 미만 AND 갭 2 이상 AND 레벨 2 이상
        gap = user.level - final_difficulty
        if accuracy >= 0.3 or gap < 2 or user.level <= 1:
            return {"action": "none"}

        # 심각한 실패 감지 → 방어 실드 처리
        if user.level_down_defense > 0:
            user.level_down_defense -= 1
            return {
                "action": "defense_consumed",
                "defense_remaining": user.level_down_defense,
            }
        else:
            # 실드 모두 소진 → 레벨 다운
            new_level = max(user.level - 1, 1)
            user.level_down_defense = MAX_DEFENSE  # 실드 리셋
            return {
                "action": "level_down",
                "new_level": new_level,
                "defense_remaining": MAX_DEFENSE,
            }

    async def update_user_gamification(
        self,
        user: User,
        xp_earned: int,
        today: str,
        adaptive_result: dict | None = None,
    ) -> dict:
        """사용자 게이미피케이션 정보 업데이트.

        Args:
            adaptive_result: 적응형 테스트 결과
                {"final_difficulty": int, "correct_count": int, "total_count": int}
        """
        if not self.db:
            raise ValueError("Database session required")

        # 레벨업 체크 (XP 기반)
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
        xp_level = level_result["new_level"] if level_result["level_up"] else user.level

        # 적응형 테스트 결과 반영
        adaptive_level = None
        level_down_result = None
        if adaptive_result:
            # 레벨업 체크 (계획서 7.3)
            adaptive_level = self.calculate_adaptive_level(
                current_level=user.level,
                final_difficulty=adaptive_result["final_difficulty"],
                correct_count=adaptive_result["correct_count"],
                total_count=adaptive_result["total_count"],
            )
            # 레벨다운 체크 (방어 시스템)
            level_down_result = self.check_level_down(
                user=user,
                final_difficulty=adaptive_result["final_difficulty"],
                correct_count=adaptive_result["correct_count"],
                total_count=adaptive_result["total_count"],
            )

        # 최종 레벨 결정
        final_level = xp_level
        level_up = False
        level_down = False

        if adaptive_level and adaptive_level > final_level:
            # 레벨업 우선
            final_level = adaptive_level
        elif level_down_result and level_down_result["action"] == "level_down":
            # 레벨다운 (실드 모두 소진)
            final_level = level_down_result["new_level"]
            level_down = True

        level_up = final_level > user.level
        if level_down:
            level_up = False  # 레벨다운 시 레벨업 플래그 무시
        user.level = final_level

        user.current_streak = streak_result["new_streak"]
        user.max_streak = max(user.max_streak, streak_result["new_streak"])
        user.last_activity_date = datetime.fromisoformat(today)

        await self.db.commit()

        return {
            "level_up": level_up,
            "level_down": level_down,
            "new_level": final_level if (level_up or level_down) else None,
            "total_xp": level_result["total_xp"],
            "current_streak": streak_result["new_streak"],
            "streak_broken": streak_result["streak_broken"],
            "level_down_defense": user.level_down_defense,
            "level_down_action": level_down_result["action"] if level_down_result else "none",
        }
