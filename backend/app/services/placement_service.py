"""진단 평가 서비스."""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.test_attempt import TestAttempt
from app.models.answer_log import AnswerLog
from app.models.question import Question
from app.models.chapter import Chapter
from app.models.user import User
from app.services.mastery_service import MasteryService
from app.services.chapter_service import ChapterService


class PlacementService:
    """진단 평가 및 배치 서비스."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.mastery_service = MasteryService(db)
        self.chapter_service = ChapterService(db)

    async def analyze_placement_result(self, attempt_id: str) -> dict:
        """진단 평가 결과 분석 및 배치 결정.

        Returns:
            dict: {
                "starting_chapter_id": str,
                "starting_chapter_name": str,
                "recommended_level": int,
                "chapter_scores": dict,  # 단원별 점수
                "unlocked_chapters": list,  # 해제할 단원 목록
                "mastered_concepts": list,  # 마스터한 개념 목록
                "weak_areas": list,  # 취약 영역
            }
        """
        attempt = await self.db.get(TestAttempt, attempt_id)
        if not attempt or not attempt.completed_at:
            return {}

        # 모든 답안 로그 조회
        stmt = (
            select(AnswerLog)
            .where(AnswerLog.attempt_id == attempt_id)
            .order_by(AnswerLog.created_at)
        )
        answer_logs = list((await self.db.scalars(stmt)).all())

        if not answer_logs:
            return {}

        # 단원별 점수 계산 (문제의 concept_id를 통해 역추적)
        chapter_scores = {}  # {chapter_id: {"correct": 0, "total": 0, "percentage": 0}}
        concept_to_chapter = {}  # 캐시: concept_id -> chapter_id

        for log in answer_logs:
            if not log.question or not log.question.concept_id:
                continue

            concept_id = log.question.concept_id

            # 이 개념이 속한 단원 찾기 (캐시 활용)
            if concept_id not in concept_to_chapter:
                chapter = await self._find_chapter_by_concept(concept_id)
                concept_to_chapter[concept_id] = chapter.id if chapter else None

            chapter_id = concept_to_chapter[concept_id]
            if not chapter_id:
                continue

            if chapter_id not in chapter_scores:
                chapter_scores[chapter_id] = {"correct": 0, "total": 0, "percentage": 0}

            chapter_scores[chapter_id]["total"] += 1
            if log.is_correct:
                chapter_scores[chapter_id]["correct"] += 1

        # 각 단원 점수 비율 계산
        for chapter_id, scores in chapter_scores.items():
            if scores["total"] > 0:
                scores["percentage"] = int(scores["correct"] / scores["total"] * 100)

        # 배치 결정 로직
        placement_result = await self._determine_placement(chapter_scores, attempt.score)

        return placement_result

    async def _find_chapter_by_concept(self, concept_id: str) -> Chapter | None:
        """개념 ID로 해당 단원 찾기."""
        stmt = select(Chapter).where(Chapter.concept_ids.contains([concept_id]))
        return await self.db.scalar(stmt)

    async def _determine_placement(
        self, chapter_scores: dict[str, dict], overall_score: int
    ) -> dict:
        """배치 결정 알고리즘.

        기준:
        - 70점 이상: 해당 단원 마스터로 간주
        - 40-69점: 해당 단원부터 시작
        - 40점 미만: 이전 단원 필요
        """
        # 모든 단원을 점수순으로 정렬
        sorted_chapters = sorted(
            chapter_scores.items(), key=lambda x: x[1]["percentage"], reverse=True
        )

        mastered_chapters = []  # 70점 이상
        moderate_chapters = []  # 40-69점
        weak_chapters = []  # 40점 미만

        for chapter_id, scores in sorted_chapters:
            percentage = scores["percentage"]
            if percentage >= 70:
                mastered_chapters.append(chapter_id)
            elif percentage >= 40:
                moderate_chapters.append(chapter_id)
            else:
                weak_chapters.append(chapter_id)

        # 시작 단원 결정
        if moderate_chapters:
            # 40-69점 구간 중 가장 높은 점수의 단원부터 시작
            starting_chapter_id = moderate_chapters[0]
        elif weak_chapters:
            # 모두 40점 미만이면 가장 낮은 단원부터
            starting_chapter_id = weak_chapters[-1]
        else:
            # 모두 70점 이상이면 마지막 마스터 단원 다음
            starting_chapter_id = mastered_chapters[-1] if mastered_chapters else None

        # 시작 단원 정보 조회
        starting_chapter = None
        if starting_chapter_id:
            starting_chapter = await self.db.get(Chapter, starting_chapter_id)

        # 추천 레벨 계산 (전체 점수 기반)
        recommended_level = self._calculate_level(overall_score)

        return {
            "starting_chapter_id": starting_chapter_id,
            "starting_chapter_name": starting_chapter.name if starting_chapter else "중1-1단원",
            "starting_chapter_number": starting_chapter.chapter_number if starting_chapter else 1,
            "recommended_level": recommended_level,
            "chapter_scores": chapter_scores,
            "unlocked_chapters": mastered_chapters,
            "weak_areas": weak_chapters,
            "mastered_count": len(mastered_chapters),
            "moderate_count": len(moderate_chapters),
            "weak_count": len(weak_chapters),
        }

    def _calculate_level(self, score: int) -> int:
        """전체 점수로 레벨 계산."""
        if score >= 90:
            return 5
        elif score >= 70:
            return 3
        elif score >= 50:
            return 2
        else:
            return 1

    async def apply_placement(self, student_id: str, attempt_id: str) -> bool:
        """진단 평가 결과 적용.

        - 사용자 레벨 설정
        - 단원 자동 해제
        - 개념 자동 해제
        """
        result = await self.analyze_placement_result(attempt_id)
        if not result:
            return False

        user = await self.db.get(User, student_id)
        if not user:
            return False

        # 1. 사용자 정보 업데이트
        user.has_completed_placement = True
        user.placement_test_id = attempt_id
        user.placement_result = result
        user.level = result["recommended_level"]

        # 2. 마스터한 단원들 해제 및 완료 처리
        for chapter_id in result["unlocked_chapters"]:
            progress = await self.chapter_service.get_or_create_progress(student_id, chapter_id)
            progress.is_unlocked = True
            progress.is_completed = True  # 마스터로 간주
            progress.overall_progress = 100
            progress.unlocked_at = datetime.now(timezone.utc)
            progress.completed_at = datetime.now(timezone.utc)

        # 3. 시작 단원 해제
        if result["starting_chapter_id"]:
            await self.chapter_service.unlock_chapter(student_id, result["starting_chapter_id"])

        # 4. 개념 해금: 완료된 단원은 전체, 시작 단원은 첫 개념만
        for chapter_id in result["unlocked_chapters"]:
            if not chapter_id:
                continue
            # 완료된(마스터) 단원: 모든 개념 해금
            chapter = await self.db.get(Chapter, chapter_id)
            if chapter and chapter.concept_ids:
                for concept_id in chapter.concept_ids:
                    await self.mastery_service.unlock_concept(student_id, concept_id)

        # 시작 단원: 첫 번째 개념만 해금
        if result["starting_chapter_id"]:
            await self.mastery_service.ensure_first_concept_unlocked(
                student_id, result["starting_chapter_id"]
            )

        await self.db.commit()
        return True

    async def get_placement_test(self) -> dict | None:
        """진단 평가 테스트 조회."""
        from app.models.test import Test

        stmt = select(Test).where(Test.is_placement == True, Test.is_active == True)  # noqa: E712
        placement_test = await self.db.scalar(stmt)

        if not placement_test:
            return None

        return {
            "test_id": placement_test.id,
            "title": placement_test.title,
            "description": placement_test.description,
            "question_count": placement_test.question_count,
            "time_limit_minutes": placement_test.time_limit_minutes,
        }
