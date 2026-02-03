"""초등 5학년 개념 문제 - 2022 개정 교육과정 기준 (3,6,7,9,11,12단원)."""

from .._base import mc, concept, test


def get_concept_data() -> dict:
    """초등 5학년 개념 문제/테스트 반환."""
    concepts = [
        concept(
            id="concept-e5-correspondence",
            name="규칙과 대응",
            grade="elementary_5",
            category="concept",
            part="algebra",
            description="두 양 사이의 대응 관계를 이해하고 기호(○, △)를 사용하여 규칙을 식으로 나타내며 변수 개념의 기초를 습득합니다.",
        ),
        concept(
            id="concept-e5-polygon-area",
            name="다각형의 둘레와 넓이",
            grade="elementary_5",
            category="concept",
            part="geo",
            description="직사각형에서 평행사변형, 삼각형, 마름모, 사다리꼴 넓이 공식을 등적 변형으로 유도하고 활용합니다.",
        ),
        concept(
            id="concept-e5-range-rounding",
            name="수의 범위와 어림하기",
            grade="elementary_5",
            category="concept",
            part="calc",
            description="이상/이하/초과/미만의 차이를 이해하고 올림/버림/반올림의 상황별 활용 방법을 습득합니다.",
        ),
        concept(
            id="concept-e5-congruence",
            name="합동과 대칭",
            grade="elementary_5",
            category="concept",
            part="geo",
            description="합동의 개념과 대응 관계를 이해하고 선대칭도형과 점대칭도형의 성질을 구별합니다.",
        ),
        concept(
            id="concept-e5-cuboid",
            name="직육면체",
            grade="elementary_5",
            category="concept",
            part="geo",
            description="직육면체와 정육면체의 구성 요소(면/모서리/꼭짓점), 겨냥도, 전개도를 이해하고 표현합니다.",
        ),
        concept(
            id="concept-e5-average",
            name="평균과 가능성",
            grade="elementary_5",
            category="concept",
            part="data",
            description="평균의 의미를 이해하고 계산하며, 가능성을 수치(0, 1/2, 1)로 표현하는 확률의 직관을 기릅니다.",
        ),
    ]

    questions = [
        # 3단원: 규칙과 대응 (3문제, 난이도 2-4)
        mc(
            id="e5-conc-001",
            concept_id="concept-e5-correspondence",
            category="concept",
            part="algebra",
            difficulty=2,
            content="자전거 1대에는 바퀴가 2개 있습니다. 자전거가 ○대 있을 때 바퀴의 수를 식으로 나타내면?",
            options=["○ + 2", "○ × 2", "○ ÷ 2", "2 - ○"],
            correct="B",
            explanation="자전거 수에 비례하여 바퀴 수가 증가합니다. 바퀴 수 = 자전거 수 × 2 = ○ × 2입니다. 이는 정비례 관계의 기초입니다.",
            points=10,
        ),
        mc(
            id="e5-conc-002",
            concept_id="concept-e5-correspondence",
            category="concept",
            part="algebra",
            difficulty=3,
            content="형의 나이는 동생의 나이보다 3살 많습니다. 동생의 나이가 △살일 때, 형의 나이는?",
            options=["△ + 3", "△ - 3", "△ × 3", "△ ÷ 3"],
            correct="A",
            explanation="형의 나이 = 동생의 나이 + 3 = △ + 3입니다. 이는 덧셈 관계(y = x + a)로 나타낼 수 있습니다.",
            points=10,
        ),
        mc(
            id="e5-conc-003",
            concept_id="concept-e5-correspondence",
            category="concept",
            part="algebra",
            difficulty=4,
            content="다음 대응 관계에서 규칙을 찾으시오.\n\n입력: 2 → 출력: 7\n입력: 3 → 출력: 10\n입력: 4 → 출력: 13\n입력: ○ → 출력: ?",
            options=["○ + 5", "○ × 3 + 1", "○ × 2 + 3", "○ × 4 - 1"],
            correct="B",
            explanation="규칙: (입력 × 3) + 1 = 출력. 2×3+1=7, 3×3+1=10, 4×3+1=13. 따라서 출력 = ○ × 3 + 1입니다.",
            points=10,
        ),

        # 6단원: 다각형의 둘레와 넓이 (3문제, 난이도 3-5)
        mc(
            id="e5-conc-004",
            concept_id="concept-e5-polygon-area",
            category="concept",
            part="geo",
            difficulty=3,
            content="평행사변형의 넓이를 구하는 공식은?",
            options=["가로 × 세로", "밑변 × 높이", "밑변 × 높이 ÷ 2", "대각선 × 대각선 ÷ 2"],
            correct="B",
            explanation="평행사변형을 잘라서 직사각형으로 등적 변형하면 넓이 = 밑변 × 높이입니다. 높이는 밑변에 수직인 선분의 길이입니다.",
            points=10,
        ),
        mc(
            id="e5-conc-005",
            concept_id="concept-e5-polygon-area",
            category="concept",
            part="geo",
            difficulty=4,
            content="삼각형의 넓이가 (밑변 × 높이 ÷ 2)인 이유는?",
            options=[
                "삼각형은 사각형의 절반이므로",
                "2개 붙이면 평행사변형이 되므로",
                "높이를 2로 나눠야 하므로",
                "밑변이 절반으로 줄어드므로"
            ],
            correct="B",
            explanation="똑같은 삼각형 2개를 붙이면 평행사변형이 됩니다. 따라서 삼각형 넓이 = (평행사변형 넓이) ÷ 2 = (밑변 × 높이) ÷ 2입니다. 오답 C는 ÷2를 누락하는 흔한 오류입니다. ★★★",
            points=10,
        ),
        mc(
            id="e5-conc-006",
            concept_id="concept-e5-polygon-area",
            category="concept",
            part="geo",
            difficulty=5,
            content="사다리꼴의 넓이 공식은 (윗변 + 아랫변) × 높이 ÷ 2입니다. 다음 중 이 공식의 유도 과정은?",
            options=[
                "직사각형을 반으로 잘랐으므로",
                "똑같은 사다리꼴 2개를 붙이면 평행사변형이 되므로",
                "평행사변형의 대각선이 사다리꼴이므로",
                "삼각형 2개의 넓이를 더했으므로"
            ],
            correct="B",
            explanation="똑같은 사다리꼴 2개를 180° 돌려 붙이면 밑변이 (윗변 + 아랫변)인 평행사변형이 됩니다. 따라서 사다리꼴 넓이 = 평행사변형 넓이 ÷ 2입니다. ÷2 누락 주의! ★★★",
            points=10,
        ),

        # 7단원: 수의 범위와 어림하기 (3문제, 난이도 3-5)
        mc(
            id="e5-conc-007",
            concept_id="concept-e5-range-rounding",
            category="concept",
            part="calc",
            difficulty=3,
            content="5 이상 10 미만인 자연수는 모두 몇 개입니까?",
            options=["4개", "5개", "6개", "7개"],
            correct="B",
            explanation="5 이상(5 포함) 10 미만(10 불포함): 5, 6, 7, 8, 9로 총 5개입니다. 이상/이하는 경계값 포함(●), 초과/미만은 불포함(○)입니다.",
            points=10,
        ),
        mc(
            id="e5-conc-008",
            concept_id="concept-e5-range-rounding",
            category="concept",
            part="calc",
            difficulty=4,
            content="456을 십의 자리에서 반올림하면?",
            options=["400", "450", "460", "500"],
            correct="D",
            explanation="십의 자리(5)가 5 이상이므로 올림합니다. 456 → 500입니다. '~에서 반올림'은 해당 자리를 보고 윗자리에 반영합니다. ★★★",
            points=10,
        ),
        mc(
            id="e5-conc-009",
            concept_id="concept-e5-range-rounding",
            category="concept",
            part="calc",
            difficulty=5,
            content="사과 127개를 상자에 10개씩 담으려고 합니다. 필요한 상자의 수는? (어림 방법 선택)",
            options=["버림: 12개", "올림: 13개", "반올림: 13개", "버림: 13개"],
            correct="B",
            explanation="127 ÷ 10 = 12.7 → 모든 사과를 담으려면 13개 필요(올림). 버림(12)은 7개가 남고, 반올림은 상황에 맞지 않습니다. 물건 묶음 구매 시 올림 사용! ★★★",
            points=10,
        ),

        # 9단원: 합동과 대칭 (3문제, 난이도 3-5)
        mc(
            id="e5-conc-010",
            concept_id="concept-e5-congruence",
            category="concept",
            part="geo",
            difficulty=3,
            content="합동인 두 도형의 성질로 옳은 것은?",
            options=[
                "모양만 같다",
                "크기만 같다",
                "모양과 크기가 모두 같다",
                "대칭축이 있다"
            ],
            correct="C",
            explanation="합동은 모양과 크기가 모두 같아 완전히 겹쳐지는 관계입니다. 대응변의 길이와 대응각의 크기가 각각 같습니다.",
            points=10,
        ),
        mc(
            id="e5-conc-011",
            concept_id="concept-e5-congruence",
            category="concept",
            part="geo",
            difficulty=4,
            content="선대칭도형에서 대칭축의 성질은?",
            options=[
                "대응점을 이은 선분의 중점을 지난다",
                "대응점을 이은 선분을 수직이등분한다",
                "도형의 무게중심을 지난다",
                "도형의 대각선이다"
            ],
            correct="B",
            explanation="선대칭도형의 대칭축은 대응점을 이은 선분을 수직이등분합니다. 대칭축을 따라 접으면 완전히 겹쳐집니다. 오답 A는 점대칭의 성질입니다.",
            points=10,
        ),
        mc(
            id="e5-conc-012",
            concept_id="concept-e5-congruence",
            category="concept",
            part="geo",
            difficulty=5,
            content="평행사변형이 점대칭도형인지 선대칭도형인지 판단하시오.",
            options=[
                "점대칭도형이다",
                "선대칭도형이다",
                "둘 다이다",
                "둘 다 아니다"
            ],
            correct="A",
            explanation="평행사변형은 대각선의 교점을 중심으로 180° 돌리면 겹치므로 점대칭도형입니다. 하지만 대칭축은 없습니다(선대칭 X). 오답 유도: 평행사변형의 대각선을 대칭축으로 착각 ★★★",
            points=10,
        ),

        # 11단원: 직육면체 (3문제, 난이도 3-5)
        mc(
            id="e5-conc-013",
            concept_id="concept-e5-cuboid",
            category="concept",
            part="geo",
            difficulty=3,
            content="직육면체의 면은 몇 개입니까?",
            options=["4개", "6개", "8개", "12개"],
            correct="B",
            explanation="직육면체는 6개의 면(앞뒤·좌우·위아래)으로 이루어져 있습니다. 모서리 12개, 꼭짓점 8개입니다.",
            points=10,
        ),
        mc(
            id="e5-conc-014",
            concept_id="concept-e5-cuboid",
            category="concept",
            part="geo",
            difficulty=4,
            content="직육면체에서 한 면과 평행한 면은 몇 개입니까?",
            options=["1개", "2개", "3개", "4개"],
            correct="A",
            explanation="직육면체에서 한 면과 평행한 면은 마주 보는 1개뿐입니다. 총 3쌍의 평행한 면이 있습니다.",
            points=10,
        ),
        mc(
            id="e5-conc-015",
            concept_id="concept-e5-cuboid",
            category="concept",
            part="geo",
            difficulty=5,
            content="직육면체의 전개도에 대한 설명으로 옳은 것은?",
            options=[
                "전개도는 오직 한 가지만 있다",
                "전개도는 여러 가지 모양이 가능하다",
                "전개도에는 항상 정사각형이 있다",
                "전개도는 십자가 모양만 가능하다"
            ],
            correct="B",
            explanation="직육면체의 전개도는 모서리를 자르는 위치에 따라 여러 가지 모양으로 만들 수 있습니다. 단, 마주 보는 면이 평행하게 배치되어야 합니다.",
            points=10,
        ),

        # 12단원: 평균과 가능성 (3문제, 난이도 3-5)
        mc(
            id="e5-conc-016",
            concept_id="concept-e5-average",
            category="concept",
            part="data",
            difficulty=3,
            content="3, 5, 7, 9의 평균을 구하시오.",
            options=["5", "6", "7", "8"],
            correct="B",
            explanation="평균 = (3 + 5 + 7 + 9) ÷ 4 = 24 ÷ 4 = 6입니다. 평균 = (모든 값의 합) ÷ (자료의 개수)입니다.",
            points=10,
        ),
        mc(
            id="e5-conc-017",
            concept_id="concept-e5-average",
            category="concept",
            part="data",
            difficulty=4,
            content="시험 점수: 80, 90, 0, 85, 95. 평균을 구하시오. (0점 포함 주의)",
            options=["70", "80", "85", "90"],
            correct="A",
            explanation="평균 = (80 + 90 + 0 + 85 + 95) ÷ 5 = 350 ÷ 5 = 70입니다. 0점도 자료에 포함하여 개수를 5개로 계산해야 합니다. 오답 유도: 0을 제외하고 4개로 나누기 ★★",
            points=10,
        ),
        mc(
            id="e5-conc-018",
            concept_id="concept-e5-average",
            category="concept",
            part="data",
            difficulty=5,
            content="주사위를 던질 때, 6의 약수(1,2,3,6)가 나올 가능성을 수치로 표현하면?",
            options=["0 (불가능)", "1/2 (반반)", "1 (확실)", "2/3 (반반보다 높음)"],
            correct="D",
            explanation="주사위 눈: 1,2,3,4,5,6 총 6가지. 6의 약수: 1,2,3,6로 4가지. 가능성 = 4/6 = 2/3입니다. 2/3 > 1/2이므로 '일 것 같다' 수준입니다.",
            points=10,
        ),
    ]

    tests = [
        test(
            id="test-e5-concept-algebra-geo",
            title="초5 개념 테스트 (대응·도형)",
            description="규칙과 대응, 다각형 넓이, 합동과 대칭, 직육면체 (3,6,9,11단원)",
            grade="elementary_5",
            concept_ids=[
                "concept-e5-correspondence",
                "concept-e5-polygon-area",
                "concept-e5-congruence",
                "concept-e5-cuboid",
            ],
            question_ids=[f"e5-conc-{str(i).zfill(3)}" for i in range(1, 16)],
            time_limit_minutes=20,
            use_question_pool=True,
            questions_per_attempt=12,
        ),
        test(
            id="test-e5-concept-data",
            title="초5 개념 테스트 (수·자료)",
            description="수의 범위와 어림하기, 평균과 가능성 (7,12단원)",
            grade="elementary_5",
            concept_ids=[
                "concept-e5-range-rounding",
                "concept-e5-average",
            ],
            question_ids=[
                f"e5-conc-{str(i).zfill(3)}" for i in range(7, 10)
            ] + [
                f"e5-conc-{str(i).zfill(3)}" for i in range(16, 19)
            ],
            time_limit_minutes=15,
            use_question_pool=True,
            questions_per_attempt=6,
        ),
    ]

    return {"concepts": concepts, "questions": questions, "tests": tests}
