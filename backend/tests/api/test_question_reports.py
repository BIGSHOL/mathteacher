"""문제 신고 API 테스트."""

import pytest
from httpx import AsyncClient


class TestCreateQuestionReport:
    """문제 신고 생성 테스트."""

    async def test_create_report_as_student(self, client: AsyncClient) -> None:
        """학생이 문제 신고 생성."""
        # 학생으로 로그인
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 문제 신고
        response = await client.post(
            "/api/v1/question-reports",
            headers=headers,
            json={
                "question_id": "question-001",
                "report_type": "wrong_answer",
                "comment": "정답이 틀린 것 같습니다.",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["question_id"] == "question-001"
        assert data["data"]["report_type"] == "wrong_answer"
        assert data["data"]["comment"] == "정답이 틀린 것 같습니다."
        assert data["data"]["status"] == "pending"
        assert data["data"]["reporter_id"] == "student-001"

    async def test_create_report_as_teacher(self, client: AsyncClient) -> None:
        """강사도 문제 신고 가능."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.post(
            "/api/v1/question-reports",
            headers=headers,
            json={
                "question_id": "question-002",
                "report_type": "wrong_options",
                "comment": "선지에 오타가 있습니다.",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["report_type"] == "wrong_options"

    async def test_create_report_question_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 문제 신고."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.post(
            "/api/v1/question-reports",
            headers=headers,
            json={
                "question_id": "nonexistent-id",
                "report_type": "wrong_answer",
                "comment": "이 문제는 존재하지 않습니다.",
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"]["error"]["code"] == "QUESTION_NOT_FOUND"

    async def test_create_duplicate_report(self, client: AsyncClient) -> None:
        """중복 신고 시 기존 신고 반환."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 첫 번째 신고
        response1 = await client.post(
            "/api/v1/question-reports",
            headers=headers,
            json={
                "question_id": "question-001",
                "report_type": "wrong_answer",
                "comment": "첫 번째 신고입니다.",
            },
        )
        assert response1.status_code == 201
        report_id1 = response1.json()["data"]["id"]

        # 같은 문제에 대한 중복 신고 (pending 상태)
        response2 = await client.post(
            "/api/v1/question-reports",
            headers=headers,
            json={
                "question_id": "question-001",
                "report_type": "question_error",
                "comment": "두 번째 신고입니다.",
            },
        )

        assert response2.status_code == 201
        report_id2 = response2.json()["data"]["id"]
        # 기존 신고 반환
        assert report_id1 == report_id2

    async def test_create_report_unauthorized(self, client: AsyncClient) -> None:
        """인증 없이 신고 생성 시도."""
        response = await client.post(
            "/api/v1/question-reports",
            json={
                "question_id": "question-001",
                "report_type": "wrong_answer",
                "comment": "인증 없는 신고",
            },
        )

        assert response.status_code == 401

    async def test_create_report_with_various_types(self, client: AsyncClient) -> None:
        """다양한 신고 유형 테스트."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 각 신고 유형마다 다른 question_id 사용 (중복 방지)
        test_cases = [
            ("question-001", "wrong_answer"),
            ("question-002", "wrong_options"),
            ("question-003", "question_error"),
            # question-001을 재사용하면 중복 신고 처리되므로 새 테스트에서는 다른 question 사용
            # 하지만 question이 3개밖에 없으므로, "other" 타입은 이미 신고된 question 사용
            # 단, 이미 신고된 question에 대해서는 기존 report를 반환하므로 report_type이 다를 수 있음
            # 따라서 이 테스트는 각 유형이 생성 가능한지만 확인
        ]

        # 각 question에 첫 신고만 확인
        for question_id, report_type in test_cases:
            response = await client.post(
                "/api/v1/question-reports",
                headers=headers,
                json={
                    "question_id": question_id,
                    "report_type": report_type,
                    "comment": f"신고 유형: {report_type}",
                },
            )

            assert response.status_code == 201
            data = response.json()
            # 중복 신고가 아닌 경우 report_type이 요청한 것과 일치
            assert data["data"]["report_type"] == report_type


class TestListQuestionReports:
    """문제 신고 목록 조회 테스트."""

    async def test_list_reports_as_teacher(self, client: AsyncClient) -> None:
        """강사가 신고 목록 조회."""
        # 학생이 먼저 신고 생성
        student_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        student_token = student_login.json()["data"]["access_token"]
        await client.post(
            "/api/v1/question-reports",
            headers={"Authorization": f"Bearer {student_token}"},
            json={
                "question_id": "question-001",
                "report_type": "wrong_answer",
                "comment": "신고 테스트",
            },
        )

        # 강사로 목록 조회
        teacher_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        teacher_token = teacher_login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {teacher_token}"}

        response = await client.get(
            "/api/v1/question-reports",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert data["data"]["total"] >= 1

    async def test_list_reports_as_master(self, client: AsyncClient) -> None:
        """마스터 관리자가 신고 목록 조회."""
        # 학생이 먼저 신고 생성
        student_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        student_token = student_login.json()["data"]["access_token"]
        await client.post(
            "/api/v1/question-reports",
            headers={"Authorization": f"Bearer {student_token}"},
            json={
                "question_id": "question-002",
                "report_type": "wrong_options",
                "comment": "선지 오류",
            },
        )

        # 마스터로 목록 조회
        master_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        master_token = master_login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {master_token}"}

        response = await client.get(
            "/api/v1/question-reports",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["total"] >= 1

    async def test_list_reports_with_status_filter(self, client: AsyncClient) -> None:
        """상태 필터로 신고 목록 조회."""
        # 신고 생성
        student_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        student_token = student_login.json()["data"]["access_token"]
        await client.post(
            "/api/v1/question-reports",
            headers={"Authorization": f"Bearer {student_token}"},
            json={
                "question_id": "question-003",
                "report_type": "other",
                "comment": "기타 문의",
            },
        )

        # 강사로 pending 상태만 조회
        teacher_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        teacher_token = teacher_login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {teacher_token}"}

        response = await client.get(
            "/api/v1/question-reports?status=pending",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        # 모든 항목이 pending 상태여야 함
        for item in data["data"]["items"]:
            assert item["status"] == "pending"

    async def test_list_reports_pagination(self, client: AsyncClient) -> None:
        """페이지네이션 테스트."""
        # 여러 신고 생성 - 각각 다른 question 사용
        student_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        student_token = student_login.json()["data"]["access_token"]

        # 3개 문제에만 신고 가능
        for i in range(3):
            await client.post(
                "/api/v1/question-reports",
                headers={"Authorization": f"Bearer {student_token}"},
                json={
                    "question_id": f"question-00{i + 1}",
                    "report_type": "other",
                    "comment": f"신고 {i+1}",
                },
            )

        # 강사로 페이지네이션 조회
        teacher_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        teacher_token = teacher_login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {teacher_token}"}

        response = await client.get(
            "/api/v1/question-reports?page=1&page_size=3",
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) <= 3
        assert data["data"]["page"] == 1
        assert data["data"]["page_size"] == 3

    async def test_list_reports_forbidden_for_student(self, client: AsyncClient) -> None:
        """학생은 신고 목록 조회 불가."""
        login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get(
            "/api/v1/question-reports",
            headers=headers,
        )

        assert response.status_code == 403

    async def test_list_reports_unauthorized(self, client: AsyncClient) -> None:
        """인증 없이 목록 조회 시도."""
        response = await client.get("/api/v1/question-reports")
        assert response.status_code == 401


class TestResolveQuestionReport:
    """문제 신고 처리 테스트."""

    async def test_resolve_report_as_master(self, client: AsyncClient) -> None:
        """마스터가 신고 처리 (resolved)."""
        # 학생이 신고 생성
        student_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        student_token = student_login.json()["data"]["access_token"]
        create_response = await client.post(
            "/api/v1/question-reports",
            headers={"Authorization": f"Bearer {student_token}"},
            json={
                "question_id": "question-001",
                "report_type": "wrong_answer",
                "comment": "정답이 틀렸습니다.",
            },
        )
        report_id = create_response.json()["data"]["id"]

        # 마스터로 처리
        master_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        master_token = master_login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {master_token}"}

        response = await client.patch(
            f"/api/v1/question-reports/{report_id}/resolve",
            headers=headers,
            json={
                "status": "resolved",
                "admin_response": "정답을 수정했습니다.",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "resolved"
        assert data["data"]["admin_response"] == "정답을 수정했습니다."
        assert data["data"]["resolved_by"] == "master-001"
        assert data["data"]["resolved_at"] is not None

    async def test_resolve_report_dismissed(self, client: AsyncClient) -> None:
        """신고 기각 (dismissed)."""
        # 학생이 신고 생성
        student_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        student_token = student_login.json()["data"]["access_token"]
        create_response = await client.post(
            "/api/v1/question-reports",
            headers={"Authorization": f"Bearer {student_token}"},
            json={
                "question_id": "question-002",
                "report_type": "wrong_answer",
                "comment": "정답이 틀린 것 같습니다.",
            },
        )
        report_id = create_response.json()["data"]["id"]

        # 마스터로 기각
        master_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        master_token = master_login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {master_token}"}

        response = await client.patch(
            f"/api/v1/question-reports/{report_id}/resolve",
            headers=headers,
            json={
                "status": "dismissed",
                "admin_response": "정답이 올바릅니다.",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "dismissed"

    async def test_resolve_report_with_pending_status(self, client: AsyncClient) -> None:
        """pending 상태로 변경 시도 (불가)."""
        # 학생이 신고 생성
        student_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        student_token = student_login.json()["data"]["access_token"]
        create_response = await client.post(
            "/api/v1/question-reports",
            headers={"Authorization": f"Bearer {student_token}"},
            json={
                "question_id": "question-003",
                "report_type": "other",
                "comment": "문의사항",
            },
        )
        report_id = create_response.json()["data"]["id"]

        # 마스터로 pending으로 처리 시도
        master_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        master_token = master_login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {master_token}"}

        response = await client.patch(
            f"/api/v1/question-reports/{report_id}/resolve",
            headers=headers,
            json={
                "status": "pending",
                "admin_response": "대기 중",
            },
        )

        assert response.status_code == 400
        assert response.json()["detail"]["error"]["code"] == "INVALID_STATUS"

    async def test_resolve_report_not_found(self, client: AsyncClient) -> None:
        """존재하지 않는 신고 처리."""
        master_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        master_token = master_login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {master_token}"}

        response = await client.patch(
            "/api/v1/question-reports/nonexistent-id/resolve",
            headers=headers,
            json={
                "status": "resolved",
                "admin_response": "처리 완료",
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"]["error"]["code"] == "REPORT_NOT_FOUND"

    async def test_resolve_report_already_processed(self, client: AsyncClient) -> None:
        """이미 처리된 신고 재처리 시도."""
        # 학생이 신고 생성
        student_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        student_token = student_login.json()["data"]["access_token"]
        create_response = await client.post(
            "/api/v1/question-reports",
            headers={"Authorization": f"Bearer {student_token}"},
            json={
                "question_id": "question-001",
                "report_type": "wrong_answer",
                "comment": "문제 있음",
            },
        )
        report_id = create_response.json()["data"]["id"]

        # 마스터로 첫 번째 처리
        master_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "master01", "password": "password123"},
        )
        master_token = master_login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {master_token}"}

        await client.patch(
            f"/api/v1/question-reports/{report_id}/resolve",
            headers=headers,
            json={
                "status": "resolved",
                "admin_response": "수정 완료",
            },
        )

        # 두 번째 처리 시도
        response = await client.patch(
            f"/api/v1/question-reports/{report_id}/resolve",
            headers=headers,
            json={
                "status": "dismissed",
                "admin_response": "다시 처리",
            },
        )

        assert response.status_code == 400
        assert response.json()["detail"]["error"]["code"] == "ALREADY_PROCESSED"

    async def test_resolve_report_forbidden_for_student(self, client: AsyncClient) -> None:
        """학생은 신고 처리 불가."""
        # 학생이 신고 생성
        student_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        student_token = student_login.json()["data"]["access_token"]
        create_response = await client.post(
            "/api/v1/question-reports",
            headers={"Authorization": f"Bearer {student_token}"},
            json={
                "question_id": "question-001",
                "report_type": "wrong_answer",
                "comment": "오류",
            },
        )
        report_id = create_response.json()["data"]["id"]

        # 학생이 직접 처리 시도
        response = await client.patch(
            f"/api/v1/question-reports/{report_id}/resolve",
            headers={"Authorization": f"Bearer {student_token}"},
            json={
                "status": "resolved",
                "admin_response": "자가 처리",
            },
        )

        assert response.status_code == 403

    async def test_resolve_report_forbidden_for_teacher(self, client: AsyncClient) -> None:
        """강사는 신고 처리 불가."""
        # 학생이 신고 생성
        student_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "student01", "password": "password123"},
        )
        student_token = student_login.json()["data"]["access_token"]
        create_response = await client.post(
            "/api/v1/question-reports",
            headers={"Authorization": f"Bearer {student_token}"},
            json={
                "question_id": "question-002",
                "report_type": "question_error",
                "comment": "문제 오류",
            },
        )
        report_id = create_response.json()["data"]["id"]

        # 강사가 처리 시도
        teacher_login = await client.post(
            "/api/v1/auth/login",
            json={"login_id": "teacher01", "password": "password123"},
        )
        teacher_token = teacher_login.json()["data"]["access_token"]

        response = await client.patch(
            f"/api/v1/question-reports/{report_id}/resolve",
            headers={"Authorization": f"Bearer {teacher_token}"},
            json={
                "status": "resolved",
                "admin_response": "처리",
            },
        )

        assert response.status_code == 403

    async def test_resolve_report_unauthorized(self, client: AsyncClient) -> None:
        """인증 없이 신고 처리 시도."""
        response = await client.patch(
            "/api/v1/question-reports/any-id/resolve",
            json={
                "status": "resolved",
                "admin_response": "처리",
            },
        )

        assert response.status_code == 401
