"""
DB-level tests for StatsService.

Tests methods that require database interactions including:
- get_student_stats
- get_class_stats
- get_concept_stats
- get_student_quota_progress
"""
import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy import select

from app.models.user import User
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.answer_log import AnswerLog
from app.models.question import Question
from app.models.concept import Concept
from app.models.class_ import Class
from app.services.stats_service import StatsService, _kst_day_utc_range, _to_kst_date


@pytest.fixture
async def stats_service(db_session):
    """Create StatsService with DB session."""
    return StatsService(db=db_session)


@pytest.fixture
async def base_stats_data(db_session):
    """Create basic stats test data."""
    # Class
    cls = Class(id="c1", name="1반", teacher_id="t1")
    db_session.add(cls)

    # Teacher
    teacher = User(
        id="t1", login_id="t1", name="강사1", role="teacher",
        hashed_password="x", is_active=True,
        level=1, total_xp=0, current_streak=0, max_streak=0,
    )
    db_session.add(teacher)

    # Student
    user = User(
        id="s1", login_id="s1", name="학생1", role="student",
        grade="middle_1", class_id="c1",
        hashed_password="x", is_active=True,
        level=3, total_xp=500, current_streak=5, max_streak=10,
    )
    db_session.add(user)

    # Concept
    concept = Concept(
        id="con1", name="방정식", grade="middle_1",
        category="concept", part="algebra"
    )
    db_session.add(concept)

    # Question
    question = Question(
        id="q1", concept_id="con1", category="concept", part="algebra",
        question_type="multiple_choice", difficulty=5,
        content="문제1", correct_answer="A", points=10,
    )
    db_session.add(question)

    # Test
    test = Test(
        id="t1", title="테스트1", grade="middle_1",
        concept_ids=["con1"], question_ids=["q1"],
        question_count=1, time_limit_minutes=10,
    )
    db_session.add(test)

    await db_session.commit()

    return {
        "student_id": "s1",
        "teacher_id": "t1",
        "class_id": "c1",
        "test_id": "t1",
        "question_id": "q1",
        "concept_id": "con1",
    }


class TestGetStudentStats:
    """Tests for get_student_stats method."""

    async def test_get_student_stats_with_completed_attempts(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns stats for student with completed test attempts."""
        # Create completed attempt
        now = datetime.now(timezone.utc)
        attempt = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=80, max_score=100, correct_count=8, total_count=10,
            xp_earned=50, started_at=now - timedelta(minutes=10),
            completed_at=now,
        )
        db_session.add(attempt)

        # Add answer log (use points_earned instead of score)
        log = AnswerLog(
            attempt_id="att1", question_id="q1",
            selected_answer="A", is_correct=True,
            points_earned=10, time_spent_seconds=30,
        )
        db_session.add(log)
        await db_session.commit()

        # Get stats
        result = await stats_service.get_student_stats("s1")

        assert result is not None
        assert result["user_id"] == "s1"
        assert result["total_tests"] == 1
        assert result["total_questions"] == 10
        assert result["correct_answers"] == 8
        assert result["accuracy_rate"] == 80.0
        assert result["level"] == 3
        assert result["total_xp"] == 500
        assert result["current_streak"] == 5
        assert result["max_streak"] == 10
        assert result["average_time_per_question"] == 30.0

    async def test_get_student_stats_no_attempts(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns zeroed stats for student with no test attempts."""
        result = await stats_service.get_student_stats("s1")

        assert result is not None
        assert result["user_id"] == "s1"
        assert result["total_tests"] == 0
        assert result["total_questions"] == 0
        assert result["correct_answers"] == 0
        assert result["accuracy_rate"] == 0.0
        assert result["average_time_per_question"] == 0.0
        assert result["today_solved"] == 0

    async def test_get_student_stats_student_not_found(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns None for non-existent student."""
        result = await stats_service.get_student_stats("nonexistent")
        assert result is None

    async def test_get_student_stats_not_student_role(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns None when user is not a student."""
        result = await stats_service.get_student_stats("t1")  # teacher
        assert result is None

    async def test_get_student_stats_today_solved(
        self, db_session, stats_service, base_stats_data
    ):
        """Counts questions solved today (KST)."""
        # Create attempt with logs today
        today_start, _ = _kst_day_utc_range(_to_kst_date(datetime.now(timezone.utc)) or datetime.now(timezone.utc).date())

        attempt = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=100, max_score=100, correct_count=10, total_count=10,
            xp_earned=50, started_at=today_start + timedelta(hours=1),
            completed_at=today_start + timedelta(hours=2),
        )
        db_session.add(attempt)

        # Add 3 answer logs today
        for i in range(3):
            log = AnswerLog(
                attempt_id="att1", question_id="q1",
                selected_answer="A", is_correct=True,
                points_earned=10, time_spent_seconds=30,
                created_at=today_start + timedelta(hours=1, minutes=i),
            )
            db_session.add(log)
        await db_session.commit()

        result = await stats_service.get_student_stats("s1")
        assert result["today_solved"] == 3

    async def test_get_student_stats_weak_concepts(
        self, db_session, stats_service, base_stats_data
    ):
        """Identifies weak concepts (accuracy < 60%)."""
        # Create completed attempt
        now = datetime.now(timezone.utc)
        attempt = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=50, max_score=100, correct_count=5, total_count=10,
            xp_earned=25, started_at=now - timedelta(minutes=10),
            completed_at=now,
        )
        db_session.add(attempt)

        # Add answer logs (5 correct, 5 incorrect)
        for i in range(10):
            log = AnswerLog(
                attempt_id="att1", question_id="q1",
                selected_answer="A", is_correct=(i < 5),
                points_earned=10 if i < 5 else 0, time_spent_seconds=30,
            )
            db_session.add(log)
        await db_session.commit()

        result = await stats_service.get_student_stats("s1")

        assert len(result["weak_concepts"]) == 1
        weak = result["weak_concepts"][0]
        assert weak["concept_id"] == "con1"
        assert weak["concept_name"] == "방정식"
        assert weak["accuracy_rate"] == 50.0
        assert weak["total_questions"] == 10
        assert weak["correct_count"] == 5

    async def test_get_student_stats_strong_concepts(
        self, db_session, stats_service, base_stats_data
    ):
        """Identifies strong concepts (accuracy >= 80%)."""
        # Create completed attempt
        now = datetime.now(timezone.utc)
        attempt = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=90, max_score=100, correct_count=9, total_count=10,
            xp_earned=45, started_at=now - timedelta(minutes=10),
            completed_at=now,
        )
        db_session.add(attempt)

        # Add answer logs (9 correct, 1 incorrect)
        for i in range(10):
            log = AnswerLog(
                attempt_id="att1", question_id="q1",
                selected_answer="A", is_correct=(i < 9),
                points_earned=10 if i < 9 else 0, time_spent_seconds=30,
            )
            db_session.add(log)
        await db_session.commit()

        result = await stats_service.get_student_stats("s1")

        assert len(result["strong_concepts"]) == 1
        strong = result["strong_concepts"][0]
        assert strong["concept_id"] == "con1"
        assert strong["accuracy_rate"] == 90.0

    async def test_get_student_stats_computation_stats(
        self, db_session, stats_service, base_stats_data
    ):
        """Calculates computation track statistics."""
        # Add computation question
        comp_question = Question(
            id="q2", concept_id="con1", category="computation", part="algebra",
            question_type="short_answer", difficulty=5,
            content="문제2", correct_answer="5", points=10,
        )
        db_session.add(comp_question)

        # Create attempt
        now = datetime.now(timezone.utc)
        attempt = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=80, max_score=100, correct_count=8, total_count=10,
            xp_earned=40, started_at=now - timedelta(minutes=10),
            completed_at=now,
        )
        db_session.add(attempt)

        # Add computation logs
        for i in range(5):
            log = AnswerLog(
                attempt_id="att1", question_id="q2",
                selected_answer="5", is_correct=True,
                points_earned=10, time_spent_seconds=20,
            )
            db_session.add(log)
        await db_session.commit()

        result = await stats_service.get_student_stats("s1")

        comp_stats = result["computation_stats"]
        assert comp_stats is not None
        assert comp_stats["total_questions"] == 5
        assert comp_stats["correct_answers"] == 5
        assert comp_stats["accuracy_rate"] == 100.0
        assert comp_stats["average_time"] == 20.0

    async def test_get_student_stats_type_stats(
        self, db_session, stats_service, base_stats_data
    ):
        """Calculates question type statistics."""
        # Create attempt
        now = datetime.now(timezone.utc)
        attempt = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=80, max_score=100, correct_count=8, total_count=10,
            xp_earned=40, started_at=now - timedelta(minutes=10),
            completed_at=now,
        )
        db_session.add(attempt)

        # Add multiple choice logs
        for i in range(10):
            log = AnswerLog(
                attempt_id="att1", question_id="q1",
                selected_answer="A", is_correct=(i < 8),
                points_earned=10 if i < 8 else 0, time_spent_seconds=25,
            )
            db_session.add(log)
        await db_session.commit()

        result = await stats_service.get_student_stats("s1")

        type_stats = result["type_stats"]
        assert "multiple_choice" in type_stats
        mc_stats = type_stats["multiple_choice"]
        assert mc_stats["total_questions"] == 10
        assert mc_stats["correct_answers"] == 8
        assert mc_stats["accuracy_rate"] == 80.0
        assert mc_stats["average_time"] == 25.0


class TestGetClassStats:
    """Tests for get_class_stats method."""

    async def test_get_class_stats_with_students(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns stats for class with students."""
        # Add another student
        student2 = User(
            id="s2", login_id="s2", name="학생2", role="student",
            grade="middle_1", class_id="c1",
            hashed_password="x", is_active=True,
            level=2, total_xp=200, current_streak=2, max_streak=5,
        )
        db_session.add(student2)

        # Create attempts
        now = datetime.now(timezone.utc)
        att1 = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=80, max_score=100, correct_count=8, total_count=10,
            xp_earned=40, started_at=now - timedelta(minutes=10),
            completed_at=now,
        )
        att2 = TestAttempt(
            id="att2", test_id="t1", student_id="s2",
            score=90, max_score=100, correct_count=9, total_count=10,
            xp_earned=45, started_at=now - timedelta(minutes=10),
            completed_at=now,
        )
        db_session.add_all([att1, att2])
        await db_session.commit()

        result = await stats_service.get_class_stats("c1", "t1")

        assert result is not None
        assert result["class_id"] == "c1"
        assert result["class_name"] == "1반"
        assert result["student_count"] == 2
        assert result["average_accuracy"] == 85.0  # (8+9)/(10+10) = 85%
        assert result["average_level"] == 2.5  # (3+2)/2

    async def test_get_class_stats_empty_class(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns zeroed stats for empty class."""
        # Create empty class
        cls2 = Class(id="c2", name="2반", teacher_id="t1")
        db_session.add(cls2)
        await db_session.commit()

        result = await stats_service.get_class_stats("c2", "t1")

        assert result is not None
        assert result["class_id"] == "c2"
        assert result["student_count"] == 0
        assert result["average_accuracy"] == 0.0
        assert result["average_level"] == 0.0
        assert result["tests_completed_today"] == 0
        assert result["top_students"] == []

    async def test_get_class_stats_class_not_found(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns None for non-existent class."""
        result = await stats_service.get_class_stats("nonexistent", "t1")
        assert result is None

    async def test_get_class_stats_permission_check(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns error for unauthorized teacher."""
        # Add another teacher
        teacher2 = User(
            id="t2", login_id="t2", name="강사2", role="teacher",
            hashed_password="x", is_active=True,
            level=1, total_xp=0, current_streak=0, max_streak=0,
        )
        db_session.add(teacher2)
        await db_session.commit()

        result = await stats_service.get_class_stats("c1", "t2")
        assert result == {"error": "forbidden"}

    async def test_get_class_stats_top_students(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns top 5 students by accuracy."""
        # Add 6 students with different accuracies
        for i in range(2, 8):
            student = User(
                id=f"s{i}", login_id=f"s{i}", name=f"학생{i}", role="student",
                grade="middle_1", class_id="c1",
                hashed_password="x", is_active=True,
                level=i, total_xp=i * 100, current_streak=0, max_streak=0,
            )
            db_session.add(student)

            # Create attempt with decreasing accuracy
            now = datetime.now(timezone.utc)
            correct = 11 - i  # s2=9, s3=8, ..., s7=4
            attempt = TestAttempt(
                id=f"att{i}", test_id="t1", student_id=f"s{i}",
                score=correct * 10, max_score=100, correct_count=correct, total_count=10,
                xp_earned=correct * 5, started_at=now - timedelta(minutes=10),
                completed_at=now,
            )
            db_session.add(attempt)

        await db_session.commit()

        result = await stats_service.get_class_stats("c1", "t1")

        # Should return top 5 by accuracy
        assert len(result["top_students"]) == 5
        # Highest accuracy first
        assert result["top_students"][0]["name"] == "학생2"
        assert result["top_students"][0]["accuracy_rate"] == 90.0
        assert result["top_students"][4]["name"] == "학생6"

    async def test_get_class_stats_today_tests(
        self, db_session, stats_service, base_stats_data
    ):
        """Counts tests completed today (KST)."""
        today_start, _ = _kst_day_utc_range(_to_kst_date(datetime.now(timezone.utc)) or datetime.now(timezone.utc).date())

        # Create 3 attempts today
        for i in range(3):
            attempt = TestAttempt(
                id=f"att{i}", test_id="t1", student_id="s1",
                score=80, max_score=100, correct_count=8, total_count=10,
                xp_earned=40, started_at=today_start + timedelta(hours=i),
                completed_at=today_start + timedelta(hours=i + 1),
            )
            db_session.add(attempt)
        await db_session.commit()

        result = await stats_service.get_class_stats("c1", "t1")
        assert result["tests_completed_today"] == 3

    async def test_get_class_stats_daily_stats(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns 7 days of daily statistics."""
        # Create attempts on different days
        base_date = datetime.now(timezone.utc).date()

        for i in range(7):
            day = base_date - timedelta(days=6 - i)
            day_start, _ = _kst_day_utc_range(day)

            attempt = TestAttempt(
                id=f"att{i}", test_id="t1", student_id="s1",
                score=80, max_score=100, correct_count=8, total_count=10,
                xp_earned=40, started_at=day_start + timedelta(hours=1),
                completed_at=day_start + timedelta(hours=2),
            )
            db_session.add(attempt)
        await db_session.commit()

        result = await stats_service.get_class_stats("c1", "t1")

        daily_stats = result["daily_stats"]
        assert len(daily_stats) == 7
        # Each day should have 1 test completed
        for day_stat in daily_stats:
            assert day_stat["active_students"] == 1
            assert day_stat["tests_completed"] == 1
            assert day_stat["average_accuracy"] == 80.0


class TestGetConceptStats:
    """Tests for get_concept_stats method."""

    async def test_get_concept_stats_basic(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns concept statistics for teacher's students."""
        # Create attempt with logs
        now = datetime.now(timezone.utc)
        attempt = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=80, max_score=100, correct_count=8, total_count=10,
            xp_earned=40, started_at=now - timedelta(minutes=10),
            completed_at=now,
        )
        db_session.add(attempt)

        # Add 10 answer logs
        for i in range(10):
            log = AnswerLog(
                attempt_id="att1", question_id="q1",
                selected_answer="A", is_correct=(i < 8),
                points_earned=10 if i < 8 else 0, time_spent_seconds=30,
            )
            db_session.add(log)
        await db_session.commit()

        result = await stats_service.get_concept_stats("t1")

        assert len(result) == 1
        concept_stat = result[0]
        assert concept_stat["concept_id"] == "con1"
        assert concept_stat["concept_name"] == "방정식"
        assert concept_stat["grade"] == "middle_1"
        assert concept_stat["total_questions"] == 10
        assert concept_stat["correct_count"] == 8
        assert concept_stat["accuracy_rate"] == 80.0
        assert concept_stat["student_count"] == 1
        assert concept_stat["average_time_seconds"] == 30.0

    async def test_get_concept_stats_multiple_concepts(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns stats for multiple concepts."""
        # Add another concept and question
        concept2 = Concept(
            id="con2", name="함수", grade="middle_1",
            category="concept", part="func"  # Use valid enum value
        )
        db_session.add(concept2)

        question2 = Question(
            id="q2", concept_id="con2", category="concept", part="func",
            question_type="multiple_choice", difficulty=5,
            content="문제2", correct_answer="B", points=10,
        )
        db_session.add(question2)

        # Create attempts for both concepts
        now = datetime.now(timezone.utc)
        attempt = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=80, max_score=100, correct_count=8, total_count=10,
            xp_earned=40, started_at=now - timedelta(minutes=10),
            completed_at=now,
        )
        db_session.add(attempt)

        # con1: 5 correct out of 5
        for i in range(5):
            log = AnswerLog(
                attempt_id="att1", question_id="q1",
                selected_answer="A", is_correct=True,
                points_earned=10, time_spent_seconds=20,
            )
            db_session.add(log)

        # con2: 3 correct out of 5
        for i in range(5):
            log = AnswerLog(
                attempt_id="att1", question_id="q2",
                selected_answer="B", is_correct=(i < 3),
                points_earned=10 if i < 3 else 0, time_spent_seconds=40,
            )
            db_session.add(log)

        await db_session.commit()

        result = await stats_service.get_concept_stats("t1")

        # Should be sorted by accuracy (lowest first)
        assert len(result) == 2
        assert result[0]["concept_name"] == "함수"
        assert result[0]["accuracy_rate"] == 60.0
        assert result[1]["concept_name"] == "방정식"
        assert result[1]["accuracy_rate"] == 100.0

    async def test_get_concept_stats_no_questions(
        self, db_session, stats_service, base_stats_data
    ):
        """Skips concepts with no questions."""
        # Add concept without questions
        concept2 = Concept(
            id="con2", name="미적분", grade="middle_1",
            category="concept", part="calc"  # Use valid enum value
        )
        db_session.add(concept2)
        await db_session.commit()

        result = await stats_service.get_concept_stats("t1")

        # Should only include con1 if it has answer logs, otherwise empty
        assert len(result) == 0

    async def test_get_concept_stats_grade_filter(
        self, db_session, stats_service, base_stats_data
    ):
        """Filters concepts by grade."""
        # Add middle_2 concept
        concept2 = Concept(
            id="con2", name="이차방정식", grade="middle_2",
            category="concept", part="algebra"
        )
        db_session.add(concept2)

        question2 = Question(
            id="q2", concept_id="con2", category="concept", part="algebra",
            question_type="multiple_choice", difficulty=5,
            content="문제2", correct_answer="B", points=10,
        )
        db_session.add(question2)
        await db_session.commit()

        # Should only return middle_1 concept
        result = await stats_service.get_concept_stats("t1", grade="middle_1")

        # No answer logs yet, so empty
        assert len(result) == 0

    async def test_get_concept_stats_empty_no_students(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns empty for teacher with no students."""
        # Create teacher with no students
        teacher2 = User(
            id="t2", login_id="t2", name="강사2", role="teacher",
            hashed_password="x", is_active=True,
            level=1, total_xp=0, current_streak=0, max_streak=0,
        )
        db_session.add(teacher2)

        cls2 = Class(id="c2", name="2반", teacher_id="t2")
        db_session.add(cls2)
        await db_session.commit()

        result = await stats_service.get_concept_stats("t2")
        assert result == []


class TestGetStudentQuotaProgress:
    """Tests for get_student_quota_progress method."""

    async def test_get_student_quota_progress_basic(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns quota progress for student."""
        # Update class with daily quota
        cls = await db_session.get(Class, "c1")
        cls.daily_quota = 20
        cls.quota_carry_over = False
        await db_session.commit()

        result = await stats_service.get_student_quota_progress("s1")

        assert result is not None
        assert result["daily_quota"] == 20
        assert result["correct_today"] == 0
        assert result["quota_remaining"] == 20
        assert result["accumulated_quota"] == 20
        assert result["quota_met"] is False
        assert result["carry_over"] is False

    async def test_get_student_quota_progress_with_correct_today(
        self, db_session, stats_service, base_stats_data
    ):
        """Calculates correct answers today."""
        # Update class
        cls = await db_session.get(Class, "c1")
        cls.daily_quota = 10
        await db_session.commit()

        # Add correct answers today
        today_start, _ = _kst_day_utc_range(_to_kst_date(datetime.now(timezone.utc)) or datetime.now(timezone.utc).date())

        attempt = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=70, max_score=100, correct_count=7, total_count=10,
            xp_earned=35, started_at=today_start + timedelta(hours=1),
            completed_at=today_start + timedelta(hours=2),
        )
        db_session.add(attempt)

        # 7 correct answers
        for i in range(7):
            log = AnswerLog(
                attempt_id="att1", question_id="q1",
                selected_answer="A", is_correct=True,
                points_earned=10, time_spent_seconds=30,
                created_at=today_start + timedelta(hours=1, minutes=i),
            )
            db_session.add(log)
        await db_session.commit()

        result = await stats_service.get_student_quota_progress("s1")

        assert result["correct_today"] == 7
        assert result["quota_remaining"] == 3
        assert result["quota_met"] is False

    async def test_get_student_quota_progress_quota_met(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns quota_met=True when quota reached."""
        # Update class
        cls = await db_session.get(Class, "c1")
        cls.daily_quota = 5
        await db_session.commit()

        # Add 5 correct answers today
        today_start, _ = _kst_day_utc_range(_to_kst_date(datetime.now(timezone.utc)) or datetime.now(timezone.utc).date())

        attempt = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=50, max_score=100, correct_count=5, total_count=10,
            xp_earned=25, started_at=today_start + timedelta(hours=1),
            completed_at=today_start + timedelta(hours=2),
        )
        db_session.add(attempt)

        for i in range(5):
            log = AnswerLog(
                attempt_id="att1", question_id="q1",
                selected_answer="A", is_correct=True,
                points_earned=10, time_spent_seconds=30,
                created_at=today_start + timedelta(hours=1, minutes=i),
            )
            db_session.add(log)
        await db_session.commit()

        result = await stats_service.get_student_quota_progress("s1")

        assert result["correct_today"] == 5
        assert result["quota_met"] is True
        assert result["quota_remaining"] == 0

    async def test_get_student_quota_progress_student_not_found(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns None for non-existent student."""
        result = await stats_service.get_student_quota_progress("nonexistent")
        assert result is None

    async def test_get_student_quota_progress_no_class(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns None for student without class."""
        # Create student without class
        student = User(
            id="s_noclass", login_id="s_noclass", name="무소속", role="student",
            grade="middle_1", class_id=None,
            hashed_password="x", is_active=True,
            level=1, total_xp=0, current_streak=0, max_streak=0,
        )
        db_session.add(student)
        await db_session.commit()

        result = await stats_service.get_student_quota_progress("s_noclass")
        assert result is None


class TestCheckAndUpdateQuotaMet:
    """Tests for check_and_update_quota_met method."""

    async def test_check_and_update_quota_met_first_time(
        self, db_session, stats_service, base_stats_data
    ):
        """Updates last_quota_met_date when quota met for first time."""
        # Update class
        cls = await db_session.get(Class, "c1")
        cls.daily_quota = 5
        await db_session.commit()

        # Add 5 correct answers today
        today_start, _ = _kst_day_utc_range(_to_kst_date(datetime.now(timezone.utc)) or datetime.now(timezone.utc).date())

        attempt = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=50, max_score=100, correct_count=5, total_count=10,
            xp_earned=25, started_at=today_start + timedelta(hours=1),
            completed_at=today_start + timedelta(hours=2),
        )
        db_session.add(attempt)

        for i in range(5):
            log = AnswerLog(
                attempt_id="att1", question_id="q1",
                selected_answer="A", is_correct=True,
                points_earned=10, time_spent_seconds=30,
                created_at=today_start + timedelta(hours=1, minutes=i),
            )
            db_session.add(log)
        await db_session.commit()

        result = await stats_service.check_and_update_quota_met("s1")

        assert result is True  # New achievement

        # Check user updated
        user = await db_session.get(User, "s1")
        assert user.last_quota_met_date is not None

    async def test_check_and_update_quota_met_already_today(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns False if already met quota today."""
        # Set last_quota_met_date to today
        user = await db_session.get(User, "s1")
        today = _to_kst_date(datetime.now(timezone.utc)) or datetime.now(timezone.utc).date()
        user.last_quota_met_date = datetime(today.year, today.month, today.day) - timedelta(hours=9)

        cls = await db_session.get(Class, "c1")
        cls.daily_quota = 5
        await db_session.commit()

        # Add correct answers
        today_start, _ = _kst_day_utc_range(today)

        attempt = TestAttempt(
            id="att1", test_id="t1", student_id="s1",
            score=50, max_score=100, correct_count=5, total_count=10,
            xp_earned=25, started_at=today_start + timedelta(hours=1),
            completed_at=today_start + timedelta(hours=2),
        )
        db_session.add(attempt)

        for i in range(5):
            log = AnswerLog(
                attempt_id="att1", question_id="q1",
                selected_answer="A", is_correct=True,
                points_earned=10, time_spent_seconds=30,
                created_at=today_start + timedelta(hours=1, minutes=i),
            )
            db_session.add(log)
        await db_session.commit()

        result = await stats_service.check_and_update_quota_met("s1")

        assert result is False  # Already met today

    async def test_check_and_update_quota_met_not_met(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns False when quota not met."""
        cls = await db_session.get(Class, "c1")
        cls.daily_quota = 10
        await db_session.commit()

        result = await stats_service.check_and_update_quota_met("s1")

        assert result is False


class TestGetClassQuotaProgress:
    """Tests for get_class_quota_progress method."""

    async def test_get_class_quota_progress_with_students(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns quota progress for all students in class."""
        # Add another student
        student2 = User(
            id="s2", login_id="s2", name="학생2", role="student",
            grade="middle_1", class_id="c1",
            hashed_password="x", is_active=True,
            level=2, total_xp=200, current_streak=0, max_streak=0,
        )
        db_session.add(student2)

        cls = await db_session.get(Class, "c1")
        cls.daily_quota = 10
        await db_session.commit()

        result = await stats_service.get_class_quota_progress("c1")

        assert len(result) == 2
        assert result[0]["student_id"] in ["s1", "s2"]
        assert result[0]["daily_quota"] == 10
        assert result[1]["student_id"] in ["s1", "s2"]

    async def test_get_class_quota_progress_class_not_found(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns empty list for non-existent class."""
        result = await stats_service.get_class_quota_progress("nonexistent")
        assert result == []

    async def test_get_class_quota_progress_empty_class(
        self, db_session, stats_service, base_stats_data
    ):
        """Returns empty list for class with no students."""
        cls2 = Class(id="c2", name="2반", teacher_id="t1")
        db_session.add(cls2)
        await db_session.commit()

        result = await stats_service.get_class_quota_progress("c2")
        assert result == []
