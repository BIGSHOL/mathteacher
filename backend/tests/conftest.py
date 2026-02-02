"""테스트 설정 및 픽스처."""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# 테스트 환경 설정 (import 전에 설정)
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-testing-only"

from app.main import app
from app.core.database import Base, get_db
from app.models import User, Class, Concept, Question, Test, TestAttempt, AnswerLog
from app.services.auth_service import AuthService


# 테스트용 SQLite 엔진
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """테스트용 DB 세션."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """각 테스트마다 새로운 DB 세션 제공."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """테스트 클라이언트."""
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)

    # 테스트 데이터 생성
    _create_test_data(db_session)

    yield TestClient(app)

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def _create_test_data(db):
    """테스트용 기본 데이터 생성."""
    auth_service = AuthService(db)

    # 강사 생성
    teacher = User(
        id="teacher-001",
        email="teacher@test.com",
        name="테스트 강사",
        role="teacher",
        hashed_password=auth_service.hash_password("password123"),
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db.add(teacher)

    # 반 생성
    test_class = Class(
        id="class-001",
        name="테스트반",
        teacher_id="teacher-001",
        grade="middle_1",
    )
    db.add(test_class)

    # 학생 생성
    student = User(
        id="student-001",
        email="student@test.com",
        name="테스트 학생",
        role="student",
        grade="middle_1",
        class_id="class-001",
        hashed_password=auth_service.hash_password("password123"),
        is_active=True,
        level=1,
        total_xp=100,
        current_streak=3,
        max_streak=5,
    )
    db.add(student)

    # 개념 생성
    concept = Concept(
        id="concept-001",
        name="일차방정식",
        grade="middle_1",
        description="일차방정식의 풀이",
    )
    db.add(concept)

    # 문제 생성 (여러 문제)
    question1 = Question(
        id="question-001",
        concept_id="concept-001",
        question_type="multiple_choice",
        difficulty="medium",
        content="x + 3 = 7 일 때 x의 값은?",
        options=[
            {"id": "1", "label": "A", "text": "2"},
            {"id": "2", "label": "B", "text": "3"},
            {"id": "3", "label": "C", "text": "4"},
            {"id": "4", "label": "D", "text": "5"},
        ],
        correct_answer="C",
        explanation="x = 7 - 3 = 4",
        points=10,
    )
    db.add(question1)

    question2 = Question(
        id="question-002",
        concept_id="concept-001",
        question_type="multiple_choice",
        difficulty="medium",
        content="2x = 10 일 때 x의 값은?",
        options=[
            {"id": "1", "label": "A", "text": "3"},
            {"id": "2", "label": "B", "text": "4"},
            {"id": "3", "label": "C", "text": "5"},
            {"id": "4", "label": "D", "text": "6"},
        ],
        correct_answer="C",
        explanation="x = 10 / 2 = 5",
        points=10,
    )
    db.add(question2)

    question3 = Question(
        id="question-003",
        concept_id="concept-001",
        question_type="multiple_choice",
        difficulty="easy",
        content="x - 2 = 3 일 때 x의 값은?",
        options=[
            {"id": "1", "label": "A", "text": "4"},
            {"id": "2", "label": "B", "text": "5"},
            {"id": "3", "label": "C", "text": "6"},
            {"id": "4", "label": "D", "text": "7"},
        ],
        correct_answer="B",
        explanation="x = 3 + 2 = 5",
        points=10,
    )
    db.add(question3)

    # 테스트 생성
    test = Test(
        id="test-001",
        title="일차방정식 테스트",
        description="일차방정식 풀이 연습",
        grade="middle_1",
        concept_ids=["concept-001"],
        question_ids=["question-001", "question-002", "question-003"],
        question_count=3,
        time_limit_minutes=10,
        is_active=True,
    )
    db.add(test)

    db.commit()
