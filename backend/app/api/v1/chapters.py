"""단원 및 개념 숙련도 API."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.v1.auth import require_role
from app.schemas.common import ApiResponse, UserRole
from app.schemas.auth import UserResponse
from app.schemas.mastery import (
    ChapterProgressResponse,
    ChapterDetailResponse,
    ConceptMasteryResponse,
    RecommendationResponse,
    ApprovalRequest,
)
from app.services.chapter_service import ChapterService
from app.services.mastery_service import MasteryService

router = APIRouter()


@router.get("/progress", response_model=ApiResponse[list[ChapterProgressResponse]])
async def get_my_chapter_progress(
    current_user: UserResponse = Depends(require_role(UserRole.STUDENT)),
    grade: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """내 단원별 진행 상황 조회 (학생)."""
    service = ChapterService(db)
    chapters = await service.get_student_chapters(current_user.id, grade)

    return ApiResponse(
        success=True,
        data=chapters,
        message="단원 진행 상황 조회 성공",
    )


@router.get("/completion-status", response_model=ApiResponse[dict])
async def get_completion_status(
    current_user: UserResponse = Depends(require_role(UserRole.STUDENT)),
    grade: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """학기/학년 완료 상태 조회 (학생)."""
    service = ChapterService(db)

    if not grade:
        grade = current_user.grade

    if not grade:
        return ApiResponse(
            success=True,
            data={"semesters": {}, "grade": {}},
            message="학년 정보가 없습니다",
        )

    semester_status = await service.get_semester_completion_status(current_user.id, grade)
    grade_status = await service.get_grade_completion_status(current_user.id, grade)

    return ApiResponse(
        success=True,
        data={
            "semesters": semester_status,
            "grade": grade_status,
        },
        message="완료 상태 조회 성공",
    )


@router.get("/progress/{chapter_id}", response_model=ApiResponse[ChapterDetailResponse])
async def get_chapter_detail(
    chapter_id: str,
    current_user: UserResponse = Depends(require_role(UserRole.STUDENT)),
    db: AsyncSession = Depends(get_db),
):
    """단원 상세 정보 조회."""
    service = ChapterService(db)
    detail = await service.update_chapter_progress(current_user.id, chapter_id)

    if not detail:
        raise HTTPException(status_code=404, detail="단원을 찾을 수 없습니다")

    return ApiResponse(
        success=True,
        data=detail,
        message="단원 상세 조회 성공",
    )


@router.get("/concepts/mastery", response_model=ApiResponse[list[ConceptMasteryResponse]])
async def get_my_concept_mastery(
    current_user: UserResponse = Depends(require_role(UserRole.STUDENT)),
    grade: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """내 개념별 숙련도 조회."""
    service = MasteryService(db)
    masteries = await service.get_student_masteries(current_user.id, grade)

    return ApiResponse(
        success=True,
        data=masteries,
        message="개념 숙련도 조회 성공",
    )


@router.get("/recommendation", response_model=ApiResponse[RecommendationResponse | None])
async def get_next_recommendation(
    current_user: UserResponse = Depends(require_role(UserRole.STUDENT)),
    db: AsyncSession = Depends(get_db),
):
    """다음 학습 추천."""
    service = ChapterService(db)
    recommendation = await service.get_next_recommendation(current_user.id)

    return ApiResponse(
        success=True,
        data=recommendation,
        message="추천 조회 성공",
    )


@router.post("/{chapter_id}/approve", response_model=ApiResponse[dict])
async def approve_chapter_completion(
    chapter_id: str,
    request: ApprovalRequest,
    current_user: UserResponse = Depends(
        require_role(UserRole.TEACHER, UserRole.ADMIN, UserRole.MASTER)
    ),
    db: AsyncSession = Depends(get_db),
):
    """단원 완료 승인 (선생님)."""
    service = ChapterService(db)

    success = await service.approve_chapter(
        request.student_id,
        chapter_id,
        current_user.id,
        request.feedback,
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="승인 조건을 충족하지 못했습니다 (60점 이상 필요)",
        )

    return ApiResponse(
        success=True,
        data={"approved": True},
        message="단원 완료 승인됨",
    )


@router.get("/students/{student_id}/progress", response_model=ApiResponse[list[ChapterProgressResponse]])
async def get_student_chapter_progress(
    student_id: str,
    current_user: UserResponse = Depends(
        require_role(UserRole.TEACHER, UserRole.ADMIN, UserRole.MASTER)
    ),
    grade: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """특정 학생의 단원 진행 상황 조회 (선생님)."""
    service = ChapterService(db)
    chapters = await service.get_student_chapters(student_id, grade)

    return ApiResponse(
        success=True,
        data=chapters,
        message="학생 단원 진행 상황 조회 성공",
    )


@router.post("/students/{student_id}/unlock/{chapter_id}", response_model=ApiResponse[dict])
async def toggle_chapter_unlock(
    student_id: str,
    chapter_id: str,
    current_user: UserResponse = Depends(
        require_role(UserRole.TEACHER, UserRole.ADMIN, UserRole.MASTER)
    ),
    db: AsyncSession = Depends(get_db),
):
    """단원 해금/잠금 토글 (관리자)."""
    from app.models.chapter_progress import ChapterProgress
    from app.models.chapter import Chapter
    from sqlalchemy import select
    from datetime import datetime, timezone

    chapter = await db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="단원을 찾을 수 없습니다")

    stmt = select(ChapterProgress).where(
        ChapterProgress.student_id == student_id,
        ChapterProgress.chapter_id == chapter_id,
    )
    progress = await db.scalar(stmt)

    if progress and progress.is_unlocked:
        # 이미 해금됨 → 잠금
        progress.is_unlocked = False
        progress.unlocked_at = None
        await db.commit()
        return ApiResponse(
            success=True,
            data={"chapter_id": chapter_id, "is_unlocked": False},
            message=f"'{chapter.name}' 단원이 잠금 처리되었습니다",
        )
    else:
        # 잠금 → 해금
        if not progress:
            progress = ChapterProgress(
                student_id=student_id,
                chapter_id=chapter_id,
                is_unlocked=True,
                unlocked_at=datetime.now(timezone.utc),
            )
            db.add(progress)
        else:
            progress.is_unlocked = True
            progress.unlocked_at = datetime.now(timezone.utc)
        await db.commit()
        return ApiResponse(
            success=True,
            data={"chapter_id": chapter_id, "is_unlocked": True},
            message=f"'{chapter.name}' 단원이 해금되었습니다",
        )


# ===== 진단 평가 (Placement Test) =====

@router.get("/placement/test", response_model=ApiResponse[dict])
async def get_placement_test(
    current_user: UserResponse = Depends(require_role(UserRole.STUDENT)),
    db: AsyncSession = Depends(get_db),
):
    """진단 평가 테스트 정보 조회."""
    from app.services.placement_service import PlacementService

    service = PlacementService(db)
    placement_test = await service.get_placement_test()

    if not placement_test:
        raise HTTPException(status_code=404, detail="진단 평가 테스트를 찾을 수 없습니다")

    return ApiResponse(
        success=True,
        data=placement_test,
        message="진단 평가 테스트 조회 성공",
    )


@router.post("/placement/complete/{attempt_id}", response_model=ApiResponse[dict])
async def complete_placement_test(
    attempt_id: str,
    current_user: UserResponse = Depends(require_role(UserRole.STUDENT)),
    db: AsyncSession = Depends(get_db),
):
    """진단 평가 완료 및 배치 적용."""
    from app.services.placement_service import PlacementService

    service = PlacementService(db)

    # 결과 분석
    result = await service.analyze_placement_result(attempt_id)

    if not result:
        raise HTTPException(status_code=400, detail="진단 평가 결과를 분석할 수 없습니다")

    # 배치 적용
    success = await service.apply_placement(current_user.id, attempt_id)

    if not success:
        raise HTTPException(status_code=500, detail="배치 적용에 실패했습니다")

    return ApiResponse(
        success=True,
        data=result,
        message="진단 평가 완료! 맞춤 학습 경로가 설정되었습니다",
    )


@router.get("/placement/status", response_model=ApiResponse[dict])
async def get_placement_status(
    current_user: UserResponse = Depends(require_role(UserRole.STUDENT)),
    db: AsyncSession = Depends(get_db),
):
    """진단 평가 완료 여부 및 결과 조회."""
    from app.models.user import User

    user = await db.get(User, current_user.id)

    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    return ApiResponse(
        success=True,
        data={
            "has_completed": user.has_completed_placement,
            "placement_result": user.placement_result,
        },
        message="진단 평가 상태 조회 성공",
    )
