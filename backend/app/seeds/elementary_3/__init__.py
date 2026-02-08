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
                "e3-1-1-1",
                "e3-1-1-2",
                "e3-1-3-1",
                "e3-1-3-2",
                "e3-1-4-1",
                "e3-1-4-2",
                "e3-2-1-1",
                "e3-2-1-2",
                "e3-2-2-1",
                "e3-2-2-2",
            ],
            question_ids=[
                "e3-1-1-2-cc-001", "e3-1-1-2-cc-002", "e3-1-1-1-cc-001",  # 덧셈뺄셈
                "e3-1-4-2-cc-001", "e3-1-4-1-cc-001", "e3-1-4-2-cc-002",  # 곱셈1
                "e3-1-3-1-cc-001", "e3-1-3-2-cc-001", "e3-1-3-1-cc-002",  # 나눗셈1
                "e3-2-1-2-cc-001", "e3-2-1-1-co-001", "e3-2-1-2-cc-002",  # 곱셈2
                "e3-2-2-1-co-001", "e3-2-2-1-cc-001", "e3-2-2-2-cc-001",  # 나눗셈2
                "e3-1-1-1-fb-004", "e3-1-1-2-fb-004", "e3-1-4-1-fb-001", "e3-1-4-2-fb-001",
                "e3-2-1-1-fb-001", "e3-2-1-2-fb-001",
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
                "e3-1-2-1",
                "e3-1-2-2",
                "e3-1-5-1",
                "e3-1-5-2",
                "e3-2-3-1",
                "e3-2-3-2",
                "e3-2-5-1",
                "e3-2-5-2",
                "e3-2-6-1",
                "e3-2-6-2",
            ],
            question_ids=[
                "e3-1-2-1-cc-001", "e3-1-2-2-cc-001", "e3-1-2-2-cc-002",  # 평면도형
                "e3-1-5-1-cc-001", "e3-1-5-2-cc-001", "e3-1-5-1-cc-002",  # 길이와 시간
                "e3-2-3-1-cc-001", "e3-2-3-1-cc-002", "e3-2-3-2-cc-001",  # 원
                "e3-2-5-1-cc-001", "e3-2-5-2-cc-001", "e3-2-5-1-cc-002",  # 들이와 무게
                "e3-2-6-2-cc-001", "e3-2-6-2-cc-002", "e3-2-6-1-cc-001",  # 자료의 정리
                "e3-1-2-2-fb-001", "e3-1-2-2-fb-002", "e3-1-5-1-fb-001", "e3-2-3-1-fb-001",
                "e3-2-5-1-fb-001", "e3-2-6-2-fb-001",
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
                "e3-1-6-1",
                "e3-1-6-2",
                "e3-2-4-1",
                "e3-2-4-2",
            ],
            question_ids=[
                "e3-1-6-1-cc-001", "e3-1-6-1-cc-002", "e3-1-6-2-cc-001",  # 분수와 소수 1학기
                "e3-2-4-2-cc-001", "e3-2-4-1-cc-001", "e3-2-4-2-cc-002",  # 분수 2학기
                "e3-1-6-1-fb-001", "e3-1-6-2-fb-001", "e3-2-4-2-fb-001", "e3-2-4-1-fb-001",
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
                "e3-1-1-1",
                "e3-1-1-2",
                "e3-1-3-1",
                "e3-1-3-2",
                "e3-1-4-1",
                "e3-1-4-2",
                "e3-2-1-1",
                "e3-2-1-2",
                "e3-2-2-1",
                "e3-2-2-2",
                "e3-1-2-1",
                "e3-1-2-2",
                "e3-1-5-1",
                "e3-1-5-2",
                "e3-1-6-1",
                "e3-1-6-2",
                "e3-2-3-1",
                "e3-2-3-2",
                "e3-2-4-1",
                "e3-2-4-2",
                "e3-2-5-1",
                "e3-2-5-2",
                "e3-2-6-1",
                "e3-2-6-2",
            ],
            question_ids=[
                # 연산 각 단원별 1~2문제씩
                "e3-1-1-2-cc-001", "e3-1-4-2-cc-001", "e3-1-3-1-cc-001", "e3-2-1-2-cc-001", "e3-2-2-1-co-001",
                # 개념 각 단원별 1~2문제씩
                "e3-1-2-1-cc-001", "e3-1-5-1-cc-001", "e3-1-6-1-cc-001", "e3-2-3-1-cc-001", "e3-2-4-2-cc-001",
                "e3-2-5-1-cc-001", "e3-2-6-2-cc-001",
                # 빈칸 채우기 혼합
                "e3-1-1-1-fb-004", "e3-1-3-1-fb-001", "e3-1-4-1-fb-001", "e3-1-6-1-fb-001", "e3-2-1-1-fb-001",
                "e3-2-2-1-fb-001", "e3-2-3-1-fb-001", "e3-2-4-2-fb-001", "e3-2-5-1-fb-001", "e3-2-6-2-fb-001",
            ],
            time_limit_minutes=40,
            is_adaptive=False,
        ),
    ]
