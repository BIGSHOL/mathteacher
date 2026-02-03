"""중2 연산 문제 - 단항식과 다항식의 계산."""
from app.seeds._base import mc, concept


def get_concepts():
    """연산 개념 정의."""
    return [
        concept(
            id="concept-m2-comp",
            name="식의 계산",
            grade="middle_2",
            category="computation",
            part="algebra",
            description="단항식의 곱셈과 나눗셈, 다항식의 덧셈과 뺄셈"
        )
    ]


def get_questions():
    """연산 문제 목록."""
    return [
        # 단항식의 곱셈 (난이도 1-3)
        mc(
            id="m2-comp-001",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=1,
            content="3a × 2a를 계산하시오.",
            options=[
                ("5a", False),
                ("6a", False),
                ("6a²", True),
                ("5a²", False)
            ],
            correct="C",
            explanation="단항식의 곱셈: 계수끼리 곱하고(3×2=6), 문자는 지수법칙으로 a×a=a²",
            points=10
        ),
        mc(
            id="m2-comp-002",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=2,
            content="(-4x²) × 3x를 계산하시오.",
            options=[
                ("-12x²", False),
                ("-12x³", True),
                ("12x³", False),
                ("-7x³", False)
            ],
            correct="B",
            explanation="(-4)×3=-12, x²×x=x³이므로 -12x³",
            points=10
        ),
        mc(
            id="m2-comp-003",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=3,
            content="2a²b × (-3ab²)를 계산하시오.",
            options=[
                ("-6a²b²", False),
                ("-6a³b³", True),
                ("6a³b³", False),
                ("-5a³b³", False)
            ],
            correct="B",
            explanation="2×(-3)=-6, a²×a=a³, b×b²=b³이므로 -6a³b³",
            points=10
        ),

        # 단항식의 나눗셈 (난이도 4-6)
        mc(
            id="m2-comp-004",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=4,
            content="6x² ÷ 2x를 계산하시오.",
            options=[
                ("3x", True),
                ("4x", False),
                ("3x²", False),
                ("4x²", False)
            ],
            correct="A",
            explanation="6÷2=3, x²÷x=x이므로 3x",
            points=10
        ),
        mc(
            id="m2-comp-005",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=5,
            content="12a³b² ÷ 3ab를 계산하시오.",
            options=[
                ("4a²b", True),
                ("4a²b²", False),
                ("9a²b", False),
                ("4ab", False)
            ],
            correct="A",
            explanation="12÷3=4, a³÷a=a², b²÷b=b이므로 4a²b",
            points=10
        ),
        mc(
            id="m2-comp-006",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=6,
            content="(-15x³y²) ÷ 5xy²를 계산하시오.",
            options=[
                ("-3x²", True),
                ("3x²", False),
                ("-3x²y", False),
                ("-10x²", False)
            ],
            correct="A",
            explanation="(-15)÷5=-3, x³÷x=x², y²÷y²=1이므로 -3x²",
            points=10
        ),

        # 다항식의 덧셈 (난이도 4-6)
        mc(
            id="m2-comp-007",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=4,
            content="(3x + 2) + (x - 5)를 계산하시오.",
            options=[
                ("4x - 3", True),
                ("4x + 7", False),
                ("2x - 3", False),
                ("4x - 7", False)
            ],
            correct="A",
            explanation="동류항끼리 모으면: 3x+x=4x, 2+(-5)=-3이므로 4x-3",
            points=10
        ),
        mc(
            id="m2-comp-008",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=5,
            content="(2x² - 3x + 1) + (x² + 5x - 4)를 계산하시오.",
            options=[
                ("3x² + 2x - 3", True),
                ("3x² - 8x + 5", False),
                ("3x² + 2x + 5", False),
                ("x² + 2x - 3", False)
            ],
            correct="A",
            explanation="2x²+x²=3x², -3x+5x=2x, 1+(-4)=-3이므로 3x²+2x-3",
            points=10
        ),

        # 다항식의 뺄셈 (난이도 7-10)
        mc(
            id="m2-comp-009",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=7,
            content="(5a - 3b) - (2a + 4b)를 계산하시오.",
            options=[
                ("3a - 7b", True),
                ("3a + b", False),
                ("7a - 7b", False),
                ("3a - b", False)
            ],
            correct="A",
            explanation="괄호를 풀면: 5a-3b-2a-4b = 3a-7b",
            points=10
        ),
        mc(
            id="m2-comp-010",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=8,
            content="(3x² - 2xy + y²) - (x² + 3xy - 2y²)를 계산하시오.",
            options=[
                ("2x² - 5xy + 3y²", True),
                ("2x² + xy + 3y²", False),
                ("4x² - 5xy + 3y²", False),
                ("2x² - 5xy - y²", False)
            ],
            correct="A",
            explanation="괄호를 풀면: 3x²-2xy+y²-x²-3xy+2y² = 2x²-5xy+3y²",
            points=10
        ),

        # 복합 계산 (난이도 8-10)
        mc(
            id="m2-comp-011",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=9,
            content="2(x + 3) - 3(x - 1)을 계산하시오.",
            options=[
                ("-x + 9", True),
                ("5x + 9", False),
                ("-x + 3", False),
                ("x + 9", False)
            ],
            correct="A",
            explanation="분배법칙: 2x+6-3x+3 = -x+9",
            points=10
        ),
        mc(
            id="m2-comp-012",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=10,
            content="3(2a - b) - 2(a + 2b) + (4a - 3b)를 계산하시오.",
            options=[
                ("8a - 10b", True),
                ("6a - 4b", False),
                ("8a - 4b", False),
                ("10a - 10b", False)
            ],
            correct="A",
            explanation="6a-3b-2a-4b+4a-3b = 8a-10b",
            points=10
        )
    ]
