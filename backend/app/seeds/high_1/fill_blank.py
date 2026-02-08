"""고1 빈칸 채우기 문제 (2022 개정 교육과정 - 전 4단원)."""
from app.seeds._base import fb, test


def get_fill_blank_data() -> dict:
    """빈칸 채우기 데이터 반환."""
    return {
        "questions": _get_questions(),
        "tests": _get_tests(),
    }


def _get_questions():
    """빈칸 채우기 문제 목록 (12문제: 4단원 × 3문제)."""
    return [
        # ========== 1단원: 다항식 (3문제) ==========

        fb(
            id="h1-1-1-1-fb-001",
            concept_id="h1-1-1-1",
            category="computation",
            part="algebra",
            difficulty=3,
            content="다항식 (x + 3)(x - 2)를 전개하면 x² + [answer]x - [answer]입니다.",
            answer="1|6",
            explanation="(x + 3)(x - 2) = x² - 2x + 3x - 6 = x² + x - 6\n첫 번째 빈칸: 1, 두 번째 빈칸: 6",
            points=10,
            accept_formats=["1|6"],
        ),

        fb(
            id="h1-1-1-1-fb-002",
            concept_id="h1-1-1-1",
            category="computation",
            part="algebra",
            difficulty=4,
            content="등식 x² + kx + 12 ≡ (x + 3)(x + a)가 항등식일 때, k = [answer]이고 a = [answer]입니다.",
            answer="7|4",
            explanation="(x + 3)(x + a) = x² + (3 + a)x + 3a\n계수 비교: 3 + a = k, 3a = 12\n∴ a = 4, k = 7",
            points=10,
            accept_formats=["7|4"],
        ),

        fb(
            id="h1-1-1-2-fb-001",
            concept_id="h1-1-1-2",
            category="computation",
            part="algebra",
            difficulty=5,
            content="다항식 f(x) = x³ - 4x² + x + 6을 x - 2로 나눈 나머지는 [answer]입니다.",
            answer="0",
            explanation="나머지정리: f(2)를 계산\nf(2) = 8 - 16 + 2 + 6 = 0\n∴ 나머지는 0 (나누어떨어짐)",
            points=10,
            accept_formats=["0"],
        ),

        # ========== 2단원: 방정식과 부등식 (3문제) ==========

        fb(
            id="h1-1-2-1-fb-001",
            concept_id="h1-1-2-1",
            category="computation",
            part="algebra",
            difficulty=3,
            content="복소수 (3 + 2i)(1 - i)를 계산하면 [answer] + [answer]i입니다.",
            answer="5|-1",
            explanation="(3 + 2i)(1 - i) = 3 - 3i + 2i - 2i²\n= 3 - i - 2(-1)\n= 3 - i + 2\n= 5 - i\n∴ 실수부: 5, 허수부: -1",
            points=10,
            accept_formats=["5|-1"],
        ),

        fb(
            id="h1-1-2-1-fb-002",
            concept_id="h1-1-2-1",
            category="computation",
            part="algebra",
            difficulty=4,
            content="이차방정식 x² - 7x + 12 = 0의 두 근을 α, β라 할 때, α + β = [answer]이고 αβ = [answer]입니다.",
            answer="7|12",
            explanation="근과 계수의 관계:\nα + β = -b/a = -(-7)/1 = 7\nαβ = c/a = 12/1 = 12",
            points=10,
            accept_formats=["7|12"],
        ),

        fb(
            id="h1-1-2-1-fb-003",
            concept_id="h1-1-2-1",
            category="computation",
            part="algebra",
            difficulty=5,
            content="이차방정식 x² + (k-1)x + 9 = 0이 중근을 가질 때, k의 값은 [answer] 또는 [answer]입니다. (작은 값부터)",
            answer="-5|7",
            explanation="중근 조건: 판별식 D = 0\nD = (k-1)² - 4×1×9 = 0\n(k-1)² = 36\nk - 1 = ±6\nk = 1 + 6 = 7 또는 k = 1 - 6 = -5\n∴ -5, 7 (작은 값부터)",
            points=10,
            accept_formats=["-5|7"],
        ),

        # ========== 3단원: 경우의 수 (3문제) ==========

        fb(
            id="h1-1-3-2-fb-001",
            concept_id="h1-1-3-2",
            category="concept",
            part="data",
            difficulty=3,
            content="6명 중에서 3명을 뽑아 일렬로 세우는 경우의 수는 [answer]가지입니다.",
            answer="120",
            explanation="순열 ₆P₃ = 6 × 5 × 4 = 120",
            points=10,
            accept_formats=["120"],
        ),

        fb(
            id="h1-1-3-2-fb-002",
            concept_id="h1-1-3-2",
            category="concept",
            part="data",
            difficulty=4,
            content="7명 중에서 4명을 선발하는 경우의 수는 [answer]가지입니다.",
            answer="35",
            explanation="조합 ₇C₄ = 7!/(4!×3!) = (7×6×5)/(3×2×1) = 35",
            points=10,
            accept_formats=["35"],
        ),

        fb(
            id="h1-1-3-2-fb-003",
            concept_id="h1-1-3-2",
            category="concept",
            part="data",
            difficulty=5,
            content="1, 2, 3, 4, 5 중에서 서로 다른 세 개를 택하여 세 자리 자연수를 만들 때, 300보다 큰 수는 [answer]개입니다.",
            answer="36",
            explanation="백의 자리가 3, 4, 5인 경우를 계산:\n백의 자리 3: 십의 자리 4가지 × 일의 자리 3가지 = 12\n백의 자리 4: 십의 자리 4가지 × 일의 자리 3가지 = 12\n백의 자리 5: 십의 자리 4가지 × 일의 자리 3가지 = 12\n∴ 12 + 12 + 12 = 36",
            points=10,
            accept_formats=["36"],
        ),

        # ========== 4단원: 행렬 (3문제) ==========

        fb(
            id="h1-1-4-1-fb-001",
            concept_id="h1-1-4-1",
            category="concept",
            part="algebra",
            difficulty=3,
            content="행렬 A = [[3, -1], [2, 0]]에 대하여 2A를 계산하면 [[6, [answer]], [[answer], 0]]입니다.",
            answer="-2|4",
            explanation="2A = [[2×3, 2×(-1)], [2×2, 2×0]] = [[6, -2], [4, 0]]\n첫 번째 빈칸: -2, 두 번째 빈칸: 4",
            points=10,
            accept_formats=["-2|4"],
        ),

        fb(
            id="h1-1-4-2-fb-001",
            concept_id="h1-1-4-2",
            category="concept",
            part="algebra",
            difficulty=4,
            content="두 행렬 A = [[1, 2], [3, 4]], B = [[2, 0], [1, 3]]에 대하여 AB를 계산하면 [[[answer], [answer]], [[answer], [answer]]]입니다.",
            answer="4|6|10|12",
            explanation="AB = [[1×2+2×1, 1×0+2×3], [3×2+4×1, 3×0+4×3]]\n   = [[2+2, 0+6], [6+4, 0+12]]\n   = [[4, 6], [10, 12]]",
            points=10,
            accept_formats=["4|6|10|12"],
        ),

        fb(
            id="h1-1-4-2-fb-002",
            concept_id="h1-1-4-2",
            category="concept",
            part="algebra",
            difficulty=5,
            content="두 행렬 A = [[2, 1], [0, 1]], B = [[1, -1], [0, 2]]에 대하여 BA를 계산하면 [[[answer], [answer]], [[answer], [answer]]]입니다.",
            answer="2|0|0|2",
            explanation="BA = [[1×2+(-1)×0, 1×1+(-1)×1], [0×2+2×0, 0×1+2×1]]\n   = [[2+0, 1-1], [0+0, 0+2]]\n   = [[2, 0], [0, 2]]\n\n[참고] AB = [[2, 1], [0, 1]][[1, -1], [0, 2]] = [[2, 0], [0, 2]]\n이 경우 AB = BA = 2I (교환법칙 예외 사례)",
            points=10,
            accept_formats=["2|0|0|2"],
        ),
    ]


def _get_tests():
    """빈칸 채우기 테스트 (없음 - 기존 테스트에 통합)."""
    return []
