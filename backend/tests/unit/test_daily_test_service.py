"""DailyTestService 단위 테스트."""

from datetime import datetime, timezone, timedelta

import pytest
from sqlalchemy import select

from app.models.chapter import Chapter
from app.models.chapter_progress import ChapterProgress
from app.models.concept import Concept
from app.models.concept_mastery import ConceptMastery
from app.models.daily_test_record import DailyTestRecord
from app.models.question import Question
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.user import User
from app.schemas.common import QuestionCategory, QuestionType, ProblemPart
from app.services.daily_test_service import DailyTestService, DAILY_CATEGORIES, KST


@pytest.mark.asyncio
async def test_get_today_str_returns_kst_date(db_session):
    """get_today_str이 KST 기준으로 오늘 날짜를 반환한다."""
    # Given: DailyTestService 인스턴스
    service = DailyTestService(db_session)

    # When: get_today_str 호출
    today_str = service.get_today_str()

    # Then: YYYY-MM-DD 형식의 문자열이 반환됨
    assert isinstance(today_str, str)
    assert len(today_str) == 10
    assert today_str.count("-") == 2

    # KST 기준 오늘 날짜와 일치하는지 확인
    expected = datetime.now(KST).date().isoformat()
    assert today_str == expected


@pytest.mark.asyncio
async def test_get_or_create_daily_test_creates_new_record(db_session):
    """get_or_create_daily_test가 새로운 일일 테스트를 생성한다."""
    # Given: 학생과 개념, 문제가 존재
    user = User(
        id="student-daily-001",
        login_id="daily_student_001",
        name="테스트 학생",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    concept = Concept(
        id="concept-daily-001",
        name="개념 1",
        grade="middle_1",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
    )
    db_session.add(concept)

    chapter = Chapter(
        id="chapter-daily-001",
        name="챕터 1",
        grade="middle_1",
        semester=1,
        chapter_number=1,
        concept_ids=["concept-daily-001"],
    )
    db_session.add(chapter)

    # 챕터 해금
    chapter_progress = ChapterProgress(
        student_id="student-daily-001",
        chapter_id="chapter-daily-001",
        is_unlocked=True,
    )
    db_session.add(chapter_progress)

    # 개념 해금
    mastery = ConceptMastery(
        student_id="student-daily-001",
        concept_id="concept-daily-001",
        is_unlocked=True,
        mastery_percentage=50,
    )
    db_session.add(mastery)

    # 문제 생성
    question = Question(
        id="question-daily-001",
        concept_id="concept-daily-001",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=5,
        content="테스트 문제",
        options=[
            {"id": "1", "label": "A", "text": "답 1"},
            {"id": "2", "label": "B", "text": "답 2"},
        ],
        correct_answer="A",
        explanation="설명",
    )
    db_session.add(question)
    await db_session.commit()

    # When: get_or_create_daily_test 호출
    service = DailyTestService(db_session)
    record = await service.get_or_create_daily_test("student-daily-001", "concept")

    # Then: 새로운 레코드가 생성됨
    assert record is not None
    assert record.student_id == "student-daily-001"
    assert record.category == "concept"
    assert record.status == "pending"
    assert record.date == service.get_today_str()
    assert record.total_count >= 0


@pytest.mark.asyncio
async def test_get_or_create_daily_test_returns_existing_record(db_session):
    """get_or_create_daily_test가 이미 존재하는 레코드를 반환한다."""
    # Given: 이미 생성된 일일 테스트
    user = User(
        id="student-daily-002",
        login_id="daily_student_002",
        name="테스트 학생 2",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    test = Test(
        id="test-daily-002",
        title="기존 테스트",
        description="기존 테스트",
        grade="middle_1",
        category="concept",
        concept_ids=["concept-001"],
        question_ids=["question-001"],
        question_count=1,
        is_active=True,
    )
    db_session.add(test)

    service = DailyTestService(db_session)
    today = service.get_today_str()

    existing_record = DailyTestRecord(
        student_id="student-daily-002",
        date=today,
        category="concept",
        test_id="test-daily-002",
        status="in_progress",
        total_count=1,
    )
    db_session.add(existing_record)
    await db_session.commit()

    # When: 같은 조건으로 get_or_create_daily_test 호출
    record = await service.get_or_create_daily_test("student-daily-002", "concept")

    # Then: 기존 레코드가 반환됨
    assert record.id == existing_record.id
    assert record.status == "in_progress"


@pytest.mark.asyncio
async def test_get_today_tests_returns_all_three_categories(db_session):
    """get_today_tests가 3개 카테고리의 테스트를 모두 반환한다."""
    # Given: 학생과 기본 데이터
    user = User(
        id="student-daily-003",
        login_id="daily_student_003",
        name="테스트 학생 3",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    concept = Concept(
        id="concept-daily-003",
        name="개념 3",
        grade="middle_1",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
    )
    db_session.add(concept)

    chapter = Chapter(
        id="chapter-daily-003",
        name="챕터 3",
        grade="middle_1",
        semester=1,
        chapter_number=1,
        concept_ids=["concept-daily-003"],
    )
    db_session.add(chapter)

    chapter_progress = ChapterProgress(
        student_id="student-daily-003",
        chapter_id="chapter-daily-003",
        is_unlocked=True,
    )
    db_session.add(chapter_progress)

    mastery = ConceptMastery(
        student_id="student-daily-003",
        concept_id="concept-daily-003",
        is_unlocked=True,
        mastery_percentage=60,
    )
    db_session.add(mastery)
    await db_session.commit()

    # When: get_today_tests 호출
    service = DailyTestService(db_session)
    records, ai_count = await service.get_today_tests("student-daily-003")

    # Then: 3개 카테고리의 레코드가 반환됨
    assert len(records) == 3
    categories = {r.category for r in records}
    assert categories == {"concept", "computation", "fill_in_blank"}


@pytest.mark.asyncio
async def test_start_daily_test_creates_attempt(db_session):
    """start_daily_test가 TestAttempt를 생성한다."""
    # Given: 일일 테스트 레코드와 테스트
    user = User(
        id="student-daily-004",
        login_id="daily_student_004",
        name="테스트 학생 4",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    concept = Concept(
        id="concept-daily-004",
        name="개념 4",
        grade="middle_1",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
    )
    db_session.add(concept)

    question = Question(
        id="question-daily-004",
        concept_id="concept-daily-004",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=5,
        content="테스트 문제 4",
        options=[{"id": "1", "label": "A", "text": "답"}],
        correct_answer="A",
        explanation="설명",
    )
    db_session.add(question)

    test = Test(
        id="test-daily-004",
        title="일일 테스트 4",
        description="테스트",
        grade="middle_1",
        category="concept",
        concept_ids=["concept-daily-004"],
        question_ids=["question-daily-004"],
        question_count=1,
        is_active=True,
        shuffle_options=True,
    )
    db_session.add(test)

    service = DailyTestService(db_session)
    today = service.get_today_str()

    record = DailyTestRecord(
        student_id="student-daily-004",
        date=today,
        category="concept",
        test_id="test-daily-004",
        status="pending",
        total_count=1,
    )
    db_session.add(record)
    await db_session.commit()

    # When: start_daily_test 호출
    attempt = await service.start_daily_test("student-daily-004", record.id)

    # Then: TestAttempt가 생성되고 레코드 상태가 업데이트됨
    assert attempt is not None
    assert attempt.student_id == "student-daily-004"
    assert attempt.test_id == "test-daily-004"

    # 레코드 상태 확인
    await db_session.refresh(record)
    assert record.status == "in_progress"
    assert record.attempt_id == attempt.id


@pytest.mark.asyncio
async def test_start_daily_test_returns_existing_attempt(db_session):
    """start_daily_test가 이미 시작된 경우 기존 attempt를 반환한다."""
    # Given: 이미 시작된 일일 테스트
    user = User(
        id="student-daily-005",
        login_id="daily_student_005",
        name="테스트 학생 5",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    concept = Concept(
        id="concept-daily-005",
        name="개념 5",
        grade="middle_1",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
    )
    db_session.add(concept)

    question = Question(
        id="question-daily-005",
        concept_id="concept-daily-005",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=5,
        content="테스트 문제 5",
        options=[{"id": "1", "label": "A", "text": "답"}],
        correct_answer="A",
        explanation="설명",
    )
    db_session.add(question)

    test = Test(
        id="test-daily-005",
        title="일일 테스트 5",
        description="테스트",
        grade="middle_1",
        category="concept",
        concept_ids=["concept-daily-005"],
        question_ids=["question-daily-005"],
        question_count=1,
        is_active=True,
        shuffle_options=False,
    )
    db_session.add(test)

    existing_attempt = TestAttempt(
        id="attempt-daily-005",
        test_id="test-daily-005",
        student_id="student-daily-005",
        started_at=datetime.now(timezone.utc),
    )
    db_session.add(existing_attempt)

    service = DailyTestService(db_session)
    today = service.get_today_str()

    record = DailyTestRecord(
        student_id="student-daily-005",
        date=today,
        category="concept",
        test_id="test-daily-005",
        status="in_progress",
        total_count=1,
        attempt_id="attempt-daily-005",
    )
    db_session.add(record)
    await db_session.commit()

    # When: start_daily_test 재호출
    attempt = await service.start_daily_test("student-daily-005", record.id)

    # Then: 기존 attempt가 반환됨
    assert attempt.id == existing_attempt.id


@pytest.mark.asyncio
async def test_try_complete_daily_test_updates_record(db_session):
    """try_complete_daily_test가 완료된 attempt에 대해 레코드를 업데이트한다."""
    # Given: 완료된 TestAttempt
    user = User(
        id="student-daily-006",
        login_id="daily_student_006",
        name="테스트 학생 6",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    test = Test(
        id="test-daily-006",
        title="일일 테스트 6",
        description="테스트",
        grade="middle_1",
        category="concept",
        concept_ids=["concept-006"],
        question_ids=["question-006"],
        question_count=1,
        is_active=True,
    )
    db_session.add(test)

    completed_at = datetime.now(timezone.utc)
    attempt = TestAttempt(
        id="attempt-daily-006",
        test_id="test-daily-006",
        student_id="student-daily-006",
        started_at=completed_at - timedelta(minutes=10),
        completed_at=completed_at,
        score=80,
        max_score=100,
        correct_count=8,
        total_count=10,
    )
    db_session.add(attempt)

    service = DailyTestService(db_session)
    today = service.get_today_str()

    record = DailyTestRecord(
        student_id="student-daily-006",
        date=today,
        category="concept",
        test_id="test-daily-006",
        status="in_progress",
        total_count=10,
        attempt_id="attempt-daily-006",
    )
    db_session.add(record)
    await db_session.commit()

    # When: try_complete_daily_test 호출
    await service.try_complete_daily_test("attempt-daily-006")

    # Then: 레코드 상태가 업데이트됨
    await db_session.refresh(record)
    assert record.status == "completed"
    assert record.score == 80
    assert record.max_score == 100
    assert record.correct_count == 8
    assert record.total_count == 10
    assert record.completed_at is not None


@pytest.mark.asyncio
async def test_get_history_returns_past_records(db_session):
    """get_history가 과거 일일 테스트 기록을 반환한다."""
    # Given: 여러 날짜의 일일 테스트 기록
    user = User(
        id="student-daily-007",
        login_id="daily_student_007",
        name="테스트 학생 7",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    test = Test(
        id="test-daily-007",
        title="일일 테스트 7",
        description="테스트",
        grade="middle_1",
        category="concept",
        concept_ids=["concept-007"],
        question_ids=["question-007"],
        question_count=5,
        is_active=True,
    )
    db_session.add(test)

    service = DailyTestService(db_session)
    today = service.get_today_str()
    yesterday = (datetime.now(KST) - timedelta(days=1)).date().isoformat()
    two_days_ago = (datetime.now(KST) - timedelta(days=2)).date().isoformat()

    # 오늘 기록 (제외되어야 함)
    today_record = DailyTestRecord(
        student_id="student-daily-007",
        date=today,
        category="concept",
        test_id="test-daily-007",
        status="completed",
        total_count=5,
    )
    db_session.add(today_record)

    # 어제 기록
    yesterday_record = DailyTestRecord(
        student_id="student-daily-007",
        date=yesterday,
        category="concept",
        test_id="test-daily-007",
        status="completed",
        total_count=5,
        score=90,
    )
    db_session.add(yesterday_record)

    # 2일 전 기록
    two_days_record = DailyTestRecord(
        student_id="student-daily-007",
        date=two_days_ago,
        category="computation",
        test_id="test-daily-007",
        status="completed",
        total_count=5,
        score=80,
    )
    db_session.add(two_days_record)
    await db_session.commit()

    # When: get_history 호출
    records, total = await service.get_history("student-daily-007", page=1, page_size=10)

    # Then: 과거 기록만 반환됨 (오늘 제외)
    assert total == 2
    assert len(records) == 2
    # 날짜 내림차순 확인
    assert records[0].date == yesterday
    assert records[1].date == two_days_ago


@pytest.mark.asyncio
async def test_get_student_available_concept_ids_returns_unlocked_concepts(db_session):
    """_get_student_available_concept_ids가 해금된 개념만 반환한다."""
    # Given: 해금된 챕터와 개념들
    user = User(
        id="student-daily-008",
        login_id="daily_student_008",
        name="테스트 학생 8",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    # 개념 생성
    concept1 = Concept(
        id="concept-daily-008-1",
        name="개념 8-1",
        grade="middle_1",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
    )
    concept2 = Concept(
        id="concept-daily-008-2",
        name="개념 8-2",
        grade="middle_1",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
    )
    concept3 = Concept(
        id="concept-daily-008-3",
        name="개념 8-3",
        grade="middle_1",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
    )
    db_session.add_all([concept1, concept2, concept3])

    # 챕터 생성
    chapter = Chapter(
        id="chapter-daily-008",
        name="챕터 8",
        grade="middle_1",
        semester=1,
        chapter_number=1,
        concept_ids=["concept-daily-008-1", "concept-daily-008-2", "concept-daily-008-3"],
    )
    db_session.add(chapter)

    # 챕터 해금
    chapter_progress = ChapterProgress(
        student_id="student-daily-008",
        chapter_id="chapter-daily-008",
        is_unlocked=True,
    )
    db_session.add(chapter_progress)

    # 개념 1, 2만 해금 (3은 잠김)
    mastery1 = ConceptMastery(
        student_id="student-daily-008",
        concept_id="concept-daily-008-1",
        is_unlocked=True,
    )
    mastery2 = ConceptMastery(
        student_id="student-daily-008",
        concept_id="concept-daily-008-2",
        is_unlocked=True,
    )
    mastery3 = ConceptMastery(
        student_id="student-daily-008",
        concept_id="concept-daily-008-3",
        is_unlocked=False,
    )
    db_session.add_all([mastery1, mastery2, mastery3])
    await db_session.commit()

    # When: _get_student_available_concept_ids 호출
    service = DailyTestService(db_session)
    concept_ids = await service._get_student_available_concept_ids(
        "student-daily-008", "middle_1"
    )

    # Then: 해금된 개념만 반환됨
    assert len(concept_ids) == 2
    assert "concept-daily-008-1" in concept_ids
    assert "concept-daily-008-2" in concept_ids
    assert "concept-daily-008-3" not in concept_ids


@pytest.mark.asyncio
async def test_get_mastery_map_returns_concept_percentages(db_session):
    """_get_mastery_map이 개념별 숙련도를 반환한다."""
    # Given: 여러 개념의 숙련도
    user = User(
        id="student-daily-009",
        login_id="daily_student_009",
        name="테스트 학생 9",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    masteries = [
        ConceptMastery(
            student_id="student-daily-009",
            concept_id="concept-a",
            is_unlocked=True,
            mastery_percentage=80,
        ),
        ConceptMastery(
            student_id="student-daily-009",
            concept_id="concept-b",
            is_unlocked=True,
            mastery_percentage=60,
        ),
        ConceptMastery(
            student_id="student-daily-009",
            concept_id="concept-c",
            is_unlocked=True,
            mastery_percentage=90,
        ),
    ]
    for m in masteries:
        db_session.add(m)
    await db_session.commit()

    # When: _get_mastery_map 호출
    service = DailyTestService(db_session)
    mastery_map = await service._get_mastery_map("student-daily-009")

    # Then: 개념별 숙련도 맵이 반환됨
    assert len(mastery_map) == 3
    assert mastery_map["concept-a"] == 80
    assert mastery_map["concept-b"] == 60
    assert mastery_map["concept-c"] == 90


@pytest.mark.asyncio
async def test_mastery_to_difficulty_range_maps_correctly(db_session):
    """_mastery_to_difficulty_range가 숙련도를 난이도 범위로 매핑한다."""
    # Given: DailyTestService 인스턴스
    service = DailyTestService(db_session)

    # When & Then: 다양한 숙련도에 대한 난이도 범위 확인
    # 0% -> 난이도 1 기준, 범위 1~2
    diff_min, diff_max = service._mastery_to_difficulty_range(0)
    assert diff_min == 1
    assert diff_max == 2

    # 50% -> 난이도 5 기준, 범위 4~6
    diff_min, diff_max = service._mastery_to_difficulty_range(50)
    assert diff_min == 4
    assert diff_max == 6

    # 100% -> 난이도 9 기준, 범위 8~10
    diff_min, diff_max = service._mastery_to_difficulty_range(100)
    assert diff_min == 8
    assert diff_max == 10


@pytest.mark.asyncio
async def test_get_recently_used_questions_returns_recent_question_ids(db_session):
    """_get_recently_used_questions가 최근 출제 문제 ID를 반환한다."""
    # Given: 최근 일일 테스트 기록
    user = User(
        id="student-daily-010",
        login_id="daily_student_010",
        name="테스트 학생 10",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    # 2일 전 테스트
    test1 = Test(
        id="test-recent-1",
        title="테스트 1",
        description="테스트",
        grade="middle_1",
        category="concept",
        concept_ids=["concept-1"],
        question_ids=["q1", "q2", "q3"],
        question_count=3,
        is_active=True,
    )
    db_session.add(test1)

    service = DailyTestService(db_session)
    two_days_ago = (datetime.now(KST) - timedelta(days=2)).date().isoformat()

    record1 = DailyTestRecord(
        student_id="student-daily-010",
        date=two_days_ago,
        category="concept",
        test_id="test-recent-1",
        status="completed",
        total_count=3,
    )
    db_session.add(record1)

    # 오늘 테스트
    test2 = Test(
        id="test-recent-2",
        title="테스트 2",
        description="테스트",
        grade="middle_1",
        category="concept",
        concept_ids=["concept-2"],
        question_ids=["q4", "q5"],
        question_count=2,
        is_active=True,
    )
    db_session.add(test2)

    today = service.get_today_str()
    record2 = DailyTestRecord(
        student_id="student-daily-010",
        date=today,
        category="concept",
        test_id="test-recent-2",
        status="completed",
        total_count=2,
    )
    db_session.add(record2)
    await db_session.commit()

    # When: _get_recently_used_questions 호출 (최근 3일)
    used_ids = await service._get_recently_used_questions(
        "student-daily-010", "concept", days=3
    )

    # Then: 최근 3일 내 출제 문제 ID가 반환됨
    assert len(used_ids) == 5
    assert set(used_ids) == {"q1", "q2", "q3", "q4", "q5"}


@pytest.mark.asyncio
async def test_get_recently_unlocked_concepts_returns_recent_concepts(db_session):
    """_get_recently_unlocked_concepts가 최근 해금된 개념을 반환한다."""
    # Given: 최근 해금된 개념들
    user = User(
        id="student-daily-011",
        login_id="daily_student_011",
        name="테스트 학생 11",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    now = datetime.now(KST)

    # 10일 전 해금 (최근 14일 내)
    mastery1 = ConceptMastery(
        student_id="student-daily-011",
        concept_id="concept-recent-1",
        is_unlocked=True,
        unlocked_at=now - timedelta(days=10),
    )

    # 20일 전 해금 (14일 이상 지남)
    mastery2 = ConceptMastery(
        student_id="student-daily-011",
        concept_id="concept-recent-2",
        is_unlocked=True,
        unlocked_at=now - timedelta(days=20),
    )

    # 오늘 해금
    mastery3 = ConceptMastery(
        student_id="student-daily-011",
        concept_id="concept-recent-3",
        is_unlocked=True,
        unlocked_at=now,
    )

    db_session.add_all([mastery1, mastery2, mastery3])
    await db_session.commit()

    # When: _get_recently_unlocked_concepts 호출 (최근 14일)
    service = DailyTestService(db_session)
    recent_concepts = await service._get_recently_unlocked_concepts(
        "student-daily-011", days=14
    )

    # Then: 최근 14일 내 해금된 개념만 반환됨
    assert len(recent_concepts) == 2
    assert "concept-recent-1" in recent_concepts
    assert "concept-recent-3" in recent_concepts
    assert "concept-recent-2" not in recent_concepts


@pytest.mark.asyncio
async def test_select_questions_filters_by_difficulty(db_session):
    """_select_questions가 난이도 범위에 맞는 문제를 선택한다."""
    # Given: 다양한 난이도의 문제들
    user = User(
        id="student-daily-012",
        login_id="daily_student_012",
        name="테스트 학생 12",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    concept = Concept(
        id="concept-daily-012",
        name="개념 12",
        grade="middle_1",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
    )
    db_session.add(concept)

    chapter = Chapter(
        id="chapter-daily-012",
        name="챕터 12",
        grade="middle_1",
        semester=1,
        chapter_number=1,
        concept_ids=["concept-daily-012"],
    )
    db_session.add(chapter)

    chapter_progress = ChapterProgress(
        student_id="student-daily-012",
        chapter_id="chapter-daily-012",
        is_unlocked=True,
    )
    db_session.add(chapter_progress)

    # 숙련도 70% (약점 아님 ≥60%, 평균 난이도 7, 범위 6~8)
    mastery = ConceptMastery(
        student_id="student-daily-012",
        concept_id="concept-daily-012",
        is_unlocked=True,
        mastery_percentage=70,
    )
    db_session.add(mastery)

    # 다양한 난이도의 문제들
    for i, diff in enumerate([1, 3, 4, 5, 6, 7, 9], start=1):
        question = Question(
            id=f"q-diff-{i}",
            concept_id="concept-daily-012",
            category=QuestionCategory.CONCEPT,
            part=ProblemPart.CALC,
            question_type=QuestionType.MULTIPLE_CHOICE,
            difficulty=diff,
            content=f"문제 {i}",
            options=[{"id": "1", "label": "A", "text": "답"}],
            correct_answer="A",
            explanation="설명",
            is_active=True,
        )
        db_session.add(question)
    await db_session.commit()

    # When: _select_questions 호출
    service = DailyTestService(db_session)
    selected_ids = await service._select_questions(
        "student-daily-012", "concept", "middle_1", count=5
    )

    # Then: 난이도 6~8 범위의 문제만 선택됨 (70% → center 7, range 6~8)
    stmt = select(Question).where(Question.id.in_(selected_ids))
    selected_questions = list((await db_session.scalars(stmt)).all())

    for q in selected_questions:
        assert 6 <= q.difficulty <= 8


@pytest.mark.asyncio
async def test_select_questions_excludes_recently_used(db_session):
    """_select_questions가 최근 출제 문제를 제외한다."""
    # Given: 문제와 최근 출제 기록
    user = User(
        id="student-daily-013",
        login_id="daily_student_013",
        name="테스트 학생 13",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    concept = Concept(
        id="concept-daily-013",
        name="개념 13",
        grade="middle_1",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
    )
    db_session.add(concept)

    chapter = Chapter(
        id="chapter-daily-013",
        name="챕터 13",
        grade="middle_1",
        semester=1,
        chapter_number=1,
        concept_ids=["concept-daily-013"],
    )
    db_session.add(chapter)

    chapter_progress = ChapterProgress(
        student_id="student-daily-013",
        chapter_id="chapter-daily-013",
        is_unlocked=True,
    )
    db_session.add(chapter_progress)

    mastery = ConceptMastery(
        student_id="student-daily-013",
        concept_id="concept-daily-013",
        is_unlocked=True,
        mastery_percentage=70,
    )
    db_session.add(mastery)

    # 난이도 7 문제 10개 생성 (mastery 70% → 범위 6~8)
    for i in range(1, 11):
        question = Question(
            id=f"q-exclude-{i}",
            concept_id="concept-daily-013",
            category=QuestionCategory.CONCEPT,
            part=ProblemPart.CALC,
            question_type=QuestionType.MULTIPLE_CHOICE,
            difficulty=7,
            content=f"문제 {i}",
            options=[{"id": "1", "label": "A", "text": "답"}],
            correct_answer="A",
            explanation="설명",
            is_active=True,
        )
        db_session.add(question)

    # 최근 출제된 문제: q-exclude-1, q-exclude-2, q-exclude-3
    test = Test(
        id="test-exclude",
        title="기존 테스트",
        description="테스트",
        grade="middle_1",
        category="concept",
        concept_ids=["concept-daily-013"],
        question_ids=["q-exclude-1", "q-exclude-2", "q-exclude-3"],
        question_count=3,
        is_active=True,
    )
    db_session.add(test)

    service = DailyTestService(db_session)
    yesterday = (datetime.now(KST) - timedelta(days=1)).date().isoformat()

    record = DailyTestRecord(
        student_id="student-daily-013",
        date=yesterday,
        category="concept",
        test_id="test-exclude",
        status="completed",
        total_count=3,
    )
    db_session.add(record)
    await db_session.commit()

    # When: _select_questions 호출
    selected_ids = await service._select_questions(
        "student-daily-013", "concept", "middle_1", count=5
    )

    # Then: 최근 출제 문제는 제외됨
    assert "q-exclude-1" not in selected_ids
    assert "q-exclude-2" not in selected_ids
    assert "q-exclude-3" not in selected_ids


@pytest.mark.asyncio
async def test_get_or_create_daily_test_regenerates_empty_test(db_session):
    """get_or_create_daily_test가 0문제 테스트를 재생성한다."""
    # Given: 0문제 테스트 레코드
    user = User(
        id="student-daily-014",
        login_id="daily_student_014",
        name="테스트 학생 14",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    concept = Concept(
        id="concept-daily-014",
        name="개념 14",
        grade="middle_1",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
    )
    db_session.add(concept)

    chapter = Chapter(
        id="chapter-daily-014",
        name="챕터 14",
        grade="middle_1",
        semester=1,
        chapter_number=1,
        concept_ids=["concept-daily-014"],
    )
    db_session.add(chapter)

    chapter_progress = ChapterProgress(
        student_id="student-daily-014",
        chapter_id="chapter-daily-014",
        is_unlocked=True,
    )
    db_session.add(chapter_progress)

    mastery = ConceptMastery(
        student_id="student-daily-014",
        concept_id="concept-daily-014",
        is_unlocked=True,
        mastery_percentage=50,
    )
    db_session.add(mastery)

    # 문제 추가
    question = Question(
        id="question-daily-014",
        concept_id="concept-daily-014",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=5,
        content="새 문제",
        options=[{"id": "1", "label": "A", "text": "답"}],
        correct_answer="A",
        explanation="설명",
        is_active=True,
    )
    db_session.add(question)

    # 0문제 테스트
    empty_test = Test(
        id="test-empty-014",
        title="빈 테스트",
        description="테스트",
        grade="middle_1",
        category="concept",
        concept_ids=[],
        question_ids=[],
        question_count=0,
        is_active=True,
    )
    db_session.add(empty_test)

    service = DailyTestService(db_session)
    today = service.get_today_str()

    empty_record = DailyTestRecord(
        student_id="student-daily-014",
        date=today,
        category="concept",
        test_id="test-empty-014",
        status="pending",
        total_count=0,
    )
    db_session.add(empty_record)
    await db_session.commit()

    # When: get_or_create_daily_test 재호출
    record = await service.get_or_create_daily_test("student-daily-014", "concept")

    # Then: 새로운 문제가 있는 테스트로 업데이트됨
    await db_session.refresh(record)
    assert record.total_count > 0


@pytest.mark.asyncio
async def test_start_daily_test_returns_none_if_completed(db_session):
    """start_daily_test가 이미 완료된 테스트에 대해 None을 반환한다."""
    # Given: 완료된 일일 테스트
    user = User(
        id="student-daily-015",
        login_id="daily_student_015",
        name="테스트 학생 15",
        role="student",
        grade="middle_1",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    test = Test(
        id="test-daily-015",
        title="완료된 테스트",
        description="테스트",
        grade="middle_1",
        category="concept",
        concept_ids=["concept-015"],
        question_ids=["question-015"],
        question_count=1,
        is_active=True,
    )
    db_session.add(test)

    service = DailyTestService(db_session)
    today = service.get_today_str()

    completed_record = DailyTestRecord(
        student_id="student-daily-015",
        date=today,
        category="concept",
        test_id="test-daily-015",
        status="completed",
        total_count=1,
        score=100,
    )
    db_session.add(completed_record)
    await db_session.commit()

    # When: start_daily_test 호출 (이미 완료됨)
    attempt = await service.start_daily_test("student-daily-015", completed_record.id)

    # Then: None 반환
    assert attempt is None


@pytest.mark.asyncio
async def test_build_category_filter_for_fill_in_blank(db_session):
    """_build_category_filter가 빈칸채우기 필터를 올바르게 적용한다."""
    # Given: 빈칸채우기 및 객관식 문제
    concept = Concept(
        id="concept-fb-001",
        name="빈칸 개념",
        grade="middle_1",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
    )
    db_session.add(concept)

    # 빈칸채우기 문제 (정상)
    fb_question = Question(
        id="q-fb-1",
        concept_id="concept-fb-001",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.FILL_IN_BLANK,
        difficulty=5,
        content="빈칸을 채우세요: 2 + 2 = __",
        correct_answer="4",
        explanation="설명",
        is_active=True,
    )
    db_session.add(fb_question)

    # 객관식 문제 (제외되어야 함)
    mc_question = Question(
        id="q-mc-1",
        concept_id="concept-fb-001",
        category=QuestionCategory.CONCEPT,
        part=ProblemPart.CALC,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=5,
        content="2 + 2 는?",
        options=[{"id": "1", "label": "A", "text": "4"}],
        correct_answer="A",
        explanation="설명",
        is_active=True,
    )
    db_session.add(mc_question)
    await db_session.commit()

    # When: fill_in_blank 필터로 쿼리
    service = DailyTestService(db_session)
    query = select(Question.id).where(Question.is_active == True)
    filtered_query = service._build_category_filter(query, "fill_in_blank")
    result_ids = list((await db_session.scalars(filtered_query)).all())

    # Then: 빈칸채우기 문제만 반환됨
    assert len(result_ids) == 1
    assert "q-fb-1" in result_ids
    assert "q-mc-1" not in result_ids
