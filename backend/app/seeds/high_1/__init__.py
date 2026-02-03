"""고등 1학년 시드 데이터."""
from .computation import get_concepts as comp_concepts, get_questions as comp_questions
from .concept_questions import get_concepts as conc_concepts, get_questions as conc_questions
from .fill_blank import get_questions as fb_questions


def get_all_data():
    """고1 전체 데이터 반환."""
    concepts = comp_concepts() + conc_concepts()
    questions = comp_questions() + conc_questions() + fb_questions()
    tests = _get_tests()
    return {"concepts": concepts, "questions": questions, "tests": tests}


def _get_tests():
    """고1 테스트 정의."""
    from app.seeds._base import test

    comp_concept_ids = ["concept-h1-poly"]
    comp_question_ids = [f"h1-comp-{i:03d}" for i in range(1, 13)]

    conc_concept_ids = ["concept-h1-complex", "concept-h1-quad-ineq", "concept-h1-set"]
    conc_question_ids = [f"h1-conc-{i:03d}" for i in range(1, 13)]

    fb_question_ids = [f"h1-fb-{i:03d}" for i in range(1, 6)]

    return [
        test(
            id="test-h1-comp",
            title="고1 다항식 연산 테스트",
            description="다항식의 곱셈, 나눗셈, 나머지정리, 인수분해",
            grade="high_1",
            concept_ids=comp_concept_ids,
            question_ids=comp_question_ids + fb_question_ids[:3],
            time_limit_minutes=40,
            is_adaptive=False,
            passing_score=70
        ),
        test(
            id="test-h1-full",
            title="고1 종합 테스트",
            description="복소수, 이차방정식/부등식, 집합과 명제",
            grade="high_1",
            concept_ids=conc_concept_ids,
            question_ids=conc_question_ids + fb_question_ids[3:],
            time_limit_minutes=50,
            is_adaptive=False,
            passing_score=70
        )
    ]
