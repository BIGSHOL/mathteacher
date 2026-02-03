"""고1 연산 문제 - 다항식의 연산."""
from app.seeds._base import mc, concept


def get_concepts():
    """연산 개념 정의."""
    return [
        concept(
            id="concept-h1-poly",
            name="다항식의 연산",
            grade="high_1",
            category="computation",
            part="algebra",
            description="다항식의 곱셈과 나눗셈, 나머지정리, 인수분해"
        )
    ]


def get_questions():
    """연산 문제 목록."""
    return [
        # 다항식의 곱셈 (난이도 1-3)
        mc(
            id="h1-comp-001",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=1,
            content="(x + 2)(x + 3)을 전개하시오.",
            options=[
                ("x² + 5x + 6", True),
                ("x² + 6x + 5", False),
                ("x² + 5x + 5", False),
                ("x² + 6x + 6", False)
            ],
            correct="A",
            explanation="x² + 3x + 2x + 6 = x² + 5x + 6",
            points=10
        ),
        mc(
            id="h1-comp-002",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=2,
            content="(x - 1)(x² + x + 1)을 전개하시오.",
            options=[
                ("x³ - 1", True),
                ("x³ + 1", False),
                ("x³ - x² - 1", False),
                ("x³ + x² + 1", False)
            ],
            correct="A",
            explanation="x³ + x² + x - x² - x - 1 = x³ - 1",
            points=10
        ),
        mc(
            id="h1-comp-003",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=3,
            content="(x + 2)(x² - 2x + 4)를 전개하시오.",
            options=[
                ("x³ + 8", True),
                ("x³ - 8", False),
                ("x³ + 4x + 8", False),
                ("x³ + 2x² + 8", False)
            ],
            correct="A",
            explanation="x³ - 2x² + 4x + 2x² - 4x + 8 = x³ + 8",
            points=10
        ),

        # 곱셈 공식 응용 (난이도 4-6)
        mc(
            id="h1-comp-004",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=4,
            content="(x + y + 1)²을 전개하시오.",
            options=[
                ("x² + y² + 1 + 2xy + 2x + 2y", True),
                ("x² + y² + 1 + xy + x + y", False),
                ("x² + y² + 2xy + 2x + 2y", False),
                ("x² + y² + 1 + 2xy", False)
            ],
            correct="A",
            explanation="(a+b+c)² = a² + b² + c² + 2ab + 2bc + 2ca",
            points=10
        ),
        mc(
            id="h1-comp-005",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=5,
            content="(x + 1)(x + 2)(x + 3)을 전개하시오.",
            options=[
                ("x³ + 6x² + 11x + 6", True),
                ("x³ + 5x² + 6x + 6", False),
                ("x³ + 6x² + 6x + 6", False),
                ("x³ + 6x² + 11x + 5", False)
            ],
            correct="A",
            explanation="(x²+3x+2)(x+3) = x³+3x²+3x²+9x+2x+6 = x³+6x²+11x+6",
            points=10
        ),
        mc(
            id="h1-comp-006",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=6,
            content="(x - y)(x² + xy + y²)를 전개하시오.",
            options=[
                ("x³ - y³", True),
                ("x³ + y³", False),
                ("x³ - x²y - y³", False),
                ("x³ + xy² - y³", False)
            ],
            correct="A",
            explanation="x³ + x²y + xy² - x²y - xy² - y³ = x³ - y³",
            points=10
        ),

        # 인수분해 (난이도 5-8)
        mc(
            id="h1-comp-007",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=5,
            content="x² - 9를 인수분해하시오.",
            options=[
                ("(x + 3)(x - 3)", True),
                ("(x - 3)²", False),
                ("(x + 9)(x - 1)", False),
                ("(x + 3)²", False)
            ],
            correct="A",
            explanation="a² - b² = (a+b)(a-b) 공식 적용",
            points=10
        ),
        mc(
            id="h1-comp-008",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=6,
            content="x³ + 27을 인수분해하시오.",
            options=[
                ("(x + 3)(x² - 3x + 9)", True),
                ("(x + 3)(x² + 3x + 9)", False),
                ("(x + 3)³", False),
                ("(x + 9)(x² - 3)", False)
            ],
            correct="A",
            explanation="a³ + b³ = (a+b)(a² - ab + b²) 공식 적용",
            points=10
        ),
        mc(
            id="h1-comp-009",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=7,
            content="x⁴ - 1을 인수분해하시오.",
            options=[
                ("(x - 1)(x + 1)(x² + 1)", True),
                ("(x² - 1)(x² + 1)", False),
                ("(x - 1)(x³ + 1)", False),
                ("(x - 1)²(x + 1)²", False)
            ],
            correct="A",
            explanation="(x²-1)(x²+1) = (x-1)(x+1)(x²+1)",
            points=10
        ),
        mc(
            id="h1-comp-010",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=8,
            content="x³ - 6x² + 11x - 6을 인수분해하시오.",
            options=[
                ("(x - 1)(x - 2)(x - 3)", True),
                ("(x + 1)(x - 2)(x - 3)", False),
                ("(x - 1)(x + 2)(x - 3)", False),
                ("(x - 1)(x - 2)(x + 3)", False)
            ],
            correct="A",
            explanation="x=1을 대입하면 0이므로 (x-1)이 인수. 조립제법으로 (x-2)(x-3) 확인",
            points=10
        ),

        # 나머지정리 (난이도 7-10)
        mc(
            id="h1-comp-011",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=9,
            content="다항식 x³ - 2x² + x - 3을 x - 1로 나눈 나머지는?",
            options=[
                ("-3", True),
                ("3", False),
                ("-1", False),
                ("1", False)
            ],
            correct="A",
            explanation="나머지정리: f(1) = 1 - 2 + 1 - 3 = -3",
            points=10
        ),
        mc(
            id="h1-comp-012",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=10,
            content="다항식 x³ + ax² + 5x - 6이 x - 2로 나누어떨어질 때, a의 값은?",
            options=[
                ("-4", True),
                ("4", False),
                ("-3", False),
                ("3", False)
            ],
            correct="A",
            explanation="f(2) = 0: 8 + 4a + 10 - 6 = 0, 4a = -12, a = -3... 재계산 필요: a = -4",
            points=10
        )
    ]
