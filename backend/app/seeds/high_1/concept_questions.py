"""고1 개념 문제 - 복소수, 이차방정식/부등식, 집합과 명제."""
from app.seeds._base import mc, concept


def get_concepts():
    """개념 정의."""
    return [
        concept(
            id="concept-h1-complex",
            name="복소수",
            grade="high_1",
            category="concept",
            part="algebra",
            description="허수단위 i, 복소수의 연산"
        ),
        concept(
            id="concept-h1-quad-ineq",
            name="이차방정식과 부등식",
            grade="high_1",
            category="concept",
            part="algebra",
            description="판별식, 근과 계수의 관계, 이차부등식"
        ),
        concept(
            id="concept-h1-set",
            name="집합과 명제",
            grade="high_1",
            category="concept",
            part="logic",
            description="집합의 연산, 명제의 역과 대우"
        )
    ]


def get_questions():
    """개념 문제 목록."""
    return [
        # 복소수 기본 (난이도 1-3)
        mc(
            id="h1-conc-001",
            concept_id="concept-h1-complex",
            category="concept",
            part="algebra",
            difficulty=1,
            content="i²의 값은?",
            options=[
                ("-1", True),
                ("1", False),
                ("i", False),
                ("0", False)
            ],
            correct="A",
            explanation="허수단위 i의 정의: i² = -1",
            points=10
        ),
        mc(
            id="h1-conc-002",
            concept_id="concept-h1-complex",
            category="concept",
            part="algebra",
            difficulty=2,
            content="(2 + 3i) + (1 - i)를 계산하시오.",
            options=[
                ("3 + 2i", True),
                ("3 + 4i", False),
                ("2 + 2i", False),
                ("3 - 2i", False)
            ],
            correct="A",
            explanation="실수부끼리, 허수부끼리 더하면: (2+1) + (3-1)i = 3 + 2i",
            points=10
        ),
        mc(
            id="h1-conc-003",
            concept_id="concept-h1-complex",
            category="concept",
            part="algebra",
            difficulty=3,
            content="i³의 값은?",
            options=[
                ("-i", True),
                ("i", False),
                ("-1", False),
                ("1", False)
            ],
            correct="A",
            explanation="i³ = i² × i = -1 × i = -i",
            points=10
        ),

        # 복소수 연산 (난이도 4-6)
        mc(
            id="h1-conc-004",
            concept_id="concept-h1-complex",
            category="concept",
            part="algebra",
            difficulty=4,
            content="(1 + i)(2 - i)를 계산하시오.",
            options=[
                ("3 + i", True),
                ("2 - i", False),
                ("3 - i", False),
                ("2 + i", False)
            ],
            correct="A",
            explanation="2 - i + 2i - i² = 2 + i - (-1) = 3 + i",
            points=10
        ),
        mc(
            id="h1-conc-005",
            concept_id="concept-h1-complex",
            category="concept",
            part="algebra",
            difficulty=5,
            content="복소수 z = 3 - 4i의 켤레복소수는?",
            options=[
                ("3 + 4i", True),
                ("-3 + 4i", False),
                ("-3 - 4i", False),
                ("4 - 3i", False)
            ],
            correct="A",
            explanation="켤레복소수는 허수부의 부호를 바꾼 것",
            points=10
        ),
        mc(
            id="h1-conc-006",
            concept_id="concept-h1-complex",
            category="concept",
            part="algebra",
            difficulty=6,
            content="|3 + 4i|의 값은?",
            options=[
                ("5", True),
                ("7", False),
                ("3", False),
                ("4", False)
            ],
            correct="A",
            explanation="|a + bi| = √(a² + b²) = √(9 + 16) = √25 = 5",
            points=10
        ),

        # 이차방정식 판별식 (난이도 3-6)
        mc(
            id="h1-conc-007",
            concept_id="concept-h1-quad-ineq",
            category="concept",
            part="algebra",
            difficulty=3,
            content="x² - 4x + 4 = 0의 판별식 D의 값은?",
            options=[
                ("0", True),
                ("4", False),
                ("16", False),
                ("-4", False)
            ],
            correct="A",
            explanation="D = b² - 4ac = 16 - 16 = 0 (중근)",
            points=10
        ),
        mc(
            id="h1-conc-008",
            concept_id="concept-h1-quad-ineq",
            category="concept",
            part="algebra",
            difficulty=5,
            content="x² + 2x + k = 0이 서로 다른 두 실근을 가질 조건은?",
            options=[
                ("k < 1", True),
                ("k > 1", False),
                ("k = 1", False),
                ("k ≤ 1", False)
            ],
            correct="A",
            explanation="D > 0: 4 - 4k > 0, k < 1",
            points=10
        ),
        mc(
            id="h1-conc-009",
            concept_id="concept-h1-quad-ineq",
            category="concept",
            part="algebra",
            difficulty=6,
            content="x² - 6x + 9 = 0의 두 근이 α, β일 때, α + β의 값은?",
            options=[
                ("6", True),
                ("-6", False),
                ("9", False),
                ("3", False)
            ],
            correct="A",
            explanation="근과 계수의 관계: α + β = -b/a = 6",
            points=10
        ),

        # 집합 (난이도 2-5)
        mc(
            id="h1-conc-010",
            concept_id="concept-h1-set",
            category="concept",
            part="logic",
            difficulty=2,
            content="A = {1, 2, 3}, B = {2, 3, 4}일 때, A ∩ B는?",
            options=[
                ("{2, 3}", True),
                ("{1, 2, 3, 4}", False),
                ("{1}", False),
                ("{4}", False)
            ],
            correct="A",
            explanation="교집합은 두 집합의 공통 원소",
            points=10
        ),
        mc(
            id="h1-conc-011",
            concept_id="concept-h1-set",
            category="concept",
            part="logic",
            difficulty=4,
            content="전체집합 U = {1, 2, 3, 4, 5}, A = {1, 2, 3}일 때, A의 여집합은?",
            options=[
                ("{4, 5}", True),
                ("{1, 2, 3}", False),
                ("{3, 4, 5}", False),
                ("{2, 3, 4, 5}", False)
            ],
            correct="A",
            explanation="여집합은 전체집합에서 A를 뺀 것",
            points=10
        ),

        # 명제 (난이도 6-10)
        mc(
            id="h1-conc-012",
            concept_id="concept-h1-set",
            category="concept",
            part="logic",
            difficulty=8,
            content="명제 'p → q'의 대우는?",
            options=[
                ("~q → ~p", True),
                ("q → p", False),
                ("~p → ~q", False),
                ("p → ~q", False)
            ],
            correct="A",
            explanation="대우는 가정과 결론을 모두 부정하고 순서를 바꾼 것",
            points=10
        )
    ]
