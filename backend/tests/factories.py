"""Factory Boy 팩토리 정의."""

import factory
from factory import Faker

from app.schemas.common import Difficulty, Grade, QuestionType, UserRole


class UserFactory(factory.Factory):
    """사용자 팩토리."""

    class Meta:
        model = dict

    id = factory.LazyFunction(lambda: str(factory.Faker._get_faker().uuid4()))
    email = Faker("email")
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
    difficulty = Difficulty.MEDIUM
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
