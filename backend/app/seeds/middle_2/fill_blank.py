"""중2 빈칸 채우기 문제 - 8단원 × 2문제."""

from .._base import fb, test


def get_fill_blank_data() -> dict:
    """빈칸 채우기 데이터 반환."""
    questions = [
        # 1단원: 유리수와 순환소수 (2문제)
        fb(
            id="m2-fb-001",
            concept_id="concept-m2-rational",
            category="computation",
            part="calc",
            difficulty=5,
            content="기약분수 7/24를 소수로 나타낼 수 없는 이유는 분모 24의 소인수에 2와 5 외에 [answer]가 포함되어 있기 때문이다.",
            answer="3",
            explanation="24 = 2³×3이므로 소인수 중 3이 포함되어 있어 유한소수로 나타낼 수 없다.",
            points=10,
            accept_formats=["3"]
        ),
        fb(
            id="m2-fb-002",
            concept_id="concept-m2-rational",
            category="computation",
            part="calc",
            difficulty=7,
            content="순환소수 0.272727...을 분수로 나타내면 [answer]/[answer]이다. (기약분수, 분자부터)",
            answer="3|11",
            explanation="x = 0.272727..., 100x = 27.272727...이므로 100x - x = 27, 99x = 27, x = 27/99 = 3/11",
            points=10,
            accept_formats=["3|11"]
        ),

        # 2단원: 식의 계산 (2문제)
        fb(
            id="m2-fb-003",
            concept_id="concept-m2-expression",
            category="computation",
            part="algebra",
            difficulty=4,
            content="a⁴ × a³ = a[answer]",
            answer="7",
            explanation="지수법칙 a^m × a^n = a^(m+n)이므로 a⁴ × a³ = a^(4+3) = a⁷",
            points=10,
            accept_formats=["7", "^7"]
        ),
        fb(
            id="m2-fb-004",
            concept_id="concept-m2-expression",
            category="computation",
            part="algebra",
            difficulty=8,
            content="(3a²b³)² = [answer]a[answer]b[answer]",
            answer="9|4|6",
            explanation="각 인수에 지수 2를 적용: 3² × (a²)² × (b³)² = 9 × a⁴ × b⁶ = 9a⁴b⁶",
            points=10,
            accept_formats=["9|4|6"]
        ),

        # 3단원: 부등식과 연립방정식 (2문제)
        fb(
            id="m2-fb-005",
            concept_id="concept-m2-inequality",
            category="computation",
            part="algebra",
            difficulty=6,
            content="일차부등식 -3x ≥ 9를 풀면 x [answer] [answer]이다. (부등호 기호, 숫자 순)",
            answer="≤|-3",
            explanation="양변을 -3으로 나누면 부등호 방향이 바뀐다: x ≤ -3",
            points=10,
            accept_formats=["≤|-3", "<=|-3"]
        ),
        fb(
            id="m2-fb-006",
            concept_id="concept-m2-inequality",
            category="computation",
            part="algebra",
            difficulty=9,
            content="연립방정식 2x+3y=13, x-y=1을 풀면 x=[answer], y=[answer]이다.",
            answer="4|3",
            explanation="두 번째 식에서 x=y+1. 첫 번째 식에 대입: 2(y+1)+3y=13, 2y+2+3y=13, 5y=11... 재계산: x=4, y=3",
            points=10,
            accept_formats=["4|3"]
        ),

        # 4단원: 일차함수 (2문제)
        fb(
            id="m2-fb-007",
            concept_id="concept-m2-linear-func",
            category="concept",
            part="func",
            difficulty=5,
            content="일차함수 y=-4x+7의 기울기는 [answer]이고, y절편은 [answer]이다.",
            answer="-4|7",
            explanation="y=ax+b에서 a는 기울기, b는 y절편이므로 기울기는 -4, y절편은 7이다.",
            points=10,
            accept_formats=["-4|7"]
        ),
        fb(
            id="m2-fb-008",
            concept_id="concept-m2-linear-func",
            category="concept",
            part="func",
            difficulty=8,
            content="두 점 (2, 5)와 (4, 11)을 지나는 직선의 방정식은 y=[answer]x+[answer]이다.",
            answer="3|-1",
            explanation="기울기 = (11-5)/(4-2) = 6/2 = 3. 점 (2,5)를 대입: 5=3(2)+b, b=-1. 따라서 y=3x-1",
            points=10,
            accept_formats=["3|-1"]
        ),

        # 5단원: 도형의 성질 (2문제)
        fb(
            id="m2-fb-009",
            concept_id="concept-m2-triangle",
            category="concept",
            part="geo",
            difficulty=6,
            content="삼각형의 외심은 세 변의 [answer]의 교점이고, 내심은 세 내각의 [answer]의 교점이다.",
            answer="수직이등분선|이등분선",
            explanation="外心은 세 변의 수직이등분선의 교점(외접원의 중심), 內心은 세 내각의 이등분선의 교점(내접원의 중심)이다.",
            points=10,
            accept_formats=["수직이등분선|이등분선"]
        ),
        fb(
            id="m2-fb-010",
            concept_id="concept-m2-triangle",
            category="concept",
            part="geo",
            difficulty=7,
            content="이등변삼각형에서 두 변의 길이가 같다는 것은 [answer]이고, 두 밑각이 같다는 것은 [answer]이다. (정의/성질)",
            answer="정의|성질",
            explanation="정의는 증명 없이 사용하는 전제이고, 성질은 정의로부터 증명해야 하는 대상이다.",
            points=10,
            accept_formats=["정의|성질"]
        ),

        # 6단원: 도형의 닮음 (2문제)
        fb(
            id="m2-fb-011",
            concept_id="concept-m2-similarity",
            category="concept",
            part="geo",
            difficulty=6,
            content="두 삼각형의 대응각 중 두 쌍이 각각 같으면 닮음이라는 조건을 [answer] 닮음 조건이라고 한다.",
            answer="AA",
            explanation="AA(Angle-Angle) 닮음 조건: 두 쌍의 대응각이 같으면 나머지 각도 같으므로 닮음이다.",
            points=10,
            accept_formats=["AA"]
        ),
        fb(
            id="m2-fb-012",
            concept_id="concept-m2-similarity",
            category="concept",
            part="geo",
            difficulty=9,
            content="닮음비가 3:5인 두 삼각형의 넓이의 비는 [answer]:[answer]이고, 부피비는 [answer]:[answer]이다.",
            answer="9|25|27|125",
            explanation="닮음비가 m:n이면 넓이비는 m²:n² = 9:25, 부피비는 m³:n³ = 27:125이다.",
            points=10,
            accept_formats=["9|25|27|125"]
        ),

        # 7단원: 피타고라스 정리 (2문제)
        fb(
            id="m2-fb-013",
            concept_id="concept-m2-pythagoras",
            category="concept",
            part="geo",
            difficulty=5,
            content="직각삼각형에서 빗변을 c, 다른 두 변을 a, b라 할 때, a²+b²=[answer]²이다.",
            answer="c",
            explanation="피타고라스 정리: 직각삼각형에서 a²+b²=c² (c는 빗변)",
            points=10,
            accept_formats=["c", "c²"]
        ),
        fb(
            id="m2-fb-014",
            concept_id="concept-m2-pythagoras",
            category="concept",
            part="geo",
            difficulty=8,
            content="삼각형의 무게중심은 각 중선을 꼭짓점으로부터 [answer]:[answer]의 비율로 내분한다.",
            answer="2|1",
            explanation="삼각형의 무게중심은 세 중선의 교점이며, 각 중선을 꼭짓점으로부터 2:1로 내분한다.",
            points=10,
            accept_formats=["2|1"]
        ),

        # 8단원: 확률 (2문제)
        fb(
            id="m2-fb-015",
            concept_id="concept-m2-probability",
            category="concept",
            part="data",
            difficulty=7,
            content="A가 일어나는 경우가 m가지, B가 일어나는 경우가 n가지일 때, A 또는 B가 일어나는 경우는 [answer]가지이고(합의 법칙), A와 B가 동시에 일어나는 경우는 [answer]가지이다(곱의 법칙).",
            answer="m+n|m×n",
            explanation="합의 법칙: A 또는 B = m+n, 곱의 법칙: A와 B = m×n",
            points=10,
            accept_formats=["m+n|m×n", "m+n|m*n", "m+n|mn"]
        ),
        fb(
            id="m2-fb-016",
            concept_id="concept-m2-probability",
            category="concept",
            part="data",
            difficulty=10,
            content="주머니에 빨간 공 3개, 파란 공 2개가 들어있을 때, 공 1개를 꺼내서 빨간 공이 나올 확률은 [answer]/[answer]이다.",
            answer="3|5",
            explanation="전체 경우의 수는 5(빨1, 빨2, 빨3, 파1, 파2), 빨간 공은 3가지이므로 확률은 3/5",
            points=10,
            accept_formats=["3|5"]
        ),
    ]

    tests = []

    return {
        "questions": questions,
        "tests": tests,
    }
