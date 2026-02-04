"""문제 신고 API 엔드포인트."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func as sa_func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user, require_role
from app.core.database import get_db
from app.models.question import Question
from app.models.question_report import QuestionReport
from app.schemas import ApiResponse, PaginatedResponse, UserResponse
from app.schemas.common import ReportStatus, ReportType

router = APIRouter(prefix="/question-reports", tags=["question-reports"])


# ===========================
# Request / Response DTOs
# ===========================


class CreateReportRequest(BaseModel):
    question_id: str
    report_type: ReportType
    comment: str = Field(min_length=1, max_length=2000)


class ResolveReportRequest(BaseModel):
    status: ReportStatus = Field(description="resolved 또는 dismissed")
    admin_response: str | None = None


class ReportResponse(BaseModel):
    id: str
    question_id: str
    question_content: str | None = None
    reporter_id: str
    reporter_name: str | None = None
    report_type: str
    comment: str
    status: str
    admin_response: str | None = None
    resolved_by: str | None = None
    reviewer_name: str | None = None
    resolved_at: str | None = None
    created_at: str
    updated_at: str


# ===========================
# 엔드포인트
# ===========================


@router.post("", response_model=ApiResponse[ReportResponse], status_code=status.HTTP_201_CREATED)
async def create_question_report(
    payload: CreateReportRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """문제 신고 등록 (로그인 사용자 전원)."""
    # 문제 존재 확인
    question = await db.get(Question, payload.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {"code": "QUESTION_NOT_FOUND", "message": "해당 문제를 찾을 수 없습니다."},
            },
        )

    # 중복 방지: 같은 user + question 에 대해 pending 상태 신고가 있으면 기존 것 반환
    existing = await db.scalar(
        select(QuestionReport).where(
            QuestionReport.reporter_id == current_user.id,
            QuestionReport.question_id == payload.question_id,
            QuestionReport.status == ReportStatus.PENDING,
        )
    )
    if existing:
        return ApiResponse(data=_to_response(existing))

    report = QuestionReport(
        question_id=payload.question_id,
        reporter_id=current_user.id,
        report_type=payload.report_type,
        comment=payload.comment,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)

    return ApiResponse(data=_to_response(report))


@router.get("", response_model=ApiResponse[PaginatedResponse[ReportResponse]])
async def list_question_reports(
    report_status: ReportStatus | None = Query(None, alias="status", description="상태 필터"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: UserResponse = Depends(require_role("teacher", "admin", "master")),
    db: AsyncSession = Depends(get_db),
):
    """신고 목록 조회 (teacher/admin/master)."""
    stmt = select(QuestionReport)

    if report_status:
        stmt = stmt.where(QuestionReport.status == report_status)

    # 총 개수
    count_stmt = select(sa_func.count()).select_from(stmt.subquery())
    total = await db.scalar(count_stmt) or 0

    # 페이징
    stmt = stmt.order_by(QuestionReport.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    reports = (await db.scalars(stmt)).unique().all()

    return ApiResponse(
        data=PaginatedResponse(
            items=[_to_response(r) for r in reports],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size if total else 0,
        )
    )


@router.patch("/{report_id}/resolve", response_model=ApiResponse[ReportResponse])
async def resolve_question_report(
    report_id: str,
    payload: ResolveReportRequest,
    current_user: UserResponse = Depends(require_role("admin", "master")),
    db: AsyncSession = Depends(get_db),
):
    """신고 처리 (admin/master)."""
    if payload.status == ReportStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {"code": "INVALID_STATUS", "message": "resolved 또는 dismissed만 가능합니다."},
            },
        )

    report = await db.get(QuestionReport, report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {"code": "REPORT_NOT_FOUND", "message": "해당 신고를 찾을 수 없습니다."},
            },
        )

    if report.status != ReportStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "ALREADY_PROCESSED",
                    "message": f"이미 {report.status.value} 상태인 신고는 변경할 수 없습니다.",
                },
            },
        )

    report.status = payload.status
    report.admin_response = payload.admin_response
    report.resolved_by = current_user.id
    report.resolved_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(report)

    return ApiResponse(data=_to_response(report))


# ===========================
# 헬퍼
# ===========================


def _to_response(r: QuestionReport) -> ReportResponse:
    return ReportResponse(
        id=r.id,
        question_id=r.question_id,
        question_content=r.question.content if r.question else None,
        reporter_id=r.reporter_id,
        reporter_name=r.reporter.name if r.reporter else None,
        report_type=r.report_type.value if hasattr(r.report_type, "value") else str(r.report_type),
        comment=r.comment,
        status=r.status.value if hasattr(r.status, "value") else str(r.status),
        admin_response=r.admin_response,
        resolved_by=r.resolved_by,
        reviewer_name=r.reviewer.name if r.reviewer else None,
        resolved_at=r.resolved_at.isoformat() if r.resolved_at else None,
        created_at=r.created_at.isoformat() if r.created_at else "",
        updated_at=r.updated_at.isoformat() if r.updated_at else "",
    )
