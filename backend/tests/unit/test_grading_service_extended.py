"""GradingService 확장 단위 테스트 - 빈칸 채우기 및 엣지 케이스."""

import json
from datetime import datetime, timezone

import pytest
from sqlalchemy import select

from app.models.answer_log import AnswerLog
from app.models.question import Question
from app.models.test_attempt import TestAttempt
from app.models.user import User
from app.schemas.common import QuestionCategory, QuestionType, ProblemPart
from app.services.grading_service import GradingService


@pytest.mark.asyncio
async def test_grade_answer_fill_in_blank_multiple_blanks_all_correct(db_session):
    """grade_answer가 빈칸 채우기 여러 개 모두 정답일 때 만점을 준다."""
    # Given: 3개 빈칸 모두 정답
    service = GradingService(db_session)

    student_answers = {
        "blank1": "5",
        "blank2": "10",
        "blank3": "15",
    }
    correct_answers = {
        "blank1": {"answer": "5"},
        "blank2": {"answer": "10"},
        "blank3": {"answer": "15"},
    }

    # When: grade_answer 호출
    result = service.grade_answer(
        question_id="q-001",
        selected_answer=student_answers,
        correct_answer=correct_answers,
        points=30,
    )

    # Then: 만점
    assert result["is_correct"] is True
    assert result["points_earned"] == 30
    assert result["correct_count"] == 3
    assert result["total_blanks"] == 3


@pytest.mark.asyncio
async def test_grade_answer_fill_in_blank_partial_correct(db_session):
    """grade_answer가 빈칸 채우기 부분 정답일 때 부분 점수를 준다."""
    # Given: 5개 중 3개 정답
    service = GradingService(db_session)

    student_answers = {
        "blank1": "correct",
        "blank2": "wrong",
        "blank3": "correct",
        "blank4": "wrong",
        "blank5": "correct",
    }
    correct_answers = {
        "blank1": {"answer": "correct"},
        "blank2": {"answer": "correct"},
        "blank3": {"answer": "correct"},
        "blank4": {"answer": "correct"},
        "blank5": {"answer": "correct"},
    }

    # When: grade_answer 호출
    result = service.grade_answer(
        question_id="q-002",
        selected_answer=student_answers,
        correct_answer=correct_answers,
        points=100,
    )

    # Then: 60점 (3/5)
    assert result["is_correct"] is False
    assert result["points_earned"] == 60
    assert result["correct_count"] == 3
    assert result["total_blanks"] == 5


@pytest.mark.asyncio
async def test_grade_answer_fill_in_blank_case_insensitive(db_session):
    """grade_answer가 빈칸 채우기에서 대소문자를 구분하지 않는다."""
    # Given: 대소문자가 다른 답안
    service = GradingService(db_session)

    student_answers = {
        "blank1": "abc",
        "blank2": "XYZ",
        "blank3": "MiXeD",
    }
    correct_answers = {
        "blank1": {"answer": "ABC"},
        "blank2": {"answer": "xyz"},
        "blank3": {"answer": "mixed"},
    }

    # When: grade_answer 호출
    result = service.grade_answer(
        question_id="q-003",
        selected_answer=student_answers,
        correct_answer=correct_answers,
        points=30,
    )

    # Then: 모두 정답
    assert result["is_correct"] is True
    assert result["points_earned"] == 30
    assert result["correct_count"] == 3


@pytest.mark.asyncio
async def test_grade_answer_fill_in_blank_with_whitespace(db_session):
    """grade_answer가 빈칸 채우기에서 공백을 제거한다."""
    # Given: 앞뒤 공백이 있는 답안
    service = GradingService(db_session)

    student_answers = {
        "blank1": "  answer  ",
        "blank2": "  correct",
        "blank3": "right  ",
    }
    correct_answers = {
        "blank1": {"answer": "answer"},
        "blank2": {"answer": "correct"},
        "blank3": {"answer": "right"},
    }

    # When: grade_answer 호출
    result = service.grade_answer(
        question_id="q-004",
        selected_answer=student_answers,
        correct_answer=correct_answers,
        points=30,
    )

    # Then: 모두 정답
    assert result["is_correct"] is True
    assert result["points_earned"] == 30


@pytest.mark.asyncio
async def test_grade_answer_fill_in_blank_empty_student_answer(db_session):
    """grade_answer가 빈칸 채우기에서 빈 답안을 0점 처리한다."""
    # Given: 빈 답안
    service = GradingService(db_session)

    student_answers = {}
    correct_answers = {
        "blank1": {"answer": "5"},
        "blank2": {"answer": "10"},
    }

    # When: grade_answer 호출
    result = service.grade_answer(
        question_id="q-005",
        selected_answer=student_answers,
        correct_answer=correct_answers,
        points=20,
    )

    # Then: 0점
    assert result["is_correct"] is False
    assert result["points_earned"] == 0
    assert result["correct_count"] == 0
    assert result["total_blanks"] == 2


@pytest.mark.asyncio
async def test_grade_answer_fill_in_blank_missing_some_blanks(db_session):
    """grade_answer가 빈칸 채우기에서 일부 빈칸이 누락되어도 부분 점수를 준다."""
    # Given: 3개 중 1개만 답함
    service = GradingService(db_session)

    student_answers = {
        "blank1": "correct",
        # blank2, blank3 누락
    }
    correct_answers = {
        "blank1": {"answer": "correct"},
        "blank2": {"answer": "answer2"},
        "blank3": {"answer": "answer3"},
    }

    # When: grade_answer 호출
    result = service.grade_answer(
        question_id="q-006",
        selected_answer=student_answers,
        correct_answer=correct_answers,
        points=30,
    )

    # Then: 10점 (1/3)
    assert result["is_correct"] is False
    assert result["points_earned"] == 10
    assert result["correct_count"] == 1
    assert result["total_blanks"] == 3


@pytest.mark.asyncio
async def test_grade_answer_string_empty_answer(db_session):
    """grade_answer가 빈 문자열 답안을 오답 처리한다."""
    # Given: 빈 답안
    service = GradingService(db_session)

    # When: grade_answer 호출
    result = service.grade_answer(
        question_id="q-007",
        selected_answer="",
        correct_answer="A",
        points=10,
    )

    # Then: 오답
    assert result["is_correct"] is False
    assert result["points_earned"] == 0


@pytest.mark.asyncio
async def test_grade_answer_string_whitespace_only(db_session):
    """grade_answer가 공백만 있는 답안을 오답 처리한다."""
    # Given: 공백만 있는 답안
    service = GradingService(db_session)

    # When: grade_answer 호출
    result = service.grade_answer(
        question_id="q-008",
        selected_answer="   ",
        correct_answer="A",
        points=10,
    )

    # Then: 오답
    assert result["is_correct"] is False
    assert result["points_earned"] == 0


@pytest.mark.asyncio
async def test_submit_answer_with_simple_fill_in_blank(db_session):
    """submit_answer가 간단한 빈칸 채우기 문제를 올바르게 채점한다."""
    # Given: 단일 빈칸 채우기 문제 (correct_answer는 string)
    user = User(
        id="student-fill-1",
        login_id="student_fill_1",
        name="빈칸 학생",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    question = Question(
        id="question-fill-1",
        concept_id="concept-001",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.FILL_IN_BLANK,
        difficulty=6,
        content="x + 5 = 10, x = _____",
        options=None,
        correct_answer="5",  # 단순 문자열
        explanation="x + 5 = 10이므로 x = 5",
        points=20,
    )
    db_session.add(question)

    attempt = TestAttempt(
        id="attempt-fill-1",
        test_id="test-001",
        student_id="student-fill-1",
        score=0,
        max_score=20,
    )
    db_session.add(attempt)

    await db_session.commit()

    # When: submit_answer 호출 (정답)
    service = GradingService(db_session)
    result = await service.submit_answer(
        attempt=attempt,
        question=question,
        selected_answer="5",
        time_spent_seconds=60,
        current_combo=0,
    )

    # Then: 정답
    assert result["is_correct"] is True
    assert result["points_earned"] == 20
    assert attempt.score == 20


@pytest.mark.asyncio
async def test_submit_answer_with_fill_in_blank_wrong(db_session):
    """submit_answer가 빈칸 채우기 오답을 올바르게 처리한다."""
    # Given: 빈칸 채우기 문제
    user = User(
        id="student-fill-2",
        login_id="student_fill_2",
        name="빈칸 학생 2",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    question = Question(
        id="question-fill-2",
        concept_id="concept-001",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.FILL_IN_BLANK,
        difficulty=6,
        content="2x = 10, x = _____",
        options=None,
        correct_answer="5",
        explanation="2x = 10이므로 x = 5",
        points=40,
    )
    db_session.add(question)

    attempt = TestAttempt(
        id="attempt-fill-2",
        test_id="test-002",
        student_id="student-fill-2",
        score=0,
        max_score=40,
    )
    db_session.add(attempt)

    await db_session.commit()

    # When: submit_answer 호출 (오답)
    service = GradingService(db_session)
    result = await service.submit_answer(
        attempt=attempt,
        question=question,
        selected_answer="10",  # 오답
        time_spent_seconds=60,
        current_combo=0,
    )

    # Then: 오답
    assert result["is_correct"] is False
    assert result["points_earned"] == 0
    assert attempt.score == 0


@pytest.mark.asyncio
async def test_override_to_correct_updates_answer_log(db_session):
    """override_to_correct가 오답을 정답으로 보정한다."""
    # Given: 오답으로 기록된 답안
    user = User(
        id="student-override",
        login_id="student_override",
        name="보정 학생",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    question = Question(
        id="question-override",
        concept_id="concept-001",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=6,
        content="문제",
        options=[],
        correct_answer="A",
        explanation="설명",
        points=10,
    )
    db_session.add(question)

    attempt = TestAttempt(
        id="attempt-override",
        test_id="test-override",
        student_id="student-override",
        score=0,
        max_score=10,
        correct_count=0,
        xp_earned=0,
        combo_max=0,
    )
    db_session.add(attempt)

    answer_log = AnswerLog(
        attempt_id="attempt-override",
        question_id="question-override",
        selected_answer="B",
        is_correct=False,
        time_spent_seconds=30,
        points_earned=0,
        combo_count=0,
    )
    db_session.add(answer_log)

    await db_session.commit()

    # When: override_to_correct 호출
    service = GradingService(db_session)
    prev_result = {
        "is_correct": False,
        "correct_answer": "A",
    }
    result = await service.override_to_correct(
        attempt=attempt,
        question=question,
        prev_result=prev_result,
        current_combo=0,
    )

    # Then: 정답으로 보정됨
    assert result["is_correct"] is True
    assert result["points_earned"] == 10
    assert result["combo_count"] == 1

    # AnswerLog 확인
    stmt = select(AnswerLog).where(
        AnswerLog.attempt_id == "attempt-override",
        AnswerLog.question_id == "question-override",
    )
    log = await db_session.scalar(stmt)
    assert log.is_correct is True
    assert log.points_earned == 10

    # TestAttempt 확인
    stmt2 = select(TestAttempt).where(TestAttempt.id == "attempt-override")
    updated_attempt = await db_session.scalar(stmt2)
    assert updated_attempt.score == 10
    assert updated_attempt.correct_count == 1


@pytest.mark.asyncio
async def test_override_to_correct_with_combo_bonus(db_session):
    """override_to_correct가 콤보 보너스를 적용한다."""
    # Given: 오답 기록 + 현재 콤보 4
    user = User(
        id="student-combo",
        login_id="student_combo",
        name="콤보 학생",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    question = Question(
        id="question-combo",
        concept_id="concept-001",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=6,
        content="문제",
        options=[],
        correct_answer="A",
        explanation="설명",
        points=10,
    )
    db_session.add(question)

    attempt = TestAttempt(
        id="attempt-combo",
        test_id="test-combo",
        student_id="student-combo",
        score=0,
        max_score=100,
        correct_count=0,
        xp_earned=0,
        combo_max=4,
    )
    db_session.add(attempt)

    answer_log = AnswerLog(
        attempt_id="attempt-combo",
        question_id="question-combo",
        selected_answer="B",
        is_correct=False,
        time_spent_seconds=30,
        points_earned=0,
        combo_count=0,
    )
    db_session.add(answer_log)

    await db_session.commit()

    # When: override_to_correct 호출 (현재 콤보 4 -> 5)
    service = GradingService(db_session)
    prev_result = {"is_correct": False, "correct_answer": "A"}
    result = await service.override_to_correct(
        attempt=attempt,
        question=question,
        prev_result=prev_result,
        current_combo=4,
    )

    # Then: 콤보 5 달성 (2.0x 보너스)
    assert result["combo_count"] == 5
    assert result["points_earned"] == 20  # 10 * 2.0


@pytest.mark.asyncio
async def test_submit_answer_enforces_max_score(db_session):
    """submit_answer가 최대 점수를 초과하지 않는다."""
    # Given: 거의 만점에 가까운 시도
    user = User(
        id="student-max",
        login_id="student_max",
        name="최대 학생",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    question = Question(
        id="question-max",
        concept_id="concept-001",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=6,
        content="문제",
        options=[],
        correct_answer="A",
        explanation="설명",
        points=10,
    )
    db_session.add(question)

    attempt = TestAttempt(
        id="attempt-max",
        test_id="test-max",
        student_id="student-max",
        score=95,  # 이미 95점
        max_score=100,
        correct_count=9,
        xp_earned=50,
        combo_max=9,
    )
    db_session.add(attempt)

    await db_session.commit()

    # When: submit_answer 호출 (콤보 9 -> 10, 10점 * 3.0 = 30점 시도)
    service = GradingService(db_session)
    result = await service.submit_answer(
        attempt=attempt,
        question=question,
        selected_answer="A",
        time_spent_seconds=30,
        current_combo=9,
    )

    # Then: 최대 100점까지만
    stmt = select(TestAttempt).where(TestAttempt.id == "attempt-max")
    updated_attempt = await db_session.scalar(stmt)
    assert updated_attempt.score == 100  # 95 + 30 = 125이지만 100으로 제한
    assert updated_attempt.score <= updated_attempt.max_score


@pytest.mark.asyncio
async def test_grade_answer_fill_in_blank_non_dict_student_answer(db_session):
    """grade_answer가 빈칸 채우기에서 non-dict 학생 답안을 빈 dict로 처리한다."""
    # Given: dict가 아닌 학생 답안
    service = GradingService(db_session)

    student_answers = "not a dict"
    correct_answers = {
        "blank1": {"answer": "5"},
        "blank2": {"answer": "10"},
    }

    # When: grade_answer 호출
    result = service.grade_answer(
        question_id="q-009",
        selected_answer=student_answers,
        correct_answer=correct_answers,
        points=20,
    )

    # Then: 0점
    assert result["is_correct"] is False
    assert result["points_earned"] == 0
    assert result["correct_count"] == 0
    assert result["total_blanks"] == 2


@pytest.mark.asyncio
async def test_grade_answer_fill_in_blank_zero_blanks(db_session):
    """grade_answer가 빈칸이 0개일 때 만점을 준다 (엣지 케이스)."""
    # Given: 빈칸 0개
    service = GradingService(db_session)

    student_answers = {}
    correct_answers = {}

    # When: grade_answer 호출
    result = service.grade_answer(
        question_id="q-010",
        selected_answer=student_answers,
        correct_answer=correct_answers,
        points=10,
    )

    # Then: 만점
    assert result["is_correct"] is True
    assert result["points_earned"] == 10
    assert result["correct_count"] == 0
    assert result["total_blanks"] == 0
