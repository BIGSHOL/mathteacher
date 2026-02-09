"""PDF 교재(큐브수학 개념 진도북) 기반 전체 개념 매핑.

ID 체계: e{학년}-{학기}-{단원}-{순번:02d}
  예: e3-1-1-01 = 초3, 1학기, 1단원, 개념01

old_ids: 기존 시드/챕터에서 사용하던 ID (마이그레이션용)
"""

# =============================================
# 초등학교 3학년 1학기
# =============================================

E3_S1_CONCEPTS = [
    # ── 1단원: 덧셈과 뺄셈 (6개) ──
    {
        "id": "e3-1-1-01",
        "name": "받아올림이 없는 (세 자리 수)+(세 자리 수)",
        "grade": "elementary_3", "semester": 1, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "각 자리의 합이 10 미만인 세 자리 수 덧셈. 자릿값을 맞추어 세로셈으로 계산하는 기초를 익힌다.",
        "old_ids": ["e3-1-1-1", "concept-e3-add-sub-01"],
    },
    {
        "id": "e3-1-1-02",
        "name": "받아올림이 한 번 있는 (세 자리 수)+(세 자리 수)",
        "grade": "elementary_3", "semester": 1, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "한 자리에서만 합이 10 이상이 되어 윗자리로 1을 올리는 덧셈. 받아올림의 원리를 이해한다.",
        "old_ids": ["e3-1-1-1"],
    },
    {
        "id": "e3-1-1-03",
        "name": "받아올림이 여러 번 있는 (세 자리 수)+(세 자리 수)",
        "grade": "elementary_3", "semester": 1, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "일의 자리와 십의 자리 모두에서 받아올림이 발생하는 덧셈. 연속 받아올림을 정확히 처리한다.",
        "old_ids": ["e3-1-1-1"],
    },
    {
        "id": "e3-1-1-04",
        "name": "받아내림이 없는 (세 자리 수)-(세 자리 수)",
        "grade": "elementary_3", "semester": 1, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "각 자리에서 윗수가 아랫수보다 크거나 같아 빌려올 필요 없는 뺄셈. 세로셈 기초를 익힌다.",
        "old_ids": ["e3-1-1-2", "concept-e3-add-sub-02"],
    },
    {
        "id": "e3-1-1-05",
        "name": "받아내림이 한 번 있는 (세 자리 수)-(세 자리 수)",
        "grade": "elementary_3", "semester": 1, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "한 자리에서 뺄 수 없어 윗자리에서 10을 빌려오는 뺄셈. 받아내림(재구조화) 원리를 이해한다.",
        "old_ids": ["e3-1-1-2"],
    },
    {
        "id": "e3-1-1-06",
        "name": "받아내림이 두 번 있는 (세 자리 수)-(세 자리 수)",
        "grade": "elementary_3", "semester": 1, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "일의 자리와 십의 자리 모두에서 받아내림이 필요한 뺄셈. 연속 받아내림을 정확히 처리한다.",
        "old_ids": ["e3-1-1-2"],
    },

    # ── 2단원: 평면도형 (6개) ──
    {
        "id": "e3-1-2-01",
        "name": "선분, 반직선, 직선",
        "grade": "elementary_3", "semester": 1, "chapter_number": 2,
        "category": "concept", "part": "geo",
        "description": "선분(두 점 사이 가장 짧은 선), 반직선(시작점에서 한 방향으로 끝없이), 직선(양쪽으로 끝없이)의 정의와 차이를 이해한다.",
        "old_ids": ["e3-1-2-1", "concept-e3-plane-01"],
    },
    {
        "id": "e3-1-2-02",
        "name": "각",
        "grade": "elementary_3", "semester": 1, "chapter_number": 2,
        "category": "concept", "part": "geo",
        "description": "한 점에서 그은 두 반직선으로 이루어진 도형. 꼭짓점과 변의 개념, 각의 크기와 변의 길이는 무관함을 안다.",
        "old_ids": ["e3-1-2-2", "concept-e3-plane-02"],
    },
    {
        "id": "e3-1-2-03",
        "name": "직각",
        "grade": "elementary_3", "semester": 1, "chapter_number": 2,
        "category": "concept", "part": "geo",
        "description": "종이를 두 번 접었을 때 생기는 각(90도). 삼각자의 직각 부분으로 직각을 확인하는 방법을 안다.",
        "old_ids": ["e3-1-2-2"],
    },
    {
        "id": "e3-1-2-04",
        "name": "직각삼각형",
        "grade": "elementary_3", "semester": 1, "chapter_number": 2,
        "category": "concept", "part": "geo",
        "description": "세 각 중 하나가 직각인 삼각형. 직각삼각형을 찾고 그릴 수 있다.",
        "old_ids": [],
    },
    {
        "id": "e3-1-2-05",
        "name": "직사각형",
        "grade": "elementary_3", "semester": 1, "chapter_number": 2,
        "category": "concept", "part": "geo",
        "description": "네 각이 모두 직각인 사각형. 직사각형의 성질(마주 보는 변의 길이가 같음)을 이해한다.",
        "old_ids": [],
    },
    {
        "id": "e3-1-2-06",
        "name": "정사각형",
        "grade": "elementary_3", "semester": 1, "chapter_number": 2,
        "category": "concept", "part": "geo",
        "description": "네 각이 모두 직각이고 네 변의 길이가 모두 같은 사각형. 직사각형과의 포함 관계를 이해한다.",
        "old_ids": [],
    },

    # ── 3단원: 나눗셈 (4개) ──
    {
        "id": "e3-1-3-01",
        "name": "똑같이 나누기",
        "grade": "elementary_3", "semester": 1, "chapter_number": 3,
        "category": "computation", "part": "calc",
        "description": "등분제(전체를 몇 명에게 똑같이)와 포함제(몇 개씩 묶으면 몇 묶음) 두 가지 나눗셈의 의미를 이해한다.",
        "old_ids": ["e3-1-3-1", "concept-e3-div1-01"],
    },
    {
        "id": "e3-1-3-02",
        "name": "곱셈과 나눗셈의 관계",
        "grade": "elementary_3", "semester": 1, "chapter_number": 3,
        "category": "computation", "part": "calc",
        "description": "12÷3=4 ↔ 3×4=12와 같이 곱셈과 나눗셈이 역연산 관계임을 이해하고 활용한다.",
        "old_ids": ["e3-1-3-2", "concept-e3-div1-02"],
    },
    {
        "id": "e3-1-3-03",
        "name": "나눗셈의 몫을 곱셈식으로 구하기",
        "grade": "elementary_3", "semester": 1, "chapter_number": 3,
        "category": "computation", "part": "calc",
        "description": "□×3=15에서 □를 구하듯, 곱셈식을 이용하여 나눗셈의 몫을 구하는 방법을 익힌다.",
        "old_ids": ["e3-1-3-2"],
    },
    {
        "id": "e3-1-3-04",
        "name": "나눗셈의 몫을 곱셈구구로 구하기",
        "grade": "elementary_3", "semester": 1, "chapter_number": 3,
        "category": "computation", "part": "calc",
        "description": "구구단을 활용하여 나눗셈의 몫을 빠르게 구한다. 예: 56÷7 → 7단에서 56 찾기 → 몫 8.",
        "old_ids": ["e3-1-3-2"],
    },

    # ── 4단원: 곱셈 (5개) ──
    {
        "id": "e3-1-4-01",
        "name": "(몇십)×(몇)",
        "grade": "elementary_3", "semester": 1, "chapter_number": 4,
        "category": "computation", "part": "calc",
        "description": "20×3=60처럼 십의 자리 수에 한 자리 수를 곱하는 계산. 0을 붙이는 원리를 이해한다.",
        "old_ids": ["e3-1-4-1", "concept-e3-mul1-01"],
    },
    {
        "id": "e3-1-4-02",
        "name": "올림이 없는 (몇십몇)×(몇)",
        "grade": "elementary_3", "semester": 1, "chapter_number": 4,
        "category": "computation", "part": "calc",
        "description": "각 자리 곱이 10 미만인 (몇십몇)×(몇). 십의 자리와 일의 자리를 분리하여 각각 곱한 후 합산한다.",
        "old_ids": ["e3-1-4-1"],
    },
    {
        "id": "e3-1-4-03",
        "name": "십의 자리에서 올림이 있는 (몇십몇)×(몇)",
        "grade": "elementary_3", "semester": 1, "chapter_number": 4,
        "category": "computation", "part": "calc",
        "description": "십의 자리 곱의 결과가 10 이상이 되어 백의 자리로 올림이 발생하는 곱셈.",
        "old_ids": ["e3-1-4-2", "concept-e3-mul1-02"],
    },
    {
        "id": "e3-1-4-04",
        "name": "일의 자리에서 올림이 있는 (몇십몇)×(몇)",
        "grade": "elementary_3", "semester": 1, "chapter_number": 4,
        "category": "computation", "part": "calc",
        "description": "일의 자리 곱의 결과가 10 이상이 되어 십의 자리로 올림이 발생하는 곱셈.",
        "old_ids": ["e3-1-4-2"],
    },
    {
        "id": "e3-1-4-05",
        "name": "올림이 두 번 있는 (몇십몇)×(몇)",
        "grade": "elementary_3", "semester": 1, "chapter_number": 4,
        "category": "computation", "part": "calc",
        "description": "일의 자리와 십의 자리 모두에서 올림이 발생하는 곱셈. 연속 올림을 정확히 처리한다.",
        "old_ids": ["e3-1-4-2"],
    },

    # ── 5단원: 길이와 시간 (6개) ──
    {
        "id": "e3-1-5-01",
        "name": "1 mm보다 작은 단위",
        "grade": "elementary_3", "semester": 1, "chapter_number": 5,
        "category": "concept", "part": "calc",
        "description": "mm 단위를 이해하고, 자의 작은 눈금 1칸이 1mm임을 안다. 10mm=1cm 관계를 이해한다.",
        "old_ids": ["e3-1-5-1", "concept-e3-length-time-01"],
    },
    {
        "id": "e3-1-5-02",
        "name": "1 m보다 큰 단위",
        "grade": "elementary_3", "semester": 1, "chapter_number": 5,
        "category": "concept", "part": "calc",
        "description": "km 단위를 이해한다. 1km=1000m 관계와 km, m를 함께 사용하는 방법을 익힌다.",
        "old_ids": ["e3-1-5-1"],
    },
    {
        "id": "e3-1-5-03",
        "name": "길이와 거리를 어림하고 재어 보기",
        "grade": "elementary_3", "semester": 1, "chapter_number": 5,
        "category": "concept", "part": "calc",
        "description": "실생활에서 길이와 거리를 어림잡고, 적절한 단위(mm, cm, m, km)를 선택하여 측정한다.",
        "old_ids": ["e3-1-5-1"],
    },
    {
        "id": "e3-1-5-04",
        "name": "1분보다 작은 단위",
        "grade": "elementary_3", "semester": 1, "chapter_number": 5,
        "category": "concept", "part": "calc",
        "description": "초 단위를 이해한다. 1분=60초 관계와 시각을 시, 분, 초로 읽는 방법을 익힌다.",
        "old_ids": ["e3-1-5-2", "concept-e3-length-time-02"],
    },
    {
        "id": "e3-1-5-05",
        "name": "시간의 덧셈과 뺄셈",
        "grade": "elementary_3", "semester": 1, "chapter_number": 5,
        "category": "computation", "part": "calc",
        "description": "시간 단위의 덧셈과 뺄셈. 60진법에 따라 초→분, 분→시 받아올림/내림을 처리한다.",
        "old_ids": ["e3-1-5-2"],
    },
    {
        "id": "e3-1-5-06",
        "name": "시간을 이용하여 문제 해결하기",
        "grade": "elementary_3", "semester": 1, "chapter_number": 5,
        "category": "concept", "part": "calc",
        "description": "걸린 시간, 도착 시각, 출발 시각 등 실생활 시간 문제를 해결한다.",
        "old_ids": ["e3-1-5-2"],
    },

    # ── 6단원: 분수와 소수 (8개) ──
    {
        "id": "e3-1-6-01",
        "name": "똑같이 나누기",
        "grade": "elementary_3", "semester": 1, "chapter_number": 6,
        "category": "concept", "part": "calc",
        "description": "전체를 '똑같이' 나누는 것의 의미. 균등 분할이 분수 개념의 기초임을 이해한다.",
        "old_ids": ["e3-1-6-1", "concept-e3-frac-dec-01"],
    },
    {
        "id": "e3-1-6-02",
        "name": "분수",
        "grade": "elementary_3", "semester": 1, "chapter_number": 6,
        "category": "concept", "part": "calc",
        "description": "분수의 정의(전체를 똑같이 n등분한 것 중 m개 → m/n). 분자, 분모의 의미를 이해한다.",
        "old_ids": ["e3-1-6-1"],
    },
    {
        "id": "e3-1-6-03",
        "name": "분수로 나타내기",
        "grade": "elementary_3", "semester": 1, "chapter_number": 6,
        "category": "concept", "part": "calc",
        "description": "색칠한 부분, 전체 중 일부를 분수로 나타내는 연습. 그림과 분수의 대응을 이해한다.",
        "old_ids": ["e3-1-6-1"],
    },
    {
        "id": "e3-1-6-04",
        "name": "단위분수의 크기 비교",
        "grade": "elementary_3", "semester": 1, "chapter_number": 6,
        "category": "concept", "part": "calc",
        "description": "분자가 1인 분수(단위분수)끼리 비교. 분모가 클수록 단위분수는 작아짐(1/3 > 1/5)을 이해한다.",
        "old_ids": ["e3-1-6-1"],
    },
    {
        "id": "e3-1-6-05",
        "name": "분모가 같은 분수의 크기 비교",
        "grade": "elementary_3", "semester": 1, "chapter_number": 6,
        "category": "concept", "part": "calc",
        "description": "동분모 분수의 크기 비교. 분모가 같으면 분자가 클수록 큰 분수(2/5 < 3/5)임을 이해한다.",
        "old_ids": ["e3-1-6-1"],
    },
    {
        "id": "e3-1-6-06",
        "name": "1보다 작은 소수",
        "grade": "elementary_3", "semester": 1, "chapter_number": 6,
        "category": "concept", "part": "calc",
        "description": "소수 도입. 1/10=0.1 관계를 이해하고, 0.1~0.9까지 소수를 수직선 위에 나타낸다.",
        "old_ids": ["e3-1-6-2", "concept-e3-frac-dec-02"],
    },
    {
        "id": "e3-1-6-07",
        "name": "1보다 큰 소수",
        "grade": "elementary_3", "semester": 1, "chapter_number": 6,
        "category": "concept", "part": "calc",
        "description": "1.1, 2.5 등 자연수 부분이 있는 소수. 소수점 왼쪽은 자연수, 오른쪽은 소수 부분임을 이해한다.",
        "old_ids": ["e3-1-6-2"],
    },
    {
        "id": "e3-1-6-08",
        "name": "소수의 크기 비교",
        "grade": "elementary_3", "semester": 1, "chapter_number": 6,
        "category": "concept", "part": "calc",
        "description": "소수끼리 크기를 비교한다. 자연수 부분 먼저 비교, 같으면 소수 부분을 비교하는 방법을 익힌다.",
        "old_ids": ["e3-1-6-2"],
    },
]

# =============================================
# 초등학교 3학년 2학기
# =============================================

E3_S2_CONCEPTS = [
    # ── 1단원: 곱셈 (7개) ──
    {
        "id": "e3-2-1-01",
        "name": "올림이 없는 (세 자리 수)×(한 자리 수)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "각 자리 곱이 10 미만인 (세 자리 수)×(한 자리 수). 세로셈으로 백·십·일의 자리를 각각 곱한다.",
        "old_ids": ["e3-2-1-1", "concept-e3-mul2-01"],
    },
    {
        "id": "e3-2-1-02",
        "name": "일의 자리에서 올림이 있는 (세 자리 수)×(한 자리 수)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "일의 자리 곱이 10 이상이 되어 십의 자리로 올림이 발생하는 곱셈.",
        "old_ids": ["e3-2-1-1"],
    },
    {
        "id": "e3-2-1-03",
        "name": "십, 백의 자리에서 올림이 있는 (세 자리 수)×(한 자리 수)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "십의 자리나 백의 자리에서 올림이 발생하는 곱셈. 연속 올림 처리를 정확히 한다.",
        "old_ids": ["e3-2-1-1"],
    },
    {
        "id": "e3-2-1-04",
        "name": "(몇십)×(몇십), (몇십몇)×(몇십)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "두 자리 수끼리의 곱셈 기초. 10의 배수끼리 곱하는 원리(20×30=600)를 이해한다.",
        "old_ids": ["e3-2-1-2", "concept-e3-mul2-02"],
    },
    {
        "id": "e3-2-1-05",
        "name": "(몇)×(몇십몇)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "교환법칙을 활용한 곱셈. 3×24=24×3으로 바꾸어 계산할 수 있음을 이해한다.",
        "old_ids": ["e3-2-1-2"],
    },
    {
        "id": "e3-2-1-06",
        "name": "올림이 한 번 있는 (몇십몇)×(몇십몇)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "(두 자리 수)×(두 자리 수)에서 올림이 한 번 발생. 부분 곱을 자릿수에 맞추어 합산한다.",
        "old_ids": ["e3-2-1-2"],
    },
    {
        "id": "e3-2-1-07",
        "name": "올림이 여러 번 있는 (몇십몇)×(몇십몇)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 1,
        "category": "computation", "part": "calc",
        "description": "(두 자리 수)×(두 자리 수)에서 올림이 여러 번 발생. 세로셈 알고리즘을 완성한다.",
        "old_ids": ["e3-2-1-2"],
    },

    # ── 2단원: 나눗셈 (8개) ──
    {
        "id": "e3-2-2-01",
        "name": "(몇십)÷(몇)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 2,
        "category": "computation", "part": "calc",
        "description": "60÷3=20처럼 십의 자리 수를 나누는 기초 나눗셈.",
        "old_ids": ["e3-2-2-1", "concept-e3-div2-01"],
    },
    {
        "id": "e3-2-2-02",
        "name": "내림이 없고 나머지가 없는 (몇십몇)÷(몇)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 2,
        "category": "computation", "part": "calc",
        "description": "십의 자리와 일의 자리 각각 나누어떨어지는 나눗셈. 예: 48÷4=12.",
        "old_ids": ["e3-2-2-1"],
    },
    {
        "id": "e3-2-2-03",
        "name": "내림이 있고 나머지가 없는 (몇십몇)÷(몇)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 2,
        "category": "computation", "part": "calc",
        "description": "십의 자리에서 나누어떨어지지 않아 일의 자리로 내리는 나눗셈. 예: 72÷3=24.",
        "old_ids": ["e3-2-2-1"],
    },
    {
        "id": "e3-2-2-04",
        "name": "내림이 없고 나머지가 있는 (몇십몇)÷(몇)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 2,
        "category": "computation", "part": "calc",
        "description": "나머지가 있는 기본 나눗셈. 나머지 < 나누는 수 조건을 확인한다.",
        "old_ids": ["e3-2-2-1"],
    },
    {
        "id": "e3-2-2-05",
        "name": "내림이 있고 나머지가 있는 (몇십몇)÷(몇)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 2,
        "category": "computation", "part": "calc",
        "description": "내림과 나머지가 모두 있는 나눗셈. 세로셈 알고리즘의 완성 단계.",
        "old_ids": ["e3-2-2-2", "concept-e3-div2-02"],
    },
    {
        "id": "e3-2-2-06",
        "name": "나머지가 없는 (세 자리 수)÷(한 자리 수)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 2,
        "category": "computation", "part": "calc",
        "description": "세 자리 수를 한 자리 수로 나누어떨어지는 나눗셈. 백·십·일의 자리 순서로 나눈다.",
        "old_ids": ["e3-2-2-2"],
    },
    {
        "id": "e3-2-2-07",
        "name": "나머지가 있는 (세 자리 수)÷(한 자리 수)",
        "grade": "elementary_3", "semester": 2, "chapter_number": 2,
        "category": "computation", "part": "calc",
        "description": "세 자리 수를 한 자리 수로 나누고 나머지를 구하는 나눗셈.",
        "old_ids": ["e3-2-2-2"],
    },
    {
        "id": "e3-2-2-08",
        "name": "맞게 계산했는지 확인하기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 2,
        "category": "computation", "part": "calc",
        "description": "나눗셈 검산: 나누는 수 × 몫 + 나머지 = 나뉨수. 검산으로 계산 정확성을 확인한다.",
        "old_ids": ["e3-2-2-2"],
    },

    # ── 3단원: 원 (4개) ──
    {
        "id": "e3-2-3-01",
        "name": "원의 중심, 반지름, 지름",
        "grade": "elementary_3", "semester": 2, "chapter_number": 3,
        "category": "concept", "part": "geo",
        "description": "원의 중심, 반지름(중심→원 위의 점), 지름(중심을 지나는 선분)의 정의를 이해한다.",
        "old_ids": ["e3-2-3-1", "concept-e3-circle-01"],
    },
    {
        "id": "e3-2-3-02",
        "name": "원의 성질",
        "grade": "elementary_3", "semester": 2, "chapter_number": 3,
        "category": "concept", "part": "geo",
        "description": "한 원에서 모든 반지름의 길이가 같고, 지름=반지름×2 관계를 이해한다.",
        "old_ids": ["e3-2-3-2", "concept-e3-circle-02"],
    },
    {
        "id": "e3-2-3-03",
        "name": "컴퍼스를 이용하여 원 그리기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 3,
        "category": "concept", "part": "geo",
        "description": "컴퍼스로 원을 그리는 방법. 컴퍼스 벌린 길이=반지름임을 이해한다.",
        "old_ids": ["e3-2-3-2"],
    },
    {
        "id": "e3-2-3-04",
        "name": "원을 이용하여 여러 가지 모양 그리기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 3,
        "category": "concept", "part": "geo",
        "description": "원을 활용한 무늬 만들기. 반지름과 중심을 조절하여 다양한 도형을 구성한다.",
        "old_ids": [],
    },

    # ── 4단원: 분수 (6개) ──
    {
        "id": "e3-2-4-01",
        "name": "분수로 나타내기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 4,
        "category": "concept", "part": "calc",
        "description": "연속량(도형의 일부)과 이산량(전체 개수의 일부)을 분수로 나타내는 방법을 익힌다.",
        "old_ids": ["e3-2-4-1", "concept-e3-frac2-01"],
    },
    {
        "id": "e3-2-4-02",
        "name": "전체 개수에 대한 분수만큼은 얼마인지 알기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 4,
        "category": "concept", "part": "calc",
        "description": "12개의 2/3는? → 12÷3×2=8개. 전체를 분모로 나누고 분자만큼 모으는 원리를 이해한다.",
        "old_ids": ["e3-2-4-1"],
    },
    {
        "id": "e3-2-4-03",
        "name": "전체 길이에 대한 분수만큼은 얼마인지 알기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 4,
        "category": "concept", "part": "calc",
        "description": "연속량에서 분수만큼의 크기를 구하기. 수직선 위에서 분수의 위치를 찾는다.",
        "old_ids": ["e3-2-4-1"],
    },
    {
        "id": "e3-2-4-04",
        "name": "진분수, 가분수, 자연수",
        "grade": "elementary_3", "semester": 2, "chapter_number": 4,
        "category": "concept", "part": "calc",
        "description": "진분수(분자<분모), 가분수(분자≥분모), 자연수(분수로 표현 가능)를 분류한다.",
        "old_ids": ["e3-2-4-2", "concept-e3-frac2-02"],
    },
    {
        "id": "e3-2-4-05",
        "name": "대분수",
        "grade": "elementary_3", "semester": 2, "chapter_number": 4,
        "category": "concept", "part": "calc",
        "description": "자연수와 진분수의 합으로 이루어진 대분수를 이해하고, 가분수↔대분수 상호 변환을 한다.",
        "old_ids": ["e3-2-4-2"],
    },
    {
        "id": "e3-2-4-06",
        "name": "분모가 같은 분수의 크기 비교",
        "grade": "elementary_3", "semester": 2, "chapter_number": 4,
        "category": "concept", "part": "calc",
        "description": "동분모 분수 비교, 진분수·가분수·대분수 간 크기 비교. 수직선을 활용한다.",
        "old_ids": ["e3-2-4-2"],
    },

    # ── 5단원: 들이와 무게 (8개) ──
    {
        "id": "e3-2-5-01",
        "name": "들이 비교하기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 5,
        "category": "concept", "part": "calc",
        "description": "두 그릇의 들이를 직접 비교하거나 임의 단위로 비교하는 방법을 이해한다.",
        "old_ids": ["e3-2-5-1", "concept-e3-vol-wt-01"],
    },
    {
        "id": "e3-2-5-02",
        "name": "들이의 단위",
        "grade": "elementary_3", "semester": 2, "chapter_number": 5,
        "category": "concept", "part": "calc",
        "description": "L(리터)와 mL(밀리리터) 단위. 1L=1000mL 관계를 이해한다.",
        "old_ids": ["e3-2-5-1"],
    },
    {
        "id": "e3-2-5-03",
        "name": "들이 어림하고 재어 보기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 5,
        "category": "concept", "part": "calc",
        "description": "실생활에서 들이를 어림하고 측정하는 활동. 적절한 단위(L/mL)를 선택한다.",
        "old_ids": ["e3-2-5-1"],
    },
    {
        "id": "e3-2-5-04",
        "name": "들이의 덧셈과 뺄셈",
        "grade": "elementary_3", "semester": 2, "chapter_number": 5,
        "category": "computation", "part": "calc",
        "description": "L와 mL 단위의 덧셈과 뺄셈. 1000mL=1L 받아올림/내림을 처리한다.",
        "old_ids": ["e3-2-5-1"],
    },
    {
        "id": "e3-2-5-05",
        "name": "무게 비교하기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 5,
        "category": "concept", "part": "calc",
        "description": "두 물체의 무게를 직접 비교(양팔 저울)하거나 임의 단위로 비교하는 방법을 이해한다.",
        "old_ids": ["e3-2-5-2", "concept-e3-vol-wt-02"],
    },
    {
        "id": "e3-2-5-06",
        "name": "무게의 단위",
        "grade": "elementary_3", "semester": 2, "chapter_number": 5,
        "category": "concept", "part": "calc",
        "description": "kg(킬로그램)과 g(그램) 단위. 1kg=1000g 관계를 이해한다.",
        "old_ids": ["e3-2-5-2"],
    },
    {
        "id": "e3-2-5-07",
        "name": "무게 어림하고 재어 보기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 5,
        "category": "concept", "part": "calc",
        "description": "실생활에서 무게를 어림하고 측정하는 활동. 적절한 단위(kg/g)를 선택한다.",
        "old_ids": ["e3-2-5-2"],
    },
    {
        "id": "e3-2-5-08",
        "name": "무게의 덧셈과 뺄셈",
        "grade": "elementary_3", "semester": 2, "chapter_number": 5,
        "category": "computation", "part": "calc",
        "description": "kg과 g 단위의 덧셈과 뺄셈. 1000g=1kg 받아올림/내림을 처리한다.",
        "old_ids": ["e3-2-5-2"],
    },

    # ── 6단원: 자료의 정리 (4개) ──
    {
        "id": "e3-2-6-01",
        "name": "표의 내용 알아보기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 6,
        "category": "concept", "part": "data",
        "description": "표에서 자료를 읽고 해석하는 방법. 항목, 수량, 합계를 이해한다.",
        "old_ids": ["e3-2-6-1", "concept-e3-data-01"],
    },
    {
        "id": "e3-2-6-02",
        "name": "그림그래프 알아보기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 6,
        "category": "concept", "part": "data",
        "description": "그림그래프의 구조(제목, 항목, 그림 단위)를 이해하고 내용을 읽는다.",
        "old_ids": ["e3-2-6-2", "concept-e3-data-02"],
    },
    {
        "id": "e3-2-6-03",
        "name": "그림그래프로 나타내기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 6,
        "category": "concept", "part": "data",
        "description": "자료를 그림그래프로 그리는 방법. 적절한 그림 단위를 정하고 그래프를 완성한다.",
        "old_ids": ["e3-2-6-2"],
    },
    {
        "id": "e3-2-6-04",
        "name": "자료를 조사하여 그림그래프로 나타내기",
        "grade": "elementary_3", "semester": 2, "chapter_number": 6,
        "category": "concept", "part": "data",
        "description": "실생활 자료를 직접 조사하고 분류하여 그림그래프로 나타내는 전체 과정을 수행한다.",
        "old_ids": [],
    },
]

# 초등 3학년 전체
E3_CONCEPTS = E3_S1_CONCEPTS + E3_S2_CONCEPTS


# =============================================
# 초등학교 4학년 1학기
# =============================================

E4_S1_CONCEPTS = [
    # ── 1단원: 큰 수 (6개) ──
    {"id": "e4-1-1-01", "name": "만", "grade": "elementary_4", "semester": 1, "chapter_number": 1, "category": "concept", "part": "calc", "description": "10000의 의미. 9999 다음 수, 천의 10배가 만임을 이해한다.", "old_ids": ["concept-e4-big-num-01"]},
    {"id": "e4-1-1-02", "name": "다섯 자리 수", "grade": "elementary_4", "semester": 1, "chapter_number": 1, "category": "concept", "part": "calc", "description": "만의 자리가 있는 다섯 자리 수. 각 자릿값을 이해하고 읽기/쓰기를 한다.", "old_ids": []},
    {"id": "e4-1-1-03", "name": "십만, 백만, 천만", "grade": "elementary_4", "semester": 1, "chapter_number": 1, "category": "concept", "part": "calc", "description": "큰 수의 자릿값. 10배씩 커지는 관계를 이해한다.", "old_ids": ["concept-e4-big-num-01"]},
    {"id": "e4-1-1-04", "name": "억과 조", "grade": "elementary_4", "semester": 1, "chapter_number": 1, "category": "concept", "part": "calc", "description": "억(100000000)과 조(1000000000000). 네 자리씩 끊어 읽는 방법을 익힌다.", "old_ids": ["concept-e4-big-num-02"]},
    {"id": "e4-1-1-05", "name": "뛰어 세기", "grade": "elementary_4", "semester": 1, "chapter_number": 1, "category": "concept", "part": "calc", "description": "만, 십만, 백만, 천만, 억 단위로 뛰어 세기.", "old_ids": []},
    {"id": "e4-1-1-06", "name": "수의 크기 비교", "grade": "elementary_4", "semester": 1, "chapter_number": 1, "category": "concept", "part": "calc", "description": "자릿수 비교 → 같으면 높은 자리부터 비교하는 방법.", "old_ids": ["concept-e4-big-num-02"]},

    # ── 2단원: 각도 (8개) ──
    {"id": "e4-1-2-01", "name": "각의 크기 비교", "grade": "elementary_4", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "두 각의 크기를 직접 비교하는 방법. 각도기 없이 겹쳐서 비교한다.", "old_ids": ["concept-e4-angle-01"]},
    {"id": "e4-1-2-02", "name": "각의 크기 재기", "grade": "elementary_4", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "각도기를 사용하여 각의 크기를 °(도) 단위로 측정한다.", "old_ids": ["concept-e4-angle-01"]},
    {"id": "e4-1-2-03", "name": "각 그리기", "grade": "elementary_4", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "각도기를 사용하여 주어진 크기의 각을 그린다.", "old_ids": []},
    {"id": "e4-1-2-04", "name": "직각보다 작은 각과 직각보다 큰 각", "grade": "elementary_4", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "예각(0°~90°)과 둔각(90°~180°)의 정의와 분류.", "old_ids": ["concept-e4-angle-02"]},
    {"id": "e4-1-2-05", "name": "각도 어림하기", "grade": "elementary_4", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "각도기 없이 각의 크기를 어림하는 방법.", "old_ids": []},
    {"id": "e4-1-2-06", "name": "각도의 덧셈과 뺄셈", "grade": "elementary_4", "semester": 1, "chapter_number": 2, "category": "computation", "part": "geo", "description": "각도의 덧셈과 뺄셈. 예: 45°+60°=105°.", "old_ids": ["concept-e4-angle-02"]},
    {"id": "e4-1-2-07", "name": "삼각형의 세 각의 크기의 합", "grade": "elementary_4", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "삼각형의 내각의 합=180°임을 실험과 증명으로 이해한다.", "old_ids": []},
    {"id": "e4-1-2-08", "name": "사각형의 네 각의 크기의 합", "grade": "elementary_4", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "사각형의 내각의 합=360°임을 이해한다.", "old_ids": []},

    # ── 3단원: 곱셈과 나눗셈 (7개) ──
    {"id": "e4-1-3-01", "name": "(세 자리 수)×(몇십)", "grade": "elementary_4", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "0을 붙이는 원리를 활용한 (세 자리 수)×(몇십) 곱셈.", "old_ids": ["concept-e4-mul-div-01"]},
    {"id": "e4-1-3-02", "name": "(세 자리 수)×(몇십몇)", "grade": "elementary_4", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "부분 곱을 구하고 자릿수에 맞추어 합산하는 (세 자리 수)×(두 자리 수) 곱셈.", "old_ids": ["concept-e4-mul-div-01"]},
    {"id": "e4-1-3-03", "name": "(세 자리 수)÷(몇십)", "grade": "elementary_4", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "어림하여 몫을 세우고 나머지를 구하는 (세 자리 수)÷(몇십) 나눗셈.", "old_ids": ["concept-e4-mul-div-02"]},
    {"id": "e4-1-3-04", "name": "몫이 한 자리 수인 (두 자리 수)÷(두 자리 수)", "grade": "elementary_4", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "몫이 한 자리인 경우의 (두 자리 수)÷(두 자리 수).", "old_ids": ["concept-e4-mul-div-02"]},
    {"id": "e4-1-3-05", "name": "몫이 한 자리 수인 (세 자리 수)÷(두 자리 수)", "grade": "elementary_4", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "몫이 한 자리인 경우의 (세 자리 수)÷(두 자리 수).", "old_ids": []},
    {"id": "e4-1-3-06", "name": "몫이 두 자리 수인 (세 자리 수)÷(두 자리 수) (1)", "grade": "elementary_4", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "몫이 두 자리인 경우의 나눗셈. 백의 자리부터 나누기 시작한다.", "old_ids": []},
    {"id": "e4-1-3-07", "name": "몫이 두 자리 수인 (세 자리 수)÷(두 자리 수) (2)", "grade": "elementary_4", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "나머지가 있는 경우를 포함한 두 자리 몫 나눗셈. 검산으로 확인한다.", "old_ids": []},

    # ── 4단원: 평면도형의 이동 (5개) ──
    {"id": "e4-1-4-01", "name": "평면도형 밀기", "grade": "elementary_4", "semester": 1, "chapter_number": 4, "category": "concept", "part": "geo", "description": "도형을 상하좌우로 밀었을 때 모양과 크기는 변하지 않음을 이해한다.", "old_ids": ["concept-e4-transform-01"]},
    {"id": "e4-1-4-02", "name": "평면도형 뒤집기", "grade": "elementary_4", "semester": 1, "chapter_number": 4, "category": "concept", "part": "geo", "description": "도형을 축을 기준으로 뒤집었을 때 좌우/상하가 바뀌는 것을 이해한다.", "old_ids": ["concept-e4-transform-01"]},
    {"id": "e4-1-4-03", "name": "평면도형 돌리기", "grade": "elementary_4", "semester": 1, "chapter_number": 4, "category": "concept", "part": "geo", "description": "도형을 한 점을 중심으로 회전. 시계 방향, 반시계 방향, 90°/180°/270° 회전.", "old_ids": ["concept-e4-transform-02"]},
    {"id": "e4-1-4-04", "name": "평면도형 뒤집고 돌리기", "grade": "elementary_4", "semester": 1, "chapter_number": 4, "category": "concept", "part": "geo", "description": "뒤집기와 돌리기를 결합한 복합 이동.", "old_ids": ["concept-e4-transform-02"]},
    {"id": "e4-1-4-05", "name": "무늬 꾸미기", "grade": "elementary_4", "semester": 1, "chapter_number": 4, "category": "concept", "part": "geo", "description": "밀기, 뒤집기, 돌리기를 활용하여 규칙적인 무늬를 만든다.", "old_ids": []},

    # ── 5단원: 막대그래프 (4개) ──
    {"id": "e4-1-5-01", "name": "막대그래프", "grade": "elementary_4", "semester": 1, "chapter_number": 5, "category": "concept", "part": "data", "description": "막대그래프의 구조(제목, 항목, 눈금, 막대)를 이해한다.", "old_ids": ["concept-e4-bar-graph-01"]},
    {"id": "e4-1-5-02", "name": "막대그래프에서 알 수 있는 내용", "grade": "elementary_4", "semester": 1, "chapter_number": 5, "category": "concept", "part": "data", "description": "막대그래프를 읽고 해석하여 자료의 특징을 파악한다.", "old_ids": ["concept-e4-bar-graph-01"]},
    {"id": "e4-1-5-03", "name": "막대그래프로 나타내기", "grade": "elementary_4", "semester": 1, "chapter_number": 5, "category": "concept", "part": "data", "description": "자료를 막대그래프로 그리는 방법. 눈금 단위를 정하고 막대를 그린다.", "old_ids": ["concept-e4-bar-graph-02"]},
    {"id": "e4-1-5-04", "name": "자료를 조사하여 막대그래프로 나타내기", "grade": "elementary_4", "semester": 1, "chapter_number": 5, "category": "concept", "part": "data", "description": "실생활 자료를 직접 조사하고 막대그래프로 나타내는 전체 과정.", "old_ids": ["concept-e4-bar-graph-02"]},

    # ── 6단원: 규칙 찾기 (5개) ──
    {"id": "e4-1-6-01", "name": "수의 배열에서 규칙 찾기", "grade": "elementary_4", "semester": 1, "chapter_number": 6, "category": "concept", "part": "algebra", "description": "수의 나열에서 규칙성을 발견한다.", "old_ids": ["concept-e4-pattern-01"]},
    {"id": "e4-1-6-02", "name": "도형의 배열에서 규칙 찾기", "grade": "elementary_4", "semester": 1, "chapter_number": 6, "category": "concept", "part": "algebra", "description": "도형의 반복 패턴에서 규칙을 발견한다.", "old_ids": ["concept-e4-pattern-01"]},
    {"id": "e4-1-6-03", "name": "덧셈식과 뺄셈식의 배열에서 규칙 찾기", "grade": "elementary_4", "semester": 1, "chapter_number": 6, "category": "concept", "part": "algebra", "description": "덧셈/뺄셈 식의 변화에서 규칙을 찾는다.", "old_ids": ["concept-e4-pattern-02"]},
    {"id": "e4-1-6-04", "name": "곱셈식과 나눗셈식의 배열에서 규칙 찾기", "grade": "elementary_4", "semester": 1, "chapter_number": 6, "category": "concept", "part": "algebra", "description": "곱셈/나눗셈 식의 변화에서 규칙을 찾는다.", "old_ids": ["concept-e4-pattern-02"]},
    {"id": "e4-1-6-05", "name": "규칙을 찾아 식으로 나타내기", "grade": "elementary_4", "semester": 1, "chapter_number": 6, "category": "concept", "part": "algebra", "description": "발견한 규칙을 수학적 식으로 표현한다.", "old_ids": []},
]

# =============================================
# 초등학교 4학년 2학기
# =============================================

E4_S2_CONCEPTS = [
    # ── 1단원: 분수의 덧셈과 뺄셈 (6개) ──
    {"id": "e4-2-1-01", "name": "(진분수)+(진분수)", "grade": "elementary_4", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "동분모 진분수의 덧셈. 분모는 그대로, 분자끼리 더한다.", "old_ids": ["concept-e4-frac-op-01"]},
    {"id": "e4-2-1-02", "name": "(대분수)+(대분수)", "grade": "elementary_4", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "자연수는 자연수끼리, 분수는 분수끼리 더하는 대분수 덧셈.", "old_ids": ["concept-e4-frac-op-01"]},
    {"id": "e4-2-1-03", "name": "(진분수)-(진분수)", "grade": "elementary_4", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "동분모 진분수의 뺄셈. 분모는 그대로, 분자끼리 뺀다.", "old_ids": ["concept-e4-frac-op-02"]},
    {"id": "e4-2-1-04", "name": "받아내림이 없는 (대분수)-(대분수)", "grade": "elementary_4", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "자연수끼리, 분수끼리 각각 빼는 대분수 뺄셈.", "old_ids": ["concept-e4-frac-op-02"]},
    {"id": "e4-2-1-05", "name": "(자연수)-(분수)", "grade": "elementary_4", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "자연수에서 분수를 빼는 계산. 자연수를 가분수로 바꾸어 계산.", "old_ids": []},
    {"id": "e4-2-1-06", "name": "받아내림이 있는 (대분수)-(대분수)", "grade": "elementary_4", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "분수 부분에서 뺄 수 없어 자연수에서 1을 빌려오는 대분수 뺄셈.", "old_ids": []},

    # ── 2단원: 삼각형 (5개) ──
    {"id": "e4-2-2-01", "name": "삼각형을 변의 길이에 따라 분류하기", "grade": "elementary_4", "semester": 2, "chapter_number": 2, "category": "concept", "part": "geo", "description": "이등변삼각형(두 변이 같음), 정삼각형(세 변이 같음), 부등변삼각형을 분류한다.", "old_ids": ["concept-e4-triangle-01"]},
    {"id": "e4-2-2-02", "name": "이등변삼각형의 성질", "grade": "elementary_4", "semester": 2, "chapter_number": 2, "category": "concept", "part": "geo", "description": "이등변삼각형의 두 밑각의 크기가 같음을 이해한다.", "old_ids": ["concept-e4-triangle-01"]},
    {"id": "e4-2-2-03", "name": "정삼각형의 성질", "grade": "elementary_4", "semester": 2, "chapter_number": 2, "category": "concept", "part": "geo", "description": "정삼각형의 세 각이 모두 60°임을 이해한다.", "old_ids": []},
    {"id": "e4-2-2-04", "name": "삼각형을 각의 크기에 따라 분류하기", "grade": "elementary_4", "semester": 2, "chapter_number": 2, "category": "concept", "part": "geo", "description": "예각삼각형, 직각삼각형, 둔각삼각형으로 분류한다.", "old_ids": ["concept-e4-triangle-02"]},
    {"id": "e4-2-2-05", "name": "삼각형을 두 가지 기준으로 분류하기", "grade": "elementary_4", "semester": 2, "chapter_number": 2, "category": "concept", "part": "geo", "description": "변의 길이와 각의 크기 두 기준을 동시에 적용하여 분류한다.", "old_ids": ["concept-e4-triangle-02"]},

    # ── 3단원: 소수의 덧셈과 뺄셈 (8개) ──
    {"id": "e4-2-3-01", "name": "소수 두 자리 수", "grade": "elementary_4", "semester": 2, "chapter_number": 3, "category": "concept", "part": "calc", "description": "소수 둘째 자리까지의 수. 0.01의 의미와 자릿값을 이해한다.", "old_ids": ["concept-e4-dec-op-01"]},
    {"id": "e4-2-3-02", "name": "소수 세 자리 수", "grade": "elementary_4", "semester": 2, "chapter_number": 3, "category": "concept", "part": "calc", "description": "소수 셋째 자리까지의 수. 0.001의 의미와 자릿값을 이해한다.", "old_ids": ["concept-e4-dec-op-01"]},
    {"id": "e4-2-3-03", "name": "소수의 크기 비교", "grade": "elementary_4", "semester": 2, "chapter_number": 3, "category": "concept", "part": "calc", "description": "소수의 크기를 비교하는 방법. 자연수 부분 → 소수 첫째 자리 → 둘째 자리 순으로 비교.", "old_ids": []},
    {"id": "e4-2-3-04", "name": "소수 사이의 관계", "grade": "elementary_4", "semester": 2, "chapter_number": 3, "category": "concept", "part": "calc", "description": "0.1=0.10=0.100 등 소수의 동치 관계. 10배, 1/10 관계를 이해한다.", "old_ids": []},
    {"id": "e4-2-3-05", "name": "소수 한 자리 수의 덧셈", "grade": "elementary_4", "semester": 2, "chapter_number": 3, "category": "computation", "part": "calc", "description": "소수점을 맞추어 더하는 소수 한 자리 수 덧셈.", "old_ids": ["concept-e4-dec-op-02"]},
    {"id": "e4-2-3-06", "name": "소수 한 자리 수의 뺄셈", "grade": "elementary_4", "semester": 2, "chapter_number": 3, "category": "computation", "part": "calc", "description": "소수점을 맞추어 빼는 소수 한 자리 수 뺄셈.", "old_ids": ["concept-e4-dec-op-02"]},
    {"id": "e4-2-3-07", "name": "소수 두 자리 수의 덧셈", "grade": "elementary_4", "semester": 2, "chapter_number": 3, "category": "computation", "part": "calc", "description": "소수 둘째 자리까지의 덧셈. 자릿수가 다른 경우 0을 채워 계산.", "old_ids": []},
    {"id": "e4-2-3-08", "name": "소수 두 자리 수의 뺄셈", "grade": "elementary_4", "semester": 2, "chapter_number": 3, "category": "computation", "part": "calc", "description": "소수 둘째 자리까지의 뺄셈. 자릿수가 다른 경우 0을 채워 계산.", "old_ids": []},

    # ── 4단원: 사각형 (7개) ──
    {"id": "e4-2-4-01", "name": "수직과 수선", "grade": "elementary_4", "semester": 2, "chapter_number": 4, "category": "concept", "part": "geo", "description": "두 직선이 만나서 이루는 각이 직각일 때 수직. 수선의 정의와 작도.", "old_ids": ["concept-e4-quad-01"]},
    {"id": "e4-2-4-02", "name": "평행과 평행선", "grade": "elementary_4", "semester": 2, "chapter_number": 4, "category": "concept", "part": "geo", "description": "한 직선에 수직인 두 직선은 서로 평행. 평행선의 정의와 성질.", "old_ids": ["concept-e4-quad-01"]},
    {"id": "e4-2-4-03", "name": "평행선 사이의 거리", "grade": "elementary_4", "semester": 2, "chapter_number": 4, "category": "concept", "part": "geo", "description": "두 평행선 사이의 수선의 길이는 어디서나 같음을 이해한다.", "old_ids": []},
    {"id": "e4-2-4-04", "name": "사다리꼴", "grade": "elementary_4", "semester": 2, "chapter_number": 4, "category": "concept", "part": "geo", "description": "마주 보는 한 쌍의 변이 평행인 사각형.", "old_ids": ["concept-e4-quad-02"]},
    {"id": "e4-2-4-05", "name": "평행사변형", "grade": "elementary_4", "semester": 2, "chapter_number": 4, "category": "concept", "part": "geo", "description": "마주 보는 두 쌍의 변이 평행인 사각형. 대변의 길이와 대각의 크기가 같다.", "old_ids": ["concept-e4-quad-02"]},
    {"id": "e4-2-4-06", "name": "마름모", "grade": "elementary_4", "semester": 2, "chapter_number": 4, "category": "concept", "part": "geo", "description": "네 변의 길이가 모두 같은 사각형. 대각선이 서로 수직으로 이등분한다.", "old_ids": []},
    {"id": "e4-2-4-07", "name": "여러 가지 사각형", "grade": "elementary_4", "semester": 2, "chapter_number": 4, "category": "concept", "part": "geo", "description": "사각형의 포함 관계: 정사각형⊂직사각형⊂평행사변형⊂사다리꼴.", "old_ids": []},

    # ── 5단원: 꺾은선그래프 (5개) ──
    {"id": "e4-2-5-01", "name": "꺾은선그래프", "grade": "elementary_4", "semester": 2, "chapter_number": 5, "category": "concept", "part": "data", "description": "시간에 따른 변화를 나타내는 꺾은선그래프의 구조를 이해한다.", "old_ids": ["concept-e4-line-graph-01"]},
    {"id": "e4-2-5-02", "name": "꺾은선그래프에서 알 수 있는 내용", "grade": "elementary_4", "semester": 2, "chapter_number": 5, "category": "concept", "part": "data", "description": "꺾은선그래프에서 증가/감소 추이, 변화폭을 읽는다.", "old_ids": ["concept-e4-line-graph-01"]},
    {"id": "e4-2-5-03", "name": "꺾은선그래프로 나타내기", "grade": "elementary_4", "semester": 2, "chapter_number": 5, "category": "concept", "part": "data", "description": "자료를 꺾은선그래프로 그리는 방법.", "old_ids": ["concept-e4-line-graph-02"]},
    {"id": "e4-2-5-04", "name": "자료를 조사하여 꺾은선그래프로 나타내기", "grade": "elementary_4", "semester": 2, "chapter_number": 5, "category": "concept", "part": "data", "description": "실생활 자료를 직접 조사하여 꺾은선그래프로 나타낸다.", "old_ids": ["concept-e4-line-graph-02"]},
    {"id": "e4-2-5-05", "name": "꺾은선그래프의 활용", "grade": "elementary_4", "semester": 2, "chapter_number": 5, "category": "concept", "part": "data", "description": "두 꺾은선그래프를 비교하고 예측하는 활용.", "old_ids": []},

    # ── 6단원: 다각형 (5개) ──
    {"id": "e4-2-6-01", "name": "다각형", "grade": "elementary_4", "semester": 2, "chapter_number": 6, "category": "concept", "part": "geo", "description": "선분으로만 둘러싸인 도형. 오각형, 육각형 등 이름과 성질.", "old_ids": ["concept-e4-polygon-01"]},
    {"id": "e4-2-6-02", "name": "정다각형", "grade": "elementary_4", "semester": 2, "chapter_number": 6, "category": "concept", "part": "geo", "description": "변의 길이와 각의 크기가 모두 같은 다각형.", "old_ids": ["concept-e4-polygon-01"]},
    {"id": "e4-2-6-03", "name": "대각선", "grade": "elementary_4", "semester": 2, "chapter_number": 6, "category": "concept", "part": "geo", "description": "다각형에서 이웃하지 않는 두 꼭짓점을 잇는 선분. 대각선 수 세기.", "old_ids": ["concept-e4-polygon-02"]},
    {"id": "e4-2-6-04", "name": "모양 만들기", "grade": "elementary_4", "semester": 2, "chapter_number": 6, "category": "concept", "part": "geo", "description": "다각형을 사용하여 여러 가지 모양을 만든다.", "old_ids": ["concept-e4-polygon-02"]},
    {"id": "e4-2-6-05", "name": "모양 채우기", "grade": "elementary_4", "semester": 2, "chapter_number": 6, "category": "concept", "part": "geo", "description": "정다각형으로 평면을 빈틈없이 채우는 테셀레이션.", "old_ids": []},
]

E4_CONCEPTS = E4_S1_CONCEPTS + E4_S2_CONCEPTS


# =============================================
# 초등학교 5학년 1학기
# =============================================

E5_S1_CONCEPTS = [
    # ── 1단원: 자연수의 혼합 계산 (5개) ──
    {"id": "e5-1-1-01", "name": "덧셈과 뺄셈이 섞여 있는 식", "grade": "elementary_5", "semester": 1, "chapter_number": 1, "category": "computation", "part": "calc", "description": "덧셈과 뺄셈만 있는 혼합 계산. 앞에서부터 차례로 계산하는 좌결합성을 이해한다.", "old_ids": ["e5-1-1-1", "concept-e5-mixed-calc-01"]},
    {"id": "e5-1-1-02", "name": "곱셈과 나눗셈이 섞여 있는 식", "grade": "elementary_5", "semester": 1, "chapter_number": 1, "category": "computation", "part": "calc", "description": "곱셈과 나눗셈만 있는 혼합 계산. 앞에서부터 차례로 계산한다.", "old_ids": ["e5-1-1-1"]},
    {"id": "e5-1-1-03", "name": "덧셈, 뺄셈, 곱셈이 섞여 있는 식", "grade": "elementary_5", "semester": 1, "chapter_number": 1, "category": "computation", "part": "calc", "description": "곱셈을 먼저 계산한 후 덧셈·뺄셈을 처리하는 연산 우선순위를 이해한다.", "old_ids": ["e5-1-1-2", "concept-e5-mixed-calc-02"]},
    {"id": "e5-1-1-04", "name": "덧셈, 뺄셈, 나눗셈이 섞여 있는 식", "grade": "elementary_5", "semester": 1, "chapter_number": 1, "category": "computation", "part": "calc", "description": "나눗셈을 먼저 계산한 후 덧셈·뺄셈을 처리한다.", "old_ids": ["e5-1-1-2"]},
    {"id": "e5-1-1-05", "name": "덧셈, 뺄셈, 곱셈, 나눗셈이 섞여 있는 식", "grade": "elementary_5", "semester": 1, "chapter_number": 1, "category": "computation", "part": "calc", "description": "사칙연산이 모두 섞인 식. 괄호 → 곱셈·나눗셈 → 덧셈·뺄셈 순서로 계산한다.", "old_ids": ["e5-1-1-2"]},

    # ── 2단원: 약수와 배수 (6개) ──
    {"id": "e5-1-2-01", "name": "약수와 배수", "grade": "elementary_5", "semester": 1, "chapter_number": 2, "category": "concept", "part": "calc", "description": "약수(나누어떨어지게 하는 수)와 배수(곱하여 나온 수)의 정의를 이해한다.", "old_ids": ["e5-1-2-1", "concept-e5-divisor-01"]},
    {"id": "e5-1-2-02", "name": "약수와 배수의 관계", "grade": "elementary_5", "semester": 1, "chapter_number": 2, "category": "concept", "part": "calc", "description": "A가 B의 약수이면 B는 A의 배수. 역도 성립하는 쌍대 관계를 이해한다.", "old_ids": ["e5-1-2-1"]},
    {"id": "e5-1-2-03", "name": "공약수와 최대공약수", "grade": "elementary_5", "semester": 1, "chapter_number": 2, "category": "concept", "part": "calc", "description": "공약수(두 수의 공통 약수)와 최대공약수의 정의. 공약수는 최대공약수의 약수임을 안다.", "old_ids": ["e5-1-2-2", "concept-e5-divisor-02"]},
    {"id": "e5-1-2-04", "name": "최대공약수 구하는 방법", "grade": "elementary_5", "semester": 1, "chapter_number": 2, "category": "computation", "part": "calc", "description": "공통으로 나누기(연습장법)를 이용하여 최대공약수를 구하는 방법을 익힌다.", "old_ids": ["e5-1-2-2"]},
    {"id": "e5-1-2-05", "name": "공배수와 최소공배수", "grade": "elementary_5", "semester": 1, "chapter_number": 2, "category": "concept", "part": "calc", "description": "공배수(두 수의 공통 배수)와 최소공배수의 정의. 공배수는 최소공배수의 배수임을 안다.", "old_ids": ["e5-1-2-2"]},
    {"id": "e5-1-2-06", "name": "최소공배수 구하는 방법", "grade": "elementary_5", "semester": 1, "chapter_number": 2, "category": "computation", "part": "calc", "description": "공통으로 나누기(연습장법)를 이용하여 최소공배수를 구하는 방법을 익힌다.", "old_ids": ["e5-1-2-2"]},

    # ── 3단원: 규칙과 대응 (3개) ──
    {"id": "e5-1-3-01", "name": "두 양 사이의 관계", "grade": "elementary_5", "semester": 1, "chapter_number": 3, "category": "concept", "part": "algebra", "description": "두 양이 함께 변하는 관계를 표로 정리하고 대응 규칙을 발견한다.", "old_ids": ["e5-1-3-1", "concept-e5-corresp-01"]},
    {"id": "e5-1-3-02", "name": "대응 관계를 식으로 나타내기", "grade": "elementary_5", "semester": 1, "chapter_number": 3, "category": "concept", "part": "algebra", "description": "발견한 대응 관계를 □, △ 등의 기호를 사용하여 식으로 표현한다.", "old_ids": ["e5-1-3-2", "concept-e5-corresp-02"]},
    {"id": "e5-1-3-03", "name": "생활 속에서 대응 관계를 찾아 식으로 나타내기", "grade": "elementary_5", "semester": 1, "chapter_number": 3, "category": "concept", "part": "algebra", "description": "실생활 상황에서 두 양의 대응 관계를 찾아 식으로 나타내고 활용한다.", "old_ids": ["e5-1-3-2"]},

    # ── 4단원: 약분과 통분 (6개) ──
    {"id": "e5-1-4-01", "name": "크기가 같은 분수", "grade": "elementary_5", "semester": 1, "chapter_number": 4, "category": "concept", "part": "calc", "description": "분자와 분모에 같은 수를 곱하거나 나누어도 크기가 같은 분수임을 이해한다.", "old_ids": ["e5-1-4-1", "concept-e5-reduce-01"]},
    {"id": "e5-1-4-02", "name": "크기가 같은 분수 만들기", "grade": "elementary_5", "semester": 1, "chapter_number": 4, "category": "concept", "part": "calc", "description": "분자와 분모에 0이 아닌 같은 수를 곱하거나 나누어 크기가 같은 분수를 만든다.", "old_ids": ["e5-1-4-1"]},
    {"id": "e5-1-4-03", "name": "분수를 간단하게 나타내기", "grade": "elementary_5", "semester": 1, "chapter_number": 4, "category": "computation", "part": "calc", "description": "약분(분자와 분모를 공약수로 나누기)으로 기약분수를 만든다.", "old_ids": ["e5-1-4-1"]},
    {"id": "e5-1-4-04", "name": "분모가 같은 분수로 나타내기", "grade": "elementary_5", "semester": 1, "chapter_number": 4, "category": "computation", "part": "calc", "description": "통분(분모를 같게 만들기). 최소공배수를 공통분모로 사용한다.", "old_ids": ["e5-1-4-2", "concept-e5-reduce-02"]},
    {"id": "e5-1-4-05", "name": "분수의 크기 비교", "grade": "elementary_5", "semester": 1, "chapter_number": 4, "category": "concept", "part": "calc", "description": "통분하여 분모를 같게 한 후 분자의 크기로 비교한다.", "old_ids": ["e5-1-4-2"]},
    {"id": "e5-1-4-06", "name": "분수와 소수의 크기 비교", "grade": "elementary_5", "semester": 1, "chapter_number": 4, "category": "concept", "part": "calc", "description": "분수를 소수로, 또는 소수를 분수로 바꾸어 크기를 비교하는 방법.", "old_ids": ["e5-1-4-2"]},

    # ── 5단원: 분수의 덧셈과 뺄셈 (6개) ──
    {"id": "e5-1-5-01", "name": "받아올림이 없는 진분수의 덧셈", "grade": "elementary_5", "semester": 1, "chapter_number": 5, "category": "computation", "part": "calc", "description": "이분모 진분수의 덧셈. 통분 후 분자끼리 더하되 합이 분모보다 작은 경우.", "old_ids": ["e5-1-5-1", "concept-e5-frac-add-01"]},
    {"id": "e5-1-5-02", "name": "받아올림이 있는 진분수의 덧셈", "grade": "elementary_5", "semester": 1, "chapter_number": 5, "category": "computation", "part": "calc", "description": "통분 후 분자의 합이 분모 이상이 되어 대분수로 바꾸는 경우.", "old_ids": ["e5-1-5-1"]},
    {"id": "e5-1-5-03", "name": "받아올림이 있는 대분수의 덧셈", "grade": "elementary_5", "semester": 1, "chapter_number": 5, "category": "computation", "part": "calc", "description": "대분수의 분수 부분끼리 더할 때 가분수가 되어 자연수로 받아올림하는 경우.", "old_ids": ["e5-1-5-1"]},
    {"id": "e5-1-5-04", "name": "받아내림이 없는 진분수의 뺄셈", "grade": "elementary_5", "semester": 1, "chapter_number": 5, "category": "computation", "part": "calc", "description": "이분모 진분수의 뺄셈. 통분 후 분자끼리 빼는 기본 뺄셈.", "old_ids": ["e5-1-5-2", "concept-e5-frac-add-02"]},
    {"id": "e5-1-5-05", "name": "받아내림이 없는 대분수의 뺄셈", "grade": "elementary_5", "semester": 1, "chapter_number": 5, "category": "computation", "part": "calc", "description": "대분수의 자연수끼리, 분수끼리 각각 빼는 뺄셈.", "old_ids": ["e5-1-5-2"]},
    {"id": "e5-1-5-06", "name": "받아내림이 있는 대분수의 뺄셈", "grade": "elementary_5", "semester": 1, "chapter_number": 5, "category": "computation", "part": "calc", "description": "분수 부분에서 뺄 수 없어 자연수에서 1을 빌려오는 대분수 뺄셈.", "old_ids": ["e5-1-5-2"]},

    # ── 6단원: 다각형의 둘레와 넓이 (9개) ──
    {"id": "e5-1-6-01", "name": "정다각형의 둘레", "grade": "elementary_5", "semester": 1, "chapter_number": 6, "category": "concept", "part": "geo", "description": "정다각형의 둘레 = 한 변의 길이 × 변의 수. 정다각형의 성질을 활용한다.", "old_ids": ["e5-1-6-1", "concept-e5-poly-area-01"]},
    {"id": "e5-1-6-02", "name": "사각형의 둘레", "grade": "elementary_5", "semester": 1, "chapter_number": 6, "category": "concept", "part": "geo", "description": "직사각형의 둘레 = (가로+세로)×2. 다양한 사각형의 둘레를 구한다.", "old_ids": ["e5-1-6-1"]},
    {"id": "e5-1-6-03", "name": "넓이의 단위 1cm²", "grade": "elementary_5", "semester": 1, "chapter_number": 6, "category": "concept", "part": "geo", "description": "1cm²(1제곱센티미터)의 정의. 넓이의 기본 단위를 이해한다.", "old_ids": ["e5-1-6-1"]},
    {"id": "e5-1-6-04", "name": "직사각형의 넓이", "grade": "elementary_5", "semester": 1, "chapter_number": 6, "category": "computation", "part": "geo", "description": "직사각형의 넓이 = 가로 × 세로. 단위넓이의 개수로 넓이 공식을 유도한다.", "old_ids": ["e5-1-6-1"]},
    {"id": "e5-1-6-05", "name": "1cm²보다 더 큰 넓이의 단위", "grade": "elementary_5", "semester": 1, "chapter_number": 6, "category": "concept", "part": "geo", "description": "1m², 1km², 1ha, 1a 등 큰 넓이 단위와 단위 환산을 이해한다.", "old_ids": ["e5-1-6-1"]},
    {"id": "e5-1-6-06", "name": "평행사변형의 넓이", "grade": "elementary_5", "semester": 1, "chapter_number": 6, "category": "computation", "part": "geo", "description": "평행사변형의 넓이 = 밑변 × 높이. 직사각형으로 변환하여 공식을 유도한다.", "old_ids": ["e5-1-6-2", "concept-e5-poly-area-02"]},
    {"id": "e5-1-6-07", "name": "삼각형의 넓이", "grade": "elementary_5", "semester": 1, "chapter_number": 6, "category": "computation", "part": "geo", "description": "삼각형의 넓이 = 밑변 × 높이 ÷ 2. 평행사변형의 절반으로 유도한다.", "old_ids": ["e5-1-6-2"]},
    {"id": "e5-1-6-08", "name": "마름모의 넓이", "grade": "elementary_5", "semester": 1, "chapter_number": 6, "category": "computation", "part": "geo", "description": "마름모의 넓이 = 한 대각선 × 다른 대각선 ÷ 2.", "old_ids": ["e5-1-6-2"]},
    {"id": "e5-1-6-09", "name": "사다리꼴의 넓이", "grade": "elementary_5", "semester": 1, "chapter_number": 6, "category": "computation", "part": "geo", "description": "사다리꼴의 넓이 = (윗변+아랫변) × 높이 ÷ 2.", "old_ids": ["e5-1-6-2"]},
]

# =============================================
# 초등학교 5학년 2학기
# =============================================

E5_S2_CONCEPTS = [
    # ── 1단원: 수의 범위와 어림하기 (7개) ──
    {"id": "e5-2-1-01", "name": "이상과 이하", "grade": "elementary_5", "semester": 2, "chapter_number": 1, "category": "concept", "part": "calc", "description": "이상(≥)과 이하(≤)의 정의. 수직선 위에서 범위를 나타낸다.", "old_ids": ["e5-2-1-1", "concept-e5-range-01"]},
    {"id": "e5-2-1-02", "name": "초과와 미만", "grade": "elementary_5", "semester": 2, "chapter_number": 1, "category": "concept", "part": "calc", "description": "초과(>)와 미만(<)의 정의. 이상/이하와의 차이를 이해한다.", "old_ids": ["e5-2-1-1"]},
    {"id": "e5-2-1-03", "name": "수의 범위 활용하기", "grade": "elementary_5", "semester": 2, "chapter_number": 1, "category": "concept", "part": "calc", "description": "실생활에서 수의 범위(이상, 이하, 초과, 미만)를 활용하여 문제를 해결한다.", "old_ids": ["e5-2-1-1"]},
    {"id": "e5-2-1-04", "name": "올림", "grade": "elementary_5", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "올림의 정의와 방법. 구하려는 자리 아래 수를 올려서 나타낸다.", "old_ids": ["e5-2-1-2", "concept-e5-round-01"]},
    {"id": "e5-2-1-05", "name": "버림", "grade": "elementary_5", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "버림의 정의와 방법. 구하려는 자리 아래 수를 버려서 나타낸다.", "old_ids": ["e5-2-1-2"]},
    {"id": "e5-2-1-06", "name": "반올림", "grade": "elementary_5", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "반올림의 정의와 방법. 구하려는 자리 바로 아래 자리 숫자가 5 이상이면 올림, 4 이하면 버림.", "old_ids": ["e5-2-1-2"]},
    {"id": "e5-2-1-07", "name": "올림, 버림, 반올림 활용하기", "grade": "elementary_5", "semester": 2, "chapter_number": 1, "category": "concept", "part": "calc", "description": "상황에 따라 올림, 버림, 반올림 중 적절한 어림 방법을 선택하여 활용한다.", "old_ids": ["e5-2-1-2"]},

    # ── 2단원: 분수의 곱셈 (5개) ──
    {"id": "e5-2-2-01", "name": "(분수)×(자연수)", "grade": "elementary_5", "semester": 2, "chapter_number": 2, "category": "computation", "part": "calc", "description": "분수에 자연수를 곱하는 계산. 분자에 자연수를 곱하고 약분한다.", "old_ids": ["e5-2-2-1", "concept-e5-frac-mul-01"]},
    {"id": "e5-2-2-02", "name": "(자연수)×(분수)", "grade": "elementary_5", "semester": 2, "chapter_number": 2, "category": "computation", "part": "calc", "description": "자연수에 분수를 곱하는 계산. 교환법칙으로 (분수)×(자연수)와 같음을 이해한다.", "old_ids": ["e5-2-2-1"]},
    {"id": "e5-2-2-03", "name": "진분수의 곱셈", "grade": "elementary_5", "semester": 2, "chapter_number": 2, "category": "computation", "part": "calc", "description": "진분수끼리의 곱셈. 분자끼리, 분모끼리 곱한다.", "old_ids": ["e5-2-2-2", "concept-e5-frac-mul-02"]},
    {"id": "e5-2-2-04", "name": "대분수의 곱셈", "grade": "elementary_5", "semester": 2, "chapter_number": 2, "category": "computation", "part": "calc", "description": "대분수를 가분수로 바꾸어 곱하는 계산.", "old_ids": ["e5-2-2-2"]},
    {"id": "e5-2-2-05", "name": "세 분수의 곱셈", "grade": "elementary_5", "semester": 2, "chapter_number": 2, "category": "computation", "part": "calc", "description": "세 분수를 연속으로 곱하는 계산. 중간에 약분하여 계산을 간단히 한다.", "old_ids": ["e5-2-2-2"]},

    # ── 3단원: 합동과 대칭 (4개) ──
    {"id": "e5-2-3-01", "name": "도형의 합동", "grade": "elementary_5", "semester": 2, "chapter_number": 3, "category": "concept", "part": "geo", "description": "합동의 정의(모양과 크기가 같은 도형). 합동인 도형을 찾는다.", "old_ids": ["e5-2-3-1", "concept-e5-congru-01"]},
    {"id": "e5-2-3-02", "name": "합동인 도형의 성질", "grade": "elementary_5", "semester": 2, "chapter_number": 3, "category": "concept", "part": "geo", "description": "대응점, 대응변, 대응각의 개념. 합동인 도형에서 대응하는 요소는 같다.", "old_ids": ["e5-2-3-1"]},
    {"id": "e5-2-3-03", "name": "선대칭도형과 그 성질", "grade": "elementary_5", "semester": 2, "chapter_number": 3, "category": "concept", "part": "geo", "description": "한 직선을 중심으로 접었을 때 완전히 겹치는 도형. 대칭축과 성질을 이해한다.", "old_ids": ["e5-2-3-2", "concept-e5-congru-02"]},
    {"id": "e5-2-3-04", "name": "점대칭도형과 그 성질", "grade": "elementary_5", "semester": 2, "chapter_number": 3, "category": "concept", "part": "geo", "description": "한 점을 중심으로 180° 돌렸을 때 원래 도형과 겹치는 도형. 대칭의 중심과 성질.", "old_ids": ["e5-2-3-2"]},

    # ── 4단원: 소수의 곱셈 (7개) ──
    {"id": "e5-2-4-01", "name": "(1보다 작은 소수)×(자연수)", "grade": "elementary_5", "semester": 2, "chapter_number": 4, "category": "computation", "part": "calc", "description": "0.3×4=1.2처럼 1보다 작은 소수에 자연수를 곱하는 계산.", "old_ids": ["e5-2-4-1", "concept-e5-dec-mul-01"]},
    {"id": "e5-2-4-02", "name": "(1보다 큰 소수)×(자연수)", "grade": "elementary_5", "semester": 2, "chapter_number": 4, "category": "computation", "part": "calc", "description": "2.5×3=7.5처럼 1보다 큰 소수에 자연수를 곱하는 계산.", "old_ids": ["e5-2-4-1"]},
    {"id": "e5-2-4-03", "name": "(자연수)×(1보다 작은 소수)", "grade": "elementary_5", "semester": 2, "chapter_number": 4, "category": "computation", "part": "calc", "description": "자연수에 1보다 작은 소수를 곱하면 원래 수보다 작아짐을 이해한다.", "old_ids": ["e5-2-4-1"]},
    {"id": "e5-2-4-04", "name": "(자연수)×(1보다 큰 소수)", "grade": "elementary_5", "semester": 2, "chapter_number": 4, "category": "computation", "part": "calc", "description": "자연수에 1보다 큰 소수를 곱하면 원래 수보다 커짐을 이해한다.", "old_ids": ["e5-2-4-2", "concept-e5-dec-mul-02"]},
    {"id": "e5-2-4-05", "name": "1보다 작은 소수끼리의 곱셈", "grade": "elementary_5", "semester": 2, "chapter_number": 4, "category": "computation", "part": "calc", "description": "0.3×0.4=0.12처럼 1보다 작은 소수끼리 곱하는 계산.", "old_ids": ["e5-2-4-2"]},
    {"id": "e5-2-4-06", "name": "1보다 큰 소수끼리의 곱셈", "grade": "elementary_5", "semester": 2, "chapter_number": 4, "category": "computation", "part": "calc", "description": "2.5×1.4처럼 1보다 큰 소수끼리 곱하는 계산.", "old_ids": ["e5-2-4-2"]},
    {"id": "e5-2-4-07", "name": "곱의 소수점 위치", "grade": "elementary_5", "semester": 2, "chapter_number": 4, "category": "concept", "part": "calc", "description": "곱의 소수점 아래 자릿수 = 두 수의 소수점 아래 자릿수의 합. 규칙을 이해한다.", "old_ids": ["e5-2-4-2"]},

    # ── 5단원: 직육면체 (6개) ──
    {"id": "e5-2-5-01", "name": "직육면체", "grade": "elementary_5", "semester": 2, "chapter_number": 5, "category": "concept", "part": "geo", "description": "직사각형 6개로 둘러싸인 도형. 면, 모서리, 꼭짓점의 수를 안다.", "old_ids": ["e5-2-5-1", "concept-e5-cuboid-01"]},
    {"id": "e5-2-5-02", "name": "정육면체", "grade": "elementary_5", "semester": 2, "chapter_number": 5, "category": "concept", "part": "geo", "description": "정사각형 6개로 둘러싸인 도형. 직육면체의 특수한 경우임을 이해한다.", "old_ids": ["e5-2-5-1"]},
    {"id": "e5-2-5-03", "name": "직육면체의 성질", "grade": "elementary_5", "semester": 2, "chapter_number": 5, "category": "concept", "part": "geo", "description": "평행한 면, 수직인 면, 평행한 모서리 등 직육면체의 구성 요소 관계를 이해한다.", "old_ids": ["e5-2-5-1"]},
    {"id": "e5-2-5-04", "name": "직육면체의 겨냥도", "grade": "elementary_5", "semester": 2, "chapter_number": 5, "category": "concept", "part": "geo", "description": "직육면체를 보이는 대로 그린 그림. 점선과 실선의 의미를 이해하고 그린다.", "old_ids": ["e5-2-5-2", "concept-e5-cuboid-02"]},
    {"id": "e5-2-5-05", "name": "정육면체의 전개도", "grade": "elementary_5", "semester": 2, "chapter_number": 5, "category": "concept", "part": "geo", "description": "정육면체를 펼친 그림. 11가지 전개도와 접었을 때 마주 보는 면을 이해한다.", "old_ids": ["e5-2-5-2"]},
    {"id": "e5-2-5-06", "name": "직육면체의 전개도", "grade": "elementary_5", "semester": 2, "chapter_number": 5, "category": "concept", "part": "geo", "description": "직육면체를 펼친 그림. 전개도에서 마주 보는 면과 맞닿는 모서리를 파악한다.", "old_ids": ["e5-2-5-2"]},

    # ── 6단원: 평균과 가능성 (6개) ──
    {"id": "e5-2-6-01", "name": "평균", "grade": "elementary_5", "semester": 2, "chapter_number": 6, "category": "concept", "part": "data", "description": "평균의 의미. 자료의 값을 고르게 한 값이 평균임을 이해한다.", "old_ids": ["e5-2-6-1", "concept-e5-avg-01"]},
    {"id": "e5-2-6-02", "name": "평균 구하기", "grade": "elementary_5", "semester": 2, "chapter_number": 6, "category": "computation", "part": "data", "description": "평균 = (자료값의 합) ÷ (자료의 수). 공식으로 평균을 구한다.", "old_ids": ["e5-2-6-1"]},
    {"id": "e5-2-6-03", "name": "평균 이용하기", "grade": "elementary_5", "semester": 2, "chapter_number": 6, "category": "concept", "part": "data", "description": "평균을 이용하여 전체 합이나 모르는 값을 구하는 문제를 해결한다.", "old_ids": ["e5-2-6-1"]},
    {"id": "e5-2-6-04", "name": "일이 일어날 가능성을 말로 표현하기", "grade": "elementary_5", "semester": 2, "chapter_number": 6, "category": "concept", "part": "data", "description": "불가능하다, ~아닐 것 같다, 반반이다, ~일 것 같다, 확실하다로 가능성을 표현한다.", "old_ids": ["e5-2-6-2", "concept-e5-avg-02"]},
    {"id": "e5-2-6-05", "name": "일이 일어날 가능성을 비교하기", "grade": "elementary_5", "semester": 2, "chapter_number": 6, "category": "concept", "part": "data", "description": "두 사건의 가능성을 비교한다. 더 일어나기 쉬운 사건을 판단한다.", "old_ids": ["e5-2-6-2"]},
    {"id": "e5-2-6-06", "name": "일이 일어날 가능성을 수로 표현하기", "grade": "elementary_5", "semester": 2, "chapter_number": 6, "category": "concept", "part": "data", "description": "가능성을 0(불가능)~1(확실) 사이의 수로 표현한다.", "old_ids": ["e5-2-6-2"]},
]

E5_CONCEPTS = E5_S1_CONCEPTS + E5_S2_CONCEPTS


# =============================================
# 초등학교 6학년 1학기
# =============================================

E6_S1_CONCEPTS = [
    # ── 1단원: 분수의 나눗셈 (4개) ──
    {"id": "e6-1-1-01", "name": "(자연수)÷(자연수)의 몫을 분수로 나타내기", "grade": "elementary_6", "semester": 1, "chapter_number": 1, "category": "computation", "part": "calc", "description": "2÷3=2/3처럼 나눗셈의 몫을 분수로 나타내는 원리를 이해한다.", "old_ids": ["e6-1-1-1", "concept-e6-frac-div1"]},
    {"id": "e6-1-1-02", "name": "(분수)÷(자연수)", "grade": "elementary_6", "semester": 1, "chapter_number": 1, "category": "computation", "part": "calc", "description": "분수를 자연수로 나누는 계산. 분자를 나누거나 분모에 곱하는 방법.", "old_ids": ["e6-1-1-1"]},
    {"id": "e6-1-1-03", "name": "(분수)÷(자연수)를 분수의 곱셈으로 나타내기", "grade": "elementary_6", "semester": 1, "chapter_number": 1, "category": "computation", "part": "calc", "description": "÷n = ×(1/n)으로 바꾸는 원리. 나눗셈을 곱셈으로 변환한다.", "old_ids": ["e6-1-1-1"]},
    {"id": "e6-1-1-04", "name": "(대분수)÷(자연수)", "grade": "elementary_6", "semester": 1, "chapter_number": 1, "category": "computation", "part": "calc", "description": "대분수를 가분수로 바꾸어 자연수로 나누는 계산.", "old_ids": ["e6-1-1-1"]},

    # ── 2단원: 각기둥과 각뿔 (6개) ──
    {"id": "e6-1-2-01", "name": "각기둥 알아보기 (1)", "grade": "elementary_6", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "각기둥의 정의와 이름(삼각기둥, 사각기둥 등). 밑면, 옆면, 높이를 안다.", "old_ids": ["e6-1-2-1", "concept-e6-prism-pyramid"]},
    {"id": "e6-1-2-02", "name": "각기둥 알아보기 (2)", "grade": "elementary_6", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "각기둥의 구성 요소(면, 모서리, 꼭짓점)의 수를 규칙적으로 파악한다.", "old_ids": ["e6-1-2-1"]},
    {"id": "e6-1-2-03", "name": "각기둥의 전개도", "grade": "elementary_6", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "각기둥을 펼친 전개도. 밑면 2개와 옆면의 관계를 이해한다.", "old_ids": ["e6-1-2-1"]},
    {"id": "e6-1-2-04", "name": "각기둥의 전개도 그리기", "grade": "elementary_6", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "주어진 각기둥의 전개도를 정확하게 그리는 방법을 익힌다.", "old_ids": ["e6-1-2-1"]},
    {"id": "e6-1-2-05", "name": "각뿔 알아보기 (1)", "grade": "elementary_6", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "각뿔의 정의와 이름(삼각뿔, 사각뿔 등). 밑면, 옆면, 꼭짓점, 높이를 안다.", "old_ids": ["e6-1-2-2"]},
    {"id": "e6-1-2-06", "name": "각뿔 알아보기 (2)", "grade": "elementary_6", "semester": 1, "chapter_number": 2, "category": "concept", "part": "geo", "description": "각뿔의 구성 요소(면, 모서리, 꼭짓점)의 수와 각기둥과의 비교.", "old_ids": ["e6-1-2-2"]},

    # ── 3단원: 소수의 나눗셈 (7개) ──
    {"id": "e6-1-3-01", "name": "자연수의 나눗셈을 이용한 (소수)÷(자연수)", "grade": "elementary_6", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "6.84÷3처럼 자연수 나눗셈 원리를 활용한 소수÷자연수 계산.", "old_ids": ["e6-1-3-1", "concept-e6-dec-div1"]},
    {"id": "e6-1-3-02", "name": "각 자리에서 나누어떨어지지 않는 (소수)÷(자연수)", "grade": "elementary_6", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "각 자리에서 나누어떨어지지 않아 내림이 필요한 소수÷자연수.", "old_ids": ["e6-1-3-1"]},
    {"id": "e6-1-3-03", "name": "몫이 1보다 작은 소수인 (소수)÷(자연수)", "grade": "elementary_6", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "0.48÷6=0.08처럼 몫의 일의 자리가 0인 경우.", "old_ids": ["e6-1-3-1"]},
    {"id": "e6-1-3-04", "name": "소수점 아래 0을 내려 계산하는 (소수)÷(자연수)", "grade": "elementary_6", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "나누어떨어지지 않아 소수점 아래에 0을 보충하여 계속 나누는 계산.", "old_ids": ["e6-1-3-1"]},
    {"id": "e6-1-3-05", "name": "몫의 소수 첫째 자리에 0이 있는 (소수)÷(자연수)", "grade": "elementary_6", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "4.08÷4=1.02처럼 소수 첫째 자리에 0이 들어가는 경우.", "old_ids": ["e6-1-3-1"]},
    {"id": "e6-1-3-06", "name": "(자연수)÷(자연수)의 몫을 소수로 나타내기", "grade": "elementary_6", "semester": 1, "chapter_number": 3, "category": "computation", "part": "calc", "description": "7÷4=1.75처럼 자연수 나눗셈의 몫을 소수로 나타낸다.", "old_ids": ["e6-1-3-1"]},
    {"id": "e6-1-3-07", "name": "몫의 소수점 위치 확인하기", "grade": "elementary_6", "semester": 1, "chapter_number": 3, "category": "concept", "part": "calc", "description": "나누는 수가 같을 때 나뉨수가 1/10이면 몫도 1/10이 되는 규칙.", "old_ids": ["e6-1-3-1"]},

    # ── 4단원: 비와 비율 (6개) ──
    {"id": "e6-1-4-01", "name": "두 수 비교하기", "grade": "elementary_6", "semester": 1, "chapter_number": 4, "category": "concept", "part": "algebra", "description": "두 수를 뺄셈(차)과 나눗셈(몫)으로 비교하는 두 가지 방법을 이해한다.", "old_ids": ["e6-1-4-1", "concept-e6-ratio"]},
    {"id": "e6-1-4-02", "name": "비", "grade": "elementary_6", "semester": 1, "chapter_number": 4, "category": "concept", "part": "algebra", "description": "비의 정의(a:b로 나타내기). 기준량과 비교하는 양, 비의 전항과 후항을 이해한다.", "old_ids": ["e6-1-4-1"]},
    {"id": "e6-1-4-03", "name": "비율", "grade": "elementary_6", "semester": 1, "chapter_number": 4, "category": "concept", "part": "algebra", "description": "비율 = (비교하는 양)÷(기준량). 분수, 소수로 나타낸다.", "old_ids": ["e6-1-4-1"]},
    {"id": "e6-1-4-04", "name": "비율이 사용되는 경우", "grade": "elementary_6", "semester": 1, "chapter_number": 4, "category": "concept", "part": "algebra", "description": "타율, 할인율, 인구 밀도 등 실생활에서 비율이 사용되는 다양한 사례.", "old_ids": ["e6-1-4-1"]},
    {"id": "e6-1-4-05", "name": "백분율", "grade": "elementary_6", "semester": 1, "chapter_number": 4, "category": "concept", "part": "algebra", "description": "비율을 100을 기준으로 나타낸 것. 비율×100=백분율(%).", "old_ids": ["e6-1-4-1"]},
    {"id": "e6-1-4-06", "name": "백분율이 사용되는 경우", "grade": "elementary_6", "semester": 1, "chapter_number": 4, "category": "concept", "part": "algebra", "description": "할인율, 득표율, 습도 등 실생활에서 백분율이 사용되는 사례와 활용.", "old_ids": ["e6-1-4-1"]},

    # ── 5단원: 여러 가지 그래프 (7개) ──
    {"id": "e6-1-5-01", "name": "그림그래프로 나타내기", "grade": "elementary_6", "semester": 1, "chapter_number": 5, "category": "concept", "part": "data", "description": "큰 수의 자료를 그림그래프로 나타내기. 그림 1개가 나타내는 수를 정한다.", "old_ids": ["e6-1-5-1", "concept-e6-graphs"]},
    {"id": "e6-1-5-02", "name": "띠그래프", "grade": "elementary_6", "semester": 1, "chapter_number": 5, "category": "concept", "part": "data", "description": "전체에 대한 각 항목의 비율을 띠 모양에 나타낸 그래프. 구조와 읽기를 익힌다.", "old_ids": ["e6-1-5-1"]},
    {"id": "e6-1-5-03", "name": "띠그래프로 나타내기", "grade": "elementary_6", "semester": 1, "chapter_number": 5, "category": "concept", "part": "data", "description": "자료를 백분율로 구하고 띠그래프로 나타내는 방법.", "old_ids": ["e6-1-5-1"]},
    {"id": "e6-1-5-04", "name": "원그래프", "grade": "elementary_6", "semester": 1, "chapter_number": 5, "category": "concept", "part": "data", "description": "전체에 대한 각 항목의 비율을 원 안에 나타낸 그래프. 구조와 읽기를 익힌다.", "old_ids": ["e6-1-5-2"]},
    {"id": "e6-1-5-05", "name": "원그래프로 나타내기", "grade": "elementary_6", "semester": 1, "chapter_number": 5, "category": "concept", "part": "data", "description": "자료를 백분율로 구하고 원그래프로 나타내는 방법.", "old_ids": ["e6-1-5-2"]},
    {"id": "e6-1-5-06", "name": "그래프 해석하기", "grade": "elementary_6", "semester": 1, "chapter_number": 5, "category": "concept", "part": "data", "description": "띠그래프와 원그래프를 읽고 자료의 특징을 해석한다.", "old_ids": ["e6-1-5-2"]},
    {"id": "e6-1-5-07", "name": "여러 가지 그래프 비교", "grade": "elementary_6", "semester": 1, "chapter_number": 5, "category": "concept", "part": "data", "description": "막대그래프, 꺾은선그래프, 띠그래프, 원그래프의 특징을 비교하고 적합한 그래프를 선택한다.", "old_ids": ["e6-1-5-2"]},

    # ── 6단원: 직육면체의 부피와 겉넓이 (4개) ──
    {"id": "e6-1-6-01", "name": "직육면체의 부피 비교", "grade": "elementary_6", "semester": 1, "chapter_number": 6, "category": "concept", "part": "geo", "description": "단위부피(1cm³)를 이용하여 직육면체의 부피를 비교한다.", "old_ids": ["e6-1-6-2", "concept-e6-volume"]},
    {"id": "e6-1-6-02", "name": "직육면체의 부피 구하는 방법", "grade": "elementary_6", "semester": 1, "chapter_number": 6, "category": "computation", "part": "geo", "description": "직육면체의 부피 = 가로 × 세로 × 높이. 공식을 유도하고 활용한다.", "old_ids": ["e6-1-6-2"]},
    {"id": "e6-1-6-03", "name": "m³ 알아보기", "grade": "elementary_6", "semester": 1, "chapter_number": 6, "category": "concept", "part": "geo", "description": "1m³=1000000cm³. 큰 부피 단위와 단위 환산을 이해한다.", "old_ids": ["e6-1-6-2"]},
    {"id": "e6-1-6-04", "name": "직육면체의 겉넓이 구하는 방법", "grade": "elementary_6", "semester": 1, "chapter_number": 6, "category": "computation", "part": "geo", "description": "직육면체의 겉넓이 = (가로×세로 + 가로×높이 + 세로×높이)×2.", "old_ids": ["e6-1-6-1"]},
]

# =============================================
# 초등학교 6학년 2학기
# =============================================

E6_S2_CONCEPTS = [
    # ── 1단원: 분수의 나눗셈 (6개) ──
    {"id": "e6-2-1-01", "name": "분모가 같은 (분수)÷(분수) (1)", "grade": "elementary_6", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "동분모 분수의 나눗셈. 분자끼리 나누는 원리를 이해한다.", "old_ids": ["e6-2-1-1", "concept-e6-frac-div2"]},
    {"id": "e6-2-1-02", "name": "분모가 같은 (분수)÷(분수) (2)", "grade": "elementary_6", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "분자끼리 나누어떨어지지 않는 동분모 분수 나눗셈.", "old_ids": ["e6-2-1-1"]},
    {"id": "e6-2-1-03", "name": "분모가 다른 (분수)÷(분수)", "grade": "elementary_6", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "통분하여 분모를 같게 한 후 나누는 이분모 분수 나눗셈.", "old_ids": ["e6-2-1-1"]},
    {"id": "e6-2-1-04", "name": "(자연수)÷(분수)", "grade": "elementary_6", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "자연수를 분수로 나누는 계산. 역수를 곱하는 방법.", "old_ids": ["e6-2-1-1"]},
    {"id": "e6-2-1-05", "name": "(분수)÷(분수)를 (분수)×(분수)로 나타내기", "grade": "elementary_6", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "나누는 수의 역수를 곱하면 됨. ÷(a/b) = ×(b/a).", "old_ids": ["e6-2-1-1"]},
    {"id": "e6-2-1-06", "name": "(분수)÷(분수)를 계산하기", "grade": "elementary_6", "semester": 2, "chapter_number": 1, "category": "computation", "part": "calc", "description": "역수를 곱하는 방법으로 다양한 분수 나눗셈을 빠르게 계산한다.", "old_ids": ["e6-2-1-1"]},

    # ── 2단원: 소수의 나눗셈 (6개) ──
    {"id": "e6-2-2-01", "name": "자연수의 나눗셈을 이용한 (소수)÷(소수)", "grade": "elementary_6", "semester": 2, "chapter_number": 2, "category": "computation", "part": "calc", "description": "나뉨수와 나누는 수에 같은 수를 곱하여 자연수 나눗셈으로 바꾸는 원리.", "old_ids": ["e6-2-2-1", "concept-e6-dec-div2"]},
    {"id": "e6-2-2-02", "name": "자릿수가 같은 (소수)÷(소수)", "grade": "elementary_6", "semester": 2, "chapter_number": 2, "category": "computation", "part": "calc", "description": "소수점 아래 자릿수가 같은 소수끼리의 나눗셈.", "old_ids": ["e6-2-2-1"]},
    {"id": "e6-2-2-03", "name": "자릿수가 다른 (소수)÷(소수)", "grade": "elementary_6", "semester": 2, "chapter_number": 2, "category": "computation", "part": "calc", "description": "소수점 아래 자릿수가 다른 소수끼리의 나눗셈. 자릿수를 맞추어 계산한다.", "old_ids": ["e6-2-2-1"]},
    {"id": "e6-2-2-04", "name": "(자연수)÷(소수)", "grade": "elementary_6", "semester": 2, "chapter_number": 2, "category": "computation", "part": "calc", "description": "자연수를 소수로 나누는 계산. 나누는 수를 자연수로 바꾸어 계산한다.", "old_ids": ["e6-2-2-1"]},
    {"id": "e6-2-2-05", "name": "몫을 반올림하여 나타내기", "grade": "elementary_6", "semester": 2, "chapter_number": 2, "category": "computation", "part": "calc", "description": "나누어떨어지지 않는 나눗셈에서 몫을 반올림하여 어림한다.", "old_ids": ["e6-2-2-1"]},
    {"id": "e6-2-2-06", "name": "나누어 주고 남는 양 알아보기", "grade": "elementary_6", "semester": 2, "chapter_number": 2, "category": "concept", "part": "calc", "description": "실생활 나눗셈에서 몫과 나머지의 의미를 이해하고 활용한다.", "old_ids": ["e6-2-2-1"]},

    # ── 3단원: 공간과 입체 (6개) ──
    {"id": "e6-2-3-01", "name": "어느 방향에서 보았는지 알아보기", "grade": "elementary_6", "semester": 2, "chapter_number": 3, "category": "concept", "part": "geo", "description": "쌓기나무로 만든 모양을 위, 앞, 옆에서 본 모양을 이해한다.", "old_ids": ["e6-2-3-1", "concept-e6-spatial"]},
    {"id": "e6-2-3-02", "name": "쌓은 모양과 위에서 본 모양으로 쌓기나무의 개수 알아보기", "grade": "elementary_6", "semester": 2, "chapter_number": 3, "category": "concept", "part": "geo", "description": "위에서 본 모양과 쌓은 모양으로 쌓기나무의 개수를 구한다.", "old_ids": ["e6-2-3-1"]},
    {"id": "e6-2-3-03", "name": "위, 앞, 옆에서 본 모양으로 쌓은 모양과 개수 알아보기", "grade": "elementary_6", "semester": 2, "chapter_number": 3, "category": "concept", "part": "geo", "description": "세 방향의 투영도로 쌓은 모양을 추론하고 쌓기나무의 개수를 구한다.", "old_ids": ["e6-2-3-1"]},
    {"id": "e6-2-3-04", "name": "위에서 본 모양에 수를 써서 쌓은 모양과 개수 알아보기", "grade": "elementary_6", "semester": 2, "chapter_number": 3, "category": "concept", "part": "geo", "description": "위에서 본 모양의 각 칸에 쌓기나무의 수를 써서 나타내는 방법.", "old_ids": ["e6-2-3-1"]},
    {"id": "e6-2-3-05", "name": "층별로 나타낸 모양으로 쌓은 모양과 개수 알아보기", "grade": "elementary_6", "semester": 2, "chapter_number": 3, "category": "concept", "part": "geo", "description": "각 층의 모양을 보고 전체 쌓은 모양과 쌓기나무의 개수를 구한다.", "old_ids": ["e6-2-3-1"]},
    {"id": "e6-2-3-06", "name": "여러 가지 모양 만들기", "grade": "elementary_6", "semester": 2, "chapter_number": 3, "category": "concept", "part": "geo", "description": "주어진 조건에 맞게 쌓기나무로 여러 가지 모양을 만든다.", "old_ids": ["e6-2-3-1"]},

    # ── 4단원: 비례식과 비례배분 (6개) ──
    {"id": "e6-2-4-01", "name": "비의 성질", "grade": "elementary_6", "semester": 2, "chapter_number": 4, "category": "concept", "part": "algebra", "description": "비의 전항과 후항에 0이 아닌 같은 수를 곱하거나 나누어도 비율은 같다.", "old_ids": ["e6-2-4-1", "concept-e6-proportion"]},
    {"id": "e6-2-4-02", "name": "간단한 자연수의 비로 나타내기", "grade": "elementary_6", "semester": 2, "chapter_number": 4, "category": "computation", "part": "algebra", "description": "분수·소수의 비를 간단한 자연수의 비로 변환한다.", "old_ids": ["e6-2-4-1"]},
    {"id": "e6-2-4-03", "name": "비례식", "grade": "elementary_6", "semester": 2, "chapter_number": 4, "category": "concept", "part": "algebra", "description": "비율이 같은 두 비를 등호로 연결한 식. 비례식의 정의와 외항·내항을 이해한다.", "old_ids": ["e6-2-4-1"]},
    {"id": "e6-2-4-04", "name": "비례식의 성질", "grade": "elementary_6", "semester": 2, "chapter_number": 4, "category": "concept", "part": "algebra", "description": "외항의 곱 = 내항의 곱(교차곱). 이를 이용하여 미지수를 구한다.", "old_ids": ["e6-2-4-1"]},
    {"id": "e6-2-4-05", "name": "비례식 활용하기", "grade": "elementary_6", "semester": 2, "chapter_number": 4, "category": "computation", "part": "algebra", "description": "실생활 문제를 비례식으로 세우고 풀이한다.", "old_ids": ["e6-2-4-1"]},
    {"id": "e6-2-4-06", "name": "비례배분", "grade": "elementary_6", "semester": 2, "chapter_number": 4, "category": "computation", "part": "algebra", "description": "전체를 주어진 비로 나누는 비례배분의 원리와 방법.", "old_ids": ["e6-2-4-2"]},

    # ── 5단원: 원의 넓이 (6개) ──
    {"id": "e6-2-5-01", "name": "원주와 지름의 관계", "grade": "elementary_6", "semester": 2, "chapter_number": 5, "category": "concept", "part": "geo", "description": "원주(원의 둘레)와 지름의 관계. 원주÷지름의 값이 일정함을 발견한다.", "old_ids": ["e6-2-5-1", "concept-e6-circle-area"]},
    {"id": "e6-2-5-02", "name": "원주율", "grade": "elementary_6", "semester": 2, "chapter_number": 5, "category": "concept", "part": "geo", "description": "원주율(π)의 의미. 약 3.14 또는 3.1로 어림하여 사용한다.", "old_ids": ["e6-2-5-1"]},
    {"id": "e6-2-5-03", "name": "원주와 지름 구하기", "grade": "elementary_6", "semester": 2, "chapter_number": 5, "category": "computation", "part": "geo", "description": "원주 = 지름 × 원주율, 지름 = 원주 ÷ 원주율. 공식을 활용한다.", "old_ids": ["e6-2-5-1"]},
    {"id": "e6-2-5-04", "name": "원의 넓이 어림하기", "grade": "elementary_6", "semester": 2, "chapter_number": 5, "category": "concept", "part": "geo", "description": "모눈종이를 이용하여 원의 넓이를 어림하는 방법.", "old_ids": ["e6-2-5-2"]},
    {"id": "e6-2-5-05", "name": "원의 넓이 구하는 방법", "grade": "elementary_6", "semester": 2, "chapter_number": 5, "category": "computation", "part": "geo", "description": "원의 넓이 = 반지름 × 반지름 × 원주율. 공식을 유도하고 활용한다.", "old_ids": ["e6-2-5-2"]},
    {"id": "e6-2-5-06", "name": "여러 가지 원의 넓이 구하기", "grade": "elementary_6", "semester": 2, "chapter_number": 5, "category": "computation", "part": "geo", "description": "반원, 부채꼴 등 다양한 원 관련 도형의 넓이를 구한다.", "old_ids": ["e6-2-5-2"]},

    # ── 6단원: 원기둥, 원뿔, 구 (4개) ──
    {"id": "e6-2-6-01", "name": "원기둥", "grade": "elementary_6", "semester": 2, "chapter_number": 6, "category": "concept", "part": "geo", "description": "원기둥의 정의와 구성 요소(밑면 2개, 옆면, 높이). 각기둥과 비교한다.", "old_ids": ["e6-2-6-1", "concept-e6-solids"]},
    {"id": "e6-2-6-02", "name": "원기둥의 전개도", "grade": "elementary_6", "semester": 2, "chapter_number": 6, "category": "concept", "part": "geo", "description": "원기둥의 전개도. 옆면은 직사각형이고 가로=원주, 세로=높이임을 이해한다.", "old_ids": ["e6-2-6-1"]},
    {"id": "e6-2-6-03", "name": "원뿔", "grade": "elementary_6", "semester": 2, "chapter_number": 6, "category": "concept", "part": "geo", "description": "원뿔의 정의와 구성 요소(밑면, 옆면, 꼭짓점, 높이, 모선).", "old_ids": ["e6-2-6-2"]},
    {"id": "e6-2-6-04", "name": "구", "grade": "elementary_6", "semester": 2, "chapter_number": 6, "category": "concept", "part": "geo", "description": "구의 정의(한 점에서 같은 거리에 있는 점의 집합). 반지름과 지름.", "old_ids": ["e6-2-6-2"]},
]

E6_CONCEPTS = E6_S1_CONCEPTS + E6_S2_CONCEPTS


# =============================================
# 집계
# =============================================

ALL_PDF_CONCEPTS = E3_CONCEPTS + E4_CONCEPTS + E5_CONCEPTS + E6_CONCEPTS

# 헬퍼 함수
def get_concepts_by_grade_semester(grade: str, semester: int) -> list[dict]:
    """특정 학년-학기의 개념 목록 반환."""
    return [c for c in ALL_PDF_CONCEPTS if c["grade"] == grade and c["semester"] == semester]

def get_old_to_new_id_map() -> dict[str, list[str]]:
    """기존 ID → 새 ID 매핑 딕셔너리 반환 (마이그레이션용)."""
    mapping: dict[str, list[str]] = {}
    for c in ALL_PDF_CONCEPTS:
        for old_id in c.get("old_ids", []):
            mapping.setdefault(old_id, []).append(c["id"])
    return mapping

def get_chapter_concept_ids(grade: str, semester: int, chapter_number: int) -> list[str]:
    """특정 단원의 개념 ID 목록 반환 (순서대로)."""
    return [
        c["id"] for c in ALL_PDF_CONCEPTS
        if c["grade"] == grade and c["semester"] == semester and c["chapter_number"] == chapter_number
    ]
