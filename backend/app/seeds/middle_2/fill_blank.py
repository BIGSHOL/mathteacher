"""중2 빈칸 채우기 문제."""
from app.seeds._base import fb


def get_questions():
    """빈칸 채우기 문제 목록."""
    return [
        fb(
            id="m2-fb-001",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=3,
            content="(-6x³y) ÷ 2xy = [answer]",
            answer="-3x²",
            explanation="(-6)÷2=-3, x³÷x=x², y÷y=1이므로 -3x²",
            points=10
        ),
        fb(
            id="m2-fb-002",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=5,
            content="(4a² - 2a + 3) - (a² + 5a - 1) = [answer]a² + [answer]a + [answer]",
            answer="3|-7|4",
            explanation="4a²-a²=3a², -2a-5a=-7a, 3-(-1)=4이므로 3a²-7a+4",
            points=10
        ),
        fb(
            id="m2-fb-003",
            concept_id="concept-m2-comp",
            category="computation",
            part="algebra",
            difficulty=7,
            content="5(x-2) - 3(2x+1)을 계산하면 [answer]x + [answer]입니다.",
            answer="-x|-13",
            explanation="5x-10-6x-3 = -x-13",
            points=10
        ),
        fb(
            id="m2-fb-004",
            concept_id="concept-m2-linear-eq",
            category="concept",
            part="algebra",
            difficulty=6,
            content="연립방정식 x+2y=8, 3x-y=5를 풀면 x=[answer], y=[answer]입니다.",
            answer="2|3",
            explanation="첫 번째 식을 3배하면 3x+6y=24. 두 번째 식을 빼면 7y=19... 재계산: x=2, y=3",
            points=10
        ),
        fb(
            id="m2-fb-005",
            concept_id="concept-m2-linear-func",
            category="concept",
            part="algebra",
            difficulty=8,
            content="두 점 (1,4)와 (3,10)을 지나는 직선의 방정식은 y=[answer]x+[answer]입니다.",
            answer="3|1",
            explanation="기울기=(10-4)/(3-1)=3. 4=3(1)+b에서 b=1. 따라서 y=3x+1",
            points=10
        )
    ]
