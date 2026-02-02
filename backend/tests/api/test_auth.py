"""인증 API 테스트 (RED 상태 - 실패하는 테스트)."""

import pytest
from fastapi.testclient import TestClient


class TestLogin:
    """로그인 API 테스트."""

    def test_login_success(self, client: TestClient) -> None:
        """유효한 자격증명으로 로그인 성공."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "student@test.com", "password": "password123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"
        assert "user" in data["data"]
        assert data["data"]["user"]["email"] == "student@test.com"

    def test_login_invalid_password(self, client: TestClient) -> None:
        """잘못된 비밀번호로 로그인 실패."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "student@test.com", "password": "wrong_password"},
        )

        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["success"] is False
        assert data["detail"]["error"]["code"] == "INVALID_CREDENTIALS"

    def test_login_nonexistent_user(self, client: TestClient) -> None:
        """존재하지 않는 사용자 로그인 실패."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@test.com", "password": "password123"},
        )

        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["success"] is False

    def test_login_invalid_email_format(self, client: TestClient) -> None:
        """유효하지 않은 이메일 형식."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "invalid-email", "password": "password123"},
        )

        assert response.status_code == 422


class TestTokenRefresh:
    """토큰 갱신 API 테스트."""

    def test_refresh_token_success(self, client: TestClient) -> None:
        """유효한 refresh token으로 갱신 성공."""
        # 먼저 로그인
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "student@test.com", "password": "password123"},
        )
        refresh_token = login_response.json()["data"]["refresh_token"]

        # 토큰 갱신
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]

    def test_refresh_token_invalid(self, client: TestClient) -> None:
        """유효하지 않은 refresh token."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token"},
        )

        assert response.status_code == 401

    def test_refresh_token_expired(self, client: TestClient) -> None:
        """만료된 refresh token."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "expired_token"},
        )

        assert response.status_code == 401


class TestLogout:
    """로그아웃 API 테스트."""

    def test_logout_success(self, client: TestClient) -> None:
        """로그아웃 성공."""
        # 먼저 로그인
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "student@test.com", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]
        refresh_token = login_response.json()["data"]["refresh_token"]

        # 로그아웃
        response = client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": refresh_token},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        assert response.json()["data"]["message"] == "로그아웃 성공"

    def test_logout_without_auth(self, client: TestClient) -> None:
        """인증 없이 로그아웃 시도."""
        response = client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": "some_token"},
        )

        assert response.status_code == 401


class TestGetMe:
    """현재 사용자 정보 조회 테스트."""

    def test_get_me_success(self, client: TestClient) -> None:
        """인증된 사용자 정보 조회."""
        # 먼저 로그인
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "student@test.com", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 내 정보 조회
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["email"] == "student@test.com"

    def test_get_me_without_auth(self, client: TestClient) -> None:
        """인증 없이 조회 시도."""
        response = client.get("/api/v1/auth/me")

        assert response.status_code == 401

    def test_get_me_invalid_token(self, client: TestClient) -> None:
        """유효하지 않은 토큰으로 조회."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401


class TestRegister:
    """사용자 등록 테스트 (강사 전용)."""

    def test_register_student_success(self, client: TestClient) -> None:
        """학생 등록 성공 (강사 권한)."""
        # 강사로 로그인
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "teacher@test.com", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 학생 등록
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newstudent@test.com",
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
        assert data["data"]["user"]["email"] == "newstudent@test.com"

    def test_register_duplicate_email(self, client: TestClient) -> None:
        """중복 이메일로 등록 실패."""
        # 강사로 로그인
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "teacher@test.com", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 이미 존재하는 이메일로 등록 시도
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "student@test.com",  # 이미 존재
                "password": "password123",
                "name": "또 다른 학생",
                "role": "student",
                "grade": "middle_1",
                "class_id": "some-class-id",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400
        assert response.json()["detail"]["error"]["code"] == "EMAIL_ALREADY_EXISTS"

    def test_register_without_auth(self, client: TestClient) -> None:
        """인증 없이 등록 시도."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newstudent@test.com",
                "password": "password123",
                "name": "새 학생",
                "role": "student",
                "grade": "middle_1",
                "class_id": "some-class-id",
            },
        )

        assert response.status_code == 401

    def test_register_student_forbidden(self, client: TestClient) -> None:
        """학생이 등록 시도 (권한 없음)."""
        # 학생으로 로그인
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "student@test.com", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 다른 학생 등록 시도
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "anotherstudent@test.com",
                "password": "password123",
                "name": "또 다른 학생",
                "role": "student",
                "grade": "middle_1",
                "class_id": "some-class-id",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403
