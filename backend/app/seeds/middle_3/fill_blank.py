"""중3 빈칸 채우기 시드 데이터 - 2022 개정 교육과정.

7개 개념 × 2문제 = 14문제
"""

from .._base import fb, test


def get_fill_blank_data() -> dict:
    """빈칸 채우기 데이터 반환."""

    questions = [
        # ── 실수와 그 연산 (2문제) ──
        fb(
            id="m3-fb-001",
            concept_id="concept-m3-real-num",
            category="computation",
            part="calc",
            difficulty=4,
            content="√32를 간단히 하면 [answer]√[answer]입니다.",
            answer="4|2",
            explanation="√32 = √(16×2) = 4√2",
            points=10,
        ),
        fb(
            id="m3-fb-002",
            concept_id="concept-m3-real-num",
            category="computation",
            part="calc",
            difficulty=7,
            content="2/√3을 분모를 유리화하면 [answer]√[answer]/[answer]입니다.",
            answer="2|3|3",
            explanation="(2/√3) × (√3/√3) = 2√3/3",
            points=10,
        ),

        # ── 다항식의 곱셈과 인수분해 (2문제) ──
        fb(
            id="m3-fb-003",
            concept_id="concept-m3-factoring",
            category="computation",
            part="algebra",
            difficulty=4,
            content="x² + 6x + 9 = (x + [answer])²",
            answer="3",
            explanation="x² + 6x + 9 = (x + 3)² (완전제곱식)",
            points=10,
        ),
        fb(
            id="m3-fb-004",
            concept_id="concept-m3-factoring",
            category="computation",
            part="algebra",
            difficulty=5,
            content="x² - 5x + 6 = (x - [answer])(x - [answer])",
            answer="2|3",
            explanation="합이 -5, 곱이 6인 두 수: -2, -3 → (x - 2)(x - 3)",
            points=10,
        ),

        # ── 이차방정식 (2문제) ──
        fb(
            id="m3-fb-005",
            concept_id="concept-m3-quad-eq",
            category="concept",
            part="algebra",
            difficulty=5,
            content="x² - 8x + 15 = 0을 인수분해하면 (x - [answer])(x - [answer]) = 0",
            answer="3|5",
            explanation="합이 -8, 곱이 15인 두 수: -3, -5 → (x - 3)(x - 5) = 0",
            points=10,
        ),
        fb(
            id="m3-fb-006",
            concept_id="concept-m3-quad-eq",
            category="concept",
            part="algebra",
            difficulty=7,
            content="x² - 6x + 9 = 0의 판별식 D = b² - 4ac의 값은 [answer]이다.",
            answer="0",
            explanation="D = (-6)² - 4(1)(9) = 36 - 36 = 0",
            points=10,
        ),

        # ── 이차함수 (2문제) ──
        fb(
            id="m3-fb-007",
            concept_id="concept-m3-quad-func",
            category="concept",
            part="func",
            difficulty=4,
            content="y = (x - 3)²의 꼭짓점 좌표는 ([answer], [answer])이다.",
            answer="3|0",
            explanation="y = (x - 3)²에서 꼭짓점은 (3, 0)",
            points=10,
        ),
        fb(
            id="m3-fb-008",
            concept_id="concept-m3-quad-func",
            category="concept",
            part="func",
            difficulty=7,
            content="y = -(x - 1)² + 5의 최댓값은 [answer]이다.",
            answer="5",
            explanation="a < 0이므로 꼭짓점 (1, 5)에서 최댓값 5 (y값이 최댓값)",
            points=10,
        ),

        # ── 삼각비 (2문제) ──
        fb(
            id="m3-fb-009",
            concept_id="concept-m3-trig",
            category="concept",
            part="geo",
            difficulty=3,
            content="sin 30° = [answer]",
            answer="1/2",
            accept_formats=["1/2", "0.5"],
            explanation="정삼각형을 반으로 나눈 30-60-90 삼각형에서 sin 30° = 1/2",
            points=10,
        ),
        fb(
            id="m3-fb-010",
            concept_id="concept-m3-trig",
            category="concept",
            part="geo",
            difficulty=4,
            content="tan 45° = [answer]",
            answer="1",
            explanation="직각이등변삼각형에서 tan 45° = 1",
            points=10,
        ),

        # ── 원의 성질 (2문제) ──
        fb(
            id="m3-fb-011",
            concept_id="concept-m3-circle",
            category="concept",
            part="geo",
            difficulty=4,
            content="반원(지름)에 대한 원주각의 크기는 [answer]°이다.",
            answer="90",
            explanation="지름에 대한 중심각 180°의 1/2 = 90°",
            points=10,
        ),
        fb(
            id="m3-fb-012",
            concept_id="concept-m3-circle",
            category="concept",
            part="geo",
            difficulty=5,
            content="원에 내접하는 사각형에서 대각의 합은 [answer]°이다.",
            answer="180",
            explanation="원에 내접하는 사각형의 대각의 합은 180°",
            points=10,
        ),

        # ── 통계 (2문제) ──
        fb(
            id="m3-fb-013",
            concept_id="concept-m3-statistics",
            category="concept",
            part="data",
            difficulty=3,
            content="편차의 총합은 항상 [answer]이다.",
            answer="0",
            explanation="편차(변량 - 평균)의 합은 정의에 의해 항상 0",
            points=10,
        ),
        fb(
            id="m3-fb-014",
            concept_id="concept-m3-statistics",
            category="concept",
            part="data",
            difficulty=5,
            content="사분위범위(IQR) = Q₃ - Q[answer]",
            answer="1",
            accept_formats=["1", "Q1"],
            explanation="IQR = Q₃ - Q₁ (제3사분위수 - 제1사분위수)",
            points=10,
        ),
    ]

    # ============================================================
    # 테스트 1개
    # ============================================================
    tests = [
        test(
            id="test-m3-fb",
            title="중3 빈칸 채우기 종합 테스트",
            description="7개 단원 주요 개념 빈칸 채우기",
            grade="middle_3",
            concept_ids=[
                "concept-m3-real-num",
                "concept-m3-factoring",
                "concept-m3-quad-eq",
                "concept-m3-quad-func",
                "concept-m3-trig",
                "concept-m3-circle",
                "concept-m3-statistics",
            ],
            question_ids=[q["id"] for q in questions],
            time_limit_minutes=25,
        ),
    ]

    return {"concepts": [], "questions": questions, "tests": tests}
