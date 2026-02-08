import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.mission_service import MissionService
from app.models.daily_mission import DailyMission
from app.models.user import User

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.mark.asyncio
async def test_get_daily_missions_creates_if_none(mock_db):
    # Setup
    service = MissionService(mock_db)
    student_id = "student-123"
    
    # Mock execute result for existing missions (return empty first)
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = []
    mock_db.execute.return_value = mock_result
    
    # Run
    missions = await service.get_daily_missions(student_id)
    
    # Verify
    assert len(missions) == 3
    # Check if add was called 3 times
    assert mock_db.add.call_count == 3
    # Check if commit was called
    assert mock_db.commit.called

@pytest.mark.asyncio
async def test_update_mission_progress(mock_db):
    # Setup
    service = MissionService(mock_db)
    student_id = "student-123"
    
    # Mock existing mission
    mission = DailyMission(
        id="mission-1",
        student_id=student_id,
        type="complete_tests",
        target_count=3,
        current_count=1,
        is_completed=False
    )
    
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = [mission]
    mock_db.execute.return_value = mock_result
    
    # Run
    await service.update_mission_progress(student_id, "complete_tests", 1)
    
    # Verify
    assert mission.current_count == 2
    assert mission.is_completed is False
    assert mock_db.commit.called

@pytest.mark.asyncio
async def test_claim_reward(mock_db):
    # Setup
    service = MissionService(mock_db)
    student_id = "student-123"
    
    # Mock completed mission
    mission = DailyMission(
        id="mission-1",
        student_id=student_id,
        type="complete_tests",
        reward_xp=100,
        is_completed=True,
        is_claimed=False
    )
    
    # Mock user
    user = User(id=student_id, total_xp=500)
    
    # Mock execute results
    # First query: get mission
    # Second query: get user
    mock_result_mission = MagicMock()
    mock_result_mission.scalar_one_or_none.return_value = mission
    
    mock_result_user = MagicMock()
    mock_result_user.scalar_one.return_value = user
    
    mock_db.execute.side_effect = [mock_result_mission, mock_result_user]
    
    # Run
    xp = await service.claim_reward("mission-1", student_id)
    
    # Verify
    assert xp == 100
    assert mission.is_claimed is True
    assert user.total_xp == 600
    assert mock_db.commit.called
