"""초등 4학년 시드 데이터."""

from .computation import get_concepts as comp_concepts, get_questions as comp_questions
from .concept_questions import get_concepts as conc_concepts, get_questions as conc_questions
from .fill_blank import get_questions as fb_questions
from .._base import test


def get_all_data():
    """초등 4학년 전체 시드 데이터 반환."""
    concepts = comp_concepts() + conc_concepts()
    questions = comp_questions() + conc_questions() + fb_questions()
    tests = _get_tests()
    return {"concepts": concepts, "questions": questions, "tests": tests}


def _get_tests():
    """초등 4학년 테스트 4개 반환."""
    return [
        # 1. 연산 종합평가
        test(
            id="test-e4-calc",
            title="초등 4학년 연산 종합평가",
            description="큰 수, 곱셈과 나눗셈, 분수의 덧셈과 뺄셈, 소수의 덧셈과 뺄셈 연산 능력을 평가합니다.",
            grade="elementary_4",
            concept_ids=[
                "e4-1-1-01", "e4-1-1-04", "e4-1-1-06",
                "e4-1-3-01", "e4-1-3-02", "e4-1-3-06",
                "e4-2-1-01", "e4-2-1-05", "e4-2-1-06",
                "e4-2-3-03", "e4-2-3-05", "e4-2-3-07",
            ],
            question_ids=[
                "e4-1-1-01-co-001", "e4-1-1-1-co-001", "e4-1-1-2-co-001",
                "e4-1-3-01-co-001", "e4-1-3-1-co-001", "e4-1-3-2-co-001",
                "e4-2-1-1-co-001", "e4-2-1-2-co-001", "e4-2-1-1-co-003",
                "e4-2-3-1-co-001", "e4-2-3-2-co-001", "e4-2-3-2-co-002",
            ],
            time_limit_minutes=25,
            is_adaptive=False,
            use_question_pool=True,
            questions_per_attempt=10,
        ),
        # 2. 도형 개념평가
        test(
            id="test-e4-geo",
            title="초등 4학년 도형 개념평가",
            description="각도, 평면도형의 이동, 삼각형, 사각형, 다각형의 개념을 평가합니다.",
            grade="elementary_4",
            concept_ids=[
                "e4-1-2-01", "e4-1-2-04", "e4-1-2-07",
                "e4-1-4-01", "e4-1-4-03",
                "e4-2-2-01", "e4-2-2-03",
                "e4-2-4-01", "e4-2-4-04",
                "e4-2-6-01", "e4-2-6-03",
            ],
            question_ids=[
                "e4-1-2-01-cc-001", "e4-1-2-04-cc-001", "e4-1-2-07-cc-001",
                "e4-1-4-01-cc-001", "e4-1-4-03-cc-001", "e4-1-4-05-cc-001",
                "e4-2-2-01-cc-001", "e4-2-2-03-cc-001", "e4-2-2-05-cc-001",
                "e4-2-4-01-cc-001", "e4-2-4-04-cc-001", "e4-2-4-07-cc-001",
                "e4-2-6-01-cc-001", "e4-2-6-03-cc-001", "e4-2-6-05-cc-001",
            ],
            time_limit_minutes=30,
            is_adaptive=False,
            use_question_pool=True,
            questions_per_attempt=10,
        ),
        # 3. 자료와 규칙 평가
        test(
            id="test-e4-data-pattern",
            title="초등 4학년 자료와 규칙 평가",
            description="막대그래프, 꺾은선그래프 해석과 규칙 찾기 능력을 평가합니다.",
            grade="elementary_4",
            concept_ids=[
                "e4-1-5-01", "e4-1-5-02",
                "e4-1-6-01", "e4-1-6-03",
                "e4-2-5-01", "e4-2-5-03",
            ],
            question_ids=[
                "e4-1-5-01-cc-001", "e4-1-5-02-cc-001", "e4-1-5-03-cc-001",
                "e4-1-6-01-cc-001", "e4-1-6-01-cc-002", "e4-1-6-03-cc-001",
                "e4-2-5-01-cc-001", "e4-2-5-03-cc-001", "e4-2-5-05-cc-001",
            ],
            time_limit_minutes=20,
            is_adaptive=False,
        ),
        # 4. 종합평가
        test(
            id="test-e4-comprehensive",
            title="초등 4학년 종합평가",
            description="1·2학기 12단원의 연산과 개념을 종합적으로 평가합니다.",
            grade="elementary_4",
            concept_ids=[
                # 연산
                "e4-1-1-01", "e4-1-1-06", "e4-1-3-01", "e4-1-3-06",
                "e4-2-1-01", "e4-2-1-06", "e4-2-3-03", "e4-2-3-07",
                # 개념
                "e4-1-2-01", "e4-1-2-07", "e4-1-4-01", "e4-1-4-03",
                "e4-1-5-01", "e4-1-5-02", "e4-1-6-01", "e4-1-6-03",
                "e4-2-2-01", "e4-2-2-03", "e4-2-4-01", "e4-2-4-04",
                "e4-2-5-01", "e4-2-5-03", "e4-2-6-01", "e4-2-6-03",
            ],
            question_ids=[
                # 연산
                "e4-1-1-01-co-001", "e4-1-3-01-co-001", "e4-2-1-1-co-001", "e4-2-3-1-co-001",
                # 개념
                "e4-1-2-01-cc-001", "e4-1-4-01-cc-001", "e4-1-5-01-cc-001", "e4-1-6-01-cc-001",
                "e4-2-2-01-cc-001", "e4-2-4-01-cc-001", "e4-2-5-01-cc-001", "e4-2-6-01-cc-001",
                # 빈칸
                "e4-1-3-1-fb-001", "e4-2-1-1-fb-001", "e4-2-3-2-fb-001",
            ],
            time_limit_minutes=35,
            is_adaptive=False,
        ),
    ]
