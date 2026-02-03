"""초등 5학년 빈칸 채우기 문제."""
from app.seeds._base import fb


def get_questions():
    """초등 5학년 빈칸 채우기 문제 반환."""
    return [
        # 약수와 배수
        fb(
            id="e5-fb-001",
            concept_id="concept-e5-comp",
            category="computation",
            part="연산",
            difficulty=2,
            content="20의 약수 중에서 가장 큰 수는 __입니다.",
            answer="20",
            explanation="어떤 수의 약수 중 가장 큰 수는 그 수 자신입니다.",
            points=10,
        ),
        fb(
            id="e5-fb-002",
            concept_id="concept-e5-comp",
            category="computation",
            part="연산",
            difficulty=4,
            content="15와 25의 최대공약수는 __입니다.",
            answer="5",
            explanation="15의 약수: 1, 3, 5, 15 / 25의 약수: 1, 5, 25 / 최대공약수는 5입니다.",
            points=10,
        ),
        # 분수의 곱셈
        fb(
            id="e5-fb-003",
            concept_id="concept-e5-comp",
            category="computation",
            part="연산",
            difficulty=5,
            content="2/5 × 3/4 = __/20입니다. 빈칸에 들어갈 수를 쓰세요.",
            answer="6",
            explanation="2/5 × 3/4 = 6/20입니다.",
            points=10,
            accept_formats=["6", "6/20"],
        ),
        fb(
            id="e5-fb-004",
            concept_id="concept-e5-comp",
            category="computation",
            part="연산",
            difficulty=7,
            content="3/8 × 4 = __입니다. 답을 기약분수로 쓰세요.",
            answer="3/2",
            explanation="3/8 × 4 = 12/8 = 3/2입니다.",
            points=10,
            accept_formats=["3/2", "1.5"],
        ),
        # 소수의 곱셈
        fb(
            id="e5-fb-005",
            concept_id="concept-e5-comp",
            category="computation",
            part="연산",
            difficulty=6,
            content="0.5 × 0.6 = __입니다.",
            answer="0.3",
            explanation="0.5 × 0.6 = 0.3입니다.",
            points=10,
            accept_formats=["0.3", "0.30"],
        ),
        # 평균
        fb(
            id="e5-fb-006",
            concept_id="concept-e5-conc",
            category="concept",
            part="개념",
            difficulty=8,
            content="7, 9, 11, 13의 평균은 __입니다.",
            answer="10",
            explanation="평균 = (7 + 9 + 11 + 13) ÷ 4 = 40 ÷ 4 = 10입니다.",
            points=10,
        ),
        # 대응 관계
        fb(
            id="e5-fb-007",
            concept_id="concept-e5-conc",
            category="concept",
            part="개념",
            difficulty=9,
            content="x와 y의 관계가 y = 2x + 3일 때, x가 6이면 y는 __입니다.",
            answer="15",
            explanation="y = 2 × 6 + 3 = 12 + 3 = 15입니다.",
            points=10,
        ),
        fb(
            id="e5-fb-008",
            concept_id="concept-e5-comp",
            category="computation",
            part="연산",
            difficulty=3,
            content="4와 6의 공배수 중 가장 작은 수는 __입니다.",
            answer="12",
            explanation="4의 배수: 4, 8, 12, 16... / 6의 배수: 6, 12, 18... / 최소공배수는 12입니다.",
            points=10,
        ),
    ]
