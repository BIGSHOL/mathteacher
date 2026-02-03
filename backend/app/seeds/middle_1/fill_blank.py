"""중1 빈칸 채우기(fill_in_blank) 문제 시드 데이터."""

from app.seeds._base import fb, test


def get_fill_blank_data() -> dict:
    """빈칸 채우기 문제 데이터 반환."""

    # ============================================================
    # 빈칸 채우기 문제 (일차방정식 + 연산)
    # ============================================================
    questions = [
        # 일차방정식 빈칸 문제
        fb(
            id="question-fb-001",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=3,
            content="일차방정식 2x + 6 = 0 의 해는 x = _____ 이다.",
            answer="-3",
            explanation="2x + 6 = 0 → 2x = -6 → x = -3",
            points=10,
            accept_formats=["-3"],
        ),
        fb(
            id="question-fb-002",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=5,
            content="일차방정식 3x - 9 = 6 의 해는 x = _____ 이다.",
            answer="5",
            explanation="3x - 9 = 6 → 3x = 15 → x = 5",
            points=10,
            accept_formats=["5"],
        ),
        fb(
            id="question-fb-005",
            concept_id="concept-001",
            category="concept",
            part="algebra",
            difficulty=7,
            content="일차방정식 5(x - 2) = 3x + 4 의 해는 x = _____ 이다.",
            answer="7",
            explanation="5x - 10 = 3x + 4 → 2x = 14 → x = 7",
            points=15,
            accept_formats=["7"],
        ),
        # 연산 빈칸 문제
        fb(
            id="question-fb-003",
            concept_id="concept-002",
            category="computation",
            part="calc",
            difficulty=4,
            content="(-12) ÷ 4 + 7 = _____",
            answer="4",
            explanation="(-12) ÷ 4 = -3, -3 + 7 = 4",
            points=10,
            accept_formats=["4"],
        ),
        fb(
            id="question-fb-004",
            concept_id="concept-002",
            category="computation",
            part="calc",
            difficulty=6,
            content="(-5) × 3 + (-2) × (-4) = _____",
            answer="-7",
            explanation="(-5) × 3 = -15, (-2) × (-4) = 8, -15 + 8 = -7",
            points=15,
            accept_formats=["-7"],
        ),
    ]

    # ============================================================
    # 빈칸 채우기 테스트
    # ============================================================
    tests = [
        test(
            id="test-006",
            title="빈칸 채우기 연습",
            description="답을 직접 입력하는 빈칸 채우기 문제",
            grade="middle_1",
            concept_ids=["concept-001", "concept-002"],
            question_ids=[
                "question-fb-001",
                "question-fb-002",
                "question-fb-003",
                "question-fb-004",
                "question-fb-005",
            ],
            time_limit_minutes=10,
        ),
    ]

    return {
        "questions": questions,
        "tests": tests,
    }
