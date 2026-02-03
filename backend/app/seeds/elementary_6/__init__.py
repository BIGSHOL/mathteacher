"""초등 6학년 시드 데이터."""
from .computation import get_concepts as comp_concepts, get_questions as comp_questions
from .concept_questions import get_concepts as conc_concepts, get_questions as conc_questions
from .fill_blank import get_questions as fb_questions


def get_all_data():
    """초등 6학년 전체 시드 데이터 반환."""
    concepts = comp_concepts() + conc_concepts()
    questions = comp_questions() + conc_questions() + fb_questions()
    tests = _get_tests()
    return {"concepts": concepts, "questions": questions, "tests": tests}


def _get_tests():
    """초등 6학년 테스트 목록 반환."""
    from app.seeds._base import test

    return [
        test(
            id="test-e6-comp",
            title="초등 6학년 연산 종합평가",
            description="분수의 나눗셈과 소수의 나눗셈 능력을 평가합니다.",
            grade="elementary_6",
            concept_ids=["concept-e6-comp"],
            question_ids=[
                "e6-comp-001", "e6-comp-002", "e6-comp-003", "e6-comp-004", "e6-comp-005",
                "e6-comp-006", "e6-comp-007", "e6-comp-008", "e6-comp-009", "e6-comp-010",
            ],
            time_limit_minutes=25,
            is_adaptive=False,
        ),
        test(
            id="test-e6-conc",
            title="초등 6학년 개념평가",
            description="비와 비율, 비례식과 비례배분, 원의 넓이 개념을 평가합니다.",
            grade="elementary_6",
            concept_ids=["concept-e6-conc"],
            question_ids=[
                "e6-conc-001", "e6-conc-002", "e6-conc-003", "e6-conc-004", "e6-conc-005",
                "e6-conc-006", "e6-conc-007", "e6-conc-008", "e6-conc-009", "e6-conc-010",
            ],
            time_limit_minutes=30,
            is_adaptive=False,
        ),
        test(
            id="test-e6-comprehensive",
            title="초등 6학년 종합평가",
            description="연산과 개념을 종합적으로 평가합니다.",
            grade="elementary_6",
            concept_ids=["concept-e6-comp", "concept-e6-conc"],
            question_ids=[
                "e6-comp-001", "e6-comp-003", "e6-comp-005", "e6-comp-007", "e6-comp-009",
                "e6-conc-002", "e6-conc-004", "e6-conc-006", "e6-conc-008", "e6-conc-010",
                "e6-fb-001", "e6-fb-003", "e6-fb-005", "e6-fb-007",
            ],
            time_limit_minutes=35,
            is_adaptive=False,
        ),
        test(
            id="test-e6-adaptive",
            title="초등 6학년 적응형 평가",
            description="학생 수준에 맞춰 난이도가 조절되는 평가입니다.",
            grade="elementary_6",
            concept_ids=["concept-e6-comp", "concept-e6-conc"],
            question_ids=[
                "e6-comp-001", "e6-comp-002", "e6-comp-003", "e6-comp-004", "e6-comp-005",
                "e6-comp-006", "e6-comp-007", "e6-comp-008", "e6-comp-009", "e6-comp-010",
                "e6-conc-001", "e6-conc-002", "e6-conc-003", "e6-conc-004", "e6-conc-005",
            ],
            time_limit_minutes=30,
            is_adaptive=True,
            use_question_pool=True,
            questions_per_attempt=10,
        ),
    ]
