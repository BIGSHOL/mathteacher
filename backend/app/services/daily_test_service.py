"""일일 테스트 서비스."""

import asyncio
import logging
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chapter import Chapter
from app.models.chapter_progress import ChapterProgress
from app.models.concept import Concept
from app.models.concept_mastery import ConceptMastery
from app.models.daily_test_record import DailyTestRecord
from app.models.question import Question
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.user import User
from app.schemas.common import QuestionCategory, QuestionType, ConceptMethod
from app.services.ai_service import AIService
from app.services.template_generator import TemplateGenerator
from app.services.review_service import ReviewService
from app.services.test_service import TestService

logger = logging.getLogger(__name__)

QUESTIONS_PER_DAILY_TEST = 10
MIN_QUESTIONS_PER_DAILY_TEST = 5
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
        self._ai_generated_count = 0

    def get_today_str(self) -> str:
        """오늘 날짜 문자열 (KST)."""
        return datetime.now(KST).date().isoformat()

    # ------------------------------------------------------------------
    # 공개 메서드
    # ------------------------------------------------------------------

    async def get_today_tests(self, student_id: str) -> tuple[list[DailyTestRecord], int]:
        """오늘의 3개 카테고리 테스트 (없으면 자동 생성).

        각 테스트 안에 약점 개념 문제가 자연스럽게 포함됨.

        Returns:
            (레코드 목록, AI 생성 문제 수)
        """
        records = []
        for cat in DAILY_CATEGORIES:
            records.append(await self.get_or_create_daily_test(student_id, cat))
        return records, self._ai_generated_count

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
            # 0문제 테스트는 재생성 시도
            if record.total_count == 0 and record.status != "completed":
                test = await self._generate_test(student_id, category, today)
                if test.question_count > 0:
                    record.test_id = test.id
                    record.total_count = test.question_count
                    await self.db.commit()
                    await self.db.refresh(record)
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
            attempt = await self.db.get(TestAttempt, record.attempt_id)
            if attempt:
                return attempt
            # attempt가 삭제된 경우 → 재생성
            record.attempt_id = None
            record.status = "pending"

        # 테스트가 삭제된 경우 → 재생성
        test = await self.db.get(Test, record.test_id)
        if not test:
            today = self.get_today_str()
            test = await self._generate_test(student_id, record.category, today)
            record.test_id = test.id
            record.total_count = test.question_count

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
        """카테고리에 맞는 테스트 생성. 시드 부족 시 AI 동적 생성."""
        student = await self.db.get(User, student_id)
        grade = student.grade if student else None

        question_ids = await self._select_questions(student_id, category, grade)

        # 연산 카테고리: 템플릿으로 추가 생성 (AI 비용 0)
        if category == "computation" and len(question_ids) < QUESTIONS_PER_DAILY_TEST and grade:
            template_ids = await self._generate_template_questions(
                student_id, grade,
                QUESTIONS_PER_DAILY_TEST - len(question_ids),
                exclude_ids=set(question_ids),
            )
            question_ids.extend(template_ids)

        # 시드 문제가 최소 기준 미달 → AI로 추가 생성 후 DB 저장
        if len(question_ids) < MIN_QUESTIONS_PER_DAILY_TEST and grade:
            needed = MIN_QUESTIONS_PER_DAILY_TEST - len(question_ids)
            ai_ids = await self._generate_ai_questions(
                student_id, category, grade, needed
            )
            question_ids.extend(ai_ids)

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
        test_id = f"daily-{student_id}-{date}-{category}"

        # 기존 테스트가 있으면 업데이트 (0문제 재생성 시)
        existing_test = await self.db.get(Test, test_id)
        if existing_test:
            existing_test.question_ids = question_ids
            existing_test.question_count = question_count
            existing_test.concept_ids = concept_ids
            await self.db.flush()
            return existing_test

        test = Test(
            id=test_id,
            title=f"오늘의 {label} ({date})",
            description=f"{date} 일일 {label} 테스트",
            grade=grade or "",
            category=category,
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
        grade: str | None,
        count: int = QUESTIONS_PER_DAILY_TEST,
    ) -> list[str]:
        """학생 맞춤형 문제 선택 알고리즘.

        전략 (10문제 기준):
          0. 오답 복습 (next_review_date ≤ 오늘) — 2문제
          1. 약점 보강 (mastery < 60%) — 3~4문제 (난이도 제한 없음)
          2. 나머지 일반 문제 — 4~5문제
        약점 문제는 난이도 범위를 풀어서 다양한 난이도로 복습.
        중복 제외: 최근 3일 출제 (복습·약점은 제외 안함)
        """
        mastery_map = await self._get_mastery_map(student_id)
        avg_mastery = (
            sum(mastery_map.values()) / len(mastery_map)
            if mastery_map else 0.0
        )
        diff_min, diff_max = self._mastery_to_difficulty_range(avg_mastery)

        recently_used = await self._get_recently_used_questions(student_id, category, days=3)

        # 해금된 개념
        available_concept_ids: list[str] = []
        if grade:
            available_concept_ids = await self._get_student_available_concept_ids(student_id, grade)

        # 약점 개념 ID (mastery < 60%)
        weak_concept_ids = [
            cid for cid in available_concept_ids
            if mastery_map.get(cid, 0) < 60
        ]

        # ── 1) 약점 보강 문제 (난이도 제한 없이 넓게 조회) ──
        weak_pool: list[Question] = []
        if weak_concept_ids:
            weak_query = select(Question).where(
                Question.is_active == True,  # noqa: E712
                Question.concept_id.in_(weak_concept_ids),
            )
            weak_query = self._build_category_filter(weak_query, category)
            weak_pool = list((await self.db.scalars(weak_query)).all())

        # ── 2) 일반 문제 풀 (약점 개념 제외, 기존 난이도 범위) ──
        normal_concept_ids = [
            cid for cid in available_concept_ids
            if cid not in weak_concept_ids
        ] if weak_concept_ids else available_concept_ids

        base_query = select(Question).where(
            Question.is_active == True,  # noqa: E712
            Question.difficulty >= diff_min,
            Question.difficulty <= diff_max,
            ~Question.id.in_(recently_used) if recently_used else True,
        )
        base_query = self._build_category_filter(base_query, category)
        if normal_concept_ids:
            base_query = base_query.where(
                Question.concept_id.in_(normal_concept_ids)
            )
        elif available_concept_ids:
            # 모든 개념이 약점이면 전체에서 출제 (약점 슬롯 + 일반 슬롯 모두 약점)
            base_query = base_query.where(
                Question.concept_id.in_(available_concept_ids)
            )

        all_questions = list((await self.db.scalars(base_query)).all())

        if not all_questions and not weak_pool:
            return await self._select_questions_fallback(
                student_id, category, grade, count, recently_used
            )

        # ── 3) 오답 복습 (스케줄 기반) ──
        review_svc = ReviewService(self.db)
        review_question_ids = await review_svc.get_due_question_ids(student_id, limit=count)
        all_question_ids = {q.id for q in all_questions} | {q.id for q in weak_pool}
        review_ids_filtered = [qid for qid in review_question_ids if qid in all_question_ids]

        # ── 4) 슬롯 배분 ──
        review_slot = min(2, len(review_ids_filtered))                  # 최대 2문제
        weak_target = min(count * 4 // 10, max(3, len(weak_pool)))      # 3~4문제
        weak_slot = min(weak_target, len(weak_pool))
        normal_slot = count - review_slot - weak_slot                   # 나머지

        selected: list[str] = []

        # 복습
        if review_ids_filtered:
            selected += review_ids_filtered[:review_slot]

        # 약점 보강 (최근 사용 제외 안 함 — 잊지 않도록 반복)
        selected_set = set(selected)
        if weak_pool:
            weak_candidates = [q.id for q in weak_pool if q.id not in selected_set]
            pick = min(weak_slot, len(weak_candidates))
            if pick > 0:
                selected += random.sample(weak_candidates, pick)
                selected_set = set(selected)

        # 일반 문제
        normal_candidates = [q.id for q in all_questions if q.id not in selected_set]
        pick = min(normal_slot, len(normal_candidates))
        if pick > 0:
            selected += random.sample(normal_candidates, pick)

        # 부족하면 남은 풀에서 채움
        if len(selected) < count:
            remaining = count - len(selected)
            selected_set = set(selected)
            leftover = [q.id for q in (all_questions + weak_pool) if q.id not in selected_set]
            # 중복 제거
            leftover = list(dict.fromkeys(leftover))
            selected += random.sample(leftover, min(remaining, len(leftover)))

        random.shuffle(selected)
        return selected

    # fill_in_blank 부적절 패턴 (AI 불량 문제 DB 레벨 제외)
    _FB_BAD_PATTERNS = ["(가)", "(나)", "고르시오", "선택하시오", "옳은 것", "옳지 않은"]

    def _build_category_filter(self, query, category: str):
        """카테고리 필터 적용 (fill_in_blank 중복 방지 포함)."""
        if category == "fill_in_blank":
            query = query.where(Question.question_type == QuestionType.FILL_IN_BLANK)
            for pat in self._FB_BAD_PATTERNS:
                query = query.where(~Question.content.contains(pat))
            return query
        elif category == "concept":
            return query.where(
                Question.category == QuestionCategory.CONCEPT,
                Question.question_type != QuestionType.FILL_IN_BLANK,
            )
        elif category == "computation":
            return query.where(
                Question.category == QuestionCategory.COMPUTATION,
                Question.question_type != QuestionType.FILL_IN_BLANK,
            )
        return query

    async def _select_questions_fallback(
        self,
        student_id: str,
        category: str,
        grade: str | None,
        count: int,
        recently_used: list[str],
    ) -> list[str]:
        """난이도 제한 없이 문제 선택 (폴백).

        해금된 단원만 출제 (잠긴 단원 문제 절대 포함 안 함):
        1) 해금 개념 + 중복 제외
        2) 해금 개념 + 중복 허용
        부족하면 있는 만큼만 반환 (잠긴 단원 확장 안 함).
        """

        # 해금된 개념 ID
        available_concept_ids: list[str] = []
        if grade:
            available_concept_ids = await self._get_student_available_concept_ids(student_id, grade)

        # 1단계: 해금 개념, 중복 제외
        q1 = self._build_category_filter(
            select(Question.id).where(Question.is_active == True), category  # noqa: E712
        )
        if available_concept_ids:
            q1 = q1.where(Question.concept_id.in_(available_concept_ids))
        if recently_used:
            q1 = q1.where(~Question.id.in_(recently_used))

        all_ids = list((await self.db.scalars(q1)).all())
        if len(all_ids) >= count:
            return random.sample(all_ids, count)
        if all_ids:
            return random.sample(all_ids, len(all_ids))

        # 2단계: 해금 개념, 중복 허용
        q2 = self._build_category_filter(
            select(Question.id).where(Question.is_active == True), category  # noqa: E712
        )
        if available_concept_ids:
            q2 = q2.where(Question.concept_id.in_(available_concept_ids))

        all_ids = list((await self.db.scalars(q2)).all())
        if all_ids:
            return random.sample(all_ids, min(count, len(all_ids)))

        # 해금 개념에 해당 카테고리 문제가 전혀 없는 경우 → 빈 목록
        return []

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

    async def _get_student_available_concept_ids(self, student_id: str, grade: str | None) -> list[str]:
        """학생이 해금한 개념 ID만 반환 (ChapterProgress.is_unlocked + ConceptMastery.is_unlocked 기반)."""
        from app.models.chapter_progress import ChapterProgress

        # 1. 해금된 챕터의 개념 ID 목록 수집
        unlocked_ch_stmt = (
            select(Chapter)
            .join(ChapterProgress, Chapter.id == ChapterProgress.chapter_id)
            .where(
                ChapterProgress.student_id == student_id,
                ChapterProgress.is_unlocked == True,  # noqa: E712
                Chapter.grade == grade,
            )
        )
        unlocked_chapters = list((await self.db.scalars(unlocked_ch_stmt)).all())
        chapter_concept_ids = set()
        for ch in unlocked_chapters:
            chapter_concept_ids.update(ch.concept_ids or [])

        if not chapter_concept_ids:
            # 폴백: 해금된 챕터가 없으면 첫 챕터 첫 개념 자동 해금
            from app.services.mastery_service import MasteryService
            first_chapter_stmt = (
                select(Chapter)
                .where(Chapter.grade == grade, Chapter.semester == 1, Chapter.chapter_number == 1)
            )
            first_chapter = await self.db.scalar(first_chapter_stmt)
            if not first_chapter or not first_chapter.concept_ids:
                return []

            mastery_service = MasteryService(self.db)
            first_concept_id = first_chapter.concept_ids[0]
            await mastery_service.ensure_first_concept_unlocked(student_id, first_chapter.id)
            await self.db.flush()
            return [first_concept_id]

        # 2. 해금된 개념 중 해금된 챕터에 속한 것만 반환
        stmt = (
            select(ConceptMastery.concept_id)
            .join(Concept, ConceptMastery.concept_id == Concept.id)
            .where(
                ConceptMastery.student_id == student_id,
                ConceptMastery.is_unlocked == True,  # noqa: E712
                Concept.grade == grade,
                ConceptMastery.concept_id.in_(chapter_concept_ids),
            )
        )
        return list((await self.db.scalars(stmt)).all())

    async def _get_mastery_map(self, student_id: str) -> dict[str, int]:
        """학생의 개념별 숙련도 맵."""
        stmt = select(
            ConceptMastery.concept_id,
            ConceptMastery.mastery_percentage,
        ).where(ConceptMastery.student_id == student_id)
        rows = (await self.db.execute(stmt)).all()
        return {row[0]: row[1] for row in rows}

    @staticmethod
    def _mastery_to_difficulty_range(avg_mastery: float) -> tuple[int, int]:
        """숙련도 → 난이도 범위 (좁은 범위, 학생 수준 밀착).

        숙련도 0~100% → 난이도 1~9 선형 매핑 후 ±1 범위.
        예: 50% → center 5, range 4~6
            80% → center 7, range 6~8
            0%  → center 1, range 1~2
        """
        center = max(1, min(9, round(1 + avg_mastery * 8 / 100)))
        diff_min = max(1, center - 1)
        diff_max = min(10, center + 1)
        return diff_min, diff_max

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

    # 학년 → ID 접두사 매핑
    GRADE_PREFIX_MAP = {
        "elementary_3": "e3", "elementary_4": "e4",
        "elementary_5": "e5", "elementary_6": "e6",
        "middle_1": "m1", "middle_2": "m2", "middle_3": "m3",
        "high_1": "h1",
    }

    # 카테고리 → ID 접두사 매핑
    CATEGORY_PREFIX_MAP = {
        "concept": "conc",
        "computation": "comp",
        "fill_in_blank": "fb",
    }

    async def _get_next_ai_seq(self, grade_prefix: str, cat_prefix: str) -> int:
        """AI 문제의 다음 시퀀스 번호를 조회.

        기존 시드(m1-1-01-01-lv02-cc-001~) + AI(ai-m1-comp-001~) 모두 확인하여
        가장 큰 번호 + 1을 반환.
        """
        ai_pattern = f"ai-{grade_prefix}-{cat_prefix}-%"
        seed_pattern = f"{grade_prefix}-{cat_prefix}-%"

        # AI 문제 최대 시퀀스
        ai_stmt = (
            select(Question.id)
            .where(Question.id.like(ai_pattern))
            .order_by(Question.id.desc())
            .limit(1)
        )
        last_ai_id = await self.db.scalar(ai_stmt)

        # 시드 문제 최대 시퀀스
        seed_stmt = (
            select(Question.id)
            .where(Question.id.like(seed_pattern))
            .order_by(Question.id.desc())
            .limit(1)
        )
        last_seed_id = await self.db.scalar(seed_stmt)

        max_seq = 0
        for qid in [last_ai_id, last_seed_id]:
            if qid:
                # "ai-m1-comp-042" → "042" → 42
                # "m1-1-04-03-lv09-co-001" → "001" → 1
                try:
                    seq_str = qid.rsplit("-", 1)[-1]
                    max_seq = max(max_seq, int(seq_str))
                except (ValueError, IndexError):
                    pass

        return max_seq + 1

    async def _generate_template_questions(
        self,
        student_id: str,
        grade: str,
        count: int,
        exclude_ids: set[str] | None = None,
    ) -> list[str]:
        """템플릿으로 연산 문제 생성 -> DB 저장 -> ID 반환.

        숫자를 랜덤으로 바꿔 무한 변형 생성. AI 비용 0원.
        """
        generator = TemplateGenerator()
        if not generator.get_available_concepts():
            return []

        available_concept_ids = await self._get_student_available_concept_ids(
            student_id, grade
        )
        if not available_concept_ids:
            return []

        # 기존 DB의 tpl- ID 조회 (중복 방지)
        existing_tpl_stmt = select(Question.id).where(
            Question.id.like("tpl-%"),
            Question.concept_id.in_(available_concept_ids),
        )
        existing_tpl_ids = set(
            (await self.db.scalars(existing_tpl_stmt)).all()
        )
        all_exclude = (exclude_ids or set()) | existing_tpl_ids

        variants = generator.generate_for_grade(
            grade, count,
            available_concept_ids=available_concept_ids,
            exclude_ids=all_exclude,
        )

        generated_ids = []
        for v in variants:
            # 이미 DB에 있으면 재사용
            existing = await self.db.get(Question, v["id"])
            if existing:
                generated_ids.append(v["id"])
                continue

            q = Question(
                id=v["id"],
                concept_id=v["concept_id"],
                category=v["category"],
                part=v["part"],
                question_type=v["question_type"],
                difficulty=v["difficulty"],
                content=v["content"],
                options=v.get("options"),
                correct_answer=v["correct_answer"],
                explanation=v.get("explanation", ""),
                points=v.get("points", 10),
                blank_config=v.get("blank_config"),
                is_active=True,
            )
            self.db.add(q)
            generated_ids.append(v["id"])

        if generated_ids:
            try:
                await self.db.flush()
                logger.info(
                    f"[Template] {grade} 연산 문제 {len(generated_ids)}개 생성 "
                    f"(학생: {student_id})"
                )
            except IntegrityError:
                await self.db.rollback()
                logger.warning("[Template] DB 저장 중 중복 ID 충돌, 스킵")
                return []

        return generated_ids

    async def _generate_ai_questions(
        self,
        student_id: str,
        category: str,
        grade: str | None,
        count: int,
    ) -> list[str]:
        """AI로 문제를 생성하여 DB에 저장하고 ID 목록을 반환.

        생성된 문제는 DB에 영구 저장되어 다음에 시드 문제처럼 재활용됩니다.
        문항 ID: ai-{grade}-{category}-{seq} (예: ai-m1-fb-025, ai-m1-cc-037)
        기존 문제 content를 AI에게 전달하여 중복 생성을 방지합니다.
        """
        # 학년/카테고리 접두사 계산
        grade_str = grade.value if hasattr(grade, "value") else str(grade)
        grade_prefix = self.GRADE_PREFIX_MAP.get(grade_str, "xx")
        cat_prefix = self.CATEGORY_PREFIX_MAP.get(category, category[:4])
        id_prefix = f"ai-{grade_prefix}-{cat_prefix}"

        # 다음 시퀀스 번호 조회
        next_seq = await self._get_next_ai_seq(grade_prefix, cat_prefix)

        # 해금된 개념 조회
        available_concept_ids = await self._get_student_available_concept_ids(
            student_id, grade
        )
        if not available_concept_ids:
            return []

        # 개념 정보 조회
        concept_stmt = select(Concept).where(
            Concept.id.in_(available_concept_ids)
        )
        concepts = list((await self.db.scalars(concept_stmt)).all())
        if not concepts:
            return []

        # question_type 결정
        if category == "fill_in_blank":
            q_type = "fill_in_blank"
        else:
            q_type = "multiple_choice"

        # 기존 문제 content 수집 (중복 방지용)
        existing_stmt = select(Question.content).where(
            Question.concept_id.in_(available_concept_ids),
            Question.is_active == True,  # noqa: E712
        )
        existing_contents = list((await self.db.scalars(existing_stmt)).all())
        existing_set = set(c.strip() for c in existing_contents if c)

        # 개념별로 분배하여 생성 (한 개념에 몰리지 않게)
        ai_service = AIService()
        generated_ids: list[str] = []
        remaining = count
        current_seq = next_seq

        random.shuffle(concepts)
        for concept in concepts:
            if remaining <= 0:
                break

            # 이 개념에 대해 생성할 수 (중복 제거 마진을 위해 +2)
            batch = min(remaining + 2, max(3, count // len(concepts) + 2))

            # AI 문제 생성 (기존 문제 전달 + 시드 패턴 ID) - 10초 타임아웃
            try:
                result = await asyncio.wait_for(
                    ai_service.generate_questions(
                        concept_name=concept.name,
                        concept_id=concept.id,
                        grade=grade_str,
                        category=category if category != "fill_in_blank" else concept.category.value,
                        part=concept.part.value if hasattr(concept.part, "value") else str(concept.part),
                        question_type=q_type,
                        count=batch,
                        # [Phase 6] 학년군별 차등 비율 적용 (Phase 6 보완)
                        concept_method=self._pick_random_concept_method(grade_str) if category == "concept" else None,
                        existing_contents=list(existing_set)[:20],
                        id_prefix=id_prefix,
                        start_seq=current_seq,
                    ),
                    timeout=10.0,
                )
            except asyncio.TimeoutError:
                logger.warning("AI question generation timed out for concept %s", concept.name)
                result = None

            if not result:
                continue

            # DB에 저장 (영구 저장 → 다음에 시드처럼 재활용)
            for q_dict in result:
                if remaining <= 0:
                    break

                # 중복 체크: content가 기존과 동일하면 건너뛰기
                content = q_dict.get("content", "").strip()
                if content in existing_set:
                    logger.debug("Skipping duplicate AI question: %s", content[:50])
                    current_seq += 1
                    continue

                try:
                    q = Question(
                        id=q_dict["id"],
                        concept_id=q_dict["concept_id"],
                        category=q_dict["category"],
                        part=q_dict["part"],
                        question_type=q_dict["question_type"],
                        difficulty=q_dict["difficulty"],
                        content=content,
                        options=q_dict.get("options"),
                        correct_answer=q_dict["correct_answer"],
                        explanation=q_dict.get("explanation", ""),
                        points=q_dict.get("points", 10),
                        blank_config=q_dict.get("blank_config"),
                        concept_method=q_dict.get("concept_method"), # DB 저장
                        is_active=True,
                    )
                    self.db.add(q)
                    generated_ids.append(q.id)
                    existing_set.add(content)
                    remaining -= 1
                    current_seq += 1
                except Exception:
                    logger.warning("Failed to save AI question: %s", q_dict.get("id"))
                    current_seq += 1
                    continue

        if generated_ids:
            await self.db.flush()
            self._ai_generated_count += len(generated_ids)
            logger.info(
                "AI generated %d questions [%s-%03d~%03d] for student %s (saved to DB)",
                len(generated_ids), id_prefix, next_seq, current_seq - 1,
                student_id[:8],
            )

        return generated_ids

    def _pick_random_concept_method(self, grade: str) -> str:
        """학년군별 차등 비율이 적용된 개념 문항 생성 방식 선택 (Phase 6 보완)."""
        r = random.random()
        
        # 기본 비율 (Default)
        # Standard: 40%, Type A: 20%, Type B: 20%, Type C: 20%
        
        # 1. 1-2학년군: 시각적 이해(Type C) 우선
        if grade in ["elementary_1", "elementary_2"]:
            if r < 0.4: return ConceptMethod.STANDARD
            if r < 0.5: return ConceptMethod.GRADUAL_FADING  # 10%
            if r < 0.7: return ConceptMethod.ERROR_ANALYSIS # 20%
            return ConceptMethod.VISUAL_DECODING            # 30%
            
        # 2. 3-4학년군: 오개념 분석(Type B) 우선
        elif grade in ["elementary_3", "elementary_4"]:
            if r < 0.4: return ConceptMethod.STANDARD
            if r < 0.5: return ConceptMethod.GRADUAL_FADING  # 10%
            if r < 0.8: return ConceptMethod.ERROR_ANALYSIS # 30%
            return ConceptMethod.VISUAL_DECODING            # 20%
            
        # 3. 5-6학년 및 중등: 논리/빈칸(Type A) 우선
        else:
            if r < 0.4: return ConceptMethod.STANDARD
            if r < 0.7: return ConceptMethod.GRADUAL_FADING  # 30%
            if r < 0.85: return ConceptMethod.ERROR_ANALYSIS # 15%
            return ConceptMethod.VISUAL_DECODING            # 15%
