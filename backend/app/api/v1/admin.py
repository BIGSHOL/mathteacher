"""관리자 전용 API (DB 초기화, 사용자 목록, AI 문제 생성 등)."""

import asyncio
import logging
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, func

from app.core.database import get_db, sync_engine
from app.api.v1.auth import require_role
from app.schemas.common import ApiResponse, PaginatedResponse, UserRole
from app.schemas.auth import UserResponse, UpdateUserRequest
from app.models.user import User
from app.services.auth_service import AuthService
from app.models.question import Question
from app.models.concept import Concept
from app.services.ai_service import AIService
from app.api.v1.questions import validate_options_no_duplicates

logger = logging.getLogger(__name__)

router = APIRouter()

_ai_service = AIService()


# ─────────────────────────────────────────────
# AI 문제 생성 스키마
# ─────────────────────────────────────────────
class AIGenerateRequest(BaseModel):
    concept_id: str = Field(..., description="개념 ID")
    count: int = Field(default=10, ge=1, le=50, description="생성할 문제 수")
    question_type: str = Field(
        default="multiple_choice",
        description="multiple_choice 또는 fill_in_blank",
    )
    difficulty_min: int = Field(default=1, ge=1, le=10)
    difficulty_max: int = Field(default=10, ge=1, le=10)


class AISaveRequest(BaseModel):
    questions: list[dict] = Field(..., description="저장할 문제 목록")


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


@router.put("/users/{user_id}", response_model=ApiResponse[dict])
async def update_user(
    user_id: str,
    update_request: UpdateUserRequest,
    current_user: UserResponse = Depends(
        require_role(UserRole.MASTER, UserRole.ADMIN)
    ),
    db: AsyncSession = Depends(get_db),
):
    """사용자 정보 수정 (관리자/마스터 전용)."""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    # 마스터 계정은 수정 불가 (마스터 본인만 예외)
    user_role = user.role.value if hasattr(user.role, "value") else user.role
    if user_role == "master" and user.id != current_user.id:
        raise HTTPException(status_code=403, detail="마스터 계정은 수정할 수 없습니다")

    # admin은 teacher/student만 수정 가능
    if current_user.role == UserRole.ADMIN and user_role in ("master", "admin"):
        raise HTTPException(status_code=403, detail="관리자/마스터 계정을 수정할 권한이 없습니다")

    # 역할 변경 시 권한 검증
    if update_request.role is not None:
        new_role = update_request.role.value if hasattr(update_request.role, "value") else update_request.role
        if new_role == "master":
            raise HTTPException(status_code=403, detail="마스터 역할로 변경할 수 없습니다")
        if new_role == "admin" and current_user.role != UserRole.MASTER:
            raise HTTPException(status_code=403, detail="관리자 역할 부여는 마스터만 가능합니다")

    # 필드 업데이트
    if update_request.name is not None:
        user.name = update_request.name
    if update_request.role is not None:
        user.role = update_request.role
    if update_request.grade is not None:
        user.grade = update_request.grade
    if update_request.class_id is not None:
        user.class_id = update_request.class_id
    if update_request.is_active is not None:
        user.is_active = update_request.is_active
    if update_request.password is not None:
        auth_service = AuthService(db)
        user.hashed_password = auth_service.hash_password(update_request.password)

    await db.commit()

    return ApiResponse(
        success=True,
        data={
            "id": user.id,
            "name": user.name,
            "role": user.role.value if hasattr(user.role, "value") else user.role,
            "grade": (user.grade.value if hasattr(user.grade, "value") else user.grade) if user.grade else None,
        },
        message=f"'{user.name}' 계정이 수정되었습니다",
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

        # 4) Re-run init_db (seeds users) + load_seed_data (seeds concepts/questions) + update chapter concept IDs
        import importlib
        main_module = importlib.import_module("app.main")
        main_module.init_db()
        main_module.load_seed_data()
        main_module.update_chapter_concept_ids()

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
        # 1학기
        "chapter-m1-01": ["concept-m1-prime"],
        "chapter-m1-02": ["concept-m1-integer", "concept-002"],
        "chapter-m1-03": ["concept-m1-expression", "concept-001", "concept-003"],
        "chapter-m1-04": ["concept-m1-equation"],
        "chapter-m1-05": ["concept-m1-coord", "concept-004"],
        "chapter-m1-06": ["concept-m1-proportion"],
        # 2학기
        "chapter-m1-07": ["concept-m1-basic-geo"],
        "chapter-m1-08": ["concept-m1-plane-fig"],
        "chapter-m1-09": ["concept-m1-solid-fig"],
        "chapter-m1-10": ["concept-m1-frequency", "concept-005"],
        "chapter-m1-11": ["concept-m1-representative"],
        "chapter-m1-12": ["concept-m1-scatter"],
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


# ─────────────────────────────────────────────
# AI 문제 대량 생성
# ─────────────────────────────────────────────
@router.post("/generate-questions", response_model=ApiResponse[dict])
async def admin_generate_questions(
    request: AIGenerateRequest,
    current_user: UserResponse = Depends(require_role(UserRole.MASTER)),
    db: AsyncSession = Depends(get_db),
):
    """AI로 문제를 생성하여 프리뷰로 반환합니다 (저장 안 함, 마스터 전용).

    개념을 선택하고 수량/난이도를 지정하면 Gemini가 문제를 생성합니다.
    반환된 문제를 검토 후 save-generated-questions로 저장하세요.
    """
    from app.core.config import settings

    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY가 설정되지 않았습니다.",
        )

    # 개념 조회
    concept = await db.get(Concept, request.concept_id)
    if not concept:
        raise HTTPException(status_code=404, detail="개념을 찾을 수 없습니다.")

    concept_name = concept.name
    grade = concept.grade.value if hasattr(concept.grade, "value") else str(concept.grade)
    category = concept.category.value if hasattr(concept.category, "value") else str(concept.category)
    part = concept.part.value if hasattr(concept.part, "value") else str(concept.part)

    # 기존 문제 content 조회 (중복 방지)
    existing_stmt = (
        select(Question.content)
        .where(Question.concept_id == request.concept_id, Question.is_active.is_(True))
    )
    existing_result = await db.execute(existing_stmt)
    existing_contents = [row[0] for row in existing_result.all()]

    # 배치 생성 (10개씩 끊어서 호출)
    BATCH_SIZE = 10
    all_generated: list[dict] = []

    for i in range(0, request.count, BATCH_SIZE):
        batch_count = min(BATCH_SIZE, request.count - i)
        batch = await _ai_service.generate_questions(
            concept_name=concept_name,
            concept_id=request.concept_id,
            grade=grade,
            category=category,
            part=part,
            question_type=request.question_type,
            count=batch_count,
            difficulty_min=request.difficulty_min,
            difficulty_max=request.difficulty_max,
            existing_contents=existing_contents + [q["content"] for q in all_generated],
            id_prefix=f"ai-{request.concept_id.replace('concept-', '')}",
            start_seq=len(all_generated) + 1,
        )
        if batch:
            all_generated.extend(batch)

        # Rate limit 배려
        if i + BATCH_SIZE < request.count:
            await asyncio.sleep(1)

    if not all_generated:
        raise HTTPException(
            status_code=500,
            detail="AI 문제 생성에 실패했습니다. 잠시 후 다시 시도하세요.",
        )

    logger.info(
        "AI generated %d questions for concept %s by user %s",
        len(all_generated), request.concept_id, current_user.id,
    )

    return ApiResponse(
        success=True,
        data={"generated": all_generated, "count": len(all_generated)},
        message=f"{len(all_generated)}개 문제가 생성되었습니다. 검토 후 저장하세요.",
    )


@router.post("/save-generated-questions", response_model=ApiResponse[dict])
async def admin_save_generated_questions(
    request: AISaveRequest,
    current_user: UserResponse = Depends(require_role(UserRole.MASTER)),
    db: AsyncSession = Depends(get_db),
):
    """생성된 문제를 DB에 저장합니다 (마스터 전용).

    generate-questions 또는 derive-fill-blank에서 반환된 문제 목록을
    검토/편집 후 이 엔드포인트로 저장합니다.
    """
    if not request.questions:
        raise HTTPException(status_code=400, detail="저장할 문제가 없습니다.")
    if len(request.questions) > 200:
        raise HTTPException(status_code=400, detail="한 번에 최대 200개까지 저장 가능합니다.")

    # 개념 ID 유효성 검증
    concept_ids = {q.get("concept_id") for q in request.questions if q.get("concept_id")}
    existing_concepts_stmt = select(Concept.id).where(Concept.id.in_(concept_ids))
    existing_result = await db.execute(existing_concepts_stmt)
    existing_concept_ids = {row[0] for row in existing_result.all()}
    missing = concept_ids - existing_concept_ids
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"존재하지 않는 개념: {', '.join(missing)}",
        )

    saved = 0
    for q_data in request.questions:
        # ID가 없으면 자동 생성
        qid = q_data.get("id") or f"ai-{uuid4().hex[:12]}"
        # 이미 존재하는 ID는 건너뛰기
        existing = await db.get(Question, qid)
        if existing:
            continue

        q = Question(
            id=qid,
            concept_id=q_data["concept_id"],
            category=q_data.get("category", "concept"),
            part=q_data.get("part", "calc"),
            question_type=q_data.get("question_type", "multiple_choice"),
            difficulty=max(1, min(10, int(q_data.get("difficulty", 5)))),
            content=q_data.get("content", ""),
            options=q_data.get("options"),
            correct_answer=q_data.get("correct_answer", ""),
            explanation=q_data.get("explanation", ""),
            points=q_data.get("points", 10),
            blank_config=q_data.get("blank_config"),
            is_active=True,
        )
        db.add(q)
        saved += 1

    await db.commit()

    logger.info(
        "Saved %d generated questions by user %s",
        saved, current_user.id,
    )

    return ApiResponse(
        success=True,
        data={"saved_count": saved},
        message=f"{saved}개 문제가 저장되었습니다.",
    )


# ─────────────────────────────────────────────
# FB 빈칸 문제 자동 파생
# ─────────────────────────────────────────────
class FBDeriveRequest(BaseModel):
    concept_id: str = Field(..., description="개념 ID")
    max_per_mc: int = Field(default=3, ge=1, le=5, description="MC 1문제당 최대 파생 수")


@router.post("/derive-fill-blank", response_model=ApiResponse[dict])
async def admin_derive_fill_blank(
    request: FBDeriveRequest,
    current_user: UserResponse = Depends(require_role(UserRole.MASTER)),
    db: AsyncSession = Depends(get_db),
):
    """MC 문제에서 빈칸 채우기 문제를 자동 파생합니다 (마스터 전용).

    선택한 개념의 MC 문제들에서 핵심 용어를 추출하여
    빈칸 채우기 변형 문제를 생성합니다.
    """
    from app.services.fb_derivation_service import FBDerivationService

    # 개념 존재 확인
    concept = await db.get(Concept, request.concept_id)
    if not concept:
        raise HTTPException(status_code=404, detail="개념을 찾을 수 없습니다.")

    # MC 문제 조회
    mc_stmt = (
        select(Question)
        .where(
            Question.concept_id == request.concept_id,
            Question.question_type == "multiple_choice",
            Question.is_active.is_(True),
        )
    )
    mc_result = await db.execute(mc_stmt)
    mc_questions = mc_result.scalars().all()

    if not mc_questions:
        raise HTTPException(
            status_code=404,
            detail="해당 개념에 MC 문제가 없습니다.",
        )

    # 파생 서비스 호출
    service = FBDerivationService()
    all_derived: list[dict] = []

    for mc_q in mc_questions:
        mc_dict = {
            "id": mc_q.id,
            "concept_id": mc_q.concept_id,
            "category": mc_q.category.value if hasattr(mc_q.category, "value") else str(mc_q.category),
            "part": mc_q.part.value if hasattr(mc_q.part, "value") else str(mc_q.part),
            "difficulty": mc_q.difficulty,
            "content": mc_q.content,
            "options": mc_q.options,
            "correct_answer": mc_q.correct_answer,
            "explanation": mc_q.explanation,
            "points": mc_q.points,
        }
        derived = service.derive_from_mc(mc_dict, max_variants=request.max_per_mc)
        all_derived.extend(derived)

    logger.info(
        "Derived %d FB questions from %d MC questions for concept %s",
        len(all_derived), len(mc_questions), request.concept_id,
    )

    return ApiResponse(
        success=True,
        data={
            "source_mc_count": len(mc_questions),
            "derived_fb_count": len(all_derived),
            "derived_questions": all_derived,
        },
        message=f"MC {len(mc_questions)}개에서 FB {len(all_derived)}개 파생. 검토 후 저장하세요.",
    )
