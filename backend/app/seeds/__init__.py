"""시드 데이터 모듈 - 전체 학년 통합."""

from app.seeds.elementary_3 import get_all_data as e3_data
from app.seeds.elementary_4 import get_all_data as e4_data
from app.seeds.elementary_5 import get_all_data as e5_data
from app.seeds.elementary_6 import get_all_data as e6_data
from app.seeds.middle_1 import get_all_data as m1_data
from app.seeds.middle_2 import get_all_data as m2_data
from app.seeds.middle_3 import get_all_data as m3_data
from app.seeds.high_1 import get_all_data as h1_data
from app.seeds.high_2 import get_all_data as h2_data


def get_all_grade_seed_data() -> dict:
    """전체 학년 시드 데이터 수집.

    Returns:
        {
            "concepts": [...],   # 모든 학년의 개념
            "questions": [...],  # 모든 학년의 문제
            "tests": [...],      # 모든 학년의 테스트
        }
    """
    all_concepts = []
    all_questions = []
    all_tests = []

    for grade_fn in [e3_data, e4_data, e5_data, e6_data, m1_data, m2_data, m3_data, h1_data, h2_data]:
        data = grade_fn()
        all_concepts.extend(data.get("concepts", []))
        all_questions.extend(data.get("questions", []))
        all_tests.extend(data.get("tests", []))

    return {
        "concepts": all_concepts,
        "questions": all_questions,
        "tests": all_tests,
    }
