"""초등 4학년 시드 데이터.

12단원 전체 커버:
  1학기: 큰 수, 각도, 곱셈과 나눗셈, 평면도형의 이동, 막대그래프, 규칙 찾기
  2학기: 분수의 덧셈과 뺄셈, 삼각형, 소수의 덧셈과 뺄셈, 사각형, 꺾은선그래프, 다각형

개념 12개, 객관식 36문항, 빈칸채우기 24문항 = 총 60문항
"""
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
        # ── 연산 종합평가 ──
        test(
            id="test-e4-calc",
            title="초등 4학년 연산 종합평가",
            description="큰 수, 곱셈과 나눗셈, 분수의 덧셈과 뺄셈, 소수의 덧셈과 뺄셈 연산 능력을 평가합니다.",
            grade="elementary_4",
            concept_ids=[
                "concept-e4-big-num",
                "concept-e4-mul-div",
                "concept-e4-frac-op",
                "concept-e4-dec-op",
            ],
            question_ids=[
                "e4-comp-001", "e4-comp-002", "e4-comp-003",
                "e4-comp-004", "e4-comp-005", "e4-comp-006",
                "e4-comp-007", "e4-comp-008", "e4-comp-009",
                "e4-comp-010", "e4-comp-011", "e4-comp-012",
            ],
            time_limit_minutes=25,
            is_adaptive=False,
            use_question_pool=True,
            questions_per_attempt=10,
        ),
        # ── 도형 개념평가 ──
        test(
            id="test-e4-geo",
            title="초등 4학년 도형 개념평가",
            description="각도, 평면도형의 이동, 삼각형, 사각형, 다각형의 개념을 평가합니다.",
            grade="elementary_4",
            concept_ids=[
                "concept-e4-angle",
                "concept-e4-transform",
                "concept-e4-triangle",
                "concept-e4-quad",
                "concept-e4-polygon",
            ],
            question_ids=[
                "e4-conc-001", "e4-conc-002", "e4-conc-003",
                "e4-conc-004", "e4-conc-005", "e4-conc-006",
                "e4-conc-013", "e4-conc-014", "e4-conc-015",
                "e4-conc-016", "e4-conc-017", "e4-conc-018",
                "e4-conc-022", "e4-conc-023", "e4-conc-024",
            ],
            time_limit_minutes=30,
            is_adaptive=False,
            use_question_pool=True,
            questions_per_attempt=10,
        ),
        # ── 자료와 규칙 평가 ──
        test(
            id="test-e4-data-pattern",
            title="초등 4학년 자료와 규칙 평가",
            description="막대그래프, 꺾은선그래프 해석과 규칙 찾기 능력을 평가합니다.",
            grade="elementary_4",
            concept_ids=[
                "concept-e4-bar-graph",
                "concept-e4-line-graph",
                "concept-e4-pattern",
            ],
            question_ids=[
                "e4-conc-007", "e4-conc-008", "e4-conc-009",
                "e4-conc-010", "e4-conc-011", "e4-conc-012",
                "e4-conc-019", "e4-conc-020", "e4-conc-021",
            ],
            time_limit_minutes=20,
            is_adaptive=False,
        ),
        # ── 종합평가 ──
        test(
            id="test-e4-comprehensive",
            title="초등 4학년 종합평가",
            description="1·2학기 12단원의 연산과 개념을 종합적으로 평가합니다.",
            grade="elementary_4",
            concept_ids=[
                "concept-e4-big-num", "concept-e4-mul-div",
                "concept-e4-frac-op", "concept-e4-dec-op",
                "concept-e4-angle", "concept-e4-transform",
                "concept-e4-bar-graph", "concept-e4-pattern",
                "concept-e4-triangle", "concept-e4-quad",
                "concept-e4-line-graph", "concept-e4-polygon",
            ],
            question_ids=[
                # 연산 (각 단원 1문항)
                "e4-comp-001", "e4-comp-005", "e4-comp-008", "e4-comp-011",
                # 개념 (각 단원 1문항)
                "e4-conc-002", "e4-conc-005", "e4-conc-008", "e4-conc-011",
                "e4-conc-014", "e4-conc-017", "e4-conc-020", "e4-conc-023",
                # 빈칸채우기 (3문항)
                "e4-fb-005", "e4-fb-013", "e4-fb-017",
            ],
            time_limit_minutes=35,
            is_adaptive=False,
        ),
    ]
