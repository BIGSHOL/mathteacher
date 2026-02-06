"""초등 4학년 개념 문제 시드 데이터.

커버 단원:
  1학기 2단원 - 각도
  1학기 4단원 - 평면도형의 이동
  1학기 5단원 - 막대그래프
  1학기 6단원 - 규칙 찾기
  2학기 2단원 - 삼각형
  2학기 4단원 - 사각형
  2학기 5단원 - 꺾은선그래프
  2학기 6단원 - 다각형
"""
from app.seeds._base import mc, concept


def get_concepts():
    """개념 관련 개념 반환."""
    return [
        concept(
            id="concept-e4-angle-01",
            name="각도 - 각의 크기와 분류",
            grade="elementary_4",
            category="concept",
            part="geo",
            description="각의 크기(예각·직각·둔각)를 이해하고, 각도기로 측정하며, 변의 길이와 각의 크기가 무관함을 압니다.",
        ),
        concept(
            id="concept-e4-angle-02",
            name="각도 - 내각의 합",
            grade="elementary_4",
            category="concept",
            part="geo",
            description="삼각형 내각의 합(180°)과 사각형 내각의 합(360°)을 이해하고 활용합니다.",
        ),
        concept(
            id="concept-e4-transform-01",
            name="평면도형의 이동 - 밀기",
            grade="elementary_4",
            category="concept",
            part="geo",
            description="밀기(평행이동)에서 위치만 변하고 모양·크기·방향은 불변임을 이해합니다.",
        ),
        concept(
            id="concept-e4-transform-02",
            name="평면도형의 이동 - 뒤집기와 돌리기",
            grade="elementary_4",
            category="concept",
            part="geo",
            description="뒤집기(대칭)와 돌리기(회전)의 차이를 이해하고, 시계/반시계 방향 관계를 압니다.",
        ),
        concept(
            id="concept-e4-bar-graph-01",
            name="막대그래프 - 읽기와 해석",
            grade="elementary_4",
            category="concept",
            part="data",
            description="막대그래프의 구성 요소를 알고, 눈금을 읽어 값을 파악하며 항목 간 비교를 합니다.",
        ),
        concept(
            id="concept-e4-bar-graph-02",
            name="막대그래프 - 그리기와 눈금 설정",
            grade="elementary_4",
            category="concept",
            part="data",
            description="자료에 적절한 눈금 크기를 정하여 막대그래프를 그릴 수 있습니다.",
        ),
        concept(
            id="concept-e4-pattern-01",
            name="규칙 찾기 - 수 배열 규칙",
            grade="elementary_4",
            category="concept",
            part="algebra",
            description="수의 배열에서 덧셈, 곱셈 등의 규칙을 찾고 다음 수를 예측합니다.",
        ),
        concept(
            id="concept-e4-pattern-02",
            name="규칙 찾기 - 도형과 계산식 패턴",
            grade="elementary_4",
            category="concept",
            part="algebra",
            description="도형 배열의 규칙과 계산식의 패턴을 발견하여 수학적 언어로 표현합니다.",
        ),
        concept(
            id="concept-e4-triangle-01",
            name="삼각형 - 변에 의한 분류",
            grade="elementary_4",
            category="concept",
            part="geo",
            description="이등변삼각형·정삼각형의 성질과 포함 관계(정삼각형 ⊂ 이등변삼각형)를 이해합니다.",
        ),
        concept(
            id="concept-e4-triangle-02",
            name="삼각형 - 각에 의한 분류",
            grade="elementary_4",
            category="concept",
            part="geo",
            description="예각삼각형·직각삼각형·둔각삼각형의 분류 기준을 이해합니다.",
        ),
        concept(
            id="concept-e4-quad-01",
            name="사각형 - 수직과 평행",
            grade="elementary_4",
            category="concept",
            part="geo",
            description="수직(90° 만남)과 평행(만나지 않음)의 개념을 이해합니다.",
        ),
        concept(
            id="concept-e4-quad-02",
            name="사각형 - 사각형 분류와 포함 관계",
            grade="elementary_4",
            category="concept",
            part="geo",
            description="사다리꼴·평행사변형·마름모·직사각형·정사각형의 분류 체계와 포함 관계를 이해합니다.",
        ),
        concept(
            id="concept-e4-line-graph-01",
            name="꺾은선그래프 - 읽기와 해석",
            grade="elementary_4",
            category="concept",
            part="data",
            description="꺾은선그래프에서 변화 추이를 읽고, 기울기로 변화 크기를 판단합니다.",
        ),
        concept(
            id="concept-e4-line-graph-02",
            name="꺾은선그래프 - 그리기와 물결선",
            grade="elementary_4",
            category="concept",
            part="data",
            description="적절한 그래프 유형을 선택하고, 물결선으로 불필요한 구간을 생략하여 그래프를 그립니다.",
        ),
        concept(
            id="concept-e4-polygon-01",
            name="다각형 - 다각형 정의와 대각선",
            grade="elementary_4",
            category="concept",
            part="geo",
            description="다각형의 정의(선분으로만 둘러싸인 닫힌 도형)와 대각선의 개념을 이해합니다.",
        ),
        concept(
            id="concept-e4-polygon-02",
            name="다각형 - 정다각형의 조건",
            grade="elementary_4",
            category="concept",
            part="geo",
            description="정다각형의 두 조건(변의 길이 모두 같음 + 각의 크기 모두 같음)을 이해합니다.",
        ),
    ]


def get_questions():
    """개념 문제 반환."""
    return [
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 2단원: 각도
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e4-conc-001",
            concept_id="concept-e4-angle-01",
            category="concept",
            part="geo",
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
            concept_id="concept-e4-angle-01",
            category="concept",
            part="geo",
            difficulty=4,
            content="두 삼각형의 한 각의 크기가 같습니다. 하나는 변이 짧고 다른 하나는 변이 깁니다. 다음 중 옳은 것은?",
            options=[
                ("변이 긴 삼각형의 각이 더 크다", "변이 긴 삼각형의 각이 더 크다"),
                ("두 각의 크기는 같다", "두 각의 크기는 같다"),
                ("변이 짧은 삼각형의 각이 더 크다", "변이 짧은 삼각형의 각이 더 크다"),
                ("비교할 수 없다", "비교할 수 없다"),
            ],
            correct="B",
            explanation="각의 크기는 두 변이 벌어진 정도이며, 변의 길이와는 관계가 없습니다. '변이 길면 각도가 크다'는 것은 흔한 오해입니다.",
            points=10,
        ),
        mc(
            id="e4-conc-003",
            concept_id="concept-e4-angle-02",
            category="concept",
            part="geo",
            difficulty=7,
            content="삼각형의 세 각의 크기의 합은 몇 도인가요?",
            options=[
                ("90도", "90도"),
                ("180도", "180도"),
                ("270도", "270도"),
                ("360도", "360도"),
            ],
            correct="B",
            explanation="삼각형의 세 각의 크기의 합은 모양이나 크기에 관계없이 항상 180도입니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 4단원: 평면도형의 이동
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e4-conc-004",
            concept_id="concept-e4-transform-01",
            category="concept",
            part="geo",
            difficulty=2,
            content="도형을 밀었을 때 변하는 것은?",
            options=[
                ("모양", "모양"),
                ("크기", "크기"),
                ("위치", "위치"),
                ("방향", "방향"),
            ],
            correct="C",
            explanation="밀기는 도형의 위치만 변화시키고, 모양·크기·방향은 변하지 않습니다.",
            points=10,
        ),
        mc(
            id="e4-conc-005",
            concept_id="concept-e4-transform-02",
            category="concept",
            part="geo",
            difficulty=5,
            content="글자 'ㄱ'을 오른쪽으로 뒤집은 결과와 시계방향으로 180° 돌린 결과는?",
            options=[
                ("같다", "같다"),
                ("다르다", "다르다"),
                ("뒤집기만 가능하다", "뒤집기만 가능하다"),
                ("돌리기만 가능하다", "돌리기만 가능하다"),
            ],
            correct="B",
            explanation="비대칭 도형(ㄱ, ㄴ, P 등)에서는 뒤집기와 180° 돌리기의 결과가 다릅니다. 뒤집기는 좌우가 반전되고, 돌리기는 상하좌우가 함께 바뀝니다.",
            points=10,
        ),
        mc(
            id="e4-conc-006",
            concept_id="concept-e4-transform-02",
            category="concept",
            part="geo",
            difficulty=7,
            content="도형을 시계방향으로 90° 돌린 것은 반시계방향으로 몇 도 돌린 것과 같은가요?",
            options=[
                ("90도", "90도"),
                ("180도", "180도"),
                ("270도", "270도"),
                ("360도", "360도"),
            ],
            correct="C",
            explanation="시계방향 90° 돌리기 = 반시계방향 270° 돌리기입니다. 시계 + 반시계 = 360°가 되어야 원래 위치입니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 5단원: 막대그래프
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e4-conc-007",
            concept_id="concept-e4-bar-graph-01",
            category="concept",
            part="data",
            difficulty=2,
            content="막대그래프의 구성 요소가 아닌 것은?",
            options=[
                ("가로축과 세로축", "가로축과 세로축"),
                ("눈금", "눈금"),
                ("꺾은선", "꺾은선"),
                ("제목", "제목"),
            ],
            correct="C",
            explanation="막대그래프의 구성 요소는 가로축, 세로축, 눈금, 막대, 제목입니다. 꺾은선은 꺾은선그래프의 요소입니다.",
            points=10,
        ),
        mc(
            id="e4-conc-008",
            concept_id="concept-e4-bar-graph-02",
            category="concept",
            part="data",
            difficulty=5,
            content="자료의 값이 10, 25, 35, 50일 때, 막대그래프의 눈금 한 칸의 크기로 가장 적절한 것은?",
            options=[
                ("1", "1"),
                ("5", "5"),
                ("20", "20"),
                ("50", "50"),
            ],
            correct="B",
            explanation="눈금 한 칸의 크기는 자료의 크기에 맞게 정합니다. 최댓값 50에 대해 5씩이면 10칸으로 적당합니다. 1이면 50칸(너무 많음), 20이면 중간값 표현이 어렵고, 50이면 1칸밖에 안 됩니다.",
            points=10,
        ),
        mc(
            id="e4-conc-009",
            concept_id="concept-e4-bar-graph-01",
            category="concept",
            part="data",
            difficulty=7,
            content="막대그래프에서 눈금 한 칸이 10명이고, 어떤 항목의 막대가 눈금 3칸과 4칸 사이 중간쯤에 있습니다. 이 항목의 인원수로 적절한 것은?",
            options=[
                ("30명", "30명"),
                ("35명", "35명"),
                ("40명", "40명"),
                ("34명", "34명"),
            ],
            correct="B",
            explanation="눈금 3칸=30명, 4칸=40명이므로 중간값은 약 35명입니다. 눈금선 중간에 있는 값을 어림하여 읽는 능력이 필요합니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 6단원: 규칙 찾기
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e4-conc-010",
            concept_id="concept-e4-pattern-01",
            category="concept",
            part="algebra",
            difficulty=1,
            content="2, 4, 6, 8 다음에 올 수는?",
            options=[
                ("9", "9"),
                ("10", "10"),
                ("12", "12"),
                ("16", "16"),
            ],
            correct="B",
            explanation="2씩 커지는 규칙입니다. 8 + 2 = 10입니다.",
            points=10,
        ),
        mc(
            id="e4-conc-011",
            concept_id="concept-e4-pattern-01",
            category="concept",
            part="algebra",
            difficulty=5,
            content="1, 2, 4, 8, 16, ... 이 수 배열의 규칙은?",
            options=[
                ("2씩 더한다", "2씩 더한다"),
                ("앞의 수에 2를 곱한다", "앞의 수에 2를 곱한다"),
                ("짝수만 나열한다", "짝수만 나열한다"),
                ("4씩 더한다", "4씩 더한다"),
            ],
            correct="B",
            explanation="1×2=2, 2×2=4, 4×2=8, 8×2=16으로 앞의 수에 2를 곱하는 규칙입니다. 차이만 보면 1,2,4,8로 일정하지 않으므로 덧셈 규칙이 아닙니다.",
            points=10,
        ),
        mc(
            id="e4-conc-012",
            concept_id="concept-e4-pattern-02",
            category="concept",
            part="algebra",
            difficulty=8,
            content="바둑돌을 1개, 3개, 6개, 10개, ... 로 삼각형 모양을 만들고 있습니다. 5번째에 필요한 바둑돌은 몇 개인가요?",
            options=[
                ("13개", "13개"),
                ("14개", "14개"),
                ("15개", "15개"),
                ("16개", "16개"),
            ],
            correct="C",
            explanation="각 단계에서 이전보다 2, 3, 4, ... 개씩 늘어납니다. 1→3(+2)→6(+3)→10(+4)→15(+5)입니다. 5번째는 15개입니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 2단원: 삼각형
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e4-conc-013",
            concept_id="concept-e4-triangle-01",
            category="concept",
            part="geo",
            difficulty=3,
            content="이등변삼각형의 특징으로 옳은 것은?",
            options=[
                ("세 변의 길이가 모두 같다", "세 변의 길이가 모두 같다"),
                ("두 변의 길이가 같고 두 밑각의 크기가 같다", "두 변의 길이가 같고 두 밑각의 크기가 같다"),
                ("세 각의 크기가 모두 다르다", "세 각의 크기가 모두 다르다"),
                ("한 각이 반드시 직각이다", "한 각이 반드시 직각이다"),
            ],
            correct="B",
            explanation="이등변삼각형은 두 변의 길이가 같고, 같은 변 사이의 두 밑각의 크기도 같습니다.",
            points=10,
        ),
        mc(
            id="e4-conc-014",
            concept_id="concept-e4-triangle-02",
            category="concept",
            part="geo",
            difficulty=6,
            content="삼각형의 세 각이 30°, 40°, 110°일 때, 이 삼각형에 대한 설명으로 옳은 것은?",
            options=[
                ("예각삼각형이다 (예각이 2개 있으므로)", "예각삼각형이다 (예각이 2개 있으므로)"),
                ("직각삼각형이다", "직각삼각형이다"),
                ("둔각삼각형이다", "둔각삼각형이다"),
                ("알 수 없다", "알 수 없다"),
            ],
            correct="C",
            explanation="110°는 둔각이므로 이 삼각형은 둔각삼각형입니다. 예각이 여러 개 있어도 둔각이 하나라도 있으면 둔각삼각형입니다. '예각이 있으면 예각삼각형'이라는 것은 오해입니다.",
            points=10,
        ),
        mc(
            id="e4-conc-015",
            concept_id="concept-e4-triangle-01",
            category="concept",
            part="geo",
            difficulty=8,
            content="정삼각형은 이등변삼각형인가요?",
            options=[
                ("아니오, 정삼각형은 세 변이 같고 이등변삼각형은 두 변만 같다", "아니오, 정삼각형은 세 변이 같고 이등변삼각형은 두 변만 같다"),
                ("예, 정삼각형도 두 변의 길이가 같은 조건을 만족한다", "예, 정삼각형도 두 변의 길이가 같은 조건을 만족한다"),
                ("같은 도형이다", "같은 도형이다"),
                ("비교할 수 없다", "비교할 수 없다"),
            ],
            correct="B",
            explanation="정삼각형은 세 변의 길이가 모두 같으므로 '두 변의 길이가 같다'는 이등변삼각형의 조건을 당연히 만족합니다. 따라서 정삼각형 ⊂ 이등변삼각형입니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 4단원: 사각형
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e4-conc-016",
            concept_id="concept-e4-quad-01",
            category="concept",
            part="geo",
            difficulty=2,
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
        mc(
            id="e4-conc-017",
            concept_id="concept-e4-quad-02",
            category="concept",
            part="geo",
            difficulty=6,
            content="정사각형은 직사각형이라고 할 수 있나요?",
            options=[
                ("아니오, 정사각형과 직사각형은 다른 도형이다", "아니오, 정사각형과 직사각형은 다른 도형이다"),
                ("예, 정사각형은 네 각이 모두 직각이므로 직사각형이다", "예, 정사각형은 네 각이 모두 직각이므로 직사각형이다"),
                ("직사각형이 정사각형이다", "직사각형이 정사각형이다"),
                ("때에 따라 다르다", "때에 따라 다르다"),
            ],
            correct="B",
            explanation="직사각형은 '네 각이 모두 직각인 사각형'입니다. 정사각형도 네 각이 모두 직각이므로 직사각형에 포함됩니다. 정사각형 ⊂ 직사각형 ⊂ 평행사변형입니다.",
            points=10,
        ),
        mc(
            id="e4-conc-018",
            concept_id="concept-e4-quad-02",
            category="concept",
            part="geo",
            difficulty=9,
            content="다음 중 평행사변형에 해당하는 것을 모두 고르면?",
            options=[
                ("평행사변형, 마름모만", "평행사변형, 마름모만"),
                ("평행사변형, 직사각형만", "평행사변형, 직사각형만"),
                ("평행사변형, 마름모, 직사각형, 정사각형 모두", "평행사변형, 마름모, 직사각형, 정사각형 모두"),
                ("평행사변형만", "평행사변형만"),
            ],
            correct="C",
            explanation="평행사변형은 '마주 보는 두 쌍의 변이 평행한 사각형'입니다. 마름모, 직사각형, 정사각형 모두 이 조건을 만족하므로 평행사변형에 포함됩니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 5단원: 꺾은선그래프
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e4-conc-019",
            concept_id="concept-e4-line-graph-01",
            category="concept",
            part="data",
            difficulty=3,
            content="꺾은선그래프로 나타내기에 가장 적합한 자료는?",
            options=[
                ("반별 학생 수", "반별 학생 수"),
                ("좋아하는 과일 종류별 학생 수", "좋아하는 과일 종류별 학생 수"),
                ("1월부터 12월까지 월별 평균 기온", "1월부터 12월까지 월별 평균 기온"),
                ("학급별 남녀 학생 수", "학급별 남녀 학생 수"),
            ],
            correct="C",
            explanation="꺾은선그래프는 시간에 따른 연속적 변화를 나타내기에 적합합니다. 월별 기온 변화가 이에 해당합니다. 항목별 비교는 막대그래프가 적합합니다.",
            points=10,
        ),
        mc(
            id="e4-conc-020",
            concept_id="concept-e4-line-graph-01",
            category="concept",
            part="data",
            difficulty=5,
            content="꺾은선그래프에서 선분의 기울기가 급할수록 무엇을 의미하나요?",
            options=[
                ("값이 크다", "값이 크다"),
                ("변화가 크다", "변화가 크다"),
                ("변화가 작다", "변화가 작다"),
                ("값이 작다", "값이 작다"),
            ],
            correct="B",
            explanation="꺾은선그래프에서 선분의 기울기가 급할수록 같은 시간 동안 변화가 크다는 것을 의미합니다.",
            points=10,
        ),
        mc(
            id="e4-conc-021",
            concept_id="concept-e4-line-graph-02",
            category="concept",
            part="data",
            difficulty=7,
            content="꺾은선그래프에서 물결선(〰)의 역할은?",
            options=[
                ("그래프가 예쁘게 보이도록 꾸민다", "그래프가 예쁘게 보이도록 꾸민다"),
                ("필요 없는 눈금 구간을 생략한다", "필요 없는 눈금 구간을 생략한다"),
                ("값이 0인 구간을 표시한다", "값이 0인 구간을 표시한다"),
                ("그래프의 끝을 나타낸다", "그래프의 끝을 나타낸다"),
            ],
            correct="B",
            explanation="물결선은 자료 값 사이에 비어 있는 불필요한 눈금 구간을 생략하기 위해 사용합니다. 예를 들어 값이 모두 80~100 사이이면 0~80 구간을 물결선으로 생략합니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 6단원: 다각형
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e4-conc-022",
            concept_id="concept-e4-polygon-01",
            category="concept",
            part="geo",
            difficulty=2,
            content="다각형이란 무엇인가요?",
            options=[
                ("곡선으로 둘러싸인 도형", "곡선으로 둘러싸인 도형"),
                ("선분으로만 둘러싸인 닫힌 도형", "선분으로만 둘러싸인 닫힌 도형"),
                ("원처럼 둥근 도형", "원처럼 둥근 도형"),
                ("각이 있는 모든 도형", "각이 있는 모든 도형"),
            ],
            correct="B",
            explanation="다각형은 선분으로만 둘러싸인 닫힌 도형입니다. 곡선이 포함되면 다각형이 아닙니다.",
            points=10,
        ),
        mc(
            id="e4-conc-023",
            concept_id="concept-e4-polygon-02",
            category="concept",
            part="geo",
            difficulty=6,
            content="마름모는 정다각형인가요?",
            options=[
                ("예, 네 변의 길이가 모두 같으므로 정다각형이다", "예, 네 변의 길이가 모두 같으므로 정다각형이다"),
                ("아니오, 네 변의 길이가 같지만 네 각의 크기가 모두 같지 않을 수 있다", "아니오, 네 변의 길이가 같지만 네 각의 크기가 모두 같지 않을 수 있다"),
                ("예, 마름모는 항상 정사각형이다", "예, 마름모는 항상 정사각형이다"),
                ("정다각형은 삼각형만 해당된다", "정다각형은 삼각형만 해당된다"),
            ],
            correct="B",
            explanation="정다각형이 되려면 '변의 길이가 모두 같고' '각의 크기도 모두 같아야' 합니다(두 조건 모두 필요). 마름모는 변의 길이는 같지만 각의 크기가 같지 않을 수 있으므로 정다각형이 아닙니다.",
            points=10,
        ),
        mc(
            id="e4-conc-024",
            concept_id="concept-e4-polygon-02",
            category="concept",
            part="geo",
            difficulty=9,
            content="다음 중 정다각형에 대한 설명으로 옳은 것은?",
            options=[
                ("변의 길이만 모두 같으면 정다각형이다", "변의 길이만 모두 같으면 정다각형이다"),
                ("각의 크기만 모두 같으면 정다각형이다", "각의 크기만 모두 같으면 정다각형이다"),
                ("변의 길이가 모두 같고 각의 크기도 모두 같아야 정다각형이다", "변의 길이가 모두 같고 각의 크기도 모두 같아야 정다각형이다"),
                ("정삼각형만 정다각형이다", "정삼각형만 정다각형이다"),
            ],
            correct="C",
            explanation="정다각형은 변의 길이가 모두 같고 각의 크기도 모두 같아야 합니다. 반례: 마름모(변만 같음, 정다각형 아님), 직사각형(각만 같음, 정다각형 아님).",
            points=10,
        ),
    ]
