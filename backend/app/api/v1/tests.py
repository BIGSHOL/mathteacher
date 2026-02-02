"""테스트 API 엔드포인트."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.question import Question
from app.schemas import (
    ApiResponse,
    AvailableTestResponse,
    CompleteTestResponse,
    GetAttemptResponse,
    Grade,
    PaginatedResponse,
    QuestionResponse,
    StartTestResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
    TestAttemptResponse,
    TestResponse,
    TestWithQuestionsResponse,
    UserResponse,
    AnswerLogResponse,
)
from app.schemas.common import UserRole
from app.services.test_service import TestService
from app.services.grading_service import GradingService
from app.services.gamification_service import GamificationService
from app.api.v1.auth import get_current_user, require_role

router = APIRouter(prefix="/tests", tags=["tests"])


def get_test_service(db: Session = Depends(get_db)) -> TestService:
    """테스트 서비스 의존성."""
    return TestService(db)


def get_grading_service(db: Session = Depends(get_db)) -> GradingService:
    """채점 서비스 의존성."""
    return GradingService(db)


def get_gamification_service(db: Session = Depends(get_db)) -> GamificationService:
    """게이미피케이션 서비스 의존성."""
    return GamificationService(db)


@router.get("/available", response_model=ApiResponse[PaginatedResponse[AvailableTestResponse]])
async def get_available_tests(
    grade: Grade | None = Query(None, description="학년 필터"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(10, ge=1, le=50, description="페이지 크기"),
    current_user: UserResponse = Depends(get_current_user),
    test_service: TestService = Depends(get_test_service),
):
    """풀 수 있는 테스트 목록 조회."""
    results, total = test_service.get_available_tests(
        student_id=current_user.id,
        grade=grade,
        page=page,
        page_size=page_size,
    )

    total_pages = (total + page_size - 1) // page_size

    items = []
    for r in results:
        test = r["test"]
        items.append(
            AvailableTestResponse(
                id=test.id,
                title=test.title,
                description=test.description,
                grade=test.grade,
                concept_ids=test.concept_ids,
                question_count=test.question_count,
                time_limit_minutes=test.time_limit_minutes,
                is_active=test.is_active,
                created_at=test.created_at,
                is_completed=r["is_completed"],
                best_score=r["best_score"],
                attempt_count=r["attempt_count"],
            )
        )

    return ApiResponse(
        data=PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
    )


@router.get("/{test_id}", response_model=ApiResponse[TestWithQuestionsResponse])
async def get_test_detail(
    test_id: str,
    current_user: UserResponse = Depends(get_current_user),
    test_service: TestService = Depends(get_test_service),
):
    """테스트 상세 조회 (문제 포함, 정답 제외)."""
    result = test_service.get_test_with_questions(test_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "테스트를 찾을 수 없습니다.",
                },
            },
        )

    test = result["test"]
    questions = result["questions"]

    # 정답 제외한 문제 목록
    question_responses = [
        QuestionResponse(
            id=q.id,
            concept_id=q.concept_id,
            question_type=q.question_type,
            difficulty=q.difficulty,
            content=q.content,
            options=q.options,
            explanation="",  # 채점 전에는 해설 숨김
            points=q.points,
        )
        for q in questions
    ]

    return ApiResponse(
        data=TestWithQuestionsResponse(
            id=test.id,
            title=test.title,
            description=test.description,
            grade=test.grade,
            concept_ids=test.concept_ids,
            question_count=test.question_count,
            time_limit_minutes=test.time_limit_minutes,
            is_active=test.is_active,
            created_at=test.created_at,
            questions=question_responses,
        )
    )


@router.post(
    "/{test_id}/start",
    response_model=ApiResponse[StartTestResponse],
    status_code=status.HTTP_201_CREATED,
)
async def start_test(
    test_id: str,
    current_user: UserResponse = Depends(get_current_user),
    test_service: TestService = Depends(get_test_service),
):
    """테스트 시작."""
    # 테스트 존재 확인
    result = test_service.get_test_with_questions(test_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "테스트를 찾을 수 없습니다.",
                },
            },
        )

    # 시도 생성
    attempt = test_service.start_test(test_id, current_user.id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "테스트 시작에 실패했습니다.",
                },
            },
        )

    test = result["test"]
    questions = result["questions"]

    # 정답 제외한 문제 목록
    question_responses = [
        QuestionResponse(
            id=q.id,
            concept_id=q.concept_id,
            question_type=q.question_type,
            difficulty=q.difficulty,
            content=q.content,
            options=q.options,
            explanation="",
            points=q.points,
        )
        for q in questions
    ]

    return ApiResponse(
        data=StartTestResponse(
            attempt_id=attempt.id,
            test=TestWithQuestionsResponse(
                id=test.id,
                title=test.title,
                description=test.description,
                grade=test.grade,
                concept_ids=test.concept_ids,
                question_count=test.question_count,
                time_limit_minutes=test.time_limit_minutes,
                is_active=test.is_active,
                created_at=test.created_at,
                questions=question_responses,
            ),
            started_at=attempt.started_at,
        )
    )


@router.post(
    "/attempts/{attempt_id}/submit",
    response_model=ApiResponse[SubmitAnswerResponse],
)
async def submit_answer(
    attempt_id: str,
    request: SubmitAnswerRequest,
    current_user: UserResponse = Depends(get_current_user),
    test_service: TestService = Depends(get_test_service),
    grading_service: GradingService = Depends(get_grading_service),
    db: Session = Depends(get_db),
):
    """답안 제출 (즉시 채점)."""
    # 시도 확인
    attempt = test_service.get_attempt_by_id(attempt_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "시도를 찾을 수 없습니다.",
                },
            },
        )

    # 본인 시도인지 확인
    if attempt.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "error": {
                    "code": "FORBIDDEN",
                    "message": "접근 권한이 없습니다.",
                },
            },
        )

    # 이미 완료된 시도인지 확인
    if attempt.completed_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "ALREADY_COMPLETED",
                    "message": "이미 완료된 테스트입니다.",
                },
            },
        )

    # 이미 답안을 제출했는지 확인
    if test_service.check_already_answered(attempt_id, request.question_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "ALREADY_SUBMITTED",
                    "message": "이미 답안을 제출한 문제입니다.",
                },
            },
        )

    # 문제 조회
    question = db.get(Question, request.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "문제를 찾을 수 없습니다.",
                },
            },
        )

    # 현재 콤보
    current_combo = test_service.get_current_combo(attempt_id)

    # 채점
    result = grading_service.submit_answer(
        attempt=attempt,
        question=question,
        selected_answer=request.selected_answer,
        time_spent_seconds=request.time_spent_seconds,
        current_combo=current_combo,
    )

    return ApiResponse(data=SubmitAnswerResponse(**result))


@router.post(
    "/attempts/{attempt_id}/complete",
    response_model=ApiResponse[CompleteTestResponse],
)
async def complete_test(
    attempt_id: str,
    current_user: UserResponse = Depends(get_current_user),
    test_service: TestService = Depends(get_test_service),
    gamification_service: GamificationService = Depends(get_gamification_service),
    db: Session = Depends(get_db),
):
    """테스트 완료."""
    # 시도 확인
    attempt = test_service.get_attempt_by_id(attempt_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "시도를 찾을 수 없습니다.",
                },
            },
        )

    # 본인 시도인지 확인
    if attempt.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "error": {
                    "code": "FORBIDDEN",
                    "message": "접근 권한이 없습니다.",
                },
            },
        )

    # 이미 완료된 시도인지 확인
    if attempt.completed_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "ALREADY_COMPLETED",
                    "message": "이미 완료된 테스트입니다.",
                },
            },
        )

    # 시도 완료
    completed_attempt = test_service.complete_attempt(attempt_id)

    # 사용자 게이미피케이션 업데이트
    from app.models.user import User
    user = db.get(User, current_user.id)
    today = datetime.now(timezone.utc).date().isoformat()
    gamification_result = gamification_service.update_user_gamification(
        user=user,
        xp_earned=completed_attempt.xp_earned,
        today=today,
    )

    # 답안 기록 조회
    details = test_service.get_attempt_with_details(attempt_id)
    answer_logs = details["answer_logs"] if details else []

    return ApiResponse(
        data=CompleteTestResponse(
            attempt=TestAttemptResponse.model_validate(completed_attempt),
            answers=[AnswerLogResponse.model_validate(log) for log in answer_logs],
            level_up=gamification_result["level_up"],
            new_level=gamification_result["new_level"],
            xp_earned=completed_attempt.xp_earned,
            achievements_earned=[],  # TODO: 업적 시스템 구현
        )
    )


@router.get("/attempts/{attempt_id}", response_model=ApiResponse[GetAttemptResponse])
async def get_attempt(
    attempt_id: str,
    current_user: UserResponse = Depends(get_current_user),
    test_service: TestService = Depends(get_test_service),
):
    """시도 결과 조회."""
    details = test_service.get_attempt_with_details(attempt_id)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "시도를 찾을 수 없습니다.",
                },
            },
        )

    attempt = details["attempt"]

    # 본인 시도이거나 강사인지 확인
    if attempt.student_id != current_user.id and current_user.role == UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "error": {
                    "code": "FORBIDDEN",
                    "message": "접근 권한이 없습니다.",
                },
            },
        )

    return ApiResponse(
        data=GetAttemptResponse(
            attempt=TestAttemptResponse.model_validate(attempt),
            answers=[AnswerLogResponse.model_validate(log) for log in details["answer_logs"]],
            test=TestResponse.model_validate(details["test"]),
        )
    )
