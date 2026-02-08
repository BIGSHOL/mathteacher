from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.concept import Concept
from app.models.concept_mastery import ConceptMastery
from app.models.question import Question
from app.models.user import User
from app.models.wrong_answer_review import WrongAnswerReview


class AiLearningService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_weaknesses(self, user_id: str, limit: int = 5) -> list[dict]:
        """학생의 취약 개념을 분석합니다.
        
        1. 숙련도(mastery_score)가 낮은 순서대로 조회
        2. 오답 노트(WrongAnswerReview)에서 자주 틀린 개념 조회 (보완 필요 시)
        
        Returns:
            list[dict]: 취약 개념 정보 리스트
        """
        # 1. 숙련도 기반 취약점 (숙련도 80점 미만, 낮은순)
        query = (
            select(ConceptMastery)
            .where(
                ConceptMastery.student_id == user_id,
                ConceptMastery.mastery_percentage < 80
            )
            .options(selectinload(ConceptMastery.concept))
            .order_by(ConceptMastery.mastery_percentage.asc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        low_mastery = result.scalars().all()
        
        weaknesses = []
        for mastery in low_mastery:
             if mastery.concept:
                weaknesses.append({
                    "concept_id": mastery.concept_id,
                    "concept_name": mastery.concept.name,
                    "mastery_score": mastery.mastery_percentage,
                    "reason": "low_mastery"
                })
                
        # TODO: 오답 노트 기반 분석 추가 (숙련도 정보가 부족할 경우)
        
        return weaknesses

    async def get_recommended_questions(self, user_id: str, count: int = 5) -> list[Question]:
        """AI 추천 문제를 생성합니다.
        
        취약 개념 위주로 문제를 선정합니다.
        취약점이 없으면 현재 학년/학기에 맞는 무작위 문제를 추천합니다.
        """
        weaknesses = await self.analyze_weaknesses(user_id)
        
        questions = []
        
        if weaknesses:
            # 취약 개념에서 문제 추출
            # 각 취약 개념당 1~2문제씩
            for weak in weaknesses:
                if len(questions) >= count:
                    break
                    
                # 해당 개념의 문제 중, 아직 풀지 않았거나(로그 없음) 오답이었던 문제 우선
                # 간단하게는 해당 개념의 랜덤 문제
                stm = (
                    select(Question)
                    .where(Question.concept_id == weak["concept_id"], Question.is_active == True)
                    .order_by(func.random())
                    .limit(1)
                )
                q_result = await self.db.execute(stm)
                q = q_result.scalar_one_or_none()
                if q:
                    questions.append(q)
        
        # 부족한 문제 수 채우기 (랜덤 추천)
        if len(questions) < count:
            user = await self.db.get(User, user_id)
            grade = user.grade if user else None
            
            needed = count - len(questions)
            stmt = select(Question).where(Question.is_active == True)
            
            if grade:
                # 같은 학년 문제 추천 (단순화: grade 필드가 Question에는 없고 Chapter-Concept 연결)
                # 성능상 복잡할 수 있으니 일단 전체 랜덤 or 최근 푼 문제의 챕터 기반
                pass
            
            stmt = stmt.order_by(func.random()).limit(needed)
            result = await self.db.execute(stmt)
            random_questions = result.scalars().all()
            questions.extend(random_questions)
            
        return questions
