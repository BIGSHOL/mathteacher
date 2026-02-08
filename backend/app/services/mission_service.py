from datetime import datetime, date
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.daily_mission import DailyMission
from app.models.user import User

class MissionService:
    MISSION_TYPES = {
        "complete_tests": {
            "title": "테스트 {count}회 완료하기",
            "counts": [1, 2, 3],
            "xp": [50, 100, 150]
        },
        "solve_questions": {
            "title": "문제 {count}개 풀기",
            "counts": [10, 20, 30],
            "xp": [50, 100, 150]
        },
        "perfect_score": {
            "title": "만점 {count}번 받기",
            "counts": [1],
            "xp": [200]
        },
        "login": {
            "title": "로그인 하기",
            "counts": [1],
            "xp": [10]
        }
    }

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_daily_missions(self, student_id: str) -> list[DailyMission]:
        """오늘의 미션을 조회하고, 없으면 생성합니다."""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 오늘 생성된 미션 조회
        query = select(DailyMission).where(
            DailyMission.student_id == student_id,
            DailyMission.created_at >= today_start
        )
        result = await self.db.execute(query)
        missions = result.scalars().all()
        
        if not missions:
            missions = await self._generate_daily_missions(student_id)
            
        return missions

    async def _generate_daily_missions(self, student_id: str) -> list[DailyMission]:
        """새로운 일일 미션 3개를 생성합니다."""
        # 로그인 미션은 고정? 아니면 랜덤 3개? 
        # 일단 랜덤 3개 (로그인 제외하고 테스트/문제풀이 위주로)
        pool = ["complete_tests", "solve_questions", "perfect_score"]
        selected_types = random.choices(pool, k=3)
        # 중복 방지 로직이 필요하다면 sample 사용, 하지만 여기선 같은 타입이 나와도 count가 다르면 OK
        # 간단하게 sample로 서로 다른 3개 타입 선택 (타입이 3개밖에 없으므로 다 선택됨)
        selected_types = ["complete_tests", "solve_questions", "perfect_score"]
        
        new_missions = []
        for m_type in selected_types:
            def_idx = random.randint(0, len(self.MISSION_TYPES[m_type]["counts"]) - 1)
            count = self.MISSION_TYPES[m_type]["counts"][def_idx]
            xp = self.MISSION_TYPES[m_type]["xp"][def_idx]
            title = self.MISSION_TYPES[m_type]["title"].format(count=count)
            
            mission = DailyMission(
                student_id=student_id,
                type=m_type,
                title=title,
                target_count=count,
                reward_xp=xp
            )
            self.db.add(mission)
            new_missions.append(mission)
            
        await self.db.commit()
        return new_missions

    async def update_mission_progress(self, student_id: str, action_type: str, count: int = 1):
        """미션 진행도를 업데이트합니다."""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        query = select(DailyMission).where(
            DailyMission.student_id == student_id,
            DailyMission.created_at >= today_start,
            DailyMission.type == action_type,
            DailyMission.is_completed == False
        )
        result = await self.db.execute(query)
        missions = result.scalars().all()
        
        for mission in missions:
            mission.current_count += count
            if mission.current_count >= mission.target_count:
                mission.current_count = mission.target_count
                mission.is_completed = True
                # 자동 보상 지급? 아니면 수동 수령? -> 수동 수령(claim) 방식이 일반적
                # 여기서는 완료 상태만 변경
        
        if missions:
            await self.db.commit()

    async def claim_reward(self, mission_id: str, student_id: str) -> int:
        """미션 보상을 수령합니다."""
        query = select(DailyMission).where(
            DailyMission.id == mission_id,
            DailyMission.student_id == student_id,
            DailyMission.is_completed == True,
            DailyMission.is_claimed == False
        )
        result = await self.db.execute(query)
        mission = result.scalar_one_or_none()
        
        if not mission:
            return 0
            
        mission.is_claimed = True
        
        # 유저 XP 증가
        user_query = select(User).where(User.id == student_id)
        user_result = await self.db.execute(user_query)
        user = user_result.scalar_one()
        user.total_xp += mission.reward_xp
        
        await self.db.commit()
        return mission.reward_xp
