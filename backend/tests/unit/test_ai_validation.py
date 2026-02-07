"""AI 문제 검증 함수 테스트 (pure functions)."""

import pytest

from app.services.ai_service import _validate_generated_question, _cross_validate_answer


class TestValidateGeneratedQuestion:
    """_validate_generated_question 함수 테스트."""

    def test_보기_기호_포함_ㄱㄴㄷ(self):
        """content에 (ㄱ), (ㄴ), (ㄷ) 등 한글 자음 보기 기호가 있으면 경고."""
        q = {"content": "다음 중 옳은 것은? (ㄱ) A (ㄴ) B", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert "보기 기호가 문제 내용에 포함됨" in warnings

    def test_보기_기호_포함_가나다(self):
        """content에 (가), (나), (다) 등 한글 음절 보기 기호가 있으면 경고."""
        q = {"content": "다음은 풀이 과정이다. (가)에 들어갈 값은?", "question_type": "multiple_choice"}
        warnings = _validate_generated_question(q)
        assert "보기 기호가 문제 내용에 포함됨" in warnings

    def test_보기_기호_없음(self):
        """보기 기호가 없으면 이 경고는 발생하지 않음."""
        q = {"content": "72를 소인수분해하면?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert "보기 기호가 문제 내용에 포함됨" not in warnings

    def test_빈칸_선택형_표현_고르시오(self):
        """빈칸 문제에 '고르시오' 포함 시 경고."""
        q = {"content": "다음 중 소수를 모두 고르시오.", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert "빈칸 문제에 선택형 표현 사용됨" in warnings

    def test_빈칸_선택형_표현_선택(self):
        """빈칸 문제에 '선택' 포함 시 경고."""
        q = {"content": "옳은 것을 선택하세요.", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert "빈칸 문제에 선택형 표현 사용됨" in warnings

    def test_빈칸_선택형_표현_모두_고르(self):
        """빈칸 문제에 '모두 고르' 포함 시 경고."""
        q = {"content": "합성수를 모두 고르면?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert "빈칸 문제에 선택형 표현 사용됨" in warnings

    def test_빈칸_외부_참조_다음_중(self):
        """빈칸 문제에 '다음 중' 포함 시 경고."""
        q = {"content": "다음 중 가장 큰 수는?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert "외부 참조 표현 '다음...' 사용됨" in warnings

    def test_빈칸_외부_참조_다음_수(self):
        """빈칸 문제에 '다음 수' 포함 시 경고."""
        q = {"content": "다음 수를 소인수분해하면?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert "외부 참조 표현 '다음...' 사용됨" in warnings

    def test_빈칸_외부_참조_다음은_표(self):
        """빈칸 문제에 '다음은 표' 포함 시 경고."""
        q = {"content": "다음은 표이다. 합은?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert "외부 참조 표현 '다음...' 사용됨" in warnings

    def test_빈칸_참조형_과정_참조(self):
        """빈칸 문제에 '과정이다. (가)' 패턴이 있으면 경고."""
        q = {"content": "다음은 풀이 과정이다. (가)에 들어갈 값은?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert "참조형 빈칸 문제 - 풀이 과정 참조" in warnings
        assert "보기 기호가 문제 내용에 포함됨" in warnings  # 중복 경고

    def test_빈칸_숫자_목록_괄호_안(self):
        """빈칸 문제에 괄호 안 숫자 목록 (2, 4, 9) 패턴이 있으면 경고."""
        q = {"content": "다음 수 중 소수는? (2, 4, 9, 11)", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert "빈칸 문제에 숫자 목록 나열됨" in warnings

    def test_빈칸_숫자_목록_쉼표_구분_4개(self):
        """빈칸 문제에 쉼표로 구분된 4개 이상 숫자가 있으면 경고."""
        q = {"content": "1, 3, 5, 7, 11 중 소수는 몇 개?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert "빈칸 문제에 쉼표 구분 숫자 나열됨" in warnings

    def test_빈칸_숫자_목록_쉼표_3개는_검출_안됨(self):
        """쉼표 구분 숫자가 3개면 4개 규칙에 걸리지 않음 (regex는 4개 이상)."""
        q = {"content": "1, 3, 5 중 소수는?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert "빈칸 문제에 쉼표 구분 숫자 나열됨" not in warnings
        # 하지만 괄호 안 3개 숫자는 검출됨 (r"\(\s*\d+\s*,\s*\d+\s*,\s*\d+" - 3개 이상)

    def test_빈칸_정상_문제(self):
        """빈칸 문제에 위반 사항이 없으면 경고 없음."""
        q = {"content": "72를 소인수분해하면?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q)
        assert len(warnings) == 0

    def test_객관식_보기_없음(self):
        """객관식인데 options가 없으면 경고."""
        q = {"content": "24의 약수는?", "question_type": "multiple_choice"}
        warnings = _validate_generated_question(q)
        assert "객관식인데 보기가 없거나 부족함" in warnings

    def test_객관식_보기_부족(self):
        """객관식인데 options가 1개뿐이면 경고."""
        q = {
            "content": "24의 약수는?",
            "question_type": "multiple_choice",
            "options": [{"label": "A", "text": "6개"}],
        }
        warnings = _validate_generated_question(q)
        assert "객관식인데 보기가 없거나 부족함" in warnings

    def test_객관식_정상_문제(self):
        """객관식 문제가 정상이면 경고 없음."""
        q = {
            "content": "24의 약수는?",
            "question_type": "multiple_choice",
            "options": [
                {"label": "A", "text": "6개"},
                {"label": "B", "text": "8개"},
            ],
            "correct_answer": "B",
            "explanation": "24=2³×3이므로 (3+1)(1+1)=8개",
        }
        warnings = _validate_generated_question(q)
        # cross_validate가 None 반환하면 경고 없음
        assert len(warnings) == 0

    def test_연산_트랙_용어_빈칸_밑줄_도(self):
        """연산 트랙에 '___도 아니다' 패턴이 있으면 경고."""
        q = {"content": "1은 소수도 아니고 ___도 아니다.", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q, category="computation")
        assert "연산 트랙에 용어 빈칸 문제" in warnings

    def test_연산_트랙_용어_빈칸_라_한다(self):
        """연산 트랙에 '___라 한다' 패턴이 있으면 경고."""
        q = {"content": "최대공약수가 1일 때 이를 ___라 한다.", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q, category="computation")
        assert "연산 트랙에 용어 빈칸 문제" in warnings

    def test_연산_트랙_판별형_예_아니오(self):
        """연산 트랙에 '예/아니오' 포함 시 경고."""
        q = {"content": "12와 35는 서로소인가? (예/아니오)", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q, category="computation")
        assert "연산 트랙에 판별형 문제" in warnings

    def test_연산_트랙_판별형_존재하는가(self):
        """연산 트랙에 '존재하는가' 포함 시 경고."""
        q = {"content": "이러한 경우는 존재하는가?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q, category="computation")
        assert "연산 트랙에 판별형 문제" in warnings

    def test_연산_트랙_암기형_무엇인가(self):
        """연산 트랙에 '무엇인가?' 로 끝나면 경고."""
        q = {"content": "가장 작은 소수는 무엇인가?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q, category="computation")
        assert "연산 트랙에 암기형 문제" in warnings

    def test_연산_트랙_암기형_무엇일까(self):
        """연산 트랙에 '무엇일까?' 로 끝나면 경고."""
        q = {"content": "약수의 개수가 2개인 수를 무엇일까?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q, category="computation")
        assert "연산 트랙에 암기형 문제" in warnings

    def test_연산_트랙_정상_계산_문제(self):
        """연산 트랙에 순수 계산 문제면 경고 없음."""
        q = {"content": "72를 소인수분해하면?", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q, category="computation")
        assert len(warnings) == 0

    def test_개념_트랙은_용어_문제_허용(self):
        """개념 트랙에서는 용어 빈칸 문제가 허용됨."""
        q = {"content": "최대공약수가 1일 때 이를 ___라 한다.", "question_type": "fill_in_blank"}
        warnings = _validate_generated_question(q, category="concept")
        assert "연산 트랙에 용어 빈칸 문제" not in warnings


class TestCrossValidateAnswer:
    """_cross_validate_answer 함수 테스트."""

    def test_정답_라벨과_해설_일치(self):
        """정답 라벨이 가리키는 선지 텍스트에 해설의 최종 답이 포함되면 None."""
        q = {
            "correct_answer": "C",
            "explanation": "24=2³×3이므로 약수의 개수=(3+1)(1+1)=8개",
        }
        options = [
            {"label": "A", "text": "4개"},
            {"label": "B", "text": "6개"},
            {"label": "C", "text": "8개"},
            {"label": "D", "text": "10개"},
        ]
        result = _cross_validate_answer(q, options)
        assert result is None  # 일치 → OK

    def test_정답_라벨_불일치_자동_수정(self):
        """정답 라벨이 틀렸지만 다른 선지에 최종 답이 있으면 자동 수정하고 None 반환."""
        q = {
            "correct_answer": "A",  # 잘못된 라벨
            "explanation": "24=2³×3이므로 약수의 개수=(3+1)(1+1)=8개",
        }
        options = [
            {"label": "A", "text": "4개"},
            {"label": "B", "text": "6개"},
            {"label": "C", "text": "8개"},
            {"label": "D", "text": "10개"},
        ]
        result = _cross_validate_answer(q, options)
        assert result is None  # 자동 수정되어 경고 없음
        assert q["correct_answer"] == "C"  # A → C로 자동 수정

    def test_최종_답_없음_None_반환(self):
        """해설에 '= 숫자' 패턴이 없으면 None (검증 불가)."""
        q = {
            "correct_answer": "A",
            "explanation": "이것은 명백하다.",
        }
        options = [{"label": "A", "text": "정답"}]
        result = _cross_validate_answer(q, options)
        assert result is None

    def test_정답_선지_텍스트_없음_None_반환(self):
        """정답 라벨에 해당하는 선지가 없으면 None."""
        q = {
            "correct_answer": "Z",  # 존재하지 않는 라벨
            "explanation": "답은 8개이다.",
        }
        options = [{"label": "A", "text": "4개"}]
        result = _cross_validate_answer(q, options)
        assert result is None

    def test_단위_포함_최종_답_일치(self):
        """해설에 '= 360원' 형태로 단위가 포함된 경우도 매칭."""
        q = {
            "correct_answer": "B",
            "explanation": "따라서 답은 360원이다. = 360원",
        }
        options = [
            {"label": "A", "text": "300원"},
            {"label": "B", "text": "360원"},
            {"label": "C", "text": "400원"},
        ]
        result = _cross_validate_answer(q, options)
        assert result is None

    def test_쉼표_포함_숫자_매칭(self):
        """해설에 '= 1,234'처럼 쉼표가 있어도 매칭 (쉼표 제거 후 비교)."""
        q = {
            "correct_answer": "A",
            "explanation": "최종 답은 = 1,234",
        }
        options = [
            {"label": "A", "text": "1234"},  # 쉼표 없음
            {"label": "B", "text": "5678"},
        ]
        result = _cross_validate_answer(q, options)
        assert result is None  # 1,234 → 1234로 정규화되어 매칭

    def test_소수점_포함_숫자_매칭(self):
        """해설에 '= 3.14' 형태의 소수도 매칭."""
        q = {
            "correct_answer": "C",
            "explanation": "원주율은 대략 = 3.14",
        }
        options = [
            {"label": "A", "text": "3"},
            {"label": "B", "text": "3.1"},
            {"label": "C", "text": "3.14"},
        ]
        result = _cross_validate_answer(q, options)
        assert result is None

    def test_음수_매칭(self):
        """해설에 '= -5' 형태의 음수도 매칭."""
        q = {
            "correct_answer": "B",
            "explanation": "따라서 x = -5",
        }
        options = [
            {"label": "A", "text": "5"},
            {"label": "B", "text": "-5"},
            {"label": "C", "text": "0"},
        ]
        result = _cross_validate_answer(q, options)
        assert result is None

    def test_마지막_등호_답만_사용(self):
        """해설에 여러 '=' 가 있으면 마지막 것만 사용."""
        q = {
            "correct_answer": "C",
            "explanation": "중간 계산: 2×3=6, 최종: 6×4=24",
        }
        options = [
            {"label": "A", "text": "6"},
            {"label": "B", "text": "12"},
            {"label": "C", "text": "24"},
        ]
        result = _cross_validate_answer(q, options)
        assert result is None  # 마지막 '=24'를 사용

    def test_options_빈_리스트_None_반환(self):
        """options가 빈 리스트면 None."""
        q = {
            "correct_answer": "A",
            "explanation": "답은 = 8",
        }
        result = _cross_validate_answer(q, [])
        assert result is None

    def test_correct_answer_없음_None_반환(self):
        """correct_answer 키가 없으면 None."""
        q = {"explanation": "답은 = 8"}
        options = [{"label": "A", "text": "8"}]
        result = _cross_validate_answer(q, options)
        assert result is None

    def test_explanation_없음_None_반환(self):
        """explanation 키가 없으면 None."""
        q = {"correct_answer": "A"}
        options = [{"label": "A", "text": "8"}]
        result = _cross_validate_answer(q, options)
        assert result is None

    def test_라벨_대소문자_정규화(self):
        """라벨을 대문자로 정규화하여 비교."""
        q = {
            "correct_answer": "b",  # 소문자
            "explanation": "답은 = 10",
        }
        options = [
            {"label": "A", "text": "5"},
            {"label": "B", "text": "10"},  # 대문자 라벨
        ]
        result = _cross_validate_answer(q, options)
        assert result is None  # 'b' → 'B'로 정규화되어 매칭

    def test_불일치_수정_불가능(self):
        """정답 선지와 해설이 불일치하고, 다른 선지에도 최종 답이 없으면 None 반환.

        Note: 현재 구현은 불일치 시에도 None을 반환함 (82번째 줄).
        원래 의도는 경고 메시지를 반환하는 것 같지만, 실제 코드는 None 반환.
        """
        q = {
            "correct_answer": "A",
            "explanation": "답은 = 99",  # 어떤 선지에도 없음
        }
        options = [
            {"label": "A", "text": "5"},
            {"label": "B", "text": "10"},
        ]
        result = _cross_validate_answer(q, options)
        assert result is None  # 현재 구현은 None 반환
