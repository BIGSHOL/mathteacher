"""테스트 서비스."""

import random
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.answer_log import AnswerLog
from app.models.question import Question
from app.schemas.common import Grade, QuestionType
from app.services.blank_service import BlankService


def shuffle_question_options(options: list[dict], correct_answer: str) -> tuple[list[dict], str]:
    """문제 보기를 셔플하고 새 정답 라벨을 반환.

    Args:
        options: 원본 보기 리스트
        correct_answer: 원본 정답 라벨 (A, B, C, D 등)

    Returns:
        tuple: (셔플된 options 리스트, 새 정답 라벨)
    """
    if not options:
        return [], correct_answer

    # 정답 option의 id 찾기
    correct_option_id = None
    for opt in options:
        if opt.get("label") == correct_answer:
            correct_option_id = opt.get("id")
            break

    # 옵션 복사 후 셔플
    shuffled = [opt.copy() for opt in options]
    random.shuffle(shuffled)

    # 새 라벨 부여 (A, B, C, D, ...)
    labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
    new_correct = correct_answer

    for i, opt in enumerate(shuffled):
        new_label = labels[i] if i < len(labels) else str(i + 1)
        if opt.get("id") == correct_option_id:
            new_correct = new_label
        opt["label"] = new_label

    return shuffled, new_correct


async def get_student_attempt_count(db: AsyncSession, student_id: str, test_id: str) -> int:
    """완료된 시도 횟수 계산."""
    stmt = select(func.count()).where(
        TestAttempt.test_id == test_id,
        TestAttempt.student_id == student_id,
        TestAttempt.completed_at.isnot(None),
    )
    return await db.scalar(stmt) or 0


class TestService:
    """테스트 서비스."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_available_tests(
        self,
        student_id: str,
        grade: Grade | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict], int]:
        """풀 수 있는 테스트 목록 조회."""
        stmt = select(Test).where(Test.is_active == True)  # noqa: E712

        if grade:
            stmt = stmt.where(Test.grade == grade)

        # 총 개수
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.db.scalar(count_stmt) or 0

        # 페이지네이션
        stmt = stmt.order_by(Test.created_at.desc())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        tests = list((await self.db.scalars(stmt)).all())

        # 한 번의 쿼리로 모든 테스트의 시도 통계 조회
        test_ids = [t.id for t in tests]
        if test_ids:
            stats_stmt = select(
                TestAttempt.test_id,
                func.count().label("attempt_count"),
                func.max(TestAttempt.score).label("best_score"),
            ).where(
                TestAttempt.test_id.in_(test_ids),
                TestAttempt.student_id == student_id,
                TestAttempt.completed_at.isnot(None),
            ).group_by(TestAttempt.test_id)

            stats_map = {}
            for row in await self.db.execute(stats_stmt):
                stats_map[row.test_id] = {
                    "attempt_count": row.attempt_count,
                    "best_score": row.best_score,
                }
        else:
            stats_map = {}

        # 각 테스트에 대한 학생의 시도 정보 추가
        result = []
        for test in tests:
            stats = stats_map.get(test.id, {"attempt_count": 0, "best_score": None})
            result.append({
                "test": test,
                "is_completed": stats["attempt_count"] > 0,
                "best_score": stats["best_score"],
                "attempt_count": stats["attempt_count"],
            })

        return result, total

    async def get_test_by_id(self, test_id: str) -> Test | None:
        """테스트 조회."""
        return await self.db.get(Test, test_id)

    async def get_test_with_questions(self, test_id: str) -> dict | None:
        """테스트와 문제 목록 조회."""
        test = await self.get_test_by_id(test_id)
        if not test:
            return None

        # 문제 조회
        stmt = select(Question).where(Question.id.in_(test.question_ids))
        questions = list((await self.db.scalars(stmt)).all())

        # 문제 순서 정렬 (question_ids 순서대로)
        question_map = {q.id: q for q in questions}
        ordered_questions = [question_map[qid] for qid in test.question_ids if qid in question_map]

        return {
            "test": test,
            "questions": ordered_questions,
        }

    async def start_test(self, test_id: str, student_id: str) -> TestAttempt | None:
        """테스트 시작."""
        test = await self.get_test_by_id(test_id)
        if not test:
            return None

        # 문제 선택
        all_question_ids = test.question_ids or []
        selected_question_ids = all_question_ids

        # 문제 풀 방식: 랜덤하게 N개 선택
        if test.use_question_pool and test.questions_per_attempt:
            pool_size = len(all_question_ids)
            select_count = min(test.questions_per_attempt, pool_size)
            selected_question_ids = random.sample(all_question_ids, select_count)

        # 선택된 문제 조회
        stmt = select(Question).where(Question.id.in_(selected_question_ids))
        questions = list((await self.db.scalars(stmt)).all())
        question_map = {q.id: q for q in questions}
        ordered_questions = [question_map[qid] for qid in selected_question_ids if qid in question_map]

        # 보기 셔플 설정 생성
        question_shuffle_config = {}
        if test.shuffle_options:
            for q in ordered_questions:
                if q.options:
                    shuffled_options, new_correct = shuffle_question_options(
                        q.options, q.correct_answer
                    )
                    question_shuffle_config[q.id] = {
                        "shuffled_options": shuffled_options,
                        "correct_answer": new_correct,
                    }

        # 빈칸 생성 (빈칸 채우기 문제용)
        attempt_count = await get_student_attempt_count(self.db, student_id, test_id) + 1
        blank_service = BlankService(self.db)

        for q in ordered_questions:
            if q.question_type == QuestionType.FILL_IN_BLANK and q.blank_config:
                # 임시 attempt_id 생성 (실제 attempt는 아직 생성 전)
                temp_attempt_id = f"temp_{test_id}_{student_id}_{attempt_count}"
                blank_data = blank_service.generate_blanks_for_attempt(
                    question=q,
                    attempt_count=attempt_count,
                    student_id=student_id,
                    attempt_id=temp_attempt_id
                )

                if blank_data:
                    if q.id not in question_shuffle_config:
                        question_shuffle_config[q.id] = {}
                    question_shuffle_config[q.id]["blank_config"] = blank_data

        # 최대 점수 계산
        max_score = sum(q.points for q in ordered_questions)

        # 시도 생성
        attempt = TestAttempt(
            test_id=test_id,
            student_id=student_id,
            max_score=max_score,
            total_count=len(ordered_questions),
            selected_question_ids=selected_question_ids if test.use_question_pool else None,
            question_shuffle_config=question_shuffle_config if question_shuffle_config else None,
        )
        self.db.add(attempt)
        await self.db.commit()
        await self.db.refresh(attempt)

        return attempt

    async def get_attempt_by_id(self, attempt_id: str) -> TestAttempt | None:
        """시도 조회."""
        return await self.db.get(TestAttempt, attempt_id)

    async def get_attempt_questions(self, attempt_id: str) -> list[dict] | None:
        """시도의 문제 목록 조회 (셔플 적용)."""
        attempt = await self.get_attempt_by_id(attempt_id)
        if not attempt:
            return None

        test = await self.get_test_by_id(attempt.test_id)
        if not test:
            return None

        # 문제 ID 결정 (문제 풀 방식이면 선택된 문제, 아니면 전체)
        question_ids = attempt.selected_question_ids or test.question_ids or []

        # 문제 조회
        stmt = select(Question).where(Question.id.in_(question_ids))
        questions = list((await self.db.scalars(stmt)).all())
        question_map = {q.id: q for q in questions}
        ordered_questions = [question_map[qid] for qid in question_ids if qid in question_map]

        # 셔플 설정 적용
        shuffle_config = attempt.question_shuffle_config or {}
        result = []

        for q in ordered_questions:
            q_data = {
                "id": q.id,
                "concept_id": q.concept_id,
                "category": q.category,
                "part": q.part,
                "content": q.content,
                "question_type": q.question_type,
                "difficulty": q.difficulty,
                "points": q.points,
                "explanation": q.explanation,
            }

            # 셔플된 보기와 정답 사용
            if q.id in shuffle_config:
                config = shuffle_config[q.id]
                if "shuffled_options" in config:
                    q_data["options"] = config["shuffled_options"]
                    # 정답은 응답에 포함하지 않음 (채점 시에만 사용)
                if "blank_config" in config:
                    q_data["blank_config"] = config["blank_config"]
            else:
                q_data["options"] = q.options

            result.append(q_data)

        return result

    async def get_correct_answer_for_attempt(self, attempt_id: str, question_id: str) -> str | None:
        """특정 시도에서 문제의 정답 조회 (셔플 적용)."""
        attempt = await self.get_attempt_by_id(attempt_id)
        if not attempt:
            return None

        # 셔플 설정에서 정답 확인
        shuffle_config = attempt.question_shuffle_config or {}
        if question_id in shuffle_config:
            return shuffle_config[question_id]["correct_answer"]

        # 셔플이 없으면 원본 정답
        question = await self.db.get(Question, question_id)
        return question.correct_answer if question else None

    async def get_attempt_with_details(self, attempt_id: str) -> dict | None:
        """시도와 상세 정보 조회."""
        attempt = await self.get_attempt_by_id(attempt_id)
        if not attempt:
            return None

        # 답안 기록 조회
        stmt = select(AnswerLog).where(AnswerLog.attempt_id == attempt_id)
        answer_logs = list((await self.db.scalars(stmt)).all())

        # 테스트 정보
        test = await self.get_test_by_id(attempt.test_id)

        return {
            "attempt": attempt,
            "answer_logs": answer_logs,
            "test": test,
        }

    async def check_already_answered(self, attempt_id: str, question_id: str) -> bool:
        """이미 답안을 제출했는지 확인."""
        stmt = select(AnswerLog).where(
            AnswerLog.attempt_id == attempt_id,
            AnswerLog.question_id == question_id,
        )
        return await self.db.scalar(stmt) is not None

    async def get_current_combo(self, attempt_id: str) -> int:
        """현재 콤보 수 조회."""
        stmt = (
            select(AnswerLog)
            .where(AnswerLog.attempt_id == attempt_id)
            .order_by(AnswerLog.created_at.desc())
        )
        logs = list((await self.db.scalars(stmt)).all())

        combo = 0
        for log in logs:
            if log.is_correct:
                combo += 1
            else:
                break

        return combo

    async def complete_attempt(self, attempt_id: str) -> TestAttempt | None:
        """시도 완료."""
        attempt = await self.get_attempt_by_id(attempt_id)
        if not attempt or attempt.completed_at:
            return None

        attempt.completed_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(attempt)

        return attempt
