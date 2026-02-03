"""중3 개념 문제 - 이차방정식과 이차함수."""
from app.seeds._base import mc, concept


def get_concepts():
    """개념 정의."""
    return [
        concept(
            id="concept-m3-quad-eq",
            name="이차방정식",
            grade="middle_3",
            category="concept",
            part="algebra",
            description="인수분해, 근의 공식을 이용한 이차방정식의 해 구하기"
        ),
        concept(
            id="concept-m3-quad-func",
            name="이차함수",
            grade="middle_3",
            category="concept",
            part="algebra",
            description="이차함수 y=ax²의 그래프와 성질"
        )
    ]


def get_questions():
    """개념 문제 목록."""
    return [
        # 이차방정식 인수분해 (난이도 1-4)
        mc(
            id="m3-conc-001",
            concept_id="concept-m3-quad-eq",
            category="concept",
            part="algebra",
            difficulty=1,
            content="x² = 9의 해를 구하시오.",
            options=[
                ("x = ±3", True),
                ("x = 3", False),
                ("x = 9", False),
                ("x = ±9", False)
            ],
            correct="A",
            explanation="제곱근을 구하면 x = ±3",
            points=10
        ),
        mc(
            id="m3-conc-002",
            concept_id="concept-m3-quad-eq",
            category="concept",
            part="algebra",
            difficulty=2,
            content="x² - 4 = 0을 인수분해하여 해를 구하시오.",
            options=[
                ("x = ±2", True),
                ("x = 2", False),
                ("x = 4", False),
                ("x = -2", False)
            ],
            correct="A",
            explanation="(x+2)(x-2) = 0이므로 x = 2 또는 x = -2",
            points=10
        ),
        mc(
            id="m3-conc-003",
            concept_id="concept-m3-quad-eq",
            category="concept",
            part="algebra",
            difficulty=3,
            content="x² - 5x + 6 = 0을 인수분해하여 해를 구하시오.",
            options=[
                ("x = 2 또는 x = 3", True),
                ("x = 1 또는 x = 6", False),
                ("x = -2 또는 x = -3", False),
                ("x = 5 또는 x = 6", False)
            ],
            correct="A",
            explanation="(x-2)(x-3) = 0이므로 x = 2 또는 x = 3",
            points=10
        ),
        mc(
            id="m3-conc-004",
            concept_id="concept-m3-quad-eq",
            category="concept",
            part="algebra",
            difficulty=4,
            content="x² + 7x + 12 = 0을 인수분해하여 해를 구하시오.",
            options=[
                ("x = -3 또는 x = -4", True),
                ("x = 3 또는 x = 4", False),
                ("x = -2 또는 x = -6", False),
                ("x = 2 또는 x = 6", False)
            ],
            correct="A",
            explanation="(x+3)(x+4) = 0이므로 x = -3 또는 x = -4",
            points=10
        ),

        # 이차방정식 근의 공식 (난이도 5-7)
        mc(
            id="m3-conc-005",
            concept_id="concept-m3-quad-eq",
            category="concept",
            part="algebra",
            difficulty=5,
            content="x² - 2x - 3 = 0의 해를 구하시오.",
            options=[
                ("x = 3 또는 x = -1", True),
                ("x = 1 또는 x = 3", False),
                ("x = -3 또는 x = 1", False),
                ("x = 2 또는 x = -3", False)
            ],
            correct="A",
            explanation="(x-3)(x+1) = 0이므로 x = 3 또는 x = -1",
            points=10
        ),
        mc(
            id="m3-conc-006",
            concept_id="concept-m3-quad-eq",
            category="concept",
            part="algebra",
            difficulty=6,
            content="x² + 4x + 1 = 0의 해를 근의 공식으로 구하시오.",
            options=[
                ("x = -2 ± √3", True),
                ("x = -2 ± √5", False),
                ("x = 2 ± √3", False),
                ("x = -4 ± √3", False)
            ],
            correct="A",
            explanation="x = (-4 ± √(16-4))/2 = (-4 ± √12)/2 = (-4 ± 2√3)/2 = -2 ± √3",
            points=10
        ),
        mc(
            id="m3-conc-007",
            concept_id="concept-m3-quad-eq",
            category="concept",
            part="algebra",
            difficulty=7,
            content="2x² - 3x - 2 = 0의 해를 구하시오.",
            options=[
                ("x = 2 또는 x = -1/2", True),
                ("x = 1 또는 x = -2", False),
                ("x = 3 또는 x = -2", False),
                ("x = 2 또는 x = 1", False)
            ],
            correct="A",
            explanation="(2x+1)(x-2) = 0이므로 x = 2 또는 x = -1/2",
            points=10
        ),

        # 이차방정식 판별식 (난이도 8-9)
        mc(
            id="m3-conc-008",
            concept_id="concept-m3-quad-eq",
            category="concept",
            part="algebra",
            difficulty=8,
            content="x² - 6x + 9 = 0의 판별식 D의 값은?",
            options=[
                ("0", True),
                ("9", False),
                ("36", False),
                ("-9", False)
            ],
            correct="A",
            explanation="D = b² - 4ac = 36 - 36 = 0 (중근을 가짐)",
            points=10
        ),
        mc(
            id="m3-conc-009",
            concept_id="concept-m3-quad-eq",
            category="concept",
            part="algebra",
            difficulty=9,
            content="x² + 2x + k = 0이 중근을 가질 때, k의 값은?",
            options=[
                ("1", True),
                ("2", False),
                ("0", False),
                ("-1", False)
            ],
            correct="A",
            explanation="중근 조건: D = 0. 4 - 4k = 0이므로 k = 1",
            points=10
        ),

        # 이차함수 (난이도 2-6)
        mc(
            id="m3-conc-010",
            concept_id="concept-m3-quad-func",
            category="concept",
            part="algebra",
            difficulty=2,
            content="이차함수 y = x²의 꼭짓점은?",
            options=[
                ("(0, 0)", True),
                ("(1, 1)", False),
                ("(0, 1)", False),
                ("(1, 0)", False)
            ],
            correct="A",
            explanation="y = x²의 꼭짓점은 원점 (0, 0)",
            points=10
        ),
        mc(
            id="m3-conc-011",
            concept_id="concept-m3-quad-func",
            category="concept",
            part="algebra",
            difficulty=4,
            content="이차함수 y = 2x²의 그래프는 y = x²의 그래프를?",
            options=[
                ("y축 방향으로 2배 확대", True),
                ("y축 방향으로 1/2배 축소", False),
                ("x축 방향으로 2배 확대", False),
                ("x축의 대칭이동", False)
            ],
            correct="A",
            explanation="a>1일 때 y축 방향으로 확대됨",
            points=10
        ),
        mc(
            id="m3-conc-012",
            concept_id="concept-m3-quad-func",
            category="concept",
            part="algebra",
            difficulty=10,
            content="이차함수 y = -x² + 4x - 3의 최댓값은?",
            options=[
                ("1", True),
                ("4", False),
                ("-3", False),
                ("0", False)
            ],
            correct="A",
            explanation="y = -(x-2)² + 1로 변형하면 꼭짓점 (2, 1)에서 최댓값 1",
            points=10
        )
    ]
