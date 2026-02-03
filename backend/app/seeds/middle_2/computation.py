"""중2 연산 문제 - 유리수·순환소수, 식의 계산, 부등식 연산."""

from .._base import mc, concept, test


def get_computation_data() -> dict:
    """연산 카테고리 데이터 반환."""
    concepts = [
        # 1단원: 유리수와 순환소수
        concept(
            id="concept-m2-rational",
            name="유리수와 순환소수",
            grade="middle_2",
            category="computation",
            part="calc",
            description="유한소수 조건 판별, 순환소수↔분수 변환, 0.999...=1 증명"
        ),
        # 2단원: 식의 계산
        concept(
            id="concept-m2-expression",
            name="식의 계산",
            grade="middle_2",
            category="computation",
            part="algebra",
            description="지수법칙(a^m×a^n, (a^m)^n), 단항식/다항식 계산, 분배법칙"
        ),
        # 3단원: 부등식과 연립방정식 (연산 부분)
        concept(
            id="concept-m2-inequality",
            name="부등식과 연립방정식",
            grade="middle_2",
            category="computation",
            part="algebra",
            description="일차부등식(음수 곱/나누면 부등호 반전), 연립방정식(가감법/대입법)"
        ),
    ]

    questions = [
        # 유리수와 순환소수 (4문제, 난이도 2~8)
        mc(
            id="m2-comp-001",
            concept_id="concept-m2-rational",
            category="computation",
            part="calc",
            difficulty=2,
            content="분수 7/20을 소수로 나타낼 때, 유한소수인지 무한소수인지 판별하시오.",
            options=["유한소수", "순환소수", "무한소수이지만 순환하지 않음", "소수로 나타낼 수 없음"],
            correct="A",
            explanation="분모 20=2²×5이므로 소인수가 2와 5뿐이다. 따라서 유한소수(0.35)로 나타낼 수 있다.",
            points=10
        ),
        mc(
            id="m2-comp-002",
            concept_id="concept-m2-rational",
            category="computation",
            part="calc",
            difficulty=4,
            content="분수 5/12를 약분한 후 분모의 소인수를 구하면? (작은 수부터)",
            options=["2, 3", "2, 5", "3, 5", "2만"],
            correct="A",
            explanation="5/12는 이미 기약분수이다. 분모 12=2²×3이므로 소인수는 2와 3이다. 2와 5뿐이 아니므로 유한소수로 나타낼 수 없다.",
            points=10
        ),
        mc(
            id="m2-comp-003",
            concept_id="concept-m2-rational",
            category="computation",
            part="calc",
            difficulty=6,
            content="순환소수 0.333...을 분수로 나타내면? (기약분수)",
            options=["1/3", "3/10", "33/100", "1/9"],
            correct="A",
            explanation="x = 0.333..., 10x = 3.333...이므로 10x - x = 3, 9x = 3, x = 1/3",
            points=10
        ),
        mc(
            id="m2-comp-004",
            concept_id="concept-m2-rational",
            category="computation",
            part="calc",
            difficulty=8,
            content="0.999...는 1과 같다는 것을 증명하는 과정이다. 빈칸에 알맞은 식은?\n\nx = 0.999...\n10x = 9.999...\n10x - x = [?]\n9x = 9\nx = 1",
            options=["9", "9.999... - 0.999...", "9 + 0.999...", "8.999..."],
            correct="A",
            explanation="10x - x = 9.999... - 0.999... = 9 (소수 부분이 상쇄됨). 따라서 9x=9, x=1이 되어 0.999...=1임을 증명한다.",
            points=10
        ),

        # 식의 계산 - 지수법칙 (4문제, 난이도 3~9)
        mc(
            id="m2-comp-005",
            concept_id="concept-m2-expression",
            category="computation",
            part="algebra",
            difficulty=3,
            content="a³ × a²를 계산하시오.",
            options=["a⁵", "a⁶", "a", "2a⁵"],
            correct="A",
            explanation="지수법칙: a^m × a^n = a^(m+n)이므로 a³ × a² = a^(3+2) = a⁵",
            points=10
        ),
        mc(
            id="m2-comp-006",
            concept_id="concept-m2-expression",
            category="computation",
            part="algebra",
            difficulty=5,
            content="(a³)²를 계산하시오.",
            options=["a⁶", "a⁵", "a⁹", "2a³"],
            correct="A",
            explanation="지수법칙: (a^m)^n = a^(mn)이므로 (a³)² = a^(3×2) = a⁶",
            points=10
        ),
        mc(
            id="m2-comp-007",
            concept_id="concept-m2-expression",
            category="computation",
            part="algebra",
            difficulty=7,
            content="(2x²y)³을 계산하시오.",
            options=["8x⁶y³", "2x⁶y³", "6x⁶y³", "8x⁵y³"],
            correct="A",
            explanation="분배법칙으로 각 인수에 지수를 적용: 2³ × (x²)³ × y³ = 8 × x⁶ × y³ = 8x⁶y³",
            points=10
        ),
        mc(
            id="m2-comp-008",
            concept_id="concept-m2-expression",
            category="computation",
            part="algebra",
            difficulty=9,
            content="a² ÷ a⁵를 계산하시오. (단, a≠0)",
            options=["1/a³", "a³", "1/a⁷", "a⁻³"],
            correct="A",
            explanation="분수로 나타내면 a²/a⁵ = (a×a)/(a×a×a×a×a) = 1/(a×a×a) = 1/a³",
            points=10
        ),

        # 부등식과 연립방정식 (4문제, 난이도 4~10)
        mc(
            id="m2-comp-009",
            concept_id="concept-m2-inequality",
            category="computation",
            part="algebra",
            difficulty=4,
            content="일차부등식 -2x > 4를 풀면?",
            options=["x < -2", "x > -2", "x < 2", "x > 2"],
            correct="A",
            explanation="양변을 -2로 나누면 부등호 방향이 바뀐다: x < 4/(-2) = x < -2",
            points=10
        ),
        mc(
            id="m2-comp-010",
            concept_id="concept-m2-inequality",
            category="computation",
            part="algebra",
            difficulty=6,
            content="연립방정식 x+y=5, x-y=1을 가감법으로 풀면?",
            options=["x=3, y=2", "x=2, y=3", "x=4, y=1", "x=1, y=4"],
            correct="A",
            explanation="두 식을 더하면 2x=6, x=3. 첫 번째 식에 대입하면 3+y=5, y=2",
            points=10
        ),
        mc(
            id="m2-comp-011",
            concept_id="concept-m2-inequality",
            category="computation",
            part="algebra",
            difficulty=8,
            content="연립방정식 3x+2y=12, 2x+y=7을 풀면?",
            options=["x=2, y=3", "x=3, y=2", "x=1, y=5", "x=4, y=0"],
            correct="A",
            explanation="두 번째 식을 2배: 4x+2y=14. 첫 번째 식을 빼면 x=2. 대입하면 2(2)+y=7, y=3",
            points=10
        ),
        mc(
            id="m2-comp-012",
            concept_id="concept-m2-inequality",
            category="computation",
            part="algebra",
            difficulty=10,
            content="연립방정식 2x-3y=1, 4x-6y=2의 해는?",
            options=["무수히 많다", "x=0, y=0", "x=1, y=1/3", "해가 없다"],
            correct="A",
            explanation="두 번째 식은 첫 번째 식의 2배이므로 두 식이 일치한다. 따라서 해가 무수히 많다(부정).",
            points=10
        ),
    ]

    tests = [
        test(
            id="test-m2-computation",
            title="중2 연산 종합 테스트",
            description="유리수와 순환소수, 식의 계산, 부등식 연산",
            grade="middle_2",
            concept_ids=["concept-m2-rational", "concept-m2-expression", "concept-m2-inequality"],
            question_ids=[f"m2-comp-{i:03d}" for i in range(1, 13)],
            time_limit_minutes=20,
            use_question_pool=True,
            questions_per_attempt=10,
        ),
    ]

    return {
        "concepts": concepts,
        "questions": questions,
        "tests": tests,
    }
