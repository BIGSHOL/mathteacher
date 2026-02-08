"""초등 5학년 연산 문제 템플릿.

개념 목록:
- concept-e5-mixed-calc-01: 혼합계산 (사칙연산 순서)
- concept-e5-mixed-calc-02: 괄호가 있는 혼합계산
- concept-e5-divisor-02: 최대공약수, 최소공배수
- concept-e5-frac-add-01: 분모가 다른 분수 덧셈/뺄셈
- concept-e5-frac-mul-02: 분수 x 분수
- concept-e5-dec-mul-01: 소수 x 자연수
- concept-e5-dec-mul-02: 소수 x 소수
"""
import math
import random

from . import register, build_mc, build_fb


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 혼합계산 (사칙연산 순서)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e5-mixed-calc-01", difficulty=4)
def e5_mixed_calc_lv4():
    """덧셈 + 곱셈 (곱셈 먼저)."""
    a = random.randint(2, 10)
    b = random.randint(2, 9)
    c = random.randint(2, 9)
    ans = a + b * c
    wrong1 = (a + b) * c  # 순서 바꾼 오답
    return build_mc(
        content=f"{a} + {b} x {c} = ?",
        answer=ans,
        wrongs=[wrong1, ans + b, ans - b, ans + c],
        explanation=f"곱셈을 먼저: {b} x {c} = {b * c}. "
                    f"{a} + {b * c} = {ans}",
        concept_id="concept-e5-mixed-calc-01", difficulty=4,
    )


@register("concept-e5-mixed-calc-01", difficulty=6)
def e5_mixed_calc_lv6():
    """뺄셈 + 나눗셈."""
    c = random.randint(2, 9)
    b = random.randint(2, 9)
    bc = b * c
    a = random.randint(bc + 5, bc + 20)
    ans = a - bc // c
    return build_mc(
        content=f"{a} - {bc} / {c} = ?",
        answer=ans,
        wrongs=[
            (a - bc) // c,
            a - bc,
            ans + c,
            ans - c,
        ],
        explanation=f"나눗셈을 먼저: {bc} / {c} = {bc // c}. "
                    f"{a} - {bc // c} = {ans}",
        concept_id="concept-e5-mixed-calc-01", difficulty=6,
    )


@register("concept-e5-mixed-calc-01", difficulty=8)
def e5_mixed_calc_lv8():
    """곱셈 + 나눗셈 + 덧셈."""
    a = random.randint(3, 8)
    b = random.randint(2, 5)
    c = random.randint(2, 6)
    d = random.randint(2, 9)
    cd = c * d
    ans = a * b + cd // d
    return build_mc(
        content=f"{a} x {b} + {cd} / {d} = ?",
        answer=ans,
        wrongs=[
            a * (b + cd // d),
            a * b + cd,
            ans + d,
            ans - d,
        ],
        explanation=f"{a} x {b} = {a * b}, {cd} / {d} = {cd // d}. "
                    f"{a * b} + {cd // d} = {ans}",
        concept_id="concept-e5-mixed-calc-01", difficulty=8,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 괄호가 있는 혼합계산
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e5-mixed-calc-02", difficulty=5)
def e5_paren_calc_lv5():
    """(a - b) x c."""
    a = random.randint(10, 30)
    b = random.randint(2, a - 2)
    c = random.randint(2, 9)
    ans = (a - b) * c
    return build_mc(
        content=f"({a} - {b}) x {c} = ?",
        answer=ans,
        wrongs=[
            a - b * c,
            a - b + c,
            ans + c,
            ans - c,
        ],
        explanation=f"괄호 먼저: {a} - {b} = {a - b}. "
                    f"{a - b} x {c} = {ans}",
        concept_id="concept-e5-mixed-calc-02", difficulty=5,
    )


@register("concept-e5-mixed-calc-02", difficulty=7)
def e5_paren_calc_lv7():
    """(a + b) x c + d."""
    a = random.randint(3, 12)
    b = random.randint(2, 10)
    c = random.randint(2, 7)
    d = random.randint(5, 15)
    ans = (a + b) * c + d
    return build_mc(
        content=f"({a} + {b}) x {c} + {d} = ?",
        answer=ans,
        wrongs=[
            (a + b) * (c + d),
            (a + b) * c,
            ans + c,
            ans - c,
        ],
        explanation=f"괄호 먼저: {a} + {b} = {a + b}. "
                    f"{a + b} x {c} = {(a + b) * c}. "
                    f"{(a + b) * c} + {d} = {ans}",
        concept_id="concept-e5-mixed-calc-02", difficulty=7,
    )


@register("concept-e5-mixed-calc-02", difficulty=9)
def e5_paren_calc_lv9():
    """a x (b + c) - d."""
    a = random.randint(3, 9)
    b = random.randint(2, 8)
    c = random.randint(2, 8)
    prod = a * (b + c)
    d = random.randint(5, prod - 5)
    ans = prod - d
    return build_mc(
        content=f"{a} x ({b} + {c}) - {d} = ?",
        answer=ans,
        wrongs=[
            a * b + c - d,
            a * (b + c),
            ans + d,
            ans - a,
        ],
        explanation=f"괄호 먼저: {b} + {c} = {b + c}. "
                    f"{a} x {b + c} = {prod}. "
                    f"{prod} - {d} = {ans}",
        concept_id="concept-e5-mixed-calc-02", difficulty=9,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 최대공약수, 최소공배수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e5-divisor-02", difficulty=4)
def e5_gcd_lv4():
    """작은 수의 최대공약수."""
    gcd_val = random.randint(2, 6)
    a_mul = random.randint(2, 8)
    b_mul = random.randint(2, 8)
    while math.gcd(a_mul, b_mul) != 1:
        b_mul = random.randint(2, 8)
    a = gcd_val * a_mul
    b = gcd_val * b_mul
    return build_mc(
        content=f"{a}와 {b}의 최대공약수는?",
        answer=gcd_val,
        wrongs=[
            gcd_val * 2,
            a_mul,
            b_mul,
            1,
        ],
        explanation=f"{a} = {gcd_val} x {a_mul}, {b} = {gcd_val} x {b_mul}. "
                    f"최대공약수는 {gcd_val}",
        concept_id="concept-e5-divisor-02", difficulty=4,
    )


@register("concept-e5-divisor-02", difficulty=6)
def e5_lcm_lv6():
    """최소공배수."""
    gcd_val = random.randint(2, 6)
    a_mul = random.randint(2, 8)
    b_mul = random.randint(2, 8)
    while math.gcd(a_mul, b_mul) != 1:
        b_mul = random.randint(2, 8)
    a = gcd_val * a_mul
    b = gcd_val * b_mul
    lcm_val = (a * b) // gcd_val
    return build_mc(
        content=f"{a}와 {b}의 최소공배수는?",
        answer=lcm_val,
        wrongs=[
            a * b,
            gcd_val,
            lcm_val // 2,
            a * a_mul,
        ],
        explanation=f"{a}와 {b}의 최대공약수는 {gcd_val}. "
                    f"최소공배수 = {a} x {b} / {gcd_val} = {lcm_val}",
        concept_id="concept-e5-divisor-02", difficulty=6,
    )


@register("concept-e5-divisor-02", difficulty=8)
def e5_gcd_three_lv8():
    """세 수의 최대공약수."""
    gcd_val = random.randint(2, 5)
    a_mul = random.randint(2, 6)
    b_mul = random.randint(2, 6)
    c_mul = random.randint(2, 6)
    while math.gcd(math.gcd(a_mul, b_mul), c_mul) != 1:
        c_mul = random.randint(2, 6)
    a = gcd_val * a_mul
    b = gcd_val * b_mul
    c = gcd_val * c_mul
    return build_mc(
        content=f"{a}, {b}, {c}의 최대공약수는?",
        answer=gcd_val,
        wrongs=[
            gcd_val * 2,
            a_mul,
            math.gcd(a, b),
            1,
        ],
        explanation=f"{a}, {b}, {c}의 최대공약수는 {gcd_val}",
        concept_id="concept-e5-divisor-02", difficulty=8,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 분모가 다른 분수 덧셈/뺄셈
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e5-frac-add-01", difficulty=5)
def e5_frac_diff_add_lv5():
    """분모가 다른 진분수 덧셈."""
    denom1 = random.randint(3, 8)
    denom2 = random.randint(3, 8)
    while denom1 == denom2:
        denom2 = random.randint(3, 8)
    num1 = random.randint(1, denom1 - 1)
    num2 = random.randint(1, denom2 - 1)
    lcm = (denom1 * denom2) // math.gcd(denom1, denom2)
    new_num1 = num1 * (lcm // denom1)
    new_num2 = num2 * (lcm // denom2)
    ans_num = new_num1 + new_num2
    gcd = math.gcd(ans_num, lcm)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = lcm // gcd
    ans_str = f"{ans_num_reduced}/{ans_denom_reduced}" if ans_denom_reduced != 1 else str(ans_num_reduced)
    return build_mc(
        content=f"{num1}/{denom1} + {num2}/{denom2} = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{num1 + num2}/{denom1 + denom2}",
            f"{ans_num}/{lcm}",
            f"{new_num1}/{lcm}",
        ],
        explanation=f"통분: {num1}/{denom1} = {new_num1}/{lcm}, {num2}/{denom2} = {new_num2}/{lcm}. "
                    f"{new_num1}/{lcm} + {new_num2}/{lcm} = {ans_num}/{lcm} = {ans_str}",
        concept_id="concept-e5-frac-add-01", difficulty=5,
    )


@register("concept-e5-frac-add-01", difficulty=7)
def e5_frac_diff_sub_lv7():
    """분모가 다른 진분수 뺄셈."""
    denom1 = random.randint(4, 10)
    denom2 = random.randint(3, 9)
    while denom1 == denom2:
        denom2 = random.randint(3, 9)
    lcm = (denom1 * denom2) // math.gcd(denom1, denom2)
    new_num1 = random.randint(lcm // 2, lcm - 1)
    new_num2 = random.randint(1, new_num1 - 1)
    num1 = new_num1 // (lcm // denom1)
    num2 = new_num2 // (lcm // denom2)
    # 정확한 계산
    new_num1 = num1 * (lcm // denom1)
    new_num2 = num2 * (lcm // denom2)
    ans_num = new_num1 - new_num2
    gcd = math.gcd(ans_num, lcm)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = lcm // gcd
    ans_str = f"{ans_num_reduced}/{ans_denom_reduced}" if ans_denom_reduced != 1 else str(ans_num_reduced)
    return build_mc(
        content=f"{num1}/{denom1} - {num2}/{denom2} = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{abs(num1 - num2)}/{abs(denom1 - denom2)}" if denom1 != denom2 else f"{num1}/{denom1}",
            f"{ans_num}/{lcm}",
            f"{new_num1}/{lcm}",
        ],
        explanation=f"통분: {num1}/{denom1} = {new_num1}/{lcm}, {num2}/{denom2} = {new_num2}/{lcm}. "
                    f"{new_num1}/{lcm} - {new_num2}/{lcm} = {ans_num}/{lcm} = {ans_str}",
        concept_id="concept-e5-frac-add-01", difficulty=7,
    )


@register("concept-e5-frac-add-01", difficulty=9)
def e5_frac_diff_mix_lv9():
    """분모가 다른 세 분수 계산."""
    denom1, denom2, denom3 = 2, 3, 4
    num1 = 1
    num2 = 1
    num3 = 1
    lcm = 12
    new_num1 = num1 * (lcm // denom1)
    new_num2 = num2 * (lcm // denom2)
    new_num3 = num3 * (lcm // denom3)
    ans_num = new_num1 + new_num2 + new_num3
    gcd = math.gcd(ans_num, lcm)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = lcm // gcd
    ans_str = f"{ans_num_reduced}/{ans_denom_reduced}" if ans_denom_reduced != 1 else str(ans_num_reduced)
    return build_mc(
        content=f"1/2 + 1/3 + 1/4 = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{ans_num}/{lcm}",
            f"1",
            f"{ans_num_reduced + 1}/{ans_denom_reduced}",
        ],
        explanation=f"통분: 1/2 = 6/12, 1/3 = 4/12, 1/4 = 3/12. "
                    f"6/12 + 4/12 + 3/12 = 13/12 = {ans_str}",
        concept_id="concept-e5-frac-add-01", difficulty=9,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 분수 x 분수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e5-frac-mul-02", difficulty=5)
def e5_frac_mul_lv5():
    """진분수 x 진분수."""
    denom1 = random.randint(3, 8)
    denom2 = random.randint(3, 8)
    num1 = random.randint(1, denom1 - 1)
    num2 = random.randint(1, denom2 - 1)
    ans_num = num1 * num2
    ans_denom = denom1 * denom2
    gcd = math.gcd(ans_num, ans_denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = ans_denom // gcd
    ans_str = f"{ans_num_reduced}/{ans_denom_reduced}" if ans_denom_reduced != 1 else str(ans_num_reduced)
    return build_mc(
        content=f"{num1}/{denom1} x {num2}/{denom2} = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{ans_num}/{ans_denom}",
            f"{num1 * num2}/{denom1}",
            f"{num1}/{denom1 * denom2}",
        ],
        explanation=f"{num1}/{denom1} x {num2}/{denom2} = {ans_num}/{ans_denom} = {ans_str}",
        concept_id="concept-e5-frac-mul-02", difficulty=5,
    )


@register("concept-e5-frac-mul-02", difficulty=7)
def e5_frac_mul_cancel_lv7():
    """약분 후 곱하기."""
    # 2/3 x 3/4 = 1/2 형태
    a = random.randint(2, 6)
    b = random.randint(a + 1, 9)
    c = a  # 약분 가능하게
    d = random.randint(2, 8)
    while d == b:
        d = random.randint(2, 8)
    ans_num = a * c
    ans_denom = b * d
    gcd = math.gcd(ans_num, ans_denom)
    ans_num_reduced = ans_num // gcd
    ans_denom_reduced = ans_denom // gcd
    ans_str = f"{ans_num_reduced}/{ans_denom_reduced}" if ans_denom_reduced != 1 else str(ans_num_reduced)
    return build_mc(
        content=f"{a}/{b} x {c}/{d} = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{ans_num}/{ans_denom}",
            f"{a * c}/{b}",
            f"{ans_num_reduced + 1}/{ans_denom_reduced}",
        ],
        explanation=f"{a}/{b} x {c}/{d} = {ans_num}/{ans_denom} = {ans_str}",
        concept_id="concept-e5-frac-mul-02", difficulty=7,
    )


@register("concept-e5-frac-mul-02", difficulty=8)
def e5_frac_mul_mixed_lv8():
    """대분수 x 진분수."""
    whole = random.randint(1, 4)
    num1 = random.randint(1, 5)
    denom1 = random.randint(num1 + 1, 8)
    num2 = random.randint(1, 6)
    denom2 = random.randint(num2 + 1, 8)
    # 가분수로 변환
    improper_num = whole * denom1 + num1
    ans_num = improper_num * num2
    ans_denom = denom1 * denom2
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
        content=f"{whole}({num1}/{denom1}) x {num2}/{denom2} = ? (기약분수로)",
        answer=ans_str,
        wrongs=[
            f"{ans_num}/{ans_denom}",
            f"{whole * num2}/{denom2}",
            f"{ans_num_reduced}/{ans_denom_reduced}",
        ],
        explanation=f"{whole}({num1}/{denom1}) = {improper_num}/{denom1}. "
                    f"{improper_num}/{denom1} x {num2}/{denom2} = {ans_num}/{ans_denom} = {ans_str}",
        concept_id="concept-e5-frac-mul-02", difficulty=8,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 소수 x 자연수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e5-dec-mul-01", difficulty=4)
def e5_dec_mul_nat_lv4():
    """소수 한 자리 x 한 자리 수."""
    a = round(random.uniform(1.1, 9.9), 1)
    b = random.randint(2, 9)
    ans = round(a * b, 1)
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[
            round(ans + b, 1),
            round(ans - b, 1),
            round(ans + 1, 1),
            round(ans - 1, 1),
        ],
        explanation=f"{a} x {b} = {ans}",
        concept_id="concept-e5-dec-mul-01", difficulty=4,
    )


@register("concept-e5-dec-mul-01", difficulty=6)
def e5_dec_mul_nat_lv6():
    """소수 두 자리 x 한 자리 수."""
    a = round(random.uniform(1.01, 9.99), 2)
    b = random.randint(3, 9)
    ans = round(a * b, 2)
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[
            round(ans + b, 2),
            round(ans - b, 2),
            round(ans + 0.1, 2),
            round(ans - 0.1, 2),
        ],
        explanation=f"{a} x {b} = {ans}",
        concept_id="concept-e5-dec-mul-01", difficulty=6,
    )


@register("concept-e5-dec-mul-01", difficulty=7)
def e5_dec_mul_nat_lv7():
    """소수 x 두 자리 수."""
    a = round(random.uniform(2.5, 9.9), 1)
    b = random.randint(10, 25)
    ans = round(a * b, 1)
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[
            round(ans + 10, 1),
            round(ans - 10, 1),
            round(ans + a, 1),
            round(ans - a, 1),
        ],
        explanation=f"{a} x {b} = {ans}",
        concept_id="concept-e5-dec-mul-01", difficulty=7,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 소수 x 소수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e5-dec-mul-02", difficulty=6)
def e5_dec_mul_dec_lv6():
    """소수 한 자리 x 소수 한 자리."""
    a = round(random.uniform(0.2, 0.9), 1)
    b = round(random.uniform(0.2, 0.9), 1)
    ans = round(a * b, 2)
    return build_mc(
        content=f"{a} x {b} = ?",
        answer=ans,
        wrongs=[
            round(ans + 0.1, 2),
            round(ans - 0.1, 2),
            round(ans + 0.01, 2),
            round(a + b, 2),
        ],
        explanation=f"{a} x {b} = {ans}",
        concept_id="concept-e5-dec-mul-02", difficulty=6,
    )


@register("concept-e5-dec-mul-02", difficulty=8)
def e5_dec_mul_dec_lv8():
    """소수 두 자리 x 소수 한 자리."""
    a = round(random.uniform(1.01, 9.99), 2)
    b = round(random.uniform(0.2, 0.9), 1)
    ans = round(a * b, 3)
    # 소수점 셋째 자리 반올림
    ans = round(ans, 2)
    return build_mc(
        content=f"{a} x {b} = ? (소수 둘째 자리까지)",
        answer=ans,
        wrongs=[
            round(ans + 0.1, 2),
            round(ans - 0.1, 2),
            round(ans + 1, 2),
            round(a * int(b * 10) / 10, 2),
        ],
        explanation=f"{a} x {b} = {ans}",
        concept_id="concept-e5-dec-mul-02", difficulty=8,
    )


@register("concept-e5-dec-mul-02", difficulty=9)
def e5_dec_mul_dec_lv9():
    """소수 두 자리 x 소수 두 자리."""
    a = round(random.uniform(1.1, 5.9), 1)
    b = round(random.uniform(1.1, 5.9), 1)
    ans = round(a * b, 2)
    return build_mc(
        content=f"{a} x {b} = ? (소수 둘째 자리까지)",
        answer=ans,
        wrongs=[
            round(ans + 1, 2),
            round(ans - 1, 2),
            round(ans + 0.5, 2),
            round(ans - 0.5, 2),
        ],
        explanation=f"{a} x {b} = {ans}",
        concept_id="concept-e5-dec-mul-02", difficulty=9,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 빈칸 채우기 (FB) 템플릿
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@register("concept-e5-mixed-calc-01", difficulty=5)
def e5_mixed_fb_lv5():
    a = random.randint(5, 15)
    b = random.randint(2, 8)
    c = random.randint(2, 9)
    ans = a + b * c
    return build_fb(
        content=f"{a} + {b} x {c} = [answer]",
        answer=str(ans),
        explanation=f"곱셈 먼저: {b} x {c} = {b * c}. {a} + {b * c} = {ans}",
        concept_id="concept-e5-mixed-calc-01", difficulty=5,
    )


@register("concept-e5-divisor-02", difficulty=5)
def e5_gcd_fb_lv5():
    gcd_val = random.randint(3, 8)
    a_mul = random.randint(3, 9)
    b_mul = random.randint(3, 9)
    while math.gcd(a_mul, b_mul) != 1:
        b_mul = random.randint(3, 9)
    a = gcd_val * a_mul
    b = gcd_val * b_mul
    return build_fb(
        content=f"{a}와 {b}의 최대공약수는 [answer]입니다.",
        answer=str(gcd_val),
        explanation=f"{a}와 {b}의 최대공약수는 {gcd_val}",
        concept_id="concept-e5-divisor-02", difficulty=5,
    )


@register("concept-e5-dec-mul-02", difficulty=7)
def e5_dec_mul_fb_lv7():
    a = round(random.uniform(1.1, 9.9), 1)
    b = round(random.uniform(0.2, 0.9), 1)
    ans = round(a * b, 2)
    return build_fb(
        content=f"{a} x {b} = [answer]",
        answer=str(ans),
        explanation=f"{a} x {b} = {ans}",
        concept_id="concept-e5-dec-mul-02", difficulty=7,
    )
