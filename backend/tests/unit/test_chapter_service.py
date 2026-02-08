"""ChapterService 단위 테스트."""

from datetime import datetime, timezone

import pytest
from sqlalchemy import select

from app.models.chapter import Chapter
from app.models.chapter_progress import ChapterProgress
from app.models.concept import Concept
from app.models.concept_mastery import ConceptMastery
from app.models.test_attempt import TestAttempt
from app.models.user import User
from app.services.chapter_service import (
    AUTO_PASS_SCORE,
    TEACHER_APPROVAL_MIN_SCORE,
    ChapterService,
)
from app.services.mastery_service import MASTERY_THRESHOLD


@pytest.mark.asyncio
async def test_get_or_create_progress_creates_new(db_session):
    """get_or_create_progress가 존재하지 않는 경우 새로운 레코드를 생성한다."""
    # Given: 챕터가 존재
    chapter = Chapter(
        id="chapter-001",
        name="테스트 챕터",
        grade="middle_1",
        semester=1,
        chapter_number=1,
    )
    db_session.add(chapter)
    await db_session.commit()

    # When: get_or_create_progress 호출
    service = ChapterService(db_session)
    progress = await service.get_or_create_progress("student-001", "chapter-001")

    # Then: 새로운 레코드가 생성되고 기본값이 설정됨
    assert progress is not None
    assert progress.student_id == "student-001"
    assert progress.chapter_id == "chapter-001"
    assert progress.is_unlocked is False
    assert progress.is_completed is False
    assert progress.overall_progress == 0


@pytest.mark.asyncio
async def test_get_or_create_progress_returns_existing(db_session):
    """get_or_create_progress가 이미 존재하는 경우 기존 레코드를 반환한다."""
    # Given: 챕터와 진행 상황이 이미 존재
    chapter = Chapter(
        id="chapter-002",
        name="테스트 챕터 2",
        grade="middle_1",
        semester=1,
        chapter_number=2,
    )
    db_session.add(chapter)

    existing_progress = ChapterProgress(
        student_id="student-002",
        chapter_id="chapter-002",
        is_unlocked=True,
        overall_progress=50,
    )
    db_session.add(existing_progress)
    await db_session.commit()

    # When: 같은 student_id, chapter_id로 get_or_create_progress 호출
    service = ChapterService(db_session)
    progress = await service.get_or_create_progress("student-002", "chapter-002")

    # Then: 기존 레코드가 반환되고 값이 유지됨
    assert progress.id == existing_progress.id
    assert progress.is_unlocked is True
    assert progress.overall_progress == 50


@pytest.mark.asyncio
async def test_unlock_chapter_newly_unlocks(db_session):
    """unlock_chapter가 잠긴 챕터를 해금한다."""
    # Given: 잠긴 챕터와 개념이 존재
    concept = Concept(
        id="concept-101",
        name="개념 101",
        grade="middle_1",
        category="concept",
        part="calc",
    )
    db_session.add(concept)

    chapter = Chapter(
        id="chapter-003",
        name="테스트 챕터 3",
        grade="middle_1",
        semester=1,
        chapter_number=3,
        concept_ids=["concept-101"],
    )
    db_session.add(chapter)
    await db_session.commit()

    # When: unlock_chapter 호출
    service = ChapterService(db_session)
    result = await service.unlock_chapter("student-003", "chapter-003")

    # Then: True를 반환하고 챕터가 해금되며 첫 개념도 해금됨
    assert result is True

    # 챕터 진행 상황 확인
    stmt = select(ChapterProgress).where(
        ChapterProgress.student_id == "student-003",
        ChapterProgress.chapter_id == "chapter-003",
    )
    progress = await db_session.scalar(stmt)
    assert progress.is_unlocked is True
    assert progress.unlocked_at is not None

    # 첫 번째 개념이 해금되었는지 확인
    mastery_stmt = select(ConceptMastery).where(
        ConceptMastery.student_id == "student-003",
        ConceptMastery.concept_id == "concept-101",
    )
    mastery = await db_session.scalar(mastery_stmt)
    assert mastery is not None
    assert mastery.is_unlocked is True


@pytest.mark.asyncio
async def test_unlock_chapter_already_unlocked(db_session):
    """unlock_chapter가 이미 해금된 챕터에 대해 False를 반환한다."""
    # Given: 이미 해금된 챕터
    chapter = Chapter(
        id="chapter-004",
        name="테스트 챕터 4",
        grade="middle_1",
        semester=1,
        chapter_number=4,
        concept_ids=[],
    )
    db_session.add(chapter)

    progress = ChapterProgress(
        student_id="student-004",
        chapter_id="chapter-004",
        is_unlocked=True,
        unlocked_at=datetime.now(timezone.utc),
    )
    db_session.add(progress)
    await db_session.commit()

    # When: unlock_chapter 재호출
    service = ChapterService(db_session)
    result = await service.unlock_chapter("student-004", "chapter-004")

    # Then: False를 반환 (이미 해금됨)
    assert result is False


@pytest.mark.asyncio
async def test_check_chapter_completion_all_concepts_mastered_no_test(db_session):
    """_check_chapter_completion: 모든 개념 마스터 + 종합 테스트 없음 -> 완료."""
    # Given: 종합 테스트가 없는 챕터
    chapter = Chapter(
        id="chapter-005",
        name="테스트 챕터 5",
        grade="middle_1",
        semester=1,
        chapter_number=5,
        concept_ids=["concept-201", "concept-202"],
        final_test_id=None,  # 종합 테스트 없음
    )
    db_session.add(chapter)

    progress = ChapterProgress(
        student_id="student-005",
        chapter_id="chapter-005",
        is_unlocked=True,
        concepts_mastery={"concept-201": 95, "concept-202": 92},
    )
    db_session.add(progress)
    await db_session.commit()

    # When: _check_chapter_completion 호출
    service = ChapterService(db_session)
    result = service._check_chapter_completion(
        chapter, progress, mastered_count=2, total_concepts=2
    )

    # Then: True를 반환 (모든 개념이 마스터되고 종합 테스트가 없음)
    assert result is True


@pytest.mark.asyncio
async def test_check_chapter_completion_not_all_mastered(db_session):
    """_check_chapter_completion: 일부 개념만 마스터 -> 미완료."""
    # Given: 일부 개념만 마스터
    chapter = Chapter(
        id="chapter-006",
        name="테스트 챕터 6",
        grade="middle_1",
        semester=1,
        chapter_number=6,
        concept_ids=["concept-301", "concept-302", "concept-303"],
        final_test_id=None,
    )
    db_session.add(chapter)

    progress = ChapterProgress(
        student_id="student-006",
        chapter_id="chapter-006",
        is_unlocked=True,
        concepts_mastery={"concept-301": 95, "concept-302": 70, "concept-303": 95},
    )
    db_session.add(progress)
    await db_session.commit()

    # When: _check_chapter_completion 호출 (2개만 마스터)
    service = ChapterService(db_session)
    result = service._check_chapter_completion(
        chapter, progress, mastered_count=2, total_concepts=3
    )

    # Then: False를 반환 (모든 개념이 마스터되지 않음)
    assert result is False


@pytest.mark.asyncio
async def test_check_chapter_completion_90_plus_score_auto_pass(db_session):
    """_check_chapter_completion: 90점 이상 -> 자동 통과."""
    # Given: 종합 테스트 90점 이상
    chapter = Chapter(
        id="chapter-007",
        name="테스트 챕터 7",
        grade="middle_1",
        semester=1,
        chapter_number=7,
        concept_ids=["concept-401"],
        final_test_id="test-final-007",
    )
    db_session.add(chapter)

    progress = ChapterProgress(
        student_id="student-007",
        chapter_id="chapter-007",
        is_unlocked=True,
        concepts_mastery={"concept-401": 95},
        final_test_attempted=True,
        final_test_score=92,
        final_test_passed=True,
    )
    db_session.add(progress)
    await db_session.commit()

    # When: _check_chapter_completion 호출
    service = ChapterService(db_session)
    result = service._check_chapter_completion(
        chapter, progress, mastered_count=1, total_concepts=1
    )

    # Then: True를 반환 (90점 이상 자동 통과)
    assert result is True


@pytest.mark.asyncio
async def test_check_chapter_completion_60_89_with_approval(db_session):
    """_check_chapter_completion: 60-89점 + 선생님 승인 -> 통과."""
    # Given: 종합 테스트 70점 + 선생님 승인 필요 + 승인 완료
    chapter = Chapter(
        id="chapter-008",
        name="테스트 챕터 8",
        grade="middle_1",
        semester=1,
        chapter_number=8,
        concept_ids=["concept-501"],
        final_test_id="test-final-008",
        require_teacher_approval=True,
    )
    db_session.add(chapter)

    progress = ChapterProgress(
        student_id="student-008",
        chapter_id="chapter-008",
        is_unlocked=True,
        concepts_mastery={"concept-501": 95},
        final_test_attempted=True,
        final_test_score=75,
        teacher_approved=True,
    )
    db_session.add(progress)
    await db_session.commit()

    # When: _check_chapter_completion 호출
    service = ChapterService(db_session)
    result = service._check_chapter_completion(
        chapter, progress, mastered_count=1, total_concepts=1
    )

    # Then: True를 반환 (60-89점 범위에서 선생님 승인 완료)
    assert result is True


@pytest.mark.asyncio
async def test_check_chapter_completion_60_89_without_approval(db_session):
    """_check_chapter_completion: 60-89점 + 승인 미완료 -> 미완료."""
    # Given: 종합 테스트 70점 + 선생님 승인 필요 + 승인 미완료
    chapter = Chapter(
        id="chapter-009",
        name="테스트 챕터 9",
        grade="middle_1",
        semester=1,
        chapter_number=9,
        concept_ids=["concept-601"],
        final_test_id="test-final-009",
        require_teacher_approval=True,
    )
    db_session.add(chapter)

    progress = ChapterProgress(
        student_id="student-009",
        chapter_id="chapter-009",
        is_unlocked=True,
        concepts_mastery={"concept-601": 95},
        final_test_attempted=True,
        final_test_score=75,
        teacher_approved=False,  # 승인 미완료
    )
    db_session.add(progress)
    await db_session.commit()

    # When: _check_chapter_completion 호출
    service = ChapterService(db_session)
    result = service._check_chapter_completion(
        chapter, progress, mastered_count=1, total_concepts=1
    )

    # Then: False를 반환 (승인이 필요하지만 미완료)
    assert result is False


@pytest.mark.asyncio
async def test_check_chapter_completion_below_60_fails(db_session):
    """_check_chapter_completion: 60점 미만 -> 통과 불가."""
    # Given: 종합 테스트 50점
    chapter = Chapter(
        id="chapter-010",
        name="테스트 챕터 10",
        grade="middle_1",
        semester=1,
        chapter_number=10,
        concept_ids=["concept-701"],
        final_test_id="test-final-010",
    )
    db_session.add(chapter)

    progress = ChapterProgress(
        student_id="student-010",
        chapter_id="chapter-010",
        is_unlocked=True,
        concepts_mastery={"concept-701": 95},
        final_test_attempted=True,
        final_test_score=50,
        final_test_passed=False,
    )
    db_session.add(progress)
    await db_session.commit()

    # When: _check_chapter_completion 호출
    service = ChapterService(db_session)
    result = service._check_chapter_completion(
        chapter, progress, mastered_count=1, total_concepts=1
    )

    # Then: False를 반환 (60점 미만은 통과 불가)
    assert result is False


@pytest.mark.asyncio
async def test_approve_chapter_success(db_session):
    """approve_chapter: 60점 이상일 때 승인이 성공한다."""
    # Given: 60점 이상 + 모든 개념 마스터
    concept = Concept(
        id="concept-801",
        name="개념 801",
        grade="middle_1",
        category="concept",
        part="calc",
    )
    db_session.add(concept)

    chapter = Chapter(
        id="chapter-011",
        name="테스트 챕터 11",
        grade="middle_1",
        semester=1,
        chapter_number=11,
        concept_ids=["concept-801"],
        final_test_id="test-final-011",
        require_teacher_approval=True,
    )
    db_session.add(chapter)

    progress = ChapterProgress(
        student_id="student-011",
        chapter_id="chapter-011",
        is_unlocked=True,
        concepts_mastery={"concept-801": 95},
        final_test_attempted=True,
        final_test_score=75,
        teacher_approved=False,
    )
    db_session.add(progress)
    await db_session.commit()

    # When: approve_chapter 호출
    service = ChapterService(db_session)
    result = await service.approve_chapter(
        "student-011", "chapter-011", "teacher-001", "잘했어요!"
    )

    # Then: True를 반환하고 승인 정보가 업데이트됨
    assert result is True

    # 데이터베이스에서 다시 조회하여 확인
    stmt = select(ChapterProgress).where(
        ChapterProgress.student_id == "student-011",
        ChapterProgress.chapter_id == "chapter-011",
    )
    updated_progress = await db_session.scalar(stmt)
    assert updated_progress.teacher_approved is True
    assert updated_progress.approved_by == "teacher-001"
    assert updated_progress.approved_at is not None
    assert updated_progress.approval_feedback == "잘했어요!"
    assert updated_progress.is_completed is True  # 완료 조건 충족


@pytest.mark.asyncio
async def test_approve_chapter_fails_below_60(db_session):
    """approve_chapter: 60점 미만일 때 승인이 실패한다."""
    # Given: 60점 미만
    chapter = Chapter(
        id="chapter-012",
        name="테스트 챕터 12",
        grade="middle_1",
        semester=1,
        chapter_number=12,
        concept_ids=["concept-901"],
        final_test_id="test-final-012",
        require_teacher_approval=True,
    )
    db_session.add(chapter)

    progress = ChapterProgress(
        student_id="student-012",
        chapter_id="chapter-012",
        is_unlocked=True,
        concepts_mastery={"concept-901": 95},
        final_test_attempted=True,
        final_test_score=55,  # 60점 미만
        teacher_approved=False,
    )
    db_session.add(progress)
    await db_session.commit()

    # When: approve_chapter 호출
    service = ChapterService(db_session)
    result = await service.approve_chapter(
        "student-012", "chapter-012", "teacher-001", "다시 시도해보세요."
    )

    # Then: False를 반환 (승인 조건 미달)
    assert result is False


@pytest.mark.asyncio
async def test_get_student_chapters_auto_unlocks_first_chapter(db_session):
    """get_student_chapters: 첫 번째 챕터를 자동으로 해금한다."""
    # Given: 3개의 챕터
    chapters = [
        Chapter(
            id=f"chapter-auto-{i}",
            name=f"챕터 {i}",
            grade="middle_1",
            semester=1,
            chapter_number=i,
            concept_ids=[f"concept-auto-{i}01"],
        )
        for i in range(1, 4)
    ]
    for ch in chapters:
        db_session.add(ch)

    # 개념 추가
    for i in range(1, 4):
        concept = Concept(
            id=f"concept-auto-{i}01",
            name=f"개념 {i}01",
            grade="middle_1",
            category="concept",
            part="calc",
        )
        db_session.add(concept)

    await db_session.commit()

    # When: get_student_chapters 호출 (진행 상황 없음)
    service = ChapterService(db_session)
    result = await service.get_student_chapters("student-new", grade="middle_1")

    # Then: 첫 번째 챕터가 자동으로 해금됨
    assert len(result) == 3
    assert result[0]["chapter_id"] == "chapter-auto-1"
    assert result[0]["is_unlocked"] is True  # 첫 번째는 자동 해금
    assert result[1]["is_unlocked"] is False
    assert result[2]["is_unlocked"] is False

    # 데이터베이스에 진행 상황이 생성되었는지 확인
    stmt = select(ChapterProgress).where(
        ChapterProgress.student_id == "student-new",
        ChapterProgress.chapter_id == "chapter-auto-1",
    )
    progress = await db_session.scalar(stmt)
    assert progress is not None
    assert progress.is_unlocked is True


@pytest.mark.asyncio
async def test_get_student_chapters_returns_progress(db_session):
    """get_student_chapters: 학생의 진행 상황을 반환한다."""
    # Given: 챕터와 진행 상황
    chapters = [
        Chapter(
            id=f"chapter-progress-{i}",
            name=f"챕터 {i}",
            grade="middle_1",
            semester=1,
            chapter_number=i,
            concept_ids=[],
        )
        for i in range(1, 4)
    ]
    for ch in chapters:
        db_session.add(ch)

    # 첫 번째 챕터는 해금됨
    progress1 = ChapterProgress(
        student_id="student-progress",
        chapter_id="chapter-progress-1",
        is_unlocked=True,
        overall_progress=75,
        is_completed=False,
    )
    db_session.add(progress1)

    # 두 번째 챕터는 해금되고 완료됨
    progress2 = ChapterProgress(
        student_id="student-progress",
        chapter_id="chapter-progress-2",
        is_unlocked=True,
        overall_progress=100,
        is_completed=True,
        final_test_score=95,
    )
    db_session.add(progress2)

    await db_session.commit()

    # When: get_student_chapters 호출
    service = ChapterService(db_session)
    result = await service.get_student_chapters("student-progress", grade="middle_1")

    # Then: 진행 상황이 올바르게 반환됨
    assert len(result) == 3

    # 첫 번째 챕터
    assert result[0]["chapter_id"] == "chapter-progress-1"
    assert result[0]["is_unlocked"] is True
    assert result[0]["overall_progress"] == 75
    assert result[0]["is_completed"] is False

    # 두 번째 챕터
    assert result[1]["chapter_id"] == "chapter-progress-2"
    assert result[1]["is_unlocked"] is True
    assert result[1]["overall_progress"] == 100
    assert result[1]["is_completed"] is True
    assert result[1]["final_test_score"] == 95

    # 세 번째 챕터
    assert result[2]["chapter_id"] == "chapter-progress-3"
    assert result[2]["is_unlocked"] is False
    assert result[2]["overall_progress"] == 0
    assert result[2]["is_completed"] is False


@pytest.mark.asyncio
async def test_update_chapter_progress_calculates_mastery(db_session):
    """update_chapter_progress: 개념별 마스터리를 계산하고 진행률을 업데이트한다."""
    # Given: 챕터와 개념 마스터리
    concepts = [
        Concept(
            id=f"concept-update-{i}",
            name=f"개념 {i}",
            grade="middle_1",
            category="concept",
            part="calc",
        )
        for i in range(1, 4)
    ]
    for c in concepts:
        db_session.add(c)

    chapter = Chapter(
        id="chapter-update",
        name="업데이트 챕터",
        grade="middle_1",
        semester=1,
        chapter_number=1,
        concept_ids=["concept-update-1", "concept-update-2", "concept-update-3"],
    )
    db_session.add(chapter)

    # 개념 마스터리
    masteries = [
        ConceptMastery(
            student_id="student-update",
            concept_id="concept-update-1",
            is_unlocked=True,
            mastery_percentage=90,
        ),
        ConceptMastery(
            student_id="student-update",
            concept_id="concept-update-2",
            is_unlocked=True,
            mastery_percentage=80,
        ),
        ConceptMastery(
            student_id="student-update",
            concept_id="concept-update-3",
            is_unlocked=True,
            mastery_percentage=70,
        ),
    ]
    for m in masteries:
        db_session.add(m)

    progress = ChapterProgress(
        student_id="student-update",
        chapter_id="chapter-update",
        is_unlocked=True,
    )
    db_session.add(progress)
    await db_session.commit()

    # When: update_chapter_progress 호출
    service = ChapterService(db_session)
    result = await service.update_chapter_progress("student-update", "chapter-update")

    # Then: 진행률이 올바르게 계산됨
    assert result["overall_progress"] == 80  # (90 + 80 + 70) / 3 = 80
    assert result["mastered_count"] == 1  # concept-update-1만 90% 이상
    assert result["total_concepts"] == 3
    assert result["concepts_mastery"] == {
        "concept-update-1": 90,
        "concept-update-2": 80,
        "concept-update-3": 70,
    }


@pytest.mark.asyncio
async def test_get_semester_completion_status(db_session):
    """get_semester_completion_status: 학기별 완료 상태를 반환한다."""
    # Given: 2개 학기, 각 2개 챕터
    chapters = [
        Chapter(
            id="chapter-sem1-1",
            name="1학기 챕터 1",
            grade="middle_1",
            semester=1,
            chapter_number=1,
            concept_ids=[],
        ),
        Chapter(
            id="chapter-sem1-2",
            name="1학기 챕터 2",
            grade="middle_1",
            semester=1,
            chapter_number=2,
            concept_ids=[],
        ),
        Chapter(
            id="chapter-sem2-1",
            name="2학기 챕터 1",
            grade="middle_1",
            semester=2,
            chapter_number=1,
            concept_ids=[],
        ),
        Chapter(
            id="chapter-sem2-2",
            name="2학기 챕터 2",
            grade="middle_1",
            semester=2,
            chapter_number=2,
            concept_ids=[],
        ),
    ]
    for ch in chapters:
        db_session.add(ch)

    # 1학기 챕터 1개만 완료
    progress1 = ChapterProgress(
        student_id="student-semester",
        chapter_id="chapter-sem1-1",
        is_unlocked=True,
        is_completed=True,
    )
    db_session.add(progress1)

    # 2학기 챕터 2개 모두 완료
    progress2 = ChapterProgress(
        student_id="student-semester",
        chapter_id="chapter-sem2-1",
        is_unlocked=True,
        is_completed=True,
    )
    progress3 = ChapterProgress(
        student_id="student-semester",
        chapter_id="chapter-sem2-2",
        is_unlocked=True,
        is_completed=True,
    )
    db_session.add(progress2)
    db_session.add(progress3)
    await db_session.commit()

    # When: get_semester_completion_status 호출
    service = ChapterService(db_session)
    result = await service.get_semester_completion_status("student-semester", "middle_1")

    # Then: 학기별 완료 상태가 올바르게 반환됨
    assert result[1] == {
        "total": 2,
        "completed": 1,
        "is_completed": False,
    }
    assert result[2] == {
        "total": 2,
        "completed": 2,
        "is_completed": True,
    }


@pytest.mark.asyncio
async def test_get_grade_completion_status(db_session):
    """get_grade_completion_status: 학년 완료 상태를 반환한다."""
    # Given: 4개 챕터, 3개 완료
    chapters = [
        Chapter(
            id=f"chapter-grade-{i}",
            name=f"챕터 {i}",
            grade="middle_1",
            semester=1,
            chapter_number=i,
            concept_ids=[],
        )
        for i in range(1, 5)
    ]
    for ch in chapters:
        db_session.add(ch)

    # 3개 챕터 완료
    for i in range(1, 4):
        progress = ChapterProgress(
            student_id="student-grade",
            chapter_id=f"chapter-grade-{i}",
            is_unlocked=True,
            is_completed=True,
        )
        db_session.add(progress)

    await db_session.commit()

    # When: get_grade_completion_status 호출
    service = ChapterService(db_session)
    result = await service.get_grade_completion_status("student-grade", "middle_1")

    # Then: 학년 완료 상태가 올바르게 반환됨
    assert result["total"] == 4
    assert result["completed"] == 3
    assert result["is_completed"] is False


@pytest.mark.asyncio
async def test_get_next_recommendation_continue(db_session):
    """get_next_recommendation: 진행 중인 챕터를 추천한다."""
    # Given: 진행 중인 챕터
    chapter = Chapter(
        id="chapter-next-1",
        name="진행 중인 챕터",
        grade="middle_1",
        semester=1,
        chapter_number=1,
        concept_ids=[],
    )
    db_session.add(chapter)

    progress = ChapterProgress(
        student_id="student-next",
        chapter_id="chapter-next-1",
        is_unlocked=True,
        is_completed=False,
        overall_progress=60,
    )
    db_session.add(progress)
    await db_session.commit()

    # When: get_next_recommendation 호출
    service = ChapterService(db_session)
    result = await service.get_next_recommendation("student-next")

    # Then: 진행 중인 챕터를 추천
    assert result is not None
    assert result["type"] == "continue"
    assert result["chapter_id"] == "chapter-next-1"
    assert result["progress"] == 60


@pytest.mark.asyncio
async def test_check_final_test_normalizes_score(db_session):
    """_check_final_test: 종합 테스트 점수를 100점 만점으로 정규화한다."""
    # Given: 챕터와 종합 테스트 시도
    user = User(
        id="student-final",
        login_id="student_final",
        name="테스트 학생",
        role="student",
        hashed_password="hashed",
        is_active=True,
        level=1,
        total_xp=0,
        current_streak=0,
        max_streak=0,
    )
    db_session.add(user)

    chapter = Chapter(
        id="chapter-final",
        name="종합 테스트 챕터",
        grade="middle_1",
        semester=1,
        chapter_number=1,
        concept_ids=["concept-final-1"],
        final_test_id="test-final",
    )
    db_session.add(chapter)

    # 150점 만점에 135점 (90%)
    attempt = TestAttempt(
        id="attempt-final",
        test_id="test-final",
        student_id="student-final",
        score=135,
        max_score=150,
        completed_at=datetime.now(timezone.utc),
    )
    db_session.add(attempt)

    progress = ChapterProgress(
        student_id="student-final",
        chapter_id="chapter-final",
        is_unlocked=True,
    )
    db_session.add(progress)
    await db_session.commit()

    # When: _check_final_test 호출
    service = ChapterService(db_session)
    await service._check_final_test("student-final", chapter, progress)

    # Then: 점수가 100점 만점으로 정규화됨 (90점)
    assert progress.final_test_attempted is True
    assert progress.final_test_score == 90  # 135/150 * 100
    assert progress.final_test_passed is True  # 90점 이상 자동 통과
