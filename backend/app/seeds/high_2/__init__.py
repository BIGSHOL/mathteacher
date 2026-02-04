"""고1 2학기 시드 데이터 모듈 (2022 개정 교육과정 - 공통수학2)."""
from app.seeds.high_2.computation import get_computation_data
from app.seeds.high_2.concept_questions import get_concept_data
from app.seeds.high_2.fill_blank import get_fill_blank_data


def get_all_data() -> dict:
    """고1 2학기(공통수학2) 전체 데이터 통합 반환.

    Returns:
        dict: {
            "concepts": [...],      # 10개 (도형4 + 집합/명제3 + 함수3)
            "questions": [...],     # 50개 (MC 30 + FB 20)
            "tests": [...]          # 3개 (도형, 집합/명제, 함수)
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
