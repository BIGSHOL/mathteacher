"""통계 서비스."""

from datetime import datetime, timedelta, timezone
from collections import defaultdict

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.class_ import Class
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

    def __init__(self, db: Session | None = None):
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

    def get_student_stats(self, student_id: str) -> dict | None:
        """학생 통계 조회."""
        if not self.db:
            raise ValueError("Database session required")

        student = self.db.get(User, student_id)
        if not student or student.role != UserRole.STUDENT:
            return None

        # 완료된 시도 조회
        attempts_stmt = select(TestAttempt).where(
            TestAttempt.student_id == student_id,
            TestAttempt.completed_at.isnot(None),
        )
        attempts = list(self.db.scalars(attempts_stmt).all())

        total_tests = len(attempts)
        total_questions = sum(a.total_count for a in attempts)
        correct_answers = sum(a.correct_count for a in attempts)
        accuracy_rate = self.calculate_accuracy_rate(correct_answers, total_questions)

        # 평균 풀이 시간
        total_time = 0
        answer_count = 0
        for attempt in attempts:
            logs = list(self.db.scalars(
                select(AnswerLog).where(AnswerLog.attempt_id == attempt.id)
            ).all())
            for log in logs:
                total_time += log.time_spent_seconds
                answer_count += 1

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
        today_solved = self.db.scalar(today_solved_stmt) or 0

        # 개념별/트랙별 통계 계산
        from app.models.question import Question

        all_logs_stmt = (
            select(AnswerLog, Question.concept_id, Question.category)
            .join(Question, AnswerLog.question_id == Question.id)
            .join(TestAttempt, AnswerLog.attempt_id == TestAttempt.id)
            .where(TestAttempt.student_id == student_id)
        )
        all_logs = list(self.db.execute(all_logs_stmt).all())

        # 개념별 집계
        concept_agg: dict[str, dict] = defaultdict(
            lambda: {"correct": 0, "total": 0}
        )
        # 트랙별 집계
        track_agg: dict[str, dict] = defaultdict(
            lambda: {"correct": 0, "total": 0}
        )

        for log, concept_id, category in all_logs:
            concept_agg[concept_id]["total"] += 1
            if log.is_correct:
                concept_agg[concept_id]["correct"] += 1
            cat_key = category.value if hasattr(category, "value") else category
            track_agg[cat_key]["total"] += 1
            if log.is_correct:
                track_agg[cat_key]["correct"] += 1

        # 개념 이름 매핑
        concept_ids = list(concept_agg.keys())
        concept_names: dict[str, str] = {}
        if concept_ids:
            concepts_stmt = select(Concept.id, Concept.name).where(
                Concept.id.in_(concept_ids)
            )
            for cid, cname in self.db.execute(concepts_stmt).all():
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
            computation_stats = {
                "total_questions": t["total"],
                "correct_answers": t["correct"],
                "accuracy_rate": self.calculate_accuracy_rate(t["correct"], t["total"]),
            }
        if "concept" in track_agg:
            t = track_agg["concept"]
            concept_stats = {
                "total_questions": t["total"],
                "correct_answers": t["correct"],
                "accuracy_rate": self.calculate_accuracy_rate(t["correct"], t["total"]),
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
        }

    def get_dashboard_stats(self, teacher_id: str) -> dict:
        """대시보드 통계 조회."""
        if not self.db:
            raise ValueError("Database session required")

        today = _kst_today()
        week_ago = today - timedelta(days=7)

        # 담당 반 조회
        classes_stmt = select(Class).where(Class.teacher_id == teacher_id)
        classes = list(self.db.scalars(classes_stmt).all())
        class_ids = [c.id for c in classes]

        # 담당 학생 조회
        students_stmt = select(User).where(
            User.class_id.in_(class_ids),
            User.role == UserRole.STUDENT,
            User.is_active == True,  # noqa: E712
        )
        students = list(self.db.scalars(students_stmt).all())
        student_ids = [s.id for s in students]

        # 오늘 통계 (KST 기준)
        today_start, today_end = _kst_day_utc_range(today)
        today_attempts_stmt = select(TestAttempt).where(
            TestAttempt.student_id.in_(student_ids),
            TestAttempt.started_at >= today_start,
            TestAttempt.started_at < today_end,
        )
        today_attempts = list(self.db.scalars(today_attempts_stmt).all())

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
        week_attempts = list(self.db.scalars(week_attempts_stmt).all())

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

    def get_students_summary(
        self,
        teacher_id: str,
        class_id: str | None = None,
        grade: Grade | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[dict], int]:
        """학생 통계 요약 목록."""
        if not self.db:
            raise ValueError("Database session required")

        # 담당 반 조회
        classes_stmt = select(Class).where(Class.teacher_id == teacher_id)
        if class_id:
            classes_stmt = classes_stmt.where(Class.id == class_id)
        classes = list(self.db.scalars(classes_stmt).all())
        class_map = {c.id: c for c in classes}
        class_ids = [c.id for c in classes]

        # 학생 조회
        students_stmt = select(User).where(
            User.class_id.in_(class_ids),
            User.role == UserRole.STUDENT,
            User.is_active == True,  # noqa: E712
        )
        if grade:
            students_stmt = students_stmt.where(User.grade == grade)

        # 총 개수
        count_stmt = select(func.count()).select_from(students_stmt.subquery())
        total = self.db.scalar(count_stmt) or 0

        # 페이지네이션
        students_stmt = students_stmt.order_by(User.name)
        students_stmt = students_stmt.offset((page - 1) * page_size).limit(page_size)
        students = list(self.db.scalars(students_stmt).all())

        result = []
        for student in students:
            # 완료된 시도 수
            attempts_stmt = select(func.count()).where(
                TestAttempt.student_id == student.id,
                TestAttempt.completed_at.isnot(None),
            )
            tests_completed = self.db.scalar(attempts_stmt) or 0

            # 정답률
            stats_stmt = select(
                func.sum(TestAttempt.correct_count),
                func.sum(TestAttempt.total_count),
            ).where(
                TestAttempt.student_id == student.id,
                TestAttempt.completed_at.isnot(None),
            )
            stats = self.db.execute(stats_stmt).first()
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

    def get_student_detail(
        self,
        student_id: str,
        teacher_id: str,
    ) -> dict | None:
        """학생 상세 통계 조회 (강사용)."""
        if not self.db:
            raise ValueError("Database session required")

        student = self.db.get(User, student_id)
        if not student or student.role != UserRole.STUDENT:
            return None

        # 권한 확인: 담당 반의 학생인지
        if student.class_id:
            class_ = self.db.get(Class, student.class_id)
            if class_ and class_.teacher_id != teacher_id:
                # admin이 아니면 접근 불가
                teacher = self.db.get(User, teacher_id)
                if not teacher or teacher.role != UserRole.ADMIN:
                    return None

        # 기본 통계
        base_stats = self.get_student_stats(student_id)
        if not base_stats:
            return None

        # 반 정보
        class_name = ""
        if student.class_id:
            class_ = self.db.get(Class, student.class_id)
            if class_:
                class_name = class_.name

        # 최근 테스트 (최근 10개)
        recent_attempts_stmt = select(TestAttempt).where(
            TestAttempt.student_id == student_id,
            TestAttempt.completed_at.isnot(None),
        ).order_by(TestAttempt.completed_at.desc()).limit(10)
        recent_attempts = list(self.db.scalars(recent_attempts_stmt).all())

        recent_tests = []
        for attempt in recent_attempts:
            test = self.db.get(Test, attempt.test_id)
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
            day_attempts = list(self.db.scalars(day_attempts_stmt).all())

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

        return {
            **base_stats,
            "name": student.name,
            "email": student.email,
            "grade": student.grade,
            "class_name": class_name,
            "recent_tests": recent_tests,
            "daily_activity": daily_activity,
        }

    def get_class_stats(
        self,
        class_id: str,
        teacher_id: str,
    ) -> dict | None:
        """반 통계 조회."""
        if not self.db:
            raise ValueError("Database session required")

        class_ = self.db.get(Class, class_id)
        if not class_:
            return None

        # 권한 확인
        if class_.teacher_id != teacher_id:
            teacher = self.db.get(User, teacher_id)
            if not teacher or teacher.role != UserRole.ADMIN:
                return {"error": "forbidden"}

        # 학생 목록
        students_stmt = select(User).where(
            User.class_id == class_id,
            User.role == UserRole.STUDENT,
            User.is_active == True,  # noqa: E712
        )
        students = list(self.db.scalars(students_stmt).all())
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

        # 평균 정답률 및 레벨
        total_correct = 0
        total_questions = 0
        total_level = sum(s.level for s in students)

        for student_id in student_ids:
            stats_stmt = select(
                func.sum(TestAttempt.correct_count),
                func.sum(TestAttempt.total_count),
            ).where(
                TestAttempt.student_id == student_id,
                TestAttempt.completed_at.isnot(None),
            )
            stats = self.db.execute(stats_stmt).first()
            total_correct += stats[0] or 0
            total_questions += stats[1] or 0

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
        tests_completed_today = self.db.scalar(today_tests_stmt) or 0

        # 상위 학생 (정답률 기준, 최대 5명)
        top_students = []
        student_accuracies = []
        for student in students:
            stats_stmt = select(
                func.sum(TestAttempt.correct_count),
                func.sum(TestAttempt.total_count),
            ).where(
                TestAttempt.student_id == student.id,
                TestAttempt.completed_at.isnot(None),
            )
            stats = self.db.execute(stats_stmt).first()
            correct = stats[0] or 0
            total_q = stats[1] or 0
            accuracy = self.calculate_accuracy_rate(correct, total_q)
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
        teacher = self.db.get(User, class_.teacher_id)
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
            day_attempts = list(self.db.scalars(day_attempts_stmt).all())

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

    def get_concept_stats(
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
        classes = list(self.db.scalars(classes_stmt).all())
        class_ids = [c.id for c in classes]

        if not class_ids:
            return []

        # 담당 학생 조회
        students_stmt = select(User).where(
            User.class_id.in_(class_ids),
            User.role == UserRole.STUDENT,
            User.is_active == True,  # noqa: E712
        )
        students = list(self.db.scalars(students_stmt).all())
        student_ids = [s.id for s in students]

        if not student_ids:
            return []

        # 개념 조회
        concepts_stmt = select(Concept)
        if grade:
            concepts_stmt = concepts_stmt.where(Concept.grade == grade)
        concepts = list(self.db.scalars(concepts_stmt).all())

        result = []
        for concept in concepts:
            # 해당 개념의 문제 ID 조회
            question_ids_stmt = select(Question.id).where(
                Question.concept_id == concept.id
            )
            question_ids = list(self.db.scalars(question_ids_stmt).all())

            if not question_ids:
                continue

            # 해당 문제들의 답안 로그 조회 (담당 학생들만)
            logs_stmt = select(AnswerLog).where(
                AnswerLog.question_id.in_(question_ids),
            ).join(TestAttempt).where(
                TestAttempt.student_id.in_(student_ids),
            )
            logs = list(self.db.scalars(logs_stmt).all())

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
                student_count = self.db.scalar(student_count_stmt) or 0
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
