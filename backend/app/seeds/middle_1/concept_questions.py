"""중1 개념(concept) 카테고리 시드 데이터."""

from app.seeds._base import mc, concept, test


def get_concept_data() -> dict:
    """개념 카테고리 데이터 반환."""

    # ============================================================
    # 개념 정의
    # ============================================================
    concepts = [
        concept(
            id="concept-001",
            name="일차방정식",
            grade="middle_1",
            category="concept",
            part="algebra",
            description="일차방정식의 풀이",
        ),
        concept(
            id="concept-003",
            name="일차부등식",
            grade="middle_1",
            category="concept",
            part="algebra",
            description="일차부등식의 풀이와 수직선 표현",
        ),
        concept(
            id="concept-004",
            name="좌표와 그래프",
            grade="middle_1",
            category="concept",
            part="func",
            description="좌표평면과 정비례·반비례 그래프",
        ),
        concept(
            id="concept-005",
            name="통계",
            grade="middle_1",
            category="concept",
            part="data",
            description="도수분포와 평균, 중앙값",
        ),
    ]

    # ============================================================
    # 일차방정식 - 기본 문제 (난이도 6)
    # ============================================================
    eq_basic = [
        mc(
            id="question-001",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=6,
            content="다음 중 일차방정식인 것은?",
            options=[
                "x² + 2 = 6",
                "3x - 5 = 7",
                "2x + y = 10",
                "x > 3",
            ],
            correct="B",
            explanation="일차방정식은 미지수가 1개이고 차수가 1인 등식입니다. A는 이차, C는 미지수 2개, D는 부등식입니다.",
            points=10,
        ),
        mc(
            id="question-002",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=6,
            content="등식 x + 5 = 12에서 x를 구하기 위해 양변에 해야 할 연산은?",
            options=[
                "양변에 5를 더한다",
                "양변에서 5를 뺀다",
                "양변에 12를 곱한다",
                "양변을 5로 나눈다",
            ],
            correct="B",
            explanation="등식의 성질: 양변에서 같은 수를 빼도 등식이 성립합니다. x + 5 - 5 = 12 - 5 → x = 7",
            points=10,
        ),
        mc(
            id="question-003",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=6,
            content="일차방정식의 풀이에서 '이항'이란?",
            options=[
                "항을 없애는 것",
                "항의 부호를 바꾸어 등호 반대편으로 옮기는 것",
                "양변에 같은 수를 곱하는 것",
                "미지수끼리 더하는 것",
            ],
            correct="B",
            explanation="이항이란 등식의 한 변의 항을 부호를 바꾸어 다른 변으로 옮기는 것입니다.",
            points=10,
        ),
    ]

    # ============================================================
    # 일차방정식 - 적응형 문제 (난이도 2-10)
    # ============================================================
    eq_adaptive = [
        # 난이도 2
        mc(
            id="question-a-001",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=2,
            content="등호(=)가 포함된 식을 무엇이라 하는가?",
            options=["부등식", "등식", "다항식", "단항식"],
            correct="B",
            explanation="등호(=)를 사용하여 두 식이 같음을 나타낸 식을 등식이라 합니다.",
            points=10,
        ),
        mc(
            id="question-a-002",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=2,
            content="다음 중 등식인 것은?",
            options=["3 + 5", "x > 2", "x + 1 = 4", "2x + 3"],
            correct="C",
            explanation="등식은 등호(=)가 있는 식입니다. x + 1 = 4만 등호가 있습니다.",
            points=10,
        ),
        # 난이도 3
        mc(
            id="question-a-003",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=3,
            content="방정식에서 값을 모르는 문자를 무엇이라 하는가?",
            options=["상수", "계수", "미지수", "차수"],
            correct="C",
            explanation="방정식에서 값을 모르는 문자를 미지수라 하고, 미지수의 값을 구하는 것을 '방정식을 푼다'고 합니다.",
            points=10,
        ),
        # 난이도 4
        mc(
            id="question-a-004",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=4,
            content="x + 5 = 8에서 x를 구하기 위해 양변에서 빼야 하는 수는?",
            options=["3", "5", "8", "13"],
            correct="B",
            explanation="등식의 성질: 양변에서 같은 수 5를 빼면 x + 5 - 5 = 8 - 5, 즉 x = 3이 됩니다.",
            points=10,
        ),
        mc(
            id="question-a-005",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=4,
            content="'a = b이면 a + c = b + c이다'는 등식의 어떤 성질인가?",
            options=[
                "양변에 같은 수를 더해도 등식은 성립한다",
                "양변에 같은 수를 곱해도 등식은 성립한다",
                "양변을 같은 수로 나누어도 등식은 성립한다",
                "양변의 부호를 바꾸어도 등식은 성립한다",
            ],
            correct="A",
            explanation="a = b이면 a + c = b + c는 '양변에 같은 수를 더해도 등식이 성립한다'는 성질입니다.",
            points=10,
        ),
        # 난이도 5
        mc(
            id="question-a-006",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=5,
            content="3x = 12를 풀 때 양변을 나누어야 하는 수는?",
            options=["2", "3", "4", "12"],
            correct="B",
            explanation="x의 계수인 3으로 양변을 나누면: 3x ÷ 3 = 12 ÷ 3, 즉 x = 4가 됩니다.",
            points=10,
        ),
        # 난이도 7
        mc(
            id="question-a-007",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=7,
            content="2x - 3 = 7의 풀이 과정입니다. 잘못된 단계는?\n① 2x - 3 + 3 = 7 + 3\n② 2x = 10\n③ 2x × 2 = 10 × 2\n④ x = 5",
            options=["① 단계", "② 단계", "③ 단계", "④ 단계"],
            correct="C",
            explanation="③에서 양변에 2를 곱하면 4x = 20이 됩니다. 올바른 방법은 양변을 2로 '나누는' 것입니다.",
            points=15,
        ),
        mc(
            id="question-a-008",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=7,
            content="다음 중 해가 x = -2인 일차방정식은?",
            options=[
                "x + 5 = 3",
                "2x + 1 = 5",
                "x - 2 = 0",
                "3x = 6",
            ],
            correct="A",
            explanation="x = -2를 대입하면: A) -2 + 5 = 3 ✓, B) -4 + 1 = -3 ✗, C) -4 ✗, D) -6 ✗",
            points=15,
        ),
        # 난이도 8
        mc(
            id="question-a-009",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=8,
            content="일차방정식 ax + b = 0 (a ≠ 0)의 해를 a, b로 나타내면?",
            options=["x = b/a", "x = -b/a", "x = a/b", "x = -a/b"],
            correct="B",
            explanation="ax + b = 0 → ax = -b → x = -b/a (a ≠ 0)",
            points=15,
        ),
        # 난이도 9
        mc(
            id="question-a-010",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=9,
            content="분수 방정식 (x+1)/3 = (x-1)/2를 풀 때 가장 먼저 해야 할 것은?",
            options=[
                "양변에 3을 곱한다",
                "양변에 6을 곱한다 (분모의 최소공배수)",
                "분자끼리 등식을 세운다",
                "양변에서 1을 뺀다",
            ],
            correct="B",
            explanation="분모 3과 2의 최소공배수 6을 양변에 곱하면 분모를 없앨 수 있습니다: 2(x+1) = 3(x-1)",
            points=20,
        ),
        # 난이도 10
        mc(
            id="question-a-011",
            concept_id="concept-001",
            category="concept",
            part="word",
            difficulty=10,
            content="'어떤 수의 3배에서 5를 빼면 그 수에 7을 더한 것과 같다'를 방정식으로 바르게 세운 것은?",
            options=[
                "3x - 5 = x + 7",
                "3(x - 5) = x + 7",
                "3x + 5 = x - 7",
                "3x - 5 = 7x",
            ],
            correct="A",
            explanation="'어떤 수의 3배' → 3x, '에서 5를 빼면' → 3x - 5, '그 수에 7을 더한 것' → x + 7. 따라서 3x - 5 = x + 7",
            points=20,
        ),
    ]

    # ============================================================
    # 일차방정식 - 고난이도 문제 (난이도 6-10)
    # ============================================================
    eq_high = [
        mc(
            id="question-eq-006",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=6,
            content="일차방정식 4x - 3 = 2x + 7 의 해는?",
            options=["x = 2", "x = 5", "x = -5", "x = -2"],
            correct="B",
            explanation="4x - 2x = 7 + 3 → 2x = 10 → x = 5",
            points=10,
        ),
        mc(
            id="question-eq-007",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=7,
            content="방정식 2(x + 3) = 3(x - 1) + 11 의 해는?",
            options=["x = 2", "x = -2", "x = 1", "x = 4"],
            correct="B",
            explanation="2x + 6 = 3x - 3 + 11 → 2x + 6 = 3x + 8 → -x = 2 → x = -2",
            points=15,
        ),
        mc(
            id="question-eq-008",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=8,
            content="방정식 (x-1)/2 = (2x+3)/5 의 해는?",
            options=["x = 11", "x = -11", "x = 7", "x = -7"],
            correct="A",
            explanation="양변에 10을 곱하면: 5(x-1) = 2(2x+3) → 5x - 5 = 4x + 6 → x = 11",
            points=15,
        ),
        mc(
            id="question-eq-009",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=9,
            content="어떤 수의 3배에서 5를 뺀 값이 그 수에 7을 더한 값의 2배와 같다. 그 수는?",
            options=["19", "17", "15", "9"],
            correct="A",
            explanation="x를 어떤 수라 하면: 3x - 5 = 2(x + 7) → 3x - 5 = 2x + 14 → x = 19",
            points=20,
        ),
        mc(
            id="question-eq-010",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=10,
            content="연속하는 세 홀수의 합이 63일 때, 가장 큰 수는?",
            options=["21", "23", "25", "19"],
            correct="B",
            explanation="연속하는 세 홀수를 x-2, x, x+2로 놓으면: (x-2)+x+(x+2)=63 → 3x=63 → x=21. 가장 큰 수는 21+2=23",
            points=20,
        ),
    ]

    # ============================================================
    # 일차부등식 문제 (난이도 6-9)
    # ============================================================
    ineq_questions = [
        mc(
            id="question-ineq-001",
            concept_id="concept-003",
            category="concept",
            part="algebra",
            difficulty=6,
            content="부등식의 양변에 같은 음수를 곱하면 부등호의 방향은 어떻게 되는가?",
            options=[
                "그대로 유지된다",
                "반대로 바뀐다",
                "등호로 바뀐다",
                "부등식이 성립하지 않는다",
            ],
            correct="B",
            explanation="부등식의 양변에 음수를 곱하거나 나누면 부등호의 방향이 반대로 바뀐다. 예: 3 > 2에서 양변에 -1을 곱하면 -3 < -2",
            points=10,
        ),
        mc(
            id="question-ineq-002",
            concept_id="concept-003",
            category="concept",
            part="algebra",
            difficulty=7,
            content="다음 중 부등식의 성질로 옳은 것은?",
            options=[
                "양변에 같은 수를 더하면 부등호 방향이 바뀐다",
                "양변에 양수를 곱하면 부등호 방향이 바뀐다",
                "양변에 음수를 곱하면 부등호 방향이 바뀐다",
                "양변에 0을 곱해도 부등호가 유지된다",
            ],
            correct="C",
            explanation="부등식의 양변에 음수를 곱하면 부등호의 방향이 바뀐다. 양변에 같은 수를 더하거나 양수를 곱할 때는 부등호 방향이 유지된다.",
            points=10,
        ),
        mc(
            id="question-ineq-003",
            concept_id="concept-003",
            category="concept",
            part="algebra",
            difficulty=7,
            content="일차부등식의 해를 수직선에 나타낼 때, x < 3의 표현으로 옳은 것은?",
            options=[
                "3에 속이 빈 원(○)을 찍고 왼쪽으로 화살표",
                "3에 속이 찬 원(●)을 찍고 왼쪽으로 화살표",
                "3에 속이 빈 원(○)을 찍고 오른쪽으로 화살표",
                "3에 속이 찬 원(●)을 찍고 오른쪽으로 화살표",
            ],
            correct="A",
            explanation="x < 3은 3을 포함하지 않으므로 속이 빈 원(○)을 사용하고, 3보다 작은 수는 왼쪽이므로 왼쪽 화살표로 나타낸다. x ≤ 3이면 속이 찬 원(●)을 사용한다.",
            points=15,
        ),
        mc(
            id="question-ineq-004",
            concept_id="concept-003",
            category="concept",
            part="algebra",
            difficulty=9,
            content="일차부등식 -3x + 6 > 0의 풀이 과정이다. 잘못된 단계는?\n① -3x + 6 > 0\n② -3x > -6 (양변에서 6을 뺌)\n③ x > 2 (양변을 -3으로 나눔)",
            options=[
                "①에서 ②로 가는 과정",
                "②에서 ③으로 가는 과정",
                "①과 ② 모두 잘못됨",
                "잘못된 단계가 없다",
            ],
            correct="B",
            explanation="②에서 ③으로 갈 때 양변을 음수(-3)로 나누었으므로 부등호 방향이 바뀌어야 한다. 올바른 결과는 x < 2이다.",
            points=15,
        ),
    ]

    # ============================================================
    # 좌표와 그래프 문제 (난이도 6-9)
    # ============================================================
    coord_questions = [
        mc(
            id="question-coord-001",
            concept_id="concept-004",
            category="concept",
            part="func",
            difficulty=6,
            content="좌표평면에서 x좌표가 양수이고 y좌표가 음수인 점은 어느 사분면에 위치하는가?",
            options=["제1사분면", "제2사분면", "제3사분면", "제4사분면"],
            correct="D",
            explanation="제4사분면은 x > 0, y < 0인 영역이다. 제1사분면(+,+), 제2사분면(-,+), 제3사분면(-,-), 제4사분면(+,-)로 구분한다.",
            points=10,
        ),
        mc(
            id="question-coord-002",
            concept_id="concept-004",
            category="concept",
            part="func",
            difficulty=7,
            content="정비례 관계 y = ax (a > 0)의 그래프에 대한 설명으로 옳은 것은?",
            options=[
                "원점을 지나는 직선이다",
                "y축과 평행한 직선이다",
                "x축과 한 점에서 만난다",
                "곡선 형태이다",
            ],
            correct="A",
            explanation="정비례 y = ax의 그래프는 항상 원점(0,0)을 지나는 직선이다. a > 0이면 오른쪽 위로 향하고, a < 0이면 오른쪽 아래로 향한다.",
            points=10,
        ),
        mc(
            id="question-coord-003",
            concept_id="concept-004",
            category="concept",
            part="func",
            difficulty=6,
            content="반비례 관계 y = a/x의 그래프가 절대 지나지 않는 곳은?",
            options=["제1사분면", "제3사분면", "원점과 좌표축", "제4사분면"],
            correct="C",
            explanation="반비례 y = a/x에서 x = 0이면 y가 정의되지 않고, y = 0이 되는 x값도 없다. 따라서 그래프는 원점과 x축, y축을 절대 지나지 않는다.",
            points=10,
        ),
        mc(
            id="question-coord-004",
            concept_id="concept-004",
            category="concept",
            part="func",
            difficulty=9,
            content="좌표평면에서 x축 위에 있는 모든 점의 공통된 특징은?",
            options=[
                "x좌표가 0이다",
                "y좌표가 0이다",
                "x좌표와 y좌표가 같다",
                "원점으로부터 거리가 같다",
            ],
            correct="B",
            explanation="x축 위의 점은 모두 y좌표가 0이다. 예: (1,0), (-3,0), (0,0) 등. 반대로, y축 위의 점은 모두 x좌표가 0이다.",
            points=15,
        ),
    ]

    # ============================================================
    # 통계 문제 (난이도 4-6)
    # ============================================================
    stat_questions = [
        mc(
            id="question-stat-001",
            concept_id="concept-005",
            category="concept",
            part="data",
            difficulty=4,
            content="평균, 중앙값, 최빈값 중에서 극단적으로 크거나 작은 값(이상값)에 가장 큰 영향을 받는 대표값은?",
            options=[
                "평균",
                "중앙값",
                "최빈값",
                "세 대표값 모두 같은 영향을 받는다",
            ],
            correct="A",
            explanation="평균은 모든 자료값의 합을 개수로 나눈 것이므로 극단값에 크게 영향을 받는다. 중앙값은 가운데 위치의 값이고 최빈값은 가장 많이 나타나는 값이므로 극단값에 상대적으로 덜 영향을 받는다.",
            points=10,
        ),
        mc(
            id="question-stat-002",
            concept_id="concept-005",
            category="concept",
            part="data",
            difficulty=6,
            content="자료를 크기순으로 나열했을 때 한가운데에 위치하는 값을 무엇이라 하는가?",
            options=["평균", "중앙값", "최빈값", "분산"],
            correct="B",
            explanation="중앙값(median)은 자료를 크기순으로 나열했을 때 정가운데에 위치하는 값이다. 자료의 개수가 짝수이면 가운데 두 값의 평균을 중앙값으로 한다.",
            points=10,
        ),
        mc(
            id="question-stat-003",
            concept_id="concept-005",
            category="concept",
            part="data",
            difficulty=6,
            content="도수분포표에서 '도수'가 의미하는 것은?",
            options=[
                "각 계급에 속하는 자료의 개수",
                "자료의 전체 개수",
                "계급의 크기",
                "자료의 평균값",
            ],
            correct="A",
            explanation="도수(frequency)란 각 계급(구간)에 속하는 자료의 개수를 말한다. 모든 계급의 도수를 합하면 전체 자료의 개수가 된다.",
            points=10,
        ),
    ]

    # ============================================================
    # 테스트 목록
    # ============================================================
    tests = [
        # 일차방정식 종합 테스트 (고정형)
        test(
            id="test-001",
            title="일차방정식 종합 테스트",
            description="일차방정식의 기본부터 응용까지 총 12문제",
            grade="middle_1",
            concept_ids=["concept-001"],
            question_ids=[
                # 기본 개념 (4문제 - 40점)
                "question-a-001",  # 등식 정의
                "question-a-002",  # 등식 판별
                "question-a-003",  # 미지수 정의
                "question-001",    # 일차방정식 판별
                # 기본 풀이 (4문제 - 40점)
                "question-002",    # 등식 성질
                "question-003",    # 이항
                "question-a-004",  # x = 7 판별
                "question-a-006",  # 3x = 12 풀이
                # 응용 (4문제 - 40점)
                "question-a-007",  # 2x + 3 = 11 풀이
                "question-a-008",  # 복잡한 방정식
                "question-a-009",  # 일반형 해
                "question-a-005",  # 해 대입 확인
            ],
            time_limit_minutes=20,
        ),
        # 적응형 테스트
        test(
            id="test-adaptive-001",
            title="적응형 일차방정식",
            description="실력에 맞게 난이도가 자동 조절됩니다",
            grade="middle_1",
            concept_ids=["concept-001"],
            question_ids=[],
            time_limit_minutes=15,
            is_adaptive=True,
        ),
        # 문제 풀 테스트
        test(
            id="test-pool-001",
            title="일차방정식 연습 (랜덤)",
            description="11개 문제 중 5개가 랜덤으로 출제되고, 보기 순서도 매번 바뀝니다. 정답 외우기 방지!",
            grade="middle_1",
            concept_ids=["concept-001"],
            question_ids=[
                "question-a-001",
                "question-a-002",
                "question-a-003",
                "question-a-004",
                "question-a-005",
                "question-a-006",
                "question-a-007",
                "question-a-008",
                "question-a-009",
                "question-a-010",
                "question-a-011",
            ],
            time_limit_minutes=10,
            use_question_pool=True,
            questions_per_attempt=5,
            shuffle_options=True,
        ),
        # 진단 평가
        test(
            id="test-placement-001",
            title="실력 진단 평가",
            description="5-10분 테스트로 당신에게 딱 맞는 학습 경로를 찾아드립니다",
            grade="middle_1",
            concept_ids=[
                "concept-001",  # 일차방정식
                "concept-002",  # 사칙연산
                "concept-003",  # 일차부등식
                "concept-004",  # 좌표와 그래프
                "concept-005",  # 통계
            ],
            question_ids=[
                # 일차방정식 (기초)
                "question-001",
                "question-002",
                # 적응형 문제 (다양한 난이도)
                "question-a-003",  # 난이도 3
                "question-a-006",  # 난이도 5
                "question-a-009",  # 난이도 8
                # 사칙연산
                "question-op-003",
                "question-op-005",
                # 일차부등식
                "question-ineq-001",
                "question-ineq-003",
                # 좌표
                "question-coord-001",
                # 통계
                "question-stat-001",
            ],
            time_limit_minutes=10,
        ),
        # 일차부등식 테스트
        test(
            id="test-003",
            title="일차부등식 테스트",
            description="부등식의 성질을 이용한 문제 풀이",
            grade="middle_1",
            concept_ids=["concept-003"],
            question_ids=[
                "question-ineq-001",
                "question-ineq-002",
                "question-ineq-003",
                "question-ineq-004",
            ],
            time_limit_minutes=8,
        ),
        # 좌표와 그래프 테스트
        test(
            id="test-004",
            title="좌표와 그래프",
            description="좌표평면 위의 점과 그래프 읽기",
            grade="middle_1",
            concept_ids=["concept-004"],
            question_ids=[
                "question-coord-001",
                "question-coord-002",
                "question-coord-003",
                "question-coord-004",
            ],
            time_limit_minutes=10,
        ),
        # 통계 테스트
        test(
            id="test-005",
            title="통계 기초",
            description="평균, 중앙값, 최빈값 구하기",
            grade="middle_1",
            concept_ids=["concept-005"],
            question_ids=[
                "question-stat-001",
                "question-stat-002",
                "question-stat-003",
            ],
            time_limit_minutes=7,
        ),
    ]

    return {
        "concepts": concepts,
        "questions": eq_basic + eq_adaptive + eq_high + ineq_questions + coord_questions + stat_questions,
        "tests": tests,
    }
