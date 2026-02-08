"""중2 시드 데이터 모듈."""

from app.seeds.middle_2.computation import get_computation_data
from app.seeds.middle_2.concept_questions import get_concept_data
from app.seeds.middle_2.fill_blank import get_fill_blank_data


def get_all_data() -> dict:
    """중2 전체 데이터 반환."""
    computation = get_computation_data()
    concept = get_concept_data()
    fill_blank = get_fill_blank_data()

    # 중복 개념 제거 (dict 사용)
    concepts_dict = {c["id"]: c for c in computation["concepts"] + concept["concepts"]}
    
    return {
        "concepts": list(concepts_dict.values()),
        "questions": computation["questions"] + concept["questions"] + fill_blank["questions"],
        "tests": computation["tests"] + concept["tests"] + fill_blank["tests"],
    }
