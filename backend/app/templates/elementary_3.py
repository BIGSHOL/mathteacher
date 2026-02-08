"""초등 3학년 연산 문제 템플릿.

개념 목록:
- concept-e3-add-sub-01: 받아올림 있는 (세 자리) 덧셈
- concept-e3-add-sub-02: 받아내림 있는 (세 자리) 뺄셈
- concept-e3-mul1-01: (두 자리)×(한 자리) 기본
- concept-e3-mul1-02: (두 자리)×(한 자리) 올림
- concept-e3-div1-01: 나눗셈 기초 (구구단 역)
- concept-e3-div1-02: 곱셈-나눗셈 관계 / 빈칸
- concept-e3-mul2-01: (세 자리)×(한 자리)
- concept-e3-mul2-02: (두 자리)×(두 자리)
- concept-e3-div2-01: (두 자리)÷(한 자리) 나머지
- concept-e3-div2-02: 나머지 활용 문제
"""
import random

from . import register, build_mc, build_fb


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 받아올림 있는 덧셈
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _has_carry(a: int, b: int) -> bool:
    """세 자리 덧셈에서 받아올림이 있는지 확인."""
    ones = (a % 10) + (b % 10)
    tens = (a // 10 % 10) + (b // 10 % 10) + (1 if ones >= 10 else 0)
    return ones >= 10 or tens >= 10


def _addition_explanation(a: int, b: int) -> str:
    answer = a + b
    o_a, o_b = a % 10, b % 10
    t_a, t_b = a // 10 % 10, b // 10 % 10
    h_a, h_b = a // 100, b // 100
    ones_sum = o_a + o_b
    carry1 = 1 if ones_sum >= 10 else 0
    tens_sum = t_a + t_b + carry1
    carry2 = 1 if tens_sum >= 10 else 0
    parts = []
    if carry1:
        parts.append(f"일의 자리: {o_a}+{o_b}={ones_sum} -> {ones_sum % 10} 쓰고 1 올림")
    if carry2:
        parts.append(f"십의 자리: {t_a}+{t_b}+{carry1}={tens_sum} -> {tens_sum % 10} 쓰고 1 올림")
    parts.append(f"백의 자리: {h_a}+{h_b}+{carry2}={h_a + h_b + carry2}")
    parts.append(f"답: {answer}")
    return ". ".join(parts)


@register("concept-e3-add-sub-01", difficulty=3)
def e3_add_lv3():
    while True:
        a = random.randint(100, 499)
        b = random.randint(100, 499)
        if _has_carry(a, b):
            break
    ans = a + b
    return build_mc(
        content=f"{a} + {b} = ?",
        answer=ans,
        wrongs=[ans + 10, ans - 10, ans - 100, ans + 100],
        explanation=_addition_explanation(a, b),
        concept_id="concept-e3-add-sub-01", difficulty=3,
    )


@register("concept-e3-add-sub-01", difficulty=5)
def e3_add_lv5():
    while True:
        a = random.randint(200, 799)
        b = random.randint(200, 799)
        if _has_carry(a, b) and a + b < 1600:
            break
    ans = a + b
    return build_mc(
        content=f"{a} + {b} = ?",
        answer=ans,
        wrongs=[ans + 10, ans - 10, ans - 100, ans + 100, ans + 1],
        explanation=_addition_explanation(a, b),
        concept_id="concept-e3-add-sub-01", difficulty=5,
    )


@register("concept-e3-add-sub-01", difficulty=7)
def e3_add_lv7():
    while True:
        a = random.randint(300, 999)
        b = random.randint(300, 999)
        # 두 자리 이상에서 받아올림
        if (a % 10 + b % 10 >= 10) and (a // 10 % 10 + b // 10 % 10 >= 9):
            break
    ans = a + b
    return build_mc(
        content=f"{a} + {b} = ?",
        answer=ans,
        wrongs=[ans + 10, ans - 10, ans + 1, ans - 1, ans + 100],
        explanation=_addition_explanation(a, b),
        concept_id="concept-e3-add-sub-01", difficulty=7,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 받아내림 있는 뺄셈
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _has_borrow(a: int, b: int) -> bool:
    return (a % 10) < (b % 10) or (a // 10 % 10) < (b // 10 % 10)


@register("concept-e3-add-sub-02", difficulty=3)
def e3_sub_lv3():
    while True:
        a = random.randint(300, 700)
        b = random.randint(100, a - 50)
        if _has_borrow(a, b) and a - b > 50:
            break
    ans = a - b
    return build_mc(
        content=f"{a} - {b} = ?",
        answer=ans,
        wrongs=[ans + 100, ans + 10, ans - 10, ans + 1],
        explanation=f"{a} - {b} = {ans}",
        concept_id="concept-e3-add-sub-02", difficulty=3,
    )


@register("concept-e3-add-sub-02", difficulty=5)
def e3_sub_lv5():
    while True:
        a = random.randint(400, 999)
        b = random.randint(200, a - 100)
        if _has_borrow(a, b):
            break
    ans = a - b
    return build_mc(
        content=f"{a} - {b} = ?",
        answer=ans,
        wrongs=[ans + 100, ans + 10, ans - 10, ans + 68, ans - 100],
        explanation=f"{a} - {b} = {ans}",
        concept_id="concept-e3-add-sub-02", difficulty=5,
    )


@register("concept-e3-add-sub-02", difficulty=7)
def e3_sub_lv7():
    """십의 자리가 0인 수에서 빼기 (예: 803 - 467)."""
    while True:
        h = random.randint(3, 9)
        a = h * 100 + random.choice([0, 1, 2, 3]) * 1  # X0Y 형태
        a = h * 100 + random.randint(0, 9)  # 십의 자리 0~1
        b = random.randint(100, a - 100)
        if _has_borrow(a, b) and a // 10 % 10 <= 1:
            break
    ans = a - b
    return build_mc(
        content=f"{a} - {b} = ?",
        answer=ans,
        wrongs=[ans + 100, ans + 10, ans - 10, ans + 108],
        explanation=f"{a} - {b} = {ans}",
        concept_id="concept-e3-add-sub-02", difficulty=7,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# (두 자리)×(한 자리) 기본
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-e3-mul1-01", difficulty=3)
def e3_mul1_lv3():
    a = random.randint(11, 49)
    b = random.randint(2, 5)
    ans = a * b
    tens, ones = a // 10, a % 10
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 10, ans - 10, tens * b * 10, ans + b],
        explanation=f"{tens * 10}x{b}={tens * 10 * b}, {ones}x{b}={ones * b}. "
                    f"{tens * 10 * b}+{ones * b}={ans}",
        concept_id="concept-e3-mul1-01", difficulty=3,
    )


@register("concept-e3-mul1-01", difficulty=5)
def e3_mul1_lv5():
    a = random.randint(12, 50)
    b = random.randint(4, 9)
    ans = a * b
    tens, ones = a // 10, a % 10
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 10, ans - 10, ans + 20, ans - b],
        explanation=f"{tens * 10}x{b}={tens * 10 * b}, {ones}x{b}={ones * b}. "
                    f"{tens * 10 * b}+{ones * b}={ans}",
        concept_id="concept-e3-mul1-01", difficulty=5,
    )


@register("concept-e3-mul1-01", difficulty=7)
def e3_mul1_lv7():
    a = random.randint(30, 99)
    b = random.randint(6, 9)
    ans = a * b
    tens, ones = a // 10, a % 10
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 10, ans - 10, ans + 20, ans - 20, ans + 100],
        explanation=f"{tens * 10}x{b}={tens * 10 * b}, {ones}x{b}={ones * b}. "
                    f"{tens * 10 * b}+{ones * b}={ans}",
        concept_id="concept-e3-mul1-01", difficulty=7,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# (두 자리)×(한 자리) 올림
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-e3-mul1-02", difficulty=4)
def e3_mul1_carry_lv4():
    while True:
        a = random.randint(13, 59)
        b = random.randint(3, 7)
        if (a % 10) * b >= 10:  # 올림 발생
            break
    ans = a * b
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 10, ans - 10, ans + 20, ans - 20],
        explanation=f"{a // 10 * 10}x{b}={a // 10 * 10 * b}, "
                    f"{a % 10}x{b}={a % 10 * b}. "
                    f"{a // 10 * 10 * b}+{a % 10 * b}={ans}",
        concept_id="concept-e3-mul1-02", difficulty=4,
    )


@register("concept-e3-mul1-02", difficulty=6)
def e3_mul1_carry_lv6():
    while True:
        a = random.randint(25, 89)
        b = random.randint(5, 9)
        if (a % 10) * b >= 10:
            break
    ans = a * b
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 10, ans - 10, ans + 20, ans - 20, ans + 2],
        explanation=f"{a // 10 * 10}x{b}={a // 10 * 10 * b}, "
                    f"{a % 10}x{b}={a % 10 * b}. "
                    f"{a // 10 * 10 * b}+{a % 10 * b}={ans}",
        concept_id="concept-e3-mul1-02", difficulty=6,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 나눗셈 기초 (구구단 역)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-e3-div1-01", difficulty=3)
def e3_div1_lv3():
    b = random.randint(2, 9)
    ans = random.randint(2, 9)
    a = b * ans
    return build_mc(
        content=f"{a} / {b} = ?",
        answer=ans,
        wrongs=[ans + 1, ans - 1, ans + 2, b],
        explanation=f"{b} x {ans} = {a}이므로 {a} / {b} = {ans}",
        concept_id="concept-e3-div1-01", difficulty=3,
    )


@register("concept-e3-div1-01", difficulty=5)
def e3_div1_lv5():
    b = random.randint(6, 9)
    ans = random.randint(5, 9)
    a = b * ans
    return build_mc(
        content=f"{a} / {b} = ?",
        answer=ans,
        wrongs=[ans + 1, ans - 1, ans + 2, ans - 2],
        explanation=f"{b} x {ans} = {a}이므로 {a} / {b} = {ans}",
        concept_id="concept-e3-div1-01", difficulty=5,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 곱셈-나눗셈 관계 (빈칸)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-e3-div1-02", difficulty=3)
def e3_div_rel_lv3():
    """□ × b = c 형태."""
    b = random.randint(3, 9)
    ans = random.randint(3, 9)
    c = b * ans
    return build_mc(
        content=f"□ x {b} = {c}일 때, □에 들어갈 수는?",
        answer=ans,
        wrongs=[ans + 1, ans - 1, b, c // 10 if c >= 10 else ans + 2],
        explanation=f"{c} / {b} = {ans}. 곱셈의 빈칸은 나눗셈으로 구합니다.",
        concept_id="concept-e3-div1-02", difficulty=3,
    )


@register("concept-e3-div1-02", difficulty=5)
def e3_div_rel_lv5():
    """□ ÷ b = c 형태 (□ 구하기)."""
    b = random.randint(3, 9)
    c = random.randint(3, 9)
    ans = b * c
    return build_mc(
        content=f"□ / {b} = {c}일 때, □에 들어갈 수는?",
        answer=ans,
        wrongs=[ans - b, ans + b, b * (c + 1), b * (c - 1)],
        explanation=f"□ = {b} x {c} = {ans}. 나눗셈의 나뉨수는 나누는 수 x 몫으로 구합니다.",
        concept_id="concept-e3-div1-02", difficulty=5,
    )


@register("concept-e3-div1-02", difficulty=7)
def e3_div_rel_lv7():
    """a ÷ b = □, □ × c = △ 형태."""
    b = random.randint(3, 9)
    mid = random.randint(3, 9)
    a = b * mid
    c = random.randint(2, 6)
    ans = mid * c
    return build_mc(
        content=f"{a} / {b} = □, □ x {c} = △일 때, △은?",
        answer=ans,
        wrongs=[mid, a, ans + c, ans - c],
        explanation=f"{a} / {b} = {mid}, {mid} x {c} = {ans}",
        concept_id="concept-e3-div1-02", difficulty=7,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# (세 자리)×(한 자리)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-e3-mul2-01", difficulty=4)
def e3_mul2_lv4():
    a = random.randint(101, 350)
    b = random.randint(2, 5)
    ans = a * b
    h, t, o = a // 100, a // 10 % 10, a % 10
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 10, ans - 10, ans + 100, ans - 100],
        explanation=f"{h * 100}x{b}={h * 100 * b}, {t * 10}x{b}={t * 10 * b}, "
                    f"{o}x{b}={o * b}. {h * 100 * b}+{t * 10 * b}+{o * b}={ans}",
        concept_id="concept-e3-mul2-01", difficulty=4,
    )


@register("concept-e3-mul2-01", difficulty=6)
def e3_mul2_lv6():
    a = random.randint(200, 500)
    b = random.randint(5, 9)
    ans = a * b
    h, t, o = a // 100, a // 10 % 10, a % 10
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 10, ans - 10, ans + 100, ans - 100, ans + 5],
        explanation=f"{h * 100}x{b}={h * 100 * b}, {t * 10}x{b}={t * 10 * b}, "
                    f"{o}x{b}={o * b}. {h * 100 * b}+{t * 10 * b}+{o * b}={ans}",
        concept_id="concept-e3-mul2-01", difficulty=6,
    )


@register("concept-e3-mul2-01", difficulty=8)
def e3_mul2_lv8():
    """가운데 0이 있는 곱셈 (407 × 5 등)."""
    h = random.randint(2, 9)
    o = random.randint(1, 9)
    a = h * 100 + o  # X0Y
    b = random.randint(3, 9)
    ans = a * b
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 10, ans - 10, ans + 100, h * 100 * b + o],
        explanation=f"{h * 100}x{b}={h * 100 * b}, 0x{b}=0, "
                    f"{o}x{b}={o * b}. {h * 100 * b}+0+{o * b}={ans}",
        concept_id="concept-e3-mul2-01", difficulty=8,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# (두 자리)×(두 자리)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-e3-mul2-02", difficulty=5)
def e3_mul2x2_lv5():
    a = random.randint(11, 35)
    b = random.randint(11, 25)
    ans = a * b
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 25, ans - 25, a * (b + 10), a * (b - 10) if b > 10 else ans + 50],
        explanation=f"{a}x{b % 10}={a * (b % 10)}, "
                    f"{a}x{b // 10 * 10}={a * (b // 10 * 10)}. "
                    f"{a * (b % 10)}+{a * (b // 10 * 10)}={ans}",
        concept_id="concept-e3-mul2-02", difficulty=5,
    )


@register("concept-e3-mul2-02", difficulty=7)
def e3_mul2x2_lv7():
    a = random.randint(20, 60)
    b = random.randint(15, 40)
    ans = a * b
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 50, ans - 50, ans + 100, ans - 100, ans + a],
        explanation=f"{a}x{b % 10}={a * (b % 10)}, "
                    f"{a}x{b // 10 * 10}={a * (b // 10 * 10)}. "
                    f"{a * (b % 10)}+{a * (b // 10 * 10)}={ans}",
        concept_id="concept-e3-mul2-02", difficulty=7,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# (두 자리)÷(한 자리) 나머지 있는 나눗셈
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-e3-div2-01", difficulty=3)
def e3_div2_lv3():
    b = random.randint(3, 9)
    quotient = random.randint(3, 9)
    remainder = random.randint(1, b - 1)
    a = b * quotient + remainder
    return build_mc(
        content=f"{a} / {b}의 나머지는?",
        answer=remainder,
        wrongs=[remainder + 1, remainder - 1 if remainder > 1 else b - 1, quotient, 0],
        explanation=f"{a} = {b} x {quotient} + {remainder}이므로 나머지는 {remainder}",
        concept_id="concept-e3-div2-01", difficulty=3,
    )


@register("concept-e3-div2-01", difficulty=5)
def e3_div2_lv5():
    b = random.randint(3, 9)
    quotient = random.randint(5, 15)
    remainder = random.randint(1, b - 1)
    a = b * quotient + remainder
    return build_mc(
        content=f"{a} / {b}의 몫과 나머지를 구하면? (몫 ... 나머지)",
        answer=f"{quotient} ... {remainder}",
        wrongs=[
            f"{quotient + 1} ... {remainder}",
            f"{quotient} ... {remainder + 1 if remainder + 1 < b else 0}",
            f"{quotient - 1} ... {remainder + b}",
        ],
        explanation=f"{a} = {b} x {quotient} + {remainder}. 몫: {quotient}, 나머지: {remainder}",
        concept_id="concept-e3-div2-01", difficulty=5,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 나머지 활용 문제
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-e3-div2-02", difficulty=5)
def e3_div2_word_lv5():
    """N명을 M명씩 배정하면 몇 묶음 필요? (올림)."""
    per_group = random.randint(3, 8)
    total = random.randint(per_group + 1, per_group * 10)
    # 나머지가 있도록
    while total % per_group == 0:
        total += 1
    quotient = total // per_group
    ans = quotient + 1  # 올림
    items = random.choice(["학생", "사과", "구슬", "색연필", "사탕"])
    containers = random.choice(["묶음", "봉지", "상자", "그룹", "팀"])
    return build_mc(
        content=f"{items} {total}개를 {per_group}개씩 {containers}에 담으면 "
                f"{containers}은 최소 몇 개 필요한가요?",
        answer=ans,
        wrongs=[quotient, ans + 1, quotient - 1, total // per_group + 2],
        explanation=f"{total} / {per_group} = {quotient} ... {total % per_group}. "
                    f"나머지 {total % per_group}개도 담아야 하므로 {containers}은 "
                    f"{quotient} + 1 = {ans}개 필요합니다.",
        concept_id="concept-e3-div2-02", difficulty=5,
    )


@register("concept-e3-div2-02", difficulty=7)
def e3_div2_word_lv7():
    """어떤 수에 a를 곱했더니 b. 어떤 수를 c로 나누면?"""
    c = random.randint(2, 6)
    some = random.randint(2, 9) * c  # c로 나누어떨어지게
    a = random.randint(2, 9)
    while a == 1:
        a = random.randint(2, 9)
    b = some * a
    ans = some // c
    return build_mc(
        content=f"어떤 수에 {a}를 곱했더니 {b}가 되었습니다. "
                f"어떤 수를 {c}으로 나누면?",
        answer=ans,
        wrongs=[some, b // c if b % c == 0 else ans + 1, ans + c, ans - 1],
        explanation=f"어떤 수 x {a} = {b}이므로 어떤 수 = {b} / {a} = {some}. "
                    f"{some} / {c} = {ans}",
        concept_id="concept-e3-div2-02", difficulty=7,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 빈칸 채우기 (FB) 템플릿
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-e3-add-sub-01", difficulty=4)
def e3_add_fb_lv4():
    while True:
        a = random.randint(100, 599)
        b = random.randint(100, 599)
        if _has_carry(a, b):
            break
    ans = a + b
    return build_fb(
        content=f"{a} + {b} = [answer]",
        answer=str(ans),
        explanation=_addition_explanation(a, b),
        concept_id="concept-e3-add-sub-01", difficulty=4,
    )


@register("concept-e3-add-sub-02", difficulty=4)
def e3_sub_fb_lv4():
    while True:
        a = random.randint(300, 900)
        b = random.randint(100, a - 100)
        if _has_borrow(a, b):
            break
    ans = a - b
    return build_fb(
        content=f"{a} - {b} = [answer]",
        answer=str(ans),
        explanation=f"{a} - {b} = {ans}",
        concept_id="concept-e3-add-sub-02", difficulty=4,
    )


@register("concept-e3-mul1-01", difficulty=4)
def e3_mul1_fb_lv4():
    a = random.randint(11, 50)
    b = random.randint(2, 9)
    ans = a * b
    return build_fb(
        content=f"{a} x {b} = [answer]",
        answer=str(ans),
        explanation=f"{a} x {b} = {ans}",
        concept_id="concept-e3-mul1-01", difficulty=4,
    )


@register("concept-e3-div1-01", difficulty=4)
def e3_div1_fb_lv4():
    b = random.randint(2, 9)
    ans = random.randint(2, 9)
    a = b * ans
    return build_fb(
        content=f"{a} / {b} = [answer]",
        answer=str(ans),
        explanation=f"{b} x {ans} = {a}이므로 {a} / {b} = {ans}",
        concept_id="concept-e3-div1-01", difficulty=4,
    )
