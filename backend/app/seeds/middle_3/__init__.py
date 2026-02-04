"""중3 시드 데이터 모듈 (2022 개정 교육과정).

1단원: 실수와 그 연산
2단원: 다항식의 곱셈과 인수분해
3단원: 이차방정식
4단원: 이차함수 (최대·최소 신설)
5단원: 삼각비
6단원: 원의 성질
7단원: 통계 (상자그림 신설/강화)
"""

from app.seeds.middle_3.computation import get_computation_data
from app.seeds.middle_3.concept_questions import get_concept_data
from app.seeds.middle_3.fill_blank import get_fill_blank_data


def get_all_data() -> dict:
    """중3 전체 데이터 반환."""
    computation = get_computation_data()
    concept = get_concept_data()
    fill_blank = get_fill_blank_data()

    return {
        "concepts": computation["concepts"] + concept["concepts"],
        "questions": computation["questions"] + concept["questions"] + fill_blank["questions"],
        "tests": computation["tests"] + concept["tests"] + fill_blank["tests"],
    }
