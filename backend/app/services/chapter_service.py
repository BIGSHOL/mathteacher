"""단원 진행 관리 서비스."""

from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.chapter import Chapter
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

    def __init__(self, db: Session):
        self.db = db
        self.mastery_service = MasteryService(db)

    def get_or_create_progress(
        self, student_id: str, chapter_id: str
    ) -> ChapterProgress:
        """단원 진행 상황 조회 또는 생성."""
        stmt = select(ChapterProgress).where(
            ChapterProgress.student_id == student_id,
            ChapterProgress.chapter_id == chapter_id,
        )
        progress = self.db.scalar(stmt)

        if not progress:
            progress = ChapterProgress(
                student_id=student_id,
                chapter_id=chapter_id,
                is_unlocked=False,
            )
            self.db.add(progress)
            self.db.flush()

        return progress

    def unlock_chapter(self, student_id: str, chapter_id: str) -> bool:
        """단원 잠금 해제."""
        progress = self.get_or_create_progress(student_id, chapter_id)

        if not progress.is_unlocked:
            progress.is_unlocked = True
            progress.unlocked_at = datetime.now(timezone.utc)
            self.db.commit()
            return True

        return False

    def update_chapter_progress(self, student_id: str, chapter_id: str) -> dict:
        """단원 진행률 업데이트 및 완료 여부 체크.

        Returns:
            dict: 진행 상황 정보
        """
        chapter = self.db.get(Chapter, chapter_id)
        if not chapter:
            return {}

        progress = self.get_or_create_progress(student_id, chapter_id)

        # 1. 개념별 마스터리 수집
        concept_ids = chapter.concept_ids or []
        concepts_mastery = {}
        mastered_count = 0

        for concept_id in concept_ids:
            stmt = select(ConceptMastery).where(
                ConceptMastery.student_id == student_id,
                ConceptMastery.concept_id == concept_id,
            )
            mastery = self.db.scalar(stmt)

            if mastery:
                concepts_mastery[concept_id] = mastery.mastery_percentage
                if mastery.mastery_percentage >= MASTERY_THRESHOLD:
                    mastered_count += 1
            else:
                concepts_mastery[concept_id] = 0

        progress.concepts_mastery = concepts_mastery

        # 2. 전체 진행률 계산
        if concept_ids:
            total_mastery = sum(concepts_mastery.values())
            progress.overall_progress = int(total_mastery / len(concept_ids))
        else:
            progress.overall_progress = 0

        # 3. 종합 테스트 확인
        if chapter.final_test_id:
            self._check_final_test(student_id, chapter, progress)

        # 4. 완료 조건 체크
        is_complete = self._check_chapter_completion(chapter, progress, mastered_count, len(concept_ids))

        if is_complete and not progress.is_completed:
            progress.is_completed = True
            progress.completed_at = datetime.now(timezone.utc)

            # 다음 단원 자동 해제
            unlocked = self._auto_unlock_next_chapters(student_id, chapter_id)

        self.db.commit()

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

    def _check_final_test(
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
        best_attempt = self.db.scalar(stmt)

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

    def approve_chapter(
        self, student_id: str, chapter_id: str, teacher_id: str, feedback: str | None = None
    ) -> bool:
        """선생님의 단원 완료 승인."""
        progress = self.get_or_create_progress(student_id, chapter_id)

        # 승인 조건: 60점 이상
        if not progress.final_test_score or progress.final_test_score < TEACHER_APPROVAL_MIN_SCORE:
            return False

        progress.teacher_approved = True
        progress.approved_by = teacher_id
        progress.approved_at = datetime.now(timezone.utc)
        progress.approval_feedback = feedback

        # 완료 조건 재체크
        chapter = self.db.get(Chapter, chapter_id)
        if chapter:
            concept_count = len(chapter.concept_ids or [])
            mastered_count = sum(
                1 for m in progress.concepts_mastery.values() if m >= MASTERY_THRESHOLD
            )

            if self._check_chapter_completion(chapter, progress, mastered_count, concept_count):
                progress.is_completed = True
                progress.completed_at = datetime.now(timezone.utc)

                # 다음 단원 해제
                self._auto_unlock_next_chapters(student_id, chapter_id)

        self.db.commit()
        return True

    def _auto_unlock_next_chapters(self, student_id: str, chapter_id: str) -> list[str]:
        """단원 완료 시 다음 단원 자동 해제."""
        chapter = self.db.get(Chapter, chapter_id)
        if not chapter:
            return []

        unlocked = []

        # 이 단원을 선수조건으로 하는 다음 단원들
        for next_chapter in chapter.dependents:
            # 선수조건 모두 충족되었는지 확인
            all_met = True

            for prereq in next_chapter.prerequisites:
                stmt = select(ChapterProgress).where(
                    ChapterProgress.student_id == student_id,
                    ChapterProgress.chapter_id == prereq.id,
                )
                prereq_progress = self.db.scalar(stmt)

                if not prereq_progress or not prereq_progress.is_completed:
                    all_met = False
                    break

            if all_met:
                if self.unlock_chapter(student_id, next_chapter.id):
                    unlocked.append(next_chapter.id)

        return unlocked

    def get_student_chapters(self, student_id: str, grade: str | None = None) -> list[dict]:
        """학생의 단원별 진행 상황 조회."""
        stmt = select(Chapter).where(Chapter.is_active == True)  # noqa: E712

        if grade:
            stmt = stmt.where(Chapter.grade == grade)

        stmt = stmt.order_by(Chapter.chapter_number)
        chapters = list(self.db.scalars(stmt).all())

        result = []
        for chapter in chapters:
            stmt = select(ChapterProgress).where(
                ChapterProgress.student_id == student_id,
                ChapterProgress.chapter_id == chapter.id,
            )
            progress = self.db.scalar(stmt)

            result.append({
                "chapter_id": chapter.id,
                "chapter_number": chapter.chapter_number,
                "name": chapter.name,
                "description": chapter.description,
                "is_unlocked": progress.is_unlocked if progress else False,
                "overall_progress": progress.overall_progress if progress else 0,
                "is_completed": progress.is_completed if progress else False,
                "final_test_score": progress.final_test_score if progress else None,
                "teacher_approved": progress.teacher_approved if progress else False,
            })

        return result

    def get_next_recommendation(self, student_id: str) -> dict | None:
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
        in_progress = self.db.scalar(stmt)

        if in_progress:
            chapter = self.db.get(Chapter, in_progress.chapter_id)
            if chapter:
                return {
                    "type": "continue",
                    "chapter_id": chapter.id,
                    "chapter_name": chapter.name,
                    "progress": in_progress.overall_progress,
                    "message": f"{chapter.name} {in_progress.overall_progress}% 완료! 계속하기",
                }

        # 2. 완료된 단원이 있으면 다음 단원 추천
        stmt = (
            select(ChapterProgress)
            .where(
                ChapterProgress.student_id == student_id,
                ChapterProgress.is_completed == True,  # noqa: E712
            )
            .order_by(ChapterProgress.completed_at.desc())
            .limit(1)
        )
        completed = self.db.scalar(stmt)

        if completed:
            chapter = self.db.get(Chapter, completed.chapter_id)
            if chapter and chapter.dependents:
                next_chapter = chapter.dependents[0]
                return {
                    "type": "next",
                    "chapter_id": next_chapter.id,
                    "chapter_name": next_chapter.name,
                    "message": f"축하합니다! 다음 단원: {next_chapter.name} 🔓",
                }

        return None
