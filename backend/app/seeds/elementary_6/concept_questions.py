"""초등 6학년 개념 문제 - PDF 기반 세분화 개념."""

from .._base import concept, mc
from app.data.pdf_concept_map import E6_S1_CONCEPTS, E6_S2_CONCEPTS


def get_concepts() -> list[dict]:
    """PDF 기반 개념 39개 반환 (S1: 23개, S2: 28개 중 대상 단원만)."""
    result = []

    # S1: 2, 5, 6단원 (6+7+4 = 17개)
    for c in E6_S1_CONCEPTS:
        if c["chapter_number"] in {2, 5, 6}:
            result.append(c)

    # S2: 3, 4, 5, 6단원 (6+6+6+4 = 22개)
    for c in E6_S2_CONCEPTS:
        if c["chapter_number"] in {3, 4, 5, 6}:
            result.append(c)

    return result


def get_questions() -> list[dict]:
    """개념 문제 78개 반환 (개념당 2개)."""
    return [
        # ====================================
        # 1학기 2단원: 각기둥과 각뿔 (12개)
        # ====================================

        # e6-1-2-01: 각기둥 알아보기 (1)
        mc(
            id="e6-1-2-01-cc-001",
            concept_id="e6-1-2-01",
            category="concept",
            part="geo",
            difficulty=4,
            content="삼각기둥의 밑면은 어떤 도형입니까?",
            options=[
                "직사각형",
                "삼각형",
                "사각형",
                "오각형",
            ],
            correct="B",
            explanation="삼각기둥은 밑면이 삼각형인 각기둥입니다. '삼각'은 밑면의 모양을 나타냅니다.",
        ),
        mc(
            id="e6-1-2-01-cc-002",
            concept_id="e6-1-2-01",
            category="concept",
            part="geo",
            difficulty=5,
            content="다음 중 각기둥을 옆으로 눕혔을 때, 밑면을 찾는 방법으로 옳은 것은?",
            options=[
                "가장 아래에 있는 면",
                "합동인 두 면",
                "가장 넓은 면",
                "직사각형 모양의 면",
            ],
            correct="B",
            explanation="각기둥의 밑면은 '합동인 두 면'입니다. 눕혀도 밑면은 바뀌지 않습니다. '밑면 = 바닥면' 오개념에 주의하세요.",
        ),

        # e6-1-2-02: 각기둥 알아보기 (2)
        mc(
            id="e6-1-2-02-cc-001",
            concept_id="e6-1-2-02",
            category="concept",
            part="geo",
            difficulty=6,
            content="오각기둥의 모서리는 모두 몇 개입니까?",
            options=[
                "10개",
                "15개",
                "20개",
                "25개",
            ],
            correct="B",
            explanation="각기둥의 모서리 = 밑면의 변 × 3입니다. 오각기둥은 5 × 3 = 15개입니다.",
        ),
        mc(
            id="e6-1-2-02-cc-002",
            concept_id="e6-1-2-02",
            category="concept",
            part="geo",
            difficulty=7,
            content="육각기둥의 꼭짓점은 모두 몇 개입니까?",
            options=[
                "6개",
                "12개",
                "18개",
                "24개",
            ],
            correct="B",
            explanation="각기둥의 꼭짓점 = 밑면의 꼭짓점 × 2입니다. 육각기둥은 6 × 2 = 12개입니다.",
        ),

        # e6-1-2-03: 각기둥의 전개도
        mc(
            id="e6-1-2-03-cc-001",
            concept_id="e6-1-2-03",
            category="concept",
            part="geo",
            difficulty=6,
            content="삼각기둥의 전개도에서 옆면은 모두 몇 개입니까?",
            options=[
                "2개",
                "3개",
                "4개",
                "5개",
            ],
            correct="B",
            explanation="삼각기둥의 옆면은 3개입니다. 각기둥의 옆면 개수 = 밑면의 변의 수입니다.",
        ),
        mc(
            id="e6-1-2-03-cc-002",
            concept_id="e6-1-2-03",
            category="concept",
            part="geo",
            difficulty=7,
            content="사각기둥의 전개도에서 옆면의 모양은 무엇입니까?",
            options=[
                "삼각형",
                "사각형",
                "오각형",
                "직사각형",
            ],
            correct="D",
            explanation="각기둥의 전개도에서 옆면은 모두 직사각형입니다.",
        ),

        # e6-1-2-04: 각기둥의 전개도 그리기
        mc(
            id="e6-1-2-04-cc-001",
            concept_id="e6-1-2-04",
            category="concept",
            part="geo",
            difficulty=8,
            content="오각기둥의 전개도를 그릴 때, 옆면의 가로는 무엇과 같습니까?",
            options=[
                "밑면의 둘레",
                "밑면의 변의 길이",
                "각기둥의 높이",
                "밑면의 대각선",
            ],
            correct="B",
            explanation="각기둥 전개도에서 각 옆면의 가로는 밑면의 각 변의 길이와 같습니다.",
        ),
        mc(
            id="e6-1-2-04-cc-002",
            concept_id="e6-1-2-04",
            category="concept",
            part="geo",
            difficulty=7,
            content="각기둥의 전개도를 그릴 때, 옆면의 세로는 무엇과 같습니까?",
            options=[
                "밑면의 변의 길이",
                "밑면의 둘레",
                "각기둥의 높이",
                "밑면의 넓이",
            ],
            correct="C",
            explanation="각기둥 전개도에서 옆면의 세로는 각기둥의 높이와 같습니다.",
        ),

        # e6-1-2-05: 각뿔 알아보기 (1)
        mc(
            id="e6-1-2-05-cc-001",
            concept_id="e6-1-2-05",
            category="concept",
            part="geo",
            difficulty=6,
            content="사각뿔에서 꼭짓점에서 밑면까지의 거리를 무엇이라 합니까?",
            options=[
                "모서리",
                "모선",
                "높이",
                "옆면",
            ],
            correct="C",
            explanation="각뿔의 높이는 꼭짓점에서 밑면에 내린 수선의 길이입니다. 옆 모서리와 혼동하지 마세요.",
        ),
        mc(
            id="e6-1-2-05-cc-002",
            concept_id="e6-1-2-05",
            category="concept",
            part="geo",
            difficulty=5,
            content="육각뿔의 밑면은 어떤 도형입니까?",
            options=[
                "삼각형",
                "사각형",
                "오각형",
                "육각형",
            ],
            correct="D",
            explanation="육각뿔은 밑면이 육각형인 각뿔입니다. 각뿔의 이름은 밑면의 모양에서 유래합니다.",
        ),

        # e6-1-2-06: 각뿔 알아보기 (2)
        mc(
            id="e6-1-2-06-cc-001",
            concept_id="e6-1-2-06",
            category="concept",
            part="geo",
            difficulty=7,
            content="오각뿔의 옆면은 모두 몇 개입니까?",
            options=[
                "4개",
                "5개",
                "6개",
                "7개",
            ],
            correct="B",
            explanation="각뿔의 옆면 개수 = 밑면의 변의 수입니다. 오각뿔은 5개의 삼각형 옆면을 가집니다.",
        ),
        mc(
            id="e6-1-2-06-cc-002",
            concept_id="e6-1-2-06",
            category="concept",
            part="geo",
            difficulty=8,
            content="삼각기둥과 삼각뿔의 공통점이 아닌 것은?",
            options=[
                "밑면이 삼각형이다",
                "옆면이 직사각형이다",
                "모서리가 있다",
                "꼭짓점이 있다",
            ],
            correct="B",
            explanation="각뿔의 옆면은 모두 삼각형입니다. 각기둥의 옆면은 직사각형입니다.",
        ),

        # ====================================
        # 1학기 5단원: 여러 가지 그래프 (14개)
        # ====================================

        # e6-1-5-01: 그림그래프로 나타내기
        mc(
            id="e6-1-5-01-cc-001",
            concept_id="e6-1-5-01",
            category="concept",
            part="data",
            difficulty=4,
            content="그림그래프에서 그림 1개가 10명을 나타낼 때, 45명은 그림 몇 개로 나타냅니까?",
            options=[
                "4개",
                "4.5개",
                "5개",
                "45개",
            ],
            correct="B",
            explanation="45 ÷ 10 = 4.5이므로 4.5개의 그림으로 나타냅니다. 반 개의 그림도 사용합니다.",
        ),
        mc(
            id="e6-1-5-01-cc-002",
            concept_id="e6-1-5-01",
            category="concept",
            part="data",
            difficulty=5,
            content="그림그래프의 장점은 무엇입니까?",
            options=[
                "정확한 수량을 알 수 있다",
                "한눈에 비교하기 쉽다",
                "비율을 알 수 있다",
                "변화를 알 수 있다",
            ],
            correct="B",
            explanation="그림그래프는 그림의 개수로 한눈에 많고 적음을 비교하기 쉽습니다.",
        ),

        # e6-1-5-02: 띠그래프
        mc(
            id="e6-1-5-02-cc-001",
            concept_id="e6-1-5-02",
            category="concept",
            part="data",
            difficulty=6,
            content="띠그래프에서 전체는 무엇으로 나타냅니까?",
            options=[
                "100",
                "100%",
                "띠의 길이",
                "띠의 넓이",
            ],
            correct="B",
            explanation="띠그래프에서 전체는 100%로 나타내고, 각 항목은 비율(%)로 표시합니다.",
        ),
        mc(
            id="e6-1-5-02-cc-002",
            concept_id="e6-1-5-02",
            category="concept",
            part="data",
            difficulty=5,
            content="띠그래프에서 30%를 차지하는 부분은 띠의 몇 %입니까?",
            options=[
                "3%",
                "30%",
                "70%",
                "100%",
            ],
            correct="B",
            explanation="띠그래프에서 각 항목의 비율이 그대로 띠의 비율이 됩니다. 30%는 띠의 30%입니다.",
        ),

        # e6-1-5-03: 띠그래프로 나타내기
        mc(
            id="e6-1-5-03-cc-001",
            concept_id="e6-1-5-03",
            category="concept",
            part="data",
            difficulty=7,
            content="띠그래프로 나타내기 위해 먼저 해야 할 일은?",
            options=[
                "그래프를 그린다",
                "백분율을 구한다",
                "막대그래프를 만든다",
                "평균을 구한다",
            ],
            correct="B",
            explanation="띠그래프로 나타내려면 먼저 각 항목의 백분율을 구해야 합니다.",
        ),
        mc(
            id="e6-1-5-03-cc-002",
            concept_id="e6-1-5-03",
            category="concept",
            part="data",
            difficulty=8,
            content="전체 200명 중 A가 50명일 때 띠그래프에서 A의 비율은?",
            options=[
                "50%",
                "25%",
                "20%",
                "10%",
            ],
            correct="B",
            explanation="50 ÷ 200 = 0.25 = 25%입니다.",
        ),

        # e6-1-5-04: 원그래프
        mc(
            id="e6-1-5-04-cc-001",
            concept_id="e6-1-5-04",
            category="concept",
            part="data",
            difficulty=6,
            content="원그래프에서 30%를 나타내는 부분의 중심각은 몇 도입니까?",
            options=[
                "30°",
                "60°",
                "90°",
                "108°",
            ],
            correct="D",
            explanation="중심각 = 360° × 비율입니다. 360° × 0.3 = 108°입니다. 30%를 30°로 착각하는 오개념에 주의하세요.",
        ),
        mc(
            id="e6-1-5-04-cc-002",
            concept_id="e6-1-5-04",
            category="concept",
            part="data",
            difficulty=5,
            content="원그래프에서 25%를 나타내는 부분의 중심각은 몇 도입니까?",
            options=[
                "25°",
                "90°",
                "100°",
                "125°",
            ],
            correct="B",
            explanation="360° × 0.25 = 90°입니다.",
        ),

        # e6-1-5-05: 원그래프로 나타내기
        mc(
            id="e6-1-5-05-cc-001",
            concept_id="e6-1-5-05",
            category="concept",
            part="data",
            difficulty=8,
            content="원그래프로 나타낼 때, 각 항목의 중심각을 구하는 방법은?",
            options=[
                "360° × 비율",
                "100 × 비율",
                "180° × 비율",
                "비율 ÷ 360°",
            ],
            correct="A",
            explanation="중심각 = 360° × 해당 항목의 비율입니다.",
        ),
        mc(
            id="e6-1-5-05-cc-002",
            concept_id="e6-1-5-05",
            category="concept",
            part="data",
            difficulty=7,
            content="원그래프의 모든 중심각의 합은?",
            options=[
                "100°",
                "180°",
                "360°",
                "항목 개수에 따라 다르다",
            ],
            correct="C",
            explanation="원그래프의 모든 중심각의 합은 360°(한 바퀴)입니다.",
        ),

        # e6-1-5-06: 그래프 해석하기
        mc(
            id="e6-1-5-06-cc-001",
            concept_id="e6-1-5-06",
            category="concept",
            part="data",
            difficulty=7,
            content="띠그래프와 원그래프의 공통점은 무엇입니까?",
            options=[
                "전체에 대한 각 부분의 비율을 나타낸다",
                "정확한 수량을 알 수 있다",
                "시간에 따른 변화를 알 수 있다",
                "두 변수의 관계를 알 수 있다",
            ],
            correct="A",
            explanation="띠그래프와 원그래프는 모두 전체에 대한 각 부분의 비율을 시각화하는 그래프입니다.",
        ),
        mc(
            id="e6-1-5-06-cc-002",
            concept_id="e6-1-5-06",
            category="concept",
            part="data",
            difficulty=6,
            content="띠그래프에서 가장 큰 비율을 차지하는 항목을 찾는 방법은?",
            options=[
                "가장 긴 부분을 찾는다",
                "가장 짧은 부분을 찾는다",
                "가장 어두운 부분을 찾는다",
                "가장 왼쪽 부분을 찾는다",
            ],
            correct="A",
            explanation="띠그래프에서 가장 긴 부분이 가장 큰 비율을 나타냅니다.",
        ),

        # e6-1-5-07: 여러 가지 그래프 비교
        mc(
            id="e6-1-5-07-cc-001",
            concept_id="e6-1-5-07",
            category="concept",
            part="data",
            difficulty=8,
            content="시간에 따른 온도 변화를 나타내기에 가장 적합한 그래프는?",
            options=[
                "막대그래프",
                "꺾은선그래프",
                "띠그래프",
                "원그래프",
            ],
            correct="B",
            explanation="시간에 따른 변화는 꺾은선그래프로 나타내는 것이 가장 적합합니다.",
        ),
        mc(
            id="e6-1-5-07-cc-002",
            concept_id="e6-1-5-07",
            category="concept",
            part="data",
            difficulty=9,
            content="학급 학생들의 혈액형 분포를 나타내기에 가장 적합한 그래프는?",
            options=[
                "꺾은선그래프",
                "막대그래프",
                "원그래프",
                "점그래프",
            ],
            correct="C",
            explanation="전체에 대한 각 부분의 비율을 나타낼 때는 원그래프나 띠그래프가 적합합니다.",
        ),

        # ====================================
        # 1학기 6단원: 직육면체의 부피와 겉넓이 (8개)
        # ====================================

        # e6-1-6-01: 직육면체의 부피 비교
        mc(
            id="e6-1-6-01-cc-001",
            concept_id="e6-1-6-01",
            category="concept",
            part="geo",
            difficulty=5,
            content="1cm³는 무엇입니까?",
            options=[
                "한 변이 1cm인 정사각형",
                "한 변이 1cm인 정육면체",
                "가로가 1cm인 직사각형",
                "높이가 1cm인 직육면체",
            ],
            correct="B",
            explanation="1cm³는 한 변이 1cm인 정육면체의 부피입니다. 이것이 부피의 단위입니다.",
        ),
        mc(
            id="e6-1-6-01-cc-002",
            concept_id="e6-1-6-01",
            category="concept",
            part="geo",
            difficulty=6,
            content="쌓기나무 20개로 만든 도형의 부피는 몇 cm³입니까? (쌓기나무 1개는 1cm³)",
            options=[
                "10 cm³",
                "20 cm³",
                "40 cm³",
                "80 cm³",
            ],
            correct="B",
            explanation="쌓기나무 1개가 1cm³이므로, 20개는 20cm³입니다.",
        ),

        # e6-1-6-02: 직육면체의 부피 구하는 방법
        mc(
            id="e6-1-6-02-cc-001",
            concept_id="e6-1-6-02",
            category="concept",
            part="geo",
            difficulty=6,
            content="직육면체의 부피를 구하는 공식은?",
            options=[
                "가로 + 세로 + 높이",
                "가로 × 세로",
                "가로 × 세로 × 높이",
                "2 × (가로 + 세로 + 높이)",
            ],
            correct="C",
            explanation="직육면체의 부피 = 밑면의 넓이 × 높이 = 가로 × 세로 × 높이입니다.",
        ),
        mc(
            id="e6-1-6-02-cc-002",
            concept_id="e6-1-6-02",
            category="concept",
            part="geo",
            difficulty=7,
            content="가로 5cm, 세로 4cm, 높이 3cm인 직육면체의 부피는?",
            options=[
                "12 cm³",
                "20 cm³",
                "60 cm³",
                "94 cm³",
            ],
            correct="C",
            explanation="5 × 4 × 3 = 60 cm³입니다.",
        ),

        # e6-1-6-03: m³ 알아보기
        mc(
            id="e6-1-6-03-cc-001",
            concept_id="e6-1-6-03",
            category="concept",
            part="geo",
            difficulty=8,
            content="1m³는 몇 cm³입니까?",
            options=[
                "100 cm³",
                "1,000 cm³",
                "10,000 cm³",
                "1,000,000 cm³",
            ],
            correct="D",
            explanation="1m = 100cm이므로, 1m³ = 100cm × 100cm × 100cm = 1,000,000cm³입니다. 단위 변환 시 세제곱에 주의하세요.",
        ),
        mc(
            id="e6-1-6-03-cc-002",
            concept_id="e6-1-6-03",
            category="concept",
            part="geo",
            difficulty=9,
            content="2,500,000 cm³는 몇 m³입니까?",
            options=[
                "2.5 m³",
                "25 m³",
                "250 m³",
                "2,500 m³",
            ],
            correct="A",
            explanation="2,500,000 ÷ 1,000,000 = 2.5 m³입니다.",
        ),

        # e6-1-6-04: 직육면체의 겉넓이 구하는 방법
        mc(
            id="e6-1-6-04-cc-001",
            concept_id="e6-1-6-04",
            category="concept",
            part="geo",
            difficulty=7,
            content="직육면체의 겉넓이는 무엇입니까?",
            options=[
                "한 면의 넓이",
                "밑면의 넓이",
                "모든 면의 넓이의 합",
                "옆면의 넓이의 합",
            ],
            correct="C",
            explanation="겉넓이는 입체도형의 모든 면의 넓이의 합입니다.",
        ),
        mc(
            id="e6-1-6-04-cc-002",
            concept_id="e6-1-6-04",
            category="concept",
            part="geo",
            difficulty=9,
            content="쌓기나무가 12개로 같은 두 입체도형이 있습니다. 이 두 도형의 겉넓이는?",
            options=[
                "항상 같다",
                "항상 다르다",
                "같을 수도, 다를 수도 있다",
                "부피가 같으면 겉넓이도 항상 같다",
            ],
            correct="C",
            explanation="부피가 같아도 쌓는 방식에 따라 겉넓이는 달라질 수 있습니다. '부피 같으면 겉넓이도 같다'는 오개념입니다.",
        ),

        # ====================================
        # 2학기 3단원: 공간과 입체 (12개)
        # ====================================

        # e6-2-3-01: 어느 방향에서 보았는지 알아보기
        mc(
            id="e6-2-3-01-cc-001",
            concept_id="e6-2-3-01",
            category="concept",
            part="geo",
            difficulty=6,
            content="쌓기나무로 만든 입체도형을 앞에서 봤을 때 고려해야 할 것은?",
            options=[
                "가로와 높이만 보인다",
                "깊이 정보도 포함된다",
                "옆면도 함께 보인다",
                "위에서 본 모양과 같다",
            ],
            correct="A",
            explanation="앞에서 본 모양은 가로와 높이만 나타나고 깊이는 나타나지 않습니다.",
        ),
        mc(
            id="e6-2-3-01-cc-002",
            concept_id="e6-2-3-01",
            category="concept",
            part="geo",
            difficulty=7,
            content="쌓기나무를 위에서 본 모양에서 알 수 있는 것은?",
            options=[
                "높이",
                "가로와 세로",
                "깊이",
                "옆면",
            ],
            correct="B",
            explanation="위에서 본 모양은 가로와 세로(평면의 모양)만 나타나고 높이는 알 수 없습니다.",
        ),

        # e6-2-3-02: 쌓은 모양과 위에서 본 모양으로 쌓기나무의 개수 알아보기
        mc(
            id="e6-2-3-02-cc-001",
            concept_id="e6-2-3-02",
            category="concept",
            part="geo",
            difficulty=7,
            content="위에서 본 모양이 2×2 정사각형일 때, 쌓기나무의 최소 개수는?",
            options=[
                "2개",
                "4개",
                "6개",
                "8개",
            ],
            correct="B",
            explanation="최소 개수는 위에서 본 모양의 칸 수와 같습니다. 2×2 = 4개입니다.",
        ),
        mc(
            id="e6-2-3-02-cc-002",
            concept_id="e6-2-3-02",
            category="concept",
            part="geo",
            difficulty=8,
            content="위에서 본 모양이 3×2이고, 각 칸에 최대 3개씩 쌓을 때, 최대 개수는?",
            options=[
                "6개",
                "12개",
                "18개",
                "24개",
            ],
            correct="C",
            explanation="위에서 본 모양의 칸 수 × 최대 높이 = 3×2 × 3 = 18개입니다.",
        ),

        # e6-2-3-03: 위, 앞, 옆에서 본 모양으로 쌓은 모양과 개수 알아보기
        mc(
            id="e6-2-3-03-cc-001",
            concept_id="e6-2-3-03",
            category="concept",
            part="geo",
            difficulty=8,
            content="위, 앞, 옆에서 본 모양만으로 쌓기나무의 전체 모양을 정확히 알 수 있습니까?",
            options=[
                "항상 알 수 있다",
                "항상 알 수 없다",
                "경우에 따라 다르다",
                "위와 앞만 있으면 알 수 있다",
            ],
            correct="C",
            explanation="투영도만으로는 전체 모양이 하나로 결정되지 않을 수 있습니다. 여러 배치가 가능한 경우가 있습니다.",
        ),
        mc(
            id="e6-2-3-03-cc-002",
            concept_id="e6-2-3-03",
            category="concept",
            part="geo",
            difficulty=9,
            content="위에서 본 모양이 2×2, 앞에서 본 모양이 높이 3인 직사각형일 때, 최소 개수는?",
            options=[
                "4개",
                "6개",
                "8개",
                "12개",
            ],
            correct="A",
            explanation="최소 개수는 위에서 본 모양의 칸 수와 같습니다. 2×2 = 4개입니다. 높이 조건은 최소 개수에 영향을 주지 않습니다.",
        ),

        # e6-2-3-04: 위에서 본 모양에 수를 써서 쌓은 모양과 개수 알아보기
        mc(
            id="e6-2-3-04-cc-001",
            concept_id="e6-2-3-04",
            category="concept",
            part="geo",
            difficulty=6,
            content="위에서 본 모양의 각 칸에 적힌 숫자는 무엇을 나타냅니까?",
            options=[
                "쌓기나무의 가로 길이",
                "쌓기나무의 세로 길이",
                "각 칸에 쌓인 쌓기나무의 개수",
                "쌓기나무의 넓이",
            ],
            correct="C",
            explanation="위에서 본 모양에 적힌 숫자는 각 칸에 쌓인 쌓기나무의 개수(높이)를 나타냅니다.",
        ),
        mc(
            id="e6-2-3-04-cc-002",
            concept_id="e6-2-3-04",
            category="concept",
            part="geo",
            difficulty=7,
            content="위에서 본 모양의 각 칸에 2, 3, 1, 4가 적혀 있을 때, 쌓기나무는 모두 몇 개입니까?",
            options=[
                "4개",
                "10개",
                "14개",
                "24개",
            ],
            correct="B",
            explanation="각 칸의 숫자를 모두 더하면 됩니다. 2 + 3 + 1 + 4 = 10개입니다.",
        ),

        # e6-2-3-05: 층별로 나타낸 모양으로 쌓은 모양과 개수 알아보기
        mc(
            id="e6-2-3-05-cc-001",
            concept_id="e6-2-3-05",
            category="concept",
            part="geo",
            difficulty=7,
            content="1층에 4개, 2층에 2개, 3층에 1개 쌓았을 때, 전체 개수는?",
            options=[
                "3개",
                "6개",
                "7개",
                "24개",
            ],
            correct="C",
            explanation="각 층의 쌓기나무 개수를 모두 더합니다. 4 + 2 + 1 = 7개입니다.",
        ),
        mc(
            id="e6-2-3-05-cc-002",
            concept_id="e6-2-3-05",
            category="concept",
            part="geo",
            difficulty=8,
            content="층별로 나타낸 모양에서 3층이 비어 있다면 전체 높이는?",
            options=[
                "1층",
                "2층",
                "3층",
                "알 수 없다",
            ],
            correct="B",
            explanation="3층이 비어 있으므로 실제 높이는 2층입니다.",
        ),

        # e6-2-3-06: 여러 가지 모양 만들기
        mc(
            id="e6-2-3-06-cc-001",
            concept_id="e6-2-3-06",
            category="concept",
            part="geo",
            difficulty=8,
            content="쌓기나무 6개로 만들 수 있는 서로 다른 모양은 몇 가지입니까?",
            options=[
                "1가지",
                "여러 가지",
                "6가지",
                "정확히 3가지",
            ],
            correct="B",
            explanation="같은 개수의 쌓기나무로 여러 가지 다른 모양을 만들 수 있습니다.",
        ),
        mc(
            id="e6-2-3-06-cc-002",
            concept_id="e6-2-3-06",
            category="concept",
            part="geo",
            difficulty=9,
            content="위에서 본 모양이 2×2이고 앞에서 본 높이가 3일 때, 만들 수 있는 모양은?",
            options=[
                "1가지뿐이다",
                "여러 가지가 가능하다",
                "불가능하다",
                "정확히 2가지이다",
            ],
            correct="B",
            explanation="같은 투영도를 만족하는 여러 가지 쌓기나무 배치가 가능합니다.",
        ),

        # ====================================
        # 2학기 4단원: 비례식과 비례배분 (12개)
        # ====================================

        # e6-2-4-01: 비의 성질
        mc(
            id="e6-2-4-01-cc-001",
            concept_id="e6-2-4-01",
            category="concept",
            part="algebra",
            difficulty=6,
            content="비 2:3에서 전항과 후항에 2를 곱하면?",
            options=[
                "2:3",
                "4:5",
                "4:6",
                "2:6",
            ],
            correct="C",
            explanation="비의 성질: 전항과 후항에 0이 아닌 같은 수를 곱해도 비율은 같습니다. 2×2 : 3×2 = 4:6입니다.",
        ),
        mc(
            id="e6-2-4-01-cc-002",
            concept_id="e6-2-4-01",
            category="concept",
            part="algebra",
            difficulty=7,
            content="비 8:12를 가장 간단한 자연수의 비로 나타내면?",
            options=[
                "2:3",
                "4:6",
                "8:12",
                "1:1.5",
            ],
            correct="A",
            explanation="8과 12의 최대공약수 4로 나눕니다. 8÷4 : 12÷4 = 2:3입니다.",
        ),

        # e6-2-4-02: 간단한 자연수의 비로 나타내기
        mc(
            id="e6-2-4-02-cc-001",
            concept_id="e6-2-4-02",
            category="concept",
            part="algebra",
            difficulty=7,
            content="비 0.5:1.5를 가장 간단한 자연수의 비로 나타내면?",
            options=[
                "1:2",
                "1:3",
                "5:15",
                "0.5:1.5",
            ],
            correct="B",
            explanation="소수를 자연수로 만들기 위해 10을 곱하면 5:15, 5로 나누면 1:3입니다.",
        ),
        mc(
            id="e6-2-4-02-cc-002",
            concept_id="e6-2-4-02",
            category="concept",
            part="algebra",
            difficulty=8,
            content="비 1/2 : 1/3을 가장 간단한 자연수의 비로 나타내면?",
            options=[
                "1:2",
                "2:3",
                "3:2",
                "1:3",
            ],
            correct="C",
            explanation="분모의 최소공배수 6을 곱하면 3:2입니다.",
        ),

        # e6-2-4-03: 비례식
        mc(
            id="e6-2-4-03-cc-001",
            concept_id="e6-2-4-03",
            category="concept",
            part="algebra",
            difficulty=6,
            content="비례식 a:b = c:d에서 외항은 무엇입니까?",
            options=[
                "a와 b",
                "b와 c",
                "a와 d",
                "c와 d",
            ],
            correct="C",
            explanation="비례식에서 외항은 양 끝의 항인 a와 d입니다. 내항은 가운데 두 항인 b와 c입니다.",
        ),
        mc(
            id="e6-2-4-03-cc-002",
            concept_id="e6-2-4-03",
            category="concept",
            part="algebra",
            difficulty=7,
            content="비례식 2:3 = 4:6에서 내항은 무엇입니까?",
            options=[
                "2와 6",
                "3과 4",
                "2와 3",
                "4와 6",
            ],
            correct="B",
            explanation="비례식에서 내항은 가운데 두 항인 3과 4입니다.",
        ),

        # e6-2-4-04: 비례식의 성질
        mc(
            id="e6-2-4-04-cc-001",
            concept_id="e6-2-4-04",
            category="concept",
            part="algebra",
            difficulty=7,
            content="비례식 2:3 = 4:☐에서 ☐에 알맞은 수는?",
            options=[
                "5",
                "6",
                "7",
                "8",
            ],
            correct="B",
            explanation="외항의 곱 = 내항의 곱이므로, 2 × ☐ = 3 × 4 = 12, ☐ = 6입니다.",
        ),
        mc(
            id="e6-2-4-04-cc-002",
            concept_id="e6-2-4-04",
            category="concept",
            part="algebra",
            difficulty=8,
            content="비례식 3:5 = 9:☐에서 ☐의 값은?",
            options=[
                "12",
                "15",
                "18",
                "20",
            ],
            correct="B",
            explanation="3 × ☐ = 5 × 9 = 45, ☐ = 15입니다.",
        ),

        # e6-2-4-05: 비례식 활용하기
        mc(
            id="e6-2-4-05-cc-001",
            concept_id="e6-2-4-05",
            category="concept",
            part="algebra",
            difficulty=8,
            content="물 2L로 주스 3L를 만들 수 있다면, 물 6L로 만들 수 있는 주스는?",
            options=[
                "6L",
                "9L",
                "12L",
                "18L",
            ],
            correct="B",
            explanation="비례식 2:3 = 6:☐에서 ☐ = 9L입니다.",
        ),
        mc(
            id="e6-2-4-05-cc-002",
            concept_id="e6-2-4-05",
            category="concept",
            part="algebra",
            difficulty=9,
            content="지도에서 2cm가 실제 10km일 때, 실제 25km는 지도에서 몇 cm입니까?",
            options=[
                "4cm",
                "5cm",
                "6cm",
                "10cm",
            ],
            correct="B",
            explanation="비례식 2:10 = ☐:25에서 ☐ = 5cm입니다.",
        ),

        # e6-2-4-06: 비례배분
        mc(
            id="e6-2-4-06-cc-001",
            concept_id="e6-2-4-06",
            category="concept",
            part="algebra",
            difficulty=8,
            content="24를 2:4의 비로 비례배분하면 작은 쪽은?",
            options=[
                "6",
                "8",
                "12",
                "16",
            ],
            correct="B",
            explanation="비의 합 = 2 + 4 = 6입니다. 작은 쪽 = 24 × 2/6 = 8입니다.",
        ),
        mc(
            id="e6-2-4-06-cc-002",
            concept_id="e6-2-4-06",
            category="concept",
            part="algebra",
            difficulty=9,
            content="30을 3:2의 비로 비례배분하면 큰 쪽은?",
            options=[
                "12",
                "15",
                "18",
                "20",
            ],
            correct="C",
            explanation="비의 합 = 3 + 2 = 5입니다. 큰 쪽 = 30 × 3/5 = 18입니다.",
        ),

        # ====================================
        # 2학기 5단원: 원의 넓이 (12개)
        # ====================================

        # e6-2-5-01: 원주와 지름의 관계
        mc(
            id="e6-2-5-01-cc-001",
            concept_id="e6-2-5-01",
            category="concept",
            part="geo",
            difficulty=6,
            content="원주와 지름의 관계는?",
            options=[
                "원주 = 지름",
                "원주 ≈ 지름 × 3.14",
                "원주 = 지름 ÷ 2",
                "원주 = 지름 + 3.14",
            ],
            correct="B",
            explanation="원주 = 지름 × 원주율(약 3.14)입니다.",
        ),
        mc(
            id="e6-2-5-01-cc-002",
            concept_id="e6-2-5-01",
            category="concept",
            part="geo",
            difficulty=7,
            content="원주를 지름으로 나누면 어떤 값이 나옵니까?",
            options=[
                "원의 넓이",
                "원주율",
                "반지름",
                "지름의 2배",
            ],
            correct="B",
            explanation="원주 ÷ 지름 = 원주율(약 3.14)입니다. 모든 원에서 이 값은 일정합니다.",
        ),

        # e6-2-5-02: 원주율
        mc(
            id="e6-2-5-02-cc-001",
            concept_id="e6-2-5-02",
            category="concept",
            part="geo",
            difficulty=5,
            content="원주율의 값은 약 얼마입니까?",
            options=[
                "2.14",
                "3.14",
                "4.14",
                "5.14",
            ],
            correct="B",
            explanation="원주율(π)은 약 3.14 또는 3.1로 어림하여 사용합니다.",
        ),
        mc(
            id="e6-2-5-02-cc-002",
            concept_id="e6-2-5-02",
            category="concept",
            part="geo",
            difficulty=6,
            content="원주율은 모든 원에서 어떻습니까?",
            options=[
                "원의 크기에 따라 다르다",
                "항상 같다",
                "작은 원일수록 크다",
                "큰 원일수록 크다",
            ],
            correct="B",
            explanation="원주율은 모든 원에서 일정한 값(약 3.14)입니다.",
        ),

        # e6-2-5-03: 원주와 지름 구하기
        mc(
            id="e6-2-5-03-cc-001",
            concept_id="e6-2-5-03",
            category="concept",
            part="geo",
            difficulty=7,
            content="지름이 10cm인 원의 원주는 약 몇 cm입니까? (원주율: 3.14)",
            options=[
                "31.4 cm",
                "62.8 cm",
                "314 cm",
                "15.7 cm",
            ],
            correct="A",
            explanation="원주 = 지름 × 원주율 = 10 × 3.14 = 31.4 cm입니다.",
        ),
        mc(
            id="e6-2-5-03-cc-002",
            concept_id="e6-2-5-03",
            category="concept",
            part="geo",
            difficulty=8,
            content="원주가 62.8cm인 원의 지름은 약 몇 cm입니까? (원주율: 3.14)",
            options=[
                "10 cm",
                "20 cm",
                "31.4 cm",
                "197.192 cm",
            ],
            correct="B",
            explanation="지름 = 원주 ÷ 원주율 = 62.8 ÷ 3.14 = 20 cm입니다.",
        ),

        # e6-2-5-04: 원의 넓이 어림하기
        mc(
            id="e6-2-5-04-cc-001",
            concept_id="e6-2-5-04",
            category="concept",
            part="geo",
            difficulty=6,
            content="모눈종이에서 원의 넓이를 어림하는 방법은?",
            options=[
                "원 안의 완전히 포함된 칸만 센다",
                "원 밖의 칸을 센다",
                "원과 걸친 칸은 반 칸으로 어림한다",
                "원의 지름을 센다",
            ],
            correct="C",
            explanation="원과 걸친 칸을 반 칸 정도로 어림하여 넓이를 구합니다.",
        ),
        mc(
            id="e6-2-5-04-cc-002",
            concept_id="e6-2-5-04",
            category="concept",
            part="geo",
            difficulty=7,
            content="원의 넓이를 어림할 때 사용하는 도구는?",
            options=[
                "자",
                "컴퍼스",
                "모눈종이",
                "각도기",
            ],
            correct="C",
            explanation="모눈종이를 이용하여 원의 넓이를 어림할 수 있습니다.",
        ),

        # e6-2-5-05: 원의 넓이 구하는 방법
        mc(
            id="e6-2-5-05-cc-001",
            concept_id="e6-2-5-05",
            category="concept",
            part="geo",
            difficulty=7,
            content="원의 넓이를 구하는 공식에서 r은 무엇을 의미합니까?",
            options=[
                "원주",
                "지름",
                "반지름",
                "원주율",
            ],
            correct="C",
            explanation="원의 넓이 = πr²에서 r은 반지름입니다.",
        ),
        mc(
            id="e6-2-5-05-cc-002",
            concept_id="e6-2-5-05",
            category="concept",
            part="geo",
            difficulty=8,
            content="반지름이 2배가 되면 원의 넓이는 몇 배가 됩니까?",
            options=[
                "2배",
                "3배",
                "4배",
                "8배",
            ],
            correct="C",
            explanation="원의 넓이 = πr²이므로, 반지름이 2배가 되면 넓이는 2² = 4배가 됩니다.",
        ),

        # e6-2-5-06: 여러 가지 원의 넓이 구하기
        mc(
            id="e6-2-5-06-cc-001",
            concept_id="e6-2-5-06",
            category="concept",
            part="geo",
            difficulty=8,
            content="반원의 둘레를 구할 때 포함해야 하는 것은?",
            options=[
                "곡선 부분만",
                "곡선 부분 + 지름",
                "곡선 부분 + 반지름 2개",
                "원주 전체",
            ],
            correct="B",
            explanation="반원의 둘레 = (원주의 반) + 지름 = πr + 2r입니다. 곡선 부분만 계산하는 오류에 주의하세요.",
        ),
        mc(
            id="e6-2-5-06-cc-002",
            concept_id="e6-2-5-06",
            category="concept",
            part="geo",
            difficulty=9,
            content="반지름이 5cm인 반원의 넓이는? (원주율: 3.14)",
            options=[
                "39.25 cm²",
                "78.5 cm²",
                "15.7 cm²",
                "25 cm²",
            ],
            correct="A",
            explanation="반원의 넓이 = (원의 넓이) ÷ 2 = 3.14 × 5 × 5 ÷ 2 = 39.25 cm²입니다.",
        ),

        # ====================================
        # 2학기 6단원: 원기둥, 원뿔, 구 (8개)
        # ====================================

        # e6-2-6-01: 원기둥
        mc(
            id="e6-2-6-01-cc-001",
            concept_id="e6-2-6-01",
            category="concept",
            part="geo",
            difficulty=5,
            content="원기둥의 밑면은 어떤 도형입니까?",
            options=[
                "직사각형",
                "삼각형",
                "원",
                "정사각형",
            ],
            correct="C",
            explanation="원기둥의 밑면은 원입니다. 밑면이 2개 있습니다.",
        ),
        mc(
            id="e6-2-6-01-cc-002",
            concept_id="e6-2-6-01",
            category="concept",
            part="geo",
            difficulty=6,
            content="원기둥을 회전축에 수직으로 자른 단면의 모양은?",
            options=[
                "직사각형",
                "원",
                "타원",
                "삼각형",
            ],
            correct="B",
            explanation="원기둥을 회전축에 수직으로 자르면 단면은 원입니다.",
        ),

        # e6-2-6-02: 원기둥의 전개도
        mc(
            id="e6-2-6-02-cc-001",
            concept_id="e6-2-6-02",
            category="concept",
            part="geo",
            difficulty=7,
            content="원기둥의 전개도에서 옆면은 어떤 도형입니까?",
            options=[
                "원",
                "정사각형",
                "직사각형",
                "삼각형",
            ],
            correct="C",
            explanation="원기둥의 전개도에서 옆면은 직사각형입니다.",
        ),
        mc(
            id="e6-2-6-02-cc-002",
            concept_id="e6-2-6-02",
            category="concept",
            part="geo",
            difficulty=8,
            content="원기둥의 전개도에서 옆면의 가로는 무엇과 같습니까?",
            options=[
                "밑면의 원주",
                "밑면의 지름",
                "원기둥의 높이",
                "밑면의 반지름",
            ],
            correct="A",
            explanation="원기둥의 전개도에서 옆면의 가로 = 밑면의 원주입니다.",
        ),

        # e6-2-6-03: 원뿔
        mc(
            id="e6-2-6-03-cc-001",
            concept_id="e6-2-6-03",
            category="concept",
            part="geo",
            difficulty=6,
            content="원뿔에서 꼭짓점에서 밑면의 원까지 수직으로 내린 선분은 무엇입니까?",
            options=[
                "모선",
                "높이",
                "반지름",
                "지름",
            ],
            correct="B",
            explanation="원뿔의 높이는 꼭짓점에서 밑면에 수직으로 내린 선분입니다. 옆면을 따라 내려가는 모선과 혼동하지 마세요.",
        ),
        mc(
            id="e6-2-6-03-cc-002",
            concept_id="e6-2-6-03",
            category="concept",
            part="geo",
            difficulty=7,
            content="원뿔의 모선은 무엇입니까?",
            options=[
                "높이",
                "밑면의 반지름",
                "꼭짓점에서 밑면의 원 위의 점까지의 선분",
                "밑면의 지름",
            ],
            correct="C",
            explanation="모선은 원뿔의 꼭짓점에서 밑면의 원 위의 점까지의 선분입니다.",
        ),

        # e6-2-6-04: 구
        mc(
            id="e6-2-6-04-cc-001",
            concept_id="e6-2-6-04",
            category="concept",
            part="geo",
            difficulty=6,
            content="구를 완벽하게 펼친 전개도를 그릴 수 있습니까?",
            options=[
                "가능하다",
                "불가능하다",
                "특정 방법으로만 가능하다",
                "작은 구만 가능하다",
            ],
            correct="B",
            explanation="구는 곡면이므로 평면으로 완벽하게 펼칠 수 없습니다. 지구본을 종이 지도로 그릴 때 왜곡이 생기는 것과 같은 원리입니다.",
        ),
        mc(
            id="e6-2-6-04-cc-002",
            concept_id="e6-2-6-04",
            category="concept",
            part="geo",
            difficulty=7,
            content="구의 중심에서 구의 표면까지의 거리를 무엇이라 합니까?",
            options=[
                "지름",
                "반지름",
                "높이",
                "모선",
            ],
            correct="B",
            explanation="구의 중심에서 표면까지의 거리는 반지름입니다.",
        ),
    ]
