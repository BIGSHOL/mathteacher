"""초등 4학년 연산 문제 시드 데이터."""
from app.seeds._base import mc, concept


def get_concepts():
    """연산 관련 개념 반환."""
    return [
        concept(
            id="concept-e4-comp",
            name="큰 수의 곱셈과 나눗셈, 분수의 덧셈과 뺄셈",
            grade="elementary_4",
            category="computation",
            part="arithmetic",
            description="세 자리 수와 두 자리 수의 곱셈, 나눗셈과 같은 분모의 분수의 덧셈과 뺄셈을 이해하고 계산할 수 있습니다.",
        ),
    ]


def get_questions():
    """연산 문제 반환."""
    return [
        # 난이도 1-3: 기초 연산
        mc(
            id="e4-comp-001",
            concept_id="concept-e4-comp",
            category="computation",
            part="arithmetic",
            difficulty=1,
            content="245 × 3을 계산하세요.",
            options=[
                ("725", "725"),
                ("735", "735"),
                ("745", "745"),
                ("755", "755"),
            ],
            correct="B",
            explanation="245 × 3 = 735입니다. 5×3=15(1 올림), 4×3+1=13(1 올림), 2×3+1=7이므로 735입니다.",
            points=10,
        ),
        mc(
            id="e4-comp-002",
            concept_id="concept-e4-comp",
            category="computation",
            part="arithmetic",
            difficulty=2,
            content="96 ÷ 8을 계산하세요.",
            options=[
                ("11", "11"),
                ("12", "12"),
                ("13", "13"),
                ("14", "14"),
            ],
            correct="B",
            explanation="96 ÷ 8 = 12입니다. 8 × 12 = 96이므로 12가 정답입니다.",
            points=10,
        ),
        mc(
            id="e4-comp-003",
            concept_id="concept-e4-comp",
            category="computation",
            part="arithmetic",
            difficulty=3,
            content="2/5 + 1/5을 계산하세요.",
            options=[
                ("2/5", "2/5"),
                ("3/5", "3/5"),
                ("3/10", "3/10"),
                ("1/5", "1/5"),
            ],
            correct="B",
            explanation="분모가 같은 분수의 덧셈은 분자끼리 더합니다. 2/5 + 1/5 = 3/5입니다.",
            points=10,
        ),

        # 난이도 4-6: 중급 연산
        mc(
            id="e4-comp-004",
            concept_id="concept-e4-comp",
            category="computation",
            part="arithmetic",
            difficulty=4,
            content="134 × 24를 계산하세요.",
            options=[
                ("3206", "3206"),
                ("3216", "3216"),
                ("3226", "3226"),
                ("3236", "3236"),
            ],
            correct="B",
            explanation="134 × 24 = 3216입니다. 134×4=536, 134×20=2680, 536+2680=3216입니다.",
            points=10,
        ),
        mc(
            id="e4-comp-005",
            concept_id="concept-e4-comp",
            category="computation",
            part="arithmetic",
            difficulty=5,
            content="756 ÷ 12를 계산하세요.",
            options=[
                ("61", "61"),
                ("62", "62"),
                ("63", "63"),
                ("64", "64"),
            ],
            correct="C",
            explanation="756 ÷ 12 = 63입니다. 12 × 63 = 756이므로 63이 정답입니다.",
            points=10,
        ),
        mc(
            id="e4-comp-006",
            concept_id="concept-e4-comp",
            category="computation",
            part="arithmetic",
            difficulty=6,
            content="4/7 - 2/7을 계산하세요.",
            options=[
                ("1/7", "1/7"),
                ("2/7", "2/7"),
                ("3/7", "3/7"),
                ("2/0", "2/0"),
            ],
            correct="B",
            explanation="분모가 같은 분수의 뺄셈은 분자끼리 뺍니다. 4/7 - 2/7 = 2/7입니다.",
            points=10,
        ),

        # 난이도 7-10: 고급 연산
        mc(
            id="e4-comp-007",
            concept_id="concept-e4-comp",
            category="computation",
            part="arithmetic",
            difficulty=7,
            content="358 × 47을 계산하세요.",
            options=[
                ("16726", "16726"),
                ("16826", "16826"),
                ("16926", "16926"),
                ("17026", "17026"),
            ],
            correct="A",
            explanation="358 × 47 = 16826입니다. 358×7=2506, 358×40=14320, 2506+14320=16826입니다.",
            points=10,
        ),
        mc(
            id="e4-comp-008",
            concept_id="concept-e4-comp",
            category="computation",
            part="arithmetic",
            difficulty=8,
            content="1248 ÷ 16을 계산하세요.",
            options=[
                ("76", "76"),
                ("77", "77"),
                ("78", "78"),
                ("79", "79"),
            ],
            correct="C",
            explanation="1248 ÷ 16 = 78입니다. 16 × 78 = 1248이므로 78이 정답입니다.",
            points=10,
        ),
        mc(
            id="e4-comp-009",
            concept_id="concept-e4-comp",
            category="computation",
            part="arithmetic",
            difficulty=9,
            content="5/9 + 2/9 - 3/9을 계산하세요.",
            options=[
                ("3/9", "3/9"),
                ("4/9", "4/9"),
                ("5/9", "5/9"),
                ("6/9", "6/9"),
            ],
            correct="B",
            explanation="분모가 같은 분수는 분자끼리 계산합니다. 5 + 2 - 3 = 4이므로 4/9입니다.",
            points=10,
        ),
        mc(
            id="e4-comp-010",
            concept_id="concept-e4-comp",
            category="computation",
            part="arithmetic",
            difficulty=10,
            content="다음 중 계산 결과가 가장 작은 것은?",
            options=[
                ("576 × 28", "576 × 28"),
                ("1872 ÷ 12", "1872 ÷ 12"),
                ("7/11 + 3/11", "7/11 + 3/11"),
                ("489 × 34", "489 × 34"),
            ],
            correct="B",
            explanation="각각 계산하면 A: 16128, B: 156, C: 10/11 ≈ 0.91, D: 16626입니다. C가 가장 작습니다.",
            points=10,
        ),
        mc(
            id="e4-comp-011",
            concept_id="concept-e4-comp",
            category="computation",
            part="arithmetic",
            difficulty=10,
            content="687 × 53을 계산하세요.",
            options=[
                ("36311", "36311"),
                ("36411", "36411"),
                ("36511", "36511"),
                ("36611", "36611"),
            ],
            correct="D",
            explanation="687 × 53 = 36411입니다. 687×3=2061, 687×50=34350, 2061+34350=36411입니다.",
            points=10,
        ),
    ]
