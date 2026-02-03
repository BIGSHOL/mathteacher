"""빈칸 채우기 샘플 데이터."""

from app.schemas.common import QuestionType, QuestionCategory, ProblemPart, Grade

# 빈칸 채우기 샘플 문제
FILL_IN_BLANK_SAMPLES = [
    {
        "content": "세 변의 길이가 같은 삼각형은 정삼각형이다.",
        "question_type": QuestionType.FILL_IN_BLANK,
        "category": QuestionCategory.CONCEPT,
        "part": ProblemPart.GEO,
        "difficulty": 3,
        "grade": Grade.MIDDLE_1,
        "blank_config": {
            "blank_positions": [
                {"index": 0, "word": "세", "importance": 3},
                {"index": 1, "word": "변의", "importance": 3},
                {"index": 2, "word": "길이가", "importance": 2},
                {"index": 3, "word": "같은", "importance": 2},
                {"index": 4, "word": "삼각형은", "importance": 1},
                {"index": 5, "word": "정삼각형이다", "importance": 3},
            ],
            "round_rules": [
                {"round": 1, "blank_count": 0},
                {"round": 2, "blank_count_range": [2, 3], "min_importance": 3},
                {"round": 3, "blank_count_range": [4, 6], "min_importance": 1}
            ]
        },
        "correct_answer": "{}",  # 빈칸 타입은 동적 생성
        "explanation": "정삼각형은 세 변의 길이가 모두 같은 삼각형입니다.",
        "points": 10
    },
    {
        "content": "평행사변형에서 마주 보는 두 변의 길이는 같다.",
        "question_type": QuestionType.FILL_IN_BLANK,
        "category": QuestionCategory.CONCEPT,
        "part": ProblemPart.GEO,
        "difficulty": 4,
        "grade": Grade.MIDDLE_1,
        "blank_config": {
            "blank_positions": [
                {"index": 0, "word": "평행사변형에서", "importance": 3},
                {"index": 1, "word": "마주", "importance": 2},
                {"index": 2, "word": "보는", "importance": 1},
                {"index": 3, "word": "두", "importance": 2},
                {"index": 4, "word": "변의", "importance": 2},
                {"index": 5, "word": "길이는", "importance": 3},
                {"index": 6, "word": "같다", "importance": 3},
            ],
            "round_rules": [
                {"round": 1, "blank_count": 0},
                {"round": 2, "blank_count_range": [2, 3], "min_importance": 3},
                {"round": 3, "blank_count_range": [5, 7], "min_importance": 1}
            ]
        },
        "correct_answer": "{}",
        "explanation": "평행사변형의 성질: 대변의 길이가 같고 대각의 크기가 같습니다.",
        "points": 10
    },
    {
        "content": "일차방정식은 미지수의 차수가 1인 방정식이다.",
        "question_type": QuestionType.FILL_IN_BLANK,
        "category": QuestionCategory.CONCEPT,
        "part": ProblemPart.ALGEBRA,
        "difficulty": 3,
        "grade": Grade.MIDDLE_1,
        "blank_config": {
            "blank_positions": [
                {"index": 0, "word": "일차방정식은", "importance": 3},
                {"index": 1, "word": "미지수의", "importance": 2},
                {"index": 2, "word": "차수가", "importance": 3},
                {"index": 3, "word": "1인", "importance": 3},
                {"index": 4, "word": "방정식이다", "importance": 2},
            ],
            "round_rules": [
                {"round": 1, "blank_count": 0},
                {"round": 2, "blank_count_range": [2, 3], "min_importance": 3},
                {"round": 3, "blank_count_range": [4, 5], "min_importance": 1}
            ]
        },
        "correct_answer": "{}",
        "explanation": "일차방정식은 미지수의 최고차항의 차수가 1인 방정식입니다.",
        "points": 10
    },
    {
        "content": "등식의 양변에 같은 수를 더하거나 빼도 등식은 성립한다.",
        "question_type": QuestionType.FILL_IN_BLANK,
        "category": QuestionCategory.CONCEPT,
        "part": ProblemPart.ALGEBRA,
        "difficulty": 2,
        "grade": Grade.MIDDLE_1,
        "blank_config": {
            "blank_positions": [
                {"index": 0, "word": "등식의", "importance": 3},
                {"index": 1, "word": "양변에", "importance": 3},
                {"index": 2, "word": "같은", "importance": 2},
                {"index": 3, "word": "수를", "importance": 2},
                {"index": 4, "word": "더하거나", "importance": 2},
                {"index": 5, "word": "빼도", "importance": 2},
                {"index": 6, "word": "등식은", "importance": 1},
                {"index": 7, "word": "성립한다", "importance": 3},
            ],
            "round_rules": [
                {"round": 1, "blank_count": 0},
                {"round": 2, "blank_count_range": [2, 3], "min_importance": 3},
                {"round": 3, "blank_count_range": [5, 8], "min_importance": 1}
            ]
        },
        "correct_answer": "{}",
        "explanation": "등식의 성질: 양변에 같은 수를 더하거나 빼도, 곱하거나 나누어도 등식이 성립합니다.",
        "points": 10
    },
    {
        "content": "정비례 관계에서 x의 값이 a배가 되면 y의 값도 a배가 된다.",
        "question_type": QuestionType.FILL_IN_BLANK,
        "category": QuestionCategory.CONCEPT,
        "part": ProblemPart.FUNC,
        "difficulty": 4,
        "grade": Grade.MIDDLE_1,
        "blank_config": {
            "blank_positions": [
                {"index": 0, "word": "정비례", "importance": 3},
                {"index": 1, "word": "관계에서", "importance": 2},
                {"index": 2, "word": "x의", "importance": 2},
                {"index": 3, "word": "값이", "importance": 1},
                {"index": 4, "word": "a배가", "importance": 3},
                {"index": 5, "word": "되면", "importance": 1},
                {"index": 6, "word": "y의", "importance": 2},
                {"index": 7, "word": "값도", "importance": 1},
                {"index": 8, "word": "a배가", "importance": 3},
                {"index": 9, "word": "된다", "importance": 2},
            ],
            "round_rules": [
                {"round": 1, "blank_count": 0},
                {"round": 2, "blank_count_range": [3, 4], "min_importance": 3},
                {"round": 3, "blank_count_range": [6, 10], "min_importance": 1}
            ]
        },
        "correct_answer": "{}",
        "explanation": "정비례 관계의 성질: y = ax 형태이며, x가 a배 되면 y도 a배가 됩니다.",
        "points": 10
    },
]


def create_fill_in_blank_questions(db, concept_id: str):
    """빈칸 채우기 샘플 문제 생성."""
    from app.models.question import Question

    questions = []
    for sample in FILL_IN_BLANK_SAMPLES:
        question = Question(
            concept_id=concept_id,
            category=sample["category"],
            part=sample["part"],
            question_type=sample["question_type"],
            difficulty=sample["difficulty"],
            content=sample["content"],
            options=None,  # 빈칸 채우기는 선택지 없음
            correct_answer=sample["correct_answer"],
            explanation=sample["explanation"],
            points=sample["points"],
            blank_config=sample["blank_config"],
            is_active=True
        )
        db.add(question)
        questions.append(question)

    db.commit()
    return questions
