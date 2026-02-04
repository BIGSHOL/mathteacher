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
    from app.core.config import settings
    from app.core.database import Base, async_engine

    logger.warning(f"DB reset requested by user {current_user.id} ({current_user.name})")

    try:
        # 0) AI 생성 문제 백업 (id가 'ai-'로 시작하는 문제)
        from app.models.question import Question
        from sqlalchemy.orm import Session as SyncSession

        ai_questions_backup = []
        with SyncSession(sync_engine) as sync_db:
            ai_qs = sync_db.query(Question).filter(
                Question.id.like("ai-%")
            ).all()
            for q in ai_qs:
                ai_questions_backup.append({
                    "id": q.id,
                    "concept_id": q.concept_id,
                    "category": q.category.value if hasattr(q.category, "value") else str(q.category),
                    "part": q.part.value if hasattr(q.part, "value") else str(q.part),
                    "question_type": q.question_type.value if hasattr(q.question_type, "value") else str(q.question_type),
                    "difficulty": q.difficulty,
                    "content": q.content,
                    "options": q.options,
                    "correct_answer": q.correct_answer,
                    "explanation": q.explanation,
                    "points": q.points,
                    "blank_config": q.blank_config,
                })
        logger.info("Backed up %d AI-generated questions", len(ai_questions_backup))

        # 1) Close async session & dispose pool to avoid SQLite lock
        await db.close()
        await async_engine.dispose()

        # 2) Drop all tables (SQLite vs PostgreSQL)
        if settings.DATABASE_URL.startswith("sqlite"):
            Base.metadata.drop_all(bind=sync_engine)
        else:
            with sync_engine.connect() as conn:
                conn.execute(text("DROP SCHEMA public CASCADE"))
                conn.execute(text("CREATE SCHEMA public"))
                conn.commit()

        # 3) Recreate tables
        Base.metadata.create_all(bind=sync_engine)

        # 4) Re-run init_db (seeds users) + load_seed_data (seeds concepts/questions)
        import importlib
        main_module = importlib.import_module("app.main")
        main_module.init_db()
        main_module.load_seed_data()

        # 5) AI 생성 문제 복원 (개념이 존재하는 것만)
        restored = 0
        if ai_questions_backup:
            with SyncSession(sync_engine) as sync_db:
                from app.models.concept import Concept
                existing_concepts = {
                    c.id for c in sync_db.query(Concept.id).all()
                }
                for q_data in ai_questions_backup:
                    if q_data["concept_id"] not in existing_concepts:
                        continue
                    # 이미 존재하는 ID는 건너뛰기
                    if sync_db.get(Question, q_data["id"]):
                        continue
                    q = Question(
                        id=q_data["id"],
                        concept_id=q_data["concept_id"],
                        category=q_data["category"],
                        part=q_data["part"],
                        question_type=q_data["question_type"],
                        difficulty=q_data["difficulty"],
                        content=q_data["content"],
                        options=q_data["options"],
                        correct_answer=q_data["correct_answer"],
                        explanation=q_data["explanation"],
                        points=q_data["points"],
                        blank_config=q_data.get("blank_config"),
                        is_active=True,
                    )
                    sync_db.add(q)
                    restored += 1
                sync_db.commit()
        logger.info("Restored %d AI-generated questions", restored)

        logger.info("DB reset completed successfully")
        return ApiResponse(
            success=True,
            data={"reset": True, "ai_questions_restored": restored},
            message=f"DB 초기화 완료! 시드 데이터 재생성 + AI 문제 {restored}개 복원. 다시 로그인해주세요.",
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
        "chapter-m1-01": ["concept-m1-prime"],
        "chapter-m1-02": ["concept-m1-integer", "concept-002"],
        "chapter-m1-03": ["concept-m1-expression", "concept-m1-equation", "concept-001", "concept-003"],
        "chapter-m1-04": ["concept-m1-coord", "concept-m1-proportion", "concept-004"],
        "chapter-m1-05": ["concept-m1-basic-geo", "concept-m1-plane-fig", "concept-m1-solid-fig"],
        "chapter-m1-06": ["concept-m1-frequency", "concept-m1-representative", "concept-m1-scatter", "concept-005"],
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
