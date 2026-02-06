"""공통수학2 연산 카테고리 - 도형의 방정식 (2022 개정 교육과정)."""
from app.seeds._base import mc, concept, test


def get_computation_data() -> dict:
    """연산 카테고리 데이터 반환."""
    return {
        "concepts": _get_concepts(),
        "questions": _get_questions(),
        "tests": _get_tests(),
    }


def _get_concepts():
    """연산 개념 정의 (4개)."""
    return [
        concept(
            id="concept-h2-plane-coord",
            name="평면좌표",
            grade="high_1",
            category="computation",
            part="calc",
            description="두 점 사이의 거리, 내분점, 무게중심 (2022 개정: 외분점 삭제)"
        ),
        concept(
            id="concept-h2-line",
            name="직선의 방정식",
            grade="high_1",
            category="computation",
            part="algebra",
            description="직선의 결정조건, 평행과 수직, 점과 직선 사이의 거리"
        ),
        concept(
            id="concept-h2-circle",
            name="원의 방정식",
            grade="high_1",
            category="computation",
            part="algebra",
            description="원의 방정식(표준형·일반형), 원과 직선의 위치 관계, 접선의 방정식"
        ),
        concept(
            id="concept-h2-transform",
            name="도형의 이동",
            grade="high_1",
            category="computation",
            part="geo",
            description="평행이동, 대칭이동(x축·y축·원점·y=x)"
        ),
    ]


def _get_questions():
    """연산 문제 목록 (12문제: 평면좌표 3 + 직선 3 + 원 3 + 이동 3)."""
    return [
        # ========== 1. 평면좌표 (3문제) ==========

        # 두 점 사이의 거리 - 기본
        mc(
            id="h2-comp-001",
            concept_id="concept-h2-plane-coord",
            category="computation",
            part="calc",
            difficulty=3,
            content="두 점 A(1, 3), B(5, 7) 사이의 거리는?",
            options=["4√2", "4", "8", "√32"],
            correct="A",
            explanation="거리 공식: d = √[(x₂ - x₁)² + (y₂ - y₁)²]\nd = √[(5 - 1)² + (7 - 3)²] = √(16 + 16) = √32 = 4√2",
            points=10,
        ),

        # 내분점 - 기본
        mc(
            id="h2-comp-002",
            concept_id="concept-h2-plane-coord",
            category="computation",
            part="calc",
            difficulty=5,
            content="두 점 A(1, 2), B(5, 8)을 1:3으로 내분하는 점의 좌표는?",
            options=["(2, 7/2)", "(3, 5)", "(4, 6)", "(2, 4)"],
            correct="A",
            explanation="내분점 공식: ((m×x₂ + n×x₁)/(m+n), (m×y₂ + n×y₁)/(m+n))\n1:3 내분점 = ((1×5 + 3×1)/(1+3), (1×8 + 3×2)/(1+3))\n= (8/4, 14/4) = (2, 7/2) = (2, 3.5)\n\n[오개념 교정] 내분점 공식에서 m:n의 위치를 혼동하지 않도록 주의합니다.",
            points=10,
        ),

        # 무게중심
        mc(
            id="h2-comp-003",
            concept_id="concept-h2-plane-coord",
            category="computation",
            part="calc",
            difficulty=7,
            content="삼각형의 세 꼭짓점이 A(1, 2), B(3, 6), C(5, 4)일 때, 무게중심의 좌표는?",
            options=["(3, 4)", "(3, 3)", "(4, 4)", "(2, 4)"],
            correct="A",
            explanation="무게중심 공식: ((x₁ + x₂ + x₃)/3, (y₁ + y₂ + y₃)/3)\n= ((1 + 3 + 5)/3, (2 + 6 + 4)/3) = (9/3, 12/3) = (3, 4)\n\n[핵심 개념] 무게중심은 세 중선의 교점으로, 좌표의 산술평균입니다.",
            points=10,
        ),

        # ========== 2. 직선의 방정식 (3문제) ==========

        # 직선의 방정식 - 기본
        mc(
            id="h2-comp-004",
            concept_id="concept-h2-line",
            category="computation",
            part="algebra",
            difficulty=3,
            content="기울기가 2이고 점 (1, 3)을 지나는 직선의 방정식은?",
            options=["y = 2x + 1", "y = 2x - 1", "y = 2x + 3", "y = x + 2"],
            correct="A",
            explanation="점-기울기 형식: y - y₁ = m(x - x₁)\ny - 3 = 2(x - 1)\ny - 3 = 2x - 2\ny = 2x + 1",
            points=10,
        ),

        # 평행과 수직
        mc(
            id="h2-comp-005",
            concept_id="concept-h2-line",
            category="computation",
            part="algebra",
            difficulty=5,
            content="두 직선 y = 2x + 1과 y = -1/2·x + 3이 이루는 관계는?",
            options=["수직", "평행", "일치", "만난다(수직 아님)"],
            correct="A",
            explanation="두 직선의 기울기: m₁ = 2, m₂ = -1/2\nm₁ × m₂ = 2 × (-1/2) = -1\n기울기의 곱이 -1이므로 두 직선은 수직입니다.\n\n[오개념 교정] 평행: m₁ = m₂, 수직: m₁ × m₂ = -1",
            points=10,
        ),

        # 점과 직선 사이의 거리
        mc(
            id="h2-comp-006",
            concept_id="concept-h2-line",
            category="computation",
            part="algebra",
            difficulty=8,
            content="점 (3, 4)와 직선 3x + 4y - 5 = 0 사이의 거리는?",
            options=["4", "3", "5", "20/5"],
            correct="A",
            explanation="점과 직선 사이의 거리 공식:\nd = |ax₁ + by₁ + c| / √(a² + b²)\n= |3×3 + 4×4 - 5| / √(3² + 4²)\n= |9 + 16 - 5| / √(9 + 16)\n= |20| / √25 = 20 / 5 = 4\n\n[핵심 공식] ax + by + c = 0과 점 (x₁, y₁)의 거리는 |ax₁ + by₁ + c| / √(a² + b²)",
            points=10,
        ),

        # ========== 3. 원의 방정식 (3문제) ==========

        # 원의 방정식 - 표준형
        mc(
            id="h2-comp-007",
            concept_id="concept-h2-circle",
            category="computation",
            part="algebra",
            difficulty=4,
            content="중심이 (2, 3)이고 반지름이 5인 원의 방정식은?",
            options=[
                "(x - 2)² + (y - 3)² = 25",
                "(x + 2)² + (y + 3)² = 25",
                "(x - 2)² + (y - 3)² = 5",
                "x² + y² = 25"
            ],
            correct="A",
            explanation="원의 표준형: (x - a)² + (y - b)² = r²\n중심 (2, 3), 반지름 5를 대입:\n(x - 2)² + (y - 3)² = 5² = 25",
            points=10,
        ),

        # 원의 방정식 - 일반형 → 표준형 변환
        mc(
            id="h2-comp-008",
            concept_id="concept-h2-circle",
            category="computation",
            part="algebra",
            difficulty=6,
            content="원 x² + y² - 6x + 4y - 12 = 0의 중심과 반지름은?",
            options=[
                "중심 (3, -2), 반지름 5",
                "중심 (-3, 2), 반지름 5",
                "중심 (3, -2), 반지름 √13",
                "중심 (6, -4), 반지름 12"
            ],
            correct="A",
            explanation="완전제곱식으로 변환:\nx² - 6x + y² + 4y = 12\n(x² - 6x + 9) + (y² + 4y + 4) = 12 + 9 + 4\n(x - 3)² + (y + 2)² = 25\n∴ 중심 (3, -2), 반지름 √25 = 5\n\n[오개념 교정] 일반형 x² + y² + Dx + Ey + F = 0에서 중심은 (-D/2, -E/2)입니다.",
            points=10,
        ),

        # 원의 접선
        mc(
            id="h2-comp-009",
            concept_id="concept-h2-circle",
            category="computation",
            part="algebra",
            difficulty=8,
            content="원 x² + y² = 5 위의 점 (1, 2)에서의 접선의 방정식은?",
            options=["x + 2y = 5", "x - 2y = 5", "2x + y = 5", "x + 2y = 1"],
            correct="A",
            explanation="원 x² + y² = r² 위의 점 (x₁, y₁)에서의 접선: x₁·x + y₁·y = r²\n점 (1, 2)를 대입:\n1·x + 2·y = 5\n∴ x + 2y = 5\n\n[검증] 점 (1, 2)가 원 위에 있는지: 1² + 2² = 1 + 4 = 5 ✓\n[핵심 공식] 접선의 방정식은 원의 방정식에서 x² → x₁·x, y² → y₁·y로 치환",
            points=10,
        ),

        # ========== 4. 도형의 이동 (3문제) ==========

        # 평행이동 - 점
        mc(
            id="h2-comp-010",
            concept_id="concept-h2-transform",
            category="computation",
            part="geo",
            difficulty=3,
            content="점 (2, 3)을 x축 방향으로 3, y축 방향으로 -2만큼 평행이동한 점의 좌표는?",
            options=["(5, 1)", "(5, 5)", "(-1, 1)", "(2, 1)"],
            correct="A",
            explanation="평행이동: (x, y) → (x + a, y + b)\n(2, 3) → (2 + 3, 3 + (-2)) = (5, 1)",
            points=10,
        ),

        # 평행이동 - 직선
        mc(
            id="h2-comp-011",
            concept_id="concept-h2-transform",
            category="computation",
            part="geo",
            difficulty=6,
            content="직선 y = 2x + 3을 x축 방향으로 1, y축 방향으로 -2만큼 평행이동한 직선의 방정식은?",
            options=["y = 2x - 1", "y = 2x + 1", "y = 2x + 5", "y = 2x - 3"],
            correct="A",
            explanation="평행이동 역변환: (x, y) → (x - a, y - b)\n원래 방정식에 (x - 1, y + 2)를 대입:\ny + 2 = 2(x - 1) + 3\ny + 2 = 2x - 2 + 3\ny = 2x - 1\n\n[오개념 교정] 도형 f(x, y) = 0을 (a, b)만큼 평행이동하면 f(x - a, y - b) = 0",
            points=10,
        ),

        # 대칭이동 - y = x
        mc(
            id="h2-comp-012",
            concept_id="concept-h2-transform",
            category="computation",
            part="geo",
            difficulty=8,
            content="점 (3, -4)를 직선 y = x에 대해 대칭이동한 점의 좌표는?",
            options=["(-4, 3)", "(4, -3)", "(-3, 4)", "(3, 4)"],
            correct="A",
            explanation="y = x에 대한 대칭이동: (x, y) → (y, x)\n(3, -4) → (-4, 3)\n\n[핵심 정리]\n- x축 대칭: (x, y) → (x, -y)\n- y축 대칭: (x, y) → (-x, y)\n- 원점 대칭: (x, y) → (-x, -y)\n- y = x 대칭: (x, y) → (y, x)",
            points=10,
        ),
    ]


def _get_tests():
    """연산 카테고리 테스트 (1개)."""
    return [
        test(
            id="test-h2-geometry-eq",
            title="공통수학2 도형의 방정식",
            description="평면좌표, 직선, 원, 도형의 이동",
            grade="high_1",
            concept_ids=[
                "concept-h2-plane-coord",
                "concept-h2-line",
                "concept-h2-circle",
                "concept-h2-transform"
            ],
            question_ids=[f"h2-comp-{i:03d}" for i in range(1, 13)],
            time_limit_minutes=20,
            use_question_pool=True,
            questions_per_attempt=8,
        ),
    ]
