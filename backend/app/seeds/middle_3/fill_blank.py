"""중3 빈칸 채우기 문제."""
from app.seeds._base import fb


def get_questions():
    """빈칸 채우기 문제 목록."""
    return [
        fb(
            id="m3-fb-001",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=4,
            content="√32를 간단히 하면 [answer]√[answer]입니다.",
            answer="4|2",
            explanation="√32 = √(16×2) = 4√2",
            points=10
        ),
        fb(
            id="m3-fb-002",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=6,
            content="√5 × √10 = [answer]√[answer]입니다.",
            answer="5|2",
            explanation="√5 × √10 = √50 = √(25×2) = 5√2",
            points=10
        ),
        fb(
            id="m3-fb-003",
            concept_id="concept-m3-sqrt",
            category="computation",
            part="algebra",
            difficulty=8,
            content="2/√3을 유리화하면 [answer]√[answer]/[answer]입니다.",
            answer="2|3|3",
            explanation="(2/√3) × (√3/√3) = 2√3/3",
            points=10
        ),
        fb(
            id="m3-fb-004",
            concept_id="concept-m3-quad-eq",
            category="concept",
            part="algebra",
            difficulty=5,
            content="이차방정식 x² - 8x + 15 = 0을 인수분해하면 (x-[answer])(x-[answer]) = 0입니다.",
            answer="3|5",
            explanation="x² - 8x + 15 = (x-3)(x-5)",
            points=10
        ),
        fb(
            id="m3-fb-005",
            concept_id="concept-m3-quad-func",
            category="concept",
            part="algebra",
            difficulty=7,
            content="이차함수 y = (x-3)²의 꼭짓점의 좌표는 ([answer], [answer])입니다.",
            answer="3|0",
            explanation="y = (x-3)²은 y = x²을 x축 방향으로 3만큼 평행이동한 것이므로 꼭짓점은 (3, 0)",
            points=10
        )
    ]
