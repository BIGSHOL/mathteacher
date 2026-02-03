"""빈칸 채우기 기능 API 테스트 시나리오."""

import requests
import json
from typing import Dict, Any

# API 베이스 URL (Railway 또는 로컬)
BASE_URL = "http://localhost:8000"  # 로컬 테스트용
# BASE_URL = "https://your-railway-app.railway.app"  # 프로덕션용

class FillInBlankAPITester:
    """빈칸 채우기 API 테스트 클래스."""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.access_token = None
        self.student_id = None
        self.test_id = None
        self.attempt_ids = []

    def print_section(self, title: str):
        """섹션 제목 출력."""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")

    def print_result(self, success: bool, message: str, data: Any = None):
        """결과 출력."""
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {message}")
        if data:
            print(f"  Data: {json.dumps(data, indent=2, ensure_ascii=False)}")

    def login(self, email: str = "student@test.com", password: str = "test1234") -> bool:
        """로그인."""
        self.print_section("1. 로그인")

        try:
            response = requests.post(
                f"{self.base_url}/api/v1/auth/login",
                json={"email": email, "password": password}
            )

            if response.status_code == 200:
                data = response.json()["data"]
                self.access_token = data["access_token"]
                self.student_id = data["user"]["id"]
                self.print_result(True, "로그인 성공", {
                    "user_id": self.student_id,
                    "name": data["user"]["name"],
                    "role": data["user"]["role"]
                })
                return True
            else:
                self.print_result(False, f"로그인 실패: {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        except Exception as e:
            self.print_result(False, f"로그인 오류: {str(e)}")
            return False

    def get_headers(self) -> Dict[str, str]:
        """인증 헤더 생성."""
        return {"Authorization": f"Bearer {self.access_token}"}

    def create_test_with_fill_in_blank(self) -> bool:
        """빈칸 채우기 문제가 포함된 테스트 생성."""
        self.print_section("2. 빈칸 채우기 테스트 생성")

        # 실제로는 teacher 계정으로 로그인하여 테스트를 생성해야 하지만,
        # 여기서는 이미 생성된 빈칸 채우기 문제가 있다고 가정하고 테스트 목록 조회
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/tests",
                headers=self.get_headers()
            )

            if response.status_code == 200:
                tests = response.json()["data"]
                # 빈칸 채우기 문제가 포함된 테스트 찾기
                for test in tests:
                    if "빈칸" in test.get("title", "") or "개념" in test.get("title", ""):
                        self.test_id = test["id"]
                        self.print_result(True, f"테스트 발견: {test['title']}", {
                            "test_id": self.test_id,
                            "question_count": test.get("question_count", 0)
                        })
                        return True

                # 빈칸 테스트가 없으면 첫 번째 테스트 사용
                if tests:
                    self.test_id = tests[0]["id"]
                    self.print_result(True, f"테스트 사용: {tests[0]['title']}", {
                        "test_id": self.test_id
                    })
                    return True
                else:
                    self.print_result(False, "사용 가능한 테스트가 없습니다")
                    return False
            else:
                self.print_result(False, f"테스트 조회 실패: {response.status_code}")
                return False
        except Exception as e:
            self.print_result(False, f"테스트 생성 오류: {str(e)}")
            return False

    def start_attempt(self, round_num: int) -> Dict[str, Any] | None:
        """테스트 시도 시작."""
        self.print_section(f"{round_num + 2}. {round_num}회차 시도 시작")

        try:
            response = requests.post(
                f"{self.base_url}/api/v1/tests/{self.test_id}/start",
                headers=self.get_headers()
            )

            if response.status_code == 200:
                data = response.json()["data"]
                attempt_id = data["attempt_id"]
                self.attempt_ids.append(attempt_id)

                # 첫 번째 문제 확인
                questions = data.get("questions", [])
                if questions:
                    first_q = questions[0]

                    result_data = {
                        "attempt_id": attempt_id,
                        "total_questions": len(questions)
                    }

                    # 빈칸 채우기 문제인 경우
                    if first_q.get("question_type") == "fill_in_blank":
                        blank_config = first_q.get("blank_config", {})
                        blank_answers = blank_config.get("blank_answers", {})
                        display_content = blank_config.get("display_content", "")

                        result_data.update({
                            "question_type": "fill_in_blank",
                            "blank_count": len(blank_answers),
                            "display_preview": display_content[:100] + "..." if len(display_content) > 100 else display_content,
                            "blanks": list(blank_answers.keys())
                        })

                        expected_blanks = {
                            1: 0,   # 1회차: 빈칸 없음
                            2: (2, 3),  # 2회차: 2-3개
                            3: (4, 6)   # 3회차: 4-6개
                        }

                        if round_num in expected_blanks:
                            exp = expected_blanks[round_num]
                            if isinstance(exp, int):
                                is_correct = len(blank_answers) == exp
                            else:
                                is_correct = exp[0] <= len(blank_answers) <= exp[1]

                            result_data["expected_blanks"] = exp
                            result_data["validation"] = "PASS" if is_correct else "FAIL"
                    else:
                        result_data["question_type"] = first_q.get("question_type", "unknown")

                    self.print_result(True, f"{round_num}회차 시작 성공", result_data)
                    return data
                else:
                    self.print_result(False, "문제가 없습니다")
                    return None
            else:
                self.print_result(False, f"시도 시작 실패: {response.status_code}")
                print(f"  Response: {response.text}")
                return None
        except Exception as e:
            self.print_result(False, f"시도 시작 오류: {str(e)}")
            return None

    def submit_answer(self, attempt_id: str, question_id: str,
                     answer: str | Dict[str, str], round_num: int) -> bool:
        """답안 제출."""
        self.print_section(f"{round_num + 5}. {round_num}회차 답안 제출")

        try:
            response = requests.post(
                f"{self.base_url}/api/v1/tests/attempts/{attempt_id}/submit",
                headers=self.get_headers(),
                json={
                    "question_id": question_id,
                    "selected_answer": answer,
                    "time_spent_seconds": 10
                }
            )

            if response.status_code == 200:
                data = response.json()["data"]

                result_data = {
                    "is_correct": data.get("is_correct"),
                    "points_earned": data.get("points_earned"),
                    "current_score": data.get("current_score")
                }

                # 부분 점수 정보 (빈칸 채우기)
                if "correct_count" in data:
                    result_data["correct_count"] = data["correct_count"]
                    result_data["total_blanks"] = data["total_blanks"]

                self.print_result(True, "답안 제출 성공", result_data)
                return True
            else:
                self.print_result(False, f"답안 제출 실패: {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        except Exception as e:
            self.print_result(False, f"답안 제출 오류: {str(e)}")
            return False

    def complete_attempt(self, attempt_id: str, round_num: int) -> bool:
        """테스트 완료."""
        self.print_section(f"{round_num + 6}. {round_num}회차 완료")

        try:
            response = requests.post(
                f"{self.base_url}/api/v1/tests/attempts/{attempt_id}/complete",
                headers=self.get_headers()
            )

            if response.status_code == 200:
                data = response.json()["data"]
                self.print_result(True, "테스트 완료", {
                    "final_score": data.get("score"),
                    "max_score": data.get("max_score"),
                    "correct_count": data.get("correct_count"),
                    "total_count": data.get("total_count"),
                    "xp_earned": data.get("xp_earned")
                })
                return True
            else:
                self.print_result(False, f"테스트 완료 실패: {response.status_code}")
                return False
        except Exception as e:
            self.print_result(False, f"테스트 완료 오류: {str(e)}")
            return False

    def run_full_scenario(self):
        """전체 시나리오 실행."""
        print("\n" + "="*60)
        print("  빈칸 채우기 기능 전체 시나리오 테스트")
        print("="*60)

        # 1. 로그인
        if not self.login():
            return

        # 2. 테스트 찾기/생성
        if not self.create_test_with_fill_in_blank():
            return

        # 3-5. 각 회차별 테스트
        for round_num in [1, 2, 3]:
            # 시도 시작
            attempt_data = self.start_attempt(round_num)
            if not attempt_data:
                continue

            attempt_id = attempt_data["attempt_id"]
            questions = attempt_data.get("questions", [])

            if not questions:
                continue

            # 첫 번째 문제만 답안 제출 (데모용)
            first_q = questions[0]
            question_id = first_q["id"]

            # 빈칸 채우기 문제인 경우
            if first_q.get("question_type") == "fill_in_blank":
                blank_config = first_q.get("blank_config", {})
                blank_answers = blank_config.get("blank_answers", {})

                # 정답 제출 (테스트용)
                student_answer = {
                    blank_id: data["answer"]
                    for blank_id, data in blank_answers.items()
                }

                self.submit_answer(attempt_id, question_id, student_answer, round_num)
            else:
                # 일반 문제는 첫 번째 선택지 선택
                if first_q.get("options"):
                    self.submit_answer(attempt_id, question_id,
                                     first_q["options"][0]["label"], round_num)

            # 테스트 완료
            self.complete_attempt(attempt_id, round_num)

        # 최종 요약
        self.print_section("최종 요약")
        print(f"✓ 총 {len(self.attempt_ids)}회 시도 완료")
        print(f"  시도 ID: {', '.join(self.attempt_ids[:3])}")
        print("\n테스트 완료!")


if __name__ == "__main__":
    # 테스트 실행
    tester = FillInBlankAPITester()
    tester.run_full_scenario()
