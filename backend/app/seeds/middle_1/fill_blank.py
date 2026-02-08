"""중1 빈칸 채우기(fill_in_blank) 문제 시드 데이터 - 2022 개정 교육과정."""

from .._base import fb, test


def get_fill_blank_data() -> dict:
    """빈칸 채우기 문제 데이터 반환 (12단원 × 2문제 = 24개)."""

    # ============================================================
    # 빈칸 채우기 문제 (12단원 × 2개씩)
    # ============================================================
    questions = [
        # [m1-1-1-2] 거듭제곱과 소인수분해
        fb(
            id="m1-1-1-2-fb-001",
            concept_id="m1-1-1-2",
            category="computation",
            part="calc",
            difficulty=3,
            content="72를 소인수분해하면 2ᵃ × 3ᵇ 꼴일 때, a + b의 값은?",
            answer="5",
            explanation="72 = 2³ × 3². a = 3, b = 2이므로 a + b = 5",
            points=10,
            accept_formats=["5"],
        ),
        # [m1-1-1-3] 최대공약수와 최소공배수
        fb(
            id="m1-1-1-3-fb-001",
            concept_id="m1-1-1-3",
            category="computation",
            part="calc",
            difficulty=5,
            content="두 수 24와 36의 최대공약수는?",
            answer="12",
            explanation="24 = 2³ × 3, 36 = 2² × 3². 최대공약수 = 2² × 3 = 12",
            points=10,
            accept_formats=["12"],
        ),
        # [m1-1-2-3] 유리수의 사칙연산
        fb(
            id="m1-1-2-3-fb-001",
            concept_id="m1-1-2-3",
            category="computation",
            part="calc",
            difficulty=4,
            content="(-8) + 5 - (-3)의 값은?",
            answer="0",
            explanation="(-8) + 5 - (-3) = -8 + 5 + 3 = 0",
            points=10,
            accept_formats=["0"],
        ),
        # [m1-1-2-2] 절대값과 유리수
        fb(
            id="m1-1-2-2-fb-001",
            concept_id="m1-1-2-2",
            category="computation",
            part="calc",
            difficulty=6,
            content="|-6| + |3 - 7|의 값은?",
            answer="10",
            explanation="|-6| = 6, |3 - 7| = |-4| = 4. 6 + 4 = 10",
            points=15,
            accept_formats=["10"],
        ),
        # [m1-1-3-2] 동류항과 식의 계산
        fb(
            id="m1-1-3-2-fb-001",
            concept_id="m1-1-3-2",
            category="computation",
            part="algebra",
            difficulty=4,
            content="5x - 2 + 3x + 7을 간단히 하면 ax + b 형태일 때, a의 값은?",
            answer="8",
            explanation="5x - 2 + 3x + 7 = 8x + 5. a = 8",
            points=10,
            accept_formats=["8"],
        ),
        # [m1-1-3-3] 대입과 식의 값
        fb(
            id="m1-1-3-3-fb-001",
            concept_id="m1-1-3-3",
            category="computation",
            part="algebra",
            difficulty=7,
            content="x = 3일 때, x² - 2x + 5의 값은?",
            answer="8",
            explanation="3² - 2(3) + 5 = 9 - 6 + 5 = 8",
            points=15,
            accept_formats=["8"],
        ),
        # [m1-1-4-2] 일차방정식의 풀이
        fb(
            id="m1-1-4-2-fb-001",
            concept_id="m1-1-4-2",
            category="computation",
            part="algebra",
            difficulty=4,
            content="일차방정식 3x + 6 = 0의 해는? (x = ?)",
            answer="-2",
            explanation="3x = -6, x = -2",
            points=10,
            accept_formats=["-2"],
        ),
        fb(
            id="m1-1-4-2-fb-002",
            concept_id="m1-1-4-2",
            category="computation",
            part="algebra",
            difficulty=7,
            content="일차방정식 2(x - 1) = x + 4의 해는? (x = ?)",
            answer="6",
            explanation="2x - 2 = x + 4, x = 6",
            points=15,
            accept_formats=["6"],
        ),
        # [m1-2-1-1] 순서쌍과 좌표평면
        fb(
            id="m1-2-1-1-fb-001",
            concept_id="m1-2-1-1",
            category="concept",
            part="func",
            difficulty=3,
            content="점 (-5, 3)은 제 몇 사분면에 있는가? (숫자만 입력)",
            answer="2",
            explanation="x < 0, y > 0이므로 제2사분면입니다.",
            points=10,
            accept_formats=["2"],
        ),
        fb(
            id="m1-2-1-1-fb-002",
            concept_id="m1-2-1-1",
            category="concept",
            part="func",
            difficulty=5,
            content="점 (a, -4)가 제4사분면에 있을 때, a의 부호는? (양수이면 +, 음수이면 - 입력)",
            answer="+",
            explanation="제4사분면은 x > 0, y < 0이므로 a > 0입니다.",
            points=10,
            accept_formats=["+", "양수", "positive"],
        ),
        # [m1-2-2-1] 정비례 관계
        fb(
            id="m1-2-2-1-fb-001",
            concept_id="m1-2-2-1",
            category="concept",
            part="func",
            difficulty=4,
            content="y가 x에 정비례하고 x = 3일 때 y = 12이다. x = 5일 때 y의 값은?",
            answer="20",
            explanation="y = ax에서 12 = 3a, a = 4. y = 4x. x = 5일 때 y = 20",
            points=10,
            accept_formats=["20"],
        ),
        # [m1-2-2-2] 반비례 관계
        fb(
            id="m1-2-2-2-fb-001",
            concept_id="m1-2-2-2",
            category="concept",
            part="func",
            difficulty=6,
            content="y가 x에 반비례하고 x = 2일 때 y = 6이다. x = 3일 때 y의 값은?",
            answer="4",
            explanation="y = a/x에서 6 = a/2, a = 12. y = 12/x. x = 3일 때 y = 4",
            points=15,
            accept_formats=["4"],
        ),
        # [m1-2-3-2] 평행선의 성질
        fb(
            id="m1-2-3-2-fb-001",
            concept_id="m1-2-3-2",
            category="concept",
            part="geo",
            difficulty=4,
            content="두 직선이 평행하고 엇각이 65°일 때, 동위각의 크기는? (단위: °)",
            answer="65",
            explanation="평행선에서 동위각과 엇각은 크기가 같으므로 65°입니다.",
            points=10,
            accept_formats=["65", "65도"],
        ),
        # [m1-2-3-1] 점/선/면과 위치관계
        fb(
            id="m1-2-3-1-fb-001",
            concept_id="m1-2-3-1",
            category="concept",
            part="geo",
            difficulty=6,
            content="두 직선이 만나서 생기는 맞꼭지각 중 하나가 120°일 때, 다른 맞꼭지각의 크기는? (단위: °)",
            answer="120",
            explanation="맞꼭지각의 크기는 항상 같으므로 120°입니다.",
            points=10,
            accept_formats=["120", "120도"],
        ),
        # [m1-2-4-1] 다각형의 내각과 외각
        fb(
            id="m1-2-4-1-fb-001",
            concept_id="m1-2-4-1",
            category="concept",
            part="geo",
            difficulty=4,
            content="육각형의 내각의 합은? (단위: °)",
            answer="720",
            explanation="(n-2) × 180° = (6-2) × 180° = 720°",
            points=10,
            accept_formats=["720", "720도"],
        ),
        # [m1-2-4-2] 원과 부채꼴의 성질
        fb(
            id="m1-2-4-2-fb-001",
            concept_id="m1-2-4-2",
            category="concept",
            part="geo",
            difficulty=7,
            content="반지름이 4cm인 원에서 중심각이 90°인 부채꼴의 호의 길이는? (π 사용, 단위: cm)",
            answer="2π",
            explanation="호의 길이 = 2πr × (중심각/360) = 2π × 4 × (90/360) = 8π × (1/4) = 2π cm",
            points=15,
            accept_formats=["2π", "2pi"],
        ),
        # [m1-2-5-2] 겉넓이와 부피
        fb(
            id="m1-2-5-2-fb-001",
            concept_id="m1-2-5-2",
            category="concept",
            part="geo",
            difficulty=5,
            content="밑면의 반지름이 2cm, 높이가 6cm인 원기둥의 부피는? (π 사용, 단위: cm³)",
            answer="24π",
            explanation="부피 = πr²h = π × 2² × 6 = 24π cm³",
            points=10,
            accept_formats=["24π", "24pi"],
        ),
        # [m1-2-5-3] 구
        fb(
            id="m1-2-5-3-fb-001",
            concept_id="m1-2-5-3",
            category="concept",
            part="geo",
            difficulty=7,
            content="반지름이 3cm인 구의 겉넓이는? (π 사용, 단위: cm²)",
            answer="36π",
            explanation="구의 겉넓이 = 4πr² = 4π × 3² = 36π cm²",
            points=15,
            accept_formats=["36π", "36pi"],
        ),
        # [m1-2-6-1] 줄기와 잎 그림/도수분포표
        fb(
            id="m1-2-6-1-fb-001",
            concept_id="m1-2-6-1",
            category="concept",
            part="data",
            difficulty=4,
            content="계급이 '20 이상 30 미만'일 때 계급값은?",
            answer="25",
            explanation="계급값 = (20 + 30) ÷ 2 = 25",
            points=10,
            accept_formats=["25"],
        ),
        # [m1-2-6-3] 상대도수
        fb(
            id="m1-2-6-3-fb-001",
            concept_id="m1-2-6-3",
            category="concept",
            part="data",
            difficulty=6,
            content="어떤 계급의 상대도수가 0.2이고 전체 도수가 50일 때, 이 계급의 도수는?",
            answer="10",
            explanation="도수 = 상대도수 × 전체 도수 = 0.2 × 50 = 10",
            points=15,
            accept_formats=["10"],
        ),
        # [m1-2-7-1] 평균/중앙값/최빈값
        fb(
            id="m1-2-7-1-fb-001",
            concept_id="m1-2-7-1",
            category="concept",
            part="data",
            difficulty=4,
            content="자료 1, 5, 3, 9, 2의 평균은?",
            answer="4",
            explanation="(1 + 5 + 3 + 9 + 2) ÷ 5 = 20 ÷ 5 = 4",
            points=10,
            accept_formats=["4"],
        ),
        fb(
            id="m1-2-7-1-fb-002",
            concept_id="m1-2-7-1",
            category="concept",
            part="data",
            difficulty=6,
            content="자료 6, 2, 8, 4, 5의 중앙값은?",
            answer="5",
            explanation="크기순 정렬: 2, 4, 5, 6, 8. 가운데 값 = 5",
            points=15,
            accept_formats=["5"],
        ),
        # [m1-2-8-1] 산점도
        fb(
            id="m1-2-8-1-fb-001",
            concept_id="m1-2-8-1",
            category="concept",
            part="data",
            difficulty=4,
            content="산점도에서 점들이 우하향으로 분포할 때 이를 무엇이라 하는가? (3글자)",
            answer="음의상관관계",
            explanation="x가 증가할 때 y가 감소하는 경향을 음의 상관관계라고 합니다.",
            points=10,
            accept_formats=["음의상관관계", "음의 상관관계", "음의 상관", "음의상관"],
        ),
        # [m1-2-8-1] 산점도
        fb(
            id="m1-2-8-1-fb-002",
            concept_id="m1-2-8-1",
            category="concept",
            part="data",
            difficulty=7,
            content="기온과 아이스크림 판매량의 관계는? (양의상관관계/음의상관관계/상관관계없음 중 택1)",
            answer="양의상관관계",
            explanation="기온이 올라가면 아이스크림 판매량도 증가하므로 양의 상관관계입니다.",
            points=15,
            accept_formats=["양의상관관계", "양의 상관관계", "양의 상관", "양의상관"],
        ),
    ]

    # ============================================================
    # 테스트 (빈칸 채우기는 통상 개별 테스트 없음)
    # ============================================================
    tests = []

    return {
        "questions": questions,
        "tests": tests,
    }
