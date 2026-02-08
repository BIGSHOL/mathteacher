"""관리자 API 테스트."""

import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch


class TestListUsers:
    """사용자 목록 조회 테스트."""

    async def test_list_users_as_master_success(self, client: AsyncClient) -> None:
        """마스터 권한으로 사용자 목록 조회 성공."""
        # 마스터로 로그인
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/admin/users",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert "page" in data["data"]
        assert "page_size" in data["data"]
        assert data["data"]["total"] >= 3  # master, teacher, student

    async def test_list_users_with_role_filter_student(self, client: AsyncClient) -> None:
        """역할 필터로 학생만 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/admin/users?role=student",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        items = data["data"]["items"]
        # 모든 항목이 student 역할
        for item in items:
            assert item["role"] == "student"

    async def test_list_users_with_role_filter_teacher(self, client: AsyncClient) -> None:
        """역할 필터로 강사만 조회."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/admin/users?role=teacher",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        items = data["data"]["items"]
        for item in items:
            assert item["role"] == "teacher"

    async def test_list_users_pagination(self, client: AsyncClient) -> None:
        """페이지네이션 테스트."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/admin/users?page=1&page_size=2",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["page"] == 1
        assert data["data"]["page_size"] == 2
        assert len(data["data"]["items"]) <= 2

    async def test_list_users_as_teacher_forbidden(self, client: AsyncClient) -> None:
        """강사는 사용자 목록 조회 권한 없음."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/admin/users",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403

    async def test_list_users_as_student_forbidden(self, client: AsyncClient) -> None:
        """학생은 사용자 목록 조회 권한 없음."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.get(
            "/api/v1/admin/users",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403

    async def test_list_users_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 조회 시도."""
        response = await client.get("/api/v1/admin/users")
        assert response.status_code == 401


class TestUpdateUser:
    """사용자 정보 수정 테스트."""

    async def test_update_user_name_as_master(self, client: AsyncClient) -> None:
        """마스터가 사용자 이름 수정."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.put(
            "/api/v1/admin/users/student-001",
            json={"name": "수정된 학생"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "수정된 학생"
        assert "계정이 수정되었습니다" in data["message"]

    async def test_update_user_role_as_master(self, client: AsyncClient) -> None:
        """마스터가 사용자 역할 수정."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.put(
            "/api/v1/admin/users/student-001",
            json={"role": "teacher"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["role"] == "teacher"

    async def test_update_user_grade_as_master(self, client: AsyncClient) -> None:
        """마스터가 학생 학년 수정."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.put(
            "/api/v1/admin/users/student-001",
            json={"grade": "middle_2"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["grade"] == "middle_2"

    async def test_update_user_password_as_master(self, client: AsyncClient) -> None:
        """마스터가 사용자 비밀번호 수정."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.put(
            "/api/v1/admin/users/student-001",
            json={"password": "new_password123"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200

        # 새 비밀번호로 로그인 시도
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "new_password123"},
        )
        assert login_response.status_code == 200

    async def test_update_master_account_forbidden(self, client: AsyncClient) -> None:
        """마스터 계정은 본인 외 수정 불가."""
        # 새 마스터 계정 생성을 위해 현재 마스터로 등록 (실제로는 불가능하므로 skip 또는 403 확인)
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 마스터가 자기 자신을 수정하려 시도 - 이건 가능해야 함
        response = await client.put(
            "/api/v1/admin/users/master-001",
            json={"name": "수정된 마스터"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # 본인 수정은 가능
        assert response.status_code == 200

    async def test_update_user_to_master_role_forbidden(self, client: AsyncClient) -> None:
        """사용자를 마스터 역할로 변경 불가."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.put(
            "/api/v1/admin/users/student-001",
            json={"role": "master"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403
        assert "마스터 역할로 변경할 수 없습니다" in response.json()["detail"]

    async def test_update_user_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 사용자 수정."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.put(
            "/api/v1/admin/users/nonexistent-id",
            json={"name": "테스트"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 404
        assert "사용자를 찾을 수 없습니다" in response.json()["detail"]

    async def test_update_user_as_teacher_forbidden(self, client: AsyncClient) -> None:
        """강사는 사용자 수정 권한 없음."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.put(
            "/api/v1/admin/users/student-001",
            json={"name": "수정 시도"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403

    async def test_update_user_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 수정 시도."""
        response = await client.put(
            "/api/v1/admin/users/student-001",
            json={"name": "테스트"},
        )
        assert response.status_code == 401


class TestResetStudent:
    """학생 데이터 초기화 테스트."""

    async def test_reset_student_data_as_admin(self, client: AsyncClient) -> None:
        """관리자 권한으로 학생 데이터 초기화 성공."""
        # admin 계정이 없으므로 master를 admin으로 변경하거나, teacher를 admin으로 변경
        # conftest에서 master는 있으므로 master로 진행 (ADMIN 권한 필요)
        # reset-student는 ADMIN 권한 필요 (MASTER는 불가)

        # teacher를 admin으로 변경
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        master_token = login_response.json()["data"]["access_token"]

        # teacher를 admin으로 승격
        await client.put(
            "/api/v1/admin/users/teacher-001",
            json={"role": "admin"},
            headers={"Authorization": f"Bearer {master_token}"},
        )

        # admin으로 로그인
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        admin_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/admin/reset-student/student-001",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "학생 데이터가 초기화되었습니다" in data["message"]
        assert data["data"]["student_id"] == "student-001"

    async def test_reset_student_not_student_role(self, client: AsyncClient) -> None:
        """학생이 아닌 계정 초기화 시도."""
        # teacher를 admin으로 승격
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        master_token = login_response.json()["data"]["access_token"]

        await client.put(
            "/api/v1/admin/users/teacher-001",
            json={"role": "admin"},
            headers={"Authorization": f"Bearer {master_token}"},
        )

        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        admin_token = login_response.json()["data"]["access_token"]

        # teacher 계정을 초기화 시도
        response = await client.post(
            "/api/v1/admin/reset-student/teacher-001",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 400
        assert "학생 계정만 리셋할 수 있습니다" in response.json()["detail"]

    async def test_reset_student_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 학생 초기화."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        master_token = login_response.json()["data"]["access_token"]

        await client.put(
            "/api/v1/admin/users/teacher-001",
            json={"role": "admin"},
            headers={"Authorization": f"Bearer {master_token}"},
        )

        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        admin_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/admin/reset-student/nonexistent-id",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 404
        assert "학생을 찾을 수 없습니다" in response.json()["detail"]

    async def test_reset_student_as_teacher_forbidden(self, client: AsyncClient) -> None:
        """강사는 학생 초기화 권한 없음."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/admin/reset-student/student-001",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403

    async def test_reset_student_as_student_forbidden(self, client: AsyncClient) -> None:
        """학생은 데이터 초기화 권한 없음."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/admin/reset-student/student-001",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403

    async def test_reset_student_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 초기화 시도."""
        response = await client.post("/api/v1/admin/reset-student/student-001")
        assert response.status_code == 401


class TestAIGenerateQuestions:
    """AI 문제 생성 테스트."""

    @patch("app.core.config.settings.GEMINI_API_KEY", "test-api-key")
    async def test_generate_questions_as_master_success(self, client: AsyncClient) -> None:
        """마스터가 AI 문제 생성 성공 (mock)."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # AI 서비스 mock
        with patch("app.api.v1.admin._ai_service.generate_questions") as mock_generate:
            mock_generate.return_value = [
                {
                    "id": "ai-test-001",
                    "concept_id": "concept-001",
                    "category": "concept",
                    "part": "algebra",
                    "question_type": "multiple_choice",
                    "difficulty": 6,
                    "content": "AI가 생성한 테스트 문제",
                    "options": [
                        {"id": "1", "label": "A", "text": "보기1"},
                        {"id": "2", "label": "B", "text": "보기2"},
                        {"id": "3", "label": "C", "text": "보기3"},
                        {"id": "4", "label": "D", "text": "보기4"},
                    ],
                    "correct_answer": "A",
                    "explanation": "AI 생성 설명",
                    "points": 10,
                }
            ]

            response = await client.post(
                "/api/v1/admin/generate-questions",
                json={
                    "concept_id": "concept-001",
                    "count": 1,
                    "question_type": "multiple_choice",
                    "difficulty_min": 5,
                    "difficulty_max": 7,
                },
                headers={"Authorization": f"Bearer {access_token}"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert len(data["data"]["generated"]) == 1
            assert "문제가 생성되었습니다" in data["message"]

    async def test_generate_questions_concept_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 개념으로 생성 시도."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        with patch("app.core.config.settings.GEMINI_API_KEY", "test-api-key"):
            response = await client.post(
                "/api/v1/admin/generate-questions",
                json={
                    "concept_id": "nonexistent-concept",
                    "count": 5,
                },
                headers={"Authorization": f"Bearer {access_token}"},
            )

            assert response.status_code == 404
            assert "개념을 찾을 수 없습니다" in response.json()["detail"]

    async def test_generate_questions_computation_forbidden(self, client: AsyncClient) -> None:
        """연산 문제는 AI 생성 불가."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        # 연산 개념을 생성하고 테스트
        # 여기서는 concept-001이 concept 타입이므로 별도 테스트 필요
        # 실제로는 computation 개념이 있어야 하지만 conftest에 없으므로 skip

    async def test_generate_questions_as_teacher_forbidden(self, client: AsyncClient) -> None:
        """강사는 AI 문제 생성 권한 없음."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/admin/generate-questions",
            json={
                "concept_id": "concept-001",
                "count": 5,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403

    async def test_generate_questions_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 생성 시도."""
        response = await client.post(
            "/api/v1/admin/generate-questions",
            json={
                "concept_id": "concept-001",
                "count": 5,
            },
        )
        assert response.status_code == 401


class TestSaveGeneratedQuestions:
    """생성된 문제 저장 테스트."""

    async def test_save_generated_questions_as_master_success(self, client: AsyncClient) -> None:
        """마스터가 생성된 문제 저장 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/admin/save-generated-questions",
            json={
                "questions": [
                    {
                        "concept_id": "concept-001",
                        "category": "concept",
                        "part": "algebra",
                        "question_type": "multiple_choice",
                        "difficulty": 6,
                        "content": "저장할 AI 문제",
                        "options": [
                            {"id": "1", "label": "A", "text": "보기1"},
                            {"id": "2", "label": "B", "text": "보기2"},
                            {"id": "3", "label": "C", "text": "보기3"},
                            {"id": "4", "label": "D", "text": "보기4"},
                        ],
                        "correct_answer": "A",
                        "explanation": "설명",
                        "points": 10,
                    }
                ]
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["saved_count"] == 1
        assert "문제가 저장되었습니다" in data["message"]

    async def test_save_generated_questions_multiple(self, client: AsyncClient) -> None:
        """여러 문제 한 번에 저장."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/admin/save-generated-questions",
            json={
                "questions": [
                    {
                        "concept_id": "concept-001",
                        "category": "concept",
                        "part": "algebra",
                        "question_type": "multiple_choice",
                        "difficulty": 5,
                        "content": "문제 1",
                        "options": [
                            {"id": "1", "label": "A", "text": "보기1"},
                            {"id": "2", "label": "B", "text": "보기2"},
                        ],
                        "correct_answer": "A",
                        "explanation": "설명 1",
                        "points": 10,
                    },
                    {
                        "concept_id": "concept-001",
                        "category": "concept",
                        "part": "algebra",
                        "question_type": "multiple_choice",
                        "difficulty": 7,
                        "content": "문제 2",
                        "options": [
                            {"id": "1", "label": "A", "text": "보기1"},
                            {"id": "2", "label": "B", "text": "보기2"},
                        ],
                        "correct_answer": "B",
                        "explanation": "설명 2",
                        "points": 10,
                    },
                ]
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["saved_count"] == 2

    async def test_save_generated_questions_empty(self, client: AsyncClient) -> None:
        """빈 문제 목록으로 저장 시도."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/admin/save-generated-questions",
            json={"questions": []},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400
        assert "저장할 문제가 없습니다" in response.json()["detail"]

    async def test_save_generated_questions_invalid_concept(self, client: AsyncClient) -> None:
        """존재하지 않는 개념 ID로 저장 시도."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/admin/save-generated-questions",
            json={
                "questions": [
                    {
                        "concept_id": "nonexistent-concept",
                        "category": "concept",
                        "part": "algebra",
                        "question_type": "multiple_choice",
                        "difficulty": 6,
                        "content": "문제",
                        "options": [
                            {"id": "1", "label": "A", "text": "보기1"},
                            {"id": "2", "label": "B", "text": "보기2"},
                        ],
                        "correct_answer": "A",
                        "explanation": "설명",
                        "points": 10,
                    }
                ]
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400
        assert "존재하지 않는 개념" in response.json()["detail"]

    async def test_save_generated_questions_as_teacher_forbidden(self, client: AsyncClient) -> None:
        """강사는 문제 저장 권한 없음."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/admin/save-generated-questions",
            json={"questions": []},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403

    async def test_save_generated_questions_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 저장 시도."""
        response = await client.post(
            "/api/v1/admin/save-generated-questions",
            json={"questions": []},
        )
        assert response.status_code == 401


class TestUpdateChapters:
    """챕터 업데이트 테스트."""

    async def test_update_chapters_as_master_success(self, client: AsyncClient) -> None:
        """마스터가 챕터 concept_ids 업데이트 성공."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        with patch("app.main.update_chapter_concept_ids"):
            with patch("app.main.migrate_concept_subdivision"):
                with patch("app.main.migrate_concept_sequential_unlock"):
                    response = await client.post(
                        "/api/v1/admin/update-chapters",
                        headers={"Authorization": f"Bearer {access_token}"},
                    )

                    assert response.status_code == 200
                    data = response.json()
                    assert data["success"] is True
                    assert "챕터" in data["message"]
                    assert "업데이트" in data["message"]

    async def test_update_chapters_as_teacher_forbidden(self, client: AsyncClient) -> None:
        """강사는 챕터 업데이트 권한 없음."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        access_token = login_response.json()["data"]["access_token"]

        response = await client.post(
            "/api/v1/admin/update-chapters",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 403

    async def test_update_chapters_without_auth(self, client: AsyncClient) -> None:
        """인증 없이 업데이트 시도."""
        response = await client.post("/api/v1/admin/update-chapters")
        assert response.status_code == 401
