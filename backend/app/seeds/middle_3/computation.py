"""중3 연산 문제 - 제곱근의 계산."""
from app.seeds._base import mc, concept


def get_concepts():
    """연산 개념 정의."""
    return [
        concept(
            id="concept-m3-sqrt",
            name="제곱근의 계산",
            grade="middle_3",
            category="computation",
            part="algebra",
            description="제곱근의 곱셈, 나눗셈, 간단히 하기, 분모의 유리화"
        )
    ]


def get_questions():
    """연산 문제 목록."""
    return [
        # 제곱근 간단히 하기 (난이도 1-3)
        mc(
            id="m3-comp-001",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=1,
            content="√4를 계산하시오.",
            options=[
                ("2", True),
                ("4", False),
                ("±2", False),
                ("16", False)
            ],
            correct="A",
            explanation="√4 = 2 (양의 제곱근)",
            points=10
        ),
        mc(
            id="m3-comp-002",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=2,
            content="√12를 간단히 하시오.",
            options=[
                ("2√3", True),
                ("3√2", False),
                ("4√3", False),
                ("√12", False)
            ],
            correct="A",
            explanation="√12 = √(4×3) = √4 × √3 = 2√3",
            points=10
        ),
        mc(
            id="m3-comp-003",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=3,
            content="√50을 간단히 하시오.",
            options=[
                ("5√2", True),
                ("2√5", False),
                ("10√5", False),
                ("25√2", False)
            ],
            correct="A",
            explanation="√50 = √(25×2) = 5√2",
            points=10
        ),

        # 제곱근의 곱셈 (난이도 4-6)
        mc(
            id="m3-comp-004",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=4,
            content="√2 × √3을 계산하시오.",
            options=[
                ("√6", True),
                ("√5", False),
                ("6", False),
                ("2√3", False)
            ],
            correct="A",
            explanation="√2 × √3 = √(2×3) = √6",
            points=10
        ),
        mc(
            id="m3-comp-005",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=5,
            content="√2 × √8을 계산하시오.",
            options=[
                ("4", True),
                ("√10", False),
                ("2√2", False),
                ("√16", False)
            ],
            correct="A",
            explanation="√2 × √8 = √16 = 4",
            points=10
        ),
        mc(
            id="m3-comp-006",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=6,
            content="2√3 × 3√6을 계산하시오.",
            options=[
                ("18√2", True),
                ("6√9", False),
                ("6√18", False),
                ("5√9", False)
            ],
            correct="A",
            explanation="2×3=6, √3×√6=√18=3√2이므로 6×3√2=18√2",
            points=10
        ),

        # 제곱근의 나눗셈 (난이도 5-7)
        mc(
            id="m3-comp-007",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=5,
            content="√6 ÷ √2를 계산하시오.",
            options=[
                ("√3", True),
                ("√4", False),
                ("3", False),
                ("√8", False)
            ],
            correct="A",
            explanation="√6 ÷ √2 = √(6÷2) = √3",
            points=10
        ),
        mc(
            id="m3-comp-008",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=6,
            content="√18 ÷ √3을 계산하시오.",
            options=[
                ("√6", True),
                ("√15", False),
                ("3", False),
                ("6", False)
            ],
            correct="A",
            explanation="√18 ÷ √3 = √(18÷3) = √6",
            points=10
        ),
        mc(
            id="m3-comp-009",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=7,
            content="6√10 ÷ 2√2를 계산하시오.",
            options=[
                ("3√5", True),
                ("4√5", False),
                ("3√8", False),
                ("12√5", False)
            ],
            correct="A",
            explanation="6÷2=3, √10÷√2=√5이므로 3√5",
            points=10
        ),

        # 분모의 유리화 (난이도 7-10)
        mc(
            id="m3-comp-010",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=7,
            content="1/√2를 분모를 유리화하여 나타내시오.",
            options=[
                ("√2/2", True),
                ("1/2", False),
                ("2/√2", False),
                ("√2", False)
            ],
            correct="A",
            explanation="(1/√2) × (√2/√2) = √2/2",
            points=10
        ),
        mc(
            id="m3-comp-011",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=8,
            content="3/√6을 분모를 유리화하여 나타내시오.",
            options=[
                ("√6/2", True),
                ("3√6/6", False),
                ("√6/3", False),
                ("3√6", False)
            ],
            correct="A",
            explanation="(3/√6) × (√6/√6) = 3√6/6 = √6/2",
            points=10
        ),
        mc(
            id="m3-comp-012",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=10,
            content="2/(√5-1)을 분모를 유리화하여 나타내시오.",
            options=[
                ("(√5+1)/2", True),
                ("(√5-1)/2", False),
                ("√5+1", False),
                ("2√5-2", False)
            ],
            correct="A",
            explanation="분자와 분모에 (√5+1)을 곱하면: 2(√5+1)/(5-1) = 2(√5+1)/4 = (√5+1)/2",
            points=10
        )
    ]
