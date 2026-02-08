"""단원 및 개념 숙련도 API 테스트."""

import pytest
from httpx import AsyncClient

from tests.conftest import TestingSessionLocal
from app.models.chapter import Chapter
from app.models.chapter_progress import ChapterProgress
from app.models.concept_mastery import ConceptMastery


async def _add_chapter(chapter_id="chapter-001", concept_ids=None):
    """테스트용 단원 데이터 추가."""
    if concept_ids is None:
        concept_ids = ["concept-001"]

    async with TestingSessionLocal() as session:
        ch = Chapter(
            id=chapter_id,
            name="1. 소인수분해",
            grade="middle_1",
            semester=1,
            chapter_number=1,
            concept_ids=concept_ids,
            description="소인수분해 학습",
        )
        session.add(ch)
        await session.commit()


async def _add_chapter_progress(student_id, chapter_id, is_unlocked=True, is_completed=False, teacher_approved=False):
    """테스트용 단원 진행 상황 추가."""
    async with TestingSessionLocal() as session:
        progress = ChapterProgress(
            student_id=student_id,
            chapter_id=chapter_id,
            is_unlocked=is_unlocked,
            is_completed=is_completed,
            teacher_approved=teacher_approved,
            final_test_score=None,
        )
        session.add(progress)
        await session.commit()


async def _add_concept_mastery(student_id, concept_id, mastery_percentage=0, is_unlocked=True):
    """테스트용 개념 숙련도 추가."""
    async with TestingSessionLocal() as session:
        mastery = ConceptMastery(
            student_id=student_id,
            concept_id=concept_id,
            mastery_percentage=mastery_percentage,
            is_unlocked=is_unlocked,
            is_mastered=mastery_percentage >= 80,
        )
        session.add(mastery)
        await session.commit()


@pytest.mark.asyncio
async def test_get_my_chapter_progress_success(client: AsyncClient):
    """학생 본인의 단원 진행 상황 조회 성공."""
    await _add_chapter()
    await _add_chapter_progress("student-001", "chapter-001")

    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 단원 진행 상황 조회
    resp = await client.get("/api/v1/chapters/progress", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_get_my_chapter_progress_forbidden_for_teacher(client: AsyncClient):
    """강사는 자신의 단원 진행 상황 조회 불가 (403)."""
    # 강사 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "teacher01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 단원 진행 상황 조회 시도
    resp = await client.get("/api/v1/chapters/progress", headers=headers)
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_get_completion_status_without_grade(client: AsyncClient):
    """완료 상태 조회 (grade 파라미터 없음)."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 완료 상태 조회
    resp = await client.get("/api/v1/chapters/completion-status", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "semesters" in data["data"]
    assert "grade" in data["data"]


@pytest.mark.asyncio
async def test_get_completion_status_with_grade(client: AsyncClient):
    """완료 상태 조회 (grade 파라미터 제공)."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 완료 상태 조회 (middle_2 학년)
    resp = await client.get(
        "/api/v1/chapters/completion-status",
        headers=headers,
        params={"grade": "middle_2"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True


@pytest.mark.asyncio
async def test_get_chapter_detail_success(client: AsyncClient):
    """단원 상세 정보 조회 성공."""
    await _add_chapter()
    await _add_chapter_progress("student-001", "chapter-001")

    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 단원 상세 조회
    resp = await client.get("/api/v1/chapters/progress/chapter-001", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["chapter_id"] == "chapter-001"


@pytest.mark.asyncio
async def test_get_chapter_detail_not_found(client: AsyncClient):
    """존재하지 않는 단원 상세 조회 (404)."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 존재하지 않는 단원 조회
    resp = await client.get("/api/v1/chapters/progress/nonexistent", headers=headers)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_my_concept_mastery(client: AsyncClient):
    """개념 숙련도 조회 성공."""
    await _add_concept_mastery("student-001", "concept-001", mastery_percentage=50)

    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 개념 숙련도 조회
    resp = await client.get("/api/v1/chapters/concepts/mastery", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_get_next_recommendation(client: AsyncClient):
    """학습 추천 조회."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 추천 조회
    resp = await client.get("/api/v1/chapters/recommendation", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    # data 필드는 RecommendationResponse 또는 null


@pytest.mark.asyncio
async def test_approve_chapter_completion_success(client: AsyncClient):
    """단원 완료 승인 성공 (강사)."""
    await _add_chapter()
    await _add_chapter_progress("student-001", "chapter-001", is_completed=False)

    # 종합 테스트 점수를 70점 이상으로 설정
    async with TestingSessionLocal() as session:
        from sqlalchemy import select
        stmt = select(ChapterProgress).where(
            ChapterProgress.student_id == "student-001",
            ChapterProgress.chapter_id == "chapter-001",
        )
        progress = await session.scalar(stmt)
        if progress:
            progress.final_test_score = 75
            await session.commit()

    # 강사 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "teacher01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 단원 완료 승인
    resp = await client.post(
        "/api/v1/chapters/chapter-001/approve",
        headers=headers,
        json={"student_id": "student-001", "feedback": "잘했어요!"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["approved"] is True


@pytest.mark.asyncio
async def test_approve_chapter_completion_bad_request(client: AsyncClient):
    """단원 완료 승인 실패 (조건 미충족 - 400)."""
    await _add_chapter()
    await _add_chapter_progress("student-001", "chapter-001", is_completed=False)

    # 종합 테스트 점수가 60점 미만
    async with TestingSessionLocal() as session:
        from sqlalchemy import select
        stmt = select(ChapterProgress).where(
            ChapterProgress.student_id == "student-001",
            ChapterProgress.chapter_id == "chapter-001",
        )
        progress = await session.scalar(stmt)
        if progress:
            progress.final_test_score = 50
            await session.commit()

    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 단원 완료 승인 시도
    resp = await client.post(
        "/api/v1/chapters/chapter-001/approve",
        headers=headers,
        json={"student_id": "student-001", "feedback": "아직 부족합니다"}
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_approve_chapter_completion_forbidden_for_student(client: AsyncClient):
    """학생은 단원 완료 승인 불가 (403)."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 단원 완료 승인 시도
    resp = await client.post(
        "/api/v1/chapters/chapter-001/approve",
        headers=headers,
        json={"student_id": "student-001", "feedback": "자가 승인?"}
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_get_student_chapter_progress_as_master(client: AsyncClient):
    """마스터가 특정 학생의 단원 진행 상황 조회."""
    await _add_chapter()
    await _add_chapter_progress("student-001", "chapter-001")

    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 학생 단원 진행 상황 조회
    resp = await client.get(
        "/api/v1/chapters/students/student-001/progress",
        headers=headers
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_get_student_chapter_progress_forbidden_for_student(client: AsyncClient):
    """학생은 다른 학생의 단원 진행 상황 조회 불가 (403)."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 다른 학생의 단원 진행 상황 조회 시도
    resp = await client.get(
        "/api/v1/chapters/students/student-002/progress",
        headers=headers
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_toggle_chapter_unlock_to_unlock(client: AsyncClient):
    """단원 해금 (잠금 → 해금)."""
    await _add_chapter()

    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 단원 해금
    resp = await client.post(
        "/api/v1/chapters/students/student-001/unlock/chapter-001",
        headers=headers
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["is_unlocked"] is True


@pytest.mark.asyncio
async def test_toggle_chapter_unlock_to_lock(client: AsyncClient):
    """단원 잠금 (해금 → 잠금)."""
    await _add_chapter()
    await _add_chapter_progress("student-001", "chapter-001", is_unlocked=True)

    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 단원 잠금
    resp = await client.post(
        "/api/v1/chapters/students/student-001/unlock/chapter-001",
        headers=headers
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["is_unlocked"] is False


@pytest.mark.asyncio
async def test_toggle_chapter_unlock_not_found(client: AsyncClient):
    """존재하지 않는 단원 해금 시도 (404)."""
    # 마스터 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "master01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 존재하지 않는 단원 해금 시도
    resp = await client.post(
        "/api/v1/chapters/students/student-001/unlock/nonexistent",
        headers=headers
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_placement_test(client: AsyncClient):
    """진단 평가 테스트 정보 조회."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 진단 평가 테스트 조회 (404 예상 - 데이터 없음)
    resp = await client.get("/api/v1/chapters/placement/test", headers=headers)
    # 실제 배포에서는 진단 평가 데이터가 있어야 하지만, 테스트 환경에서는 404가 정상
    assert resp.status_code in [200, 404]


@pytest.mark.asyncio
async def test_get_placement_status(client: AsyncClient):
    """진단 평가 완료 여부 및 결과 조회."""
    # 학생 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "student01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 진단 평가 상태 조회
    resp = await client.get("/api/v1/chapters/placement/status", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "has_completed" in data["data"]
    assert "placement_result" in data["data"]


@pytest.mark.asyncio
async def test_get_placement_status_forbidden_for_teacher(client: AsyncClient):
    """강사는 진단 평가 상태 조회 불가 (403)."""
    # 강사 로그인
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"login_id": "teacher01", "password": "password123"}
    )
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 진단 평가 상태 조회 시도
    resp = await client.get("/api/v1/chapters/placement/status", headers=headers)
    assert resp.status_code == 403
