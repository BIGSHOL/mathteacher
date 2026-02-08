"""초등 6학년 연산 문제 템플릿.

개념 목록:
- concept-e6-frac-div1: 분수 ÷ 자연수
- concept-e6-frac-div2: 분수 ÷ 분수
- concept-e6-dec-div1: 소수 ÷ 자연수
- concept-e6-dec-div2: 소수 ÷ 소수
"""
import math
import random

from . import register, build_mc, build_fb


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 분수 ÷ 자연수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e6-frac-div1", difficulty=4)
def e6_frac_div_nat_lv4():
    """진분수 ÷ 자연수."""
    denom = random.randint(4, 12)
    num = random.randint(2, denom - 1)
    divisor = random.randint(2, 5)
    # 결과: num/denom ÷ divisor = num/(denom × divisor)
    ans_num = num
    ans_denom = denom * divisor
    gcd = math.gcd(ans_num, ans_denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = ans_denom // gcd
    ans_str = f"{ans_num_reduced}/{ans_denom_reduced}"
    return build_mc(
        content=f"{num}/{denom} ÷ {divisor} = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{num}/{denom}",
            f"{num * divisor}/{denom}",
            f"{ans_num}/{ans_denom}",
        ],
        explanation=f"{num}/{denom} ÷ {divisor} = {num}/{denom} x 1/{divisor} = "
                    f"{ans_num}/{ans_denom} = {ans_str}",
        concept_id="concept-e6-frac-div1", difficulty=4,
    )


@register("concept-e6-frac-div1", difficulty=6)
def e6_frac_div_nat_lv6():
    """가분수 ÷ 자연수."""
    denom = random.randint(3, 8)
    num = random.randint(denom + 1, denom * 3)
    divisor = random.randint(2, 6)
    ans_num = num
    ans_denom = denom * divisor
    gcd = math.gcd(ans_num, ans_denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = ans_denom // gcd
    # 대분수로 변환
    ans_whole = ans_num_reduced // ans_denom_reduced
    ans_remainder = ans_num_reduced % ans_denom_reduced
    if ans_remainder == 0:
        ans_str = str(ans_whole)
    elif ans_whole == 0:
        ans_str = f"{ans_remainder}/{ans_denom_reduced}"
    else:
        ans_str = f"{ans_whole}({ans_remainder}/{ans_denom_reduced})"
    return build_mc(
        content=f"{num}/{denom} ÷ {divisor} = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{num}/{denom}",
            f"{ans_num_reduced}/{ans_denom_reduced}",
            f"{ans_whole}" if ans_remainder != 0 else f"{ans_whole + 1}",
        ],
        explanation=f"{num}/{denom} ÷ {divisor} = {num}/{denom} x 1/{divisor} = "
                    f"{ans_num}/{ans_denom} = {ans_str}",
        concept_id="concept-e6-frac-div1", difficulty=6,
    )


@register("concept-e6-frac-div1", difficulty=8)
def e6_frac_div_nat_lv8():
    """대분수 ÷ 자연수."""
    whole = random.randint(2, 6)
    num = random.randint(1, 7)
    denom = random.randint(num + 1, 10)
    divisor = random.randint(2, 5)
    # 가분수로 변환
    improper_num = whole * denom + num
    ans_num = improper_num
    ans_denom = denom * divisor
    gcd = math.gcd(ans_num, ans_denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = ans_denom // gcd
    # 대분수로 변환
    ans_whole = ans_num_reduced // ans_denom_reduced
    ans_remainder = ans_num_reduced % ans_denom_reduced
    if ans_remainder == 0:
        ans_str = str(ans_whole)
    elif ans_whole == 0:
        ans_str = f"{ans_remainder}/{ans_denom_reduced}"
    else:
        ans_str = f"{ans_whole}({ans_remainder}/{ans_denom_reduced})"
    return build_mc(
        content=f"{whole}({num}/{denom}) ÷ {divisor} = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{whole // divisor}({num}/{denom})" if whole >= divisor else f"{whole}({num}/{denom})",
            f"{ans_num_reduced}/{ans_denom_reduced}",
            f"{ans_whole}" if ans_remainder != 0 else f"{ans_whole + 1}",
        ],
        explanation=f"{whole}({num}/{denom}) = {improper_num}/{denom}. "
                    f"{improper_num}/{denom} ÷ {divisor} = {improper_num}/{denom * divisor} = {ans_str}",
        concept_id="concept-e6-frac-div1", difficulty=8,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 분수 ÷ 분수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e6-frac-div2", difficulty=5)
def e6_frac_div_frac_lv5():
    """진분수 ÷ 진분수."""
    denom1 = random.randint(3, 8)
    num1 = random.randint(2, denom1 - 1)
    denom2 = random.randint(3, 8)
    num2 = random.randint(2, denom2 - 1)
    # 결과: (num1/denom1) ÷ (num2/denom2) = (num1 × denom2) / (denom1 × num2)
    ans_num = num1 * denom2
    ans_denom = denom1 * num2
    gcd = math.gcd(ans_num, ans_denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = ans_denom // gcd
    # 대분수로 변환
    ans_whole = ans_num_reduced // ans_denom_reduced
    ans_remainder = ans_num_reduced % ans_denom_reduced
    if ans_remainder == 0:
        ans_str = str(ans_whole)
    elif ans_whole == 0:
        ans_str = f"{ans_remainder}/{ans_denom_reduced}"
    else:
        ans_str = f"{ans_whole}({ans_remainder}/{ans_denom_reduced})"
    return build_mc(
        content=f"{num1}/{denom1} ÷ {num2}/{denom2} = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{num1 * num2}/{denom1 * denom2}",
            f"{ans_num}/{ans_denom}",
            f"{ans_num_reduced}/{ans_denom_reduced}",
        ],
        explanation=f"{num1}/{denom1} ÷ {num2}/{denom2} = {num1}/{denom1} x {denom2}/{num2} = "
                    f"{ans_num}/{ans_denom} = {ans_str}",
        concept_id="concept-e6-frac-div2", difficulty=5,
    )


@register("concept-e6-frac-div2", difficulty=7)
def e6_frac_div_frac_lv7():
    """가분수 ÷ 진분수."""
    denom1 = random.randint(3, 7)
    num1 = random.randint(denom1 + 1, denom1 * 2)
    denom2 = random.randint(3, 7)
    num2 = random.randint(1, denom2 - 1)
    ans_num = num1 * denom2
    ans_denom = denom1 * num2
    gcd = math.gcd(ans_num, ans_denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = ans_denom // gcd
    # 대분수로 변환
    ans_whole = ans_num_reduced // ans_denom_reduced
    ans_remainder = ans_num_reduced % ans_denom_reduced
    if ans_remainder == 0:
        ans_str = str(ans_whole)
    elif ans_whole == 0:
        ans_str = f"{ans_remainder}/{ans_denom_reduced}"
    else:
        ans_str = f"{ans_whole}({ans_remainder}/{ans_denom_reduced})"
    return build_mc(
        content=f"{num1}/{denom1} ÷ {num2}/{denom2} = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{ans_num}/{ans_denom}",
            f"{ans_num_reduced}/{ans_denom_reduced}",
            f"{ans_whole}" if ans_remainder != 0 else f"{ans_whole + 1}",
        ],
        explanation=f"{num1}/{denom1} ÷ {num2}/{denom2} = {num1}/{denom1} x {denom2}/{num2} = "
                    f"{ans_num}/{ans_denom} = {ans_str}",
        concept_id="concept-e6-frac-div2", difficulty=7,
    )


@register("concept-e6-frac-div2", difficulty=9)
def e6_frac_div_frac_lv9():
    """대분수 ÷ 대분수."""
    whole1 = random.randint(1, 4)
    num1 = random.randint(1, 5)
    denom1 = random.randint(num1 + 1, 8)
    whole2 = random.randint(1, 3)
    num2 = random.randint(1, 5)
    denom2 = random.randint(num2 + 1, 8)
    # 가분수로 변환
    improper_num1 = whole1 * denom1 + num1
    improper_num2 = whole2 * denom2 + num2
    ans_num = improper_num1 * denom2
    ans_denom = denom1 * improper_num2
    gcd = math.gcd(ans_num, ans_denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = ans_denom // gcd
    # 대분수로 변환
    ans_whole = ans_num_reduced // ans_denom_reduced
    ans_remainder = ans_num_reduced % ans_denom_reduced
    if ans_remainder == 0:
        ans_str = str(ans_whole)
    elif ans_whole == 0:
        ans_str = f"{ans_remainder}/{ans_denom_reduced}"
    else:
        ans_str = f"{ans_whole}({ans_remainder}/{ans_denom_reduced})"
    return build_mc(
        content=f"{whole1}({num1}/{denom1}) ÷ {whole2}({num2}/{denom2}) = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{ans_num_reduced}/{ans_denom_reduced}",
            f"{whole1 // whole2}" if whole1 >= whole2 else "1",
            f"{ans_whole}" if ans_remainder != 0 else f"{ans_whole + 1}",
        ],
        explanation=f"{whole1}({num1}/{denom1}) = {improper_num1}/{denom1}, "
                    f"{whole2}({num2}/{denom2}) = {improper_num2}/{denom2}. "
                    f"{improper_num1}/{denom1} ÷ {improper_num2}/{denom2} = "
                    f"{improper_num1}/{denom1} x {denom2}/{improper_num2} = {ans_str}",
        concept_id="concept-e6-frac-div2", difficulty=9,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 소수 ÷ 자연수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e6-dec-div1", difficulty=4)
def e6_dec_div_nat_lv4():
    """소수 한 자리 ÷ 한 자리 수 (나누어떨어짐)."""
    divisor = random.randint(2, 9)
    quotient = round(random.uniform(1.1, 9.9), 1)
    dividend = round(quotient * divisor, 1)
    ans = quotient
    return build_mc(
        content=f"{dividend} ÷ {divisor} = ?",
        answer=ans,
        wrongs=[
            round(ans + 1, 1),
            round(ans - 1, 1),
            round(ans + 0.1, 1),
            round(ans - 0.1, 1),
        ],
        explanation=f"{dividend} ÷ {divisor} = {ans}",
        concept_id="concept-e6-dec-div1", difficulty=4,
    )


@register("concept-e6-dec-div1", difficulty=6)
def e6_dec_div_nat_lv6():
    """소수 두 자리 ÷ 한 자리 수."""
    divisor = random.randint(2, 9)
    quotient = round(random.uniform(1.1, 9.99), 2)
    dividend = round(quotient * divisor, 2)
    ans = round(dividend / divisor, 2)
    return build_mc(
        content=f"{dividend} ÷ {divisor} = ? (소수 둘째 자리까지)",
        answer=ans,
        wrongs=[
            round(ans + 1, 2),
            round(ans - 1, 2),
            round(ans + 0.1, 2),
            round(ans - 0.1, 2),
        ],
        explanation=f"{dividend} ÷ {divisor} = {ans}",
        concept_id="concept-e6-dec-div1", difficulty=6,
    )


@register("concept-e6-dec-div1", difficulty=8)
def e6_dec_div_nat_lv8():
    """자연수 ÷ 자연수 = 소수 (몫을 소수로)."""
    divisor = random.randint(4, 8)
    whole = random.randint(5, 30)
    dividend = whole
    ans = round(dividend / divisor, 2)
    return build_mc(
        content=f"{dividend} ÷ {divisor} = ? (소수 둘째 자리까지)",
        answer=ans,
        wrongs=[
            round(ans + 1, 2),
            round(ans - 1, 2),
            whole // divisor,
            round(ans + 0.5, 2),
        ],
        explanation=f"{dividend} ÷ {divisor} = {ans}",
        concept_id="concept-e6-dec-div1", difficulty=8,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 소수 ÷ 소수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e6-dec-div2", difficulty=6)
def e6_dec_div_dec_lv6():
    """소수 한 자리 ÷ 소수 한 자리."""
    divisor = round(random.uniform(0.2, 0.9), 1)
    quotient = random.randint(2, 9)
    dividend = round(divisor * quotient, 1)
    ans = quotient
    return build_mc(
        content=f"{dividend} ÷ {divisor} = ?",
        answer=ans,
        wrongs=[
            ans + 1,
            ans - 1,
            ans + 2,
            round(dividend * divisor, 1),
        ],
        explanation=f"{dividend} ÷ {divisor} = {dividend} ÷ {divisor} x 10/10 = "
                    f"{dividend * 10} ÷ {divisor * 10} = {ans}",
        concept_id="concept-e6-dec-div2", difficulty=6,
    )


@register("concept-e6-dec-div2", difficulty=8)
def e6_dec_div_dec_lv8():
    """소수 ÷ 소수 (결과가 소수)."""
    divisor = round(random.uniform(0.5, 2.0), 1)
    dividend = round(random.uniform(3.0, 15.0), 1)
    ans = round(dividend / divisor, 1)
    return build_mc(
        content=f"{dividend} ÷ {divisor} = ? (소수 첫째 자리까지)",
        answer=ans,
        wrongs=[
            round(ans + 1, 1),
            round(ans - 1, 1),
            round(ans + 0.5, 1),
            round(ans - 0.5, 1),
        ],
        explanation=f"{dividend} ÷ {divisor} = {ans}",
        concept_id="concept-e6-dec-div2", difficulty=8,
    )


@register("concept-e6-dec-div2", difficulty=9)
def e6_dec_div_dec_lv9():
    """복잡한 소수 나눗셈."""
    divisor = round(random.uniform(1.2, 3.5), 1)
    dividend = round(random.uniform(8.0, 25.0), 1)
    ans = round(dividend / divisor, 2)
    return build_mc(
        content=f"{dividend} ÷ {divisor} = ? (소수 둘째 자리까지)",
        answer=ans,
        wrongs=[
            round(ans + 1, 2),
            round(ans - 1, 2),
            round(ans + 0.5, 2),
            round(ans * 0.5, 2),
        ],
        explanation=f"{dividend} ÷ {divisor} = {ans}",
        concept_id="concept-e6-dec-div2", difficulty=9,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 빈칸 채우기 (FB) 템플릿
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e6-frac-div1", difficulty=5)
def e6_frac_div_nat_fb_lv5():
    denom = random.randint(4, 10)
    num = random.randint(2, denom - 1)
    divisor = random.randint(2, 5)
    ans_num = num
    ans_denom = denom * divisor
    gcd = math.gcd(ans_num, ans_denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = ans_denom // gcd
    ans_str = f"{ans_num_reduced}/{ans_denom_reduced}"
    return build_fb(
        content=f"{num}/{denom} ÷ {divisor} = [answer] (기약분수로, 예: 1/2)",
        answer=ans_str,
        explanation=f"{num}/{denom} ÷ {divisor} = {ans_str}",
        concept_id="concept-e6-frac-div1", difficulty=5,
    )


@register("concept-e6-frac-div2", difficulty=6)
def e6_frac_div_frac_fb_lv6():
    denom1 = random.randint(3, 8)
    num1 = random.randint(2, denom1 - 1)
    denom2 = random.randint(3, 8)
    num2 = random.randint(2, denom2 - 1)
    ans_num = num1 * denom2
    ans_denom = denom1 * num2
    gcd = math.gcd(ans_num, ans_denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = ans_denom // gcd
    ans_whole = ans_num_reduced // ans_denom_reduced
    ans_remainder = ans_num_reduced % ans_denom_reduced
    if ans_remainder == 0:
        ans_str = str(ans_whole)
    elif ans_whole == 0:
        ans_str = f"{ans_remainder}/{ans_denom_reduced}"
    else:
        ans_str = f"{ans_whole}({ans_remainder}/{ans_denom_reduced})"
    return build_fb(
        content=f"{num1}/{denom1} ÷ {num2}/{denom2} = [answer] (기약분수로, 예: 2(1/3))",
        answer=ans_str,
        explanation=f"{num1}/{denom1} ÷ {num2}/{denom2} = {ans_str}",
        concept_id="concept-e6-frac-div2", difficulty=6,
    )


@register("concept-e6-dec-div2", difficulty=7)
def e6_dec_div_dec_fb_lv7():
    divisor = round(random.uniform(0.5, 2.5), 1)
    dividend = round(random.uniform(5.0, 20.0), 1)
    ans = round(dividend / divisor, 1)
    return build_fb(
        content=f"{dividend} ÷ {divisor} = [answer] (소수 첫째 자리까지)",
        answer=str(ans),
        explanation=f"{dividend} ÷ {divisor} = {ans}",
        concept_id="concept-e6-dec-div2", difficulty=7,
    )
