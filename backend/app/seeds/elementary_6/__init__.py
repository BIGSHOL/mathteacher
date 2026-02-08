"""초등 6학년 시드 데이터."""

from .computation import get_concepts as comp_concepts, get_questions as comp_questions
from . import computation
from . import concept_questions
from . import fill_blank
from .._base import test, concept


def get_all_data():
    """초등 6학년 전체 시드 데이터 반환."""
    concepts = (
        computation.get_concepts()
        + concept_questions.get_concepts()
        + [
            concept(
                id="e6-2-3-1",
                name="공간과 입체",
                grade="elementary_6",
                category="concept",
                part="geo",
                description="쌓기나무로 만든 모양을 보고 위, 앞, 옆에서 본 모양을 추론하고 개수를 구합니다.",
            )
        ]
    )
    questions = (
        computation.get_questions()
        + concept_questions.get_questions()
        + fill_blank.get_questions()
    )
    tests = _get_tests()
    return {"concepts": concepts, "questions": questions, "tests": tests}


def _get_tests():
    """초등 6학년 테스트 목록 반환."""
    from .._base import test

    return [
        test(
            id="test-e6-1-1-1",
            name="초6-1-1 분수의 나눗셈 (기본)",
            grade="elementary_6",
            concept_ids=["e6-1-1-1", "e6-2-1-1"],
            question_ids=["e6-1-1-1-co-001", "e6-1-1-1-co-002", "e6-2-1-1-co-001"],
        ),
        test(
            id="test-e6-1-2-1",
            name="초6-1-2 각기둥과 각뿔 (기본)",
            grade="elementary_6",
            concept_ids=["e6-1-2-1", "e6-1-2-2"],
            question_ids=["e6-1-2-1-cc-001", "e6-1-2-2-cc-001", "e6-1-2-1-fb-001"],
        ),
        test(
            id="test-e6-1-3-1",
            name="초6-1-3 소수의 나눗셈 (기본)",
            grade="elementary_6",
            concept_ids=["e6-1-3-1", "e6-2-2-1"],
            question_ids=["e6-1-3-1-co-001", "e6-2-2-1-co-001"],
        ),
        test(
            id="test-e6-1-4-1",
            name="초6-1-4 비와 비율 (기본)",
            grade="elementary_6",
            concept_ids=["e6-1-4-1"],
            question_ids=["e6-1-4-1-co-001", "e6-1-4-1-co-002"],
        ),
        test(
            id="test-e6-1-5-1",
            name="초6-1-5 여러 가지 그래프 (기본)",
            grade="elementary_6",
            concept_ids=["e6-1-5-1", "e6-1-5-2"],
            question_ids=["e6-1-5-1-cc-001", "e6-1-5-2-cc-001", "e6-1-5-1-fb-001"],
        ),
        test(
            id="test-e6-1-6-1",
            name="초6-1-6 직육면체의 겉넓이와 부피 (기본)",
            grade="elementary_6",
            concept_ids=["e6-1-6-1", "e6-1-6-2"],
            question_ids=["e6-1-6-1-cc-001", "e6-1-6-2-cc-001", "e6-1-6-2-fb-001"],
        ),
        test(
            id="test-e6-2-3-1",
            name="초6-2-3 공간과 입체 (기본)",
            grade="elementary_6",
            concept_ids=["e6-2-3-1"],
            question_ids=["e6-2-3-1-cc-001", "e6-2-3-1-fb-001"],
        ),
        test(
            id="test-e6-2-4-1",
            name="초6-2-4 비례식과 비례배분 (기본)",
            grade="elementary_6",
            concept_ids=["e6-2-4-1", "e6-2-4-2"],
            question_ids=["e6-2-4-1-cc-001", "e6-2-4-2-cc-001", "e6-2-4-1-fb-001"],
        ),
        test(
            id="test-e6-2-5-1",
            name="초6-2-5 원의 넓이 (기본)",
            grade="elementary_6",
            concept_ids=["e6-2-5-1", "e6-2-5-2"],
            question_ids=["e6-2-5-1-cc-001", "e6-2-5-2-cc-001", "e6-2-5-1-fb-001"],
        ),
        test(
            id="test-e6-2-6-1",
            name="초6-2-6 원기둥, 원뿔, 구 (기본)",
            grade="elementary_6",
            concept_ids=["e6-2-6-1", "e6-2-6-2"],
            question_ids=["e6-2-6-1-cc-001", "e6-2-6-2-cc-001"],
        ),
    ]
