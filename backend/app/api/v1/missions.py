from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas import ApiResponse, UserResponse
from app.api.v1.auth import get_current_user
from app.services.mission_service import MissionService
from app.models.daily_mission import DailyMission
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/missions", tags=["missions"])

class DailyMissionResponse(BaseModel):
    id: str
    type: str
    title: str
    target_count: int
    current_count: int
    is_completed: bool
    is_claimed: bool
    reward_xp: int
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=ApiResponse[list[DailyMissionResponse]])
async def get_my_missions(
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """내 일일 미션 조회."""
    service = MissionService(db)
    missions = await service.get_daily_missions(current_user.id)
    return ApiResponse(data=[DailyMissionResponse.model_validate(m) for m in missions])

@router.post("/{mission_id}/claim", response_model=ApiResponse[dict])
async def claim_mission_reward(
    mission_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """미션 보상 수령."""
    service = MissionService(db)
    xp_earned = await service.claim_reward(mission_id, current_user.id)
    
    if xp_earned == 0:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="보상을 수령할 수 없습니다. (미완료 또는 이미 수령함)"
        )
        
    return ApiResponse(data={"xp_earned": xp_earned})
