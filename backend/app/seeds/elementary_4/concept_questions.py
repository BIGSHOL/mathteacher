"""초등 4학년 개념 문제 시드 데이터.

커버 단원:
  1학기 2단원 - 각도 (8개 개념)
  1학기 4단원 - 평면도형의 이동 (5개 개념)
  1학기 5단원 - 막대그래프 (4개 개념)
  1학기 6단원 - 규칙 찾기 (5개 개념)
  2학기 2단원 - 삼각형 (5개 개념)
  2학기 4단원 - 사각형 (7개 개념)
  2학기 5단원 - 꺾은선그래프 (5개 개념)
  2학기 6단원 - 다각형 (5개 개념)

총 44개 개념
"""
from app.seeds._base import mc, concept
from app.data.pdf_concept_map import E4_S1_CONCEPTS, E4_S2_CONCEPTS


def get_concepts():
    """개념 관련 개념 반환 (PDF 기반 세분화)."""
    # concept_questions.py가 다루는 단원만 필터링
    s1_chapters = {2, 4, 5, 6}
    s2_chapters = {2, 4, 5, 6}

    result = []

    # 1학기 개념 (2, 4, 5, 6단원)
    for c in E4_S1_CONCEPTS:
        if c["chapter_number"] in s1_chapters:
            result.append(concept(
                id=c["id"],
                name=c["name"],
                grade=c["grade"],
                category=c["category"],
                part=c["part"],
                description=c["description"],
            ))

    # 2학기 개념 (2, 4, 5, 6단원)
    for c in E4_S2_CONCEPTS:
        if c["chapter_number"] in s2_chapters:
            result.append(concept(
                id=c["id"],
                name=c["name"],
                grade=c["grade"],
                category=c["category"],
                part=c["part"],
                description=c["description"],
            ))

    return result


def get_questions():
    """개념 문제 반환."""
    return [
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 2단원: 각도 (8개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # e4-1-2-01: 각의 크기 비교
        mc(
            id="e4-1-2-01-cc-001",
            concept_id="e4-1-2-01",
            category="concept",
            part="geo",
            difficulty=1,
            content="두 각의 크기를 비교할 때, 각도기 없이 비교하는 방법은?",
            options=[
                "변의 길이로 비교한다",
                "두 각을 겹쳐서 비교한다",
                "각의 높이로 비교한다",
                "도형의 크기로 비교한다",
            ],
            correct="B",
            explanation="각도기 없이는 두 각을 겹쳐서 벌어진 정도를 직접 비교합니다.",
            points=10,
        ),

        # e4-1-2-02: 각의 크기 재기
        mc(
            id="e4-1-2-02-cc-001",
            concept_id="e4-1-2-02",
            category="concept",
            part="geo",
            difficulty=1,
            content="직각은 몇 도인가요?",
            options=[
                "45도",
                "60도",
                "90도",
                "180도",
            ],
            correct="C",
            explanation="직각은 90도입니다.",
            points=10,
        ),
        mc(
            id="e4-1-2-02-cc-002",
            concept_id="e4-1-2-02",
            category="concept",
            part="geo",
            difficulty=4,
            content="두 삼각형의 한 각의 크기가 같습니다. 하나는 변이 짧고 다른 하나는 변이 깁니다. 다음 중 옳은 것은?",
            options=[
                "변이 긴 삼각형의 각이 더 크다",
                "두 각의 크기는 같다",
                "변이 짧은 삼각형의 각이 더 크다",
                "비교할 수 없다",
            ],
            correct="B",
            explanation="각의 크기는 두 변이 벌어진 정도이며, 변의 길이와는 관계가 없습니다. '변이 길면 각도가 크다'는 것은 흔한 오해입니다.",
            points=10,
        ),

        # e4-1-2-03: 각 그리기
        mc(
            id="e4-1-2-03-cc-001",
            concept_id="e4-1-2-03",
            category="concept",
            part="geo",
            difficulty=3,
            content="각도기를 사용하여 50도 각을 그릴 때, 먼저 해야 할 일은?",
            options=[
                "반직선을 그린다",
                "각도기의 눈금 50을 찾는다",
                "각의 꼭짓점을 표시한다",
                "각도기를 놓을 곳을 정한다",
            ],
            correct="A",
            explanation="각을 그릴 때는 먼저 반직선(한 변)을 그린 후, 각도기의 중심을 꼭짓점에 맞추고 밑변을 반직선에 맞춘 다음 원하는 각도 눈금에 점을 찍고 연결합니다.",
            points=10,
        ),

        # e4-1-2-04: 직각보다 작은 각과 직각보다 큰 각
        mc(
            id="e4-1-2-04-cc-001",
            concept_id="e4-1-2-04",
            category="concept",
            part="geo",
            difficulty=2,
            content="70도 각은 어떤 각인가요?",
            options=[
                "예각",
                "직각",
                "둔각",
                "평각",
            ],
            correct="A",
            explanation="예각은 0도보다 크고 90도보다 작은 각입니다. 70도는 예각입니다.",
            points=10,
        ),
        mc(
            id="e4-1-2-04-cc-002",
            concept_id="e4-1-2-04",
            category="concept",
            part="geo",
            difficulty=3,
            content="120도 각은 어떤 각인가요?",
            options=[
                "예각",
                "직각",
                "둔각",
                "평각",
            ],
            correct="C",
            explanation="둔각은 90도보다 크고 180도보다 작은 각입니다. 120도는 둔각입니다.",
            points=10,
        ),

        # e4-1-2-05: 각도 어림하기
        mc(
            id="e4-1-2-05-cc-001",
            concept_id="e4-1-2-05",
            category="concept",
            part="geo",
            difficulty=4,
            content="각도기 없이 각도를 어림할 때, 기준으로 삼기 좋은 각도는?",
            options=[
                "30도와 60도",
                "45도와 90도",
                "20도와 40도",
                "50도와 70도",
            ],
            correct="B",
            explanation="45도(직각의 반)와 90도(직각)를 기준으로 삼으면 각도를 쉽게 어림할 수 있습니다.",
            points=10,
        ),

        # e4-1-2-06: 각도의 덧셈과 뺄셈
        mc(
            id="e4-1-2-06-cc-001",
            concept_id="e4-1-2-06",
            category="computation",
            part="geo",
            difficulty=2,
            content="45도 + 60도는 몇 도인가요?",
            options=[
                "95도",
                "100도",
                "105도",
                "110도",
            ],
            correct="C",
            explanation="각도의 덧셈은 도 단위끼리 더합니다. 45 + 60 = 105도입니다.",
            points=10,
        ),
        mc(
            id="e4-1-2-06-cc-002",
            concept_id="e4-1-2-06",
            category="computation",
            part="geo",
            difficulty=3,
            content="180도 - 65도는 몇 도인가요?",
            options=[
                "105도",
                "115도",
                "125도",
                "135도",
            ],
            correct="B",
            explanation="각도의 뺄셈은 도 단위끼리 뺍니다. 180 - 65 = 115도입니다.",
            points=10,
        ),

        # e4-1-2-07: 삼각형의 세 각의 크기의 합
        mc(
            id="e4-1-2-07-cc-001",
            concept_id="e4-1-2-07",
            category="concept",
            part="geo",
            difficulty=7,
            content="삼각형의 세 각의 크기의 합은 몇 도인가요?",
            options=[
                "90도",
                "180도",
                "270도",
                "360도",
            ],
            correct="B",
            explanation="삼각형의 세 각의 크기의 합은 모양이나 크기에 관계없이 항상 180도입니다.",
            points=10,
        ),
        mc(
            id="e4-1-2-07-cc-002",
            concept_id="e4-1-2-07",
            category="concept",
            part="geo",
            difficulty=5,
            content="삼각형의 두 각이 50도와 70도일 때, 나머지 한 각의 크기는?",
            options=[
                "50도",
                "60도",
                "70도",
                "80도",
            ],
            correct="B",
            explanation="삼각형의 세 각의 합은 180도입니다. 180 - 50 - 70 = 60도입니다.",
            points=10,
        ),

        # e4-1-2-08: 사각형의 네 각의 크기의 합
        mc(
            id="e4-1-2-08-cc-001",
            concept_id="e4-1-2-08",
            category="concept",
            part="geo",
            difficulty=5,
            content="사각형의 네 각의 크기의 합은 몇 도인가요?",
            options=[
                "180도",
                "270도",
                "360도",
                "540도",
            ],
            correct="C",
            explanation="사각형의 네 각의 크기의 합은 항상 360도입니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 4단원: 평면도형의 이동 (5개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # e4-1-4-01: 평면도형 밀기
        mc(
            id="e4-1-4-01-cc-001",
            concept_id="e4-1-4-01",
            category="concept",
            part="geo",
            difficulty=2,
            content="도형을 밀었을 때 변하는 것은?",
            options=[
                "모양",
                "크기",
                "위치",
                "방향",
            ],
            correct="C",
            explanation="밀기는 도형의 위치만 변화시키고, 모양·크기·방향은 변하지 않습니다.",
            points=10,
        ),

        # e4-1-4-02: 평면도형 뒤집기
        mc(
            id="e4-1-4-02-cc-001",
            concept_id="e4-1-4-02",
            category="concept",
            part="geo",
            difficulty=3,
            content="도형을 세로 축을 기준으로 뒤집으면 무엇이 바뀌나요?",
            options=[
                "상하가 바뀐다",
                "좌우가 바뀐다",
                "크기가 바뀐다",
                "모양이 바뀐다",
            ],
            correct="B",
            explanation="세로 축을 기준으로 뒤집으면 좌우가 바뀝니다. 가로 축을 기준으로 뒤집으면 상하가 바뀝니다.",
            points=10,
        ),

        # e4-1-4-03: 평면도형 돌리기
        mc(
            id="e4-1-4-03-cc-001",
            concept_id="e4-1-4-03",
            category="concept",
            part="geo",
            difficulty=5,
            content="글자 'ㄱ'을 오른쪽으로 뒤집은 결과와 시계방향으로 180° 돌린 결과는?",
            options=[
                "같다",
                "다르다",
                "뒤집기만 가능하다",
                "돌리기만 가능하다",
            ],
            correct="B",
            explanation="비대칭 도형(ㄱ, ㄴ, P 등)에서는 뒤집기와 180° 돌리기의 결과가 다릅니다. 뒤집기는 좌우가 반전되고, 돌리기는 상하좌우가 함께 바뀝니다.",
            points=10,
        ),
        mc(
            id="e4-1-4-03-cc-002",
            concept_id="e4-1-4-03",
            category="concept",
            part="geo",
            difficulty=7,
            content="도형을 시계방향으로 90° 돌린 것은 반시계방향으로 몇 도 돌린 것과 같은가요?",
            options=[
                "90도",
                "180도",
                "270도",
                "360도",
            ],
            correct="C",
            explanation="시계방향 90° 돌리기 = 반시계방향 270° 돌리기입니다. 시계 + 반시계 = 360°가 되어야 원래 위치입니다.",
            points=10,
        ),

        # e4-1-4-04: 평면도형 뒤집고 돌리기
        mc(
            id="e4-1-4-04-cc-001",
            concept_id="e4-1-4-04",
            category="concept",
            part="geo",
            difficulty=6,
            content="도형을 뒤집은 후 다시 돌릴 때, 어떤 순서로 하는지가 중요한가요?",
            options=[
                "순서는 중요하지 않다",
                "순서가 중요하다",
                "뒤집기만 하면 된다",
                "돌리기만 하면 된다",
            ],
            correct="B",
            explanation="뒤집기와 돌리기를 결합할 때는 순서가 중요합니다. 순서가 바뀌면 결과가 달라질 수 있습니다.",
            points=10,
        ),

        # e4-1-4-05: 무늬 꾸미기
        mc(
            id="e4-1-4-05-cc-001",
            concept_id="e4-1-4-05",
            category="concept",
            part="geo",
            difficulty=4,
            content="규칙적인 무늬를 만들 때 사용할 수 있는 이동 방법이 아닌 것은?",
            options=[
                "밀기",
                "뒤집기",
                "돌리기",
                "늘이기",
            ],
            correct="D",
            explanation="규칙적인 무늬는 밀기, 뒤집기, 돌리기로 만들 수 있습니다. 늘이기는 도형의 크기를 변화시키므로 합동 관계가 아닙니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 5단원: 막대그래프 (4개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # e4-1-5-01: 막대그래프
        mc(
            id="e4-1-5-01-cc-001",
            concept_id="e4-1-5-01",
            category="concept",
            part="data",
            difficulty=2,
            content="막대그래프의 구성 요소가 아닌 것은?",
            options=[
                "가로축과 세로축",
                "눈금",
                "꺾은선",
                "제목",
            ],
            correct="C",
            explanation="막대그래프의 구성 요소는 가로축, 세로축, 눈금, 막대, 제목입니다. 꺾은선은 꺾은선그래프의 요소입니다.",
            points=10,
        ),

        # e4-1-5-02: 막대그래프에서 알 수 있는 내용
        mc(
            id="e4-1-5-02-cc-001",
            concept_id="e4-1-5-02",
            category="concept",
            part="data",
            difficulty=7,
            content="막대그래프에서 눈금 한 칸이 10명이고, 어떤 항목의 막대가 눈금 3칸과 4칸 사이 중간쯤에 있습니다. 이 항목의 인원수로 적절한 것은?",
            options=[
                "30명",
                "35명",
                "40명",
                "34명",
            ],
            correct="B",
            explanation="눈금 3칸=30명, 4칸=40명이므로 중간값은 약 35명입니다. 눈금선 중간에 있는 값을 어림하여 읽는 능력이 필요합니다.",
            points=10,
        ),

        # e4-1-5-03: 막대그래프로 나타내기
        mc(
            id="e4-1-5-03-cc-001",
            concept_id="e4-1-5-03",
            category="concept",
            part="data",
            difficulty=5,
            content="자료의 값이 10, 25, 35, 50일 때, 막대그래프의 눈금 한 칸의 크기로 가장 적절한 것은?",
            options=[
                "1",
                "5",
                "20",
                "50",
            ],
            correct="B",
            explanation="눈금 한 칸의 크기는 자료의 크기에 맞게 정합니다. 최댓값 50에 대해 5씩이면 10칸으로 적당합니다. 1이면 50칸(너무 많음), 20이면 중간값 표현이 어렵고, 50이면 1칸밖에 안 됩니다.",
            points=10,
        ),

        # e4-1-5-04: 자료를 조사하여 막대그래프로 나타내기
        mc(
            id="e4-1-5-04-cc-001",
            concept_id="e4-1-5-04",
            category="concept",
            part="data",
            difficulty=6,
            content="자료를 조사하여 막대그래프로 나타낼 때 순서로 올바른 것은?",
            options=[
                "자료 조사 → 표 만들기 → 눈금 정하기 → 막대 그리기",
                "눈금 정하기 → 자료 조사 → 표 만들기 → 막대 그리기",
                "막대 그리기 → 자료 조사 → 표 만들기 → 눈금 정하기",
                "표 만들기 → 자료 조사 → 눈금 정하기 → 막대 그리기",
            ],
            correct="A",
            explanation="먼저 자료를 조사하고, 표로 정리한 다음, 적절한 눈금을 정하여 막대그래프를 그립니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 6단원: 규칙 찾기 (5개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # e4-1-6-01: 수의 배열에서 규칙 찾기
        mc(
            id="e4-1-6-01-cc-001",
            concept_id="e4-1-6-01",
            category="concept",
            part="algebra",
            difficulty=1,
            content="2, 4, 6, 8 다음에 올 수는?",
            options=[
                "9",
                "10",
                "12",
                "16",
            ],
            correct="B",
            explanation="2씩 커지는 규칙입니다. 8 + 2 = 10입니다.",
            points=10,
        ),
        mc(
            id="e4-1-6-01-cc-002",
            concept_id="e4-1-6-01",
            category="concept",
            part="algebra",
            difficulty=5,
            content="1, 2, 4, 8, 16, ... 이 수 배열의 규칙은?",
            options=[
                "2씩 더한다",
                "앞의 수에 2를 곱한다",
                "짝수만 나열한다",
                "4씩 더한다",
            ],
            correct="B",
            explanation="1×2=2, 2×2=4, 4×2=8, 8×2=16으로 앞의 수에 2를 곱하는 규칙입니다. 차이만 보면 1,2,4,8로 일정하지 않으므로 덧셈 규칙이 아닙니다.",
            points=10,
        ),

        # e4-1-6-02: 도형의 배열에서 규칙 찾기
        mc(
            id="e4-1-6-02-cc-001",
            concept_id="e4-1-6-02",
            category="concept",
            part="algebra",
            difficulty=8,
            content="바둑돌을 1개, 3개, 6개, 10개, ... 로 삼각형 모양을 만들고 있습니다. 5번째에 필요한 바둑돌은 몇 개인가요?",
            options=[
                "13개",
                "14개",
                "15개",
                "16개",
            ],
            correct="C",
            explanation="각 단계에서 이전보다 2, 3, 4, ... 개씩 늘어납니다. 1→3(+2)→6(+3)→10(+4)→15(+5)입니다. 5번째는 15개입니다.",
            points=10,
        ),

        # e4-1-6-03: 덧셈식과 뺄셈식의 배열에서 규칙 찾기
        mc(
            id="e4-1-6-03-cc-001",
            concept_id="e4-1-6-03",
            category="concept",
            part="algebra",
            difficulty=4,
            content="10+5=15, 20+5=25, 30+5=35, ... 에서 □+5=85일 때 □는 몇인가요?",
            options=[
                "70",
                "75",
                "80",
                "90",
            ],
            correct="C",
            explanation="첫 번째 수가 10씩 커지는 규칙입니다. 85-5=80입니다.",
            points=10,
        ),

        # e4-1-6-04: 곱셈식과 나눗셈식의 배열에서 규칙 찾기
        mc(
            id="e4-1-6-04-cc-001",
            concept_id="e4-1-6-04",
            category="concept",
            part="algebra",
            difficulty=5,
            content="3×4=12, 6×4=24, 9×4=36, ... 에서 다음 식은?",
            options=[
                "10×4=40",
                "11×4=44",
                "12×4=48",
                "15×4=60",
            ],
            correct="C",
            explanation="첫 번째 수가 3씩 커지고 두 번째 수는 4로 같으므로, 다음은 12×4=48입니다.",
            points=10,
        ),

        # e4-1-6-05: 규칙을 찾아 식으로 나타내기
        mc(
            id="e4-1-6-05-cc-001",
            concept_id="e4-1-6-05",
            category="concept",
            part="algebra",
            difficulty=6,
            content="한 변에 성냥개비 5개가 필요한 정오각형을 만들 때, 정오각형 개수와 성냥개비 수의 관계를 식으로 나타내면?",
            options=[
                "□+5",
                "□-5",
                "□×5",
                "□÷5",
            ],
            correct="C",
            explanation="정오각형 1개는 5개, 2개는 10개, ... 이므로 정오각형 개수(□)에 5를 곱합니다. □×5입니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 2단원: 삼각형 (5개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # e4-2-2-01: 삼각형을 변의 길이에 따라 분류하기
        mc(
            id="e4-2-2-01-cc-001",
            concept_id="e4-2-2-01",
            category="concept",
            part="geo",
            difficulty=3,
            content="이등변삼각형의 특징으로 옳은 것은?",
            options=[
                "세 변의 길이가 모두 같다",
                "두 변의 길이가 같고 두 밑각의 크기가 같다",
                "세 각의 크기가 모두 다르다",
                "한 각이 반드시 직각이다",
            ],
            correct="B",
            explanation="이등변삼각형은 두 변의 길이가 같고, 같은 변 사이의 두 밑각의 크기도 같습니다.",
            points=10,
        ),
        mc(
            id="e4-2-2-01-cc-002",
            concept_id="e4-2-2-01",
            category="concept",
            part="geo",
            difficulty=2,
            content="세 변의 길이가 모두 다른 삼각형을 무엇이라고 하나요?",
            options=[
                "이등변삼각형",
                "정삼각형",
                "부등변삼각형",
                "직각삼각형",
            ],
            correct="C",
            explanation="세 변의 길이가 모두 다른 삼각형은 부등변삼각형입니다.",
            points=10,
        ),

        # e4-2-2-02: 이등변삼각형의 성질
        mc(
            id="e4-2-2-02-cc-001",
            concept_id="e4-2-2-02",
            category="concept",
            part="geo",
            difficulty=5,
            content="이등변삼각형에서 같은 두 변을 '변'이라 하고, 그 사이의 각을 '꼭지각', 나머지 두 각을 '밑각'이라 합니다. 밑각의 특징은?",
            options=[
                "밑각의 크기는 항상 다르다",
                "밑각의 크기는 항상 같다",
                "밑각의 크기는 꼭지각보다 크다",
                "밑각의 크기는 항상 90도이다",
            ],
            correct="B",
            explanation="이등변삼각형의 두 밑각의 크기는 항상 같습니다.",
            points=10,
        ),

        # e4-2-2-03: 정삼각형의 성질
        mc(
            id="e4-2-2-03-cc-001",
            concept_id="e4-2-2-03",
            category="concept",
            part="geo",
            difficulty=8,
            content="정삼각형은 이등변삼각형인가요?",
            options=[
                "아니오, 정삼각형은 세 변이 같고 이등변삼각형은 두 변만 같다",
                "예, 정삼각형도 두 변의 길이가 같은 조건을 만족한다",
                "같은 도형이다",
                "비교할 수 없다",
            ],
            correct="B",
            explanation="정삼각형은 세 변의 길이가 모두 같으므로 '두 변의 길이가 같다'는 이등변삼각형의 조건을 당연히 만족합니다. 따라서 정삼각형 ⊂ 이등변삼각형입니다.",
            points=10,
        ),
        mc(
            id="e4-2-2-03-cc-002",
            concept_id="e4-2-2-03",
            category="concept",
            part="geo",
            difficulty=4,
            content="정삼각형의 한 각의 크기는 몇 도인가요?",
            options=[
                "45도",
                "60도",
                "90도",
                "120도",
            ],
            correct="B",
            explanation="정삼각형의 세 각의 크기는 모두 같고, 삼각형의 내각의 합은 180도이므로 180÷3=60도입니다.",
            points=10,
        ),

        # e4-2-2-04: 삼각형을 각의 크기에 따라 분류하기
        mc(
            id="e4-2-2-04-cc-001",
            concept_id="e4-2-2-04",
            category="concept",
            part="geo",
            difficulty=6,
            content="삼각형의 세 각이 30°, 40°, 110°일 때, 이 삼각형에 대한 설명으로 옳은 것은?",
            options=[
                "예각삼각형이다 (예각이 2개 있으므로)",
                "직각삼각형이다",
                "둔각삼각형이다",
                "알 수 없다",
            ],
            correct="C",
            explanation="110°는 둔각이므로 이 삼각형은 둔각삼각형입니다. 예각이 여러 개 있어도 둔각이 하나라도 있으면 둔각삼각형입니다. '예각이 있으면 예각삼각형'이라는 것은 오해입니다.",
            points=10,
        ),

        # e4-2-2-05: 삼각형을 두 가지 기준으로 분류하기
        mc(
            id="e4-2-2-05-cc-001",
            concept_id="e4-2-2-05",
            category="concept",
            part="geo",
            difficulty=7,
            content="두 변의 길이가 같고 한 각이 직각인 삼각형을 무엇이라고 하나요?",
            options=[
                "정삼각형",
                "예각 이등변삼각형",
                "직각 이등변삼각형",
                "둔각 이등변삼각형",
            ],
            correct="C",
            explanation="변의 길이(이등변)와 각의 크기(직각) 두 기준을 모두 적용하여 직각 이등변삼각형이라고 합니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 4단원: 사각형 (7개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # e4-2-4-01: 수직과 수선
        mc(
            id="e4-2-4-01-cc-001",
            concept_id="e4-2-4-01",
            category="concept",
            part="geo",
            difficulty=2,
            content="두 직선이 만나서 이루는 각이 90도일 때, 이 두 직선은 어떤 관계인가요?",
            options=[
                "평행",
                "수직",
                "일치",
                "교차",
            ],
            correct="B",
            explanation="두 직선이 만나서 이루는 각이 90도일 때 수직이라고 합니다.",
            points=10,
        ),
        mc(
            id="e4-2-4-01-cc-002",
            concept_id="e4-2-4-01",
            category="concept",
            part="geo",
            difficulty=3,
            content="한 직선에 수직인 선을 무엇이라고 하나요?",
            options=[
                "평행선",
                "수선",
                "대각선",
                "빗변",
            ],
            correct="B",
            explanation="한 직선에 수직으로 만나는 선을 수선이라고 합니다.",
            points=10,
        ),

        # e4-2-4-02: 평행과 평행선
        mc(
            id="e4-2-4-02-cc-001",
            concept_id="e4-2-4-02",
            category="concept",
            part="geo",
            difficulty=3,
            content="평행선의 정의로 옳은 것은?",
            options=[
                "만나는 두 직선",
                "수직으로 만나는 두 직선",
                "한없이 늘여도 만나지 않는 두 직선",
                "한 점에서 만나는 두 직선",
            ],
            correct="C",
            explanation="평행선은 한없이 늘여도 만나지 않는 두 직선입니다.",
            points=10,
        ),

        # e4-2-4-03: 평행선 사이의 거리
        mc(
            id="e4-2-4-03-cc-001",
            concept_id="e4-2-4-03",
            category="concept",
            part="geo",
            difficulty=4,
            content="두 평행선 사이의 거리는 어디서나 어떻게 되나요?",
            options=[
                "점점 멀어진다",
                "점점 가까워진다",
                "어디서나 같다",
                "알 수 없다",
            ],
            correct="C",
            explanation="두 평행선 사이의 수선의 길이는 어디서나 같습니다. 이것을 평행선 사이의 거리라고 합니다.",
            points=10,
        ),

        # e4-2-4-04: 사다리꼴
        mc(
            id="e4-2-4-04-cc-001",
            concept_id="e4-2-4-04",
            category="concept",
            part="geo",
            difficulty=3,
            content="사다리꼴의 정의로 옳은 것은?",
            options=[
                "네 변의 길이가 모두 같은 사각형",
                "마주 보는 한 쌍의 변이 평행한 사각형",
                "네 각이 모두 직각인 사각형",
                "마주 보는 두 쌍의 변이 평행한 사각형",
            ],
            correct="B",
            explanation="사다리꼴은 마주 보는 한 쌍의 변이 평행한 사각형입니다.",
            points=10,
        ),

        # e4-2-4-05: 평행사변형
        mc(
            id="e4-2-4-05-cc-001",
            concept_id="e4-2-4-05",
            category="concept",
            part="geo",
            difficulty=4,
            content="평행사변형의 성질로 옳지 않은 것은?",
            options=[
                "마주 보는 두 쌍의 변이 평행하다",
                "마주 보는 변의 길이가 같다",
                "마주 보는 각의 크기가 같다",
                "네 각이 모두 직각이다",
            ],
            correct="D",
            explanation="평행사변형의 네 각은 모두 직각이 아닐 수 있습니다. 네 각이 모두 직각인 평행사변형은 직사각형입니다.",
            points=10,
        ),

        # e4-2-4-06: 마름모
        mc(
            id="e4-2-4-06-cc-001",
            concept_id="e4-2-4-06",
            category="concept",
            part="geo",
            difficulty=4,
            content="마름모의 특징으로 옳은 것은?",
            options=[
                "네 각이 모두 같다",
                "네 변의 길이가 모두 같다",
                "대각선의 길이가 같다",
                "마주 보는 변이 평행하지 않다",
            ],
            correct="B",
            explanation="마름모는 네 변의 길이가 모두 같은 사각형입니다. 네 각이 모두 같으면 정사각형입니다.",
            points=10,
        ),

        # e4-2-4-07: 여러 가지 사각형
        mc(
            id="e4-2-4-07-cc-001",
            concept_id="e4-2-4-07",
            category="concept",
            part="geo",
            difficulty=6,
            content="정사각형은 직사각형이라고 할 수 있나요?",
            options=[
                "아니오, 정사각형과 직사각형은 다른 도형이다",
                "예, 정사각형은 네 각이 모두 직각이므로 직사각형이다",
                "직사각형이 정사각형이다",
                "때에 따라 다르다",
            ],
            correct="B",
            explanation="직사각형은 '네 각이 모두 직각인 사각형'입니다. 정사각형도 네 각이 모두 직각이므로 직사각형에 포함됩니다. 정사각형 ⊂ 직사각형 ⊂ 평행사변형입니다.",
            points=10,
        ),
        mc(
            id="e4-2-4-07-cc-002",
            concept_id="e4-2-4-07",
            category="concept",
            part="geo",
            difficulty=9,
            content="다음 중 평행사변형에 해당하는 것을 모두 고르면?",
            options=[
                "평행사변형, 마름모만",
                "평행사변형, 직사각형만",
                "평행사변형, 마름모, 직사각형, 정사각형 모두",
                "평행사변형만",
            ],
            correct="C",
            explanation="평행사변형은 '마주 보는 두 쌍의 변이 평행한 사각형'입니다. 마름모, 직사각형, 정사각형 모두 이 조건을 만족하므로 평행사변형에 포함됩니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 5단원: 꺾은선그래프 (5개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # e4-2-5-01: 꺾은선그래프
        mc(
            id="e4-2-5-01-cc-001",
            concept_id="e4-2-5-01",
            category="concept",
            part="data",
            difficulty=3,
            content="꺾은선그래프로 나타내기에 가장 적합한 자료는?",
            options=[
                "반별 학생 수",
                "좋아하는 과일 종류별 학생 수",
                "1월부터 12월까지 월별 평균 기온",
                "학급별 남녀 학생 수",
            ],
            correct="C",
            explanation="꺾은선그래프는 시간에 따른 연속적 변화를 나타내기에 적합합니다. 월별 기온 변화가 이에 해당합니다. 항목별 비교는 막대그래프가 적합합니다.",
            points=10,
        ),

        # e4-2-5-02: 꺾은선그래프에서 알 수 있는 내용
        mc(
            id="e4-2-5-02-cc-001",
            concept_id="e4-2-5-02",
            category="concept",
            part="data",
            difficulty=5,
            content="꺾은선그래프에서 선분의 기울기가 급할수록 무엇을 의미하나요?",
            options=[
                "값이 크다",
                "변화가 크다",
                "변화가 작다",
                "값이 작다",
            ],
            correct="B",
            explanation="꺾은선그래프에서 선분의 기울기가 급할수록 같은 시간 동안 변화가 크다는 것을 의미합니다.",
            points=10,
        ),

        # e4-2-5-03: 꺾은선그래프로 나타내기
        mc(
            id="e4-2-5-03-cc-001",
            concept_id="e4-2-5-03",
            category="concept",
            part="data",
            difficulty=7,
            content="꺾은선그래프에서 물결선(〰)의 역할은?",
            options=[
                "그래프가 예쁘게 보이도록 꾸민다",
                "필요 없는 눈금 구간을 생략한다",
                "값이 0인 구간을 표시한다",
                "그래프의 끝을 나타낸다",
            ],
            correct="B",
            explanation="물결선은 자료 값 사이에 비어 있는 불필요한 눈금 구간을 생략하기 위해 사용합니다. 예를 들어 값이 모두 80~100 사이이면 0~80 구간을 물결선으로 생략합니다.",
            points=10,
        ),

        # e4-2-5-04: 자료를 조사하여 꺾은선그래프로 나타내기
        mc(
            id="e4-2-5-04-cc-001",
            concept_id="e4-2-5-04",
            category="concept",
            part="data",
            difficulty=6,
            content="꺾은선그래프를 그릴 때 점을 찍은 후 해야 할 일은?",
            options=[
                "점을 크게 다시 그린다",
                "점들을 선분으로 잇는다",
                "점을 지운다",
                "물결선을 그린다",
            ],
            correct="B",
            explanation="꺾은선그래프는 점을 찍은 후 점들을 선분으로 이어서 완성합니다.",
            points=10,
        ),

        # e4-2-5-05: 꺾은선그래프의 활용
        mc(
            id="e4-2-5-05-cc-001",
            concept_id="e4-2-5-05",
            category="concept",
            part="data",
            difficulty=7,
            content="두 꺾은선그래프를 비교할 때 알 수 있는 것이 아닌 것은?",
            options=[
                "두 자료의 변화 추이 비교",
                "특정 시점의 값 비교",
                "두 자료의 평균값",
                "미래 값 예측",
            ],
            correct="C",
            explanation="꺾은선그래프에서는 변화 추이, 특정 시점 값, 미래 예측 등을 할 수 있지만, 평균값은 그래프만으로 정확히 알기 어렵습니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 6단원: 다각형 (5개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # e4-2-6-01: 다각형
        mc(
            id="e4-2-6-01-cc-001",
            concept_id="e4-2-6-01",
            category="concept",
            part="geo",
            difficulty=2,
            content="다각형이란 무엇인가요?",
            options=[
                "곡선으로 둘러싸인 도형",
                "선분으로만 둘러싸인 닫힌 도형",
                "원처럼 둥근 도형",
                "각이 있는 모든 도형",
            ],
            correct="B",
            explanation="다각형은 선분으로만 둘러싸인 닫힌 도형입니다. 곡선이 포함되면 다각형이 아닙니다.",
            points=10,
        ),
        mc(
            id="e4-2-6-01-cc-002",
            concept_id="e4-2-6-01",
            category="concept",
            part="geo",
            difficulty=3,
            content="육각형은 변이 몇 개인가요?",
            options=[
                "4개",
                "5개",
                "6개",
                "8개",
            ],
            correct="C",
            explanation="육각형은 변이 6개인 다각형입니다.",
            points=10,
        ),

        # e4-2-6-02: 정다각형
        mc(
            id="e4-2-6-02-cc-001",
            concept_id="e4-2-6-02",
            category="concept",
            part="geo",
            difficulty=6,
            content="마름모는 정다각형인가요?",
            options=[
                "예, 네 변의 길이가 모두 같으므로 정다각형이다",
                "아니오, 네 변의 길이가 같지만 네 각의 크기가 모두 같지 않을 수 있다",
                "예, 마름모는 항상 정사각형이다",
                "정다각형은 삼각형만 해당된다",
            ],
            correct="B",
            explanation="정다각형이 되려면 '변의 길이가 모두 같고' '각의 크기도 모두 같아야' 합니다(두 조건 모두 필요). 마름모는 변의 길이는 같지만 각의 크기가 같지 않을 수 있으므로 정다각형이 아닙니다.",
            points=10,
        ),
        mc(
            id="e4-2-6-02-cc-002",
            concept_id="e4-2-6-02",
            category="concept",
            part="geo",
            difficulty=9,
            content="다음 중 정다각형에 대한 설명으로 옳은 것은?",
            options=[
                "변의 길이만 모두 같으면 정다각형이다",
                "각의 크기만 모두 같으면 정다각형이다",
                "변의 길이가 모두 같고 각의 크기도 모두 같아야 정다각형이다",
                "정삼각형만 정다각형이다",
            ],
            correct="C",
            explanation="정다각형은 변의 길이가 모두 같고 각의 크기도 모두 같아야 합니다. 반례: 마름모(변만 같음, 정다각형 아님), 직사각형(각만 같음, 정다각형 아님).",
            points=10,
        ),

        # e4-2-6-03: 대각선
        mc(
            id="e4-2-6-03-cc-001",
            concept_id="e4-2-6-03",
            category="concept",
            part="geo",
            difficulty=4,
            content="대각선의 정의로 옳은 것은?",
            options=[
                "다각형의 한 변",
                "다각형에서 이웃하지 않는 두 꼭짓점을 잇는 선분",
                "다각형의 모든 변의 합",
                "다각형의 높이",
            ],
            correct="B",
            explanation="대각선은 다각형에서 이웃하지 않는 두 꼭짓점을 잇는 선분입니다.",
            points=10,
        ),
        mc(
            id="e4-2-6-03-cc-002",
            concept_id="e4-2-6-03",
            category="concept",
            part="geo",
            difficulty=6,
            content="오각형의 대각선은 모두 몇 개인가요?",
            options=[
                "3개",
                "4개",
                "5개",
                "6개",
            ],
            correct="C",
            explanation="오각형의 한 꼭짓점에서 그을 수 있는 대각선은 2개이고, 5개 꼭짓점에서 10개를 그을 수 있지만 각 대각선이 2번씩 세어지므로 10÷2=5개입니다.",
            points=10,
        ),

        # e4-2-6-04: 모양 만들기
        mc(
            id="e4-2-6-04-cc-001",
            concept_id="e4-2-6-04",
            category="concept",
            part="geo",
            difficulty=5,
            content="정삼각형 2개를 붙여서 만들 수 있는 도형은?",
            options=[
                "정사각형",
                "마름모",
                "정오각형",
                "정육각형",
            ],
            correct="B",
            explanation="정삼각형 2개를 밑변을 맞대어 붙이면 마름모(또는 정사각형이 아닌 평행사변형)를 만들 수 있습니다.",
            points=10,
        ),

        # e4-2-6-05: 모양 채우기
        mc(
            id="e4-2-6-05-cc-001",
            concept_id="e4-2-6-05",
            category="concept",
            part="geo",
            difficulty=7,
            content="평면을 빈틈없이 채울 수 있는 정다각형이 아닌 것은?",
            options=[
                "정삼각형",
                "정사각형",
                "정오각형",
                "정육각형",
            ],
            correct="C",
            explanation="정삼각형, 정사각형, 정육각형은 평면을 빈틈없이 채울 수 있지만, 정오각형은 각의 크기(108도) 때문에 빈틈없이 채울 수 없습니다.",
            points=10,
        ),
    ]
