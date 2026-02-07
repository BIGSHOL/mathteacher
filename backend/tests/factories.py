"""Factory Boy 팩토리 정의."""

import factory
from factory import Faker, Sequence

from app.schemas.common import Difficulty, Grade, QuestionType, UserRole


class UserFactory(factory.Factory):
    """사용자 팩토리."""

    class Meta:
        model = dict

    id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    login_id = Sequence(lambda n: f"testuser{n:03d}")
    name = Faker("name")
    role = UserRole.STUDENT
    grade = Grade.MIDDLE_1
    class_id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    level = 1
    total_xp = 0
    current_streak = 0
    hashed_password = "hashed_password_123"


class TeacherFactory(UserFactory):
    """강사 팩토리."""

    role = UserRole.TEACHER
    grade = None
    class_id = None


class ClassFactory(factory.Factory):
    """반 팩토리."""

    class Meta:
        model = dict

    id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    name = Faker("word")
    teacher_id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    grade = Grade.MIDDLE_1


class ConceptFactory(factory.Factory):
    """개념 팩토리."""

    class Meta:
        model = dict

    id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    name = Faker("sentence", nb_words=3)
    grade = Grade.MIDDLE_1
    description = Faker("paragraph")
    parent_id = None


class QuestionFactory(factory.Factory):
    """문제 팩토리."""

    class Meta:
        model = dict

    id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    concept_id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    question_type = QuestionType.MULTIPLE_CHOICE
    difficulty = 5
    content = Faker("paragraph")
    options = factory.LazyFunction(
        lambda: [
            {"id": "1", "label": "A", "text": "Option A"},
            {"id": "2", "label": "B", "text": "Option B"},
            {"id": "3", "label": "C", "text": "Option C"},
            {"id": "4", "label": "D", "text": "Option D"},
        ]
    )
    correct_answer = "A"
    explanation = Faker("paragraph")
    points = 10


class TestFactory(factory.Factory):
    """테스트 팩토리."""

    class Meta:
        model = dict

    id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    title = Faker("sentence", nb_words=4)
    description = Faker("paragraph")
    grade = Grade.MIDDLE_1
    concept_ids = factory.LazyFunction(
        lambda: [str(factory.Faker._get_faker().uuid4())]
    )
    question_count = 10
    time_limit_minutes = 30
    is_active = True


class TestAttemptFactory(factory.Factory):
    """테스트 시도 팩토리."""

    class Meta:
        model = dict

    id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    test_id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    student_id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    score = 0
    max_score = 100
    correct_count = 0
    total_count = 10
    xp_earned = 0
    combo_max = 0


class ChapterFactory(factory.Factory):
    """단원 팩토리."""

    class Meta:
        model = dict

    id = Sequence(lambda n: f"chapter-{n:03d}")
    name = Faker("sentence", nb_words=3)
    grade = Grade.MIDDLE_1
    semester = 1
    chapter_number = Sequence(lambda n: n)
    concept_ids = factory.LazyFunction(lambda: [])
    is_active = True
    prerequisite_chapter_ids = factory.LazyFunction(lambda: [])
    description = Faker("paragraph")
    mastery_threshold = 80
    final_test_pass_score = 70
    require_teacher_approval = False


class ChapterProgressFactory(factory.Factory):
    """단원 진행 상황 팩토리."""

    class Meta:
        model = dict

    id = Sequence(lambda n: f"chapter-progress-{n:03d}")
    student_id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    chapter_id = Sequence(lambda n: f"chapter-{n:03d}")
    is_unlocked = False
    is_completed = False
    overall_progress = 0.0
    teacher_approved = False
    final_test_attempted = False
    final_test_passed = False


class ConceptMasteryFactory(factory.Factory):
    """개념 숙련도 팩토리."""

    class Meta:
        model = dict

    id = Sequence(lambda n: f"mastery-{n:03d}")
    student_id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    concept_id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    is_unlocked = False
    is_mastered = False
    mastery_percentage = 0.0
    total_attempts = 0
    correct_count = 0
    average_score = 0.0


class AnswerLogFactory(factory.Factory):
    """답안 기록 팩토리."""

    class Meta:
        model = dict

    id = Sequence(lambda n: f"answer-log-{n:03d}")
    attempt_id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    question_id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    selected_answer = "A"
    is_correct = True
    time_spent_seconds = 10
    combo_count = 0
    points_earned = 0
    question_difficulty = 5
    question_category = "concept"
