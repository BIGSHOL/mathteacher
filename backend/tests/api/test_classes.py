"""반 관리 API 테스트."""

import pytest
from httpx import AsyncClient

from tests.conftest import TestingSessionLocal
from app.models.class_ import Class


async def _add_class(class_id, name, teacher_id, daily_quota=20, quota_carry_over=False):
    """테스트용 반 데이터 추가."""
    async with TestingSessionLocal() as session:
        cls = Class(
            id=class_id,
            name=name,
            teacher_id=teacher_id,
            daily_quota=daily_quota,
            quota_carry_over=quota_carry_over,
        )
        session.add(cls)
        await session.commit()


@pytest.mark.asyncio
async def test_get_classes_as_teacher(client: AsyncClient):
    """강사가 자신의 반 목록 조회."""
    # 강사 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "teacher01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 반 목록 조회
    resp = await client.get("/api/v1/classes", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "items" in data["data"]
    assert "total" in data["data"]

    # conftest에서 생성한 class-001이 포함되어 있어야 함
    items = data["data"]["items"]
    assert len(items) > 0
    assert any(item["id"] == "class-001" for item in items)


@pytest.mark.asyncio
async def test_get_classes_as_master(client: AsyncClient):
    """마스터가 모든 반 목록 조회."""
    # 추가 반 생성 (다른 강사의 반)
    await _add_class("class-002", "다른 반", "teacher-002")

    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 반 목록 조회
    resp = await client.get("/api/v1/classes", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    items = data["data"]["items"]

    # 모든 반이 조회되어야 함
    assert len(items) >= 2
    class_ids = [item["id"] for item in items]
    assert "class-001" in class_ids
    assert "class-002" in class_ids


@pytest.mark.asyncio
async def test_get_classes_forbidden_for_student(client: AsyncClient):
    """학생은 반 목록 조회 불가 (403)."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 반 목록 조회 시도
    resp = await client.get("/api/v1/classes", headers=headers)
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_update_class_quota_as_teacher(client: AsyncClient):
    """강사가 자신의 반 할당량 수정."""
    # 강사 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "teacher01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 할당량 수정
    resp = await client.patch(
        "/api/v1/classes/class-001/quota",
        headers=headers,
        json={"daily_quota": 30, "quota_carry_over": True}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["daily_quota"] == 30
    assert data["data"]["quota_carry_over"] is True


@pytest.mark.asyncio
async def test_update_class_quota_as_master(client: AsyncClient):
    """마스터가 임의의 반 할당량 수정."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 할당량 수정
    resp = await client.patch(
        "/api/v1/classes/class-001/quota",
        headers=headers,
        json={"daily_quota": 50, "quota_carry_over": False}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["daily_quota"] == 50
    assert data["data"]["quota_carry_over"] is False


@pytest.mark.asyncio
async def test_update_class_quota_not_found(client: AsyncClient):
    """존재하지 않는 반 할당량 수정 (404)."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 존재하지 않는 반 수정 시도
    resp = await client.patch(
        "/api/v1/classes/nonexistent/quota",
        headers=headers,
        json={"daily_quota": 25, "quota_carry_over": False}
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_class_quota_forbidden_for_other_teacher(client: AsyncClient):
    """강사가 다른 강사의 반 할당량 수정 시도 (403)."""
    # 다른 강사의 반 생성
    await _add_class("class-003", "다른 강사 반", "teacher-999")

    # 강사 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "teacher01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 다른 강사의 반 수정 시도
    resp = await client.patch(
        "/api/v1/classes/class-003/quota",
        headers=headers,
        json={"daily_quota": 40, "quota_carry_over": False}
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_update_class_quota_forbidden_for_student(client: AsyncClient):
    """학생은 반 할당량 수정 불가 (403)."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 할당량 수정 시도
    resp = await client.patch(
        "/api/v1/classes/class-001/quota",
        headers=headers,
        json={"daily_quota": 35, "quota_carry_over": False}
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_update_class_quota_validation_min(client: AsyncClient):
    """할당량 최소값 검증 (1 이상)."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # daily_quota < 1 시도
    resp = await client.patch(
        "/api/v1/classes/class-001/quota",
        headers=headers,
        json={"daily_quota": 0, "quota_carry_over": False}
    )
    assert resp.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_update_class_quota_validation_max(client: AsyncClient):
    """할당량 최대값 검증 (100 이하)."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # daily_quota > 100 시도
    resp = await client.patch(
        "/api/v1/classes/class-001/quota",
        headers=headers,
        json={"daily_quota": 101, "quota_carry_over": False}
    )
    assert resp.status_code == 422  # Validation error
