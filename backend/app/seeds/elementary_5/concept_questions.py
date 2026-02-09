"""초등학교 5학년 개념 문제 시드 데이터.

커버 단원 (PDF 기반 35개 세분화 개념):
  1학기 3단원 - 규칙과 대응 (3개)
  1학기 6단원 - 다각형의 둘레와 넓이 (9개)
  2학기 1단원 - 수의 범위와 어림하기 (7개)
  2학기 3단원 - 합동과 대칭 (4개)
  2학기 5단원 - 직육면체 (6개)
  2학기 6단원 - 평균과 가능성 (6개)
"""

from .._base import concept, mc


def get_concepts() -> list[dict]:
    """개념 35개 반환 (PDF 기반 세분화 - 개념 단원만)."""
    from app.data.pdf_concept_map import E5_S1_CONCEPTS, E5_S2_CONCEPTS

    # 1학기 개념 단원: ch3(규칙과 대응), ch6(다각형의 둘레와 넓이)
    concept_s1_chapters = {3, 6}
    # 2학기 개념 단원: ch1(수의 범위와 어림하기), ch3(합동과 대칭), ch5(직육면체), ch6(평균과 가능성)
    concept_s2_chapters = {1, 3, 5, 6}

    result = []
    for c in E5_S1_CONCEPTS:
        if c["chapter_number"] in concept_s1_chapters:
            result.append(concept(
                id=c["id"], name=c["name"], grade=c["grade"],
                category=c["category"], part=c["part"], description=c["description"],
            ))
    for c in E5_S2_CONCEPTS:
        if c["chapter_number"] in concept_s2_chapters:
            result.append(concept(
                id=c["id"], name=c["name"], grade=c["grade"],
                category=c["category"], part=c["part"], description=c["description"],
            ))
    return result


def get_questions() -> list[dict]:
    """개념 문제 반환 (기존 문제 concept_id 변경 + 신규 문제)."""
    return [
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 3단원: 규칙과 대응 (3개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e5-1-3-01: 두 양 사이의 관계 ──
        mc(
            id="e5-1-3-1-cc-001",
            concept_id="e5-1-3-01",  # 변경: e5-1-3-1 → e5-1-3-01
            category="concept",
            part="algebra",
            difficulty=2,
            content="자전거 1대에는 바퀴가 2개 있습니다. 자전거가 ○대 있을 때 바퀴의 수를 식으로 나타내면?",
            options=["○ + 2", "○ × 2", "○ ÷ 2", "2 - ○"],
            correct="B",
            explanation="자전거 수에 비례하여 바퀴 수가 증가합니다. 바퀴 수 = 자전거 수 × 2 = ○ × 2입니다. 이는 정비례 관계의 기초입니다.",
            points=10,
        ),
        mc(
            id="e5-1-3-1-cc-002",
            concept_id="e5-1-3-01",  # 변경: e5-1-3-1 → e5-1-3-01
            category="concept",
            part="algebra",
            difficulty=3,
            content="형의 나이는 동생의 나이보다 3살 많습니다. 동생의 나이가 △살일 때, 형의 나이는?",
            options=["△ + 3", "△ - 3", "△ × 3", "△ ÷ 3"],
            correct="A",
            explanation="형의 나이 = 동생의 나이 + 3 = △ + 3입니다. 이는 덧셈 관계(y = x + a)로 나타낼 수 있습니다.",
            points=10,
        ),

        # ── e5-1-3-02: 대응 관계를 식으로 나타내기 ──
        mc(
            id="e5-1-3-2-cc-001",
            concept_id="e5-1-3-02",  # 변경: e5-1-3-2 → e5-1-3-02
            category="concept",
            part="algebra",
            difficulty=4,
            content="다음 대응 관계에서 규칙을 찾으시오.\n\n입력: 2 → 출력: 7\n입력: 3 → 출력: 10\n입력: 4 → 출력: 13\n입력: ○ → 출력: ?",
            options=["○ + 5", "○ × 3 + 1", "○ × 2 + 3", "○ × 4 - 1"],
            correct="B",
            explanation="규칙: (입력 × 3) + 1 = 출력. 2×3+1=7, 3×3+1=10, 4×3+1=13. 따라서 출력 = ○ × 3 + 1입니다.",
            points=10,
        ),
        mc(
            id="e5-1-3-2-cc-002",
            concept_id="e5-1-3-02",  # 신규 추가
            category="concept",
            part="algebra",
            difficulty=5,
            content="□가 1씩 커질 때 △가 5씩 커지는 관계를 식으로 나타내면? (□=1일 때 △=8)",
            options=["△ = □ + 7", "△ = □ × 5 + 3", "△ = □ + 5", "△ = □ × 8"],
            correct="B",
            explanation="□가 1씩 커질 때 △가 5씩 커지므로 △ = □ × 5 + a 형태입니다. □=1일 때 △=8이므로 8 = 1×5 + a → a=3. 따라서 △ = □ × 5 + 3입니다.",
            points=10,
        ),

        # ── e5-1-3-03: 생활 속에서 대응 관계를 찾아 식으로 나타내기 ──
        mc(
            id="e5-1-3-3-cc-001",  # 신규 추가
            concept_id="e5-1-3-03",
            category="concept",
            part="algebra",
            difficulty=6,
            content="한 봉지에 사탕 5개씩 들어있고, 낱개 사탕 3개가 따로 있습니다. 봉지가 ○개일 때 전체 사탕 수를 식으로 나타내면?",
            options=["○ × 5", "○ × 5 + 3", "○ + 5 + 3", "○ × 3 + 5"],
            correct="B",
            explanation="봉지 ○개에 들어있는 사탕: ○ × 5개, 낱개 사탕: 3개. 전체 = ○ × 5 + 3개입니다. 실생활에서 두 양의 대응 관계를 찾는 문제입니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 6단원: 다각형의 둘레와 넓이 (9개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e5-1-6-01: 정다각형의 둘레 ──
        mc(
            id="e5-1-6-1-cc-003",  # 신규 추가
            concept_id="e5-1-6-01",
            category="concept",
            part="geo",
            difficulty=3,
            content="정육각형의 한 변의 길이가 7cm입니다. 둘레는?",
            options=["42cm", "49cm", "35cm", "56cm"],
            correct="A",
            explanation="정다각형의 둘레 = 한 변 × 변의 수. 정육각형은 6개 변이므로 7 × 6 = 42cm입니다.",
            points=10,
        ),

        # ── e5-1-6-02: 사각형의 둘레 ──
        mc(
            id="e5-1-6-2-cc-003",  # 신규 추가
            concept_id="e5-1-6-02",
            category="concept",
            part="geo",
            difficulty=4,
            content="가로 8cm, 세로 5cm인 직사각형의 둘레를 구하는 식은?",
            options=["8 + 5", "(8 + 5) × 2", "8 × 5", "8 × 2 + 5"],
            correct="B",
            explanation="직사각형의 둘레 = (가로 + 세로) × 2. (8 + 5) × 2 = 13 × 2 = 26cm입니다.",
            points=10,
        ),

        # ── e5-1-6-03: 넓이의 단위 1cm² ──
        mc(
            id="e5-1-6-3-cc-001",  # 신규 추가
            concept_id="e5-1-6-03",
            category="concept",
            part="geo",
            difficulty=2,
            content="1cm²는 무엇을 의미합니까?",
            options=[
                "한 변이 1cm인 정사각형의 넓이",
                "가로 1cm, 세로 2cm인 직사각형의 넓이",
                "둘레가 1cm인 도형의 넓이",
                "한 변이 1m인 정사각형의 넓이"
            ],
            correct="A",
            explanation="1cm²(1제곱센티미터)는 한 변의 길이가 1cm인 정사각형의 넓이입니다. 넓이의 기본 단위입니다.",
            points=10,
        ),

        # ── e5-1-6-04: 직사각형의 넓이 ──
        mc(
            id="e5-1-6-4-cc-001",  # 신규 추가
            concept_id="e5-1-6-04",
            category="concept",
            part="geo",
            difficulty=3,
            content="직사각형의 넓이 공식 (가로 × 세로)는 왜 성립합니까?",
            options=[
                "가로 방향 단위넓이 개수 × 세로 방향 줄 수를 세면 전체 개수가 나오므로",
                "직사각형은 정사각형과 같으므로",
                "둘레와 넓이는 항상 같으므로",
                "공식이므로 외워야 한다"
            ],
            correct="A",
            explanation="직사각형을 1cm² 단위로 채우면, 가로 방향에 가로(cm)개, 세로 방향에 세로(줄)개가 배열됩니다. 전체 개수 = 가로 × 세로 = 넓이(cm²)입니다.",
            points=10,
        ),

        # ── e5-1-6-05: 1cm²보다 더 큰 넓이의 단위 ──
        mc(
            id="e5-1-6-5-cc-001",  # 신규 추가
            concept_id="e5-1-6-05",
            category="concept",
            part="geo",
            difficulty=4,
            content="1m²는 몇 cm²입니까?",
            options=["100cm²", "1000cm²", "10000cm²", "1000000cm²"],
            correct="C",
            explanation="1m = 100cm이므로, 1m² = (100cm)² = 100cm × 100cm = 10000cm²입니다. 길이의 제곱임을 주의하세요!",
            points=10,
        ),

        # ── e5-1-6-06: 평행사변형의 넓이 ──
        mc(
            id="e5-1-6-1-cc-001",
            concept_id="e5-1-6-06",  # 변경: e5-1-6-1 → e5-1-6-06
            category="concept",
            part="geo",
            difficulty=3,
            content="평행사변형의 넓이를 구하는 공식은?",
            options=["가로 × 세로", "밑변 × 높이", "밑변 × 높이 ÷ 2", "대각선 × 대각선 ÷ 2"],
            correct="B",
            explanation="평행사변형을 잘라서 직사각형으로 등적 변형하면 넓이 = 밑변 × 높이입니다. 높이는 밑변에 수직인 선분의 길이입니다.",
            points=10,
        ),

        # ── e5-1-6-07: 삼각형의 넓이 ──
        mc(
            id="e5-1-6-1-cc-002",
            concept_id="e5-1-6-07",  # 변경: e5-1-6-1 → e5-1-6-07
            category="concept",
            part="geo",
            difficulty=4,
            content="삼각형의 넓이가 (밑변 × 높이 ÷ 2)인 이유는?",
            options=[
                "삼각형은 사각형의 절반이므로",
                "2개 붙이면 평행사변형이 되므로",
                "높이를 2로 나눠야 하므로",
                "밑변이 절반으로 줄어드므로"
            ],
            correct="B",
            explanation="똑같은 삼각형 2개를 붙이면 평행사변형이 됩니다. 따라서 삼각형 넓이 = (평행사변형 넓이) ÷ 2 = (밑변 × 높이) ÷ 2입니다. 오답 C는 ÷2를 누락하는 흔한 오류입니다. ★★★",
            points=10,
        ),

        # ── e5-1-6-08: 마름모의 넓이 ──
        mc(
            id="e5-1-6-2-cc-002",  # 신규 추가
            concept_id="e5-1-6-08",
            category="concept",
            part="geo",
            difficulty=5,
            content="마름모의 넓이를 구하는 공식은?",
            options=[
                "밑변 × 높이",
                "한 변 × 한 변",
                "(한 대각선 × 다른 대각선) ÷ 2",
                "(한 대각선 + 다른 대각선) ÷ 2"
            ],
            correct="C",
            explanation="마름모의 넓이 = (한 대각선 × 다른 대각선) ÷ 2. 두 대각선이 수직으로 만나는 성질을 이용하여 삼각형 4개로 나누어 유도합니다.",
            points=10,
        ),

        # ── e5-1-6-09: 사다리꼴의 넓이 ──
        mc(
            id="e5-1-6-2-cc-001",
            concept_id="e5-1-6-09",  # 변경: e5-1-6-2 → e5-1-6-09
            category="concept",
            part="geo",
            difficulty=5,
            content="사다리꼴의 넓이 공식은 (윗변 + 아랫변) × 높이 ÷ 2입니다. 다음 중 이 공식의 유도 과정은?",
            options=[
                "직사각형을 반으로 잘랐으므로",
                "똑같은 사다리꼴 2개를 붙이면 평행사변형이 되므로",
                "평행사변형의 대각선이 사다리꼴이므로",
                "삼각형 2개의 넓이를 더했으므로"
            ],
            correct="B",
            explanation="똑같은 사다리꼴 2개를 180° 돌려 붙이면 밑변이 (윗변 + 아랫변)인 평행사변형이 됩니다. 따라서 사다리꼴 넓이 = 평행사변형 넓이 ÷ 2입니다. ÷2 누락 주의! ★★★",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 1단원: 수의 범위와 어림하기 (7개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e5-2-1-01: 이상과 이하 ──
        mc(
            id="e5-2-1-1-cc-002",  # 신규 추가
            concept_id="e5-2-1-01",
            category="concept",
            part="calc",
            difficulty=2,
            content="10 이하의 자연수는 10을 포함합니까?",
            options=["포함한다", "포함하지 않는다", "경우에 따라 다르다", "판단할 수 없다"],
            correct="A",
            explanation="이하(≤)는 경계값을 포함합니다. 10 이하는 10도 포함하여 1,2,3,...,9,10을 의미합니다. 미만(<)과 구별하세요!",
            points=10,
        ),

        # ── e5-2-1-02: 초과와 미만 ──
        mc(
            id="e5-2-1-1-cc-001",
            concept_id="e5-2-1-02",  # 변경: e5-2-1-1 → e5-2-1-02 (기존 문제는 이상/미만 혼합이므로 초과/미만 개념으로 이동)
            category="concept",
            part="calc",
            difficulty=3,
            content="5 이상 10 미만인 자연수는 모두 몇 개입니까?",
            options=["4개", "5개", "6개", "7개"],
            correct="B",
            explanation="5 이상(5 포함) 10 미만(10 불포함): 5, 6, 7, 8, 9로 총 5개입니다. 이상/이하는 경계값 포함(●), 초과/미만은 불포함(○)입니다.",
            points=10,
        ),

        # ── e5-2-1-03: 수의 범위 활용하기 ──
        mc(
            id="e5-2-1-3-cc-001",  # 신규 추가
            concept_id="e5-2-1-03",
            category="concept",
            part="calc",
            difficulty=5,
            content="놀이기구 탑승 키 제한: '120cm 이상'. 키가 119.8cm인 어린이는 탈 수 있습니까?",
            options=["탈 수 있다", "탈 수 없다", "약간 크므로 탈 수 있다", "판단할 수 없다"],
            correct="B",
            explanation="120cm 이상이므로 120cm보다 작으면 탈 수 없습니다. 119.8cm < 120cm이므로 탑승 불가입니다. 이상/초과의 실생활 활용 문제입니다.",
            points=10,
        ),

        # ── e5-2-1-04: 올림 ──
        mc(
            id="e5-2-1-4-cc-001",  # 신규 추가
            concept_id="e5-2-1-04",
            category="concept",
            part="calc",
            difficulty=3,
            content="456을 십의 자리에서 올림하면?",
            options=["400", "450", "460", "500"],
            correct="D",
            explanation="십의 자리에서 올림하면 십의 자리 아래를 버리고 백의 자리를 올립니다. 456 → 500입니다. 반올림과 다릅니다!",
            points=10,
        ),

        # ── e5-2-1-05: 버림 ──
        mc(
            id="e5-2-1-5-cc-001",  # 신규 추가
            concept_id="e5-2-1-05",
            category="concept",
            part="calc",
            difficulty=3,
            content="789를 십의 자리에서 버림하면?",
            options=["700", "780", "790", "800"],
            correct="B",
            explanation="십의 자리에서 버림하면 일의 자리를 버립니다. 789 → 780입니다.",
            points=10,
        ),

        # ── e5-2-1-06: 반올림 ──
        mc(
            id="e5-2-1-2-cc-001",
            concept_id="e5-2-1-06",  # 변경: e5-2-1-2 → e5-2-1-06
            category="concept",
            part="calc",
            difficulty=4,
            content="456을 십의 자리에서 반올림하면?",
            options=["400", "450", "460", "500"],
            correct="D",
            explanation="십의 자리(5)가 5 이상이므로 올림합니다. 456 → 500입니다. '~에서 반올림'은 해당 자리를 보고 윗자리에 반영합니다. ★★★",
            points=10,
        ),

        # ── e5-2-1-07: 올림, 버림, 반올림 활용하기 ──
        mc(
            id="e5-2-1-2-cc-002",
            concept_id="e5-2-1-07",  # 변경: e5-2-1-2 → e5-2-1-07
            category="concept",
            part="calc",
            difficulty=5,
            content="사과 127개를 상자에 10개씩 담으려고 합니다. 필요한 상자의 수는? (어림 방법 선택)",
            options=["버림: 12개", "올림: 13개", "반올림: 13개", "버림: 13개"],
            correct="B",
            explanation="127 ÷ 10 = 12.7 → 모든 사과를 담으려면 13개 필요(올림). 버림(12)은 7개가 남고, 반올림은 상황에 맞지 않습니다. 물건 묶음 구매 시 올림 사용! ★★★",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 3단원: 합동과 대칭 (4개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e5-2-3-01: 도형의 합동 ──
        mc(
            id="e5-2-3-1-cc-001",
            concept_id="e5-2-3-01",  # 변경: e5-2-3-1 → e5-2-3-01
            category="concept",
            part="geo",
            difficulty=3,
            content="합동인 두 도형의 성질로 옳은 것은?",
            options=[
                "모양만 같다",
                "크기만 같다",
                "모양과 크기가 모두 같다",
                "대칭축이 있다"
            ],
            correct="C",
            explanation="합동은 모양과 크기가 모두 같아 완전히 겹쳐지는 관계입니다. 대응변의 길이와 대응각의 크기가 각각 같습니다.",
            points=10,
        ),

        # ── e5-2-3-02: 합동인 도형의 성질 ──
        mc(
            id="e5-2-3-2-cc-003",  # 신규 추가
            concept_id="e5-2-3-02",
            category="concept",
            part="geo",
            difficulty=4,
            content="합동인 두 삼각형에서 대응변의 관계는?",
            options=[
                "대응변의 길이는 같다",
                "대응변의 길이는 2배이다",
                "대응변의 길이는 관계없다",
                "대응변의 길이는 각각 다르다"
            ],
            correct="A",
            explanation="합동인 도형에서 대응변의 길이는 같고, 대응각의 크기도 같습니다. 이것이 합동의 핵심 성질입니다.",
            points=10,
        ),

        # ── e5-2-3-03: 선대칭도형과 그 성질 ──
        mc(
            id="e5-2-3-2-cc-001",
            concept_id="e5-2-3-03",  # 변경: e5-2-3-2 → e5-2-3-03
            category="concept",
            part="geo",
            difficulty=4,
            content="선대칭도형에서 대칭축의 성질은?",
            options=[
                "대응점을 이은 선분의 중점을 지난다",
                "대응점을 이은 선분을 수직이등분한다",
                "도형의 무게중심을 지난다",
                "도형의 대각선이다"
            ],
            correct="B",
            explanation="선대칭도형의 대칭축은 대응점을 이은 선분을 수직이등분합니다. 대칭축을 따라 접으면 완전히 겹쳐집니다. 오답 A는 점대칭의 성질입니다.",
            points=10,
        ),

        # ── e5-2-3-04: 점대칭도형과 그 성질 ──
        mc(
            id="e5-2-3-2-cc-002",
            concept_id="e5-2-3-04",  # 변경: e5-2-3-2 → e5-2-3-04
            category="concept",
            part="geo",
            difficulty=5,
            content="평행사변형이 점대칭도형인지 선대칭도형인지 판단하시오.",
            options=[
                "점대칭도형이다",
                "선대칭도형이다",
                "둘 다이다",
                "둘 다 아니다"
            ],
            correct="A",
            explanation="평행사변형은 대각선의 교점을 중심으로 180° 돌리면 겹치므로 점대칭도형입니다. 하지만 대칭축은 없습니다(선대칭 X). 오답 유도: 평행사변형의 대각선을 대칭축으로 착각 ★★★",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 5단원: 직육면체 (6개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e5-2-5-01: 직육면체 ──
        mc(
            id="e5-2-5-1-cc-001",
            concept_id="e5-2-5-01",  # 변경: e5-2-5-1 → e5-2-5-01
            category="concept",
            part="geo",
            difficulty=3,
            content="직육면체의 면은 몇 개입니까?",
            options=["4개", "6개", "8개", "12개"],
            correct="B",
            explanation="직육면체는 6개의 면(앞뒤·좌우·위아래)으로 이루어져 있습니다. 모서리 12개, 꼭짓점 8개입니다.",
            points=10,
        ),

        # ── e5-2-5-02: 정육면체 ──
        mc(
            id="e5-2-5-2-cc-003",  # 신규 추가
            concept_id="e5-2-5-02",
            category="concept",
            part="geo",
            difficulty=4,
            content="정육면체는 직육면체의 특수한 경우입니다. 정육면체의 특징은?",
            options=[
                "6개의 면이 모두 정사각형이다",
                "6개의 면이 모두 직사각형이다",
                "4개의 면이 정사각형이다",
                "대각선의 길이가 모두 다르다"
            ],
            correct="A",
            explanation="정육면체는 6개의 면이 모두 합동인 정사각형입니다. 모든 모서리의 길이가 같습니다.",
            points=10,
        ),

        # ── e5-2-5-03: 직육면체의 성질 ──
        mc(
            id="e5-2-5-1-cc-002",
            concept_id="e5-2-5-03",  # 변경: e5-2-5-1 → e5-2-5-03
            category="concept",
            part="geo",
            difficulty=4,
            content="직육면체에서 한 면과 평행한 면은 몇 개입니까?",
            options=["1개", "2개", "3개", "4개"],
            correct="A",
            explanation="직육면체에서 한 면과 평행한 면은 마주 보는 1개뿐입니다. 총 3쌍의 평행한 면이 있습니다.",
            points=10,
        ),

        # ── e5-2-5-04: 직육면체의 겨냥도 ──
        mc(
            id="e5-2-5-4-cc-001",  # 신규 추가
            concept_id="e5-2-5-04",
            category="concept",
            part="geo",
            difficulty=5,
            content="겨냥도에서 보이지 않는 모서리는 어떻게 나타냅니까?",
            options=["실선으로 그린다", "점선으로 그린다", "그리지 않는다", "굵은 선으로 그린다"],
            correct="B",
            explanation="겨냥도에서 보이지 않는 모서리는 점선으로 나타냅니다. 보이는 모서리는 실선으로 그립니다.",
            points=10,
        ),

        # ── e5-2-5-05: 정육면체의 전개도 ──
        mc(
            id="e5-2-5-5-cc-001",  # 신규 추가
            concept_id="e5-2-5-05",
            category="concept",
            part="geo",
            difficulty=6,
            content="정육면체의 전개도는 몇 가지입니까?",
            options=["1가지", "6가지", "11가지", "무한히 많다"],
            correct="C",
            explanation="정육면체의 전개도는 11가지입니다. 접었을 때 마주 보는 면을 파악하는 것이 중요합니다.",
            points=10,
        ),

        # ── e5-2-5-06: 직육면체의 전개도 ──
        mc(
            id="e5-2-5-2-cc-001",
            concept_id="e5-2-5-06",  # 변경: e5-2-5-2 → e5-2-5-06
            category="concept",
            part="geo",
            difficulty=5,
            content="직육면체의 전개도에 대한 설명으로 옳은 것은?",
            options=[
                "전개도는 오직 한 가지만 있다",
                "전개도는 여러 가지 모양이 가능하다",
                "전개도에는 항상 정사각형이 있다",
                "전개도는 십자가 모양만 가능하다"
            ],
            correct="B",
            explanation="직육면체의 전개도는 모서리를 자르는 위치에 따라 여러 가지 모양으로 만들 수 있습니다. 단, 마주 보는 면이 평행하게 배치되어야 합니다.",
            points=10,
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 6단원: 평균과 가능성 (6개 개념)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e5-2-6-01: 평균 ──
        mc(
            id="e5-2-6-1-cc-003",  # 신규 추가
            concept_id="e5-2-6-01",
            category="concept",
            part="data",
            difficulty=2,
            content="평균의 의미로 올바른 것은?",
            options=[
                "자료 중 가장 큰 값",
                "자료의 값을 고르게 한 값",
                "자료 중 가장 작은 값",
                "자료의 개수"
            ],
            correct="B",
            explanation="평균은 자료의 값을 고르게 한 값입니다. 모든 자료를 대표하는 하나의 값으로 이해합니다.",
            points=10,
        ),

        # ── e5-2-6-02: 평균 구하기 ──
        mc(
            id="e5-2-6-1-cc-001",
            concept_id="e5-2-6-02",  # 변경: e5-2-6-1 → e5-2-6-02
            category="concept",
            part="data",
            difficulty=3,
            content="3, 5, 7, 9의 평균을 구하시오.",
            options=["5", "6", "7", "8"],
            correct="B",
            explanation="평균 = (3 + 5 + 7 + 9) ÷ 4 = 24 ÷ 4 = 6입니다. 평균 = (모든 값의 합) ÷ (자료의 개수)입니다.",
            points=10,
        ),
        mc(
            id="e5-2-6-1-cc-002",
            concept_id="e5-2-6-02",  # 변경: e5-2-6-1 → e5-2-6-02
            category="concept",
            part="data",
            difficulty=4,
            content="시험 점수: 80, 90, 0, 85, 95. 평균을 구하시오. (0점 포함 주의)",
            options=["70", "80", "85", "90"],
            correct="A",
            explanation="평균 = (80 + 90 + 0 + 85 + 95) ÷ 5 = 350 ÷ 5 = 70입니다. 0점도 자료에 포함하여 개수를 5개로 계산해야 합니다. 오답 유도: 0을 제외하고 4개로 나누기 ★★",
            points=10,
        ),

        # ── e5-2-6-03: 평균 이용하기 ──
        mc(
            id="e5-2-6-3-cc-001",  # 신규 추가
            concept_id="e5-2-6-03",
            category="concept",
            part="data",
            difficulty=6,
            content="5명의 키 평균이 150cm입니다. 5명의 키의 합은?",
            options=["150cm", "300cm", "750cm", "알 수 없다"],
            correct="C",
            explanation="평균 = (합) ÷ (개수)이므로, 합 = 평균 × 개수 = 150 × 5 = 750cm입니다. 평균을 역으로 활용하는 문제입니다.",
            points=10,
        ),

        # ── e5-2-6-04: 일이 일어날 가능성을 말로 표현하기 ──
        mc(
            id="e5-2-6-4-cc-001",  # 신규 추가
            concept_id="e5-2-6-04",
            category="concept",
            part="data",
            difficulty=3,
            content="주사위를 던질 때 7이 나올 가능성을 말로 표현하면?",
            options=["불가능하다", "~아닐 것 같다", "반반이다", "확실하다"],
            correct="A",
            explanation="주사위 눈은 1~6이므로 7은 나올 수 없습니다. 따라서 '불가능하다'입니다.",
            points=10,
        ),

        # ── e5-2-6-05: 일이 일어날 가능성을 비교하기 ──
        mc(
            id="e5-2-6-5-cc-001",  # 신규 추가
            concept_id="e5-2-6-05",
            category="concept",
            part="data",
            difficulty=5,
            content="주사위를 던질 때, '짝수가 나올 가능성'과 '3의 배수가 나올 가능성'을 비교하면?",
            options=[
                "짝수가 나올 가능성이 더 높다",
                "3의 배수가 나올 가능성이 더 높다",
                "둘의 가능성은 같다",
                "비교할 수 없다"
            ],
            correct="A",
            explanation="짝수(2,4,6) 3가지, 3의 배수(3,6) 2가지. 짝수가 나올 가능성이 더 높습니다. 경우의 수를 세어 비교합니다.",
            points=10,
        ),

        # ── e5-2-6-06: 일이 일어날 가능성을 수로 표현하기 ──
        mc(
            id="e5-2-6-2-cc-001",
            concept_id="e5-2-6-06",  # 변경: e5-2-6-2 → e5-2-6-06
            category="concept",
            part="data",
            difficulty=5,
            content="주사위를 던질 때, 6의 약수(1,2,3,6)가 나올 가능성을 수치로 표현하면?",
            options=["0 (불가능)", "1/2 (반반)", "1 (확실)", "2/3 (반반보다 높음)"],
            correct="D",
            explanation="주사위 눈: 1,2,3,4,5,6 총 6가지. 6의 약수: 1,2,3,6로 4가지. 가능성 = 4/6 = 2/3입니다. 2/3 > 1/2이므로 '일 것 같다' 수준입니다.",
            points=10,
        ),

        # ────────────────────────────────────────────────────────
        # 추가 문제: 각 개념별 커버리지 확대 (신규 문제)
        # ────────────────────────────────────────────────────────

        # e5-1-6-01 추가 문제
        mc(
            id="e5-1-6-1-cc-004",
            concept_id="e5-1-6-01",
            category="concept",
            part="geo",
            difficulty=5,
            content="정오각형의 둘레가 35cm입니다. 한 변의 길이는?",
            options=["5cm", "7cm", "30cm", "40cm"],
            correct="B",
            explanation="정오각형의 둘레 = 한 변 × 5. 35 ÷ 5 = 7cm입니다. 둘레에서 한 변을 구하는 역산 문제입니다.",
            points=10,
        ),

        # e5-1-6-02 추가 문제
        mc(
            id="e5-1-6-2-cc-004",
            concept_id="e5-1-6-02",
            category="concept",
            part="geo",
            difficulty=6,
            content="직사각형의 둘레가 30cm이고, 가로가 세로보다 5cm 더 큽니다. 가로는?",
            options=["5cm", "10cm", "12.5cm", "15cm"],
            correct="B",
            explanation="둘레 = (가로+세로)×2 = 30. 가로+세로=15. 가로=세로+5이므로, (세로+5)+세로=15 → 2×세로=10 → 세로=5cm, 가로=10cm입니다.",
            points=10,
        ),

        # e5-2-1-01 추가 문제
        mc(
            id="e5-2-1-1-cc-003",
            concept_id="e5-2-1-01",
            category="concept",
            part="calc",
            difficulty=4,
            content="x 이상 y 이하를 기호로 나타내면?",
            options=["x < y", "x ≤ y", "x ≥ y", "x > y"],
            correct="B",
            explanation="이상은 ≥, 이하는 ≤입니다. x 이상 y 이하는 x ≤ 범위 ≤ y를 의미합니다. (엄밀히는 x ≤ 값 ≤ y)",
            points=10,
        ),

        # e5-2-3-01 추가 문제
        mc(
            id="e5-2-3-1-cc-002",
            concept_id="e5-2-3-01",
            category="concept",
            part="geo",
            difficulty=5,
            content="합동인 두 삼각형은 항상 닮음입니까?",
            options=["항상 닮음이다", "닮음이 아니다", "경우에 따라 다르다", "합동과 닮음은 무관하다"],
            correct="A",
            explanation="합동은 모양과 크기가 모두 같은 것이고, 닮음은 모양이 같은 것입니다. 따라서 합동 ⊂ 닮음 관계로, 합동이면 항상 닮음입니다. (초등 수준에서는 직관적 이해)",
            points=10,
        ),

        # e5-2-5-01 추가 문제
        mc(
            id="e5-2-5-1-cc-003",
            concept_id="e5-2-5-01",
            category="concept",
            part="geo",
            difficulty=4,
            content="직육면체의 모서리는 몇 개입니까?",
            options=["6개", "8개", "12개", "24개"],
            correct="C",
            explanation="직육면체의 모서리는 12개입니다. (가로 4개, 세로 4개, 높이 4개). 면 6개, 꼭짓점 8개, 모서리 12개를 기억하세요!",
            points=10,
        ),

        # e5-2-6-04 추가 문제
        mc(
            id="e5-2-6-4-cc-002",
            concept_id="e5-2-6-04",
            category="concept",
            part="data",
            difficulty=4,
            content="내일 해가 동쪽에서 뜰 가능성을 말로 표현하면?",
            options=["불가능하다", "~아닐 것 같다", "반반이다", "확실하다"],
            correct="D",
            explanation="해는 항상 동쪽에서 뜨므로 '확실하다'입니다. 가능성 1(100%)인 사건입니다.",
            points=10,
        ),
    ]
