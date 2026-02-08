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
    from .._base import test

    return [
        # 연산평가 (분수/소수 나눗셈, 비와 비율)
        test(
            id="test-e6-computation",
            title="초등 6학년 연산평가",
            description="분수와 소수의 나눗셈, 비와 비율 능력을 평가합니다.",
            grade="elementary_6",
            concept_ids=[
                "concept-e6-frac-div1",
                "concept-e6-dec-div1",
                "concept-e6-ratio",
                "concept-e6-frac-div2",
                "concept-e6-dec-div2",
            ],
            question_ids=[
                "e6-1-1-1-lv03-co-001", "e6-1-1-1-lv05-co-001", "e6-1-1-1-lv04-co-001",  # 분수나눗셈1
                "e6-1-3-1-lv06-co-001", "e6-1-3-1-lv05-co-001", "e6-1-3-1-lv04-co-001",  # 소수나눗셈1
                "e6-1-4-1-lv08-co-001", "e6-1-4-1-lv07-co-001", "e6-1-4-1-lv06-co-001",  # 비와 비율
                "e6-2-1-1-lv07-co-001", "e6-2-1-1-lv06-co-001", "e6-2-1-1-lv05-co-001",  # 분수나눗셈2
                "e6-2-2-1-lv07-co-001", "e6-2-2-1-lv08-co-001", "e6-2-2-1-lv09-co-001",  # 소수나눗셈2
            ],
            time_limit_minutes=30,
            is_adaptive=False,
        ),
        # 도형/공간평가 (각기둥/각뿔, 부피/겉넓이, 공간/입체, 원의넓이, 원기둥/원뿔/구)
        test(
            id="test-e6-geometry",
            title="초등 6학년 도형·공간평가",
            description="도형의 구성 요소, 부피와 겉넓이, 공간 감각, 원의 넓이를 평가합니다.",
            grade="elementary_6",
            concept_ids=[
                "concept-e6-prism-pyramid",
                "concept-e6-volume",
                "concept-e6-spatial",
                "concept-e6-circle-area",
                "concept-e6-solids",
            ],
            question_ids=[
                "e6-1-2-1-lv04-cc-001", "e6-1-2-1-lv06-cc-001", "e6-1-2-1-lv05-cc-001",  # 각기둥/각뿔
                "e6-1-6-1-lv08-cc-001", "e6-1-6-1-lv07-cc-001", "e6-1-6-1-lv09-cc-001",  # 부피/겉넓이
                "e6-2-3-1-lv08-cc-001", "e6-2-3-1-lv09-cc-001", "e6-2-3-1-lv07-cc-001",  # 공간/입체
                "e6-2-5-1-lv09-cc-001", "e6-2-5-1-lv06-cc-001", "e6-2-5-1-lv08-cc-001",  # 원의넓이
                "e6-2-6-1-lv07-cc-001", "e6-2-6-1-lv08-cc-001", "e6-2-6-1-lv06-cc-001",  # 원기둥/원뿔/구
            ],
            time_limit_minutes=30,
            is_adaptive=False,
        ),
        # 비율/그래프평가 (그래프, 비례식/비례배분)
        test(
            id="test-e6-ratio-graph",
            title="초등 6학년 비율·그래프평가",
            description="그래프 해석, 비례식의 성질과 비례배분을 평가합니다.",
            grade="elementary_6",
            concept_ids=[
                "concept-e6-graphs",
                "concept-e6-proportion",
            ],
            question_ids=[
                "e6-1-5-1-lv07-cc-001", "e6-1-5-1-lv05-cc-001", "e6-1-5-1-lv06-cc-001",  # 여러 가지 그래프
                "e6-2-4-1-lv08-cc-001", "e6-2-4-1-lv09-cc-001", "e6-2-4-1-lv07-cc-001",  # 비례식/비례배분
                "e6-1-5-1-lv07-fb-001", "e6-1-5-1-lv08-fb-001",  # 그래프 빈칸
                "e6-2-4-1-lv09-fb-001", "e6-2-4-1-lv10-fb-001",  # 비례식 빈칸
            ],
            time_limit_minutes=20,
            is_adaptive=False,
        ),
        # 종합평가 (전 단원 통합)
        test(
            id="test-e6-comprehensive",
            title="초등 6학년 종합평가",
            description="초등 6학년 전 단원을 종합적으로 평가합니다.",
            grade="elementary_6",
            concept_ids=[
                "concept-e6-frac-div1", "concept-e6-dec-div1", "concept-e6-ratio",
                "concept-e6-frac-div2", "concept-e6-dec-div2",
                "concept-e6-prism-pyramid", "concept-e6-graphs", "concept-e6-volume",
                "concept-e6-spatial", "concept-e6-proportion", "concept-e6-circle-area",
                "concept-e6-solids",
            ],
            question_ids=[
                # 연산 5문항
                "e6-1-1-1-lv03-co-001", "e6-1-3-1-lv06-co-001", "e6-1-4-1-lv08-co-001", "e6-2-1-1-lv07-co-001", "e6-2-2-1-lv07-co-001",
                # 개념 10문항
                "e6-1-2-1-lv04-cc-001", "e6-1-5-1-lv07-cc-001", "e6-1-6-1-lv08-cc-001", "e6-2-3-1-lv08-cc-001", "e6-2-4-1-lv08-cc-001",
                "e6-2-5-1-lv09-cc-001", "e6-2-6-1-lv07-cc-001", "e6-1-2-1-lv06-cc-001", "e6-1-6-1-lv07-cc-001", "e6-2-4-1-lv09-cc-001",
                # 빈칸 5문항
                "e6-1-1-1-lv04-fb-001", "e6-1-4-1-lv08-fb-001", "e6-1-6-1-lv08-fb-001", "e6-2-3-1-lv08-fb-001", "e6-2-5-1-lv08-fb-001",
            ],
            time_limit_minutes=40,
            is_adaptive=False,
        ),
    ]
