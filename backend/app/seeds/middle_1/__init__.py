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

    return {
        "concepts": computation["concepts"] + concept["concepts"],
        "questions": computation["questions"] + concept["questions"] + fill_blank["questions"],
        "tests": computation["tests"] + concept["tests"] + fill_blank["tests"],
    }
