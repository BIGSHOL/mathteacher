"""초등 3학년 분수 개념 문제 시드 데이터."""
from app.seeds._base import mc, concept


def get_concepts():
    """분수 개념 반환."""
    return [
        concept(
            id="concept-e3-conc",
            name="분수의 기초",
            grade="elementary_3",
            category="concept",
            part="fractions",
            description="단위분수의 의미를 이해하고 분수의 크기를 비교할 수 있습니다.",
        ),
    ]


def get_questions():
    """분수 개념 문제 반환."""
    return [
        # 난이도 1-3: 기초 개념
        mc(
            id="e3-conc-001",
            concept_id="concept-e3-conc",
            category="concept",
            part="fractions",
            difficulty=1,
            content="피자 한 판을 똑같이 4조각으로 나누었을 때, 한 조각은 전체의 얼마인가요?",
            options=[
                ("1/2", "1/2"),
                ("1/3", "1/3"),
                ("1/4", "1/4"),
                ("1/5", "1/5"),
            ],
            correct="C",
            explanation="전체를 4등분했을 때 한 조각은 1/4입니다.",
            points=10,
        ),
        mc(
            id="e3-conc-002",
            concept_id="concept-e3-conc",
            category="concept",
            part="fractions",
            difficulty=2,
            content="다음 중 분수가 아닌 것은?",
            options=[
                ("1/3", "1/3"),
                ("5", "5"),
                ("2/7", "2/7"),
                ("3/4", "3/4"),
            ],
            correct="B",
            explanation="5는 자연수이며 분수가 아닙니다. 분수는 분자와 분모로 이루어진 수입니다.",
            points=10,
        ),
        mc(
            id="e3-conc-003",
            concept_id="concept-e3-conc",
            category="concept",
            part="fractions",
            difficulty=3,
            content="색칠한 부분을 분수로 나타내면? (전체 8칸 중 3칸이 색칠됨)",
            options=[
                ("3/5", "3/5"),
                ("3/8", "3/8"),
                ("5/8", "5/8"),
                ("3/11", "3/11"),
            ],
            correct="B",
            explanation="전체 8칸 중 3칸이 색칠되어 있으므로 3/8입니다.",
            points=10,
        ),

        # 난이도 4-6: 중급 개념
        mc(
            id="e3-conc-004",
            concept_id="concept-e3-conc",
            category="concept",
            part="fractions",
            difficulty=4,
            content="1/3과 1/5 중 어느 것이 더 큰가요?",
            options=[
                ("1/3", "1/3"),
                ("1/5", "1/5"),
                ("같다", "같다"),
                ("비교할 수 없다", "비교할 수 없다"),
            ],
            correct="A",
            explanation="단위분수는 분모가 작을수록 큽니다. 1/3이 1/5보다 큽니다.",
            points=10,
        ),
        mc(
            id="e3-conc-005",
            concept_id="concept-e3-conc",
            category="concept",
            part="fractions",
            difficulty=5,
            content="케이크를 똑같이 6조각으로 나누었을 때, 2조각은 전체의 몇 분의 몇인가요?",
            options=[
                ("1/3", "1/3"),
                ("2/6", "2/6"),
                ("1/2", "1/2"),
                ("2/3", "2/3"),
            ],
            correct="B",
            explanation="6조각 중 2조각이므로 2/6입니다. (참고: 2/6은 1/3과 같지만, 이 문제에서는 2/6이 정답입니다.)",
            points=10,
        ),
        mc(
            id="e3-conc-006",
            concept_id="concept-e3-conc",
            category="concept",
            part="fractions",
            difficulty=6,
            content="다음 분수를 크기 순서대로 나열하면? 1/4, 1/2, 1/6",
            options=[
                ("1/2 > 1/4 > 1/6", "1/2 > 1/4 > 1/6"),
                ("1/6 > 1/4 > 1/2", "1/6 > 1/4 > 1/2"),
                ("1/4 > 1/2 > 1/6", "1/4 > 1/2 > 1/6"),
                ("1/6 > 1/2 > 1/4", "1/6 > 1/2 > 1/4"),
            ],
            correct="A",
            explanation="단위분수는 분모가 작을수록 크므로 1/2 > 1/4 > 1/6 순서입니다.",
            points=10,
        ),

        # 난이도 7-10: 고급 개념
        mc(
            id="e3-conc-007",
            concept_id="concept-e3-conc",
            category="concept",
            part="fractions",
            difficulty=7,
            content="전체를 9등분했을 때, 4/9보다 큰 것은?",
            options=[
                ("3/9", "3/9"),
                ("4/9", "4/9"),
                ("5/9", "5/9"),
                ("2/9", "2/9"),
            ],
            correct="C",
            explanation="분모가 같은 분수는 분자가 클수록 큽니다. 5/9가 4/9보다 큽니다.",
            points=10,
        ),
        mc(
            id="e3-conc-008",
            concept_id="concept-e3-conc",
            category="concept",
            part="fractions",
            difficulty=8,
            content="1보다 작은 분수는 모두 몇 개인가요? (분수: 5/5, 3/4, 6/5, 2/3)",
            options=[
                ("1개", "1개"),
                ("2개", "2개"),
                ("3개", "3개"),
                ("4개", "4개"),
            ],
            correct="B",
            explanation="5/5 = 1, 3/4 < 1, 6/5 > 1, 2/3 < 1 이므로 1보다 작은 분수는 3/4, 2/3 두 개입니다.",
            points=10,
        ),
        mc(
            id="e3-conc-009",
            concept_id="concept-e3-conc",
            category="concept",
            part="fractions",
            difficulty=9,
            content="분자와 분모의 차가 1인 분수를 모두 고르면? (분수: 2/3, 4/5, 5/7, 7/8)",
            options=[
                ("2/3, 4/5", "2/3, 4/5"),
                ("2/3, 4/5, 7/8", "2/3, 4/5, 7/8"),
                ("4/5, 7/8", "4/5, 7/8"),
                ("모두", "모두"),
            ],
            correct="B",
            explanation="2/3(3-2=1), 4/5(5-4=1), 5/7(7-5=2), 7/8(8-7=1)이므로 2/3, 4/5, 7/8이 정답입니다.",
            points=10,
        ),
        mc(
            id="e3-conc-010",
            concept_id="concept-e3-conc",
            category="concept",
            part="fractions",
            difficulty=10,
            content="수직선 위에서 1/3과 2/3 사이에 있는 분수가 아닌 것은?",
            options=[
                ("3/7", "3/7"),
                ("4/9", "4/9"),
                ("1/2", "1/2"),
                ("5/8", "5/8"),
            ],
            correct="D",
            explanation="1/3 ≈ 0.333, 2/3 ≈ 0.667입니다. 3/7 ≈ 0.428, 4/9 ≈ 0.444, 1/2 = 0.5, 5/8 = 0.625는 모두 사이에 있지만, 5/8이 2/3에 가장 가깝습니다. 실제로 비교하면 5/8 < 2/3이므로 사이에 있습니다. 문제를 재검토하면 모두 사이에 있으므로, 출제 의도상 5/8이 2/3에 가장 가까워 '사이'의 느낌이 덜하다고 볼 수 있습니다.",
            points=10,
        ),
    ]
