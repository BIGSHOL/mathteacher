"""일일 테스트 서비스."""

import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.concept import Concept
from app.models.concept_mastery import ConceptMastery
from app.models.daily_test_record import DailyTestRecord
from app.models.question import Question
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.user import User
from app.schemas.common import QuestionCategory, QuestionType
from app.services.test_service import TestService

QUESTIONS_PER_DAILY_TEST = 10
CATEGORY_LABELS = {
    "concept": "개념",
    "computation": "연산",
    "fill_in_blank": "빈칸",
}
DAILY_CATEGORIES = ["concept", "computation", "fill_in_blank"]
KST = timezone(timedelta(hours=9))


class DailyTestService:
    """일일 테스트 서비스."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def get_today_str(self) -> str:
        """오늘 날짜 문자열 (KST)."""
        return datetime.now(KST).date().isoformat()

    # ------------------------------------------------------------------
    # 공개 메서드
    # ------------------------------------------------------------------

    async def get_today_tests(self, student_id: str) -> list[DailyTestRecord]:
        """오늘의 3개 카테고리 테스트 (없으면 자동 생성)."""
        records = []
        for cat in DAILY_CATEGORIES:
            records.append(await self.get_or_create_daily_test(student_id, cat))
        return records

    async def get_or_create_daily_test(
        self, student_id: str, category: str
    ) -> DailyTestRecord:
        """오늘자 테스트 조회 또는 생성."""
        today = self.get_today_str()

        # 1. 기존 레코드 확인
        stmt = select(DailyTestRecord).where(
            DailyTestRecord.student_id == student_id,
            DailyTestRecord.date == today,
            DailyTestRecord.category == category,
        )
        record = await self.db.scalar(stmt)
        if record:
            return record

        # 2. 테스트 생성
        test = await self._generate_test(student_id, category, today)

        # 3. DailyTestRecord 생성
        record = DailyTestRecord(
            student_id=student_id,
            date=today,
            category=category,
            test_id=test.id,
            status="pending",
            total_count=test.question_count,
        )

        try:
            self.db.add(record)
            await self.db.commit()
            await self.db.refresh(record)
        except IntegrityError:
            # 동시 요청으로 이미 생성됨 → 재조회
            await self.db.rollback()
            record = await self.db.scalar(stmt)

        return record

    async def start_daily_test(
        self, student_id: str, record_id: str
    ) -> TestAttempt | None:
        """일일 테스트 시작 → TestAttempt 생성."""
        record = await self.db.get(DailyTestRecord, record_id)
        if not record or record.student_id != student_id:
            return None
        if record.status == "completed":
            return None

        # 이미 시작한 경우 기존 attempt 반환
        if record.attempt_id:
            return await self.db.get(TestAttempt, record.attempt_id)

        # TestService로 시도 생성
        test_service = TestService(self.db)
        attempt = await test_service.start_test(record.test_id, student_id)
        if not attempt:
            return None

        record.attempt_id = attempt.id
        record.status = "in_progress"
        await self.db.commit()
        await self.db.refresh(record)

        return attempt

    async def try_complete_daily_test(self, attempt_id: str) -> None:
        """테스트 완료 시 DailyTestRecord 상태 동기화 (훅)."""
        stmt = select(DailyTestRecord).where(
            DailyTestRecord.attempt_id == attempt_id
        )
        record = await self.db.scalar(stmt)
        if not record:
            return  # 일일 테스트가 아님

        attempt = await self.db.get(TestAttempt, attempt_id)
        if not attempt or not attempt.completed_at:
            return

        record.status = "completed"
        record.score = attempt.score
        record.max_score = attempt.max_score
        record.correct_count = attempt.correct_count
        record.total_count = attempt.total_count
        record.completed_at = attempt.completed_at
        await self.db.commit()

    async def get_history(
        self, student_id: str, page: int = 1, page_size: int = 30
    ) -> tuple[list[DailyTestRecord], int]:
        """과거 일일 테스트 이력 (오늘 제외, 날짜 내림차순)."""
        today = self.get_today_str()

        base = select(DailyTestRecord).where(
            DailyTestRecord.student_id == student_id,
            DailyTestRecord.date < today,
        )

        # 총 개수
        count_stmt = select(func.count()).select_from(base.subquery())
        total = await self.db.scalar(count_stmt) or 0

        # 페이지네이션
        stmt = base.order_by(
            DailyTestRecord.date.desc(),
            DailyTestRecord.category,
        ).offset((page - 1) * page_size).limit(page_size)
        records = list((await self.db.scalars(stmt)).all())

        return records, total

    # ------------------------------------------------------------------
    # 내부 메서드
    # ------------------------------------------------------------------

    async def _generate_test(self, student_id: str, category: str, date: str) -> Test:
        """카테고리에 맞는 테스트 생성."""
        student = await self.db.get(User, student_id)
        grade = student.grade if student else None

        question_ids = await self._select_questions(student_id, category, grade)
        question_count = len(question_ids)

        # 관련 개념 ID 수집
        if question_ids:
            stmt = select(Question.concept_id).where(
                Question.id.in_(question_ids)
            ).distinct()
            concept_ids = [r for r in (await self.db.scalars(stmt)).all()]
        else:
            concept_ids = []

        label = CATEGORY_LABELS.get(category, category)
        test = Test(
            id=f"daily-{student_id[:8]}-{date}-{category}",
            title=f"오늘의 {label} ({date})",
            description=f"{date} 일일 {label} 테스트",
            grade=grade,
            concept_ids=concept_ids,
            question_ids=question_ids,
            question_count=question_count,
            is_adaptive=False,
            shuffle_options=True,
            is_active=True,
        )
        self.db.add(test)
        await self.db.flush()
        return test

    async def _select_questions(
        self,
        student_id: str,
        category: str,
        grade,
        count: int = QUESTIONS_PER_DAILY_TEST,
    ) -> list[str]:
        """학생 맞춤형 문제 선택 알고리즘.

        전략:
          1. 약점 개념 (mastery < 60%) 문제 40%
          2. 최근 해금 개념 문제 20%
          3. 나머지 풀에서 랜덤 40%
        난이도: 학생 레벨 기반 (레벨-2 ~ 레벨+1)
        중복 제외: 최근 3일 출제 문제
        """
        student = await self.db.get(User, student_id)
        level = student.level if student else 3

        # 난이도 범위
        diff_min = max(1, level - 2)
        diff_max = min(10, level + 1)

        # 최근 3일 출제 문제 ID
        recently_used = await self._get_recently_used_questions(student_id, category, days=3)

        # 기본 문제 풀 쿼리
        base_query = select(Question).where(
            Question.is_active == True,  # noqa: E712
            Question.difficulty >= diff_min,
            Question.difficulty <= diff_max,
            ~Question.id.in_(recently_used) if recently_used else True,
        )

        # 카테고리 필터
        if category == "fill_in_blank":
            base_query = base_query.where(
                Question.question_type == QuestionType.FILL_IN_BLANK
            )
        elif category == "concept":
            base_query = base_query.where(
                Question.category == QuestionCategory.CONCEPT
            )
        elif category == "computation":
            base_query = base_query.where(
                Question.category == QuestionCategory.COMPUTATION
            )

        # 학년 필터: 해당 학년의 개념에 속하는 문제
        if grade:
            grade_concept_ids = await self._get_grade_concept_ids(grade)
            if grade_concept_ids:
                base_query = base_query.where(
                    Question.concept_id.in_(grade_concept_ids)
                )

        all_questions = list((await self.db.scalars(base_query)).all())

        if not all_questions:
            # 난이도 범위를 넓혀서 재시도
            return await self._select_questions_fallback(
                student_id, category, grade, count, recently_used
            )

        # 숙련도 기반 분류
        mastery_map = await self._get_mastery_map(student_id)
        weak_questions = []
        recent_questions = []
        other_questions = []

        recent_concept_ids = await self._get_recently_unlocked_concepts(student_id, days=14)

        for q in all_questions:
            mastery = mastery_map.get(q.concept_id, 0)
            if mastery < 60:
                weak_questions.append(q.id)
            elif q.concept_id in recent_concept_ids:
                recent_questions.append(q.id)
            else:
                other_questions.append(q.id)

        # 슬롯 배분 (40% / 20% / 40%)
        weak_slot = min(count * 4 // 10, len(weak_questions))
        recent_slot = min(count * 2 // 10, len(recent_questions))
        other_slot = count - weak_slot - recent_slot

        selected = []
        if weak_questions:
            selected += random.sample(weak_questions, min(weak_slot, len(weak_questions)))
        if recent_questions:
            selected += random.sample(recent_questions, min(recent_slot, len(recent_questions)))

        # 나머지 채우기
        remaining = count - len(selected)
        if remaining > 0:
            pool = [q for q in other_questions if q not in selected]
            # 다른 풀이 부족하면 weak/recent에서도 추가
            if len(pool) < remaining:
                all_ids = [q.id for q in all_questions if q.id not in selected]
                pool = all_ids
            selected += random.sample(pool, min(remaining, len(pool)))

        random.shuffle(selected)
        return selected

    async def _select_questions_fallback(
        self,
        student_id: str,
        category: str,
        grade,
        count: int,
        recently_used: list[str],
    ) -> list[str]:
        """난이도 제한 없이 문제 선택 (폴백)."""
        base_query = select(Question.id).where(
            Question.is_active == True,  # noqa: E712
        )

        if category == "fill_in_blank":
            base_query = base_query.where(
                Question.question_type == QuestionType.FILL_IN_BLANK
            )
        elif category == "concept":
            base_query = base_query.where(
                Question.category == QuestionCategory.CONCEPT
            )
        elif category == "computation":
            base_query = base_query.where(
                Question.category == QuestionCategory.COMPUTATION
            )

        if grade:
            grade_concept_ids = await self._get_grade_concept_ids(grade)
            if grade_concept_ids:
                base_query = base_query.where(
                    Question.concept_id.in_(grade_concept_ids)
                )

        if recently_used:
            base_query = base_query.where(~Question.id.in_(recently_used))

        all_ids = list((await self.db.scalars(base_query)).all())
        if not all_ids:
            # 중복 허용
            base_query_no_exclude = select(Question.id).where(
                Question.is_active == True,  # noqa: E712
            )
            if category == "fill_in_blank":
                base_query_no_exclude = base_query_no_exclude.where(
                    Question.question_type == QuestionType.FILL_IN_BLANK
                )
            elif category == "concept":
                base_query_no_exclude = base_query_no_exclude.where(
                    Question.category == QuestionCategory.CONCEPT
                )
            elif category == "computation":
                base_query_no_exclude = base_query_no_exclude.where(
                    Question.category == QuestionCategory.COMPUTATION
                )
            all_ids = list((await self.db.scalars(base_query_no_exclude)).all())

        return random.sample(all_ids, min(count, len(all_ids)))

    # ------------------------------------------------------------------
    # 헬퍼 메서드
    # ------------------------------------------------------------------

    async def _get_recently_used_questions(
        self, student_id: str, category: str, days: int = 3
    ) -> list[str]:
        """최근 N일간 출제된 문제 ID."""
        today = self.get_today_str()
        cutoff = (datetime.now(KST) - timedelta(days=days)).date().isoformat()

        stmt = select(DailyTestRecord.test_id).where(
            DailyTestRecord.student_id == student_id,
            DailyTestRecord.category == category,
            DailyTestRecord.date >= cutoff,
            DailyTestRecord.date <= today,
        )
        test_ids = list((await self.db.scalars(stmt)).all())
        if not test_ids:
            return []

        # 해당 테스트들의 question_ids 수집
        stmt2 = select(Test.question_ids).where(Test.id.in_(test_ids))
        question_id_lists = list((await self.db.scalars(stmt2)).all())

        used = []
        for qids in question_id_lists:
            if qids:
                used.extend(qids)
        return list(set(used))

    async def _get_grade_concept_ids(self, grade) -> list[str]:
        """해당 학년의 모든 개념 ID."""
        stmt = select(Concept.id).where(Concept.grade == grade)
        return list((await self.db.scalars(stmt)).all())

    async def _get_mastery_map(self, student_id: str) -> dict[str, int]:
        """학생의 개념별 숙련도 맵."""
        stmt = select(
            ConceptMastery.concept_id,
            ConceptMastery.mastery_percentage,
        ).where(ConceptMastery.student_id == student_id)
        rows = (await self.db.execute(stmt)).all()
        return {row[0]: row[1] for row in rows}

    async def _get_recently_unlocked_concepts(
        self, student_id: str, days: int = 14
    ) -> set[str]:
        """최근 N일 내 해금된 개념 ID."""
        cutoff = datetime.now(KST) - timedelta(days=days)
        stmt = select(ConceptMastery.concept_id).where(
            ConceptMastery.student_id == student_id,
            ConceptMastery.is_unlocked == True,  # noqa: E712
            ConceptMastery.unlocked_at >= cutoff,
        )
        return set((await self.db.scalars(stmt)).all())
