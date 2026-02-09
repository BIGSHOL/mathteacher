"""초등학교 3학년 개념 문제 시드 데이터.

커버 단원 (PDF 기반 42개 세분화 개념):
  1학기 2단원 - 평면도형 (6개)
  1학기 5단원 - 길이와 시간 (6개)
  1학기 6단원 - 분수와 소수 (8개)
  2학기 3단원 - 원 (4개)
  2학기 4단원 - 분수 (6개)
  2학기 5단원 - 들이와 무게 (8개)
  2학기 6단원 - 자료의 정리 (4개)
"""

from .._base import concept, mc


def get_concepts() -> list[dict]:
    """개념 42개 반환 (PDF 기반 세분화 - 개념 단원만)."""
    from app.data.pdf_concept_map import E3_S1_CONCEPTS, E3_S2_CONCEPTS

    # 1학기 개념 단원: ch2(평면도형), ch5(길이와 시간), ch6(분수와 소수)
    # 주의: ch5의 e3-1-5-05는 category=computation이지만 개념 단원 소속이므로 포함
    concept_s1_chapters = {2, 5, 6}
    # 2학기 개념 단원: ch3(원), ch4(분수), ch5(들이와 무게), ch6(자료의 정리)
    concept_s2_chapters = {3, 4, 5, 6}

    result = []
    for c in E3_S1_CONCEPTS:
        if c["chapter_number"] in concept_s1_chapters:
            result.append(concept(
                id=c["id"], name=c["name"], grade=c["grade"],
                category=c["category"], part=c["part"], description=c["description"],
            ))
    for c in E3_S2_CONCEPTS:
        if c["chapter_number"] in concept_s2_chapters:
            result.append(concept(
                id=c["id"], name=c["name"], grade=c["grade"],
                category=c["category"], part=c["part"], description=c["description"],
            ))
    return result


def get_questions() -> list[dict]:
    """개념 문제 반환 (기존 23개 concept_id 변경 + 신규 24개 추가 = 총 47개)."""
    return [
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 2단원: 평면도형 (6개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e3-1-2-01: 선분, 반직선, 직선 ──
        mc(
            id="e3-1-2-1-cc-001",
            concept_id="e3-1-2-01",  # 변경: e3-1-2-1 → e3-1-2-01
            category="concept",
            part="geo",
            difficulty=3,
            content="반직선 AB와 반직선 BA는 같은가요?",
            options=[
                "같다",
                "다르다",
                "때에 따라 다르다",
                "판단할 수 없다",
            ],
            correct="B",
            explanation="반직선은 시작점과 방향이 모두 중요합니다. "
            "반직선 AB는 A에서 시작해 B 방향으로 뻗은 선이고, "
            "반직선 BA는 B에서 시작해 A 방향으로 뻗은 선이므로 다릅니다. "
            "선분 AB = 선분 BA와 혼동하지 않도록 주의하세요!",
        ),

        # ── e3-1-2-02: 각 ──
        mc(
            id="e3-1-2-2-cc-002",
            concept_id="e3-1-2-02",  # 변경: e3-1-2-2 → e3-1-2-02
            category="concept",
            part="geo",
            difficulty=5,
            content="두 각 A, B가 있습니다. 각 A의 변이 각 B의 변보다 깁니다. 두 각의 크기를 비교하면?",
            options=[
                "각 A가 더 크다",
                "각 B가 더 크다",
                "같다",
                "변의 길이만으로는 비교할 수 없다",
            ],
            correct="D",
            explanation="각의 크기는 두 변이 벌어진 정도(벌어진 각도)로 결정됩니다. "
            "변의 길이와는 관계가 없습니다! "
            "변이 길어도 좁게 벌어지면 작은 각이고, 변이 짧아도 넓게 벌어지면 큰 각입니다.",
        ),

        # ── e3-1-2-03: 직각 ──
        mc(
            id="e3-1-2-2-cc-001",
            concept_id="e3-1-2-03",  # 변경: e3-1-2-2 → e3-1-2-03
            category="concept",
            part="geo",
            difficulty=4,
            content="다음 그림에서 직각을 모두 고르세요. (도형이 45도 기울어져 있음)",
            options=[
                "가만",
                "가, 나",
                "가, 나, 다",
                "직각이 없다",
            ],
            correct="C",
            explanation="직각은 방향과 관계없이 90도인 각입니다. "
            "도형이 기울어져 있어도 직각은 직각입니다. "
            "수평/수직 방향으로만 놓인 각만 직각이라고 생각하는 것은 오개념입니다.",
        ),

        # ── e3-1-2-04: 직각삼각형 (신규) ──
        mc(
            id="e3-1-2-04-cc-001",
            concept_id="e3-1-2-04",
            category="concept",
            part="geo",
            difficulty=3,
            content="직각삼각형은 무엇인가요?",
            options=[
                "세 각이 모두 직각인 삼각형",
                "세 각 중 하나가 직각인 삼각형",
                "세 변의 길이가 같은 삼각형",
                "직각이 없는 삼각형",
            ],
            correct="B",
            explanation="직각삼각형은 세 각 중 하나가 직각(90도)인 삼각형입니다. "
            "삼각형의 세 각의 합은 180도이므로 직각이 2개 이상이면 삼각형이 될 수 없습니다.",
        ),
        mc(
            id="e3-1-2-04-cc-002",
            concept_id="e3-1-2-04",
            category="concept",
            part="geo",
            difficulty=4,
            content="다음 중 직각삼각형을 찾는 가장 정확한 방법은?",
            options=[
                "눈으로 보고 판단한다",
                "삼각자의 직각을 이용하여 확인한다",
                "변의 길이를 잰다",
                "종이를 접어본다",
            ],
            correct="B",
            explanation="삼각자의 직각 부분을 삼각형의 각에 맞춰보면 직각인지 정확히 확인할 수 있습니다.",
        ),

        # ── e3-1-2-05: 직사각형 (신규) ──
        mc(
            id="e3-1-2-05-cc-001",
            concept_id="e3-1-2-05",
            category="concept",
            part="geo",
            difficulty=3,
            content="직사각형의 특징으로 옳은 것은?",
            options=[
                "네 변의 길이가 모두 같다",
                "네 각이 모두 직각이다",
                "마주 보는 각의 크기가 같다",
                "세 각이 직각이다",
            ],
            correct="B",
            explanation="직사각형은 네 각이 모두 직각인 사각형입니다. "
            "또한 마주 보는 변의 길이가 같은 성질도 있습니다.",
        ),

        # ── e3-1-2-06: 정사각형 (신규) ──
        mc(
            id="e3-1-2-06-cc-001",
            concept_id="e3-1-2-06",
            category="concept",
            part="geo",
            difficulty=4,
            content="정사각형과 직사각형의 관계는?",
            options=[
                "정사각형은 직사각형이 아니다",
                "정사각형은 직사각형의 특별한 경우이다",
                "직사각형은 정사각형의 특별한 경우이다",
                "정사각형과 직사각형은 전혀 다르다",
            ],
            correct="B",
            explanation="정사각형은 네 각이 모두 직각이고 네 변의 길이가 모두 같은 사각형입니다. "
            "네 각이 모두 직각이므로 직사각형의 조건을 만족합니다. "
            "즉, 모든 정사각형은 직사각형이지만, 모든 직사각형이 정사각형인 것은 아닙니다.",
        ),
        mc(
            id="e3-1-2-06-cc-002",
            concept_id="e3-1-2-06",
            category="concept",
            part="geo",
            difficulty=5,
            content="한 변이 5cm인 정사각형의 네 변의 길이의 합은?",
            options=[
                "10cm",
                "15cm",
                "20cm",
                "25cm",
            ],
            correct="C",
            explanation="정사각형은 네 변의 길이가 모두 같으므로 5×4=20cm입니다.",
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 3단원: 나눗셈 (개념 문제 1개만 - 연산 단원)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-1-3-2-cc-001",
            concept_id="e3-1-3-02",  # 변경: e3-1-3-2 → e3-1-3-02
            category="concept",
            part="calc",
            difficulty=5,
            content="다음 중 틀린 설명은?",
            options=[
                "12 ÷ 4 = 3과 3 × 4 = 12는 서로 관련이 있다",
                "12 ÷ 4와 4 ÷ 12는 같은 값이다",
                "사과 12개를 4개씩 나누면 3묶음이 된다",
                "나눗셈에서 몫의 단위는 상황에 따라 달라진다",
            ],
            correct="B",
            explanation="나눗셈은 교환법칙이 성립하지 않습니다! "
            "12 ÷ 4 = 3이지만 4 ÷ 12는 나누어떨어지지 않습니다. "
            "덧셈과 곱셈에서는 교환법칙이 성립하지만, 뺄셈과 나눗셈에서는 순서를 바꾸면 결과가 달라집니다.",
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 5단원: 길이와 시간 (6개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e3-1-5-01: 1 mm보다 작은 단위 ──
        mc(
            id="e3-1-5-1-cc-001",
            concept_id="e3-1-5-01",  # 변경: e3-1-5-1 → e3-1-5-01
            category="concept",
            part="calc",
            difficulty=4,
            content="자의 3cm 눈금에서 8cm 눈금까지의 길이는?",
            options=[
                "8cm",
                "5cm",
                "11cm",
                "3cm",
            ],
            correct="B",
            explanation="부러진 자 문제입니다! "
            "길이 = 끝 눈금 - 시작 눈금 = 8 - 3 = 5cm입니다. "
            "자가 항상 0에서 시작한다고 착각하면 틀립니다.",
        ),

        # ── e3-1-5-02: 1 m보다 큰 단위 ──
        mc(
            id="e3-1-5-1-cc-002",
            concept_id="e3-1-5-02",  # 변경: e3-1-5-1 → e3-1-5-02
            category="concept",
            part="calc",
            difficulty=6,
            content="1km는 몇 m인가요?",
            options=[
                "10m",
                "100m",
                "1000m",
                "10000m",
            ],
            correct="C",
            explanation="1km = 1000m입니다. "
            "길이 단위 변환: 10mm = 1cm, 100cm = 1m, 1000m = 1km",
        ),

        # ── e3-1-5-03: 길이와 거리를 어림하고 재어 보기 (신규) ──
        mc(
            id="e3-1-5-03-cc-001",
            concept_id="e3-1-5-03",
            category="concept",
            part="calc",
            difficulty=5,
            content="다음 중 길이를 재는 단위로 가장 적절한 것은?\n\n학교 운동장의 한 바퀴 길이",
            options=[
                "mm",
                "cm",
                "m",
                "km",
            ],
            correct="C",
            explanation="운동장의 길이는 수백 미터 정도이므로 m 단위가 가장 적절합니다. "
            "mm나 cm는 너무 작고, km는 너무 큰 단위입니다.",
        ),

        # ── e3-1-5-04: 1분보다 작은 단위 (신규) ──
        mc(
            id="e3-1-5-04-cc-001",
            concept_id="e3-1-5-04",
            category="concept",
            part="calc",
            difficulty=3,
            content="1분은 몇 초인가요?",
            options=[
                "10초",
                "30초",
                "60초",
                "100초",
            ],
            correct="C",
            explanation="1분 = 60초입니다. 시계의 초침이 한 바퀴 도는 시간이 60초(1분)입니다.",
        ),
        mc(
            id="e3-1-5-04-cc-002",
            concept_id="e3-1-5-04",
            category="concept",
            part="calc",
            difficulty=4,
            content="2분 30초는 몇 초인가요?",
            options=[
                "32초",
                "90초",
                "120초",
                "150초",
            ],
            correct="D",
            explanation="2분 = 2 × 60 = 120초, 120초 + 30초 = 150초입니다.",
        ),

        # ── e3-1-5-05: 시간의 덧셈과 뺄셈 (연산이지만 개념 단원 소속) ──
        mc(
            id="e3-1-5-2-cc-001",
            concept_id="e3-1-5-05",  # 변경: e3-1-5-2 → e3-1-5-05
            category="concept",
            part="calc",
            difficulty=5,
            content="1시간 40분 + 30분 = ?",
            options=[
                "1시간 70분",
                "2시간 10분",
                "1.7시간",
                "2시간",
            ],
            correct="B",
            explanation="시간은 60진법입니다! "
            "40분 + 30분 = 70분인데, 60분이 되면 1시간으로 받아올림합니다. "
            "70분 = 1시간 10분이므로, 1시간 + 1시간 10분 = 2시간 10분입니다. "
            "'1시간 70분'이나 '1.7시간'은 틀린 표현입니다.",
        ),

        # ── e3-1-5-06: 시간을 이용하여 문제 해결하기 (신규) ──
        mc(
            id="e3-1-5-06-cc-001",
            concept_id="e3-1-5-06",
            category="concept",
            part="calc",
            difficulty=6,
            content="영수는 오전 9시 30분에 출발하여 1시간 45분 동안 여행했습니다. 도착 시각은?",
            options=[
                "오전 10시 75분",
                "오전 11시 15분",
                "오전 10시 15분",
                "오후 12시 15분",
            ],
            correct="B",
            explanation="9시 30분 + 1시간 45분 = 10시 75분. "
            "75분 = 1시간 15분이므로 10시 + 1시간 15분 = 11시 15분입니다.",
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 6단원: 분수와 소수 (8개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e3-1-6-01: 똑같이 나누기 (신규) ──
        mc(
            id="e3-1-6-01-cc-001",
            concept_id="e3-1-6-01",
            category="concept",
            part="calc",
            difficulty=3,
            content="분수를 배우기 전에 가장 중요한 것은?",
            options=[
                "큰 수부터 센다",
                "전체를 똑같이 나눈다",
                "가능한 많이 나눈다",
                "색칠을 예쁘게 한다",
            ],
            correct="B",
            explanation="분수의 기초는 전체를 '똑같이' 나누는 것입니다. "
            "크기가 다르게 나누면 분수가 아닙니다. 균등 분할(등분)이 핵심입니다!",
        ),

        # ── e3-1-6-02: 분수 (신규) ──
        mc(
            id="e3-1-6-02-cc-001",
            concept_id="e3-1-6-02",
            category="concept",
            part="calc",
            difficulty=4,
            content="분수 3/5에서 5를 무엇이라고 하나요?",
            options=[
                "분자",
                "분모",
                "전체",
                "부분",
            ],
            correct="B",
            explanation="분수선 아래의 수를 분모라고 합니다. 분모는 전체를 몇 조각으로 나누었는지를 나타냅니다. "
            "분수선 위의 수는 분자라고 하며, 그 중 몇 조각인지를 나타냅니다.",
        ),

        # ── e3-1-6-03: 분수로 나타내기 ──
        mc(
            id="e3-1-6-1-cc-001",
            concept_id="e3-1-6-03",  # 변경: e3-1-6-1 → e3-1-6-03
            category="concept",
            part="calc",
            difficulty=4,
            content="다음 중 1/4를 올바르게 나타낸 그림은? (4개 제시)",
            options=[
                "크기가 다른 4조각 중 1개를 색칠",
                "똑같은 4조각 중 1개를 색칠",
                "3조각 중 1개를 색칠",
                "5조각 중 1개를 색칠",
            ],
            correct="B",
            explanation="분수는 전체를 '똑같이' 나눈 것 중의 일부입니다! "
            "크기가 다른 조각으로 나누면 분수가 아닙니다. "
            "등분(똑같이 나누기) ≠ 비등분(크기가 다르게 나누기)",
        ),

        # ── e3-1-6-04: 단위분수의 크기 비교 ──
        mc(
            id="e3-1-6-1-cc-002",
            concept_id="e3-1-6-04",  # 변경: e3-1-6-1 → e3-1-6-04
            category="concept",
            part="calc",
            difficulty=6,
            content="1/3과 1/2 중 어느 것이 더 큰가요?",
            options=[
                "1/3",
                "1/2",
                "같다",
                "비교할 수 없다",
            ],
            correct="B",
            explanation="단위분수는 분모가 작을수록 큽니다! "
            "전체를 2조각으로 나눈 것이 3조각으로 나눈 것보다 큽니다. "
            "'3이 2보다 크니까 1/3이 더 크다'는 자연수 지식의 간섭으로 인한 오개념입니다.",
        ),

        # ── e3-1-6-05: 분모가 같은 분수의 크기 비교 (신규) ──
        mc(
            id="e3-1-6-05-cc-001",
            concept_id="e3-1-6-05",
            category="concept",
            part="calc",
            difficulty=5,
            content="2/7과 5/7 중 어느 것이 더 큰가요?",
            options=[
                "2/7",
                "5/7",
                "같다",
                "비교할 수 없다",
            ],
            correct="B",
            explanation="분모가 같은 분수는 분자가 클수록 큽니다. "
            "똑같은 크기의 조각(1/7)이 5개 있는 것이 2개 있는 것보다 큽니다.",
        ),

        # ── e3-1-6-06: 1보다 작은 소수 ──
        mc(
            id="e3-1-6-2-cc-001",
            concept_id="e3-1-6-06",  # 변경: e3-1-6-2 → e3-1-6-06
            category="concept",
            part="calc",
            difficulty=7,
            content="수직선에서 0과 1 사이를 10칸으로 똑같이 나누었을 때, 0에서 1칸 간 지점은?",
            options=[
                "0",
                "0.1",
                "1",
                "10",
            ],
            correct="B",
            explanation="0과 1 사이를 10칸으로 나누면 한 칸은 1/10입니다. "
            "1/10 = 0.1입니다. "
            "소수는 0보다 작은 수가 아니라 0과 1 사이의 수입니다!",
        ),

        # ── e3-1-6-07: 1보다 큰 소수 (신규) ──
        mc(
            id="e3-1-6-07-cc-001",
            concept_id="e3-1-6-07",
            category="concept",
            part="calc",
            difficulty=5,
            content="1.5는 무엇을 뜻하나요?",
            options=[
                "1과 5",
                "1.5배",
                "1과 0.5의 합",
                "15",
            ],
            correct="C",
            explanation="1.5 = 1 + 0.5입니다. 소수점 왼쪽은 자연수 부분(1), 오른쪽은 소수 부분(0.5)입니다.",
        ),

        # ── e3-1-6-08: 소수의 크기 비교 (신규) ──
        mc(
            id="e3-1-6-08-cc-001",
            concept_id="e3-1-6-08",
            category="concept",
            part="calc",
            difficulty=6,
            content="다음 중 가장 큰 수는?",
            options=[
                "0.9",
                "1.1",
                "0.5",
                "1.0",
            ],
            correct="B",
            explanation="소수의 크기 비교: 먼저 자연수 부분을 비교합니다. "
            "자연수 부분이 1인 1.1이 가장 큽니다. 0.9는 1보다 작습니다!",
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 1단원: 곱셈 (2) (개념 문제 1개만 - 연산 단원)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-2-1-2-cc-002",
            concept_id="e3-2-1-06",  # 변경: e3-2-1-2 → e3-2-1-06
            category="concept",
            part="calc",
            difficulty=7,
            content="다음 계산 과정에서 0을 쓰는 이유는?\n\n    3 4\n  × 1 2\n  -----\n    6 8  ← 34 × 2\n  3 4 0  ← 34 × 10\n  -----\n  4 0 8",
            options=[
                "계산을 편하게 하기 위해",
                "자릿수를 맞추기 위해 (십의 자리 계산이므로)",
                "0을 쓰지 않아도 상관없다",
                "두 자리 수를 만들기 위해",
            ],
            correct="B",
            explanation="12의 '1'은 십의 자리이므로 실제로는 10입니다. "
            "34 × 10 = 340이므로 일의 자리에 0을 써서 340으로 표기해야 합니다. "
            "0을 생략하고 34로 쓰면 34 × 1로 계산한 것이 되어 결과가 틀립니다.",
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 3단원: 원 (4개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e3-2-3-01: 원의 중심, 반지름, 지름 ──
        mc(
            id="e3-2-3-1-cc-002",
            concept_id="e3-2-3-01",  # 변경: e3-2-3-1 → e3-2-3-01
            category="concept",
            part="geo",
            difficulty=5,
            content="원 안에 여러 선분이 그려져 있습니다. 다음 중 지름인 것은?",
            options=[
                "원 위의 두 점을 잇는 모든 선분",
                "원의 중심을 지나는 선분",
                "가장 긴 선분",
                "원 안쪽을 지나는 선분",
            ],
            correct="B",
            explanation="지름의 정의: 원 위의 두 점을 잇는 선분 중 '중심을 지나는' 선분입니다. "
            "중심을 지나지 않는 선분은 '현'이라고 부르며 지름이 아닙니다. "
            "지름 = 반지름 × 2",
        ),

        # ── e3-2-3-02: 원의 성질 ──
        mc(
            id="e3-2-3-1-cc-001",
            concept_id="e3-2-3-02",  # 변경: e3-2-3-1 → e3-2-3-02
            category="concept",
            part="geo",
            difficulty=3,
            content="한 원에서 모든 반지름의 길이는?",
            options=[
                "모두 같다",
                "방향에 따라 다르다",
                "위쪽이 더 길다",
                "옆쪽이 더 길다",
            ],
            correct="A",
            explanation="한 원에서 반지름은 방향과 관계없이 모두 같은 길이입니다! "
            "이것이 원의 정의입니다. "
            "시각적으로 어떤 반지름이 더 길어 보여도 실제로는 모두 같습니다.",
        ),
        mc(
            id="e3-2-3-2-cc-001",
            concept_id="e3-2-3-02",  # 변경: e3-2-3-2 → e3-2-3-02
            category="concept",
            part="geo",
            difficulty=6,
            content="반지름이 5cm인 원의 지름은?",
            options=[
                "5cm",
                "10cm",
                "15cm",
                "2.5cm",
            ],
            correct="B",
            explanation="지름 = 반지름 × 2 = 5 × 2 = 10cm입니다.",
        ),

        # ── e3-2-3-03: 컴퍼스를 이용하여 원 그리기 (신규) ──
        mc(
            id="e3-2-3-03-cc-001",
            concept_id="e3-2-3-03",
            category="concept",
            part="geo",
            difficulty=4,
            content="컴퍼스로 반지름이 3cm인 원을 그리려고 합니다. 컴퍼스를 어떻게 벌려야 하나요?",
            options=[
                "1.5cm만큼 벌린다",
                "3cm만큼 벌린다",
                "6cm만큼 벌린다",
                "원하는 대로 벌린다",
            ],
            correct="B",
            explanation="컴퍼스를 벌린 길이가 바로 반지름이 됩니다. "
            "반지름이 3cm인 원을 그리려면 컴퍼스를 3cm만큼 벌려야 합니다.",
        ),

        # ── e3-2-3-04: 원을 이용하여 여러 가지 모양 그리기 (신규) ──
        mc(
            id="e3-2-3-04-cc-001",
            concept_id="e3-2-3-04",
            category="concept",
            part="geo",
            difficulty=6,
            content="같은 크기의 원 4개를 겹치지 않게 배열하여 꽃 모양을 만들려면?",
            options=[
                "원의 중심을 모두 같은 곳에 둔다",
                "원의 중심을 정사각형 꼭짓점에 둔다",
                "원의 반지름을 다르게 한다",
                "컴퍼스 없이 그린다",
            ],
            correct="B",
            explanation="같은 크기의 원을 규칙적으로 배열하려면 중심의 위치를 정확히 정해야 합니다. "
            "정사각형 꼭짓점에 중심을 두면 균형잡힌 꽃 모양을 만들 수 있습니다.",
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 4단원: 분수 (6개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e3-2-4-01: 분수로 나타내기 (신규) ──
        mc(
            id="e3-2-4-01-cc-001",
            concept_id="e3-2-4-01",
            category="concept",
            part="calc",
            difficulty=4,
            content="사과 12개 중 3개를 먹었습니다. 먹은 사과는 전체의 몇 분의 몇인가요?",
            options=[
                "3/12",
                "3/9",
                "12/3",
                "9/12",
            ],
            correct="A",
            explanation="전체(12개) 중 일부(3개)를 분수로 나타내면 3/12입니다. "
            "이산량(개수가 있는 것)도 분수로 나타낼 수 있습니다.",
        ),

        # ── e3-2-4-02: 전체 개수에 대한 분수만큼은 얼마인지 알기 (신규) ──
        mc(
            id="e3-2-4-02-cc-001",
            concept_id="e3-2-4-02",
            category="concept",
            part="calc",
            difficulty=6,
            content="사탕 15개의 2/5는 몇 개인가요?",
            options=[
                "3개",
                "5개",
                "6개",
                "10개",
            ],
            correct="C",
            explanation="15개를 5등분하면 한 묶음은 15÷5=3개입니다. "
            "그 중 2묶음이므로 3×2=6개입니다.",
        ),

        # ── e3-2-4-03: 전체 길이에 대한 분수만큼은 얼마인지 알기 (신규) ──
        mc(
            id="e3-2-4-03-cc-001",
            concept_id="e3-2-4-03",
            category="concept",
            part="calc",
            difficulty=7,
            content="20cm의 3/4는 몇 cm인가요?",
            options=[
                "10cm",
                "15cm",
                "12cm",
                "16cm",
            ],
            correct="B",
            explanation="20cm를 4등분하면 한 부분은 20÷4=5cm입니다. "
            "그 중 3부분이므로 5×3=15cm입니다.",
        ),

        # ── e3-2-4-04: 진분수, 가분수, 자연수 ──
        mc(
            id="e3-2-4-1-cc-001",
            concept_id="e3-2-4-04",  # 변경: e3-2-4-1 → e3-2-4-04
            category="concept",
            part="calc",
            difficulty=5,
            content="7/5는 어떤 분수인가요?",
            options=[
                "진분수",
                "가분수",
                "대분수",
                "단위분수",
            ],
            correct="B",
            explanation="가분수: 분자 ≥ 분모인 분수입니다. "
            "7/5는 분자(7)가 분모(5)보다 크므로 가분수입니다. "
            "진분수: 분자 < 분모 (예: 3/5), 대분수: 자연수 + 진분수 (예: 1와 2/5)",
        ),

        # ── e3-2-4-05: 대분수 (신규) ──
        mc(
            id="e3-2-4-05-cc-001",
            concept_id="e3-2-4-05",
            category="concept",
            part="calc",
            difficulty=6,
            content="가분수 9/4를 대분수로 나타내면?",
            options=[
                "1과 5/4",
                "2와 1/4",
                "2와 2/4",
                "3과 1/4",
            ],
            correct="B",
            explanation="9÷4=2...1이므로 9/4 = 2와 1/4입니다. "
            "가분수를 대분수로: 분자÷분모의 몫이 자연수, 나머지가 새 분자가 됩니다.",
        ),

        # ── e3-2-4-06: 분모가 같은 분수의 크기 비교 ──
        mc(
            id="e3-2-4-2-cc-001",
            concept_id="e3-2-4-06",  # 변경: e3-2-4-2 → e3-2-4-06
            category="concept",
            part="calc",
            difficulty=4,
            content="2/7 + 3/7 = ?",
            options=[
                "5/7",
                "5/14",
                "6/14",
                "2/7",
            ],
            correct="A",
            explanation="분모가 같은 분수의 덧셈: 분모는 그대로 두고 분자끼리 더합니다. "
            "2/7 + 3/7 = (2+3)/7 = 5/7입니다. "
            "'2/7 + 3/7 = 5/14'는 분모까지 더한 오류입니다!",
        ),
        mc(
            id="e3-2-4-2-cc-002",
            concept_id="e3-2-4-06",  # 변경: e3-2-4-2 → e3-2-4-06
            category="concept",
            part="calc",
            difficulty=7,
            content="파이 차트에서 2/7이 색칠되어 있고, 3/7을 더 색칠하면 전체 몇/몇이 색칠되나요?",
            options=[
                "5/7",
                "5/14",
                "1",
                "2/3",
            ],
            correct="A",
            explanation="2/7 + 3/7 = 5/7입니다. "
            "파이 차트로 시각적으로 확인하면: 조각의 크기(분모 7)는 불변하고, "
            "색칠된 조각의 개수(분자)만 2개 → 5개로 증가합니다.",
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 5단원: 들이와 무게 (8개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e3-2-5-01: 들이 비교하기 (신규) ──
        mc(
            id="e3-2-5-01-cc-001",
            concept_id="e3-2-5-01",
            category="concept",
            part="calc",
            difficulty=3,
            content="들이를 비교하는 가장 정확한 방법은?",
            options=[
                "눈으로 보고 판단한다",
                "손으로 들어본다",
                "같은 컵에 옮겨 담아 비교한다",
                "무게를 잰다",
            ],
            correct="C",
            explanation="들이를 정확히 비교하려면 같은 크기의 컵에 옮겨 담아 비교하거나, "
            "표준 단위(L, mL)를 사용하여 측정해야 합니다.",
        ),

        # ── e3-2-5-02: 들이의 단위 ──
        mc(
            id="e3-2-5-1-cc-001",
            concept_id="e3-2-5-02",  # 변경: e3-2-5-1 → e3-2-5-02
            category="concept",
            part="calc",
            difficulty=3,
            content="1L는 몇 mL인가요?",
            options=[
                "10mL",
                "100mL",
                "1000mL",
                "10000mL",
            ],
            correct="C",
            explanation="1L = 1000mL입니다. "
            "들이 단위 변환: 1L = 1000mL",
        ),

        # ── e3-2-5-03: 들이 어림하고 재어 보기 (신규) ──
        mc(
            id="e3-2-5-03-cc-001",
            concept_id="e3-2-5-03",
            category="concept",
            part="calc",
            difficulty=4,
            content="다음 중 들이가 약 1L인 것은?",
            options=[
                "숟가락",
                "컵",
                "큰 물병",
                "욕조",
            ],
            correct="C",
            explanation="1L는 1000mL로 큰 물병 정도의 들이입니다. "
            "숟가락이나 컵은 mL 단위, 욕조는 수백 L 이상입니다.",
        ),

        # ── e3-2-5-04: 들이의 덧셈과 뺄셈 (신규) ──
        mc(
            id="e3-2-5-04-cc-001",
            concept_id="e3-2-5-04",
            category="concept",
            part="calc",
            difficulty=5,
            content="2L 500mL + 1L 800mL = ?",
            options=[
                "3L 300mL",
                "4L 300mL",
                "3L 1300mL",
                "4L",
            ],
            correct="B",
            explanation="500mL + 800mL = 1300mL = 1L 300mL입니다. "
            "2L + 1L + 1L 300mL = 4L 300mL입니다.",
        ),

        # ── e3-2-5-05: 무게 비교하기 ──
        mc(
            id="e3-2-5-2-cc-001",
            concept_id="e3-2-5-05",  # 변경: e3-2-5-2 → e3-2-5-05
            category="concept",
            part="calc",
            difficulty=5,
            content="다음 중 가장 무거운 것은?",
            options=[
                "큰 스티로폼 상자",
                "작은 쇠구슬",
                "부피로 판단할 수 없다",
                "크기가 같으면 무게도 같다",
            ],
            correct="C",
            explanation="부피(크기)와 무게는 다릅니다! "
            "스티로폼 상자는 부피가 크지만 가볍고, 쇠구슬은 작지만 무겁습니다. "
            "'부피가 크면 무게도 크다'는 오개념입니다.",
        ),

        # ── e3-2-5-06: 무게의 단위 ──
        mc(
            id="e3-2-5-1-cc-002",
            concept_id="e3-2-5-06",  # 변경: e3-2-5-1 → e3-2-5-06
            category="concept",
            part="calc",
            difficulty=6,
            content="1kg은 몇 g인가요?",
            options=[
                "10g",
                "100g",
                "1000g",
                "10000g",
            ],
            correct="C",
            explanation="1kg = 1000g입니다. "
            "무게 단위 변환: 1kg = 1000g",
        ),

        # ── e3-2-5-07: 무게 어림하고 재어 보기 (신규) ──
        mc(
            id="e3-2-5-07-cc-001",
            concept_id="e3-2-5-07",
            category="concept",
            part="calc",
            difficulty=4,
            content="다음 중 무게가 약 1kg인 것은?",
            options=[
                "연필 1자루",
                "공책 1권",
                "물 1L (큰 물병)",
                "책상",
            ],
            correct="C",
            explanation="물 1L의 무게는 약 1kg입니다. "
            "연필이나 공책은 수십 g, 책상은 수십 kg 정도입니다.",
        ),

        # ── e3-2-5-08: 무게의 덧셈과 뺄셈 (신규) ──
        mc(
            id="e3-2-5-08-cc-001",
            concept_id="e3-2-5-08",
            category="concept",
            part="calc",
            difficulty=6,
            content="3kg 200g - 1kg 500g = ?",
            options=[
                "1kg 700g",
                "2kg 700g",
                "2kg 300g",
                "1kg 300g",
            ],
            correct="A",
            explanation="200g에서 500g을 뺄 수 없으므로 1kg을 빌려옵니다. "
            "1200g - 500g = 700g. 2kg - 1kg = 1kg. 답: 1kg 700g",
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 6단원: 자료의 정리 (4개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e3-2-6-01: 표의 내용 알아보기 ──
        mc(
            id="e3-2-6-1-cc-001",
            concept_id="e3-2-6-01",  # 변경: e3-2-6-1 → e3-2-6-01
            category="concept",
            part="data",
            difficulty=7,
            content="자료를 표로 정리하는 이유는?",
            options=[
                "그림을 그리기 위해",
                "자료를 한눈에 알아보기 쉽게 하기 위해",
                "숫자를 많이 쓰기 위해",
                "계산을 빠르게 하기 위해",
            ],
            correct="B",
            explanation="표는 자료를 체계적으로 정리하여 한눈에 비교하고 파악할 수 있게 합니다.",
        ),

        # ── e3-2-6-02: 그림그래프 알아보기 ──
        mc(
            id="e3-2-6-2-cc-001",
            concept_id="e3-2-6-02",  # 변경: e3-2-6-2 → e3-2-6-02
            category="concept",
            part="data",
            difficulty=4,
            content="그림그래프에서 큰 스마일 1개 = 10명입니다. 큰 스마일 3개는 몇 명을 나타내나요?",
            options=[
                "3명",
                "13명",
                "30명",
                "300명",
            ],
            correct="C",
            explanation="범례를 확인해야 합니다! "
            "큰 스마일 1개 = 10명이므로, 3개 = 10 × 3 = 30명입니다. "
            "'그림 개수 = 사람 수'로 착각하면 틀립니다.",
        ),
        mc(
            id="e3-2-6-2-cc-002",
            concept_id="e3-2-6-02",  # 변경: e3-2-6-2 → e3-2-6-02
            category="concept",
            part="data",
            difficulty=6,
            content="그림그래프에서 큰 그림 1개 = 100, 작은 그림 1개 = 10입니다. "
            "큰 그림 2개와 작은 그림 3개는?",
            options=[
                "5",
                "23",
                "230",
                "2030",
            ],
            correct="C",
            explanation="큰 그림 2개 = 100 × 2 = 200, 작은 그림 3개 = 10 × 3 = 30입니다. "
            "합계: 200 + 30 = 230입니다. "
            "범례를 무시하고 그림 개수만 세면 틀립니다.",
        ),

        # ── e3-2-6-03: 그림그래프로 나타내기 (신규) ──
        mc(
            id="e3-2-6-03-cc-001",
            concept_id="e3-2-6-03",
            category="concept",
            part="data",
            difficulty=5,
            content="자료를 그림그래프로 나타낼 때 가장 먼저 해야 할 일은?",
            options=[
                "제목을 쓴다",
                "그림을 그린다",
                "그림 하나가 나타내는 수(범례)를 정한다",
                "색칠한다",
            ],
            correct="C",
            explanation="그림그래프를 그리기 전에 범례(그림 하나가 나타내는 수)를 먼저 정해야 합니다. "
            "범례에 따라 필요한 그림의 개수가 달라집니다.",
        ),

        # ── e3-2-6-04: 자료를 조사하여 그림그래프로 나타내기 (신규) ──
        mc(
            id="e3-2-6-04-cc-001",
            concept_id="e3-2-6-04",
            category="concept",
            part="data",
            difficulty=7,
            content="학급 친구들이 좋아하는 과일을 조사하여 그림그래프로 나타내려고 합니다. "
            "다음 중 올바른 순서는?",
            options=[
                "조사 → 표 정리 → 범례 정하기 → 그래프 그리기",
                "그래프 그리기 → 조사 → 표 정리",
                "범례 정하기 → 조사 → 그래프 그리기",
                "표 정리 → 조사 → 그래프 그리기",
            ],
            correct="A",
            explanation="자료 정리의 순서: 1) 자료 조사 → 2) 표로 정리 → 3) 범례 정하기 → 4) 그림그래프 그리기입니다. "
            "체계적인 순서를 따라야 정확한 그래프를 만들 수 있습니다.",
        ),
    ]
