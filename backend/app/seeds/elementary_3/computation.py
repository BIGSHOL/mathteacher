"""초등학교 3학년 연산 문제 시드 데이터.

커버 단원:
  1학기 1단원 - 덧셈과 뺄셈
  1학기 3단원 - 나눗셈
  1학기 4단원 - 곱셈
  2학기 7단원 - 곱셈 (2)
  2학기 8단원 - 나눗셈 (2)
"""

from .._base import concept, mc


def get_concepts() -> list[dict]:
    """연산 개념 10개 반환 (단원당 2개)."""
    return [
        # ━━ 1학기 1단원: 덧셈과 뺄셈 ━━
        concept(
            id="concept-e3-add-sub-01",
            name="덧셈과 뺄셈 - 받아올림 있는 덧셈",
            grade="elementary_3",
            category="computation",
            part="calc",
            description="세 자리 수의 덧셈에서 각 자리의 합이 10 이상일 때 상위 자릿수로 1을 올리는 받아올림 원리를 이해합니다.",
        ),
        concept(
            id="concept-e3-add-sub-02",
            name="덧셈과 뺄셈 - 받아내림 있는 뺄셈",
            grade="elementary_3",
            category="computation",
            part="calc",
            description="세 자리 수의 뺄셈에서 상위 자리에서 1을 빌려 10으로 바꾸는 받아내림(재구조화) 원리를 이해합니다.",
        ),
        # ━━ 1학기 4단원: 곱셈 ━━
        concept(
            id="concept-e3-mul1-01",
            name="곱셈 (1) - (몇십몇)×(몇) 기본 계산",
            grade="elementary_3",
            category="computation",
            part="calc",
            description="(몇십몇)×(몇) 계산에서 십의 자리와 일의 자리를 분리하여 각각 곱하는 원리를 이해합니다.",
        ),
        concept(
            id="concept-e3-mul1-02",
            name="곱셈 (1) - 분배법칙의 기초와 올림",
            grade="elementary_3",
            category="computation",
            part="calc",
            description="분배법칙의 기초(23×4=20×4+3×4)를 이해하고, 올림이 있는 곱셈을 정확히 계산합니다.",
        ),
        # ━━ 1학기 3단원: 나눗셈 ━━
        concept(
            id="concept-e3-div1-01",
            name="나눗셈 (1) - 등분제와 포함제",
            grade="elementary_3",
            category="computation",
            part="calc",
            description="등분제(똑같이 나누기)와 포함제(몇 묶음인지 구하기) 두 가지 나눗셈 의미를 이해합니다.",
        ),
        concept(
            id="concept-e3-div1-02",
            name="나눗셈 (1) - 곱셈과 나눗셈의 관계",
            grade="elementary_3",
            category="computation",
            part="calc",
            description="12÷3=4 ↔ 3×4=12와 같이 곱셈과 나눗셈의 역연산 관계를 이해하고, 나눗셈의 교환법칙 불성립을 알아봅니다.",
        ),
        # ━━ 2학기 7단원: 곱셈 (2) ━━
        concept(
            id="concept-e3-mul2-01",
            name="곱셈 (2) - (세 자리 수)×(한 자리 수)",
            grade="elementary_3",
            category="computation",
            part="calc",
            description="(세 자리 수)×(한 자리 수) 세로셈에서 받아올림을 정확히 처리하여 계산합니다.",
        ),
        concept(
            id="concept-e3-mul2-02",
            name="곱셈 (2) - (두 자리 수)×(두 자리 수)",
            grade="elementary_3",
            category="computation",
            part="calc",
            description="(두 자리 수)×(두 자리 수) 세로셈에서 부분 곱을 자릿수에 맞추어 합산하는 알고리즘을 이해합니다.",
        ),
        # ━━ 2학기 8단원: 나눗셈 (2) ━━
        concept(
            id="concept-e3-div2-01",
            name="나눗셈 (2) - 나머지가 있는 나눗셈과 검산",
            grade="elementary_3",
            category="computation",
            part="calc",
            description="나머지가 있는 나눗셈을 계산하고, 검산(A=B×Q+R)과 나머지<나누는 수 조건을 확인합니다.",
        ),
        concept(
            id="concept-e3-div2-02",
            name="나눗셈 (2) - 나머지의 맥락적 해석",
            grade="elementary_3",
            category="computation",
            part="calc",
            description="나머지가 있을 때 올림 상황(텐트 배정)과 버림 상황(사탕 나누기)을 구별하여 해석합니다.",
        ),
    ]


def get_questions() -> list[dict]:
    """연산 문제 50개 반환 (개념당 5개 연산 시드)."""
    return [
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 1단원: 덧셈과 뺄셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-1-1-2-lv03-co-001",
            concept_id="concept-e3-add-sub-02",
            category="computation",
            part="calc",
            difficulty=3,
            content="계산 과정을 보고 틀린 곳을 찾으세요.\n\n  423\n- 157\n-----\n  334\n\n어느 자리에서 처음 실수가 발생했나요?",
            options=[
                "일의 자리",
                "십의 자리",
                "백의 자리",
                "틀린 곳이 없다",
            ],
            correct="A",
            explanation="일의 자리에서 3-7이 안 되니까 십의 자리에서 1을 빌려와야 합니다. "
            "13-7=6이 되어야 하는데, 큰 수-작은 수 규칙을 잘못 적용해 7-3=4로 계산한 오류입니다. (정답: 266)",
        ),
        mc(
            id="e3-1-1-2-lv04-co-001",
            concept_id="concept-e3-add-sub-02",
            category="computation",
            part="calc",
            difficulty=4,
            content="받아내림을 할 때, 십의 자리에서 가져온 수는 실제로 얼마를 의미하나요?\n\n  524\n-  78\n-----",
            options=[
                "1",
                "10",
                "100",
                "0.1",
            ],
            correct="B",
            explanation="십의 자리 숫자 1개는 실제로 10을 의미합니다. "
            "따라서 십의 자리에서 1을 빌려오면 일의 자리에서는 10으로 사용할 수 있습니다. "
            "이것이 자릿값의 핵심 원리입니다.",
        ),
        mc(
            id="e3-1-1-1-lv05-co-001",
            concept_id="concept-e3-add-sub-01",
            category="computation",
            part="calc",
            difficulty=5,
            content="다음 계산에서 받아올림이 일어나는 자리를 모두 고르세요.\n\n  378\n+ 465\n-----",
            options=[
                "일의 자리만",
                "십의 자리만",
                "일의 자리, 십의 자리",
                "백의 자리",
            ],
            correct="C",
            explanation="일의 자리: 8+5=13 (10 이상이므로 받아올림)\n"
            "십의 자리: 7+6+1(받아올림)=14 (10 이상이므로 받아올림)\n"
            "백의 자리: 3+4+1(받아올림)=8 (10 미만이므로 받아올림 없음)\n"
            "따라서 일의 자리와 십의 자리에서 받아올림이 발생합니다.",
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 4단원: 곱셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-1-4-2-lv03-co-001",
            concept_id="concept-e3-mul1-02",
            category="computation",
            part="calc",
            difficulty=3,
            content="23 × 4를 계산하는 과정입니다. 빈칸에 들어갈 알맞은 수는?\n\n23 × 4 = (20 + 3) × 4\n      = 20 × 4 + 3 × 4\n      = 80 + (   )\n      = 92",
            options=[
                "7",
                "12",
                "34",
                "43",
            ],
            correct="B",
            explanation="3 × 4 = 12입니다. "
            "이것이 분배법칙의 기초로, 23을 20과 3으로 나누어 각각 곱한 후 더하는 원리입니다.",
        ),
        mc(
            id="e3-1-4-1-lv04-co-001",
            concept_id="concept-e3-mul1-01",
            category="computation",
            part="calc",
            difficulty=4,
            content="다음 중 46 × 2를 바르게 계산한 것은?",
            options=[
                "40 × 2 + 6 × 2 = 80 + 12 = 92",
                "4 × 2 + 6 × 2 = 8 + 12 = 20",
                "46 × 1 + 46 × 1 = 46 + 46 = 82",
                "460 × 2 = 920",
            ],
            correct="A",
            explanation="46을 40과 6으로 나누어 각각 2를 곱한 후 더해야 합니다. "
            "십의 자리 '4'는 실제로 '40'을 의미하므로 40 × 2 = 80이 되어야 합니다. "
            "'4 × 2 = 8'로 계산하는 것은 자릿수를 무시한 오류입니다.",
        ),
        mc(
            id="e3-1-4-2-lv06-co-001",
            concept_id="concept-e3-mul1-02",
            category="computation",
            part="calc",
            difficulty=6,
            content="모눈종이에서 가로 23칸, 세로 4칸의 직사각형 넓이를 구할 때, "
            "20 × 4 영역과 3 × 4 영역으로 나누어 계산하는 이유는?",
            options=[
                "계산을 빠르게 하기 위해",
                "23을 자릿값에 따라 20과 3으로 나누어 각각 계산하기 위해",
                "4를 2와 2로 나누어 계산하기 위해",
                "모눈종이의 칸 수를 세기 쉽게 하기 위해",
            ],
            correct="B",
            explanation="분배법칙의 시각적 이해를 위한 것입니다. "
            "23 × 4 = (20 + 3) × 4 = 20 × 4 + 3 × 4 원리를 "
            "넓이로 확인할 수 있으며, 십의 자리와 일의 자리를 분리해서 계산하는 알고리즘의 기초가 됩니다.",
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 3단원: 나눗셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-1-3-1-lv03-co-001",
            concept_id="concept-e3-div1-01",
            category="computation",
            part="calc",
            difficulty=3,
            content="사탕 12개를 3명에게 똑같이 나누면 한 명당 몇 개씩인가요?",
            options=[
                "3개",
                "4개",
                "9개",
                "15개",
            ],
            correct="B",
            explanation="12 ÷ 3 = 4입니다. "
            "이것은 '등분제' 나눗셈으로, 전체를 똑같은 수의 묶음으로 나눌 때 한 묶음의 개수를 구하는 것입니다. "
            "12 = 3 × 4로 확인할 수 있습니다.",
        ),
        mc(
            id="e3-1-3-1-lv06-co-001",
            concept_id="concept-e3-div1-01",
            category="computation",
            part="calc",
            difficulty=6,
            content="구슬 20개를 4개씩 묶으면 몇 묶음인가요? 이 상황을 나타내는 나눗셈식은?",
            options=[
                "20 ÷ 5 = 4",
                "20 ÷ 4 = 5",
                "4 ÷ 20 = 0.2",
                "20 - 4 = 16",
            ],
            correct="B",
            explanation="'4개씩 묶으면 몇 묶음?'은 포함제 나눗셈입니다. "
            "전체 20개를 한 묶음 4개씩 덜어내면 5묶음이 됩니다. "
            "20 ÷ 4 = 5에서 몫 5의 단위는 '묶음'입니다.",
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 7단원: 곱셈 (2)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-2-1-2-lv05-co-001",
            concept_id="concept-e3-mul2-02",
            category="computation",
            part="calc",
            difficulty=5,
            content="34 × 12를 계산할 때, 다음 중 옳은 과정은?",
            options=[
                "34 × 2 + 34 × 1 = 68 + 34 = 102",
                "34 × 2 + 34 × 10 = 68 + 340 = 408",
                "3 × 12 + 4 × 12 = 36 + 48 = 84",
                "34 + 12 = 46",
            ],
            correct="B",
            explanation="12 = 10 + 2로 나누어야 합니다. "
            "12의 십의 자리 '1'은 실제로 '10'을 의미하므로 34 × 10 = 340이 되어야 합니다. "
            "'34 × 1 = 34'로 계산하는 것은 자릿수를 무시한 오류입니다.",
        ),
        mc(
            id="e3-2-1-1-lv06-co-001",
            concept_id="concept-e3-mul2-01",
            category="computation",
            part="calc",
            difficulty=6,
            content="세로셈으로 계산할 때 빈칸에 들어갈 수는?\n\n    2 3\n  ×  4\n  -----\n    (  )",
            options=[
                "812",
                "92",
                "82",
                "102",
            ],
            correct="B",
            explanation="23 × 4 = (20 + 3) × 4 = 80 + 12 = 92입니다. "
            "'3 × 4 = 12, 2 × 4 = 8'을 나열해 812로 쓰는 것은 오류입니다. "
            "일의 자리 계산 결과 12에서 1을 십의 자리로 받아올려야 합니다.",
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 8단원: 나눗셈 (2)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━
        mc(
            id="e3-2-2-1-lv04-co-001",
            concept_id="concept-e3-div2-01",
            category="computation",
            part="calc",
            difficulty=4,
            content="14 ÷ 3의 나머지는?",
            options=[
                "1",
                "2",
                "3",
                "5",
            ],
            correct="B",
            explanation="14 ÷ 3 = 4 ... 2입니다. "
            "3 × 4 = 12이고, 14 - 12 = 2가 남습니다. "
            "검산: 3 × 4 + 2 = 14 (맞음)\n"
            "나머지는 항상 나누는 수보다 작아야 합니다 (2 < 3).",
        ),
        mc(
            id="e3-2-2-1-lv06-co-001",
            concept_id="concept-e3-div2-01",
            category="computation",
            part="calc",
            difficulty=6,
            content="다음 계산이 틀린 이유를 설명하세요.\n\n14 ÷ 3 = 3 ... 5",
            options=[
                "몫이 틀렸다 (4가 되어야 함)",
                "나머지가 나누는 수 3보다 크거나 같다",
                "계산식 자체가 성립하지 않는다",
                "나눗셈은 나머지가 있을 수 없다",
            ],
            correct="B",
            explanation="나머지는 항상 나누는 수보다 작아야 합니다. "
            "나머지가 5라면 3을 한 번 더 덜어낼 수 있으므로 몫이 3이 아니라 4가 되어야 합니다. "
            "나머지 < 나누는 수 (R < B) 조건을 항상 확인해야 합니다.",
        ),
        mc(
            id="e3-2-2-2-lv08-co-001",
            concept_id="concept-e3-div2-02",
            category="computation",
            part="calc",
            difficulty=8,
            content="학생 14명을 3명씩 텐트에 배정하려고 합니다. 텐트는 최소 몇 개 필요한가요?",
            options=[
                "3개",
                "4개",
                "5개",
                "6개",
            ],
            correct="C",
            explanation="14 ÷ 3 = 4 ... 2입니다. "
            "4개 텐트에 12명이 들어가고 2명이 남습니다. "
            "남는 2명도 텐트가 필요하므로 1개를 더 준비해야 합니다. "
            "이것은 '올림 상황'으로, 나머지가 있으면 몫에 1을 더해야 합니다. (정답: 5개)",
        ),
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 추가 연산 시드 (개념당 5개 달성용)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # ── 받아올림 있는 덧셈 (concept-e3-add-sub-01) ──
        mc(
            id="e3-1-1-1-lv03-co-001",
            concept_id="concept-e3-add-sub-01",
            category="computation",
            part="calc",
            difficulty=3,
            content="345 + 278 = ?",
            options=["623", "613", "523", "633"],
            correct="A",
            explanation="일의 자리: 5+8=13 → 3 쓰고 1 올림. "
            "십의 자리: 4+7+1=12 → 2 쓰고 1 올림. 백의 자리: 3+2+1=6. 답: 623",
        ),
        mc(
            id="e3-1-1-1-lv04-co-001",
            concept_id="concept-e3-add-sub-01",
            category="computation",
            part="calc",
            difficulty=4,
            content="167 + 458 = ?",
            options=["625", "615", "525", "635"],
            correct="A",
            explanation="일의 자리: 7+8=15 → 5 쓰고 1 올림. "
            "십의 자리: 6+5+1=12 → 2 쓰고 1 올림. 백의 자리: 1+4+1=6. 답: 625",
        ),
        mc(
            id="e3-1-1-1-lv05-co-002",
            concept_id="concept-e3-add-sub-01",
            category="computation",
            part="calc",
            difficulty=5,
            content="589 + 347 = ?",
            options=["936", "826", "926", "836"],
            correct="A",
            explanation="일의 자리: 9+7=16 → 6 쓰고 1 올림. "
            "십의 자리: 8+4+1=13 → 3 쓰고 1 올림. 백의 자리: 5+3+1=9. 답: 936",
        ),
        mc(
            id="e3-1-1-1-lv06-co-001",
            concept_id="concept-e3-add-sub-01",
            category="computation",
            part="calc",
            difficulty=6,
            content="476 + 358 = ?",
            options=["834", "724", "824", "734"],
            correct="A",
            explanation="일의 자리: 6+8=14 → 4 쓰고 1 올림. "
            "십의 자리: 7+5+1=13 → 3 쓰고 1 올림. 백의 자리: 4+3+1=8. 답: 834",
        ),
        # ── 받아내림 있는 뺄셈 (concept-e3-add-sub-02) ──
        mc(
            id="e3-1-1-2-lv03-co-002",
            concept_id="concept-e3-add-sub-02",
            category="computation",
            part="calc",
            difficulty=3,
            content="500 - 263 = ?",
            options=["237", "337", "247", "257"],
            correct="A",
            explanation="500에서 빌려오기: 일의 자리 10-3=7, 십의 자리 9-6=3, 백의 자리 4-2=2. 답: 237",
        ),
        mc(
            id="e3-1-1-2-lv05-co-001",
            concept_id="concept-e3-add-sub-02",
            category="computation",
            part="calc",
            difficulty=5,
            content="724 - 358 = ?",
            options=["366", "434", "376", "466"],
            correct="A",
            explanation="일의 자리: 14-8=6(받아내림). "
            "십의 자리: 11-5=6(받아내림). 백의 자리: 6-3=3. 답: 366",
        ),
        mc(
            id="e3-1-1-2-lv06-co-001",
            concept_id="concept-e3-add-sub-02",
            category="computation",
            part="calc",
            difficulty=6,
            content="803 - 467 = ?",
            options=["336", "444", "346", "436"],
            correct="A",
            explanation="십의 자리가 0이므로 백의 자리에서 빌려옴. "
            "일의 자리: 13-7=6, 십의 자리: 9-6=3, 백의 자리: 7-4=3. 답: 336",
        ),
        # ── (몇십몇)×(몇) 기본 계산 (concept-e3-mul1-01) ──
        mc(
            id="e3-1-4-1-lv03-co-001",
            concept_id="concept-e3-mul1-01",
            category="computation",
            part="calc",
            difficulty=3,
            content="32 × 3 = ?",
            options=["96", "36", "69", "86"],
            correct="A",
            explanation="30×3=90, 2×3=6. 90+6=96",
        ),
        mc(
            id="e3-1-4-1-lv04-co-002",
            concept_id="concept-e3-mul1-01",
            category="computation",
            part="calc",
            difficulty=4,
            content="27 × 3 = ?",
            options=["81", "71", "63", "91"],
            correct="A",
            explanation="20×3=60, 7×3=21. 60+21=81",
        ),
        mc(
            id="e3-1-4-1-lv05-co-001",
            concept_id="concept-e3-mul1-01",
            category="computation",
            part="calc",
            difficulty=5,
            content="15 × 6 = ?",
            options=["90", "80", "60", "96"],
            correct="A",
            explanation="10×6=60, 5×6=30. 60+30=90",
        ),
        mc(
            id="e3-1-4-1-lv06-co-001",
            concept_id="concept-e3-mul1-01",
            category="computation",
            part="calc",
            difficulty=6,
            content="38 × 7 = ?",
            options=["266", "246", "256", "276"],
            correct="A",
            explanation="30×7=210, 8×7=56. 210+56=266",
        ),
        # ── 분배법칙의 기초와 올림 (concept-e3-mul1-02) ──
        mc(
            id="e3-1-4-2-lv04-co-001",
            concept_id="concept-e3-mul1-02",
            category="computation",
            part="calc",
            difficulty=4,
            content="37 × 5 = ?",
            options=["185", "175", "195", "155"],
            correct="A",
            explanation="30×5=150, 7×5=35. 150+35=185",
        ),
        mc(
            id="e3-1-4-2-lv05-co-001",
            concept_id="concept-e3-mul1-02",
            category="computation",
            part="calc",
            difficulty=5,
            content="48 × 6 = ?",
            options=["288", "248", "268", "298"],
            correct="A",
            explanation="40×6=240, 8×6=48. 240+48=288",
        ),
        mc(
            id="e3-1-4-2-lv07-co-001",
            concept_id="concept-e3-mul1-02",
            category="computation",
            part="calc",
            difficulty=7,
            content="56 × 8 = ?",
            options=["448", "408", "468", "428"],
            correct="A",
            explanation="50×8=400, 6×8=48. 400+48=448",
        ),
        # ── 등분제와 포함제 (concept-e3-div1-01) ──
        mc(
            id="e3-1-3-1-lv03-co-002",
            concept_id="concept-e3-div1-01",
            category="computation",
            part="calc",
            difficulty=3,
            content="36 ÷ 4 = ?",
            options=["9", "8", "7", "6"],
            correct="A",
            explanation="4 × 9 = 36이므로 36 ÷ 4 = 9",
        ),
        mc(
            id="e3-1-3-1-lv04-co-001",
            concept_id="concept-e3-div1-01",
            category="computation",
            part="calc",
            difficulty=4,
            content="56 ÷ 8 = ?",
            options=["7", "6", "8", "9"],
            correct="A",
            explanation="8 × 7 = 56이므로 56 ÷ 8 = 7",
        ),
        mc(
            id="e3-1-3-1-lv05-co-001",
            concept_id="concept-e3-div1-01",
            category="computation",
            part="calc",
            difficulty=5,
            content="72 ÷ 9 = ?",
            options=["8", "7", "9", "6"],
            correct="A",
            explanation="9 × 8 = 72이므로 72 ÷ 9 = 8",
        ),
        # ── 곱셈과 나눗셈의 관계 (concept-e3-div1-02) ──
        mc(
            id="e3-1-3-2-lv03-co-001",
            concept_id="concept-e3-div1-02",
            category="computation",
            part="calc",
            difficulty=3,
            content="□ × 6 = 42일 때, □에 들어갈 수는?",
            options=["7", "6", "8", "9"],
            correct="A",
            explanation="42 ÷ 6 = 7. 곱셈의 빈칸은 나눗셈으로 구합니다.",
        ),
        mc(
            id="e3-1-3-2-lv04-co-001",
            concept_id="concept-e3-div1-02",
            category="computation",
            part="calc",
            difficulty=4,
            content="63 ÷ □ = 9일 때, □에 들어갈 수는?",
            options=["7", "8", "6", "9"],
            correct="A",
            explanation="□ × 9 = 63이므로 □ = 63 ÷ 9 = 7",
        ),
        mc(
            id="e3-1-3-2-lv05-co-001",
            concept_id="concept-e3-div1-02",
            category="computation",
            part="calc",
            difficulty=5,
            content="□ ÷ 8 = 5일 때, □에 들어갈 수는?",
            options=["40", "35", "45", "48"],
            correct="A",
            explanation="□ = 8 × 5 = 40. 나눗셈의 나뉨수는 나누는 수 × 몫으로 구합니다.",
        ),
        mc(
            id="e3-1-3-2-lv06-co-001",
            concept_id="concept-e3-div1-02",
            category="computation",
            part="calc",
            difficulty=6,
            content="54 ÷ 6 = □, □ × 4 = △일 때, △은?",
            options=["36", "24", "32", "28"],
            correct="A",
            explanation="54 ÷ 6 = 9, 9 × 4 = 36",
        ),
        mc(
            id="e3-1-3-2-lv07-co-001",
            concept_id="concept-e3-div1-02",
            category="computation",
            part="calc",
            difficulty=7,
            content="어떤 수에 5를 곱했더니 45가 되었습니다. 어떤 수를 3으로 나누면?",
            options=["3", "5", "9", "15"],
            correct="A",
            explanation="어떤 수 × 5 = 45이므로 어떤 수 = 45 ÷ 5 = 9. 9 ÷ 3 = 3",
        ),
        # ── (세 자리 수)×(한 자리 수) (concept-e3-mul2-01) ──
        mc(
            id="e3-2-1-1-lv04-co-001",
            concept_id="concept-e3-mul2-01",
            category="computation",
            part="calc",
            difficulty=4,
            content="123 × 4 = ?",
            options=["492", "482", "512", "432"],
            correct="A",
            explanation="100×4=400, 20×4=80, 3×4=12. 400+80+12=492",
        ),
        mc(
            id="e3-2-1-1-lv05-co-001",
            concept_id="concept-e3-mul2-01",
            category="computation",
            part="calc",
            difficulty=5,
            content="256 × 3 = ?",
            options=["768", "668", "778", "758"],
            correct="A",
            explanation="200×3=600, 50×3=150, 6×3=18. 600+150+18=768",
        ),
        mc(
            id="e3-2-1-1-lv06-co-002",
            concept_id="concept-e3-mul2-01",
            category="computation",
            part="calc",
            difficulty=6,
            content="315 × 7 = ?",
            options=["2205", "2105", "2215", "2195"],
            correct="A",
            explanation="300×7=2100, 10×7=70, 5×7=35. 2100+70+35=2205",
        ),
        mc(
            id="e3-2-1-1-lv07-co-001",
            concept_id="concept-e3-mul2-01",
            category="computation",
            part="calc",
            difficulty=7,
            content="407 × 5 = ?",
            options=["2035", "2005", "2045", "2350"],
            correct="A",
            explanation="400×5=2000, 0×5=0, 7×5=35. 2000+0+35=2035",
        ),
        # ── (두 자리 수)×(두 자리 수) (concept-e3-mul2-02) ──
        mc(
            id="e3-2-1-2-lv05-co-002",
            concept_id="concept-e3-mul2-02",
            category="computation",
            part="calc",
            difficulty=5,
            content="25 × 13 = ?",
            options=["325", "275", "350", "300"],
            correct="A",
            explanation="25×3=75, 25×10=250. 75+250=325",
        ),
        mc(
            id="e3-2-1-2-lv06-co-001",
            concept_id="concept-e3-mul2-02",
            category="computation",
            part="calc",
            difficulty=6,
            content="34 × 21 = ?",
            options=["714", "680", "744", "614"],
            correct="A",
            explanation="34×1=34, 34×20=680. 34+680=714",
        ),
        mc(
            id="e3-2-1-2-lv07-co-001",
            concept_id="concept-e3-mul2-02",
            category="computation",
            part="calc",
            difficulty=7,
            content="42 × 15 = ?",
            options=["630", "620", "650", "580"],
            correct="A",
            explanation="42×5=210, 42×10=420. 210+420=630",
        ),
        mc(
            id="e3-2-1-2-lv08-co-001",
            concept_id="concept-e3-mul2-02",
            category="computation",
            part="calc",
            difficulty=8,
            content="17 × 23 = ?",
            options=["391", "371", "381", "401"],
            correct="A",
            explanation="17×3=51, 17×20=340. 51+340=391",
        ),
        # ── 나머지가 있는 나눗셈과 검산 (concept-e3-div2-01) ──
        mc(
            id="e3-2-2-1-lv04-co-002",
            concept_id="concept-e3-div2-01",
            category="computation",
            part="calc",
            difficulty=4,
            content="29 ÷ 6의 몫과 나머지를 차례로 구하면?",
            options=[
                "몫 4, 나머지 5",
                "몫 5, 나머지 1",
                "몫 3, 나머지 11",
                "몫 4, 나머지 6",
            ],
            correct="A",
            explanation="6 × 4 = 24, 29 - 24 = 5. 검산: 6 × 4 + 5 = 29 ✓",
        ),
        mc(
            id="e3-2-2-1-lv05-co-001",
            concept_id="concept-e3-div2-01",
            category="computation",
            part="calc",
            difficulty=5,
            content="47 ÷ 8의 나머지는?",
            options=["7", "5", "3", "1"],
            correct="A",
            explanation="8 × 5 = 40, 47 - 40 = 7. 검산: 8 × 5 + 7 = 47 ✓",
        ),
        mc(
            id="e3-2-2-1-lv06-co-002",
            concept_id="concept-e3-div2-01",
            category="computation",
            part="calc",
            difficulty=6,
            content="65 ÷ 7의 몫은?",
            options=["9", "8", "10", "7"],
            correct="A",
            explanation="7 × 9 = 63, 65 - 63 = 2. 나머지 2 < 나누는 수 7 ✓. 몫은 9",
        ),
        # ── 나머지의 맥락적 해석 (concept-e3-div2-02) ──
        mc(
            id="e3-2-2-2-lv05-co-001",
            concept_id="concept-e3-div2-02",
            category="computation",
            part="calc",
            difficulty=5,
            content="25명이 4인승 보트를 타려고 합니다. 보트는 최소 몇 대 필요한가요?",
            options=["7대", "6대", "5대", "8대"],
            correct="A",
            explanation="25 ÷ 4 = 6 ... 1. 남은 1명도 보트가 필요하므로 6+1=7대 (올림 상황)",
        ),
        mc(
            id="e3-2-2-2-lv05-co-002",
            concept_id="concept-e3-div2-02",
            category="computation",
            part="calc",
            difficulty=5,
            content="사탕 23개를 5명에게 똑같이 나누면 한 명은 최대 몇 개 받나요?",
            options=["4개", "5개", "3개", "6개"],
            correct="A",
            explanation="23 ÷ 5 = 4 ... 3. 나머지 3개는 더 나눌 수 없으므로 한 명당 4개 (버림 상황)",
        ),
        mc(
            id="e3-2-2-2-lv06-co-001",
            concept_id="concept-e3-div2-02",
            category="computation",
            part="calc",
            difficulty=6,
            content="리본 38cm를 7cm씩 자르면 최대 몇 도막을 만들 수 있나요?",
            options=["5도막", "6도막", "4도막", "7도막"],
            correct="A",
            explanation="38 ÷ 7 = 5 ... 3. 남은 3cm로는 7cm 도막을 만들 수 없으므로 5도막 (버림 상황)",
        ),
        mc(
            id="e3-2-2-2-lv07-co-001",
            concept_id="concept-e3-div2-02",
            category="computation",
            part="calc",
            difficulty=7,
            content="학생 33명이 8인승 차를 타려고 합니다. 차는 최소 몇 대 필요한가요?",
            options=["5대", "4대", "3대", "6대"],
            correct="A",
            explanation="33 ÷ 8 = 4 ... 1. 남은 1명도 차가 필요하므로 4+1=5대 (올림 상황)",
        ),
    ]
