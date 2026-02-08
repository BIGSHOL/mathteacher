"""오답 간격 반복 학습 서비스."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wrong_answer_review import WrongAnswerReview

# KST 타임존
KST = timezone(timedelta(hours=9))

# stage → 다음 복습까지 일수
REVIEW_INTERVALS = {1: 1, 2: 3, 3: 7, 4: 30, 5: 60}
MAX_STAGE = 5


class ReviewService:
    """오답 간격 반복 학습 관리.

    틀린 문제를 1일→3일→7일→30일→60일 간격으로 재출제.
    5단계 모두 통과하면 졸업. 졸업 후 또 틀리면 리셋.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    def _today_str(self) -> str:
        """KST 기준 오늘 날짜 문자열."""
        return datetime.now(KST).date().isoformat()

    def _future_date_str(self, days: int) -> str:
        """KST 기준 N일 후 날짜 문자열."""
        return (datetime.now(KST).date() + timedelta(days=days)).isoformat()

    async def register_wrong(self, student_id: str, question_id: str) -> None:
        """틀린 문제 등록 또는 리셋.

        - 신규: stage=1, next_review_date=내일
        - 기존(복습 중): stage=1로 리셋, wrong_count += 1
        - 기존(졸업): 졸업 취소, stage=1로 리셋
        """
        now = datetime.now(timezone.utc)
        review = await self._get(student_id, question_id)

        if review:
            review.wrong_count += 1
            review.review_stage = 1
            review.correct_streak = 0
            review.is_graduated = False
            review.graduated_at = None
            review.next_review_date = self._future_date_str(REVIEW_INTERVALS[1])
            review.last_wrong_at = now
        else:
            review = WrongAnswerReview(
                student_id=student_id,
                question_id=question_id,
                review_stage=1,
                next_review_date=self._future_date_str(REVIEW_INTERVALS[1]),
                wrong_count=1,
                correct_streak=0,
                last_wrong_at=now,
            )
            self.db.add(review)

        await self.db.flush()

    async def register_correct(self, student_id: str, question_id: str) -> None:
        """복습 대상 문제를 맞힌 경우 stage 승급.

        - 복습 대상 아니면 무시 (한 번도 틀리지 않은 문제)
        - 이미 졸업이면 무시
        - stage 5에서 맞추면 졸업
        """
        review = await self._get(student_id, question_id)
        if not review or review.is_graduated:
            return

        now = datetime.now(timezone.utc)
        review.correct_streak += 1
        review.last_reviewed_at = now

        if review.review_stage >= MAX_STAGE:
            # 졸업
            review.is_graduated = True
            review.graduated_at = now
        else:
            # 다음 stage로 승급
            review.review_stage += 1
            days = REVIEW_INTERVALS[review.review_stage]
            review.next_review_date = self._future_date_str(days)

        await self.db.flush()

    async def get_due_question_ids(
        self, student_id: str, limit: int = 3
    ) -> list[str]:
        """오늘 복습 예정인 문제 ID 목록.

        우선순위: 낮은 stage 먼저, 같은 stage면 최근 틀린 것 먼저.
        """
        today = self._today_str()
        stmt = (
            select(WrongAnswerReview.question_id)
            .where(
                WrongAnswerReview.student_id == student_id,
                WrongAnswerReview.is_graduated == False,
                WrongAnswerReview.next_review_date <= today,
            )
            .order_by(
                WrongAnswerReview.review_stage.asc(),
                WrongAnswerReview.last_wrong_at.desc(),
            )
            .limit(limit)
        )
        return list((await self.db.scalars(stmt)).all())

    async def get_review_stats(self, student_id: str) -> dict:
        """학생의 복습 현황 통계."""
        stmt = select(WrongAnswerReview).where(
            WrongAnswerReview.student_id == student_id
        )
        reviews = list((await self.db.scalars(stmt)).all())

        today = self._today_str()
        active = [r for r in reviews if not r.is_graduated]
        graduated = [r for r in reviews if r.is_graduated]
        due_today = [r for r in active if r.next_review_date <= today]

        return {
            "total_tracked": len(reviews),
            "active_reviews": len(active),
            "graduated": len(graduated),
            "due_today": len(due_today),
            "by_stage": {
                stage: sum(1 for r in active if r.review_stage == stage)
                for stage in range(1, MAX_STAGE + 1)
            },
        }

    async def _get(
        self, student_id: str, question_id: str
    ) -> WrongAnswerReview | None:
        """student_id + question_id로 조회."""
        stmt = select(WrongAnswerReview).where(
            WrongAnswerReview.student_id == student_id,
            WrongAnswerReview.question_id == question_id,
        )
        return await self.db.scalar(stmt)
