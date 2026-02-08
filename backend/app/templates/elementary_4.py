"""초등 4학년 연산 문제 템플릿.

개념 목록:
- concept-e4-mul-div-01: 3자리 x 2자리 곱셈
- concept-e4-mul-div-02: 3자리 ÷ 2자리 나눗셈
- concept-e4-frac-op-01: 분모가 같은 분수 덧셈/뺄셈
- concept-e4-frac-op-02: 대분수 연산 (받아내림 포함)
- concept-e4-dec-op-02: 소수 덧셈/뺄셈
"""
import math
import random

from . import register, build_mc, build_fb


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3자리 x 2자리 곱셈
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e4-mul-div-01", difficulty=4)
def e4_mul_3x2_lv4():
    a = random.randint(100, 300)
    b = random.randint(11, 30)
    ans = a * b
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 100, ans - 100, ans + 50, ans - 50],
        explanation=f"{a}x{b % 10}={a * (b % 10)}, "
                    f"{a}x{b // 10 * 10}={a * (b // 10 * 10)}. "
                    f"{a * (b % 10)}+{a * (b // 10 * 10)}={ans}",
        concept_id="concept-e4-mul-div-01", difficulty=4,
    )


@register("concept-e4-mul-div-01", difficulty=6)
def e4_mul_3x2_lv6():
    a = random.randint(200, 600)
    b = random.randint(20, 60)
    ans = a * b
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 200, ans - 200, ans + 500, ans - 500, ans + 1000],
        explanation=f"{a}x{b % 10}={a * (b % 10)}, "
                    f"{a}x{b // 10 * 10}={a * (b // 10 * 10)}. "
                    f"{a * (b % 10)}+{a * (b // 10 * 10)}={ans}",
        concept_id="concept-e4-mul-div-01", difficulty=6,
    )


@register("concept-e4-mul-div-01", difficulty=8)
def e4_mul_3x2_lv8():
    a = random.randint(300, 999)
    b = random.randint(40, 99)
    ans = a * b
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[ans + 500, ans - 500, ans + 1000, ans - 1000, ans + 100],
        explanation=f"{a}x{b % 10}={a * (b % 10)}, "
                    f"{a}x{b // 10 * 10}={a * (b // 10 * 10)}. "
                    f"{a * (b % 10)}+{a * (b // 10 * 10)}={ans}",
        concept_id="concept-e4-mul-div-01", difficulty=8,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3자리 ÷ 2자리 나눗셈
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e4-mul-div-02", difficulty=4)
def e4_div_3by2_lv4():
    """나누어 떨어지는 나눗셈."""
    b = random.randint(11, 30)
    quotient = random.randint(5, 15)
    a = b * quotient
    return build_mc(
        content=f"{a} ÷ {b} = ?",
        answer=quotient,
        wrongs=[quotient + 1, quotient - 1, quotient + 2, quotient + 5],
        explanation=f"{b} x {quotient} = {a}이므로 {a} ÷ {b} = {quotient}",
        concept_id="concept-e4-mul-div-02", difficulty=4,
    )


@register("concept-e4-mul-div-02", difficulty=6)
def e4_div_3by2_lv6():
    """나머지 있는 나눗셈."""
    b = random.randint(15, 40)
    quotient = random.randint(10, 20)
    remainder = random.randint(1, b - 1)
    a = b * quotient + remainder
    return build_mc(
        content=f"{a} ÷ {b}의 몫과 나머지를 구하면? (몫 ... 나머지)",
        answer=f"{quotient} ... {remainder}",
        wrongs=[
            f"{quotient + 1} ... {remainder}",
            f"{quotient} ... {remainder + 1 if remainder + 1 < b else 0}",
            f"{quotient - 1} ... {remainder + b}",
        ],
        explanation=f"{a} = {b} x {quotient} + {remainder}. 몫: {quotient}, 나머지: {remainder}",
        concept_id="concept-e4-mul-div-02", difficulty=6,
    )


@register("concept-e4-mul-div-02", difficulty=8)
def e4_div_3by2_lv8():
    """큰 수의 나눗셈."""
    b = random.randint(20, 50)
    quotient = random.randint(15, 30)
    remainder = random.randint(0, b - 1)
    a = b * quotient + remainder
    return build_mc(
        content=f"{a} ÷ {b}의 몫은?",
        answer=quotient,
        wrongs=[quotient + 1, quotient - 1, quotient + 2, remainder],
        explanation=f"{a} = {b} x {quotient} + {remainder}이므로 몫은 {quotient}",
        concept_id="concept-e4-mul-div-02", difficulty=8,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 분모가 같은 분수 덧셈/뺄셈
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e4-frac-op-01", difficulty=3)
def e4_frac_same_add_lv3():
    """분모가 같은 진분수 덧셈."""
    denom = random.randint(4, 12)
    num1 = random.randint(1, denom - 2)
    num2 = random.randint(1, denom - num1 - 1)
    ans_num = num1 + num2
    gcd = math.gcd(ans_num, denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = denom // gcd
    ans_str = f"{ans_num_reduced}/{ans_denom_reduced}" if ans_denom_reduced != 1 else str(ans_num_reduced)
    return build_mc(
        content=f"{num1}/{denom} + {num2}/{denom} = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{num1 + num2}/{denom}",
            f"{num1}/{denom}",
            f"{num2}/{denom}",
        ],
        explanation=f"{num1}/{denom} + {num2}/{denom} = {ans_num}/{denom} = {ans_str}",
        concept_id="concept-e4-frac-op-01", difficulty=3,
    )


@register("concept-e4-frac-op-01", difficulty=5)
def e4_frac_same_sub_lv5():
    """분모가 같은 진분수 뺄셈."""
    denom = random.randint(5, 15)
    num1 = random.randint(3, denom - 1)
    num2 = random.randint(1, num1 - 1)
    ans_num = num1 - num2
    gcd = math.gcd(ans_num, denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = denom // gcd
    ans_str = f"{ans_num_reduced}/{ans_denom_reduced}" if ans_denom_reduced != 1 else str(ans_num_reduced)
    return build_mc(
        content=f"{num1}/{denom} - {num2}/{denom} = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{num1 - num2}/{denom}",
            f"{num1}/{denom}",
            f"{num2}/{denom}",
        ],
        explanation=f"{num1}/{denom} - {num2}/{denom} = {ans_num}/{denom} = {ans_str}",
        concept_id="concept-e4-frac-op-01", difficulty=5,
    )


@register("concept-e4-frac-op-01", difficulty=7)
def e4_frac_same_mix_lv7():
    """분모가 같은 분수 덧셈 (결과가 가분수)."""
    denom = random.randint(5, 10)
    num1 = random.randint(denom // 2, denom - 1)
    num2 = random.randint(denom // 2, denom - 1)
    ans_num = num1 + num2
    whole = ans_num // denom
    remainder = ans_num % denom
    gcd = math.gcd(remainder, denom) if remainder > 0 else 1
    remainder_reduced = remainder // gcd
    denom_reduced = denom // gcd
    if remainder == 0:
        ans_str = str(whole)
    else:
        ans_str = f"{whole}({remainder_reduced}/{denom_reduced})"
    return build_mc(
        content=f"{num1}/{denom} + {num2}/{denom} = ? (대분수로)",
        answer=ans_str,
        wrongs=[
            f"{ans_num}/{denom}",
            f"{whole}({remainder}/{denom})" if remainder > 0 else f"{whole + 1}",
            f"{whole - 1}({remainder_reduced}/{denom_reduced})" if whole > 1 else f"1",
        ],
        explanation=f"{num1}/{denom} + {num2}/{denom} = {ans_num}/{denom} = {ans_str}",
        concept_id="concept-e4-frac-op-01", difficulty=7,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 대분수 연산 (받아내림 포함)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e4-frac-op-02", difficulty=5)
def e4_mixed_sub_lv5():
    """자연수 - 진분수 (받아내림)."""
    whole = random.randint(3, 9)
    denom = random.randint(4, 8)
    num = random.randint(1, denom - 1)
    # 결과: (whole - 1) + (denom - num)/denom
    ans_whole = whole - 1
    ans_num = denom - num
    gcd = math.gcd(ans_num, denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = denom // gcd
    ans_str = f"{ans_whole}({ans_num_reduced}/{ans_denom_reduced})"
    return build_mc(
        content=f"{whole} - {num}/{denom} = ? (대분수로)",
        answer=ans_str,
        wrongs=[
            f"{whole}({num}/{denom})",
            f"{whole - 1}({num}/{denom})",
            f"{ans_whole}({ans_num}/{denom})",
        ],
        explanation=f"{whole} = {whole - 1}({denom}/{denom}). "
                    f"{whole - 1}({denom}/{denom}) - {num}/{denom} = {ans_whole}({denom - num}/{denom}) = {ans_str}",
        concept_id="concept-e4-frac-op-02", difficulty=5,
    )


@register("concept-e4-frac-op-02", difficulty=7)
def e4_mixed_add_lv7():
    """대분수 + 대분수."""
    denom = random.randint(4, 8)
    whole1 = random.randint(1, 5)
    whole2 = random.randint(1, 5)
    num1 = random.randint(1, denom - 1)
    num2 = random.randint(1, denom - 1)
    # 결과 계산
    total_num = num1 + num2
    carry = total_num // denom
    ans_whole = whole1 + whole2 + carry
    ans_num = total_num % denom
    gcd = math.gcd(ans_num, denom) if ans_num > 0 else 1
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = denom // gcd
    if ans_num == 0:
        ans_str = str(ans_whole)
    else:
        ans_str = f"{ans_whole}({ans_num_reduced}/{ans_denom_reduced})"
    return build_mc(
        content=f"{whole1}({num1}/{denom}) + {whole2}({num2}/{denom}) = ? (대분수로)",
        answer=ans_str,
        wrongs=[
            f"{whole1 + whole2}({num1 + num2}/{denom})" if num1 + num2 < denom else f"{whole1 + whole2}",
            f"{ans_whole + 1}({ans_num}/{denom})" if ans_num > 0 else f"{ans_whole - 1}",
            f"{ans_whole}({ans_num}/{denom})" if ans_num > 0 else f"{ans_whole + 1}",
        ],
        explanation=f"{whole1}({num1}/{denom}) + {whole2}({num2}/{denom}) = "
                    f"{whole1 + whole2}({num1 + num2}/{denom}) = {ans_str}",
        concept_id="concept-e4-frac-op-02", difficulty=7,
    )


@register("concept-e4-frac-op-02", difficulty=8)
def e4_mixed_sub_lv8():
    """대분수 - 대분수 (받아내림)."""
    denom = random.randint(5, 10)
    whole1 = random.randint(4, 9)
    whole2 = random.randint(1, whole1 - 2)
    num1 = random.randint(1, denom - 2)
    num2 = random.randint(num1 + 1, denom - 1)  # 받아내림 발생
    # 받아내림 계산
    ans_whole = whole1 - whole2 - 1
    ans_num = denom + num1 - num2
    gcd = math.gcd(ans_num, denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = denom // gcd
    ans_str = f"{ans_whole}({ans_num_reduced}/{ans_denom_reduced})"
    return build_mc(
        content=f"{whole1}({num1}/{denom}) - {whole2}({num2}/{denom}) = ? (대분수로)",
        answer=ans_str,
        wrongs=[
            f"{whole1 - whole2}({num1 - num2}/{denom})" if num1 > num2 else f"{whole1 - whole2}",
            f"{ans_whole + 1}({ans_num}/{denom})",
            f"{ans_whole}({ans_num}/{denom})",
        ],
        explanation=f"{whole1}({num1}/{denom}) - {whole2}({num2}/{denom}). "
                    f"받아내림: {whole1 - 1}({denom + num1}/{denom}) - {whole2}({num2}/{denom}) = {ans_str}",
        concept_id="concept-e4-frac-op-02", difficulty=8,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 소수 덧셈/뺄셈
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e4-dec-op-02", difficulty=4)
def e4_dec_add_lv4():
    """소수 한 자리 덧셈."""
    a = round(random.uniform(1.0, 9.9), 1)
    b = round(random.uniform(1.0, 9.9), 1)
    ans = round(a + b, 1)
    return build_mc(
        content=f"{a} + {b} = ?",
        answer=ans,
        wrongs=[
            round(ans + 1.0, 1),
            round(ans - 1.0, 1),
            round(ans + 0.1, 1),
            round(ans - 0.1, 1),
        ],
        explanation=f"{a} + {b} = {ans}",
        concept_id="concept-e4-dec-op-02", difficulty=4,
    )


@register("concept-e4-dec-op-02", difficulty=6)
def e4_dec_add_lv6():
    """소수 두 자리 덧셈."""
    a = round(random.uniform(0.5, 9.99), 2)
    b = round(random.uniform(0.5, 9.99), 2)
    ans = round(a + b, 2)
    return build_mc(
        content=f"{a} + {b} = ?",
        answer=ans,
        wrongs=[
            round(ans + 1.0, 2),
            round(ans - 1.0, 2),
            round(ans + 0.1, 2),
            round(ans - 0.1, 2),
        ],
        explanation=f"{a} + {b} = {ans}",
        concept_id="concept-e4-dec-op-02", difficulty=6,
    )


@register("concept-e4-dec-op-02", difficulty=7)
def e4_dec_sub_lv7():
    """소수 뺄셈 (받아내림 포함)."""
    a = round(random.uniform(5.0, 19.99), 2)
    b = round(random.uniform(1.0, a - 1.0), 2)
    ans = round(a - b, 2)
    return build_mc(
        content=f"{a} - {b} = ?",
        answer=ans,
        wrongs=[
            round(ans + 1.0, 2),
            round(ans - 1.0, 2),
            round(ans + 0.1, 2),
            round(ans - 0.1, 2),
        ],
        explanation=f"{a} - {b} = {ans}",
        concept_id="concept-e4-dec-op-02", difficulty=7,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 빈칸 채우기 (FB) 템플릿
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e4-mul-div-01", difficulty=5)
def e4_mul_fb_lv5():
    a = random.randint(150, 400)
    b = random.randint(15, 40)
    ans = a * b
    return build_fb(
        content=f"{a} x {b} = [answer]",
        answer=str(ans),
        explanation=f"{a} x {b} = {ans}",
        concept_id="concept-e4-mul-div-01", difficulty=5,
    )


@register("concept-e4-mul-div-02", difficulty=5)
def e4_div_fb_lv5():
    b = random.randint(12, 30)
    quotient = random.randint(10, 25)
    a = b * quotient
    return build_fb(
        content=f"{a} ÷ {b} = [answer]",
        answer=str(quotient),
        explanation=f"{a} ÷ {b} = {quotient}",
        concept_id="concept-e4-mul-div-02", difficulty=5,
    )


@register("concept-e4-dec-op-02", difficulty=5)
def e4_dec_fb_lv5():
    a = round(random.uniform(1.5, 9.9), 2)
    b = round(random.uniform(0.5, 5.0), 2)
    ans = round(a + b, 2)
    return build_fb(
        content=f"{a} + {b} = [answer]",
        answer=str(ans),
        explanation=f"{a} + {b} = {ans}",
        concept_id="concept-e4-dec-op-02", difficulty=5,
    )
