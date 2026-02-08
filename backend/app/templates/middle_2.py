"""중등 2학년 연산 문제 템플릿.

개념 목록:
- concept-m2-expr-01: 지수법칙
- concept-m2-ineq-01: 일차부등식 기본
- concept-m2-ineq-02: 복잡한 일차부등식
- concept-m2-simul-01: 연립방정식
"""
import random

from . import register, build_mc, build_fb, sup


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 지수법칙
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m2-expr-01", difficulty=3)
def m2_exponent_mult_lv3():
    """거듭제곱의 곱셈 (aᵐ × aⁿ = aᵐ⁺ⁿ)."""
    var = random.choice(["a", "x", "y"])
    m = random.randint(2, 5)
    n = random.randint(2, 4)
    ans_exp = m + n

    return build_mc(
        content=f"{var}{sup(m)} × {var}{sup(n)} = ?",
        answer=f"{var}{sup(ans_exp)}",
        wrongs=[
            f"{var}{sup(m * n)}",
            f"{var}{sup(abs(m - n))}",
            f"{m + n}{var}",
            f"{var}{sup(ans_exp + 1)}",
        ],
        explanation=f"{var}{sup(m)} × {var}{sup(n)} = {var}{sup(f'{m}+{n}')} = {var}{sup(ans_exp)}",
        concept_id="concept-m2-expr-01", difficulty=3,
        part="algebra",
    )


@register("concept-m2-expr-01", difficulty=5)
def m2_exponent_power_lv5():
    """거듭제곱의 거듭제곱 ((aᵐ)ⁿ = aᵐⁿ)."""
    var = random.choice(["a", "b", "x"])
    m = random.randint(2, 4)
    n = random.randint(2, 3)
    ans_exp = m * n

    return build_mc(
        content=f"({var}{sup(m)}){sup(n)} = ?",
        answer=f"{var}{sup(ans_exp)}",
        wrongs=[
            f"{var}{sup(m + n)}",
            f"{var}{sup(m ** n)}",
            f"{var}{sup(n)}",
            f"{var}{sup(ans_exp - 1)}",
        ],
        explanation=f"({var}{sup(m)}){sup(n)} = {var}{sup(f'{m}×{n}')} = {var}{sup(ans_exp)}",
        concept_id="concept-m2-expr-01", difficulty=5,
        part="algebra",
    )


@register("concept-m2-expr-01", difficulty=7)
def m2_exponent_div_lv7():
    """거듭제곱의 나눗셈 (aᵐ / aⁿ = aᵐ⁻ⁿ)."""
    var = random.choice(["a", "x", "y"])
    m = random.randint(5, 9)
    n = random.randint(2, m - 1)
    ans_exp = m - n

    return build_mc(
        content=f"{var}{sup(m)} / {var}{sup(n)} = ?",
        answer=f"{var}{sup(ans_exp)}",
        wrongs=[
            f"{var}{sup(m + n)}",
            f"{var}{sup(n - m)}",
            f"{var}{sup(m // n)}",
            f"{var}{sup(ans_exp + 1)}",
        ],
        explanation=f"{var}{sup(m)} / {var}{sup(n)} = {var}{sup(f'{m}-{n}')} = {var}{sup(ans_exp)}",
        concept_id="concept-m2-expr-01", difficulty=7,
        part="algebra",
    )


@register("concept-m2-expr-01", difficulty=8)
def m2_exponent_mixed_lv8():
    """혼합 지수법칙 ((ab)ⁿ = aⁿ × bⁿ)."""
    var1 = "a"
    var2 = "b"
    n = random.randint(2, 4)
    sn = sup(n)

    return build_mc(
        content=f"({var1}{var2}){sn} = ?",
        answer=f"{var1}{sn}{var2}{sn}",
        wrongs=[
            f"{var1}{var2}{sn}",
            f"{var1}{sn}{var2}",
            f"{var1}{sn}+{var2}{sn}",
            f"{n}{var1}{var2}",
        ],
        explanation=f"({var1}{var2}){sn} = {var1}{sn} × {var2}{sn} = {var1}{sn}{var2}{sn}",
        concept_id="concept-m2-expr-01", difficulty=8,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 일차부등식 기본
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m2-ineq-01", difficulty=3)
def m2_ineq_basic_lv3():
    """기본 일차부등식 (x + a < b)."""
    ans = random.randint(1, 12)
    a = random.randint(2, 8)
    b = ans + a

    return build_mc(
        content=f"x + {a} < {b}의 해는?",
        answer=f"x < {ans}",
        wrongs=[
            f"x > {ans}",
            f"x < {ans + 1}",
            f"x ≤ {ans}",
            f"x > {b - a + 1}",
        ],
        explanation=f"x < {b} - {a} = {ans}",
        concept_id="concept-m2-ineq-01", difficulty=3,
        part="algebra",
    )


@register("concept-m2-ineq-01", difficulty=5)
def m2_ineq_negative_lv5():
    """음수로 나누기 (부등호 방향 바뀜)."""
    ans = random.randint(1, 10)
    a = random.randint(-5, -2)
    b = a * ans

    return build_mc(
        content=f"{a}x > {b}의 해는?",
        answer=f"x < {ans}",
        wrongs=[
            f"x > {ans}",
            f"x < {-ans}",
            f"x > {-ans}",
            f"x ≤ {ans}",
        ],
        explanation=f"양변을 {a}로 나누면 부등호 방향이 바뀝니다. x < {b}/{a} = {ans}",
        concept_id="concept-m2-ineq-01", difficulty=5,
        part="algebra",
    )


@register("concept-m2-ineq-01", difficulty=7)
def m2_ineq_coefficient_lv7():
    """계수가 있는 일차부등식 (ax + b ≤ c)."""
    ans = random.randint(3, 15)
    a = random.randint(2, 5)
    b = random.randint(-6, -1)
    c = a * ans + b

    b_str = str(b) if b < 0 else f"+{b}"

    return build_mc(
        content=f"{a}x{b_str} ≤ {c}의 해는?",
        answer=f"x ≤ {ans}",
        wrongs=[
            f"x ≥ {ans}",
            f"x < {ans}",
            f"x ≤ {ans + 1}",
            f"x ≤ {c - b}",
        ],
        explanation=f"{a}x ≤ {c} - ({b}) = {c - b}. x ≤ {c - b}/{a} = {ans}",
        concept_id="concept-m2-ineq-01", difficulty=7,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 복잡한 일차부등식
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m2-ineq-02", difficulty=5)
def m2_ineq_both_sides_lv5():
    """양변에 x가 있는 부등식 (ax + b > cx + d)."""
    ans = random.randint(2, 10)
    a = random.randint(3, 6)
    c = random.randint(1, a - 1)
    b = random.randint(1, 8)
    d = (a - c) * ans + b

    return build_mc(
        content=f"{a}x + {b} > {c}x + {d}의 해는?",
        answer=f"x > {ans}",
        wrongs=[
            f"x < {ans}",
            f"x > {ans + 1}",
            f"x ≥ {ans}",
            f"x > {d - b}",
        ],
        explanation=f"{a}x - {c}x > {d} - {b}. {a - c}x > {d - b}. x > {ans}",
        concept_id="concept-m2-ineq-02", difficulty=5,
        part="algebra",
    )


@register("concept-m2-ineq-02", difficulty=7)
def m2_ineq_distribute_lv7():
    """괄호가 있는 부등식 (-a(x - b) < c)."""
    ans = random.randint(3, 12)
    a = random.randint(2, 4)
    b = random.randint(1, 6)
    # -a(x - b) < c → -ax + ab < c → -ax < c - ab → x > (ab - c) / a
    c = a * b - a * ans

    return build_mc(
        content=f"-{a}(x - {b}) < {c}의 해는?",
        answer=f"x > {ans}",
        wrongs=[
            f"x < {ans}",
            f"x > {-ans}",
            f"x < {-ans}",
            f"x > {ans - 1}",
        ],
        explanation=f"-{a}x + {a * b} < {c}. -{a}x < {c - a * b}. x > {ans}",
        concept_id="concept-m2-ineq-02", difficulty=7,
        part="algebra",
    )


@register("concept-m2-ineq-02", difficulty=8)
def m2_ineq_fraction_lv8():
    """분수 계수 부등식."""
    ans = random.randint(4, 16)
    # (x + a) / 2 ≥ b → x + a ≥ 2b → x ≥ 2b - a
    a = random.randint(2, 8)
    b = (ans + a) // 2

    return build_mc(
        content=f"(x + {a}) / 2 ≥ {b}의 해는?",
        answer=f"x ≥ {ans}",
        wrongs=[
            f"x ≤ {ans}",
            f"x ≥ {ans + 1}",
            f"x ≥ {2 * b}",
            f"x > {ans}",
        ],
        explanation=f"x + {a} ≥ {2 * b}. x ≥ {2 * b - a} = {ans}",
        concept_id="concept-m2-ineq-02", difficulty=8,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 연립방정식
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m2-simul-01", difficulty=5)
def m2_simul_basic_lv5():
    """기본 연립방정식 (x + y = a, x - y = b)."""
    x_ans = random.randint(3, 10)
    y_ans = random.randint(1, 8)
    a = x_ans + y_ans
    b = x_ans - y_ans

    return build_mc(
        content=f"x + y = {a}, x - y = {b}의 해는?",
        answer=f"x={x_ans}, y={y_ans}",
        wrongs=[
            f"x={y_ans}, y={x_ans}",
            f"x={x_ans + 1}, y={y_ans}",
            f"x={x_ans}, y={y_ans + 1}",
            f"x={a}, y={b}",
        ],
        explanation=f"두 식을 더하면 2x = {a + b}, x = {x_ans}. "
                    f"첫 식에 대입하면 y = {a} - {x_ans} = {y_ans}",
        concept_id="concept-m2-simul-01", difficulty=5,
        part="algebra",
    )


@register("concept-m2-simul-01", difficulty=7)
def m2_simul_coefficient_lv7():
    """계수가 있는 연립방정식 (ax + by = c, dx + ey = f)."""
    x_ans = random.randint(2, 7)
    y_ans = random.randint(1, 6)
    a = random.randint(2, 4)
    b = random.randint(1, 3)
    d = random.randint(1, 3)
    e = random.randint(2, 4)
    c = a * x_ans + b * y_ans
    f = d * x_ans + e * y_ans

    return build_mc(
        content=f"{a}x + {b}y = {c}, {d}x + {e}y = {f}의 해는?",
        answer=f"x={x_ans}, y={y_ans}",
        wrongs=[
            f"x={y_ans}, y={x_ans}",
            f"x={x_ans + 1}, y={y_ans}",
            f"x={x_ans}, y={y_ans + 1}",
            f"x={x_ans - 1}, y={y_ans + 1}",
        ],
        explanation=f"연립방정식을 풀면 x = {x_ans}, y = {y_ans}",
        concept_id="concept-m2-simul-01", difficulty=7,
        part="algebra",
    )


@register("concept-m2-simul-01", difficulty=8)
def m2_simul_negative_lv8():
    """음수 해를 갖는 연립방정식."""
    x_ans = random.randint(-6, -1)
    y_ans = random.randint(3, 9)
    a = 2
    b = 3
    c = a * x_ans + b * y_ans
    d = 1
    e = -1
    f = d * x_ans + e * y_ans

    return build_mc(
        content=f"{a}x + {b}y = {c}, x - y = {f}의 해는?",
        answer=f"x={x_ans}, y={y_ans}",
        wrongs=[
            f"x={-x_ans}, y={y_ans}",
            f"x={x_ans}, y={-y_ans}",
            f"x={y_ans}, y={x_ans}",
            f"x={x_ans + 1}, y={y_ans - 1}",
        ],
        explanation=f"연립방정식을 풀면 x = {x_ans}, y = {y_ans}",
        concept_id="concept-m2-simul-01", difficulty=8,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 빈칸 채우기 (Fill-in-blank)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m2-expr-01", difficulty=4)
def m2_exponent_fb_lv4():
    var = random.choice(["a", "x", "y"])
    m = random.randint(3, 6)
    n = random.randint(2, 4)
    ans_exp = m + n

    return build_fb(
        content=f"{var}{sup(m)} × {var}{sup(n)} = {var}^[answer]",
        answer=str(ans_exp),
        explanation=f"{var}{sup(m)} × {var}{sup(n)} = {var}{sup(ans_exp)}",
        concept_id="concept-m2-expr-01", difficulty=4,
        part="algebra",
    )


@register("concept-m2-ineq-01", difficulty=4)
def m2_ineq_fb_lv4():
    ans = random.randint(2, 15)
    a = random.randint(-4, -2)
    b = a * ans

    return build_fb(
        content=f"{a}x ≥ {b}일 때, x ≤ [answer]",
        answer=str(ans),
        explanation=f"양변을 {a}로 나누면 부등호 방향이 바뀝니다. x ≤ {ans}",
        concept_id="concept-m2-ineq-01", difficulty=4,
        part="algebra",
    )


@register("concept-m2-simul-01", difficulty=6)
def m2_simul_fb_lv6():
    x_ans = random.randint(2, 9)
    y_ans = random.randint(1, 7)
    a = x_ans + y_ans
    b = x_ans - y_ans

    return build_fb(
        content=f"x + y = {a}, x - y = {b}일 때, x = [answer]",
        answer=str(x_ans),
        explanation=f"두 식을 더하면 2x = {a + b}, x = {x_ans}",
        concept_id="concept-m2-simul-01", difficulty=6,
        part="algebra",
    )
