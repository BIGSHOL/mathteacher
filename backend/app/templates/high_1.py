"""고등 1학년 연산 문제 템플릿.

개념 목록:
- concept-h1-polynomial-01: 다항식 연산 (덧셈, 뺄셈, 곱셈, 전개)
- concept-h1-equation-01: 이차방정식 (인수분해, 근의 공식)
- concept-h1-equation-02: 이차부등식 (해의 범위)
"""
import random
import math

from . import register, build_mc, build_fb


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 다항식 연산
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-h1-polynomial-01", difficulty=3)
def h1_poly_add_lv3():
    """(ax²+bx+c)+(dx²+ex+f) 형태."""
    a, b, c = random.randint(1, 5), random.randint(-5, 5), random.randint(-5, 5)
    d, e, f = random.randint(1, 5), random.randint(-5, 5), random.randint(-5, 5)

    ans_a = a + d
    ans_b = b + e
    ans_c = c + f

    def fmt_poly(x2, x1, x0):
        """Format polynomial with proper signs."""
        parts = []
        if x2 != 0:
            parts.append(f"{x2}x²" if x2 != 1 else "x²")
        if x1 != 0:
            if x1 > 0 and parts:
                parts.append(f"+{x1}x" if x1 != 1 else "+x")
            elif x1 < 0:
                parts.append(f"{x1}x" if x1 != -1 else "-x")
            else:
                parts.append(f"{x1}x" if x1 != 1 else "x")
        if x0 != 0:
            if x0 > 0 and parts:
                parts.append(f"+{x0}")
            else:
                parts.append(f"{x0}")
        return "".join(parts) if parts else "0"

    p1 = fmt_poly(a, b, c)
    p2 = fmt_poly(d, e, f)
    answer_str = fmt_poly(ans_a, ans_b, ans_c)

    # Distractors: wrong coefficient combinations
    wrong1 = fmt_poly(ans_a + 1, ans_b, ans_c)
    wrong2 = fmt_poly(ans_a, ans_b - 1, ans_c)
    wrong3 = fmt_poly(ans_a, ans_b, ans_c + 1)

    return build_mc(
        content=f"({p1}) + ({p2}) = ?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"x²계수: {a}+{d}={ans_a}, x계수: {b}+{e}={ans_b}, 상수: {c}+{f}={ans_c}. 답: {answer_str}",
        concept_id="concept-h1-polynomial-01",
        difficulty=3,
        part="algebra",
    )


@register("concept-h1-polynomial-01", difficulty=5)
def h1_poly_mul_binomial_lv5():
    """(x+a)(x+b) 전개."""
    a = random.randint(-8, 8)
    b = random.randint(-8, 8)
    while a == 0 or b == 0:
        a = random.randint(-8, 8)
        b = random.randint(-8, 8)

    # (x+a)(x+b) = x² + (a+b)x + ab
    coef_x = a + b
    const = a * b

    def fmt_binom(n):
        if n > 0:
            return f"x+{n}"
        else:
            return f"x{n}"  # includes minus sign

    def fmt_quad(cx, c0):
        parts = ["x²"]
        if cx > 0:
            parts.append(f"+{cx}x" if cx != 1 else "+x")
        elif cx < 0:
            parts.append(f"{cx}x" if cx != -1 else "-x")

        if c0 > 0:
            parts.append(f"+{c0}")
        elif c0 < 0:
            parts.append(f"{c0}")

        return "".join(parts)

    answer_str = fmt_quad(coef_x, const)

    # Common mistakes
    wrong1 = fmt_quad(coef_x + 1, const)  # wrong x coefficient
    wrong2 = fmt_quad(coef_x, const + a)  # wrong constant
    wrong3 = fmt_quad(a, b)  # forgot to multiply

    return build_mc(
        content=f"({fmt_binom(a)})({fmt_binom(b)})를 전개하면?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"(x+{a})(x+{b}) = x² + ({a}+{b})x + {a}×{b} = x² + {coef_x}x + {const} = {answer_str}",
        concept_id="concept-h1-polynomial-01",
        difficulty=5,
        part="algebra",
    )


@register("concept-h1-polynomial-01", difficulty=7)
def h1_poly_cube_lv7():
    """(x+a)³ 전개."""
    a = random.randint(-3, 3)
    while a == 0:
        a = random.randint(-3, 3)

    # (x+a)³ = x³ + 3ax² + 3a²x + a³
    coef_x2 = 3 * a
    coef_x1 = 3 * a * a
    coef_x0 = a * a * a

    def fmt_cubic(c2, c1, c0):
        parts = ["x³"]
        if c2 > 0:
            parts.append(f"+{c2}x²")
        elif c2 < 0:
            parts.append(f"{c2}x²")

        if c1 > 0:
            parts.append(f"+{c1}x")
        elif c1 < 0:
            parts.append(f"{c1}x")

        if c0 > 0:
            parts.append(f"+{c0}")
        elif c0 < 0:
            parts.append(f"{c0}")

        return "".join(parts)

    answer_str = fmt_cubic(coef_x2, coef_x1, coef_x0)

    # Common mistakes
    wrong1 = fmt_cubic(coef_x2, coef_x1 * 2, coef_x0)  # wrong x coefficient
    wrong2 = fmt_cubic(coef_x2 * 2, coef_x1, coef_x0)  # wrong x² coefficient
    wrong3 = f"x³+{coef_x0}"  # forgot middle terms

    return build_mc(
        content=f"(x{'+' if a > 0 else ''}{a})³를 전개하면?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"(x+a)³ = x³ + 3ax² + 3a²x + a³ 공식 사용. a={a}이므로 {answer_str}",
        concept_id="concept-h1-polynomial-01",
        difficulty=7,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 이차방정식
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-h1-equation-01", difficulty=3)
def h1_quad_factor_lv3():
    """x² + bx + c = 0을 인수분해로 풀기 (근이 정수)."""
    # 근 p, q를 먼저 선택 (정수)
    p = random.randint(-8, 8)
    q = random.randint(-8, 8)
    while p == q:
        q = random.randint(-8, 8)

    # (x-p)(x-q) = x² - (p+q)x + pq
    b = -(p + q)
    c = p * q

    # 근을 정렬하여 표준 형태로
    roots = sorted([p, q])
    answer_str = f"x={roots[0]}, x={roots[1]}"

    # Distractors
    wrong1 = f"x={-roots[0]}, x={-roots[1]}"  # sign error
    wrong2 = f"x={p+q}, x={p*q}"  # confused with coefficients
    wrong3 = f"x={roots[0]+1}, x={roots[1]}"

    def fmt_eq(b_val, c_val):
        parts = ["x²"]
        if b_val > 0:
            parts.append(f"+{b_val}x")
        elif b_val < 0:
            parts.append(f"{b_val}x")

        if c_val > 0:
            parts.append(f"+{c_val}")
        elif c_val < 0:
            parts.append(f"{c_val}")

        return "".join(parts) + "=0"

    return build_mc(
        content=f"{fmt_eq(b, c)}의 해는?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"x²{'+' if b > 0 else ''}{b}x{'+' if c > 0 else ''}{c} = (x-{p})(x-{q}) = 0. 따라서 x={p} 또는 x={q}",
        concept_id="concept-h1-equation-01",
        difficulty=3,
        part="algebra",
    )


@register("concept-h1-equation-01", difficulty=5)
def h1_quad_discriminant_lv5():
    """판별식 D=b²-4ac 계산."""
    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)

    D = b * b - 4 * a * c

    # Distractors
    wrong1 = b * b + 4 * a * c  # sign error
    wrong2 = b * b - 4 * c  # forgot a
    wrong3 = b - 4 * a * c  # forgot to square b

    def fmt_eq(a_val, b_val, c_val):
        parts = []
        if a_val != 1:
            parts.append(f"{a_val}x²")
        else:
            parts.append("x²")

        if b_val > 0:
            parts.append(f"+{b_val}x")
        elif b_val < 0:
            parts.append(f"{b_val}x")
        elif b_val == 0:
            pass

        if c_val > 0:
            parts.append(f"+{c_val}")
        elif c_val < 0:
            parts.append(f"{c_val}")

        return "".join(parts) + "=0"

    return build_mc(
        content=f"{fmt_eq(a, b, c)}의 판별식 D의 값은?",
        answer=D,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"D = b² - 4ac = ({b})² - 4×{a}×{c} = {b*b} - {4*a*c} = {D}",
        concept_id="concept-h1-equation-01",
        difficulty=5,
        part="algebra",
    )


@register("concept-h1-equation-01", difficulty=7)
def h1_quad_formula_lv7():
    """근의 공식 사용 (근이 무리수)."""
    # Pick D that is not a perfect square
    a = 1  # Keep a=1 for simplicity
    b = random.randint(-6, 6)
    while b == 0:
        b = random.randint(-6, 6)

    # Pick c such that D > 0 and not a perfect square
    for _ in range(100):
        c = random.randint(-10, 10)
        D = b * b - 4 * a * c
        if D > 0 and int(math.sqrt(D))**2 != D:
            break

    # x = (-b ± √D) / 2a
    # With a=1: x = (-b ± √D) / 2

    def fmt_root(b_val, d_val):
        """Format the root as a string."""
        if b_val > 0:
            return f"(-{b_val}±√{d_val})/2"
        elif b_val < 0:
            return f"({-b_val}±√{d_val})/2"
        else:
            return f"±√{d_val}/2"

    answer_str = fmt_root(b, D)

    # Distractors
    wrong1 = fmt_root(-b, D)  # forgot negative sign
    wrong2 = fmt_root(b, b*b - 4*c)  # forgot the 'a' in 4ac but kept it in 2a
    wrong3 = f"({-b}±{int(math.sqrt(abs(D)))})/2" if D > 0 else answer_str + "_w"

    def fmt_eq_simple(b_val, c_val):
        parts = ["x²"]
        if b_val > 0:
            parts.append(f"+{b_val}x")
        elif b_val < 0:
            parts.append(f"{b_val}x")

        if c_val > 0:
            parts.append(f"+{c_val}")
        elif c_val < 0:
            parts.append(f"{c_val}")

        return "".join(parts) + "=0"

    return build_mc(
        content=f"{fmt_eq_simple(b, c)}의 해를 근의 공식으로 나타내면?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"근의 공식: x = (-b±√D)/2a. D={b}²-4×1×{c}={D}. x = ({-b}±√{D})/2",
        concept_id="concept-h1-equation-01",
        difficulty=7,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 이차부등식
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-h1-equation-02", difficulty=4)
def h1_quad_ineq_lv4():
    """x² + bx + c < 0 해의 범위 (근이 정수, a>0)."""
    # Pick two integer roots p < q
    p = random.randint(-8, -1)
    q = random.randint(1, 8)

    # (x-p)(x-q) = x² - (p+q)x + pq
    b = -(p + q)
    c = p * q

    # For x² + bx + c < 0 (a=1>0), solution is p < x < q
    answer_str = f"{p}<x<{q}"

    # Distractors
    wrong1 = f"x<{p}, x>{q}"  # wrong inequality
    wrong2 = f"{q}<x<{p}"  # swapped roots
    wrong3 = f"{p}≤x≤{q}"  # used ≤ instead of <

    def fmt_ineq(b_val, c_val):
        parts = ["x²"]
        if b_val > 0:
            parts.append(f"+{b_val}x")
        elif b_val < 0:
            parts.append(f"{b_val}x")

        if c_val > 0:
            parts.append(f"+{c_val}")
        elif c_val < 0:
            parts.append(f"{c_val}")

        return "".join(parts) + "<0"

    return build_mc(
        content=f"{fmt_ineq(b, c)}의 해는?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"x²{'+' if b>0 else ''}{b}x{'+' if c>0 else ''}{c} = (x-{p})(x-{q}). "
                    f"이차항 계수가 양수이므로, 두 근 사이에서 음수. 답: {answer_str}",
        concept_id="concept-h1-equation-02",
        difficulty=4,
        part="algebra",
    )


@register("concept-h1-equation-02", difficulty=6)
def h1_quad_ineq_geq_lv6():
    """x² + bx + c ≥ 0 해의 범위."""
    p = random.randint(-6, -1)
    q = random.randint(1, 6)

    b = -(p + q)
    c = p * q

    # For x² + bx + c ≥ 0 (a>0), solution is x ≤ p or x ≥ q
    answer_str = f"x≤{p}, x≥{q}"

    # Distractors
    wrong1 = f"{p}≤x≤{q}"  # wrong region
    wrong2 = f"x<{p}, x>{q}"  # forgot equal sign
    wrong3 = f"x≤{q}, x≥{p}"  # swapped

    def fmt_ineq_geq(b_val, c_val):
        parts = ["x²"]
        if b_val > 0:
            parts.append(f"+{b_val}x")
        elif b_val < 0:
            parts.append(f"{b_val}x")

        if c_val > 0:
            parts.append(f"+{c_val}")
        elif c_val < 0:
            parts.append(f"{c_val}")

        return "".join(parts) + "≥0"

    return build_mc(
        content=f"{fmt_ineq_geq(b, c)}의 해는?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"(x-{p})(x-{q})≥0. 이차항 계수가 양수이므로 x≤{p} 또는 x≥{q}",
        concept_id="concept-h1-equation-02",
        difficulty=6,
        part="algebra",
    )


@register("concept-h1-equation-02", difficulty=8)
def h1_quad_ineq_negative_a_lv8():
    """-x² + bx + c > 0 (a<0인 경우)."""
    p = random.randint(-5, -1)
    q = random.randint(1, 5)

    # -(x-p)(x-q) = -x² + (p+q)x - pq
    b = p + q
    c = -p * q

    # For -x² + bx + c > 0, i.e., -(x-p)(x-q) > 0, solution is p < x < q
    answer_str = f"{p}<x<{q}"

    # Distractors
    wrong1 = f"x<{p}, x>{q}"  # forgot a<0
    wrong2 = f"{q}<x<{p}"  # wrong order
    wrong3 = f"{p}≤x≤{q}"  # used ≤

    def fmt_ineq_neg(b_val, c_val):
        parts = ["-x²"]
        if b_val > 0:
            parts.append(f"+{b_val}x")
        elif b_val < 0:
            parts.append(f"{b_val}x")

        if c_val > 0:
            parts.append(f"+{c_val}")
        elif c_val < 0:
            parts.append(f"{c_val}")

        return "".join(parts) + ">0"

    return build_mc(
        content=f"{fmt_ineq_neg(b, c)}의 해는?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"-x²{'+' if b>0 else ''}{b}x{'+' if c>0 else ''}{c} = -(x-{p})(x-{q}). "
                    f"이차항 계수가 음수이므로 두 근 사이에서 양수. 답: {answer_str}",
        concept_id="concept-h1-equation-02",
        difficulty=8,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Fill-in-blank variants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-h1-polynomial-01", difficulty=4)
def h1_poly_fb_lv4():
    """(x+a)(x+b) 전개 fill-in-blank."""
    a = random.randint(-5, 5)
    b = random.randint(-5, 5)
    while a == 0 or b == 0:
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)

    coef_x = a + b
    const = a * b

    answer_str = f"x²{'+' if coef_x >= 0 else ''}{coef_x}x{'+' if const >= 0 else ''}{const}"
    answer_str = answer_str.replace("+-", "-")  # clean up

    return build_fb(
        content=f"(x{'+' if a > 0 else ''}{a})(x{'+' if b > 0 else ''}{b}) = [answer]",
        answer=answer_str,
        explanation=f"(x+{a})(x+{b}) = x² + {coef_x}x + {const}",
        concept_id="concept-h1-polynomial-01",
        difficulty=4,
        part="algebra",
    )


@register("concept-h1-equation-01", difficulty=4)
def h1_quad_fb_lv4():
    """이차방정식 해 구하기 (fill-in-blank)."""
    p = random.randint(-6, 6)
    q = random.randint(-6, 6)
    while p == q:
        q = random.randint(-6, 6)

    b = -(p + q)
    c = p * q

    roots = sorted([p, q])
    answer_str = f"{roots[0]},{roots[1]}"

    return build_fb(
        content=f"x²{'+' if b >= 0 else ''}{b}x{'+' if c >= 0 else ''}{c}=0의 두 해를 작은 것부터 쉼표로 구분하여 입력하세요: [answer]",
        answer=answer_str,
        explanation=f"(x-{p})(x-{q})=0이므로 x={p} 또는 x={q}",
        concept_id="concept-h1-equation-01",
        difficulty=4,
        part="algebra",
        accept_formats=[answer_str, f"{roots[1]},{roots[0]}"],  # both orders accepted
    )
