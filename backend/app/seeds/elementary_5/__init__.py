"""초등 5학년 시드 데이터 모듈 - 2022 개정 교육과정."""

from app.seeds.elementary_5.computation import get_computation_data
from app.seeds.elementary_5.concept_questions import get_concept_data
from app.seeds.elementary_5.fill_blank import get_fill_blank_data


def get_all_data() -> dict:
    """초5 전체 데이터 반환 (12단원 통합)."""
    computation = get_computation_data()
    concept = get_concept_data()
    fill_blank = get_fill_blank_data()

    return {
        "concepts": computation["concepts"] + concept["concepts"],
        "questions": computation["questions"] + concept["questions"] + fill_blank["questions"],
        "tests": computation["tests"] + concept["tests"] + fill_blank["tests"],
    }
