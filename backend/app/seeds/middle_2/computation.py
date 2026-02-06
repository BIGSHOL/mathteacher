"""중2 연산 카테고리 시드 데이터 - 2022 개정 교육과정.

1단원: 유리수와 순환소수
2단원: 식의 계산
3-1단원: 일차부등식
3-2단원: 연립일차방정식
"""

from .._base import mc, concept, test


def get_computation_data() -> dict:
    """연산 카테고리 데이터 반환."""
    concepts = [
        # ── 1단원: 유리수와 순환소수 (2개) ──
        concept(
            id="concept-m2-rational-01",
            name="유한소수 판별",
            grade="middle_2",
            category="computation",
            part="calc",
            description="유리수의 정의(a/b), 기약분수의 분모 소인수가 2와 5뿐이면 유한소수, 유한소수 판별 3단계(약분→소인수분해→판단)",
        ),
        concept(
            id="concept-m2-rational-02",
            name="순환소수와 분수 변환",
            grade="middle_2",
            category="computation",
            part="calc",
            description="순환소수의 정의와 순환마디, 순환소수↔분수 변환(10x-x 방법), 0.999...=1 증명",
        ),
        # ── 2단원: 식의 계산 (2개) ──
        concept(
            id="concept-m2-expr-01",
            name="지수법칙",
            grade="middle_2",
            category="computation",
            part="algebra",
            description="a^m×a^n=a^(m+n), (a^m)^n=a^(mn), (ab)^n=a^n·b^n, 거듭제곱의 정의로부터 유도",
        ),
        concept(
            id="concept-m2-expr-02",
            name="다항식의 계산",
            grade="middle_2",
            category="computation",
            part="algebra",
            description="단항식·다항식의 곱셈/나눗셈, 동류항 정리, 분배법칙 전개, 지수법칙 복합 적용",
        ),
        # ── 3-1단원: 일차부등식 (2개) ──
        concept(
            id="concept-m2-ineq-01",
            name="부등식의 성질과 풀이",
            grade="middle_2",
            category="computation",
            part="algebra",
            description="부등호의 의미, 부등식의 성질(양변에 같은 수 더하기/빼기/곱하기/나누기), 음수 곱·나눗셈 시 부등호 방향 반전, 수직선 표현",
        ),
        concept(
            id="concept-m2-ineq-02",
            name="일차부등식의 활용",
            grade="middle_2",
            category="computation",
            part="algebra",
            description="복합 일차부등식 풀이, 분배법칙 활용, 실생활 맥락 부등식 모델링, 연립부등식",
        ),
        # ── 3-2단원: 연립일차방정식 (2개) ──
        concept(
            id="concept-m2-simul-01",
            name="연립방정식의 풀이",
            grade="middle_2",
            category="computation",
            part="algebra",
            description="가감법(한 문자 소거), 대입법(한 식을 다른 식에 대입), 계수 맞추기, 풀이 전략 선택",
        ),
        concept(
            id="concept-m2-simul-02",
            name="연립방정식의 해의 해석",
            grade="middle_2",
            category="computation",
            part="algebra",
            description="해의 기하학적 의미(두 직선의 교점), 해의 특수성: 해 1개(일반), 해 없음(불능·평행), 해 무수히 많음(부정·일치)",
        ),
    ]

    # ── 유리수와 순환소수 (4문제) ──
    rational_questions = [
        mc(
            id="m2-comp-001",
            concept_id="concept-m2-rational-01",
            category="computation",
            part="calc",
            difficulty=2,
            content="분수 7/20을 소수로 나타낼 때, 유한소수인지 무한소수인지 판별하시오.",
            options=["유한소수", "순환소수", "무한소수이지만 순환하지 않음", "소수로 나타낼 수 없음"],
            correct="A",
            explanation="분모 20=2²×5이므로 소인수가 2와 5뿐이다. 따라서 유한소수(0.35)로 나타낼 수 있다.",
            points=10,
        ),
        mc(
            id="m2-comp-002",
            concept_id="concept-m2-rational-01",
            category="computation",
            part="calc",
            difficulty=4,
            content="분수 5/12를 약분한 후 분모의 소인수를 구하면? (작은 수부터)",
            options=["2, 3", "2, 5", "3, 5", "2만"],
            correct="A",
            explanation="5/12는 이미 기약분수이다. 분모 12=2²×3이므로 소인수는 2와 3이다. 2와 5뿐이 아니므로 유한소수로 나타낼 수 없다.",
            points=10,
        ),
        mc(
            id="m2-comp-003",
            concept_id="concept-m2-rational-02",
            category="computation",
            part="calc",
            difficulty=6,
            content="순환소수 0.333...을 분수로 나타내면? (기약분수)",
            options=["1/3", "3/10", "33/100", "1/9"],
            correct="A",
            explanation="x = 0.333..., 10x = 3.333...이므로 10x - x = 3, 9x = 3, x = 1/3",
            points=10,
        ),
        mc(
            id="m2-comp-004",
            concept_id="concept-m2-rational-02",
            category="computation",
            part="calc",
            difficulty=8,
            content="0.999...는 1과 같다는 것을 증명하는 과정이다. 빈칸에 알맞은 식은?\n\nx = 0.999...\n10x = 9.999...\n10x - x = [?]\n9x = 9\nx = 1",
            options=["9", "9.999... - 0.999...", "9 + 0.999...", "8.999..."],
            correct="A",
            explanation="10x - x = 9.999... - 0.999... = 9 (소수 부분이 상쇄됨). 따라서 9x=9, x=1이 되어 0.999...=1임을 증명한다.",
            points=10,
        ),
    ]

    # ── 식의 계산 (4문제) ──
    expression_questions = [
        mc(
            id="m2-comp-005",
            concept_id="concept-m2-expr-01",
            category="computation",
            part="algebra",
            difficulty=3,
            content="a³ × a²를 계산하시오.",
            options=["a⁵", "a⁶", "a", "2a⁵"],
            correct="A",
            explanation="지수법칙: a^m × a^n = a^(m+n)이므로 a³ × a² = a^(3+2) = a⁵",
            points=10,
        ),
        mc(
            id="m2-comp-006",
            concept_id="concept-m2-expr-01",
            category="computation",
            part="algebra",
            difficulty=5,
            content="(a³)²를 계산하시오.",
            options=["a⁶", "a⁵", "a⁹", "2a³"],
            correct="A",
            explanation="지수법칙: (a^m)^n = a^(mn)이므로 (a³)² = a^(3×2) = a⁶",
            points=10,
        ),
        mc(
            id="m2-comp-007",
            concept_id="concept-m2-expr-02",
            category="computation",
            part="algebra",
            difficulty=7,
            content="(2x²y)³을 계산하시오.",
            options=["8x⁶y³", "2x⁶y³", "6x⁶y³", "8x⁵y³"],
            correct="A",
            explanation="분배법칙으로 각 인수에 지수를 적용: 2³ × (x²)³ × y³ = 8 × x⁶ × y³ = 8x⁶y³",
            points=10,
        ),
        mc(
            id="m2-comp-008",
            concept_id="concept-m2-expr-02",
            category="computation",
            part="algebra",
            difficulty=9,
            content="a² ÷ a⁵를 계산하시오. (단, a≠0)",
            options=["1/a³", "a³", "1/a⁷", "a⁻³"],
            correct="A",
            explanation="분수로 나타내면 a²/a⁵ = (a×a)/(a×a×a×a×a) = 1/(a×a×a) = 1/a³",
            points=10,
        ),
    ]

    # ── 일차부등식 (3문제) ──
    inequality_questions = [
        mc(
            id="m2-comp-009",
            concept_id="concept-m2-ineq-01",
            category="computation",
            part="algebra",
            difficulty=4,
            content="일차부등식 -2x > 4를 풀면?",
            options=["x < -2", "x > -2", "x < 2", "x > 2"],
            correct="A",
            explanation="양변을 -2로 나누면 부등호 방향이 바뀐다: x < 4/(-2) = x < -2",
            points=10,
        ),
        mc(
            id="m2-comp-010",
            concept_id="concept-m2-ineq-01",
            category="computation",
            part="algebra",
            difficulty=6,
            content="부등식 3x - 5 ≤ 7을 풀면?",
            options=["x ≤ 4", "x ≥ 4", "x ≤ 2/3", "x ≥ 2/3"],
            correct="A",
            explanation="3x ≤ 12, x ≤ 4. 양수로 나누므로 부등호 방향은 그대로 유지된다.",
            points=10,
        ),
        mc(
            id="m2-comp-011",
            concept_id="concept-m2-ineq-02",
            category="computation",
            part="algebra",
            difficulty=8,
            content="부등식 -3(x - 2) < 6을 풀면?",
            options=["x > 0", "x < 0", "x > -4", "x < 4"],
            correct="A",
            explanation="-3x + 6 < 6, -3x < 0, 양변을 -3으로 나누면 부등호 반전: x > 0",
            points=10,
        ),
    ]

    # ── 연립일차방정식 (3문제) ──
    simultaneous_questions = [
        mc(
            id="m2-comp-012",
            concept_id="concept-m2-simul-01",
            category="computation",
            part="algebra",
            difficulty=5,
            content="연립방정식 x+y=5, x-y=1을 가감법으로 풀면?",
            options=["x=3, y=2", "x=2, y=3", "x=4, y=1", "x=1, y=4"],
            correct="A",
            explanation="두 식을 더하면 2x=6, x=3. 첫 번째 식에 대입하면 3+y=5, y=2",
            points=10,
        ),
        mc(
            id="m2-comp-013",
            concept_id="concept-m2-simul-01",
            category="computation",
            part="algebra",
            difficulty=7,
            content="연립방정식 3x+2y=12, 2x+y=7을 풀면?",
            options=["x=2, y=3", "x=3, y=2", "x=1, y=5", "x=4, y=0"],
            correct="A",
            explanation="두 번째 식을 2배: 4x+2y=14. 첫 번째 식을 빼면 x=2. 대입하면 2(2)+y=7, y=3",
            points=10,
        ),
        mc(
            id="m2-comp-014",
            concept_id="concept-m2-simul-02",
            category="computation",
            part="algebra",
            difficulty=9,
            content="연립방정식 2x-3y=1, 4x-6y=2의 해는?",
            options=["무수히 많다", "x=0, y=0", "x=1, y=1/3", "해가 없다"],
            correct="A",
            explanation="두 번째 식은 첫 번째 식의 2배이므로 두 식이 일치한다. 따라서 해가 무수히 많다(부정).",
            points=10,
        ),
    ]

    questions = rational_questions + expression_questions + inequality_questions + simultaneous_questions

    tests = [
        test(
            id="test-m2-computation",
            title="중2 연산 종합 테스트",
            description="유리수와 순환소수, 식의 계산, 일차부등식, 연립일차방정식",
            grade="middle_2",
            concept_ids=[c["id"] for c in concepts],
            question_ids=[q["id"] for q in questions],
            time_limit_minutes=25,
            use_question_pool=True,
            questions_per_attempt=10,
        ),
    ]

    return {"concepts": concepts, "questions": questions, "tests": tests}
