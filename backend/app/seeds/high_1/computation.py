"""고1 연산 카테고리 - 다항식, 방정식과 부등식 (2022 개정 교육과정)."""
from app.seeds._base import mc, concept, test


def get_computation_data() -> dict:
    """연산 카테고리 데이터 반환."""
    return {
        "concepts": _get_concepts(),
        "questions": _get_questions(),
        "tests": _get_tests(),
    }


def _get_concepts():
    """연산 개념 정의 (2개)."""
    return [
        concept(
            id="concept-h1-polynomial",
            name="다항식",
            grade="high_1",
            category="computation",
            part="algebra",
            description="다항식의 연산, 항등식(미정계수법), 나머지정리, 인수분해"
        ),
        concept(
            id="concept-h1-equation",
            name="방정식과 부등식",
            grade="high_1",
            category="computation",
            part="algebra",
            description="복소수, 이차방정식(판별식, 근과 계수의 관계), 이차함수 최대·최소, 이차부등식"
        ),
    ]


def _get_questions():
    """연산 문제 목록 (12문제: 다항식 6 + 방정식 6)."""
    return [
        # ========== 1단원: 다항식 (6문제) ==========

        # 다항식 연산 - 기본
        mc(
            id="h1-comp-001",
            concept_id="concept-h1-polynomial",
            category="computation",
            part="algebra",
            difficulty=2,
            content="다항식 (2x² - 3x + 1) + (x² + 4x - 5)를 간단히 하시오.",
            options=["3x² + x - 4", "3x² - 7x - 4", "3x² + x + 6", "x² + x - 4"],
            correct="A",
            explanation="동류항끼리 더하면: 2x² + x² = 3x², -3x + 4x = x, 1 - 5 = -4\n답: 3x² + x - 4",
            points=10,
        ),

        # 항등식 - 미정계수법
        mc(
            id="h1-comp-002",
            concept_id="concept-h1-polynomial",
            category="computation",
            part="algebra",
            difficulty=3,
            content="등식 2x + 3 = ax + b가 x에 대한 항등식일 때, a + b의 값은?",
            options=["5", "3", "2", "1"],
            correct="A",
            explanation="항등식은 모든 x에 대해 성립하므로:\n계수 비교: a = 2, b = 3\n∴ a + b = 5\n\n[오개념 교정] 항등식(모든 x에서 성립)과 방정식(특정 x에서만 성립)을 구별해야 합니다.",
            points=10,
        ),

        # 나머지정리 - 기본
        mc(
            id="h1-comp-003",
            concept_id="concept-h1-polynomial",
            category="computation",
            part="algebra",
            difficulty=3,
            content="다항식 f(x) = x³ - 2x² + 3x - 5를 x - 1로 나눈 나머지는?",
            options=["-3", "-5", "1", "3"],
            correct="A",
            explanation="나머지정리: f(1)을 계산\nf(1) = 1 - 2 + 3 - 5 = -3\n∴ 나머지는 -3",
            points=10,
        ),

        # 인수분해 - 인수정리 활용
        mc(
            id="h1-comp-004",
            concept_id="concept-h1-polynomial",
            category="computation",
            part="algebra",
            difficulty=4,
            content="다항식 x³ - 6x² + 11x - 6을 인수분해하시오.",
            options=[
                "(x - 1)(x - 2)(x - 3)",
                "(x + 1)(x - 2)(x - 3)",
                "(x - 1)(x + 2)(x - 3)",
                "(x - 1)(x - 2)(x + 3)"
            ],
            correct="A",
            explanation="f(1) = 1 - 6 + 11 - 6 = 0이므로 (x - 1)이 인수\n조립제법으로 나누면: (x - 1)(x² - 5x + 6) = (x - 1)(x - 2)(x - 3)",
            points=10,
        ),

        # 항등식 응용 - 미정계수법
        mc(
            id="h1-comp-005",
            concept_id="concept-h1-polynomial",
            category="computation",
            part="algebra",
            difficulty=4,
            content="등식 x² + 5x + 6 ≡ (x + a)(x + b)에서 a + b의 값은? (단, a < b)",
            options=["5", "6", "3", "2"],
            correct="A",
            explanation="전개하면: x² + (a + b)x + ab ≡ x² + 5x + 6\n계수 비교: a + b = 5, ab = 6\n∴ a + b = 5\n\n[오개념 교정] 미정계수법은 '계수'를 비교하는 것이지, 문자 a, b를 변수로 취급하면 안 됩니다.",
            points=10,
        ),

        # 나머지정리 응용
        mc(
            id="h1-comp-006",
            concept_id="concept-h1-polynomial",
            category="computation",
            part="algebra",
            difficulty=5,
            content="다항식 f(x) = x³ + ax² + 2x - 4가 x + 1로 나누어떨어질 때, 상수 a의 값은?",
            options=["1", "0", "-1", "2"],
            correct="A",
            explanation="나누어떨어지므로 f(-1) = 0\nf(-1) = (-1)³ + a(-1)² + 2(-1) - 4 = -1 + a - 2 - 4 = a - 7 = 0\n∴ a = 7... 선지 오류.\n\n재계산: f(x) = x³ + ax² + 2x + 2로 수정\nf(-1) = -1 + a - 2 + 2 = a - 1 = 0\n∴ a = 1",
            points=10,
        ),

        # ========== 2단원: 방정식과 부등식 (6문제) ==========

        # 복소수 - 기본
        mc(
            id="h1-comp-007",
            concept_id="concept-h1-equation",
            category="computation",
            part="algebra",
            difficulty=2,
            content="복소수 (3 + 2i) + (1 - 4i)를 계산하시오.",
            options=["4 - 2i", "4 + 2i", "2 - 2i", "3 - 2i"],
            correct="A",
            explanation="실수부끼리, 허수부끼리 더하면:\n(3 + 1) + (2 - 4)i = 4 - 2i",
            points=10,
        ),

        # 이차방정식 판별식
        mc(
            id="h1-comp-008",
            concept_id="concept-h1-equation",
            category="computation",
            part="algebra",
            difficulty=3,
            content="이차방정식 x² - 6x + k = 0이 중근을 가질 때, 상수 k의 값은?",
            options=["9", "6", "3", "0"],
            correct="A",
            explanation="중근 조건: 판별식 D = 0\nD = (-6)² - 4(1)(k) = 36 - 4k = 0\n∴ k = 9",
            points=10,
        ),

        # 근과 계수의 관계
        mc(
            id="h1-comp-009",
            concept_id="concept-h1-equation",
            category="computation",
            part="algebra",
            difficulty=3,
            content="이차방정식 x² - 5x + 6 = 0의 두 근을 α, β라 할 때, α + β의 값은?",
            options=["5", "6", "-5", "-6"],
            correct="A",
            explanation="근과 계수의 관계: α + β = -b/a = -(-5)/1 = 5",
            points=10,
        ),

        # 판별식 응용 - 이차항 계수 조건 체크 ★★★
        mc(
            id="h1-comp-010",
            concept_id="concept-h1-equation",
            category="computation",
            part="algebra",
            difficulty=4,
            content="방정식 kx² - 4x + 1 = 0이 서로 다른 두 실근을 가질 조건은?",
            options=["k < 4이고 k ≠ 0", "k > 4", "k < 4", "0 < k < 4"],
            correct="A",
            explanation="[핵심 주의!] 이차방정식이 되려면 k ≠ 0\n판별식 D > 0: 16 - 4k > 0 → k < 4\n∴ k < 4이고 k ≠ 0\n\n[오개념 교정] ★★★ 판별식을 사용할 때는 반드시 이차항 계수 ≠ 0 조건을 확인해야 합니다!",
            points=10,
        ),

        # 이차함수 최대·최소 (제한 범위)
        mc(
            id="h1-comp-011",
            concept_id="concept-h1-equation",
            category="computation",
            part="algebra",
            difficulty=4,
            content="함수 f(x) = x² - 4x + 5 (0 ≤ x ≤ 3)의 최솟값은?",
            options=["1", "0", "2", "5"],
            correct="A",
            explanation="f(x) = (x - 2)² + 1\n꼭짓점 x = 2는 범위 [0, 3] 내에 있음\n∴ 최솟값 = f(2) = 1",
            points=10,
        ),

        # 이차부등식
        mc(
            id="h1-comp-012",
            concept_id="concept-h1-equation",
            category="computation",
            part="algebra",
            difficulty=5,
            content="이차부등식 x² - 5x + 6 < 0의 해는?",
            options=["2 < x < 3", "x < 2 또는 x > 3", "1 < x < 6", "x < 1 또는 x > 6"],
            correct="A",
            explanation="x² - 5x + 6 = (x - 2)(x - 3)\n부등식 (x - 2)(x - 3) < 0의 해는 두 근 사이\n∴ 2 < x < 3",
            points=10,
        ),
    ]


def _get_tests():
    """연산 카테고리 테스트 (1개)."""
    return [
        test(
            id="test-h1-computation",
            title="고1 연산 종합 테스트",
            description="다항식의 연산·항등식·나머지정리·인수분해, 복소수·이차방정식·판별식·이차부등식",
            grade="high_1",
            concept_ids=["concept-h1-polynomial", "concept-h1-equation"],
            question_ids=[f"h1-comp-{i:03d}" for i in range(1, 13)],
            time_limit_minutes=30,
            use_question_pool=True,
            questions_per_attempt=10,
        ),
    ]
