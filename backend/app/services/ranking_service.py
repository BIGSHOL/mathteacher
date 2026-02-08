from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.models.user import User

class RankingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_top_users(self, limit: int = 50, grade: str | None = None) -> list[dict]:
        """상위 유저 랭킹 조회."""
        query = select(User).where(User.role == 'student').order_by(desc(User.total_xp)).limit(limit)
        
        if grade:
             query = query.where(User.grade == grade)
             
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        return [
            {
                "rank": i + 1,
                "user_id": u.id,
                "name": u.name,
                "level": u.level,
                "total_xp": u.total_xp,
                "grade": u.grade,
                # "profile_image": u.profile_image # 추후 프로필 이미지 추가 시 연동
            }
            for i, u in enumerate(users)
        ]

    async def get_user_rank(self, user_id: str, grade: str | None = None) -> dict | None:
        """특정 유저의 랭킹 조회."""
        # 유저 정보 조회
        user_query = select(User).where(User.id == user_id)
        user_result = await self.db.execute(user_query)
        user = user_result.scalar_one_or_none()
        
        if not user:
            return None

        # 자신보다 XP가 높은 유저 수 카운트 (동점자 처리: 동일 등수로 할지, 순번으로 할지 결정 필요. 여기선 단순 count + 1)
        # 동점일 경우... ID순? 가입일순? 일단 단순하게 XP 크기로만 비교하면 동점자는 같은 등수가 아님 (count니까). 
        # 동점자 처리를 위해 >= 로 하거나 별도 로직이 필요하지만, MVP에서는 > 로 해서 동점자끼리의 순서는 운에 맡기거나(DB정렬), 
        # 정확히는 '나보다 잘한 사람 수 + 1' 이니까 동점자가 있으면 
        # A(100), B(100), Me(100) -> 나보다 큰사람 0명 -> 1등. 
        # 이러면 공동 1등이 됨. 이게 더 합리적.
        
        rank_query = select(func.count()).where(User.role == 'student', User.total_xp > user.total_xp)
        if grade:
            rank_query = rank_query.where(User.grade == grade)
            
        rank_result = await self.db.execute(rank_query)
        higher_rank_count = rank_result.scalar()
        
        return {
             "rank": higher_rank_count + 1,
             "user_id": user.id,
             "name": user.name,
             "level": user.level,
             "total_xp": user.total_xp,
             "grade": user.grade
        }
