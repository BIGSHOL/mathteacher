"""일일 테스트 API 엔드포인트."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import (
    ApiResponse,
    PaginatedResponse,
    UserResponse,
)
from app.schemas.daily_test import (
    CATEGORY_LABELS,
    DailyTestRecordResponse,
    DailyTestStartResponse,
    DailyTestTodayResponse,
)
from app.services.daily_test_service import DailyTestService
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/daily-tests", tags=["daily-tests"])


def get_daily_test_service(db: AsyncSession = Depends(get_db)) -> DailyTestService:
    """일일 테스트 서비스 의존성."""
    return DailyTestService(db)


async def _to_response(record, db: AsyncSession) -> DailyTestRecordResponse:
    """DailyTestRecord → Response 변환."""
    from app.models.test import Test

    test = await db.get(Test, record.test_id)
    question_count = test.question_count if test else 0

    return DailyTestRecordResponse(
        id=record.id,
        date=record.date,
        category=record.category,
        category_label=CATEGORY_LABELS.get(record.category, record.category),
        status=record.status,
        test_id=record.test_id,
        attempt_id=record.attempt_id,
        score=record.score,
        max_score=record.max_score,
        correct_count=record.correct_count,
        total_count=record.total_count,
        completed_at=record.completed_at,
        question_count=question_count,
    )


@router.get("/today", response_model=ApiResponse[DailyTestTodayResponse])
async def get_today_tests(
    current_user: UserResponse = Depends(get_current_user),
    service: DailyTestService = Depends(get_daily_test_service),
    db: AsyncSession = Depends(get_db),
):
    """오늘의 일일 테스트 3개 조회 (없으면 자동 생성)."""
    records, ai_count = await service.get_today_tests(current_user.id)
    return ApiResponse(
        data=DailyTestTodayResponse(
            date=service.get_today_str(),
            tests=[await _to_response(r, db) for r in records],
            ai_generated_count=ai_count,
        )
    )


@router.post(
    "/{record_id}/start",
    response_model=ApiResponse[DailyTestStartResponse],
)
async def start_daily_test(
    record_id: str,
    current_user: UserResponse = Depends(get_current_user),
    service: DailyTestService = Depends(get_daily_test_service),
):
    """일일 테스트 시작."""
    attempt = await service.start_daily_test(current_user.id, record_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "CANNOT_START",
                    "message": "테스트를 시작할 수 없습니다.",
                },
            },
        )
    return ApiResponse(data=DailyTestStartResponse(attempt_id=attempt.id))


@router.get(
    "/history",
    response_model=ApiResponse[PaginatedResponse[DailyTestRecordResponse]],
)
async def get_daily_test_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(30, ge=1, le=100),
    current_user: UserResponse = Depends(get_current_user),
    service: DailyTestService = Depends(get_daily_test_service),
    db: AsyncSession = Depends(get_db),
):
    """일일 테스트 이력 조회 (오늘 제외)."""
    records, total = await service.get_history(current_user.id, page, page_size)
    total_pages = (total + page_size - 1) // page_size

    return ApiResponse(
        data=PaginatedResponse(
            items=[await _to_response(r, db) for r in records],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
    )
