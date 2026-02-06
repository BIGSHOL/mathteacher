"""초등학교 3학년 시드 데이터."""

from .computation import get_concepts as comp_concepts, get_questions as comp_questions
from .concept_questions import get_concepts as conc_concepts, get_questions as conc_questions
from .fill_blank import get_questions as fb_questions
from .._base import test


def get_all_data():
    """초등 3학년 전체 시드 데이터 반환."""
    concepts = comp_concepts() + conc_concepts()
    questions = comp_questions() + conc_questions() + fb_questions()
    tests = _get_tests()
    return {"concepts": concepts, "questions": questions, "tests": tests}


def _get_tests():
    """초등 3학년 테스트 4개 반환."""
    return [
        # 1. 연산평가 (덧셈/뺄셈, 곱셈, 나눗셈)
        test(
            id="test-e3-comp",
            title="초등 3학년 연산 종합평가",
            description="세 자리 수의 사칙연산, 곱셈과 나눗셈의 원리를 평가합니다.",
            grade="elementary_3",
            concept_ids=[
                "concept-e3-add-sub-01",
                "concept-e3-add-sub-02",
                "concept-e3-mul1-01",
                "concept-e3-mul1-02",
                "concept-e3-div1-01",
                "concept-e3-div1-02",
                "concept-e3-mul2-01",
                "concept-e3-mul2-02",
                "concept-e3-div2-01",
                "concept-e3-div2-02",
            ],
            question_ids=[
                "e3-comp-001", "e3-comp-002", "e3-comp-003",  # 덧셈뺄셈
                "e3-comp-004", "e3-comp-005", "e3-comp-006",  # 곱셈1
                "e3-comp-007", "e3-comp-008", "e3-comp-009",  # 나눗셈1
                "e3-comp-010", "e3-comp-011", "e3-comp-012",  # 곱셈2
                "e3-comp-013", "e3-comp-014", "e3-comp-015",  # 나눗셈2
                "e3-fb-001", "e3-fb-002", "e3-fb-007", "e3-fb-008",
                "e3-fb-013", "e3-fb-014",
            ],
            time_limit_minutes=30,
            is_adaptive=False,
        ),
        # 2. 개념평가 (도형, 측정, 자료)
        test(
            id="test-e3-conc",
            title="초등 3학년 개념 종합평가",
            description="평면도형, 원, 측정 단위, 자료 정리 개념을 평가합니다.",
            grade="elementary_3",
            concept_ids=[
                "concept-e3-plane-01",
                "concept-e3-plane-02",
                "concept-e3-length-time-01",
                "concept-e3-length-time-02",
                "concept-e3-circle-01",
                "concept-e3-circle-02",
                "concept-e3-vol-wt-01",
                "concept-e3-vol-wt-02",
                "concept-e3-data-01",
                "concept-e3-data-02",
            ],
            question_ids=[
                "e3-conc-001", "e3-conc-002", "e3-conc-003",  # 평면도형
                "e3-conc-004", "e3-conc-005", "e3-conc-006",  # 길이와 시간
                "e3-conc-010", "e3-conc-011", "e3-conc-012",  # 원
                "e3-conc-016", "e3-conc-017", "e3-conc-018",  # 들이와 무게
                "e3-conc-019", "e3-conc-020", "e3-conc-021",  # 자료의 정리
                "e3-fb-003", "e3-fb-004", "e3-fb-009", "e3-fb-017",
                "e3-fb-021", "e3-fb-023",
            ],
            time_limit_minutes=30,
            is_adaptive=False,
        ),
        # 3. 분수 특별평가 (1학기 + 2학기 통합)
        test(
            id="test-e3-frac",
            title="초등 3학년 분수 집중평가",
            description="단위분수, 소수, 진분수/가분수/대분수, 분수 연산을 평가합니다. "
            "수포자 발생의 분수령이 되는 핵심 단원입니다.",
            grade="elementary_3",
            concept_ids=[
                "concept-e3-frac-dec-01",
                "concept-e3-frac-dec-02",
                "concept-e3-frac2-01",
                "concept-e3-frac2-02",
            ],
            question_ids=[
                "e3-conc-007", "e3-conc-008", "e3-conc-009",  # 분수와 소수 1학기
                "e3-conc-013", "e3-conc-014", "e3-conc-015",  # 분수 2학기
                "e3-fb-011", "e3-fb-012", "e3-fb-019", "e3-fb-020",
            ],
            time_limit_minutes=20,
            is_adaptive=False,
        ),
        # 4. 종합평가 (연산 + 개념 혼합)
        test(
            id="test-e3-comprehensive",
            title="초등 3학년 전체 종합평가",
            description="3학년 1, 2학기 전 단원을 골고루 평가합니다. "
            "자연수 연산 완성과 추상적 수 개념(분수, 소수) 도입을 종합적으로 확인합니다.",
            grade="elementary_3",
            concept_ids=[
                "concept-e3-add-sub-01",
                "concept-e3-add-sub-02",
                "concept-e3-mul1-01",
                "concept-e3-mul1-02",
                "concept-e3-div1-01",
                "concept-e3-div1-02",
                "concept-e3-mul2-01",
                "concept-e3-mul2-02",
                "concept-e3-div2-01",
                "concept-e3-div2-02",
                "concept-e3-plane-01",
                "concept-e3-plane-02",
                "concept-e3-length-time-01",
                "concept-e3-length-time-02",
                "concept-e3-frac-dec-01",
                "concept-e3-frac-dec-02",
                "concept-e3-circle-01",
                "concept-e3-circle-02",
                "concept-e3-frac2-01",
                "concept-e3-frac2-02",
                "concept-e3-vol-wt-01",
                "concept-e3-vol-wt-02",
                "concept-e3-data-01",
                "concept-e3-data-02",
            ],
            question_ids=[
                # 연산 각 단원별 1~2문제씩
                "e3-comp-001", "e3-comp-004", "e3-comp-007", "e3-comp-010", "e3-comp-013",
                # 개념 각 단원별 1~2문제씩
                "e3-conc-001", "e3-conc-004", "e3-conc-007", "e3-conc-010", "e3-conc-013",
                "e3-conc-016", "e3-conc-019",
                # 빈칸 채우기 혼합
                "e3-fb-001", "e3-fb-005", "e3-fb-007", "e3-fb-011", "e3-fb-013",
                "e3-fb-015", "e3-fb-017", "e3-fb-019", "e3-fb-021", "e3-fb-023",
            ],
            time_limit_minutes=40,
            is_adaptive=False,
        ),
    ]
