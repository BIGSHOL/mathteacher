"""관리자 전용 API (DB 초기화, 사용자 목록 등)."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, func

from app.core.database import get_db, sync_engine
from app.api.v1.auth import require_role
from app.schemas.common import ApiResponse, PaginatedResponse, UserRole
from app.schemas.auth import UserResponse
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/users", response_model=ApiResponse[PaginatedResponse[dict]])
async def list_users(
    role: Optional[str] = Query(None, description="역할 필터 (student, teacher, admin, master)"),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=500),
    current_user: UserResponse = Depends(
        require_role(UserRole.MASTER, UserRole.ADMIN)
    ),
    db: AsyncSession = Depends(get_db),
):
    """사용자 목록 조회 (관리자/마스터 전용)."""
    stmt = select(User)
    count_stmt = select(func.count(User.id))

    if role:
        stmt = stmt.where(User.role == role)
        count_stmt = count_stmt.where(User.role == role)

    # Total count
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # Paginated query
    offset = (page - 1) * page_size
    stmt = stmt.order_by(User.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(stmt)
    users = result.scalars().all()

    items = [
        {
            "id": u.id,
            "login_id": u.login_id,
            "name": u.name,
            "role": u.role.value if hasattr(u.role, 'value') else u.role,
            "grade": (u.grade.value if hasattr(u.grade, 'value') else u.grade) if u.grade else None,
            "class_id": u.class_id,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in users
    ]

    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return ApiResponse(
        success=True,
        data=PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        ),
    )


@router.post("/reset-db", response_model=ApiResponse[dict])
async def reset_database(
    current_user: UserResponse = Depends(
        require_role(UserRole.MASTER)
    ),
    db: AsyncSession = Depends(get_db),
):
    """DB 전체 초기화 후 시드 데이터 재생성 (마스터 전용).

    모든 테이블을 드롭하고 재생성 + 시드 데이터 로드.
    기존 모든 사용자/테스트 기록이 삭제됩니다.
    """
    from app.models import Base

    logger.warning(f"DB reset requested by user {current_user.id} ({current_user.name})")

    try:
        # 1) Drop all tables
        with sync_engine.connect() as conn:
            conn.execute(text("DROP SCHEMA public CASCADE"))
            conn.execute(text("CREATE SCHEMA public"))
            conn.commit()

        # 2) Recreate tables
        Base.metadata.create_all(bind=sync_engine)

        # 3) Re-run init_db (seeds users)
        import importlib
        main_module = importlib.import_module("app.main")
        main_module.init_db()

        # 4) Re-run load_seed_data (seeds concepts/questions)
        main_module.load_seed_data()

        logger.info("DB reset completed successfully")
        return ApiResponse(
            success=True,
            data={"reset": True},
            message="DB 초기화 완료! 시드 데이터가 재생성되었습니다. 다시 로그인해주세요.",
        )
    except Exception as e:
        logger.error(f"DB reset failed: {e}")
        raise HTTPException(status_code=500, detail=f"DB 초기화 실패: {e}")


@router.post("/update-chapters", response_model=ApiResponse[dict])
async def update_chapter_data(
    current_user: UserResponse = Depends(
        require_role(UserRole.MASTER, UserRole.ADMIN)
    ),
    db: AsyncSession = Depends(get_db),
):
    """챕터 concept_ids 업데이트 (관리자용).

    DB 전체 초기화 없이 챕터의 concept_ids만 갱신합니다.
    """
    from app.models.chapter import Chapter

    CHAPTER_CONCEPT_MAP = {
        "chapter-m1-01": ["M1-NUM-01", "M1-NUM-02"],
        "chapter-m1-02": ["M1-NUM-03", "M1-NUM-04"],
        "chapter-m1-03": ["M1-ALG-01", "M1-ALG-02", "concept-001"],
        "chapter-m1-04": ["M1-FUNC-01"],
        "chapter-m1-05": ["M1-GEO-01", "M1-GEO-02", "M1-GEO-03"],
        "chapter-m1-06": ["M1-STA-01"],
    }

    stmt = select(Chapter).where(Chapter.grade == "middle_1")
    result = await db.execute(stmt)
    chapters = result.scalars().all()

    updated = 0
    for ch in chapters:
        if ch.id in CHAPTER_CONCEPT_MAP:
            new_ids = CHAPTER_CONCEPT_MAP[ch.id]
            if ch.concept_ids != new_ids:
                ch.concept_ids = new_ids
                updated += 1

    await db.commit()

    return ApiResponse(
        success=True,
        data={"updated_chapters": updated, "total_chapters": len(chapters)},
        message=f"{updated}개 챕터의 concept_ids가 업데이트되었습니다.",
    )
