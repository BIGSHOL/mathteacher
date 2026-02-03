"""초등 3학년 연산 문제 시드 데이터."""
from app.seeds._base import mc, concept


def get_concepts():
    """연산 관련 개념 반환."""
    return [
        concept(
            id="concept-e3-comp",
            name="세 자리 수의 덧셈, 뺄셈과 곱셈",
            grade="elementary_3",
            category="computation",
            part="arithmetic",
            description="세 자리 수의 덧셈과 뺄셈, 두 자리 수와 한 자리 수의 곱셈을 이해하고 계산할 수 있습니다.",
        ),
    ]


def get_questions():
    """연산 문제 반환."""
    return [
        # 난이도 1-3: 기초 연산
        mc(
            id="e3-comp-001",
            concept_id="concept-e3-comp",
            category="computation",
            part="arithmetic",
            difficulty=1,
            content="258 + 147을 계산하세요.",
            options=[
                ("395", "395"),
                ("405", "405"),
                ("415", "415"),
                ("305", "305"),
            ],
            correct="B",
            explanation="258 + 147 = 405입니다. 일의 자리부터 차례로 더하면 8+7=15(1 올림), 5+4+1=10(1 올림), 2+1+1=4이므로 405입니다.",
            points=10,
        ),
        mc(
            id="e3-comp-002",
            concept_id="concept-e3-comp",
            category="computation",
            part="arithmetic",
            difficulty=2,
            content="503 - 286을 계산하세요.",
            options=[
                ("217", "217"),
                ("227", "227"),
                ("317", "317"),
                ("207", "207"),
            ],
            correct="A",
            explanation="503 - 286 = 217입니다. 백의 자리에서 받아내림하여 계산하면 됩니다.",
            points=10,
        ),
        mc(
            id="e3-comp-003",
            concept_id="concept-e3-comp",
            category="computation",
            part="arithmetic",
            difficulty=3,
            content="34 × 6을 계산하세요.",
            options=[
                ("194", "194"),
                ("204", "204"),
                ("214", "214"),
                ("224", "224"),
            ],
            correct="B",
            explanation="34 × 6 = 204입니다. 4×6=24(2 올림), 3×6+2=20이므로 204입니다.",
            points=10,
        ),

        # 난이도 4-6: 중급 연산
        mc(
            id="e3-comp-004",
            concept_id="concept-e3-comp",
            category="computation",
            part="arithmetic",
            difficulty=4,
            content="675 + 289를 계산하세요.",
            options=[
                ("954", "954"),
                ("964", "964"),
                ("974", "974"),
                ("984", "984"),
            ],
            correct="B",
            explanation="675 + 289 = 964입니다. 일의 자리 5+9=14(1 올림), 십의 자리 7+8+1=16(1 올림), 백의 자리 6+2+1=9이므로 964입니다.",
            points=10,
        ),
        mc(
            id="e3-comp-005",
            concept_id="concept-e3-comp",
            category="computation",
            part="arithmetic",
            difficulty=4,
            content="724 - 458을 계산하세요.",
            options=[
                ("256", "256"),
                ("266", "266"),
                ("276", "276"),
                ("286", "286"),
            ],
            correct="B",
            explanation="724 - 458 = 266입니다. 십의 자리와 일의 자리에서 받아내림하여 계산합니다.",
            points=10,
        ),
        mc(
            id="e3-comp-006",
            concept_id="concept-e3-comp",
            category="computation",
            part="arithmetic",
            difficulty=5,
            content="58 × 7을 계산하세요.",
            options=[
                ("396", "396"),
                ("406", "406"),
                ("416", "416"),
                ("426", "426"),
            ],
            correct="B",
            explanation="58 × 7 = 406입니다. 8×7=56(5 올림), 5×7+5=40이므로 406입니다.",
            points=10,
        ),
        mc(
            id="e3-comp-007",
            concept_id="concept-e3-comp",
            category="computation",
            part="arithmetic",
            difficulty=6,
            content="835 + 478을 계산하세요.",
            options=[
                ("1303", "1303"),
                ("1313", "1313"),
                ("1323", "1323"),
                ("1333", "1333"),
            ],
            correct="B",
            explanation="835 + 478 = 1313입니다. 각 자리를 차례로 더하고 올림을 처리하면 됩니다.",
            points=10,
        ),

        # 난이도 7-10: 고급 연산
        mc(
            id="e3-comp-008",
            concept_id="concept-e3-comp",
            category="computation",
            part="arithmetic",
            difficulty=7,
            content="1000 - 673을 계산하세요.",
            options=[
                ("317", "317"),
                ("327", "327"),
                ("337", "337"),
                ("347", "347"),
            ],
            correct="B",
            explanation="1000 - 673 = 327입니다. 천의 자리에서 받아내림하여 계산합니다.",
            points=10,
        ),
        mc(
            id="e3-comp-009",
            concept_id="concept-e3-comp",
            category="computation",
            part="arithmetic",
            difficulty=8,
            content="89 × 9를 계산하세요.",
            options=[
                ("791", "791"),
                ("801", "801"),
                ("811", "811"),
                ("821", "821"),
            ],
            correct="B",
            explanation="89 × 9 = 801입니다. 9×9=81(8 올림), 8×9+8=80이므로 801입니다.",
            points=10,
        ),
        mc(
            id="e3-comp-010",
            concept_id="concept-e3-comp",
            category="computation",
            part="arithmetic",
            difficulty=9,
            content="567 + 834를 계산하세요.",
            options=[
                ("1391", "1391"),
                ("1401", "1401"),
                ("1411", "1411"),
                ("1421", "1421"),
            ],
            correct="B",
            explanation="567 + 834 = 1401입니다. 7+4=11(1 올림), 6+3+1=10(1 올림), 5+8+1=14이므로 1401입니다.",
            points=10,
        ),
        mc(
            id="e3-comp-011",
            concept_id="concept-e3-comp",
            category="computation",
            part="arithmetic",
            difficulty=10,
            content="다음 중 계산 결과가 가장 큰 것은?",
            options=[
                ("678 + 456", "678 + 456"),
                ("97 × 12", "97 × 12"),
                ("2000 - 835", "2000 - 835"),
                ("86 × 13", "86 × 13"),
            ],
            correct="B",
            explanation="각각 계산하면 A: 1134, B: 1164, C: 1165, D: 1118입니다. 따라서 2000 - 835 = 1165가 가장 큽니다.",
            points=10,
        ),
    ]
