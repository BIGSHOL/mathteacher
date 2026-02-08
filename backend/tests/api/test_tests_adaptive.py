"""적응형 테스트 API 통합 테스트."""

import pytest
from httpx import AsyncClient

from tests.conftest import TestingSessionLocal
from app.models.test import Test
from app.models.question import Question


async def _add_adaptive_test():
    """Create an adaptive test with enough questions at different difficulties."""
    async with TestingSessionLocal() as session:
        # Add questions at different difficulties
        for i in range(1, 11):
            q = Question(
                id=f"adaptive-q-{i}",
                concept_id="concept-001",
                category="concept",
                part="algebra",
                question_type="multiple_choice",
                difficulty=i,  # 1-10
                content=f"적응형 문제 {i}",
                options=[
                    {"id": "1", "label": "A", "text": f"선택지A-{i}"},
                    {"id": "2", "label": "B", "text": f"선택지B-{i}"},
                    {"id": "3", "label": "C", "text": f"선택지C-{i}"},
                    {"id": "4", "label": "D", "text": f"선택지D-{i}"},
                ],
                correct_answer="B",
                points=10,
            )
            session.add(q)

        # Create adaptive test
        test = Test(
            id="adaptive-test-001",
            title="적응형 테스트",
            description="적응형 난이도 테스트",
            grade="middle_1",
            concept_ids=["concept-001"],
            question_ids=[f"adaptive-q-{i}" for i in range(1, 11)],
            question_count=5,  # 5 questions per attempt
            time_limit_minutes=15,
            is_active=True,
            is_adaptive=True,
        )
        session.add(test)
        await session.commit()


class TestAdaptiveTestStart:
    """적응형 테스트 시작 테스트."""

    async def test_start_adaptive_test_success(self, client: AsyncClient) -> None:
        """적응형 테스트 시작 성공."""
        # Setup adaptive test
        await _add_adaptive_test()

        # Login as student
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Start adaptive test
        response = await client.post(
            "/api/v1/tests/adaptive-test-001/start",
            headers=headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["is_adaptive"] is True
        assert "current_difficulty" in data["data"]
        assert "attempt_id" in data["data"]

        # Should return only 1 question initially
        test_data = data["data"]["test"]
        assert len(test_data["questions"]) == 1
        assert test_data["is_adaptive"] is True

    async def test_start_adaptive_test_has_initial_difficulty(self, client: AsyncClient) -> None:
        """적응형 테스트는 초기 난이도를 가져야 한다."""
        await _add_adaptive_test()

        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.post(
            "/api/v1/tests/adaptive-test-001/start",
            headers=headers,
        )

        data = response.json()
        current_diff = data["data"]["current_difficulty"]

        # Initial difficulty should be in valid range (1-10)
        assert 1 <= current_diff <= 10


class TestAdaptiveTestSubmitAnswer:
    """적응형 테스트 답안 제출 테스트."""

    async def test_submit_answer_on_adaptive_test(self, client: AsyncClient) -> None:
        """적응형 테스트에서 답안 제출."""
        await _add_adaptive_test()

        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Start test
        start_resp = await client.post(
            "/api/v1/tests/adaptive-test-001/start",
            headers=headers,
        )
        attempt_id = start_resp.json()["data"]["attempt_id"]
        first_question_id = start_resp.json()["data"]["test"]["questions"][0]["id"]

        # Submit answer
        submit_resp = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/submit",
            headers=headers,
            json={
                "question_id": first_question_id,
                "selected_answer": "B",
                "time_spent_seconds": 30,
            },
        )

        assert submit_resp.status_code == 200
        submit_data = submit_resp.json()
        assert submit_data["success"] is True
        assert "is_correct" in submit_data["data"]
        assert "next_difficulty" in submit_data["data"]  # Adaptive specific field


class TestGetNextAdaptiveQuestion:
    """적응형 테스트 다음 문제 조회 테스트."""

    async def test_get_next_question_success(self, client: AsyncClient) -> None:
        """다음 문제 조회 성공."""
        await _add_adaptive_test()

        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Start and submit first answer
        start_resp = await client.post(
            "/api/v1/tests/adaptive-test-001/start",
            headers=headers,
        )
        attempt_id = start_resp.json()["data"]["attempt_id"]
        first_question_id = start_resp.json()["data"]["test"]["questions"][0]["id"]

        await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/submit",
            headers=headers,
            json={
                "question_id": first_question_id,
                "selected_answer": "B",
                "time_spent_seconds": 30,
            },
        )

        # Get next question
        next_resp = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/next",
            headers=headers,
        )

        assert next_resp.status_code == 200
        next_data = next_resp.json()
        assert next_data["success"] is True
        assert "current_difficulty" in next_data["data"]
        assert "questions_answered" in next_data["data"]
        assert "questions_remaining" in next_data["data"]

        # Should have a question
        assert next_data["data"]["question"] is not None
        assert next_data["data"]["is_complete"] is False

    async def test_get_next_question_not_adaptive_error(self, client: AsyncClient) -> None:
        """비적응형 테스트에서 다음 문제 조회 시도 - 에러."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Start normal (non-adaptive) test
        start_resp = await client.post(
            "/api/v1/tests/test-001/start",  # test-001 is not adaptive
            headers=headers,
        )
        attempt_id = start_resp.json()["data"]["attempt_id"]

        # Try to get next question (should fail)
        next_resp = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/next",
            headers=headers,
        )

        assert next_resp.status_code == 400
        error = next_resp.json()
        assert error["detail"]["success"] is False
        assert error["detail"]["error"]["code"] == "NOT_ADAPTIVE"

    async def test_get_next_question_already_completed_error(self, client: AsyncClient) -> None:
        """이미 완료된 테스트에서 다음 문제 조회 - 에러."""
        await _add_adaptive_test()

        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Start adaptive test
        start_resp = await client.post(
            "/api/v1/tests/adaptive-test-001/start",
            headers=headers,
        )
        attempt_id = start_resp.json()["data"]["attempt_id"]

        # Complete the test immediately
        await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/complete",
            headers=headers,
        )

        # Try to get next question (should fail)
        next_resp = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/next",
            headers=headers,
        )

        assert next_resp.status_code == 400
        error = next_resp.json()
        assert error["detail"]["success"] is False
        assert error["detail"]["error"]["code"] == "ALREADY_COMPLETED"

    async def test_get_next_question_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 시도로 다음 문제 조회 - 404."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        next_resp = await client.post(
            "/api/v1/tests/attempts/nonexistent-id/next",
            headers=headers,
        )

        assert next_resp.status_code == 404
        error = next_resp.json()
        assert error["detail"]["error"]["code"] == "NOT_FOUND"

    async def test_get_next_question_forbidden(self, client: AsyncClient) -> None:
        """다른 사용자의 시도로 다음 문제 조회 - 403."""
        await _add_adaptive_test()

        # Create another student
        async with TestingSessionLocal() as session:
            from app.models.user import User
            from app.services.auth_service import AuthService
            auth_service = AuthService()

            student2 = User(
                id="student-002",
                login_id="student02",
                name="테스트 학생2",
                role="student",
                grade="middle_1",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
                level=1,
                total_xp=0,
                current_streak=0,
                max_streak=0,
            )
            session.add(student2)
            await session.commit()

        # Student 1 starts test
        login1 = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token1 = login1.json()["data"]["access_token"]

        start_resp = await client.post(
            "/api/v1/tests/adaptive-test-001/start",
            headers={"Authorization": f"Bearer {token1}"},
        )
        attempt_id = start_resp.json()["data"]["attempt_id"]

        # Student 2 tries to access student 1's attempt
        login2 = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student02", "password": "password123"},
        )
        token2 = login2.json()["data"]["access_token"]

        next_resp = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/next",
            headers={"Authorization": f"Bearer {token2}"},
        )

        assert next_resp.status_code == 403
        error = next_resp.json()
        assert error["detail"]["error"]["code"] == "FORBIDDEN"


class TestFullAdaptiveFlow:
    """적응형 테스트 전체 플로우 테스트."""

    async def test_complete_adaptive_flow(self, client: AsyncClient) -> None:
        """적응형 테스트 전체 플로우: 시작 → 제출 → 다음 → ... → 완료."""
        await _add_adaptive_test()

        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Start test
        start_resp = await client.post(
            "/api/v1/tests/adaptive-test-001/start",
            headers=headers,
        )
        assert start_resp.status_code == 201
        attempt_id = start_resp.json()["data"]["attempt_id"]

        # 2. Go through 5 questions
        total_questions = 5
        questions_answered = 0

        for i in range(total_questions):
            # Get current or next question
            if i == 0:
                # First question is from start response
                question_id = start_resp.json()["data"]["test"]["questions"][0]["id"]
            else:
                # Get next question
                next_resp = await client.post(
                    f"/api/v1/tests/attempts/{attempt_id}/next",
                    headers=headers,
                )
                assert next_resp.status_code == 200
                next_data = next_resp.json()["data"]

                if next_data["is_complete"]:
                    break

                question_id = next_data["question"]["id"]

            # Submit answer (always correct)
            submit_resp = await client.post(
                f"/api/v1/tests/attempts/{attempt_id}/submit",
                headers=headers,
                json={
                    "question_id": question_id,
                    "selected_answer": "B",
                    "time_spent_seconds": 30,
                },
            )

            # Allow for test completion scenarios
            if submit_resp.status_code == 200:
                questions_answered += 1
            elif submit_resp.status_code == 400:
                # May hit "already completed" or "already submitted" errors
                error = submit_resp.json()
                error_code = error["detail"]["error"]["code"]
                if error_code in ("ALREADY_COMPLETED", "ALREADY_SUBMITTED"):
                    # Test is complete or question was already handled
                    break
                # Otherwise, this is an actual error
                assert False, f"Unexpected error: {error}"

        # 3. Complete test (if not already completed)
        complete_resp = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/complete",
            headers=headers,
        )

        # Either success or already completed
        assert complete_resp.status_code in [200, 400]

        if complete_resp.status_code == 200:
            complete_data = complete_resp.json()
            assert complete_data["success"] is True

            # Verify attempt data
            attempt_data = complete_data["data"]["attempt"]
            assert attempt_data["completed_at"] is not None
            assert attempt_data["is_adaptive"] is True


class TestSubmitAnswerEdgeCases:
    """답안 제출 엣지 케이스 테스트."""

    async def test_submit_to_completed_attempt_error(self, client: AsyncClient) -> None:
        """이미 완료된 시도에 답안 제출 - 에러."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Start test
        start_resp = await client.post(
            "/api/v1/tests/test-001/start",
            headers=headers,
        )
        attempt_id = start_resp.json()["data"]["attempt_id"]

        # Complete the test
        await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/complete",
            headers=headers,
        )

        # Try to submit answer
        submit_resp = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/submit",
            headers=headers,
            json={
                "question_id": "question-001",
                "selected_answer": "B",
                "time_spent_seconds": 30,
            },
        )

        assert submit_resp.status_code == 400
        error = submit_resp.json()
        assert error["detail"]["error"]["code"] == "ALREADY_COMPLETED"

    async def test_submit_to_nonexistent_attempt_error(self, client: AsyncClient) -> None:
        """존재하지 않는 시도에 답안 제출 - 404."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        submit_resp = await client.post(
            "/api/v1/tests/attempts/nonexistent-id/submit",
            headers=headers,
            json={
                "question_id": "question-001",
                "selected_answer": "B",
                "time_spent_seconds": 30,
            },
        )

        assert submit_resp.status_code == 404
        error = submit_resp.json()
        assert error["detail"]["error"]["code"] == "NOT_FOUND"

    async def test_submit_for_wrong_user_attempt_error(self, client: AsyncClient) -> None:
        """다른 사용자의 시도에 답안 제출 - 403."""
        # Create another student
        async with TestingSessionLocal() as session:
            from app.models.user import User
            from app.services.auth_service import AuthService
            auth_service = AuthService()

            student2 = User(
                id="student-003",
                login_id="student03",
                name="테스트 학생3",
                role="student",
                grade="middle_1",
                hashed_password=auth_service.hash_password("password123"),
                is_active=True,
                level=1,
                total_xp=0,
                current_streak=0,
                max_streak=0,
            )
            session.add(student2)
            await session.commit()

        # Student 1 starts test
        login1 = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token1 = login1.json()["data"]["access_token"]

        start_resp = await client.post(
            "/api/v1/tests/test-001/start",
            headers={"Authorization": f"Bearer {token1}"},
        )
        attempt_id = start_resp.json()["data"]["attempt_id"]

        # Student 2 tries to submit for student 1's attempt
        login2 = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student03", "password": "password123"},
        )
        token2 = login2.json()["data"]["access_token"]

        submit_resp = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/submit",
            headers={"Authorization": f"Bearer {token2}"},
            json={
                "question_id": "question-001",
                "selected_answer": "B",
                "time_spent_seconds": 30,
            },
        )

        assert submit_resp.status_code == 403
        error = submit_resp.json()
        assert error["detail"]["error"]["code"] == "FORBIDDEN"

    async def test_submit_already_answered_question_error(self, client: AsyncClient) -> None:
        """이미 답안을 제출한 문제에 재제출 - 에러."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Start test
        start_resp = await client.post(
            "/api/v1/tests/test-001/start",
            headers=headers,
        )
        attempt_id = start_resp.json()["data"]["attempt_id"]

        # Submit answer once
        await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/submit",
            headers=headers,
            json={
                "question_id": "question-001",
                "selected_answer": "B",
                "time_spent_seconds": 30,
            },
        )

        # Try to submit again for the same question
        submit_resp = await client.post(
            f"/api/v1/tests/attempts/{attempt_id}/submit",
            headers=headers,
            json={
                "question_id": "question-001",
                "selected_answer": "A",
                "time_spent_seconds": 10,
            },
        )

        assert submit_resp.status_code == 400
        error = submit_resp.json()
        assert error["detail"]["error"]["code"] == "ALREADY_SUBMITTED"
