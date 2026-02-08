"""AdaptiveService DB 메서드 단위 테스트."""

from datetime import datetime, timezone

import pytest
from sqlalchemy import select

from app.models.answer_log import AnswerLog
from app.models.concept import Concept
from app.models.question import Question
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.user import User
from app.services.adaptive_service import AdaptiveService


@pytest.mark.asyncio
async def test_determine_initial_difficulty_new_student(db_session):
    """determine_initial_difficulty: 신규 학생(레벨 1, 기록 없음) -> 난이도 3."""
    # Given: 레벨 1인 신규 학생
    student = User(
        id="student-001",
        login_id="student01",
        name="신규 학생",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)

    concept = Concept(
        id="concept-001",
        name="일차방정식",
        grade="middle_1",
        category="concept",
        part="algebra",
    )
    db_session.add(concept)
    await db_session.commit()

    # When: determine_initial_difficulty 호출
    service = AdaptiveService(db_session)
    difficulty = await service.determine_initial_difficulty(
        "student-001", ["concept-001"]
    )

    # Then: 낮은 난이도(3) 반환
    # readiness = (1/10) * 0.4 + 0.5 * 0.6 = 0.04 + 0.3 = 0.34 < 0.35
    assert difficulty == 3


@pytest.mark.asyncio
async def test_determine_initial_difficulty_intermediate_student(db_session):
    """determine_initial_difficulty: 중급 학생(레벨 5, 정답률 70%) -> 난이도 6."""
    # Given: 레벨 5인 학생
    student = User(
        id="student-002",
        login_id="student02",
        name="중급 학생",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=5,
        total_xp=500,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)

    concept = Concept(
        id="concept-002",
        name="이차방정식",
        grade="middle_2",
        category="concept",
        part="algebra",
    )
    db_session.add(concept)

    test = Test(
        id="test-002",
        title="테스트 2",
        description="설명",
        grade="middle_2",
        concept_ids=["concept-002"],
        question_ids=["q-001", "q-002"],
        question_count=2,
        time_limit_minutes=10,
        is_active=True,
    )
    db_session.add(test)

    question = Question(
        id="q-001",
        concept_id="concept-002",
        category="concept",
        part="algebra",
        question_type="multiple_choice",
        difficulty=5,
        content="문제 내용",
        options=[],
        correct_answer="A",
        explanation="설명",
        points=10,
    )
    db_session.add(question)

    attempt = TestAttempt(
        id="attempt-002",
        test_id="test-002",
        student_id="student-002",
        score=0,
        max_score=10,
    )
    db_session.add(attempt)

    # 10개 중 7개 정답 (70% 정답률)
    for i in range(10):
        log = AnswerLog(
            id=f"log-002-{i}",
            attempt_id="attempt-002",
            question_id="q-001",
            selected_answer="A",
            is_correct=(i < 7),
            time_spent_seconds=30,
        )
        db_session.add(log)

    await db_session.commit()

    # When: determine_initial_difficulty 호출
    service = AdaptiveService(db_session)
    difficulty = await service.determine_initial_difficulty(
        "student-002", ["concept-002"]
    )

    # Then: 중간 난이도(6) 반환
    # readiness = (5/10) * 0.4 + 0.7 * 0.6 = 0.2 + 0.42 = 0.62 (0.35 ~ 0.65 범위)
    assert difficulty == 6


@pytest.mark.asyncio
async def test_determine_initial_difficulty_advanced_student(db_session):
    """determine_initial_difficulty: 고급 학생(레벨 10, 정답률 90%) -> 난이도 8."""
    # Given: 레벨 10인 고급 학생
    student = User(
        id="student-003",
        login_id="student03",
        name="고급 학생",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=10,
        total_xp=10000,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)

    concept = Concept(
        id="concept-003",
        name="미분",
        grade="high_1",
        category="concept",
        part="calc",
    )
    db_session.add(concept)

    test = Test(
        id="test-003",
        title="테스트 3",
        description="설명",
        grade="high_1",
        concept_ids=["concept-003"],
        question_ids=["q-003"],
        question_count=1,
        time_limit_minutes=10,
        is_active=True,
    )
    db_session.add(test)

    question = Question(
        id="q-003",
        concept_id="concept-003",
        category="concept",
        part="calc",
        question_type="multiple_choice",
        difficulty=8,
        content="미분 문제",
        options=[],
        correct_answer="A",
        explanation="설명",
        points=10,
    )
    db_session.add(question)

    attempt = TestAttempt(
        id="attempt-003",
        test_id="test-003",
        student_id="student-003",
        score=0,
        max_score=10,
    )
    db_session.add(attempt)

    # 10개 중 9개 정답 (90% 정답률)
    for i in range(10):
        log = AnswerLog(
            id=f"log-003-{i}",
            attempt_id="attempt-003",
            question_id="q-003",
            selected_answer="A",
            is_correct=(i < 9),
            time_spent_seconds=30,
        )
        db_session.add(log)

    await db_session.commit()

    # When: determine_initial_difficulty 호출
    service = AdaptiveService(db_session)
    difficulty = await service.determine_initial_difficulty(
        "student-003", ["concept-003"]
    )

    # Then: 높은 난이도(8) 반환
    # readiness = (10/10) * 0.4 + 0.9 * 0.6 = 0.4 + 0.54 = 0.94 >= 0.65
    assert difficulty == 8


@pytest.mark.asyncio
async def test_get_concept_accuracy_no_history(db_session):
    """_get_concept_accuracy: 기록이 없으면 중립값 0.5 반환."""
    # Given: 학생과 개념만 존재, 답변 기록 없음
    student = User(
        id="student-004",
        login_id="student04",
        name="기록 없는 학생",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)

    concept = Concept(
        id="concept-004",
        name="삼각함수",
        grade="middle_3",
        category="concept",
        part="func",
    )
    db_session.add(concept)
    await db_session.commit()

    # When: _get_concept_accuracy 호출
    service = AdaptiveService(db_session)
    accuracy = await service._get_concept_accuracy("student-004", ["concept-004"])

    # Then: 중립값 0.5 반환
    assert accuracy == 0.5


@pytest.mark.asyncio
async def test_get_concept_accuracy_with_history(db_session):
    """_get_concept_accuracy: 기록이 있으면 정답률 계산."""
    # Given: 학생, 개념, 답변 기록
    student = User(
        id="student-005",
        login_id="student05",
        name="학생",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)

    concept = Concept(
        id="concept-005",
        name="확률",
        grade="middle_2",
        category="concept",
        part="data",
    )
    db_session.add(concept)

    test = Test(
        id="test-005",
        title="확률 테스트",
        description="확률",
        grade="middle_2",
        concept_ids=["concept-005"],
        question_ids=["q-005"],
        question_count=1,
        time_limit_minutes=10,
        is_active=True,
    )
    db_session.add(test)

    question = Question(
        id="q-005",
        concept_id="concept-005",
        category="concept",
        part="data",
        question_type="multiple_choice",
        difficulty=5,
        content="확률 문제",
        options=[],
        correct_answer="A",
        explanation="설명",
        points=10,
    )
    db_session.add(question)

    attempt = TestAttempt(
        id="attempt-005",
        test_id="test-005",
        student_id="student-005",
        score=0,
        max_score=10,
    )
    db_session.add(attempt)

    # 20개 중 15개 정답 (75% 정답률)
    for i in range(20):
        log = AnswerLog(
            id=f"log-005-{i}",
            attempt_id="attempt-005",
            question_id="q-005",
            selected_answer="A",
            is_correct=(i < 15),
            time_spent_seconds=30,
        )
        db_session.add(log)

    await db_session.commit()

    # When: _get_concept_accuracy 호출
    service = AdaptiveService(db_session)
    accuracy = await service._get_concept_accuracy("student-005", ["concept-005"])

    # Then: 0.75 반환 (15/20)
    assert accuracy == 0.75


@pytest.mark.asyncio
async def test_select_first_question(db_session):
    """select_first_question: 초기 난이도에 맞는 첫 문제 선택."""
    # Given: 신규 학생(난이도 3)과 다양한 난이도의 문제들
    student = User(
        id="student-006",
        login_id="student06",
        name="학생 6",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)

    concept = Concept(
        id="concept-006",
        name="개념 6",
        grade="middle_1",
        category="concept",
        part="algebra",
    )
    db_session.add(concept)

    # 난이도 1, 3, 5, 7, 9의 문제들 생성
    question_ids = []
    for diff in [1, 3, 5, 7, 9]:
        q_id = f"q-006-{diff}"
        question_ids.append(q_id)
        question = Question(
            id=q_id,
            concept_id="concept-006",
            category="concept",
            part="algebra",
            question_type="multiple_choice",
            difficulty=diff,
            content=f"난이도 {diff} 문제",
            options=[],
            correct_answer="A",
            explanation="설명",
            points=10,
        )
        db_session.add(question)

    test = Test(
        id="test-006",
        title="테스트 6",
        description="설명",
        grade="middle_1",
        concept_ids=["concept-006"],
        question_ids=question_ids,
        question_count=5,
        time_limit_minutes=10,
        is_active=True,
    )
    db_session.add(test)
    await db_session.commit()

    # When: select_first_question 호출
    service = AdaptiveService(db_session)
    question = await service.select_first_question(test, "student-006")

    # Then: 난이도 3 문제 선택됨
    assert question is not None
    assert question.difficulty == 3
    assert question.id == "q-006-3"


@pytest.mark.asyncio
async def test_select_next_question_increases_difficulty_on_correct(db_session):
    """select_next_question: 정답 시 난이도 증가."""
    # Given: 적응형 테스트 진행 중 (현재 난이도 5, 마지막 정답)
    student = User(
        id="student-007",
        login_id="student07",
        name="학생 7",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)

    concept = Concept(
        id="concept-007",
        name="개념 7",
        grade="middle_1",
        category="concept",
        part="algebra",
    )
    db_session.add(concept)

    # 난이도 5, 6 문제들 생성
    for diff in [5, 6]:
        question = Question(
            id=f"q-007-{diff}",
            concept_id="concept-007",
            category="concept",
            part="algebra",
            question_type="multiple_choice",
            difficulty=diff,
            content=f"난이도 {diff} 문제",
            options=[],
            correct_answer="A",
            explanation="설명",
            points=10,
        )
        db_session.add(question)

    test = Test(
        id="test-007",
        title="적응형 테스트",
        description="설명",
        grade="middle_1",
        concept_ids=["concept-007"],
        question_ids=["q-007-5", "q-007-6"],
        question_count=5,
        time_limit_minutes=10,
        is_active=True,
        is_adaptive=True,
    )
    db_session.add(test)

    attempt = TestAttempt(
        id="attempt-007",
        test_id="test-007",
        student_id="student-007",
        score=10,
        max_score=10,
        total_count=5,
        current_difficulty=5,
        adaptive_question_ids=["q-007-5"],
        is_adaptive=True,
    )
    db_session.add(attempt)

    # 마지막 답변: 난이도 5 정답
    log = AnswerLog(
        id="log-007-1",
        attempt_id="attempt-007",
        question_id="q-007-5",
        selected_answer="A",
        is_correct=True,
        question_difficulty=5,
        time_spent_seconds=30,
    )
    db_session.add(log)
    await db_session.commit()

    # When: select_next_question 호출
    service = AdaptiveService(db_session)
    question, target_difficulty = await service.select_next_question(attempt)

    # Then: 난이도 6 문제 선택됨 (5 + 1)
    assert question is not None
    assert target_difficulty == 6
    assert question.difficulty == 6
    assert attempt.current_difficulty == 6


@pytest.mark.asyncio
async def test_select_next_question_decreases_difficulty_on_wrong(db_session):
    """select_next_question: 오답 시 난이도 감소."""
    # Given: 적응형 테스트 진행 중 (현재 난이도 5, 마지막 오답)
    student = User(
        id="student-008",
        login_id="student08",
        name="학생 8",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)

    concept = Concept(
        id="concept-008",
        name="개념 8",
        grade="middle_1",
        category="concept",
        part="algebra",
    )
    db_session.add(concept)

    # 난이도 4, 5 문제들 생성
    for diff in [4, 5]:
        question = Question(
            id=f"q-008-{diff}",
            concept_id="concept-008",
            category="concept",
            part="algebra",
            question_type="multiple_choice",
            difficulty=diff,
            content=f"난이도 {diff} 문제",
            options=[],
            correct_answer="A",
            explanation="설명",
            points=10,
        )
        db_session.add(question)

    test = Test(
        id="test-008",
        title="적응형 테스트",
        description="설명",
        grade="middle_1",
        concept_ids=["concept-008"],
        question_ids=["q-008-4", "q-008-5"],
        question_count=5,
        time_limit_minutes=10,
        is_active=True,
        is_adaptive=True,
    )
    db_session.add(test)

    attempt = TestAttempt(
        id="attempt-008",
        test_id="test-008",
        student_id="student-008",
        score=0,
        max_score=10,
        total_count=5,
        current_difficulty=5,
        adaptive_question_ids=["q-008-5"],
        is_adaptive=True,
    )
    db_session.add(attempt)

    # 마지막 답변: 난이도 5 오답
    log = AnswerLog(
        id="log-008-1",
        attempt_id="attempt-008",
        question_id="q-008-5",
        selected_answer="B",
        is_correct=False,
        question_difficulty=5,
        time_spent_seconds=30,
    )
    db_session.add(log)
    await db_session.commit()

    # When: select_next_question 호출
    service = AdaptiveService(db_session)
    question, target_difficulty = await service.select_next_question(attempt)

    # Then: 난이도 4 문제 선택됨 (5 - 1)
    assert question is not None
    assert target_difficulty == 4
    assert question.difficulty == 4
    assert attempt.current_difficulty == 4


@pytest.mark.asyncio
async def test_select_next_question_returns_none_when_completed(db_session):
    """select_next_question: 모든 문제 완료 시 None 반환."""
    # Given: 이미 모든 문제를 푼 시도
    student = User(
        id="student-009",
        login_id="student09",
        name="학생 9",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)

    concept = Concept(
        id="concept-009",
        name="개념 9",
        grade="middle_1",
        category="concept",
        part="algebra",
    )
    db_session.add(concept)

    test = Test(
        id="test-009",
        title="적응형 테스트",
        description="설명",
        grade="middle_1",
        concept_ids=["concept-009"],
        question_ids=["q-009-1", "q-009-2"],
        question_count=2,
        time_limit_minutes=10,
        is_active=True,
        is_adaptive=True,
    )
    db_session.add(test)

    # 이미 2문제 모두 푼 상태 (total_count = 2, answered = 2)
    attempt = TestAttempt(
        id="attempt-009",
        test_id="test-009",
        student_id="student-009",
        score=20,
        max_score=20,
        total_count=2,
        current_difficulty=5,
        adaptive_question_ids=["q-009-1", "q-009-2"],
        is_adaptive=True,
    )
    db_session.add(attempt)
    await db_session.commit()

    # When: select_next_question 호출
    service = AdaptiveService(db_session)
    question, target_difficulty = await service.select_next_question(attempt)

    # Then: None 반환 (모든 문제 완료)
    assert question is None
    assert target_difficulty == 5  # 현재 난이도 유지


@pytest.mark.asyncio
async def test_peek_next_difficulty(db_session):
    """peek_next_difficulty: 다음 문제의 예상 난이도 반환."""
    # Given: 적응형 테스트 진행 중
    student = User(
        id="student-010",
        login_id="student10",
        name="학생 10",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)

    test = Test(
        id="test-010",
        title="적응형 테스트",
        description="설명",
        grade="middle_1",
        concept_ids=["concept-010"],
        question_ids=["q-010-1"],
        question_count=5,
        time_limit_minutes=10,
        is_active=True,
        is_adaptive=True,
    )
    db_session.add(test)

    attempt = TestAttempt(
        id="attempt-010",
        test_id="test-010",
        student_id="student-010",
        score=10,
        max_score=10,
        total_count=5,
        current_difficulty=6,
        adaptive_question_ids=["q-010-1"],
        is_adaptive=True,
    )
    db_session.add(attempt)

    # 마지막 답변: 정답
    log = AnswerLog(
        id="log-010-1",
        attempt_id="attempt-010",
        question_id="q-010-1",
        selected_answer="A",
        is_correct=True,
        question_difficulty=6,
        time_spent_seconds=30,
    )
    db_session.add(log)
    await db_session.commit()

    # When: peek_next_difficulty 호출
    service = AdaptiveService(db_session)
    next_difficulty = await service.peek_next_difficulty(attempt)

    # Then: 다음 난이도 7 예상 (6 + 1)
    assert next_difficulty == 7


@pytest.mark.asyncio
async def test_peek_next_difficulty_returns_none_when_completed(db_session):
    """peek_next_difficulty: 완료된 테스트는 None 반환."""
    # Given: 완료된 적응형 테스트
    student = User(
        id="student-011",
        login_id="student11",
        name="학생 11",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)

    test = Test(
        id="test-011",
        title="적응형 테스트",
        description="설명",
        grade="middle_1",
        concept_ids=["concept-011"],
        question_ids=["q-011-1"],
        question_count=1,
        time_limit_minutes=10,
        is_active=True,
        is_adaptive=True,
    )
    db_session.add(test)

    # 모든 문제 완료
    attempt = TestAttempt(
        id="attempt-011",
        test_id="test-011",
        student_id="student-011",
        score=10,
        max_score=10,
        total_count=1,
        current_difficulty=6,
        adaptive_question_ids=["q-011-1"],
        is_adaptive=True,
    )
    db_session.add(attempt)
    await db_session.commit()

    # When: peek_next_difficulty 호출
    service = AdaptiveService(db_session)
    next_difficulty = await service.peek_next_difficulty(attempt)

    # Then: None 반환
    assert next_difficulty is None


@pytest.mark.asyncio
async def test_peek_next_difficulty_returns_none_for_non_adaptive(db_session):
    """peek_next_difficulty: 비적응형 테스트는 None 반환."""
    # Given: 비적응형 테스트
    student = User(
        id="student-012",
        login_id="student12",
        name="학생 12",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)

    test = Test(
        id="test-012",
        title="일반 테스트",
        description="설명",
        grade="middle_1",
        concept_ids=["concept-012"],
        question_ids=["q-012-1"],
        question_count=1,
        time_limit_minutes=10,
        is_active=True,
        is_adaptive=False,  # 비적응형
    )
    db_session.add(test)

    attempt = TestAttempt(
        id="attempt-012",
        test_id="test-012",
        student_id="student-012",
        score=0,
        max_score=10,
        total_count=1,
        is_adaptive=False,
    )
    db_session.add(attempt)
    await db_session.commit()

    # When: peek_next_difficulty 호출
    service = AdaptiveService(db_session)
    next_difficulty = await service.peek_next_difficulty(attempt)

    # Then: None 반환 (비적응형 테스트)
    assert next_difficulty is None
