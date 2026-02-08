"""
공통수학2 빈칸 채우기 문제 (20문항)
- 10개 개념, 각 2문항
- ID: h2-2-1-1-lv04-fb-001 ~ h2-2-3-3-lv08-fb-001
"""

from app.seeds._base import fb, test


def get_fill_blank_data() -> dict:
    """공통수학2 빈칸 채우기 문제 데이터 반환"""

    questions = [
        # 1. 평면좌표 (concept-h2-plane-coord, 2문항)
        fb(
            id="h2-2-1-1-lv04-fb-001",
            concept_id="concept-h2-plane-coord",
            content="두 점 A(0, 0), B(3, 4) 사이의 거리는?",
            answer="5",
            accept_formats=["5", "5.0"],
            explanation="두 점 사이의 거리 공식: d = √[(x₂-x₁)² + (y₂-y₁)²]\nd = √[(3-0)² + (4-0)²] = √(9 + 16) = √25 = 5",
            difficulty=4,
            category="computation",
            part="calc"
        ),
        fb(
            id="h2-2-1-1-lv06-fb-001",
            concept_id="concept-h2-plane-coord",
            content="두 점 A(2, 1), B(6, 9)의 중점의 좌표에서 x좌표는?",
            answer="4",
            accept_formats=["4", "4.0"],
            explanation="중점 공식: M = ((x₁+x₂)/2, (y₁+y₂)/2)\nx좌표 = (2+6)/2 = 8/2 = 4",
            difficulty=6,
            category="computation",
            part="calc"
        ),

        # 2. 직선의 방정식 (concept-h2-line, 2문항)
        fb(
            id="h2-2-1-2-lv04-fb-001",
            concept_id="concept-h2-line",
            content="두 점 (1, 2), (3, 6)을 지나는 직선의 기울기는?",
            answer="2",
            accept_formats=["2", "2.0"],
            explanation="기울기 공식: m = (y₂-y₁)/(x₂-x₁)\nm = (6-2)/(3-1) = 4/2 = 2",
            difficulty=4,
            category="computation",
            part="algebra"
        ),
        fb(
            id="h2-2-1-2-lv07-fb-001",
            concept_id="concept-h2-line",
            content="점 (1, 2)와 직선 3x - 4y + 5 = 0 사이의 거리는?",
            answer="0",
            accept_formats=["0", "0.0"],
            explanation="점과 직선 사이의 거리 공식: d = |ax₀ + by₀ + c|/√(a² + b²)\nd = |3(1) - 4(2) + 5|/√(9 + 16)\n= |3 - 8 + 5|/√25\n= |0|/5 = 0\n점이 직선 위에 있으므로 거리는 0",
            difficulty=7,
            category="computation",
            part="algebra"
        ),

        # 3. 원의 방정식 (concept-h2-circle, 2문항)
        fb(
            id="h2-2-1-3-lv05-fb-001",
            concept_id="concept-h2-circle",
            content="원 (x-1)² + (y+2)² = 9의 반지름은?",
            answer="3",
            accept_formats=["3", "3.0"],
            explanation="원의 표준형: (x-a)² + (y-b)² = r²\n중심 (1, -2), 반지름 r\nr² = 9이므로 r = 3",
            difficulty=5,
            category="computation",
            part="algebra"
        ),
        fb(
            id="h2-2-1-3-lv07-fb-001",
            concept_id="concept-h2-circle",
            content="원 x² + y² = 10과 직선 y = 3x의 교점 개수는?",
            answer="2",
            accept_formats=["2", "2.0"],
            explanation="y = 3x를 원의 방정식에 대입:\nx² + (3x)² = 10\nx² + 9x² = 10\n10x² = 10\nx² = 1\nx = ±1\n\n두 개의 서로 다른 실근이 존재하므로 교점은 2개",
            difficulty=7,
            category="computation",
            part="algebra"
        ),

        # 4. 도형의 이동 (concept-h2-transform, 2문항)
        fb(
            id="h2-2-1-4-lv04-fb-001",
            concept_id="concept-h2-transform",
            content="점 (3, 5)를 x축에 대해 대칭이동한 점의 y좌표는?",
            answer="-5",
            accept_formats=["-5", "-5.0"],
            explanation="x축 대칭이동: (x, y) → (x, -y)\n(3, 5) → (3, -5)\ny좌표는 -5",
            difficulty=4,
            category="computation",
            part="geo"
        ),
        fb(
            id="h2-2-1-4-lv06-fb-001",
            concept_id="concept-h2-transform",
            content="점 (2, -3)를 원점에 대해 대칭이동한 점의 x좌표는?",
            answer="-2",
            accept_formats=["-2", "-2.0"],
            explanation="원점 대칭이동: (x, y) → (-x, -y)\n(2, -3) → (-2, 3)\nx좌표는 -2",
            difficulty=6,
            category="computation",
            part="geo"
        ),

        # 5. 집합 (concept-h2-set, 2문항)
        fb(
            id="h2-2-2-1-lv04-fb-001",
            concept_id="concept-h2-set",
            content="집합 A = {1, 2, 3}의 부분집합의 개수는?",
            answer="8",
            accept_formats=["8", "8.0"],
            explanation="원소가 n개인 집합의 부분집합 개수: 2ⁿ\nn = 3이므로 2³ = 8개",
            difficulty=4,
            category="concept",
            part="data"
        ),
        fb(
            id="h2-2-2-1-lv06-fb-001",
            concept_id="concept-h2-set",
            content="n(A) = 5, n(B) = 4, n(A∩B) = 2일 때 n(A∪B)는?",
            answer="7",
            accept_formats=["7", "7.0"],
            explanation="합집합의 원소 개수: n(A∪B) = n(A) + n(B) - n(A∩B)\nn(A∪B) = 5 + 4 - 2 = 7",
            difficulty=6,
            category="concept",
            part="data"
        ),

        # 6. 명제 (concept-h2-proposition, 2문항)
        fb(
            id="h2-2-2-2-lv05-fb-001",
            concept_id="concept-h2-proposition",
            content="집합 A = {1, 2}의 진부분집합의 개수는?",
            answer="3",
            accept_formats=["3", "3.0"],
            explanation="원소가 n개인 집합의 진부분집합 개수: 2ⁿ - 1\nn = 2이므로 2² - 1 = 4 - 1 = 3개\n(공집합, {1}, {2})",
            difficulty=5,
            category="concept",
            part="data"
        ),
        fb(
            id="h2-2-2-2-lv07-fb-001",
            concept_id="concept-h2-proposition",
            content="명제 'p이면 q이다'가 참일 때, 반드시 참인 것은 '¬q이면 ¬p이다'이므로, 이를 무엇이라 하는가? (2글자)",
            answer="대우",
            accept_formats=["대우"],
            explanation="명제 'p → q'가 참일 때, 그 대우 '¬q → ¬p'도 참이다.\n명제와 대우는 진리값이 같다.\n답: 대우",
            difficulty=7,
            category="concept",
            part="data"
        ),

        # 7. 절대부등식 (concept-h2-abs-inequality, 2문항)
        fb(
            id="h2-2-2-3-lv05-fb-001",
            concept_id="concept-h2-abs-inequality",
            content="x > 0일 때 x + 9/x의 최솟값은?",
            answer="6",
            accept_formats=["6", "6.0"],
            explanation="산술-기하 평균 부등식: a + b ≥ 2√(ab) (등호: a = b)\nx + 9/x ≥ 2√(x · 9/x) = 2√9 = 2 × 3 = 6\n등호 조건: x = 9/x → x² = 9 → x = 3 (x > 0)\n최솟값: 6",
            difficulty=5,
            category="concept",
            part="algebra"
        ),
        fb(
            id="h2-2-2-3-lv08-fb-001",
            concept_id="concept-h2-abs-inequality",
            content="a > 0, b > 0, a + b = 6일 때 ab의 최댓값은?",
            answer="9",
            accept_formats=["9", "9.0"],
            explanation="산술-기하 평균 부등식: (a + b)/2 ≥ √(ab) (등호: a = b)\n6/2 ≥ √(ab)\n3 ≥ √(ab)\n9 ≥ ab\n등호 조건: a = b = 3\n최댓값: 9",
            difficulty=8,
            category="concept",
            part="algebra"
        ),

        # 8. 함수의 뜻과 그래프 (concept-h2-function, 2문항)
        fb(
            id="h2-2-3-1-lv04-fb-001",
            concept_id="concept-h2-function",
            content="집합 X = {1, 2, 3}에서 Y = {a, b}로의 함수의 개수는?",
            answer="8",
            accept_formats=["8", "8.0"],
            explanation="X의 각 원소는 Y의 원소 중 하나와 대응\n각 원소마다 2가지 선택 → 2 × 2 × 2 = 2³ = 8개",
            difficulty=4,
            category="concept",
            part="func"
        ),
        fb(
            id="h2-2-3-1-lv06-fb-001",
            concept_id="concept-h2-function",
            content="f(x) = x² + 1에서 f(3)의 값은?",
            answer="10",
            accept_formats=["10", "10.0"],
            explanation="f(3) = 3² + 1 = 9 + 1 = 10",
            difficulty=6,
            category="concept",
            part="func"
        ),

        # 9. 합성함수와 역함수 (concept-h2-composite, 2문항)
        fb(
            id="h2-2-3-2-lv05-fb-001",
            concept_id="concept-h2-composite",
            content="f(x) = 2x - 3의 역함수 f⁻¹(x)에서 f⁻¹(5)의 값은?",
            answer="4",
            accept_formats=["4", "4.0"],
            explanation="y = 2x - 3에서 x와 y를 바꾸고 x에 대해 정리:\nx = 2y - 3\n2y = x + 3\ny = (x + 3)/2\n\nf⁻¹(x) = (x + 3)/2\nf⁻¹(5) = (5 + 3)/2 = 8/2 = 4",
            difficulty=5,
            category="concept",
            part="func"
        ),
        fb(
            id="h2-2-3-2-lv07-fb-001",
            concept_id="concept-h2-composite",
            content="f(x) = x + 2, g(x) = 3x일 때 (g∘f)(1)의 값은?",
            answer="9",
            accept_formats=["9", "9.0"],
            explanation="(g∘f)(1) = g(f(1))\nf(1) = 1 + 2 = 3\ng(3) = 3 × 3 = 9",
            difficulty=7,
            category="concept",
            part="func"
        ),

        # 10. 유리함수와 무리함수 (concept-h2-rational-irrational, 2문항)
        fb(
            id="h2-2-3-3-lv05-fb-001",
            concept_id="concept-h2-rational-irrational",
            content="함수 y = 2/(x-3) + 1의 수직점근선의 x값은?",
            answer="3",
            accept_formats=["3", "3.0"],
            explanation="유리함수 y = a/(x-p) + q의 수직점근선: x = p\ny = 2/(x-3) + 1의 수직점근선: x = 3",
            difficulty=5,
            category="concept",
            part="func"
        ),
        fb(
            id="h2-2-3-3-lv08-fb-001",
            concept_id="concept-h2-rational-irrational",
            content="무리함수 y = √(3x-6)의 정의역에서 x의 최솟값은?",
            answer="2",
            accept_formats=["2", "2.0"],
            explanation="제곱근 안의 식은 0 이상이어야 함:\n3x - 6 ≥ 0\n3x ≥ 6\nx ≥ 2\n\n정의역: x ≥ 2이므로 최솟값은 2",
            difficulty=8,
            category="concept",
            part="func"
        ),
    ]

    # 공통수학2는 빈칸 채우기만 제공 (시험 문제 없음)
    tests = []

    return {
        "questions": questions,
        "tests": tests
    }
