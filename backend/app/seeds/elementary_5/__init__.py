"""초등 5학년 시드 데이터."""
from .computation import get_concepts as comp_concepts, get_questions as comp_questions
from .concept_questions import get_concepts as conc_concepts, get_questions as conc_questions
from .fill_blank import get_questions as fb_questions


def get_all_data():
    """초등 5학년 전체 시드 데이터 반환."""
    concepts = comp_concepts() + conc_concepts()
    questions = comp_questions() + conc_questions() + fb_questions()
    tests = _get_tests()
    return {"concepts": concepts, "questions": questions, "tests": tests}


def _get_tests():
    """초등 5학년 테스트 목록 반환."""
    from app.seeds._base import test

    return [
        test(
            id="test-e5-comp",
            title="초등 5학년 연산 종합평가",
            description="약수와 배수, 분수의 곱셈, 소수의 곱셈 능력을 평가합니다.",
            grade="elementary_5",
            concept_ids=["concept-e5-comp"],
            question_ids=[
                "e5-comp-001", "e5-comp-002", "e5-comp-003", "e5-comp-004", "e5-comp-005",
                "e5-comp-006", "e5-comp-007", "e5-comp-008", "e5-comp-009", "e5-comp-010",
            ],
            time_limit_minutes=25,
            is_adaptive=False,
        ),
        test(
            id="test-e5-conc",
            title="초등 5학년 개념평가",
            description="합동과 대칭, 규칙과 대응, 평균 개념을 평가합니다.",
            grade="elementary_5",
            concept_ids=["concept-e5-conc"],
            question_ids=[
                "e5-conc-001", "e5-conc-002", "e5-conc-003", "e5-conc-004", "e5-conc-005",
                "e5-conc-006", "e5-conc-007", "e5-conc-008", "e5-conc-009", "e5-conc-010",
            ],
            time_limit_minutes=30,
            is_adaptive=False,
        ),
        test(
            id="test-e5-comprehensive",
            title="초등 5학년 종합평가",
            description="연산과 개념을 종합적으로 평가합니다.",
            grade="elementary_5",
            concept_ids=["concept-e5-comp", "concept-e5-conc"],
            question_ids=[
                "e5-comp-001", "e5-comp-003", "e5-comp-005", "e5-comp-007", "e5-comp-009",
                "e5-conc-002", "e5-conc-004", "e5-conc-006", "e5-conc-008", "e5-conc-010",
                "e5-fb-001", "e5-fb-003", "e5-fb-005", "e5-fb-007",
            ],
            time_limit_minutes=35,
            is_adaptive=False,
        ),
        test(
            id="test-e5-adaptive",
            title="초등 5학년 적응형 평가",
            description="학생 수준에 맞춰 난이도가 조절되는 평가입니다.",
            grade="elementary_5",
            concept_ids=["concept-e5-comp", "concept-e5-conc"],
            question_ids=[
                "e5-comp-001", "e5-comp-002", "e5-comp-003", "e5-comp-004", "e5-comp-005",
                "e5-comp-006", "e5-comp-007", "e5-comp-008", "e5-comp-009", "e5-comp-010",
                "e5-conc-001", "e5-conc-002", "e5-conc-003", "e5-conc-004", "e5-conc-005",
            ],
            time_limit_minutes=30,
            is_adaptive=True,
            use_question_pool=True,
            questions_per_attempt=10,
        ),
    ]
