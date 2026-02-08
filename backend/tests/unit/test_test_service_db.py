"""TestService database integration tests - focusing on uncovered lines."""

import pytest
from datetime import datetime, timezone
from sqlalchemy import select

from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.answer_log import AnswerLog
from app.models.question import Question
from app.models.chapter import Chapter
from app.models.chapter_progress import ChapterProgress
from app.models.concept import Concept
from app.models.concept_mastery import ConceptMastery
from app.models.user import User
from app.models.daily_test_record import DailyTestRecord
from app.services.test_service import TestService


class TestGetStudentAvailableConceptIds:
    """Tests for _get_student_available_concept_ids method."""

    @pytest.mark.asyncio
    async def test_fallback_no_unlocked_chapters_creates_first_concept(self, db_session):
        """When no unlocked chapters exist, unlock first concept of first chapter."""
        # Create student
        user = User(
            id="s1", login_id="s1", name="학생", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concept
        concept = Concept(
            id="c1", name="개념1", grade="middle_1", category="concept", part="algebra"
        )
        db_session.add(concept)

        # Create chapter with concept_ids
        chapter = Chapter(
            id="ch1", name="1. 단원", grade="middle_1", semester=1,
            chapter_number=1, concept_ids=["c1"]
        )
        db_session.add(chapter)
        await db_session.commit()

        service = TestService(db_session)
        result = await service._get_student_available_concept_ids("s1", "middle_1")

        # Should return the first concept
        assert result == ["c1"]

        # Verify ConceptMastery was created and unlocked
        stmt = select(ConceptMastery).where(
            ConceptMastery.student_id == "s1",
            ConceptMastery.concept_id == "c1"
        )
        mastery = await db_session.scalar(stmt)
        assert mastery is not None
        assert mastery.is_unlocked is True

    @pytest.mark.asyncio
    async def test_fallback_no_chapters_returns_all_concepts(self, db_session):
        """When no chapters exist for grade, return all concepts for that grade."""
        # Create student
        user = User(
            id="s2", login_id="s2", name="학생2", role="student", grade="middle_2",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concepts with no chapters
        c1 = Concept(id="c1", name="개념1", grade="middle_2", category="concept", part="algebra")
        c2 = Concept(id="c2", name="개념2", grade="middle_2", category="concept", part="geometry")
        db_session.add_all([c1, c2])
        await db_session.commit()

        service = TestService(db_session)
        result = await service._get_student_available_concept_ids("s2", "middle_2")

        # Should return all concepts for the grade
        assert set(result) == {"c1", "c2"}

    @pytest.mark.asyncio
    async def test_normal_path_returns_unlocked_concepts_only(self, db_session):
        """With unlocked chapters and ConceptMastery records, returns only unlocked concepts."""
        # Create student
        user = User(
            id="s3", login_id="s3", name="학생3", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concepts
        c1 = Concept(id="c1", name="개념1", grade="middle_1", category="concept", part="algebra")
        c2 = Concept(id="c2", name="개념2", grade="middle_1", category="concept", part="algebra")
        c3 = Concept(id="c3", name="개념3", grade="middle_1", category="concept", part="algebra")
        db_session.add_all([c1, c2, c3])

        # Create chapter with all three concepts
        chapter = Chapter(
            id="ch1", name="1. 단원", grade="middle_1", semester=1,
            chapter_number=1, concept_ids=["c1", "c2", "c3"]
        )
        db_session.add(chapter)

        # Unlock chapter
        progress = ChapterProgress(student_id="s3", chapter_id="ch1", is_unlocked=True)
        db_session.add(progress)

        # Only unlock c1 and c2
        m1 = ConceptMastery(student_id="s3", concept_id="c1", is_unlocked=True)
        m2 = ConceptMastery(student_id="s3", concept_id="c2", is_unlocked=True)
        m3 = ConceptMastery(student_id="s3", concept_id="c3", is_unlocked=False)
        db_session.add_all([m1, m2, m3])
        await db_session.commit()

        service = TestService(db_session)
        result = await service._get_student_available_concept_ids("s3", "middle_1")

        # Should only return unlocked concepts
        assert set(result) == {"c1", "c2"}

    @pytest.mark.asyncio
    async def test_unlocked_chapters_but_no_concept_mastery(self, db_session):
        """When chapters are unlocked but no ConceptMastery exists, returns empty list."""
        # Create student
        user = User(
            id="s4", login_id="s4", name="학생4", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concept
        c1 = Concept(id="c1", name="개념1", grade="middle_1", category="concept", part="algebra")
        db_session.add(c1)

        # Create chapter
        chapter = Chapter(
            id="ch1", name="1. 단원", grade="middle_1", semester=1,
            chapter_number=1, concept_ids=["c1"]
        )
        db_session.add(chapter)

        # Unlock chapter but no ConceptMastery
        progress = ChapterProgress(student_id="s4", chapter_id="ch1", is_unlocked=True)
        db_session.add(progress)
        await db_session.commit()

        service = TestService(db_session)
        result = await service._get_student_available_concept_ids("s4", "middle_1")

        # Should return empty list
        assert result == []


class TestGenerateComprehensiveTest:
    """Tests for generate_comprehensive_test method."""

    @pytest.mark.asyncio
    async def test_returns_none_when_no_available_concepts(self, db_session):
        """Returns None when student has no unlocked concepts."""
        # Create student with no unlocked concepts
        user = User(
            id="s1", login_id="s1", name="학생", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)
        await db_session.commit()

        service = TestService(db_session)
        result = await service.generate_comprehensive_test("s1", "middle_1", "cumulative")

        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_when_less_than_10_questions(self, db_session):
        """Returns None when less than 10 questions exist."""
        # Create student
        user = User(
            id="s2", login_id="s2", name="학생2", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concept
        c1 = Concept(id="c1", name="개념1", grade="middle_1", category="concept", part="algebra")
        db_session.add(c1)

        # Unlock concept
        m1 = ConceptMastery(student_id="s2", concept_id="c1", is_unlocked=True)
        db_session.add(m1)

        # Create only 5 questions
        for i in range(5):
            q = Question(
                id=f"q{i}", concept_id="c1", category="concept", part="algebra",
                question_type="multiple_choice", difficulty=5,
                content=f"문제 {i}", correct_answer="A", points=10
            )
            db_session.add(q)
        await db_session.commit()

        service = TestService(db_session)
        result = await service.generate_comprehensive_test("s2", "middle_1", "cumulative")

        assert result is None

    @pytest.mark.asyncio
    async def test_successfully_generates_test_with_difficulty_distribution(self, db_session):
        """Successfully generates test with 10+ questions and difficulty distribution."""
        # Create student
        user = User(
            id="s3", login_id="s3", name="학생3", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concept
        c1 = Concept(id="c1", name="개념1", grade="middle_1", category="concept", part="algebra")
        db_session.add(c1)

        # Unlock concept
        m1 = ConceptMastery(student_id="s3", concept_id="c1", is_unlocked=True)
        db_session.add(m1)

        # Create 15 questions with various difficulties
        # 5 easy (difficulty <= 4)
        for i in range(5):
            q = Question(
                id=f"q_easy_{i}", concept_id="c1", category="concept", part="algebra",
                question_type="multiple_choice", difficulty=3,
                content=f"쉬운 문제 {i}", correct_answer="A", points=10
            )
            db_session.add(q)
        # 5 medium (5 <= difficulty <= 7)
        for i in range(5):
            q = Question(
                id=f"q_med_{i}", concept_id="c1", category="concept", part="algebra",
                question_type="multiple_choice", difficulty=6,
                content=f"중간 문제 {i}", correct_answer="A", points=10
            )
            db_session.add(q)
        # 5 hard (difficulty >= 8)
        for i in range(5):
            q = Question(
                id=f"q_hard_{i}", concept_id="c1", category="concept", part="algebra",
                question_type="multiple_choice", difficulty=9,
                content=f"어려운 문제 {i}", correct_answer="A", points=10
            )
            db_session.add(q)
        await db_session.commit()

        service = TestService(db_session)
        result = await service.generate_comprehensive_test("s3", "middle_1", "cumulative")

        assert result is not None
        assert result["title"] == "중1 누적 종합 평가"
        assert result["question_count"] == 15  # min(20, 15)
        assert len(result["question_ids"]) == 15
        assert result["test_type"] == "cumulative"
        assert result["grade"] == "middle_1"
        assert "c1" in result["concept_ids"]

    @pytest.mark.asyncio
    async def test_semester_final_filters_by_semester(self, db_session):
        """semester_final test type filters concepts by semester."""
        # Create student
        user = User(
            id="s4", login_id="s4", name="학생4", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concepts for different semesters
        c1 = Concept(id="c1_s1", name="개념1학기1", grade="middle_1", category="concept", part="algebra")
        c2 = Concept(id="c2_s2", name="개념2학기1", grade="middle_1", category="concept", part="geometry")
        db_session.add_all([c1, c2])

        # Create chapters
        ch1 = Chapter(
            id="ch1", name="1. 단원", grade="middle_1", semester=1,
            chapter_number=1, concept_ids=["c1_s1"]
        )
        ch2 = Chapter(
            id="ch2", name="2. 단원", grade="middle_1", semester=2,
            chapter_number=2, concept_ids=["c2_s2"]
        )
        db_session.add_all([ch1, ch2])

        # Unlock both concepts
        m1 = ConceptMastery(student_id="s4", concept_id="c1_s1", is_unlocked=True)
        m2 = ConceptMastery(student_id="s4", concept_id="c2_s2", is_unlocked=True)
        db_session.add_all([m1, m2])

        # Create questions for both concepts
        for i in range(10):
            q = Question(
                id=f"q_s1_{i}", concept_id="c1_s1", category="concept", part="algebra",
                question_type="multiple_choice", difficulty=5,
                content=f"1학기 문제 {i}", correct_answer="A", points=10
            )
            db_session.add(q)
        for i in range(10):
            q = Question(
                id=f"q_s2_{i}", concept_id="c2_s2", category="concept", part="geometry",
                question_type="multiple_choice", difficulty=5,
                content=f"2학기 문제 {i}", correct_answer="A", points=10
            )
            db_session.add(q)
        await db_session.commit()

        service = TestService(db_session)
        result = await service.generate_comprehensive_test(
            "s4", "middle_1", "semester_final", semester=1
        )

        assert result is not None
        assert result["title"] == "중1 1학기 기말고사"
        assert result["test_type"] == "semester_final"
        assert result["semester"] == 1
        # Should only contain semester 1 concepts
        assert "c1_s1" in result["concept_ids"]
        assert "c2_s2" not in result["concept_ids"]

    @pytest.mark.asyncio
    async def test_different_test_types_produce_different_titles(self, db_session):
        """Different test types produce different titles."""
        # Create student
        user = User(
            id="s5", login_id="s5", name="학생5", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concept
        c1 = Concept(id="c1", name="개념1", grade="middle_1", category="concept", part="algebra")
        db_session.add(c1)

        # Unlock concept
        m1 = ConceptMastery(student_id="s5", concept_id="c1", is_unlocked=True)
        db_session.add(m1)

        # Create 15 questions
        for i in range(15):
            q = Question(
                id=f"q{i}", concept_id="c1", category="concept", part="algebra",
                question_type="multiple_choice", difficulty=5,
                content=f"문제 {i}", correct_answer="A", points=10
            )
            db_session.add(q)
        await db_session.commit()

        service = TestService(db_session)

        # Test cumulative
        cumulative = await service.generate_comprehensive_test("s5", "middle_1", "cumulative")
        assert cumulative["title"] == "중1 누적 종합 평가"

        # Test grade_final
        grade_final = await service.generate_comprehensive_test("s5", "middle_1", "grade_final")
        assert grade_final["title"] == "중1 학년 종합 평가"


class TestStartTestBlankHandling:
    """Tests for start_test method blank question handling."""

    @pytest.mark.asyncio
    async def test_start_with_answer_marker_in_content(self, db_session):
        """Fill-in-blank with [answer] marker gets processed correctly."""
        # Create student
        user = User(
            id="s1", login_id="s1", name="학생", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concept
        c1 = Concept(id="c1", name="개념1", grade="middle_1", category="concept", part="algebra")
        db_session.add(c1)

        # Fill-in-blank question with [answer] marker
        q_blank = Question(
            id="qb1", concept_id="c1", category="concept", part="algebra",
            question_type="fill_in_blank", difficulty=5,
            content="x + 3 = 7에서 x = [answer]", correct_answer="4",
            points=10
        )
        db_session.add(q_blank)

        # Create test
        test = Test(
            id="test1", title="테스트1", grade="middle_1",
            concept_ids=["c1"], question_ids=["qb1"],
            question_count=1, time_limit_minutes=10, is_active=True
        )
        db_session.add(test)
        await db_session.commit()

        service = TestService(db_session)
        attempt = await service.start_test("test1", "s1")

        assert attempt is not None
        assert "qb1" in attempt.question_shuffle_config
        blank_config = attempt.question_shuffle_config["qb1"]["blank_config"]
        assert blank_config["display_content"] == "x + 3 = 7에서 x = ___"
        assert "blank_0" in blank_config["blank_answers"]
        assert blank_config["blank_answers"]["blank_0"]["answer"] == "4"

    @pytest.mark.asyncio
    async def test_start_with_accept_formats(self, db_session):
        """Fill-in-blank with accept_formats gets processed correctly."""
        # Create student
        user = User(
            id="s2", login_id="s2", name="학생2", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concept
        c1 = Concept(id="c1", name="개념1", grade="middle_1", category="concept", part="algebra")
        db_session.add(c1)

        # Fill-in-blank question with accept_formats
        q_fb = Question(
            id="qb2", concept_id="c1", category="concept", part="algebra",
            question_type="fill_in_blank", difficulty=5,
            content="3 + 5의 값은?", correct_answer="8",
            points=10,
            blank_config={"accept_formats": ["integer"]}
        )
        db_session.add(q_fb)

        # Create test
        test = Test(
            id="test2", title="테스트2", grade="middle_1",
            concept_ids=["c1"], question_ids=["qb2"],
            question_count=1, time_limit_minutes=10, is_active=True
        )
        db_session.add(test)
        await db_session.commit()

        service = TestService(db_session)
        attempt = await service.start_test("test2", "s2")

        assert attempt is not None
        assert "qb2" in attempt.question_shuffle_config
        blank_config = attempt.question_shuffle_config["qb2"]["blank_config"]
        assert blank_config["display_content"] == "3 + 5의 값은 ___"
        assert "blank_0" in blank_config["blank_answers"]
        assert blank_config["blank_answers"]["blank_0"]["answer"] == "8"

    @pytest.mark.asyncio
    async def test_start_with_blank_positions(self, db_session):
        """Fill-in-blank with blank_positions delegates to BlankService."""
        # Create student
        user = User(
            id="s3", login_id="s3", name="학생3", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concept
        c1 = Concept(id="c1", name="개념1", grade="middle_1", category="concept", part="algebra")
        db_session.add(c1)

        # Fill-in-blank question with blank_positions
        q_bp = Question(
            id="qb3", concept_id="c1", category="concept", part="algebra",
            question_type="fill_in_blank", difficulty=5,
            content="세 변의 길이가 같은 삼각형은 정삼각형이다", correct_answer="답",
            points=10,
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "세", "importance": 5},
                    {"index": 1, "word": "변의", "importance": 3},
                ],
                "round_rules": [
                    {"round": 1, "blank_count": 1, "min_importance": 3}
                ]
            }
        )
        db_session.add(q_bp)

        # Create test
        test = Test(
            id="test3", title="테스트3", grade="middle_1",
            concept_ids=["c1"], question_ids=["qb3"],
            question_count=1, time_limit_minutes=10, is_active=True
        )
        db_session.add(test)
        await db_session.commit()

        service = TestService(db_session)
        attempt = await service.start_test("test3", "s3")

        assert attempt is not None
        assert "qb3" in attempt.question_shuffle_config
        blank_config = attempt.question_shuffle_config["qb3"]["blank_config"]
        # BlankService should have processed this
        assert "display_content" in blank_config
        assert "blank_answers" in blank_config


class TestAbandonAttemptWithDailyTestRecord:
    """Tests for abandon_attempt method with DailyTestRecord."""

    @pytest.mark.asyncio
    async def test_abandon_resets_daily_test_record(self, db_session):
        """Abandoning attempt also resets the DailyTestRecord."""
        # Create student
        user = User(
            id="s1", login_id="s1", name="학생", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create test
        test = Test(
            id="daily-test1", title="일일테스트", grade="middle_1",
            concept_ids=[], question_ids=[],
            question_count=0, time_limit_minutes=10, is_active=True
        )
        db_session.add(test)

        # Create attempt
        attempt = TestAttempt(
            id="attempt1",
            test_id="daily-test1",
            student_id="s1",
            max_score=100,
            total_count=10
        )
        db_session.add(attempt)

        # Create DailyTestRecord pointing to the attempt
        daily_record = DailyTestRecord(
            id="dr1",
            student_id="s1",
            date="2026-02-07",
            category="concept",
            test_id="daily-test1",
            attempt_id="attempt1",
            status="in_progress"
        )
        db_session.add(daily_record)
        await db_session.commit()

        service = TestService(db_session)
        result = await service.abandon_attempt("attempt1", "s1")

        assert result is True

        # Verify DailyTestRecord was reset
        await db_session.refresh(daily_record)
        assert daily_record.attempt_id is None
        assert daily_record.status == "pending"

    @pytest.mark.asyncio
    async def test_abandon_without_daily_record_succeeds(self, db_session):
        """Abandoning attempt without DailyTestRecord succeeds."""
        # Create student
        user = User(
            id="s2", login_id="s2", name="학생2", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create test
        test = Test(
            id="test2", title="테스트", grade="middle_1",
            concept_ids=[], question_ids=[],
            question_count=0, time_limit_minutes=10, is_active=True
        )
        db_session.add(test)

        # Create attempt (no DailyTestRecord)
        attempt = TestAttempt(
            id="attempt2",
            test_id="test2",
            student_id="s2",
            max_score=100,
            total_count=10
        )
        db_session.add(attempt)
        await db_session.commit()

        service = TestService(db_session)
        result = await service.abandon_attempt("attempt2", "s2")

        assert result is True

        # Verify attempt was deleted
        deleted_attempt = await db_session.get(TestAttempt, "attempt2")
        assert deleted_attempt is None


class TestGetAvailableTestsFiltering:
    """Tests for get_available_tests method filtering logic."""

    @pytest.mark.asyncio
    async def test_basic_filtering_with_concepts(self, db_session):
        """Basic test for get_available_tests with concept-based filtering."""
        # Create student
        user = User(
            id="s1", login_id="s1", name="학생", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concepts
        c1 = Concept(id="c1", name="개념1", grade="middle_1", category="concept", part="algebra")
        c2 = Concept(id="c2", name="개념2", grade="middle_1", category="concept", part="algebra")
        db_session.add_all([c1, c2])

        # Create chapter
        chapter = Chapter(
            id="ch1", name="1. 단원", grade="middle_1", semester=1,
            chapter_number=1, concept_ids=["c1", "c2"]
        )
        db_session.add(chapter)

        # Unlock chapter and concepts
        progress = ChapterProgress(student_id="s1", chapter_id="ch1", is_unlocked=True)
        db_session.add(progress)
        m1 = ConceptMastery(student_id="s1", concept_id="c1", is_unlocked=True)
        db_session.add(m1)

        # Create test requiring c1 only
        test = Test(
            id="test1", title="테스트1", grade="middle_1",
            concept_ids=["c1"], question_ids=[],
            question_count=0, time_limit_minutes=10, is_active=True
        )
        db_session.add(test)
        await db_session.commit()

        service = TestService(db_session)
        results, total = await service.get_available_tests("s1", "middle_1")

        # Should include test1 since c1 is unlocked
        assert total >= 1
        test_ids = [r["test"].id if hasattr(r["test"], "id") else r["test"]["id"] for r in results]
        assert "test1" in test_ids

    @pytest.mark.asyncio
    async def test_filters_out_daily_tests(self, db_session):
        """Daily tests should be filtered out from available tests when grade is provided."""
        # Create student
        user = User(
            id="s2", login_id="s2", name="학생2", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create concept and unlock it to ensure we're testing with grade filter
        c1 = Concept(id="c1", name="개념1", grade="middle_1", category="concept", part="algebra")
        db_session.add(c1)
        m1 = ConceptMastery(student_id="s2", concept_id="c1", is_unlocked=True)
        db_session.add(m1)

        # Create daily test
        daily_test = Test(
            id="daily-test1", title="일일테스트", grade="middle_1",
            concept_ids=[], question_ids=[],
            question_count=0, time_limit_minutes=10, is_active=True
        )
        db_session.add(daily_test)
        await db_session.commit()

        service = TestService(db_session)
        # Must provide grade for filtering to happen
        results, total = await service.get_available_tests("s2", "middle_1")

        # Daily test should not appear
        test_ids = [r["test"].id if hasattr(r["test"], "id") else r["test"]["id"] for r in results]
        assert "daily-test1" not in test_ids

    @pytest.mark.asyncio
    async def test_includes_placement_tests_always(self, db_session):
        """Placement tests should always be shown regardless of concepts."""
        # Create student
        user = User(
            id="s3", login_id="s3", name="학생3", role="student", grade="middle_1",
            hashed_password="x", is_active=True, level=1, total_xp=0,
            current_streak=0, max_streak=0
        )
        db_session.add(user)

        # Create placement test
        placement_test = Test(
            id="placement1", title="진단평가", grade="middle_1",
            concept_ids=["c999"],  # Concept student doesn't have
            question_ids=[],
            question_count=0, time_limit_minutes=10, is_active=True,
            is_placement=True
        )
        db_session.add(placement_test)
        await db_session.commit()

        service = TestService(db_session)
        results, total = await service.get_available_tests("s3", "middle_1")

        # Placement test should appear
        test_ids = [r["test"].id if hasattr(r["test"], "id") else r["test"]["id"] for r in results]
        assert "placement1" in test_ids
