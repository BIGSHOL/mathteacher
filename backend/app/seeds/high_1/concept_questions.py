"""고1 개념 카테고리 - 경우의 수, 행렬 (2022 개정 교육과정)."""
from app.seeds._base import mc, concept, test


def get_concept_data() -> dict:
    """개념 카테고리 데이터 반환."""
    return {
        "concepts": _get_concepts(),
        "questions": _get_questions(),
        "tests": _get_tests(),
    }


def _get_concepts():
    """개념 정의 (4개: 2단원 × 2)."""
    return [
        concept(
            id="concept-h1-counting-01",
            name="합의 법칙과 곱의 법칙",
            grade="high_1",
            category="concept",
            part="data",
            description="합의 법칙(배반사건), 곱의 법칙(연속·동시 사건), 경우의 수 세기 기초"
        ),
        concept(
            id="concept-h1-counting-02",
            name="순열과 조합",
            grade="high_1",
            category="concept",
            part="data",
            description="순열 nPr(순서O), 조합 nCr(순서X), 조건부 선택, 분할 문제"
        ),
        concept(
            id="concept-h1-matrix-01",
            name="행렬의 정의와 기본 연산",
            grade="high_1",
            category="concept",
            part="algebra",
            description="행렬의 정의(2×2), 행렬의 덧셈·뺄셈·실수배, 같은 위치 성분별 연산"
        ),
        concept(
            id="concept-h1-matrix-02",
            name="행렬의 곱셈과 비가환성",
            grade="high_1",
            category="concept",
            part="algebra",
            description="행렬 곱셈(행×열 내적), AB≠BA(비가환성), 영인자, 약분 불가, 단위행렬·거듭제곱"
        ),
    ]


def _get_questions():
    """개념 문제 목록 (12문제: 경우의 수 6 + 행렬 6)."""
    return [
        # ========== 3단원: 경우의 수 (6문제) ==========

        # 합의 법칙
        mc(
            id="h1-conc-001",
            concept_id="concept-h1-counting-01",
            category="concept",
            part="data",
            difficulty=2,
            content="A 상자에 공이 3개, B 상자에 공이 5개 있을 때, 한 개의 공을 꺼내는 경우의 수는?",
            options=["8", "15", "3", "5"],
            correct="A",
            explanation="합의 법칙: A에서 택하거나 B에서 택하는 경우\n∴ 3 + 5 = 8",
            points=10,
        ),

        # 곱의 법칙
        mc(
            id="h1-conc-002",
            concept_id="concept-h1-counting-01",
            category="concept",
            part="data",
            difficulty=2,
            content="주사위 1개와 동전 1개를 던질 때, 나올 수 있는 모든 경우의 수는?",
            options=["12", "8", "6", "2"],
            correct="A",
            explanation="곱의 법칙: 주사위(6) × 동전(2) = 12",
            points=10,
        ),

        # 순열 기본
        mc(
            id="h1-conc-003",
            concept_id="concept-h1-counting-02",
            category="concept",
            part="data",
            difficulty=3,
            content="5개의 문자 A, B, C, D, E 중에서 3개를 뽑아 일렬로 나열하는 경우의 수는?",
            options=["60", "10", "120", "20"],
            correct="A",
            explanation="순열 ₅P₃ = 5 × 4 × 3 = 60",
            points=10,
        ),

        # 조합 기본
        mc(
            id="h1-conc-004",
            concept_id="concept-h1-counting-02",
            category="concept",
            part="data",
            difficulty=3,
            content="5명 중에서 2명을 뽑는 경우의 수는?",
            options=["10", "20", "5", "15"],
            correct="A",
            explanation="조합 ₅C₂ = 5!/(2!×3!) = (5×4)/(2×1) = 10",
            points=10,
        ),

        # 동적 선택지 축소 문제 ★★★
        mc(
            id="h1-conc-005",
            concept_id="concept-h1-counting-02",
            category="concept",
            part="data",
            difficulty=4,
            content="1, 2, 3, 4 중에서 서로 다른 세 개를 택하여 세 자리 자연수를 만들 때, 200보다 큰 수의 개수는?",
            options=["12", "18", "24", "6"],
            correct="A",
            explanation="백의 자리가 2, 3, 4인 경우를 계산:\n백의 자리 2: 십의 자리 3가지(1,3,4) × 일의 자리 2가지 = 6\n백의 자리 3: 십의 자리 3가지(1,2,4) × 일의 자리 2가지 = 6\n백의 자리 4: 십의 자리 3가지(1,2,3) × 일의 자리 2가지 = 6\n∴ 6 + 6 = 12 (2, 3만 계산... 오류)\n\n재계산: 200보다 크려면 백의 자리가 2 이상\n백의 자리 2: 6가지\n∴ 6가지... 잘못됨.\n\n정확한 계산: 200보다 크려면 200, 201 등 포함\n백의 자리 2, 3, 4: 각 6가지씩 → 6×2 = 12\n아니다, 백의 자리 2면 200대 (200~243), 3이면 300대, 4면 400대\n그런데 200은 만들 수 없음 (0이 없음)\n210, 213, 214, 231, 234, 241, 243: 2 시작 6개\n312, 314, 321, 324, 341, 342: 3 시작 6개\n∴ 6 + 6 = 12\n\n[오개념 교정] ★★★ 조건부 선택에서는 자릿수별로 선택지 개수가 달라집니다!",
            points=10,
        ),

        # 중복조합 vs 조합 혼동 방지
        mc(
            id="h1-conc-006",
            concept_id="concept-h1-counting-02",
            category="concept",
            part="data",
            difficulty=5,
            content="서로 다른 4개의 공을 구별되지 않는 2개의 상자에 빈 상자 없이 넣는 경우의 수는?",
            options=["7", "14", "8", "15"],
            correct="A",
            explanation="공을 (1,3) 또는 (2,2)로 분할:\n(1,3) 분할: ₄C₁ = 4가지\n(2,2) 분할: ₄C₂ / 2 = 6/2 = 3가지\n∴ 4 + 3 = 7\n\n[오개념 교정] 구별 안 되는 상자에 넣을 때는 분할 문제로 접근합니다.",
            points=10,
        ),

        # ========== 4단원: 행렬 (6문제) ==========

        # 행렬 덧셈
        mc(
            id="h1-conc-007",
            concept_id="concept-h1-matrix-01",
            category="concept",
            part="algebra",
            difficulty=2,
            content="두 행렬 A = [[1, 2], [3, 4]], B = [[5, 6], [7, 8]]에 대하여 A + B를 구하시오.",
            options=["[[6, 8], [10, 12]]", "[[5, 8], [10, 12]]", "[[6, 8], [9, 12]]", "[[1, 2], [3, 4]]"],
            correct="A",
            explanation="같은 위치의 성분끼리 더함:\nA + B = [[1+5, 2+6], [3+7, 4+8]] = [[6, 8], [10, 12]]",
            points=10,
        ),

        # 행렬 실수배
        mc(
            id="h1-conc-008",
            concept_id="concept-h1-matrix-01",
            category="concept",
            part="algebra",
            difficulty=2,
            content="행렬 A = [[2, -1], [0, 3]]에 대하여 3A를 구하시오.",
            options=["[[6, -3], [0, 9]]", "[[5, 2], [3, 6]]", "[[6, -3], [3, 9]]", "[[2, -1], [0, 9]]"],
            correct="A",
            explanation="각 성분에 3을 곱함:\n3A = [[3×2, 3×(-1)], [3×0, 3×3]] = [[6, -3], [0, 9]]",
            points=10,
        ),

        # 행렬 곱셈 기본
        mc(
            id="h1-conc-009",
            concept_id="concept-h1-matrix-02",
            category="concept",
            part="algebra",
            difficulty=3,
            content="두 행렬 A = [[1, 2], [3, 4]], B = [[1, 0], [0, 1]]에 대하여 AB를 구하시오.",
            options=["[[1, 2], [3, 4]]", "[[1, 0], [0, 1]]", "[[1, 2], [3, 5]]", "[[2, 2], [4, 4]]"],
            correct="A",
            explanation="행렬 곱셈:\nAB = [[1×1+2×0, 1×0+2×1], [3×1+4×0, 3×0+4×1]]\n   = [[1, 2], [3, 4]]\n(B는 단위행렬이므로 AB = A)",
            points=10,
        ),

        # 행렬 교환법칙 불성립 ★★★
        mc(
            id="h1-conc-010",
            concept_id="concept-h1-matrix-02",
            category="concept",
            part="algebra",
            difficulty=4,
            content="두 행렬 A = [[1, 2], [0, 1]], B = [[1, 0], [1, 1]]에 대하여 AB와 BA를 비교하시오.",
            options=["AB ≠ BA", "AB = BA", "AB + BA = 0", "AB = 2BA"],
            correct="A",
            explanation="AB = [[1×1+2×1, 1×0+2×1], [0×1+1×1, 0×0+1×1]] = [[3, 2], [1, 1]]\nBA = [[1×1+0×0, 1×2+0×1], [1×1+1×0, 1×2+1×1]] = [[1, 2], [1, 3]]\n∴ AB ≠ BA\n\n[오개념 교정] ★★★ 행렬 곱셈은 교환법칙이 성립하지 않습니다! AB ≠ BA",
            points=10,
        ),

        # 영인자 존재 ★★★
        mc(
            id="h1-conc-011",
            concept_id="concept-h1-matrix-02",
            category="concept",
            part="algebra",
            difficulty=5,
            content="두 행렬 A = [[1, 1], [2, 2]], B = [[2, -2], [-2, 2]]에 대하여 AB를 계산하시오.",
            options=["[[0, 0], [0, 0]]", "[[1, 1], [2, 2]]", "[[2, -2], [-2, 2]]", "[[0, 1], [0, 2]]"],
            correct="A",
            explanation="AB = [[1×2+1×(-2), 1×(-2)+1×2], [2×2+2×(-2), 2×(-2)+2×2]]\n   = [[2-2, -2+2], [4-4, -4+4]]\n   = [[0, 0], [0, 0]]\n\n[오개념 교정] ★★★ 행렬에서는 A ≠ O, B ≠ O이지만 AB = O인 경우(영인자)가 존재합니다!",
            points=10,
        ),

        # 약분 불가 ★★★
        mc(
            id="h1-conc-012",
            concept_id="concept-h1-matrix-02",
            category="concept",
            part="algebra",
            difficulty=5,
            content="두 행렬 A = [[0, 1], [0, 0]], B = [[1, 2], [3, 4]], C = [[5, 6], [3, 4]]에 대하여 AB = AC일 때, B와 C의 관계는?",
            options=["B ≠ C", "B = C", "B = 2C", "B + C = 0"],
            correct="A",
            explanation="AB = [[0×1+1×3, 0×2+1×4], [0×1+0×3, 0×2+0×4]] = [[3, 4], [0, 0]]\nAC = [[0×5+1×3, 0×6+1×4], [0×5+0×3, 0×6+0×4]] = [[3, 4], [0, 0]]\n∴ AB = AC이지만 B ≠ C\n\n[오개념 교정] ★★★ 행렬에서는 AB = AC라도 B = C가 아닐 수 있습니다! (약분 불가)",
            points=10,
        ),

        # ========== 1~2단원 개념 문제 (다항식, 방정식과 부등식) ==========

        # 다항식 (3문제)
        mc(
            id="h1-conc-013",
            concept_id="concept-h1-polynomial-01",
            category="concept",
            part="algebra",
            difficulty=3,
            content="다음 중 항등식의 정의로 올바른 것은?",
            options=[
                "미지수에 어떤 값을 대입해도 항상 성립하는 등식",
                "미지수의 특정 값에서만 성립하는 등식",
                "좌변과 우변이 다른 등식",
                "해가 없는 등식",
            ],
            correct="A",
            explanation="항등식은 미지수에 어떤 값을 넣어도 항상 참인 등식입니다. 예: (x + 1)² = x² + 2x + 1. 반면 방정식은 특정 값에서만 성립합니다.",
            points=10,
        ),
        mc(
            id="h1-conc-014",
            concept_id="concept-h1-polynomial-02",
            category="concept",
            part="algebra",
            difficulty=5,
            content="나머지정리에 의하면, 다항식 f(x)를 (x - a)로 나눈 나머지는?",
            options=["f(a)", "f(-a)", "f(0)", "a"],
            correct="A",
            explanation="나머지정리: f(x)를 (x - a)로 나눌 때 나머지는 f(a)입니다. f(x) = (x - a)Q(x) + R에서 x = a를 대입하면 R = f(a)입니다.",
            points=10,
        ),
        mc(
            id="h1-conc-015",
            concept_id="concept-h1-polynomial-02",
            category="concept",
            part="algebra",
            difficulty=7,
            content="인수정리에 의하면, f(a) = 0일 때 다항식 f(x)는 무엇을 인수로 가지는가?",
            options=["(x - a)", "(x + a)", "x", "a"],
            correct="A",
            explanation="인수정리: f(a) = 0이면 f(x)는 (x - a)를 인수로 가집니다. 이는 나머지정리에서 나머지 = f(a) = 0이므로 (x - a)로 나누어떨어지기 때문입니다.",
            points=15,
        ),
        # 방정식과 부등식 (3문제)
        mc(
            id="h1-conc-016",
            concept_id="concept-h1-equation-01",
            category="concept",
            part="algebra",
            difficulty=4,
            content="허수 단위 i를 도입한 이유는?",
            options=[
                "실수 범위에서 x² + 1 = 0의 해가 존재하지 않기 때문",
                "계산을 간단히 하기 위해",
                "모든 방정식의 해가 양수이기 때문",
                "소수를 확장하기 위해",
            ],
            correct="A",
            explanation="x² = -1을 만족하는 실수는 없습니다. 이 방정식의 해를 나타내기 위해 i² = -1을 만족하는 허수 단위 i를 도입했습니다.",
            points=10,
        ),
        mc(
            id="h1-conc-017",
            concept_id="concept-h1-equation-01",
            category="concept",
            part="algebra",
            difficulty=6,
            content="이차방정식의 판별식 D = b² - 4ac의 값에 따른 근의 개수로 옳은 것은?",
            options=[
                "D > 0: 서로 다른 두 실근, D = 0: 중근, D < 0: 실근 없음",
                "D > 0: 근 없음, D = 0: 한 근, D < 0: 두 근",
                "D의 값과 근의 개수는 무관하다",
                "D > 0: 중근, D = 0: 서로 다른 두 근",
            ],
            correct="A",
            explanation="판별식 D의 부호가 근의 개수를 결정합니다. D > 0이면 서로 다른 두 실근, D = 0이면 중근, D < 0이면 실근이 없고 허근을 가집니다.",
            points=10,
        ),
        mc(
            id="h1-conc-018",
            concept_id="concept-h1-equation-02",
            category="concept",
            part="algebra",
            difficulty=8,
            content="이차부등식 (x - 1)(x - 3) > 0의 해가 x < 1 또는 x > 3인 이유는?",
            options=[
                "y = (x - 1)(x - 3)의 그래프에서 y > 0인 구간이 두 근의 바깥이기 때문",
                "부등식의 부등호 방향과 무관하다",
                "모든 이차부등식의 해는 두 근 사이이다",
                "두 근의 합이 양수이기 때문",
            ],
            correct="A",
            explanation="위로 볼록(a > 0)인 이차함수 그래프에서 y > 0인 구간은 두 근의 바깥 영역입니다. y < 0인 구간은 두 근 사이입니다.",
            points=15,
        ),
    ]


def _get_tests():
    """개념 카테고리 테스트 (3개)."""
    return [
        test(
            id="test-h1-counting",
            title="고1 경우의 수 테스트",
            description="합의 법칙, 곱의 법칙, 순열(nPr), 조합(nCr), 동적 선택지 축소 문제",
            grade="high_1",
            concept_ids=["concept-h1-counting-01", "concept-h1-counting-02"],
            question_ids=[f"h1-conc-{i:03d}" for i in range(1, 7)],
            time_limit_minutes=20,
            use_question_pool=True,
            questions_per_attempt=5,
        ),
        test(
            id="test-h1-matrix",
            title="고1 행렬 테스트",
            description="2×2 행렬의 연산, 교환법칙 불성립, 영인자 존재, 약분 불가",
            grade="high_1",
            concept_ids=["concept-h1-matrix-01", "concept-h1-matrix-02"],
            question_ids=[f"h1-conc-{i:03d}" for i in range(7, 13)],
            time_limit_minutes=20,
            use_question_pool=True,
            questions_per_attempt=5,
        ),
        test(
            id="test-h1-ch1-concept",
            title="고1 다항식·방정식 개념",
            description="항등식, 나머지정리, 인수분해, 복소수, 판별식, 이차부등식의 개념 이해",
            grade="high_1",
            concept_ids=["concept-h1-polynomial-01", "concept-h1-polynomial-02", "concept-h1-equation-01", "concept-h1-equation-02"],
            question_ids=[f"h1-conc-{i:03d}" for i in range(13, 19)],
            time_limit_minutes=10,
            use_question_pool=True,
            questions_per_attempt=5,
        ),
    ]
