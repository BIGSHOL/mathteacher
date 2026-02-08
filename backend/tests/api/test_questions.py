"""문제 API 테스트."""

import pytest
from httpx import AsyncClient


class TestListQuestions:
    """문제 목록 조회 테스트."""

    async def test_list_questions_success(self, client: AsyncClient) -> None:
        """문제 목록 조회 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/questions",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert "page" in data["data"]

    async def test_list_questions_with_concept_filter(self, client: AsyncClient) -> None:
        """개념 필터로 문제 목록 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/questions?concept_id=concept-001",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        # 모든 문제가 해당 개념인지 확인
        for question in data["data"]["items"]:
            assert question["concept_id"] == "concept-001"

    async def test_list_questions_with_grade_filter(self, client: AsyncClient) -> None:
        """학년 필터로 문제 목록 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/questions?grade=middle_1",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        # 모든 문제가 해당 학년인지 확인
        for question in data["data"]["items"]:
            assert question["grade"] == "middle_1"

    async def test_list_questions_with_difficulty_filter(self, client: AsyncClient) -> None:
        """난이도 필터로 문제 목록 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/questions?difficulty=6",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        for question in data["data"]["items"]:
            assert question["difficulty"] == 6

    async def test_list_questions_with_category_filter(self, client: AsyncClient) -> None:
        """카테고리 필터로 문제 목록 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/questions?category=concept",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        for question in data["data"]["items"]:
            assert question["category"] == "concept"

    async def test_list_questions_pagination(self, client: AsyncClient) -> None:
        """페이지네이션 테스트."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/questions?page=1&page_size=2",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) <= 2
        assert data["data"]["page"] == 1
        assert data["data"]["page_size"] == 2

    async def test_list_questions_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 조회 시도."""
        response = await client.get("/api/v1/questions")
        assert response.status_code == 401


class TestGetQuestionsByConcept:
    """개념별 문제 조회 테스트."""

    async def test_get_questions_by_concept_success(self, client: AsyncClient) -> None:
        """특정 개념의 문제 조회 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/questions/by-concept/concept-001",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)
        # 모든 문제가 해당 개념인지 확인
        for question in data["data"]:
            assert question["concept_id"] == "concept-001"

    async def test_get_questions_by_concept_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 개념으로 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/questions/by-concept/nonexistent-concept",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 404

    async def test_get_questions_by_concept_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 조회 시도."""
        response = await client.get("/api/v1/questions/by-concept/concept-001")
        assert response.status_code == 401


class TestGetFilterOptions:
    """필터 옵션 조회 테스트."""

    async def test_get_filter_options_success(self, client: AsyncClient) -> None:
        """필터 옵션 조회 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/questions/filter-options",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "chapters" in data["data"]
        assert "concepts" in data["data"]

    async def test_get_filter_options_with_grade(self, client: AsyncClient) -> None:
        """학년 필터로 옵션 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/questions/filter-options?grade=middle_1",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        # 모든 챕터와 개념이 해당 학년인지 확인
        for chapter in data["data"]["chapters"]:
            assert chapter["grade"] == "middle_1"
        for concept in data["data"]["concepts"]:
            assert concept["grade"] == "middle_1"

    async def test_get_filter_options_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 조회 시도."""
        response = await client.get("/api/v1/questions/filter-options")
        assert response.status_code == 401


class TestCreateQuestion:
    """문제 생성 테스트."""

    async def test_create_question_success(self, client: AsyncClient) -> None:
        """문제 생성 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/questions",
            json={
                "concept_id": "concept-001",
                "category": "concept",
                "part": "algebra",
                "question_type": "multiple_choice",
                "difficulty": 7,
                "content": "새로운 문제",
                "options": [
                    {"id": "1", "label": "A", "text": "보기1"},
                    {"id": "2", "label": "B", "text": "보기2"},
                    {"id": "3", "label": "C", "text": "보기3"},
                    {"id": "4", "label": "D", "text": "보기4"},
                ],
                "correct_answer": "A",
                "explanation": "설명",
                "points": 10,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["content"] == "새로운 문제"
        assert data["data"]["concept_id"] == "concept-001"

    async def test_create_question_concept_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 개념으로 문제 생성."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/questions",
            json={
                "concept_id": "nonexistent-concept",
                "category": "concept",
                "part": "algebra",
                "question_type": "multiple_choice",
                "difficulty": 7,
                "content": "새로운 문제",
                "options": [
                    {"id": "1", "label": "A", "text": "보기1"},
                    {"id": "2", "label": "B", "text": "보기2"},
                ],
                "correct_answer": "A",
                "explanation": "설명",
                "points": 10,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 404

    async def test_create_question_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 문제 생성 시도."""
        response = await client.post(
            "/api/v1/questions",
            json={
                "concept_id": "concept-001",
                "category": "concept",
                "part": "algebra",
                "question_type": "multiple_choice",
                "difficulty": 7,
                "content": "새로운 문제",
                "correct_answer": "A",
                "explanation": "설명",
                "points": 10,
            },
        )
        assert response.status_code == 401

    async def test_create_question_student_forbidden(self, client: AsyncClient) -> None:
        """학생이 문제 생성 시도."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/questions",
            json={
                "concept_id": "concept-001",
                "category": "concept",
                "part": "algebra",
                "question_type": "multiple_choice",
                "difficulty": 7,
                "content": "새로운 문제",
                "correct_answer": "A",
                "explanation": "설명",
                "points": 10,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403


class TestQuestionStats:
    """문제 통계 테스트."""

    async def test_get_question_stats_success(self, client: AsyncClient) -> None:
        """문제 통계 조회 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/questions/stats",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "total" in data["data"]
        assert "by_concept" in data["data"]
        assert isinstance(data["data"]["by_concept"], dict)

    async def test_get_question_stats_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 통계 조회 시도."""
        response = await client.get("/api/v1/questions/stats")
        assert response.status_code == 401

    async def test_get_question_stats_student_forbidden(self, client: AsyncClient) -> None:
        """학생이 통계 조회 시도."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/questions/stats",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403
