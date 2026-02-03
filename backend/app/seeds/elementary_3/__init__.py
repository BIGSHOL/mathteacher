"""초등 3학년 시드 데이터."""
from .computation import get_concepts as comp_concepts, get_questions as comp_questions
from .concept_questions import get_concepts as conc_concepts, get_questions as conc_questions
from .fill_blank import get_questions as fb_questions


def get_all_data():
    """초등 3학년 전체 시드 데이터 반환."""
    concepts = comp_concepts() + conc_concepts()
    questions = comp_questions() + conc_questions() + fb_questions()
    tests = _get_tests()
    return {"concepts": concepts, "questions": questions, "tests": tests}


def _get_tests():
    """초등 3학년 테스트 목록 반환."""
    from app.seeds._base import test

    return [
        test(
            id="test-e3-comp",
            title="초등 3학년 연산 종합평가",
            description="세 자리 수의 덧셈과 뺄셈, 곱셈 연산 능력을 평가합니다.",
            grade="elementary_3",
            concept_ids=["concept-e3-comp"],
            question_ids=[
                "e3-comp-001", "e3-comp-002", "e3-comp-003", "e3-comp-004", "e3-comp-005",
                "e3-comp-006", "e3-comp-007", "e3-comp-008", "e3-comp-009", "e3-comp-010",
            ],
            time_limit_minutes=20,
            is_adaptive=False,
        ),
        test(
            id="test-e3-conc",
            title="초등 3학년 분수 개념평가",
            description="단위분수와 분수의 크기 비교 개념을 평가합니다.",
            grade="elementary_3",
            concept_ids=["concept-e3-conc"],
            question_ids=[
                "e3-conc-001", "e3-conc-002", "e3-conc-003", "e3-conc-004", "e3-conc-005",
                "e3-conc-006", "e3-conc-007", "e3-conc-008", "e3-conc-009", "e3-conc-010",
            ],
            time_limit_minutes=25,
            is_adaptive=False,
        ),
        test(
            id="test-e3-comprehensive",
            title="초등 3학년 종합평가",
            description="연산과 분수 개념을 종합적으로 평가합니다.",
            grade="elementary_3",
            concept_ids=["concept-e3-comp", "concept-e3-conc"],
            question_ids=[
                "e3-comp-001", "e3-comp-003", "e3-comp-005", "e3-comp-007", "e3-comp-009",
                "e3-conc-001", "e3-conc-003", "e3-conc-005", "e3-conc-007", "e3-conc-009",
                "e3-fb-001", "e3-fb-003", "e3-fb-005",
            ],
            time_limit_minutes=30,
            is_adaptive=False,
        ),
    ]
