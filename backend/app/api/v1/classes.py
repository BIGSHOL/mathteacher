"""반 관리 API 엔드포인트."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.class_ import Class
from app.schemas import ApiResponse, PaginatedResponse
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

    model_config = {"from_attributes": True}


@router.get("", response_model=ApiResponse[PaginatedResponse[ClassResponse]])
async def get_classes(
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN, UserRole.MASTER)),
    db: Session = Depends(get_db),
):
    """반 목록 조회 (강사/관리자 전용)."""
    stmt = select(Class)

    # 강사인 경우 자신의 반만 조회
    if current_user.role == UserRole.TEACHER:
        stmt = stmt.where(Class.teacher_id == current_user.id)

    stmt = stmt.order_by(Class.name)
    classes = list(db.scalars(stmt).all())

    return ApiResponse(
        data=PaginatedResponse(
            items=[ClassResponse.model_validate(c) for c in classes],
            total=len(classes),
            page=1,
            page_size=100,
            total_pages=1,
        )
    )
