import logging
from contextlib import asynccontextmanager

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
    from app.models import User, Class, Concept, Question, Test, TestAttempt, AnswerLog
    from app.models.user import RefreshToken
    from app.services.auth_service import AuthService

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Seed initial data if database is empty
    db = SessionLocal()
    try:
        if not db.query(User).first():
            auth_service = AuthService(db)

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

            # Create class
            test_class = Class(
                id="class-001",
                name="테스트반",
                teacher_id="teacher-001",
                grade="middle_1",
            )
            db.add(test_class)

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
                description="일차방정식의 풀이",
            )
            db.add(concept)

            # Create questions
            questions = [
                Question(
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
                ),
                Question(
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
                ),
                Question(
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
                ),
            ]
            for q in questions:
                db.add(q)

            # Create test
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
            print("Database seeded with initial data")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    init_db()
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


# Exception handler for debugging
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


# API v1 Router
from app.api.v1 import api_router

app.include_router(api_router)
