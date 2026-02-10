"""테스트 API 테스트."""

import pytest
from httpx import AsyncClient


class TestGetAvailableTests:
    """풀 수 있는 테스트 목록 조회 테스트."""

    async def test_get_available_tests_success(self, client: AsyncClient) -> None:
        """테스트 목록 조회 성공."""
        # 학생으로 로그인
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/tests/available",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert "page" in data["data"]

    async def test_get_available_tests_with_grade_filter(self, client: AsyncClient) -> None:
        """학년 필터로 테스트 목록 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/tests/available?grade=middle_1",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        # 모든 테스트가 해당 학년인지 확인
        for test in data["data"]["items"]:
            assert test["grade"] == "middle_1"

    async def test_get_available_tests_pagination(self, client: AsyncClient) -> None:
        """페이지네이션 테스트."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/tests/available?page=1&page_size=5",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) <= 5
        assert data["data"]["page"] == 1

    async def test_get_available_tests_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 조회 시도."""
        response = await client.get("/api/v1/tests/available")
        assert response.status_code == 401


class TestGetTestDetail:
    """테스트 상세 조회 테스트."""

    async def test_get_test_detail_success(self, client: AsyncClient) -> None:
        """테스트 상세 조회 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        test_id = "test-001"  # fixture의 테스트 ID
        response = await client.get(
            f"/api/v1/tests/{test_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "questions" in data["data"]
        # 정답이 노출되지 않아야 함
        for question in data["data"]["questions"]:
            assert question.get("correct_answer") is None

    async def test_get_test_detail_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 테스트 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/tests/nonexistent-id",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 404


class TestStartTest:
    """테스트 시작 테스트."""

    async def test_start_test_success(self, client: AsyncClient) -> None:
        """테스트 시작 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        test_id = "test-001"
        response = await client.post(
            f"/api/v1/tests/{test_id}/start",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert "attempt_id" in data["data"]
        assert "test" in data["data"]
        assert "started_at" in data["data"]

    async def test_start_test_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 테스트 시작."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/tests/nonexistent-id/start",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 404


class TestSubmitAnswer:
    """답안 제출 테스트."""

    async def test_submit_answer_correct(self, client: AsyncClient) -> None:
        """정답 제출."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 테스트 시작
        test_id = "test-001"
        start_response = await client.post(
            f"/api/v1/tests/{test_id}/start",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        attempt_id = start_response.json()["data"]["attempt_id"]
        question_id = start_response.json()["data"]["test"]["questions"][0]["id"]

        # 정답 제출 (question-001의 정답은 "B")
        response = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/submit",
            json={
                "question_id": question_id,
                "selected_answer": "B",
                "time_spent_seconds": 15,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["is_correct"] is True
        assert "correct_answer" in data["data"]
        assert "explanation" in data["data"]
        assert data["data"]["points_earned"] > 0

    async def test_submit_answer_incorrect(self, client: AsyncClient) -> None:
        """오답 제출."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 테스트 시작
        test_id = "test-001"
        start_response = await client.post(
            f"/api/v1/tests/{test_id}/start",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        attempt_id = start_response.json()["data"]["attempt_id"]
        question_id = start_response.json()["data"]["test"]["questions"][0]["id"]

        # 오답 제출 (question-001의 정답은 "B", "A"는 오답)
        response = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/submit",
            json={
                "question_id": question_id,
                "selected_answer": "A",
                "time_spent_seconds": 20,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["is_correct"] is False
        assert data["data"]["points_earned"] == 0

    async def test_submit_answer_combo(self, client: AsyncClient) -> None:
        """연속 정답 시 콤보 증가."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 테스트 시작
        test_id = "test-001"
        start_response = await client.post(
            f"/api/v1/tests/{test_id}/start",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        attempt_id = start_response.json()["data"]["attempt_id"]
        questions = start_response.json()["data"]["test"]["questions"]

        # 첫 번째 정답 (question-001의 정답은 "B")
        response1 = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/submit",
            json={
                "question_id": questions[0]["id"],
                "selected_answer": "B",
                "time_spent_seconds": 10,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response1.json()["data"]["combo_count"] == 1

        # 두 번째 연속 정답 (question-002의 정답도 "B")
        response2 = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/submit",
            json={
                "question_id": questions[1]["id"],
                "selected_answer": "B",
                "time_spent_seconds": 10,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response2.json()["data"]["combo_count"] == 2

    async def test_submit_answer_already_submitted(self, client: AsyncClient) -> None:
        """이미 제출한 문제 재제출 시도."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        test_id = "test-001"
        start_response = await client.post(
            f"/api/v1/tests/{test_id}/start",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        attempt_id = start_response.json()["data"]["attempt_id"]
        question_id = start_response.json()["data"]["test"]["questions"][0]["id"]

        # 첫 번째 제출
        await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/submit",
            json={
                "question_id": question_id,
                "selected_answer": "B",
                "time_spent_seconds": 10,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # 같은 문제 재제출
        response = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/submit",
            json={
                "question_id": question_id,
                "selected_answer": "A",
                "time_spent_seconds": 5,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400
        assert response.json()["detail"]["error"]["code"] == "ALREADY_SUBMITTED"


class TestCompleteTest:
    """테스트 완료 테스트."""

    async def test_complete_test_success(self, client: AsyncClient) -> None:
        """테스트 완료 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 테스트 시작 및 모든 문제 풀기
        test_id = "test-001"
        start_response = await client.post(
            f"/api/v1/tests/{test_id}/start",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        attempt_id = start_response.json()["data"]["attempt_id"]

        # 테스트 완료
        response = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/complete",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "attempt" in data["data"]
        assert "answers" in data["data"]
        assert "xp_earned" in data["data"]
        assert "level_up" in data["data"]

    async def test_complete_test_already_completed(self, client: AsyncClient) -> None:
        """이미 완료된 테스트 재완료 시도."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        test_id = "test-001"
        start_response = await client.post(
            f"/api/v1/tests/{test_id}/start",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        attempt_id = start_response.json()["data"]["attempt_id"]

        # 첫 번째 완료
        await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/complete",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # 재완료 시도
        response = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/complete",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400
        assert response.json()["detail"]["error"]["code"] == "ALREADY_COMPLETED"


class TestGetAttempt:
    """시도 결과 조회 테스트."""

    async def test_get_attempt_success(self, client: AsyncClient) -> None:
        """시도 결과 조회 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 먼저 테스트 시작하여 attempt 생성
        test_id = "test-001"
        start_response = await client.post(
            f"/api/v1/tests/{test_id}/start",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        attempt_id = start_response.json()["data"]["attempt_id"]

        response = await client.get(
            f"/api/v1/tests/attempts/{attempt_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "attempt" in data["data"]
        assert "answers" in data["data"]
        assert "test" in data["data"]

    async def test_get_attempt_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 시도 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/tests/attempts/nonexistent-id",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 404
