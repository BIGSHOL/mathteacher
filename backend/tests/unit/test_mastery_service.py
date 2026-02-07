"""MasteryService 단위 테스트."""

import pytest
from sqlalchemy import select

from app.models.chapter import Chapter
from app.models.concept import Concept
from app.models.concept_mastery import ConceptMastery
from app.services.mastery_service import MasteryService


@pytest.mark.asyncio
async def test_get_or_create_creates_new(db_session):
    """get_or_create_mastery가 존재하지 않는 경우 새로운 레코드를 생성한다."""
    # Given: 개념이 DB에 존재
    concept = Concept(
        id="test-concept-001",
        name="테스트 개념",
        grade="middle_1",
        category="concept",
        part="calc",
    )
    db_session.add(concept)
    await db_session.commit()

    # When: get_or_create 호출
    service = MasteryService(db_session)
    mastery = await service.get_or_create_mastery("student-001", "test-concept-001")

    # Then: 새로운 레코드가 생성되고 기본값이 설정됨
    assert mastery is not None
    assert mastery.student_id == "student-001"
    assert mastery.concept_id == "test-concept-001"
    assert mastery.is_unlocked is False
    assert mastery.is_mastered is False
    assert mastery.mastery_percentage == 0


@pytest.mark.asyncio
async def test_get_or_create_returns_existing(db_session):
    """get_or_create_mastery가 이미 존재하는 경우 기존 레코드를 반환한다."""
    # Given: 개념과 숙련도 레코드가 이미 존재
    concept = Concept(
        id="test-concept-002",
        name="테스트 개념 2",
        grade="middle_1",
        category="concept",
        part="calc",
    )
    db_session.add(concept)

    existing_mastery = ConceptMastery(
        student_id="student-002",
        concept_id="test-concept-002",
        is_unlocked=True,
        mastery_percentage=75,
    )
    db_session.add(existing_mastery)
    await db_session.commit()

    # When: 같은 student_id, concept_id로 get_or_create 호출
    service = MasteryService(db_session)
    mastery = await service.get_or_create_mastery("student-002", "test-concept-002")

    # Then: 기존 레코드가 반환되고 값이 유지됨
    assert mastery.id == existing_mastery.id
    assert mastery.is_unlocked is True
    assert mastery.mastery_percentage == 75


@pytest.mark.asyncio
async def test_unlock_concept_newly_unlocks(db_session):
    """unlock_concept가 잠긴 개념을 해금한다."""
    # Given: 잠긴 개념이 존재
    concept = Concept(
        id="test-concept-003",
        name="테스트 개념 3",
        grade="middle_1",
        category="concept",
        part="calc",
    )
    db_session.add(concept)

    mastery = ConceptMastery(
        student_id="student-003",
        concept_id="test-concept-003",
        is_unlocked=False,
    )
    db_session.add(mastery)
    await db_session.commit()

    # When: unlock_concept 호출
    service = MasteryService(db_session)
    result = await service.unlock_concept("student-003", "test-concept-003")

    # Then: True를 반환하고 is_unlocked가 True로 변경됨
    assert result is True

    # 데이터베이스에서 다시 조회하여 확인
    stmt = select(ConceptMastery).where(
        ConceptMastery.student_id == "student-003",
        ConceptMastery.concept_id == "test-concept-003",
    )
    updated_mastery = await db_session.scalar(stmt)
    assert updated_mastery.is_unlocked is True
    assert updated_mastery.unlocked_at is not None


@pytest.mark.asyncio
async def test_unlock_concept_already_unlocked(db_session):
    """unlock_concept가 이미 해금된 개념에 대해 False를 반환한다."""
    # Given: 이미 해금된 개념이 존재
    concept = Concept(
        id="test-concept-004",
        name="테스트 개념 4",
        grade="middle_1",
        category="concept",
        part="calc",
    )
    db_session.add(concept)

    mastery = ConceptMastery(
        student_id="student-004",
        concept_id="test-concept-004",
        is_unlocked=True,
    )
    db_session.add(mastery)
    await db_session.commit()

    # When: unlock_concept 재호출
    service = MasteryService(db_session)
    result = await service.unlock_concept("student-004", "test-concept-004")

    # Then: False를 반환 (이미 해금됨)
    assert result is False


@pytest.mark.asyncio
async def test_unlock_concept_creates_if_not_exists(db_session):
    """unlock_concept가 숙련도 레코드가 없는 경우 생성한다."""
    # Given: 개념은 존재하지만 숙련도 레코드가 없음
    concept = Concept(
        id="test-concept-005",
        name="테스트 개념 5",
        grade="middle_1",
        category="concept",
        part="calc",
    )
    db_session.add(concept)
    await db_session.commit()

    # When: unlock_concept 호출
    service = MasteryService(db_session)
    result = await service.unlock_concept("student-005", "test-concept-005")

    # Then: True를 반환하고 새로운 레코드가 생성됨
    assert result is True

    stmt = select(ConceptMastery).where(
        ConceptMastery.student_id == "student-005",
        ConceptMastery.concept_id == "test-concept-005",
    )
    mastery = await db_session.scalar(stmt)
    assert mastery is not None
    assert mastery.is_unlocked is True


@pytest.mark.asyncio
async def test_ensure_first_concept_unlocked_unlocks_first(db_session):
    """ensure_first_concept_unlocked가 챕터의 첫 번째 개념을 해금한다."""
    # Given: 챕터와 개념들이 존재
    concepts = [
        Concept(
            id=f"concept-{i:03d}",
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
        id="chapter-001",
        name="테스트 챕터",
        grade="middle_1",
        semester=1,
        chapter_number=1,
        concept_ids=["concept-001", "concept-002", "concept-003"],
    )
    db_session.add(chapter)
    await db_session.commit()

    # When: ensure_first_concept_unlocked 호출
    service = MasteryService(db_session)
    result = await service.ensure_first_concept_unlocked("student-006", "chapter-001")

    # Then: 첫 번째 개념 ID를 반환하고 해금됨
    assert result == "concept-001"

    stmt = select(ConceptMastery).where(
        ConceptMastery.student_id == "student-006",
        ConceptMastery.concept_id == "concept-001",
    )
    mastery = await db_session.scalar(stmt)
    assert mastery is not None
    assert mastery.is_unlocked is True


@pytest.mark.asyncio
async def test_ensure_first_concept_unlocked_already_unlocked(db_session):
    """ensure_first_concept_unlocked가 이미 해금된 경우 None을 반환한다."""
    # Given: 챕터와 이미 해금된 첫 개념
    concept = Concept(
        id="concept-010",
        name="개념 10",
        grade="middle_1",
        category="concept",
        part="calc",
    )
    db_session.add(concept)

    chapter = Chapter(
        id="chapter-002",
        name="테스트 챕터 2",
        grade="middle_1",
        semester=1,
        chapter_number=2,
        concept_ids=["concept-010"],
    )
    db_session.add(chapter)

    mastery = ConceptMastery(
        student_id="student-007",
        concept_id="concept-010",
        is_unlocked=True,
    )
    db_session.add(mastery)
    await db_session.commit()

    # When: ensure_first_concept_unlocked 호출
    service = MasteryService(db_session)
    result = await service.ensure_first_concept_unlocked("student-007", "chapter-002")

    # Then: None을 반환 (이미 해금됨)
    assert result is None


@pytest.mark.asyncio
async def test_ensure_first_concept_unlocked_empty_chapter(db_session):
    """ensure_first_concept_unlocked가 개념이 없는 챕터에 대해 None을 반환한다."""
    # Given: 개념이 없는 챕터
    chapter = Chapter(
        id="chapter-003",
        name="빈 챕터",
        grade="middle_1",
        semester=1,
        chapter_number=3,
        concept_ids=[],
    )
    db_session.add(chapter)
    await db_session.commit()

    # When: ensure_first_concept_unlocked 호출
    service = MasteryService(db_session)
    result = await service.ensure_first_concept_unlocked("student-008", "chapter-003")

    # Then: None을 반환
    assert result is None


@pytest.mark.asyncio
@pytest.mark.xfail(reason="SQLite JSON contains() 미지원 - PostgreSQL에서는 정상 동작")
async def test_unlock_next_concept_in_chapter_unlocks_next(db_session):
    """unlock_next_concept_in_chapter가 다음 개념을 해금한다."""
    # Given: 챕터와 3개의 순차적 개념
    concepts = [
        Concept(
            id=f"concept-2{i:02d}",
            name=f"개념 2{i}",
            grade="middle_1",
            category="concept",
            part="calc",
        )
        for i in range(1, 4)
    ]
    for c in concepts:
        db_session.add(c)

    chapter = Chapter(
        id="chapter-004",
        name="순차 챕터",
        grade="middle_1",
        semester=1,
        chapter_number=4,
        concept_ids=["concept-201", "concept-202", "concept-203"],
    )
    db_session.add(chapter)

    # 첫 번째 개념은 이미 해금됨
    mastery1 = ConceptMastery(
        student_id="student-009",
        concept_id="concept-201",
        is_unlocked=True,
        is_mastered=True,
    )
    db_session.add(mastery1)
    await db_session.commit()

    # When: 첫 번째 개념을 마스터한 후 다음 개념 해금 시도
    service = MasteryService(db_session)
    result = await service.unlock_next_concept_in_chapter("student-009", "concept-201")

    # Then: 두 번째 개념 ID를 반환하고 해금됨
    assert result == "concept-202"

    stmt = select(ConceptMastery).where(
        ConceptMastery.student_id == "student-009",
        ConceptMastery.concept_id == "concept-202",
    )
    mastery2 = await db_session.scalar(stmt)
    assert mastery2 is not None
    assert mastery2.is_unlocked is True


@pytest.mark.asyncio
async def test_unlock_next_concept_in_chapter_last_concept(db_session):
    """unlock_next_concept_in_chapter가 마지막 개념일 경우 None을 반환한다."""
    # Given: 챕터와 2개의 개념 (마지막 개념에서 시도)
    concepts = [
        Concept(
            id=f"concept-3{i:02d}",
            name=f"개념 3{i}",
            grade="middle_1",
            category="concept",
            part="calc",
        )
        for i in range(1, 3)
    ]
    for c in concepts:
        db_session.add(c)

    chapter = Chapter(
        id="chapter-005",
        name="마지막 챕터",
        grade="middle_1",
        semester=1,
        chapter_number=5,
        concept_ids=["concept-301", "concept-302"],
    )
    db_session.add(chapter)

    mastery = ConceptMastery(
        student_id="student-010",
        concept_id="concept-302",
        is_unlocked=True,
        is_mastered=True,
    )
    db_session.add(mastery)
    await db_session.commit()

    # When: 마지막 개념에서 다음 개념 해금 시도
    service = MasteryService(db_session)
    result = await service.unlock_next_concept_in_chapter("student-010", "concept-302")

    # Then: None을 반환 (다음 개념이 없음)
    assert result is None


@pytest.mark.asyncio
async def test_unlock_next_concept_in_chapter_not_in_chapter(db_session):
    """unlock_next_concept_in_chapter가 챕터에 속하지 않는 개념에 대해 None을 반환한다."""
    # Given: 챕터에 속하지 않는 개념
    concept = Concept(
        id="concept-999",
        name="고립된 개념",
        grade="middle_1",
        category="concept",
        part="calc",
    )
    db_session.add(concept)

    chapter = Chapter(
        id="chapter-006",
        name="다른 챕터",
        grade="middle_1",
        semester=1,
        chapter_number=6,
        concept_ids=["concept-401", "concept-402"],
    )
    db_session.add(chapter)
    await db_session.commit()

    # When: 챕터에 속하지 않는 개념으로 호출
    service = MasteryService(db_session)
    result = await service.unlock_next_concept_in_chapter("student-011", "concept-999")

    # Then: None을 반환
    assert result is None


@pytest.mark.asyncio
async def test_unlock_next_concept_already_unlocked(db_session):
    """unlock_next_concept_in_chapter가 이미 해금된 다음 개념을 건너뛴다."""
    # Given: 챕터와 3개의 개념, 두 번째 개념이 이미 해금됨
    concepts = [
        Concept(
            id=f"concept-5{i:02d}",
            name=f"개념 5{i}",
            grade="middle_1",
            category="concept",
            part="calc",
        )
        for i in range(1, 4)
    ]
    for c in concepts:
        db_session.add(c)

    chapter = Chapter(
        id="chapter-007",
        name="중복 해금 챕터",
        grade="middle_1",
        semester=1,
        chapter_number=7,
        concept_ids=["concept-501", "concept-502", "concept-503"],
    )
    db_session.add(chapter)

    mastery1 = ConceptMastery(
        student_id="student-012",
        concept_id="concept-501",
        is_unlocked=True,
        is_mastered=True,
    )
    mastery2 = ConceptMastery(
        student_id="student-012",
        concept_id="concept-502",
        is_unlocked=True,  # 이미 해금됨
    )
    db_session.add(mastery1)
    db_session.add(mastery2)
    await db_session.commit()

    # When: 첫 번째 개념에서 다음 개념 해금 시도
    service = MasteryService(db_session)
    result = await service.unlock_next_concept_in_chapter("student-012", "concept-501")

    # Then: None을 반환 (이미 해금됨)
    assert result is None
