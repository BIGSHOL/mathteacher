"""초등 5학년 시드 데이터 모듈."""

from app.seeds.elementary_5.computation import get_computation_data
from app.seeds.elementary_5.concept_questions import get_concepts as conc_concepts, get_questions as conc_questions
from app.seeds.elementary_5.fill_blank import get_questions as fb_questions


def get_all_data() -> dict:
    """초5 전체 데이터 반환."""
    computation = get_computation_data()

    return {
        "concepts": computation["concepts"] + conc_concepts(),
        "questions": computation["questions"] + conc_questions() + fb_questions(),
        "tests": computation["tests"],
    }
