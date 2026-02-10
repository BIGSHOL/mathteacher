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
    """개념 목록 반환."""
    return [
        concept(
            id="h1-2-1-1",
            name="평면좌표",
            grade="high_1",
            category="computation",
            part="calc",
            description="두 점 사이의 거리, 내분점, 무게중심 (2022 개정: 외분점 삭제)"
        ),
        concept(
            id="h1-2-1-2",
            name="직선의 방정식",
            grade="high_1",
            category="computation",
            part="algebra",
            description="직선의 결정조건, 평행과 수직, 점과 직선 사이의 거리"
        ),
        concept(
            id="h1-2-1-3",
            name="원의 방정식",
            grade="high_1",
            category="computation",
            part="algebra",
            description="원의 방정식(표준형·일반형), 원과 직선의 위치 관계, 접선의 방정식"
        ),
        concept(
            id="h1-2-1-4",
            name="도형의 이동",
            grade="high_1",
            category="computation",
            part="geo",
            description="평행이동, 대칭이동(x축·y축·원점·y=x)"
        ),
    ]


def _get_questions():
    """연산 문제 목록 (20문제: 각 개념당 5문제)."""
    return [
        # ========== 1. 평면좌표 (5문제) ==========

        # 두 점 사이의 거리 - 기본
        mc(
            id="h1-2-1-1-co-001",
            concept_id="h1-2-1-1",
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
            id="h1-2-1-1-co-002",
            concept_id="h1-2-1-1",
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
            id="h1-2-1-1-co-003",
            concept_id="h1-2-1-1",
            category="computation",
            part="calc",
            difficulty=7,
            content="삼각형의 세 꼭짓점이 A(1, 2), B(3, 6), C(5, 4)일 때, 무게중심의 좌표는?",
            options=["(3, 4)", "(3, 3)", "(4, 4)", "(2, 4)"],
            correct="A",
            explanation="무게중심 공식: ((x₁ + x₂ + x₃)/3, (y₁ + y₂ + y₃)/3)\n= ((1 + 3 + 5)/3, (2 + 6 + 4)/3) = (9/3, 12/3) = (3, 4)\n\n[핵심 개념] 무게중심은 세 중선의 교점으로, 좌표의 산술평균입니다.",
            points=10,
        ),

        # ========== 2. 직선의 방정식 (5문제) ==========

        # 직선의 방정식 - 기본
        mc(
            id="h1-2-1-2-co-001",
            concept_id="h1-2-1-2",
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
            id="h1-2-1-2-co-002",
            concept_id="h1-2-1-2",
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
            id="h1-2-1-2-co-003",
            concept_id="h1-2-1-2",
            category="computation",
            part="algebra",
            difficulty=8,
            content="점 (3, 4)와 직선 3x + 4y - 5 = 0 사이의 거리는?",
            options=["4", "3", "5", "20/5"],
            correct="A",
            explanation="점과 직선 사이의 거리 공식:\nd = |ax₁ + by₁ + c| / √(a² + b²)\n= |3×3 + 4×4 - 5| / √(3² + 4²)\n= |9 + 16 - 5| / √(9 + 16)\n= |20| / √25 = 20 / 5 = 4\n\n[핵심 공식] ax + by + c = 0과 점 (x₁, y₁)의 거리는 |ax₁ + by₁ + c| / √(a² + b²)",
            points=10,
        ),

        # ========== 3. 원의 방정식 (5문제) ==========

        # 원의 방정식 - 표준형
        mc(
            id="h1-2-1-3-co-001",
            concept_id="h1-2-1-3",
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
            id="h1-2-1-3-co-002",
            concept_id="h1-2-1-3",
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
            id="h1-2-1-3-co-003",
            concept_id="h1-2-1-3",
            category="computation",
            part="algebra",
            difficulty=8,
            content="원 x² + y² = 5 위의 점 (1, 2)에서의 접선의 방정식은?",
            options=["x + 2y = 5", "x - 2y = 5", "2x + y = 5", "x + 2y = 1"],
            correct="A",
            explanation="원 x² + y² = r² 위의 점 (x₁, y₁)에서의 접선: x₁·x + y₁·y = r²\n점 (1, 2)를 대입:\n1·x + 2·y = 5\n∴ x + 2y = 5\n\n[검증] 점 (1, 2)가 원 위에 있는지: 1² + 2² = 1 + 4 = 5 ✓\n[핵심 공식] 접선의 방정식은 원의 방정식에서 x² → x₁·x, y² → y₁·y로 치환",
            points=10,
        ),

        # ========== 4. 도형의 이동 (5문제) ==========

        # 평행이동 - 점
        mc(
            id="h1-2-1-4-co-001",
            concept_id="h1-2-1-4",
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
            id="h1-2-1-4-co-002",
            concept_id="h1-2-1-4",
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
            id="h1-2-1-4-co-003",
            concept_id="h1-2-1-4",
            category="computation",
            part="geo",
            difficulty=8,
            content="점 (3, -4)를 직선 y = x에 대해 대칭이동한 점의 좌표는?",
            options=["(-4, 3)", "(4, -3)", "(-3, 4)", "(3, 4)"],
            correct="A",
            explanation="y = x에 대한 대칭이동: (x, y) → (y, x)\n(3, -4) → (-4, 3)\n\n[핵심 정리]\n- x축 대칭: (x, y) → (x, -y)\n- y축 대칭: (x, y) → (-x, y)\n- 원점 대칭: (x, y) → (-x, -y)\n- y = x 대칭: (x, y) → (y, x)",
            points=10,
        ),

        # ========== 추가 문제 (각 개념당 5개 달성) ==========

        # 평면좌표 - 거리 응용
        mc(
            id="h1-2-1-1-co-004",
            concept_id="h1-2-1-1",
            category="computation",
            part="calc",
            difficulty=6,
            content="두 점 A(-2, 1), B(4, 9) 사이의 거리는?",
            options=["10", "8", "√100", "6"],
            correct="A",
            explanation="거리 공식: d = √[(x₂ - x₁)² + (y₂ - y₁)²]\nd = √[(4 - (-2))² + (9 - 1)²] = √[(6)² + (8)²] = √(36 + 64) = √100 = 10",
            points=10,
        ),

        # 평면좌표 - 내분점 응용
        mc(
            id="h1-2-1-1-co-005",
            concept_id="h1-2-1-1",
            category="computation",
            part="calc",
            difficulty=8,
            content="두 점 A(-1, 3), B(5, 9)를 2:1로 내분하는 점의 좌표는?",
            options=["(3, 7)", "(2, 6)", "(4, 8)", "(1, 5)"],
            correct="A",
            explanation="내분점 공식: ((m×x₂ + n×x₁)/(m+n), (m×y₂ + n×y₁)/(m+n))\n2:1 내분점 = ((2×5 + 1×(-1))/(2+1), (2×9 + 1×3)/(2+1))\n= ((10 - 1)/3, (18 + 3)/3) = (9/3, 21/3) = (3, 7)",
            points=10,
        ),

        # 직선 - 두 점을 지나는 직선
        mc(
            id="h1-2-1-2-co-004",
            concept_id="h1-2-1-2",
            category="computation",
            part="algebra",
            difficulty=6,
            content="두 점 (1, 2), (3, 8)을 지나는 직선의 기울기는?",
            options=["3", "2", "1/3", "6"],
            correct="A",
            explanation="기울기 공식: m = (y₂ - y₁)/(x₂ - x₁)\nm = (8 - 2)/(3 - 1) = 6/2 = 3",
            points=10,
        ),

        # 직선 - 일반형 → 기울기-절편 형식
        mc(
            id="h1-2-1-2-co-005",
            concept_id="h1-2-1-2",
            category="computation",
            part="algebra",
            difficulty=7,
            content="직선 3x - 2y + 6 = 0의 기울기와 y절편은?",
            options=["기울기 3/2, y절편 3", "기울기 -3/2, y절편 3", "기울기 3/2, y절편 -3", "기울기 2/3, y절편 3"],
            correct="A",
            explanation="일반형을 y = mx + b로 변환:\n-2y = -3x - 6\ny = (3/2)x + 3\n∴ 기울기 3/2, y절편 3",
            points=10,
        ),

        # 원 - 원과 직선의 위치 관계
        mc(
            id="h1-2-1-3-co-004",
            concept_id="h1-2-1-3",
            category="computation",
            part="algebra",
            difficulty=9,
            content="원 x² + y² = 25와 직선 y = 3의 교점의 x좌표는?",
            options=["±4", "±3", "±5", "없음"],
            correct="A",
            explanation="y = 3을 원의 방정식에 대입:\nx² + 3² = 25\nx² + 9 = 25\nx² = 16\nx = ±4",
            points=10,
        ),

        # 원 - 중심을 지나는 현의 길이
        mc(
            id="h1-2-1-3-co-005",
            concept_id="h1-2-1-3",
            category="computation",
            part="algebra",
            difficulty=10,
            content="원 (x - 1)² + (y - 2)² = 9의 넓이는?",
            options=["9π", "3π", "18π", "81π"],
            correct="A",
            explanation="원의 반지름: r = √9 = 3\n넓이 = πr² = π × 3² = 9π",
            points=10,
        ),

        # 도형의 이동 - x축 대칭
        mc(
            id="h1-2-1-4-co-004",
            concept_id="h1-2-1-4",
            category="computation",
            part="geo",
            difficulty=5,
            content="점 (5, -3)을 x축에 대해 대칭이동한 점의 좌표는?",
            options=["(5, 3)", "(-5, -3)", "(-5, 3)", "(5, -3)"],
            correct="A",
            explanation="x축 대칭: (x, y) → (x, -y)\n(5, -3) → (5, 3)",
            points=10,
        ),

        # 도형의 이동 - 원점 대칭
        mc(
            id="h1-2-1-4-co-005",
            concept_id="h1-2-1-4",
            category="computation",
            part="geo",
            difficulty=7,
            content="점 (2, -5)를 원점에 대해 대칭이동한 점의 좌표는?",
            options=["(-2, 5)", "(2, 5)", "(-2, -5)", "(-5, 2)"],
            correct="A",
            explanation="원점 대칭: (x, y) → (-x, -y)\n(2, -5) → (-2, 5)",
            points=10,
        ),
    ]


def _get_tests():
    """연산 카테고리 테스트 (1개)."""
    return [
        test(
            id="test-h1-geometry-eq",
            title="공통수학2 도형의 방정식",
            description="평면좌표, 직선, 원, 도형의 이동",
            grade="high_1",
            concept_ids=[
                "h1-2-1-1",
                "h1-2-1-2",
                "h1-2-1-3",
                "h1-2-1-4"
            ],
            question_ids=[
                "h1-2-1-1-co-001", "h1-2-1-1-co-002", "h1-2-1-1-co-003", "h1-2-1-1-co-004", "h1-2-1-1-co-005",
                "h1-2-1-2-co-001", "h1-2-1-2-co-002", "h1-2-1-2-co-003", "h1-2-1-2-co-004", "h1-2-1-2-co-005",
                "h1-2-1-3-co-001", "h1-2-1-3-co-002", "h1-2-1-3-co-003", "h1-2-1-3-co-004", "h1-2-1-3-co-005",
                "h1-2-1-4-co-001", "h1-2-1-4-co-002", "h1-2-1-4-co-003", "h1-2-1-4-co-004", "h1-2-1-4-co-005"
            ],
            time_limit_minutes=30,
            use_question_pool=True,
            questions_per_attempt=10,
        ),
    ]
