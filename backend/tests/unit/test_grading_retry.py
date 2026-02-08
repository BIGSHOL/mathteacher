"""GradingService 재도전 로직 단위 테스트."""

import json
import pytest
from sqlalchemy import select

from app.models.question import Question
from app.models.test_attempt import TestAttempt
from app.models.user import User
from app.models.focus_check import FocusCheckItem
from app.schemas.common import QuestionCategory, QuestionType, ProblemPart
from app.services.grading_service import GradingService


@pytest.mark.asyncio
async def test_submit_answer_with_retry_correct(db_session):
    """submit_answer_with_retry가 정답일 때 큐에서 제거하고 점수를 부여한다."""
    # Given
    user = User(
        id="student-retry-1",
        login_id="student_retry_1",
        name="재도전 학생 1",
        role="student",
        hashed_password="hashed"
    )
    db_session.add(user)

    question = Question(
        id="q-retry-1",
        concept_id="c-001",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=1,
        content="문제",
        correct_answer="A",
        points=10
    )
    db_session.add(question)

    attempt = TestAttempt(
        id="attempt-retry-1",
        test_id="daily-test-1",
        student_id="student-retry-1",
        score=0,
        retry_queue=["q-retry-1"],  # 큐에 있음
        retry_counts={"q-retry-1": 1},  # 1번 틀렸던 상태
        current_question_index=0
    )
    db_session.add(attempt)
    await db_session.commit()

    # When
    service = GradingService(db_session)
    result = await service.submit_answer_with_retry(
        attempt=attempt,
        question=question,
        selected_answer="A",  # 정답
        time_spent_seconds=10,
        current_combo=0,
        is_daily_test=True
    )

    # Then
    assert result["is_correct"] is True
    assert result["points_earned"] > 0
    
    # DB 상태 확인
    await db_session.refresh(attempt)
    assert "q-retry-1" not in attempt.retry_queue  # 큐에서 제거됨
    assert attempt.retry_counts["q-retry-1"] == 1  # 카운트는 유지 (이력용)


@pytest.mark.asyncio
async def test_submit_answer_with_retry_wrong_first(db_session):
    """submit_answer_with_retry가 첫 오답일 때 큐에 추가하고 힌트를 제공한다."""
    # Given
    user = User(
        id="student-retry-2",
        login_id="student_retry_2",
        name="재도전 학생 2",
        role="student",
        hashed_password="hashed"
    )
    db_session.add(user)

    question = Question(
        id="q-retry-2",
        concept_id="c-001",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=1,
        content="문제",
        correct_answer="A",
        points=10
    )
    db_session.add(question)

    attempt = TestAttempt(
        id="attempt-retry-2",
        test_id="daily-test-2",
        student_id="student-retry-2",
        score=0,
        retry_queue=[],
        retry_counts={},
        current_question_index=0
    )
    db_session.add(attempt)
    await db_session.commit()

    # When
    service = GradingService(db_session)
    result = await service.submit_answer_with_retry(
        attempt=attempt,
        question=question,
        selected_answer="B",  # 오답
        time_spent_seconds=10,
        current_combo=0,
        is_daily_test=True
    )

    # Then
    assert result["is_correct"] is False
    assert result["retry_scheduled"] is True
    assert result["retry_count"] == 1
    assert result["hint"]["level"] == 1  # 1차 힌트

    # DB 상태 확인
    await db_session.refresh(attempt)
    assert "q-retry-2" in attempt.retry_queue
    assert attempt.retry_counts["q-retry-2"] == 1


@pytest.mark.asyncio
async def test_submit_answer_with_retry_focus_check(db_session):
    """submit_answer_with_retry가 4번째 오답일 때 포커스 체크로 이동한다."""
    # Given
    user = User(
        id="student-retry-3",
        login_id="student_retry_3",
        name="재도전 학생 3",
        role="student",
        hashed_password="hashed"
    )
    db_session.add(user)

    question = Question(
        id="q-retry-3",
        concept_id="c-001",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=1,
        content="문제",
        correct_answer="A",
        points=10
    )
    db_session.add(question)

    attempt = TestAttempt(
        id="attempt-retry-3",
        test_id="daily-test-3",
        student_id="student-retry-3",
        score=0,
        retry_queue=["q-retry-3"],
        retry_counts={"q-retry-3": 3},  # 이미 3번 틀림
        current_question_index=0
    )
    db_session.add(attempt)
    await db_session.commit()

    # When: 4번째 오답
    service = GradingService(db_session)
    result = await service.submit_answer_with_retry(
        attempt=attempt,
        question=question,
        selected_answer="B",
        time_spent_seconds=10,
        current_combo=0,
        is_daily_test=True
    )

    # Then
    assert result["is_correct"] is False
    assert result["moved_to_focus_check"] is True
    
    # DB 상태 확인
    await db_session.refresh(attempt)
    assert "q-retry-3" not in attempt.retry_queue  # 큐에서 제거됨
    assert attempt.retry_counts["q-retry-3"] == 4

    # 포커스 체크 아이템 생성 확인
    stmt = select(FocusCheckItem).where(
        FocusCheckItem.student_id == "student-retry-3",
        FocusCheckItem.question_id == "q-retry-3"
    )
    focus_item = await db_session.scalar(stmt)
    assert focus_item is not None
    assert focus_item.wrong_count == 4


def test_get_hint_for_retry():
    """get_hint_for_retry가 단계별 힌트를 올바르게 생성한다."""
    service = GradingService()
    question = Question(
        id="q-hint",
        concept_id="c-hint",
        explanation="이것은 해설입니다. 자세한 내용은..."
    )

    # 1회차: 개념 힌트
    hint1 = service.get_hint_for_retry(question, 1)
    assert hint1["level"] == 1
    assert hint1["type"] == "concept"

    # 2회차: 해설 앞부분
    hint2 = service.get_hint_for_retry(question, 2)
    assert hint2["level"] == 2
    assert hint2["type"] == "direction"
    assert "이것은 해설입니다" in hint2["message"]

    # 3회차: 확장 해설
    hint3 = service.get_hint_for_retry(question, 3)
    assert hint3["level"] == 3
    assert hint3["type"] == "extended"
