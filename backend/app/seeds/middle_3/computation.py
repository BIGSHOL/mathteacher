"""중3 연산 카테고리 시드 데이터 - 2022 개정 교육과정.

1단원: 실수와 그 연산
2단원: 다항식의 곱셈과 인수분해
"""

from .._base import mc, concept, test


def get_computation_data() -> dict:
    """연산 카테고리 데이터 반환."""

    # ============================================================
    # 개념 6개 (2단원 × 3개)
    # ============================================================
    concepts = [
        # ── 1단원: 실수와 그 연산 (3개) ──
        concept(
            id="concept-m3-sqrt-01",
            name="제곱근의 정의와 성질",
            grade="middle_3",
            category="computation",
            part="calc",
            description="제곱근의 정의(x²=a의 해), √a²=|a|, 완전제곱수 판별",
        ),
        concept(
            id="concept-m3-sqrt-02",
            name="무리수와 실수의 분류",
            grade="middle_3",
            category="computation",
            part="calc",
            description="무리수(순환하지 않는 무한소수), 실수=유리수+무리수, 실수의 대소 비교, 수직선 위의 무리수",
        ),
        concept(
            id="concept-m3-sqrt-03",
            name="근호를 포함한 식의 계산",
            grade="middle_3",
            category="computation",
            part="calc",
            description="근호의 사칙연산(√a√b=√ab), 분모의 유리화, 합차를 이용한 유리화",
        ),
        # ── 2단원: 다항식의 곱셈과 인수분해 (3개) ──
        concept(
            id="concept-m3-factor-01",
            name="다항식의 곱셈과 곱셈 공식",
            grade="middle_3",
            category="computation",
            part="algebra",
            description="분배법칙, 완전제곱식 (a±b)², 합차 공식 (a+b)(a-b), 곱셈 공식의 수 계산 활용",
        ),
        concept(
            id="concept-m3-factor-02",
            name="인수분해 기본",
            grade="middle_3",
            category="computation",
            part="algebra",
            description="공통인수 묶기, X자형 분리법(합과 곱 조건), 완전제곱식 인수분해, 합차 인수분해",
        ),
        concept(
            id="concept-m3-factor-03",
            name="완전제곱식과 인수분해 심화",
            grade="middle_3",
            category="computation",
            part="algebra",
            description="완전제곱식 조건 판별, 이차항 계수가 1이 아닌 경우의 인수분해, 복잡한 식의 인수분해",
        ),
    ]

    # ============================================================
    # 문제: 실수와 그 연산 (8문제)
    # ============================================================
    real_questions = [
        mc(
            id="m3-comp-001",
            concept_id="concept-m3-sqrt-01",
            category="computation",
            part="calc",
            difficulty=1,
            content="25의 제곱근을 모두 구하시오.",
            options=["±5", "5", "-5", "±25"],
            correct="A",
            explanation="x² = 25를 만족하는 x는 5와 -5이므로 25의 제곱근은 ±5입니다.",
            points=10,
        ),
        mc(
            id="m3-comp-002",
            concept_id="concept-m3-sqrt-01",
            category="computation",
            part="calc",
            difficulty=2,
            content="√(-3)²의 값은?",
            options=["3", "-3", "±3", "9"],
            correct="A",
            explanation="√(a²) = |a|이므로 √(-3)² = √9 = |-3| = 3입니다.",
            points=10,
        ),
        mc(
            id="m3-comp-003",
            concept_id="concept-m3-sqrt-02",
            category="concept",
            part="calc",
            difficulty=3,
            content="다음 중 옳은 것은?",
            options=[
                "순환소수는 유리수이다",
                "모든 무한소수는 무리수이다",
                "√4는 무리수이다",
                "유리수와 무리수 사이에는 수가 없다",
            ],
            correct="A",
            explanation="순환소수는 분수로 나타낼 수 있으므로 유리수입니다. 무한소수 중 순환하는 것은 유리수이므로 '모든 무한소수는 무리수'는 거짓입니다.",
            points=10,
        ),
        mc(
            id="m3-comp-004",
            concept_id="concept-m3-sqrt-03",
            category="computation",
            part="calc",
            difficulty=4,
            content="√48을 간단히 하시오.",
            options=["4√3", "2√12", "3√4", "√48"],
            correct="A",
            explanation="√48 = √(16×3) = 4√3",
            points=10,
        ),
        mc(
            id="m3-comp-005",
            concept_id="concept-m3-sqrt-03",
            category="computation",
            part="calc",
            difficulty=5,
            content="√2 × √8을 계산하시오.",
            options=["4", "√10", "2√2", "√16"],
            correct="A",
            explanation="√2 × √8 = √(2×8) = √16 = 4",
            points=10,
        ),
        mc(
            id="m3-comp-006",
            concept_id="concept-m3-sqrt-03",
            category="concept",
            part="calc",
            difficulty=6,
            content="다음 중 옳은 것은?",
            options=[
                "√2 + √3 ≠ √5",
                "√2 + √3 = √5",
                "√8 - √2 = √6",
                "√12 + √3 = √15",
            ],
            correct="A",
            explanation="√2 ≈ 1.414, √3 ≈ 1.732이므로 합 ≈ 3.146이지만, √5 ≈ 2.236으로 전혀 다릅니다. 근호의 덧셈에는 분배법칙이 성립하지 않습니다.",
            points=10,
        ),
        mc(
            id="m3-comp-007",
            concept_id="concept-m3-sqrt-03",
            category="computation",
            part="calc",
            difficulty=7,
            content="1/√3을 분모를 유리화하면?",
            options=["√3/3", "3/√3", "1/3", "√3"],
            correct="A",
            explanation="(1/√3) × (√3/√3) = √3/3",
            points=10,
        ),
        mc(
            id="m3-comp-008",
            concept_id="concept-m3-sqrt-03",
            category="computation",
            part="calc",
            difficulty=9,
            content="2/(√5 - 1)을 분모를 유리화하면?",
            options=["(√5 + 1)/2", "(√5 - 1)/2", "√5 + 1", "2√5 - 2"],
            correct="A",
            explanation="분자·분모에 (√5 + 1)을 곱하면: 2(√5 + 1)/(5 - 1) = 2(√5 + 1)/4 = (√5 + 1)/2",
            points=10,
        ),
    ]

    # ============================================================
    # 문제: 다항식의 곱셈과 인수분해 (8문제)
    # ============================================================
    factor_questions = [
        mc(
            id="m3-comp-009",
            concept_id="concept-m3-factor-01",
            category="computation",
            part="algebra",
            difficulty=2,
            content="(x + 3)²을 전개하시오.",
            options=["x² + 6x + 9", "x² + 9", "x² + 3x + 9", "x² + 6x + 3"],
            correct="A",
            explanation="(x + 3)² = x² + 2·x·3 + 3² = x² + 6x + 9. 중간항 2ab를 반드시 포함해야 합니다.",
            points=10,
        ),
        mc(
            id="m3-comp-010",
            concept_id="concept-m3-factor-01",
            category="computation",
            part="algebra",
            difficulty=3,
            content="(a + b)(a - b)를 전개하면?",
            options=["a² - b²", "a² + b²", "a² - ab + b²", "a² - 2ab + b²"],
            correct="A",
            explanation="합차 공식: (a + b)(a - b) = a² - b²",
            points=10,
        ),
        mc(
            id="m3-comp-011",
            concept_id="concept-m3-factor-02",
            category="computation",
            part="algebra",
            difficulty=4,
            content="x² + 6x + 9를 인수분해하시오.",
            options=["(x + 3)²", "(x + 9)(x + 1)", "(x + 3)(x - 3)", "(x + 6)(x + 3)"],
            correct="A",
            explanation="x² + 6x + 9 = x² + 2·3·x + 3² = (x + 3)² (완전제곱식)",
            points=10,
        ),
        mc(
            id="m3-comp-012",
            concept_id="concept-m3-factor-02",
            category="computation",
            part="algebra",
            difficulty=5,
            content="x² - 5x + 6을 인수분해하시오.",
            options=["(x - 2)(x - 3)", "(x + 2)(x + 3)", "(x - 1)(x - 6)", "(x + 2)(x - 3)"],
            correct="A",
            explanation="합이 -5이고 곱이 6인 두 수: -2와 -3. 따라서 (x - 2)(x - 3)",
            points=10,
        ),
        mc(
            id="m3-comp-013",
            concept_id="concept-m3-factor-02",
            category="computation",
            part="algebra",
            difficulty=6,
            content="2x² - 8을 완전히 인수분해하시오.",
            options=["2(x + 2)(x - 2)", "2(x² - 4)", "(2x + 4)(x - 2)", "2(x - 2)²"],
            correct="A",
            explanation="2x² - 8 = 2(x² - 4) = 2(x + 2)(x - 2). 2(x² - 4)에서 멈추면 불완전한 인수분해입니다.",
            points=10,
        ),
        mc(
            id="m3-comp-014",
            concept_id="concept-m3-factor-03",
            category="computation",
            part="algebra",
            difficulty=7,
            content="x² + 10x + □가 완전제곱식이 되려면 □에 알맞은 수는?",
            options=["25", "100", "10", "5"],
            correct="A",
            explanation="완전제곱식 조건: □ = (10/2)² = 5² = 25. 즉, x² + 10x + 25 = (x + 5)²",
            points=10,
        ),
        mc(
            id="m3-comp-015",
            concept_id="concept-m3-factor-02",
            category="computation",
            part="algebra",
            difficulty=8,
            content="x² - x - 12를 인수분해하면?",
            options=["(x + 3)(x - 4)", "(x - 3)(x + 4)", "(x - 2)(x + 6)", "(x + 2)(x - 6)"],
            correct="A",
            explanation="합이 -1이고 곱이 -12인 두 수: 3과 -4. 따라서 (x + 3)(x - 4)",
            points=10,
        ),
        mc(
            id="m3-comp-016",
            concept_id="concept-m3-factor-03",
            category="computation",
            part="algebra",
            difficulty=9,
            content="4x² - 12x + 9를 인수분해하시오.",
            options=["(2x - 3)²", "(4x - 3)(x - 3)", "(2x + 3)²", "(2x - 9)(2x - 1)"],
            correct="A",
            explanation="4x² - 12x + 9 = (2x)² - 2·(2x)·3 + 3² = (2x - 3)²",
            points=10,
        ),
    ]

    questions = real_questions + factor_questions

    # ============================================================
    # 테스트 1개
    # ============================================================
    tests = [
        test(
            id="test-m3-comp",
            title="중3 실수·인수분해 연산 테스트",
            description="실수와 그 연산, 다항식의 곱셈과 인수분해",
            grade="middle_3",
            concept_ids=[c["id"] for c in concepts],
            question_ids=[q["id"] for q in questions],
            time_limit_minutes=30,
        ),
    ]

    return {"concepts": concepts, "questions": questions, "tests": tests}
