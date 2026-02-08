"""고1 2학기 시드 데이터 모듈 (2022 개정 교육과정 - 공통수학2)."""
from .computation import get_computation_data
from .concept_questions import get_concept_data
from .fill_blank import get_fill_blank_data


def get_all_data() -> dict:
    """고1 공통수학2 전체 데이터 통합 반환 (high_2 폴더).

    Returns:
        dict: {
            "concepts": [...],      # 10개 (도형4, 집합3, 함수3)
            "questions": [...],     # 68개 (MC 48 + FB 20)
            "tests": [...]          # 4개 (도형, 집합, 함수, 도형개념)
        }
    """
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
