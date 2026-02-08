"""초등학교 3학년 빈칸 채우기 문제 시드 데이터.

12단원 전체 커버 (단원당 2문항):
  1학기: 덧셈과 뺄셈, 평면도형, 나눗셈, 곱셈, 길이와 시간, 분수와 소수
  2학기: 곱셈 (2), 나눗셈 (2), 원, 분수 (2), 들이와 무게, 자료의 정리
"""

from .._base import fb


def get_questions() -> list[dict]:
    """빈칸 채우기 문제 24개 반환 (단원당 2개)."""
    return [
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 1단원: 덧셈과 뺄셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e3-1-1-1-fb-004",
            concept_id="e3-1-1-1",
            category="computation",
            part="calc",
            difficulty=3,
            content="456 + 287 = ____",
            answer="743",
            explanation="456 + 287 = 743입니다. "
            "일의 자리: 6+7=13 (1 올림), 십의 자리: 5+8+1=14 (1 올림), 백의 자리: 4+2+1=7",
            accept_formats=["743"],
        ),
        fb(
            id="e3-1-1-2-fb-004",
            concept_id="e3-1-1-2",
            category="computation",
            part="calc",
            difficulty=4,
            content="612 - 348 = ____",
            answer="264",
            explanation="612 - 348 = 264입니다. "
            "받아내림을 올바르게 처리해야 합니다. 일의 자리에서 십의 자리로, 십의 자리에서 백의 자리로 빌려옵니다.",
            accept_formats=["264"],
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 2단원: 평면도형
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e3-1-2-2-fb-001",
            concept_id="e3-1-2-2",
            category="concept",
            part="geo",
            difficulty=4,
            content="종이를 반듯하게 두 번 접었을 때 생기는 각을 ____이라고 합니다.",
            answer="직각",
            explanation="직각의 정의: 종이를 반듯하게 두 번 접았을 때 생기는 각입니다. 90도입니다.",
            accept_formats=["직각"],
        ),
        fb(
            id="e3-1-2-2-fb-002",
            concept_id="e3-1-2-2",
            category="concept",
            part="geo",
            difficulty=5,
            content="한 점에서 그은 두 반직선으로 이루어진 도형을 ____이라고 합니다.",
            answer="각",
            explanation="각의 정의: 한 점(꼭짓점)에서 그은 두 반직선(변)으로 이루어진 도형입니다.",
            accept_formats=["각"],
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 3단원: 나눗셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e3-1-3-1-fb-001",
            concept_id="e3-1-3-1",
            category="computation",
            part="calc",
            difficulty=3,
            content="18 ÷ 3 = ____",
            answer="6",
            explanation="18 ÷ 3 = 6입니다. 검산: 3 × 6 = 18",
            accept_formats=["6"],
        ),
        fb(
            id="e3-1-3-1-fb-002",
            concept_id="e3-1-3-1",
            category="computation",
            part="calc",
            difficulty=5,
            content="사과 24개를 4개씩 묶으면 ____ 묶음입니다.",
            answer="6",
            explanation="24 ÷ 4 = 6묶음입니다. 이것은 포함제 나눗셈입니다.",
            accept_formats=["6"],
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 4단원: 곱셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e3-1-4-1-fb-001",
            concept_id="e3-1-4-1",
            category="computation",
            part="calc",
            difficulty=3,
            content="34 × 2 = ____",
            answer="68",
            explanation="34 × 2 = (30 + 4) × 2 = 60 + 8 = 68입니다.",
            accept_formats=["68"],
        ),
        fb(
            id="e3-1-4-2-fb-001",
            concept_id="e3-1-4-2",
            category="computation",
            part="calc",
            difficulty=4,
            content="52 × 3 = ____",
            answer="156",
            explanation="52 × 3 = (50 + 2) × 3 = 150 + 6 = 156입니다.",
            accept_formats=["156"],
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 5단원: 길이와 시간
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e3-1-5-1-fb-001",
            concept_id="e3-1-5-1",
            category="concept",
            part="calc",
            difficulty=4,
            content="1cm = ____ mm",
            answer="10",
            explanation="1cm = 10mm입니다. 길이 단위 변환을 기억하세요.",
            accept_formats=["10"],
        ),
        fb(
            id="e3-1-5-2-fb-001",
            concept_id="e3-1-5-2",
            category="concept",
            part="calc",
            difficulty=5,
            content="2시간 30분 + 1시간 40분 = ____ 시간 ____ 분",
            answer="4시간 10분",
            explanation="30분 + 40분 = 70분 = 1시간 10분입니다. "
            "2시간 + 1시간 + 1시간 10분 = 4시간 10분입니다. 60진법을 잊지 마세요!",
            accept_formats=["4시간 10분", "4 10"],
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 6단원: 분수와 소수
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e3-1-6-1-fb-001",
            concept_id="e3-1-6-1",
            category="concept",
            part="calc",
            difficulty=4,
            content="전체를 5등분했을 때 한 조각은 전체의 ____입니다. (분수로 쓰세요)",
            answer="1/5",
            explanation="전체를 5등분하면 한 조각은 1/5입니다. 이것을 단위분수라고 합니다.",
            accept_formats=["1/5"],
        ),
        fb(
            id="e3-1-6-2-fb-001",
            concept_id="e3-1-6-2",
            category="concept",
            part="calc",
            difficulty=6,
            content="1/10을 소수로 나타내면 ____입니다.",
            answer="0.1",
            explanation="1/10 = 0.1입니다. 소수 0.1은 '영 점 일'이라고 읽습니다.",
            accept_formats=["0.1"],
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 7단원: 곱셈 (2)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e3-2-1-1-fb-001",
            concept_id="e3-2-1-1",
            category="computation",
            part="calc",
            difficulty=5,
            content="123 × 4 = ____",
            answer="492",
            explanation="123 × 4 = (100 + 20 + 3) × 4 = 400 + 80 + 12 = 492입니다.",
            accept_formats=["492"],
        ),
        fb(
            id="e3-2-1-2-fb-001",
            concept_id="e3-2-1-2",
            category="computation",
            part="calc",
            difficulty=7,
            content="23 × 14 = ____",
            answer="322",
            explanation="23 × 14 = 23 × (10 + 4) = 23 × 10 + 23 × 4 = 230 + 92 = 322입니다. "
            "십의 자리 계산에서 0을 빠뜨리지 않도록 주의하세요!",
            accept_formats=["322"],
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 8단원: 나눗셈 (2)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e3-2-2-1-fb-001",
            concept_id="e3-2-2-1",
            category="computation",
            part="calc",
            difficulty=4,
            content="17 ÷ 5 = 3 ... ____",
            answer="2",
            explanation="17 ÷ 5 = 3 ... 2입니다. 검산: 5 × 3 + 2 = 17 (나머지 2 < 나누는 수 5)",
            accept_formats=["2"],
        ),
        fb(
            id="e3-2-2-1-fb-002",
            concept_id="e3-2-2-1",
            category="computation",
            part="calc",
            difficulty=6,
            content="나눗셈에서 나머지는 항상 나누는 수보다 ____ 합니다. (작아야/커야 중 선택)",
            answer="작아야",
            explanation="나머지 < 나누는 수 조건은 나눗셈의 필수 규칙입니다. "
            "나머지가 나누는 수보다 크거나 같으면 한 번 더 나눌 수 있으므로 계산이 끝나지 않은 것입니다.",
            accept_formats=["작아야"],
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 9단원: 원
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e3-2-3-1-fb-001",
            concept_id="e3-2-3-1",
            category="concept",
            part="geo",
            difficulty=3,
            content="원의 중심에서 원 위의 한 점까지 이은 선분을 ____이라고 합니다.",
            answer="반지름",
            explanation="반지름의 정의: 원의 중심에서 원 위의 한 점까지 이은 선분입니다. 한 원에서 모든 반지름의 길이는 같습니다.",
            accept_formats=["반지름"],
        ),
        fb(
            id="e3-2-3-2-fb-001",
            concept_id="e3-2-3-2",
            category="concept",
            part="geo",
            difficulty=5,
            content="반지름이 6cm인 원의 지름은 ____ cm입니다.",
            answer="12",
            explanation="지름 = 반지름 × 2 = 6 × 2 = 12cm입니다.",
            accept_formats=["12"],
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 10단원: 분수 (2)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e3-2-4-2-fb-001",
            concept_id="e3-2-4-2",
            category="concept",
            part="calc",
            difficulty=4,
            content="3/8 + 2/8 = ____",
            answer="5/8",
            explanation="분모가 같은 분수의 덧셈: 분모는 그대로 두고 분자끼리 더합니다. "
            "3/8 + 2/8 = (3+2)/8 = 5/8입니다.",
            accept_formats=["5/8"],
        ),
        fb(
            id="e3-2-4-1-fb-001",
            concept_id="e3-2-4-1",
            category="concept",
            part="calc",
            difficulty=6,
            content="분자가 분모보다 크거나 같은 분수를 ____라고 합니다.",
            answer="가분수",
            explanation="가분수: 분자 ≥ 분모인 분수입니다. (예: 7/5, 8/3)",
            accept_formats=["가분수"],
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 11단원: 들이와 무게
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e3-2-5-1-fb-001",
            concept_id="e3-2-5-1",
            category="concept",
            part="calc",
            difficulty=3,
            content="1L = ____ mL",
            answer="1000",
            explanation="1L = 1000mL입니다. 들이 단위 변환을 기억하세요.",
            accept_formats=["1000"],
        ),
        fb(
            id="e3-2-5-1-fb-002",
            concept_id="e3-2-5-1",
            category="concept",
            part="calc",
            difficulty=4,
            content="1kg = ____ g",
            answer="1000",
            explanation="1kg = 1000g입니다. 무게 단위 변환을 기억하세요.",
            accept_formats=["1000"],
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 12단원: 자료의 정리
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        fb(
            id="e3-2-6-2-fb-001",
            concept_id="e3-2-6-2",
            category="concept",
            part="data",
            difficulty=5,
            content="그림그래프에서 그림 1개가 나타내는 수를 ____라고 합니다.",
            answer="범례",
            explanation="범례: 그림그래프에서 그림 하나가 나타내는 수량의 기준입니다. "
            "범례를 확인하지 않으면 그래프를 잘못 읽게 됩니다.",
            accept_formats=["범례"],
        ),
        fb(
            id="e3-2-6-2-fb-002",
            concept_id="e3-2-6-2",
            category="concept",
            part="data",
            difficulty=6,
            content="그림그래프에서 별 1개 = 5명입니다. 별 4개는 ____ 명을 나타냅니다.",
            answer="20",
            explanation="별 1개 = 5명이므로, 별 4개 = 5 × 4 = 20명입니다. "
            "범례를 이용해 계산해야 합니다.",
            accept_formats=["20"],
        ),
    ]
