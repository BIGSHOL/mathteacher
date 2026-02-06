"""초등학교 3학년 개념 문제 시드 데이터.

커버 단원:
  1학기 2단원 - 평면도형
  1학기 5단원 - 길이와 시간
  1학기 6단원 - 분수와 소수
  2학기 9단원 - 원
  2학기 10단원 - 분수 (2)
  2학기 11단원 - 들이와 무게
  2학기 12단원 - 자료의 정리
"""

from .._base import concept, mc


def get_concepts() -> list[dict]:
    """개념 14개 반환 (단원당 2개)."""
    return [
        # ━━ 1학기 2단원: 평면도형 ━━
        concept(
            id="concept-e3-plane-01",
            name="평면도형 - 선분·반직선·직선",
            grade="elementary_3",
            category="concept",
            part="geo",
            description="선분(두 점 사이 가장 짧은 선), 반직선(시작점+방향), 직선(양쪽 무한)의 정의와 성질을 이해합니다.",
        ),
        concept(
            id="concept-e3-plane-02",
            name="평면도형 - 각과 직각",
            grade="elementary_3",
            category="concept",
            part="geo",
            description="각(한 점에서 그은 두 반직선)의 정의, 직각(90도)의 성질, 각의 크기와 변의 길이는 무관함을 이해합니다.",
        ),
        # ━━ 1학기 5단원: 길이와 시간 ━━
        concept(
            id="concept-e3-length-time-01",
            name="길이와 시간 - 길이 단위와 변환",
            grade="elementary_3",
            category="concept",
            part="calc",
            description="mm, cm, m, km 단위 변환(10mm=1cm, 100cm=1m, 1000m=1km)과 자 눈금 읽기를 이해합니다.",
        ),
        concept(
            id="concept-e3-length-time-02",
            name="길이와 시간 - 시각과 시간, 60진법",
            grade="elementary_3",
            category="concept",
            part="calc",
            description="시각과 시간(양)을 구별하고, 60진법 기반의 시간 덧셈과 뺄셈을 정확히 계산합니다.",
        ),
        # ━━ 1학기 6단원: 분수와 소수 ━━
        concept(
            id="concept-e3-frac-dec-01",
            name="분수와 소수 - 분수의 개념과 단위분수",
            grade="elementary_3",
            category="concept",
            part="calc",
            description="분수의 정의(전체를 '똑같이' 나눈 것 중 일부), 단위분수(분자가 1인 분수), 단위분수의 크기 비교를 이해합니다.",
        ),
        concept(
            id="concept-e3-frac-dec-02",
            name="분수와 소수 - 소수의 개념과 분수-소수 관계",
            grade="elementary_3",
            category="concept",
            part="calc",
            description="소수 도입(1/10=0.1), 수직선 위 소수 위치, 분수와 소수의 관계를 이해합니다.",
        ),
        # ━━ 2학기 9단원: 원 ━━
        concept(
            id="concept-e3-circle-01",
            name="원 - 중심·반지름·지름의 정의",
            grade="elementary_3",
            category="concept",
            part="geo",
            description="원의 중심, 반지름(중심→원 위), 지름(중심을 지나는 선분)의 정의를 이해하고, 한 원에서 모든 반지름의 길이가 같음을 압니다.",
        ),
        concept(
            id="concept-e3-circle-02",
            name="원 - 반지름과 지름의 관계·활용",
            grade="elementary_3",
            category="concept",
            part="geo",
            description="지름=반지름×2 관계를 이해하고, 컴퍼스를 사용하여 원을 그리는 원리를 알아봅니다.",
        ),
        # ━━ 2학기 10단원: 분수 (2) ━━
        concept(
            id="concept-e3-frac2-01",
            name="분수 (2) - 진분수·가분수·대분수 분류",
            grade="elementary_3",
            category="concept",
            part="calc",
            description="진분수(분자<분모), 가분수(분자≥분모), 대분수(자연수+진분수)를 분류하고 상호 변환합니다.",
        ),
        concept(
            id="concept-e3-frac2-02",
            name="분수 (2) - 동분모 분수의 비교와 연산",
            grade="elementary_3",
            category="concept",
            part="calc",
            description="분모가 같은 분수의 크기 비교와 덧셈·뺄셈에서 분모는 그대로 두고 분자끼리 연산하는 원리를 이해합니다.",
        ),
        # ━━ 2학기 11단원: 들이와 무게 ━━
        concept(
            id="concept-e3-vol-wt-01",
            name="들이와 무게 - 단위(L, mL, kg, g)와 변환",
            grade="elementary_3",
            category="concept",
            part="calc",
            description="들이(L, mL)와 무게(kg, g) 단위를 알고, 1L=1000mL, 1kg=1000g 변환을 정확히 합니다.",
        ),
        concept(
            id="concept-e3-vol-wt-02",
            name="들이와 무게 - 부피와 무게의 구별, 덧뺄셈",
            grade="elementary_3",
            category="concept",
            part="calc",
            description="부피(크기)와 무게는 다른 양임을 이해하고, 같은 단위끼리 들이·무게의 덧셈과 뺄셈을 합니다.",
        ),
        # ━━ 2학기 12단원: 자료의 정리 ━━
        concept(
            id="concept-e3-data-01",
            name="자료의 정리 - 자료 수집과 표 정리",
            grade="elementary_3",
            category="concept",
            part="data",
            description="자료를 수집하고 표로 체계적으로 정리하여 한눈에 비교·파악하는 방법을 이해합니다.",
        ),
        concept(
            id="concept-e3-data-02",
            name="자료의 정리 - 그림그래프와 범례",
            grade="elementary_3",
            category="concept",
            part="data",
            description="그림그래프에서 범례(그림 하나가 나타내는 수)를 확인하고, 그래프를 정확히 읽는 방법을 이해합니다.",
        ),
    ]


def get_questions() -> list[dict]:
    """개념 문제 21개 반환 (단원당 3개)."""
    return [
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 2단원: 평면도형
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-conc-001",
            concept_id="concept-e3-plane-01",
            category="concept",
            part="geo",
            difficulty=3,
            content="반직선 AB와 반직선 BA는 같은가요?",
            options=[
                ("같다", "같다"),
                ("다르다", "다르다"),
                ("때에 따라 다르다", "때에 따라 다르다"),
                ("판단할 수 없다", "판단할 수 없다"),
            ],
            correct="다르다",
            explanation="반직선은 시작점과 방향이 모두 중요합니다. "
            "반직선 AB는 A에서 시작해 B 방향으로 뻗은 선이고, "
            "반직선 BA는 B에서 시작해 A 방향으로 뻗은 선이므로 다릅니다. "
            "선분 AB = 선분 BA와 혼동하지 않도록 주의하세요!",
        ),
        mc(
            id="e3-conc-002",
            concept_id="concept-e3-plane-02",
            category="concept",
            part="geo",
            difficulty=4,
            content="다음 그림에서 직각을 모두 고르세요. (도형이 45도 기울어져 있음)",
            options=[
                ("가만", "가만"),
                ("가, 나", "가, 나"),
                ("가, 나, 다", "가, 나, 다"),
                ("직각이 없다", "직각이 없다"),
            ],
            correct="가, 나, 다",
            explanation="직각은 방향과 관계없이 90도인 각입니다. "
            "도형이 기울어져 있어도 직각은 직각입니다. "
            "수평/수직 방향으로만 놓인 각만 직각이라고 생각하는 것은 오개념입니다.",
        ),
        mc(
            id="e3-conc-003",
            concept_id="concept-e3-plane-02",
            category="concept",
            part="geo",
            difficulty=5,
            content="두 각 A, B가 있습니다. 각 A의 변이 각 B의 변보다 깁니다. 두 각의 크기를 비교하면?",
            options=[
                ("각 A가 더 크다", "각 A가 더 크다"),
                ("각 B가 더 크다", "각 B가 더 크다"),
                ("같다", "같다"),
                ("변의 길이만으로는 비교할 수 없다", "변의 길이만으로는 비교할 수 없다"),
            ],
            correct="변의 길이만으로는 비교할 수 없다",
            explanation="각의 크기는 두 변이 벌어진 정도(벌어진 각도)로 결정됩니다. "
            "변의 길이와는 관계가 없습니다! "
            "변이 길어도 좁게 벌어지면 작은 각이고, 변이 짧아도 넓게 벌어지면 큰 각입니다.",
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 5단원: 길이와 시간
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-conc-004",
            concept_id="concept-e3-length-time-01",
            category="concept",
            part="calc",
            difficulty=4,
            content="자의 3cm 눈금에서 8cm 눈금까지의 길이는?",
            options=[
                ("8cm", "8cm"),
                ("5cm", "5cm"),
                ("11cm", "11cm"),
                ("3cm", "3cm"),
            ],
            correct="5cm",
            explanation="부러진 자 문제입니다! "
            "길이 = 끝 눈금 - 시작 눈금 = 8 - 3 = 5cm입니다. "
            "자가 항상 0에서 시작한다고 착각하면 틀립니다.",
        ),
        mc(
            id="e3-conc-005",
            concept_id="concept-e3-length-time-02",
            category="concept",
            part="calc",
            difficulty=5,
            content="1시간 40분 + 30분 = ?",
            options=[
                ("1시간 70분", "1시간 70분"),
                ("2시간 10분", "2시간 10분"),
                ("1.7시간", "1.7시간"),
                ("2시간", "2시간"),
            ],
            correct="2시간 10분",
            explanation="시간은 60진법입니다! "
            "40분 + 30분 = 70분인데, 60분이 되면 1시간으로 받아올림합니다. "
            "70분 = 1시간 10분이므로, 1시간 + 1시간 10분 = 2시간 10분입니다. "
            "'1시간 70분'이나 '1.7시간'은 틀린 표현입니다.",
        ),
        mc(
            id="e3-conc-006",
            concept_id="concept-e3-length-time-01",
            category="concept",
            part="calc",
            difficulty=6,
            content="1km는 몇 m인가요?",
            options=[
                ("10m", "10m"),
                ("100m", "100m"),
                ("1000m", "1000m"),
                ("10000m", "10000m"),
            ],
            correct="1000m",
            explanation="1km = 1000m입니다. "
            "길이 단위 변환: 10mm = 1cm, 100cm = 1m, 1000m = 1km",
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 6단원: 분수와 소수
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-conc-007",
            concept_id="concept-e3-frac-dec-01",
            category="concept",
            part="calc",
            difficulty=4,
            content="다음 중 1/4를 올바르게 나타낸 그림은? (4개 제시)",
            options=[
                ("크기가 다른 4조각 중 1개를 색칠", "크기가 다른 4조각 중 1개를 색칠"),
                ("똑같은 4조각 중 1개를 색칠", "똑같은 4조각 중 1개를 색칠"),
                ("3조각 중 1개를 색칠", "3조각 중 1개를 색칠"),
                ("5조각 중 1개를 색칠", "5조각 중 1개를 색칠"),
            ],
            correct="똑같은 4조각 중 1개를 색칠",
            explanation="분수는 전체를 '똑같이' 나눈 것 중의 일부입니다! "
            "크기가 다른 조각으로 나누면 분수가 아닙니다. "
            "등분(똑같이 나누기) ≠ 비등분(크기가 다르게 나누기)",
        ),
        mc(
            id="e3-conc-008",
            concept_id="concept-e3-frac-dec-01",
            category="concept",
            part="calc",
            difficulty=6,
            content="1/3과 1/2 중 어느 것이 더 큰가요?",
            options=[
                ("1/3", "1/3"),
                ("1/2", "1/2"),
                ("같다", "같다"),
                ("비교할 수 없다", "비교할 수 없다"),
            ],
            correct="1/2",
            explanation="단위분수는 분모가 작을수록 큽니다! "
            "전체를 2조각으로 나눈 것이 3조각으로 나눈 것보다 큽니다. "
            "'3이 2보다 크니까 1/3이 더 크다'는 자연수 지식의 간섭으로 인한 오개념입니다.",
        ),
        mc(
            id="e3-conc-009",
            concept_id="concept-e3-frac-dec-02",
            category="concept",
            part="calc",
            difficulty=7,
            content="수직선에서 0과 1 사이를 10칸으로 똑같이 나누었을 때, 0에서 1칸 간 지점은?",
            options=[
                ("0", "0"),
                ("0.1", "0.1"),
                ("1", "1"),
                ("10", "10"),
            ],
            correct="0.1",
            explanation="0과 1 사이를 10칸으로 나누면 한 칸은 1/10입니다. "
            "1/10 = 0.1입니다. "
            "소수는 0보다 작은 수가 아니라 0과 1 사이의 수입니다!",
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 9단원: 원
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-conc-010",
            concept_id="concept-e3-circle-01",
            category="concept",
            part="geo",
            difficulty=3,
            content="한 원에서 모든 반지름의 길이는?",
            options=[
                ("모두 같다", "모두 같다"),
                ("방향에 따라 다르다", "방향에 따라 다르다"),
                ("위쪽이 더 길다", "위쪽이 더 길다"),
                ("옆쪽이 더 길다", "옆쪽이 더 길다"),
            ],
            correct="모두 같다",
            explanation="한 원에서 반지름은 방향과 관계없이 모두 같은 길이입니다! "
            "이것이 원의 정의입니다. "
            "시각적으로 어떤 반지름이 더 길어 보여도 실제로는 모두 같습니다.",
        ),
        mc(
            id="e3-conc-011",
            concept_id="concept-e3-circle-01",
            category="concept",
            part="geo",
            difficulty=5,
            content="원 안에 여러 선분이 그려져 있습니다. 다음 중 지름인 것은?",
            options=[
                ("원 위의 두 점을 잇는 모든 선분", "원 위의 두 점을 잇는 모든 선분"),
                ("원의 중심을 지나는 선분", "원의 중심을 지나는 선분"),
                ("가장 긴 선분", "가장 긴 선분"),
                ("원 안쪽을 지나는 선분", "원 안쪽을 지나는 선분"),
            ],
            correct="원의 중심을 지나는 선분",
            explanation="지름의 정의: 원 위의 두 점을 잇는 선분 중 '중심을 지나는' 선분입니다. "
            "중심을 지나지 않는 선분은 '현'이라고 부르며 지름이 아닙니다. "
            "지름 = 반지름 × 2",
        ),
        mc(
            id="e3-conc-012",
            concept_id="concept-e3-circle-02",
            category="concept",
            part="geo",
            difficulty=6,
            content="반지름이 5cm인 원의 지름은?",
            options=[
                ("5cm", "5cm"),
                ("10cm", "10cm"),
                ("15cm", "15cm"),
                ("2.5cm", "2.5cm"),
            ],
            correct="10cm",
            explanation="지름 = 반지름 × 2 = 5 × 2 = 10cm입니다.",
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 10단원: 분수 (2)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-conc-013",
            concept_id="concept-e3-frac2-02",
            category="concept",
            part="calc",
            difficulty=4,
            content="2/7 + 3/7 = ?",
            options=[
                ("5/7", "5/7"),
                ("5/14", "5/14"),
                ("6/14", "6/14"),
                ("2/7", "2/7"),
            ],
            correct="5/7",
            explanation="분모가 같은 분수의 덧셈: 분모는 그대로 두고 분자끼리 더합니다. "
            "2/7 + 3/7 = (2+3)/7 = 5/7입니다. "
            "'2/7 + 3/7 = 5/14'는 분모까지 더한 오류입니다!",
        ),
        mc(
            id="e3-conc-014",
            concept_id="concept-e3-frac2-01",
            category="concept",
            part="calc",
            difficulty=5,
            content="7/5는 어떤 분수인가요?",
            options=[
                ("진분수", "진분수"),
                ("가분수", "가분수"),
                ("대분수", "대분수"),
                ("단위분수", "단위분수"),
            ],
            correct="가분수",
            explanation="가분수: 분자 ≥ 분모인 분수입니다. "
            "7/5는 분자(7)가 분모(5)보다 크므로 가분수입니다. "
            "진분수: 분자 < 분모 (예: 3/5), 대분수: 자연수 + 진분수 (예: 1와 2/5)",
        ),
        mc(
            id="e3-conc-015",
            concept_id="concept-e3-frac2-02",
            category="concept",
            part="calc",
            difficulty=7,
            content="파이 차트에서 2/7이 색칠되어 있고, 3/7을 더 색칠하면 전체 몇/몇이 색칠되나요?",
            options=[
                ("5/7", "5/7"),
                ("5/14", "5/14"),
                ("1", "1"),
                ("2/3", "2/3"),
            ],
            correct="5/7",
            explanation="2/7 + 3/7 = 5/7입니다. "
            "파이 차트로 시각적으로 확인하면: 조각의 크기(분모 7)는 불변하고, "
            "색칠된 조각의 개수(분자)만 2개 → 5개로 증가합니다.",
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 11단원: 들이와 무게
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-conc-016",
            concept_id="concept-e3-vol-wt-01",
            category="concept",
            part="calc",
            difficulty=3,
            content="1L는 몇 mL인가요?",
            options=[
                ("10mL", "10mL"),
                ("100mL", "100mL"),
                ("1000mL", "1000mL"),
                ("10000mL", "10000mL"),
            ],
            correct="1000mL",
            explanation="1L = 1000mL입니다. "
            "들이 단위 변환: 1L = 1000mL",
        ),
        mc(
            id="e3-conc-017",
            concept_id="concept-e3-vol-wt-02",
            category="concept",
            part="calc",
            difficulty=5,
            content="다음 중 가장 무거운 것은?",
            options=[
                ("큰 스티로폼 상자", "큰 스티로폼 상자"),
                ("작은 쇠구슬", "작은 쇠구슬"),
                ("부피로 판단할 수 없다", "부피로 판단할 수 없다"),
                ("크기가 같으면 무게도 같다", "크기가 같으면 무게도 같다"),
            ],
            correct="부피로 판단할 수 없다",
            explanation="부피(크기)와 무게는 다릅니다! "
            "스티로폼 상자는 부피가 크지만 가볍고, 쇠구슬은 작지만 무겁습니다. "
            "'부피가 크면 무게도 크다'는 오개념입니다.",
        ),
        mc(
            id="e3-conc-018",
            concept_id="concept-e3-vol-wt-01",
            category="concept",
            part="calc",
            difficulty=6,
            content="1kg은 몇 g인가요?",
            options=[
                ("10g", "10g"),
                ("100g", "100g"),
                ("1000g", "1000g"),
                ("10000g", "10000g"),
            ],
            correct="1000g",
            explanation="1kg = 1000g입니다. "
            "무게 단위 변환: 1kg = 1000g",
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 12단원: 자료의 정리
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-conc-019",
            concept_id="concept-e3-data-02",
            category="concept",
            part="data",
            difficulty=4,
            content="그림그래프에서 큰 스마일 1개 = 10명입니다. 큰 스마일 3개는 몇 명을 나타내나요?",
            options=[
                ("3명", "3명"),
                ("13명", "13명"),
                ("30명", "30명"),
                ("300명", "300명"),
            ],
            correct="30명",
            explanation="범례를 확인해야 합니다! "
            "큰 스마일 1개 = 10명이므로, 3개 = 10 × 3 = 30명입니다. "
            "'그림 개수 = 사람 수'로 착각하면 틀립니다.",
        ),
        mc(
            id="e3-conc-020",
            concept_id="concept-e3-data-02",
            category="concept",
            part="data",
            difficulty=6,
            content="그림그래프에서 큰 그림 1개 = 100, 작은 그림 1개 = 10입니다. "
            "큰 그림 2개와 작은 그림 3개는?",
            options=[
                ("5", "5"),
                ("23", "23"),
                ("230", "230"),
                ("2030", "2030"),
            ],
            correct="230",
            explanation="큰 그림 2개 = 100 × 2 = 200, 작은 그림 3개 = 10 × 3 = 30입니다. "
            "합계: 200 + 30 = 230입니다. "
            "범례를 무시하고 그림 개수만 세면 틀립니다.",
        ),
        mc(
            id="e3-conc-021",
            concept_id="concept-e3-data-01",
            category="concept",
            part="data",
            difficulty=7,
            content="자료를 표로 정리하는 이유는?",
            options=[
                ("그림을 그리기 위해", "그림을 그리기 위해"),
                ("자료를 한눈에 알아보기 쉽게 하기 위해", "자료를 한눈에 알아보기 쉽게 하기 위해"),
                ("숫자를 많이 쓰기 위해", "숫자를 많이 쓰기 위해"),
                ("계산을 빠르게 하기 위해", "계산을 빠르게 하기 위해"),
            ],
            correct="자료를 한눈에 알아보기 쉽게 하기 위해",
            explanation="표는 자료를 체계적으로 정리하여 한눈에 비교하고 파악할 수 있게 합니다.",
        ),
    ]
