"""채점 서비스."""

from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.test_attempt import TestAttempt
from app.models.answer_log import AnswerLog


class GradingService:
    """채점 서비스."""

    def __init__(self, db: Session | None = None):
        self.db = db

    def grade_answer(
        self,
        question_id: str,
        selected_answer: str,
        correct_answer: str,
        points: int,
    ) -> dict:
        """답안 채점."""
        is_correct = selected_answer.strip().upper() == correct_answer.strip().upper()
        points_earned = points if is_correct else 0

        return {
            "is_correct": is_correct,
            "points_earned": points_earned,
        }

    def calculate_combo_bonus(self, combo_count: int, base_points: int) -> int:
        """콤보 보너스 계산."""
        if combo_count >= 10:
            multiplier = 3.0
        elif combo_count >= 5:
            multiplier = 2.0
        elif combo_count >= 3:
            multiplier = 1.5
        else:
            multiplier = 1.0

        return int(base_points * multiplier)

    def submit_answer(
        self,
        attempt: TestAttempt,
        question: Question,
        selected_answer: str,
        time_spent_seconds: int,
        current_combo: int,
    ) -> dict:
        """답안 제출 및 채점."""
        if not self.db:
            raise ValueError("Database session required")

        # 채점
        result = self.grade_answer(
            question_id=question.id,
            selected_answer=selected_answer,
            correct_answer=question.correct_answer,
            points=question.points,
        )

        is_correct = result["is_correct"]

        # 콤보 계산
        if is_correct:
            new_combo = current_combo + 1
            points_with_bonus = self.calculate_combo_bonus(new_combo, question.points)
        else:
            new_combo = 0
            points_with_bonus = 0

        # XP 계산 (기본: 점수의 절반)
        xp_earned = points_with_bonus // 2 if is_correct else 0

        # 답안 기록 저장
        answer_log = AnswerLog(
            attempt_id=attempt.id,
            question_id=question.id,
            selected_answer=selected_answer,
            is_correct=is_correct,
            time_spent_seconds=time_spent_seconds,
            combo_count=new_combo,
            points_earned=points_with_bonus,
            question_difficulty=question.difficulty,
            question_category=question.category.value if question.category else None,
        )
        self.db.add(answer_log)

        # 시도 업데이트 (max_score 초과 방지)
        attempt.score = min(attempt.score + points_with_bonus, attempt.max_score)
        attempt.xp_earned += xp_earned
        if is_correct:
            attempt.correct_count += 1
        attempt.combo_max = max(attempt.combo_max, new_combo)

        self.db.commit()

        # 남은 문제 수 계산
        answered_count = len(attempt.answer_logs)
        questions_remaining = attempt.total_count - answered_count

        return {
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
            "points_earned": points_with_bonus,
            "combo_count": new_combo,
            "xp_earned": xp_earned,
            "current_score": attempt.score,
            "questions_remaining": questions_remaining,
        }
