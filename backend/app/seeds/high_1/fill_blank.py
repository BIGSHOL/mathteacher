"""고1 빈칸 채우기 문제."""
from app.seeds._base import fb


def get_questions():
    """빈칸 채우기 문제 목록."""
    return [
        fb(
            id="h1-fb-001",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=4,
            content="(x + 3)(x - 5)를 전개하면 x² + [answer]x + [answer]입니다.",
            answer="-2|-15",
            explanation="x² - 5x + 3x - 15 = x² - 2x - 15",
            points=10
        ),
        fb(
            id="h1-fb-002",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=7,
            content="x³ - 8을 인수분해하면 (x - [answer])(x² + [answer]x + [answer])입니다.",
            answer="2|2|4",
            explanation="a³ - b³ = (a-b)(a² + ab + b²) 공식 적용: (x-2)(x²+2x+4)",
            points=10
        ),
        fb(
            id="h1-fb-003",
            concept_id="concept-h1-poly",
            category="computation",
            part="algebra",
            difficulty=9,
            content="다항식 x³ + 3x² - x - 3을 x + 1로 나눈 나머지는 [answer]입니다.",
            answer="0",
            explanation="나머지정리: f(-1) = -1 + 3 + 1 - 3 = 0 (나누어떨어짐)",
            points=10
        ),
        fb(
            id="h1-fb-004",
            concept_id="concept-h1-complex",
            category="concept",
            part="algebra",
            difficulty=5,
            content="(3 + 2i)(1 - i)를 계산하면 [answer] + [answer]i입니다.",
            answer="5|-1",
            explanation="3 - 3i + 2i - 2i² = 3 - i - 2(-1) = 3 - i + 2 = 5 - i",
            points=10
        ),
        fb(
            id="h1-fb-005",
            concept_id="concept-h1-quad-ineq",
            category="concept",
            part="algebra",
            difficulty=7,
            content="이차방정식 x² - 5x + 6 = 0의 두 근이 α, β일 때, αβ = [answer]입니다.",
            answer="6",
            explanation="근과 계수의 관계: αβ = c/a = 6",
            points=10
        )
    ]
