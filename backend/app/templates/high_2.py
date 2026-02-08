"""고등 2학년 연산 문제 템플릿.

개념 목록:
- concept-h2-plane-coord: 좌표평면 (두 점 사이 거리, 중점)
- concept-h2-line: 직선의 방정식 (기울기, 절편, 평행/수직)
- concept-h2-circle: 원의 방정식 (중심, 반지름)
"""
import random
import math

from . import register, build_mc, build_fb


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 좌표평면 - 거리와 중점
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-h2-plane-coord", difficulty=3)
def h2_distance_lv3():
    """두 점 사이의 거리 (피타고라스 정수쌍 사용)."""
    # Use Pythagorean triples for clean answers: (3,4,5), (5,12,13), (8,15,17)
    triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10)]
    dx, dy, dist = random.choice(triples)

    # Random starting point
    x1 = random.randint(-5, 5)
    y1 = random.randint(-5, 5)

    # Apply dx, dy with random signs
    dx = dx * random.choice([-1, 1])
    dy = dy * random.choice([-1, 1])

    x2 = x1 + dx
    y2 = y1 + dy

    answer = dist

    # Distractors
    wrong1 = abs(dx) + abs(dy)  # Manhattan distance
    wrong2 = dist + 1
    wrong3 = int(math.sqrt(dx**2 + dy**2 + 1))  # calculation error

    return build_mc(
        content=f"두 점 A({x1}, {y1}), B({x2}, {y2}) 사이의 거리는?",
        answer=answer,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"거리 = √[(x₂-x₁)² + (y₂-y₁)²] = √[({x2}-{x1})² + ({y2}-{y1})²] = √[{dx**2} + {dy**2}] = √{dx**2 + dy**2} = {answer}",
        concept_id="concept-h2-plane-coord",
        difficulty=3,
        part="algebra",
    )


@register("concept-h2-plane-coord", difficulty=5)
def h2_midpoint_lv5():
    """두 점의 중점 좌표."""
    x1 = random.randint(-8, 8)
    y1 = random.randint(-8, 8)
    x2 = random.randint(-8, 8)
    y2 = random.randint(-8, 8)

    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    # Format as integer or decimal
    if mid_x == int(mid_x) and mid_y == int(mid_y):
        answer_str = f"({int(mid_x)}, {int(mid_y)})"
    else:
        answer_str = f"({mid_x}, {mid_y})"

    # Distractors
    wrong1 = f"({(x1+x2)}, {(y1+y2)})"  # forgot to divide by 2
    wrong2 = f"({int((x1+x2)/2) + 1}, {int((y1+y2)/2)})"
    wrong3 = f"({(x2-x1)/2}, {(y2-y1)/2})"  # used difference instead

    return build_mc(
        content=f"두 점 A({x1}, {y1}), B({x2}, {y2})의 중점 좌표는?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"중점 = ((x₁+x₂)/2, (y₁+y₂)/2) = (({x1}+{x2})/2, ({y1}+{y2})/2) = {answer_str}",
        concept_id="concept-h2-plane-coord",
        difficulty=5,
        part="algebra",
    )


@register("concept-h2-plane-coord", difficulty=7)
def h2_distance_formula_lv7():
    """원점으로부터의 거리."""
    # Pick point such that distance is simple
    x = random.randint(-10, 10)
    y = random.randint(-10, 10)
    while x == 0 and y == 0:
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)

    dist_sq = x*x + y*y
    # Check if perfect square
    dist = math.sqrt(dist_sq)

    if dist == int(dist):
        answer_str = str(int(dist))
    else:
        answer_str = f"√{dist_sq}"

    # Distractors
    wrong1 = str(abs(x) + abs(y))
    wrong2 = f"√{dist_sq + 1}"
    wrong3 = str(int(dist) + 1) if dist == int(dist) else f"√{dist_sq - 1}"

    return build_mc(
        content=f"점 P({x}, {y})와 원점 사이의 거리는?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"거리 = √(x² + y²) = √({x}² + {y}²) = √{dist_sq}" + (f" = {int(dist)}" if dist == int(dist) else ""),
        concept_id="concept-h2-plane-coord",
        difficulty=7,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 직선의 방정식
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-h2-line", difficulty=3)
def h2_line_slope_lv3():
    """기울기와 한 점이 주어졌을 때 직선의 방정식."""
    m = random.randint(-5, 5)
    while m == 0:
        m = random.randint(-5, 5)

    x0 = random.randint(-5, 5)
    y0 = random.randint(-5, 5)

    # y - y0 = m(x - x0) → y = mx - mx0 + y0
    b = y0 - m * x0

    # Format: y = mx + b
    def fmt_line(slope, intercept):
        if slope == 1:
            slope_str = "x"
        elif slope == -1:
            slope_str = "-x"
        else:
            slope_str = f"{slope}x"

        if intercept > 0:
            return f"y={slope_str}+{intercept}"
        elif intercept < 0:
            return f"y={slope_str}{intercept}"
        else:
            return f"y={slope_str}"

    answer_str = fmt_line(m, b)

    # Distractors
    wrong1 = fmt_line(m, b + 1)
    wrong2 = fmt_line(m + 1, b)
    wrong3 = fmt_line(-m, b)  # sign error

    return build_mc(
        content=f"기울기가 {m}이고 점 ({x0}, {y0})을 지나는 직선의 방정식은?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"y - {y0} = {m}(x - {x0}) → y = {m}x - {m*x0} + {y0} → {answer_str}",
        concept_id="concept-h2-line",
        difficulty=3,
        part="algebra",
    )


@register("concept-h2-line", difficulty=5)
def h2_line_two_points_lv5():
    """두 점을 지나는 직선의 기울기."""
    x1 = random.randint(-5, 5)
    y1 = random.randint(-5, 5)
    x2 = random.randint(-5, 5)
    y2 = random.randint(-5, 5)

    # Ensure different x-coordinates
    while x1 == x2:
        x2 = random.randint(-5, 5)

    # m = (y2 - y1) / (x2 - x1)
    dy = y2 - y1
    dx = x2 - x1

    # Simplify fraction if possible
    from math import gcd
    g = gcd(abs(dy), abs(dx))
    dy //= g
    dx //= g

    if dx == 1:
        answer_str = str(dy)
    elif dx == -1:
        answer_str = str(-dy)
    else:
        answer_str = f"{dy}/{dx}"

    # Distractors
    wrong1 = f"{dx}/{dy}" if dy != 0 else "0"  # reciprocal
    wrong2 = str(dy + dx)  # sum instead of quotient
    wrong3 = f"{dy}/{dx+1}"

    return build_mc(
        content=f"두 점 A({x1}, {y1}), B({x2}, {y2})를 지나는 직선의 기울기는?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"기울기 = (y₂-y₁)/(x₂-x₁) = ({y2}-{y1})/({x2}-{x1}) = {dy}/{dx}" + (f" = {dy//dx}" if dx != 0 and dy % dx == 0 else ""),
        concept_id="concept-h2-line",
        difficulty=5,
        part="algebra",
    )


@register("concept-h2-line", difficulty=7)
def h2_line_parallel_lv7():
    """평행한 두 직선 (기울기 같음)."""
    m = random.randint(-5, 5)
    while m == 0:
        m = random.randint(-5, 5)

    b1 = random.randint(-8, 8)
    b2 = random.randint(-8, 8)
    while b1 == b2:
        b2 = random.randint(-8, 8)

    def fmt_line(slope, intercept):
        if slope == 1:
            slope_str = "x"
        elif slope == -1:
            slope_str = "-x"
        else:
            slope_str = f"{slope}x"

        if intercept > 0:
            return f"y={slope_str}+{intercept}"
        elif intercept < 0:
            return f"y={slope_str}{intercept}"
        else:
            return f"y={slope_str}"

    line1 = fmt_line(m, b1)

    # Ask for parallel line through a specific point
    x0 = random.randint(-5, 5)
    y0 = m * x0 + b2  # This ensures the new line passes through (x0, y0) with slope m

    answer_str = fmt_line(m, b2)

    # Distractors
    wrong1 = fmt_line(-m, b2)  # wrong slope
    wrong2 = fmt_line(m, b1)  # same line
    wrong3 = fmt_line(m, b2 + 1)

    return build_mc(
        content=f"직선 {line1}에 평행하고 점 ({x0}, {y0})을 지나는 직선의 방정식은?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"평행한 직선은 기울기가 같으므로 m={m}. y-{y0}={m}(x-{x0}) → {answer_str}",
        concept_id="concept-h2-line",
        difficulty=7,
        part="algebra",
    )


@register("concept-h2-line", difficulty=8)
def h2_line_perpendicular_lv8():
    """수직인 두 직선 (기울기의 곱이 -1)."""
    # Pick m1 such that m2 = -1/m1 is also simple
    m1_num = random.randint(-4, 4)
    while m1_num == 0:
        m1_num = random.randint(-4, 4)

    m1_den = random.randint(1, 3)

    # m2 = -m1_den / m1_num
    m2_num = -m1_den
    m2_den = m1_num

    from math import gcd
    g = gcd(abs(m2_num), abs(m2_den))
    m2_num //= g
    m2_den //= g

    # For simplicity, format as decimal if it's simple
    if m1_den == 1:
        m1_str = str(m1_num)
    else:
        m1_str = f"{m1_num}/{m1_den}"

    if m2_den == 1:
        m2_answer = str(m2_num)
    elif m2_den == -1:
        m2_answer = str(-m2_num)
    else:
        if m2_den < 0:
            m2_num = -m2_num
            m2_den = -m2_den
        m2_answer = f"{m2_num}/{m2_den}"

    # Distractors
    wrong1 = m1_str  # same slope
    wrong2 = str(-int(m2_num/m2_den)) if m2_den != 0 else "1"  # sign error
    wrong3 = f"{m2_den}/{m2_num}" if m2_num != 0 else "0"  # reciprocal without sign

    return build_mc(
        content=f"기울기가 {m1_str}인 직선에 수직인 직선의 기울기는?",
        answer=m2_answer,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"수직인 직선의 기울기의 곱은 -1. m₁×m₂=-1이므로 m₂=-1/m₁ = -1/({m1_str}) = {m2_answer}",
        concept_id="concept-h2-line",
        difficulty=8,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 원의 방정식
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-h2-circle", difficulty=3)
def h2_circle_standard_lv3():
    """중심과 반지름이 주어졌을 때 원의 방정식."""
    h = random.randint(-5, 5)
    k = random.randint(-5, 5)
    r = random.randint(1, 8)

    # (x-h)² + (y-k)² = r²
    def fmt_circle(cx, cy, radius):
        parts = []

        if cx == 0:
            parts.append("x²")
        elif cx > 0:
            parts.append(f"(x-{cx})²")
        else:
            parts.append(f"(x+{-cx})²")

        parts.append("+")

        if cy == 0:
            parts.append("y²")
        elif cy > 0:
            parts.append(f"(y-{cy})²")
        else:
            parts.append(f"(y+{-cy})²")

        parts.append(f"={radius**2}")

        return "".join(parts)

    answer_str = fmt_circle(h, k, r)

    # Distractors
    wrong1 = fmt_circle(-h, k, r)  # sign error on h
    wrong2 = fmt_circle(h, k, r + 1)  # wrong radius
    wrong3 = fmt_circle(h, k, r).replace(f"={r**2}", f"={r}")  # forgot to square r

    return build_mc(
        content=f"중심이 ({h}, {k})이고 반지름이 {r}인 원의 방정식은?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"원의 방정식: (x-a)² + (y-b)² = r². 중심({h},{k}), 반지름{r}이므로 {answer_str}",
        concept_id="concept-h2-circle",
        difficulty=3,
        part="algebra",
    )


@register("concept-h2-circle", difficulty=5)
def h2_circle_center_lv5():
    """원의 방정식에서 중심 좌표 구하기."""
    h = random.randint(-8, 8)
    k = random.randint(-8, 8)
    r = random.randint(1, 10)

    def fmt_circle(cx, cy, radius):
        parts = []

        if cx == 0:
            parts.append("x²")
        elif cx > 0:
            parts.append(f"(x-{cx})²")
        else:
            parts.append(f"(x+{-cx})²")

        parts.append("+")

        if cy == 0:
            parts.append("y²")
        elif cy > 0:
            parts.append(f"(y-{cy})²")
        else:
            parts.append(f"(y+{-cy})²")

        parts.append(f"={radius**2}")

        return "".join(parts)

    circle_eq = fmt_circle(h, k, r)

    answer_str = f"({h}, {k})"

    # Distractors
    wrong1 = f"({-h}, {-k})"  # sign error
    wrong2 = f"({k}, {h})"  # swapped coordinates
    wrong3 = f"({h+1}, {k})"

    return build_mc(
        content=f"원 {circle_eq}의 중심 좌표는?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"(x-a)² + (y-b)² = r² 꼴에서 중심은 (a,b). 따라서 중심은 {answer_str}",
        concept_id="concept-h2-circle",
        difficulty=5,
        part="algebra",
    )


@register("concept-h2-circle", difficulty=7)
def h2_circle_radius_lv7():
    """원의 방정식에서 반지름 구하기."""
    h = random.randint(-5, 5)
    k = random.randint(-5, 5)
    r = random.randint(2, 10)

    def fmt_circle(cx, cy, radius):
        parts = []

        if cx == 0:
            parts.append("x²")
        elif cx > 0:
            parts.append(f"(x-{cx})²")
        else:
            parts.append(f"(x+{-cx})²")

        parts.append("+")

        if cy == 0:
            parts.append("y²")
        elif cy > 0:
            parts.append(f"(y-{cy})²")
        else:
            parts.append(f"(y+{-cy})²")

        parts.append(f"={radius**2}")

        return "".join(parts)

    circle_eq = fmt_circle(h, k, r)

    answer = r

    # Distractors
    wrong1 = r**2  # forgot to take square root
    wrong2 = r + 1
    wrong3 = r - 1

    return build_mc(
        content=f"원 {circle_eq}의 반지름은?",
        answer=answer,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"(x-a)² + (y-b)² = r² 꼴에서 반지름은 r. r² = {r**2}이므로 r = {r}",
        concept_id="concept-h2-circle",
        difficulty=7,
        part="algebra",
    )


@register("concept-h2-circle", difficulty=8)
def h2_circle_expand_lv8():
    """원의 방정식 전개형 → 표준형."""
    # Start with (x-h)² + (y-k)² = r²
    # Expand to x² + y² + Dx + Ey + F = 0
    # where D = -2h, E = -2k, F = h² + k² - r²

    h = random.randint(-4, 4)
    k = random.randint(-4, 4)
    r = random.randint(2, 6)

    D = -2 * h
    E = -2 * k
    F = h * h + k * k - r * r

    # Format expanded form: x² + y² + Dx + Ey + F = 0
    def fmt_expanded(d, e, f):
        parts = ["x²+y²"]

        if d > 0:
            parts.append(f"+{d}x")
        elif d < 0:
            parts.append(f"{d}x")

        if e > 0:
            parts.append(f"+{e}y")
        elif e < 0:
            parts.append(f"{e}y")

        if f > 0:
            parts.append(f"+{f}")
        elif f < 0:
            parts.append(f"{f}")

        parts.append("=0")

        return "".join(parts)

    expanded_eq = fmt_expanded(D, E, F)

    answer_str = f"({h}, {k})"

    # Distractors
    wrong1 = f"({-D//2}, {-E//2})" if D % 2 == 0 and E % 2 == 0 else f"({h+1}, {k})"  # correct formula but might be same
    wrong2 = f"({D}, {E})"  # forgot to divide by 2
    wrong3 = f"({-h}, {-k})"  # sign error

    # Make sure wrong1 is different from answer
    if wrong1 == answer_str:
        wrong1 = f"({h+1}, {k+1})"

    return build_mc(
        content=f"원 {expanded_eq}의 중심 좌표는?",
        answer=answer_str,
        wrongs=[wrong1, wrong2, wrong3],
        explanation=f"x²+y²+Dx+Ey+F=0을 표준형으로 변환: (x+D/2)²+(y+E/2)²=(D²+E²-4F)/4. "
                    f"중심 (-D/2, -E/2) = ({-D//2}, {-E//2}) = {answer_str}",
        concept_id="concept-h2-circle",
        difficulty=8,
        part="algebra",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Fill-in-blank variants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@register("concept-h2-plane-coord", difficulty=4)
def h2_distance_fb_lv4():
    """두 점 사이 거리 fill-in-blank."""
    triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10)]
    dx, dy, dist = random.choice(triples)

    x1 = random.randint(-5, 5)
    y1 = random.randint(-5, 5)

    dx = dx * random.choice([-1, 1])
    dy = dy * random.choice([-1, 1])

    x2 = x1 + dx
    y2 = y1 + dy

    return build_fb(
        content=f"두 점 A({x1}, {y1}), B({x2}, {y2}) 사이의 거리는 [answer]입니다.",
        answer=str(dist),
        explanation=f"거리 = √[({x2}-{x1})² + ({y2}-{y1})²] = √[{dx**2} + {dy**2}] = {dist}",
        concept_id="concept-h2-plane-coord",
        difficulty=4,
        part="algebra",
    )


@register("concept-h2-line", difficulty=4)
def h2_slope_fb_lv4():
    """두 점을 지나는 직선의 기울기 fill-in-blank."""
    x1 = random.randint(-5, 5)
    y1 = random.randint(-5, 5)
    x2 = random.randint(-5, 5)
    y2 = random.randint(-5, 5)

    while x1 == x2:
        x2 = random.randint(-5, 5)

    dy = y2 - y1
    dx = x2 - x1

    from math import gcd
    g = gcd(abs(dy), abs(dx))
    dy //= g
    dx //= g

    if dx == 1:
        answer_str = str(dy)
    elif dx == -1:
        answer_str = str(-dy)
    else:
        if dx < 0:
            dy = -dy
            dx = -dx
        answer_str = f"{dy}/{dx}"

    return build_fb(
        content=f"두 점 ({x1}, {y1}), ({x2}, {y2})를 지나는 직선의 기울기는 [answer]입니다.",
        answer=answer_str,
        explanation=f"기울기 = ({y2}-{y1})/({x2}-{x1}) = {answer_str}",
        concept_id="concept-h2-line",
        difficulty=4,
        part="algebra",
    )


@register("concept-h2-circle", difficulty=4)
def h2_circle_fb_lv4():
    """원의 반지름 구하기 fill-in-blank."""
    h = random.randint(-5, 5)
    k = random.randint(-5, 5)
    r = random.randint(2, 8)

    def fmt_circle(cx, cy, radius):
        parts = []

        if cx == 0:
            parts.append("x²")
        elif cx > 0:
            parts.append(f"(x-{cx})²")
        else:
            parts.append(f"(x+{-cx})²")

        parts.append("+")

        if cy == 0:
            parts.append("y²")
        elif cy > 0:
            parts.append(f"(y-{cy})²")
        else:
            parts.append(f"(y+{-cy})²")

        parts.append(f"={radius**2}")

        return "".join(parts)

    circle_eq = fmt_circle(h, k, r)

    return build_fb(
        content=f"원 {circle_eq}의 반지름은 [answer]입니다.",
        answer=str(r),
        explanation=f"원의 방정식에서 r² = {r**2}이므로 r = {r}",
        concept_id="concept-h2-circle",
        difficulty=4,
        part="algebra",
    )
