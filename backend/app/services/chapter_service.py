"""단원 진행 관리 서비스."""

from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.chapter import Chapter, chapter_prerequisites
from app.models.chapter_progress import ChapterProgress
from app.models.concept_mastery import ConceptMastery
from app.models.test_attempt import TestAttempt
from app.services.mastery_service import MasteryService, MASTERY_THRESHOLD

# 종합 테스트 통과 기준
AUTO_PASS_SCORE = 90  # 90점 이상: 자동 통과
TEACHER_APPROVAL_MIN_SCORE = 60  # 60점 이상: 선생님 승인 가능
# 60점 미만: 통과 불가


class ChapterService:
    """단원 진행 상황 관리."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.mastery_service = MasteryService(db)

    async def get_or_create_progress(
        self, student_id: str, chapter_id: str
    ) -> ChapterProgress:
        """단원 진행 상황 조회 또는 생성."""
        stmt = select(ChapterProgress).where(
            ChapterProgress.student_id == student_id,
            ChapterProgress.chapter_id == chapter_id,
        )
        progress = await self.db.scalar(stmt)

        if not progress:
            progress = ChapterProgress(
                student_id=student_id,
                chapter_id=chapter_id,
                is_unlocked=False,
            )
            self.db.add(progress)
            await self.db.flush()

        return progress

    async def unlock_chapter(self, student_id: str, chapter_id: str) -> bool:
        """단원 잠금 해제."""
        progress = await self.get_or_create_progress(student_id, chapter_id)

        if not progress.is_unlocked:
            progress.is_unlocked = True
            progress.unlocked_at = datetime.now(timezone.utc)
            await self.db.commit()
            return True

        return False

    async def update_chapter_progress(self, student_id: str, chapter_id: str) -> dict:
        """단원 진행률 업데이트 및 완료 여부 체크.

        Returns:
            dict: 진행 상황 정보
        """
        chapter = await self.db.get(Chapter, chapter_id)
        if not chapter:
            return {}

        progress = await self.get_or_create_progress(student_id, chapter_id)

        # 1. 개념별 마스터리 배치 조회 (루프 쿼리 → 단일 쿼리)
        concept_ids = chapter.concept_ids or []
        concepts_mastery = {cid: 0 for cid in concept_ids}
        mastered_count = 0

        if concept_ids:
            stmt = select(ConceptMastery).where(
                ConceptMastery.student_id == student_id,
                ConceptMastery.concept_id.in_(concept_ids),
            )
            masteries = list((await self.db.scalars(stmt)).all())
            for m in masteries:
                concepts_mastery[m.concept_id] = m.mastery_percentage
                if m.mastery_percentage >= MASTERY_THRESHOLD:
                    mastered_count += 1

        progress.concepts_mastery = concepts_mastery

        # 2. 전체 진행률 계산
        if concept_ids:
            total_mastery = sum(concepts_mastery.values())
            progress.overall_progress = int(total_mastery / len(concept_ids))
        else:
            progress.overall_progress = 0

        # 3. 종합 테스트 확인
        if chapter.final_test_id:
            await self._check_final_test(student_id, chapter, progress)

        # 4. 완료 조건 체크
        is_complete = self._check_chapter_completion(chapter, progress, mastered_count, len(concept_ids))

        if is_complete and not progress.is_completed:
            progress.is_completed = True
            progress.completed_at = datetime.now(timezone.utc)

            # 다음 단원 자동 해제
            unlocked = await self._auto_unlock_next_chapters(student_id, chapter_id)

        await self.db.commit()

        return {
            "chapter_id": chapter_id,
            "overall_progress": progress.overall_progress,
            "concepts_mastery": concepts_mastery,
            "mastered_count": mastered_count,
            "total_concepts": len(concept_ids),
            "final_test_passed": progress.final_test_passed,
            "final_test_score": progress.final_test_score,
            "teacher_approved": progress.teacher_approved,
            "is_completed": progress.is_completed,
        }

    async def _check_final_test(
        self, student_id: str, chapter: Chapter, progress: ChapterProgress
    ):
        """종합 테스트 결과 확인 및 업데이트."""
        if not chapter.final_test_id:
            return

        # 최고 점수 시도 조회
        stmt = (
            select(TestAttempt)
            .where(
                TestAttempt.test_id == chapter.final_test_id,
                TestAttempt.student_id == student_id,
                TestAttempt.completed_at.isnot(None),
            )
            .order_by(TestAttempt.score.desc())
            .limit(1)
        )
        best_attempt = await self.db.scalar(stmt)

        if best_attempt:
            progress.final_test_attempted = True
            progress.final_test_attempt_id = best_attempt.id

            # 점수를 100점 만점으로 정규화
            max_score = best_attempt.max_score if best_attempt.max_score else 100
            normalized_score = int((best_attempt.score / max_score) * 100)
            progress.final_test_score = normalized_score

            # 90점 이상: 자동 통과
            if normalized_score >= AUTO_PASS_SCORE:
                progress.final_test_passed = True

    def _check_chapter_completion(
        self, chapter: Chapter, progress: ChapterProgress, mastered_count: int, total_concepts: int
    ) -> bool:
        """단원 완료 조건 체크.

        조건:
        1. 모든 개념 90% 이상 마스터
        2. 종합 테스트 90점 이상 (자동 통과)
           또는 60점 이상 + 선생님 승인
        """
        # 1. 개념 마스터리 체크
        if total_concepts == 0 or mastered_count < total_concepts:
            return False

        # 2. 종합 테스트 체크
        if chapter.final_test_id:
            if not progress.final_test_attempted:
                return False

            # 90점 이상: 자동 통과
            if progress.final_test_score and progress.final_test_score >= AUTO_PASS_SCORE:
                return True

            # 60-89점: 선생님 승인 필요
            if (
                progress.final_test_score
                and progress.final_test_score >= TEACHER_APPROVAL_MIN_SCORE
                and chapter.require_teacher_approval
            ):
                return progress.teacher_approved

            # 60점 미만: 통과 불가
            return False

        # 종합 테스트가 없으면 개념 마스터만으로 완료
        return True

    async def approve_chapter(
        self, student_id: str, chapter_id: str, teacher_id: str, feedback: str | None = None
    ) -> bool:
        """선생님의 단원 완료 승인."""
        progress = await self.get_or_create_progress(student_id, chapter_id)

        # 승인 조건: 60점 이상
        if not progress.final_test_score or progress.final_test_score < TEACHER_APPROVAL_MIN_SCORE:
            return False

        progress.teacher_approved = True
        progress.approved_by = teacher_id
        progress.approved_at = datetime.now(timezone.utc)
        progress.approval_feedback = feedback

        # 완료 조건 재체크
        chapter = await self.db.get(Chapter, chapter_id)
        if chapter:
            concept_count = len(chapter.concept_ids or [])
            mastered_count = sum(
                1 for m in progress.concepts_mastery.values() if m >= MASTERY_THRESHOLD
            )

            if self._check_chapter_completion(chapter, progress, mastered_count, concept_count):
                progress.is_completed = True
                progress.completed_at = datetime.now(timezone.utc)

                # 다음 단원 해제
                await self._auto_unlock_next_chapters(student_id, chapter_id)

        await self.db.commit()
        return True

    async def _auto_unlock_next_chapters(self, student_id: str, chapter_id: str) -> list[str]:
        """단원 완료 시 다음 단원 자동 해제 (명시적 쿼리로 lazy='raise' 대응)."""
        # chapter_prerequisites 테이블에서 이 단원을 선수조건으로 가진 다음 단원 조회
        dependent_stmt = (
            select(Chapter)
            .where(
                Chapter.id.in_(
                    select(chapter_prerequisites.c.chapter_id).where(
                        chapter_prerequisites.c.prerequisite_id == chapter_id
                    )
                )
            )
            .options(selectinload(Chapter.prerequisites))
        )
        next_chapters = list((await self.db.scalars(dependent_stmt)).all())
        if not next_chapters:
            return []

        unlocked = []

        # 각 다음 단원의 선수조건 완료 여부 배치 확인
        all_prereq_ids = set()
        for nc in next_chapters:
            for prereq in nc.prerequisites:
                all_prereq_ids.add(prereq.id)

        # 선수조건 챕터들의 진행 상황을 한번에 조회
        prereq_progress_map: dict[str, bool] = {}
        if all_prereq_ids:
            progress_stmt = select(ChapterProgress).where(
                ChapterProgress.student_id == student_id,
                ChapterProgress.chapter_id.in_(all_prereq_ids),
            )
            prereq_progresses = list((await self.db.scalars(progress_stmt)).all())
            for p in prereq_progresses:
                prereq_progress_map[p.chapter_id] = p.is_completed

        for next_chapter in next_chapters:
            all_met = all(
                prereq_progress_map.get(prereq.id, False)
                for prereq in next_chapter.prerequisites
            )

            if all_met:
                if await self.unlock_chapter(student_id, next_chapter.id):
                    unlocked.append(next_chapter.id)

        return unlocked

    async def get_student_chapters(self, student_id: str, grade: str | None = None) -> list[dict]:
        """학생의 단원별 진행 상황 조회 (배치 쿼리)."""
        stmt = select(Chapter).where(Chapter.is_active == True)  # noqa: E712

        if grade:
            stmt = stmt.where(Chapter.grade == grade)

        stmt = stmt.order_by(Chapter.chapter_number)
        chapters = list((await self.db.scalars(stmt)).all())

        if not chapters:
            return []

        # 모든 챕터의 진행 상황을 한번에 조회
        chapter_ids = [ch.id for ch in chapters]
        progress_stmt = select(ChapterProgress).where(
            ChapterProgress.student_id == student_id,
            ChapterProgress.chapter_id.in_(chapter_ids),
        )
        progresses = list((await self.db.scalars(progress_stmt)).all())
        progress_map = {p.chapter_id: p for p in progresses}

        # 첫 번째 단원은 자동 해금
        first_chapter = chapters[0] if chapters else None
        if first_chapter:
            progress = progress_map.get(first_chapter.id)
            if not progress:
                progress = ChapterProgress(
                    student_id=student_id,
                    chapter_id=first_chapter.id,
                    is_unlocked=True,
                    unlocked_at=datetime.now(timezone.utc),
                )
                self.db.add(progress)
                await self.db.flush()
                progress_map[first_chapter.id] = progress
            elif not progress.is_unlocked:
                progress.is_unlocked = True
                progress.unlocked_at = datetime.now(timezone.utc)
                await self.db.flush()

            await self.db.commit()

        result = []
        for chapter in chapters:
            progress = progress_map.get(chapter.id)

            result.append({
                "chapter_id": chapter.id,
                "chapter_number": chapter.chapter_number,
                "semester": chapter.semester,
                "name": chapter.name,
                "description": chapter.description,
                "is_unlocked": progress.is_unlocked if progress else False,
                "overall_progress": progress.overall_progress if progress else 0,
                "is_completed": progress.is_completed if progress else False,
                "final_test_score": progress.final_test_score if progress else None,
                "teacher_approved": progress.teacher_approved if progress else False,
            })

        return result

    async def get_semester_completion_status(
        self, student_id: str, grade: str
    ) -> dict[int, dict]:
        """학기별 완료 상태 조회.

        Returns:
            {1: {"total": 6, "completed": 3, "is_completed": False},
             2: {"total": 6, "completed": 6, "is_completed": True}}
        """
        # 해당 학년의 모든 단원 조회
        stmt = select(Chapter).where(
            Chapter.is_active == True,  # noqa: E712
            Chapter.grade == grade,
        )
        chapters = list((await self.db.scalars(stmt)).all())

        if not chapters:
            return {}

        # 학기별로 그룹화
        semesters = {}
        for ch in chapters:
            sem = ch.semester
            if sem not in semesters:
                semesters[sem] = []
            semesters[sem].append(ch.id)

        # 각 학기의 완료 상태 확인
        chapter_ids = [ch.id for ch in chapters]
        progress_stmt = select(ChapterProgress).where(
            ChapterProgress.student_id == student_id,
            ChapterProgress.chapter_id.in_(chapter_ids),
        )
        progresses = list((await self.db.scalars(progress_stmt)).all())
        progress_map = {p.chapter_id: p for p in progresses}

        result = {}
        for sem, ch_ids in semesters.items():
            completed = sum(
                1 for ch_id in ch_ids
                if progress_map.get(ch_id) and progress_map[ch_id].is_completed
            )
            result[sem] = {
                "total": len(ch_ids),
                "completed": completed,
                "is_completed": completed == len(ch_ids),
            }

        return result

    async def get_grade_completion_status(
        self, student_id: str, grade: str
    ) -> dict:
        """학년 완료 상태 조회.

        Returns:
            {"total": 12, "completed": 9, "is_completed": False}
        """
        stmt = select(Chapter).where(
            Chapter.is_active == True,  # noqa: E712
            Chapter.grade == grade,
        )
        chapters = list((await self.db.scalars(stmt)).all())

        if not chapters:
            return {"total": 0, "completed": 0, "is_completed": False}

        chapter_ids = [ch.id for ch in chapters]
        progress_stmt = select(ChapterProgress).where(
            ChapterProgress.student_id == student_id,
            ChapterProgress.chapter_id.in_(chapter_ids),
        )
        progresses = list((await self.db.scalars(progress_stmt)).all())

        completed = sum(1 for p in progresses if p.is_completed)

        return {
            "total": len(chapters),
            "completed": completed,
            "is_completed": completed == len(chapters),
        }

    async def get_next_recommendation(self, student_id: str) -> dict | None:
        """다음 학습 추천."""
        # 1. 해제되었지만 완료되지 않은 단원 찾기
        stmt = (
            select(ChapterProgress)
            .where(
                ChapterProgress.student_id == student_id,
                ChapterProgress.is_unlocked == True,  # noqa: E712
                ChapterProgress.is_completed == False,  # noqa: E712
            )
            .order_by(ChapterProgress.overall_progress.desc())
        )
        in_progress = await self.db.scalar(stmt)

        if in_progress:
            chapter = await self.db.get(Chapter, in_progress.chapter_id)
            if chapter:
                return {
                    "type": "continue",
                    "chapter_id": chapter.id,
                    "chapter_name": chapter.name,
                    "progress": in_progress.overall_progress,
                    "message": f"{chapter.name} {in_progress.overall_progress}% 완료! 계속하기",
                }

        # 2. 완료된 단원이 있으면 다음 단원 추천 (명시적 쿼리)
        stmt = (
            select(ChapterProgress)
            .where(
                ChapterProgress.student_id == student_id,
                ChapterProgress.is_completed == True,  # noqa: E712
            )
            .order_by(ChapterProgress.completed_at.desc())
            .limit(1)
        )
        completed = await self.db.scalar(stmt)

        if completed:
            # dependents를 명시적 쿼리로 조회 (lazy='raise' 대응)
            dependent_stmt = select(Chapter).where(
                Chapter.id.in_(
                    select(chapter_prerequisites.c.chapter_id).where(
                        chapter_prerequisites.c.prerequisite_id == completed.chapter_id
                    )
                )
            )
            dependents = list((await self.db.scalars(dependent_stmt)).all())
            if dependents:
                next_chapter = dependents[0]
                return {
                    "type": "next",
                    "chapter_id": next_chapter.id,
                    "chapter_name": next_chapter.name,
                    "message": f"축하합니다! 다음 단원: {next_chapter.name}",
                }

        return None
