"""중1 시드 데이터 모듈."""

from app.seeds.middle_1.computation import get_computation_data
from app.seeds.middle_1.concept_questions import get_concept_data
from app.seeds.middle_1.fill_blank import get_fill_blank_data


def get_all_data() -> dict:
    """
    중1 전체 데이터 반환.

    Returns:
        dict: {
            "concepts": [...],
            "questions": [...],
            "tests": [...]
        }
    """
    computation = get_computation_data()
    concept = get_concept_data()
    fill_blank = get_fill_blank_data()

    # 개념 중복 제거 (computation과 concept에서 공통 개념 사용 가능성)
    concepts_dict = {c["id"]: c for c in (computation["concepts"] + concept["concepts"])}
    all_concepts = list(concepts_dict.values())

    # 표준화된 테스트 정의
    tests = [
        test(
            id="m1-1-1-test",
            name="중1-1 소인수분해 단원평가",
            grade="middle_1",
            question_ids=[
                "m1-1-1-1-co-001", "m1-1-1-1-co-002", "m1-1-1-1-cc-001",
                "m1-1-1-2-co-001", "m1-1-1-2-fb-001", "m1-1-1-3-co-001",
                "m1-1-1-3-fb-001"
            ]
        ),
        test(
            id="m1-1-2-test",
            name="중1-1 정수와 유리수 단원평가",
            grade="middle_1",
            question_ids=[
                "m1-1-2-1-co-001", "m1-1-2-1-cc-001", "m1-1-2-2-co-001",
                "m1-1-2-2-cc-001", "m1-1-2-2-fb-001", "m1-1-2-3-co-001",
                "m1-1-2-3-fb-001"
            ]
        ),
        test(
            id="m1-1-3-test",
            name="중1-1 문자와 식 단원평가",
            grade="middle_1",
            question_ids=[
                "m1-1-3-1-co-001", "m1-1-3-1-cc-001", "m1-1-3-2-co-001",
                "m1-1-3-2-cc-001", "m1-1-3-2-fb-001", "m1-1-3-3-co-001",
                "m1-1-3-3-cc-001", "m1-1-3-3-fb-001"
            ]
        ),
        test(
            id="m1-1-4-test",
            name="중1-1 일차방정식 단원평가",
            grade="middle_1",
            question_ids=[
                "m1-1-4-1-co-001", "m1-1-4-1-cc-001", "m1-1-4-2-co-001",
                "m1-1-4-2-co-002", "m1-1-4-2-fb-001", "m1-1-4-2-fb-002"
            ]
        ),
        test(
            id="m1-2-1-test",
            name="중1-2 좌표평면과 그래프 단원평가",
            grade="middle_1",
            question_ids=[
                "m1-2-1-1-co-001", "m1-2-1-1-cc-001", "m1-2-1-1-fb-001",
                "m1-2-1-2-co-001", "m1-2-1-2-cc-001"
            ]
        ),
        test(
            id="m1-2-3-test",
            name="중1-2 도형의 기초 단원평가",
            grade="middle_1",
            question_ids=[
                "m1-2-3-1-co-001", "m1-2-3-1-cc-001", "m1-2-3-1-fb-001",
                "m1-2-3-2-co-001", "m1-2-3-2-cc-001", "m1-2-3-2-fb-001",
                "m1-2-3-3-co-001", "m1-2-3-3-cc-001"
            ]
        ),
    ]

    return {
        "concepts": all_concepts,
        "questions": computation["questions"] + concept["questions"] + fill_blank["questions"],
        "tests": computation["tests"] + concept["tests"] + fill_blank["tests"] + tests,
    }
