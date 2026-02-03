"""초등 6학년 빈칸 채우기 문제."""
from app.seeds._base import fb


def get_questions():
    """초등 6학년 빈칸 채우기 문제 반환."""
    return [
        # 분수의 나눗셈
        fb(
            id="e6-fb-001",
            concept_id="concept-e6-comp",
            category="computation",
            part="연산",
            difficulty=2,
            content="1/3 ÷ 2 = __입니다. 답을 분수로 쓰세요.",
            answer="1/6",
            explanation="1/3 ÷ 2 = 1/3 × 1/2 = 1/6입니다.",
            points=10,
        ),
        fb(
            id="e6-fb-002",
            concept_id="concept-e6-comp",
            category="computation",
            part="연산",
            difficulty=4,
            content="4/5 ÷ 1/5 = __입니다.",
            answer="4",
            explanation="4/5 ÷ 1/5 = 4/5 × 5/1 = 20/5 = 4입니다.",
            points=10,
        ),
        # 소수의 나눗셈
        fb(
            id="e6-fb-003",
            concept_id="concept-e6-comp",
            category="computation",
            part="연산",
            difficulty=5,
            content="1.2 ÷ 0.3 = __입니다.",
            answer="4",
            explanation="1.2 ÷ 0.3 = 12 ÷ 3 = 4입니다.",
            points=10,
        ),
        fb(
            id="e6-fb-004",
            concept_id="concept-e6-comp",
            category="computation",
            part="연산",
            difficulty=7,
            content="6.4 ÷ 0.8 = __입니다.",
            answer="8",
            explanation="6.4 ÷ 0.8 = 64 ÷ 8 = 8입니다.",
            points=10,
        ),
        # 비와 비율
        fb(
            id="e6-fb-005",
            concept_id="concept-e6-conc",
            category="concept",
            part="개념",
            difficulty=3,
            content="15와 25의 비를 가장 간단한 자연수의 비로 나타내면 __ : __입니다. (작은 수를 먼저 쓰세요)",
            answer="3:5",
            explanation="15 : 25 = 3 : 5입니다.",
            points=10,
            accept_formats=["3:5", "3 : 5"],
        ),
        # 비례식
        fb(
            id="e6-fb-006",
            concept_id="concept-e6-conc",
            category="concept",
            part="개념",
            difficulty=6,
            content="비례식 4 : 7 = 12 : □에서 □는 __입니다.",
            answer="21",
            explanation="4 × □ = 7 × 12이므로, 4 × □ = 84, □ = 21입니다.",
            points=10,
        ),
        # 비례배분
        fb(
            id="e6-fb-007",
            concept_id="concept-e6-conc",
            category="concept",
            part="개념",
            difficulty=8,
            content="60을 2 : 3으로 나누면 작은 쪽은 __입니다.",
            answer="24",
            explanation="2 + 3 = 5, 60 × 2/5 = 24입니다.",
            points=10,
        ),
        # 원의 넓이
        fb(
            id="e6-fb-008",
            concept_id="concept-e6-conc",
            category="concept",
            part="개념",
            difficulty=9,
            content="반지름이 4cm인 원의 넓이는 __ cm²입니다. (π = 3으로 계산)",
            answer="48",
            explanation="원의 넓이 = 3 × 4 × 4 = 48 cm²입니다.",
            points=10,
            accept_formats=["48"],
        ),
    ]
