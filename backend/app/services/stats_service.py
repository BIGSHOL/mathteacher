"""통계 서비스."""

from datetime import datetime, timedelta, timezone
from collections import defaultdict

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.class_ import Class
from app.models.chapter import Chapter
from app.models.chapter_progress import ChapterProgress
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.answer_log import AnswerLog
from app.models.concept import Concept
from app.schemas.common import Grade, UserRole

# KST (한국 표준시, UTC+9)
KST = timezone(timedelta(hours=9))


def _kst_today():
    """오늘 날짜 (KST 기준)."""
    return datetime.now(KST).date()


def _kst_day_utc_range(day):
    """KST 날짜의 UTC 범위 반환 (start <= ts < end).

    DB에 UTC로 저장된 타임스탬프를 KST 날짜 기준으로 필터링할 때 사용.
    예: KST 2024-01-15 → UTC 2024-01-14 15:00 ~ 2024-01-15 15:00
    """
    start_utc = datetime(day.year, day.month, day.day) - timedelta(hours=9)
    end_utc = start_utc + timedelta(days=1)
    return start_utc, end_utc


def _to_kst_date(dt):
    """UTC datetime을 KST 날짜로 변환."""
    if dt is None:
        return None
    return (dt + timedelta(hours=9)).date()


class StatsService:
    """통계 서비스."""

    def __init__(self, db: AsyncSession | None = None):
        self.db = db

    def calculate_accuracy_rate(self, correct: int, total: int) -> float:
        """정답률 계산."""
        if total == 0:
            return 0.0
        return round((correct / total) * 100, 1)

    def identify_weak_concepts(
        self,
        answer_logs: list[dict],
        threshold: float = 60.0,
    ) -> list[dict]:
        """취약 개념 식별."""
        concept_stats: dict[str, dict] = defaultdict(
            lambda: {"correct": 0, "total": 0}
        )

        for log in answer_logs:
            concept_id = log.get("concept_id")
            if concept_id:
                concept_stats[concept_id]["total"] += 1
                if log.get("is_correct"):
                    concept_stats[concept_id]["correct"] += 1

        weak = []
        for concept_id, stats in concept_stats.items():
            accuracy = self.calculate_accuracy_rate(stats["correct"], stats["total"])
            if accuracy < threshold:
                weak.append({
                    "concept_id": concept_id,
                    "accuracy_rate": accuracy,
                    "total": stats["total"],
                    "correct": stats["correct"],
                })

        return sorted(weak, key=lambda x: x["accuracy_rate"])

    async def get_student_stats(self, student_id: str) -> dict | None:
        """학생 통계 조회."""
        if not self.db:
            raise ValueError("Database session required")

        student = await self.db.get(User, student_id)
        if not student or student.role != UserRole.STUDENT:
            return None

        # 완료된 시도 조회
        attempts_stmt = select(TestAttempt).where(
            TestAttempt.student_id == student_id,
            TestAttempt.completed_at.isnot(None),
        )
        attempts = list((await self.db.scalars(attempts_stmt)).all())

        total_tests = len(attempts)
        total_questions = sum(a.total_count for a in attempts)
        correct_answers = sum(a.correct_count for a in attempts)
        accuracy_rate = self.calculate_accuracy_rate(correct_answers, total_questions)

        # 평균 풀이 시간 - N+1 쿼리 수정: 한 번의 집계 쿼리로 교체
        attempt_ids = [a.id for a in attempts]
        if attempt_ids:
            time_stmt = select(
                func.sum(AnswerLog.time_spent_seconds),
                func.count(),
            ).where(AnswerLog.attempt_id.in_(attempt_ids))
            time_result = (await self.db.execute(time_stmt)).first()
            total_time = time_result[0] or 0
            answer_count = time_result[1] or 0
        else:
            total_time = 0
            answer_count = 0

        avg_time = total_time / answer_count if answer_count > 0 else 0

        # 오늘 푼 문제 수 (KST 기준)
        today = _kst_today()
        today_start, today_end = _kst_day_utc_range(today)
        today_solved_stmt = select(func.count()).select_from(AnswerLog).join(
            TestAttempt, AnswerLog.attempt_id == TestAttempt.id
        ).where(
            TestAttempt.student_id == student_id,
            AnswerLog.created_at >= today_start,
            AnswerLog.created_at < today_end,
        )
        today_solved = await self.db.scalar(today_solved_stmt) or 0

        # 개념별/트랙별/유형별 통계 계산
        from app.models.question import Question

        all_logs_stmt = (
            select(AnswerLog, Question.concept_id, Question.category, Question.question_type)
            .join(Question, AnswerLog.question_id == Question.id)
            .join(TestAttempt, AnswerLog.attempt_id == TestAttempt.id)
            .join(Concept, Question.concept_id == Concept.id)
            .where(TestAttempt.student_id == student_id)
        )
        # 학생 학년에 해당하는 개념만 필터링
        if student and student.grade:
            all_logs_stmt = all_logs_stmt.where(Concept.grade == student.grade)
        all_logs = list((await self.db.execute(all_logs_stmt)).all())

        # 개념별 집계
        concept_agg: dict[str, dict] = defaultdict(
            lambda: {"correct": 0, "total": 0}
        )
        # 트랙별 집계 (평균 시간 포함)
        track_agg: dict[str, dict] = defaultdict(
            lambda: {"correct": 0, "total": 0, "time": 0.0}
        )
        # 문제 유형별 집계 (평균 시간 포함)
        type_agg: dict[str, dict] = defaultdict(
            lambda: {"correct": 0, "total": 0, "time": 0.0}
        )

        for log, concept_id, category, question_type in all_logs:
            concept_agg[concept_id]["total"] += 1
            if log.is_correct:
                concept_agg[concept_id]["correct"] += 1

            # 트랙별 집계
            cat_key = category.value if hasattr(category, "value") else category
            track_agg[cat_key]["total"] += 1
            track_agg[cat_key]["time"] += (log.time_spent_seconds or 0)
            if log.is_correct:
                track_agg[cat_key]["correct"] += 1

            # 문제 유형별 집계
            type_key = question_type.value if hasattr(question_type, "value") else question_type
            type_agg[type_key]["total"] += 1
            type_agg[type_key]["time"] += (log.time_spent_seconds or 0)
            if log.is_correct:
                type_agg[type_key]["correct"] += 1

        # 개념 이름 매핑
        concept_ids = list(concept_agg.keys())
        concept_names: dict[str, str] = {}
        if concept_ids:
            concepts_stmt = select(Concept.id, Concept.name).where(
                Concept.id.in_(concept_ids)
            )
            for cid, cname in (await self.db.execute(concepts_stmt)).all():
                concept_names[cid] = cname

        # 취약 개념 (정답률 < 60%) / 강점 개념 (정답률 >= 80%)
        weak_concepts = []
        strong_concepts = []
        for cid, cstats in concept_agg.items():
            if cstats["total"] < 1:
                continue
            acc = self.calculate_accuracy_rate(cstats["correct"], cstats["total"])
            entry = {
                "concept_id": cid,
                "concept_name": concept_names.get(cid, ""),
                "total_questions": cstats["total"],
                "correct_count": cstats["correct"],
                "accuracy_rate": acc,
            }
            if acc < 60.0:
                weak_concepts.append(entry)
            elif acc >= 80.0:
                strong_concepts.append(entry)

        weak_concepts.sort(key=lambda x: x["accuracy_rate"])
        strong_concepts.sort(key=lambda x: x["accuracy_rate"], reverse=True)

        # 트랙별 통계
        computation_stats = None
        concept_stats = None
        if "computation" in track_agg:
            t = track_agg["computation"]
            avg_time = t["time"] / t["total"] if t["total"] > 0 else 0
            computation_stats = {
                "total_questions": t["total"],
                "correct_answers": t["correct"],
                "accuracy_rate": self.calculate_accuracy_rate(t["correct"], t["total"]),
                "average_time": round(avg_time, 1),
            }
        if "concept" in track_agg:
            t = track_agg["concept"]
            avg_time = t["time"] / t["total"] if t["total"] > 0 else 0
            concept_stats = {
                "total_questions": t["total"],
                "correct_answers": t["correct"],
                "accuracy_rate": self.calculate_accuracy_rate(t["correct"], t["total"]),
                "average_time": round(avg_time, 1),
            }

        # 문제 유형별 통계
        type_stats = {}
        for type_key, t in type_agg.items():
            if t["total"] > 0:
                avg_time = t["time"] / t["total"]
                type_stats[type_key] = {
                    "total_questions": t["total"],
                    "correct_answers": t["correct"],
                    "accuracy_rate": self.calculate_accuracy_rate(t["correct"], t["total"]),
                    "average_time": round(avg_time, 1),
                }

        return {
            "user_id": student_id,
            "total_tests": total_tests,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy_rate": accuracy_rate,
            "average_time_per_question": round(avg_time, 1),
            "current_streak": student.current_streak,
            "max_streak": student.max_streak,
            "level": student.level,
            "total_xp": student.total_xp,
            "today_solved": today_solved,
            "weak_concepts": weak_concepts,
            "strong_concepts": strong_concepts,
            "computation_stats": computation_stats,
            "concept_stats": concept_stats,
            "type_stats": type_stats,
        }

    async def get_dashboard_stats(self, teacher_id: str | None = None) -> dict:
        """대시보드 통계 조회."""
        if not self.db:
            raise ValueError("Database session required")

        today = _kst_today()
        week_ago = today - timedelta(days=7)

        # 담당 반 조회 (teacher_id가 None이면 전체 - 관리자/마스터)
        classes_stmt = select(Class)
        if teacher_id:
            classes_stmt = classes_stmt.where(Class.teacher_id == teacher_id)
        classes = list((await self.db.scalars(classes_stmt)).all())
        class_ids = [c.id for c in classes]

        # 담당 학생 조회
        students_stmt = select(User).where(
            User.role == UserRole.STUDENT,
            User.is_active == True,  # noqa: E712
        )
        if teacher_id:
            students_stmt = students_stmt.where(User.class_id.in_(class_ids))
        students = list((await self.db.scalars(students_stmt)).all())
        student_ids = [s.id for s in students]

        # 오늘 통계 (KST 기준)
        today_start, today_end = _kst_day_utc_range(today)
        today_attempts_stmt = select(TestAttempt).where(
            TestAttempt.student_id.in_(student_ids),
            TestAttempt.started_at >= today_start,
            TestAttempt.started_at < today_end,
        )
        today_attempts = list((await self.db.scalars(today_attempts_stmt)).all())

        today_active = len(set(a.student_id for a in today_attempts))
        today_tests = len([a for a in today_attempts if a.completed_at])
        today_questions = sum(a.total_count for a in today_attempts if a.completed_at)
        today_correct = sum(a.correct_count for a in today_attempts if a.completed_at)
        today_accuracy = self.calculate_accuracy_rate(today_correct, today_questions)

        # 이번 주 통계 (KST 기준)
        week_start, _ = _kst_day_utc_range(week_ago)
        week_attempts_stmt = select(TestAttempt).where(
            TestAttempt.student_id.in_(student_ids),
            TestAttempt.started_at >= week_start,
        )
        week_attempts = list((await self.db.scalars(week_attempts_stmt)).all())

        week_active = len(set(a.student_id for a in week_attempts))
        week_tests = len([a for a in week_attempts if a.completed_at])

        # 7일간 정답률 트렌드
        accuracy_trend = []
        for i in range(7):
            day = today - timedelta(days=6 - i)
            day_attempts = [
                a for a in week_attempts
                if a.completed_at and _to_kst_date(a.started_at) == day
            ]
            day_questions = sum(a.total_count for a in day_attempts)
            day_correct = sum(a.correct_count for a in day_attempts)
            accuracy_trend.append(self.calculate_accuracy_rate(day_correct, day_questions))

        # 알림 생성
        alerts = []
        for student in students:
            # 비활동 학생
            if student.last_activity_date:
                days_inactive = (today - _to_kst_date(student.last_activity_date)).days
                if days_inactive >= 3:
                    alerts.append({
                        "type": "inactive",
                        "student_id": student.id,
                        "student_name": student.name,
                        "message": f"{days_inactive}일째 학습하지 않았어요",
                    })

        return {
            "today": {
                "active_students": today_active,
                "tests_completed": today_tests,
                "questions_answered": today_questions,
                "average_accuracy": today_accuracy,
            },
            "this_week": {
                "active_students": week_active,
                "tests_completed": week_tests,
                "accuracy_trend": accuracy_trend,
            },
            "alerts": alerts[:10],  # 최대 10개
        }

    async def get_students_summary(
        self,
        teacher_id: str | None = None,
        class_id: str | None = None,
        grade: Grade | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[dict], int]:
        """학생 통계 요약 목록."""
        if not self.db:
            raise ValueError("Database session required")

        # 담당 반 조회 (teacher_id가 None이면 전체 반 조회 - 관리자/마스터)
        classes_stmt = select(Class)
        if teacher_id:
            classes_stmt = classes_stmt.where(Class.teacher_id == teacher_id)
        if class_id:
            classes_stmt = classes_stmt.where(Class.id == class_id)
        classes = list((await self.db.scalars(classes_stmt)).all())
        class_map = {c.id: c for c in classes}
        class_ids = [c.id for c in classes]

        # 학생 조회
        students_stmt = select(User).where(
            User.role == UserRole.STUDENT,
            User.is_active == True,  # noqa: E712
        )
        if teacher_id:
            # 강사는 자신의 반 학생만
            students_stmt = students_stmt.where(User.class_id.in_(class_ids))
        elif class_id:
            # 관리자가 특정 반 필터
            students_stmt = students_stmt.where(User.class_id.in_(class_ids))
        if grade:
            students_stmt = students_stmt.where(User.grade == grade)

        # 총 개수
        count_stmt = select(func.count()).select_from(students_stmt.subquery())
        total = await self.db.scalar(count_stmt) or 0

        # 페이지네이션
        students_stmt = students_stmt.order_by(User.name)
        students_stmt = students_stmt.offset((page - 1) * page_size).limit(page_size)
        students = list((await self.db.scalars(students_stmt)).all())

        result = []
        for student in students:
            # 완료된 시도 수
            attempts_stmt = select(func.count()).where(
                TestAttempt.student_id == student.id,
                TestAttempt.completed_at.isnot(None),
            )
            tests_completed = await self.db.scalar(attempts_stmt) or 0

            # 정답률
            stats_stmt = select(
                func.sum(TestAttempt.correct_count),
                func.sum(TestAttempt.total_count),
            ).where(
                TestAttempt.student_id == student.id,
                TestAttempt.completed_at.isnot(None),
            )
            stats = (await self.db.execute(stats_stmt)).first()
            correct = stats[0] or 0
            total_q = stats[1] or 0
            accuracy = self.calculate_accuracy_rate(correct, total_q)

            class_ = class_map.get(student.class_id)

            result.append({
                "user_id": student.id,
                "name": student.name,
                "grade": student.grade,
                "class_name": class_.name if class_ else "",
                "level": student.level,
                "total_xp": student.total_xp,
                "accuracy_rate": accuracy,
                "tests_completed": tests_completed,
                "current_streak": student.current_streak,
                "last_activity_at": student.last_activity_date,
            })

        return result, total

    async def get_student_detail(
        self,
        student_id: str,
        teacher_id: str,
    ) -> dict | None:
        """학생 상세 통계 조회 (강사용)."""
        if not self.db:
            raise ValueError("Database session required")

        student = await self.db.get(User, student_id)
        if not student or student.role != UserRole.STUDENT:
            return None

        # 권한 확인: 담당 반의 학생인지
        if student.class_id:
            class_ = await self.db.get(Class, student.class_id)
            if class_ and class_.teacher_id != teacher_id:
                # admin이 아니면 접근 불가
                teacher = await self.db.get(User, teacher_id)
                if not teacher or teacher.role != UserRole.ADMIN:
                    return None

        # 기본 통계
        base_stats = await self.get_student_stats(student_id)
        if not base_stats:
            return None

        # 반 정보
        class_name = ""
        if student.class_id:
            class_ = await self.db.get(Class, student.class_id)
            if class_:
                class_name = class_.name

        # 최근 테스트 (최근 10개)
        recent_attempts_stmt = select(TestAttempt).where(
            TestAttempt.student_id == student_id,
            TestAttempt.completed_at.isnot(None),
        ).order_by(TestAttempt.completed_at.desc()).limit(10)
        recent_attempts = list((await self.db.scalars(recent_attempts_stmt)).all())

        recent_tests = []
        for attempt in recent_attempts:
            test = await self.db.get(Test, attempt.test_id)
            if test:
                recent_tests.append({
                    "test_id": test.id,
                    "test_title": test.title,
                    "score": attempt.score,
                    "max_score": attempt.max_score,
                    "accuracy_rate": self.calculate_accuracy_rate(
                        attempt.correct_count, attempt.total_count
                    ),
                    "completed_at": attempt.completed_at,
                })

        # 일별 활동 (최근 7일, KST 기준)
        today = _kst_today()
        daily_activity = []
        for i in range(7):
            day = today - timedelta(days=6 - i)
            day_start, day_end = _kst_day_utc_range(day)
            day_attempts_stmt = select(TestAttempt).where(
                TestAttempt.student_id == student_id,
                TestAttempt.completed_at.isnot(None),
                TestAttempt.started_at >= day_start,
                TestAttempt.started_at < day_end,
            )
            day_attempts = list((await self.db.scalars(day_attempts_stmt)).all())

            tests_completed = len(day_attempts)
            questions_answered = sum(a.total_count for a in day_attempts)
            correct = sum(a.correct_count for a in day_attempts)
            accuracy = self.calculate_accuracy_rate(correct, questions_answered)

            daily_activity.append({
                "date": day.isoformat(),
                "tests_completed": tests_completed,
                "questions_answered": questions_answered,
                "accuracy_rate": accuracy,
            })

        # 단원별 진행률 조회
        chapter_progress_list = []
        if student.grade:
            chapters_stmt = (
                select(Chapter)
                .where(Chapter.grade == student.grade, Chapter.is_active == True)  # noqa: E712
                .order_by(Chapter.chapter_number)
            )
            chapters = list((await self.db.scalars(chapters_stmt)).all())

            # 학생의 모든 ChapterProgress 조회
            progress_stmt = select(ChapterProgress).where(
                ChapterProgress.student_id == student_id
            )
            progress_map = {
                p.chapter_id: p
                for p in (await self.db.scalars(progress_stmt)).all()
            }

            # 개념 이름 맵
            all_concept_ids = []
            for ch in chapters:
                all_concept_ids.extend(ch.concept_ids or [])
            concept_name_map: dict[str, str] = {}
            if all_concept_ids:
                cn_stmt = select(Concept.id, Concept.name).where(
                    Concept.id.in_(list(set(all_concept_ids)))
                )
                for row in (await self.db.execute(cn_stmt)).all():
                    concept_name_map[row[0]] = row[1]

            for ch in chapters:
                prog = progress_map.get(ch.id)
                # concepts_mastery를 개념 이름 기반으로 변환
                named_mastery = {}
                if prog and prog.concepts_mastery:
                    for cid, pct in prog.concepts_mastery.items():
                        cname = concept_name_map.get(cid, cid)
                        named_mastery[cname] = pct

                chapter_progress_list.append({
                    "chapter_id": ch.id,
                    "chapter_name": ch.name,
                    "chapter_number": ch.chapter_number,
                    "is_unlocked": prog.is_unlocked if prog else False,
                    "is_completed": prog.is_completed if prog else False,
                    "overall_progress": prog.overall_progress if prog else 0,
                    "concepts_mastery": named_mastery,
                })

        return {
            **base_stats,
            "name": student.name,
            "login_id": student.login_id,
            "grade": student.grade,
            "class_name": class_name,
            "recent_tests": recent_tests,
            "daily_activity": daily_activity,
            "chapter_progress": chapter_progress_list,
        }

    async def get_class_stats(
        self,
        class_id: str,
        teacher_id: str,
    ) -> dict | None:
        """반 통계 조회."""
        if not self.db:
            raise ValueError("Database session required")

        class_ = await self.db.get(Class, class_id)
        if not class_:
            return None

        # 권한 확인
        if class_.teacher_id != teacher_id:
            teacher = await self.db.get(User, teacher_id)
            if not teacher or teacher.role != UserRole.ADMIN:
                return {"error": "forbidden"}

        # 학생 목록
        students_stmt = select(User).where(
            User.class_id == class_id,
            User.role == UserRole.STUDENT,
            User.is_active == True,  # noqa: E712
        )
        students = list((await self.db.scalars(students_stmt)).all())
        student_ids = [s.id for s in students]

        student_count = len(students)
        if student_count == 0:
            return {
                "class_id": class_id,
                "class_name": class_.name,
                "teacher_name": "",
                "grade": class_.grade,
                "student_count": 0,
                "average_accuracy": 0.0,
                "average_level": 0.0,
                "tests_completed_today": 0,
                "weak_concepts": [],
                "top_students": [],
                "concept_stats": [],
                "daily_stats": [],
            }

        # 평균 정답률 및 레벨 - N+1 쿼리 수정: IN절로 한 번에 조회
        total_level = sum(s.level for s in students)

        if student_ids:
            total_stats_stmt = select(
                func.sum(TestAttempt.correct_count),
                func.sum(TestAttempt.total_count),
            ).where(
                TestAttempt.student_id.in_(student_ids),
                TestAttempt.completed_at.isnot(None),
            )
            total_stats = (await self.db.execute(total_stats_stmt)).first()
            total_correct = total_stats[0] or 0
            total_questions = total_stats[1] or 0
        else:
            total_correct = 0
            total_questions = 0

        average_accuracy = self.calculate_accuracy_rate(total_correct, total_questions)
        average_level = round(total_level / student_count, 1) if student_count > 0 else 0

        # 오늘 완료된 테스트 (KST 기준)
        today = _kst_today()
        today_start, today_end = _kst_day_utc_range(today)
        today_tests_stmt = select(func.count()).where(
            TestAttempt.student_id.in_(student_ids),
            TestAttempt.completed_at.isnot(None),
            TestAttempt.started_at >= today_start,
            TestAttempt.started_at < today_end,
        )
        tests_completed_today = await self.db.scalar(today_tests_stmt) or 0

        # 상위 학생 (정답률 기준, 최대 5명) - N+1 쿼리 수정: GROUP BY로 한 번에 조회
        if student_ids:
            per_student_stmt = select(
                TestAttempt.student_id,
                func.sum(TestAttempt.correct_count).label("correct"),
                func.sum(TestAttempt.total_count).label("total"),
            ).where(
                TestAttempt.student_id.in_(student_ids),
                TestAttempt.completed_at.isnot(None),
            ).group_by(TestAttempt.student_id)

            per_student_stats = {}
            for row in await self.db.execute(per_student_stmt):
                per_student_stats[row.student_id] = {
                    "correct": row.correct or 0,
                    "total": row.total or 0,
                }
        else:
            per_student_stats = {}

        student_accuracies = []
        for student in students:
            s = per_student_stats.get(student.id, {"correct": 0, "total": 0})
            accuracy = self.calculate_accuracy_rate(s["correct"], s["total"])
            student_accuracies.append({
                "user_id": student.id,
                "name": student.name,
                "level": student.level,
                "accuracy_rate": accuracy,
            })

        top_students = sorted(
            student_accuracies,
            key=lambda x: x["accuracy_rate"],
            reverse=True,
        )[:5]

        # 담당 강사 이름
        teacher = await self.db.get(User, class_.teacher_id)
        teacher_name = teacher.name if teacher else ""

        # 일별 통계 (최근 7일, KST 기준)
        daily_stats = []
        for i in range(7):
            day = today - timedelta(days=6 - i)
            day_start, day_end = _kst_day_utc_range(day)
            day_attempts_stmt = select(TestAttempt).where(
                TestAttempt.student_id.in_(student_ids),
                TestAttempt.completed_at.isnot(None),
                TestAttempt.started_at >= day_start,
                TestAttempt.started_at < day_end,
            )
            day_attempts = list((await self.db.scalars(day_attempts_stmt)).all())

            active = len(set(a.student_id for a in day_attempts))
            tests = len(day_attempts)
            questions = sum(a.total_count for a in day_attempts)
            correct = sum(a.correct_count for a in day_attempts)
            accuracy = self.calculate_accuracy_rate(correct, questions)

            daily_stats.append({
                "date": day.isoformat(),
                "active_students": active,
                "tests_completed": tests,
                "average_accuracy": accuracy,
            })

        return {
            "class_id": class_id,
            "class_name": class_.name,
            "teacher_name": teacher_name,
            "grade": class_.grade,
            "student_count": student_count,
            "average_accuracy": average_accuracy,
            "average_level": average_level,
            "tests_completed_today": tests_completed_today,
            "weak_concepts": [],
            "top_students": top_students,
            "concept_stats": [],
            "daily_stats": daily_stats,
        }

    async def get_concept_stats(
        self,
        teacher_id: str,
        grade: Grade | None = None,
        class_id: str | None = None,
    ) -> list[dict]:
        """개념별 통계 조회."""
        if not self.db:
            raise ValueError("Database session required")

        from app.models.question import Question

        # 담당 반 조회
        classes_stmt = select(Class).where(Class.teacher_id == teacher_id)
        if class_id:
            classes_stmt = classes_stmt.where(Class.id == class_id)
        classes = list((await self.db.scalars(classes_stmt)).all())
        class_ids = [c.id for c in classes]

        if not class_ids:
            return []

        # 담당 학생 조회
        students_stmt = select(User).where(
            User.class_id.in_(class_ids),
            User.role == UserRole.STUDENT,
            User.is_active == True,  # noqa: E712
        )
        students = list((await self.db.scalars(students_stmt)).all())
        student_ids = [s.id for s in students]

        if not student_ids:
            return []

        # 개념 조회
        concepts_stmt = select(Concept)
        if grade:
            concepts_stmt = concepts_stmt.where(Concept.grade == grade)
        concepts = list((await self.db.scalars(concepts_stmt)).all())

        result = []
        for concept in concepts:
            # 해당 개념의 문제 ID 조회
            question_ids_stmt = select(Question.id).where(
                Question.concept_id == concept.id
            )
            question_ids = list((await self.db.scalars(question_ids_stmt)).all())

            if not question_ids:
                continue

            # 해당 문제들의 답안 로그 조회 (담당 학생들만)
            logs_stmt = select(AnswerLog).where(
                AnswerLog.question_id.in_(question_ids),
            ).join(TestAttempt).where(
                TestAttempt.student_id.in_(student_ids),
            )
            logs = list((await self.db.scalars(logs_stmt)).all())

            if not logs:
                continue

            total_questions = len(logs)
            correct_count = sum(1 for log in logs if log.is_correct)
            accuracy_rate = self.calculate_accuracy_rate(correct_count, total_questions)

            # 풀이한 학생 수
            attempt_ids = [log.attempt_id for log in logs]
            if attempt_ids:
                student_count_stmt = select(func.count(func.distinct(TestAttempt.student_id))).where(
                    TestAttempt.id.in_(attempt_ids)
                )
                student_count = await self.db.scalar(student_count_stmt) or 0
            else:
                student_count = 0

            # 평균 풀이 시간
            total_time = sum(log.time_spent_seconds for log in logs)
            avg_time = total_time / len(logs) if logs else 0

            result.append({
                "concept_id": concept.id,
                "concept_name": concept.name,
                "grade": concept.grade,
                "total_questions": total_questions,
                "correct_count": correct_count,
                "accuracy_rate": accuracy_rate,
                "student_count": student_count,
                "average_time_seconds": round(avg_time, 1),
                "difficulty_distribution": {"easy": 0, "medium": 0, "hard": 0},
            })

        return sorted(result, key=lambda x: x["accuracy_rate"])

    # ===========================
    # 일일 할당량 (Daily Quota)
    # ===========================

    async def _count_correct_today(self, student_id: str) -> int:
        """오늘 정답 수 계산 (KST 기준)."""
        today = _kst_today()
        today_start, today_end = _kst_day_utc_range(today)
        stmt = (
            select(func.count())
            .select_from(AnswerLog)
            .join(TestAttempt, AnswerLog.attempt_id == TestAttempt.id)
            .where(
                TestAttempt.student_id == student_id,
                AnswerLog.is_correct.is_(True),
                AnswerLog.created_at >= today_start,
                AnswerLog.created_at < today_end,
            )
        )
        return await self.db.scalar(stmt) or 0

    async def get_student_quota_progress(self, student_id: str) -> dict | None:
        """학생의 일일 할당량 진행 상황 조회."""
        user = await self.db.get(User, student_id)
        if not user or not user.class_id:
            return None

        cls = await self.db.get(Class, user.class_id)
        if not cls:
            return None

        daily_quota = cls.daily_quota or 20
        carry_over = cls.quota_carry_over or False
        correct_today = await self._count_correct_today(student_id)

        # 누적 모드 계산
        if carry_over and user.last_quota_met_date:
            last_met = _to_kst_date(user.last_quota_met_date)
            today = _kst_today()
            days_behind = max(1, (today - last_met).days)
            accumulated_quota = daily_quota * days_behind
        else:
            accumulated_quota = daily_quota

        quota_remaining = max(0, accumulated_quota - correct_today)
        quota_met = correct_today >= accumulated_quota

        return {
            "daily_quota": daily_quota,
            "correct_today": correct_today,
            "quota_remaining": quota_remaining,
            "accumulated_quota": accumulated_quota,
            "quota_met": quota_met,
            "carry_over": carry_over,
        }

    async def check_and_update_quota_met(self, student_id: str) -> bool:
        """할당량 달성 체크 후 last_quota_met_date 갱신. True면 새로 달성."""
        progress = await self.get_student_quota_progress(student_id)
        if not progress or not progress["quota_met"]:
            return False

        user = await self.db.get(User, student_id)
        today = _kst_today()
        last_met = _to_kst_date(user.last_quota_met_date) if user.last_quota_met_date else None

        if last_met != today:
            # KST 오늘 날짜를 UTC로 변환해서 저장
            user.last_quota_met_date = datetime(today.year, today.month, today.day) - timedelta(hours=9)
            await self.db.commit()
            return True
        return False

    async def get_class_quota_progress(self, class_id: str) -> list[dict]:
        """반 전체 학생의 할당량 진행 현황."""
        cls = await self.db.get(Class, class_id)
        if not cls:
            return []

        students = (
            (await self.db.scalars(
                select(User).where(
                    User.class_id == class_id,
                    User.role == UserRole.STUDENT,
                    User.is_active.is_(True),
                )
            )).all()
        )

        result = []
        for student in students:
            progress = await self.get_student_quota_progress(student.id)
            if progress:
                result.append({
                    "student_id": student.id,
                    "student_name": student.name,
                    **progress,
                })
        return result
