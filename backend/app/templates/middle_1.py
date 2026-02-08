"""중등 1학년 연산 문제 템플릿.

개념 목록:
- concept-m1-prime-02: 소인수분해
- concept-m1-prime-03: 최대공약수와 최소공배수
- concept-m1-int-02: 절댓값
- concept-m1-int-03: 정수의 사칙연산
- concept-m1-expr-02: 동류항 정리
- concept-m1-expr-03: 식의 값 (대입)
- concept-m1-eq-02: 일차방정식 풀이
"""
import random
import math

from . import register, build_mc, build_fb


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 소인수분해
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _prime_factorize(n: int) -> dict[int, int]:
    """소인수분해 결과를 {소수: 지수} dict로 반환."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def _factorization_str(factors: dict[int, int]) -> str:
    """소인수분해 결과를 문자열로 변환. 예: {2:3, 3:2} -> "2³×3²"."""
    parts = []
    for prime in sorted(factors.keys()):
        exp = factors[prime]
        if exp == 1:
            parts.append(str(prime))
        else:
            # Use superscript for exponents
            superscripts = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
            parts.append(f"{prime}{str(exp).translate(superscripts)}")
    return "×".join(parts) if parts else "1"


@register("concept-m1-prime-02", difficulty=3)
def m1_prime_factor_lv3():
    """작은 수의 소인수분해."""
    candidates = [12, 18, 20, 24, 30, 36, 40, 45, 48, 50, 54, 60]
    n = random.choice(candidates)
    factors = _prime_factorize(n)
    ans = _factorization_str(factors)

    # 오답: 잘못된 지수, 누락된 소인수
    wrongs = []
    if 2 in factors:
        wrong_factors = factors.copy()
        wrong_factors[2] = (wrong_factors[2] + 1) % 4 or 1
        wrongs.append(_factorization_str(wrong_factors))
    if 3 in factors:
        wrong_factors = factors.copy()
        wrong_factors[3] = (wrong_factors[3] + 1) % 3 or 1
        wrongs.append(_factorization_str(wrong_factors))

    # 추가 오답
    wrongs.append(f"{n}")
    wrongs.append(_factorization_str({p: 1 for p in factors}))

    return build_mc(
        content=f"{n}을 소인수분해하면?",
        answer=ans,
        wrongs=wrongs,
        explanation=f"{n} = {ans}",
        concept_id="concept-m1-prime-02", difficulty=3,
        part="calc",
    )


@register("concept-m1-prime-02", difficulty=5)
def m1_prime_factor_lv5():
    """중간 크기의 소인수분해."""
    candidates = [72, 84, 90, 96, 100, 108, 120, 144, 150, 180]
    n = random.choice(candidates)
    factors = _prime_factorize(n)
    ans = _factorization_str(factors)

    wrongs = []
    # 지수 ±1 오류
    for p in factors:
        wrong_factors = factors.copy()
        if wrong_factors[p] > 1:
            wrong_factors[p] -= 1
            wrongs.append(_factorization_str(wrong_factors))
        wrong_factors = factors.copy()
        wrong_factors[p] += 1
        wrongs.append(_factorization_str(wrong_factors))

    wrongs.append(str(n))

    return build_mc(
        content=f"{n}을 소인수분해하면?",
        answer=ans,
        wrongs=wrongs,
        explanation=f"{n} = {ans}",
        concept_id="concept-m1-prime-02", difficulty=5,
        part="calc",
    )


@register("concept-m1-prime-02", difficulty=7)
def m1_prime_factor_lv7():
    """큰 수의 소인수분해."""
    candidates = [200, 216, 240, 250, 288, 300, 360, 400, 432, 500]
    n = random.choice(candidates)
    factors = _prime_factorize(n)
    ans = _factorization_str(factors)

    wrongs = []
    # 다양한 오류 패턴
    for p in list(factors.keys())[:2]:
        wrong_factors = factors.copy()
        wrong_factors[p] = max(1, wrong_factors[p] - 1)
        wrongs.append(_factorization_str(wrong_factors))

    # 소인수 누락
    if len(factors) > 2:
        wrong_factors = {k: v for k, v in list(factors.items())[:-1]}
        wrongs.append(_factorization_str(wrong_factors))

    wrongs.append(str(n))

    return build_mc(
        content=f"{n}을 소인수분해하면?",
        answer=ans,
        wrongs=wrongs,
        explanation=f"{n} = {ans}",
        concept_id="concept-m1-prime-02", difficulty=7,
        part="calc",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 최대공약수와 최소공배수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m1-prime-03", difficulty=3)
def m1_gcd_lv3():
    """작은 수의 최대공약수."""
    pairs = [(12, 18), (20, 30), (24, 36), (15, 25), (18, 24), (14, 21)]
    a, b = random.choice(pairs)
    ans = math.gcd(a, b)

    return build_mc(
        content=f"{a}과 {b}의 최대공약수는?",
        answer=ans,
        wrongs=[ans * 2, ans // 2 if ans > 2 else ans + 1, a, b],
        explanation=f"최대공약수(GCD)는 {ans}",
        concept_id="concept-m1-prime-03", difficulty=3,
        part="calc",
    )


@register("concept-m1-prime-03", difficulty=5)
def m1_lcm_lv5():
    """중간 크기의 최소공배수."""
    pairs = [(12, 18), (15, 20), (24, 36), (30, 45), (16, 24)]
    a, b = random.choice(pairs)
    ans = (a * b) // math.gcd(a, b)

    return build_mc(
        content=f"{a}과 {b}의 최소공배수는?",
        answer=ans,
        wrongs=[ans // 2, ans * 2, a * b, math.gcd(a, b)],
        explanation=f"최소공배수(LCM)는 {ans}",
        concept_id="concept-m1-prime-03", difficulty=5,
        part="calc",
    )


@register("concept-m1-prime-03", difficulty=7)
def m1_gcd_lcm_lv7():
    """세 수의 최대공약수."""
    triples = [(12, 18, 24), (20, 30, 40), (15, 25, 35), (16, 24, 32)]
    a, b, c = random.choice(triples)
    ans = math.gcd(math.gcd(a, b), c)

    return build_mc(
        content=f"{a}, {b}, {c}의 최대공약수는?",
        answer=ans,
        wrongs=[ans * 2, ans // 2 if ans > 1 else ans + 1,
                math.gcd(a, b), math.gcd(b, c)],
        explanation=f"세 수의 최대공약수는 {ans}",
        concept_id="concept-m1-prime-03", difficulty=7,
        part="calc",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 절댓값
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m1-int-02", difficulty=3)
def m1_abs_lv3():
    """기본 절댓값 계산."""
    a = random.randint(-15, -1)
    ans = abs(a)

    return build_mc(
        content=f"|{a}| = ?",
        answer=ans,
        wrongs=[a, -ans, ans + 1, ans - 1],
        explanation=f"|{a}| = {ans}",
        concept_id="concept-m1-int-02", difficulty=3,
        part="calc",
    )


@register("concept-m1-int-02", difficulty=5)
def m1_abs_add_lv5():
    """절댓값의 덧셈."""
    a = random.randint(-12, -3)
    b = random.randint(1, 12)
    ans = abs(a) + abs(b)

    return build_mc(
        content=f"|{a}| + |{b}| = ?",
        answer=ans,
        wrongs=[a + b, abs(a + b), ans - 2, ans + 2],
        explanation=f"|{a}| = {abs(a)}, |{b}| = {abs(b)}. {abs(a)} + {abs(b)} = {ans}",
        concept_id="concept-m1-int-02", difficulty=5,
        part="calc",
    )


@register("concept-m1-int-02", difficulty=7)
def m1_abs_expr_lv7():
    """절댓값 혼합 계산."""
    a = random.randint(-10, -2)
    b = random.randint(2, 10)
    ans = abs(a) - abs(b) if abs(a) > abs(b) else abs(b) - abs(a)
    sign = "-" if abs(a) > abs(b) else "+"

    return build_mc(
        content=f"|{a}| - |{b}| = ?",
        answer=abs(a) - abs(b),
        wrongs=[abs(b) - abs(a), a - b, abs(a - b), abs(a) + abs(b)],
        explanation=f"|{a}| = {abs(a)}, |{b}| = {abs(b)}. {abs(a)} - {abs(b)} = {abs(a) - abs(b)}",
        concept_id="concept-m1-int-02", difficulty=7,
        part="calc",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 정수의 사칙연산
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m1-int-03", difficulty=3)
def m1_int_add_lv3():
    """정수 덧셈 기본."""
    a = random.randint(-15, -5)
    b = random.randint(3, 15)
    ans = a + b

    return build_mc(
        content=f"({a}) + {b} = ?",
        answer=ans,
        wrongs=[ans + 2, ans - 2, abs(a) + b, -ans],
        explanation=f"({a}) + {b} = {ans}",
        concept_id="concept-m1-int-03", difficulty=3,
        part="calc",
    )


@register("concept-m1-int-03", difficulty=5)
def m1_int_mixed_lv5():
    """정수 덧셈과 뺄셈 혼합."""
    a = random.randint(-10, -2)
    b = random.randint(5, 12)
    c = random.randint(-8, -2)
    ans = a + b - c

    return build_mc(
        content=f"({a}) + {b} - ({c}) = ?",
        answer=ans,
        wrongs=[ans + 2, ans - 2, a + b + c, a - b - c],
        explanation=f"({a}) + {b} - ({c}) = {a + b} - ({c}) = {ans}",
        concept_id="concept-m1-int-03", difficulty=5,
        part="calc",
    )


@register("concept-m1-int-03", difficulty=7)
def m1_int_mult_lv7():
    """정수의 곱셈과 거듭제곱."""
    a = random.choice([-3, -2, 2, 3])
    exp = random.randint(2, 3)
    b = random.randint(2, 5)
    result = (a ** exp) * b
    ans = result

    sign_str = "+" if a > 0 else ""

    from . import sup
    return build_mc(
        content=f"({sign_str}{a}){sup(exp)} × {b} = ?",
        answer=ans,
        wrongs=[-(a ** exp) * b, (a ** exp) * (-b),
                a * exp * b, ans + a],
        explanation=f"({sign_str}{a}){sup(exp)} = {a ** exp}. {a ** exp} × {b} = {ans}",
        concept_id="concept-m1-int-03", difficulty=7,
        part="calc",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 동류항 정리
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m1-expr-02", difficulty=3)
def m1_like_terms_lv3():
    """기본 동류항 정리."""
    a = random.randint(2, 7)
    b = random.randint(1, 5)
    ans_coef = a + b

    return build_mc(
        content=f"{a}x + {b}x를 간단히 하면?",
        answer=f"{ans_coef}x",
        wrongs=[f"{a * b}x", f"{a}x{b}", f"{ans_coef}", f"{ans_coef - 1}x"],
        explanation=f"{a}x + {b}x = ({a} + {b})x = {ans_coef}x",
        concept_id="concept-m1-expr-02", difficulty=3,
        part="algebra",
    )


@register("concept-m1-expr-02", difficulty=5)
def m1_like_terms_lv5():
    """동류항 정리와 상수항."""
    a = random.randint(2, 6)
    b = random.randint(-5, -1)
    c = random.randint(1, 4)
    d = random.randint(3, 9)
    ans_coef = a + c
    ans_const = b + d
    ans_str = f"{ans_coef}x" + (f"+{ans_const}" if ans_const > 0 else str(ans_const))

    b_str = str(b) if b < 0 else f"+{b}"
    c_str = f"+{c}x" if c > 0 else f"{c}x"
    d_str = f"+{d}" if d > 0 else str(d)

    return build_mc(
        content=f"{a}x{b_str}{c_str}{d_str}를 간단히 하면?",
        answer=ans_str,
        wrongs=[
            f"{a + c + 1}x{ans_const if ans_const < 0 else f'+{ans_const}'}",
            f"{ans_coef}x{ans_const + 1 if ans_const >= 0 else ans_const - 1}",
            f"{a}x{b + d if b + d < 0 else f'+{b + d}'}",
        ],
        explanation=f"동류항끼리 모으면: ({a}x{c_str}) + ({b}{d_str}) = {ans_str}",
        concept_id="concept-m1-expr-02", difficulty=5,
        part="algebra",
    )


@register("concept-m1-expr-02", difficulty=7)
def m1_like_terms_complex_lv7():
    """복잡한 동류항 정리."""
    a = random.randint(3, 7)
    b = random.randint(-6, -2)
    c = random.randint(-4, -1)
    d = random.randint(5, 10)
    ans_coef = a + b
    ans_const = c + d

    ans_str = f"{ans_coef}x" if ans_coef != 1 else "x"
    if ans_const > 0:
        ans_str += f"+{ans_const}"
    elif ans_const < 0:
        ans_str += str(ans_const)

    b_str = str(b) + "x" if b < 0 else f"+{b}x"

    return build_mc(
        content=f"{a}x{c:+d}{b_str}{d:+d}를 간단히 하면?",
        answer=ans_str,
        wrongs=[
            f"{ans_coef + 1}x{ans_const:+d}",
            f"{ans_coef}x{ans_const + 1:+d}",
            f"{a + b + 1}x{c + d:+d}",
        ],
        explanation=f"x 항: {a}x{b_str} = {ans_coef}x, 상수항: {c}{d:+d} = {ans_const}. 답: {ans_str}",
        concept_id="concept-m1-expr-02", difficulty=7,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 식의 값 (대입)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m1-expr-03", difficulty=3)
def m1_substitution_lv3():
    """일차식에 값 대입."""
    a = random.randint(2, 7)
    b = random.randint(1, 10)
    x_val = random.randint(1, 5)
    ans = a * x_val + b

    return build_mc(
        content=f"x = {x_val}일 때, {a}x + {b}의 값은?",
        answer=ans,
        wrongs=[ans + 1, ans - 1, a * x_val, ans + a],
        explanation=f"{a} × {x_val} + {b} = {a * x_val} + {b} = {ans}",
        concept_id="concept-m1-expr-03", difficulty=3,
        part="algebra",
    )


@register("concept-m1-expr-03", difficulty=5)
def m1_substitution_lv5():
    """일차식에 음수 대입."""
    a = random.randint(2, 6)
    b = random.randint(-8, -2)
    x_val = random.randint(-5, -1)
    ans = a * x_val + b

    b_str = str(b) if b < 0 else f"+{b}"

    return build_mc(
        content=f"x = {x_val}일 때, {a}x{b_str}의 값은?",
        answer=ans,
        wrongs=[ans + a, ans - a, -(a * x_val + b), a * (-x_val) + b],
        explanation=f"{a} × ({x_val}) + ({b}) = {a * x_val} + ({b}) = {ans}",
        concept_id="concept-m1-expr-03", difficulty=5,
        part="algebra",
    )


@register("concept-m1-expr-03", difficulty=7)
def m1_substitution_complex_lv7():
    """이차식에 값 대입."""
    a = random.randint(1, 3)
    b = random.randint(-5, -1)
    c = random.randint(2, 8)
    x_val = random.randint(2, 4)
    ans = a * (x_val ** 2) + b * x_val + c

    b_str = str(b) + "x" if b < 0 else f"+{b}x"
    c_str = f"+{c}" if c > 0 else str(c)

    return build_mc(
        content=f"x = {x_val}일 때, {a}x²{b_str}{c_str}의 값은?",
        answer=ans,
        wrongs=[ans + b, ans - a, a * x_val + b * x_val + c, ans + x_val],
        explanation=f"{a}×{x_val}² + {b}×{x_val} + {c} = {a * x_val ** 2} + {b * x_val} + {c} = {ans}",
        concept_id="concept-m1-expr-03", difficulty=7,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 일차방정식 풀이
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m1-eq-02", difficulty=3)
def m1_linear_eq_lv3():
    """기본 일차방정식 (x + a = b 형태)."""
    ans = random.randint(1, 15)
    a = random.randint(3, 12)
    b = ans + a

    return build_mc(
        content=f"x + {a} = {b}의 해는?",
        answer=ans,
        wrongs=[ans + 1, ans - 1, b - a - 1, a + b],
        explanation=f"x = {b} - {a} = {ans}",
        concept_id="concept-m1-eq-02", difficulty=3,
        part="algebra",
    )


@register("concept-m1-eq-02", difficulty=5)
def m1_linear_eq_lv5():
    """일차방정식 (ax + b = c 형태)."""
    ans = random.randint(2, 10)
    a = random.randint(2, 6)
    b = random.randint(1, 8)
    c = a * ans + b

    return build_mc(
        content=f"{a}x + {b} = {c}의 해는?",
        answer=ans,
        wrongs=[ans + 1, ans - 1, (c - b) // a + 1 if (c - b) % a == 0 else ans + 2, c - b],
        explanation=f"{a}x = {c} - {b} = {c - b}. x = {c - b} / {a} = {ans}",
        concept_id="concept-m1-eq-02", difficulty=5,
        part="algebra",
    )


@register("concept-m1-eq-02", difficulty=7)
def m1_linear_eq_complex_lv7():
    """복잡한 일차방정식 (ax + b = cx + d 형태)."""
    ans = random.randint(2, 12)
    a = random.randint(3, 7)
    c = random.randint(1, a - 1)
    b = random.randint(1, 10)
    d = (a - c) * ans + b

    return build_mc(
        content=f"{a}x + {b} = {c}x + {d}의 해는?",
        answer=ans,
        wrongs=[ans + 1, ans - 1, (d - b) // (a - c) + 1 if (a - c) != 0 else ans + 2, d - b],
        explanation=f"{a}x - {c}x = {d} - {b}. {a - c}x = {d - b}. x = {ans}",
        concept_id="concept-m1-eq-02", difficulty=7,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 빈칸 채우기 (Fill-in-blank)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m1-int-03", difficulty=4)
def m1_int_fb_lv4():
    a = random.randint(-8, -2)
    b = random.randint(5, 12)
    c = random.randint(-6, -1)
    ans = a + b - c

    return build_fb(
        content=f"({a}) + {b} - ({c}) = [answer]",
        answer=str(ans),
        explanation=f"({a}) + {b} - ({c}) = {ans}",
        concept_id="concept-m1-int-03", difficulty=4,
        part="calc",
    )


@register("concept-m1-prime-03", difficulty=4)
def m1_gcd_fb_lv4():
    pairs = [(24, 36), (30, 45), (18, 27), (20, 35)]
    a, b = random.choice(pairs)
    ans = math.gcd(a, b)

    return build_fb(
        content=f"{a}과 {b}의 최대공약수는 [answer]",
        answer=str(ans),
        explanation=f"최대공약수는 {ans}",
        concept_id="concept-m1-prime-03", difficulty=4,
        part="calc",
    )


@register("concept-m1-eq-02", difficulty=4)
def m1_linear_eq_fb_lv4():
    ans = random.randint(3, 12)
    a = random.randint(2, 5)
    b = random.randint(2, 9)
    c = a * ans + b

    return build_fb(
        content=f"{a}x + {b} = {c}의 해 x = [answer]",
        answer=str(ans),
        explanation=f"{a}x = {c - b}, x = {ans}",
        concept_id="concept-m1-eq-02", difficulty=4,
        part="algebra",
    )
