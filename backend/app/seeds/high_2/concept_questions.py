"""고2 개념 카테고리 - 집합과 명제, 함수 (2022 개정 교육과정 - 공통수학2)."""
from app.seeds._base import mc, concept, test


def get_concept_data() -> dict:
    """개념 카테고리 데이터 반환."""
    return {
        "concepts": _get_concepts(),
        "questions": _get_questions(),
        "tests": _get_tests(),
    }


def _get_concepts():
    """개념 정의 (6개)."""
    return [
        # 2단원: 집합과 명제
        concept(
            id="concept-h2-set",
            name="집합",
            grade="high_2",
            category="concept",
            part="data",
            description="집합의 정의, ∈과 ⊂ 구분, 교집합/합집합/여집합/차집합, 드 모르간의 법칙, 포함-배제 원리"
        ),
        concept(
            id="concept-h2-proposition",
            name="명제",
            grade="high_2",
            category="concept",
            part="data",
            description="명제, 조건과 진리집합, 역/대우, 충분조건/필요조건"
        ),
        concept(
            id="concept-h2-abs-inequality",
            name="절대부등식",
            grade="high_2",
            category="concept",
            part="algebra",
            description="A²≥0, AM-GM(산술평균≥기하평균), 양수 조건, 등호 성립"
        ),

        # 3단원: 함수
        concept(
            id="concept-h2-function",
            name="함수의 뜻과 그래프",
            grade="high_2",
            category="concept",
            part="func",
            description="함수의 정의, 일대일 함수, 일대일 대응"
        ),
        concept(
            id="concept-h2-composite",
            name="합성함수와 역함수",
            grade="high_2",
            category="concept",
            part="func",
            description="합성함수 교환법칙 불성립, 역함수 존재 조건(일대일 대응), y=x 대칭"
        ),
        concept(
            id="concept-h2-rational-irrational",
            name="유리함수와 무리함수",
            grade="high_2",
            category="concept",
            part="func",
            description="유리함수 y=k/(x-p)+q 점근선, 무리함수 y=√(ax+b) 정의역, 무연근"
        ),
    ]


def _get_questions():
    """개념 문제 목록 (18문제: 집합 3 + 명제 3 + 절대부등식 3 + 함수 3 + 합성/역함수 3 + 유리/무리함수 3)."""
    return [
        # ========== 2단원: 집합과 명제 (9문제) ==========

        # 집합 (3문제)
        mc(
            id="h2-conc-001",
            concept_id="concept-h2-set",
            category="concept",
            part="data",
            difficulty=3,
            content="두 집합 A = {1, 2, 3, 4, 5}, B = {3, 4, 5, 6, 7}에 대하여 A ∩ B를 구하시오.",
            options=["{3, 4, 5}", "{1, 2, 3, 4, 5, 6, 7}", "{1, 2}", "{6, 7}"],
            correct="A",
            explanation="교집합 A ∩ B는 A와 B에 공통으로 속하는 원소의 집합:\nA ∩ B = {3, 4, 5}",
            points=10,
        ),

        mc(
            id="h2-conc-002",
            concept_id="concept-h2-set",
            category="concept",
            part="data",
            difficulty=6,
            content="전체집합 U = {1, 2, 3, 4, 5, 6, 7, 8}, A = {1, 3, 5, 7}, B = {2, 3, 5, 8}일 때, (A ∪ B)ᶜ를 구하시오.",
            options=["{4, 6}", "{1, 2, 3, 5, 7, 8}", "{3, 5}", "∅"],
            correct="A",
            explanation="먼저 A ∪ B를 구함:\nA ∪ B = {1, 2, 3, 5, 7, 8}\n\n여집합 (A ∪ B)ᶜ는 U에서 A ∪ B를 뺀 집합:\n(A ∪ B)ᶜ = U - (A ∪ B) = {4, 6}",
            points=10,
        ),

        mc(
            id="h2-conc-003",
            concept_id="concept-h2-set",
            category="concept",
            part="data",
            difficulty=8,
            content="집합 A = {1, 2, {1, 2}}에 대하여 다음 중 옳은 것은?",
            options=["{1, 2} ∈ A", "{1, 2} ⊂ A", "1 ⊄ A", "{1} ∈ A"],
            correct="A",
            explanation="집합 A의 원소는 1, 2, {1, 2} 세 개입니다.\n\n{1, 2}는 A의 원소로 포함되어 있으므로 {1, 2} ∈ A가 참입니다.\n\n[오개념 교정] ★★★ ∈(원소)과 ⊂(부분집합)을 구분해야 합니다!\n- {1, 2} ∈ A: 참 (원소로 포함)\n- {1, 2} ⊂ A: 거짓 ({1, 2}의 모든 원소가 A에 속해야 하는데, 집합 {1, 2} 자체는 A의 원소이지 1과 2를 직접 포함하는 것은 아님)",
            points=10,
        ),

        # 명제 (3문제)
        mc(
            id="h2-conc-004",
            concept_id="concept-h2-proposition",
            category="concept",
            part="data",
            difficulty=4,
            content="명제 'x = 1이면 x² = 1이다'에서 x = 1은 x² = 1이기 위한 무슨 조건인가?",
            options=["충분조건", "필요조건", "필요충분조건", "조건이 아님"],
            correct="A",
            explanation="x = 1의 진리집합: P = {1}\nx² = 1의 진리집합: Q = {-1, 1}\n\nP ⊂ Q이므로 x = 1은 x² = 1이기 위한 충분조건입니다.\n(x = 1이면 항상 x² = 1이지만, x² = 1이라고 x = 1인 것은 아님 (x = -1도 가능))",
            points=10,
        ),

        mc(
            id="h2-conc-005",
            concept_id="concept-h2-proposition",
            category="concept",
            part="data",
            difficulty=6,
            content="명제 'p → q'의 대우는?",
            options=["¬q → ¬p", "q → p", "¬p → ¬q", "p → ¬q"],
            correct="A",
            explanation="명제 'p → q'의 대우는 '¬q → ¬p'입니다.\n\n참고:\n- 역(converse): q → p\n- 이(inverse): ¬p → ¬q\n- 대우(contrapositive): ¬q → ¬p\n\n원명제와 대우는 진리값이 항상 같습니다.",
            points=10,
        ),

        mc(
            id="h2-conc-006",
            concept_id="concept-h2-proposition",
            category="concept",
            part="data",
            difficulty=8,
            content="명제 'x² = 4이면 x = 2이다'에 대하여 다음 중 참인 것은?",
            options=["역은 참이다", "원명제가 참이다", "대우가 참이다", "이가 참이다"],
            correct="A",
            explanation="원명제: x² = 4 → x = 2 (거짓, x = -2일 수도 있음)\n역: x = 2 → x² = 4 (참)\n이: x² ≠ 4 → x ≠ 2 (거짓, x = -2일 때 x² = 4이므로 x² ≠ 4이면 x ≠ 2가 성립하지 않음)\n대우: x ≠ 2 → x² ≠ 4 (거짓, x = -2 반례)\n\n[오개념 교정] ★★★ 원명제와 대우는 진리값이 같고, 역과 이는 진리값이 같습니다.\n그러나 원명제와 역은 진리값이 다를 수 있습니다!",
            points=10,
        ),

        # 절대부등식 (3문제)
        mc(
            id="h2-conc-007",
            concept_id="concept-h2-abs-inequality",
            category="concept",
            part="algebra",
            difficulty=4,
            content="a > 0, b > 0일 때, (a + b) / 2와 √(ab)의 대소 관계는?",
            options=["(a + b) / 2 ≥ √(ab)", "(a + b) / 2 ≤ √(ab)", "(a + b) / 2 = √(ab)", "비교 불가"],
            correct="A",
            explanation="산술평균-기하평균 부등식 (AM-GM 부등식):\n(a + b) / 2 ≥ √(ab)\n\n등호는 a = b일 때 성립합니다.",
            points=10,
        ),

        mc(
            id="h2-conc-008",
            concept_id="concept-h2-abs-inequality",
            category="concept",
            part="algebra",
            difficulty=7,
            content="x > 0일 때, x + 4/x의 최솟값은?",
            options=["4", "2", "8", "1"],
            correct="A",
            explanation="AM-GM 부등식 적용:\nx + 4/x ≥ 2√(x × 4/x) = 2√4 = 2 × 2 = 4\n\n등호 조건: x = 4/x → x² = 4 → x = 2 (x > 0)\n\n∴ 최솟값은 4 (x = 2일 때)",
            points=10,
        ),

        mc(
            id="h2-conc-009",
            concept_id="concept-h2-abs-inequality",
            category="concept",
            part="algebra",
            difficulty=9,
            content="a > 0, b > 0이고 a + b = 4일 때, 1/a + 1/b의 최솟값은?",
            options=["1", "2", "1/2", "4"],
            correct="A",
            explanation="1/a + 1/b = (b + a) / (ab) = (a + b) / (ab) = 4 / (ab)\n\nAM-GM 부등식에서:\n(a + b) / 2 ≥ √(ab)\n4 / 2 ≥ √(ab)\n2 ≥ √(ab)\nab ≤ 4\n\n따라서 1/a + 1/b = 4 / (ab) ≥ 4 / 4 = 1\n\n등호 조건: a = b일 때 → a = b = 2\n검증: 1/2 + 1/2 = 1 ✓\n\n∴ 최솟값은 1",
            points=10,
        ),

        # ========== 3단원: 함수 (9문제) ==========

        # 함수의 뜻과 그래프 (3문제)
        mc(
            id="h2-conc-010",
            concept_id="concept-h2-function",
            category="concept",
            part="func",
            difficulty=3,
            content="다음 중 함수인 것은?",
            options=["x = 2일 때 y = 3, y = 4인 관계", "y = 2x + 1", "x² + y² = 1", "x = y²"],
            correct="B",
            explanation="함수의 정의: 정의역의 각 원소에 대하여 치역의 원소가 오직 하나 대응되는 관계\n\nA. x = 2일 때 y가 3, 4 두 개 → 함수 아님\nB. y = 2x + 1 → 각 x에 대해 y가 하나씩 대응 → 함수 ✓\nC. x² + y² = 1 → x = 0일 때 y = ±1 (두 개) → 함수 아님\nD. x = y² → y = 0일 때 x = 0이지만, x = 1일 때 y = ±1 (두 개)... 아니다, 이것은 y를 x의 함수로 보면 y = ±√x이므로 함수 아님\n\n[오개념 교정] ★★★ 세로선 판별법: 수직선이 그래프와 두 점 이상에서 만나면 함수가 아닙니다!",
            points=10,
        ),

        mc(
            id="h2-conc-011",
            concept_id="concept-h2-function",
            category="concept",
            part="func",
            difficulty=5,
            content="함수 f: {1, 2, 3} → {a, b, c}에서 f(1) = a, f(2) = a, f(3) = b일 때, 이 함수의 치역은?",
            options=["{a, b}", "{a, b, c}", "{1, 2, 3}", "{a}"],
            correct="A",
            explanation="치역(range)은 실제로 대응된 y값들의 집합입니다.\n\nf(1) = a\nf(2) = a\nf(3) = b\n\n∴ 치역 = {a, b}\n\n참고: 공역(codomain)은 {a, b, c}이지만, 치역은 {a, b}입니다.\nc는 공역의 원소이지만 치역의 원소는 아닙니다.",
            points=10,
        ),

        mc(
            id="h2-conc-012",
            concept_id="concept-h2-function",
            category="concept",
            part="func",
            difficulty=7,
            content="다음 중 일대일 함수이지만 일대일 대응이 아닌 예는?",
            options=["f: {1, 2} → {a, b, c}에서 f(1) = a, f(2) = b", "f: {1, 2} → {a, b}에서 f(1) = a, f(2) = b", "f: {1, 2} → {a, b}에서 f(1) = a, f(2) = a", "f: {1, 2, 3} → {a, b}에서 f(1) = a, f(2) = a, f(3) = b"],
            correct="A",
            explanation="일대일 함수: 서로 다른 x에 대해 f(x)가 서로 다름 (x₁ ≠ x₂ → f(x₁) ≠ f(x₂))\n일대일 대응: 일대일 함수이면서 치역 = 공역 (전사함수)\n\nA. f(1) = a, f(2) = b → 일대일 함수 ✓, 치역 = {a, b} ≠ 공역 {a, b, c} → 일대일 대응 ✗\nB. 일대일 함수이면서 일대일 대응 ✓\nC. f(1) = f(2) = a → 일대일 함수 ✗\nD. f(1) = f(2) = a → 일대일 함수 ✗\n\n[오개념 교정] ★★★ 일대일 대응 = 일대일 함수 + 전사함수 (치역 = 공역)",
            points=10,
        ),

        # 합성함수와 역함수 (3문제)
        mc(
            id="h2-conc-013",
            concept_id="concept-h2-composite",
            category="concept",
            part="func",
            difficulty=4,
            content="f(x) = 2x + 1, g(x) = x²일 때, (f ∘ g)(2)의 값은?",
            options=["9", "25", "5", "17"],
            correct="A",
            explanation="합성함수 (f ∘ g)(x) = f(g(x))\n\n(f ∘ g)(2) = f(g(2))\n            = f(2²)\n            = f(4)\n            = 2 × 4 + 1\n            = 9",
            points=10,
        ),

        mc(
            id="h2-conc-014",
            concept_id="concept-h2-composite",
            category="concept",
            part="func",
            difficulty=6,
            content="함수 f(x) = 3x - 2의 역함수 f⁻¹(x)는?",
            options=["(x + 2) / 3", "(x - 2) / 3", "3x + 2", "(2 - x) / 3"],
            correct="A",
            explanation="y = 3x - 2에서 x를 y로 나타냄:\ny = 3x - 2\ny + 2 = 3x\nx = (y + 2) / 3\n\n∴ f⁻¹(x) = (x + 2) / 3\n\n검증: f(f⁻¹(x)) = f((x + 2) / 3) = 3 × (x + 2) / 3 - 2 = x + 2 - 2 = x ✓",
            points=10,
        ),

        mc(
            id="h2-conc-015",
            concept_id="concept-h2-composite",
            category="concept",
            part="func",
            difficulty=8,
            content="f(x) = x + 1, g(x) = 2x일 때, (f ∘ g)(1)과 (g ∘ f)(1)을 비교하시오.",
            options=["(f ∘ g)(1) = 3, (g ∘ f)(1) = 4로 서로 다르다", "(f ∘ g)(1) = (g ∘ f)(1) = 3", "(f ∘ g)(1) = (g ∘ f)(1) = 4", "(f ∘ g)(1) = 4, (g ∘ f)(1) = 3으로 서로 다르다"],
            correct="A",
            explanation="(f ∘ g)(1) = f(g(1)) = f(2 × 1) = f(2) = 2 + 1 = 3\n(g ∘ f)(1) = g(f(1)) = g(1 + 1) = g(2) = 2 × 2 = 4\n\n∴ (f ∘ g)(1) = 3 ≠ 4 = (g ∘ f)(1)\n\n[오개념 교정] ★★★ 합성함수는 교환법칙이 성립하지 않습니다! f ∘ g ≠ g ∘ f",
            points=10,
        ),

        # 유리함수와 무리함수 (3문제)
        mc(
            id="h2-conc-016",
            concept_id="concept-h2-rational-irrational",
            category="concept",
            part="func",
            difficulty=4,
            content="유리함수 y = 3 / (x - 1) + 2의 점근선은?",
            options=["x = 1, y = 2", "x = -1, y = 2", "x = 1, y = -2", "x = 0, y = 0"],
            correct="A",
            explanation="유리함수 y = k / (x - p) + q의 점근선:\n- 수직 점근선: x = p\n- 수평 점근선: y = q\n\ny = 3 / (x - 1) + 2에서:\n- 수직 점근선: x = 1 (분모가 0)\n- 수평 점근선: y = 2 (x → ±∞일 때 y → 2)",
            points=10,
        ),

        mc(
            id="h2-conc-017",
            concept_id="concept-h2-rational-irrational",
            category="concept",
            part="func",
            difficulty=7,
            content="무리함수 y = √(2x - 4)의 정의역은?",
            options=["x ≥ 2", "x > 2", "x ≥ -2", "x > -2"],
            correct="A",
            explanation="무리함수 y = √(f(x))의 정의역: f(x) ≥ 0\n\n2x - 4 ≥ 0\n2x ≥ 4\nx ≥ 2\n\n∴ 정의역: x ≥ 2 또는 [2, ∞)",
            points=10,
        ),

        mc(
            id="h2-conc-018",
            concept_id="concept-h2-rational-irrational",
            category="concept",
            part="func",
            difficulty=9,
            content="방정식 √(x + 3) = x - 3의 해는?",
            options=["x = 6", "x = 1", "x = 1, x = 6", "해가 없다"],
            correct="A",
            explanation="양변을 제곱:\nx + 3 = (x - 3)²\nx + 3 = x² - 6x + 9\n0 = x² - 7x + 6\n0 = (x - 1)(x - 6)\nx = 1 또는 x = 6\n\n무연근 검증:\nx = 1: √(1 + 3) = √4 = 2, 1 - 3 = -2 → 2 ≠ -2 (무연근!) ✗\nx = 6: √(6 + 3) = √9 = 3, 6 - 3 = 3 → 3 = 3 ✓\n\n∴ x = 6\n\n[오개념 교정] ★★★ 무리방정식을 풀 때는 반드시 무연근을 확인해야 합니다!\n양변을 제곱하면 해가 아닌 값이 생길 수 있습니다.",
            points=10,
        ),
    ]


def _get_tests():
    """개념 카테고리 테스트 (2개)."""
    return [
        test(
            id="test-h2-set-proposition",
            title="공통수학2 집합과 명제",
            description="집합(교집합/합집합/여집합), 명제(역/대우/충분조건), 절대부등식(AM-GM)",
            grade="high_2",
            concept_ids=["concept-h2-set", "concept-h2-proposition", "concept-h2-abs-inequality"],
            question_ids=[f"h2-conc-{i:03d}" for i in range(1, 10)],
            time_limit_minutes=15,
            use_question_pool=True,
            questions_per_attempt=7,
        ),
        test(
            id="test-h2-function",
            title="공통수학2 함수",
            description="함수의 정의와 그래프, 합성함수와 역함수, 유리함수와 무리함수",
            grade="high_2",
            concept_ids=["concept-h2-function", "concept-h2-composite", "concept-h2-rational-irrational"],
            question_ids=[f"h2-conc-{i:03d}" for i in range(10, 19)],
            time_limit_minutes=15,
            use_question_pool=True,
            questions_per_attempt=7,
        ),
    ]
