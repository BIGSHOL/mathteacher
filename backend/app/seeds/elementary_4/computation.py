"""초등 4학년 연산 문제 시드 데이터.

커버 단원:
  1학기 1단원 - 큰 수
  1학기 3단원 - 곱셈과 나눗셈
  2학기 1단원 - 분수의 덧셈과 뺄셈
  2학기 3단원 - 소수의 덧셈과 뺄셈
"""
from app.seeds._base import mc, concept


def get_concepts():
    """연산 관련 개념 반환."""
    return [
        concept(
            id="concept-e4-big-num",
            name="큰 수",
            grade="elementary_4",
            category="computation",
            part="calc",
            description="만, 억, 조 단위의 큰 수를 읽고 쓸 수 있으며, 10배의 원리와 수의 크기 비교를 이해합니다.",
        ),
        concept(
            id="concept-e4-mul-div",
            name="곱셈과 나눗셈",
            grade="elementary_4",
            category="computation",
            part="calc",
            description="(세 자리 수)×(두 자리 수), (세 자리 수)÷(두 자리 수) 계산과 검산(나누는 수×몫+나머지=나누어지는 수)을 할 수 있습니다.",
        ),
        concept(
            id="concept-e4-frac-op",
            name="분수의 덧셈과 뺄셈",
            grade="elementary_4",
            category="computation",
            part="calc",
            description="분모가 같은 분수의 덧셈·뺄셈, 대분수의 덧셈·뺄셈(받아내림 포함)을 이해하고 계산할 수 있습니다.",
        ),
        concept(
            id="concept-e4-dec-op",
            name="소수의 덧셈과 뺄셈",
            grade="elementary_4",
            category="computation",
            part="calc",
            description="소수의 크기 비교, 소수점 위치를 맞추어 정렬한 덧셈과 뺄셈을 할 수 있습니다.",
        ),
    ]


def get_questions():
    """연산 문제 반환."""
    return [
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 1단원: 큰 수
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e4-comp-001",
            concept_id="concept-e4-big-num",
            category="computation",
            part="calc",
            difficulty=2,
            content="삼억 오천만을 숫자로 바르게 쓴 것은?",
            options=[
                ("35000000", "35000000"),
                ("305000000", "305000000"),
                ("350000000", "350000000"),
                ("3500000000", "3500000000"),
            ],
            correct="C",
            explanation="삼억 오천만 = 3억 5000만 = 350,000,000입니다. 억 자리에 3, 천만 자리에 5를 쓰고 나머지는 0으로 채웁니다. 0이 포함된 큰 수를 쓸 때 빈 자리를 누락하지 않도록 주의합니다.",
            points=10,
        ),
        mc(
            id="e4-comp-002",
            concept_id="concept-e4-big-num",
            category="computation",
            part="calc",
            difficulty=4,
            content="50000에서 숫자 5가 나타내는 값은?",
            options=[
                ("5", "5"),
                ("500", "500"),
                ("5000", "5000"),
                ("50000", "50000"),
            ],
            correct="D",
            explanation="50000에서 5는 만의 자리에 있으므로 5가 나타내는 값(자릿값)은 50000입니다. 숫자 자체(5)와 자릿값(50000)을 구별해야 합니다.",
            points=10,
        ),
        mc(
            id="e4-comp-003",
            concept_id="concept-e4-big-num",
            category="computation",
            part="calc",
            difficulty=6,
            content="다음 중 가장 큰 수는?",
            options=[
                ("9억 9800만", "9억 9800만"),
                ("10억 50만", "10억 50만"),
                ("9억 9999만", "9억 9999만"),
                ("10억", "10억"),
            ],
            correct="B",
            explanation="각 수를 비교하면 A=998,000,000, B=1,000,500,000, C=999,900,000, D=1,000,000,000입니다. 자릿수가 같으면 최상위 자릿수부터 비교합니다. 10억 50만(B)이 가장 큽니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 3단원: 곱셈과 나눗셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e4-comp-004",
            concept_id="concept-e4-mul-div",
            category="computation",
            part="calc",
            difficulty=3,
            content="245 × 13을 계산하세요.",
            options=[
                ("3085", "3085"),
                ("3185", "3185"),
                ("3285", "3285"),
                ("3385", "3385"),
            ],
            correct="B",
            explanation="245 × 13 = 3185입니다. 245×3=735, 245×10=2450, 735+2450=3185입니다. 세로셈에서 자릿수를 정확히 맞추어야 합니다.",
            points=10,
        ),
        mc(
            id="e4-comp-005",
            concept_id="concept-e4-mul-div",
            category="computation",
            part="calc",
            difficulty=5,
            content="756 ÷ 12를 계산하세요.",
            options=[
                ("61", "61"),
                ("62", "62"),
                ("63", "63"),
                ("64", "64"),
            ],
            correct="C",
            explanation="756 ÷ 12 = 63입니다. 검산: 12 × 63 = 756이므로 정답입니다. 몫을 가늠할 때 12×60=720, 12×70=840이므로 몫은 60~70 사이입니다.",
            points=10,
        ),
        mc(
            id="e4-comp-006",
            concept_id="concept-e4-mul-div",
            category="computation",
            part="calc",
            difficulty=8,
            content="빵 365개를 한 상자에 24개씩 담으려 합니다. 모든 빵을 담으려면 상자는 최소 몇 개 필요한가요?",
            options=[
                ("14개", "14개"),
                ("15개", "15개"),
                ("16개", "16개"),
                ("17개", "17개"),
            ],
            correct="C",
            explanation="365 ÷ 24 = 15 나머지 5입니다. 나머지 5개도 상자에 담아야 하므로 15+1=16개가 필요합니다. 나머지를 맥락에 맞게 해석(올림)하는 것이 중요합니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 1단원: 분수의 덧셈과 뺄셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e4-comp-007",
            concept_id="concept-e4-frac-op",
            category="computation",
            part="calc",
            difficulty=2,
            content="3/8 + 2/8을 계산하세요.",
            options=[
                ("5/16", "5/16"),
                ("5/8", "5/8"),
                ("6/8", "6/8"),
                ("1/8", "1/8"),
            ],
            correct="B",
            explanation="분모가 같은 분수의 덧셈은 분모는 그대로 두고 분자끼리 더합니다. 3/8 + 2/8 = 5/8입니다. 5/16(분모끼리 더한 결과)은 틀린 답입니다.",
            points=10,
        ),
        mc(
            id="e4-comp-008",
            concept_id="concept-e4-frac-op",
            category="computation",
            part="calc",
            difficulty=5,
            content="1/3 + 1/3의 계산으로 올바른 것은?",
            options=[
                ("2/6", "2/6"),
                ("2/3", "2/3"),
                ("1/6", "1/6"),
                ("1/3", "1/3"),
            ],
            correct="B",
            explanation="분모가 같은 분수의 덧셈은 분자끼리만 더합니다. 1/3 + 1/3 = 2/3입니다. 분모끼리 더해 2/6으로 계산하는 것은 가장 흔한 오류입니다.",
            points=10,
        ),
        mc(
            id="e4-comp-009",
            concept_id="concept-e4-frac-op",
            category="computation",
            part="calc",
            difficulty=8,
            content="3 - 2/5를 계산하세요.",
            options=[
                ("1/5", "1/5"),
                ("2 3/5", "2 3/5"),
                ("1 2/5", "1 2/5"),
                ("2 2/5", "2 2/5"),
            ],
            correct="B",
            explanation="자연수에서 분수를 빼려면 3을 2 5/5로 바꿉니다. 2 5/5 - 2/5 = 2 3/5입니다. 자연수에서 1을 빌려와 분모와 같은 분자의 가분수로 만드는 것이 핵심입니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 3단원: 소수의 덧셈과 뺄셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e4-comp-010",
            concept_id="concept-e4-dec-op",
            category="computation",
            part="calc",
            difficulty=2,
            content="0.3 + 0.5를 계산하세요.",
            options=[
                ("0.2", "0.2"),
                ("0.8", "0.8"),
                ("0.35", "0.35"),
                ("8", "8"),
            ],
            correct="B",
            explanation="0.3 + 0.5 = 0.8입니다. 소수 첫째 자리끼리 더하면 3+5=8이므로 0.8입니다.",
            points=10,
        ),
        mc(
            id="e4-comp-011",
            concept_id="concept-e4-dec-op",
            category="computation",
            part="calc",
            difficulty=5,
            content="0.125와 0.5 중 더 큰 수는?",
            options=[
                ("0.125 (자릿수가 더 많으므로)", "0.125 (자릿수가 더 많으므로)"),
                ("0.5", "0.5"),
                ("같다", "같다"),
                ("비교할 수 없다", "비교할 수 없다"),
            ],
            correct="B",
            explanation="소수의 크기를 비교할 때는 소수점 아래 같은 자리부터 비교합니다. 0.125=0.125, 0.5=0.500이므로 0.5가 더 큽니다. '소수가 길면 크다'는 착각은 흔한 오류입니다.",
            points=10,
        ),
        mc(
            id="e4-comp-012",
            concept_id="concept-e4-dec-op",
            category="computation",
            part="calc",
            difficulty=7,
            content="2.5 + 1.38을 계산하세요.",
            options=[
                ("3.43", "3.43"),
                ("3.88", "3.88"),
                ("1.63", "1.63"),
                ("3.83", "3.83"),
            ],
            correct="B",
            explanation="소수점을 맞추어 세로로 정렬합니다. 2.50 + 1.38 = 3.88입니다. 2.5를 2.50으로 바꾸어 자릿수를 맞추는 것이 핵심입니다.",
            points=10,
        ),
    ]
