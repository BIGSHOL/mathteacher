"""고1 시드 데이터 모듈 (2022 개정 교육과정 - 공통수학1)."""
from app.seeds.high_1.computation import get_computation_data
from app.seeds.high_1.concept_questions import get_concept_data
from app.seeds.high_1.fill_blank import get_fill_blank_data


def get_all_data() -> dict:
    """고1 전체 데이터 통합 반환.

    Returns:
        dict: {
            "concepts": [...],      # 8개 (다항식2, 방정식2, 경우의 수2, 행렬2)
            "questions": [...],     # 36개 (MC 24 + FB 12)
            "tests": [...]          # 3개 (연산, 경우의 수, 행렬)
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
