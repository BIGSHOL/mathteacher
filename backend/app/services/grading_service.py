"""채점 서비스."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.question import Question
from app.models.test_attempt import TestAttempt
from app.models.answer_log import AnswerLog
from app.models.focus_check import FocusCheckItem

# 재도전 관련 상수
MAX_RETRY_COUNT = 4  # 최대 재도전 횟수 (4회 틀리면 집중체크로)


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

    async def submit_answer_with_retry(
        self,
        attempt: TestAttempt,
        question: Question,
        selected_answer: str,
        time_spent_seconds: int,
        current_combo: int,
        correct_answer_override: str | None = None,
        is_daily_test: bool = False,
    ) -> dict:
        """답안 제출 및 채점 (재도전 기능 포함).
        
        오늘의 학습(daily test)에서 틀린 문제는 재도전 큐에 추가됩니다.
        4회 이상 틀리면 집중 체크 목록에 저장됩니다.
        """
        # 기본 채점 수행
        result = await self.submit_answer(
            attempt=attempt,
            question=question,
            selected_answer=selected_answer,
            time_spent_seconds=time_spent_seconds,
            current_combo=current_combo,
            correct_answer_override=correct_answer_override,
        )
        
        # 일일 테스트가 아니면 기본 결과 반환
        if not is_daily_test:
            return result
        
        # 재도전 로직 (오답인 경우에만)
        if not result["is_correct"]:
            # SQLAlchemy 변경 감지를 위해 복사본 생성 (JSON 타입 컬럼의 변경 추적 문제 해결)
            # list()와 dict()를 사용하여 명시적으로 새로운 객체를 생성해야 SQLAlchemy가 변경사항을 감지함
            retry_counts = dict(attempt.retry_counts or {})
            retry_queue = list(attempt.retry_queue or [])
            
            # 해당 문제의 틀린 횟수 증가
            current_count = retry_counts.get(question.id, 0) + 1
            retry_counts[question.id] = current_count
            
            if current_count >= MAX_RETRY_COUNT:
                # 4회 이상 틀림 → 집중 체크에 저장
                focus_item = FocusCheckItem(
                    student_id=attempt.student_id,
                    question_id=question.id,
                    attempt_id=attempt.id,
                    wrong_count=current_count,
                )
                self.db.add(focus_item)
                result["moved_to_focus_check"] = True
                result["focus_check_message"] = "이 문제는 집중 체크 목록에 추가되었습니다."
                
                # 재도전 큐에서 제거 (이미 있다면)
                if question.id in retry_queue:
                    retry_queue.remove(question.id)
            else:
                # 재도전 큐 뒤에 추가
                if question.id not in retry_queue:
                    retry_queue.append(question.id)
                result["retry_scheduled"] = True
                result["retry_count"] = current_count
            
            # 힌트 정보 추가
            result["hint"] = self.get_hint_for_retry(question, current_count)
            
            # attempt 업데이트
            attempt.retry_counts = retry_counts
            attempt.retry_queue = retry_queue
            
            try:
                await self.db.commit()
                await self.db.refresh(attempt)
            except Exception:
                await self.db.rollback()
                raise
        else:
            # 정답인 경우 재도전 큐에서 제거
            retry_queue = list(attempt.retry_queue or [])
            if question.id in retry_queue:
                retry_queue.remove(question.id)
                attempt.retry_queue = retry_queue
                await self.db.commit()
                await self.db.refresh(attempt)
        
        # 남은 문제 계산 (재도전 포함)
        result["retry_queue_count"] = len(attempt.retry_queue or [])
        
        return result

    def get_hint_for_retry(self, question: Question, retry_count: int) -> dict | None:
        """재도전 횟수에 따른 힌트 생성.
        
        힌트는 정답 유도가 아닌 사고 방향 제시 수준으로 제한합니다.
        """
        if retry_count < 1:
            return None
        
        hint = {"level": retry_count}
        
        if retry_count == 1:
            # 1회: 관련 개념명만
            hint["type"] = "concept"
            hint["message"] = f"💡 이 문제의 관련 개념을 떠올려보세요."
            hint["concept_id"] = question.concept_id
        elif retry_count == 2:
            # 2회: 풀이 방향 유도 (해설 앞부분 30자, 정답 직접 유도 금지)
            hint["type"] = "direction"
            explanation = question.explanation or ""
            # 첫 문장만 추출 (마침표 기준)
            first_sentence = explanation.split('.')[0] if '.' in explanation else explanation[:30]
            hint["message"] = f"📖 힌트: {first_sentence[:30]}..."
        elif retry_count >= 3:
            # 3회: 약간 더 자세한 유도 (해설 앞부분 50자)
            hint["type"] = "extended"
            explanation = question.explanation or ""
            hint["message"] = f"📚 다시 생각해보세요: {explanation[:50]}..."
        
        return hint
