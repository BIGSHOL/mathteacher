"""테스트 서비스."""

from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.answer_log import AnswerLog
from app.models.question import Question
from app.schemas.common import Grade


class TestService:
    """테스트 서비스."""

    def __init__(self, db: Session):
        self.db = db

    def get_available_tests(
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
        total = self.db.scalar(count_stmt) or 0

        # 페이지네이션
        stmt = stmt.order_by(Test.created_at.desc())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        tests = list(self.db.scalars(stmt).all())

        # 각 테스트에 대한 학생의 시도 정보 추가
        result = []
        for test in tests:
            # 완료된 시도 수
            attempt_stmt = select(func.count()).where(
                TestAttempt.test_id == test.id,
                TestAttempt.student_id == student_id,
                TestAttempt.completed_at.isnot(None),
            )
            attempt_count = self.db.scalar(attempt_stmt) or 0

            # 최고 점수
            best_stmt = select(func.max(TestAttempt.score)).where(
                TestAttempt.test_id == test.id,
                TestAttempt.student_id == student_id,
                TestAttempt.completed_at.isnot(None),
            )
            best_score = self.db.scalar(best_stmt)

            result.append({
                "test": test,
                "is_completed": attempt_count > 0,
                "best_score": best_score,
                "attempt_count": attempt_count,
            })

        return result, total

    def get_test_by_id(self, test_id: str) -> Test | None:
        """테스트 조회."""
        return self.db.get(Test, test_id)

    def get_test_with_questions(self, test_id: str) -> dict | None:
        """테스트와 문제 목록 조회."""
        test = self.get_test_by_id(test_id)
        if not test:
            return None

        # 문제 조회
        stmt = select(Question).where(Question.id.in_(test.question_ids))
        questions = list(self.db.scalars(stmt).all())

        # 문제 순서 정렬 (question_ids 순서대로)
        question_map = {q.id: q for q in questions}
        ordered_questions = [question_map[qid] for qid in test.question_ids if qid in question_map]

        return {
            "test": test,
            "questions": ordered_questions,
        }

    def start_test(self, test_id: str, student_id: str) -> TestAttempt | None:
        """테스트 시작."""
        test_data = self.get_test_with_questions(test_id)
        if not test_data:
            return None

        test = test_data["test"]
        questions = test_data["questions"]

        # 최대 점수 계산
        max_score = sum(q.points for q in questions)

        # 시도 생성
        attempt = TestAttempt(
            test_id=test_id,
            student_id=student_id,
            max_score=max_score,
            total_count=len(questions),
        )
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)

        return attempt

    def get_attempt_by_id(self, attempt_id: str) -> TestAttempt | None:
        """시도 조회."""
        return self.db.get(TestAttempt, attempt_id)

    def get_attempt_with_details(self, attempt_id: str) -> dict | None:
        """시도와 상세 정보 조회."""
        attempt = self.get_attempt_by_id(attempt_id)
        if not attempt:
            return None

        # 답안 기록 조회
        stmt = select(AnswerLog).where(AnswerLog.attempt_id == attempt_id)
        answer_logs = list(self.db.scalars(stmt).all())

        # 테스트 정보
        test = self.get_test_by_id(attempt.test_id)

        return {
            "attempt": attempt,
            "answer_logs": answer_logs,
            "test": test,
        }

    def check_already_answered(self, attempt_id: str, question_id: str) -> bool:
        """이미 답안을 제출했는지 확인."""
        stmt = select(AnswerLog).where(
            AnswerLog.attempt_id == attempt_id,
            AnswerLog.question_id == question_id,
        )
        return self.db.scalar(stmt) is not None

    def get_current_combo(self, attempt_id: str) -> int:
        """현재 콤보 수 조회."""
        stmt = (
            select(AnswerLog)
            .where(AnswerLog.attempt_id == attempt_id)
            .order_by(AnswerLog.created_at.desc())
        )
        logs = list(self.db.scalars(stmt).all())

        combo = 0
        for log in logs:
            if log.is_correct:
                combo += 1
            else:
                break

        return combo

    def complete_attempt(self, attempt_id: str) -> TestAttempt | None:
        """시도 완료."""
        attempt = self.get_attempt_by_id(attempt_id)
        if not attempt or attempt.completed_at:
            return None

        attempt.completed_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(attempt)

        return attempt
