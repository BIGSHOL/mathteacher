import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text as sa_text

from app.core.config import settings
from app.core.database import Base, sync_engine, AsyncSessionLocal, SyncSessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("google_genai").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Rate Limiter 설정
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])


def init_db():
    """Initialize database tables and seed data."""
    # Import all models to register them with Base
    from app.models import (
        User, Class, Concept, Question, Test, TestAttempt, AnswerLog,
        Chapter, ChapterProgress, ConceptMastery, DailyTestRecord
    )
    from app.models.user import RefreshToken
    from app.services.auth_service import AuthService

    # 테이블 생성 (없는 테이블만 생성, 기존 데이터 보존)
    Base.metadata.create_all(bind=sync_engine)

    # Seed initial data if database is empty (using sync session)
    db = SyncSessionLocal()
    try:
        if not db.query(User).first():
            auth_service = AuthService(db)

            # Create master (최고 관리자)
            master = User(
                id="master-001",
                login_id="master01",
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
                login_id="admin01",
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
                login_id="teacher01",
                name="테스트 강사",
                role="teacher",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
            )
            db.add(teacher)
            db.flush()

            # Create classes (학년별 테스트반)
            test_class_m1 = Class(
                id="class-001",
                name="중1 테스트반",
                teacher_id="teacher-001",
                grade="middle_1",
            )
            test_class_e3 = Class(
                id="class-002",
                name="초3 테스트반",
                teacher_id="teacher-001",
                grade="elementary_3",
            )
            test_class_h1 = Class(
                id="class-003",
                name="고1 테스트반",
                teacher_id="teacher-001",
                grade="high_1",
            )
            db.add_all([test_class_m1, test_class_e3, test_class_h1])
            db.flush()

            # Create students (학년별 테스트 학생)
            student_m1 = User(
                id="student-001",
                login_id="student01",
                name="테스트 학생(중1)",
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
            student_e3 = User(
                id="student-002",
                login_id="student02",
                name="테스트 학생(초3)",
                role="student",
                grade="elementary_3",
                class_id="class-002",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
                level=1,
                total_xp=0,
                current_streak=0,
                max_streak=0,
            )
            student_h1 = User(
                id="student-003",
                login_id="student03",
                name="테스트 학생(고1)",
                role="student",
                grade="high_1",
                class_id="class-003",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
                level=1,
                total_xp=0,
                current_streak=0,
                max_streak=0,
            )
            db.add_all([student_m1, student_e3, student_h1])

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

            # 2022 개정 교육과정 중1 단원 구조 (6단원, 완전 순차)
            m1_chapters = [
                Chapter(
                    id="chapter-m1-01",
                    name="1. 소인수분해",
                    grade="middle_1",
                    chapter_number=1,
                    description="소수, 합성수, 소인수분해, 최대공약수, 최소공배수",
                    concept_ids=["concept-m1-prime"],
                    mastery_threshold=90,
                    final_test_pass_score=90,
                    require_teacher_approval=False,
                    is_active=True,
                ),
                Chapter(
                    id="chapter-m1-02",
                    name="2. 정수와 유리수",
                    grade="middle_1",
                    chapter_number=2,
                    description="양수·음수, 절댓값, 정수·유리수 사칙연산, 혼합 계산",
                    concept_ids=["concept-m1-integer", "concept-002"],
                    mastery_threshold=90,
                    final_test_pass_score=90,
                    require_teacher_approval=False,
                    is_active=True,
                ),
                Chapter(
                    id="chapter-m1-03",
                    name="3. 문자와 식 / 일차방정식",
                    grade="middle_1",
                    chapter_number=3,
                    description="문자 사용, 식의 값, 일차식 계산, 등식의 성질, 일차방정식 풀이",
                    concept_ids=["concept-m1-expression", "concept-m1-equation", "concept-001", "concept-003"],
                    final_test_id="test-001",
                    mastery_threshold=90,
                    final_test_pass_score=90,
                    require_teacher_approval=False,
                    is_active=True,
                ),
                Chapter(
                    id="chapter-m1-04",
                    name="4. 좌표평면과 그래프",
                    grade="middle_1",
                    chapter_number=4,
                    description="순서쌍, 좌표평면, 사분면, 정비례·반비례 그래프",
                    concept_ids=["concept-m1-coord", "concept-m1-proportion", "concept-004"],
                    mastery_threshold=90,
                    final_test_pass_score=90,
                    require_teacher_approval=False,
                    is_active=True,
                ),
                Chapter(
                    id="chapter-m1-05",
                    name="5. 기본 도형과 작도",
                    grade="middle_1",
                    chapter_number=5,
                    description="점·선·면·각, 작도, 삼각형 합동조건, 다각형 내각·외각",
                    concept_ids=["concept-m1-basic-geo", "concept-m1-plane-fig", "concept-m1-solid-fig"],
                    mastery_threshold=90,
                    final_test_pass_score=90,
                    require_teacher_approval=False,
                    is_active=True,
                ),
                Chapter(
                    id="chapter-m1-06",
                    name="6. 자료의 정리와 해석",
                    grade="middle_1",
                    chapter_number=6,
                    description="줄기와 잎 그림, 도수분포표, 히스토그램, 상대도수",
                    concept_ids=["concept-m1-frequency", "concept-m1-representative", "concept-m1-scatter", "concept-005"],
                    mastery_threshold=90,
                    final_test_pass_score=90,
                    require_teacher_approval=False,
                    is_active=True,
                ),
            ]
            for ch in m1_chapters:
                db.add(ch)

            db.flush()

            # 단원 선수관계 설정 (완전 순차: 1→2→3→4→5→6)
            for i in range(1, len(m1_chapters)):
                m1_chapters[i].prerequisites.append(m1_chapters[i - 1])

            # =============================================
            # 전체 학년 Chapter 데이터 (2022 개정 교육과정)
            # 초3~초6: 12단원 (1학기 6 + 2학기 6)
            # 중2: 6단원, 중3: 7단원
            # 공통수학1(high_1): 4단원, 공통수학2(high_2): 3단원
            # =============================================
            _chapter_defs = {
                # --- 초등학교 3학년 (12단원) - 개념 데이터 미구축 ---
                "e3": ("elementary_3", [
                    ("1. 덧셈과 뺄셈", "세 자리 수의 덧셈과 뺄셈, 받아올림과 받아내림", []),
                    ("2. 평면도형", "선분, 반직선, 직선, 각, 직각", []),
                    ("3. 나눗셈", "등분제, 포함제, 곱셈과 나눗셈의 관계", []),
                    ("4. 곱셈", "(몇십몇)×(몇), 올림이 있는 곱셈, 분배법칙의 기초", []),
                    ("5. 길이와 시간", "km와 m, 시간의 덧셈과 뺄셈", []),
                    ("6. 분수와 소수", "분수의 개념, 소수의 개념, 분수와 소수의 관계", []),
                    ("7. 곱셈 (2)", "(몇)×(몇십몇), (몇십몇)×(몇십몇)", []),
                    ("8. 나눗셈 (2)", "(두 자리 수)÷(한 자리 수), 나머지가 있는 나눗셈", []),
                    ("9. 원", "원의 중심, 반지름, 지름, 컴퍼스 사용", []),
                    ("10. 들이와 무게", "L와 mL, kg과 g, 들이와 무게의 덧셈과 뺄셈", []),
                    ("11. 분수 (2)", "단위분수, 진분수, 가분수, 대분수, 분수의 크기 비교", []),
                    ("12. 자료의 정리", "그림그래프, 자료의 분류와 정리", []),
                ]),
                # --- 초등학교 4학년 (12단원) ---
                "e4": ("elementary_4", [
                    ("1. 큰 수", "만, 억, 조, 수의 크기 비교, 자릿값", ["E4-NUM-01", "E4-NUM-02", "E4-NUM-03", "E4-NUM-04"]),
                    ("2. 각도", "각의 크기, 예각·직각·둔각, 삼각형 내각의 합", ["E4-GEO-01", "E4-GEO-02", "E4-GEO-03"]),
                    ("3. 곱셈과 나눗셈", "(세 자리 수)×(두 자리 수), (세 자리 수)÷(두 자리 수)", ["E4-NUM-05", "E4-NUM-06"]),
                    ("4. 평면도형의 이동", "밀기, 뒤집기, 돌리기", ["E4-GEO-08"]),
                    ("5. 막대그래프", "막대그래프 읽기와 그리기, 눈금 설정", ["E4-STA-01"]),
                    ("6. 규칙 찾기", "수의 배열에서 규칙 찾기, 규칙을 식으로 나타내기", ["E4-ALG-01"]),
                    ("7. 분수의 덧셈과 뺄셈", "진분수·대분수의 덧셈과 뺄셈, 통분", ["E4-NUM-07", "E4-NUM-08", "E4-NUM-09", "E4-NUM-10"]),
                    ("8. 삼각형", "이등변삼각형, 정삼각형, 예각·직각·둔각삼각형", ["E4-GEO-04", "E4-GEO-05"]),
                    ("9. 소수의 덧셈과 뺄셈", "소수 두 자리 수의 덧셈과 뺄셈", ["E4-NUM-11", "E4-NUM-12"]),
                    ("10. 사각형", "수직과 평행, 평행사변형, 마름모, 사다리꼴", ["E4-GEO-06"]),
                    ("11. 꺾은선그래프", "꺾은선그래프 읽기와 그리기, 변화 추이", ["E4-STA-02"]),
                    ("12. 다각형", "정다각형, 대각선, 다각형의 내각의 합", ["E4-GEO-07"]),
                ]),
                # --- 초등학교 5학년 (12단원) ---
                "e5": ("elementary_5", [
                    ("1. 자연수의 혼합 계산", "연산의 우선순위, 괄호가 있는 식, 문장제 모델링", ["E5-NUM-07"]),
                    ("2. 약수와 배수", "약수, 배수, 최대공약수, 최소공배수", ["E5-NUM-01", "E5-NUM-02", "E5-NUM-03", "E5-NUM-04"]),
                    ("3. 규칙과 대응", "두 양 사이의 관계, 대응 관계를 식으로 표현", ["E5-ALG-01"]),
                    ("4. 약분과 통분", "분수의 기본 성질, 약분, 통분, 크기 비교", ["E5-NUM-05", "E5-NUM-06"]),
                    ("5. 분수의 덧셈과 뺄셈", "이분모 분수의 덧셈과 뺄셈, 대분수 혼합 계산", ["E5-NUM-08", "E5-NUM-09", "E5-NUM-10"]),
                    ("6. 다각형의 둘레와 넓이", "직사각형, 평행사변형, 삼각형, 사다리꼴, 마름모의 넓이", ["E5-GEO-01", "E5-GEO-02", "E5-GEO-03", "E5-GEO-04"]),
                    ("7. 수의 범위와 어림하기", "이상, 이하, 초과, 미만, 올림, 버림, 반올림", ["E5-NUM-11", "E5-NUM-12"]),
                    ("8. 분수의 곱셈", "(분수)×(자연수), (자연수)×(분수), (분수)×(분수)", ["E5-NUM-13"]),
                    ("9. 합동과 대칭", "합동인 도형, 선대칭, 점대칭", ["E5-GEO-05", "E5-GEO-06"]),
                    ("10. 소수의 곱셈", "(소수)×(자연수), (소수)×(소수), 곱의 소수점 위치", ["E5-NUM-14"]),
                    ("11. 직육면체", "직육면체와 정육면체, 전개도, 겨냥도", ["E5-GEO-07"]),
                    ("12. 평균과 가능성", "평균 구하기, 가능성의 표현, 경우의 수", ["E5-NUM-15", "E5-NUM-16"]),
                ]),
                # --- 초등학교 6학년 (12단원) ---
                "e6": ("elementary_6", [
                    ("1. 분수의 나눗셈", "(자연수)÷(자연수)의 몫을 분수로, (분수)÷(자연수)", ["E6-NUM-01", "E6-NUM-02"]),
                    ("2. 각기둥과 각뿔", "각기둥과 각뿔의 구성 요소, 전개도", ["E6-GEO-01"]),
                    ("3. 소수의 나눗셈", "(소수)÷(자연수), 몫의 소수점 위치", ["E6-NUM-04"]),
                    ("4. 비와 비율", "비, 비율, 백분율, 기준량과 비교하는 양", ["E6-ALG-01", "E6-ALG-02"]),
                    ("5. 여러 가지 그래프", "띠그래프, 원그래프, 그래프 해석", ["E6-STA-01"]),
                    ("6. 직육면체의 부피와 겉넓이", "부피 단위, 직육면체의 부피와 겉넓이 구하기", ["E6-GEO-02"]),
                    ("7. 분수의 나눗셈 (2)", "(분수)÷(분수), 역수 활용", ["E6-NUM-03"]),
                    ("8. 소수의 나눗셈 (2)", "(소수)÷(소수), 소수점 이동 원리", ["E6-NUM-05"]),
                    ("9. 공간과 입체", "쌓기나무, 공간 감각, 위·앞·옆에서 본 모양", ["E6-GEO-06"]),
                    ("10. 비례식과 비례배분", "비례식의 성질, 비례배분", ["E6-ALG-03", "E6-ALG-04"]),
                    ("11. 원의 넓이", "원주율, 원의 둘레, 원의 넓이", ["E6-GEO-03", "E6-GEO-04"]),
                    ("12. 원기둥, 원뿔, 구", "원기둥의 전개도와 겉넓이, 원뿔, 구의 특징", ["E6-GEO-05"]),
                ]),
                # --- 중학교 2학년 (6단원) ---
                "m2": ("middle_2", [
                    ("1. 유리수와 순환소수 / 식의 계산", "유한소수, 순환소수, 지수법칙, 다항식 계산", ["M2-NUM-01", "M2-ALG-01", "M2-ALG-02"]),
                    ("2. 일차부등식과 연립방정식", "일차부등식 풀이, 연립일차방정식(가감법·대입법)", ["M2-ALG-03", "M2-ALG-04"]),
                    ("3. 일차함수", "기울기, 절편, 그래프, 일차함수와 일차방정식", ["M2-FUNC-01"]),
                    ("4. 삼각형과 사각형의 성질", "이등변삼각형, 외심·내심, 평행사변형, 특수사각형", ["M2-GEO-01"]),
                    ("5. 도형의 닮음과 피타고라스 정리", "닮음 조건, 닮음비, 피타고라스 정리", ["M2-GEO-02"]),
                    ("6. 확률", "경우의 수, 확률의 기본, 여사건, 연속 사건", ["M2-STA-01"]),
                ]),
                # --- 중학교 3학년 (7단원) ---
                "m3": ("middle_3", [
                    ("1. 실수와 그 연산", "제곱근, 무리수, 실수의 대소, 근호 계산, 분모의 유리화", ["M3-NUM-01", "M3-NUM-02"]),
                    ("2. 다항식의 곱셈과 인수분해", "곱셈공식, 인수분해, 완전제곱식", ["M3-ALG-01", "M3-ALG-02"]),
                    ("3. 이차방정식", "인수분해·완전제곱식·근의 공식 풀이, 판별식", ["M3-ALG-03"]),
                    ("4. 이차함수", "y=ax², 표준형, 일반형, 꼭짓점, 최대·최소", ["M3-FUNC-01"]),
                    ("5. 삼각비", "sin·cos·tan 정의, 특수각, 삼각형 넓이", ["M3-GEO-01"]),
                    ("6. 원의 성질", "원주각, 중심각, 접선, 내접 사각형", ["M3-GEO-02"]),
                    ("7. 통계", "대푯값, 산점도, 상관관계, 상자그림", ["M3-STA-01", "M3-STA-02"]),
                ]),
                # --- 공통수학1 / 고1 1학기 (4단원) ---
                "h1": ("high_1", [
                    ("1. 다항식", "다항식 연산, 항등식, 나머지정리, 인수분해", ["H1-ALG-01", "H1-ALG-02", "H1-ALG-03", "H1-ALG-04", "H1-ALG-05"]),
                    ("2. 방정식과 부등식", "복소수, 이차방정식, 이차함수, 이차부등식", ["H1-ALG-06", "H1-ALG-07", "H1-ALG-08", "H1-ALG-09", "H1-ALG-10", "H1-ALG-11", "H1-ALG-12", "H1-ALG-13", "H1-ALG-14", "H1-ALG-15", "H1-ALG-16", "H1-ALG-17"]),
                    ("3. 경우의 수", "합·곱의 법칙, 순열, 조합", ["H1-STA-10", "H1-STA-08", "H1-STA-09", "H1-STA-11", "H1-STA-12"]),
                    ("4. 행렬", "행렬의 덧셈·뺄셈·실수배·곱셈 (2×2 한정)", ["H1-ALG-18", "H1-ALG-19", "H1-ALG-20", "H1-ALG-21", "H1-ALG-22", "H1-ALG-23"]),
                ]),
                # --- 공통수학2 / 고1 2학기 (3단원) - 개념 데이터 미구축 ---
                "h2": ("high_2", [
                    ("1. 도형의 방정식", "평면좌표, 직선·원의 방정식, 평행이동·대칭이동", []),
                    ("2. 집합과 명제", "집합 연산, 명제와 조건, 절대부등식", ["H1-STA-01", "H1-STA-02", "H1-STA-03", "H1-STA-04", "H1-STA-05", "H1-STA-06", "H1-STA-07"]),
                    ("3. 함수", "합성함수, 역함수, 유리함수, 무리함수", []),
                ]),
            }

            all_new_chapters = {}
            for prefix, (grade, ch_list) in _chapter_defs.items():
                grade_chapters = []
                for idx, (name, desc, cids) in enumerate(ch_list, 1):
                    ch = Chapter(
                        id=f"chapter-{prefix}-{idx:02d}",
                        name=name,
                        grade=grade,
                        chapter_number=idx,
                        description=desc,
                        concept_ids=cids,
                        mastery_threshold=90,
                        final_test_pass_score=90,
                        require_teacher_approval=False,
                        is_active=True,
                    )
                    db.add(ch)
                    grade_chapters.append(ch)
                all_new_chapters[prefix] = grade_chapters

            db.flush()

            # 각 학년 단원 선수관계 설정 (순차)
            for grade_chapters in all_new_chapters.values():
                for i in range(1, len(grade_chapters)):
                    grade_chapters[i].prerequisites.append(grade_chapters[i - 1])

            # 각 테스트 학생에게 1단원 해제 (학습 시작 가능)
            _unlock_defs = [
                ("student-001", "chapter-m1-01", "concept-001"),   # 중1
                ("student-002", "chapter-e3-01", None),            # 초3
                ("student-003", "chapter-h1-01", None),            # 고1
            ]
            for sid, ch_id, concept_id in _unlock_defs:
                db.add(ChapterProgress(
                    student_id=sid,
                    chapter_id=ch_id,
                    is_unlocked=True,
                    unlocked_at=datetime.now(timezone.utc),
                ))
                if concept_id:
                    db.add(ConceptMastery(
                        student_id=sid,
                        concept_id=concept_id,
                        is_unlocked=True,
                        unlocked_at=datetime.now(timezone.utc),
                    ))

            db.commit()
            print("Database seeded with initial data")
    finally:
        db.close()


def load_seed_data():
    """Load structured seed data (concepts, questions, tests) from seeds module."""
    from app.models.concept import Concept
    from app.models.question import Question
    from app.models.test import Test

    db = SyncSessionLocal()
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


def update_chapter_concept_ids():
    """서버 시작 시 챕터 concept_ids를 최신 매핑으로 갱신."""
    from app.models.chapter import Chapter

    # 중1 단원-개념 매핑 (실제 seed_concepts.py의 ID 사용)
    CHAPTER_CONCEPT_MAP = {
        "chapter-m1-01": ["M1-NUM-01", "M1-NUM-02"],  # 소인수분해
        "chapter-m1-02": ["M1-NUM-03", "M1-NUM-04"],  # 정수와 유리수
        "chapter-m1-03": ["M1-ALG-01", "M1-ALG-02"],  # 문자와 식 / 일차방정식
        "chapter-m1-04": ["M1-FUNC-01"],             # 좌표평면과 그래프
        "chapter-m1-05": ["M1-GEO-01", "M1-GEO-02", "M1-GEO-03"],  # 기본 도형과 작도
        "chapter-m1-06": ["M1-STA-01"],              # 자료의 정리와 해석
    }

    db = SyncSessionLocal()
    try:
        updated = 0
        for chapter_id, concept_ids in CHAPTER_CONCEPT_MAP.items():
            ch = db.query(Chapter).filter(Chapter.id == chapter_id).first()
            if ch and ch.concept_ids != concept_ids:
                ch.concept_ids = concept_ids
                updated += 1
        if updated:
            # 챕터 매핑이 변경되면 오늘의 일일 테스트를 삭제하여 재생성 유도
            _cleanup_today_daily_tests(db)
            db.commit()
            logger.info(f"Updated concept_ids for {updated} chapters, cleaned up today's daily tests")
        else:
            db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update chapter concept_ids: {e}")
    finally:
        db.close()


def _cleanup_today_daily_tests(db):
    """오늘의 일일 테스트 레코드 및 관련 테스트/시도 삭제."""
    from app.models.daily_test_record import DailyTestRecord
    from app.models.test import Test
    from app.models.test_attempt import TestAttempt
    from app.models.answer_log import AnswerLog

    KST = timezone(timedelta(hours=9))
    today = datetime.now(KST).date().isoformat()
    records = db.query(DailyTestRecord).filter(DailyTestRecord.date == today).all()
    if not records:
        return

    for record in records:
        # 연결된 attempt와 answer_log 삭제
        if record.attempt_id:
            db.query(AnswerLog).filter(AnswerLog.attempt_id == record.attempt_id).delete()
            db.query(TestAttempt).filter(TestAttempt.id == record.attempt_id).delete()
        # 일일 테스트 Test 레코드 삭제
        if record.test_id:
            db.query(Test).filter(Test.id == record.test_id).delete()
        db.delete(record)

    logger.info(f"Cleaned up {len(records)} daily test records for today ({today})")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup - 동기 DB 초기화를 스레드풀에서 실행 (이벤트 루프 블로킹 방지)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, init_db)
    await loop.run_in_executor(None, load_seed_data)
    await loop.run_in_executor(None, update_chapter_concept_ids)
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

# Rate Limiter를 앱에 연결
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
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
# CORS 헤더를 에러 응답에도 추가하여 브라우저에서 에러 내용을 확인할 수 있도록 함
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 서버 로그에는 상세 정보 기록 (디버깅용)
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    # Origin 헤더 확인하여 CORS 헤더 추가
    origin = request.headers.get("origin", "")
    cors_headers = {}
    if origin in settings.BACKEND_CORS_ORIGINS:
        cors_headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
        }

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
            headers=cors_headers,
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
            headers=cors_headers,
        )


# API v1 Router
from app.api.v1 import api_router

app.include_router(api_router)
