"""중1 연산(computation) 카테고리 시드 데이터."""

from app.seeds._base import mc, concept, test


def get_computation_data() -> dict:
    """연산 카테고리 데이터 반환."""

    # ============================================================
    # 개념: 사칙연산
    # ============================================================
    concepts = [
        concept(
            id="concept-002",
            name="사칙연산",
            grade="middle_1",
            category="computation",
            part="calc",
            description="덧셈, 뺄셈, 곱셈, 나눗셈 연산 연습",
        ),
    ]

    # ============================================================
    # 문제: 기초 연산 (난이도 2-5)
    # ============================================================
    basic_questions = [
        mc(
            id="question-op-001",
            concept_id="concept-002",
            category="computation",
            part="calc",
            difficulty=2,
            content="25 + 37 = ?",
            options=["52", "62", "72", "63"],
            correct="B",
            explanation="25 + 37 = 62",
            points=10,
        ),
        mc(
            id="question-op-002",
            concept_id="concept-002",
            category="computation",
            part="calc",
            difficulty=2,
            content="84 - 29 = ?",
            options=["45", "65", "55", "53"],
            correct="C",
            explanation="84 - 29 = 55",
            points=10,
        ),
        mc(
            id="question-op-003",
            concept_id="concept-002",
            category="computation",
            part="calc",
            difficulty=3,
            content="12 × 7 = ?",
            options=["74", "84", "94", "72"],
            correct="B",
            explanation="12 × 7 = 84",
            points=10,
        ),
        mc(
            id="question-op-004",
            concept_id="concept-002",
            category="computation",
            part="calc",
            difficulty=3,
            content="96 ÷ 8 = ?",
            options=["11", "12", "13", "14"],
            correct="B",
            explanation="96 ÷ 8 = 12",
            points=10,
        ),
        mc(
            id="question-op-005",
            concept_id="concept-002",
            category="computation",
            part="calc",
            difficulty=5,
            content="(-3) × (-8) + 5 = ?",
            options=["19", "29", "-19", "-29"],
            correct="B",
            explanation="(-3) × (-8) = 24, 24 + 5 = 29",
            points=15,
        ),
    ]

    # ============================================================
    # 문제: 고난이도 연산 (난이도 6-10)
    # ============================================================
    high_questions = [
        mc(
            id="question-op-006",
            concept_id="concept-002",
            category="computation",
            part="calc",
            difficulty=6,
            content="(-2)³ + 3² = ?",
            options=["1", "-1", "17", "-17"],
            correct="A",
            explanation="(-2)³ = -8, 3² = 9, -8 + 9 = 1",
            points=15,
        ),
        mc(
            id="question-op-007",
            concept_id="concept-002",
            category="computation",
            part="calc",
            difficulty=7,
            content="|-5| × (-3) + |12 - 20| = ?",
            options=["-7", "7", "-23", "23"],
            correct="A",
            explanation="|-5| = 5, 5 × (-3) = -15, |12-20| = |-8| = 8, -15 + 8 = -7",
            points=15,
        ),
        mc(
            id="question-op-008",
            concept_id="concept-002",
            category="computation",
            part="calc",
            difficulty=8,
            content="(-1)¹⁰⁰ + (-1)⁹⁹ = ?",
            options=["2", "-2", "0", "1"],
            correct="C",
            explanation="(-1)¹⁰⁰ = 1 (짝수 거듭제곱), (-1)⁹⁹ = -1 (홀수 거듭제곱), 1 + (-1) = 0",
            points=15,
        ),
        mc(
            id="question-op-009",
            concept_id="concept-002",
            category="computation",
            part="calc",
            difficulty=9,
            content="2/3 ÷ (-4/9) × 3/2 = ?",
            options=["-9/4", "9/4", "-3/2", "4/9"],
            correct="A",
            explanation="2/3 ÷ (-4/9) = 2/3 × (-9/4) = -18/12 = -3/2, (-3/2) × (3/2) = -9/4",
            points=20,
        ),
        mc(
            id="question-op-010",
            concept_id="concept-002",
            category="computation",
            part="calc",
            difficulty=10,
            content="다음 식을 간단히 하면? (-3)² × 2 - 4 × (-2)³ ÷ (-8)",
            options=["14", "22", "18", "14"],
            correct="B",
            explanation="(-3)² = 9, 9 × 2 = 18. (-2)³ = -8, 4 × (-8) = -32, -32 ÷ (-8) = 4. 18 + 4 = 22",
            points=20,
        ),
    ]

    # ============================================================
    # 테스트
    # ============================================================
    tests = [
        test(
            id="test-002",
            title="연산 연습",
            description="반복 연습으로 연산 속도를 높여보세요",
            grade="middle_1",
            concept_ids=["concept-002"],
            question_ids=[
                "question-op-001",
                "question-op-002",
                "question-op-003",
                "question-op-004",
                "question-op-005",
            ],
            time_limit_minutes=5,
        ),
    ]

    return {
        "concepts": concepts,
        "questions": basic_questions + high_questions,
        "tests": tests,
    }
