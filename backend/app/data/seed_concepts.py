"""교육과정 기반 개념 시드 데이터.

초등 4~6학년: docs/work-plans/elementary-math-curriculum-guide.md 기준
중학교 1~3학년: data/middle_school_math_concepts.md 기준
고등학교 1학년(공통수학1): data/high1.txt + reports/math-concepts-full.md 기준

각 개념은 고유 ID, 학년, 트랙(연산/개념), 파트(6대 영역), 설명, 선수관계를 포함합니다.
"""

# ──────────────────────────────────────────
# 개념 시드 데이터 구조
# ──────────────────────────────────────────
# {
#   "id": 고유 ID (가이드 문서의 ID 체계 활용),
#   "name": 개념명,
#   "grade": Grade enum 값,
#   "category": "computation" | "concept",
#   "part": "calc" | "algebra" | "func" | "geo" | "data" | "word",
#   "description": 설명,
#   "parent_id": 상위 개념 ID (없으면 None),
#   "prerequisites": [선수 개념 ID 목록],
# }


# =============================================
# 초등학교 4학년 (elementary_4)
# =============================================

ELEMENTARY_4_CONCEPTS = [
    # ── 수와 연산 (NUM) ──
    {
        "id": "E4-NUM-01",
        "name": "만 단위 이해",
        "grade": "elementary_4",
        "category": "concept",
        "part": "calc",
        "description": "10,000 = 천의 10배. 네 자리씩 끊어 읽기 (조, 억, 만)",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "E4-NUM-02",
        "name": "억 단위 이해",
        "grade": "elementary_4",
        "category": "concept",
        "part": "calc",
        "description": "100,000,000 = 만의 만 배. 숫자 읽기/쓰기",
        "parent_id": "E4-NUM-01",
        "prerequisites": ["E4-NUM-01"],
    },
    {
        "id": "E4-NUM-03",
        "name": "조 단위 이해",
        "grade": "elementary_4",
        "category": "concept",
        "part": "calc",
        "description": "1,000,000,000,000 = 억의 만 배. 단위 변환",
        "parent_id": "E4-NUM-02",
        "prerequisites": ["E4-NUM-02"],
    },
    {
        "id": "E4-NUM-04",
        "name": "큰 수 비교",
        "grade": "elementary_4",
        "category": "concept",
        "part": "calc",
        "description": "자릿수 비교, 같은 자릿수면 높은 자리부터 비교",
        "parent_id": "E4-NUM-01",
        "prerequisites": ["E4-NUM-01"],
    },
    {
        "id": "E4-NUM-05",
        "name": "세 자리 × 두 자리 곱셈",
        "grade": "elementary_4",
        "category": "computation",
        "part": "calc",
        "description": "각 자리 곱셈 후 합산. 282 × 20 = 5,640",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "E4-NUM-06",
        "name": "세 자리 ÷ 두 자리 나눗셈",
        "grade": "elementary_4",
        "category": "computation",
        "part": "calc",
        "description": "어림 → 곱하기 확인 → 나머지. 281 ÷ 50 = 5...31",
        "parent_id": None,
        "prerequisites": ["E4-NUM-05"],
    },
    {
        "id": "E4-NUM-07",
        "name": "동분모 분수 덧셈",
        "grade": "elementary_4",
        "category": "computation",
        "part": "calc",
        "description": "a/n + b/n = (a+b)/n. 분모는 그대로, 분자끼리 더함",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "E4-NUM-08",
        "name": "동분모 분수 뺄셈",
        "grade": "elementary_4",
        "category": "computation",
        "part": "calc",
        "description": "a/n - b/n = (a-b)/n. 1에서 분수 빼기 포함",
        "parent_id": "E4-NUM-07",
        "prerequisites": ["E4-NUM-07"],
    },
    {
        "id": "E4-NUM-09",
        "name": "1에서 분수 빼기",
        "grade": "elementary_4",
        "category": "computation",
        "part": "calc",
        "description": "1 = n/n으로 변환 후 뺄셈. 1 - 1/9 = 8/9",
        "parent_id": "E4-NUM-08",
        "prerequisites": ["E4-NUM-08"],
    },
    {
        "id": "E4-NUM-10",
        "name": "대분수 연산 (동분모)",
        "grade": "elementary_4",
        "category": "computation",
        "part": "calc",
        "description": "가분수로 변환 후 계산. 받아올림/받아내림 처리",
        "parent_id": "E4-NUM-07",
        "prerequisites": ["E4-NUM-07", "E4-NUM-08"],
    },
    {
        "id": "E4-NUM-11",
        "name": "소수 덧셈",
        "grade": "elementary_4",
        "category": "computation",
        "part": "calc",
        "description": "소수점 세로 정렬 후 자연수처럼 계산. 2.35 + 1.48 = 3.83",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "E4-NUM-12",
        "name": "소수 뺄셈",
        "grade": "elementary_4",
        "category": "computation",
        "part": "calc",
        "description": "빈 자리 0 채우기. 5.2 - 2.75 = 2.45",
        "parent_id": "E4-NUM-11",
        "prerequisites": ["E4-NUM-11"],
    },

    # ── 도형과 측정 (GEO) ──
    {
        "id": "E4-GEO-01",
        "name": "예각",
        "grade": "elementary_4",
        "category": "concept",
        "part": "geo",
        "description": "직각보다 작은 각. 0° < θ < 90°",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "E4-GEO-02",
        "name": "직각",
        "grade": "elementary_4",
        "category": "concept",
        "part": "geo",
        "description": "정확히 90°",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "E4-GEO-03",
        "name": "둔각",
        "grade": "elementary_4",
        "category": "concept",
        "part": "geo",
        "description": "직각보다 큰 각. 90° < θ < 180°",
        "parent_id": None,
        "prerequisites": ["E4-GEO-02"],
    },
    {
        "id": "E4-GEO-04",
        "name": "삼각형 분류 (변)",
        "grade": "elementary_4",
        "category": "concept",
        "part": "geo",
        "description": "이등변삼각형: 두 변 같음(두 밑각 같음). 정삼각형: 세 변 같음(세 각 60°)",
        "parent_id": None,
        "prerequisites": ["E4-GEO-01", "E4-GEO-02", "E4-GEO-03"],
    },
    {
        "id": "E4-GEO-05",
        "name": "삼각형 분류 (각)",
        "grade": "elementary_4",
        "category": "concept",
        "part": "geo",
        "description": "예각삼각형: 세 각 모두 예각. 직각삼각형: 한 각 직각. 둔각삼각형: 한 각 둔각",
        "parent_id": "E4-GEO-04",
        "prerequisites": ["E4-GEO-01", "E4-GEO-02", "E4-GEO-03"],
    },
    {
        "id": "E4-GEO-06",
        "name": "사각형 분류와 포함관계",
        "grade": "elementary_4",
        "category": "concept",
        "part": "geo",
        "description": "사각형 ⊃ 사다리꼴 ⊃ 평행사변형 ⊃ 마름모/직사각형 ⊃ 정사각형. 정사각형은 마름모이자 직사각형",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "E4-GEO-07",
        "name": "다각형과 대각선",
        "grade": "elementary_4",
        "category": "concept",
        "part": "geo",
        "description": "한 꼭짓점에서 대각선: n-3. 전체 대각선: n(n-3)÷2",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "E4-GEO-08",
        "name": "평면도형의 이동",
        "grade": "elementary_4",
        "category": "concept",
        "part": "geo",
        "description": "밀기(평행이동), 뒤집기(대칭이동), 돌리기(회전이동)",
        "parent_id": None,
        "prerequisites": [],
    },

    # ── 자료와 가능성 (STA) ──
    {
        "id": "E4-STA-01",
        "name": "막대그래프",
        "grade": "elementary_4",
        "category": "concept",
        "part": "data",
        "description": "크기 비교에 적합. 좋아하는 과목별 인원 등",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "E4-STA-02",
        "name": "꺾은선그래프",
        "grade": "elementary_4",
        "category": "concept",
        "part": "data",
        "description": "변화 추세에 적합. 시간에 따른 온도/키/인구 변화. 물결선(≈) 활용",
        "parent_id": None,
        "prerequisites": ["E4-STA-01"],
    },

    # ── 변화와 관계 (ALG) ──
    {
        "id": "E4-ALG-01",
        "name": "규칙 찾기",
        "grade": "elementary_4",
        "category": "concept",
        "part": "algebra",
        "description": "수/도형 배열 패턴. 계산식 규칙 (1+2+3+2+1 = 3²)",
        "parent_id": None,
        "prerequisites": [],
    },
]


# =============================================
# 초등학교 5학년 (elementary_5)
# =============================================

ELEMENTARY_5_CONCEPTS = [
    # ── 수와 연산 (NUM) ──
    {
        "id": "E5-NUM-01",
        "name": "약수",
        "grade": "elementary_5",
        "category": "concept",
        "part": "calc",
        "description": "어떤 수를 나누어떨어지게 하는 수. 12의 약수: 1,2,3,4,6,12",
        "parent_id": None,
        "prerequisites": ["E4-NUM-06"],
    },
    {
        "id": "E5-NUM-02",
        "name": "배수",
        "grade": "elementary_5",
        "category": "concept",
        "part": "calc",
        "description": "어떤 수를 1배, 2배, 3배... 한 수. 3의 배수: 3,6,9,12,...",
        "parent_id": None,
        "prerequisites": ["E4-NUM-05"],
    },
    {
        "id": "E5-NUM-03",
        "name": "공약수와 최대공약수 (GCD)",
        "grade": "elementary_5",
        "category": "computation",
        "part": "calc",
        "description": "두 수의 공통된 약수 중 가장 큰 수. 거꾸로 나눗셈 방법",
        "parent_id": "E5-NUM-01",
        "prerequisites": ["E5-NUM-01"],
    },
    {
        "id": "E5-NUM-04",
        "name": "공배수와 최소공배수 (LCM)",
        "grade": "elementary_5",
        "category": "computation",
        "part": "calc",
        "description": "두 수의 공통된 배수 중 가장 작은 수. 공배수 = 최소공배수의 배수",
        "parent_id": "E5-NUM-02",
        "prerequisites": ["E5-NUM-02", "E5-NUM-03"],
    },
    {
        "id": "E5-NUM-05",
        "name": "약분과 기약분수",
        "grade": "elementary_5",
        "category": "computation",
        "part": "calc",
        "description": "분모·분자를 공약수로 나눔. 기약분수: 더 이상 약분 불가",
        "parent_id": "E5-NUM-03",
        "prerequisites": ["E5-NUM-03"],
    },
    {
        "id": "E5-NUM-06",
        "name": "통분",
        "grade": "elementary_5",
        "category": "computation",
        "part": "calc",
        "description": "분모를 같게 만듦. 두 분모의 최소공배수 이용",
        "parent_id": "E5-NUM-04",
        "prerequisites": ["E5-NUM-04"],
    },
    {
        "id": "E5-NUM-07",
        "name": "혼합 계산 (연산 순서)",
        "grade": "elementary_5",
        "category": "computation",
        "part": "calc",
        "description": "괄호 → 곱셈/나눗셈 → 덧셈/뺄셈. 좌결합성",
        "parent_id": None,
        "prerequisites": ["E4-NUM-05", "E4-NUM-06"],
    },
    {
        "id": "E5-NUM-08",
        "name": "이분모 분수 덧셈",
        "grade": "elementary_5",
        "category": "computation",
        "part": "calc",
        "description": "통분 후 분자끼리 더함. 1/2 + 1/3 = 3/6 + 2/6 = 5/6",
        "parent_id": "E5-NUM-06",
        "prerequisites": ["E5-NUM-06", "E4-NUM-07"],
    },
    {
        "id": "E5-NUM-09",
        "name": "이분모 분수 뺄셈",
        "grade": "elementary_5",
        "category": "computation",
        "part": "calc",
        "description": "통분 후 분자끼리 뺌. 3/4 - 1/3 = 9/12 - 4/12 = 5/12",
        "parent_id": "E5-NUM-08",
        "prerequisites": ["E5-NUM-06", "E4-NUM-08"],
    },
    {
        "id": "E5-NUM-10",
        "name": "대분수 연산 (이분모)",
        "grade": "elementary_5",
        "category": "computation",
        "part": "calc",
        "description": "받아올림/받아내림 처리. 2³⁄₄ + 1²⁄₃ = 4⁵⁄₁₂",
        "parent_id": "E5-NUM-08",
        "prerequisites": ["E5-NUM-08", "E5-NUM-09", "E4-NUM-10"],
    },
    {
        "id": "E5-NUM-11",
        "name": "수의 범위 (이상/이하/초과/미만)",
        "grade": "elementary_5",
        "category": "concept",
        "part": "calc",
        "description": "이상(≥)/이하(≤): 경계값 포함. 초과(>)/미만(<): 경계값 불포함",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "E5-NUM-12",
        "name": "어림하기 (올림/버림/반올림)",
        "grade": "elementary_5",
        "category": "computation",
        "part": "calc",
        "description": "올림: 아랫자리 0이 아니면 윗자리+1. 버림: 아랫자리 0. 반올림: 0~4 버림, 5~9 올림",
        "parent_id": "E5-NUM-11",
        "prerequisites": ["E5-NUM-11"],
    },
    {
        "id": "E5-NUM-13",
        "name": "분수의 곱셈",
        "grade": "elementary_5",
        "category": "computation",
        "part": "calc",
        "description": "(분수)×(자연수), (자연수)×(분수), (분수)×(분수). 분자끼리·분모끼리 곱함",
        "parent_id": None,
        "prerequisites": ["E5-NUM-05"],
    },
    {
        "id": "E5-NUM-14",
        "name": "소수의 곱셈",
        "grade": "elementary_5",
        "category": "computation",
        "part": "calc",
        "description": "소수점 아래 자릿수의 합만큼 이동. 0.2 × 0.3 = 0.06",
        "parent_id": None,
        "prerequisites": ["E4-NUM-11"],
    },
    {
        "id": "E5-NUM-15",
        "name": "평균",
        "grade": "elementary_5",
        "category": "concept",
        "part": "data",
        "description": "평균 = 모든 값의 합 ÷ 자료의 개수",
        "parent_id": None,
        "prerequisites": ["E5-NUM-07"],
    },
    {
        "id": "E5-NUM-16",
        "name": "가능성 (확률 기초)",
        "grade": "elementary_5",
        "category": "concept",
        "part": "data",
        "description": "불가능(0), 반반(1/2), 확실(1)로 수치화",
        "parent_id": None,
        "prerequisites": [],
    },

    # ── 도형과 측정 (GEO) ──
    {
        "id": "E5-GEO-01",
        "name": "다각형의 둘레",
        "grade": "elementary_5",
        "category": "concept",
        "part": "geo",
        "description": "정다각형: 한 변 × 변의 수. 직사각형: (가로+세로)×2",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "E5-GEO-02",
        "name": "직사각형/평행사변형 넓이",
        "grade": "elementary_5",
        "category": "concept",
        "part": "geo",
        "description": "직사각형: 가로×세로. 평행사변형: 밑변×높이 (등적변형)",
        "parent_id": "E5-GEO-01",
        "prerequisites": ["E5-GEO-01"],
    },
    {
        "id": "E5-GEO-03",
        "name": "삼각형 넓이",
        "grade": "elementary_5",
        "category": "concept",
        "part": "geo",
        "description": "밑변 × 높이 ÷ 2. 2개 붙이면 평행사변형",
        "parent_id": "E5-GEO-02",
        "prerequisites": ["E5-GEO-02"],
    },
    {
        "id": "E5-GEO-04",
        "name": "마름모/사다리꼴 넓이",
        "grade": "elementary_5",
        "category": "concept",
        "part": "geo",
        "description": "마름모: 대각선×대각선÷2. 사다리꼴: (윗변+아랫변)×높이÷2",
        "parent_id": "E5-GEO-03",
        "prerequisites": ["E5-GEO-03"],
    },
    {
        "id": "E5-GEO-05",
        "name": "합동",
        "grade": "elementary_5",
        "category": "concept",
        "part": "geo",
        "description": "모양과 크기가 같아 완전히 겹쳐지는 관계. 대응변 길이·대응각 크기 같음",
        "parent_id": None,
        "prerequisites": ["E4-GEO-04"],
    },
    {
        "id": "E5-GEO-06",
        "name": "선대칭과 점대칭",
        "grade": "elementary_5",
        "category": "concept",
        "part": "geo",
        "description": "선대칭: 대칭축 기준 접으면 겹침. 점대칭: 중심점 기준 180° 회전시 겹침",
        "parent_id": "E5-GEO-05",
        "prerequisites": ["E5-GEO-05", "E4-GEO-08"],
    },
    {
        "id": "E5-GEO-07",
        "name": "직육면체와 정육면체",
        "grade": "elementary_5",
        "category": "concept",
        "part": "geo",
        "description": "면 6개, 모서리 12개, 꼭짓점 8개. 오일러 공식: V-E+F=2. 겨냥도/전개도",
        "parent_id": None,
        "prerequisites": ["E4-GEO-06"],
    },

    # ── 변화와 관계 (ALG) ──
    {
        "id": "E5-ALG-01",
        "name": "규칙과 대응",
        "grade": "elementary_5",
        "category": "concept",
        "part": "algebra",
        "description": "대응 관계: 한 양이 변하면 다른 양도 규칙적으로 변함. ○, △ 기호 사용. 함수적 사고 기초",
        "parent_id": "E4-ALG-01",
        "prerequisites": ["E4-ALG-01"],
    },
]


# =============================================
# 초등학교 6학년 (elementary_6)
# =============================================

ELEMENTARY_6_CONCEPTS = [
    # ── 수와 연산 (NUM) ──
    {
        "id": "E6-NUM-01",
        "name": "자연수÷자연수→분수",
        "grade": "elementary_6",
        "category": "computation",
        "part": "calc",
        "description": "a ÷ b = a/b. 3 ÷ 7 = 3/7",
        "parent_id": None,
        "prerequisites": ["E5-NUM-05"],
    },
    {
        "id": "E6-NUM-02",
        "name": "분수÷자연수",
        "grade": "elementary_6",
        "category": "computation",
        "part": "calc",
        "description": "a/b ÷ c = a/(b×c). 6/7 ÷ 2 = 3/7",
        "parent_id": "E6-NUM-01",
        "prerequisites": ["E6-NUM-01", "E5-NUM-13"],
    },
    {
        "id": "E6-NUM-03",
        "name": "분수÷분수 (역수 곱셈)",
        "grade": "elementary_6",
        "category": "computation",
        "part": "calc",
        "description": "a/b ÷ c/d = a/b × d/c. 역수를 곱하는 원리 이해 필수",
        "parent_id": "E6-NUM-02",
        "prerequisites": ["E6-NUM-02", "E5-NUM-13"],
    },
    {
        "id": "E6-NUM-04",
        "name": "소수÷자연수",
        "grade": "elementary_6",
        "category": "computation",
        "part": "calc",
        "description": "몫의 소수점 위치 확인. 2.46 ÷ 3 = 0.82",
        "parent_id": None,
        "prerequisites": ["E5-NUM-14"],
    },
    {
        "id": "E6-NUM-05",
        "name": "소수÷소수",
        "grade": "elementary_6",
        "category": "computation",
        "part": "calc",
        "description": "소수점 동시 이동. 3.25 ÷ 0.5 = 6.5. 나머지의 소수점은 원래 위치",
        "parent_id": "E6-NUM-04",
        "prerequisites": ["E6-NUM-04"],
    },

    # ── 변화와 관계 (ALG) - 비와 비율 ──
    {
        "id": "E6-ALG-01",
        "name": "비와 비율",
        "grade": "elementary_6",
        "category": "concept",
        "part": "algebra",
        "description": "비(a:b): 두 양의 상대적 크기 비교. 비율 = 비교하는양 ÷ 기준량",
        "parent_id": None,
        "prerequisites": ["E5-NUM-05"],
    },
    {
        "id": "E6-ALG-02",
        "name": "백분율",
        "grade": "elementary_6",
        "category": "concept",
        "part": "algebra",
        "description": "기준량을 100으로 환산. 비율 × 100%",
        "parent_id": "E6-ALG-01",
        "prerequisites": ["E6-ALG-01"],
    },
    {
        "id": "E6-ALG-03",
        "name": "비례식",
        "grade": "elementary_6",
        "category": "computation",
        "part": "algebra",
        "description": "a:b = c:d ⟺ ad = bc. 외항의 곱 = 내항의 곱",
        "parent_id": "E6-ALG-01",
        "prerequisites": ["E6-ALG-01"],
    },
    {
        "id": "E6-ALG-04",
        "name": "비례배분",
        "grade": "elementary_6",
        "category": "computation",
        "part": "algebra",
        "description": "A의 몫 = 전체 × A/(A+B). 전체를 비율로 분할",
        "parent_id": "E6-ALG-03",
        "prerequisites": ["E6-ALG-03"],
    },

    # ── 도형과 측정 (GEO) ──
    {
        "id": "E6-GEO-01",
        "name": "각기둥과 각뿔",
        "grade": "elementary_6",
        "category": "concept",
        "part": "geo",
        "description": "n각기둥: 면 n+2, 꼭짓점 2n, 모서리 3n. n각뿔: 면 n+1, 꼭짓점 n+1, 모서리 2n",
        "parent_id": "E5-GEO-07",
        "prerequisites": ["E5-GEO-07"],
    },
    {
        "id": "E6-GEO-02",
        "name": "직육면체의 부피와 겉넓이",
        "grade": "elementary_6",
        "category": "computation",
        "part": "geo",
        "description": "부피 V = abc. 겉넓이 S = 2(ab+bc+ca). 1m³ = 1,000,000cm³",
        "parent_id": "E5-GEO-07",
        "prerequisites": ["E5-GEO-07", "E5-GEO-02"],
    },
    {
        "id": "E6-GEO-03",
        "name": "원주와 원주율",
        "grade": "elementary_6",
        "category": "concept",
        "part": "geo",
        "description": "원주율 π ≈ 3.14. 원주(둘레) = 2πr = πd",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "E6-GEO-04",
        "name": "원의 넓이",
        "grade": "elementary_6",
        "category": "computation",
        "part": "geo",
        "description": "πr². 유도: 원을 잘게 잘라 직사각형으로 등적변형 (가로=πr, 세로=r)",
        "parent_id": "E6-GEO-03",
        "prerequisites": ["E6-GEO-03", "E5-GEO-02"],
    },
    {
        "id": "E6-GEO-05",
        "name": "원기둥·원뿔·구 (회전체)",
        "grade": "elementary_6",
        "category": "concept",
        "part": "geo",
        "description": "직사각형→원기둥. 직각삼각형→원뿔. 반원→구. 원기둥 겉넓이 = 2πr²+2πrh",
        "parent_id": "E6-GEO-04",
        "prerequisites": ["E6-GEO-04", "E6-GEO-01"],
    },

    # ── 자료와 가능성 (STA) ──
    {
        "id": "E6-STA-01",
        "name": "띠그래프와 원그래프",
        "grade": "elementary_6",
        "category": "concept",
        "part": "data",
        "description": "전체를 100%로 표현. 띠(길이), 원(면적). 비율의 구조 파악",
        "parent_id": "E4-STA-02",
        "prerequisites": ["E4-STA-02", "E6-ALG-02"],
    },

    # ── 공간과 입체 ──
    {
        "id": "E6-GEO-06",
        "name": "쌓기나무와 투영도",
        "grade": "elementary_6",
        "category": "concept",
        "part": "geo",
        "description": "위/앞/옆에서 본 모양. 3차원→2차원 압축. 최소/최대 개수 추론",
        "parent_id": "E5-GEO-07",
        "prerequisites": ["E5-GEO-07"],
    },
]


# =============================================
# 중학교 1학년 (middle_1)
# =============================================

MIDDLE_1_CONCEPTS = [
    # ── 수와 연산 ──
    {
        "id": "M1-NUM-01",
        "name": "소인수분해",
        "grade": "middle_1",
        "category": "computation",
        "part": "calc",
        "description": "소수·합성수, 거듭제곱, 소인수분해. 약수의 개수=(a+1)(b+1)",
        "parent_id": None,
        "prerequisites": ["E5-NUM-01", "E5-NUM-03"],
    },
    {
        "id": "M1-NUM-02",
        "name": "최대공약수·최소공배수 (소인수분해)",
        "grade": "middle_1",
        "category": "computation",
        "part": "calc",
        "description": "GCD: 공통 소인수의 최소 지수 곱. LCM: 모든 소인수의 최대 지수 곱",
        "parent_id": "M1-NUM-01",
        "prerequisites": ["M1-NUM-01", "E5-NUM-03", "E5-NUM-04"],
    },
    {
        "id": "M1-NUM-03",
        "name": "정수와 유리수",
        "grade": "middle_1",
        "category": "concept",
        "part": "calc",
        "description": "양의 정수, 0, 음의 정수. 유리수 = a/b (b≠0). 절댓값 = 원점으로부터 거리",
        "parent_id": None,
        "prerequisites": ["E6-NUM-03"],
    },
    {
        "id": "M1-NUM-04",
        "name": "정수·유리수 사칙연산",
        "grade": "middle_1",
        "category": "computation",
        "part": "calc",
        "description": "부호 규칙, 역수, 혼합 계산. (+)×(-)=(-), (-)×(-)=(+)",
        "parent_id": "M1-NUM-03",
        "prerequisites": ["M1-NUM-03", "E5-NUM-07"],
    },

    # ── 문자와 식 ──
    {
        "id": "M1-ALG-01",
        "name": "문자와 식",
        "grade": "middle_1",
        "category": "concept",
        "part": "algebra",
        "description": "문자 사용 규칙, 곱셈 기호 생략, 식의 값, 동류항, 일차식 계산",
        "parent_id": None,
        "prerequisites": ["E5-ALG-01", "M1-NUM-04"],
    },
    {
        "id": "M1-ALG-02",
        "name": "일차방정식",
        "grade": "middle_1",
        "category": "computation",
        "part": "algebra",
        "description": "등식의 성질, ax+b=0, 이항. 실생활 모델링 문제",
        "parent_id": "M1-ALG-01",
        "prerequisites": ["M1-ALG-01"],
    },

    # ── 좌표와 그래프 ──
    {
        "id": "M1-FUNC-01",
        "name": "좌표평면과 그래프",
        "grade": "middle_1",
        "category": "concept",
        "part": "func",
        "description": "순서쌍 (x,y), 사분면. 정비례 y=ax, 반비례 y=a/x",
        "parent_id": None,
        "prerequisites": ["E5-ALG-01"],
    },

    # ── 도형 ──
    {
        "id": "M1-GEO-01",
        "name": "기본 도형과 작도",
        "grade": "middle_1",
        "category": "concept",
        "part": "geo",
        "description": "점, 선, 면, 각. 수직이등분선, 각의 이등분선 작도",
        "parent_id": None,
        "prerequisites": ["E4-GEO-02"],
    },
    {
        "id": "M1-GEO-02",
        "name": "삼각형의 성질과 합동조건",
        "grade": "middle_1",
        "category": "concept",
        "part": "geo",
        "description": "SSS, SAS, ASA 합동. 삼각형 내각의 합 = 180°",
        "parent_id": "M1-GEO-01",
        "prerequisites": ["M1-GEO-01", "E5-GEO-05"],
    },
    {
        "id": "M1-GEO-03",
        "name": "평면도형의 성질",
        "grade": "middle_1",
        "category": "concept",
        "part": "geo",
        "description": "다각형 내각·외각의 합. n각형 내각합 = 180°×(n-2)",
        "parent_id": "M1-GEO-02",
        "prerequisites": ["M1-GEO-02", "E4-GEO-07"],
    },

    # ── 통계 ──
    {
        "id": "M1-STA-01",
        "name": "자료의 정리와 해석",
        "grade": "middle_1",
        "category": "concept",
        "part": "data",
        "description": "줄기와 잎 그림, 도수분포표, 히스토그램, 도수분포다각형, 상대도수",
        "parent_id": None,
        "prerequisites": ["E6-STA-01", "E5-NUM-15"],
    },
]


# =============================================
# 중학교 2학년 (middle_2)
# =============================================

MIDDLE_2_CONCEPTS = [
    # ── 수와 연산 ──
    {
        "id": "M2-NUM-01",
        "name": "유리수와 순환소수",
        "grade": "middle_2",
        "category": "concept",
        "part": "calc",
        "description": "순환소수 표현, 순환소수↔분수 변환",
        "parent_id": "M1-NUM-03",
        "prerequisites": ["M1-NUM-03", "M1-NUM-04"],
    },

    # ── 식의 계산 ──
    {
        "id": "M2-ALG-01",
        "name": "지수법칙과 단항식 계산",
        "grade": "middle_2",
        "category": "computation",
        "part": "algebra",
        "description": "a^m × a^n = a^(m+n), (a^m)^n = a^(mn), (ab)^n = a^n·b^n",
        "parent_id": "M1-ALG-01",
        "prerequisites": ["M1-ALG-01", "M1-NUM-01"],
    },
    {
        "id": "M2-ALG-02",
        "name": "다항식의 덧셈·뺄셈·곱셈",
        "grade": "middle_2",
        "category": "computation",
        "part": "algebra",
        "description": "동류항 정리, 분배법칙, 다항식×단항식",
        "parent_id": "M2-ALG-01",
        "prerequisites": ["M2-ALG-01"],
    },

    # ── 부등식·방정식 ──
    {
        "id": "M2-ALG-03",
        "name": "일차부등식",
        "grade": "middle_2",
        "category": "computation",
        "part": "algebra",
        "description": "부등식의 성질, ax+b>0 풀이. 음수 곱/나누면 부등호 방향 바뀜",
        "parent_id": "M1-ALG-02",
        "prerequisites": ["M1-ALG-02"],
    },
    {
        "id": "M2-ALG-04",
        "name": "연립방정식",
        "grade": "middle_2",
        "category": "computation",
        "part": "algebra",
        "description": "가감법, 대입법. 미지수 2개 일차방정식 체계",
        "parent_id": "M1-ALG-02",
        "prerequisites": ["M1-ALG-02", "M2-ALG-03"],
    },

    # ── 함수 ──
    {
        "id": "M2-FUNC-01",
        "name": "일차함수",
        "grade": "middle_2",
        "category": "concept",
        "part": "func",
        "description": "y=ax+b, 기울기와 y절편. 그래프의 평행·일치. 연립방정식과 관계",
        "parent_id": "M1-FUNC-01",
        "prerequisites": ["M1-FUNC-01", "M1-ALG-02"],
    },

    # ── 도형 ──
    {
        "id": "M2-GEO-01",
        "name": "삼각형·사각형의 성질",
        "grade": "middle_2",
        "category": "concept",
        "part": "geo",
        "description": "이등변삼각형, 직각삼각형 성질. 평행사변형 조건",
        "parent_id": "M1-GEO-02",
        "prerequisites": ["M1-GEO-02"],
    },
    {
        "id": "M2-GEO-02",
        "name": "닮음과 피타고라스 정리",
        "grade": "middle_2",
        "category": "concept",
        "part": "geo",
        "description": "닮음비, AA/SAS/SSS 닮음. a²+b²=c²",
        "parent_id": "M2-GEO-01",
        "prerequisites": ["M2-GEO-01"],
    },

    # ── 확률 ──
    {
        "id": "M2-STA-01",
        "name": "경우의 수와 확률",
        "grade": "middle_2",
        "category": "concept",
        "part": "data",
        "description": "합의 법칙, 곱의 법칙. 확률의 정의와 성질",
        "parent_id": "M1-STA-01",
        "prerequisites": ["M1-STA-01", "E5-NUM-16"],
    },
]


# =============================================
# 중학교 3학년 (middle_3)
# =============================================

MIDDLE_3_CONCEPTS = [
    # ── 수와 연산 ──
    {
        "id": "M3-NUM-01",
        "name": "제곱근과 실수",
        "grade": "middle_3",
        "category": "concept",
        "part": "calc",
        "description": "제곱근의 뜻, √a 성질. 무리수, 실수의 대소 관계",
        "parent_id": "M1-NUM-03",
        "prerequisites": ["M1-NUM-04", "M2-ALG-01"],
    },
    {
        "id": "M3-NUM-02",
        "name": "근호를 포함한 식의 계산",
        "grade": "middle_3",
        "category": "computation",
        "part": "calc",
        "description": "√a×√b=√(ab), 분모 유리화, 근호 포함 사칙연산",
        "parent_id": "M3-NUM-01",
        "prerequisites": ["M3-NUM-01"],
    },

    # ── 식의 계산 ──
    {
        "id": "M3-ALG-01",
        "name": "다항식의 곱셈과 곱셈공식",
        "grade": "middle_3",
        "category": "computation",
        "part": "algebra",
        "description": "(a+b)²=a²+2ab+b², (a-b)²=a²-2ab+b², (a+b)(a-b)=a²-b²",
        "parent_id": "M2-ALG-02",
        "prerequisites": ["M2-ALG-02"],
    },
    {
        "id": "M3-ALG-02",
        "name": "인수분해",
        "grade": "middle_3",
        "category": "computation",
        "part": "algebra",
        "description": "공통인수, 곱셈공식의 역, x²+(a+b)x+ab=(x+a)(x+b)",
        "parent_id": "M3-ALG-01",
        "prerequisites": ["M3-ALG-01"],
    },
    {
        "id": "M3-ALG-03",
        "name": "이차방정식",
        "grade": "middle_3",
        "category": "computation",
        "part": "algebra",
        "description": "인수분해, 완전제곱식, 근의 공식. x=(-b±√(b²-4ac))/2a",
        "parent_id": "M3-ALG-02",
        "prerequisites": ["M3-ALG-02", "M3-NUM-02"],
    },

    # ── 함수 ──
    {
        "id": "M3-FUNC-01",
        "name": "이차함수",
        "grade": "middle_3",
        "category": "concept",
        "part": "func",
        "description": "y=ax², y=a(x-p)²+q. 꼭짓점, 축, 개형. 최댓값/최솟값",
        "parent_id": "M2-FUNC-01",
        "prerequisites": ["M2-FUNC-01", "M3-ALG-03"],
    },

    # ── 도형 ──
    {
        "id": "M3-GEO-01",
        "name": "삼각비",
        "grade": "middle_3",
        "category": "concept",
        "part": "geo",
        "description": "sin, cos, tan. 특수각(30°,45°,60°) 삼각비값",
        "parent_id": "M2-GEO-02",
        "prerequisites": ["M2-GEO-02"],
    },
    {
        "id": "M3-GEO-02",
        "name": "원의 성질",
        "grade": "middle_3",
        "category": "concept",
        "part": "geo",
        "description": "원주각·중심각, 원에 내접하는 사각형, 접선과 할선",
        "parent_id": "E6-GEO-04",
        "prerequisites": ["E6-GEO-04", "M2-GEO-02"],
    },

    # ── 통계 ──
    {
        "id": "M3-STA-01",
        "name": "대푯값과 산포도",
        "grade": "middle_3",
        "category": "concept",
        "part": "data",
        "description": "평균, 중앙값, 최빈값. 분산, 표준편차",
        "parent_id": "M2-STA-01",
        "prerequisites": ["M2-STA-01", "E5-NUM-15"],
    },
    {
        "id": "M3-STA-02",
        "name": "상관관계",
        "grade": "middle_3",
        "category": "concept",
        "part": "data",
        "description": "산점도, 양의 상관, 음의 상관, 상관 없음",
        "parent_id": "M3-STA-01",
        "prerequisites": ["M3-STA-01", "M1-FUNC-01"],
    },
]


# =============================================
# 고등학교 1학년 - 공통수학1 (high_1)
# data/high1.txt + reports/math-concepts-full.md 기준
# =============================================

HIGH_1_CONCEPTS = [
    # ── 다항식 (ALG) ──
    {
        "id": "H1-ALG-01",
        "name": "다항식 정리와 연산",
        "grade": "high_1",
        "category": "computation",
        "part": "algebra",
        "description": "내림차순 정리, 사칙연산, 곱셈 공식((a±b)³, (a+b+c)²)",
        "parent_id": "M3-ALG-01",
        "prerequisites": ["M3-ALG-01"],
    },
    {
        "id": "H1-ALG-02",
        "name": "다항식의 나눗셈",
        "grade": "high_1",
        "category": "computation",
        "part": "algebra",
        "description": "A=BQ+R, 조립제법(호너의 방법), deg(R)<deg(B)",
        "parent_id": "H1-ALG-01",
        "prerequisites": ["H1-ALG-01"],
    },
    {
        "id": "H1-ALG-03",
        "name": "나머지정리",
        "grade": "high_1",
        "category": "concept",
        "part": "algebra",
        "description": "P(x)를 (x-a)로 나눈 나머지 = P(a)",
        "parent_id": "H1-ALG-02",
        "prerequisites": ["H1-ALG-02"],
    },
    {
        "id": "H1-ALG-04",
        "name": "인수정리",
        "grade": "high_1",
        "category": "concept",
        "part": "algebra",
        "description": "P(a)=0이면 (x-a)는 P(x)의 인수. 고차방정식 해결의 열쇠",
        "parent_id": "H1-ALG-03",
        "prerequisites": ["H1-ALG-03"],
    },
    {
        "id": "H1-ALG-05",
        "name": "인수분해 (고급)",
        "grade": "high_1",
        "category": "computation",
        "part": "algebra",
        "description": "고차식·세제곱(a³±b³) 인수분해, 치환, 복이차식, 대칭식",
        "parent_id": "H1-ALG-04",
        "prerequisites": ["M3-ALG-02", "H1-ALG-04"],
    },

    # ── 방정식 (ALG) ──
    {
        "id": "H1-ALG-06",
        "name": "복소수",
        "grade": "high_1",
        "category": "concept",
        "part": "algebra",
        "description": "i²=-1, a+bi 형태, 실수부·허수부, 복소수의 상등",
        "parent_id": "M3-NUM-02",
        "prerequisites": ["M3-NUM-02"],
    },
    {
        "id": "H1-ALG-07",
        "name": "복소수의 사칙연산",
        "grade": "high_1",
        "category": "computation",
        "part": "algebra",
        "description": "덧뺄셈·곱셈·나눗셈(켤레복소수 이용 분모 실수화)",
        "parent_id": "H1-ALG-06",
        "prerequisites": ["H1-ALG-06"],
    },
    {
        "id": "H1-ALG-08",
        "name": "이차방정식의 판별식",
        "grade": "high_1",
        "category": "concept",
        "part": "algebra",
        "description": "D=b²-4ac, D>0 서로 다른 두 실근, D=0 중근, D<0 두 허근",
        "parent_id": "H1-ALG-06",
        "prerequisites": ["M3-ALG-03", "H1-ALG-06"],
    },
    {
        "id": "H1-ALG-09",
        "name": "근과 계수의 관계",
        "grade": "high_1",
        "category": "concept",
        "part": "algebra",
        "description": "α+β=-b/a, αβ=c/a. 근을 구하지 않고 대칭식 값 계산",
        "parent_id": "H1-ALG-08",
        "prerequisites": ["H1-ALG-08"],
    },
    {
        "id": "H1-ALG-10",
        "name": "고차방정식",
        "grade": "high_1",
        "category": "computation",
        "part": "algebra",
        "description": "삼차·사차 방정식, 인수정리+조립제법으로 차수 낮추기, 상반방정식",
        "parent_id": "H1-ALG-05",
        "prerequisites": ["H1-ALG-05", "H1-ALG-04"],
    },
    {
        "id": "H1-ALG-17",
        "name": "연립이차방정식",
        "grade": "high_1",
        "category": "computation",
        "part": "algebra",
        "description": "일차+이차 연립(대입법), 이차+이차 연립(소거법)",
        "parent_id": "H1-ALG-10",
        "prerequisites": ["H1-ALG-10", "M2-ALG-04"],
    },

    # ── 부등식 (ALG) ──
    {
        "id": "H1-ALG-11",
        "name": "이차부등식",
        "grade": "high_1",
        "category": "computation",
        "part": "algebra",
        "description": "ax²+bx+c>0 풀이(그래프 이용), 절대부등식(D<0)",
        "parent_id": "M2-ALG-03",
        "prerequisites": ["M3-FUNC-01", "M2-ALG-03"],
    },
    {
        "id": "H1-ALG-12",
        "name": "연립부등식",
        "grade": "high_1",
        "category": "computation",
        "part": "algebra",
        "description": "여러 부등식의 공통 해, 수직선 영역 표시",
        "parent_id": "H1-ALG-11",
        "prerequisites": ["H1-ALG-11"],
    },
    {
        "id": "H1-ALG-13",
        "name": "절대값 방정식·부등식",
        "grade": "high_1",
        "category": "computation",
        "part": "algebra",
        "description": "|ax+b|=c, |ax+b|<c, 경우 나누기",
        "parent_id": "M2-ALG-03",
        "prerequisites": ["M2-ALG-03"],
    },

    # ── 이차함수 (FUNC) ──
    {
        "id": "H1-ALG-14",
        "name": "이차함수의 최대·최소",
        "grade": "high_1",
        "category": "concept",
        "part": "func",
        "description": "정의역 제한 시 최대/최소, 꼭짓점과 구간 관계",
        "parent_id": "M3-FUNC-01",
        "prerequisites": ["M3-FUNC-01"],
    },
    {
        "id": "H1-ALG-15",
        "name": "이차함수와 이차방정식",
        "grade": "high_1",
        "category": "concept",
        "part": "func",
        "description": "그래프와 x축의 교점 = 방정식의 근, 판별식의 기하학적 의미",
        "parent_id": "H1-ALG-14",
        "prerequisites": ["H1-ALG-08", "M3-FUNC-01"],
    },
    {
        "id": "H1-ALG-16",
        "name": "이차함수와 이차부등식",
        "grade": "high_1",
        "category": "concept",
        "part": "func",
        "description": "그래프를 이용한 부등식 풀이, x축 위/아래 영역",
        "parent_id": "H1-ALG-15",
        "prerequisites": ["H1-ALG-11", "H1-ALG-15"],
    },

    # ── 집합과 명제 (STA) ──
    {
        "id": "H1-STA-01",
        "name": "집합의 뜻과 표현",
        "grade": "high_1",
        "category": "concept",
        "part": "data",
        "description": "원소, 집합, 원소나열법, 조건제시법, ∈",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "H1-STA-02",
        "name": "부분집합",
        "grade": "high_1",
        "category": "concept",
        "part": "data",
        "description": "부분집합, 진부분집합, 공집합, ⊂/⊃/∅",
        "parent_id": "H1-STA-01",
        "prerequisites": ["H1-STA-01"],
    },
    {
        "id": "H1-STA-03",
        "name": "집합의 연산",
        "grade": "high_1",
        "category": "concept",
        "part": "data",
        "description": "교집합(∩), 합집합(∪), 여집합, 차집합",
        "parent_id": "H1-STA-01",
        "prerequisites": ["H1-STA-01"],
    },
    {
        "id": "H1-STA-04",
        "name": "드모르간 법칙",
        "grade": "high_1",
        "category": "concept",
        "part": "data",
        "description": "(A∪B)ᶜ=Aᶜ∩Bᶜ, (A∩B)ᶜ=Aᶜ∪Bᶜ",
        "parent_id": "H1-STA-03",
        "prerequisites": ["H1-STA-03"],
    },
    {
        "id": "H1-STA-05",
        "name": "명제와 조건",
        "grade": "high_1",
        "category": "concept",
        "part": "data",
        "description": "참/거짓 판별, p→q, 진리집합",
        "parent_id": "H1-STA-01",
        "prerequisites": ["H1-STA-01"],
    },
    {
        "id": "H1-STA-06",
        "name": "역·이·대우",
        "grade": "high_1",
        "category": "concept",
        "part": "data",
        "description": "명제의 역/이/대우 관계, 대우를 이용한 증명",
        "parent_id": "H1-STA-05",
        "prerequisites": ["H1-STA-05"],
    },
    {
        "id": "H1-STA-07",
        "name": "필요조건·충분조건",
        "grade": "high_1",
        "category": "concept",
        "part": "data",
        "description": "p⊂q이면 p는 충분, q는 필요. 필요충분조건",
        "parent_id": "H1-STA-05",
        "prerequisites": ["H1-STA-05", "H1-STA-02"],
    },

    # ── 경우의 수 (STA) ──
    {
        "id": "H1-STA-10",
        "name": "합의 법칙과 곱의 법칙",
        "grade": "high_1",
        "category": "concept",
        "part": "data",
        "description": "배반사건의 합, 연속사건의 곱, 포함-배제 원리, 수형도",
        "parent_id": "M2-STA-01",
        "prerequisites": ["M2-STA-01"],
    },
    {
        "id": "H1-STA-08",
        "name": "순열",
        "grade": "high_1",
        "category": "computation",
        "part": "data",
        "description": "nPr=n!/(n-r)!, 팩토리얼(n!), 0!=1",
        "parent_id": "H1-STA-10",
        "prerequisites": ["H1-STA-10"],
    },
    {
        "id": "H1-STA-09",
        "name": "조합",
        "grade": "high_1",
        "category": "computation",
        "part": "data",
        "description": "nCr=n!/r!(n-r)!, nCr=nC(n-r), 파스칼 삼각형",
        "parent_id": "H1-STA-08",
        "prerequisites": ["H1-STA-08"],
    },
    {
        "id": "H1-STA-11",
        "name": "순열의 활용",
        "grade": "high_1",
        "category": "computation",
        "part": "data",
        "description": "이웃하는 순열(묶음), 이웃하지 않는 순열(칸막이)",
        "parent_id": "H1-STA-08",
        "prerequisites": ["H1-STA-08"],
    },
    {
        "id": "H1-STA-12",
        "name": "조합의 활용",
        "grade": "high_1",
        "category": "computation",
        "part": "data",
        "description": "직선·삼각형·사각형 개수, 분할, 평행사변형(mC2×nC2)",
        "parent_id": "H1-STA-09",
        "prerequisites": ["H1-STA-09"],
    },

    # ── 행렬 (ALG) ──
    {
        "id": "H1-ALG-18",
        "name": "행렬의 뜻과 표현",
        "grade": "high_1",
        "category": "concept",
        "part": "algebra",
        "description": "수를 직사각형 배열, 성분(aᵢⱼ), m×n 행렬, 데이터 구조화",
        "parent_id": None,
        "prerequisites": [],
    },
    {
        "id": "H1-ALG-19",
        "name": "행렬의 덧셈·뺄셈·실수배",
        "grade": "high_1",
        "category": "computation",
        "part": "algebra",
        "description": "같은 위치 성분끼리 연산, 교환·결합법칙 성립, 영행렬",
        "parent_id": "H1-ALG-18",
        "prerequisites": ["H1-ALG-18"],
    },
    {
        "id": "H1-ALG-20",
        "name": "행렬의 곱셈",
        "grade": "high_1",
        "category": "computation",
        "part": "algebra",
        "description": "행과 열의 내적, AB≠BA(비가환성), 영인자 존재",
        "parent_id": "H1-ALG-19",
        "prerequisites": ["H1-ALG-19"],
    },
    {
        "id": "H1-ALG-21",
        "name": "단위행렬",
        "grade": "high_1",
        "category": "concept",
        "part": "algebra",
        "description": "AE=EA=A, 곱셈의 항등원, 모든 행렬과 교환 가능",
        "parent_id": "H1-ALG-20",
        "prerequisites": ["H1-ALG-20"],
    },
    {
        "id": "H1-ALG-22",
        "name": "역행렬",
        "grade": "high_1",
        "category": "concept",
        "part": "algebra",
        "description": "AA⁻¹=E, 2×2 역행렬 공식, ad-bc≠0 존재조건(행렬식)",
        "parent_id": "H1-ALG-21",
        "prerequisites": ["H1-ALG-21"],
    },
    {
        "id": "H1-ALG-23",
        "name": "케일리-해밀턴 정리",
        "grade": "high_1",
        "category": "concept",
        "part": "algebra",
        "description": "A²-(a+d)A+(ad-bc)E=O, 고차식→1차식 환원(심화)",
        "parent_id": "H1-ALG-22",
        "prerequisites": ["H1-ALG-22"],
    },
]


# =============================================
# 전체 개념 목록 + 학년 간 연결 맵
# =============================================

ALL_CONCEPTS = (
    ELEMENTARY_4_CONCEPTS
    + ELEMENTARY_5_CONCEPTS
    + ELEMENTARY_6_CONCEPTS
    + MIDDLE_1_CONCEPTS
    + MIDDLE_2_CONCEPTS
    + MIDDLE_3_CONCEPTS
    + HIGH_1_CONCEPTS
)

# 학년 간 연계 흐름 (가이드 문서 기준)
CROSS_GRADE_CHAINS = {
    "분수 계통": [
        "E4-NUM-07",  # 동분모 분수 덧뺄셈
        "E5-NUM-06",  # 통분
        "E5-NUM-08",  # 이분모 분수 덧뺄셈
        "E5-NUM-13",  # 분수의 곱셈
        "E6-NUM-03",  # 분수÷분수
        "M1-NUM-04",  # 정수·유리수 사칙연산
    ],
    "소수 계통": [
        "E4-NUM-11",  # 소수 덧셈
        "E5-NUM-14",  # 소수의 곱셈
        "E6-NUM-05",  # 소수÷소수
    ],
    "도형 계통": [
        "E4-GEO-01",  # 예각
        "E5-GEO-03",  # 삼각형 넓이
        "E6-GEO-04",  # 원의 넓이
        "M1-GEO-03",  # 평면도형의 성질
        "M2-GEO-02",  # 닮음과 피타고라스
        "M3-GEO-01",  # 삼각비
    ],
    "그래프 계통": [
        "E4-STA-01",  # 막대그래프
        "E4-STA-02",  # 꺾은선그래프
        "E6-STA-01",  # 띠/원그래프
        "M1-STA-01",  # 도수분포표
        "M2-STA-01",  # 확률
        "M3-STA-01",  # 대푯값과 산포도
    ],
    "방정식 계통": [
        "E5-ALG-01",  # 규칙과 대응
        "E6-ALG-03",  # 비례식
        "M1-ALG-02",  # 일차방정식
        "M2-ALG-04",  # 연립방정식
        "M3-ALG-03",  # 이차방정식
        "H1-ALG-08",  # 이차방정식의 판별식
        "H1-ALG-10",  # 고차방정식
        "H1-ALG-17",  # 연립이차방정식
    ],
    "함수 계통": [
        "E4-ALG-01",  # 규칙 찾기
        "E5-ALG-01",  # 규칙과 대응
        "M1-FUNC-01",  # 좌표평면과 그래프
        "M2-FUNC-01",  # 일차함수
        "M3-FUNC-01",  # 이차함수
        "H1-ALG-14",  # 이차함수의 최대·최소
        "H1-ALG-15",  # 이차함수와 이차방정식
    ],
    "다항식·인수분해 계통": [
        "M2-ALG-02",  # 다항식의 덧셈·뺄셈·곱셈
        "M3-ALG-01",  # 다항식의 곱셈과 곱셈공식
        "M3-ALG-02",  # 인수분해
        "H1-ALG-01",  # 다항식 정리와 연산
        "H1-ALG-02",  # 다항식의 나눗셈
        "H1-ALG-03",  # 나머지정리
        "H1-ALG-04",  # 인수정리
        "H1-ALG-05",  # 인수분해 (고급)
    ],
    "부등식 계통": [
        "M2-ALG-03",  # 일차부등식
        "H1-ALG-11",  # 이차부등식
        "H1-ALG-12",  # 연립부등식
        "H1-ALG-13",  # 절대값 방정식·부등식
        "H1-ALG-16",  # 이차함수와 이차부등식
    ],
    "수 체계 계통": [
        "E4-NUM-07",  # 동분모 분수 덧뺄셈
        "M1-NUM-04",  # 정수·유리수 사칙연산
        "M3-NUM-01",  # 제곱근과 실수
        "M3-NUM-02",  # 근호를 포함한 식의 계산
        "H1-ALG-06",  # 복소수
        "H1-ALG-07",  # 복소수의 사칙연산
    ],
    "경우의 수·확률 계통": [
        "M2-STA-01",  # 경우의 수와 확률
        "H1-STA-10",  # 합의 법칙과 곱의 법칙
        "H1-STA-08",  # 순열
        "H1-STA-09",  # 조합
    ],
    "행렬 계통": [
        "H1-ALG-18",  # 행렬의 뜻과 표현
        "H1-ALG-19",  # 행렬의 덧셈·뺄셈·실수배
        "H1-ALG-20",  # 행렬의 곱셈
        "H1-ALG-21",  # 단위행렬
        "H1-ALG-22",  # 역행렬
        "H1-ALG-23",  # 케일리-해밀턴 정리
    ],
}


def get_concept_by_id(concept_id: str) -> dict | None:
    """ID로 개념을 찾습니다."""
    for c in ALL_CONCEPTS:
        if c["id"] == concept_id:
            return c
    return None


def get_concepts_by_grade(grade: str) -> list[dict]:
    """학년별 개념 목록을 반환합니다."""
    return [c for c in ALL_CONCEPTS if c["grade"] == grade]


def get_prerequisite_chain(concept_id: str) -> list[str]:
    """개념의 전체 선수학습 체인을 재귀적으로 반환합니다."""
    visited: set[str] = set()
    chain: list[str] = []

    def _traverse(cid: str) -> None:
        if cid in visited:
            return
        visited.add(cid)
        concept = get_concept_by_id(cid)
        if not concept:
            return
        for prereq_id in concept.get("prerequisites", []):
            _traverse(prereq_id)
            if prereq_id not in chain:
                chain.append(prereq_id)

    _traverse(concept_id)
    return chain
