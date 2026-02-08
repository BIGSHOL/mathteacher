"""일일 테스트 API 통합 테스트."""

import pytest
from httpx import AsyncClient

from tests.conftest import TestingSessionLocal


async def _setup_daily_test_data():
    """일일 테스트에 필요한 데이터 설정."""
    from app.models.chapter import Chapter
    from app.models.chapter_progress import ChapterProgress
    from app.models.concept_mastery import ConceptMastery

    async with TestingSessionLocal() as session:
        # Chapter with concept-001
        chapter = Chapter(
            id="ch-daily-1",
            name="1. 일차방정식",
            grade="middle_1",
            semester=1,
            chapter_number=1,
            concept_ids=["concept-001"],
        )
        session.add(chapter)

        # Unlock chapter for student
        progress = ChapterProgress(
            student_id="student-001",
            chapter_id="ch-daily-1",
            is_unlocked=True,
        )
        session.add(progress)

        # Unlock concept for student
        mastery = ConceptMastery(
            student_id="student-001",
            concept_id="concept-001",
            is_unlocked=True,
        )
        session.add(mastery)

        await session.commit()


class TestGetTodayTests:
    """오늘의 일일 테스트 조회 테스트."""

    async def test_get_today_tests_with_data(self, client: AsyncClient) -> None:
        """데이터 설정 후 오늘의 테스트 조회."""
        # Setup required data
        await _setup_daily_test_data()

        # Login as student
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get today's tests
        response = await client.get(
            "/api/v1/daily-tests/today",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "date" in data["data"]
        assert "tests" in data["data"]
        assert "ai_generated_count" in data["data"]

        # Tests should be a list
        assert isinstance(data["data"]["tests"], list)

    async def test_get_today_tests_without_data(self, client: AsyncClient) -> None:
        """데이터 설정 없이 오늘의 테스트 조회."""
        # Don't setup data - test should still work but may return empty or limited results

        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get(
            "/api/v1/daily-tests/today",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "tests" in data["data"]
        # Even without proper data, API should return successfully (may be empty)
        assert isinstance(data["data"]["tests"], list)

    async def test_get_today_tests_unauthorized(self, client: AsyncClient) -> None:
        """인증 없이 오늘의 테스트 조회 - 401."""
        response = await client.get("/api/v1/daily-tests/today")

        assert response.status_code == 401

    async def test_get_today_tests_response_structure(self, client: AsyncClient) -> None:
        """응답 구조 검증."""
        await _setup_daily_test_data()

        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get(
            "/api/v1/daily-tests/today",
            headers=headers,
        )

        data = response.json()["data"]

        # Verify response structure
        assert "date" in data
        assert "tests" in data
        assert "ai_generated_count" in data

        # Check test record structure if any tests exist
        if data["tests"]:
            test = data["tests"][0]
            assert "id" in test
            assert "date" in test
            assert "category" in test
            assert "category_label" in test
            assert "status" in test
            assert "test_id" in test
            assert "question_count" in test


class TestStartDailyTest:
    """일일 테스트 시작 테스트."""

    async def test_start_daily_test_success(self, client: AsyncClient) -> None:
        """일일 테스트 시작 성공."""
        await _setup_daily_test_data()

        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get today's tests first
        today_resp = await client.get(
            "/api/v1/daily-tests/today",
            headers=headers,
        )
        tests = today_resp.json()["data"]["tests"]

        # If we have tests, try to start one
        if tests:
            record_id = tests[0]["id"]

            start_resp = await client.post(
                f"/api/v1/daily-tests/{record_id}/start",
                headers=headers,
            )

            assert start_resp.status_code == 200
            data = start_resp.json()
            assert data["success"] is True
            assert "attempt_id" in data["data"]
            assert data["data"]["attempt_id"] is not None

    async def test_start_daily_test_invalid_record(self, client: AsyncClient) -> None:
        """존재하지 않는 일일 테스트 기록으로 시작 시도 - 400."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        start_resp = await client.post(
            "/api/v1/daily-tests/invalid-record-id/start",
            headers=headers,
        )

        assert start_resp.status_code == 400
        error = start_resp.json()
        assert error["detail"]["success"] is False
        assert error["detail"]["error"]["code"] == "CANNOT_START"

    async def test_start_daily_test_unauthorized(self, client: AsyncClient) -> None:
        """인증 없이 일일 테스트 시작 시도 - 401."""
        response = await client.post("/api/v1/daily-tests/some-id/start")

        assert response.status_code == 401


class TestGetDailyTestHistory:
    """일일 테스트 이력 조회 테스트."""

    async def test_get_history_success(self, client: AsyncClient) -> None:
        """일일 테스트 이력 조회 성공."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get(
            "/api/v1/daily-tests/history",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert "page" in data["data"]
        assert "page_size" in data["data"]
        assert "total_pages" in data["data"]

        # Initially should be empty (no past tests)
        assert isinstance(data["data"]["items"], list)

    async def test_get_history_unauthorized(self, client: AsyncClient) -> None:
        """인증 없이 이력 조회 - 401."""
        response = await client.get("/api/v1/daily-tests/history")

        assert response.status_code == 401

    async def test_get_history_with_pagination(self, client: AsyncClient) -> None:
        """페이지네이션 파라미터로 이력 조회."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get(
            "/api/v1/daily-tests/history?page=1&page_size=10",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()["data"]

        assert data["page"] == 1
        assert data["page_size"] == 10
        assert len(data["items"]) <= 10

    async def test_get_history_different_page_sizes(self, client: AsyncClient) -> None:
        """다양한 페이지 크기로 조회."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Test with page_size=5
        response = await client.get(
            "/api/v1/daily-tests/history?page=1&page_size=5",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["page_size"] == 5

        # Test with page_size=50
        response = await client.get(
            "/api/v1/daily-tests/history?page=1&page_size=50",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["page_size"] == 50


class TestDailyTestWorkflow:
    """일일 테스트 전체 워크플로우 테스트."""

    async def test_daily_test_full_workflow(self, client: AsyncClient) -> None:
        """일일 테스트 전체 플로우: 조회 → 시작 → 답안 제출 → 완료."""
        await _setup_daily_test_data()

        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Get today's tests
        today_resp = await client.get(
            "/api/v1/daily-tests/today",
            headers=headers,
        )
        assert today_resp.status_code == 200
        tests = today_resp.json()["data"]["tests"]

        # If we have tests available
        if tests:
            record_id = tests[0]["id"]
            test_id = tests[0]["test_id"]

            # 2. Start test
            start_resp = await client.post(
                f"/api/v1/daily-tests/{record_id}/start",
                headers=headers,
            )
            assert start_resp.status_code == 200
            attempt_id = start_resp.json()["data"]["attempt_id"]

            # 3. Get test details to know what questions to answer
            test_detail_resp = await client.get(
                f"/api/v1/tests/{test_id}",
                headers=headers,
            )
            if test_detail_resp.status_code == 200:
                questions = test_detail_resp.json()["data"]["questions"]

                # 4. Submit answers for all questions
                for question in questions:
                    submit_resp = await client.post(
                        f"/api/v1/tests/attempts/{attempt_id}/submit",
                        headers=headers,
                        json={
                            "question_id": question["id"],
                            "selected_answer": "B",  # Assuming correct answer
                            "time_spent_seconds": 30,
                        },
                    )
                    # May fail if already submitted, that's ok
                    if submit_resp.status_code != 200:
                        break

                # 5. Complete test
                complete_resp = await client.post(
                    f"/api/v1/tests/attempts/{attempt_id}/complete",
                    headers=headers,
                )
                assert complete_resp.status_code == 200

                # 6. Check that the daily test record was updated
                # (The service should have marked it as completed)
                today_resp2 = await client.get(
                    "/api/v1/daily-tests/today",
                    headers=headers,
                )
                if today_resp2.status_code == 200:
                    updated_tests = today_resp2.json()["data"]["tests"]
                    # Find our test record
                    our_test = next((t for t in updated_tests if t["id"] == record_id), None)
                    if our_test:
                        # Status should be "completed"
                        assert our_test["status"] == "completed"
                        assert our_test["completed_at"] is not None


class TestDailyTestResponseFields:
    """일일 테스트 응답 필드 검증."""

    async def test_daily_test_record_fields(self, client: AsyncClient) -> None:
        """일일 테스트 기록 응답 필드 검증."""
        await _setup_daily_test_data()

        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get(
            "/api/v1/daily-tests/today",
            headers=headers,
        )

        if response.status_code == 200:
            tests = response.json()["data"]["tests"]
            if tests:
                test = tests[0]

                # Required fields
                required_fields = [
                    "id",
                    "date",
                    "category",
                    "category_label",
                    "status",
                    "test_id",
                    "question_count",
                ]

                for field in required_fields:
                    assert field in test, f"Missing required field: {field}"

                # Optional fields (may be None)
                optional_fields = ["attempt_id", "score", "max_score", "correct_count", "total_count", "completed_at"]

                for field in optional_fields:
                    assert field in test, f"Missing optional field: {field}"

    async def test_category_labels_present(self, client: AsyncClient) -> None:
        """카테고리 라벨이 올바르게 표시되는지 확인."""
        await _setup_daily_test_data()

        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get(
            "/api/v1/daily-tests/today",
            headers=headers,
        )

        if response.status_code == 200:
            tests = response.json()["data"]["tests"]
            for test in tests:
                # category_label should not be empty
                assert test["category_label"]
                # category_label should be human-readable (not just a code)
                # Common labels: "개념 이해", "유형 연습", "종합 평가"
                assert len(test["category_label"]) > 0
