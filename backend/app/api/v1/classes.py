"""반 관리 API 엔드포인트."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.class_ import Class
from app.schemas import ApiResponse, PaginatedResponse, QuotaUpdateRequest
from app.schemas.common import UserRole
from app.schemas.auth import UserResponse
from app.api.v1.auth import require_role
from pydantic import BaseModel


router = APIRouter(prefix="/classes", tags=["classes"])


class ClassResponse(BaseModel):
    """반 응답 스키마."""
    id: str
    name: str
    grade: str
    teacher_id: str
    description: str | None = None
    daily_quota: int = 20
    quota_carry_over: bool = False

    model_config = {"from_attributes": True}


@router.get("", response_model=ApiResponse[PaginatedResponse[ClassResponse]])
async def get_classes(
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN, UserRole.MASTER)),
    db: AsyncSession = Depends(get_db),
):
    """반 목록 조회 (강사/관리자 전용)."""
    stmt = select(Class)

    # 강사인 경우 자신의 반만 조회
    if current_user.role == UserRole.TEACHER:
        stmt = stmt.where(Class.teacher_id == current_user.id)

    stmt = stmt.order_by(Class.name)
    classes = list((await db.scalars(stmt)).all())

    return ApiResponse(
        data=PaginatedResponse(
            items=[ClassResponse.model_validate(c) for c in classes],
            total=len(classes),
            page=1,
            page_size=100,
            total_pages=1,
        )
    )


@router.patch("/{class_id}/quota", response_model=ApiResponse[ClassResponse])
async def update_class_quota(
    class_id: str,
    request: QuotaUpdateRequest,
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN, UserRole.MASTER)),
    db: AsyncSession = Depends(get_db),
):
    """반 할당량 설정 (강사/관리자 전용)."""
    cls = await db.get(Class, class_id)
    if not cls:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {"code": "NOT_FOUND", "message": "반을 찾을 수 없습니다."},
            },
        )

    # 강사는 자기 반만 수정 가능
    if current_user.role == UserRole.TEACHER and cls.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "error": {"code": "FORBIDDEN", "message": "접근 권한이 없습니다."},
            },
        )

    cls.daily_quota = request.daily_quota
    cls.quota_carry_over = request.quota_carry_over
    await db.commit()
    await db.refresh(cls)

    return ApiResponse(data=ClassResponse.model_validate(cls))
