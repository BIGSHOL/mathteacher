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
        category="concept",
        part="algebra",
        description="일차방정식의 풀이",
    )
    db.add(concept)

    # 문제 생성 (개념 이해 문제)
    question1 = Question(
        id="question-001",
        concept_id="concept-001",
        category="concept",
        part="algebra",
        question_type="multiple_choice",
        difficulty=6,
        content="다음 중 일차방정식인 것은?",
        options=[
            {"id": "1", "label": "A", "text": "x + 3"},
            {"id": "2", "label": "B", "text": "2x - 1 = 5"},
            {"id": "3", "label": "C", "text": "x² = 4"},
            {"id": "4", "label": "D", "text": "x + y = 3"},
        ],
        correct_answer="B",
        explanation="일차방정식은 미지수가 1개이고 차수가 1인 등식이다. 2x - 1 = 5만 이 조건을 만족한다.",
        points=10,
    )
    db.add(question1)

    question2 = Question(
        id="question-002",
        concept_id="concept-001",
        category="concept",
        part="algebra",
        question_type="multiple_choice",
        difficulty=6,
        content="등식 x + 5 = 12에서 x를 구하기 위해 양변에 해야 할 연산은?",
        options=[
            {"id": "1", "label": "A", "text": "양변에 5를 더한다"},
            {"id": "2", "label": "B", "text": "양변에서 5를 뺀다"},
            {"id": "3", "label": "C", "text": "양변에 12를 더한다"},
            {"id": "4", "label": "D", "text": "양변을 5로 나눈다"},
        ],
        correct_answer="B",
        explanation="좌변의 +5를 없애려면 양변에서 5를 빼야 한다. 이것이 등식의 성질이다.",
        points=10,
    )
    db.add(question2)

    question3 = Question(
        id="question-003",
        concept_id="concept-001",
        category="concept",
        part="algebra",
        question_type="multiple_choice",
        difficulty=6,
        content="일차방정식의 풀이에서 '이항'이란?",
        options=[
            {"id": "1", "label": "A", "text": "등호 양변에 같은 수를 더하는 것"},
            {"id": "2", "label": "B", "text": "항을 등호의 반대편으로 부호를 바꿔 옮기는 것"},
            {"id": "3", "label": "C", "text": "미지수끼리 모으는 것"},
            {"id": "4", "label": "D", "text": "양변을 같은 수로 나누는 것"},
        ],
        correct_answer="B",
        explanation="이항이란 등식에서 한 항을 부호를 바꾸어 반대편으로 옮기는 것이다.",
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
