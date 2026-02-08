"""Template-based computation question generator registry.

Templates are Python functions decorated with @register that generate
random question variants. Each call produces different numbers but
the same question structure.
"""
import hashlib
import random
from typing import Callable

# Unicode superscript mapping for math expressions
_SUP_MAP = str.maketrans("0123456789+-()abcdefghijklmnopqrstuvwxyz",
                         "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁽⁾ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ\u02E0ʳˢᵗᵘᵛʷˣʸᶻ")


def sup(n) -> str:
    """Convert a number or simple expression to Unicode superscript."""
    return str(n).translate(_SUP_MAP)

# concept_id -> [(difficulty, generator_function), ...]
TEMPLATE_REGISTRY: dict[str, list[tuple[int, Callable]]] = {}


def register(concept_id: str, difficulty: int):
    """Register a template generator function for a concept + difficulty."""
    def decorator(fn: Callable):
        TEMPLATE_REGISTRY.setdefault(concept_id, []).append((difficulty, fn))
        return fn
    return decorator


def build_mc(
    content: str,
    answer,
    wrongs: list,
    explanation: str,
    concept_id: str,
    difficulty: int,
    part: str = "calc",
) -> dict:
    """Build a multiple-choice question dict with auto-shuffled options.

    answer: correct answer value (int, float, or str)
    wrongs: list of 3+ wrong answer values
    """
    answer_str = str(answer)

    # Ensure we have exactly 3 unique wrong answers (different from correct)
    wrong_strs = []
    for w in wrongs:
        ws = str(w)
        if ws != answer_str and ws not in wrong_strs:
            wrong_strs.append(ws)
        if len(wrong_strs) == 3:
            break

    # Fallback: if not enough wrongs, generate offset values
    offset = 1
    while len(wrong_strs) < 3:
        try:
            fallback = int(answer) + offset
        except (ValueError, TypeError):
            fallback = f"{answer}_{offset}"
        offset += 1
        fs = str(fallback)
        if fs != answer_str and fs not in wrong_strs:
            wrong_strs.append(fs)

    all_options = [answer_str] + wrong_strs
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    correct_label = labels[all_options.index(answer_str)]

    # Generate deterministic ID from content
    content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
    # Short concept code: concept-e3-add-sub-01 -> e3-add01
    parts = concept_id.replace("concept-", "").split("-")
    if len(parts) >= 3:
        short = f"{parts[0]}-{''.join(parts[1:-1])}{parts[-1]}"
    else:
        short = "-".join(parts)
    question_id = f"tpl-{short}-{content_hash}"

    return {
        "id": question_id,
        "concept_id": concept_id,
        "category": "computation",
        "part": part,
        "question_type": "multiple_choice",
        "difficulty": difficulty,
        "content": content,
        "options": [
            {"id": str(i + 1), "label": labels[i], "text": opt}
            for i, opt in enumerate(all_options)
        ],
        "correct_answer": correct_label,
        "explanation": explanation,
        "points": 10,
        "is_active": True,
    }


def build_fb(
    content: str,
    answer: str,
    explanation: str,
    concept_id: str,
    difficulty: int,
    part: str = "calc",
    accept_formats: list[str] | None = None,
) -> dict:
    """Build a fill-in-blank question dict."""
    content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
    parts = concept_id.replace("concept-", "").split("-")
    if len(parts) >= 3:
        short = f"{parts[0]}-{''.join(parts[1:-1])}{parts[-1]}"
    else:
        short = "-".join(parts)
    question_id = f"tpl-{short}-{content_hash}"

    return {
        "id": question_id,
        "concept_id": concept_id,
        "category": "computation",
        "part": part,
        "question_type": "fill_in_blank",
        "difficulty": difficulty,
        "content": content,
        "options": None,
        "correct_answer": answer,
        "explanation": explanation,
        "points": 10,
        "is_active": True,
        "blank_config": {
            "blank_count": 1,
            "accept_formats": accept_formats or [answer],
        },
    }


# Import all grade template modules to trigger @register decorators
def _load_all_templates():
    from . import elementary_3  # noqa: F401
    from . import elementary_4  # noqa: F401
    from . import elementary_5  # noqa: F401
    from . import elementary_6  # noqa: F401
    from . import middle_1  # noqa: F401
    from . import middle_2  # noqa: F401
    from . import middle_3  # noqa: F401
    from . import high_1  # noqa: F401
    from . import high_2  # noqa: F401


_load_all_templates()
