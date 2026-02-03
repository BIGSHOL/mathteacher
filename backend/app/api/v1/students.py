"""학생 관리 API 엔드포인트."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import (
    ApiResponse,
    Grade,
    PaginatedResponse,
    RegisterStudentRequest,
    UserResponse,
    UserUpdate,
)
from app.schemas.common import UserRole
from app.services.student_service import StudentService
from app.services.auth_service import AuthService
from app.api.v1.auth import get_current_user, require_role


class ResetPasswordRequest(BaseModel):
    """비밀번호 초기화 요청."""
    new_password: str = Field(..., min_length=6, max_length=100)

router = APIRouter(prefix="/students", tags=["students"])


def get_student_service(db: Session = Depends(get_db)) -> StudentService:
    """학생 서비스 의존성."""
    return StudentService(db)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """인증 서비스 의존성."""
    return AuthService(db)


@router.get("", response_model=ApiResponse[PaginatedResponse[UserResponse]])
async def get_students(
    class_id: str | None = Query(None, description="반 ID 필터"),
    grade: Grade | None = Query(None, description="학년 필터"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    student_service: StudentService = Depends(get_student_service),
):
    """학생 목록 조회 (강사/관리자 전용)."""
    # 강사는 자신의 반 학생만 조회 가능
    teacher_id = current_user.id if current_user.role == UserRole.TEACHER else None

    students, total = student_service.get_students(
        teacher_id=teacher_id,
        class_id=class_id,
        grade=grade,
        page=page,
        page_size=page_size,
    )

    total_pages = (total + page_size - 1) // page_size

    return ApiResponse(
        data=PaginatedResponse(
            items=[UserResponse.model_validate(s) for s in students],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
    )


@router.get("/{student_id}", response_model=ApiResponse[UserResponse])
async def get_student(
    student_id: str,
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    student_service: StudentService = Depends(get_student_service),
):
    """학생 상세 조회."""
    student = student_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "학생을 찾을 수 없습니다.",
                },
            },
        )

    # 강사는 자신의 반 학생만 조회 가능
    if current_user.role == UserRole.TEACHER:
        if not student_service.check_teacher_access(current_user.id, student_id):
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

    return ApiResponse(data=UserResponse.model_validate(student))


@router.post(
    "",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    request: RegisterStudentRequest,
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    student_service: StudentService = Depends(get_student_service),
    auth_service: AuthService = Depends(get_auth_service),
):
    """학생 생성 (강사/관리자 전용)."""
    # 이메일 중복 체크
    existing_user = auth_service.get_user_by_email(request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "EMAIL_ALREADY_EXISTS",
                    "message": "이미 사용 중인 이메일입니다.",
                },
            },
        )

    student = student_service.create_student(
        email=request.email,
        password=request.password,
        name=request.name,
        grade=request.grade,
        class_id=request.class_id,
    )

    return ApiResponse(data=UserResponse.model_validate(student))


@router.patch("/{student_id}", response_model=ApiResponse[UserResponse])
async def update_student(
    student_id: str,
    request: UserUpdate,
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    student_service: StudentService = Depends(get_student_service),
):
    """학생 정보 수정."""
    # 강사는 자신의 반 학생만 수정 가능
    if current_user.role == UserRole.TEACHER:
        if not student_service.check_teacher_access(current_user.id, student_id):
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

    student = student_service.update_student(student_id, request)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "학생을 찾을 수 없습니다.",
                },
            },
        )

    return ApiResponse(data=UserResponse.model_validate(student))


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: str,
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    student_service: StudentService = Depends(get_student_service),
):
    """학생 삭제 (비활성화)."""
    # 강사는 자신의 반 학생만 삭제 가능
    if current_user.role == UserRole.TEACHER:
        if not student_service.check_teacher_access(current_user.id, student_id):
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

    success = student_service.delete_student(student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "학생을 찾을 수 없습니다.",
                },
            },
        )


@router.post("/{student_id}/reset-password", response_model=ApiResponse[dict])
async def reset_student_password(
    student_id: str,
    request: ResetPasswordRequest,
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    student_service: StudentService = Depends(get_student_service),
):
    """학생 비밀번호 초기화 (강사/관리자 전용)."""
    # 강사는 자신의 반 학생만 수정 가능
    if current_user.role == UserRole.TEACHER:
        if not student_service.check_teacher_access(current_user.id, student_id):
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

    student = student_service.reset_password(student_id, request.new_password)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "학생을 찾을 수 없습니다.",
                },
            },
        )

    return ApiResponse(data={"message": "비밀번호가 초기화되었습니다."})


@router.post("/{student_id}/reset-history", response_model=ApiResponse[dict])
async def reset_student_history(
    student_id: str,
    current_user: UserResponse = Depends(require_role(UserRole.TEACHER, UserRole.ADMIN)),
    student_service: StudentService = Depends(get_student_service),
):
    """학생 테스트 기록 초기화 (강사/관리자 전용)."""
    # 강사는 자신의 반 학생만 수정 가능
    if current_user.role == UserRole.TEACHER:
        if not student_service.check_teacher_access(current_user.id, student_id):
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

    success = student_service.reset_test_history(student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "학생을 찾을 수 없습니다.",
                },
            },
        )

    return ApiResponse(data={"message": "테스트 기록이 초기화되었습니다."})
