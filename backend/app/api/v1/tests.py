"""테스트 API 엔드포인트."""

from datetime import datetime, timedelta, timezone

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
    NextQuestionResponse,
    PaginatedResponse,
    QuestionResponse,
    QuestionWithAnswer,
    ReviewResponse,
    StartTestResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
    TestAttemptResponse,
    TestResponse,
    TestWithQuestionsResponse,
    UserResponse,
    AnswerLogResponse,
    WrongQuestionItem,
)
from app.schemas.common import UserRole
from app.services.test_service import TestService
from app.services.grading_service import GradingService
from app.services.gamification_service import GamificationService
from app.services.adaptive_service import AdaptiveService
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


def get_adaptive_service(db: Session = Depends(get_db)) -> AdaptiveService:
    """적응형 서비스 의존성."""
    return AdaptiveService(db)


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
                is_adaptive=test.is_adaptive,
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


@router.get("/review/wrong-questions", response_model=ApiResponse[ReviewResponse])
async def get_wrong_questions(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """틀렸던 문제 목록 조회 (복습용)."""
    from app.models.answer_log import AnswerLog
    from app.models.test_attempt import TestAttempt
    from sqlalchemy import select, func, desc

    # 학생의 오답 중 가장 최근 기록을 question_id별로 조회
    # 서브쿼리: 각 문제별 오답 횟수와 최근 기록
    wrong_subq = (
        select(
            AnswerLog.question_id,
            func.count(AnswerLog.id).label("wrong_count"),
            func.max(AnswerLog.created_at).label("last_attempted_at"),
        )
        .join(TestAttempt, AnswerLog.attempt_id == TestAttempt.id)
        .where(
            TestAttempt.student_id == current_user.id,
            AnswerLog.is_correct == False,  # noqa: E712
        )
        .group_by(AnswerLog.question_id)
        .subquery()
    )

    # 이미 정답을 맞힌 문제는 제외 (최근 시도에서 맞힌 것)
    correct_subq = (
        select(AnswerLog.question_id)
        .join(TestAttempt, AnswerLog.attempt_id == TestAttempt.id)
        .where(
            TestAttempt.student_id == current_user.id,
            AnswerLog.is_correct == True,  # noqa: E712
        )
        .distinct()
        .subquery()
    )

    # 오답 문제 조회 (정답 맞힌 적 없는 것만)
    stmt = (
        select(Question, wrong_subq.c.wrong_count, wrong_subq.c.last_attempted_at)
        .join(wrong_subq, Question.id == wrong_subq.c.question_id)
        .where(Question.id.notin_(select(correct_subq.c.question_id)))
        .order_by(desc(wrong_subq.c.wrong_count))
    )

    results = db.execute(stmt).all()

    items = []
    for question, wrong_count, last_attempted_at in results:
        # 해당 문제의 가장 최근 오답 선택지 조회
        last_answer_stmt = (
            select(AnswerLog.selected_answer)
            .join(TestAttempt, AnswerLog.attempt_id == TestAttempt.id)
            .where(
                TestAttempt.student_id == current_user.id,
                AnswerLog.question_id == question.id,
                AnswerLog.is_correct == False,  # noqa: E712
            )
            .order_by(desc(AnswerLog.created_at))
            .limit(1)
        )
        last_selected = db.scalar(last_answer_stmt) or ""

        items.append(
            WrongQuestionItem(
                question=QuestionWithAnswer(
                    id=question.id,
                    concept_id=question.concept_id,
                    question_type=question.question_type,
                    difficulty=question.difficulty,
                    content=question.content,
                    options=question.options,
                    explanation=question.explanation,
                    points=question.points,
                    correct_answer=question.correct_answer,
                ),
                wrong_count=wrong_count,
                last_selected_answer=last_selected,
                last_attempted_at=last_attempted_at,
            )
        )

    return ApiResponse(
        data=ReviewResponse(items=items, total=len(items))
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
            category=q.category,
            part=q.part,
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
    adaptive_service: AdaptiveService = Depends(get_adaptive_service),
    db: Session = Depends(get_db),
):
    """테스트 시작."""
    from app.models.test import Test as TestModel

    test = db.get(TestModel, test_id)
    if not test or not test.is_active:
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

    if test.is_adaptive:
        # 적응형 테스트: 첫 문제만 선택
        first_question = adaptive_service.select_first_question(test, current_user.id)
        if not first_question:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "success": False,
                    "error": {
                        "code": "NO_QUESTIONS",
                        "message": "출제할 문제가 없습니다.",
                    },
                },
            )

        initial_diff = adaptive_service.get_initial_difficulty_for(test, current_user.id)

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

        # 적응형 필드 설정
        attempt.is_adaptive = True
        attempt.initial_difficulty = initial_diff
        attempt.current_difficulty = initial_diff
        attempt.adaptive_question_ids = [first_question.id]
        attempt.max_score = first_question.points  # 첫 문제 점수로 시작
        db.commit()

        question_responses = [
            QuestionResponse(
                id=first_question.id,
                concept_id=first_question.concept_id,
                category=first_question.category,
                part=first_question.part,
                question_type=first_question.question_type,
                difficulty=first_question.difficulty,
                content=first_question.content,
                options=first_question.options,
                explanation="",
                points=first_question.points,
            )
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
                    is_adaptive=True,
                    created_at=test.created_at,
                    questions=question_responses,
                ),
                started_at=attempt.started_at,
                is_adaptive=True,
                current_difficulty=initial_diff,
            )
        )

    # 고정형 테스트 (문제 풀 + 셔플 지원)
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

    # 셔플 적용된 문제 가져오기
    shuffled_questions = test_service.get_attempt_questions(attempt.id)
    if not shuffled_questions:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": {
                    "code": "NO_QUESTIONS",
                    "message": "문제를 불러올 수 없습니다.",
                },
            },
        )

    question_responses = [
        QuestionResponse(
            id=q["id"],
            concept_id=q.get("concept_id", ""),
            category=q["category"],
            part=q["part"],
            question_type=q["question_type"],
            difficulty=q["difficulty"],
            content=q["content"],
            options=q["options"],
            explanation=q.get("explanation", ""),
            points=q["points"],
        )
        for q in shuffled_questions
    ]

    # 실제 출제 문제 수 (문제 풀에서 선택된 경우)
    actual_question_count = len(shuffled_questions)

    return ApiResponse(
        data=StartTestResponse(
            attempt_id=attempt.id,
            test=TestWithQuestionsResponse(
                id=test.id,
                title=test.title,
                description=test.description,
                grade=test.grade,
                concept_ids=test.concept_ids,
                question_count=actual_question_count,
                time_limit_minutes=test.time_limit_minutes,
                is_active=test.is_active,
                is_adaptive=False,
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

    # 셔플된 정답 가져오기 (셔플이 적용된 경우)
    correct_answer_override = test_service.get_correct_answer_for_attempt(
        attempt_id, request.question_id
    )

    # 채점
    result = grading_service.submit_answer(
        attempt=attempt,
        question=question,
        selected_answer=request.selected_answer,
        time_spent_seconds=request.time_spent_seconds,
        current_combo=current_combo,
        correct_answer_override=correct_answer_override,
    )

    # 적응형이면 다음 난이도 힌트 추가
    if attempt.is_adaptive:
        adaptive_svc = AdaptiveService(db)
        result["next_difficulty"] = adaptive_svc.peek_next_difficulty(attempt)

    return ApiResponse(data=SubmitAnswerResponse(**result))


@router.post(
    "/attempts/{attempt_id}/next",
    response_model=ApiResponse[NextQuestionResponse],
)
async def get_next_question(
    attempt_id: str,
    current_user: UserResponse = Depends(get_current_user),
    test_service: TestService = Depends(get_test_service),
    adaptive_service: AdaptiveService = Depends(get_adaptive_service),
):
    """적응형 테스트 다음 문제 조회."""
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

    if not attempt.is_adaptive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_ADAPTIVE",
                    "message": "적응형 테스트가 아닙니다.",
                },
            },
        )

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

    answered_count = len(attempt.adaptive_question_ids or [])
    questions_remaining = attempt.total_count - answered_count

    # 이미 모든 문제 출제됨
    if questions_remaining <= 0:
        return ApiResponse(
            data=NextQuestionResponse(
                question=None,
                current_difficulty=attempt.current_difficulty or 6,
                questions_answered=answered_count,
                questions_remaining=0,
                is_complete=True,
            )
        )

    question, target_difficulty = adaptive_service.select_next_question(attempt)

    if not question:
        return ApiResponse(
            data=NextQuestionResponse(
                question=None,
                current_difficulty=target_difficulty,
                questions_answered=answered_count,
                questions_remaining=0,
                is_complete=True,
            )
        )

    new_answered = len(attempt.adaptive_question_ids or [])
    new_remaining = attempt.total_count - new_answered

    return ApiResponse(
        data=NextQuestionResponse(
            question=QuestionResponse(
                id=question.id,
                concept_id=question.concept_id,
                question_type=question.question_type,
                difficulty=question.difficulty,
                content=question.content,
                options=question.options,
                explanation="",
                points=question.points,
            ),
            current_difficulty=target_difficulty,
            questions_answered=new_answered,
            questions_remaining=new_remaining,
            is_complete=False,
        )
    )


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
    KST = timezone(timedelta(hours=9))
    today = datetime.now(KST).date().isoformat()

    # 적응형 테스트이면 최종 난이도 기반 레벨 반영
    adaptive_result = None
    if completed_attempt.is_adaptive and completed_attempt.current_difficulty:
        adaptive_result = {
            "final_difficulty": completed_attempt.current_difficulty,
            "correct_count": completed_attempt.correct_count,
            "total_count": completed_attempt.total_count,
        }

    gamification_result = gamification_service.update_user_gamification(
        user=user,
        xp_earned=completed_attempt.xp_earned,
        today=today,
        adaptive_result=adaptive_result,
    )

    # 개념 숙련도 업데이트 및 자동 해제
    from app.services.mastery_service import MasteryService
    from app.services.chapter_service import ChapterService

    mastery_service = MasteryService(db)
    chapter_service = ChapterService(db)

    # 개념별 숙련도 업데이트
    mastery_service.update_mastery_from_attempt(current_user.id, attempt_id)

    # 관련 단원 진행률 업데이트 (테스트의 개념들이 속한 단원)
    # TODO: 테스트와 단원 연결 후 구현

    # 답안 기록 조회
    details = test_service.get_attempt_with_details(attempt_id)
    answer_logs = details["answer_logs"] if details else []

    return ApiResponse(
        data=CompleteTestResponse(
            attempt=TestAttemptResponse.model_validate(completed_attempt),
            answers=[AnswerLogResponse.model_validate(log) for log in answer_logs],
            level_up=gamification_result["level_up"],
            level_down=gamification_result.get("level_down", False),
            new_level=gamification_result["new_level"],
            xp_earned=completed_attempt.xp_earned,
            total_xp=gamification_result.get("total_xp"),
            current_streak=gamification_result.get("current_streak"),
            achievements_earned=[],  # TODO: 업적 시스템 구현
            level_down_defense=gamification_result.get("level_down_defense"),
            level_down_action=gamification_result.get("level_down_action", "none"),
        )
    )


@router.get("/attempts/{attempt_id}", response_model=ApiResponse[GetAttemptResponse])
async def get_attempt(
    attempt_id: str,
    current_user: UserResponse = Depends(get_current_user),
    test_service: TestService = Depends(get_test_service),
    db: Session = Depends(get_db),
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

    # 문제 포함 테스트 정보 조회
    test = details["test"]

    if attempt.is_adaptive and attempt.adaptive_question_ids:
        # 적응형: adaptive_question_ids 순서대로 문제 복원
        q_ids = attempt.adaptive_question_ids
        q_map = {}
        for qid in q_ids:
            q = db.get(Question, qid)
            if q:
                q_map[qid] = q
        questions = [q_map[qid] for qid in q_ids if qid in q_map]
    else:
        test_with_questions = test_service.get_test_with_questions(test.id)
        questions = test_with_questions["questions"] if test_with_questions else []

    question_responses = [
        QuestionResponse(
            id=q.id,
            concept_id=q.concept_id,
            category=q.category,
            part=q.part,
            question_type=q.question_type,
            difficulty=q.difficulty,
            content=q.content,
            options=q.options,
            explanation="" if not attempt.completed_at else q.explanation,
            points=q.points,
        )
        for q in questions
    ]

    return ApiResponse(
        data=GetAttemptResponse(
            attempt=TestAttemptResponse.model_validate(attempt),
            answers=[AnswerLogResponse.model_validate(log) for log in details["answer_logs"]],
            test=TestWithQuestionsResponse(
                id=test.id,
                title=test.title,
                description=test.description,
                grade=test.grade,
                concept_ids=test.concept_ids,
                question_count=test.question_count,
                time_limit_minutes=test.time_limit_minutes,
                is_active=test.is_active,
                is_adaptive=test.is_adaptive,
                created_at=test.created_at,
                questions=question_responses,
            ),
        )
    )
