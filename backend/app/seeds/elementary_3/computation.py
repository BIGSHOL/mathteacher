"""초등학교 3학년 연산 문제 시드 데이터.

커버 단원 (PDF 기반 세분화):
  1학기 1단원 - 덧셈과 뺄셈 (6개 개념)
  1학기 3단원 - 나눗셈 (4개 개념)
  1학기 4단원 - 곱셈 (5개 개념)
  2학기 1단원 - 곱셈 (7개 개념)
  2학기 2단원 - 나눗셈 (8개 개념)
"""

from .._base import concept, mc, fb


def get_concepts() -> list[dict]:
    """연산 개념 30개 반환 (PDF 기반 세분화)."""
    from app.data.pdf_concept_map import E3_S1_CONCEPTS, E3_S2_CONCEPTS

    comp_s1 = {1, 3, 4}  # 1학기 연산 단원
    comp_s2 = {1, 2}     # 2학기 연산 단원
    result = []
    for c in E3_S1_CONCEPTS:
        if c["chapter_number"] in comp_s1:
            result.append(concept(
                id=c["id"], name=c["name"], grade=c["grade"],
                category=c["category"], part=c["part"], description=c["description"],
            ))
    for c in E3_S2_CONCEPTS:
        if c["chapter_number"] in comp_s2:
            result.append(concept(
                id=c["id"], name=c["name"], grade=c["grade"],
                category=c["category"], part=c["part"], description=c["description"],
            ))
    return result


def get_questions() -> list[dict]:
    """연산 문제 반환."""
    return [
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 1단원: 덧셈과 뺄셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e3-1-1-01: 받아올림 없는 덧셈 ──
        mc(
            id="e3-1-1-1-cc-002", concept_id="e3-1-1-01",
            category="concept", part="calc", difficulty=1,
            content="$234 + 5$를 세로셈으로 계산하려고 합니다. 숫자 5는 어느 자리 숫자 밑에 써야 하나요?",
            options=["백의 자리 (2 밑에)", "십의 자리 (3 밑에)", "일의 자리 (4 밑에)", "아무 곳이나"],
            correct="C",
            explanation="덧셈은 같은 자리 수끼리 계산해야 하므로, 일의 자리 숫자인 5는 234의 일의 자리인 4 밑에 맞춰 써야 합니다.",
            hint="일의 자리는 일의 자리끼리 더해야 해요.",
        ),
        fb(
            id="e3-1-1-1-fb-001", concept_id="e3-1-1-01",
            category="concept", part="calc", difficulty=1,
            content="덧셈을 할 때는 자릿수를 맞추어 쓰고, **( )**의 자리부터 순서대로 계산합니다.",
            answer="일",
            explanation="덧셈의 계산 순서는 일의 자리 → 십의 자리 → 백의 자리 순서입니다.",
            hint="가장 작은 자릿수부터 계산해요.",
        ),
        mc(
            id="e3-1-1-01-co-001", concept_id="e3-1-1-01",
            category="computation", part="calc", difficulty=2,
            content="321 + 245 = ?",
            options=["566", "556", "576", "466"],
            correct="A",
            explanation="일의 자리: 1+5=6, 십의 자리: 2+4=6, 백의 자리: 3+2=5. 답: 566. 각 자리 합이 10 미만이므로 받아올림 없음.",
        ),

        # ── e3-1-1-02: 받아올림 1번 ──
        mc(
            id="e3-1-1-1-cc-003", concept_id="e3-1-1-02",
            category="concept", part="calc", difficulty=2,
            content="일의 자리끼리의 합이 14가 되었습니다. 올바른 계산 방법은?",
            options=[
                "일의 자리에 14를 다 쓴다.",
                "4는 일의 자리에, 10은 십의 자리로 올린다.",
                "1은 일의 자리에, 4는 십의 자리로 올린다.",
                "그냥 4만 쓴다.",
            ],
            correct="B",
            explanation="합이 10이 넘으면 10을 바로 윗자리(십의 자리)로 1만큼 받아올림하고, 나머지(4)만 해당 자리에 씁니다.",
            hint="14는 10과 4로 나눌 수 있어요.",
        ),
        fb(
            id="e3-1-1-1-fb-002", concept_id="e3-1-1-02",
            category="concept", part="calc", difficulty=2,
            content="각 자리의 합이 **( )**이거나 그보다 크면 바로 윗자리로 1을 받아올림합니다.",
            answer="10",
            explanation="받아올림의 기준이 되는 수는 10입니다.",
            hint="우리는 십진법을 사용해요.",
        ),
        mc(
            id="e3-1-1-02-co-001", concept_id="e3-1-1-02",
            category="computation", part="calc", difficulty=3,
            content="352 + 219 = ?",
            options=["571", "561", "581", "471"],
            correct="A",
            explanation="일의 자리: 2+9=11 → 1 쓰고 1 올림. 십의 자리: 5+1+1=7. 백의 자리: 3+2=5. 답: 571",
        ),

        # ── e3-1-1-03: 받아올림 여러 번 ──
        mc(
            id="e3-1-1-1-cc-001", concept_id="e3-1-1-03",
            category="concept", part="calc", difficulty=5,
            content="다음 계산에서 받아올림이 일어나는 자리를 모두 고르세요.\n\n  378\n+ 465\n-----",
            options=["일의 자리만", "십의 자리만", "일의 자리, 십의 자리", "백의 자리"],
            correct="C",
            explanation="일의 자리: 8+5=13 (받아올림)\n십의 자리: 7+6+1=14 (받아올림)\n백의 자리: 3+4+1=8 (받아올림 없음)",
        ),
        mc(
            id="e3-1-1-1-cc-004", concept_id="e3-1-1-03",
            category="concept", part="calc", difficulty=3,
            content="$587 + 346$에서 십의 자리 계산 $(1+8+4)$의 합이 13입니다. 백의 자리에 어떻게 표시하나요?",
            options=["백의 자리 위로 1을 올린다.", "백의 자리에 그냥 13을 쓴다.", "받아올림하지 않고 버린다.", "일의 자리로 1을 내린다."],
            correct="A",
            explanation="십의 자리 합이 13이므로 10은 백의 자리로 받아올림하여 '1'로 표시합니다.",
            hint="십의 자리 13개는 100이 1개, 10이 3개인 것과 같아요.",
        ),
        fb(
            id="e3-1-1-1-fb-003", concept_id="e3-1-1-03",
            category="concept", part="calc", difficulty=3,
            content="받아올림이 여러 번 있어도, 합이 10이 넘으면 계속 **( )**자리로 1을 올려줍니다.",
            answer="윗",
            explanation="받아올림은 항상 바로 윗자리로 올려줍니다.",
            accept_formats=["윗", "앞", "다음"],
            hint="지금 계산하는 자리보다 더 큰 자리로 보내야 해요.",
        ),
        mc(
            id="e3-1-1-1-co-002", concept_id="e3-1-1-03",
            category="computation", part="calc", difficulty=3,
            content="345 + 278 = ?",
            options=["623", "613", "523", "633"],
            correct="A",
            explanation="일의 자리: 5+8=13 → 3 쓰고 1 올림. 십의 자리: 4+7+1=12 → 2 쓰고 1 올림. 백의 자리: 3+2+1=6. 답: 623",
        ),
        mc(
            id="e3-1-1-1-co-003", concept_id="e3-1-1-03",
            category="computation", part="calc", difficulty=4,
            content="167 + 458 = ?",
            options=["625", "615", "525", "635"],
            correct="A",
            explanation="일의 자리: 7+8=15 → 5 쓰고 1 올림. 십의 자리: 6+5+1=12 → 2 쓰고 1 올림. 백의 자리: 1+4+1=6. 답: 625",
        ),
        mc(
            id="e3-1-1-1-co-004", concept_id="e3-1-1-03",
            category="computation", part="calc", difficulty=5,
            content="589 + 347 = ?",
            options=["936", "826", "926", "836"],
            correct="A",
            explanation="일의 자리: 9+7=16 → 6 쓰고 1 올림. 십의 자리: 8+4+1=13 → 3 쓰고 1 올림. 백의 자리: 5+3+1=9. 답: 936",
        ),
        mc(
            id="e3-1-1-1-co-005", concept_id="e3-1-1-03",
            category="computation", part="calc", difficulty=6,
            content="476 + 358 = ?",
            options=["834", "724", "824", "734"],
            correct="A",
            explanation="일의 자리: 6+8=14 → 4 쓰고 1 올림. 십의 자리: 7+5+1=13 → 3 쓰고 1 올림. 백의 자리: 4+3+1=8. 답: 834",
        ),

        # ── e3-1-1-04: 받아내림 없는 뺄셈 ──
        mc(
            id="e3-1-1-2-cc-003", concept_id="e3-1-1-04",
            category="concept", part="calc", difficulty=1,
            content="뺄셈 $456 - 123$을 계산할 때 가장 먼저 계산하는 것은?",
            options=["$4 - 1$", "$5 - 2$", "$6 - 3$", "$456 - 100$"],
            correct="C",
            explanation="뺄셈도 덧셈과 마찬가지로 일의 자리($6-3$)부터 계산합니다.",
            hint="덧셈과 순서가 같아요.",
        ),
        fb(
            id="e3-1-1-2-fb-001", concept_id="e3-1-1-04",
            category="concept", part="calc", difficulty=1,
            content="뺄셈을 계산할 때는 **( )**의 자리부터 순서대로 계산합니다.",
            answer="일",
            explanation="자릿수를 맞추어 쓰고 일의 자리부터 차례대로 뺍니다.",
            hint="가장 작은 자리부터 계산해요.",
        ),
        mc(
            id="e3-1-1-04-co-001", concept_id="e3-1-1-04",
            category="computation", part="calc", difficulty=2,
            content="687 - 253 = ?",
            options=["434", "444", "424", "534"],
            correct="A",
            explanation="일의 자리: 7-3=4, 십의 자리: 8-5=3, 백의 자리: 6-2=4. 답: 434. 받아내림 없음.",
        ),

        # ── e3-1-1-05: 받아내림 1번 ──
        mc(
            id="e3-1-1-2-cc-001", concept_id="e3-1-1-05",
            category="concept", part="calc", difficulty=3,
            content="계산 과정을 보고 틀린 곳을 찾으세요.\n\n  423\n- 157\n-----\n  334\n\n어느 자리에서 처음 실수가 발생했나요?",
            options=["일의 자리", "십의 자리", "백의 자리", "틀린 곳이 없다"],
            correct="A",
            explanation="일의 자리에서 3-7이 안 되니까 십의 자리에서 1을 빌려와야 합니다. "
            "13-7=6이 되어야 하는데, 큰 수-작은 수 규칙을 잘못 적용해 7-3=4로 계산한 오류입니다. (정답: 266)",
        ),
        mc(
            id="e3-1-1-2-cc-002", concept_id="e3-1-1-05",
            category="concept", part="calc", difficulty=4,
            content="받아내림을 할 때, 십의 자리에서 가져온 수는 실제로 얼마를 의미하나요?\n\n  524\n-  78\n-----",
            options=["1", "10", "100", "0.1"],
            correct="B",
            explanation="십의 자리 숫자 1개는 실제로 10을 의미합니다. 따라서 십의 자리에서 1을 빌려오면 일의 자리에서는 10으로 사용합니다.",
        ),
        mc(
            id="e3-1-1-2-cc-004", concept_id="e3-1-1-05",
            category="concept", part="calc", difficulty=2,
            content="일의 자리끼리 뺄 수 없을 때(예: $2-8$) 가장 먼저 해야 할 일은?",
            options=["그냥 $8-2$를 한다.", "십의 자리에서 10을 빌려온다.", "백의 자리에서 100을 빌려온다.", "계산을 포기한다."],
            correct="B",
            explanation="뺄 수 없을 때는 바로 윗자리(십의 자리)에서 1을 받아내림하면 10이 됩니다.",
            hint="작은 수에서 큰 수를 뺄 수 없을 때는 옆집에서 빌려와야 해요.",
        ),
        fb(
            id="e3-1-1-2-fb-002", concept_id="e3-1-1-05",
            category="concept", part="calc", difficulty=2,
            content="뺄 수 없을 때는 윗자리에서 **( )**을 받아내림하여 계산합니다.",
            answer="10",
            explanation="윗자리의 1은 아랫자리의 10과 같습니다.",
            hint="십의 자리 모형 1개는 일의 자리 모형 10개와 같아요.",
        ),

        # ── e3-1-1-06: 받아내림 2번 ──
        mc(
            id="e3-1-1-2-cc-005", concept_id="e3-1-1-06",
            category="concept", part="calc", difficulty=3,
            content="$624 - 357$처럼 일, 십의 자리 모두 뺄 수 없을 때 빌려오는 순서는?",
            options=["십의 자리 → 백의 자리 (순서대로)", "백의 자리 → 십의 자리", "한꺼번에 다 빌려온다", "편한 대로"],
            correct="A",
            explanation="일의 자리 계산을 위해 십의 자리에서 빌려오고, 그 다음 십의 자리 계산을 위해 백의 자리에서 빌려옵니다.",
            hint="계산 순서대로 차근차근 빌려와요.",
        ),
        fb(
            id="e3-1-1-2-fb-003", concept_id="e3-1-1-06",
            category="concept", part="calc", difficulty=3,
            content="앞 자리에서 받아내림한 수가 있으면, 그 수를 **( )**하고 계산해야 합니다. (더하고/빼고/곱하고 중 선택)",
            answer="빼고",
            explanation="윗자리 숫자는 빌려준 만큼 1 작아져야 하므로 1을 빼고 남은 수로 계산합니다.",
            hint="친구에게 1개를 주었으니 내 것은 줄어들어야겠죠?",
        ),
        mc(
            id="e3-1-1-2-co-003", concept_id="e3-1-1-06",
            category="computation", part="calc", difficulty=3,
            content="500 - 263 = ?",
            options=["237", "337", "247", "257"],
            correct="A",
            explanation="500에서 빌려오기: 일의 자리 10-3=7, 십의 자리 9-6=3, 백의 자리 4-2=2. 답: 237",
        ),
        mc(
            id="e3-1-1-2-co-004", concept_id="e3-1-1-06",
            category="computation", part="calc", difficulty=5,
            content="724 - 358 = ?",
            options=["366", "434", "376", "466"],
            correct="A",
            explanation="일의 자리: 14-8=6(받아내림). 십의 자리: 11-5=6(받아내림). 백의 자리: 6-3=3. 답: 366",
        ),
        mc(
            id="e3-1-1-2-co-005", concept_id="e3-1-1-06",
            category="computation", part="calc", difficulty=6,
            content="803 - 467 = ?",
            options=["336", "444", "346", "436"],
            correct="A",
            explanation="십의 자리가 0이므로 백의 자리에서 빌려옴. 일의 자리: 13-7=6, 십의 자리: 9-6=3, 백의 자리: 7-4=3. 답: 336",
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 3단원: 나눗셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e3-1-3-01: 똑같이 나누기 ──
        mc(
            id="e3-1-3-1-cc-001", concept_id="e3-1-3-01",
            category="concept", part="calc", difficulty=3,
            content="사탕 12개를 3명에게 똑같이 나누면 한 명당 몇 개씩인가요?",
            options=["3개", "4개", "9개", "15개"],
            correct="B",
            explanation="12 ÷ 3 = 4입니다. 이것은 '등분제' 나눗셈으로, 전체를 똑같은 수의 묶음으로 나눕니다.",
        ),
        mc(
            id="e3-1-3-1-cc-002", concept_id="e3-1-3-01",
            category="concept", part="calc", difficulty=6,
            content="구슬 20개를 4개씩 묶으면 몇 묶음인가요? 이 상황을 나타내는 나눗셈식은?",
            options=["20 ÷ 5 = 4", "20 ÷ 4 = 5", "4 ÷ 20 = 0.2", "20 - 4 = 16"],
            correct="B",
            explanation="'4개씩 묶으면 몇 묶음?'은 포함제 나눗셈입니다. 20 ÷ 4 = 5에서 몫 5의 단위는 '묶음'입니다.",
        ),
        mc(
            id="e3-1-3-01-co-001", concept_id="e3-1-3-01",
            category="computation", part="calc", difficulty=2,
            content="15개의 연필을 5명에게 똑같이 나누면 한 명당 몇 개?",
            options=["3개", "5개", "2개", "4개"],
            correct="A",
            explanation="15 ÷ 5 = 3. 등분제: 전체 15개를 5명에게 똑같이 나누면 한 명당 3개입니다.",
        ),

        # ── e3-1-3-02: 곱셈과 나눗셈의 관계 ──
        mc(
            id="e3-1-3-2-co-001", concept_id="e3-1-3-02",
            category="computation", part="calc", difficulty=3,
            content="□ × 6 = 42일 때, □에 들어갈 수는?",
            options=["7", "6", "8", "9"],
            correct="A",
            explanation="42 ÷ 6 = 7. 곱셈의 빈칸은 나눗셈으로 구합니다.",
        ),
        mc(
            id="e3-1-3-2-co-002", concept_id="e3-1-3-02",
            category="computation", part="calc", difficulty=4,
            content="63 ÷ □ = 9일 때, □에 들어갈 수는?",
            options=["7", "8", "6", "9"],
            correct="A",
            explanation="□ × 9 = 63이므로 □ = 63 ÷ 9 = 7",
        ),
        mc(
            id="e3-1-3-2-co-004", concept_id="e3-1-3-02",
            category="computation", part="calc", difficulty=6,
            content="54 ÷ 6 = □, □ × 4 = △일 때, △은?",
            options=["36", "24", "32", "28"],
            correct="A",
            explanation="54 ÷ 6 = 9, 9 × 4 = 36",
        ),

        # ── e3-1-3-03: 나눗셈의 몫을 곱셈식으로 구하기 ──
        mc(
            id="e3-1-3-2-co-003", concept_id="e3-1-3-03",
            category="computation", part="calc", difficulty=5,
            content="□ ÷ 8 = 5일 때, □에 들어갈 수는?",
            options=["40", "35", "45", "48"],
            correct="A",
            explanation="□ = 8 × 5 = 40. 나눗셈의 나뉨수는 나누는 수 × 몫으로 구합니다.",
        ),
        mc(
            id="e3-1-3-2-co-005", concept_id="e3-1-3-03",
            category="computation", part="calc", difficulty=7,
            content="어떤 수에 5를 곱했더니 45가 되었습니다. 어떤 수를 3으로 나누면?",
            options=["3", "5", "9", "15"],
            correct="A",
            explanation="어떤 수 × 5 = 45이므로 어떤 수 = 45 ÷ 5 = 9. 9 ÷ 3 = 3",
        ),

        # ── e3-1-3-04: 나눗셈의 몫을 곱셈구구로 구하기 ──
        mc(
            id="e3-1-3-1-co-003", concept_id="e3-1-3-04",
            category="computation", part="calc", difficulty=3,
            content="36 ÷ 4 = ?",
            options=["9", "8", "7", "6"],
            correct="A",
            explanation="4단에서 36을 찾으면: 4 × 9 = 36이므로 36 ÷ 4 = 9",
        ),
        mc(
            id="e3-1-3-1-co-004", concept_id="e3-1-3-04",
            category="computation", part="calc", difficulty=4,
            content="56 ÷ 8 = ?",
            options=["7", "6", "8", "9"],
            correct="A",
            explanation="8단에서 56을 찾으면: 8 × 7 = 56이므로 56 ÷ 8 = 7",
        ),
        mc(
            id="e3-1-3-1-co-005", concept_id="e3-1-3-04",
            category="computation", part="calc", difficulty=5,
            content="72 ÷ 9 = ?",
            options=["8", "7", "9", "6"],
            correct="A",
            explanation="9단에서 72를 찾으면: 9 × 8 = 72이므로 72 ÷ 9 = 8",
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1학기 4단원: 곱셈
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e3-1-4-01: (몇십)×(몇) ──
        mc(
            id="e3-1-4-01-co-001", concept_id="e3-1-4-01",
            category="computation", part="calc", difficulty=2,
            content="20 × 3 = ?",
            options=["60", "50", "23", "6"],
            correct="A",
            explanation="2 × 3 = 6에 0을 붙여 60. 20 × 3 = 60",
        ),
        mc(
            id="e3-1-4-01-co-002", concept_id="e3-1-4-01",
            category="computation", part="calc", difficulty=3,
            content="40 × 7 = ?",
            options=["280", "28", "270", "480"],
            correct="A",
            explanation="4 × 7 = 28에 0을 붙여 280",
        ),
        fb(
            id="e3-1-4-01-fb-001", concept_id="e3-1-4-01",
            category="computation", part="calc", difficulty=2,
            content="30 × 5 = ____",
            answer="150",
            explanation="3 × 5 = 15에 0을 붙여 150",
            accept_formats=["150"],
        ),

        # ── e3-1-4-02: 올림 없는 (몇십몇)×(몇) ──
        mc(
            id="e3-1-4-1-cc-001", concept_id="e3-1-4-02",
            category="concept", part="calc", difficulty=4,
            content="다음 중 46 × 2를 바르게 계산한 것은?",
            options=[
                "40 × 2 + 6 × 2 = 80 + 12 = 92",
                "4 × 2 + 6 × 2 = 8 + 12 = 20",
                "46 × 1 + 46 × 1 = 46 + 46 = 82",
                "460 × 2 = 920",
            ],
            correct="A",
            explanation="46을 40과 6으로 나누어 각각 2를 곱한 후 더해야 합니다. "
            "십의 자리 '4'는 실제로 '40'을 의미합니다.",
        ),
        mc(
            id="e3-1-4-1-co-002", concept_id="e3-1-4-02",
            category="computation", part="calc", difficulty=3,
            content="32 × 3 = ?",
            options=["96", "36", "69", "86"],
            correct="A",
            explanation="30×3=90, 2×3=6. 90+6=96. 올림 없음.",
        ),

        # ── e3-1-4-03: 십의 자리에서 올림 ──
        mc(
            id="e3-1-4-03-co-001", concept_id="e3-1-4-03",
            category="computation", part="calc", difficulty=4,
            content="53 × 4 = ?",
            options=["212", "202", "232", "192"],
            correct="A",
            explanation="3×4=12 → 2 쓰고 1 올림. 5×4=20+1=21. 답: 212. 십의 자리 곱에서 올림 발생.",
        ),
        mc(
            id="e3-1-4-03-co-002", concept_id="e3-1-4-03",
            category="computation", part="calc", difficulty=5,
            content="72 × 4 = ?",
            options=["288", "268", "298", "278"],
            correct="A",
            explanation="2×4=8 (올림 없음). 7×4=28 → 백의 자리로 올림. 답: 288",
        ),

        # ── e3-1-4-04: 일의 자리에서 올림 ──
        mc(
            id="e3-1-4-2-cc-001", concept_id="e3-1-4-04",
            category="concept", part="calc", difficulty=3,
            content="23 × 4를 계산하는 과정입니다. 빈칸에 들어갈 알맞은 수는?\n\n23 × 4 = (20 + 3) × 4\n      = 20 × 4 + 3 × 4\n      = 80 + (   )\n      = 92",
            options=["7", "12", "34", "43"],
            correct="B",
            explanation="3 × 4 = 12입니다. 분배법칙: 23을 20과 3으로 나누어 각각 곱한 후 더합니다.",
        ),
        mc(
            id="e3-1-4-1-co-003", concept_id="e3-1-4-04",
            category="computation", part="calc", difficulty=4,
            content="27 × 3 = ?",
            options=["81", "71", "63", "91"],
            correct="A",
            explanation="7×3=21 → 1 쓰고 2 올림. 2×3=6+2=8. 답: 81",
        ),
        mc(
            id="e3-1-4-1-co-004", concept_id="e3-1-4-04",
            category="computation", part="calc", difficulty=5,
            content="15 × 6 = ?",
            options=["90", "80", "60", "96"],
            correct="A",
            explanation="5×6=30 → 0 쓰고 3 올림. 1×6=6+3=9. 답: 90",
        ),

        # ── e3-1-4-05: 올림 2번 ──
        mc(
            id="e3-1-4-2-cc-002", concept_id="e3-1-4-05",
            category="concept", part="calc", difficulty=6,
            content="모눈종이에서 가로 23칸, 세로 4칸의 직사각형 넓이를 구할 때, "
            "20 × 4 영역과 3 × 4 영역으로 나누어 계산하는 이유는?",
            options=[
                "계산을 빠르게 하기 위해",
                "23을 자릿값에 따라 20과 3으로 나누어 각각 계산하기 위해",
                "4를 2와 2로 나누어 계산하기 위해",
                "모눈종이의 칸 수를 세기 쉽게 하기 위해",
            ],
            correct="B",
            explanation="분배법칙의 시각적 이해입니다. 십의 자리와 일의 자리를 분리해서 계산하는 알고리즘의 기초입니다.",
        ),
        mc(
            id="e3-1-4-1-co-005", concept_id="e3-1-4-05",
            category="computation", part="calc", difficulty=6,
            content="38 × 7 = ?",
            options=["266", "246", "256", "276"],
            correct="A",
            explanation="8×7=56 → 6 쓰고 5 올림. 3×7=21+5=26. 답: 266. 일의 자리와 십의 자리 모두 올림.",
        ),
        mc(
            id="e3-1-4-2-co-003", concept_id="e3-1-4-05",
            category="computation", part="calc", difficulty=4,
            content="37 × 5 = ?",
            options=["185", "175", "195", "155"],
            correct="A",
            explanation="7×5=35 → 5 쓰고 3 올림. 3×5=15+3=18. 답: 185",
        ),
        mc(
            id="e3-1-4-2-co-004", concept_id="e3-1-4-05",
            category="computation", part="calc", difficulty=5,
            content="48 × 6 = ?",
            options=["288", "248", "268", "298"],
            correct="A",
            explanation="8×6=48 → 8 쓰고 4 올림. 4×6=24+4=28. 답: 288",
        ),
        mc(
            id="e3-1-4-2-co-005", concept_id="e3-1-4-05",
            category="computation", part="calc", difficulty=7,
            content="56 × 8 = ?",
            options=["448", "408", "468", "428"],
            correct="A",
            explanation="6×8=48 → 8 쓰고 4 올림. 5×8=40+4=44. 답: 448",
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 1단원: 곱셈 (2)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e3-2-1-01: 올림 없는 (세 자리 수)×(한 자리 수) ──
        mc(
            id="e3-2-1-1-co-002", concept_id="e3-2-1-01",
            category="computation", part="calc", difficulty=3,
            content="213 × 3 = ?",
            options=["639", "649", "629", "739"],
            correct="A",
            explanation="3×3=9, 1×3=3, 2×3=6. 답: 639. 올림 없음.",
        ),
        mc(
            id="e3-2-1-01-co-001", concept_id="e3-2-1-01",
            category="computation", part="calc", difficulty=2,
            content="112 × 4 = ?",
            options=["448", "448", "438", "458"],
            correct="A",
            explanation="2×4=8, 1×4=4, 1×4=4. 답: 448. 올림 없음.",
        ),

        # ── e3-2-1-02: 일의 자리에서 올림 ──
        mc(
            id="e3-2-1-02-co-001", concept_id="e3-2-1-02",
            category="computation", part="calc", difficulty=4,
            content="126 × 3 = ?",
            options=["378", "368", "388", "348"],
            correct="A",
            explanation="6×3=18 → 8 쓰고 1 올림. 2×3=6+1=7. 1×3=3. 답: 378",
        ),
        mc(
            id="e3-2-1-02-co-002", concept_id="e3-2-1-02",
            category="computation", part="calc", difficulty=5,
            content="218 × 4 = ?",
            options=["872", "862", "882", "852"],
            correct="A",
            explanation="8×4=32 → 2 쓰고 3 올림. 1×4=4+3=7. 2×4=8. 답: 872",
        ),

        # ── e3-2-1-03: 십·백의 자리에서 올림 ──
        mc(
            id="e3-2-1-1-co-003", concept_id="e3-2-1-03",
            category="computation", part="calc", difficulty=5,
            content="256 × 3 = ?",
            options=["768", "668", "778", "758"],
            correct="A",
            explanation="6×3=18 → 올림. 5×3=15+1=16 → 올림. 2×3=6+1=7. 답: 768",
        ),
        mc(
            id="e3-2-1-1-co-004", concept_id="e3-2-1-03",
            category="computation", part="calc", difficulty=6,
            content="315 × 7 = ?",
            options=["2205", "2105", "2215", "2195"],
            correct="A",
            explanation="5×7=35 → 올림. 1×7=7+3=10 → 올림. 3×7=21+1=22. 답: 2205",
        ),
        mc(
            id="e3-2-1-1-co-005", concept_id="e3-2-1-03",
            category="computation", part="calc", difficulty=7,
            content="407 × 5 = ?",
            options=["2035", "2005", "2045", "2350"],
            correct="A",
            explanation="7×5=35 → 올림. 0×5=0+3=3. 4×5=20. 답: 2035",
        ),

        # ── e3-2-1-04: (몇십)×(몇십), (몇십몇)×(몇십) ──
        mc(
            id="e3-2-1-04-co-001", concept_id="e3-2-1-04",
            category="computation", part="calc", difficulty=4,
            content="20 × 30 = ?",
            options=["600", "60", "6000", "500"],
            correct="A",
            explanation="2×3=6에 0을 2개 붙여 600. 십의 자리끼리 곱하면 0이 2개.",
        ),
        mc(
            id="e3-2-1-04-co-002", concept_id="e3-2-1-04",
            category="computation", part="calc", difficulty=5,
            content="15 × 30 = ?",
            options=["450", "45", "350", "550"],
            correct="A",
            explanation="15×3=45에 0을 붙여 450",
        ),

        # ── e3-2-1-05: (몇)×(몇십몇) ──
        mc(
            id="e3-2-1-05-co-001", concept_id="e3-2-1-05",
            category="computation", part="calc", difficulty=4,
            content="3 × 24 = ?",
            options=["72", "62", "82", "92"],
            correct="A",
            explanation="교환법칙: 3×24 = 24×3. 4×3=12 → 올림. 2×3=6+1=7. 답: 72",
        ),

        # ── e3-2-1-06: 올림 1번 (두 자리)×(두 자리) ──
        mc(
            id="e3-2-1-2-cc-001", concept_id="e3-2-1-06",
            category="concept", part="calc", difficulty=5,
            content="34 × 12를 계산할 때, 다음 중 옳은 과정은?",
            options=[
                "34 × 2 + 34 × 1 = 68 + 34 = 102",
                "34 × 2 + 34 × 10 = 68 + 340 = 408",
                "3 × 12 + 4 × 12 = 36 + 48 = 84",
                "34 + 12 = 46",
            ],
            correct="B",
            explanation="12의 십의 자리 '1'은 실제로 '10'을 의미하므로 34 × 10 = 340이 되어야 합니다.",
        ),
        mc(
            id="e3-2-1-2-co-002", concept_id="e3-2-1-06",
            category="computation", part="calc", difficulty=5,
            content="25 × 13 = ?",
            options=["325", "275", "350", "300"],
            correct="A",
            explanation="25×3=75, 25×10=250. 75+250=325",
        ),
        mc(
            id="e3-2-1-2-co-003", concept_id="e3-2-1-06",
            category="computation", part="calc", difficulty=6,
            content="34 × 21 = ?",
            options=["714", "680", "744", "614"],
            correct="A",
            explanation="34×1=34, 34×20=680. 34+680=714",
        ),

        # ── e3-2-1-07: 올림 여러 번 (두 자리)×(두 자리) ──
        mc(
            id="e3-2-1-2-co-004", concept_id="e3-2-1-07",
            category="computation", part="calc", difficulty=7,
            content="42 × 15 = ?",
            options=["630", "620", "650", "580"],
            correct="A",
            explanation="42×5=210, 42×10=420. 210+420=630",
        ),
        mc(
            id="e3-2-1-2-co-005", concept_id="e3-2-1-07",
            category="computation", part="calc", difficulty=8,
            content="17 × 23 = ?",
            options=["391", "371", "381", "401"],
            correct="A",
            explanation="17×3=51, 17×20=340. 51+340=391",
        ),
        mc(
            id="e3-2-1-07-co-001", concept_id="e3-2-1-07",
            category="computation", part="calc", difficulty=6,
            content="36 × 25 = ?",
            options=["900", "800", "850", "950"],
            correct="A",
            explanation="36×5=180, 36×20=720. 180+720=900",
        ),

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2학기 2단원: 나눗셈 (2)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        # ── e3-2-2-01: (몇십)÷(몇) ──
        mc(
            id="e3-2-2-01-co-001", concept_id="e3-2-2-01",
            category="computation", part="calc", difficulty=2,
            content="60 ÷ 3 = ?",
            options=["20", "30", "2", "18"],
            correct="A",
            explanation="6÷3=2에 0을 붙여 20. 또는 3×20=60.",
        ),
        mc(
            id="e3-2-2-01-co-002", concept_id="e3-2-2-01",
            category="computation", part="calc", difficulty=3,
            content="80 ÷ 4 = ?",
            options=["20", "2", "40", "8"],
            correct="A",
            explanation="8÷4=2에 0을 붙여 20",
        ),

        # ── e3-2-2-02: 내림 없고 나머지 없는 (몇십몇)÷(몇) ──
        mc(
            id="e3-2-2-02-co-001", concept_id="e3-2-2-02",
            category="computation", part="calc", difficulty=3,
            content="48 ÷ 4 = ?",
            options=["12", "11", "14", "8"],
            correct="A",
            explanation="4÷4=1 (십의 자리), 8÷4=2 (일의 자리). 답: 12",
        ),
        mc(
            id="e3-2-2-02-co-002", concept_id="e3-2-2-02",
            category="computation", part="calc", difficulty=4,
            content="69 ÷ 3 = ?",
            options=["23", "22", "33", "13"],
            correct="A",
            explanation="6÷3=2, 9÷3=3. 답: 23. 각 자리가 나누어떨어짐.",
        ),

        # ── e3-2-2-03: 내림 있고 나머지 없는 (몇십몇)÷(몇) ──
        mc(
            id="e3-2-2-03-co-001", concept_id="e3-2-2-03",
            category="computation", part="calc", difficulty=4,
            content="72 ÷ 3 = ?",
            options=["24", "23", "34", "22"],
            correct="A",
            explanation="7÷3=2...1 → 십의 자리 2, 나머지 1을 일의 자리로 내림 → 12÷3=4. 답: 24",
        ),
        mc(
            id="e3-2-2-03-co-002", concept_id="e3-2-2-03",
            category="computation", part="calc", difficulty=5,
            content="84 ÷ 6 = ?",
            options=["14", "12", "16", "13"],
            correct="A",
            explanation="8÷6=1...2 → 내림 → 24÷6=4. 답: 14",
        ),

        # ── e3-2-2-04: 내림 없고 나머지 있는 (몇십몇)÷(몇) ──
        mc(
            id="e3-2-2-1-co-001", concept_id="e3-2-2-04",
            category="computation", part="calc", difficulty=4,
            content="14 ÷ 3의 나머지는?",
            options=["1", "2", "3", "5"],
            correct="B",
            explanation="14 ÷ 3 = 4 ... 2입니다. 3 × 4 = 12, 14 - 12 = 2. 나머지 2 < 나누는 수 3 ✓",
        ),
        mc(
            id="e3-2-2-1-co-003", concept_id="e3-2-2-04",
            category="computation", part="calc", difficulty=4,
            content="29 ÷ 6의 몫과 나머지를 차례로 구하면?",
            options=["몫 4, 나머지 5", "몫 5, 나머지 1", "몫 3, 나머지 11", "몫 4, 나머지 6"],
            correct="A",
            explanation="6 × 4 = 24, 29 - 24 = 5. 검산: 6 × 4 + 5 = 29 ✓",
        ),
        mc(
            id="e3-2-2-1-co-004", concept_id="e3-2-2-04",
            category="computation", part="calc", difficulty=5,
            content="47 ÷ 8의 나머지는?",
            options=["7", "5", "3", "1"],
            correct="A",
            explanation="8 × 5 = 40, 47 - 40 = 7. 검산: 8 × 5 + 7 = 47 ✓",
        ),

        # ── e3-2-2-05: 내림 있고 나머지 있는 (몇십몇)÷(몇) ──
        mc(
            id="e3-2-2-1-co-005", concept_id="e3-2-2-05",
            category="computation", part="calc", difficulty=6,
            content="65 ÷ 7의 몫은?",
            options=["9", "8", "10", "7"],
            correct="A",
            explanation="7 × 9 = 63, 65 - 63 = 2. 나머지 2 < 나누는 수 7 ✓. 몫은 9",
        ),
        mc(
            id="e3-2-2-05-co-001", concept_id="e3-2-2-05",
            category="computation", part="calc", difficulty=5,
            content="53 ÷ 4의 몫과 나머지는?",
            options=["몫 13, 나머지 1", "몫 12, 나머지 5", "몫 14, 나머지 1", "몫 13, 나머지 3"],
            correct="A",
            explanation="5÷4=1...1 → 내림 → 13÷4=3...1. 답: 몫 13, 나머지 1. 검산: 4×13+1=53 ✓",
        ),

        # ── e3-2-2-06: 나머지 없는 (세 자리 수)÷(한 자리 수) ──
        mc(
            id="e3-2-2-06-co-001", concept_id="e3-2-2-06",
            category="computation", part="calc", difficulty=5,
            content="369 ÷ 3 = ?",
            options=["123", "133", "113", "223"],
            correct="A",
            explanation="3÷3=1, 6÷3=2, 9÷3=3. 답: 123",
        ),
        mc(
            id="e3-2-2-06-co-002", concept_id="e3-2-2-06",
            category="computation", part="calc", difficulty=6,
            content="456 ÷ 4 = ?",
            options=["114", "113", "124", "104"],
            correct="A",
            explanation="4÷4=1, 5÷4=1...1 → 내림 → 16÷4=4. 답: 114",
        ),

        # ── e3-2-2-07: 나머지 있는 (세 자리 수)÷(한 자리 수) ──
        mc(
            id="e3-2-2-07-co-001", concept_id="e3-2-2-07",
            category="computation", part="calc", difficulty=6,
            content="425 ÷ 3의 몫과 나머지는?",
            options=["몫 141, 나머지 2", "몫 142, 나머지 1", "몫 140, 나머지 5", "몫 141, 나머지 3"],
            correct="A",
            explanation="4÷3=1...1 → 12÷3=4 → 5÷3=1...2. 답: 몫 141, 나머지 2. 검산: 3×141+2=425 ✓",
        ),

        # ── e3-2-2-08: 맞게 계산했는지 확인하기 (검산) ──
        mc(
            id="e3-2-2-1-cc-001", concept_id="e3-2-2-08",
            category="concept", part="calc", difficulty=6,
            content="다음 계산이 틀린 이유를 설명하세요.\n\n14 ÷ 3 = 3 ... 5",
            options=[
                "몫이 틀렸다 (4가 되어야 함)",
                "나머지가 나누는 수 3보다 크거나 같다",
                "계산식 자체가 성립하지 않는다",
                "나눗셈은 나머지가 있을 수 없다",
            ],
            correct="B",
            explanation="나머지는 항상 나누는 수보다 작아야 합니다. 나머지 5 ≥ 나누는 수 3이므로 한 번 더 나눠야 합니다.",
        ),
        mc(
            id="e3-2-2-2-cc-001", concept_id="e3-2-2-08",
            category="concept", part="calc", difficulty=8,
            content="학생 14명을 3명씩 텐트에 배정하려고 합니다. 텐트는 최소 몇 개 필요한가요?",
            options=["3개", "4개", "5개", "6개"],
            correct="C",
            explanation="14 ÷ 3 = 4 ... 2. 남는 2명도 텐트가 필요하므로 5개 (올림 상황).",
        ),
        mc(
            id="e3-2-2-2-cc-002", concept_id="e3-2-2-08",
            category="concept", part="calc", difficulty=5,
            content="25명이 4인승 보트를 타려고 합니다. 보트는 최소 몇 대 필요한가요?",
            options=["7대", "6대", "5대", "8대"],
            correct="A",
            explanation="25 ÷ 4 = 6 ... 1. 남은 1명도 보트가 필요하므로 6+1=7대 (올림 상황)",
        ),
        mc(
            id="e3-2-2-2-cc-003", concept_id="e3-2-2-08",
            category="concept", part="calc", difficulty=5,
            content="사탕 23개를 5명에게 똑같이 나누면 한 명은 최대 몇 개 받나요?",
            options=["4개", "5개", "3개", "6개"],
            correct="A",
            explanation="23 ÷ 5 = 4 ... 3. 나머지 3개는 더 나눌 수 없으므로 한 명당 4개 (버림 상황)",
        ),
        mc(
            id="e3-2-2-2-cc-004", concept_id="e3-2-2-08",
            category="concept", part="calc", difficulty=6,
            content="리본 38cm를 7cm씩 자르면 최대 몇 도막을 만들 수 있나요?",
            options=["5도막", "6도막", "4도막", "7도막"],
            correct="A",
            explanation="38 ÷ 7 = 5 ... 3. 남은 3cm로는 7cm 도막을 못 만듦. 5도막 (버림 상황)",
        ),
        mc(
            id="e3-2-2-2-cc-005", concept_id="e3-2-2-08",
            category="concept", part="calc", difficulty=7,
            content="학생 33명이 8인승 차를 타려고 합니다. 차는 최소 몇 대 필요한가요?",
            options=["5대", "4대", "3대", "6대"],
            correct="A",
            explanation="33 ÷ 8 = 4 ... 1. 남은 1명도 차가 필요하므로 4+1=5대 (올림 상황)",
        ),
    ]
