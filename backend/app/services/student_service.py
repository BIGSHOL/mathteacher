"""학생 관리 서비스."""

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.class_ import Class
from app.schemas.common import Grade, UserRole
from app.schemas.auth import UserCreate, UserResponse, UserUpdate
from app.core.security import get_password_hash


class StudentService:
    """학생 관리 서비스."""

    def __init__(self, db: Session):
        self.db = db

    def get_students(
        self,
        teacher_id: str | None = None,
        class_id: str | None = None,
        grade: Grade | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[User], int]:
        """학생 목록 조회."""
        stmt = select(User).where(User.role == UserRole.STUDENT, User.is_active == True)  # noqa: E712

        # 강사인 경우 자신의 반 학생만 조회
        if teacher_id:
            # 강사가 담당하는 반 ID 목록
            class_stmt = select(Class.id).where(Class.teacher_id == teacher_id)
            class_ids = self.db.scalars(class_stmt).all()
            stmt = stmt.where(User.class_id.in_(class_ids))

        if class_id:
            stmt = stmt.where(User.class_id == class_id)

        if grade:
            stmt = stmt.where(User.grade == grade)

        # 총 개수
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.scalar(count_stmt) or 0

        # 페이지네이션
        stmt = stmt.order_by(User.name).offset((page - 1) * page_size).limit(page_size)
        students = list(self.db.scalars(stmt).all())

        return students, total

    def get_student_by_id(self, student_id: str) -> User | None:
        """학생 조회."""
        stmt = select(User).where(
            User.id == student_id,
            User.role == UserRole.STUDENT,
        )
        return self.db.scalar(stmt)

    def create_student(
        self,
        email: str,
        password: str,
        name: str,
        grade: Grade,
        class_id: str,
    ) -> User:
        """학생 생성."""
        hashed_password = get_password_hash(password)
        student = User(
            email=email,
            hashed_password=hashed_password,
            name=name,
            role=UserRole.STUDENT,
            grade=grade,
            class_id=class_id,
        )
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def update_student(
        self,
        student_id: str,
        update_data: UserUpdate,
    ) -> User | None:
        """학생 정보 수정."""
        student = self.get_student_by_id(student_id)
        if not student:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(student, field, value)

        self.db.commit()
        self.db.refresh(student)
        return student

    def delete_student(self, student_id: str) -> bool:
        """학생 삭제 (비활성화)."""
        student = self.get_student_by_id(student_id)
        if not student:
            return False

        student.is_active = False
        self.db.commit()
        return True

    def check_teacher_access(self, teacher_id: str, student_id: str) -> bool:
        """강사가 해당 학생에 접근 권한이 있는지 확인."""
        student = self.get_student_by_id(student_id)
        if not student or not student.class_id:
            return False

        # 학생이 속한 반의 담당 강사인지 확인
        class_ = self.db.get(Class, student.class_id)
        if not class_:
            return False

        return class_.teacher_id == teacher_id
