"""통계 API 엔드포인트."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import (
    ApiResponse,
    DashboardStats,
    Grade,
    PaginatedResponse,
    StudentStats,
    StudentStatsSummary,
    StudentDetailStats,
    ClassDetailStats,
    ConceptDetailStat,
    RecentTest,
    DailyActivity,
    TopStudent,
    DailyClassStat,
    TodayStats,
    WeekStats,
    UserResponse,
)
from app.schemas.common import UserRole
from app.services.stats_service import StatsService
from app.api.v1.auth import get_current_user, require_role

router = APIRouter(prefix="/stats", tags=["stats"])


def get_stats_service(db: Session = Depends(get_db)) -> StatsService:
    """통계 서비스 의존성."""
    return StatsService(db)


@router.get("/me", response_model=ApiResponse[StudentStats])
async def get_my_stats(
    current_user: UserResponse = Depends(get_current_user),
    stats_service: StatsService = Depends(get_stats_service),
):
    """내 통계 조회 (학생용)."""
    stats = stats_service.get_student_stats(current_user.id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "통계를 찾을 수 없습니다.",
                },
            },
        )

    return ApiResponse(data=StudentStats(**stats))


@router.get("/dashboard", response_model=ApiResponse[DashboardStats])
async def get_dashboard(
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    stats_service: StatsService = Depends(get_stats_service),
):
    """대시보드 통계 (강사용)."""
    stats = stats_service.get_dashboard_stats(current_user.id)

    return ApiResponse(
        data=DashboardStats(
            today=TodayStats(**stats["today"]),
            this_week=WeekStats(**stats["this_week"]),
            alerts=[],  # TODO: 알림 스키마 매핑
        )
    )


@router.get("/students", response_model=ApiResponse[PaginatedResponse[StudentStatsSummary]])
async def get_students_stats(
    class_id: str | None = Query(None, description="반 ID 필터"),
    grade: Grade | None = Query(None, description="학년 필터"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    stats_service: StatsService = Depends(get_stats_service),
):
    """학생 통계 목록 (강사용)."""
    students, total = stats_service.get_students_summary(
        teacher_id=current_user.id,
        class_id=class_id,
        grade=grade,
        page=page,
        page_size=page_size,
    )

    total_pages = (total + page_size - 1) // page_size

    items = [
        StudentStatsSummary(
            user_id=s["user_id"],
            name=s["name"],
            grade=s["grade"],
            class_name=s["class_name"],
            level=s["level"],
            total_xp=s["total_xp"],
            accuracy_rate=s["accuracy_rate"],
            tests_completed=s["tests_completed"],
            current_streak=s["current_streak"],
            last_activity_at=s["last_activity_at"],
        )
        for s in students
    ]

    return ApiResponse(
        data=PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
    )


@router.get("/students/{student_id}", response_model=ApiResponse[StudentDetailStats])
async def get_student_detail(
    student_id: str,
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    stats_service: StatsService = Depends(get_stats_service),
):
    """학생 상세 통계 (강사용)."""
    stats = stats_service.get_student_detail(student_id, current_user.id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "학생을 찾을 수 없습니다.",
                },
            },
        )

    return ApiResponse(
        data=StudentDetailStats(
            **{
                **stats,
                "recent_tests": [RecentTest(**t) for t in stats["recent_tests"]],
                "daily_activity": [DailyActivity(**d) for d in stats["daily_activity"]],
            }
        )
    )


@router.get("/class/{class_id}", response_model=ApiResponse[ClassDetailStats])
async def get_class_stats(
    class_id: str,
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    stats_service: StatsService = Depends(get_stats_service),
):
    """반 통계 (강사용)."""
    stats = stats_service.get_class_stats(class_id, current_user.id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "반을 찾을 수 없습니다.",
                },
            },
        )

    if stats.get("error") == "forbidden":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "error": {
                    "code": "FORBIDDEN",
                    "message": "해당 반에 접근 권한이 없습니다.",
                },
            },
        )

    return ApiResponse(
        data=ClassDetailStats(
            class_id=stats["class_id"],
            class_name=stats["class_name"],
            teacher_name=stats["teacher_name"],
            grade=stats["grade"],
            student_count=stats["student_count"],
            average_accuracy=stats["average_accuracy"],
            average_level=stats["average_level"],
            tests_completed_today=stats["tests_completed_today"],
            weak_concepts=stats["weak_concepts"],
            top_students=[TopStudent(**s) for s in stats["top_students"]],
            concept_stats=stats["concept_stats"],
            daily_stats=[DailyClassStat(**d) for d in stats["daily_stats"]],
        )
    )


@router.get("/concepts", response_model=ApiResponse[list[ConceptDetailStat]])
async def get_concept_stats(
    grade: Grade | None = Query(None, description="학년 필터"),
    class_id: str | None = Query(None, description="반 ID 필터"),
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    stats_service: StatsService = Depends(get_stats_service),
):
    """개념별 통계 (강사용)."""
    stats = stats_service.get_concept_stats(current_user.id, grade, class_id)

    return ApiResponse(
        data=[
            ConceptDetailStat(
                concept_id=s["concept_id"],
                concept_name=s["concept_name"],
                grade=s["grade"],
                total_questions=s["total_questions"],
                correct_count=s["correct_count"],
                accuracy_rate=s["accuracy_rate"],
                student_count=s["student_count"],
                average_time_seconds=s["average_time_seconds"],
                difficulty_distribution=s["difficulty_distribution"],
            )
            for s in stats
        ]
    )
