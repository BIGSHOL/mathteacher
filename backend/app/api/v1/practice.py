"""빠른 연습 API 엔드포인트."""

import random
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.question import Question
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.concept import Concept
from app.schemas import ApiResponse, QuestionResponse, StartTestResponse, TestWithQuestionsResponse
from app.schemas.common import Grade
from app.api.v1.auth import get_current_user
from app.schemas import UserResponse

router = APIRouter(prefix="/practice", tags=["practice"])


class PracticeStartRequest(BaseModel):
    """빠른 연습 시작 요청."""

    grade: Grade
    category: str
    count: int = Field(default=10, ge=5, le=30)
    starting_difficulty: int = Field(default=5, ge=1, le=10)


class PracticeStartData(BaseModel):
    """빠른 연습 시작 응답 데이터."""

    attempt_id: str


@router.post("/start", response_model=ApiResponse[PracticeStartData], status_code=status.HTTP_201_CREATED)
async def start_practice(
    request: PracticeStartRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """빠른 연습 시작 - 동적 적응형 테스트 생성."""

    # 1. 해당 학년의 개념 ID 조회
    concept_stmt = select(Concept.id).where(Concept.grade == request.grade)
    concept_ids = list((await db.scalars(concept_stmt)).all())

    if not concept_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NO_CONCEPTS",
                    "message": f"{request.grade.value} 학년에 해당하는 개념이 없습니다.",
                },
            },
        )

    # 2. 해당 카테고리의 문제 조회
    q_stmt = (
        select(Question)
        .where(
            Question.concept_id.in_(concept_ids),
            Question.category == request.category,
            Question.is_active == True,  # noqa: E712
        )
    )
    all_questions = list((await db.scalars(q_stmt)).all())

    if not all_questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NO_QUESTIONS",
                    "message": f"해당 조건에 맞는 문제가 없습니다.",
                },
            },
        )

    # 3. 동적 테스트 생성
    category_label = "연산" if request.category == "computation" else "개념"
    practice_test = Test(
        id=f"practice-{uuid4().hex[:12]}",
        title=f"{category_label} 빠른 연습 (Lv.{request.starting_difficulty})",
        description="빠른 연습 모드 - 적응형",
        grade=request.grade,
        concept_ids=concept_ids,
        question_ids=[q.id for q in all_questions],
        question_count=request.count,
        time_limit_minutes=None,
        is_adaptive=True,
        is_active=True,
    )
    db.add(practice_test)
    await db.flush()

    # 4. 시작 난이도에 가장 가까운 첫 문제 선택
    first_question = _select_closest_question(
        all_questions, request.starting_difficulty, exclude_ids=[]
    )
    if not first_question:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NO_QUESTIONS",
                    "message": "시작 난이도에 맞는 문제가 없습니다.",
                },
            },
        )

    # 5. TestAttempt 생성
    attempt = TestAttempt(
        test_id=practice_test.id,
        student_id=current_user.id,
        max_score=first_question.points,
        total_count=request.count,
        is_adaptive=True,
        initial_difficulty=request.starting_difficulty,
        current_difficulty=request.starting_difficulty,
        adaptive_question_ids=[first_question.id],
    )
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)

    return ApiResponse(data=PracticeStartData(attempt_id=attempt.id))


def _select_closest_question(
    questions: list[Question], target: int, exclude_ids: list[str]
) -> Question | None:
    """target 난이도에 가장 가까운 문제 선택."""
    for spread in range(10):
        candidates = []
        for diff in [target + spread, target - spread]:
            if diff < 1 or diff > 10:
                continue
            for q in questions:
                if q.difficulty == diff and q.id not in exclude_ids:
                    candidates.append(q)
        if candidates:
            return random.choice(candidates)
    return None
