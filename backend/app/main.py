import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Initialize database tables and seed data."""
    # Import all models to register them with Base
    from app.models import (
        User, Class, Concept, Question, Test, TestAttempt, AnswerLog,
        Chapter, ChapterProgress, ConceptMastery
    )
    from app.models.user import RefreshToken
    from app.services.auth_service import AuthService

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Seed initial data if database is empty
    db = SessionLocal()
    try:
        if not db.query(User).first():
            auth_service = AuthService(db)

            # Create master (최고 관리자)
            master = User(
                id="master-001",
                email="master@test.com",
                name="마스터 관리자",
                role="master",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
            )
            db.add(master)
            db.flush()

            # Create admin (관리자)
            admin = User(
                id="admin-001",
                email="admin@test.com",
                name="테스트 관리자",
                role="admin",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
            )
            db.add(admin)
            db.flush()

            # Create teacher
            teacher = User(
                id="teacher-001",
                email="teacher@test.com",
                name="테스트 강사",
                role="teacher",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
            )
            db.add(teacher)
            db.flush()

            # Create class
            test_class = Class(
                id="class-001",
                name="테스트반",
                teacher_id="teacher-001",
                grade="middle_1",
            )
            db.add(test_class)
            db.flush()

            # Create student
            student = User(
                id="student-001",
                email="student@test.com",
                name="테스트 학생",
                role="student",
                grade="middle_1",
                class_id="class-001",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
                level=3,
                total_xp=450,
                current_streak=5,
                max_streak=7,
            )
            db.add(student)

            # Create concept
            concept = Concept(
                id="concept-001",
                name="일차방정식",
                grade="middle_1",
                category="concept",
                part="algebra",
                description="일차방정식의 풀이",
            )
            db.add(concept)

            # Create questions (개념 이해도 테스트 - 정의/성질/과정 이해)
            questions = [
                Question(
                    id="question-001",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=6,
                    content="다음 중 일차방정식인 것은?",
                    options=[
                        {"id": "1", "label": "A", "text": "x² + 2 = 6"},
                        {"id": "2", "label": "B", "text": "3x - 5 = 7"},
                        {"id": "3", "label": "C", "text": "2x + y = 10"},
                        {"id": "4", "label": "D", "text": "x > 3"},
                    ],
                    correct_answer="B",
                    explanation="일차방정식은 미지수가 1개이고 차수가 1인 등식입니다. A는 이차, C는 미지수 2개, D는 부등식입니다.",
                    points=10,
                ),
                Question(
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
                        {"id": "3", "label": "C", "text": "양변에 12를 곱한다"},
                        {"id": "4", "label": "D", "text": "양변을 5로 나눈다"},
                    ],
                    correct_answer="B",
                    explanation="등식의 성질: 양변에서 같은 수를 빼도 등식이 성립합니다. x + 5 - 5 = 12 - 5 → x = 7",
                    points=10,
                ),
                Question(
                    id="question-003",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=6,
                    content="일차방정식의 풀이에서 '이항'이란?",
                    options=[
                        {"id": "1", "label": "A", "text": "항을 없애는 것"},
                        {"id": "2", "label": "B", "text": "항의 부호를 바꾸어 등호 반대편으로 옮기는 것"},
                        {"id": "3", "label": "C", "text": "양변에 같은 수를 곱하는 것"},
                        {"id": "4", "label": "D", "text": "미지수끼리 더하는 것"},
                    ],
                    correct_answer="B",
                    explanation="이항이란 등식의 한 변의 항을 부호를 바꾸어 다른 변으로 옮기는 것입니다.",
                    points=10,
                ),
            ]
            for q in questions:
                db.add(q)

            # 적응형 풀을 위한 추가 일차방정식 문제 (개념 이해도, 다양한 난이도)
            adaptive_questions = [
                # 난이도 2 (기초 정의)
                Question(
                    id="question-a-001",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=2,
                    content="등호(=)가 포함된 식을 무엇이라 하는가?",
                    options=[
                        {"id": "1", "label": "A", "text": "부등식"},
                        {"id": "2", "label": "B", "text": "등식"},
                        {"id": "3", "label": "C", "text": "다항식"},
                        {"id": "4", "label": "D", "text": "단항식"},
                    ],
                    correct_answer="B",
                    explanation="등호(=)를 사용하여 두 식이 같음을 나타낸 식을 등식이라 합니다.",
                    points=10,
                ),
                Question(
                    id="question-a-002",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=2,
                    content="다음 중 등식인 것은?",
                    options=[
                        {"id": "1", "label": "A", "text": "3 + 5"},
                        {"id": "2", "label": "B", "text": "x > 2"},
                        {"id": "3", "label": "C", "text": "x + 1 = 4"},
                        {"id": "4", "label": "D", "text": "2x + 3"},
                    ],
                    correct_answer="C",
                    explanation="등식은 등호(=)가 있는 식입니다. x + 1 = 4만 등호가 있습니다.",
                    points=10,
                ),
                # 난이도 3
                Question(
                    id="question-a-003",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=3,
                    content="방정식에서 값을 모르는 문자를 무엇이라 하는가?",
                    options=[
                        {"id": "1", "label": "A", "text": "상수"},
                        {"id": "2", "label": "B", "text": "계수"},
                        {"id": "3", "label": "C", "text": "미지수"},
                        {"id": "4", "label": "D", "text": "차수"},
                    ],
                    correct_answer="C",
                    explanation="방정식에서 값을 모르는 문자를 미지수라 하고, 미지수의 값을 구하는 것을 '방정식을 푼다'고 합니다.",
                    points=10,
                ),
                # 난이도 4
                Question(
                    id="question-a-004",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=4,
                    content="x + 5 = 8에서 x를 구하기 위해 양변에서 빼야 하는 수는?",
                    options=[
                        {"id": "1", "label": "A", "text": "3"},
                        {"id": "2", "label": "B", "text": "5"},
                        {"id": "3", "label": "C", "text": "8"},
                        {"id": "4", "label": "D", "text": "13"},
                    ],
                    correct_answer="B",
                    explanation="등식의 성질: 양변에서 같은 수 5를 빼면 x + 5 - 5 = 8 - 5, 즉 x = 3이 됩니다.",
                    points=10,
                ),
                Question(
                    id="question-a-005",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=4,
                    content="'a = b이면 a + c = b + c이다'는 등식의 어떤 성질인가?",
                    options=[
                        {"id": "1", "label": "A", "text": "양변에 같은 수를 더해도 등식은 성립한다"},
                        {"id": "2", "label": "B", "text": "양변에 같은 수를 곱해도 등식은 성립한다"},
                        {"id": "3", "label": "C", "text": "양변을 같은 수로 나누어도 등식은 성립한다"},
                        {"id": "4", "label": "D", "text": "양변의 부호를 바꾸어도 등식은 성립한다"},
                    ],
                    correct_answer="A",
                    explanation="a = b이면 a + c = b + c는 '양변에 같은 수를 더해도 등식이 성립한다'는 성질입니다.",
                    points=10,
                ),
                # 난이도 5
                Question(
                    id="question-a-006",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=5,
                    content="3x = 12를 풀 때 양변을 나누어야 하는 수는?",
                    options=[
                        {"id": "1", "label": "A", "text": "2"},
                        {"id": "2", "label": "B", "text": "3"},
                        {"id": "3", "label": "C", "text": "4"},
                        {"id": "4", "label": "D", "text": "12"},
                    ],
                    correct_answer="B",
                    explanation="x의 계수인 3으로 양변을 나누면: 3x ÷ 3 = 12 ÷ 3, 즉 x = 4가 됩니다.",
                    points=10,
                ),
                # 난이도 7
                Question(
                    id="question-a-007",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=7,
                    content="2x - 3 = 7의 풀이 과정입니다. 잘못된 단계는?\n① 2x - 3 + 3 = 7 + 3\n② 2x = 10\n③ 2x × 2 = 10 × 2\n④ x = 5",
                    options=[
                        {"id": "1", "label": "A", "text": "① 단계"},
                        {"id": "2", "label": "B", "text": "② 단계"},
                        {"id": "3", "label": "C", "text": "③ 단계"},
                        {"id": "4", "label": "D", "text": "④ 단계"},
                    ],
                    correct_answer="C",
                    explanation="③에서 양변에 2를 곱하면 4x = 20이 됩니다. 올바른 방법은 양변을 2로 '나누는' 것입니다.",
                    points=15,
                ),
                Question(
                    id="question-a-008",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=7,
                    content="다음 중 해가 x = -2인 일차방정식은?",
                    options=[
                        {"id": "1", "label": "A", "text": "x + 5 = 3"},
                        {"id": "2", "label": "B", "text": "2x + 1 = 5"},
                        {"id": "3", "label": "C", "text": "x - 2 = 0"},
                        {"id": "4", "label": "D", "text": "3x = 6"},
                    ],
                    correct_answer="A",
                    explanation="x = -2를 대입하면: A) -2 + 5 = 3 ✓, B) -4 + 1 = -3 ✗, C) -4 ✗, D) -6 ✗",
                    points=15,
                ),
                # 난이도 8
                Question(
                    id="question-a-009",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=8,
                    content="일차방정식 ax + b = 0 (a ≠ 0)의 해를 a, b로 나타내면?",
                    options=[
                        {"id": "1", "label": "A", "text": "x = b/a"},
                        {"id": "2", "label": "B", "text": "x = -b/a"},
                        {"id": "3", "label": "C", "text": "x = a/b"},
                        {"id": "4", "label": "D", "text": "x = -a/b"},
                    ],
                    correct_answer="B",
                    explanation="ax + b = 0 → ax = -b → x = -b/a (a ≠ 0)",
                    points=15,
                ),
                # 난이도 9
                Question(
                    id="question-a-010",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=9,
                    content="분수 방정식 (x+1)/3 = (x-1)/2를 풀 때 가장 먼저 해야 할 것은?",
                    options=[
                        {"id": "1", "label": "A", "text": "양변에 3을 곱한다"},
                        {"id": "2", "label": "B", "text": "양변에 6을 곱한다 (분모의 최소공배수)"},
                        {"id": "3", "label": "C", "text": "분자끼리 등식을 세운다"},
                        {"id": "4", "label": "D", "text": "양변에서 1을 뺀다"},
                    ],
                    correct_answer="B",
                    explanation="분모 3과 2의 최소공배수 6을 양변에 곱하면 분모를 없앨 수 있습니다: 2(x+1) = 3(x-1)",
                    points=20,
                ),
                # 난이도 10 (문장제 개념)
                Question(
                    id="question-a-011",
                    concept_id="concept-001",
                    category="concept",
                    part="word",
                    question_type="multiple_choice",
                    difficulty=10,
                    content="'어떤 수의 3배에서 5를 빼면 그 수에 7을 더한 것과 같다'를 방정식으로 바르게 세운 것은?",
                    options=[
                        {"id": "1", "label": "A", "text": "3x - 5 = x + 7"},
                        {"id": "2", "label": "B", "text": "3(x - 5) = x + 7"},
                        {"id": "3", "label": "C", "text": "3x + 5 = x - 7"},
                        {"id": "4", "label": "D", "text": "3x - 5 = 7x"},
                    ],
                    correct_answer="A",
                    explanation="'어떤 수의 3배' → 3x, '에서 5를 빼면' → 3x - 5, '그 수에 7을 더한 것' → x + 7. 따라서 3x - 5 = x + 7",
                    points=20,
                ),
            ]
            for q in adaptive_questions:
                db.add(q)

            # Create test (고정형) - 종합 테스트 12문제로 확대
            test = Test(
                id="test-001",
                title="일차방정식 종합 테스트",
                description="일차방정식의 기본부터 응용까지 총 12문제",
                grade="middle_1",
                concept_ids=["concept-001"],
                question_ids=[
                    # 기본 개념 (4문제 - 40점)
                    "question-a-001",  # 등식 정의
                    "question-a-002",  # 등식 판별
                    "question-a-003",  # 미지수 정의
                    "question-001",    # 일차방정식 판별
                    # 기본 풀이 (4문제 - 40점)
                    "question-002",    # 등식 성질
                    "question-003",    # 이항
                    "question-a-004",  # x = 7 판별
                    "question-a-006",  # 3x = 12 풀이
                    # 응용 (4문제 - 40점)
                    "question-a-007",  # 2x + 3 = 11 풀이
                    "question-a-008",  # 복잡한 방정식
                    "question-a-009",  # 일반형 해
                    "question-a-005",  # 해 대입 확인
                ],
                question_count=12,
                time_limit_minutes=20,
                is_active=True,
            )
            db.add(test)

            # Create adaptive test (적응형)
            adaptive_test = Test(
                id="test-adaptive-001",
                title="적응형 일차방정식",
                description="실력에 맞게 난이도가 자동 조절됩니다",
                grade="middle_1",
                concept_ids=["concept-001"],
                question_ids=[],  # 적응형은 비워둠
                question_count=8,
                time_limit_minutes=15,
                is_active=True,
                is_adaptive=True,
            )
            db.add(adaptive_test)

            # Create question pool test (문제 풀 테스트)
            # 11개 문제 중 랜덤으로 5개만 출제, 보기 셔플
            pool_test = Test(
                id="test-pool-001",
                title="일차방정식 연습 (랜덤)",
                description="11개 문제 중 5개가 랜덤으로 출제되고, 보기 순서도 매번 바뀝니다. 정답 외우기 방지!",
                grade="middle_1",
                concept_ids=["concept-001"],
                question_ids=[
                    "question-a-001",
                    "question-a-002",
                    "question-a-003",
                    "question-a-004",
                    "question-a-005",
                    "question-a-006",
                    "question-a-007",
                    "question-a-008",
                    "question-a-009",
                    "question-a-010",
                    "question-a-011",
                ],
                question_count=11,  # 전체 풀 크기
                time_limit_minutes=10,
                is_active=True,
                use_question_pool=True,
                questions_per_attempt=5,  # 한 번 시도에 5문제만
                shuffle_options=True,  # 보기 셔플
            )
            db.add(pool_test)

            # Create placement test (진단 평가)
            # 다양한 단원의 대표 문제로 구성
            placement_test = Test(
                id="test-placement-001",
                title="실력 진단 평가",
                description="5-10분 테스트로 당신에게 딱 맞는 학습 경로를 찾아드립니다",
                grade="middle_1",
                concept_ids=[
                    "concept-001",  # 일차방정식
                    "concept-002",  # 사칙연산
                    "concept-003",  # 일차부등식
                    "concept-004",  # 좌표와 그래프
                    "concept-005",  # 통계
                ],
                question_ids=[
                    # 일차방정식 (기초)
                    "question-001",
                    "question-002",
                    # 적응형 문제 (다양한 난이도)
                    "question-a-003",  # 난이도 3
                    "question-a-006",  # 난이도 5
                    "question-a-009",  # 난이도 8
                    # 사칙연산
                    "question-op-003",
                    "question-op-005",
                    # 일차부등식
                    "question-ineq-001",
                    "question-ineq-003",
                    # 좌표
                    "question-coord-001",
                    # 통계
                    "question-stat-001",
                ],
                question_count=11,
                time_limit_minutes=10,
                is_active=True,
                is_placement=True,  # 진단 평가 플래그
            )
            db.add(placement_test)

            # Create operation practice concept
            op_concept = Concept(
                id="concept-002",
                name="사칙연산",
                grade="middle_1",
                category="computation",
                part="calc",
                description="덧셈, 뺄셈, 곱셈, 나눗셈 연산 연습",
            )
            db.add(op_concept)

            # Create operation practice questions
            op_questions = [
                Question(
                    id="question-op-001",
                    concept_id="concept-002",
                    category="computation",
                    part="calc",
                    question_type="multiple_choice",
                    difficulty=2,
                    content="25 + 37 = ?",
                    options=[
                        {"id": "1", "label": "A", "text": "52"},
                        {"id": "2", "label": "B", "text": "62"},
                        {"id": "3", "label": "C", "text": "72"},
                        {"id": "4", "label": "D", "text": "63"},
                    ],
                    correct_answer="B",
                    explanation="25 + 37 = 62",
                    points=10,
                ),
                Question(
                    id="question-op-002",
                    concept_id="concept-002",
                    category="computation",
                    part="calc",
                    question_type="multiple_choice",
                    difficulty=2,
                    content="84 - 29 = ?",
                    options=[
                        {"id": "1", "label": "A", "text": "45"},
                        {"id": "2", "label": "B", "text": "65"},
                        {"id": "3", "label": "C", "text": "55"},
                        {"id": "4", "label": "D", "text": "53"},
                    ],
                    correct_answer="C",
                    explanation="84 - 29 = 55",
                    points=10,
                ),
                Question(
                    id="question-op-003",
                    concept_id="concept-002",
                    category="computation",
                    part="calc",
                    question_type="multiple_choice",
                    difficulty=3,
                    content="12 × 7 = ?",
                    options=[
                        {"id": "1", "label": "A", "text": "74"},
                        {"id": "2", "label": "B", "text": "84"},
                        {"id": "3", "label": "C", "text": "94"},
                        {"id": "4", "label": "D", "text": "72"},
                    ],
                    correct_answer="B",
                    explanation="12 × 7 = 84",
                    points=10,
                ),
                Question(
                    id="question-op-004",
                    concept_id="concept-002",
                    category="computation",
                    part="calc",
                    question_type="multiple_choice",
                    difficulty=3,
                    content="96 ÷ 8 = ?",
                    options=[
                        {"id": "1", "label": "A", "text": "11"},
                        {"id": "2", "label": "B", "text": "12"},
                        {"id": "3", "label": "C", "text": "13"},
                        {"id": "4", "label": "D", "text": "14"},
                    ],
                    correct_answer="B",
                    explanation="96 ÷ 8 = 12",
                    points=10,
                ),
                Question(
                    id="question-op-005",
                    concept_id="concept-002",
                    category="computation",
                    part="calc",
                    question_type="multiple_choice",
                    difficulty=5,
                    content="(-3) × (-8) + 5 = ?",
                    options=[
                        {"id": "1", "label": "A", "text": "19"},
                        {"id": "2", "label": "B", "text": "29"},
                        {"id": "3", "label": "C", "text": "-19"},
                        {"id": "4", "label": "D", "text": "-29"},
                    ],
                    correct_answer="B",
                    explanation="(-3) × (-8) = 24, 24 + 5 = 29",
                    points=15,
                ),
            ]
            for q in op_questions:
                db.add(q)

            # Create operation practice test
            op_test = Test(
                id="test-002",
                title="연산 연습",
                description="반복 연습으로 연산 속도를 높여보세요",
                grade="middle_1",
                concept_ids=["concept-002"],
                question_ids=[
                    "question-op-001",
                    "question-op-002",
                    "question-op-003",
                    "question-op-004",
                    "question-op-005",
                ],
                question_count=5,
                time_limit_minutes=5,
                is_active=True,
            )
            db.add(op_test)

            # Create inequalities concept
            ineq_concept = Concept(
                id="concept-003",
                name="일차부등식",
                grade="middle_1",
                category="concept",
                part="algebra",
                description="일차부등식의 풀이와 수직선 표현",
            )
            db.add(ineq_concept)

            ineq_questions = [
                Question(
                    id="question-ineq-001",
                    concept_id="concept-003",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=6,
                    content="부등식의 양변에 같은 음수를 곱하면 부등호의 방향은 어떻게 되는가?",
                    options=[
                        {"id": "1", "label": "A", "text": "그대로 유지된다"},
                        {"id": "2", "label": "B", "text": "반대로 바뀐다"},
                        {"id": "3", "label": "C", "text": "등호로 바뀐다"},
                        {"id": "4", "label": "D", "text": "부등식이 성립하지 않는다"},
                    ],
                    correct_answer="B",
                    explanation="부등식의 양변에 음수를 곱하거나 나누면 부등호의 방향이 반대로 바뀐다. 예: 3 > 2에서 양변에 -1을 곱하면 -3 < -2",
                    points=10,
                ),
                Question(
                    id="question-ineq-002",
                    concept_id="concept-003",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=7,
                    content="다음 중 부등식의 성질로 옳은 것은?",
                    options=[
                        {"id": "1", "label": "A", "text": "양변에 같은 수를 더하면 부등호 방향이 바뀐다"},
                        {"id": "2", "label": "B", "text": "양변에 양수를 곱하면 부등호 방향이 바뀐다"},
                        {"id": "3", "label": "C", "text": "양변에 음수를 곱하면 부등호 방향이 바뀐다"},
                        {"id": "4", "label": "D", "text": "양변에 0을 곱해도 부등호가 유지된다"},
                    ],
                    correct_answer="C",
                    explanation="부등식의 양변에 음수를 곱하면 부등호의 방향이 바뀐다. 양변에 같은 수를 더하거나 양수를 곱할 때는 부등호 방향이 유지된다.",
                    points=10,
                ),
                Question(
                    id="question-ineq-003",
                    concept_id="concept-003",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=7,
                    content="일차부등식의 해를 수직선에 나타낼 때, x < 3의 표현으로 옳은 것은?",
                    options=[
                        {"id": "1", "label": "A", "text": "3에 속이 빈 원(○)을 찍고 왼쪽으로 화살표"},
                        {"id": "2", "label": "B", "text": "3에 속이 찬 원(●)을 찍고 왼쪽으로 화살표"},
                        {"id": "3", "label": "C", "text": "3에 속이 빈 원(○)을 찍고 오른쪽으로 화살표"},
                        {"id": "4", "label": "D", "text": "3에 속이 찬 원(●)을 찍고 오른쪽으로 화살표"},
                    ],
                    correct_answer="A",
                    explanation="x < 3은 3을 포함하지 않으므로 속이 빈 원(○)을 사용하고, 3보다 작은 수는 왼쪽이므로 왼쪽 화살표로 나타낸다. x ≤ 3이면 속이 찬 원(●)을 사용한다.",
                    points=15,
                ),
                Question(
                    id="question-ineq-004",
                    concept_id="concept-003",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=9,
                    content="일차부등식 -3x + 6 > 0의 풀이 과정이다. 잘못된 단계는?\n① -3x + 6 > 0\n② -3x > -6 (양변에서 6을 뺌)\n③ x > 2 (양변을 -3으로 나눔)",
                    options=[
                        {"id": "1", "label": "A", "text": "①에서 ②로 가는 과정"},
                        {"id": "2", "label": "B", "text": "②에서 ③으로 가는 과정"},
                        {"id": "3", "label": "C", "text": "①과 ② 모두 잘못됨"},
                        {"id": "4", "label": "D", "text": "잘못된 단계가 없다"},
                    ],
                    correct_answer="B",
                    explanation="②에서 ③으로 갈 때 양변을 음수(-3)로 나누었으므로 부등호 방향이 바뀌어야 한다. 올바른 결과는 x < 2이다.",
                    points=15,
                ),
            ]
            for q in ineq_questions:
                db.add(q)

            ineq_test = Test(
                id="test-003",
                title="일차부등식 테스트",
                description="부등식의 성질을 이용한 문제 풀이",
                grade="middle_1",
                concept_ids=["concept-003"],
                question_ids=["question-ineq-001", "question-ineq-002", "question-ineq-003", "question-ineq-004"],
                question_count=4,
                time_limit_minutes=8,
                is_active=True,
            )
            db.add(ineq_test)

            # Create coordinate & graph concept
            coord_concept = Concept(
                id="concept-004",
                name="좌표와 그래프",
                grade="middle_1",
                category="concept",
                part="func",
                description="좌표평면과 정비례·반비례 그래프",
            )
            db.add(coord_concept)

            coord_questions = [
                Question(
                    id="question-coord-001",
                    concept_id="concept-004",
                    category="concept",
                    part="func",
                    question_type="multiple_choice",
                    difficulty=6,
                    content="좌표평면에서 x좌표가 양수이고 y좌표가 음수인 점은 어느 사분면에 위치하는가?",
                    options=[
                        {"id": "1", "label": "A", "text": "제1사분면"},
                        {"id": "2", "label": "B", "text": "제2사분면"},
                        {"id": "3", "label": "C", "text": "제3사분면"},
                        {"id": "4", "label": "D", "text": "제4사분면"},
                    ],
                    correct_answer="D",
                    explanation="제4사분면은 x > 0, y < 0인 영역이다. 제1사분면(+,+), 제2사분면(-,+), 제3사분면(-,-), 제4사분면(+,-)로 구분한다.",
                    points=10,
                ),
                Question(
                    id="question-coord-002",
                    concept_id="concept-004",
                    category="concept",
                    part="func",
                    question_type="multiple_choice",
                    difficulty=7,
                    content="정비례 관계 y = ax (a > 0)의 그래프에 대한 설명으로 옳은 것은?",
                    options=[
                        {"id": "1", "label": "A", "text": "원점을 지나는 직선이다"},
                        {"id": "2", "label": "B", "text": "y축과 평행한 직선이다"},
                        {"id": "3", "label": "C", "text": "x축과 한 점에서 만난다"},
                        {"id": "4", "label": "D", "text": "곡선 형태이다"},
                    ],
                    correct_answer="A",
                    explanation="정비례 y = ax의 그래프는 항상 원점(0,0)을 지나는 직선이다. a > 0이면 오른쪽 위로 향하고, a < 0이면 오른쪽 아래로 향한다.",
                    points=10,
                ),
                Question(
                    id="question-coord-003",
                    concept_id="concept-004",
                    category="concept",
                    part="func",
                    question_type="multiple_choice",
                    difficulty=6,
                    content="반비례 관계 y = a/x의 그래프가 절대 지나지 않는 곳은?",
                    options=[
                        {"id": "1", "label": "A", "text": "제1사분면"},
                        {"id": "2", "label": "B", "text": "제3사분면"},
                        {"id": "3", "label": "C", "text": "원점과 좌표축"},
                        {"id": "4", "label": "D", "text": "제4사분면"},
                    ],
                    correct_answer="C",
                    explanation="반비례 y = a/x에서 x = 0이면 y가 정의되지 않고, y = 0이 되는 x값도 없다. 따라서 그래프는 원점과 x축, y축을 절대 지나지 않는다.",
                    points=10,
                ),
                Question(
                    id="question-coord-004",
                    concept_id="concept-004",
                    category="concept",
                    part="func",
                    question_type="multiple_choice",
                    difficulty=9,
                    content="좌표평면에서 x축 위에 있는 모든 점의 공통된 특징은?",
                    options=[
                        {"id": "1", "label": "A", "text": "x좌표가 0이다"},
                        {"id": "2", "label": "B", "text": "y좌표가 0이다"},
                        {"id": "3", "label": "C", "text": "x좌표와 y좌표가 같다"},
                        {"id": "4", "label": "D", "text": "원점으로부터 거리가 같다"},
                    ],
                    correct_answer="B",
                    explanation="x축 위의 점은 모두 y좌표가 0이다. 예: (1,0), (-3,0), (0,0) 등. 반대로, y축 위의 점은 모두 x좌표가 0이다.",
                    points=15,
                ),
            ]
            for q in coord_questions:
                db.add(q)

            coord_test = Test(
                id="test-004",
                title="좌표와 그래프",
                description="좌표평면 위의 점과 그래프 읽기",
                grade="middle_1",
                concept_ids=["concept-004"],
                question_ids=["question-coord-001", "question-coord-002", "question-coord-003", "question-coord-004"],
                question_count=4,
                time_limit_minutes=10,
                is_active=True,
            )
            db.add(coord_test)

            # Create statistics concept
            stat_concept = Concept(
                id="concept-005",
                name="통계",
                grade="middle_1",
                category="concept",
                part="data",
                description="도수분포와 평균, 중앙값",
            )
            db.add(stat_concept)

            stat_questions = [
                Question(
                    id="question-stat-001",
                    concept_id="concept-005",
                    category="concept",
                    part="data",
                    question_type="multiple_choice",
                    difficulty=4,
                    content="평균, 중앙값, 최빈값 중에서 극단적으로 크거나 작은 값(이상값)에 가장 큰 영향을 받는 대표값은?",
                    options=[
                        {"id": "1", "label": "A", "text": "평균"},
                        {"id": "2", "label": "B", "text": "중앙값"},
                        {"id": "3", "label": "C", "text": "최빈값"},
                        {"id": "4", "label": "D", "text": "세 대표값 모두 같은 영향을 받는다"},
                    ],
                    correct_answer="A",
                    explanation="평균은 모든 자료값의 합을 개수로 나눈 것이므로 극단값에 크게 영향을 받는다. 중앙값은 가운데 위치의 값이고 최빈값은 가장 많이 나타나는 값이므로 극단값에 상대적으로 덜 영향을 받는다.",
                    points=10,
                ),
                Question(
                    id="question-stat-002",
                    concept_id="concept-005",
                    category="concept",
                    part="data",
                    question_type="multiple_choice",
                    difficulty=6,
                    content="자료를 크기순으로 나열했을 때 한가운데에 위치하는 값을 무엇이라 하는가?",
                    options=[
                        {"id": "1", "label": "A", "text": "평균"},
                        {"id": "2", "label": "B", "text": "중앙값"},
                        {"id": "3", "label": "C", "text": "최빈값"},
                        {"id": "4", "label": "D", "text": "분산"},
                    ],
                    correct_answer="B",
                    explanation="중앙값(median)은 자료를 크기순으로 나열했을 때 정가운데에 위치하는 값이다. 자료의 개수가 짝수이면 가운데 두 값의 평균을 중앙값으로 한다.",
                    points=10,
                ),
                Question(
                    id="question-stat-003",
                    concept_id="concept-005",
                    category="concept",
                    part="data",
                    question_type="multiple_choice",
                    difficulty=6,
                    content="도수분포표에서 '도수'가 의미하는 것은?",
                    options=[
                        {"id": "1", "label": "A", "text": "각 계급에 속하는 자료의 개수"},
                        {"id": "2", "label": "B", "text": "자료의 전체 개수"},
                        {"id": "3", "label": "C", "text": "계급의 크기"},
                        {"id": "4", "label": "D", "text": "자료의 평균값"},
                    ],
                    correct_answer="A",
                    explanation="도수(frequency)란 각 계급(구간)에 속하는 자료의 개수를 말한다. 모든 계급의 도수를 합하면 전체 자료의 개수가 된다.",
                    points=10,
                ),
            ]
            for q in stat_questions:
                db.add(q)

            stat_test = Test(
                id="test-005",
                title="통계 기초",
                description="평균, 중앙값, 최빈값 구하기",
                grade="middle_1",
                concept_ids=["concept-005"],
                question_ids=["question-stat-001", "question-stat-002", "question-stat-003"],
                question_count=3,
                time_limit_minutes=7,
                is_active=True,
            )
            db.add(stat_test)

            # ============================================================
            # 빈칸 채우기(fill_in_blank) 문제 추가
            # ============================================================
            fill_blank_questions = [
                Question(
                    id="question-fb-001",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="fill_in_blank",
                    difficulty=3,
                    content="일차방정식 2x + 6 = 0 의 해는 x = _____ 이다.",
                    options=None,
                    correct_answer="-3",
                    explanation="2x + 6 = 0 → 2x = -6 → x = -3",
                    points=10,
                    blank_config={
                        "blank_count": 1,
                        "accept_formats": ["-3"],
                    },
                ),
                Question(
                    id="question-fb-002",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="fill_in_blank",
                    difficulty=5,
                    content="일차방정식 3x - 9 = 6 의 해는 x = _____ 이다.",
                    options=None,
                    correct_answer="5",
                    explanation="3x - 9 = 6 → 3x = 15 → x = 5",
                    points=10,
                    blank_config={
                        "blank_count": 1,
                        "accept_formats": ["5"],
                    },
                ),
                Question(
                    id="question-fb-003",
                    concept_id="concept-002",
                    category="computation",
                    part="calc",
                    question_type="fill_in_blank",
                    difficulty=4,
                    content="(-12) ÷ 4 + 7 = _____",
                    options=None,
                    correct_answer="4",
                    explanation="(-12) ÷ 4 = -3, -3 + 7 = 4",
                    points=10,
                    blank_config={
                        "blank_count": 1,
                        "accept_formats": ["4"],
                    },
                ),
                Question(
                    id="question-fb-004",
                    concept_id="concept-002",
                    category="computation",
                    part="calc",
                    question_type="fill_in_blank",
                    difficulty=6,
                    content="(-5) × 3 + (-2) × (-4) = _____",
                    options=None,
                    correct_answer="-7",
                    explanation="(-5) × 3 = -15, (-2) × (-4) = 8, -15 + 8 = -7",
                    points=15,
                    blank_config={
                        "blank_count": 1,
                        "accept_formats": ["-7"],
                    },
                ),
                Question(
                    id="question-fb-005",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="fill_in_blank",
                    difficulty=7,
                    content="일차방정식 5(x - 2) = 3x + 4 의 해는 x = _____ 이다.",
                    options=None,
                    correct_answer="7",
                    explanation="5x - 10 = 3x + 4 → 2x = 14 → x = 7",
                    points=15,
                    blank_config={
                        "blank_count": 1,
                        "accept_formats": ["7"],
                    },
                ),
            ]
            for q in fill_blank_questions:
                db.add(q)

            # ============================================================
            # 고난이도 문제 추가 (Lv.6~10) - 적응형 테스트 난이도 범위 확대
            # ============================================================

            # 연산(computation) 고난이도
            high_op_questions = [
                Question(
                    id="question-op-006",
                    concept_id="concept-002",
                    category="computation",
                    part="calc",
                    question_type="multiple_choice",
                    difficulty=6,
                    content="(-2)³ + 3² = ?",
                    options=[
                        {"id": "1", "label": "A", "text": "1"},
                        {"id": "2", "label": "B", "text": "-1"},
                        {"id": "3", "label": "C", "text": "17"},
                        {"id": "4", "label": "D", "text": "-17"},
                    ],
                    correct_answer="A",
                    explanation="(-2)³ = -8, 3² = 9, -8 + 9 = 1",
                    points=15,
                ),
                Question(
                    id="question-op-007",
                    concept_id="concept-002",
                    category="computation",
                    part="calc",
                    question_type="multiple_choice",
                    difficulty=7,
                    content="|-5| × (-3) + |12 - 20| = ?",
                    options=[
                        {"id": "1", "label": "A", "text": "-7"},
                        {"id": "2", "label": "B", "text": "7"},
                        {"id": "3", "label": "C", "text": "-23"},
                        {"id": "4", "label": "D", "text": "23"},
                    ],
                    correct_answer="A",
                    explanation="|-5| = 5, 5 × (-3) = -15, |12-20| = |-8| = 8, -15 + 8 = -7",
                    points=15,
                ),
                Question(
                    id="question-op-008",
                    concept_id="concept-002",
                    category="computation",
                    part="calc",
                    question_type="multiple_choice",
                    difficulty=8,
                    content="(-1)¹⁰⁰ + (-1)⁹⁹ = ?",
                    options=[
                        {"id": "1", "label": "A", "text": "2"},
                        {"id": "2", "label": "B", "text": "-2"},
                        {"id": "3", "label": "C", "text": "0"},
                        {"id": "4", "label": "D", "text": "1"},
                    ],
                    correct_answer="C",
                    explanation="(-1)¹⁰⁰ = 1 (짝수 거듭제곱), (-1)⁹⁹ = -1 (홀수 거듭제곱), 1 + (-1) = 0",
                    points=15,
                ),
                Question(
                    id="question-op-009",
                    concept_id="concept-002",
                    category="computation",
                    part="calc",
                    question_type="multiple_choice",
                    difficulty=9,
                    content="2/3 ÷ (-4/9) × 3/2 = ?",
                    options=[
                        {"id": "1", "label": "A", "text": "-9/4"},
                        {"id": "2", "label": "B", "text": "9/4"},
                        {"id": "3", "label": "C", "text": "-3/2"},
                        {"id": "4", "label": "D", "text": "4/9"},
                    ],
                    correct_answer="A",
                    explanation="2/3 ÷ (-4/9) = 2/3 × (-9/4) = -18/12 = -3/2, (-3/2) × (3/2) = -9/4",
                    points=20,
                ),
                Question(
                    id="question-op-010",
                    concept_id="concept-002",
                    category="computation",
                    part="calc",
                    question_type="multiple_choice",
                    difficulty=10,
                    content="다음 식을 간단히 하면? (-3)² × 2 - 4 × (-2)³ ÷ (-8)",
                    options=[
                        {"id": "1", "label": "A", "text": "14"},
                        {"id": "2", "label": "B", "text": "22"},
                        {"id": "3", "label": "C", "text": "18"},
                        {"id": "4", "label": "D", "text": "14"},
                    ],
                    correct_answer="B",
                    explanation="(-3)² = 9, 9 × 2 = 18. (-2)³ = -8, 4 × (-8) = -32, -32 ÷ (-8) = 4. 18 + 4 = 22",
                    points=20,
                ),
            ]
            for q in high_op_questions:
                db.add(q)

            # 개념(concept) 고난이도 - 일차방정식
            high_eq_questions = [
                Question(
                    id="question-eq-006",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=6,
                    content="일차방정식 4x - 3 = 2x + 7 의 해는?",
                    options=[
                        {"id": "1", "label": "A", "text": "x = 2"},
                        {"id": "2", "label": "B", "text": "x = 5"},
                        {"id": "3", "label": "C", "text": "x = -5"},
                        {"id": "4", "label": "D", "text": "x = -2"},
                    ],
                    correct_answer="B",
                    explanation="4x - 2x = 7 + 3 → 2x = 10 → x = 5",
                    points=10,
                ),
                Question(
                    id="question-eq-007",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=7,
                    content="방정식 2(x + 3) = 3(x - 1) + 11 의 해는?",
                    options=[
                        {"id": "1", "label": "A", "text": "x = 2"},
                        {"id": "2", "label": "B", "text": "x = -2"},
                        {"id": "3", "label": "C", "text": "x = 1"},
                        {"id": "4", "label": "D", "text": "x = 4"},
                    ],
                    correct_answer="B",
                    explanation="2x + 6 = 3x - 3 + 11 → 2x + 6 = 3x + 8 → -x = 2 → x = -2",
                    points=15,
                ),
                Question(
                    id="question-eq-008",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=8,
                    content="방정식 (x-1)/2 = (2x+3)/5 의 해는?",
                    options=[
                        {"id": "1", "label": "A", "text": "x = 11"},
                        {"id": "2", "label": "B", "text": "x = -11"},
                        {"id": "3", "label": "C", "text": "x = 7"},
                        {"id": "4", "label": "D", "text": "x = -7"},
                    ],
                    correct_answer="A",
                    explanation="양변에 10을 곱하면: 5(x-1) = 2(2x+3) → 5x - 5 = 4x + 6 → x = 11",
                    points=15,
                ),
                Question(
                    id="question-eq-009",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=9,
                    content="어떤 수의 3배에서 5를 뺀 값이 그 수에 7을 더한 값의 2배와 같다. 그 수는?",
                    options=[
                        {"id": "1", "label": "A", "text": "19"},
                        {"id": "2", "label": "B", "text": "17"},
                        {"id": "3", "label": "C", "text": "15"},
                        {"id": "4", "label": "D", "text": "9"},
                    ],
                    correct_answer="A",
                    explanation="x를 어떤 수라 하면: 3x - 5 = 2(x + 7) → 3x - 5 = 2x + 14 → x = 19",
                    points=20,
                ),
                Question(
                    id="question-eq-010",
                    concept_id="concept-001",
                    category="concept",
                    part="algebra",
                    question_type="multiple_choice",
                    difficulty=10,
                    content="연속하는 세 홀수의 합이 63일 때, 가장 큰 수는?",
                    options=[
                        {"id": "1", "label": "A", "text": "21"},
                        {"id": "2", "label": "B", "text": "23"},
                        {"id": "3", "label": "C", "text": "25"},
                        {"id": "4", "label": "D", "text": "19"},
                    ],
                    correct_answer="B",
                    explanation="연속하는 세 홀수를 x-2, x, x+2로 놓으면: (x-2)+x+(x+2)=63 → 3x=63 → x=21. 가장 큰 수는 21+2=23",
                    points=20,
                ),
            ]
            for q in high_eq_questions:
                db.add(q)

            # 빈칸 채우기 문제를 포함하는 테스트 생성
            fill_blank_test = Test(
                id="test-006",
                title="빈칸 채우기 연습",
                description="답을 직접 입력하는 빈칸 채우기 문제",
                grade="middle_1",
                concept_ids=["concept-001", "concept-002"],
                question_ids=[
                    "question-fb-001", "question-fb-002", "question-fb-003",
                    "question-fb-004", "question-fb-005",
                ],
                question_count=5,
                time_limit_minutes=10,
                is_active=True,
            )
            db.add(fill_blank_test)

            db.flush()

            # 계통수학: 개념 선수관계 설정
            # 일차방정식(concept-001) ← 사칙연산(concept-002) 필요
            concept.prerequisites.append(op_concept)
            # 일차부등식(concept-003) ← 일차방정식(concept-001) 필요
            ineq_concept.prerequisites.append(concept)
            # 좌표와 그래프(concept-004) ← 일차방정식(concept-001) 필요
            coord_concept.prerequisites.append(concept)
            # 통계(concept-005) ← 사칙연산(concept-002) 필요
            stat_concept.prerequisites.append(op_concept)

            # 2022 개정 교육과정 단원 구조 (예시: 중1 첫 단원)
            chapter1 = Chapter(
                id="chapter-m1-01",
                name="1. 소인수분해",
                grade="middle_1",
                chapter_number=1,
                description="소수, 합성수, 소인수분해, 최대공약수, 최소공배수",
                concept_ids=[],  # TODO: 소인수분해 관련 개념 추가
                mastery_threshold=90,
                final_test_pass_score=90,
                require_teacher_approval=False,
                is_active=True,
            )
            db.add(chapter1)

            chapter2 = Chapter(
                id="chapter-m1-02",
                name="2. 정수와 유리수",
                grade="middle_1",
                chapter_number=2,
                description="부호, 사칙연산, 혼합 계산, 절댓값",
                concept_ids=[],
                mastery_threshold=90,
                final_test_pass_score=90,
                require_teacher_approval=False,
                is_active=True,
            )
            db.add(chapter2)

            chapter3 = Chapter(
                id="chapter-m1-03",
                name="3. 문자와 식 / 일차방정식",
                grade="middle_1",
                chapter_number=3,
                description="식의 값, 일차방정식 풀이, 활용 문제",
                concept_ids=["concept-001"],  # 일차방정식 개념
                final_test_id="test-001",  # 일차방정식 테스트를 종합 테스트로
                mastery_threshold=90,
                final_test_pass_score=90,
                require_teacher_approval=False,
                is_active=True,
            )
            db.add(chapter3)

            db.flush()

            # 단원 선수관계 설정
            chapter2.prerequisites.append(chapter1)  # 2단원은 1단원 선행
            chapter3.prerequisites.append(chapter2)  # 3단원은 2단원 선행

            # student@test.com에게 1단원 해제 (학습 시작 가능)
            student_user = db.query(User).filter(User.email == "student@test.com").first()
            if student_user:
                # 1단원 해제
                ch1_progress = ChapterProgress(
                    student_id=student_user.id,
                    chapter_id="chapter-m1-01",
                    is_unlocked=True,
                    unlocked_at=datetime.now(timezone.utc),
                )
                db.add(ch1_progress)

                # 일차방정식 개념 해제 (3단원 학습 위해)
                concept_mastery = ConceptMastery(
                    student_id=student_user.id,
                    concept_id="concept-001",
                    is_unlocked=True,
                    unlocked_at=datetime.now(timezone.utc),
                )
                db.add(concept_mastery)

            db.commit()
            print("Database seeded with initial data")
    finally:
        db.close()


def load_seed_data():
    """Load structured seed data (concepts, questions, tests) from seeds module."""
    from app.models.concept import Concept
    from app.models.question import Question
    from app.models.test import Test

    db = SessionLocal()
    try:
        # Check if seed data already loaded (by checking for seed-style concept IDs)
        seed_exists = db.query(Concept).filter(Concept.id.like("concept-m1-%")).first()
        if seed_exists:
            logger.info("Seed data already loaded, skipping")
            return

        logger.info("Loading seed data from seeds module...")
        from app.seeds import get_all_grade_seed_data
        data = get_all_grade_seed_data()

        existing_concepts = {c.id for c in db.query(Concept.id).all()}
        existing_questions = {q.id for q in db.query(Question.id).all()}
        existing_tests = {t.id for t in db.query(Test.id).all()}

        # Concepts
        created_concepts = 0
        for c in data["concepts"]:
            if c["id"] not in existing_concepts:
                db.add(Concept(
                    id=c["id"], name=c["name"], grade=c["grade"],
                    category=c["category"], part=c["part"],
                    description=c.get("description", ""),
                    parent_id=c.get("parent_id"),
                ))
                created_concepts += 1
        db.flush()

        # Questions
        created_questions = 0
        for q in data["questions"]:
            if q["id"] not in existing_questions:
                db.add(Question(
                    id=q["id"], concept_id=q["concept_id"],
                    category=q["category"], part=q["part"],
                    question_type=q["question_type"], difficulty=q["difficulty"],
                    content=q["content"], options=q.get("options"),
                    correct_answer=q["correct_answer"],
                    explanation=q.get("explanation", ""),
                    points=q.get("points", 10),
                    blank_config=q.get("blank_config"),
                ))
                created_questions += 1
        db.flush()

        # Tests
        created_tests = 0
        for t in data["tests"]:
            if t["id"] not in existing_tests:
                db.add(Test(
                    id=t["id"], title=t["title"],
                    description=t.get("description", ""),
                    grade=t["grade"], concept_ids=t["concept_ids"],
                    question_ids=t["question_ids"],
                    question_count=t.get("question_count", len(t["question_ids"])),
                    time_limit_minutes=t.get("time_limit_minutes"),
                    is_adaptive=t.get("is_adaptive", False),
                    is_active=t.get("is_active", True),
                    use_question_pool=t.get("use_question_pool", False),
                    questions_per_attempt=t.get("questions_per_attempt"),
                    shuffle_options=t.get("shuffle_options", True),
                ))
                created_tests += 1

        db.commit()
        logger.info(
            f"Seed data loaded: {created_concepts} concepts, "
            f"{created_questions} questions, {created_tests} tests"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to load seed data: {e}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    init_db()
    load_seed_data()
    yield
    # Shutdown


app = FastAPI(
    title="Math Test API",
    description="수학 개념 및 연산 테스트 프로그램 API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Math Test API", "docs": "/docs"}


# Exception handler - 프로덕션에서는 상세 에러 정보 숨김
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 서버 로그에는 상세 정보 기록 (디버깅용)
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    # 클라이언트 응답에는 환경에 따라 다르게 처리
    if settings.ENV == "development":
        # 개발 환경: 디버깅을 위해 상세 에러 표시
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": str(exc),
                    "type": type(exc).__name__,
                }
            },
        )
    else:
        # 프로덕션/스테이징: 보안을 위해 일반적인 에러 메시지만 표시
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "서버 내부 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
                }
            },
        )


# API v1 Router
from app.api.v1 import api_router

app.include_router(api_router)
