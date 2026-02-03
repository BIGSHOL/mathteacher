"""초등 4학년 시드 데이터."""
from .computation import get_concepts as comp_concepts, get_questions as comp_questions
from .concept_questions import get_concepts as conc_concepts, get_questions as conc_questions
from .fill_blank import get_questions as fb_questions


def get_all_data():
    """초등 4학년 전체 시드 데이터 반환."""
    concepts = comp_concepts() + conc_concepts()
    questions = comp_questions() + conc_questions() + fb_questions()
    tests = _get_tests()
    return {"concepts": concepts, "questions": questions, "tests": tests}


def _get_tests():
    """초등 4학년 테스트 목록 반환."""
    from app.seeds._base import test

    return [
        test(
            id="test-e4-comp",
            title="초등 4학년 연산 종합평가",
            description="큰 수의 곱셈과 나눗셈, 분수의 덧셈과 뺄셈 연산 능력을 평가합니다.",
            grade="elementary_4",
            concept_ids=["concept-e4-comp"],
            question_ids=[
                "e4-comp-001", "e4-comp-002", "e4-comp-003", "e4-comp-004", "e4-comp-005",
                "e4-comp-006", "e4-comp-007", "e4-comp-008", "e4-comp-009", "e4-comp-010",
            ],
            time_limit_minutes=25,
            is_adaptive=False,
        ),
        test(
            id="test-e4-conc",
            title="초등 4학년 도형 개념평가",
            description="각도, 수직과 평행, 삼각형과 사각형의 분류 개념을 평가합니다.",
            grade="elementary_4",
            concept_ids=["concept-e4-conc"],
            question_ids=[
                "e4-conc-001", "e4-conc-002", "e4-conc-003", "e4-conc-004", "e4-conc-005",
                "e4-conc-006", "e4-conc-007", "e4-conc-008", "e4-conc-009", "e4-conc-010",
            ],
            time_limit_minutes=25,
            is_adaptive=False,
        ),
        test(
            id="test-e4-comprehensive",
            title="초등 4학년 종합평가",
            description="연산과 도형 개념을 종합적으로 평가합니다.",
            grade="elementary_4",
            concept_ids=["concept-e4-comp", "concept-e4-conc"],
            question_ids=[
                "e4-comp-001", "e4-comp-003", "e4-comp-005", "e4-comp-007", "e4-comp-009",
                "e4-conc-001", "e4-conc-003", "e4-conc-005", "e4-conc-007", "e4-conc-009",
                "e4-fb-001", "e4-fb-003", "e4-fb-005",
            ],
            time_limit_minutes=30,
            is_adaptive=False,
        ),
    ]
