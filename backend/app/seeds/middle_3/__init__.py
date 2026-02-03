"""중등 3학년 시드 데이터."""
from .computation import get_concepts as comp_concepts, get_questions as comp_questions
from .concept_questions import get_concepts as conc_concepts, get_questions as conc_questions
from .fill_blank import get_questions as fb_questions


def get_all_data():
    """중3 전체 데이터 반환."""
    concepts = comp_concepts() + conc_concepts()
    questions = comp_questions() + conc_questions() + fb_questions()
    tests = _get_tests()
    return {"concepts": concepts, "questions": questions, "tests": tests}


def _get_tests():
    """중3 테스트 정의."""
    from app.seeds._base import test

    comp_concept_ids = ["concept-m3-sqrt"]
    comp_question_ids = [f"m3-comp-{i:03d}" for i in range(1, 13)]

    conc_concept_ids = ["concept-m3-quad-eq", "concept-m3-quad-func"]
    conc_question_ids = [f"m3-conc-{i:03d}" for i in range(1, 13)]

    fb_question_ids = [f"m3-fb-{i:03d}" for i in range(1, 6)]

    return [
        test(
            id="test-m3-comp",
            title="중3 제곱근 계산 테스트",
            description="제곱근의 곱셈, 나눗셈, 유리화",
            grade="middle_3",
            concept_ids=comp_concept_ids,
            question_ids=comp_question_ids + fb_question_ids[:3],
            time_limit_minutes=30,
            is_adaptive=False,
            passing_score=70
        ),
        test(
            id="test-m3-full",
            title="중3 종합 테스트",
            description="이차방정식과 이차함수",
            grade="middle_3",
            concept_ids=conc_concept_ids,
            question_ids=conc_question_ids + fb_question_ids[3:],
            time_limit_minutes=45,
            is_adaptive=False,
            passing_score=70
        )
    ]
