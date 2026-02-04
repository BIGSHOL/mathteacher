"""관리자 전용 API (DB 초기화 등)."""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

from app.core.database import get_db
from app.api.v1.auth import require_role
from app.schemas.common import ApiResponse
from app.schemas.auth import UserResponse, UserRole

logger = logging.getLogger(__name__)

router = APIRouter()


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
    from app.core.database import sync_engine, SyncSessionLocal
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

        # 3) Re-run init_db logic inline (avoid circular import)
        _run_init_db(sync_engine, SyncSessionLocal, Base)

        # 4) Re-run load_seed_data
        _run_load_seed_data(SyncSessionLocal)

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


def _run_init_db(sync_engine, SyncSessionLocal, Base):
    """init_db 로직 재실행 (main.py에서 분리)."""
    from app.models.user import User, RefreshToken
    from app.models.concept import Concept
    from app.models.question import Question
    from app.models.test import Test
    from app.models.chapter import Chapter
    from app.models.chapter_progress import ChapterProgress
    from app.models.concept_mastery import ConceptMastery
    from app.services.auth_service import AuthService
    from datetime import datetime, timezone

    db = SyncSessionLocal()
    try:
        if not db.query(User).first():
            # main.py의 init_db()를 호출 (lazy import로 순환 방지)
            import importlib
            main_module = importlib.import_module("app.main")
            # init_db는 이미 테이블이 생성된 상태이므로 시드만 실행
            main_module.init_db()
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"init_db re-run failed: {e}")
        raise
    finally:
        db.close()


def _run_load_seed_data(SyncSessionLocal):
    """load_seed_data 재실행."""
    try:
        import importlib
        main_module = importlib.import_module("app.main")
        main_module.load_seed_data()
    except Exception as e:
        logger.error(f"load_seed_data re-run failed: {e}")
        raise
