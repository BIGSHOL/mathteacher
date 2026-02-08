"""테스트 서비스."""

import random
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.answer_log import AnswerLog
from app.models.question import Question
from app.models.chapter import Chapter
from app.models.chapter_progress import ChapterProgress
from app.models.concept import Concept
from app.models.concept_mastery import ConceptMastery
from app.schemas.common import Grade, QuestionType
from app.services.blank_service import BlankService


def shuffle_question_options(options: list[dict], correct_answer: str) -> tuple[list[dict], str]:
    """문제 보기를 셔플하고 새 정답 라벨을 반환.

    Args:
        options: 원본 보기 리스트
        correct_answer: 원본 정답 라벨 (A, B, C, D 등)

    Returns:
        tuple: (셔플된 options 리스트, 새 정답 라벨)
    """
    if not options:
        return [], correct_answer

    # 정답 option의 id 찾기
    correct_option_id = None
    for opt in options:
        if opt.get("label") == correct_answer:
            correct_option_id = opt.get("id")
            break

    # 옵션 복사 후 셔플
    shuffled = [opt.copy() for opt in options]
    random.shuffle(shuffled)

    # 새 라벨 부여 (A, B, C, D, ...)
    labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
    new_correct = correct_answer

    for i, opt in enumerate(shuffled):
        new_label = labels[i] if i < len(labels) else str(i + 1)
        if opt.get("id") == correct_option_id:
            new_correct = new_label
        opt["label"] = new_label

    return shuffled, new_correct


async def get_student_attempt_count(db: AsyncSession, student_id: str, test_id: str) -> int:
    """완료된 시도 횟수 계산."""
    stmt = select(func.count()).where(
        TestAttempt.test_id == test_id,
        TestAttempt.student_id == student_id,
        TestAttempt.completed_at.isnot(None),
    )
    return await db.scalar(stmt) or 0


class TestService:
    """테스트 서비스."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_student_available_concept_ids(self, student_id: str, grade: Grade) -> list[str]:
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
            if first_chapter and first_chapter.concept_ids:
                mastery_service = MasteryService(self.db)
                first_concept_id = first_chapter.concept_ids[0]
                await mastery_service.ensure_first_concept_unlocked(student_id, first_chapter.id)
                await self.db.flush()
                return [first_concept_id]

            # 최종 폴백: 챕터 데이터가 없는 학년 → 전체 개념
            fallback_stmt = select(Concept.id).where(Concept.grade == grade)
            return list((await self.db.scalars(fallback_stmt)).all())

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

    async def generate_comprehensive_test(
        self,
        student_id: str,
        grade: Grade,
        test_type: str,
        semester: int | None = None,
    ) -> dict | None:
        """종합시험 자동 생성.

        Args:
            test_type: "cumulative", "semester_final", "grade_final"
            semester: 학기 종합시험의 경우 학기 번호
        """
        from app.services.chapter_service import ChapterService

        # 개념 조회
        available_concept_ids = await self._get_student_available_concept_ids(student_id, grade)

        if not available_concept_ids:
            return None

        # 테스트 유형별 필터링
        if test_type == "semester_final":
            # 학기 종합시험: 해당 학기의 개념만
            chapter_service = ChapterService(self.db)
            stmt = select(Chapter).where(
                Chapter.is_active == True,  # noqa: E712
                Chapter.grade == grade,
                Chapter.semester == semester,
            )
            semester_chapters = list((await self.db.scalars(stmt)).all())
            semester_concept_ids = []
            for ch in semester_chapters:
                semester_concept_ids.extend(ch.concept_ids or [])
            available_concept_ids = [cid for cid in available_concept_ids if cid in semester_concept_ids]

        if not available_concept_ids:
            return None

        # 해당 개념의 문제 조회 (난이도 분포 고려)
        stmt = select(Question).where(
            Question.concept_id.in_(available_concept_ids)
        )
        all_questions = list((await self.db.scalars(stmt)).all())

        if len(all_questions) < 10:
            return None

        # 난이도별 분포 (쉬움 30%, 중간 40%, 어려움 30%)
        easy = [q for q in all_questions if q.difficulty <= 4]
        medium = [q for q in all_questions if 5 <= q.difficulty <= 7]
        hard = [q for q in all_questions if q.difficulty >= 8]

        selected = []
        target_count = min(20, len(all_questions))

        # 난이도 분포에 맞게 선택
        easy_count = int(target_count * 0.3)
        medium_count = int(target_count * 0.4)
        hard_count = target_count - easy_count - medium_count

        if easy:
            selected.extend(random.sample(easy, min(easy_count, len(easy))))
        if medium:
            selected.extend(random.sample(medium, min(medium_count, len(medium))))
        if hard:
            selected.extend(random.sample(hard, min(hard_count, len(hard))))

        # 부족하면 나머지에서 랜덤 선택
        if len(selected) < target_count:
            remaining = [q for q in all_questions if q not in selected]
            selected.extend(random.sample(remaining, min(target_count - len(selected), len(remaining))))

        random.shuffle(selected)
        question_ids = [q.id for q in selected]

        # 테스트 제목 생성
        grade_labels = {
            "elementary_3": "초3", "elementary_4": "초4", "elementary_5": "초5", "elementary_6": "초6",
            "middle_1": "중1", "middle_2": "중2", "middle_3": "중3",
            "high_1": "고1", "high_2": "고1",
        }
        grade_key = grade.value if hasattr(grade, "value") else grade
        grade_label = grade_labels.get(grade_key, str(grade_key))

        if test_type == "cumulative":
            title = f"{grade_label} 누적 종합 평가"
            description = f"지금까지 학습한 {len(available_concept_ids)}개 개념을 종합적으로 평가합니다."
        elif test_type == "semester_final":
            title = f"{grade_label} {semester}학기 기말고사"
            description = f"{semester}학기에 배운 모든 내용을 종합적으로 평가합니다."
        else:  # grade_final
            title = f"{grade_label} 학년 종합 평가"
            description = f"{grade_label} 전체 과정을 종합적으로 평가합니다."

        # 가상 테스트 객체 생성 (DB에 저장하지 않음)
        grade_val = grade.value if hasattr(grade, "value") else grade
        return {
            "id": f"auto-{test_type}-{grade_val}-{semester or ''}",
            "title": title,
            "description": description,
            "grade": grade_val,
            "category": None,
            "test_type": test_type,
            "semester": semester,
            "concept_ids": available_concept_ids,
            "question_ids": question_ids,
            "question_count": len(question_ids),
            "time_limit_minutes": max(30, len(question_ids) * 2),
            "is_active": True,
            "is_adaptive": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    async def generate_weak_concept_test(
        self,
        student_id: str,
        grade: Grade,
        count: int = 15,
    ) -> dict | None:
        """약점 집중 테스트 생성.

        mastery < 60% 인 개념을 낮은 순으로 우선 출제.
        약점 개념이 없으면 None.
        """
        from app.models.concept_mastery import ConceptMastery

        # 약점 개념 조회 (mastery < 60%, 낮은 순)
        available_concept_ids = await self._get_student_available_concept_ids(student_id, grade)
        if not available_concept_ids:
            return None

        stmt = (
            select(ConceptMastery)
            .where(
                ConceptMastery.student_id == student_id,
                ConceptMastery.concept_id.in_(available_concept_ids),
                ConceptMastery.mastery_percentage < 60,
                ConceptMastery.is_unlocked == True,  # noqa: E712
            )
            .order_by(ConceptMastery.mastery_percentage.asc())
        )
        weak_masteries = list((await self.db.scalars(stmt)).all())

        if not weak_masteries:
            return None

        weak_concept_ids = [m.concept_id for m in weak_masteries]

        # 약점 개념의 문제 조회
        q_stmt = select(Question).where(
            Question.concept_id.in_(weak_concept_ids),
            Question.is_active == True,  # noqa: E712
        )
        all_questions = list((await self.db.scalars(q_stmt)).all())

        if not all_questions:
            return None

        # 개념별 문제 분류 (약한 순서 유지)
        concept_questions: dict[str, list] = {cid: [] for cid in weak_concept_ids}
        for q in all_questions:
            if q.concept_id in concept_questions:
                concept_questions[q.concept_id].append(q)

        # 약한 개념 순으로 문제 선택 (가장 약한 개념에 더 많은 문제)
        selected = []
        target_count = min(count, len(all_questions))

        # 1단계: 각 약점 개념에서 최소 2문제씩
        for cid in weak_concept_ids:
            qs = concept_questions[cid]
            if qs and len(selected) < target_count:
                pick = min(2, len(qs), target_count - len(selected))
                selected.extend(random.sample(qs, pick))

        # 2단계: 남은 슬롯을 가장 약한 개념 순으로 채움
        selected_ids = {q.id for q in selected}
        for cid in weak_concept_ids:
            if len(selected) >= target_count:
                break
            remaining_qs = [q for q in concept_questions[cid] if q.id not in selected_ids]
            if remaining_qs:
                pick = min(len(remaining_qs), target_count - len(selected))
                added = random.sample(remaining_qs, pick)
                selected.extend(added)
                selected_ids.update(q.id for q in added)

        random.shuffle(selected)
        question_ids = [q.id for q in selected]

        # 개념 이름 조회
        concept_stmt = select(Concept.id, Concept.name).where(
            Concept.id.in_(weak_concept_ids)
        )
        concept_names = {row[0]: row[1] for row in (await self.db.execute(concept_stmt)).all()}

        # 약점 개념 정보 (프론트엔드에 표시용)
        weak_info = []
        for m in weak_masteries:
            if m.concept_id in concept_names:
                weak_info.append({
                    "concept_id": m.concept_id,
                    "concept_name": concept_names[m.concept_id],
                    "mastery_percentage": m.mastery_percentage,
                })

        grade_labels = {
            "elementary_3": "초3", "elementary_4": "초4", "elementary_5": "초5", "elementary_6": "초6",
            "middle_1": "중1", "middle_2": "중2", "middle_3": "중3",
            "high_1": "고1", "high_2": "고2",
        }
        grade_key = grade.value if hasattr(grade, "value") else grade
        grade_label = grade_labels.get(grade_key, str(grade_key))

        return {
            "id": f"auto-weak-{grade_key}",
            "title": f"{grade_label} 약점 집중 훈련",
            "description": f"숙련도 60% 미만인 {len(weak_concept_ids)}개 개념을 집중 학습합니다.",
            "grade": grade_key,
            "category": None,
            "test_type": "weak_concept",
            "concept_ids": weak_concept_ids,
            "question_ids": question_ids,
            "question_count": len(question_ids),
            "time_limit_minutes": max(20, len(question_ids) * 2),
            "is_active": True,
            "is_adaptive": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "weak_concepts": weak_info,
        }

    async def get_available_tests(
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

        # 해금된 챕터의 concept_ids로 테스트 필터링
        available_concept_ids: list[str] = []
        if grade:
            available_concept_ids = await self._get_student_available_concept_ids(student_id, grade)

        # 페이지네이션 전에 전체 목록을 가져와서 concept 필터링
        stmt = stmt.order_by(Test.created_at.desc())
        all_tests = list((await self.db.scalars(stmt)).all())

        # 테스트의 concept_ids가 해금된 concept에 포함되는 것만 필터링
        if available_concept_ids and grade:
            from app.services.chapter_service import ChapterService
            chapter_service = ChapterService(self.db)

            # 학기/학년 완료 상태 조회
            semester_status = await chapter_service.get_semester_completion_status(student_id, grade)
            grade_status = await chapter_service.get_grade_completion_status(student_id, grade)

            filtered_tests = []
            for t in all_tests:
                # 일일 테스트는 별도 API(/daily-tests)로 관리 → available 목록에서 제외
                if t.id.startswith("daily-"):
                    continue
                # 진단 평가는 항상 표시
                if getattr(t, "is_placement", False):
                    filtered_tests.append(t)
                    continue
                if not t.concept_ids:
                    filtered_tests.append(t)
                    continue

                # 테스트 유형별 필터링
                test_type = getattr(t, "test_type", "concept")

                if test_type == "semester_final":
                    # 학기 종합시험: 해당 학기 100% 완료 시에만 표시
                    semester = getattr(t, "semester", None)
                    if semester and semester_status.get(semester, {}).get("is_completed"):
                        filtered_tests.append(t)
                elif test_type == "grade_final":
                    # 학년 종합시험: 학년 전체 100% 완료 시에만 표시
                    if grade_status.get("is_completed"):
                        filtered_tests.append(t)
                elif test_type == "cumulative":
                    # 누적 종합시험: 해금된 개념만 포함 (동적 필터링)
                    # 해금된 개념 중 하나라도 있으면 표시
                    if any(cid in available_concept_ids for cid in t.concept_ids):
                        filtered_tests.append(t)
                else:
                    # 일반 개념/연산 테스트: 테스트의 모든 concept_ids가 해금되어야 표시
                    if t.concept_ids and all(cid in available_concept_ids for cid in t.concept_ids):
                        filtered_tests.append(t)
            all_tests = filtered_tests

            # 자동 생성 종합시험 추가
            auto_tests = []

            # 1. 누적 종합시험 (항상 표시)
            cumulative = await self.generate_comprehensive_test(student_id, grade, "cumulative")
            if cumulative:
                auto_tests.append(cumulative)

            # 2. 학기 기말시험 (학기 완료 시 표시)
            for sem, status in semester_status.items():
                if status.get("is_completed"):
                    sem_final = await self.generate_comprehensive_test(student_id, grade, "semester_final", sem)
                    if sem_final:
                        auto_tests.append(sem_final)

            # 3. 학년 기말시험 (학년 완료 시 표시)
            if grade_status.get("is_completed"):
                grade_final = await self.generate_comprehensive_test(student_id, grade, "grade_final")
                if grade_final:
                    auto_tests.append(grade_final)

            # 자동 생성 테스트를 앞에 추가
            all_tests = auto_tests + all_tests

        total = len(all_tests)

        # 페이지네이션
        start = (page - 1) * page_size
        tests = all_tests[start:start + page_size]

        # 한 번의 쿼리로 모든 테스트의 시도 통계 조회
        test_ids = [t.id if hasattr(t, 'id') else t['id'] for t in tests]
        if test_ids:
            stats_stmt = select(
                TestAttempt.test_id,
                func.count().label("attempt_count"),
                func.max(TestAttempt.score).label("best_score"),
            ).where(
                TestAttempt.test_id.in_(test_ids),
                TestAttempt.student_id == student_id,
                TestAttempt.completed_at.isnot(None),
            ).group_by(TestAttempt.test_id)

            stats_map = {}
            for row in await self.db.execute(stats_stmt):
                stats_map[row.test_id] = {
                    "attempt_count": row.attempt_count,
                    "best_score": row.best_score,
                }
        else:
            stats_map = {}

        # 각 테스트의 문제 평균 난이도 조회
        all_question_ids = []
        for t in tests:
            qids = t.question_ids if hasattr(t, 'question_ids') else t.get('question_ids', [])
            all_question_ids.extend(qids or [])
        diff_map: dict[str, int] = {}
        if all_question_ids:
            diff_stmt = select(Question.id, Question.difficulty).where(
                Question.id.in_(list(set(all_question_ids)))
            )
            q_diff = {row[0]: row[1] for row in (await self.db.execute(diff_stmt)).all()}
            for t in tests:
                tid = t.id if hasattr(t, 'id') else t['id']
                qids = t.question_ids if hasattr(t, 'question_ids') else t.get('question_ids', [])
                diffs = [q_diff[qid] for qid in (qids or []) if qid in q_diff]
                diff_map[tid] = round(sum(diffs) / len(diffs)) if diffs else 5

        # 각 테스트에 대한 학생의 시도 정보 추가
        result = []
        for test in tests:
            tid = test.id if hasattr(test, 'id') else test['id']
            stats = stats_map.get(tid, {"attempt_count": 0, "best_score": None})
            result.append({
                "test": test,
                "is_completed": stats["attempt_count"] > 0,
                "best_score": stats["best_score"],
                "attempt_count": stats["attempt_count"],
                "difficulty": diff_map.get(tid, 5),
            })

        return result, total

    async def get_test_by_id(self, test_id: str, student_id: str | None = None) -> Test | dict | None:
        """테스트 조회 (auto-generated 테스트 포함)."""
        # 자동 생성 테스트 처리
        if test_id.startswith("auto-") and student_id:
            # auto-weak-{grade} 형식
            if test_id.startswith("auto-weak-"):
                grade = test_id.replace("auto-weak-", "")
                return await self.generate_weak_concept_test(student_id, grade)

            # auto-cumulative-middle_1- 형식 파싱
            parts = test_id.split("-")
            if len(parts) >= 3:
                test_type = parts[1]  # cumulative, semester_final, grade_final
                grade = parts[2]
                semester = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else None
                return await self.generate_comprehensive_test(student_id, grade, test_type, semester)

        return await self.db.get(Test, test_id)

    async def get_test_with_questions(self, test_id: str, student_id: str | None = None) -> dict | None:
        """테스트와 문제 목록 조회."""
        test = await self.get_test_by_id(test_id, student_id)
        if not test:
            return None

        # test가 dict인 경우 (auto-generated)
        if isinstance(test, dict):
            question_ids = test['question_ids']
        else:
            question_ids = test.question_ids

        # 문제 조회
        stmt = select(Question).where(Question.id.in_(question_ids))
        questions = list((await self.db.scalars(stmt)).all())

        # 문제 순서 정렬 (question_ids 순서대로)
        question_map = {q.id: q for q in questions}
        ordered_questions = [question_map[qid] for qid in question_ids if qid in question_map]

        return {
            "test": test,
            "questions": ordered_questions,
        }

    async def start_test(self, test_id: str, student_id: str) -> TestAttempt | None:
        """테스트 시작."""
        test = await self.get_test_by_id(test_id, student_id)
        if not test:
            return None

        # test가 dict인 경우 (auto-generated) 처리
        is_auto = isinstance(test, dict)
        if is_auto:
            all_question_ids = test.get('question_ids', [])
            use_pool = False
            questions_per_attempt = None
            shuffle_options = True
        else:
            all_question_ids = test.question_ids or []
            use_pool = test.use_question_pool
            questions_per_attempt = test.questions_per_attempt
            shuffle_options = test.shuffle_options

        # 문제 선택
        selected_question_ids = all_question_ids

        # 문제 풀 방식: 랜덤하게 N개 선택
        if use_pool and questions_per_attempt:
            pool_size = len(all_question_ids)
            select_count = min(test.questions_per_attempt, pool_size)
            selected_question_ids = random.sample(all_question_ids, select_count)

        # 선택된 문제 조회
        stmt = select(Question).where(Question.id.in_(selected_question_ids))
        questions = list((await self.db.scalars(stmt)).all())
        question_map = {q.id: q for q in questions}
        ordered_questions = [question_map[qid] for qid in selected_question_ids if qid in question_map]

        # 보기 셔플 설정 생성
        question_shuffle_config = {}
        if shuffle_options:
            for q in ordered_questions:
                if q.options:
                    shuffled_options, new_correct = shuffle_question_options(
                        q.options, q.correct_answer
                    )
                    question_shuffle_config[q.id] = {
                        "shuffled_options": shuffled_options,
                        "correct_answer": new_correct,
                    }

        # 빈칸 생성 (빈칸 채우기 문제용)
        attempt_count = await get_student_attempt_count(self.db, student_id, test_id) + 1
        blank_service = BlankService(self.db)

        for q in ordered_questions:
            if q.question_type == QuestionType.FILL_IN_BLANK:
                blank_data = None

                # 1) 새로운 형식: blank_positions + round_rules → BlankService
                if q.blank_config and q.blank_config.get("blank_positions"):
                    temp_attempt_id = f"temp_{test_id}_{student_id}_{attempt_count}"
                    blank_data = blank_service.generate_blanks_for_attempt(
                        question=q,
                        attempt_count=attempt_count,
                        student_id=student_id,
                        attempt_id=temp_attempt_id
                    )

                # 2) 이전 형식: content에 [answer] 마커가 있는 문제
                elif "[answer]" in (q.content or ""):
                    display_content = q.content.replace("[answer]", "___")
                    answers = (q.correct_answer or "").split("|")
                    blank_answers = {}
                    for i, ans in enumerate(answers):
                        blank_answers[f"blank_{i}"] = {
                            "answer": ans.strip(),
                            "position": i,
                        }
                    blank_data = {
                        "display_content": display_content,
                        "blank_answers": blank_answers,
                        "original_content": q.content,
                    }

                # 3) fb() 스타일: blank_config에 accept_formats가 있지만 [answer] 없는 문제
                elif q.blank_config and q.blank_config.get("accept_formats"):
                    content_text = q.content or ""
                    # "~의 값은?" 형태를 "~의 값은 ___" 로 변환
                    if content_text.endswith("?"):
                        display_content = content_text[:-1].rstrip() + " ___"
                    else:
                        display_content = content_text + " ___"
                    blank_answers = {
                        "blank_0": {
                            "answer": (q.correct_answer or "").strip(),
                            "position": 0,
                        }
                    }
                    blank_data = {
                        "display_content": display_content,
                        "blank_answers": blank_answers,
                        "original_content": q.content,
                    }

                if blank_data:
                    if q.id not in question_shuffle_config:
                        question_shuffle_config[q.id] = {}
                    question_shuffle_config[q.id]["blank_config"] = blank_data

        # 최대 점수 계산
        max_score = sum(q.points for q in ordered_questions)

        # 시도 생성
        attempt = TestAttempt(
            test_id=test_id,
            student_id=student_id,
            max_score=max_score,
            total_count=len(ordered_questions),
            selected_question_ids=selected_question_ids if use_pool else None,
            question_shuffle_config=question_shuffle_config if question_shuffle_config else None,
        )
        self.db.add(attempt)
        await self.db.commit()
        await self.db.refresh(attempt)

        return attempt

    async def get_attempt_by_id(self, attempt_id: str) -> TestAttempt | None:
        """시도 조회."""
        return await self.db.get(TestAttempt, attempt_id)

    async def get_attempt_questions(
        self, attempt_id: str, include_answer: bool = False
    ) -> list[dict] | None:
        """시도의 문제 목록 조회 (셔플 적용)."""
        attempt = await self.get_attempt_by_id(attempt_id)
        if not attempt:
            return None

        test = await self.get_test_by_id(attempt.test_id)
        if not test:
            return None

        # 문제 ID 결정 (문제 풀 방식이면 선택된 문제, 아니면 전체)
        question_ids = attempt.selected_question_ids or test.question_ids or []

        # 문제 조회
        stmt = select(Question).where(Question.id.in_(question_ids))
        questions = list((await self.db.scalars(stmt)).all())
        question_map = {q.id: q for q in questions}
        ordered_questions = [question_map[qid] for qid in question_ids if qid in question_map]

        # 셔플 설정 적용
        shuffle_config = attempt.question_shuffle_config or {}
        result = []

        # 개념 이름 일괄 조회
        from app.models.concept import Concept
        concept_ids = list({q.concept_id for q in ordered_questions if q.concept_id})
        concept_name_map: dict[str, str] = {}
        if concept_ids:
            concept_stmt = select(Concept.id, Concept.name).where(Concept.id.in_(concept_ids))
            for row in (await self.db.execute(concept_stmt)).all():
                concept_name_map[row[0]] = row[1]

        for q in ordered_questions:
            q_data = {
                "id": q.id,
                "concept_id": q.concept_id,
                "concept_name": concept_name_map.get(q.concept_id, ""),
                "category": q.category,
                "part": q.part,
                "content": q.content,
                "question_type": q.question_type,
                "difficulty": q.difficulty,
                "points": q.points,
                "explanation": q.explanation,
                "options": q.options,
            }

            # 셔플된 보기와 정답 사용
            if q.id in shuffle_config:
                config = shuffle_config[q.id]
                if "shuffled_options" in config:
                    q_data["options"] = config["shuffled_options"]
                    # 정답은 응답에 포함하지 않음 (채점 시에만 사용)
                if "blank_config" in config:
                    q_data["blank_config"] = config["blank_config"]
                
                if include_answer and "correct_answer" in config:
                    q_data["correct_answer"] = config["correct_answer"]
            
            if include_answer and "correct_answer" not in q_data:
                 q_data["correct_answer"] = q.correct_answer

            result.append(q_data)

        return result

    async def get_correct_answer_for_attempt(self, attempt_id: str, question_id: str) -> str | None:
        """특정 시도에서 문제의 정답 조회 (셔플 적용)."""
        attempt = await self.get_attempt_by_id(attempt_id)
        if not attempt:
            return None

        # 셔플 설정에서 정답 확인
        shuffle_config = attempt.question_shuffle_config or {}
        if question_id in shuffle_config and "correct_answer" in shuffle_config[question_id]:
            return shuffle_config[question_id]["correct_answer"]

        # 셔플이 없거나 correct_answer가 없으면 원본 정답
        question = await self.db.get(Question, question_id)
        return question.correct_answer if question else None

    async def get_attempt_with_details(
        self, attempt_id: str, include_answer: bool = False
    ) -> dict | None:
        """시도와 상세 정보 조회."""
        attempt = await self.get_attempt_by_id(attempt_id)
        if not attempt:
            return None

        # 답안 기록 조회
        stmt = select(AnswerLog).where(AnswerLog.attempt_id == attempt_id)
        answer_logs = list((await self.db.scalars(stmt)).all())

        # 테스트 정보
        test = await self.get_test_by_id(attempt.test_id)


        return {
            "attempt": attempt,
            "answer_logs": answer_logs,
            "test": test,
        }

    async def abandon_attempt(self, attempt_id: str, student_id: str) -> bool:
        """시험 시도를 포기(삭제)합니다. 본인의 미완료 시도만 삭제 가능."""
        attempt = await self.get_attempt_by_id(attempt_id)
        if not attempt:
            return False
        if attempt.student_id != student_id:
            return False
        if attempt.completed_at is not None:
            return False

        # DailyTestRecord에서 참조 해제
        from app.models.daily_test_record import DailyTestRecord
        dr_stmt = select(DailyTestRecord).where(
            DailyTestRecord.attempt_id == attempt_id
        )
        daily_record = await self.db.scalar(dr_stmt)
        if daily_record:
            daily_record.attempt_id = None
            daily_record.status = "pending"

        await self.db.delete(attempt)
        await self.db.commit()
        return True

    async def check_already_answered(self, attempt_id: str, question_id: str) -> bool:
        """이미 답안을 제출했는지 확인."""
        stmt = select(AnswerLog).where(
            AnswerLog.attempt_id == attempt_id,
            AnswerLog.question_id == question_id,
        )
        return await self.db.scalar(stmt) is not None

    async def get_current_combo(self, attempt_id: str) -> int:
        """현재 콤보 수 조회."""
        stmt = (
            select(AnswerLog)
            .where(AnswerLog.attempt_id == attempt_id)
            .order_by(AnswerLog.created_at.desc())
        )
        logs = list((await self.db.scalars(stmt)).all())

        combo = 0
        for log in logs:
            if log.is_correct:
                combo += 1
            else:
                break

        return combo

    async def complete_attempt(self, attempt_id: str) -> TestAttempt | None:
        """시도 완료."""
        attempt = await self.get_attempt_by_id(attempt_id)
        if not attempt or attempt.completed_at:
            return None

        attempt.completed_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(attempt)

        return attempt
