"""중등 3학년 연산 문제 템플릿.

개념 목록:
- concept-m3-sqrt-01: 제곱근의 뜻
- concept-m3-sqrt-03: 무리수의 계산
- concept-m3-factor-01: 인수분해 (곱셈 공식)
- concept-m3-factor-02: 인수분해 (일반)
"""
import random
import math

from . import register, build_mc, build_fb


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 제곱근의 뜻
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m3-sqrt-01", difficulty=3)
def m3_sqrt_basic_lv3():
    """기본 제곱근 (완전제곱수)."""
    n = random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100])
    ans = int(math.sqrt(n))

    return build_mc(
        content=f"{n}의 양의 제곱근은?",
        answer=ans,
        wrongs=[
            -ans,
            ans + 1,
            ans - 1 if ans > 1 else ans + 2,
            n,
        ],
        explanation=f"{ans}² = {n}이므로 {n}의 양의 제곱근은 {ans}",
        concept_id="concept-m3-sqrt-01", difficulty=3,
        part="calc",
    )


@register("concept-m3-sqrt-01", difficulty=5)
def m3_sqrt_two_roots_lv5():
    """제곱근의 개수."""
    n = random.choice([9, 16, 25, 36, 49, 64])
    ans = int(math.sqrt(n))

    return build_mc(
        content=f"{n}의 제곱근은? (모두 고르시오)",
        answer=f"±{ans}",
        wrongs=[
            f"{ans}",
            f"-{ans}",
            f"√{n}",
            f"{ans}, {-ans - 1}",
        ],
        explanation=f"{n}의 제곱근은 ±{ans}입니다. (양수 {ans}와 음수 -{ans})",
        concept_id="concept-m3-sqrt-01", difficulty=5,
        part="calc",
    )


@register("concept-m3-sqrt-01", difficulty=7)
def m3_sqrt_negative_lv7():
    """음수의 절댓값과 제곱근."""
    a = random.randint(-9, -2)
    ans = abs(a)

    return build_mc(
        content=f"√({a})² = ?",
        answer=ans,
        wrongs=[
            a,
            -ans,
            ans ** 2,
            f"√{a}",
        ],
        explanation=f"√({a})² = √{a ** 2} = |{a}| = {ans}",
        concept_id="concept-m3-sqrt-01", difficulty=7,
        part="calc",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 무리수의 계산
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _simplify_sqrt(n: int) -> tuple[int, int]:
    """√n을 a√b 형태로 간단히 (a²×b = n)."""
    a = 1
    b = n
    for i in range(int(math.sqrt(n)), 1, -1):
        if n % (i * i) == 0:
            a = i
            b = n // (i * i)
            break
    return a, b


@register("concept-m3-sqrt-03", difficulty=3)
def m3_radical_simplify_lv3():
    """제곱근 간단히 하기."""
    bases = [2, 3, 5]
    base = random.choice(bases)
    k = random.choice([4, 9, 16, 25])
    n = k * base
    coef = int(math.sqrt(k))

    return build_mc(
        content=f"√{n}을 간단히 하면?",
        answer=f"{coef}√{base}",
        wrongs=[
            f"√{n}",
            f"{coef + 1}√{base}",
            f"{coef}√{base + 1}",
            f"{coef * base}",
        ],
        explanation=f"√{n} = √({k}×{base}) = √{k} × √{base} = {coef}√{base}",
        concept_id="concept-m3-sqrt-03", difficulty=3,
        part="calc",
    )


@register("concept-m3-sqrt-03", difficulty=5)
def m3_radical_mult_lv5():
    """제곱근의 곱셈."""
    a_coef = random.randint(2, 5)
    b_coef = random.randint(2, 5)
    base = random.choice([2, 3, 5, 6])
    product = a_coef * b_coef

    return build_mc(
        content=f"√{a_coef ** 2} × √{b_coef ** 2} = ?",
        answer=product,
        wrongs=[
            product + 1,
            product - 1,
            a_coef + b_coef,
            f"√{product}",
        ],
        explanation=f"√{a_coef ** 2} × √{b_coef ** 2} = {a_coef} × {b_coef} = {product}",
        concept_id="concept-m3-sqrt-03", difficulty=5,
        part="calc",
    )


@register("concept-m3-sqrt-03", difficulty=7)
def m3_radical_complex_lv7():
    """복잡한 무리수 곱셈."""
    # √a × √b = √(ab), 완전제곱수가 되도록
    pairs = [(2, 8), (3, 12), (5, 20), (6, 24), (2, 18)]
    a, b = random.choice(pairs)
    product = a * b
    ans = int(math.sqrt(product))

    return build_mc(
        content=f"√{a} × √{b} = ?",
        answer=ans,
        wrongs=[
            f"√{a + b}",
            ans + 1,
            ans - 1 if ans > 1 else ans + 2,
            f"{ans}√2",
        ],
        explanation=f"√{a} × √{b} = √({a}×{b}) = √{product} = {ans}",
        concept_id="concept-m3-sqrt-03", difficulty=7,
        part="calc",
    )


@register("concept-m3-sqrt-03", difficulty=8)
def m3_radical_add_lv8():
    """제곱근의 덧셈 (동류항)."""
    base = random.choice([2, 3, 5])
    a = random.randint(2, 5)
    b = random.randint(1, 4)
    ans_coef = a + b

    return build_mc(
        content=f"{a}√{base} + {b}√{base} = ?",
        answer=f"{ans_coef}√{base}",
        wrongs=[
            f"{a + b}√{2 * base}",
            f"{a * b}√{base}",
            f"{ans_coef + 1}√{base}",
            f"√{ans_coef * base}",
        ],
        explanation=f"{a}√{base} + {b}√{base} = ({a}+{b})√{base} = {ans_coef}√{base}",
        concept_id="concept-m3-sqrt-03", difficulty=8,
        part="calc",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 인수분해 (곱셈 공식)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m3-factor-01", difficulty=3)
def m3_expand_square_lv3():
    """완전제곱식 전개 (x+a)²."""
    a = random.randint(2, 7)
    # (x + a)² = x² + 2ax + a²
    coef = 2 * a
    const = a ** 2

    return build_mc(
        content=f"(x + {a})² = ?",
        answer=f"x²+{coef}x+{const}",
        wrongs=[
            f"x²+{a}x+{const}",
            f"x²+{coef}x+{a}",
            f"x²+{coef + 1}x+{const}",
            f"x²+{2 * a}x+{2 * a}",
        ],
        explanation=f"(x+{a})² = x² + 2×{a}×x + {a}² = x²+{coef}x+{const}",
        concept_id="concept-m3-factor-01", difficulty=3,
        part="algebra",
    )


@register("concept-m3-factor-01", difficulty=5)
def m3_expand_diff_lv5():
    """곱셈 공식 (a+b)(a-b)."""
    a = random.randint(2, 8)
    b = random.randint(2, 6)
    # (x+a)(x-a) = x² - a²
    const = a ** 2

    return build_mc(
        content=f"(x + {a})(x - {a}) = ?",
        answer=f"x²-{const}",
        wrongs=[
            f"x²+{const}",
            f"x²-{2 * a}",
            f"x²",
            f"x²-{a}x-{const}",
        ],
        explanation=f"(x+{a})(x-{a}) = x² - {a}² = x²-{const}",
        concept_id="concept-m3-factor-01", difficulty=5,
        part="algebra",
    )


@register("concept-m3-factor-01", difficulty=7)
def m3_expand_general_lv7():
    """일반 전개 (x+a)(x+b)."""
    a = random.randint(2, 6)
    b = random.randint(2, 6)
    # (x+a)(x+b) = x² + (a+b)x + ab
    coef = a + b
    const = a * b

    return build_mc(
        content=f"(x + {a})(x + {b}) = ?",
        answer=f"x²+{coef}x+{const}",
        wrongs=[
            f"x²+{a * b}x+{a + b}",
            f"x²+{coef + 1}x+{const}",
            f"x²+{coef}x+{const + 1}",
            f"x²+{a}x+{b}x+{const}",
        ],
        explanation=f"(x+{a})(x+{b}) = x² + ({a}+{b})x + {a}×{b} = x²+{coef}x+{const}",
        concept_id="concept-m3-factor-01", difficulty=7,
        part="algebra",
    )


@register("concept-m3-factor-01", difficulty=8)
def m3_expand_negative_lv8():
    """음수 포함 전개 (x+a)(x-b)."""
    a = random.randint(3, 8)
    b = random.randint(2, 6)
    # (x+a)(x-b) = x² + (a-b)x - ab
    coef = a - b
    const = -(a * b)

    coef_str = f"+{coef}" if coef > 0 else str(coef) if coef < 0 else ""
    const_str = str(const)

    return build_mc(
        content=f"(x + {a})(x - {b}) = ?",
        answer=f"x²{coef_str}x{const_str}",
        wrongs=[
            f"x²+{a - b}x+{a * b}",
            f"x²+{a + b}x-{a * b}",
            f"x²{coef + 1}x{const}",
            f"x²+{coef}x+{const}",
        ],
        explanation=f"(x+{a})(x-{b}) = x² + ({a}-{b})x - {a}×{b} = x²{coef_str}x{const_str}",
        concept_id="concept-m3-factor-01", difficulty=8,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 인수분해 (일반)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m3-factor-02", difficulty=3)
def m3_factor_perfect_square_lv3():
    """완전제곱식 인수분해."""
    a = random.randint(2, 6)
    # x² + 2ax + a² = (x + a)²
    coef = 2 * a
    const = a ** 2

    return build_mc(
        content=f"x² + {coef}x + {const}를 인수분해하면?",
        answer=f"(x+{a})²",
        wrongs=[
            f"(x+{a})(x+{a + 1})",
            f"(x+{coef})²",
            f"(x+{a})(x-{a})",
            f"(x²+{a})²",
        ],
        explanation=f"x² + {coef}x + {const} = x² + 2×{a}×x + {a}² = (x+{a})²",
        concept_id="concept-m3-factor-02", difficulty=3,
        part="algebra",
    )


@register("concept-m3-factor-02", difficulty=5)
def m3_factor_difference_lv5():
    """제곱의 차 인수분해."""
    a = random.randint(3, 9)
    # x² - a² = (x+a)(x-a)
    const = a ** 2

    return build_mc(
        content=f"x² - {const}를 인수분해하면?",
        answer=f"(x+{a})(x-{a})",
        wrongs=[
            f"(x-{a})²",
            f"(x+{a})²",
            f"(x-{const})(x+1)",
            f"x(x-{a})",
        ],
        explanation=f"x² - {const} = x² - {a}² = (x+{a})(x-{a})",
        concept_id="concept-m3-factor-02", difficulty=5,
        part="algebra",
    )


@register("concept-m3-factor-02", difficulty=7)
def m3_factor_general_lv7():
    """일반 인수분해 x² + (a+b)x + ab."""
    a = random.randint(2, 6)
    b = random.randint(2, 5)
    # x² + (a+b)x + ab = (x+a)(x+b)
    coef = a + b
    const = a * b

    return build_mc(
        content=f"x² + {coef}x + {const}를 인수분해하면?",
        answer=f"(x+{a})(x+{b})",
        wrongs=[
            f"(x+{coef})(x+1)",
            f"(x+{const})(x+1)",
            f"(x+{a})(x+{b + 1})",
            f"(x+{a})²",
        ],
        explanation=f"x² + {coef}x + {const} = (x+{a})(x+{b}) "
                    f"(∵ {a}+{b}={coef}, {a}×{b}={const})",
        concept_id="concept-m3-factor-02", difficulty=7,
        part="algebra",
    )


@register("concept-m3-factor-02", difficulty=8)
def m3_factor_negative_lv8():
    """음수 상수항 인수분해 x² + (a-b)x - ab."""
    a = random.randint(4, 8)
    b = random.randint(2, a - 1)
    # x² + (a-b)x - ab = (x+a)(x-b)
    coef = a - b
    const = -(a * b)

    coef_str = f"+{coef}" if coef > 0 else str(coef) if coef != 0 else ""

    return build_mc(
        content=f"x²{coef_str}x{const}를 인수분해하면?",
        answer=f"(x+{a})(x-{b})",
        wrongs=[
            f"(x-{a})(x+{b})",
            f"(x+{a})(x+{b})",
            f"(x+{a})(x-{b + 1})",
            f"(x-{coef})(x-{const})",
        ],
        explanation=f"x²{coef_str}x{const} = (x+{a})(x-{b}) "
                    f"(∵ {a}-{b}={coef}, {a}×(-{b})={const})",
        concept_id="concept-m3-factor-02", difficulty=8,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 빈칸 채우기 (Fill-in-blank)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-m3-sqrt-01", difficulty=4)
def m3_sqrt_fb_lv4():
    n = random.choice([16, 25, 36, 49, 64, 81, 100])
    ans = int(math.sqrt(n))

    return build_fb(
        content=f"{n}의 양의 제곱근은 [answer]",
        answer=str(ans),
        explanation=f"{ans}² = {n}",
        concept_id="concept-m3-sqrt-01", difficulty=4,
        part="calc",
    )


@register("concept-m3-sqrt-03", difficulty=5)
def m3_radical_fb_lv5():
    bases = [2, 3, 5]
    base = random.choice(bases)
    k = random.choice([4, 9, 16])
    n = k * base
    coef = int(math.sqrt(k))

    return build_fb(
        content=f"√{n} = [answer]√{base}",
        answer=str(coef),
        explanation=f"√{n} = √({k}×{base}) = {coef}√{base}",
        concept_id="concept-m3-sqrt-03", difficulty=5,
        part="calc",
    )


@register("concept-m3-factor-02", difficulty=6)
def m3_factor_fb_lv6():
    a = random.randint(2, 6)
    coef = 2 * a
    const = a ** 2

    return build_fb(
        content=f"x² + {coef}x + {const} = (x+[answer])²",
        answer=str(a),
        explanation=f"완전제곱식: (x+{a})²",
        concept_id="concept-m3-factor-02", difficulty=6,
        part="algebra",
    )
