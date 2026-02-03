# API v1 module

from fastapi import APIRouter

from .auth import router as auth_router
from .students import router as students_router
from .tests import router as tests_router
from .stats import router as stats_router
from .questions import router as questions_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(students_router)
api_router.include_router(tests_router)
api_router.include_router(stats_router)
api_router.include_router(questions_router)
