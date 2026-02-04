"""채점 서비스."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.question import Question
from app.models.test_attempt import TestAttempt
from app.models.answer_log import AnswerLog


class GradingService:
    """채점 서비스."""

    def __init__(self, db: AsyncSession | None = None):
        self.db = db

    def grade_answer(
        self,
        question_id: str,
        selected_answer: str | dict,
        correct_answer: str | dict,
        points: int,
    ) -> dict:
        """답안 채점 (빈칸 채우기 지원)."""
        # 빈칸 채우기 타입 (dict)
        if isinstance(correct_answer, dict):
            return self._grade_fill_in_blank(selected_answer, correct_answer, points)

        # 일반 문제 (string)
        is_correct = selected_answer.strip().upper() == correct_answer.strip().upper()
        points_earned = points if is_correct else 0

        return {
            "is_correct": is_correct,
            "points_earned": points_earned,
        }

    def _grade_fill_in_blank(
        self,
        student_answers: dict,
        correct_answers: dict,
        points: int
    ) -> dict:
        """빈칸 채우기 채점 (부분 점수 지원)."""
        if not isinstance(student_answers, dict):
            student_answers = {}

        total_blanks = len(correct_answers)
        if total_blanks == 0:
            return {
                "is_correct": True,
                "points_earned": points,
                "correct_count": 0,
                "total_blanks": 0
            }

        correct_count = sum(
            1 for blank_id, correct_data in correct_answers.items()
            if student_answers.get(blank_id, "").strip().upper()
               == correct_data.get("answer", "").strip().upper()
        )

        is_correct = correct_count == total_blanks
        points_earned = int((correct_count / total_blanks) * points)

        return {
            "is_correct": is_correct,
            "points_earned": points_earned,
            "correct_count": correct_count,
            "total_blanks": total_blanks
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

    async def override_to_correct(
        self,
        attempt: TestAttempt,
        question: Question,
        prev_result: dict,
        current_combo: int,
    ) -> dict:
        """AI 유연 채점에서 정답 판정 시, 기존 오답 기록을 정답으로 보정."""
        if not self.db:
            raise ValueError("Database session required")

        # 가장 최근 AnswerLog 조회
        stmt = (
            select(AnswerLog)
            .where(AnswerLog.attempt_id == attempt.id)
            .where(AnswerLog.question_id == question.id)
            .order_by(AnswerLog.created_at.desc())
            .limit(1)
        )
        row = await self.db.execute(stmt)
        answer_log = row.scalar_one_or_none()

        if not answer_log:
            return prev_result

        # 새 콤보/점수/XP 계산
        new_combo = current_combo + 1
        points_with_bonus = self.calculate_combo_bonus(new_combo, question.points)
        xp_earned = points_with_bonus // 2

        old_points = answer_log.points_earned  # 0 (오답이었으므로)

        # AnswerLog 업데이트
        answer_log.is_correct = True
        answer_log.combo_count = new_combo
        answer_log.points_earned = points_with_bonus

        # TestAttempt 업데이트
        attempt.score = min(
            attempt.score - old_points + points_with_bonus, attempt.max_score
        )
        attempt.xp_earned += xp_earned
        attempt.correct_count += 1
        attempt.combo_max = max(attempt.combo_max, new_combo)

        try:
            await self.db.commit()
            await self.db.refresh(attempt)
        except Exception:
            await self.db.rollback()
            raise

        answered_count = await self.db.scalar(
            select(func.count(AnswerLog.id)).where(AnswerLog.attempt_id == attempt.id)
        ) or 0
        questions_remaining = attempt.total_count - answered_count

        return {
            "is_correct": True,
            "correct_answer": prev_result.get("correct_answer", question.correct_answer),
            "explanation": question.explanation,
            "points_earned": points_with_bonus,
            "combo_count": new_combo,
            "xp_earned": xp_earned,
            "current_score": attempt.score,
            "questions_remaining": questions_remaining,
        }

    async def submit_answer(
        self,
        attempt: TestAttempt,
        question: Question,
        selected_answer: str,
        time_spent_seconds: int,
        current_combo: int,
        correct_answer_override: str | None = None,
    ) -> dict:
        """답안 제출 및 채점.

        Args:
            correct_answer_override: 셔플된 경우 사용할 정답 (없으면 원본 사용)
        """
        if not self.db:
            raise ValueError("Database session required")

        # 셔플된 정답 또는 원본 정답 사용
        correct_answer = correct_answer_override or question.correct_answer

        # 채점
        result = self.grade_answer(
            question_id=question.id,
            selected_answer=selected_answer,
            correct_answer=correct_answer,
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

        try:
            self.db.add(answer_log)

            # 시도 업데이트 (max_score 초과 방지)
            attempt.score = min(attempt.score + points_with_bonus, attempt.max_score)
            attempt.xp_earned += xp_earned
            if is_correct:
                attempt.correct_count += 1
            attempt.combo_max = max(attempt.combo_max, new_combo)

            await self.db.commit()
            await self.db.refresh(attempt)
        except Exception:
            await self.db.rollback()
            raise

        # 남은 문제 수 계산
        answered_count = await self.db.scalar(
            select(func.count(AnswerLog.id)).where(AnswerLog.attempt_id == attempt.id)
        ) or 0
        questions_remaining = attempt.total_count - answered_count

        return {
            "is_correct": is_correct,
            "correct_answer": correct_answer,  # 셔플된 정답 반환
            "explanation": question.explanation,
            "points_earned": points_with_bonus,
            "combo_count": new_combo,
            "xp_earned": xp_earned,
            "current_score": attempt.score,
            "questions_remaining": questions_remaining,
        }
