"""통계 API 테스트 (RED 상태 - 실패하는 테스트)."""

import pytest
from httpx import AsyncClient


class TestGetMyStats:
    """내 통계 조회 테스트."""

    async def test_get_my_stats_success(self, client: AsyncClient) -> None:
        """내 통계 조회 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/stats/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "total_tests" in data["data"]
        assert "accuracy_rate" in data["data"]
        assert "level" in data["data"]
        assert "weak_concepts" in data["data"]
        assert "strong_concepts" in data["data"]

    async def test_get_my_stats_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 조회 시도."""
        response = await client.get("/api/v1/stats/me")
        assert response.status_code == 401


class TestGetStudentStats:
    """학생 통계 목록 조회 테스트 (강사용)."""

    async def test_get_student_stats_success(self, client: AsyncClient) -> None:
        """학생 통계 목록 조회 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/stats/students",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "items" in data["data"]
        assert "total" in data["data"]

    async def test_get_student_stats_with_filter(self, client: AsyncClient) -> None:
        """필터와 함께 학생 통계 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/stats/students?grade=middle_1&sort_by=accuracy&sort_order=desc",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200

    async def test_get_student_stats_forbidden_for_student(self, client: AsyncClient) -> None:
        """학생이 조회 시도 (권한 없음)."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/stats/students",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403


class TestGetStudentDetail:
    """학생 상세 통계 조회 테스트 (강사용)."""

    async def test_get_student_detail_success(self, client: AsyncClient) -> None:
        """학생 상세 통계 조회 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 테스트 데이터의 실제 학생 ID 사용
        student_id = "student-001"
        response = await client.get(
            f"/api/v1/stats/students/{student_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "recent_tests" in data["data"]
        assert "daily_activity" in data["data"]
        assert "weak_concepts" in data["data"]

    async def test_get_student_detail_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 학생 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/stats/students/nonexistent-id",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 404


class TestGetClassStats:
    """반 통계 조회 테스트."""

    async def test_get_class_stats_success(self, client: AsyncClient) -> None:
        """반 통계 조회 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 테스트 데이터의 실제 반 ID 사용
        class_id = "class-001"
        response = await client.get(
            f"/api/v1/stats/class/{class_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "student_count" in data["data"]
        assert "average_accuracy" in data["data"]
        assert "top_students" in data["data"]

    async def test_get_class_stats_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 반 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/stats/class/nonexistent-id",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 404

    async def test_get_class_stats_forbidden(self, client: AsyncClient) -> None:
        """다른 강사의 반 조회 시도 - 존재하지 않는 반은 404."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 존재하지 않는 반 ID -> 404
        other_class_id = "other-teacher-class-id"
        response = await client.get(
            f"/api/v1/stats/class/{other_class_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # 존재하지 않는 반은 404
        assert response.status_code == 404


class TestGetConceptStats:
    """개념별 통계 조회 테스트."""

    async def test_get_concept_stats_success(self, client: AsyncClient) -> None:
        """개념별 통계 조회 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/stats/concepts",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["data"], list)
        if len(data["data"]) > 0:
            assert "concept_name" in data["data"][0]
            assert "accuracy_rate" in data["data"][0]

    async def test_get_concept_stats_with_filter(self, client: AsyncClient) -> None:
        """필터와 함께 개념별 통계 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/stats/concepts?grade=middle_1",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200


class TestGetDashboardStats:
    """대시보드 통계 조회 테스트."""

    async def test_get_dashboard_stats_success(self, client: AsyncClient) -> None:
        """대시보드 통계 조회 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/stats/dashboard",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "today" in data["data"]
        assert "this_week" in data["data"]
        assert "alerts" in data["data"]

    async def test_get_dashboard_stats_forbidden_for_student(
        self, client: AsyncClient
    ) -> None:
        """학생이 대시보드 조회 시도."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/stats/dashboard",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403
