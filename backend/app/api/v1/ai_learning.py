from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.ai_learning_service import AiLearningService

router = APIRouter(prefix="/ai-learning", tags=["ai-learning"])


@router.get("/recommendations")
async def get_recommendations(
    count: int = 3,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """AI 맞춤형 추천 문제를 조회합니다."""
    service = AiLearningService(db)
    questions = await service.get_recommended_questions(current_user.id, count)
    
    data = []
    for q in questions:
        data.append({
            "id": q.id,
            "content": q.content,
            "answer": q.answer, # 실제 서비스에선 정답 노출 주의 (프론트에서 체점에 사용하거나 숨김)
            "difficulty": q.difficulty,
            "concept_id": q.concept_id,
            # 필요한 필드 추가
        })
        
    # 취약점 분석 정보도 함께 반환하면 좋음
    weaknesses = await service.analyze_weaknesses(current_user.id, limit=3)
    
    return {
        "success": True, 
        "data": {
            "questions": data,
            "weaknesses": weaknesses
        }
    }
