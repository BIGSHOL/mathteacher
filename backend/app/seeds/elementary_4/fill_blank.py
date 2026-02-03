"""초등 4학년 빈칸 채우기 문제 시드 데이터.

12단원 전체 커버 (단원당 2문항):
  1학기: 큰 수, 각도, 곱셈과 나눗셈, 평면도형의 이동, 막대그래프, 규칙 찾기
  2학기: 분수의 덧셈과 뺄셈, 삼각형, 소수의 덧셈과 뺄셈, 사각형, 꺾은선그래프, 다각형
"""
from app.seeds._base import fb


def get_questions():
    """빈칸 채우기 문제 반환."""
    return [
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 1단원: 큰 수
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e4-fb-001",
            concept_id="concept-e4-big-num",
            category="computation",
            part="calc",
            difficulty=2,
            content="10000이 10개이면 ____입니다.",
            answer="100000",
            explanation="10000 × 10 = 100000입니다. 10배의 원리로 자릿수가 왼쪽으로 한 칸 이동합니다.",
            points=10,
            accept_formats=["100000", "10만"],
        ),
        fb(
            id="e4-fb-002",
            concept_id="concept-e4-big-num",
            category="computation",
            part="calc",
            difficulty=5,
            content="1억은 1000만의 ____배입니다.",
            answer="10",
            explanation="1억 = 100,000,000이고 1000만 = 10,000,000입니다. 100,000,000 ÷ 10,000,000 = 10이므로 10배입니다.",
            points=10,
            accept_formats=["10"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 2단원: 각도
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e4-fb-003",
            concept_id="concept-e4-angle",
            category="concept",
            part="geo",
            difficulty=2,
            content="0도보다 크고 ____도보다 작은 각을 예각이라고 합니다.",
            answer="90",
            explanation="예각은 0도보다 크고 90도(직각)보다 작은 각입니다.",
            points=10,
            accept_formats=["90"],
        ),
        fb(
            id="e4-fb-004",
            concept_id="concept-e4-angle",
            category="concept",
            part="geo",
            difficulty=6,
            content="삼각형의 두 각이 70도와 50도일 때, 나머지 한 각은 ____도입니다.",
            answer="60",
            explanation="삼각형의 세 각의 합은 180도입니다. 180 - 70 - 50 = 60이므로 나머지 각은 60도입니다.",
            points=10,
            accept_formats=["60"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 3단원: 곱셈과 나눗셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e4-fb-005",
            concept_id="concept-e4-mul-div",
            category="computation",
            part="calc",
            difficulty=2,
            content="156 × 4 = ____",
            answer="624",
            explanation="156 × 4 = 624입니다. 6×4=24(2 올림), 5×4+2=22(2 올림), 1×4+2=6이므로 624입니다.",
            points=10,
            accept_formats=["624"],
        ),
        fb(
            id="e4-fb-006",
            concept_id="concept-e4-mul-div",
            category="computation",
            part="calc",
            difficulty=6,
            content="468 ÷ 18 = ____",
            answer="26",
            explanation="468 ÷ 18 = 26입니다. 검산: 18 × 26 = 468입니다.",
            points=10,
            accept_formats=["26"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 4단원: 평면도형의 이동
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e4-fb-007",
            concept_id="concept-e4-transform",
            category="concept",
            part="geo",
            difficulty=3,
            content="도형을 밀면 모양과 크기는 변하지 않고 ____만 변합니다.",
            answer="위치",
            explanation="밀기(평행이동)에서는 도형의 위치만 변하고, 모양·크기·방향은 변하지 않습니다.",
            points=10,
            accept_formats=["위치"],
        ),
        fb(
            id="e4-fb-008",
            concept_id="concept-e4-transform",
            category="concept",
            part="geo",
            difficulty=7,
            content="시계방향으로 90° 돌리기는 반시계방향으로 ____° 돌리기와 같습니다.",
            answer="270",
            explanation="시계방향 90° + 반시계방향 = 360°이므로 반시계방향 360° - 90° = 270°입니다.",
            points=10,
            accept_formats=["270"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 5단원: 막대그래프
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e4-fb-009",
            concept_id="concept-e4-bar-graph",
            category="concept",
            part="data",
            difficulty=3,
            content="막대그래프에서 세로축의 눈금 한 칸이 5명을 나타낼 때, 막대가 눈금 3칸이면 ____명입니다.",
            answer="15",
            explanation="눈금 한 칸이 5명이므로 3칸 = 5 × 3 = 15명입니다.",
            points=10,
            accept_formats=["15"],
        ),
        fb(
            id="e4-fb-010",
            concept_id="concept-e4-bar-graph",
            category="concept",
            part="data",
            difficulty=5,
            content="막대그래프에서 눈금 한 칸이 2명을 나타냅니다. 어떤 항목의 막대가 눈금 7칸이면 그 항목은 ____명입니다.",
            answer="14",
            explanation="눈금 한 칸이 2명이므로 7칸 = 2 × 7 = 14명입니다.",
            points=10,
            accept_formats=["14"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 6단원: 규칙 찾기
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e4-fb-011",
            concept_id="concept-e4-pattern",
            category="concept",
            part="algebra",
            difficulty=2,
            content="3, 6, 9, 12, ____",
            answer="15",
            explanation="3씩 커지는 규칙입니다. 12 + 3 = 15입니다.",
            points=10,
            accept_formats=["15"],
        ),
        fb(
            id="e4-fb-012",
            concept_id="concept-e4-pattern",
            category="concept",
            part="algebra",
            difficulty=8,
            content="1, 4, 9, 16, ____",
            answer="25",
            explanation="1=1², 4=2², 9=3², 16=4²이므로 다음은 5²=25입니다. 제곱수의 규칙입니다.",
            points=10,
            accept_formats=["25"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 1단원: 분수의 덧셈과 뺄셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e4-fb-013",
            concept_id="concept-e4-frac-op",
            category="computation",
            part="calc",
            difficulty=3,
            content="5/7 - 2/7 = ____",
            answer="3/7",
            explanation="분모가 같은 분수의 뺄셈은 분자끼리 뺍니다. 5/7 - 2/7 = 3/7입니다.",
            points=10,
            accept_formats=["3/7"],
        ),
        fb(
            id="e4-fb-014",
            concept_id="concept-e4-frac-op",
            category="computation",
            part="calc",
            difficulty=7,
            content="3 2/7 - 1 5/7 = ____",
            answer="1 4/7",
            explanation="2/7에서 5/7을 뺄 수 없으므로 3 2/7을 2 9/7로 바꿉니다. 2 9/7 - 1 5/7 = 1 4/7입니다.",
            points=10,
            accept_formats=["1 4/7", "11/7"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 2단원: 삼각형
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e4-fb-015",
            concept_id="concept-e4-triangle",
            category="concept",
            part="geo",
            difficulty=3,
            content="정삼각형의 한 각의 크기는 ____도입니다.",
            answer="60",
            explanation="정삼각형은 세 각의 크기가 모두 같습니다. 180 ÷ 3 = 60이므로 한 각은 60도입니다.",
            points=10,
            accept_formats=["60"],
        ),
        fb(
            id="e4-fb-016",
            concept_id="concept-e4-triangle",
            category="concept",
            part="geo",
            difficulty=7,
            content="이등변삼각형의 꼭지각이 40도일 때, 밑각의 크기는 ____도입니다.",
            answer="70",
            explanation="이등변삼각형의 두 밑각의 크기는 같습니다. (180 - 40) ÷ 2 = 70이므로 밑각은 70도입니다.",
            points=10,
            accept_formats=["70"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 3단원: 소수의 덧셈과 뺄셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e4-fb-017",
            concept_id="concept-e4-dec-op",
            category="computation",
            part="calc",
            difficulty=3,
            content="0.7 + 0.6 = ____",
            answer="1.3",
            explanation="0.7 + 0.6 = 1.3입니다. 소수 첫째 자리끼리 더하면 7+6=13이므로 1.3입니다.",
            points=10,
            accept_formats=["1.3"],
        ),
        fb(
            id="e4-fb-018",
            concept_id="concept-e4-dec-op",
            category="computation",
            part="calc",
            difficulty=7,
            content="3.5 - 1.28 = ____",
            answer="2.22",
            explanation="소수점을 맞추어 3.50 - 1.28 = 2.22입니다. 3.5를 3.50으로 바꾸어 자릿수를 맞추는 것이 핵심입니다.",
            points=10,
            accept_formats=["2.22"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 4단원: 사각형
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e4-fb-019",
            concept_id="concept-e4-quad",
            category="concept",
            part="geo",
            difficulty=3,
            content="사각형의 네 각의 크기의 합은 ____도입니다.",
            answer="360",
            explanation="사각형의 네 각의 크기의 합은 항상 360도입니다.",
            points=10,
            accept_formats=["360"],
        ),
        fb(
            id="e4-fb-020",
            concept_id="concept-e4-quad",
            category="concept",
            part="geo",
            difficulty=5,
            content="네 변의 길이가 모두 같은 사각형을 ____이라고 합니다.",
            answer="마름모",
            explanation="네 변의 길이가 모두 같은 사각형을 마름모라고 합니다. (네 각이 모두 직각이면 정사각형)",
            points=10,
            accept_formats=["마름모"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 5단원: 꺾은선그래프
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e4-fb-021",
            concept_id="concept-e4-line-graph",
            category="concept",
            part="data",
            difficulty=2,
            content="꺾은선그래프에서 선분이 오른쪽 위로 향하면 값이 ____하고 있다는 뜻입니다.",
            answer="증가",
            explanation="꺾은선그래프에서 선분이 위로 향하면 시간이 지남에 따라 값이 증가하고 있다는 뜻입니다.",
            points=10,
            accept_formats=["증가", "커지고", "늘어나고"],
        ),
        fb(
            id="e4-fb-022",
            concept_id="concept-e4-line-graph",
            category="concept",
            part="data",
            difficulty=4,
            content="시간에 따른 기온의 변화를 나타내기에 적합한 그래프는 ____그래프입니다.",
            answer="꺾은선",
            explanation="시간에 따른 연속적 변화를 나타내기에는 꺾은선그래프가 적합합니다.",
            points=10,
            accept_formats=["꺾은선"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 6단원: 다각형
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e4-fb-023",
            concept_id="concept-e4-polygon",
            category="concept",
            part="geo",
            difficulty=2,
            content="선분으로만 둘러싸인 닫힌 도형을 ____이라고 합니다.",
            answer="다각형",
            explanation="선분으로만 둘러싸인 닫힌 도형을 다각형이라고 합니다.",
            points=10,
            accept_formats=["다각형"],
        ),
        fb(
            id="e4-fb-024",
            concept_id="concept-e4-polygon",
            category="concept",
            part="geo",
            difficulty=6,
            content="오각형의 대각선의 수는 ____개입니다.",
            answer="5",
            explanation="대각선의 수 = n(n-3)/2입니다. 오각형(n=5): 5×(5-3)/2 = 5×2/2 = 5개입니다.",
            points=10,
            accept_formats=["5"],
        ),
    ]
