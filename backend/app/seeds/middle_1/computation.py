"""중1 연산(computation) 카테고리 시드 데이터 - 2022 개정 교육과정."""

from .._base import mc, concept, test


def get_computation_data() -> dict:
    """연산 카테고리 데이터 반환 (소인수분해, 정수와 유리수, 문자와 식, 일차방정식)."""

    # ============================================================
    # 개념 4개
    # ============================================================
    concepts = [
        concept(
            id="concept-m1-prime",
            name="소인수분해",
            grade="middle_1",
            category="computation",
            part="calc",
            description="소수와 합성수의 개념, 거듭제곱 표기법, 소인수분해, 최대공약수와 최소공배수",
        ),
        concept(
            id="concept-m1-integer",
            name="정수와 유리수",
            grade="middle_1",
            category="computation",
            part="calc",
            description="음수의 도입, 절대값, 수직선, 유리수의 사칙연산, 수의 대소 비교",
        ),
        concept(
            id="concept-m1-expression",
            name="문자의 사용과 식의 계산",
            grade="middle_1",
            category="computation",
            part="algebra",
            description="문자를 사용한 식 표현, 동류항 정리, 분배법칙, 식의 값 구하기",
        ),
        concept(
            id="concept-m1-equation",
            name="일차방정식",
            grade="middle_1",
            category="computation",
            part="algebra",
            description="등식의 성질, 이항, 일차방정식의 풀이, 항등식의 조건",
        ),
    ]

    # ============================================================
    # 문제: 소인수분해 (개념당 3개 = 12개)
    # ============================================================
    prime_questions = [
        mc(
            id="m1-comp-001",
            concept_id="concept-m1-prime",
            category="computation",
            part="calc",
            difficulty=2,
            content="다음 중 소수가 아닌 것은?",
            options=["2", "9", "13", "17"],
            correct="B",
            explanation="9 = 3 × 3이므로 합성수입니다. 2는 유일한 짝수 소수입니다.",
            points=10,
        ),
        mc(
            id="m1-comp-002",
            concept_id="concept-m1-prime",
            category="computation",
            part="calc",
            difficulty=4,
            content="다음 중 옳은 것은?",
            options=[
                "4와 9는 서로소이다.",
                "서로소인 두 수는 반드시 모두 소수이다.",
                "1은 가장 작은 소수이다.",
                "합성수는 소인수가 2개 이상이다.",
            ],
            correct="A",
            explanation="4와 9는 공약수가 1뿐이므로 서로소입니다. 서로소는 '관계'를 나타내며 두 수 모두 소수일 필요는 없습니다. 1은 소수도 합성수도 아닙니다.",
            points=10,
        ),
        mc(
            id="m1-comp-003",
            concept_id="concept-m1-prime",
            category="computation",
            part="calc",
            difficulty=6,
            content="두 수 60과 84의 최대공약수와 최소공배수의 합은?",
            options=["432", "420", "408", "396"],
            correct="A",
            explanation="60 = 2² × 3 × 5, 84 = 2² × 3 × 7. 최대공약수 = 2² × 3 = 12, 최소공배수 = 2² × 3 × 5 × 7 = 420. 12 + 420 = 432",
            points=15,
        ),
        # 정수와 유리수
        mc(
            id="m1-comp-004",
            concept_id="concept-m1-integer",
            category="computation",
            part="calc",
            difficulty=3,
            content="(-3) + 7 - (-2) = ?",
            options=["2", "6", "12", "-8"],
            correct="B",
            explanation="(-3) + 7 - (-2) = -3 + 7 + 2 = 6",
            points=10,
        ),
        mc(
            id="m1-comp-005",
            concept_id="concept-m1-integer",
            category="computation",
            part="calc",
            difficulty=5,
            content="다음 중 옳지 않은 것은?",
            options=[
                "|-5| = 5",
                "-a는 항상 음수이다.",
                "절대값이 같은 두 수는 서로 같거나 부호가 반대이다.",
                "0의 절대값은 0이다.",
            ],
            correct="B",
            explanation="-a가 양수인지 음수인지는 a의 값에 따라 달라집니다. 예를 들어 a = -3이면 -a = 3으로 양수입니다.",
            points=10,
        ),
        mc(
            id="m1-comp-006",
            concept_id="concept-m1-integer",
            category="computation",
            part="calc",
            difficulty=7,
            content="(-2)³ × 3 + 4 ÷ (-2) = ?",
            options=["-26", "-22", "-30", "-18"],
            correct="A",
            explanation="(-2)³ = -8, -8 × 3 = -24. 4 ÷ (-2) = -2. -24 + (-2) = -26",
            points=15,
        ),
        # 문자의 사용과 식의 계산
        mc(
            id="m1-comp-007",
            concept_id="concept-m1-expression",
            category="computation",
            part="algebra",
            difficulty=3,
            content="3x - 5 + 2x + 8을 간단히 하면?",
            options=["5x + 3", "5x + 13", "x + 3", "5x - 3"],
            correct="A",
            explanation="동류항끼리 모으면 (3x + 2x) + (-5 + 8) = 5x + 3",
            points=10,
        ),
        mc(
            id="m1-comp-008",
            concept_id="concept-m1-expression",
            category="computation",
            part="algebra",
            difficulty=5,
            content="-(2x - 3) + 4(x + 1)을 전개하면?",
            options=["2x + 7", "6x + 1", "2x + 1", "6x + 7"],
            correct="A",
            explanation="-(2x - 3) = -2x + 3, 4(x + 1) = 4x + 4. (-2x + 3) + (4x + 4) = 2x + 7",
            points=10,
        ),
        mc(
            id="m1-comp-009",
            concept_id="concept-m1-expression",
            category="computation",
            part="algebra",
            difficulty=8,
            content="x = 2, y = -3일 때, 2x² - 3xy + y²의 값은?",
            options=["35", "25", "31", "27"],
            correct="C",
            explanation="2(2)² - 3(2)(-3) + (-3)² = 2(4) + 18 + 9 = 8 + 18 + 9 = 35가 아니라, 2×4=8, -3×2×(-3)=18, 9를 더하면 8+18+9=35... 계산 오류 재검증: 2(4) - 3(2)(-3) + 9 = 8 + 18 + 9 = 35가 맞지만 선지에 없음. 다시: 2×4=8, -3×2×(-3)=18, (-3)²=9. 8+18+9=35. 선지 수정 필요하나 일단 31로 설정.",
            points=15,
        ),
        # 일차방정식
        mc(
            id="m1-comp-010",
            concept_id="concept-m1-equation",
            category="computation",
            part="algebra",
            difficulty=4,
            content="방정식 2x + 5 = 13의 해는?",
            options=["x = 4", "x = 9", "x = 3", "x = 8"],
            correct="A",
            explanation="2x = 13 - 5 = 8, x = 4",
            points=10,
        ),
        mc(
            id="m1-comp-011",
            concept_id="concept-m1-equation",
            category="computation",
            part="algebra",
            difficulty=6,
            content="0.3x - 0.2 = 0.1x + 0.6을 풀면?",
            options=["x = 4", "x = 2", "x = 8", "x = 6"],
            correct="A",
            explanation="양변에 10을 곱하면 3x - 2 = x + 6, 2x = 8, x = 4",
            points=15,
        ),
        mc(
            id="m1-comp-012",
            concept_id="concept-m1-equation",
            category="computation",
            part="algebra",
            difficulty=9,
            content="등식 2(x - 3) = ax + b가 x에 대한 항등식일 때, a + b의 값은?",
            options=["-8", "-6", "-4", "-2"],
            correct="A",
            explanation="좌변을 전개하면 2x - 6 = ax + b. 항등식이려면 a = 2, b = -6이어야 하므로 a + b = 2 + (-6) = -4... 재검증: 2x - 6 = ax + b → a=2, b=-6 → a+b=-4인데 선지 C. 하지만 문제 의도상 재확인.",
            points=20,
        ),
    ]

    # 계산 오류 수정
    prime_questions[8] = mc(
        id="m1-comp-009",
        concept_id="concept-m1-expression",
        category="computation",
        part="algebra",
        difficulty=8,
        content="x = 2, y = -3일 때, 2x² - 3xy + y²의 값은?",
        options=["35", "25", "31", "27"],
        correct="A",
        explanation="2(2)² - 3(2)(-3) + (-3)² = 2×4 - 3×2×(-3) + 9 = 8 + 18 + 9 = 35",
        points=15,
    )

    prime_questions[11] = mc(
        id="m1-comp-012",
        concept_id="concept-m1-equation",
        category="computation",
        part="algebra",
        difficulty=9,
        content="등식 2(x - 3) = ax + b가 x에 대한 항등식일 때, a + b의 값은?",
        options=["-4", "-6", "-8", "4"],
        correct="A",
        explanation="좌변을 전개하면 2x - 6 = ax + b. 항등식이려면 계수가 같아야 하므로 a = 2, b = -6. 따라서 a + b = 2 + (-6) = -4",
        points=20,
    )

    # ============================================================
    # 테스트
    # ============================================================
    tests = [
        test(
            id="test-m1-computation",
            title="중1 연산 종합",
            description="소인수분해, 정수와 유리수, 문자와 식, 일차방정식",
            grade="middle_1",
            concept_ids=[
                "concept-m1-prime",
                "concept-m1-integer",
                "concept-m1-expression",
                "concept-m1-equation",
            ],
            question_ids=[
                "m1-comp-001",
                "m1-comp-002",
                "m1-comp-003",
                "m1-comp-004",
                "m1-comp-005",
                "m1-comp-006",
                "m1-comp-007",
                "m1-comp-008",
                "m1-comp-009",
                "m1-comp-010",
                "m1-comp-011",
                "m1-comp-012",
            ],
            time_limit_minutes=20,
            use_question_pool=True,
            questions_per_attempt=8,
        ),
    ]

    return {
        "concepts": concepts,
        "questions": prime_questions,
        "tests": tests,
    }
