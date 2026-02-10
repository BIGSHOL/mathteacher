"""초등학교 3학년 빈칸 채우기 문제 시드 데이터.

12단원 전체 커버, 개념별 세분화:
  1학기: 덧셈과 뺄셈, 평면도형, 나눗셈, 곱셈, 길이와 시간, 분수와 소수
  2학기: 곱셈 (2), 나눗셈 (2), 원, 분수 (2), 들이와 무게, 자료의 정리
총 72문항 (기존 24개 + 신규 48개)
"""

from .._base import fb


def get_questions() -> list[dict]:
    """빈칸 채우기 문제 72개 반환."""
    return [
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 1단원: 덧셈과 뺄셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # e3-1-1-01: 받아올림 없는 덧셈
        fb(
            id="e3-1-1-01-fb-001",
            concept_id="e3-1-1-01",
            category="computation",
            part="calc",
            difficulty=2,
            content="523 + 314 = ____",
            answer="837",
            explanation="523 + 314 = 837입니다. 각 자리 수를 더하면 받아올림이 없습니다. "
            "일의 자리: 3+4=7, 십의 자리: 2+1=3, 백의 자리: 5+3=8",
            accept_formats=["837"],
        ),

        # e3-1-1-02: 받아올림 1번 덧셈
        fb(
            id="e3-1-1-02-fb-001",
            concept_id="e3-1-1-02",
            category="computation",
            part="calc",
            difficulty=3,
            content="347 + 125 = ____",
            answer="472",
            explanation="347 + 125 = 472입니다. 일의 자리에서 7+5=12이므로 1을 올림합니다. "
            "일의 자리: 7+5=12 (1 올림), 십의 자리: 4+2+1=7, 백의 자리: 3+1=4",
            accept_formats=["472"],
        ),

        # e3-1-1-03: 받아올림 여러 번 덧셈 (기존 문제, concept_id 수정)
        fb(
            id="e3-1-1-1-fb-004",
            concept_id="e3-1-1-03",
            category="computation",
            part="calc",
            difficulty=3,
            content="456 + 287 = ____",
            answer="743",
            explanation="456 + 287 = 743입니다. "
            "일의 자리: 6+7=13 (1 올림), 십의 자리: 5+8+1=14 (1 올림), 백의 자리: 4+2+1=7",
            accept_formats=["743"],
        ),

        # e3-1-1-04: 받아내림 없는 뺄셈
        fb(
            id="e3-1-1-04-fb-001",
            concept_id="e3-1-1-04",
            category="computation",
            part="calc",
            difficulty=2,
            content="785 - 423 = ____",
            answer="362",
            explanation="785 - 423 = 362입니다. 각 자리 수를 빼면 받아내림이 없습니다. "
            "일의 자리: 5-3=2, 십의 자리: 8-2=6, 백의 자리: 7-4=3",
            accept_formats=["362"],
        ),

        # e3-1-1-05: 받아내림 1번 뺄셈
        fb(
            id="e3-1-1-05-fb-001",
            concept_id="e3-1-1-05",
            category="computation",
            part="calc",
            difficulty=3,
            content="532 - 147 = ____",
            answer="385",
            explanation="532 - 147 = 385입니다. 일의 자리에서 2-7을 할 수 없으므로 받아내립니다. "
            "일의 자리: 12-7=5 (1 빌림), 십의 자리: 2-4=? → 12-4-1=7 (1 빌림), 백의 자리: 5-1-1=3",
            accept_formats=["385"],
        ),

        # e3-1-1-06: 받아내림 두 번 뺄셈 (기존 문제, concept_id 수정)
        fb(
            id="e3-1-1-2-fb-004",
            concept_id="e3-1-1-06",
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

        # e3-1-2-01: 선분/반직선/직선
        fb(
            id="e3-1-2-01-fb-001",
            concept_id="e3-1-2-01",
            category="concept",
            part="geo",
            difficulty=3,
            content="양쪽 끝이 있는 곧은 선을 ____이라고 합니다.",
            answer="선분",
            explanation="선분: 양쪽 끝이 있는 곧은 선입니다. 반직선은 한쪽 끝만 있고, 직선은 양쪽 끝이 없습니다.",
            accept_formats=["선분"],
        ),

        # e3-1-2-02: 각의 정의 (기존 문제, concept_id 수정)
        fb(
            id="e3-1-2-2-fb-002",
            concept_id="e3-1-2-02",
            category="concept",
            part="geo",
            difficulty=5,
            content="한 점에서 그은 두 반직선으로 이루어진 도형을 ____이라고 합니다.",
            answer="각",
            explanation="각의 정의: 한 점(꼭짓점)에서 그은 두 반직선(변)으로 이루어진 도형입니다.",
            accept_formats=["각"],
        ),

        # e3-1-2-03: 직각 정의 (기존 문제, concept_id 수정)
        fb(
            id="e3-1-2-2-fb-001",
            concept_id="e3-1-2-03",
            category="concept",
            part="geo",
            difficulty=4,
            content="종이를 반듯하게 두 번 접었을 때 생기는 각을 ____이라고 합니다.",
            answer="직각",
            explanation="직각의 정의: 종이를 반듯하게 두 번 접았을 때 생기는 각입니다. 90도입니다.",
            accept_formats=["직각"],
        ),

        # e3-1-2-04: 직각삼각형
        fb(
            id="e3-1-2-04-fb-001",
            concept_id="e3-1-2-04",
            category="concept",
            part="geo",
            difficulty=4,
            content="직각이 한 개 있는 삼각형을 ____이라고 합니다.",
            answer="직각삼각형",
            explanation="직각삼각형: 세 각 중 하나가 직각(90도)인 삼각형입니다.",
            accept_formats=["직각삼각형"],
        ),

        # e3-1-2-05: 직사각형
        fb(
            id="e3-1-2-05-fb-001",
            concept_id="e3-1-2-05",
            category="concept",
            part="geo",
            difficulty=3,
            content="네 각이 모두 직각인 사각형을 ____이라고 합니다.",
            answer="직사각형",
            explanation="직사각형: 네 각이 모두 직각이고, 마주 보는 변의 길이가 같은 사각형입니다.",
            accept_formats=["직사각형"],
        ),

        # e3-1-2-06: 정사각형
        fb(
            id="e3-1-2-06-fb-001",
            concept_id="e3-1-2-06",
            category="concept",
            part="geo",
            difficulty=4,
            content="네 변의 길이가 모두 같고 네 각이 모두 직각인 사각형을 ____이라고 합니다.",
            answer="정사각형",
            explanation="정사각형: 네 변의 길이가 모두 같고 네 각이 모두 직각인 사각형입니다. 정사각형은 특별한 직사각형입니다.",
            accept_formats=["정사각형"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 3단원: 나눗셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # e3-1-3-01: 똑같이 나누기 & 포함제 (기존 문제 2개)
        fb(
            id="e3-1-3-1-fb-001",
            concept_id="e3-1-3-01",
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
            concept_id="e3-1-3-01",
            category="computation",
            part="calc",
            difficulty=5,
            content="사과 24개를 4개씩 묶으면 ____ 묶음입니다.",
            answer="6",
            explanation="24 ÷ 4 = 6묶음입니다. 이것은 포함제 나눗셈입니다.",
            accept_formats=["6"],
        ),

        # e3-1-3-02: 곱셈과 나눗셈 관계
        fb(
            id="e3-1-3-02-fb-001",
            concept_id="e3-1-3-02",
            category="concept",
            part="calc",
            difficulty=4,
            content="4 × ____ = 28이면, 28 ÷ 4 = ____입니다.",
            answer="7",
            explanation="4 × 7 = 28이므로, 28 ÷ 4 = 7입니다. 곱셈과 나눗셈은 역연산 관계입니다.",
            accept_formats=["7"],
        ),

        # e3-1-3-03: 곱셈식으로 몫 구하기
        fb(
            id="e3-1-3-03-fb-001",
            concept_id="e3-1-3-03",
            category="computation",
            part="calc",
            difficulty=4,
            content="35 ÷ 7 = ____입니다. (7 × ____ = 35를 이용하세요)",
            answer="5",
            explanation="7 × 5 = 35이므로, 35 ÷ 7 = 5입니다. 곱셈구구를 이용하여 나눗셈을 할 수 있습니다.",
            accept_formats=["5"],
        ),

        # e3-1-3-04: 곱셈구구로 몫 구하기
        fb(
            id="e3-1-3-04-fb-001",
            concept_id="e3-1-3-04",
            category="computation",
            part="calc",
            difficulty=3,
            content="56 ÷ 8 = ____",
            answer="7",
            explanation="8 × 7 = 56이므로, 56 ÷ 8 = 7입니다. 8단 곱셈구구를 이용합니다.",
            accept_formats=["7"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 4단원: 곱셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # e3-1-4-01: (몇십)×(몇)
        fb(
            id="e3-1-4-01-fb-002",
            concept_id="e3-1-4-01",
            category="computation",
            part="calc",
            difficulty=2,
            content="30 × 4 = ____",
            answer="120",
            explanation="30 × 4 = (3 × 10) × 4 = 3 × 4 × 10 = 12 × 10 = 120입니다.",
            accept_formats=["120"],
        ),

        # e3-1-4-02: 올림없는 (몇십몇)×(몇) (기존 문제, concept_id 수정)
        fb(
            id="e3-1-4-1-fb-001",
            concept_id="e3-1-4-02",
            category="computation",
            part="calc",
            difficulty=3,
            content="34 × 2 = ____",
            answer="68",
            explanation="34 × 2 = (30 + 4) × 2 = 60 + 8 = 68입니다.",
            accept_formats=["68"],
        ),

        # e3-1-4-03: 십의 자리 올림
        fb(
            id="e3-1-4-03-fb-001",
            concept_id="e3-1-4-03",
            category="computation",
            part="calc",
            difficulty=4,
            content="67 × 2 = ____",
            answer="134",
            explanation="67 × 2 = (60 + 7) × 2 = 120 + 14 = 134입니다. "
            "십의 자리로 올림이 발생합니다. 7×2=14에서 10을 올립니다.",
            accept_formats=["134"],
        ),

        # e3-1-4-04: 일의 자리 올림 (기존 문제, concept_id 수정)
        fb(
            id="e3-1-4-2-fb-001",
            concept_id="e3-1-4-04",
            category="computation",
            part="calc",
            difficulty=4,
            content="52 × 3 = ____",
            answer="156",
            explanation="52 × 3 = (50 + 2) × 3 = 150 + 6 = 156입니다.",
            accept_formats=["156"],
        ),

        # e3-1-4-05: 올림 2번
        fb(
            id="e3-1-4-05-fb-001",
            concept_id="e3-1-4-05",
            category="computation",
            part="calc",
            difficulty=5,
            content="78 × 4 = ____",
            answer="312",
            explanation="78 × 4 = 312입니다. 일의 자리: 8×4=32 (3 올림), 십의 자리: 7×4+3=31 (3 올림), 백의 자리: 3",
            accept_formats=["312"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 5단원: 길이와 시간
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # e3-1-5-01: mm↔cm 단위 (기존 문제, concept_id 수정)
        fb(
            id="e3-1-5-1-fb-001",
            concept_id="e3-1-5-01",
            category="concept",
            part="calc",
            difficulty=4,
            content="1cm = ____ mm",
            answer="10",
            explanation="1cm = 10mm입니다. 길이 단위 변환을 기억하세요.",
            accept_formats=["10"],
        ),

        # e3-1-5-02: km 단위
        fb(
            id="e3-1-5-02-fb-001",
            concept_id="e3-1-5-02",
            category="concept",
            part="calc",
            difficulty=4,
            content="1km = ____ m",
            answer="1000",
            explanation="1km = 1000m입니다. 1킬로미터는 1000미터입니다.",
            accept_formats=["1000"],
        ),

        # e3-1-5-03: 시, 분, 초 관계
        fb(
            id="e3-1-5-03-fb-001",
            concept_id="e3-1-5-03",
            category="concept",
            part="calc",
            difficulty=3,
            content="1시간 = ____ 분",
            answer="60",
            explanation="1시간 = 60분입니다. 시간은 60진법을 사용합니다.",
            accept_formats=["60"],
        ),

        # e3-1-5-04: 초 단위
        fb(
            id="e3-1-5-04-fb-001",
            concept_id="e3-1-5-04",
            category="concept",
            part="calc",
            difficulty=3,
            content="1분 = ____ 초",
            answer="60",
            explanation="1분 = 60초입니다. 시간은 60진법을 사용합니다.",
            accept_formats=["60"],
        ),

        # e3-1-5-05: 시간 덧셈 (기존 문제, concept_id 수정)
        fb(
            id="e3-1-5-2-fb-001",
            concept_id="e3-1-5-05",
            category="concept",
            part="calc",
            difficulty=5,
            content="2시간 30분 + 1시간 40분 = ____ 시간 ____ 분",
            answer="4시간 10분",
            explanation="30분 + 40분 = 70분 = 1시간 10분입니다. "
            "2시간 + 1시간 + 1시간 10분 = 4시간 10분입니다. 60진법을 잊지 마세요!",
            accept_formats=["4시간 10분", "4 10"],
        ),

        # e3-1-5-06: 시간 문제 해결
        fb(
            id="e3-1-5-06-fb-001",
            concept_id="e3-1-5-06",
            category="fill_in_blank",
            part="calc",
            difficulty=6,
            content="영화가 오후 2시 45분에 시작해서 1시간 50분 동안 상영됩니다. 끝나는 시각은 오후 ____ 시 ____ 분입니다.",
            answer="4시 35분",
            explanation="2시 45분 + 1시간 50분 = 2시 45분 + 1시간 + 50분 = 3시 45분 + 50분 = 4시 35분입니다. "
            "45분 + 50분 = 95분 = 1시간 35분",
            accept_formats=["4시 35분", "4 35"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 6단원: 분수와 소수
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # e3-1-6-01: 단위분수 개념 (기존 문제, concept_id 수정)
        fb(
            id="e3-1-6-1-fb-001",
            concept_id="e3-1-6-01",
            category="concept",
            part="calc",
            difficulty=4,
            content="전체를 5등분했을 때 한 조각은 전체의 ____입니다. (분수로 쓰세요)",
            answer="1/5",
            explanation="전체를 5등분하면 한 조각은 1/5입니다. 이것을 단위분수라고 합니다.",
            accept_formats=["1/5"],
        ),

        # e3-1-6-02: 분수 정의
        fb(
            id="e3-1-6-02-fb-001",
            concept_id="e3-1-6-02",
            category="concept",
            part="calc",
            difficulty=4,
            content="분수에서 전체를 똑같이 나눈 수를 ____라고 하고, 그 중에서 선택한 부분의 수를 ____라고 합니다.",
            answer="분모, 분자",
            explanation="분모: 전체를 똑같이 나눈 수 (아래 숫자), 분자: 선택한 부분의 수 (위 숫자)",
            accept_formats=["분모, 분자", "분모 분자", "분모,분자"],
        ),

        # e3-1-6-03: 분수로 나타내기
        fb(
            id="e3-1-6-03-fb-001",
            concept_id="e3-1-6-03",
            category="fill_in_blank",
            part="calc",
            difficulty=5,
            content="전체를 7등분하여 3조각을 선택하면 ____입니다. (분수로 쓰세요)",
            answer="3/7",
            explanation="전체를 7등분(분모)하여 3조각(분자)을 선택하면 3/7입니다.",
            accept_formats=["3/7"],
        ),

        # e3-1-6-04: 단위분수 비교
        fb(
            id="e3-1-6-04-fb-001",
            concept_id="e3-1-6-04",
            category="concept",
            part="calc",
            difficulty=5,
            content="1/3과 1/5 중에서 더 큰 분수는 ____입니다.",
            answer="1/3",
            explanation="단위분수는 분모가 작을수록 큽니다. 3 < 5이므로 1/3 > 1/5입니다. "
            "전체를 3등분한 조각이 5등분한 조각보다 큽니다.",
            accept_formats=["1/3"],
        ),

        # e3-1-6-05: 동분모 비교
        fb(
            id="e3-1-6-05-fb-001",
            concept_id="e3-1-6-05",
            category="concept",
            part="calc",
            difficulty=4,
            content="2/7과 5/7 중에서 더 큰 분수는 ____입니다.",
            answer="5/7",
            explanation="분모가 같은 분수는 분자가 클수록 큽니다. 2 < 5이므로 2/7 < 5/7입니다.",
            accept_formats=["5/7"],
        ),

        # e3-1-6-06: 소수 (기존 문제, concept_id 수정)
        fb(
            id="e3-1-6-2-fb-001",
            concept_id="e3-1-6-06",
            category="concept",
            part="calc",
            difficulty=6,
            content="1/10을 소수로 나타내면 ____입니다.",
            answer="0.1",
            explanation="1/10 = 0.1입니다. 소수 0.1은 '영 점 일'이라고 읽습니다.",
            accept_formats=["0.1"],
        ),

        # e3-1-6-07: 1보다 큰 소수
        fb(
            id="e3-1-6-07-fb-001",
            concept_id="e3-1-6-07",
            category="concept",
            part="calc",
            difficulty=5,
            content="1과 3/10을 소수로 나타내면 ____입니다.",
            answer="1.3",
            explanation="1과 3/10 = 1 + 0.3 = 1.3입니다. '일 점 삼'이라고 읽습니다.",
            accept_formats=["1.3"],
        ),

        # e3-1-6-08: 소수 비교
        fb(
            id="e3-1-6-08-fb-001",
            concept_id="e3-1-6-08",
            category="concept",
            part="calc",
            difficulty=5,
            content="0.7과 0.4 중에서 더 큰 수는 ____입니다.",
            answer="0.7",
            explanation="소수점 아래 첫째 자리를 비교합니다. 7 > 4이므로 0.7 > 0.4입니다.",
            accept_formats=["0.7"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 1단원: 곱셈 (2)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # e3-2-1-01: 올림 없는 (세 자리)×(한 자리)
        fb(
            id="e3-2-1-01-fb-001",
            concept_id="e3-2-1-01",
            category="computation",
            part="calc",
            difficulty=4,
            content="213 × 3 = ____",
            answer="639",
            explanation="213 × 3 = (200 + 10 + 3) × 3 = 600 + 30 + 9 = 639입니다. 올림이 없습니다.",
            accept_formats=["639"],
        ),

        # e3-2-1-02: 일의 자리 올림
        fb(
            id="e3-2-1-02-fb-001",
            concept_id="e3-2-1-02",
            category="computation",
            part="calc",
            difficulty=4,
            content="218 × 3 = ____",
            answer="654",
            explanation="218 × 3 = 654입니다. 일의 자리: 8×3=24 (2 올림), 십의 자리: 1×3+2=5, 백의 자리: 2×3=6",
            accept_formats=["654"],
        ),

        # e3-2-1-03: 올림 여러 번 (기존 문제, concept_id 수정)
        fb(
            id="e3-2-1-1-fb-001",
            concept_id="e3-2-1-03",
            category="computation",
            part="calc",
            difficulty=5,
            content="123 × 4 = ____",
            answer="492",
            explanation="123 × 4 = (100 + 20 + 3) × 4 = 400 + 80 + 12 = 492입니다.",
            accept_formats=["492"],
        ),

        # e3-2-1-04: (몇십)×(몇십)
        fb(
            id="e3-2-1-04-fb-001",
            concept_id="e3-2-1-04",
            category="computation",
            part="calc",
            difficulty=5,
            content="30 × 20 = ____",
            answer="600",
            explanation="30 × 20 = 3 × 10 × 2 × 10 = 3 × 2 × 100 = 6 × 100 = 600입니다.",
            accept_formats=["600"],
        ),

        # e3-2-1-05: (몇)×(몇십몇)
        fb(
            id="e3-2-1-05-fb-001",
            concept_id="e3-2-1-05",
            category="computation",
            part="calc",
            difficulty=5,
            content="4 × 23 = ____",
            answer="92",
            explanation="4 × 23 = 4 × (20 + 3) = 4 × 20 + 4 × 3 = 80 + 12 = 92입니다.",
            accept_formats=["92"],
        ),

        # e3-2-1-06: 올림 1번 (두 자리)×(두 자리)
        fb(
            id="e3-2-1-06-fb-001",
            concept_id="e3-2-1-06",
            category="computation",
            part="calc",
            difficulty=6,
            content="12 × 13 = ____",
            answer="156",
            explanation="12 × 13 = 12 × (10 + 3) = 12 × 10 + 12 × 3 = 120 + 36 = 156입니다.",
            accept_formats=["156"],
        ),

        # e3-2-1-07: 올림 여러 번 (기존 문제, concept_id 수정)
        fb(
            id="e3-2-1-2-fb-001",
            concept_id="e3-2-1-07",
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
        # 2학기 2단원: 나눗셈 (2)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # e3-2-2-01: (몇십)÷(몇)
        fb(
            id="e3-2-2-01-fb-001",
            concept_id="e3-2-2-01",
            category="computation",
            part="calc",
            difficulty=3,
            content="60 ÷ 3 = ____",
            answer="20",
            explanation="60 ÷ 3 = (6 × 10) ÷ 3 = (6 ÷ 3) × 10 = 2 × 10 = 20입니다.",
            accept_formats=["20"],
        ),

        # e3-2-2-02: 나머지 없는 (몇십몇)÷(몇)
        fb(
            id="e3-2-2-02-fb-001",
            concept_id="e3-2-2-02",
            category="computation",
            part="calc",
            difficulty=4,
            content="48 ÷ 4 = ____",
            answer="12",
            explanation="48 ÷ 4 = 12입니다. 검산: 4 × 12 = 48",
            accept_formats=["12"],
        ),

        # e3-2-2-03: 내림 있는 나눗셈
        fb(
            id="e3-2-2-03-fb-001",
            concept_id="e3-2-2-03",
            category="computation",
            part="calc",
            difficulty=5,
            content="56 ÷ 3 = ____",
            answer="18",
            explanation="56 ÷ 3 = 18...2입니다. 몫은 18, 나머지는 2입니다. 검산: 3 × 18 + 2 = 56",
            accept_formats=["18"],
        ),

        # e3-2-2-04: 나머지 있는 나눗셈 (기존 문제 2개)
        fb(
            id="e3-2-2-1-fb-001",
            concept_id="e3-2-2-04",
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
            concept_id="e3-2-2-04",
            category="computation",
            part="calc",
            difficulty=6,
            content="나눗셈에서 나머지는 항상 나누는 수보다 ____ 합니다. (작아야/커야 중 선택)",
            answer="작아야",
            explanation="나머지 < 나누는 수 조건은 나눗셈의 필수 규칙입니다. "
            "나머지가 나누는 수보다 크거나 같으면 한 번 더 나눌 수 있으므로 계산이 끝나지 않은 것입니다.",
            accept_formats=["작아야"],
        ),

        # e3-2-2-05: 내림+나머지
        fb(
            id="e3-2-2-05-fb-001",
            concept_id="e3-2-2-05",
            category="computation",
            part="calc",
            difficulty=5,
            content="73 ÷ 5 = ____ ... ____",
            answer="14 ... 3",
            explanation="73 ÷ 5 = 14 ... 3입니다. 검산: 5 × 14 + 3 = 70 + 3 = 73",
            accept_formats=["14 ... 3", "14...3", "14 3"],
        ),

        # e3-2-2-06: (세 자리)÷(한 자리) 나머지X
        fb(
            id="e3-2-2-06-fb-001",
            concept_id="e3-2-2-06",
            category="computation",
            part="calc",
            difficulty=5,
            content="246 ÷ 2 = ____",
            answer="123",
            explanation="246 ÷ 2 = 123입니다. 백의 자리부터 순서대로 나눕니다. 검산: 2 × 123 = 246",
            accept_formats=["123"],
        ),

        # e3-2-2-07: (세 자리)÷(한 자리) 나머지O
        fb(
            id="e3-2-2-07-fb-001",
            concept_id="e3-2-2-07",
            category="computation",
            part="calc",
            difficulty=6,
            content="157 ÷ 3 = ____ ... ____",
            answer="52 ... 1",
            explanation="157 ÷ 3 = 52 ... 1입니다. 검산: 3 × 52 + 1 = 156 + 1 = 157",
            accept_formats=["52 ... 1", "52...1", "52 1"],
        ),

        # e3-2-2-08: 검산
        fb(
            id="e3-2-2-08-fb-001",
            concept_id="e3-2-2-08",
            category="concept",
            part="calc",
            difficulty=6,
            content="나눗셈의 검산: (나누는 수) × (____) + (나머지) = (나누어지는 수)",
            answer="몫",
            explanation="나눗셈 검산 공식: (나누는 수) × (몫) + (나머지) = (나누어지는 수)입니다. "
            "예: 17 ÷ 5 = 3...2 → 5 × 3 + 2 = 17",
            accept_formats=["몫"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 3단원: 원
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # e3-2-3-01: 반지름 정의 (기존 문제, concept_id 수정)
        fb(
            id="e3-2-3-1-fb-001",
            concept_id="e3-2-3-01",
            category="concept",
            part="geo",
            difficulty=3,
            content="원의 중심에서 원 위의 한 점까지 이은 선분을 ____이라고 합니다.",
            answer="반지름",
            explanation="반지름의 정의: 원의 중심에서 원 위의 한 점까지 이은 선분입니다. 한 원에서 모든 반지름의 길이는 같습니다.",
            accept_formats=["반지름"],
        ),

        # e3-2-3-02: 지름 정의 (기존 문제, concept_id 수정)
        fb(
            id="e3-2-3-2-fb-001",
            concept_id="e3-2-3-02",
            category="concept",
            part="geo",
            difficulty=5,
            content="반지름이 6cm인 원의 지름은 ____ cm입니다.",
            answer="12",
            explanation="지름 = 반지름 × 2 = 6 × 2 = 12cm입니다.",
            accept_formats=["12"],
        ),

        # e3-2-3-03: 컴퍼스
        fb(
            id="e3-2-3-03-fb-001",
            concept_id="e3-2-3-03",
            category="concept",
            part="geo",
            difficulty=4,
            content="원을 그리는 도구를 ____라고 합니다.",
            answer="컴퍼스",
            explanation="컴퍼스: 원을 그리는 도구입니다. 침과 연필 사이의 거리가 반지름이 됩니다.",
            accept_formats=["컴퍼스"],
        ),

        # e3-2-3-04: 원 모양
        fb(
            id="e3-2-3-04-fb-001",
            concept_id="e3-2-3-04",
            category="fill_in_blank",
            part="geo",
            difficulty=5,
            content="반지름이 4cm인 원을 그리려면 컴퍼스의 침과 연필 사이를 ____ cm로 벌려야 합니다.",
            answer="4",
            explanation="컴퍼스의 침과 연필 사이의 거리 = 반지름 = 4cm입니다.",
            accept_formats=["4"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 4단원: 분수 (2)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # e3-2-4-01: 분수로 나타내기
        fb(
            id="e3-2-4-01-fb-001",
            concept_id="e3-2-4-01",
            category="concept",
            part="calc",
            difficulty=4,
            content="도넛 12개 중에서 5개를 먹었습니다. 먹은 도넛은 전체의 ____입니다. (분수로 쓰세요)",
            answer="5/12",
            explanation="전체 12개(분모) 중 5개(분자)를 먹었으므로 5/12입니다.",
            accept_formats=["5/12"],
        ),

        # e3-2-4-02: 전체 개수의 분수만큼
        fb(
            id="e3-2-4-02-fb-001",
            concept_id="e3-2-4-02",
            category="fill_in_blank",
            part="calc",
            difficulty=5,
            content="사탕 20개의 3/5는 ____ 개입니다.",
            answer="12",
            explanation="20개의 3/5 = 20 ÷ 5 × 3 = 4 × 3 = 12개입니다. "
            "먼저 전체를 5등분(20÷5=4)하고, 그 중 3개(4×3=12)를 구합니다.",
            accept_formats=["12"],
        ),

        # e3-2-4-03: 전체 길이의 분수만큼
        fb(
            id="e3-2-4-03-fb-001",
            concept_id="e3-2-4-03",
            category="fill_in_blank",
            part="calc",
            difficulty=5,
            content="끈 12m의 2/3는 ____ m입니다.",
            answer="8",
            explanation="12m의 2/3 = 12 ÷ 3 × 2 = 4 × 2 = 8m입니다.",
            accept_formats=["8"],
        ),

        # e3-2-4-04: 가분수 정의 (기존 문제, concept_id 수정)
        fb(
            id="e3-2-4-1-fb-001",
            concept_id="e3-2-4-04",
            category="concept",
            part="calc",
            difficulty=6,
            content="분자가 분모보다 크거나 같은 분수를 ____라고 합니다.",
            answer="가분수",
            explanation="가분수: 분자 ≥ 분모인 분수입니다. (예: 7/5, 8/3)",
            accept_formats=["가분수"],
        ),

        # e3-2-4-05: 대분수
        fb(
            id="e3-2-4-05-fb-001",
            concept_id="e3-2-4-05",
            category="concept",
            part="calc",
            difficulty=5,
            content="자연수와 진분수로 나타낸 분수를 ____라고 합니다.",
            answer="대분수",
            explanation="대분수: 자연수와 진분수로 나타낸 분수입니다. (예: 2와 1/3 = 2 1/3)",
            accept_formats=["대분수"],
        ),

        # e3-2-4-06: 동분모 분수 덧셈 (기존 문제, concept_id 수정)
        fb(
            id="e3-2-4-2-fb-001",
            concept_id="e3-2-4-06",
            category="concept",
            part="calc",
            difficulty=4,
            content="3/8 + 2/8 = ____",
            answer="5/8",
            explanation="분모가 같은 분수의 덧셈: 분모는 그대로 두고 분자끼리 더합니다. "
            "3/8 + 2/8 = (3+2)/8 = 5/8입니다.",
            accept_formats=["5/8"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 5단원: 들이와 무게
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # e3-2-5-01: 들이 비교
        fb(
            id="e3-2-5-01-fb-001",
            concept_id="e3-2-5-01",
            category="concept",
            part="calc",
            difficulty=3,
            content="그릇에 담을 수 있는 물의 양을 ____라고 합니다.",
            answer="들이",
            explanation="들이: 그릇에 담을 수 있는 물의 양을 나타내는 단위입니다. L(리터)와 mL(밀리리터)로 나타냅니다.",
            accept_formats=["들이"],
        ),

        # e3-2-5-02: 1L=1000mL (기존 문제, concept_id 수정)
        fb(
            id="e3-2-5-1-fb-001",
            concept_id="e3-2-5-02",
            category="concept",
            part="calc",
            difficulty=3,
            content="1L = ____ mL",
            answer="1000",
            explanation="1L = 1000mL입니다. 들이 단위 변환을 기억하세요.",
            accept_formats=["1000"],
        ),

        # e3-2-5-03: 들이 어림
        fb(
            id="e3-2-5-03-fb-001",
            concept_id="e3-2-5-03",
            category="fill_in_blank",
            part="calc",
            difficulty=4,
            content="생수병 한 병의 들이는 약 ____ mL입니다. (500/2000 중 선택)",
            answer="500",
            explanation="생수병 한 병은 보통 500mL입니다. 2L 생수는 2000mL입니다.",
            accept_formats=["500"],
        ),

        # e3-2-5-04: 들이 덧셈
        fb(
            id="e3-2-5-04-fb-001",
            concept_id="e3-2-5-04",
            category="computation",
            part="calc",
            difficulty=5,
            content="2L 300mL + 1L 800mL = ____ L ____ mL",
            answer="4L 100mL",
            explanation="300mL + 800mL = 1100mL = 1L 100mL, 2L + 1L + 1L = 4L, 따라서 4L 100mL입니다.",
            accept_formats=["4L 100mL", "4 100"],
        ),

        # e3-2-5-05: 무게 비교
        fb(
            id="e3-2-5-05-fb-001",
            concept_id="e3-2-5-05",
            category="concept",
            part="calc",
            difficulty=3,
            content="물건의 무거운 정도를 ____라고 합니다.",
            answer="무게",
            explanation="무게: 물건의 무거운 정도를 나타내는 단위입니다. kg(킬로그램)과 g(그램)으로 나타냅니다.",
            accept_formats=["무게"],
        ),

        # e3-2-5-06: 1kg=1000g (기존 문제, concept_id 수정)
        fb(
            id="e3-2-5-1-fb-002",
            concept_id="e3-2-5-06",
            category="concept",
            part="calc",
            difficulty=4,
            content="1kg = ____ g",
            answer="1000",
            explanation="1kg = 1000g입니다. 무게 단위 변환을 기억하세요.",
            accept_formats=["1000"],
        ),

        # e3-2-5-07: 무게 어림
        fb(
            id="e3-2-5-07-fb-001",
            concept_id="e3-2-5-07",
            category="fill_in_blank",
            part="calc",
            difficulty=4,
            content="1원짜리 동전 한 개의 무게는 약 ____ g입니다. (1/10/100 중 선택)",
            answer="1",
            explanation="1원짜리 동전 한 개의 무게는 약 1g입니다.",
            accept_formats=["1"],
        ),

        # e3-2-5-08: 무게 덧셈
        fb(
            id="e3-2-5-08-fb-001",
            concept_id="e3-2-5-08",
            category="computation",
            part="calc",
            difficulty=5,
            content="3kg 500g + 2kg 800g = ____ kg ____ g",
            answer="6kg 300g",
            explanation="500g + 800g = 1300g = 1kg 300g, 3kg + 2kg + 1kg = 6kg, 따라서 6kg 300g입니다.",
            accept_formats=["6kg 300g", "6 300"],
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 6단원: 자료의 정리
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # e3-2-6-01: 표 읽기
        fb(
            id="e3-2-6-01-fb-001",
            concept_id="e3-2-6-01",
            category="concept",
            part="data",
            difficulty=4,
            content="조사한 자료를 가로줄과 세로줄로 정리한 것을 ____라고 합니다.",
            answer="표",
            explanation="표: 자료를 가로줄과 세로줄로 정리하여 한눈에 알아보기 쉽게 나타낸 것입니다.",
            accept_formats=["표"],
        ),

        # e3-2-6-02: 범례 정의 (기존 문제 2개)
        fb(
            id="e3-2-6-2-fb-001",
            concept_id="e3-2-6-02",
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
            concept_id="e3-2-6-02",
            category="concept",
            part="data",
            difficulty=6,
            content="그림그래프에서 별 1개 = 5명입니다. 별 4개는 ____ 명을 나타냅니다.",
            answer="20",
            explanation="별 1개 = 5명이므로, 별 4개 = 5 × 4 = 20명입니다. "
            "범례를 이용해 계산해야 합니다.",
            accept_formats=["20"],
        ),

        # e3-2-6-03: 그래프 그리기
        fb(
            id="e3-2-6-03-fb-001",
            concept_id="e3-2-6-03",
            category="fill_in_blank",
            part="data",
            difficulty=6,
            content="그림그래프에서 12명을 나타내려고 합니다. 별 1개 = 3명이면 별을 ____ 개 그려야 합니다.",
            answer="4",
            explanation="12명 ÷ 3명 = 4개입니다. 범례를 이용하여 그림의 개수를 계산합니다.",
            accept_formats=["4"],
        ),

        # e3-2-6-04: 자료 조사
        fb(
            id="e3-2-6-04-fb-001",
            concept_id="e3-2-6-04",
            category="fill_in_blank",
            part="data",
            difficulty=5,
            content="좋아하는 과일을 조사하여 표로 나타냈습니다. 사과 15명, 포도 12명, 바나나 8명일 때, "
            "가장 많은 학생이 좋아하는 과일은 ____입니다.",
            answer="사과",
            explanation="15 > 12 > 8이므로 사과를 좋아하는 학생이 가장 많습니다. 표를 보고 자료를 분석할 수 있어야 합니다.",
            accept_formats=["사과"],
        ),
    ]
