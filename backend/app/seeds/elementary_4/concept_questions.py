"""초등 4학년 도형 개념 문제 시드 데이터."""
from app.seeds._base import mc, concept


def get_concepts():
    """도형 개념 반환."""
    return [
        concept(
            id="concept-e4-conc",
            name="각도와 도형",
            grade="elementary_4",
            category="concept",
            part="geometry",
            description="각도의 종류, 수직과 평행, 삼각형과 사각형의 분류를 이해할 수 있습니다.",
        ),
    ]


def get_questions():
    """도형 개념 문제 반환."""
    return [
        # 난이도 1-3: 기초 개념
        mc(
            id="e4-conc-001",
            concept_id="concept-e4-conc",
            category="concept",
            part="geometry",
            difficulty=1,
            content="직각은 몇 도인가요?",
            options=[
                ("45도", "45도"),
                ("60도", "60도"),
                ("90도", "90도"),
                ("180도", "180도"),
            ],
            correct="C",
            explanation="직각은 90도입니다.",
            points=10,
        ),
        mc(
            id="e4-conc-002",
            concept_id="concept-e4-conc",
            category="concept",
            part="geometry",
            difficulty=2,
            content="90도보다 작은 각을 무엇이라고 하나요?",
            options=[
                ("직각", "직각"),
                ("예각", "예각"),
                ("둔각", "둔각"),
                ("평각", "평각"),
            ],
            correct="B",
            explanation="90도보다 작은 각을 예각이라고 합니다.",
            points=10,
        ),
        mc(
            id="e4-conc-003",
            concept_id="concept-e4-conc",
            category="concept",
            part="geometry",
            difficulty=3,
            content="두 직선이 만나서 이루는 각이 90도일 때, 이 두 직선은 어떤 관계인가요?",
            options=[
                ("평행", "평행"),
                ("수직", "수직"),
                ("일치", "일치"),
                ("교차", "교차"),
            ],
            correct="B",
            explanation="두 직선이 만나서 이루는 각이 90도일 때 수직이라고 합니다.",
            points=10,
        ),

        # 난이도 4-6: 중급 개념
        mc(
            id="e4-conc-004",
            concept_id="concept-e4-conc",
            category="concept",
            part="geometry",
            difficulty=4,
            content="둔각은 몇 도보다 크고 몇 도보다 작은가요?",
            options=[
                ("0도보다 크고 90도보다 작다", "0도보다 크고 90도보다 작다"),
                ("90도보다 크고 180도보다 작다", "90도보다 크고 180도보다 작다"),
                ("180도보다 크고 360도보다 작다", "180도보다 크고 360도보다 작다"),
                ("90도와 같다", "90도와 같다"),
            ],
            correct="B",
            explanation="둔각은 90도보다 크고 180도보다 작은 각입니다.",
            points=10,
        ),
        mc(
            id="e4-conc-005",
            concept_id="concept-e4-conc",
            category="concept",
            part="geometry",
            difficulty=5,
            content="평행한 두 직선 사이의 거리는 어떤 특징이 있나요?",
            options=[
                ("점점 멀어진다", "점점 멀어진다"),
                ("점점 가까워진다", "점점 가까워진다"),
                ("어디서나 같다", "어디서나 같다"),
                ("만난다", "만난다"),
            ],
            correct="C",
            explanation="평행한 두 직선 사이의 거리는 어디서나 같습니다.",
            points=10,
        ),
        mc(
            id="e4-conc-006",
            concept_id="concept-e4-conc",
            category="concept",
            part="geometry",
            difficulty=6,
            content="세 각이 모두 예각인 삼각형을 무엇이라고 하나요?",
            options=[
                ("직각삼각형", "직각삼각형"),
                ("예각삼각형", "예각삼각형"),
                ("둔각삼각형", "둔각삼각형"),
                ("정삼각형", "정삼각형"),
            ],
            correct="B",
            explanation="세 각이 모두 예각인 삼각형을 예각삼각형이라고 합니다.",
            points=10,
        ),

        # 난이도 7-10: 고급 개념
        mc(
            id="e4-conc-007",
            concept_id="concept-e4-conc",
            category="concept",
            part="geometry",
            difficulty=7,
            content="삼각형의 세 각의 크기의 합은 몇 도인가요?",
            options=[
                ("90도", "90도"),
                ("180도", "180도"),
                ("270도", "270도"),
                ("360도", "360도"),
            ],
            correct="B",
            explanation="삼각형의 세 각의 크기의 합은 항상 180도입니다.",
            points=10,
        ),
        mc(
            id="e4-conc-008",
            concept_id="concept-e4-conc",
            category="concept",
            part="geometry",
            difficulty=8,
            content="네 각이 모두 직각인 사각형은?",
            options=[
                ("정사각형만", "정사각형만"),
                ("직사각형만", "직사각형만"),
                ("정사각형과 직사각형", "정사각형과 직사각형"),
                ("평행사변형", "평행사변형"),
            ],
            correct="C",
            explanation="네 각이 모두 직각인 사각형은 정사각형과 직사각형입니다.",
            points=10,
        ),
        mc(
            id="e4-conc-009",
            concept_id="concept-e4-conc",
            category="concept",
            part="geometry",
            difficulty=9,
            content="삼각형에서 한 각이 100도일 때, 이 삼각형은?",
            options=[
                ("예각삼각형", "예각삼각형"),
                ("직각삼각형", "직각삼각형"),
                ("둔각삼각형", "둔각삼각형"),
                ("알 수 없다", "알 수 없다"),
            ],
            correct="C",
            explanation="한 각이 100도로 둔각이므로 이 삼각형은 둔각삼각형입니다.",
            points=10,
        ),
        mc(
            id="e4-conc-010",
            concept_id="concept-e4-conc",
            category="concept",
            part="geometry",
            difficulty=10,
            content="사각형의 네 각의 크기의 합은 몇 도인가요?",
            options=[
                ("180도", "180도"),
                ("270도", "270도"),
                ("360도", "360도"),
                ("450도", "450도"),
            ],
            correct="C",
            explanation="사각형의 네 각의 크기의 합은 항상 360도입니다.",
            points=10,
        ),
        mc(
            id="e4-conc-011",
            concept_id="concept-e4-conc",
            category="concept",
            part="geometry",
            difficulty=10,
            content="마름모의 특징이 아닌 것은?",
            options=[
                ("네 변의 길이가 모두 같다", "네 변의 길이가 모두 같다"),
                ("마주 보는 두 쌍의 변이 평행하다", "마주 보는 두 쌍의 변이 평행하다"),
                ("네 각이 모두 직각이다", "네 각이 모두 직각이다"),
                ("마주 보는 각의 크기가 같다", "마주 보는 각의 크기가 같다"),
            ],
            correct="C",
            explanation="마름모는 네 변의 길이가 모두 같고 평행하지만, 네 각이 모두 직각인 것은 아닙니다. 네 각이 모두 직각이면 정사각형입니다.",
            points=10,
        ),
    ]
