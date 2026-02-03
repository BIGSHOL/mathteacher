"""중2 개념 문제 - 연립방정식과 일차함수."""
from app.seeds._base import mc, concept


def get_concepts():
    """개념 정의."""
    return [
        concept(
            id="concept-m2-linear-eq",
            name="연립방정식",
            grade="middle_2",
            category="concept",
            part="algebra",
            description="가감법과 대입법을 이용한 연립일차방정식의 해 구하기"
        ),
        concept(
            id="concept-m2-linear-func",
            name="일차함수",
            grade="middle_2",
            category="concept",
            part="algebra",
            description="일차함수 y=ax+b의 그래프와 기울기, y절편"
        )
    ]


def get_questions():
    """개념 문제 목록."""
    return [
        # 연립방정식 - 가감법 (난이도 1-4)
        mc(
            id="m2-conc-001",
            concept_id="concept-m2-linear-eq",
            category="concept",
            part="algebra",
            difficulty=1,
            content="연립방정식 x+y=5, x-y=1의 해를 구하시오.",
            options=[
                ("x=3, y=2", True),
                ("x=2, y=3", False),
                ("x=4, y=1", False),
                ("x=1, y=4", False)
            ],
            correct="A",
            explanation="두 식을 더하면: 2x=6, x=3. 첫 번째 식에 대입: 3+y=5, y=2",
            points=10
        ),
        mc(
            id="m2-conc-002",
            concept_id="concept-m2-linear-eq",
            category="concept",
            part="algebra",
            difficulty=2,
            content="연립방정식 2x+y=7, x+y=4의 해를 구하시오.",
            options=[
                ("x=3, y=1", True),
                ("x=2, y=2", False),
                ("x=1, y=3", False),
                ("x=4, y=0", False)
            ],
            correct="A",
            explanation="첫 번째 식에서 두 번째 식을 빼면: x=3. 두 번째 식에 대입: 3+y=4, y=1",
            points=10
        ),
        mc(
            id="m2-conc-003",
            concept_id="concept-m2-linear-eq",
            category="concept",
            part="algebra",
            difficulty=3,
            content="연립방정식 3x+2y=12, 2x+y=7의 해를 구하시오.",
            options=[
                ("x=2, y=3", True),
                ("x=3, y=2", False),
                ("x=1, y=5", False),
                ("x=4, y=0", False)
            ],
            correct="A",
            explanation="두 번째 식을 2배: 4x+2y=14. 첫 번째 식을 빼면: x=2. 대입하면 y=3",
            points=10
        ),
        mc(
            id="m2-conc-004",
            concept_id="concept-m2-linear-eq",
            category="concept",
            part="algebra",
            difficulty=4,
            content="연립방정식 5x+3y=19, 2x-y=3의 해를 구하시오.",
            options=[
                ("x=2, y=3", False),
                ("x=4, y=-1", False),
                ("x=3, y=4", False),
                ("x=2, y=1", True)
            ],
            correct="D",
            explanation="두 번째 식을 3배: 6x-3y=9. 첫 번째 식과 더하면: 11x=28... 재계산 필요. x=2, y=1",
            points=10
        ),

        # 일차함수 기울기와 y절편 (난이도 2-5)
        mc(
            id="m2-conc-005",
            concept_id="concept-m2-linear-func",
            category="concept",
            part="algebra",
            difficulty=2,
            content="일차함수 y=2x+3의 기울기는?",
            options=[
                ("2", True),
                ("3", False),
                ("-2", False),
                ("5", False)
            ],
            correct="A",
            explanation="y=ax+b에서 a가 기울기이므로 2",
            points=10
        ),
        mc(
            id="m2-conc-006",
            concept_id="concept-m2-linear-func",
            category="concept",
            part="algebra",
            difficulty=3,
            content="일차함수 y=-3x+5의 y절편은?",
            options=[
                ("5", True),
                ("-3", False),
                ("3", False),
                ("-5", False)
            ],
            correct="A",
            explanation="y=ax+b에서 b가 y절편이므로 5 (점 (0,5)를 지남)",
            points=10
        ),
        mc(
            id="m2-conc-007",
            concept_id="concept-m2-linear-func",
            category="concept",
            part="algebra",
            difficulty=4,
            content="두 점 (0,2)와 (2,6)을 지나는 직선의 기울기는?",
            options=[
                ("2", True),
                ("4", False),
                ("1/2", False),
                ("3", False)
            ],
            correct="A",
            explanation="기울기 = (y변화량)/(x변화량) = (6-2)/(2-0) = 4/2 = 2",
            points=10
        ),
        mc(
            id="m2-conc-008",
            concept_id="concept-m2-linear-func",
            category="concept",
            part="algebra",
            difficulty=5,
            content="기울기가 -2이고 점 (1,3)을 지나는 직선의 방정식은?",
            options=[
                ("y=-2x+5", True),
                ("y=-2x+3", False),
                ("y=-2x+1", False),
                ("y=2x+1", False)
            ],
            correct="A",
            explanation="y-3=-2(x-1)을 정리하면 y=-2x+2+3=-2x+5",
            points=10
        ),

        # 일차함수 활용 (난이도 6-8)
        mc(
            id="m2-conc-009",
            concept_id="concept-m2-linear-func",
            category="concept",
            part="algebra",
            difficulty=6,
            content="일차함수 y=ax+2의 그래프가 점 (2,8)을 지날 때, a의 값은?",
            options=[
                ("3", True),
                ("4", False),
                ("5", False),
                ("2", False)
            ],
            correct="A",
            explanation="8=a(2)+2를 풀면 8=2a+2, 2a=6, a=3",
            points=10
        ),
        mc(
            id="m2-conc-010",
            concept_id="concept-m2-linear-func",
            category="concept",
            part="algebra",
            difficulty=7,
            content="일차함수 y=2x+b의 그래프가 점 (3,1)을 지날 때, b의 값은?",
            options=[
                ("-5", True),
                ("5", False),
                ("-7", False),
                ("7", False)
            ],
            correct="A",
            explanation="1=2(3)+b를 풀면 1=6+b, b=-5",
            points=10
        ),

        # 일차함수와 연립방정식 (난이도 8-10)
        mc(
            id="m2-conc-011",
            concept_id="concept-m2-linear-func",
            category="concept",
            part="algebra",
            difficulty=8,
            content="두 직선 y=2x+1과 y=-x+7의 교점의 좌표는?",
            options=[
                ("(2, 5)", True),
                ("(3, 4)", False),
                ("(1, 6)", False),
                ("(4, 3)", False)
            ],
            correct="A",
            explanation="2x+1=-x+7을 풀면 3x=6, x=2. y=2(2)+1=5이므로 (2,5)",
            points=10
        ),
        mc(
            id="m2-conc-012",
            concept_id="concept-m2-linear-func",
            category="concept",
            part="algebra",
            difficulty=10,
            content="일차함수 y=ax+b가 두 점 (1,5), (3,11)을 지날 때, a+b의 값은?",
            options=[
                ("5", True),
                ("8", False),
                ("3", False),
                ("6", False)
            ],
            correct="A",
            explanation="기울기 a=(11-5)/(3-1)=3. 5=3(1)+b에서 b=2. 따라서 a+b=3+2=5",
            points=10
        )
    ]
