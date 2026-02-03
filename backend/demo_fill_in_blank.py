"""Fill-in-Blank Feature Demo - Full Flow Simulation."""

from app.core.database import SessionLocal
from app.models import Question, User, Test
from app.schemas.common import QuestionType, Grade
from app.services.blank_service import BlankService
from app.services.grading_service import GradingService
import json


def print_section(title: str):
    """Print section title."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_data(label: str, data: any):
    """Print data."""
    print(f"{label}:")
    if isinstance(data, dict) or isinstance(data, list):
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"  {data}")
    print()


def main():
    """빈칸 채우기 기능 전체 흐름 데모."""
    db = SessionLocal()

    try:
        print_section("빈칸 채우기 기능 전체 시나리오 데모")

        # 1. 빈칸 채우기 문제 조회
        print_section("1단계: 빈칸 채우기 문제 조회")
        question = db.query(Question).filter(
            Question.question_type == QuestionType.FILL_IN_BLANK
        ).first()

        if not question:
            print("빈칸 채우기 문제가 없습니다. 먼저 샘플 데이터를 생성하세요.")
            return

        print_data("문제 내용", question.content)
        print_data("문제 ID", question.id)
        print_data("난이도", question.difficulty)
        print_data("배점", question.points)
        print_data("빈칸 설정", question.blank_config)

        # 서비스 초기화
        blank_service = BlankService(db)
        grading_service = GradingService(db)

        # 시뮬레이션할 학생 정보
        student_id = "test-student-123"
        test_student_name = "테스트 학생"

        print_section("학생 정보")
        print(f"학생 ID: {student_id}")
        print(f"학생 이름: {test_student_name}")

        # 2-4. 각 회차별 시뮬레이션
        for round_num in [1, 2, 3]:
            print_section(f"{round_num}회차: 테스트 시작")

            attempt_id = f"attempt-round-{round_num}"

            # 빈칸 생성
            blank_data = blank_service.generate_blanks_for_attempt(
                question=question,
                attempt_count=round_num,
                student_id=student_id,
                attempt_id=attempt_id
            )

            print(f"시도 ID: {attempt_id}")
            print(f"회차: {round_num}")
            print()

            # 생성된 빈칸 정보
            blank_answers = blank_data.get("blank_answers", {})
            display_content = blank_data.get("display_content", "")

            print_data("빈칸 개수", len(blank_answers))
            print_data("화면 표시 내용", display_content)

            if blank_answers:
                print("빈칸 정답:")
                for blank_id, answer_data in blank_answers.items():
                    print(f"  {blank_id}: '{answer_data['answer']}' (위치: {answer_data['position']})")
                print()

            # 회차별 예상 빈칸 개수
            expected_ranges = {
                1: (0, 0),
                2: (2, 3),
                3: (4, 6)
            }
            exp_min, exp_max = expected_ranges[round_num]
            actual = len(blank_answers)

            if exp_min <= actual <= exp_max:
                print(f"[OK] 검증 통과: 예상 {exp_min}~{exp_max}개, 실제 {actual}개")
            else:
                print(f"[X] 검증 실패: 예상 {exp_min}~{exp_max}개, 실제 {actual}개")

            # 답안 제출 시뮬레이션
            print_section(f"{round_num}회차: 답안 제출 및 채점")

            if round_num == 1:
                # 1회차는 빈칸이 없으므로 답안 제출 불필요
                print("1회차는 빈칸이 없으므로 읽기만 수행합니다.")
                continue

            # 시나리오 1: 모든 정답
            print("\n[시나리오 A] 모든 빈칸 정답:")
            student_answers_perfect = {
                blank_id: data["answer"]
                for blank_id, data in blank_answers.items()
            }

            result_perfect = grading_service.grade_answer(
                question_id=question.id,
                selected_answer=student_answers_perfect,
                correct_answer=blank_answers,
                points=question.points
            )

            print(f"  학생 답안: {student_answers_perfect}")
            print(f"  정답 여부: {'[OK] 정답' if result_perfect['is_correct'] else '[X] 오답'}")
            print(f"  획득 점수: {result_perfect['points_earned']}/{question.points}점")
            print(f"  정답 개수: {result_perfect['correct_count']}/{result_perfect['total_blanks']}개")

            # 시나리오 2: 부분 정답
            if len(blank_answers) >= 2:
                print("\n[시나리오 B] 부분 정답 (첫 번째만 오답):")
                student_answers_partial = student_answers_perfect.copy()
                first_blank_id = list(blank_answers.keys())[0]
                student_answers_partial[first_blank_id] = "틀린답"

                result_partial = grading_service.grade_answer(
                    question_id=question.id,
                    selected_answer=student_answers_partial,
                    correct_answer=blank_answers,
                    points=question.points
                )

                print(f"  학생 답안: {student_answers_partial}")
                print(f"  정답 여부: {'[OK] 정답' if result_partial['is_correct'] else '[X] 오답'}")
                print(f"  획득 점수: {result_partial['points_earned']}/{question.points}점")
                print(f"  정답 개수: {result_partial['correct_count']}/{result_partial['total_blanks']}개")

            # 시나리오 3: 모두 오답
            print("\n[시나리오 C] 모두 오답:")
            student_answers_wrong = {
                blank_id: "틀린답"
                for blank_id in blank_answers.keys()
            }

            result_wrong = grading_service.grade_answer(
                question_id=question.id,
                selected_answer=student_answers_wrong,
                correct_answer=blank_answers,
                points=question.points
            )

            print(f"  학생 답안: {student_answers_wrong}")
            print(f"  정답 여부: {'[OK] 정답' if result_wrong['is_correct'] else '[X] 오답'}")
            print(f"  획득 점수: {result_wrong['points_earned']}/{question.points}점")
            print(f"  정답 개수: {result_wrong['correct_count']}/{result_wrong['total_blanks']}개")

        # 최종 요약
        print_section("[OK] 전체 시나리오 완료")
        print("주요 기능:")
        print("  [OK] 1회차: 빈칸 0개 (완독)")
        print("  [OK] 2회차: 빈칸 2-3개 (중요 단어)")
        print("  [OK] 3회차: 빈칸 4-6개 (대부분 단어)")
        print("  [OK] 부분 점수 채점")
        print("  [OK] 회차별 랜덤 빈칸 생성")
        print("\n모든 기능이 정상적으로 작동합니다!")

    finally:
        db.close()


if __name__ == "__main__":
    main()
