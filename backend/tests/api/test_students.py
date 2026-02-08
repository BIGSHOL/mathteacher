"""학생 관리 API 테스트."""

import pytest
from httpx import AsyncClient

from tests.conftest import TestingSessionLocal
from app.models.user import User
from app.models.class_ import Class
from app.services.auth_service import AuthService


async def _add_student(student_id, login_id, name, class_id, grade="middle_1"):
    """테스트용 학생 추가."""
    auth_service = AuthService()
    async with TestingSessionLocal() as session:
        student = User(
            id=student_id,
            login_id=login_id,
            name=name,
            role="student",
            grade=grade,
            class_id=class_id,
            hashed_password=auth_service.hash_password("password123"),
            is_active=True,
            level=1,
            total_xp=0,
            current_streak=0,
            max_streak=0,
        )
        session.add(student)
        await session.commit()


async def _add_class(class_id, name, teacher_id):
    """테스트용 반 추가."""
    async with TestingSessionLocal() as session:
        cls = Class(
            id=class_id,
            name=name,
            teacher_id=teacher_id,
        )
        session.add(cls)
        await session.commit()


@pytest.mark.asyncio
async def test_get_students_as_teacher(client: AsyncClient):
    """강사가 자신의 반 학생 목록 조회."""
    # 강사 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "teacher01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 학생 목록 조회
    resp = await client.get("/api/v1/students", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "items" in data["data"]
    assert "total" in data["data"]

    # conftest에서 생성한 student-001이 포함되어 있어야 함
    items = data["data"]["items"]
    assert len(items) > 0
    assert any(item["id"] == "student-001" for item in items)


@pytest.mark.asyncio
async def test_get_students_as_master(client: AsyncClient):
    """마스터가 모든 학생 목록 조회."""
    # 다른 반 추가
    await _add_class("class-002", "다른 반", "teacher-002")
    # 다른 반 학생 추가
    await _add_student("student-002", "student02", "다른 학생", "class-002")

    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 학생 목록 조회
    resp = await client.get("/api/v1/students", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    items = data["data"]["items"]

    # 모든 학생이 조회되어야 함
    assert len(items) >= 2
    student_ids = [item["id"] for item in items]
    assert "student-001" in student_ids
    assert "student-002" in student_ids


@pytest.mark.asyncio
async def test_get_students_forbidden_for_student(client: AsyncClient):
    """학생은 학생 목록 조회 불가 (403)."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 학생 목록 조회 시도
    resp = await client.get("/api/v1/students", headers=headers)
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_get_student_detail_as_master(client: AsyncClient):
    """마스터가 학생 상세 조회."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 학생 상세 조회
    resp = await client.get("/api/v1/students/student-001", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["id"] == "student-001"
    assert data["data"]["role"] == "student"


@pytest.mark.asyncio
async def test_get_student_detail_not_found(client: AsyncClient):
    """존재하지 않는 학생 조회 (404)."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 존재하지 않는 학생 조회
    resp = await client.get("/api/v1/students/nonexistent", headers=headers)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_student_detail_forbidden_for_other_teacher(client: AsyncClient):
    """강사가 다른 반 학생 조회 시도 (403)."""
    # 다른 반 추가
    await _add_class("class-003", "다른 반", "teacher-003")
    # 다른 반 학생 추가
    await _add_student("student-003", "student03", "다른 반 학생", "class-003")

    # 강사 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "teacher01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 다른 반 학생 조회 시도
    resp = await client.get("/api/v1/students/student-003", headers=headers)
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_create_student_success(client: AsyncClient):
    """학생 생성 성공."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 학생 생성
    resp = await client.post(
        "/api/v1/students",
        headers=headers,
        json={
            "login_id": "newstudent01",
            "password": "newpass123",
            "name": "신규 학생",
            "role": "student",
            "grade": "middle_1",
            "class_id": "class-001",
        }
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["login_id"] == "newstudent01"
    assert data["data"]["name"] == "신규 학생"
    assert data["data"]["role"] == "student"


@pytest.mark.asyncio
async def test_create_student_duplicate_login_id(client: AsyncClient):
    """중복 아이디로 학생 생성 시도 (400)."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 이미 존재하는 login_id로 학생 생성 시도
    resp = await client.post(
        "/api/v1/students",
        headers=headers,
        json={
            "login_id": "student01",  # 이미 존재
            "password": "newpass123",
            "name": "중복 학생",
            "role": "student",
            "grade": "middle_1",
            "class_id": "class-001",
        }
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_create_student_forbidden_for_student(client: AsyncClient):
    """학생은 학생 생성 불가 (403)."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 학생 생성 시도
    resp = await client.post(
        "/api/v1/students",
        headers=headers,
        json={
            "login_id": "unauthorized",
            "password": "pass123",
            "name": "권한 없음",
            "role": "student",
            "grade": "middle_1",
            "class_id": "class-001",
        }
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_update_student_success(client: AsyncClient):
    """학생 정보 수정 성공."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 학생 정보 수정
    resp = await client.patch(
        "/api/v1/students/student-001",
        headers=headers,
        json={
            "name": "수정된 학생 이름",
            "grade": "middle_2",
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["name"] == "수정된 학생 이름"
    assert data["data"]["grade"] == "middle_2"


@pytest.mark.asyncio
async def test_update_student_not_found(client: AsyncClient):
    """존재하지 않는 학생 수정 (404)."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 존재하지 않는 학생 수정 시도
    resp = await client.patch(
        "/api/v1/students/nonexistent",
        headers=headers,
        json={"name": "존재하지 않음"}
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_student_success(client: AsyncClient):
    """학생 삭제 성공 (204)."""
    # 삭제할 학생 추가
    await _add_student("student-to-delete", "studentdel", "삭제될 학생", "class-001")

    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 학생 삭제
    resp = await client.delete("/api/v1/students/student-to-delete", headers=headers)
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_delete_student_not_found(client: AsyncClient):
    """존재하지 않는 학생 삭제 (404)."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 존재하지 않는 학생 삭제 시도
    resp = await client.delete("/api/v1/students/nonexistent", headers=headers)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_reset_student_password_success(client: AsyncClient):
    """학생 비밀번호 초기화 성공."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 비밀번호 초기화
    resp = await client.post(
        "/api/v1/students/student-001/reset-password",
        headers=headers,
        json={"new_password": "newpassword123"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "비밀번호가 초기화되었습니다" in data["data"]["message"]


@pytest.mark.asyncio
async def test_reset_student_password_validation(client: AsyncClient):
    """비밀번호 최소 길이 검증 (6자 이상)."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 너무 짧은 비밀번호
    resp = await client.post(
        "/api/v1/students/student-001/reset-password",
        headers=headers,
        json={"new_password": "short"}
    )
    assert resp.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_reset_student_password_not_found(client: AsyncClient):
    """존재하지 않는 학생 비밀번호 초기화 (404)."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 존재하지 않는 학생 비밀번호 초기화 시도
    resp = await client.post(
        "/api/v1/students/nonexistent/reset-password",
        headers=headers,
        json={"new_password": "newpass123"}
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_reset_student_history_success(client: AsyncClient):
    """학생 테스트 기록 초기화 성공."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 테스트 기록 초기화
    resp = await client.post(
        "/api/v1/students/student-001/reset-history",
        headers=headers
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "테스트 기록이 초기화되었습니다" in data["data"]["message"]


@pytest.mark.asyncio
async def test_reset_student_history_not_found(client: AsyncClient):
    """존재하지 않는 학생 테스트 기록 초기화 (404)."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 존재하지 않는 학생 테스트 기록 초기화 시도
    resp = await client.post(
        "/api/v1/students/nonexistent/reset-history",
        headers=headers
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_teacher_update_other_class_student_forbidden(client: AsyncClient):
    """강사가 다른 반 학생 수정 시도 (403)."""
    await _add_class("class-other", "다른 반", "teacher-999")
    await _add_student("student-other", "studentother", "다른 반 학생", "class-other")

    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "teacher01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = await client.patch(
        "/api/v1/students/student-other",
        headers=headers,
        json={"name": "변경 시도"}
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_teacher_delete_other_class_student_forbidden(client: AsyncClient):
    """강사가 다른 반 학생 삭제 시도 (403)."""
    await _add_class("class-other2", "다른 반2", "teacher-888")
    await _add_student("student-other2", "studentother2", "다른 반 학생2", "class-other2")

    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "teacher01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = await client.delete("/api/v1/students/student-other2", headers=headers)
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_teacher_reset_password_other_class_student_forbidden(client: AsyncClient):
    """강사가 다른 반 학생 비밀번호 초기화 시도 (403)."""
    await _add_class("class-other3", "다른 반3", "teacher-777")
    await _add_student("student-other3", "studentother3", "다른 반 학생3", "class-other3")

    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "teacher01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = await client.post(
        "/api/v1/students/student-other3/reset-password",
        headers=headers,
        json={"new_password": "newpass123"}
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_teacher_reset_history_other_class_student_forbidden(client: AsyncClient):
    """강사가 다른 반 학생 기록 초기화 시도 (403)."""
    await _add_class("class-other4", "다른 반4", "teacher-666")
    await _add_student("student-other4", "studentother4", "다른 반 학생4", "class-other4")

    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "teacher01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = await client.post(
        "/api/v1/students/student-other4/reset-history",
        headers=headers,
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_reset_student_history_forbidden_for_student(client: AsyncClient):
    """학생은 테스트 기록 초기화 불가 (403)."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 테스트 기록 초기화 시도
    resp = await client.post(
        "/api/v1/students/student-001/reset-history",
        headers=headers
    )
    assert resp.status_code == 403
