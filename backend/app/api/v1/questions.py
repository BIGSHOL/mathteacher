"""문제 생성/조회 API 엔드포인트."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func as sa_func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, selectinload

from app.core.database import get_db
from app.models.chapter import Chapter
from app.models.concept import Concept
from app.models.question import Question
from app.schemas import (
    ApiResponse,
    PaginatedResponse,
    QuestionCreate,
    QuestionResponse,
    QuestionWithAnswer,
    UserResponse,
)
from app.schemas.common import Grade, ProblemPart, QuestionCategory, QuestionType
from app.api.v1.auth import get_current_user, require_role

router = APIRouter(prefix="/questions", tags=["questions"])


# ===========================
# 문제 생성
# ===========================


@router.post(
    "",
    response_model=ApiResponse[QuestionWithAnswer],
    status_code=status.HTTP_201_CREATED,
)
async def create_question(
    payload: QuestionCreate,
    db: AsyncSession = Depends(get_db),
    _user: UserResponse = Depends(require_role("teacher", "admin", "master")),
):
    """단일 문제 생성."""
    # concept 존재 확인
    concept = await db.get(Concept, payload.concept_id)
    if not concept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {"code": "CONCEPT_NOT_FOUND", "message": f"개념 {payload.concept_id}을 찾을 수 없습니다."},
            },
        )

    question = Question(
        concept_id=payload.concept_id,
        category=payload.category,
        part=payload.part,
        question_type=payload.question_type,
        difficulty=payload.difficulty,
        content=payload.content,
        options=[opt.model_dump() for opt in payload.options] if payload.options else None,
        correct_answer=payload.correct_answer,
        explanation=payload.explanation,
        points=payload.points,
        prerequisite_concept_ids=payload.prerequisite_concept_ids,
    )
    db.add(question)
    await db.commit()
    await db.refresh(question)

    return ApiResponse(data=_to_question_with_answer(question))


@router.post(
    "/batch",
    response_model=ApiResponse[list[QuestionWithAnswer]],
    status_code=status.HTTP_201_CREATED,
)
async def create_questions_batch(
    payload: list[QuestionCreate],
    db: AsyncSession = Depends(get_db),
    _user: UserResponse = Depends(require_role("teacher", "admin", "master")),
):
    """문제 일괄 생성 (프론트 템플릿 → DB 파이프라인)."""
    if len(payload) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {"code": "BATCH_TOO_LARGE", "message": "한 번에 최대 100문제까지 생성할 수 있습니다."},
            },
        )

    # 모든 concept_id 유효성 검증
    concept_ids = {q.concept_id for q in payload}
    existing = {
        c.id
        for c in (await db.scalars(select(Concept.id).where(Concept.id.in_(concept_ids)))).all()
    }
    missing = concept_ids - existing
    if missing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "CONCEPTS_NOT_FOUND",
                    "message": f"다음 개념을 찾을 수 없습니다: {', '.join(missing)}",
                },
            },
        )

    questions = []
    for item in payload:
        q = Question(
            concept_id=item.concept_id,
            category=item.category,
            part=item.part,
            question_type=item.question_type,
            difficulty=item.difficulty,
            content=item.content,
            options=[opt.model_dump() for opt in item.options] if item.options else None,
            correct_answer=item.correct_answer,
            explanation=item.explanation,
            points=item.points,
            prerequisite_concept_ids=item.prerequisite_concept_ids,
        )
        db.add(q)
        questions.append(q)

    await db.commit()

    # 배치 재조회 (개별 refresh 대신 한번에 조회)
    question_ids = [q.id for q in questions]
    stmt = select(Question).where(Question.id.in_(question_ids)).options(selectinload(Question.concept))
    refreshed = list((await db.scalars(stmt)).all())

    return ApiResponse(data=[_to_question_with_answer(q) for q in refreshed])


# ===========================
# 문제 조회
# ===========================


@router.get("", response_model=ApiResponse[PaginatedResponse[QuestionWithAnswer]])
async def list_questions(
    concept_id: str | None = Query(None, description="개념 ID로 필터링"),
    grade: Grade | None = Query(None, description="학년으로 필터링"),
    category: QuestionCategory | None = Query(None),
    part: ProblemPart | None = Query(None),
    difficulty: int | None = Query(None, ge=1, le=10),
    question_type: QuestionType | None = Query(None, description="문제 유형 필터"),
    chapter_id: str | None = Query(None, description="단원 ID로 필터링"),
    search: str | None = Query(None, description="문제 내용 검색"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _user: UserResponse = Depends(get_current_user),
):
    """문제 목록 조회 (필터링/페이징)."""
    stmt = select(Question).where(Question.is_active.is_(True))

    joined_concept = False
    if concept_id:
        stmt = stmt.where(Question.concept_id == concept_id)
    if grade:
        stmt = stmt.join(Concept).where(Concept.grade == grade)
        stmt = stmt.options(contains_eager(Question.concept))
        joined_concept = True
    if category:
        stmt = stmt.where(Question.category == category)
    if part:
        stmt = stmt.where(Question.part == part)
    if difficulty:
        stmt = stmt.where(Question.difficulty == difficulty)
    if question_type:
        stmt = stmt.where(Question.question_type == question_type)
    if chapter_id:
        chapter = await db.get(Chapter, chapter_id)
        if chapter and chapter.concept_ids:
            stmt = stmt.where(Question.concept_id.in_(chapter.concept_ids))
    if search:
        stmt = stmt.where(Question.content.ilike(f"%{search}%"))

    # JOIN 없으면 selectinload 명시 (모델 기본 selectin 대신 제어)
    if not joined_concept:
        stmt = stmt.options(selectinload(Question.concept))

    # 총 개수 계산
    count_stmt = select(sa_func.count()).select_from(stmt.subquery())
    total = await db.scalar(count_stmt)

    # 페이징 적용
    stmt = stmt.order_by(Question.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    questions = (await db.scalars(stmt)).unique().all()

    # concept_id → chapter.name 매핑 (해당 문제의 concept/grade만 조회)
    q_concept_ids = {q.concept_id for q in questions}
    q_grades = {q.concept.grade for q in questions if q.concept and q.concept.grade}
    concept_chapter_map = await _build_concept_chapter_map(db, q_concept_ids, q_grades)

    return ApiResponse(
        data=PaginatedResponse(
            items=[_to_question_with_answer(q, concept_chapter_map) for q in questions],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )
    )


@router.get("/filter-options", response_model=ApiResponse[dict])
async def get_filter_options(
    grade: Grade | None = Query(None),
    db: AsyncSession = Depends(get_db),
    _user: UserResponse = Depends(get_current_user),
):
    """필터용 단원+개념 목록을 한 번에 조회 (단일 라운드트립)."""
    # 단원 조회
    ch_stmt = select(
        Chapter.id, Chapter.name, Chapter.grade,
        Chapter.chapter_number, Chapter.concept_ids,
    ).where(Chapter.is_active.is_(True))
    if grade:
        ch_stmt = ch_stmt.where(Chapter.grade == grade)
    ch_stmt = ch_stmt.order_by(Chapter.grade, Chapter.chapter_number)

    # 개념 조회
    co_stmt = select(Concept.id, Concept.name, Concept.grade)
    if grade:
        co_stmt = co_stmt.where(Concept.grade == grade)
    co_stmt = co_stmt.order_by(Concept.name)

    ch_rows, co_rows = (await db.execute(ch_stmt)).all(), (await db.execute(co_stmt)).all()
    return ApiResponse(
        data={
            "chapters": [
                {
                    "id": r.id,
                    "name": r.name,
                    "grade": r.grade.value if hasattr(r.grade, "value") else r.grade,
                    "chapter_number": r.chapter_number,
                    "concept_ids": r.concept_ids or [],
                }
                for r in ch_rows
            ],
            "concepts": [
                {"id": r.id, "name": r.name, "grade": r.grade.value if hasattr(r.grade, "value") else r.grade}
                for r in co_rows
            ],
        }
    )


@router.get("/chapters-list", response_model=ApiResponse[list[dict]])
async def list_chapters_for_filter(
    grade: Grade | None = Query(None),
    db: AsyncSession = Depends(get_db),
    _user: UserResponse = Depends(get_current_user),
):
    """필터용 단원 목록 조회 (경량: 필요한 컬럼만 SELECT)."""
    cols = select(
        Chapter.id, Chapter.name, Chapter.grade,
        Chapter.chapter_number, Chapter.concept_ids,
    ).where(Chapter.is_active.is_(True))
    if grade:
        cols = cols.where(Chapter.grade == grade)
    cols = cols.order_by(Chapter.grade, Chapter.chapter_number)
    rows = (await db.execute(cols)).all()
    return ApiResponse(
        data=[
            {
                "id": r.id,
                "name": r.name,
                "grade": r.grade.value if hasattr(r.grade, "value") else r.grade,
                "chapter_number": r.chapter_number,
                "concept_ids": r.concept_ids or [],
            }
            for r in rows
        ]
    )


@router.get("/concepts-list", response_model=ApiResponse[list[dict]])
async def list_concepts_for_filter(
    grade: Grade | None = Query(None),
    chapter_id: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    _user: UserResponse = Depends(get_current_user),
):
    """필터용 개념 목록 조회 (경량: id, name, grade만 SELECT)."""
    cols = select(Concept.id, Concept.name, Concept.grade)
    if chapter_id:
        chapter = await db.get(Chapter, chapter_id)
        if chapter and chapter.concept_ids:
            stmt = cols.where(Concept.id.in_(chapter.concept_ids))
        else:
            return ApiResponse(data=[])
    elif grade:
        stmt = cols.where(Concept.grade == grade)
    else:
        stmt = cols
    stmt = stmt.order_by(Concept.name)
    rows = (await db.execute(stmt)).all()
    return ApiResponse(
        data=[{"id": r.id, "name": r.name, "grade": r.grade.value if hasattr(r.grade, "value") else r.grade} for r in rows]
    )


@router.get("/by-concept/{concept_id}", response_model=ApiResponse[list[QuestionWithAnswer]])
async def get_questions_by_concept(
    concept_id: str,
    db: AsyncSession = Depends(get_db),
    _user: UserResponse = Depends(get_current_user),
):
    """특정 개념의 전체 문제 조회."""
    concept = await db.get(Concept, concept_id)
    if not concept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {"code": "CONCEPT_NOT_FOUND", "message": f"개념 {concept_id}을 찾을 수 없습니다."},
            },
        )

    stmt = (
        select(Question)
        .where(Question.concept_id == concept_id, Question.is_active.is_(True))
        .order_by(Question.difficulty)
    )
    questions = (await db.scalars(stmt)).all()

    # concept_id → chapter.name 매핑 (해당 concept의 grade만)
    concept_grade = {concept.grade} if concept.grade else None
    concept_chapter_map = await _build_concept_chapter_map(db, {concept_id}, concept_grade)

    return ApiResponse(data=[_to_question_with_answer(q, concept_chapter_map) for q in questions])


@router.get("/stats", response_model=ApiResponse[dict])
async def get_question_stats(
    db: AsyncSession = Depends(get_db),
    _user: UserResponse = Depends(require_role("teacher", "admin", "master")),
):
    """문제 통계 (개념별 문제 수)."""
    stmt = (
        select(
            Question.concept_id,
            sa_func.count(Question.id).label("count"),
        )
        .where(Question.is_active.is_(True))
        .group_by(Question.concept_id)
    )

    stats = (await db.execute(stmt)).all()

    return ApiResponse(
        data={
            "total": sum(s.count for s in stats),
            "by_concept": {s.concept_id: s.count for s in stats},
        }
    )


# ===========================
# 헬퍼
# ===========================


async def _build_concept_chapter_map(
    db: AsyncSession, concept_ids: set[str], grades: set | None = None
) -> dict[str, str]:
    """concept_id → chapter.name 매핑 (필요한 grade의 chapter만 조회)."""
    if not concept_ids:
        return {}
    stmt = select(Chapter)
    if grades:
        stmt = stmt.where(Chapter.grade.in_(grades))
    chapters = (await db.scalars(stmt)).all()
    result: dict[str, str] = {}
    for ch in chapters:
        for cid in ch.concept_ids or []:
            if cid in concept_ids:
                result[cid] = ch.name
    return result


def _to_question_with_answer(
    q: Question,
    concept_chapter_map: dict[str, str] | None = None,
) -> QuestionWithAnswer:
    """Question ORM → QuestionWithAnswer schema."""
    return QuestionWithAnswer(
        id=q.id,
        concept_id=q.concept_id,
        concept_name=q.concept.name if q.concept else "",
        grade=q.concept.grade.value if q.concept and q.concept.grade else None,
        chapter_name=(concept_chapter_map or {}).get(q.concept_id),
        category=q.category,
        part=q.part,
        question_type=q.question_type,
        difficulty=q.difficulty,
        content=q.content,
        options=q.options,
        correct_answer=q.correct_answer,
        explanation=q.explanation,
        points=q.points,
        prerequisite_concept_ids=q.prerequisite_concept_ids,
    )
