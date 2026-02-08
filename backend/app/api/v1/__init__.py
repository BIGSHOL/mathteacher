# API v1 module

from fastapi import APIRouter

from .auth import router as auth_router
from .students import router as students_router
from .tests import router as tests_router
from .stats import router as stats_router
from .questions import router as questions_router
from .classes import router as classes_router
from .chapters import router as chapters_router
from .practice import router as practice_router
from .ai_assist import router as ai_assist_router
from .daily_tests import router as daily_tests_router
from .admin import router as admin_router
from .question_reports import router as question_reports_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(students_router)
api_router.include_router(tests_router)
api_router.include_router(stats_router)
api_router.include_router(questions_router)
api_router.include_router(classes_router)
api_router.include_router(chapters_router, prefix="/chapters", tags=["chapters"])
api_router.include_router(practice_router)
api_router.include_router(ai_assist_router)
api_router.include_router(daily_tests_router)
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(question_reports_router)

from .assignments import router as assignments_router
api_router.include_router(assignments_router)

from .missions import router as missions_router
api_router.include_router(missions_router)

from .shop import router as shop_router
api_router.include_router(shop_router)

from .ai_learning import router as ai_learning_router
api_router.include_router(ai_learning_router)
