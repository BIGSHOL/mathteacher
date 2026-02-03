"""시드 데이터 헬퍼 - 반복 코드를 줄이기 위한 팩토리 함수."""


def mc(
    id: str,
    concept_id: str,
    category: str,
    part: str,
    difficulty: int,
    content: str,
    options: list[tuple[str, str]],
    correct: str,
    explanation: str,
    points: int = 10,
) -> dict:
    """객관식 문제 dict 생성."""
    labels = ["A", "B", "C", "D"]
    return {
        "id": id,
        "concept_id": concept_id,
        "category": category,
        "part": part,
        "question_type": "multiple_choice",
        "difficulty": difficulty,
        "content": content,
        "options": [
            {"id": str(i + 1), "label": labels[i], "text": t}
            for i, t in enumerate(options)
        ],
        "correct_answer": correct,
        "explanation": explanation,
        "points": points,
    }


def fb(
    id: str,
    concept_id: str,
    category: str,
    part: str,
    difficulty: int,
    content: str,
    answer: str,
    explanation: str,
    points: int = 10,
    accept_formats: list[str] | None = None,
) -> dict:
    """빈칸 채우기 문제 dict 생성."""
    return {
        "id": id,
        "concept_id": concept_id,
        "category": category,
        "part": part,
        "question_type": "fill_in_blank",
        "difficulty": difficulty,
        "content": content,
        "options": None,
        "correct_answer": answer,
        "explanation": explanation,
        "points": points,
        "blank_config": {
            "blank_count": 1,
            "accept_formats": accept_formats or [answer],
        },
    }


def concept(id: str, name: str, grade: str, category: str, part: str, description: str) -> dict:
    """개념 dict 생성."""
    return {
        "id": id,
        "name": name,
        "grade": grade,
        "category": category,
        "part": part,
        "description": description,
    }


def test(
    id: str,
    title: str,
    description: str,
    grade: str,
    concept_ids: list[str],
    question_ids: list[str],
    time_limit_minutes: int | None = None,
    is_adaptive: bool = False,
    use_question_pool: bool = False,
    questions_per_attempt: int | None = None,
    shuffle_options: bool = True,
) -> dict:
    """테스트 dict 생성."""
    return {
        "id": id,
        "title": title,
        "description": description,
        "grade": grade,
        "concept_ids": concept_ids,
        "question_ids": question_ids,
        "question_count": len(question_ids),
        "time_limit_minutes": time_limit_minutes,
        "is_active": True,
        "is_adaptive": is_adaptive,
        "use_question_pool": use_question_pool,
        "questions_per_attempt": questions_per_attempt,
        "shuffle_options": shuffle_options,
    }
