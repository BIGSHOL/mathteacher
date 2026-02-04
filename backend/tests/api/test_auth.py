"""인증 API 테스트 (RED 상태 - 실패하는 테스트)."""

import pytest
from httpx import AsyncClient


class TestLogin:
    """로그인 API 테스트."""

    async def test_login_success(self, client: AsyncClient) -> None:
        """유효한 자격증명으로 로그인 성공."""
        response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"
        assert "user" in data["data"]
        assert data["data"]["user"]["login_id"] == "student01"

    async def test_login_invalid_password(self, client: AsyncClient) -> None:
        """잘못된 비밀번호로 로그인 실패."""
        response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "wrong_password"},
        )

        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["success"] is False
        assert data["detail"]["error"]["code"] == "INVALID_CREDENTIALS"

    async def test_login_nonexistent_user(self, client: AsyncClient) -> None:
        """존재하지 않는 사용자 로그인 실패."""
        response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "nonexistent01", "password": "password123"},
        )

        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["success"] is False

    async def test_login_invalid_login_id_format(self, client: AsyncClient) -> None:
        """유효하지 않은 아이디 형식 - 빈 값은 422 반환."""
        response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "", "password": "password123"},
        )

        assert response.status_code == 422


class TestTokenRefresh:
    """토큰 갱신 API 테스트."""

    async def test_refresh_token_success(self, client: AsyncClient) -> None:
        """유효한 refresh token으로 갱신 성공."""
        # 먼저 로그인
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        refresh_token = login_response.json()["data"]["refresh_token"]

        # 토큰 갱신
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]

    async def test_refresh_token_invalid(self, client: AsyncClient) -> None:
        """유효하지 않은 refresh token."""
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token"},
        )

        assert response.status_code == 401

    async def test_refresh_token_expired(self, client: AsyncClient) -> None:
        """만료된 refresh token."""
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "expired_token"},
        )

        assert response.status_code == 401


class TestLogout:
    """로그아웃 API 테스트."""

    async def test_logout_success(self, client: AsyncClient) -> None:
        """로그아웃 성공."""
        # 먼저 로그인
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]
        refresh_token = login_response.json()["data"]["refresh_token"]

        # 로그아웃
        response = await client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": refresh_token},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        assert response.json()["data"]["message"] == "로그아웃 성공"

    async def test_logout_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 로그아웃 시도."""
        response = await client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": "some_token"},
        )

        assert response.status_code == 401


class TestGetMe:
    """현재 사용자 정보 조회 테스트."""

    async def test_get_me_success(self, client: AsyncClient) -> None:
        """인증된 사용자 정보 조회."""
        # 먼저 로그인
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 내 정보 조회
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["login_id"] == "student01"

    async def test_get_me_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 조회 시도."""
        response = await client.get("/api/v1/auth/me")

        assert response.status_code == 401

    async def test_get_me_invalid_token(self, client: AsyncClient) -> None:
        """유효하지 않은 토큰으로 조회."""
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401


class TestRegister:
    """사용자 등록 테스트 (강사 전용)."""

    async def test_register_student_success(self, client: AsyncClient) -> None:
        """학생 등록 성공 (강사 권한)."""
        # 강사로 로그인
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 학생 등록
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "login_id": "new_student01",
                "password": "password123",
                "name": "새 학생",
                "role": "student",
                "grade": "middle_1",
                "class_id": "some-class-id",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["user"]["login_id"] == "new_student01"

    async def test_register_duplicate_login_id(self, client: AsyncClient) -> None:
        """중복 아이디로 등록 실패."""
        # 강사로 로그인
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 이미 존재하는 아이디로 등록 시도
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "login_id": "student01",  # 이미 존재
                "password": "password123",
                "name": "또 다른 학생",
                "role": "student",
                "grade": "middle_1",
                "class_id": "some-class-id",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400
        assert response.json()["detail"]["error"]["code"] == "LOGIN_ID_ALREADY_EXISTS"

    async def test_register_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 등록 시도."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "login_id": "new_student01",
                "password": "password123",
                "name": "새 학생",
                "role": "student",
                "grade": "middle_1",
                "class_id": "some-class-id",
            },
        )

        assert response.status_code == 401

    async def test_register_student_forbidden(self, client: AsyncClient) -> None:
        """학생이 등록 시도 (권한 없음)."""
        # 학생으로 로그인
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 다른 학생 등록 시도
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "login_id": "another_student01",
                "password": "password123",
                "name": "또 다른 학생",
                "role": "student",
                "grade": "middle_1",
                "class_id": "some-class-id",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403
