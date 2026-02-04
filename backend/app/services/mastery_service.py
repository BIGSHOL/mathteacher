"""개념 숙련도 관리 서비스."""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.concept_mastery import ConceptMastery
from app.models.concept import Concept
from app.models.answer_log import AnswerLog
from app.models.test_attempt import TestAttempt

MASTERY_THRESHOLD = 90  # 90% 이상이면 마스터


class MasteryService:
    """개념 숙련도 추적 및 관리."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_mastery(
        self, student_id: str, concept_id: str
    ) -> ConceptMastery:
        """개념 숙련도 조회 또는 생성."""
        stmt = select(ConceptMastery).where(
            ConceptMastery.student_id == student_id,
            ConceptMastery.concept_id == concept_id,
        )
        mastery = await self.db.scalar(stmt)

        if not mastery:
            mastery = ConceptMastery(
                student_id=student_id,
                concept_id=concept_id,
                is_unlocked=False,  # 기본적으로 잠김
            )
            self.db.add(mastery)
            await self.db.flush()

        return mastery

    async def unlock_concept(self, student_id: str, concept_id: str) -> bool:
        """개념 잠금 해제."""
        mastery = await self.get_or_create_mastery(student_id, concept_id)

        if not mastery.is_unlocked:
            mastery.is_unlocked = True
            mastery.unlocked_at = datetime.now(timezone.utc)
            await self.db.commit()
            return True

        return False

    async def update_mastery_from_attempt(
        self, student_id: str, attempt_id: str
    ) -> dict[str, int]:
        """테스트 시도 결과로 개념 숙련도 업데이트.

        Returns:
            dict: 업데이트된 개념별 숙련도 {concept_id: mastery_percentage}
        """
        # 시도 조회
        attempt = await self.db.get(TestAttempt, attempt_id)
        if not attempt or not attempt.completed_at:
            return {}

        # 시도의 모든 답안 조회
        stmt = (
            select(AnswerLog)
            .where(AnswerLog.attempt_id == attempt_id)
            .order_by(AnswerLog.created_at)
        )
        answer_logs = list((await self.db.scalars(stmt)).all())

        if not answer_logs:
            return {}

        # 개념별로 그룹화
        concept_stats: dict[str, dict] = {}

        for log in answer_logs:
            if not log.question or not log.question.concept_id:
                continue

            concept_id = log.question.concept_id

            if concept_id not in concept_stats:
                concept_stats[concept_id] = {
                    "total": 0,
                    "correct": 0,
                    "points_earned": 0,
                    "points_total": 0,
                }

            concept_stats[concept_id]["total"] += 1
            concept_stats[concept_id]["points_total"] += log.question.points

            if log.is_correct:
                concept_stats[concept_id]["correct"] += 1
                concept_stats[concept_id]["points_earned"] += log.points_earned

        # 각 개념의 숙련도 업데이트
        updated_masteries = {}

        for concept_id, stats in concept_stats.items():
            mastery = await self.get_or_create_mastery(student_id, concept_id)

            # 누적 통계 업데이트
            mastery.total_attempts += stats["total"]
            mastery.correct_count += stats["correct"]

            # 평균 점수 계산 (가중 평균)
            total_weight = mastery.total_attempts
            old_score = mastery.average_score * (total_weight - stats["total"])
            new_score = (
                stats["points_earned"] / stats["points_total"] * 100
                if stats["points_total"] > 0
                else 0
            )
            mastery.average_score = (old_score + new_score * stats["total"]) / total_weight

            # 숙련도 계산: 정답률 70% + 평균점수 30%
            accuracy = mastery.correct_count / mastery.total_attempts * 100
            mastery.mastery_percentage = int(accuracy * 0.7 + mastery.average_score * 0.3)

            # 마스터리 달성 체크
            if mastery.mastery_percentage >= MASTERY_THRESHOLD and not mastery.is_mastered:
                mastery.is_mastered = True
                mastery.mastered_at = datetime.now(timezone.utc)

            mastery.last_practiced = datetime.now(timezone.utc)

            updated_masteries[concept_id] = mastery.mastery_percentage

        await self.db.commit()
        return updated_masteries

    async def get_student_masteries(
        self, student_id: str, grade: str | None = None
    ) -> list[dict]:
        """학생의 개념별 숙련도 조회."""
        stmt = select(ConceptMastery).where(ConceptMastery.student_id == student_id)

        if grade:
            # Concept와 조인하여 grade 필터링
            stmt = stmt.join(Concept).where(Concept.grade == grade)

        masteries = list((await self.db.scalars(stmt)).all())

        # N+1 쿼리 방지: 모든 concept을 한 번에 조회
        concept_ids = [m.concept_id for m in masteries]
        if concept_ids:
            concepts = list((await self.db.scalars(
                select(Concept).where(Concept.id.in_(concept_ids))
            )).all())
            concept_map = {c.id: c for c in concepts}
        else:
            concept_map = {}

        result = []
        for m in masteries:
            concept = concept_map.get(m.concept_id)
            result.append({
                "concept_id": m.concept_id,
                "concept_name": concept.name if concept else "Unknown",
                "mastery_percentage": m.mastery_percentage,
                "is_mastered": m.is_mastered,
                "is_unlocked": m.is_unlocked,
                "total_attempts": m.total_attempts,
                "correct_count": m.correct_count,
                "average_score": round(m.average_score, 1),
                "last_practiced": m.last_practiced,
            })

        return result

    async def check_prerequisites_met(
        self, student_id: str, concept_id: str
    ) -> tuple[bool, list[str]]:
        """선수 개념이 모두 마스터되었는지 확인.

        Returns:
            tuple: (모두 완료 여부, 미완료 개념 ID 리스트)
        """
        concept = await self.db.get(Concept, concept_id)
        if not concept or not concept.prerequisites:
            return True, []

        unmet_prerequisites = []

        for prereq in concept.prerequisites:
            stmt = select(ConceptMastery).where(
                ConceptMastery.student_id == student_id,
                ConceptMastery.concept_id == prereq.id,
            )
            mastery = await self.db.scalar(stmt)

            # 마스터리가 없거나 90% 미만이면 선수조건 미달
            if not mastery or mastery.mastery_percentage < MASTERY_THRESHOLD:
                unmet_prerequisites.append(prereq.id)

        return len(unmet_prerequisites) == 0, unmet_prerequisites

    async def auto_unlock_next_concepts(self, student_id: str, concept_id: str) -> list[str]:
        """개념 마스터 시 다음 개념 자동 해제.

        Returns:
            list: 새로 해제된 개념 ID 리스트
        """
        # 현재 개념이 마스터되었는지 확인
        stmt = select(ConceptMastery).where(
            ConceptMastery.student_id == student_id,
            ConceptMastery.concept_id == concept_id,
        )
        mastery = await self.db.scalar(stmt)

        if not mastery or not mastery.is_mastered:
            return []

        # 이 개념을 선수조건으로 하는 다음 개념들 찾기
        concept = await self.db.get(Concept, concept_id)
        if not concept:
            return []

        unlocked = []

        # dependents: 이 개념을 선수로 요구하는 개념들
        for next_concept in concept.dependents:
            # 선수조건 모두 충족되었는지 확인
            all_met, _ = await self.check_prerequisites_met(student_id, next_concept.id)

            if all_met:
                # 자동 해제
                if await self.unlock_concept(student_id, next_concept.id):
                    unlocked.append(next_concept.id)

        return unlocked
