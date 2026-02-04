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
        concept(
            id="concept-m2-linear-func",
            name="일차함수",
            grade="middle_2",
            category="concept",
            part="func",
            description="y=ax+b, 기울기/절편, 일차함수↔일차방정식 연결",
        ),
        concept(
            id="concept-m2-triangle",
            name="삼각형의 성질",
            grade="middle_2",
            category="concept",
            part="geo",
            description="이등변삼각형, 외심(수직이등분선 교점), 내심(이등분선 교점)",
        ),
        concept(
            id="concept-m2-quadrilateral",
            name="사각형의 성질",
            grade="middle_2",
            category="concept",
            part="geo",
            description="평행사변형, 직사각형, 마름모, 정사각형 계통도, 정의 vs 성질 구분",
        ),
        concept(
            id="concept-m2-similarity",
            name="도형의 닮음",
            grade="middle_2",
            category="concept",
            part="geo",
            description="SSS/SAS/AA 닮음 조건, 닮음비→넓이비→부피비",
        ),
        concept(
            id="concept-m2-pythagoras",
            name="피타고라스 정리",
            grade="middle_2",
            category="concept",
            part="geo",
            description="삼각형 무게중심(2:1), 피타고라스 정리와 피타고라스 수",
        ),
        concept(
            id="concept-m2-probability",
            name="확률",
            grade="middle_2",
            category="concept",
            part="data",
            description="합의 법칙/곱의 법칙, 수학적 확률, 근원사건 동등성",
        ),
    ]

    # ── 일차함수 (3문제) ──
    func_questions = [
        mc(
            id="m2-conc-001",
            concept_id="concept-m2-linear-func",
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
            id="m2-conc-002",
            concept_id="concept-m2-linear-func",
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
            id="m2-conc-003",
            concept_id="concept-m2-linear-func",
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
            id="m2-conc-004",
            concept_id="concept-m2-triangle",
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
            id="m2-conc-005",
            concept_id="concept-m2-triangle",
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
            id="m2-conc-006",
            concept_id="concept-m2-triangle",
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
            id="m2-conc-007",
            concept_id="concept-m2-quadrilateral",
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
            id="m2-conc-008",
            concept_id="concept-m2-quadrilateral",
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
            id="m2-conc-009",
            concept_id="concept-m2-quadrilateral",
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
            id="m2-conc-010",
            concept_id="concept-m2-similarity",
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
            id="m2-conc-011",
            concept_id="concept-m2-similarity",
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
            id="m2-conc-012",
            concept_id="concept-m2-similarity",
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
            id="m2-conc-013",
            concept_id="concept-m2-pythagoras",
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
            id="m2-conc-014",
            concept_id="concept-m2-pythagoras",
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
            id="m2-conc-015",
            concept_id="concept-m2-pythagoras",
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
            id="m2-conc-016",
            concept_id="concept-m2-probability",
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
            id="m2-conc-017",
            concept_id="concept-m2-probability",
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
            id="m2-conc-018",
            concept_id="concept-m2-probability",
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

    questions = (
        func_questions + triangle_questions + quadrilateral_questions
        + similarity_questions + pythagoras_questions + probability_questions
    )

    tests = [
        test(
            id="test-m2-function",
            title="중2 일차함수 테스트",
            description="기울기, 절편, 일차함수와 일차방정식",
            grade="middle_2",
            concept_ids=["concept-m2-linear-func"],
            question_ids=[q["id"] for q in func_questions],
            time_limit_minutes=10,
        ),
        test(
            id="test-m2-geometry",
            title="중2 도형 종합 테스트",
            description="삼각형의 성질, 사각형의 성질, 닮음, 피타고라스 정리",
            grade="middle_2",
            concept_ids=["concept-m2-triangle", "concept-m2-quadrilateral", "concept-m2-similarity", "concept-m2-pythagoras"],
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
            concept_ids=["concept-m2-probability"],
            question_ids=[q["id"] for q in probability_questions],
            time_limit_minutes=10,
        ),
    ]

    return {"concepts": concepts, "questions": questions, "tests": tests}
