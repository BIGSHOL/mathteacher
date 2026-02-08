"""StudentService 단위 테스트."""

import pytest
from sqlalchemy import select

from app.models.answer_log import AnswerLog
from app.models.class_ import Class
from app.models.test_attempt import TestAttempt
from app.models.user import User
from app.schemas.auth import UserUpdate
from app.schemas.common import Grade, UserRole
from app.services.student_service import StudentService


@pytest.mark.asyncio
async def test_get_students_by_class(db_session):
    """get_students: 특정 반의 학생 목록 조회."""
    # Given: 2개 반과 각 반의 학생들
    teacher = User(
        id="teacher-001",
        login_id="teacher01",
        name="강사 1",
        role=UserRole.TEACHER,
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(teacher)

    class1 = Class(
        id="class-001",
        name="1반",
        teacher_id="teacher-001",
    )
    class2 = Class(
        id="class-002",
        name="2반",
        teacher_id="teacher-001",
    )
    db_session.add(class1)
    db_session.add(class2)

    # 1반 학생 2명
    for i in range(1, 3):
        student = User(
            id=f"student-class1-{i}",
            login_id=f"student1_{i}",
            name=f"학생 1-{i}",
            role=UserRole.STUDENT,
            grade=Grade.MIDDLE_1,
            class_id="class-001",
            hashed_password="hashed",
            is_active=True,
            level=1,
            total_xp=0,
            current_streak=0,
            max_streak=0,
        )
        db_session.add(student)

    # 2반 학생 3명
    for i in range(1, 4):
        student = User(
            id=f"student-class2-{i}",
            login_id=f"student2_{i}",
            name=f"학생 2-{i}",
            role=UserRole.STUDENT,
            grade=Grade.MIDDLE_2,
            class_id="class-002",
            hashed_password="hashed",
            is_active=True,
            level=1,
            total_xp=0,
            current_streak=0,
            max_streak=0,
        )
        db_session.add(student)

    await db_session.commit()

    # When: class_id로 학생 조회
    service = StudentService(db_session)
    students, total = await service.get_students(class_id="class-001")

    # Then: 1반 학생 2명 반환
    assert total == 2
    assert len(students) == 2
    assert all(s.class_id == "class-001" for s in students)


@pytest.mark.asyncio
async def test_get_students_by_grade(db_session):
    """get_students: 특정 학년의 학생 목록 조회."""
    # Given: 다양한 학년의 학생들
    teacher = User(
        id="teacher-002",
        login_id="teacher02",
        name="강사 2",
        role=UserRole.TEACHER,
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(teacher)

    class1 = Class(
        id="class-003",
        name="3반",
        teacher_id="teacher-002",
    )
    db_session.add(class1)

    # 중1 학생 2명, 중2 학생 1명
    grades = [Grade.MIDDLE_1, Grade.MIDDLE_1, Grade.MIDDLE_2]
    for i, grade in enumerate(grades, 1):
        student = User(
            id=f"student-grade-{i}",
            login_id=f"student_grade_{i}",
            name=f"학생 {i}",
            role=UserRole.STUDENT,
            grade=grade,
            class_id="class-003",
            hashed_password="hashed",
            is_active=True,
            level=1,
            total_xp=0,
            current_streak=0,
            max_streak=0,
        )
        db_session.add(student)

    await db_session.commit()

    # When: 중1 학생만 조회
    service = StudentService(db_session)
    students, total = await service.get_students(grade=Grade.MIDDLE_1)

    # Then: 중1 학생 2명 반환
    assert total == 2
    assert len(students) == 2
    assert all(s.grade == Grade.MIDDLE_1 for s in students)


@pytest.mark.asyncio
async def test_get_students_by_teacher(db_session):
    """get_students: 강사가 담당하는 반의 학생만 조회."""
    # Given: 2명의 강사와 각자의 반
    teacher1 = User(
        id="teacher-003",
        login_id="teacher03",
        name="강사 3",
        role=UserRole.TEACHER,
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    teacher2 = User(
        id="teacher-004",
        login_id="teacher04",
        name="강사 4",
        role=UserRole.TEACHER,
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(teacher1)
    db_session.add(teacher2)

    class1 = Class(id="class-004", name="4반", teacher_id="teacher-003")
    class2 = Class(id="class-005", name="5반", teacher_id="teacher-004")
    db_session.add(class1)
    db_session.add(class2)

    # 각 반에 학생 추가
    student1 = User(
        id="student-teacher-1",
        login_id="student_t1",
        name="학생 T1",
        role=UserRole.STUDENT,
        grade=Grade.MIDDLE_1,
        class_id="class-004",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    student2 = User(
        id="student-teacher-2",
        login_id="student_t2",
        name="학생 T2",
        role=UserRole.STUDENT,
        grade=Grade.MIDDLE_1,
        class_id="class-005",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student1)
    db_session.add(student2)
    await db_session.commit()

    # When: teacher1이 자신의 학생만 조회
    service = StudentService(db_session)
    students, total = await service.get_students(teacher_id="teacher-003")

    # Then: class-004의 학생만 반환
    assert total == 1
    assert len(students) == 1
    assert students[0].class_id == "class-004"


@pytest.mark.asyncio
async def test_get_students_excludes_inactive(db_session):
    """get_students: 비활성 학생은 제외."""
    # Given: 활성/비활성 학생
    teacher = User(
        id="teacher-005",
        login_id="teacher05",
        name="강사 5",
        role=UserRole.TEACHER,
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(teacher)

    class1 = Class(id="class-006", name="6반", teacher_id="teacher-005")
    db_session.add(class1)

    active_student = User(
        id="student-active",
        login_id="student_active",
        name="활성 학생",
        role=UserRole.STUDENT,
        class_id="class-006",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    inactive_student = User(
        id="student-inactive",
        login_id="student_inactive",
        name="비활성 학생",
        role=UserRole.STUDENT,
        class_id="class-006",
        hashed_password="hashed",
        is_active=False,  # 비활성
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(active_student)
    db_session.add(inactive_student)
    await db_session.commit()

    # When: 학생 목록 조회
    service = StudentService(db_session)
    students, total = await service.get_students(class_id="class-006")

    # Then: 활성 학생만 반환
    assert total == 1
    assert len(students) == 1
    assert students[0].id == "student-active"


@pytest.mark.asyncio
async def test_get_student_by_id(db_session):
    """get_student_by_id: 학생 ID로 조회."""
    # Given: 학생 존재
    student = User(
        id="student-get-001",
        login_id="student_get_001",
        name="조회 학생",
        role=UserRole.STUDENT,
        grade=Grade.MIDDLE_1,
        hashed_password="hashed",
        is_active=True,
        level=5,
        total_xp=500,
        current_streak=3,
        max_streak=10,
    )
    db_session.add(student)
    await db_session.commit()

    # When: get_student_by_id 호출
    service = StudentService(db_session)
    result = await service.get_student_by_id("student-get-001")

    # Then: 학생 정보 반환
    assert result is not None
    assert result.id == "student-get-001"
    assert result.name == "조회 학생"
    assert result.level == 5
    assert result.total_xp == 500


@pytest.mark.asyncio
async def test_get_student_by_id_not_found(db_session):
    """get_student_by_id: 존재하지 않는 학생은 None 반환."""
    # Given: 학생 없음
    service = StudentService(db_session)

    # When: 존재하지 않는 ID로 조회
    result = await service.get_student_by_id("nonexistent")

    # Then: None 반환
    assert result is None


@pytest.mark.asyncio
async def test_create_student(db_session):
    """create_student: 새 학생 생성."""
    # Given: 반 존재
    teacher = User(
        id="teacher-006",
        login_id="teacher06",
        name="강사 6",
        role=UserRole.TEACHER,
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(teacher)

    class1 = Class(id="class-007", name="7반", teacher_id="teacher-006")
    db_session.add(class1)
    await db_session.commit()

    # When: create_student 호출
    service = StudentService(db_session)
    student = await service.create_student(
        login_id="new_student",
        password="password123",
        name="신규 학생",
        grade=Grade.MIDDLE_1,
        class_id="class-007",
    )

    # Then: 학생이 생성됨
    assert student.id is not None
    assert student.login_id == "new_student"
    assert student.name == "신규 학생"
    assert student.role == UserRole.STUDENT
    assert student.grade == Grade.MIDDLE_1
    assert student.class_id == "class-007"
    assert student.is_active is True

    # DB에서 다시 조회하여 확인
    stmt = select(User).where(User.login_id == "new_student")
    saved_student = await db_session.scalar(stmt)
    assert saved_student is not None
    assert saved_student.name == "신규 학생"


@pytest.mark.asyncio
async def test_update_student(db_session):
    """update_student: 학생 정보 수정."""
    # Given: 학생 존재
    student = User(
        id="student-update-001",
        login_id="student_update_001",
        name="원래 이름",
        role=UserRole.STUDENT,
        grade=Grade.MIDDLE_1,
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)
    await db_session.commit()

    # When: update_student 호출
    service = StudentService(db_session)
    update_data = UserUpdate(name="변경된 이름", grade=Grade.MIDDLE_2)
    updated_student = await service.update_student("student-update-001", update_data)

    # Then: 학생 정보가 수정됨
    assert updated_student is not None
    assert updated_student.name == "변경된 이름"
    assert updated_student.grade == Grade.MIDDLE_2

    # DB에서 다시 조회하여 확인
    stmt = select(User).where(User.id == "student-update-001")
    saved_student = await db_session.scalar(stmt)
    assert saved_student.name == "변경된 이름"
    assert saved_student.grade == Grade.MIDDLE_2


@pytest.mark.asyncio
async def test_update_student_not_found(db_session):
    """update_student: 존재하지 않는 학생은 None 반환."""
    # Given: 학생 없음
    service = StudentService(db_session)

    # When: 존재하지 않는 학생 수정 시도
    update_data = UserUpdate(name="변경된 이름")
    result = await service.update_student("nonexistent", update_data)

    # Then: None 반환
    assert result is None


@pytest.mark.asyncio
async def test_delete_student(db_session):
    """delete_student: 학생 삭제(비활성화)."""
    # Given: 학생 존재
    student = User(
        id="student-delete-001",
        login_id="student_delete_001",
        name="삭제 대상",
        role=UserRole.STUDENT,
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)
    await db_session.commit()

    # When: delete_student 호출
    service = StudentService(db_session)
    result = await service.delete_student("student-delete-001")

    # Then: 삭제 성공 (비활성화)
    assert result is True

    # DB에서 확인
    stmt = select(User).where(User.id == "student-delete-001")
    deleted_student = await db_session.scalar(stmt)
    assert deleted_student is not None
    assert deleted_student.is_active is False


@pytest.mark.asyncio
async def test_delete_student_not_found(db_session):
    """delete_student: 존재하지 않는 학생은 False 반환."""
    # Given: 학생 없음
    service = StudentService(db_session)

    # When: 존재하지 않는 학생 삭제 시도
    result = await service.delete_student("nonexistent")

    # Then: False 반환
    assert result is False


@pytest.mark.asyncio
async def test_check_teacher_access_success(db_session):
    """check_teacher_access: 담당 강사는 접근 가능."""
    # Given: 강사와 학생
    teacher = User(
        id="teacher-007",
        login_id="teacher07",
        name="강사 7",
        role=UserRole.TEACHER,
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(teacher)

    class1 = Class(id="class-008", name="8반", teacher_id="teacher-007")
    db_session.add(class1)

    student = User(
        id="student-access-001",
        login_id="student_access_001",
        name="학생",
        role=UserRole.STUDENT,
        class_id="class-008",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)
    await db_session.commit()

    # When: check_teacher_access 호출
    service = StudentService(db_session)
    result = await service.check_teacher_access("teacher-007", "student-access-001")

    # Then: True 반환 (담당 강사)
    assert result is True


@pytest.mark.asyncio
async def test_check_teacher_access_denied(db_session):
    """check_teacher_access: 다른 반 강사는 접근 불가."""
    # Given: 2명의 강사와 각자의 반
    teacher1 = User(
        id="teacher-008",
        login_id="teacher08",
        name="강사 8",
        role=UserRole.TEACHER,
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    teacher2 = User(
        id="teacher-009",
        login_id="teacher09",
        name="강사 9",
        role=UserRole.TEACHER,
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(teacher1)
    db_session.add(teacher2)

    class1 = Class(id="class-009", name="9반", teacher_id="teacher-008")
    class2 = Class(id="class-010", name="10반", teacher_id="teacher-009")
    db_session.add(class1)
    db_session.add(class2)

    student = User(
        id="student-access-002",
        login_id="student_access_002",
        name="학생",
        role=UserRole.STUDENT,
        class_id="class-009",  # teacher-008의 반
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)
    await db_session.commit()

    # When: teacher-009가 teacher-008의 학생에 접근 시도
    service = StudentService(db_session)
    result = await service.check_teacher_access("teacher-009", "student-access-002")

    # Then: False 반환 (다른 반 학생)
    assert result is False


@pytest.mark.asyncio
async def test_reset_password(db_session):
    """reset_password: 학생 비밀번호 초기화."""
    # Given: 학생 존재
    student = User(
        id="student-password-001",
        login_id="student_password_001",
        name="학생",
        role=UserRole.STUDENT,
        hashed_password="old_hashed_password",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(student)
    await db_session.commit()

    old_password = student.hashed_password

    # When: reset_password 호출
    service = StudentService(db_session)
    result = await service.reset_password("student-password-001", "new_password123")

    # Then: 비밀번호가 변경됨
    assert result is not None
    assert result.hashed_password != old_password
    assert result.hashed_password != "new_password123"  # 해시됨

    # DB에서 확인
    stmt = select(User).where(User.id == "student-password-001")
    saved_student = await db_session.scalar(stmt)
    assert saved_student.hashed_password == result.hashed_password


@pytest.mark.asyncio
async def test_reset_test_history(db_session):
    """reset_test_history: 학생의 모든 테스트 기록 초기화."""
    # Given: 테스트 기록이 있는 학생
    student = User(
        id="student-history-001",
        login_id="student_history_001",
        name="학생",
        role=UserRole.STUDENT,
        hashed_password="hashed",
        is_active=True,
        level=5,
        total_xp=1000,
        current_streak=10,
        max_streak=20,
    )
    db_session.add(student)

    # 테스트 시도 2개
    attempt1 = TestAttempt(
        id="attempt-history-1",
        test_id="test-001",
        student_id="student-history-001",
        score=80,
        max_score=100,
    )
    attempt2 = TestAttempt(
        id="attempt-history-2",
        test_id="test-002",
        student_id="student-history-001",
        score=90,
        max_score=100,
    )
    db_session.add(attempt1)
    db_session.add(attempt2)

    # 답변 로그
    log1 = AnswerLog(
        id="log-history-1",
        attempt_id="attempt-history-1",
        question_id="q-001",
        selected_answer="A",
        is_correct=True,
        time_spent_seconds=30,
    )
    log2 = AnswerLog(
        id="log-history-2",
        attempt_id="attempt-history-2",
        question_id="q-002",
        selected_answer="B",
        is_correct=True,
        time_spent_seconds=45,
    )
    db_session.add(log1)
    db_session.add(log2)
    await db_session.commit()

    # When: reset_test_history 호출
    service = StudentService(db_session)
    result = await service.reset_test_history("student-history-001")

    # Then: 테스트 기록 삭제 및 통계 초기화
    assert result is True

    # 테스트 시도 삭제 확인
    stmt_attempts = select(TestAttempt).where(
        TestAttempt.student_id == "student-history-001"
    )
    attempts = (await db_session.scalars(stmt_attempts)).all()
    assert len(attempts) == 0

    # 답변 로그 삭제 확인
    stmt_logs = select(AnswerLog).where(
        AnswerLog.id.in_(["log-history-1", "log-history-2"])
    )
    logs = (await db_session.scalars(stmt_logs)).all()
    assert len(logs) == 0

    # 학생 통계 초기화 확인
    stmt_student = select(User).where(User.id == "student-history-001")
    updated_student = await db_session.scalar(stmt_student)
    assert updated_student.level == 1
    assert updated_student.total_xp == 0
    assert updated_student.current_streak == 0
    assert updated_student.max_streak == 0


@pytest.mark.asyncio
async def test_reset_test_history_not_found(db_session):
    """reset_test_history: 존재하지 않는 학생은 False 반환."""
    # Given: 학생 없음
    service = StudentService(db_session)

    # When: 존재하지 않는 학생의 기록 초기화 시도
    result = await service.reset_test_history("nonexistent")

    # Then: False 반환
    assert result is False
