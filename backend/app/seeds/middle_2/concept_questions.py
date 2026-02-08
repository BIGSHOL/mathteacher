"""중2 개념 카테고리 시드 데이터 - 2022 개정 교육과정.

4단원: 일차함수
5-1단원: 삼각형의 성질
5-2단원: 사각형의 성질
6단원: 도형의 닮음
7단원: 피타고라스 정리
8단원: 확률
"""

from .._base import mc, concept, test


def get_concept_data() -> dict:
    """개념 카테고리 데이터 반환."""
    concepts = [
        # ── 4단원: 일차함수 (2개) ──
        concept(
            id="concept-m2-linfn-01",
            name="일차함수의 그래프",
            grade="middle_2",
            category="concept",
            part="func",
            description="y=ax+b(a≠0), 기울기(a)=Δy/Δx, y절편(b), 기울기의 부호·절댓값에 따른 그래프 변화, 상수함수와의 차이",
        ),
        concept(
            id="concept-m2-linfn-02",
            name="일차함수와 일차방정식의 관계",
            grade="middle_2",
            category="concept",
            part="func",
            description="ax+by+c=0의 그래프는 직선, 두 점을 지나는 직선의 방정식 구하기, x=k(세로선)는 함수가 아님, 연립방정식의 해와 교점",
        ),
        # ── 5-1단원: 삼각형의 성질 (2개) ──
        concept(
            id="concept-m2-tri-01",
            name="이등변삼각형과 직각삼각형",
            grade="middle_2",
            category="concept",
            part="geo",
            description="이등변삼각형의 정의(두 변 같음)와 성질(두 밑각 같음), 정의와 성질의 구분, 직각삼각형의 합동 조건",
        ),
        concept(
            id="concept-m2-tri-02",
            name="삼각형의 외심과 내심",
            grade="middle_2",
            category="concept",
            part="geo",
            description="외심: 세 변의 수직이등분선 교점(외접원 중심), 내심: 세 내각의 이등분선 교점(내접원 중심), 예각/직각/둔각삼각형에서 외심의 위치",
        ),
        # ── 5-2단원: 사각형의 성질 (2개) ──
        concept(
            id="concept-m2-quad-01",
            name="평행사변형의 성질과 조건",
            grade="middle_2",
            category="concept",
            part="geo",
            description="평행사변형의 정의·성질(대변·대각·대각선), 평행사변형이 되기 위한 조건 5가지",
        ),
        concept(
            id="concept-m2-quad-02",
            name="특수 사각형의 관계",
            grade="middle_2",
            category="concept",
            part="geo",
            description="직사각형·마름모·정사각형의 정의와 성질, 사각형 계통도(포함 관계), 정의 vs 성질 구분",
        ),
        # ── 6단원: 도형의 닮음 (2개) ──
        concept(
            id="concept-m2-simil-01",
            name="닮음의 조건",
            grade="middle_2",
            category="concept",
            part="geo",
            description="SSS·SAS·AA 닮음 조건, 대응변과 대응각 찾기, 평행선과 선분의 비",
        ),
        concept(
            id="concept-m2-simil-02",
            name="닮음비와 넓이비·부피비",
            grade="middle_2",
            category="concept",
            part="geo",
            description="닮음비 m:n → 넓이비 m²:n² → 부피비 m³:n³, 축소·확대 계산, 축도와 실제 크기",
        ),
        # ── 7단원: 피타고라스 정리 (2개) ──
        concept(
            id="concept-m2-pytha-01",
            name="피타고라스 정리와 증명",
            grade="middle_2",
            category="concept",
            part="geo",
            description="a²+b²=c²(c는 빗변), 다양한 증명 방법, 피타고라스 정리의 역(직각삼각형 판별), 피타고라스 수(3-4-5, 5-12-13)",
        ),
        concept(
            id="concept-m2-pytha-02",
            name="피타고라스 정리의 활용과 무게중심",
            grade="middle_2",
            category="concept",
            part="geo",
            description="좌표평면에서 두 점 사이 거리, 특수 직각삼각형(1:1:√2, 1:√3:2), 삼각형의 무게중심(중선을 2:1로 내분)",
        ),
        # ── 8단원: 확률 (2개) ──
        concept(
            id="concept-m2-prob-01",
            name="경우의 수",
            grade="middle_2",
            category="concept",
            part="data",
            description="합의 법칙(A 또는 B), 곱의 법칙(A 그리고 B), 사건의 배타성, 수형도·표를 이용한 경우의 수",
        ),
        concept(
            id="concept-m2-prob-02",
            name="확률의 계산과 성질",
            grade="middle_2",
            category="concept",
            part="data",
            description="수학적 확률 P(A)=n(A)/n(S), 근원사건의 동등성, 여사건 P(A')=1-P(A), 복원/비복원 추출 구별",
        ),
    ]

    # ── 일차함수 (3문제) ──
    func_questions = [
        mc(
            id="m2-2-1-01-lv02-cc-001",
            concept_id="concept-m2-linfn-01",
            category="concept",
            part="func",
            difficulty=2,
            content="일차함수 y=2x+3의 기울기는?",
            options=["2", "3", "-2", "5"],
            correct="A",
            explanation="y=ax+b에서 a가 기울기이므로 2이다.",
            points=10,
        ),
        mc(
            id="m2-2-1-01-lv05-cc-001",
            concept_id="concept-m2-linfn-01",
            category="concept",
            part="func",
            difficulty=5,
            content="일차함수 y=-3x+5와 y=-5x+7 중 어느 그래프가 더 가파른가?",
            options=["y=-5x+7", "y=-3x+5", "둘 다 같다", "비교할 수 없다"],
            correct="A",
            explanation="가파른 정도는 기울기의 절댓값으로 결정된다. |-5|=5 > |-3|=3이므로 y=-5x+7이 더 가파르다.",
            points=10,
        ),
        mc(
            id="m2-2-1-02-lv07-cc-001",
            concept_id="concept-m2-linfn-02",
            category="concept",
            part="func",
            difficulty=7,
            content="두 점 (1, 4)와 (3, 10)을 지나는 직선의 방정식은?",
            options=["y=3x+1", "y=2x+2", "y=3x-1", "y=2x+3"],
            correct="A",
            explanation="기울기 = (10-4)/(3-1) = 6/2 = 3. 점 (1,4)를 대입하면 4=3(1)+b, b=1. 따라서 y=3x+1",
            points=10,
        ),
    ]

    # ── 삼각형의 성질 (3문제) ──
    triangle_questions = [
        mc(
            id="m2-2-2-01-lv03-cc-001",
            concept_id="concept-m2-tri-01",
            category="concept",
            part="geo",
            difficulty=3,
            content="이등변삼각형에서 '두 밑각의 크기가 같다'는 것은 정의인가, 성질인가?",
            options=["성질", "정의", "공리", "정리"],
            correct="A",
            explanation="이등변삼각형의 정의는 '두 변의 길이가 같은 삼각형'이다. '두 밑각의 크기가 같다'는 정의로부터 증명되는 성질이다.",
            points=10,
        ),
        mc(
            id="m2-2-2-02-lv06-cc-001",
            concept_id="concept-m2-tri-02",
            category="concept",
            part="geo",
            difficulty=6,
            content="삼각형의 외심은 무엇의 교점인가?",
            options=["세 변의 수직이등분선", "세 내각의 이등분선", "세 중선", "세 높이"],
            correct="A",
            explanation="外心(바깥 원)은 외접원의 중심이며, 세 변의 수직이등분선이 만나는 점이다. 세 꼭짓점까지의 거리가 같다.",
            points=10,
        ),
        mc(
            id="m2-2-2-02-lv08-cc-001",
            concept_id="concept-m2-tri-02",
            category="concept",
            part="geo",
            difficulty=8,
            content="둔각삼각형의 외심은 어디에 위치하는가?",
            options=["삼각형의 외부", "삼각형의 내부", "빗변 위", "꼭짓점 위"],
            correct="A",
            explanation="예각삼각형의 외심은 내부, 직각삼각형의 외심은 빗변의 중점, 둔각삼각형의 외심은 삼각형 외부에 위치한다.",
            points=10,
        ),
    ]

    # ── 사각형의 성질 (3문제) ──
    quadrilateral_questions = [
        mc(
            id="m2-2-3-01-lv03-cc-001",
            concept_id="concept-m2-quad-01",
            category="concept",
            part="geo",
            difficulty=3,
            content="직사각형의 정의로 올바른 것은?",
            options=["네 각이 모두 직각인 사각형", "대각선의 길이가 같은 사각형", "두 쌍의 대변이 평행한 사각형", "네 변의 길이가 같은 사각형"],
            correct="A",
            explanation="직사각형의 정의는 '네 각이 모두 직각인 사각형'이다. '대각선의 길이가 같다'는 성질(증명 대상)이다.",
            points=10,
        ),
        mc(
            id="m2-2-3-02-lv06-cc-001",
            concept_id="concept-m2-quad-02",
            category="concept",
            part="geo",
            difficulty=6,
            content="평행사변형, 직사각형, 정사각형의 포함 관계로 올바른 것은?",
            options=["정사각형 ⊂ 직사각형 ⊂ 평행사변형", "직사각형 ⊂ 정사각형 ⊂ 평행사변형", "평행사변형 ⊂ 직사각형 ⊂ 정사각형", "정사각형 ⊂ 평행사변형 ⊂ 직사각형"],
            correct="A",
            explanation="정사각형은 직사각형이면서 마름모이고, 직사각형은 평행사변형의 특수한 경우이다.",
            points=10,
        ),
        mc(
            id="m2-2-3-01-lv08-cc-001",
            concept_id="concept-m2-quad-01",
            category="concept",
            part="geo",
            difficulty=8,
            content="평행사변형의 성질이 아닌 것은?",
            options=["대각선의 길이가 같다", "대각의 크기가 같다", "대변의 길이가 같다", "대각선이 서로를 이등분한다"],
            correct="A",
            explanation="'대각선의 길이가 같다'는 직사각형의 성질이다. 일반 평행사변형에서는 대각선의 길이가 같지 않을 수 있다.",
            points=10,
        ),
    ]

    # ── 도형의 닮음 (3문제) ──
    similarity_questions = [
        mc(
            id="m2-2-4-01-lv04-cc-001",
            concept_id="concept-m2-simil-01",
            category="concept",
            part="geo",
            difficulty=4,
            content="두 삼각형이 AA 닮음 조건을 만족하려면?",
            options=["두 쌍의 대응각이 각각 같다", "세 쌍의 대응각이 모두 같다", "두 쌍의 대응변의 비가 같다", "세 쌍의 대응변의 비가 같다"],
            correct="A",
            explanation="AA 닮음: 두 쌍의 대응각이 같으면 나머지 한 각도 자동으로 같으므로 닮음이다.",
            points=10,
        ),
        mc(
            id="m2-2-4-02-lv07-cc-001",
            concept_id="concept-m2-simil-02",
            category="concept",
            part="geo",
            difficulty=7,
            content="닮음비가 2:3인 두 삼각형의 넓이의 비는?",
            options=["4:9", "2:3", "8:27", "4:6"],
            correct="A",
            explanation="닮음비가 m:n이면 넓이비는 m²:n²이다. 따라서 2²:3² = 4:9",
            points=10,
        ),
        mc(
            id="m2-2-4-02-lv09-cc-001",
            concept_id="concept-m2-simil-02",
            category="concept",
            part="geo",
            difficulty=9,
            content="닮음비가 1:2인 두 정육면체의 부피의 비는?",
            options=["1:8", "1:4", "1:2", "1:6"],
            correct="A",
            explanation="닮음비가 m:n이면 부피비는 m³:n³이다. 따라서 1³:2³ = 1:8",
            points=10,
        ),
    ]

    # ── 피타고라스 정리 (3문제) ──
    pythagoras_questions = [
        mc(
            id="m2-2-5-01-lv03-cc-001",
            concept_id="concept-m2-pytha-01",
            category="concept",
            part="geo",
            difficulty=3,
            content="직각삼각형에서 빗변의 길이가 5, 한 변의 길이가 3일 때, 나머지 한 변의 길이는?",
            options=["4", "3", "5", "6"],
            correct="A",
            explanation="피타고라스 정리: a²+b²=c²에서 3²+b²=5², 9+b²=25, b²=16, b=4 (피타고라스 수 3-4-5)",
            points=10,
        ),
        mc(
            id="m2-2-5-02-lv06-cc-001",
            concept_id="concept-m2-pytha-02",
            category="concept",
            part="geo",
            difficulty=6,
            content="삼각형의 무게중심은 각 중선을 어떤 비율로 내분하는가?",
            options=["2:1", "1:1", "3:1", "1:2"],
            correct="A",
            explanation="삼각형의 무게중심은 세 중선의 교점이며, 각 중선을 꼭짓점으로부터 2:1로 내분한다.",
            points=10,
        ),
        mc(
            id="m2-2-5-01-lv08-cc-001",
            concept_id="concept-m2-pytha-01",
            category="concept",
            part="geo",
            difficulty=8,
            content="세 변의 길이가 5, 12, 13인 삼각형은?",
            options=["직각삼각형", "예각삼각형", "둔각삼각형", "정삼각형"],
            correct="A",
            explanation="5²+12²=25+144=169=13²이므로 피타고라스 정리의 역에 의해 직각삼각형이다.",
            points=10,
        ),
    ]

    # ── 확률 (3문제) ──
    probability_questions = [
        mc(
            id="m2-2-6-02-lv04-cc-001",
            concept_id="concept-m2-prob-02",
            category="concept",
            part="data",
            difficulty=4,
            content="주사위 1개를 던질 때 짝수가 나올 확률은?",
            options=["1/2", "1/3", "2/3", "1/6"],
            correct="A",
            explanation="짝수는 2, 4, 6으로 3가지이고, 전체 경우의 수는 6이므로 확률은 3/6 = 1/2",
            points=10,
        ),
        mc(
            id="m2-2-6-02-lv07-cc-001",
            concept_id="concept-m2-prob-02",
            category="concept",
            part="data",
            difficulty=7,
            content="흰 공 2개와 검은 공 1개가 들어있는 주머니에서 공 1개를 꺼낼 때, 흰 공이 나올 확률은?",
            options=["2/3", "1/2", "1/3", "3/4"],
            correct="A",
            explanation="흰 공 2개를 흰1, 흰2로 구분해야 근원사건의 동등성이 보장된다. 전체 3, 흰 공 2이므로 2/3",
            points=10,
        ),
        mc(
            id="m2-2-6-01-lv10-cc-001",
            concept_id="concept-m2-prob-01",
            category="concept",
            part="data",
            difficulty=10,
            content="주사위 2개를 동시에 던질 때, 두 눈의 수의 합이 7이 될 확률은?",
            options=["1/6", "1/12", "1/9", "1/7"],
            correct="A",
            explanation="전체 경우의 수는 6×6=36. 합이 7인 경우는 (1,6), (2,5), (3,4), (4,3), (5,2), (6,1)로 6가지. 6/36 = 1/6",
            points=10,
        ),
    ]

    # ── 1~3단원 개념 문제 (유리수와 순환소수, 식의 계산, 일차부등식, 연립방정식) ──
    ch1_concept_questions = [
        # 유리수와 순환소수 (3문제)
        mc(
            id="m2-1-1-01-lv03-cc-001",
            concept_id="concept-m2-rational-01",
            category="concept",
            part="calc",
            difficulty=3,
            content="다음 중 유한소수로 나타낼 수 있는 분수의 조건은?",
            options=[
                "기약분수의 분모의 소인수가 2와 5뿐인 분수",
                "분자가 짝수인 분수",
                "분모가 10의 배수인 분수",
                "분자가 분모보다 작은 분수",
            ],
            correct="A",
            explanation="기약분수로 나타냈을 때 분모의 소인수가 2와 5뿐이면 유한소수로 나타낼 수 있습니다. 예: 3/20 → 20 = 2² × 5이므로 유한소수(0.15)",
            points=10,
        ),
        mc(
            id="m2-1-1-02-lv05-cc-001",
            concept_id="concept-m2-rational-02",
            category="concept",
            part="calc",
            difficulty=5,
            content="순환소수 0.272727...의 순환마디는?",
            options=["27", "2", "7", "272"],
            correct="A",
            explanation="순환마디는 소수점 아래에서 반복되는 숫자의 묶음입니다. 0.272727...에서 '27'이 반복되므로 순환마디는 27입니다.",
            points=10,
        ),
        mc(
            id="m2-1-1-02-lv07-cc-001",
            concept_id="concept-m2-rational-02",
            category="concept",
            part="calc",
            difficulty=7,
            content="다음 중 순환소수에 대한 설명으로 옳은 것은?",
            options=[
                "모든 순환소수는 유리수이다",
                "모든 순환소수는 무리수이다",
                "순환소수는 분수로 나타낼 수 없다",
                "순환소수는 항상 정수이다",
            ],
            correct="A",
            explanation="순환소수는 분수로 나타낼 수 있으므로 유리수입니다. 예: 0.333... = 1/3. 무리수는 순환하지 않는 무한소수(π, √2 등)입니다.",
            points=15,
        ),
        # 식의 계산 (3문제)
        mc(
            id="m2-1-2-01-lv03-cc-001",
            concept_id="concept-m2-expr-01",
            category="concept",
            part="algebra",
            difficulty=3,
            content="지수법칙 aᵐ × aⁿ = aᵐ⁺ⁿ이 성립하는 이유는?",
            options=[
                "a를 m번 곱한 것에 n번 더 곱하면 총 (m+n)번이므로",
                "지수끼리 곱하면 되므로",
                "밑끼리 더하면 되므로",
                "지수를 빼야 하므로",
            ],
            correct="A",
            explanation="aᵐ × aⁿ = (a × a × ... m번) × (a × a × ... n번) = a × a × ... (m+n)번 = aᵐ⁺ⁿ. 곱셈의 반복이라는 거듭제곱의 정의에서 자연스럽게 유도됩니다.",
            points=10,
        ),
        mc(
            id="m2-1-2-02-lv05-cc-001",
            concept_id="concept-m2-expr-02",
            category="concept",
            part="algebra",
            difficulty=5,
            content="다음 중 단항식인 것은?",
            options=["3x²y", "3x + 2", "x² + y²", "x + y + 1"],
            correct="A",
            explanation="단항식은 수와 문자의 곱으로만 이루어진 식입니다. 덧셈이나 뺄셈이 포함되면 다항식입니다. 3x²y는 3 × x² × y로 곱으로만 이루어져 있으므로 단항식입니다.",
            points=10,
        ),
        mc(
            id="m2-1-2-02-lv07-cc-001",
            concept_id="concept-m2-expr-02",
            category="concept",
            part="algebra",
            difficulty=7,
            content="다항식 3x² - 5x + 2의 차수는?",
            options=["2", "3", "-5", "0"],
            correct="A",
            explanation="다항식의 차수는 각 항에서 가장 높은 문자의 지수입니다. 3x²의 차수가 2, -5x의 차수가 1, 2의 차수가 0이므로 최고 차수는 2입니다.",
            points=15,
        ),
        # 일차부등식 (3문제)
        mc(
            id="m2-1-3-01-lv03-cc-001",
            concept_id="concept-m2-ineq-01",
            category="concept",
            part="algebra",
            difficulty=3,
            content="부등식의 양변에 음수를 곱하면 부등호의 방향은?",
            options=["반대로 바뀐다", "그대로 유지된다", "등호가 된다", "부등식이 성립하지 않는다"],
            correct="A",
            explanation="부등식의 양변에 음수를 곱하거나 음수로 나누면 부등호의 방향이 반대로 바뀝니다. 예: 2 < 3에서 양변에 -1을 곱하면 -2 > -3",
            points=10,
        ),
        mc(
            id="m2-1-3-01-lv05-cc-001",
            concept_id="concept-m2-ineq-01",
            category="concept",
            part="algebra",
            difficulty=5,
            content="부등식 x < 3의 해를 수직선에 나타낼 때, x = 3인 점은?",
            options=[
                "빈 원(○)으로 표시 (포함하지 않음)",
                "채운 원(●)으로 표시 (포함)",
                "표시하지 않음",
                "화살표로 표시",
            ],
            correct="A",
            explanation="부등호가 <, >이면 경계값을 포함하지 않으므로 빈 원(○)으로, ≤, ≥이면 포함하므로 채운 원(●)으로 표시합니다.",
            points=10,
        ),
        mc(
            id="m2-1-3-02-lv07-cc-001",
            concept_id="concept-m2-ineq-02",
            category="concept",
            part="algebra",
            difficulty=7,
            content="방정식과 부등식의 차이점으로 올바른 것은?",
            options=[
                "방정식의 해는 특정 값이고, 부등식의 해는 범위이다",
                "둘 다 해가 하나뿐이다",
                "방정식에만 미지수가 있다",
                "부등식은 풀 수 없다",
            ],
            correct="A",
            explanation="방정식의 해는 등식을 만족하는 특정 값이지만, 부등식의 해는 부등호를 만족하는 값들의 범위입니다. 예: x + 1 = 3 → x = 2, x + 1 < 3 → x < 2",
            points=15,
        ),
        # 연립일차방정식 (3문제)
        mc(
            id="m2-1-4-01-lv04-cc-001",
            concept_id="concept-m2-simul-01",
            category="concept",
            part="algebra",
            difficulty=4,
            content="연립방정식의 해는 기하학적으로 무엇을 의미하는가?",
            options=["두 직선의 교점", "두 직선의 기울기", "한 직선의 y절편", "두 직선 사이의 거리"],
            correct="A",
            explanation="연립방정식의 각 식은 좌표평면에서 직선을 나타냅니다. 연립방정식의 해는 두 직선이 만나는 교점의 좌표입니다.",
            points=10,
        ),
        mc(
            id="m2-1-4-02-lv06-cc-001",
            concept_id="concept-m2-simul-02",
            category="concept",
            part="algebra",
            difficulty=6,
            content="연립방정식의 두 식이 나타내는 직선이 평행할 때, 해의 상태는?",
            options=["해가 없다 (불능)", "해가 무수히 많다 (부정)", "해가 하나이다", "해가 두 개이다"],
            correct="A",
            explanation="두 직선이 평행하면 교점이 없으므로 해가 없습니다(불능). 두 직선이 일치하면 해가 무수히 많습니다(부정). 한 점에서 만나면 해가 하나입니다.",
            points=10,
        ),
        mc(
            id="m2-1-4-01-lv08-cc-001",
            concept_id="concept-m2-simul-01",
            category="concept",
            part="algebra",
            difficulty=8,
            content="연립방정식을 풀 때 대입법이 유리한 경우는?",
            options=[
                "한 식이 y = ax + b 형태로 정리되어 있을 때",
                "두 식의 계수가 같을 때",
                "미지수가 3개 이상일 때",
                "상수항이 0일 때",
            ],
            correct="A",
            explanation="한 식이 y = ax + b처럼 한 미지수에 대해 정리되어 있으면 바로 다른 식에 대입할 수 있어 대입법이 편리합니다. 계수가 같은 경우에는 가감법이 더 유리합니다.",
            points=15,
        ),
    ]

    questions = (
        func_questions + triangle_questions + quadrilateral_questions
        + similarity_questions + pythagoras_questions + probability_questions
        + ch1_concept_questions
    )

    tests = [
        test(
            id="test-m2-function",
            title="중2 일차함수 테스트",
            description="기울기, 절편, 일차함수와 일차방정식",
            grade="middle_2",
            concept_ids=["concept-m2-linfn-01", "concept-m2-linfn-02"],
            question_ids=[q["id"] for q in func_questions],
            time_limit_minutes=10,
        ),
        test(
            id="test-m2-geometry",
            title="중2 도형 종합 테스트",
            description="삼각형의 성질, 사각형의 성질, 닮음, 피타고라스 정리",
            grade="middle_2",
            concept_ids=["concept-m2-tri-01", "concept-m2-tri-02", "concept-m2-quad-01", "concept-m2-quad-02", "concept-m2-simil-01", "concept-m2-simil-02", "concept-m2-pytha-01", "concept-m2-pytha-02"],
            question_ids=[q["id"] for q in triangle_questions + quadrilateral_questions + similarity_questions + pythagoras_questions],
            time_limit_minutes=25,
            use_question_pool=True,
            questions_per_attempt=8,
        ),
        test(
            id="test-m2-probability",
            title="중2 확률 테스트",
            description="합의 법칙, 곱의 법칙, 근원사건의 동등성",
            grade="middle_2",
            concept_ids=["concept-m2-prob-01", "concept-m2-prob-02"],
            question_ids=[q["id"] for q in probability_questions],
            time_limit_minutes=10,
        ),
        test(
            id="test-m2-ch1-concept",
            title="중2 수와 식 개념",
            description="유리수와 순환소수, 식의 계산, 일차부등식, 연립방정식의 개념 이해",
            grade="middle_2",
            concept_ids=[
                "concept-m2-rational-01", "concept-m2-rational-02",
                "concept-m2-expr-01", "concept-m2-expr-02",
                "concept-m2-ineq-01", "concept-m2-ineq-02",
                "concept-m2-simul-01", "concept-m2-simul-02",
            ],
            question_ids=[q["id"] for q in ch1_concept_questions],
            time_limit_minutes=15,
            use_question_pool=True,
            questions_per_attempt=8,
        ),
    ]

    return {"concepts": concepts, "questions": questions, "tests": tests}
