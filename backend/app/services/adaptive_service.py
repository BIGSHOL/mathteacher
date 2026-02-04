"""적응형 난이도 서비스."""

import random

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.answer_log import AnswerLog
from app.models.question import Question
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.user import User

MIN_DIFFICULTY = 1
MAX_DIFFICULTY = 10


class AdaptiveService:
    """적응형 난이도 서비스 (1-10 정수 난이도 체계)."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def determine_initial_difficulty(
        self, student_id: str, concept_ids: list[str]
    ) -> int:
        """Phase A: 학생 레벨과 정답률 기반 초기 난이도 결정.

        readiness = (level / 10) * 0.4 + accuracy * 0.6
        readiness < 0.35 → 난이도 3 (easy 영역 중심)
        0.35 ~ 0.65     → 난이도 6 (medium 영역 중심)
        >= 0.65          → 난이도 8 (hard 영역 중심)
        """
        student = await self.db.get(User, student_id)
        level = student.level if student else 1

        accuracy = await self._get_concept_accuracy(student_id, concept_ids)
        readiness = (level / 10) * 0.4 + accuracy * 0.6

        if readiness < 0.35:
            return 3
        elif readiness < 0.65:
            return 6
        else:
            return 8

    async def select_first_question(
        self, test: Test, student_id: str
    ) -> Question | None:
        """Phase A: 초기 난이도에 맞는 첫 번째 문제 선택."""
        target = await self.determine_initial_difficulty(student_id, test.concept_ids)
        return await self._select_closest_question(test, target, exclude_ids=[])

    async def get_initial_difficulty_for(
        self, test: Test, student_id: str
    ) -> int:
        """초기 난이도 값 반환 (attempt에 기록용)."""
        return await self.determine_initial_difficulty(student_id, test.concept_ids)

    async def select_next_question(
        self, attempt: TestAttempt
    ) -> tuple[Question | None, int]:
        """Phase B: 실시간 적응형 다음 문제 선택.

        Returns:
            (question, target_difficulty) 또는 (None, current_difficulty) 완료 시
        """
        answered_count = len(attempt.adaptive_question_ids or [])
        if answered_count >= attempt.total_count:
            return None, attempt.current_difficulty or 6

        # 최근 답안 기록 조회
        logs = list(
            (await self.db.scalars(
                select(AnswerLog)
                .where(AnswerLog.attempt_id == attempt.id)
                .order_by(AnswerLog.created_at.desc())
            )).all()
        )

        current = attempt.current_difficulty or 6
        target = self._calculate_next_difficulty(current, logs)

        # 문제 풀에서 선택
        test = attempt.test
        exclude_ids = attempt.adaptive_question_ids or []
        question = await self._select_closest_question(test, target, exclude_ids)

        if not question:
            return None, target

        # attempt 상태 업데이트
        new_ids = list(exclude_ids) + [question.id]
        attempt.adaptive_question_ids = new_ids
        attempt.current_difficulty = target
        attempt.max_score += question.points
        await self.db.flush()

        return question, target

    async def peek_next_difficulty(self, attempt: TestAttempt) -> int | None:
        """다음 문제의 예상 난이도 (UI 힌트용)."""
        if not attempt.is_adaptive:
            return None

        answered_count = len(attempt.adaptive_question_ids or [])
        if answered_count >= attempt.total_count:
            return None

        logs = list(
            (await self.db.scalars(
                select(AnswerLog)
                .where(AnswerLog.attempt_id == attempt.id)
                .order_by(AnswerLog.created_at.desc())
            )).all()
        )

        current = attempt.current_difficulty or 6
        return self._calculate_next_difficulty(current, logs)

    def _calculate_next_difficulty(
        self, current: int, logs: list[AnswerLog]
    ) -> int:
        """최근 답안 기반 다음 난이도 계산.

        - 정답 → +1
        - 오답 → -1
        - 같은 난이도에서 연속 2회 정답 → +2
        - 같은 난이도에서 연속 2회 오답 → -2
        """
        if not logs:
            return current

        last = logs[0]

        if last.is_correct:
            step = 1
            if (
                len(logs) >= 2
                and logs[1].is_correct
                and logs[1].question_difficulty == current
                and last.question_difficulty == current
            ):
                step = 2
            return min(current + step, MAX_DIFFICULTY)
        else:
            step = 1
            if (
                len(logs) >= 2
                and not logs[1].is_correct
                and logs[1].question_difficulty == current
                and last.question_difficulty == current
            ):
                step = 2
            return max(current - step, MIN_DIFFICULTY)

    async def _select_closest_question(
        self, test: Test, target: int, exclude_ids: list[str]
    ) -> Question | None:
        """target 난이도에 가장 가까운 문제 선택.

        정확히 일치하는 문제 우선, 없으면 ±1, ±2... 범위 확장.
        """
        for spread in range(MAX_DIFFICULTY):
            candidates = []
            for diff in [target + spread, target - spread]:
                if diff < MIN_DIFFICULTY or diff > MAX_DIFFICULTY:
                    continue
                pool = await self._get_pool_by_difficulty(test, diff, exclude_ids)
                candidates.extend(pool)
            if candidates:
                return random.choice(candidates)
        return None

    async def _get_pool_by_difficulty(
        self, test: Test, difficulty: int, exclude_ids: list[str]
    ) -> list[Question]:
        """특정 난이도의 사용 가능한 문제 풀 조회."""
        stmt = (
            select(Question)
            .where(
                Question.concept_id.in_(test.concept_ids),
                Question.difficulty == difficulty,
                Question.is_active == True,  # noqa: E712
            )
        )
        if exclude_ids:
            stmt = stmt.where(Question.id.notin_(exclude_ids))

        return list((await self.db.scalars(stmt)).all())

    async def _get_concept_accuracy(
        self, student_id: str, concept_ids: list[str]
    ) -> float:
        """학생의 특정 개념에 대한 과거 정답률."""
        stmt = (
            select(
                func.count(AnswerLog.id).label("total"),
                func.sum(
                    func.case((AnswerLog.is_correct == True, 1), else_=0)  # noqa: E712
                ).label("correct"),
            )
            .join(TestAttempt, AnswerLog.attempt_id == TestAttempt.id)
            .join(Question, AnswerLog.question_id == Question.id)
            .where(
                TestAttempt.student_id == student_id,
                Question.concept_id.in_(concept_ids),
            )
        )
        result = (await self.db.execute(stmt)).first()
        if not result or not result.total:
            return 0.5  # 기록 없으면 중립값

        return (result.correct or 0) / result.total
