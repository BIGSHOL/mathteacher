import asyncio
import logging
import re
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
        Chapter, ChapterProgress, ConceptMastery, DailyTestRecord,
        WrongAnswerReview, Assignment,
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
            )
            test_class_e3 = Class(
                id="class-002",
                name="초3 테스트반",
                teacher_id="teacher-001",
            )
            test_class_h1 = Class(
                id="class-003",
                name="고1 테스트반",
                teacher_id="teacher-001",
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

            # 계통수학: 개념 선수관계 설정 (lazy='raise' 때문에 직접 테이블에 insert)
            from app.models.concept import concept_prerequisites
            # 일차방정식(concept-001) ← 사칙연산(concept-002) 필요
            db.execute(concept_prerequisites.insert().values(
                concept_id=concept.id, prerequisite_id=op_concept.id
            ))
            # 일차부등식(concept-003) ← 일차방정식(concept-001) 필요
            db.execute(concept_prerequisites.insert().values(
                concept_id=ineq_concept.id, prerequisite_id=concept.id
            ))
            # 좌표와 그래프(concept-004) ← 일차방정식(concept-001) 필요
            db.execute(concept_prerequisites.insert().values(
                concept_id=coord_concept.id, prerequisite_id=concept.id
            ))
            # 통계(concept-005) ← 사칙연산(concept-002) 필요
            db.execute(concept_prerequisites.insert().values(
                concept_id=stat_concept.id, prerequisite_id=op_concept.id
            ))

            # =============================================
            # 전체 학년 Chapter 데이터 (2022 개정 교육과정)
            # docs/guides/ 가이드 문서 기준 단원 구성
            # 초3~초6: 12단원 (1학기 6 + 2학기 6)
            # 중1: 12단원 (1학기 6 + 2학기 6)
            # 중2: 8단원 (1학기 4 + 2학기 4)
            # 중3: 7단원 (1학기 4 + 2학기 3)
            # 고1(high_1): 7단원 (공통수학1 4 + 공통수학2 3)
            # =============================================
            _chapter_defs = {
                # --- 초등학교 3학년 (12단원) ---
                # 형식: (name, description, concept_ids, semester)
                "e3": ("elementary_3", [
                    ("1. 덧셈과 뺄셈", "세 자리 수의 덧셈과 뺄셈, 받아올림과 받아내림", ["concept-e3-add-sub-01", "concept-e3-add-sub-02"], 1),
                    ("2. 평면도형", "선분, 반직선, 직선, 각, 직각", ["concept-e3-plane-01", "concept-e3-plane-02"], 1),
                    ("3. 나눗셈", "등분제, 포함제, 곱셈과 나눗셈의 관계", ["concept-e3-div1-01", "concept-e3-div1-02"], 1),
                    ("4. 곱셈", "(몇십몇)×(몇), 올림이 있는 곱셈, 분배법칙의 기초", ["concept-e3-mul1-01", "concept-e3-mul1-02"], 1),
                    ("5. 길이와 시간", "km와 m, 시간의 덧셈과 뺄셈", ["concept-e3-length-time-01", "concept-e3-length-time-02"], 1),
                    ("6. 분수와 소수", "분수의 개념, 소수의 개념, 분수와 소수의 관계", ["concept-e3-frac-dec-01", "concept-e3-frac-dec-02"], 1),
                    ("7. 곱셈 (2)", "(몇)×(몇십몇), (몇십몇)×(몇십몇)", ["concept-e3-mul2-01", "concept-e3-mul2-02"], 2),
                    ("8. 나눗셈 (2)", "(두 자리 수)÷(한 자리 수), 나머지가 있는 나눗셈", ["concept-e3-div2-01", "concept-e3-div2-02"], 2),
                    ("9. 원", "원의 중심, 반지름, 지름, 컴퍼스 사용", ["concept-e3-circle-01", "concept-e3-circle-02"], 2),
                    ("10. 분수 (2)", "단위분수, 진분수, 가분수, 대분수, 분수의 크기 비교", ["concept-e3-frac2-01", "concept-e3-frac2-02"], 2),
                    ("11. 들이와 무게", "L와 mL, kg과 g, 들이와 무게의 덧셈과 뺄셈", ["concept-e3-vol-wt-01", "concept-e3-vol-wt-02"], 2),
                    ("12. 자료의 정리", "그림그래프, 자료의 분류와 정리", ["concept-e3-data-01", "concept-e3-data-02"], 2),
                ]),
                # --- 초등학교 4학년 (12단원) ---
                "e4": ("elementary_4", [
                    ("1. 큰 수", "만, 억, 조, 수의 크기 비교, 자릿값", ["concept-e4-big-num-01", "concept-e4-big-num-02"], 1),
                    ("2. 각도", "각의 크기, 예각·직각·둔각, 삼각형 내각의 합", ["concept-e4-angle-01", "concept-e4-angle-02"], 1),
                    ("3. 곱셈과 나눗셈", "(세 자리 수)×(두 자리 수), (세 자리 수)÷(두 자리 수)", ["concept-e4-mul-div-01", "concept-e4-mul-div-02"], 1),
                    ("4. 평면도형의 이동", "밀기, 뒤집기, 돌리기", ["concept-e4-transform-01", "concept-e4-transform-02"], 1),
                    ("5. 막대그래프", "막대그래프 읽기와 그리기, 눈금 설정", ["concept-e4-bar-graph-01", "concept-e4-bar-graph-02"], 1),
                    ("6. 규칙 찾기", "수의 배열에서 규칙 찾기, 규칙을 식으로 나타내기", ["concept-e4-pattern-01", "concept-e4-pattern-02"], 1),
                    ("7. 분수의 덧셈과 뺄셈", "진분수·대분수의 덧셈과 뺄셈, 통분", ["concept-e4-frac-op-01", "concept-e4-frac-op-02"], 2),
                    ("8. 삼각형", "이등변삼각형, 정삼각형, 예각·직각·둔각삼각형", ["concept-e4-triangle-01", "concept-e4-triangle-02"], 2),
                    ("9. 소수의 덧셈과 뺄셈", "소수 두 자리 수의 덧셈과 뺄셈", ["concept-e4-dec-op-01", "concept-e4-dec-op-02"], 2),
                    ("10. 사각형", "수직과 평행, 평행사변형, 마름모, 사다리꼴", ["concept-e4-quad-01", "concept-e4-quad-02"], 2),
                    ("11. 꺾은선그래프", "꺾은선그래프 읽기와 그리기, 변화 추이", ["concept-e4-line-graph-01", "concept-e4-line-graph-02"], 2),
                    ("12. 다각형", "정다각형, 대각선, 다각형의 내각의 합", ["concept-e4-polygon-01", "concept-e4-polygon-02"], 2),
                ]),
                # --- 초등학교 5학년 (12단원) ---
                "e5": ("elementary_5", [
                    ("1. 자연수의 혼합 계산", "연산의 우선순위, 괄호가 있는 식, 문장제 모델링", ["concept-e5-mixed-calc-01", "concept-e5-mixed-calc-02"], 1),
                    ("2. 약수와 배수", "약수, 배수, 최대공약수, 최소공배수", ["concept-e5-divisor-01", "concept-e5-divisor-02"], 1),
                    ("3. 규칙과 대응", "두 양 사이의 관계, 대응 관계를 식으로 표현", ["concept-e5-corresp-01", "concept-e5-corresp-02"], 1),
                    ("4. 약분과 통분", "분수의 기본 성질, 약분, 통분, 크기 비교", ["concept-e5-reduce-01", "concept-e5-reduce-02"], 1),
                    ("5. 분수의 덧셈과 뺄셈", "이분모 분수의 덧셈과 뺄셈, 대분수 혼합 계산", ["concept-e5-frac-add-01", "concept-e5-frac-add-02"], 1),
                    ("6. 다각형의 둘레와 넓이", "직사각형, 평행사변형, 삼각형, 사다리꼴, 마름모의 넓이", ["concept-e5-poly-area-01", "concept-e5-poly-area-02"], 1),
                    ("7. 수의 범위와 어림하기", "이상, 이하, 초과, 미만, 올림, 버림, 반올림", ["concept-e5-range-01", "concept-e5-round-01"], 2),
                    ("8. 분수의 곱셈", "(분수)×(자연수), (자연수)×(분수), (분수)×(분수)", ["concept-e5-frac-mul-01", "concept-e5-frac-mul-02"], 2),
                    ("9. 합동과 대칭", "합동인 도형, 선대칭, 점대칭", ["concept-e5-congru-01", "concept-e5-congru-02"], 2),
                    ("10. 소수의 곱셈", "(소수)×(자연수), (소수)×(소수), 곱의 소수점 위치", ["concept-e5-dec-mul-01", "concept-e5-dec-mul-02"], 2),
                    ("11. 직육면체", "직육면체와 정육면체, 전개도, 겨냥도", ["concept-e5-cuboid-01", "concept-e5-cuboid-02"], 2),
                    ("12. 평균과 가능성", "평균 구하기, 가능성의 표현, 경우의 수", ["concept-e5-avg-01", "concept-e5-avg-02"], 2),
                ]),
                # --- 초등학교 6학년 (12단원) ---
                "e6": ("elementary_6", [
                    ("1. 분수의 나눗셈", "(자연수)÷(자연수)의 몫을 분수로, (분수)÷(자연수)", ["concept-e6-frac-div1"], 1),
                    ("2. 각기둥과 각뿔", "각기둥과 각뿔의 구성 요소, 전개도", ["concept-e6-prism-pyramid"], 1),
                    ("3. 소수의 나눗셈", "(소수)÷(자연수), 몫의 소수점 위치", ["concept-e6-dec-div1"], 1),
                    ("4. 비와 비율", "비, 비율, 백분율, 기준량과 비교하는 양", ["concept-e6-ratio"], 1),
                    ("5. 여러 가지 그래프", "띠그래프, 원그래프, 그래프 해석", ["concept-e6-graphs"], 1),
                    ("6. 직육면체의 부피와 겉넓이", "부피 단위, 직육면체의 부피와 겉넓이 구하기", ["concept-e6-volume"], 1),
                    ("7. 분수의 나눗셈 (2)", "(분수)÷(분수), 역수 활용", ["concept-e6-frac-div2"], 2),
                    ("8. 소수의 나눗셈 (2)", "(소수)÷(소수), 소수점 이동 원리", ["concept-e6-dec-div2"], 2),
                    ("9. 공간과 입체", "쌓기나무, 공간 감각, 위·앞·옆에서 본 모양", ["concept-e6-spatial"], 2),
                    ("10. 비례식과 비례배분", "비례식의 성질, 비례배분", ["concept-e6-proportion"], 2),
                    ("11. 원의 넓이", "원주율, 원의 둘레, 원의 넓이", ["concept-e6-circle-area"], 2),
                    ("12. 원기둥, 원뿔, 구", "원기둥의 전개도와 겉넓이, 원뿔, 구의 특징", ["concept-e6-solids"], 2),
                ]),
                # --- 중학교 1학년 (12단원: 1학기 6 + 2학기 6) ---
                "m1": ("middle_1", [
                    # 1학기
                    ("1. 소인수분해", "소수, 합성수, 소인수분해, 최대공약수, 최소공배수", ["concept-m1-prime-01", "concept-m1-prime-02", "concept-m1-prime-03"], 1),
                    ("2. 정수와 유리수", "양수·음수·0, 절댓값, 정수·유리수 사칙연산", ["concept-m1-int-01", "concept-m1-int-02", "concept-m1-int-03"], 1),
                    ("3. 문자의 사용과 식의 계산", "문자 사용, 대수적 관습, 동류항, 식의 값", ["concept-m1-expr-01", "concept-m1-expr-02", "concept-m1-expr-03"], 1),
                    ("4. 일차방정식", "등식의 성질, 이항, 일차방정식의 풀이, 활용", ["concept-m1-eq-01", "concept-m1-eq-02", "concept-m1-eq-03"], 1),
                    ("5. 좌표평면과 그래프", "순서쌍, 좌표, 사분면, 그래프 해석", ["concept-m1-coord-01", "concept-m1-coord-02"], 1),
                    ("6. 정비례와 반비례", "정비례 y=ax, 반비례 y=a/x, 그래프", ["concept-m1-prop-01", "concept-m1-prop-02", "concept-m1-prop-03"], 1),
                    # 2학기
                    ("7. 기본 도형과 작도", "점·선·면, 위치 관계, 평행선 성질, 작도, 삼각형 합동", ["concept-m1-geo-01", "concept-m1-geo-02", "concept-m1-geo-03"], 2),
                    ("8. 평면도형의 성질", "다각형 내각·외각의 합, 원과 부채꼴", ["concept-m1-plane-01", "concept-m1-plane-02"], 2),
                    ("9. 입체도형의 성질", "다면체, 회전체, 겉넓이와 부피", ["concept-m1-solid-01", "concept-m1-solid-02", "concept-m1-solid-03"], 2),
                    ("10. 자료의 정리와 해석", "줄기와 잎 그림, 도수분포표, 히스토그램, 상대도수", ["concept-m1-freq-01", "concept-m1-freq-02", "concept-m1-freq-03"], 2),
                    ("11. 대푯값", "평균, 중앙값, 최빈값, 상황별 대푯값 선택", ["concept-m1-repr-01", "concept-m1-repr-02"], 2),
                    ("12. 산점도와 상관관계", "산점도, 양의 상관관계, 음의 상관관계, 인과관계 구분", ["concept-m1-scat-01", "concept-m1-scat-02"], 2),
                ]),
                # --- 중학교 2학년 (8단원: 1학기 4 + 2학기 4) ---
                "m2": ("middle_2", [
                    # 1학기
                    ("1. 유리수와 순환소수", "유한소수 판별, 순환소수, 순환소수의 분수 표현", ["concept-m2-rational-01", "concept-m2-rational-02"], 1),
                    ("2. 식의 계산", "지수법칙, 다항식 계산, 동류항, 분배법칙", ["concept-m2-expr-01", "concept-m2-expr-02"], 1),
                    ("3. 부등식과 연립방정식", "일차부등식 풀이, 연립일차방정식(가감법·대입법)", ["concept-m2-ineq-01", "concept-m2-ineq-02", "concept-m2-simul-01", "concept-m2-simul-02"], 1),
                    ("4. 일차함수", "기울기, 절편, 그래프, 일차함수와 일차방정식", ["concept-m2-linfn-01", "concept-m2-linfn-02"], 1),
                    # 2학기
                    ("5. 도형의 성질", "이등변삼각형, 외심·내심, 평행사변형, 특수사각형", ["concept-m2-tri-01", "concept-m2-tri-02", "concept-m2-quad-01", "concept-m2-quad-02"], 2),
                    ("6. 도형의 닮음", "닮음 조건(SSS, SAS, AA), 닮음비, 넓이비, 부피비", ["concept-m2-simil-01", "concept-m2-simil-02"], 2),
                    ("7. 평행선과 피타고라스 정리", "평행선과 선분의 비, 삼각형 무게중심, 피타고라스 정리", ["concept-m2-pytha-01", "concept-m2-pytha-02"], 2),
                    ("8. 확률", "경우의 수, 합·곱의 법칙, 확률의 기본, 여사건", ["concept-m2-prob-01", "concept-m2-prob-02"], 2),
                ]),
                # --- 중학교 3학년 (7단원) ---
                "m3": ("middle_3", [
                    ("1. 실수와 그 연산", "제곱근, 무리수, 실수의 대소, 근호 계산, 분모의 유리화", ["concept-m3-sqrt-01", "concept-m3-sqrt-02", "concept-m3-sqrt-03"], 1),
                    ("2. 다항식의 곱셈과 인수분해", "곱셈공식, 인수분해, 완전제곱식", ["concept-m3-factor-01", "concept-m3-factor-02", "concept-m3-factor-03"], 1),
                    ("3. 이차방정식", "인수분해·완전제곱식·근의 공식 풀이, 판별식", ["concept-m3-quadeq-01", "concept-m3-quadeq-02", "concept-m3-quadeq-03"], 1),
                    ("4. 이차함수", "y=ax², 표준형, 일반형, 꼭짓점, 최대·최소", ["concept-m3-quadfn-01", "concept-m3-quadfn-02", "concept-m3-quadfn-03"], 1),
                    ("5. 삼각비", "sin·cos·tan 정의, 특수각, 삼각형 넓이", ["concept-m3-trig-01", "concept-m3-trig-02"], 2),
                    ("6. 원의 성질", "원주각, 중심각, 접선, 내접 사각형", ["concept-m3-circle-01", "concept-m3-circle-02", "concept-m3-circle-03"], 2),
                    ("7. 통계", "대푯값, 산점도, 상관관계, 상자그림", ["concept-m3-stat-01", "concept-m3-stat-02", "concept-m3-stat-03"], 2),
                ]),
                # --- 고1 (7단원: 공통수학1 4단원 + 공통수학2 3단원) ---
                "h1": ("high_1", [
                    # 공통수학1 (1학기)
                    ("1. 다항식", "다항식 연산, 항등식, 나머지정리, 인수분해", ["concept-h1-polynomial-01", "concept-h1-polynomial-02"], 1),
                    ("2. 방정식과 부등식", "복소수, 이차방정식, 이차함수, 이차부등식", ["concept-h1-equation-01", "concept-h1-equation-02"], 1),
                    ("3. 경우의 수", "합·곱의 법칙, 순열, 조합", ["concept-h1-counting-01", "concept-h1-counting-02"], 1),
                    ("4. 행렬", "행렬의 덧셈·뺄셈·실수배·곱셈 (2×2 한정)", ["concept-h1-matrix-01", "concept-h1-matrix-02"], 1),
                    # 공통수학2 (2학기)
                    ("5. 도형의 방정식", "평면좌표, 직선·원의 방정식, 평행이동·대칭이동", ["concept-h2-plane-coord", "concept-h2-line", "concept-h2-circle", "concept-h2-transform"], 2),
                    ("6. 집합과 명제", "집합 연산, 명제와 조건, 절대부등식", ["concept-h2-set", "concept-h2-proposition", "concept-h2-abs-inequality"], 2),
                    ("7. 함수", "합성함수, 역함수, 유리함수, 무리함수", ["concept-h2-function", "concept-h2-composite", "concept-h2-rational-irrational"], 2),
                ]),
            }

            all_new_chapters = {}
            for prefix, (grade, ch_list) in _chapter_defs.items():
                grade_chapters = []
                semester_counters: dict[int, int] = {}
                for idx, (name, desc, cids, semester) in enumerate(ch_list, 1):
                    semester_counters[semester] = semester_counters.get(semester, 0) + 1
                    ch_num = semester_counters[semester]
                    # 단원명에서 기존 번호를 제거하고 학기별 번호로 교체
                    clean_name = re.sub(r'^\d+\.\s*', '', name)
                    display_name = f"{ch_num}. {clean_name}"
                    ch = Chapter(
                        id=f"chapter-{prefix}-{idx:02d}",
                        name=display_name,
                        grade=grade,
                        semester=semester,
                        chapter_number=ch_num,
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
            # lazy='raise' 때문에 직접 테이블에 insert
            from app.models.chapter import chapter_prerequisites
            for grade_chapters in all_new_chapters.values():
                for i in range(1, len(grade_chapters)):
                    db.execute(chapter_prerequisites.insert().values(
                        chapter_id=grade_chapters[i].id,
                        prerequisite_id=grade_chapters[i - 1].id
                    ))

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
        else:
            # 기존 테스트 유저의 grade 동기화 (코드와 DB 불일치 해결)
            TEST_USER_GRADES = {
                "student-001": "middle_1",
                "student-002": "elementary_3",
                "student-003": "high_1",
            }
            updated = 0
            for user_id, expected_grade in TEST_USER_GRADES.items():
                user = db.query(User).filter(User.id == user_id).first()
                if user and user.grade != expected_grade:
                    user.grade = expected_grade
                    updated += 1
            if updated:
                db.commit()
                logger.info(f"Updated {updated} test user grades")
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

    # 전체 학년 단원-개념 매핑 (시드 데이터 concept ID 기준)
    CHAPTER_CONCEPT_MAP = {
        # --- 초3 ---
        "chapter-e3-01": ["concept-e3-add-sub-01", "concept-e3-add-sub-02"],
        "chapter-e3-02": ["concept-e3-plane-01", "concept-e3-plane-02"],
        "chapter-e3-03": ["concept-e3-div1-01", "concept-e3-div1-02"],
        "chapter-e3-04": ["concept-e3-mul1-01", "concept-e3-mul1-02"],
        "chapter-e3-05": ["concept-e3-length-time-01", "concept-e3-length-time-02"],
        "chapter-e3-06": ["concept-e3-frac-dec-01", "concept-e3-frac-dec-02"],
        "chapter-e3-07": ["concept-e3-mul2-01", "concept-e3-mul2-02"],
        "chapter-e3-08": ["concept-e3-div2-01", "concept-e3-div2-02"],
        "chapter-e3-09": ["concept-e3-circle-01", "concept-e3-circle-02"],
        "chapter-e3-10": ["concept-e3-frac2-01", "concept-e3-frac2-02"],
        "chapter-e3-11": ["concept-e3-vol-wt-01", "concept-e3-vol-wt-02"],
        "chapter-e3-12": ["concept-e3-data-01", "concept-e3-data-02"],
        # --- 초4 ---
        "chapter-e4-01": ["concept-e4-big-num-01", "concept-e4-big-num-02"],
        "chapter-e4-02": ["concept-e4-angle-01", "concept-e4-angle-02"],
        "chapter-e4-03": ["concept-e4-mul-div-01", "concept-e4-mul-div-02"],
        "chapter-e4-04": ["concept-e4-transform-01", "concept-e4-transform-02"],
        "chapter-e4-05": ["concept-e4-bar-graph-01", "concept-e4-bar-graph-02"],
        "chapter-e4-06": ["concept-e4-pattern-01", "concept-e4-pattern-02"],
        "chapter-e4-07": ["concept-e4-frac-op-01", "concept-e4-frac-op-02"],
        "chapter-e4-08": ["concept-e4-triangle-01", "concept-e4-triangle-02"],
        "chapter-e4-09": ["concept-e4-dec-op-01", "concept-e4-dec-op-02"],
        "chapter-e4-10": ["concept-e4-quad-01", "concept-e4-quad-02"],
        "chapter-e4-11": ["concept-e4-line-graph-01", "concept-e4-line-graph-02"],
        "chapter-e4-12": ["concept-e4-polygon-01", "concept-e4-polygon-02"],
        # --- 초5 ---
        "chapter-e5-01": ["concept-e5-mixed-calc-01", "concept-e5-mixed-calc-02"],
        "chapter-e5-02": ["concept-e5-divisor-01", "concept-e5-divisor-02"],
        "chapter-e5-03": ["concept-e5-corresp-01", "concept-e5-corresp-02"],
        "chapter-e5-04": ["concept-e5-reduce-01", "concept-e5-reduce-02"],
        "chapter-e5-05": ["concept-e5-frac-add-01", "concept-e5-frac-add-02"],
        "chapter-e5-06": ["concept-e5-poly-area-01", "concept-e5-poly-area-02"],
        "chapter-e5-07": ["concept-e5-range-01", "concept-e5-round-01"],
        "chapter-e5-08": ["concept-e5-frac-mul-01", "concept-e5-frac-mul-02"],
        "chapter-e5-09": ["concept-e5-congru-01", "concept-e5-congru-02"],
        "chapter-e5-10": ["concept-e5-dec-mul-01", "concept-e5-dec-mul-02"],
        "chapter-e5-11": ["concept-e5-cuboid-01", "concept-e5-cuboid-02"],
        "chapter-e5-12": ["concept-e5-avg-01", "concept-e5-avg-02"],
        # --- 초6 ---
        "chapter-e6-01": ["concept-e6-frac-div1"],
        "chapter-e6-02": ["concept-e6-prism-pyramid"],
        "chapter-e6-03": ["concept-e6-dec-div1"],
        "chapter-e6-04": ["concept-e6-ratio"],
        "chapter-e6-05": ["concept-e6-graphs"],
        "chapter-e6-06": ["concept-e6-volume"],
        "chapter-e6-07": ["concept-e6-frac-div2"],
        "chapter-e6-08": ["concept-e6-dec-div2"],
        "chapter-e6-09": ["concept-e6-spatial"],
        "chapter-e6-10": ["concept-e6-proportion"],
        "chapter-e6-11": ["concept-e6-circle-area"],
        "chapter-e6-12": ["concept-e6-solids"],
        # --- 중1 ---
        "chapter-m1-01": ["concept-m1-prime-01", "concept-m1-prime-02", "concept-m1-prime-03"],
        "chapter-m1-02": ["concept-m1-int-01", "concept-m1-int-02", "concept-m1-int-03"],
        "chapter-m1-03": ["concept-m1-expr-01", "concept-m1-expr-02", "concept-m1-expr-03"],
        "chapter-m1-04": ["concept-m1-eq-01", "concept-m1-eq-02", "concept-m1-eq-03"],
        "chapter-m1-05": ["concept-m1-coord-01", "concept-m1-coord-02"],
        "chapter-m1-06": ["concept-m1-prop-01", "concept-m1-prop-02", "concept-m1-prop-03"],
        "chapter-m1-07": ["concept-m1-geo-01", "concept-m1-geo-02", "concept-m1-geo-03"],
        "chapter-m1-08": ["concept-m1-plane-01", "concept-m1-plane-02"],
        "chapter-m1-09": ["concept-m1-solid-01", "concept-m1-solid-02", "concept-m1-solid-03"],
        "chapter-m1-10": ["concept-m1-freq-01", "concept-m1-freq-02", "concept-m1-freq-03"],
        "chapter-m1-11": ["concept-m1-repr-01", "concept-m1-repr-02"],
        "chapter-m1-12": ["concept-m1-scat-01", "concept-m1-scat-02"],
        # --- 중2 ---
        "chapter-m2-01": ["concept-m2-rational-01", "concept-m2-rational-02"],
        "chapter-m2-02": ["concept-m2-expr-01", "concept-m2-expr-02"],
        "chapter-m2-03": ["concept-m2-ineq-01", "concept-m2-ineq-02", "concept-m2-simul-01", "concept-m2-simul-02"],
        "chapter-m2-04": ["concept-m2-linfn-01", "concept-m2-linfn-02"],
        "chapter-m2-05": ["concept-m2-tri-01", "concept-m2-tri-02", "concept-m2-quad-01", "concept-m2-quad-02"],
        "chapter-m2-06": ["concept-m2-simil-01", "concept-m2-simil-02"],
        "chapter-m2-07": ["concept-m2-pytha-01", "concept-m2-pytha-02"],
        "chapter-m2-08": ["concept-m2-prob-01", "concept-m2-prob-02"],
        # --- 중3 ---
        "chapter-m3-01": ["concept-m3-sqrt-01", "concept-m3-sqrt-02", "concept-m3-sqrt-03"],
        "chapter-m3-02": ["concept-m3-factor-01", "concept-m3-factor-02", "concept-m3-factor-03"],
        "chapter-m3-03": ["concept-m3-quadeq-01", "concept-m3-quadeq-02", "concept-m3-quadeq-03"],
        "chapter-m3-04": ["concept-m3-quadfn-01", "concept-m3-quadfn-02", "concept-m3-quadfn-03"],
        "chapter-m3-05": ["concept-m3-trig-01", "concept-m3-trig-02"],
        "chapter-m3-06": ["concept-m3-circle-01", "concept-m3-circle-02", "concept-m3-circle-03"],
        "chapter-m3-07": ["concept-m3-stat-01", "concept-m3-stat-02", "concept-m3-stat-03"],
        # --- 고1 (h1+h2 통합) ---
        "chapter-h1-01": ["concept-h1-polynomial-01", "concept-h1-polynomial-02"],
        "chapter-h1-02": ["concept-h1-equation-01", "concept-h1-equation-02"],
        "chapter-h1-03": ["concept-h1-counting-01", "concept-h1-counting-02"],
        "chapter-h1-04": ["concept-h1-matrix-01", "concept-h1-matrix-02"],
        "chapter-h1-05": ["concept-h2-plane-coord", "concept-h2-line", "concept-h2-circle", "concept-h2-transform"],
        "chapter-h1-06": ["concept-h2-set", "concept-h2-proposition", "concept-h2-abs-inequality"],
        "chapter-h1-07": ["concept-h2-function", "concept-h2-composite", "concept-h2-rational-irrational"],
    }

    db = SyncSessionLocal()
    try:
        updated = 0
        missing = 0
        for chapter_id, concept_ids in CHAPTER_CONCEPT_MAP.items():
            ch = db.query(Chapter).filter(Chapter.id == chapter_id).first()
            if not ch:
                missing += 1
                logger.warning(f"Chapter not found: {chapter_id}")
                continue
            if ch.concept_ids != concept_ids:
                logger.info(f"Updating {chapter_id}: {ch.concept_ids} -> {concept_ids}")
                ch.concept_ids = concept_ids
                updated += 1

        # 항상 오늘의 0문제 일일 테스트 정리 (매핑 변경 여부와 무관)
        _cleanup_today_daily_tests(db)
        db.commit()

        if updated:
            logger.info(f"Updated concept_ids for {updated} chapters (missing: {missing}), cleaned up today's daily tests")
        else:
            logger.info(f"All {len(CHAPTER_CONCEPT_MAP)} chapter concept_ids already up to date (missing: {missing})")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update chapter concept_ids: {e}", exc_info=True)
    finally:
        db.close()


def audit_question_categories():
    """DB 문제의 category가 실제 내용과 맞는지 검토하고 자동 수정."""
    from app.models.question import Question

    # -- 1단계: computation → concept 패턴 (연산인데 개념형) --
    COMP_TO_CONCEPT_PATTERNS = [
        re.compile(r"몇\s*개|개수|몇\s*가지"),                          # 개수 세기
        re.compile(r"정의|뜻[은이]|의미"),                               # 정의/용어
        re.compile(r"라\s*한다|이라\s*한다"),                            # ~라 한다
        re.compile(r"성질|특징|옳은\s*것|옳지\s*않은\s*것|바른\s*것"),   # 성질/특징
        re.compile(r"분류|구별|판별"),                                    # 분류
        re.compile(r"인\s*것[은을]|이\s*아닌\s*것"),                     # ~인 것은
        re.compile(r"_{2,}[도를이]|_{2,}\s*(라고?\s*한다|이라)"),        # 용어 빈칸
        re.compile(r"예\s*/\s*아니오|존재하는가|존재하지\s*않"),          # 판별형
        re.compile(r"무엇인가\??$|무엇일까\??$"),                        # 암기형
    ]

    # -- 2단계: concept → computation 패턴 (개념인데 연산형) --
    CALC_INSTRUCTION = re.compile(r"계산하[시여면]오?|구하[시여면]오?|값[은을]\s*구|얼마")
    CALC_EXPRESSION = re.compile(r"[\d]+\s*[+\-×÷*/]\s*[\d]+")
    # '의미', '뜻', '몇 개' 등이 포함되면 연산 수식이 있더라도 개념형으로 유지
    CONCEPT_CONTEXT = re.compile(r"정의|성질|옳은|설명|이유|특징|의미|뜻|몇\s*개|개수")

    db = SyncSessionLocal()
    try:
        questions = db.query(Question).filter(
            Question.is_active == True,  # noqa: E712
        ).all()

        recategorized = 0
        deactivated = 0

        for q in questions:
            content = q.content or ""
            original_cat = q.category

            # 1단계: computation → concept
            if q.category == "computation":
                for pat in COMP_TO_CONCEPT_PATTERNS:
                    if pat.search(content):
                        q.category = "concept"
                        recategorized += 1
                        logger.info(
                            "카테고리 변경 comp→concept: %s | %s",
                            q.id, content[:60],
                        )
                        break

            # 2단계: concept → computation
            elif q.category == "concept":
                if (CALC_INSTRUCTION.search(content)
                        and CALC_EXPRESSION.search(content)
                        and not CONCEPT_CONTEXT.search(content)):
                    q.category = "computation"
                    recategorized += 1
                    logger.info(
                        "카테고리 변경 concept→comp: %s | %s",
                        q.id, content[:60],
                    )

            # 3단계: 재분류 후 연산 품질 검증 (AI 문제만 비활성화)
            if q.category == "computation" and q.id.startswith("ai-"):
                bad_comp = False
                if re.search(r"_{2,}[도를이]|_{2,}\s*(라고?\s*한다|이라)", content):
                    bad_comp = True
                if re.search(r"예\s*/\s*아니오|존재하는가|존재하지\s*않", content):
                    bad_comp = True
                if re.search(r"무엇인가\??$|무엇일까\??$", content.strip()):
                    bad_comp = True
                if bad_comp:
                    q.is_active = False
                    deactivated += 1
                    logger.info(
                        "연산 부적합 AI 문제 비활성화: %s | %s",
                        q.id, content[:60],
                    )

        db.commit()
        if recategorized or deactivated:
            logger.info(
                "카테고리 감사 완료: %d개 재분류, %d개 비활성화",
                recategorized, deactivated,
            )
        else:
            logger.info("카테고리 감사 완료: 변경 없음")
    except Exception as e:
        db.rollback()
        logger.error(f"카테고리 감사 실패: {e}", exc_info=True)
    finally:
        db.close()


def fix_mc_answer_mismatch():
    """객관식 문제의 정답 라벨-해설 불일치를 자동 수정."""
    from app.models.question import Question

    db = SyncSessionLocal()
    try:
        questions = db.query(Question).filter(
            Question.question_type == "multiple_choice",
            Question.options.isnot(None),
            Question.explanation.isnot(None),
        ).all()

        fixed = 0
        for q in questions:
            if not q.options or not q.explanation or not q.correct_answer:
                continue

            correct_label = q.correct_answer.strip().upper()
            label_to_text: dict[str, str] = {}
            for opt in q.options:
                if isinstance(opt, dict):
                    label_to_text[str(opt.get("label", "")).upper()] = str(opt.get("text", ""))

            correct_text = label_to_text.get(correct_label, "")
            if not correct_text:
                continue

            # 해설에서 최종 답 추출
            final_answers = re.findall(
                r"=\s*(\-?[\d,]+(?:\.\d+)?)\s*(개|cm|m|kg|g|원|명|마리|장|번|°)?",
                q.explanation,
            )
            if not final_answers:
                continue

            final_value = final_answers[-1][0].replace(",", "")
            final_unit = final_answers[-1][1]
            final_str = f"{final_value}{final_unit}" if final_unit else final_value

            # 정답 선지에 최종 답이 이미 포함 → OK
            if final_value in correct_text or final_str in correct_text:
                continue

            # 다른 선지에서 매칭되는 것 찾기
            for label, text in label_to_text.items():
                if label != correct_label and (final_value in text or final_str in text):
                    logger.info(
                        "Fix MC answer: Q=%s, %s(%s)→%s(%s), 해설답=%s",
                        q.id, correct_label, correct_text, label, text, final_str,
                    )
                    q.correct_answer = label
                    fixed += 1
                    break

        db.commit()
        if fixed:
            logger.info(f"Fixed {fixed} MC questions with answer-explanation mismatch")
        else:
            logger.info("No MC answer mismatches found")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to fix MC answers: {e}", exc_info=True)
    finally:
        db.close()


def migrate_test_category():
    """기존 일일 테스트의 category 컬럼을 ID에서 파싱하여 채움."""
    from app.models.test import Test

    db = SyncSessionLocal()
    try:
        # category 컬럼 추가 (없으면)
        from sqlalchemy import inspect, text
        inspector = inspect(db.bind)
        columns = [c["name"] for c in inspector.get_columns("tests")]
        if "category" not in columns:
            db.execute(text("ALTER TABLE tests ADD COLUMN category VARCHAR(30)"))
            db.commit()
            logger.info("Added 'category' column to tests table")

        # 일일 테스트: ID에서 category 파싱 (daily-{sid}-{date}-{category})
        daily_tests = db.query(Test).filter(
            Test.id.like("daily-%"),
            Test.category.is_(None),
        ).all()
        updated = 0
        for t in daily_tests:
            parts = t.id.split("-")
            # daily-student-001-2026-02-07-concept → category = 마지막 부분
            if len(parts) >= 5:
                cat = parts[-1]
                if cat in ("concept", "computation", "fill_in_blank"):
                    t.category = cat
                    updated += 1
        db.commit()
        if updated:
            logger.info(f"Migrated category for {updated} daily tests")
        else:
            logger.info("No daily tests needed category migration")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to migrate test category: {e}", exc_info=True)
    finally:
        db.close()


def migrate_chapter_semester_numbering():
    """기존 챕터의 chapter_number와 name을 학기별 번호로 업데이트 (2학기도 1부터 시작)."""
    from app.models.chapter import Chapter

    db = SyncSessionLocal()
    try:
        chapters = db.query(Chapter).order_by(Chapter.grade, Chapter.id).all()

        # 학년별로 그룹화
        grade_chapters: dict[str, list] = {}
        for ch in chapters:
            grade_chapters.setdefault(ch.grade, []).append(ch)

        updated = 0
        for grade_chs in grade_chapters.values():
            # 기존 chapter_number(=전체 순번) 기준 정렬 유지
            grade_chs.sort(key=lambda c: (c.semester, c.id))

            semester_counters: dict[int, int] = {}
            for ch in grade_chs:
                semester_counters[ch.semester] = semester_counters.get(ch.semester, 0) + 1
                new_num = semester_counters[ch.semester]

                # chapter_number 업데이트
                if ch.chapter_number != new_num:
                    ch.chapter_number = new_num
                    updated += 1

                # 단원명 업데이트: "7. 기본 도형과 작도" → "1. 기본 도형과 작도"
                clean_name = re.sub(r'^\d+\.\s*', '', ch.name)
                new_name = f"{new_num}. {clean_name}"
                if ch.name != new_name:
                    ch.name = new_name
                    updated += 1

        db.commit()
        if updated:
            logger.info(f"Chapter semester numbering migration: {updated} field updates")
        else:
            logger.info("Chapter semester numbering already up to date")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to migrate chapter numbering: {e}", exc_info=True)
    finally:
        db.close()


def _cleanup_today_daily_tests(db):
    """오늘의 0문제/미완료 일일 테스트 정리. 완료된 테스트는 보존."""
    from app.models.daily_test_record import DailyTestRecord
    from app.models.test import Test
    from app.models.test_attempt import TestAttempt
    from app.models.answer_log import AnswerLog

    # The following lines appear to be misplaced router registrations.
    # They are syntactically incorrect as import statements and
    # would cause runtime errors if 'app' and 'settings' are not defined.
    # To maintain syntactic correctness as per instructions, these lines are commented out.
    # If these are meant to be router registrations, they should be placed in the main application file.
    # from    app.include_router(stats.router, prefix=settings.API_V1_STR)
    # from app.api.v1 import missions
    # app.include_router(missions.router, prefix=settings.API_V1_STR)

    # return app.models.answer_log import AnswerLog # This line is also syntactically incorrect.

    KST = timezone(timedelta(hours=9))
    today = datetime.now(KST).date().isoformat()
    # 0문제이거나 아직 시작 안 한 테스트만 정리 (완료된 것은 보존)
    records = db.query(DailyTestRecord).filter(
        DailyTestRecord.date == today,
        DailyTestRecord.status != "completed",
    ).all()
    if not records:
        return

    for record in records:
        test_id = record.test_id
        attempt_id = record.attempt_id
        # 1. DailyTestRecord 먼저 삭제 (test_id, attempt_id FK 해소)
        db.delete(record)
        db.flush()
        # 2. AnswerLog 삭제 (attempt_id FK 해소)
        if attempt_id:
            db.query(AnswerLog).filter(AnswerLog.attempt_id == attempt_id).delete()
        # 3. TestAttempt 삭제
        if attempt_id:
            db.query(TestAttempt).filter(TestAttempt.id == attempt_id).delete()
        # 4. Test 삭제
        if test_id:
            db.query(Test).filter(Test.id == test_id).delete()

    logger.info(f"Cleaned up {len(records)} daily test records for today ({today})")


def migrate_concept_subdivision():
    """개념 세분화 마이그레이션: 기존 단일 개념 ID → 세분화 ID 전환.

    서버 시작 시 자동 실행. 이미 마이그레이션된 경우 건너뜀.
    구 개념 ID가 DB에 존재하면 마이그레이션 수행:
    1. 시드 데이터에서 신규 개념 레코드 생성
    2. 문제(questions) concept_id 업데이트
    3. 숙련도(concept_mastery) 이전
    4. 선수관계(concept_prerequisites) 업데이트
    5. 테스트(tests) concept_ids JSON 업데이트
    6. 문제 prerequisite_concept_ids JSON 업데이트
    7. 구 개념 레코드 삭제
    """
    from app.models.concept import Concept, concept_prerequisites
    from app.models.question import Question
    from app.models.concept_mastery import ConceptMastery
    from app.models.test import Test

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 구 개념 ID → 신규 세분화 개념 ID 매핑
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    OLD_TO_NEW: dict[str, list[str]] = {
        # ── 초3 ──
        "concept-e3-add-sub": ["concept-e3-add-sub-01", "concept-e3-add-sub-02"],
        "concept-e3-plane": ["concept-e3-plane-01", "concept-e3-plane-02"],
        "concept-e3-div1": ["concept-e3-div1-01", "concept-e3-div1-02"],
        "concept-e3-mul1": ["concept-e3-mul1-01", "concept-e3-mul1-02"],
        "concept-e3-length-time": ["concept-e3-length-time-01", "concept-e3-length-time-02"],
        "concept-e3-frac-dec": ["concept-e3-frac-dec-01", "concept-e3-frac-dec-02"],
        "concept-e3-mul2": ["concept-e3-mul2-01", "concept-e3-mul2-02"],
        "concept-e3-div2": ["concept-e3-div2-01", "concept-e3-div2-02"],
        "concept-e3-circle": ["concept-e3-circle-01", "concept-e3-circle-02"],
        "concept-e3-frac2": ["concept-e3-frac2-01", "concept-e3-frac2-02"],
        "concept-e3-volume-weight": ["concept-e3-vol-wt-01", "concept-e3-vol-wt-02"],
        "concept-e3-data": ["concept-e3-data-01", "concept-e3-data-02"],
        # ── 초4 ──
        "concept-e4-big-num": ["concept-e4-big-num-01", "concept-e4-big-num-02"],
        "concept-e4-angle": ["concept-e4-angle-01", "concept-e4-angle-02"],
        "concept-e4-mul-div": ["concept-e4-mul-div-01", "concept-e4-mul-div-02"],
        "concept-e4-transform": ["concept-e4-transform-01", "concept-e4-transform-02"],
        "concept-e4-bar-graph": ["concept-e4-bar-graph-01", "concept-e4-bar-graph-02"],
        "concept-e4-pattern": ["concept-e4-pattern-01", "concept-e4-pattern-02"],
        "concept-e4-frac-op": ["concept-e4-frac-op-01", "concept-e4-frac-op-02"],
        "concept-e4-triangle": ["concept-e4-triangle-01", "concept-e4-triangle-02"],
        "concept-e4-dec-op": ["concept-e4-dec-op-01", "concept-e4-dec-op-02"],
        "concept-e4-quad": ["concept-e4-quad-01", "concept-e4-quad-02"],
        "concept-e4-line-graph": ["concept-e4-line-graph-01", "concept-e4-line-graph-02"],
        "concept-e4-polygon": ["concept-e4-polygon-01", "concept-e4-polygon-02"],
        # ── 초5 ──
        "concept-e5-mixed-calc": ["concept-e5-mixed-calc-01", "concept-e5-mixed-calc-02"],
        "concept-e5-divisor": ["concept-e5-divisor-01", "concept-e5-divisor-02"],
        "concept-e5-correspondence": ["concept-e5-corresp-01", "concept-e5-corresp-02"],
        "concept-e5-reduce": ["concept-e5-reduce-01", "concept-e5-reduce-02"],
        "concept-e5-frac-add": ["concept-e5-frac-add-01", "concept-e5-frac-add-02"],
        "concept-e5-polygon-area": ["concept-e5-poly-area-01", "concept-e5-poly-area-02"],
        "concept-e5-range-rounding": ["concept-e5-range-01", "concept-e5-round-01"],
        "concept-e5-frac-mul": ["concept-e5-frac-mul-01", "concept-e5-frac-mul-02"],
        "concept-e5-congruence": ["concept-e5-congru-01", "concept-e5-congru-02"],
        "concept-e5-dec-mul": ["concept-e5-dec-mul-01", "concept-e5-dec-mul-02"],
        "concept-e5-cuboid": ["concept-e5-cuboid-01", "concept-e5-cuboid-02"],
        "concept-e5-average": ["concept-e5-avg-01", "concept-e5-avg-02"],
        # ── 중1 (초기 시드 구 ID) ──
        "concept-001": ["concept-m1-eq-01"],        # 일차방정식 → 일차방정식 기초
        "concept-002": ["concept-m1-int-01"],        # 사칙연산 → 정수의 사칙연산
        "concept-003": ["concept-m1-expr-01"],       # 일차부등식 → 문자와 식 기초
        "concept-004": ["concept-m1-coord-01"],      # 좌표와 그래프 → 좌표 기초
        "concept-005": ["concept-m1-freq-01"],       # 통계 → 도수분포 기초
        # ── 중1 ──
        "concept-m1-prime": ["concept-m1-prime-01", "concept-m1-prime-02", "concept-m1-prime-03"],
        "concept-m1-integer": ["concept-m1-int-01", "concept-m1-int-02", "concept-m1-int-03"],
        "concept-m1-expression": ["concept-m1-expr-01", "concept-m1-expr-02", "concept-m1-expr-03"],
        "concept-m1-equation": ["concept-m1-eq-01", "concept-m1-eq-02", "concept-m1-eq-03"],
        "concept-m1-coord": ["concept-m1-coord-01", "concept-m1-coord-02"],
        "concept-m1-proportion": ["concept-m1-prop-01", "concept-m1-prop-02", "concept-m1-prop-03"],
        "concept-m1-basic-geo": ["concept-m1-geo-01", "concept-m1-geo-02", "concept-m1-geo-03"],
        "concept-m1-plane-fig": ["concept-m1-plane-01", "concept-m1-plane-02"],
        "concept-m1-solid-fig": ["concept-m1-solid-01", "concept-m1-solid-02", "concept-m1-solid-03"],
        "concept-m1-frequency": ["concept-m1-freq-01", "concept-m1-freq-02", "concept-m1-freq-03"],
        "concept-m1-representative": ["concept-m1-repr-01", "concept-m1-repr-02"],
        "concept-m1-scatter": ["concept-m1-scat-01", "concept-m1-scat-02"],
        # ── 중2 ──
        "concept-m2-rational": ["concept-m2-rational-01", "concept-m2-rational-02"],
        "concept-m2-expression": ["concept-m2-expr-01", "concept-m2-expr-02"],
        "concept-m2-inequality": ["concept-m2-ineq-01", "concept-m2-ineq-02"],
        "concept-m2-simultaneous": ["concept-m2-simul-01", "concept-m2-simul-02"],
        "concept-m2-linear-func": ["concept-m2-linfn-01", "concept-m2-linfn-02"],
        "concept-m2-triangle": ["concept-m2-tri-01", "concept-m2-tri-02"],
        "concept-m2-quadrilateral": ["concept-m2-quad-01", "concept-m2-quad-02"],
        "concept-m2-similarity": ["concept-m2-simil-01", "concept-m2-simil-02"],
        "concept-m2-pythagoras": ["concept-m2-pytha-01", "concept-m2-pytha-02"],
        "concept-m2-probability": ["concept-m2-prob-01", "concept-m2-prob-02"],
        # ── 중3 ──
        "concept-m3-real-num": ["concept-m3-sqrt-01", "concept-m3-sqrt-02", "concept-m3-sqrt-03"],
        "concept-m3-factoring": ["concept-m3-factor-01", "concept-m3-factor-02", "concept-m3-factor-03"],
        "concept-m3-quad-eq": ["concept-m3-quadeq-01", "concept-m3-quadeq-02", "concept-m3-quadeq-03"],
        "concept-m3-quad-func": ["concept-m3-quadfn-01", "concept-m3-quadfn-02", "concept-m3-quadfn-03"],
        "concept-m3-trig": ["concept-m3-trig-01", "concept-m3-trig-02"],
        "concept-m3-circle": ["concept-m3-circle-01", "concept-m3-circle-02", "concept-m3-circle-03"],
        "concept-m3-statistics": ["concept-m3-stat-01", "concept-m3-stat-02", "concept-m3-stat-03"],
        # ── 고1 공통수학1 ──
        "concept-h1-polynomial": ["concept-h1-polynomial-01", "concept-h1-polynomial-02"],
        "concept-h1-equation": ["concept-h1-equation-01", "concept-h1-equation-02"],
        "concept-h1-counting": ["concept-h1-counting-01", "concept-h1-counting-02"],
        "concept-h1-matrix": ["concept-h1-matrix-01", "concept-h1-matrix-02"],
    }

    all_old_ids = set(OLD_TO_NEW.keys())

    db = SyncSessionLocal()
    try:
        # 마이그레이션 필요 여부 확인
        old_concept = db.query(Concept).filter(
            Concept.id.in_(all_old_ids)
        ).first()
        if not old_concept:
            logger.info("개념 세분화 마이그레이션 불필요 (이미 완료)")
            return

        logger.info(f"개념 세분화 마이그레이션 시작 (구 개념 {len(all_old_ids)}개 → 세분화)")

        # ── 1단계: 시드 데이터에서 신규 개념 레코드 생성 ──
        from app.seeds import get_all_grade_seed_data
        seed_data = get_all_grade_seed_data()

        all_new_ids = set()
        for new_ids in OLD_TO_NEW.values():
            all_new_ids.update(new_ids)

        existing_concept_ids = {c.id for c in db.query(Concept.id).all()}
        seed_concept_map = {c["id"]: c for c in seed_data["concepts"]}

        concepts_created = 0
        for concept_id in sorted(all_new_ids):
            if concept_id not in existing_concept_ids and concept_id in seed_concept_map:
                c = seed_concept_map[concept_id]
                db.add(Concept(
                    id=c["id"], name=c["name"], grade=c["grade"],
                    category=c["category"], part=c["part"],
                    description=c.get("description", ""),
                    parent_id=c.get("parent_id"),
                ))
                concepts_created += 1
        db.flush()
        logger.info(f"  [1/7] 신규 개념 {concepts_created}개 생성")

        # ── 2단계: 문제 concept_id 업데이트 ──
        # 시드 문제: 시드 데이터의 정확한 매핑 사용
        # AI 생성 문제: 기본값 -01 (기초 하위 개념) 배정
        seed_question_concept = {q["id"]: q["concept_id"] for q in seed_data["questions"]}

        questions_from_seed = 0
        questions_ai = 0
        for q in db.query(Question).filter(
            Question.concept_id.in_(all_old_ids)
        ).all():
            if q.id in seed_question_concept:
                q.concept_id = seed_question_concept[q.id]
                questions_from_seed += 1
            else:
                q.concept_id = OLD_TO_NEW[q.concept_id][0]
                questions_ai += 1
        db.flush()
        logger.info(f"  [2/7] 문제 concept_id 업데이트: 시드 {questions_from_seed}개, AI생성 {questions_ai}개")

        # ── 3단계: concept_mastery 이전 (-01로 이전, 중복 시 삭제) ──
        mastery_migrated = 0
        mastery_deleted = 0
        for m in db.query(ConceptMastery).filter(
            ConceptMastery.concept_id.in_(all_old_ids)
        ).all():
            new_id = OLD_TO_NEW[m.concept_id][0]
            existing = db.query(ConceptMastery).filter(
                ConceptMastery.student_id == m.student_id,
                ConceptMastery.concept_id == new_id,
            ).first()
            if existing:
                db.delete(m)
                mastery_deleted += 1
            else:
                m.concept_id = new_id
                mastery_migrated += 1
        db.flush()
        logger.info(f"  [3/7] concept_mastery: {mastery_migrated}개 이전, {mastery_deleted}개 중복 삭제")

        # ── 4단계: concept_prerequisites 업데이트 ──
        prereq_rows = db.execute(
            concept_prerequisites.select().where(
                concept_prerequisites.c.concept_id.in_(all_old_ids)
                | concept_prerequisites.c.prerequisite_id.in_(all_old_ids)
            )
        ).fetchall()

        if prereq_rows:
            # 기존 행 삭제
            db.execute(
                concept_prerequisites.delete().where(
                    concept_prerequisites.c.concept_id.in_(all_old_ids)
                    | concept_prerequisites.c.prerequisite_id.in_(all_old_ids)
                )
            )
            # 신규 조합 삽입
            new_pairs = set()
            for row in prereq_rows:
                old_cid, old_pid = row[0], row[1]
                new_cids = OLD_TO_NEW.get(old_cid, [old_cid])
                new_pids = OLD_TO_NEW.get(old_pid, [old_pid])
                for nc in new_cids:
                    for np in new_pids:
                        if nc != np:
                            new_pairs.add((nc, np))

            # 기존에 있는 쌍 제외
            existing_pairs = {
                (r[0], r[1]) for r in db.execute(concept_prerequisites.select()).fetchall()
            }
            insert_pairs = new_pairs - existing_pairs
            for nc, np in insert_pairs:
                db.execute(concept_prerequisites.insert().values(
                    concept_id=nc, prerequisite_id=np
                ))
            db.flush()
            logger.info(f"  [4/7] concept_prerequisites: {len(prereq_rows)}개 → {len(insert_pairs)}개 재생성")
        else:
            logger.info("  [4/7] concept_prerequisites: 변경 대상 없음")

        # ── 5단계: tests concept_ids JSON 업데이트 ──
        tests_updated = 0
        for t in db.query(Test).all():
            if not t.concept_ids:
                continue
            new_ids = []
            changed = False
            for cid in t.concept_ids:
                if cid in OLD_TO_NEW:
                    new_ids.extend(OLD_TO_NEW[cid])
                    changed = True
                else:
                    new_ids.append(cid)
            if changed:
                t.concept_ids = new_ids
                tests_updated += 1
        db.flush()
        logger.info(f"  [5/7] tests concept_ids: {tests_updated}개 업데이트")

        # ── 6단계: questions prerequisite_concept_ids JSON 업데이트 ──
        prereq_q_updated = 0
        for q in db.query(Question).filter(
            Question.prerequisite_concept_ids.isnot(None)
        ).all():
            if not q.prerequisite_concept_ids:
                continue
            new_ids = []
            changed = False
            for cid in q.prerequisite_concept_ids:
                if cid in OLD_TO_NEW:
                    new_ids.extend(OLD_TO_NEW[cid])
                    changed = True
                else:
                    new_ids.append(cid)
            if changed:
                q.prerequisite_concept_ids = new_ids
                prereq_q_updated += 1
        db.flush()
        logger.info(f"  [6/7] questions prerequisite_concept_ids: {prereq_q_updated}개 업데이트")

        # ── 7단계: 구 개념 레코드 삭제 ──
        deleted = db.query(Concept).filter(
            Concept.id.in_(all_old_ids)
        ).delete(synchronize_session="fetch")

        db.commit()
        logger.info(f"  [7/7] 구 개념 {deleted}개 삭제")
        logger.info("개념 세분화 마이그레이션 완료!")

    except Exception as e:
        db.rollback()
        logger.error(f"개념 세분화 마이그레이션 실패: {e}", exc_info=True)
    finally:
        db.close()


def migrate_concept_sequential_unlock():
    """기존 학생의 개념 순차 해금 마이그레이션.

    해금된 챕터가 있지만 ConceptMastery 레코드가 없거나 is_unlocked=False인 학생 처리:
    - mastery_percentage > 0인 개념 → is_unlocked = True
    - 해금된 챕터의 첫 개념 → is_unlocked = True
    - 완료된 챕터의 모든 개념 → is_unlocked = True
    """
    from app.models.chapter import Chapter
    from app.models.chapter_progress import ChapterProgress
    from app.models.concept_mastery import ConceptMastery
    from app.models.user import User

    db = SyncSessionLocal()
    try:
        students = db.query(User).filter(User.role == "student").all()
        if not students:
            return

        migrated_count = 0
        for student in students:
            student_id = student.id

            # 해금된 챕터 조회
            progresses = db.query(ChapterProgress).filter(
                ChapterProgress.student_id == student_id,
                ChapterProgress.is_unlocked == True,  # noqa: E712
            ).all()

            if not progresses:
                continue

            now = datetime.now(timezone.utc)
            changed = False

            for progress in progresses:
                chapter = db.query(Chapter).get(progress.chapter_id)
                if not chapter or not chapter.concept_ids:
                    continue

                if progress.is_completed:
                    # 완료된 챕터: 모든 개념 해금
                    for concept_id in chapter.concept_ids:
                        mastery = db.query(ConceptMastery).filter(
                            ConceptMastery.student_id == student_id,
                            ConceptMastery.concept_id == concept_id,
                        ).first()
                        if mastery and not mastery.is_unlocked:
                            mastery.is_unlocked = True
                            mastery.unlocked_at = now
                            changed = True
                        elif not mastery:
                            mastery = ConceptMastery(
                                student_id=student_id,
                                concept_id=concept_id,
                                is_unlocked=True,
                                unlocked_at=now,
                            )
                            db.add(mastery)
                            changed = True
                else:
                    # 미완료 해금 챕터: mastery > 0인 개념 해금 + 첫 개념 해금
                    first_concept_id = chapter.concept_ids[0]

                    for concept_id in chapter.concept_ids:
                        mastery = db.query(ConceptMastery).filter(
                            ConceptMastery.student_id == student_id,
                            ConceptMastery.concept_id == concept_id,
                        ).first()

                        should_unlock = (
                            concept_id == first_concept_id
                            or (mastery and mastery.mastery_percentage > 0)
                        )

                        if mastery and not mastery.is_unlocked and should_unlock:
                            mastery.is_unlocked = True
                            mastery.unlocked_at = now
                            changed = True
                        elif not mastery and should_unlock:
                            mastery = ConceptMastery(
                                student_id=student_id,
                                concept_id=concept_id,
                                is_unlocked=True,
                                unlocked_at=now,
                            )
                            db.add(mastery)
                            changed = True

                    # mastery > 0인 개념들의 다음 개념도 해금 (연쇄)
                    for i, concept_id in enumerate(chapter.concept_ids[:-1]):
                        m = db.query(ConceptMastery).filter(
                            ConceptMastery.student_id == student_id,
                            ConceptMastery.concept_id == concept_id,
                        ).first()
                        if m and m.mastery_percentage > 0:
                            next_cid = chapter.concept_ids[i + 1]
                            next_m = db.query(ConceptMastery).filter(
                                ConceptMastery.student_id == student_id,
                                ConceptMastery.concept_id == next_cid,
                            ).first()
                            if next_m and not next_m.is_unlocked:
                                next_m.is_unlocked = True
                                next_m.unlocked_at = now
                                changed = True
                            elif not next_m:
                                next_m = ConceptMastery(
                                    student_id=student_id,
                                    concept_id=next_cid,
                                    is_unlocked=True,
                                    unlocked_at=now,
                                )
                                db.add(next_m)
                                changed = True

            if changed:
                migrated_count += 1

        if migrated_count > 0:
            db.commit()
            logger.info(f"개념 순차 해금 마이그레이션: {migrated_count}명 학생 처리 완료")
        else:
            logger.info("개념 순차 해금 마이그레이션: 변경 없음")

    except Exception as e:
        db.rollback()
        logger.error(f"개념 순차 해금 마이그레이션 실패: {e}", exc_info=True)
    finally:
        db.close()


def cleanup_bad_ai_questions():
    """AI가 생성한 불량 문제(참조형 빈칸, 외부 참조 등)를 비활성화."""
    import re as _re
    from app.models.question import Question
    db = SyncSessionLocal()
    try:
        # 먼저, 이전 과도한 패턴('다음 중')으로 잘못 비활성화된 문제 복구
        wrongly_deactivated = db.query(Question).filter(
            Question.is_active == False,  # noqa: E712
            Question.id.like("ai-%"),
        ).all()
        reactivated = 0
        for q in wrongly_deactivated:
            content = q.content or ""
            # 실제 불량 기준에 해당하지 않으면 복구
            is_actually_bad = False
            if _re.search(r"\([ㄱㄴㄷㄹㅁ가나다라]\)", content):
                is_actually_bad = True
            if _re.search(r"다음[은의]\s*(표|식|그림|과정)", content):
                is_actually_bad = True
            if q.question_type == "fill_in_blank" and _re.search(r"고르[시면]|선택|모두 고르", content):
                is_actually_bad = True
            if not is_actually_bad:
                q.is_active = True
                reactivated += 1
        if reactivated:
            db.commit()
            logger.info(f"잘못 비활성화된 AI 문제 {reactivated}개 복구")

        questions = db.query(Question).filter(
            Question.is_active == True,  # noqa: E712
            Question.id.like("ai-%"),
        ).all()

        deactivated = 0
        for q in questions:
            content = q.content or ""
            bad = False
            # (가)/(나) 등 참조형 기호
            if _re.search(r"\([ㄱㄴㄷㄹㅁ가나다라]\)", content):
                bad = True
            # '다음은...과정이다' 외부 참조 (단, '다음 중'은 일반 표현이므로 제외)
            if _re.search(r"다음[은의]\s*(표|식|그림|과정)", content):
                bad = True
            # 빈칸인데 선택형 표현
            if q.question_type == "fill_in_blank":
                if _re.search(r"고르[시면]|선택|모두 고르", content):
                    bad = True
            if bad:
                q.is_active = False
                deactivated += 1
                logger.info(f"불량 AI 문제 비활성화: {q.id} | {content[:60]}")

        if deactivated:
            db.commit()
            logger.info(f"불량 AI 문제 {deactivated}개 비활성화 완료")
        else:
            logger.info("불량 AI 문제 없음 (정리 불필요)")
    except Exception as e:
        db.rollback()
        logger.error(f"불량 AI 문제 정리 실패: {e}", exc_info=True)
    finally:
        db.close()


def migrate_wrong_answer_reviews():
    """기존 AnswerLog에서 오답 기록을 WrongAnswerReview로 이관.

    - 틀린 적 있고, 한 번도 맞추지 못한 (student_id, question_id) 쌍을 찾아
      WrongAnswerReview에 stage=1, next_review_date=오늘로 등록.
    - 이미 데이터가 있으면 스킵 (멱등).
    """
    from datetime import date
    from sqlalchemy import text
    from app.models.wrong_answer_review import WrongAnswerReview

    db = SyncSessionLocal()
    try:
        # 이미 마이그레이션 되었으면 스킵
        existing = db.query(WrongAnswerReview).first()
        if existing:
            return

        # 틀린 적 있고 아직 맞추지 못한 (student_id, question_id) 쌍
        wrong_pairs = db.execute(text("""
            SELECT al.question_id, ta.student_id,
                   COUNT(*) as wrong_cnt,
                   MAX(al.created_at) as last_wrong
            FROM answer_logs al
            JOIN test_attempts ta ON al.attempt_id = ta.id
            WHERE al.is_correct = FALSE
            AND NOT EXISTS (
                SELECT 1 FROM answer_logs al2
                JOIN test_attempts ta2 ON al2.attempt_id = ta2.id
                WHERE al2.question_id = al.question_id
                AND ta2.student_id = ta.student_id
                AND al2.is_correct = TRUE
            )
            GROUP BY al.question_id, ta.student_id
        """)).all()

        if not wrong_pairs:
            logger.info("오답 복습 마이그레이션: 대상 없음")
            return

        today = date.today().isoformat()
        count = 0
        for row in wrong_pairs:
            review = WrongAnswerReview(
                student_id=row.student_id,
                question_id=row.question_id,
                review_stage=1,
                next_review_date=today,
                wrong_count=row.wrong_cnt,
                last_wrong_at=row.last_wrong,
            )
            db.add(review)
            count += 1

        db.commit()
        logger.info(f"오답 복습 마이그레이션 완료: {count}건")
    except Exception as e:
        db.rollback()
        logger.error(f"오답 복습 마이그레이션 실패: {e}", exc_info=True)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup - 동기 DB 초기화를 스레드풀에서 실행 (이벤트 루프 블로킹 방지)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, init_db)
    await loop.run_in_executor(None, load_seed_data)
    await loop.run_in_executor(None, migrate_concept_subdivision)
    await loop.run_in_executor(None, update_chapter_concept_ids)
    await loop.run_in_executor(None, migrate_chapter_semester_numbering)
    await loop.run_in_executor(None, migrate_test_category)
    await loop.run_in_executor(None, fix_mc_answer_mismatch)
    await loop.run_in_executor(None, audit_question_categories)
    await loop.run_in_executor(None, migrate_concept_sequential_unlock)
    await loop.run_in_executor(None, cleanup_bad_ai_questions)
    await loop.run_in_executor(None, migrate_wrong_answer_reviews)
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
