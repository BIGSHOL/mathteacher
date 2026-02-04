"""MC 문제에서 빈칸 채우기(FB) 문제를 자동 파생하는 서비스."""

import re
import logging

logger = logging.getLogger(__name__)

# 한국어 수학 핵심 용어 패턴 (2글자 이상만, 조사/어미 매칭 방지)
_CONCEPT_NAMES = (
    r"소인수분해|소인수|소수|합성수|"
    r"약수|배수|최대공약수|최소공배수|공약수|공배수|"
    r"약분|통분|기약분수|가분수|대분수|진분수|"
    r"정비례|반비례|비례식|비례|비율|"
    r"합동|대칭|선대칭|점대칭|대칭축|"
    r"동위각|엇각|맞꼭지각|"
    r"평균|중앙값|최빈값|분산|표준편차|상대도수|도수|계급값|"
    r"좌표평면|사분면|원점|좌표|순서쌍|"
    r"방정식|부등식|등식|미지수|"
    r"동류항|계수|상수항|차수|"
    r"대입|이항|전개|인수분해|"
    r"유리수|정수|자연수|양수|음수|실수|무리수|"
    r"받아올림|받아내림|올림|내림|몫|나머지|"
    r"제곱근|거듭제곱|지수|"
    r"함수|그래프|기울기|절편|교점|"
    r"확률|경우의 수|"
    r"중심각|원주각|접선|현|호"
)

_SHAPE_NAMES = (
    r"정삼각형|이등변삼각형|직각삼각형|삼각형|"
    r"평행사변형|마름모|사다리꼴|직사각형|정사각형|사각형|"
    r"정다각형|다각형|"
    r"원기둥|원뿔|각기둥|각뿔|직육면체|정육면체|"
    r"부채꼴|반원"
)

_FORMULA_PARTS = (
    r"밑변|높이|반지름|지름|둘레|넓이|부피|겉넓이|"
    r"모선|호의 길이|"
    r"모서리|꼭짓점|대각선|"
    r"내각|외각|"
    r"분모|분자|"
    r"자릿값|일의 자리|십의 자리|백의 자리"
)

# 컴파일된 패턴 — 단어 경계를 위해 앞뒤에 한글 어미/조사가 바로 붙지 않도록 체크
_PATTERNS = [
    ("concept", re.compile(f"({_CONCEPT_NAMES})", re.UNICODE)),
    ("shape", re.compile(f"({_SHAPE_NAMES})", re.UNICODE)),
    ("formula", re.compile(f"({_FORMULA_PARTS})", re.UNICODE)),
    ("number", re.compile(r"(?<![a-zA-Z\d])(\d+(?:\.\d+)?(?:/\d+)?)(?![a-zA-Z\d])")),
]

# 숫자 결과를 나타내는 패턴: "= 42", "= 8개" 등
_RESULT_PATTERN = re.compile(r"=\s*(\d+(?:\.\d+)?(?:/\d+)?)\s*(?:개|명|cm|m|kg|g|L|mL|°|도|원)?")

# 한글 어미/조사 (이것들이 바로 뒤에 오면 용어가 아닌 동사/형용사 어미)
_VERB_SUFFIXES = re.compile(r"^(하|해|한|할|합|했|하면|하고|하는|하여|되|된|될|되면|이다|이고|인)")

# 선지 의존형 MC 패턴 — 이런 문제는 FB로 변환하면 선지가 없어 무의미
_OPTIONS_DEPENDENT = re.compile(
    r"다음 중|다음 보기|보기 중|"
    r"어느 것|어떤 것|"
    r"짝지어진|짝 지어진|"
    r"골라|고르시오|고르세요|고른 것|"
    r"선택하시오|선택하세요|"
    r"알맞은 것은|알맞은 것을|"
    r"무엇입니까|무엇인가요|무엇일까요|"
    r"것을 찾|것은 무엇|것을 모두",
    re.UNICODE,
)

# Yes/No 유사 답변 매핑
_YES_VARIANTS = ["네", "예", "있습니다", "있어요", "있음", "맞습니다", "맞아요", "필요합니다", "필요해요", "필요함"]
_NO_VARIANTS = ["아니요", "아니오", "없습니다", "없어요", "없음", "아닙니다", "필요없습니다", "필요없음"]

# 단순 사칙연산 줄 패턴 (예: "382 + 149 = 531 입니다", "13-7=6")
# 이런 줄은 빈칸 처리해도 단순 계산 문제밖에 안 됨
_TRIVIAL_CALC_LINE = re.compile(
    r'^[\s\d+\-×÷*/=().,:\s]+(?:입니다|이다|이므로|이에요)?[.\s]*$',
    re.UNICODE,
)


class FBDerivationService:
    """MC 문제에서 FB 변형 문제를 자동 파생."""

    def derive_from_mc(
        self,
        mc_question: dict,
        max_variants: int = 3,
    ) -> list[dict]:
        """MC 문제에서 FB 변형 문제들을 생성."""
        correct_text = ""
        correct_label = mc_question.get("correct_answer", "")
        options = mc_question.get("options") or []
        for opt in options:
            if isinstance(opt, dict) and opt.get("label") == correct_label:
                correct_text = opt.get("text", "")
                break

        explanation = mc_question.get("explanation", "")
        content = mc_question.get("content", "")

        # 선지 의존형 MC는 FB 변환 완전 차단
        # ("다음 중", "고르세요", "무엇입니까" 등 — 선지 없이 의미 없음)
        if _OPTIONS_DEPENDENT.search(content):
            return []

        variants: list[dict] = []
        mc_id = mc_question.get("id", "unknown")

        # === 전략 1: 정답 선지를 빈칸으로 (최우선) ===
        # 순수 숫자 정답은 FB에서 문맥 없이 추론 불가 → 스킵
        if correct_text and len(correct_text) >= 2:
            is_pure_number = bool(re.match(
                r'^\d+(?:\.\d+)?(?:/\d+)?$', correct_text.strip()
            ))
            if not is_pure_number:
                fb = self._create_answer_blank(mc_question, correct_text, 0, mc_id)
                if fb:
                    variants.append(fb)

        # === 전략 2: 해설 속 계산 결과(= N) 빈칸 ===
        result_blanks = self._extract_calculation_results(explanation)
        for rb in result_blanks:
            if len(variants) >= max_variants:
                break
            fb = self._create_result_blank(mc_question, rb, len(variants), mc_id)
            if fb:
                variants.append(fb)

        # === 전략 3: 해설 속 핵심 수학 용어 빈칸 ===
        # 숫자 유형은 전략 2에서 이미 처리하므로 개념/도형/공식 용어만 빈칸 처리
        if len(variants) < max_variants:
            terms = self._extract_key_terms(explanation)
            for term_info in terms:
                if len(variants) >= max_variants:
                    break
                if term_info["type"] == "number":
                    continue
                used_answers = {v.get("correct_answer", "") for v in variants}
                if term_info["term"] in used_answers:
                    continue
                fb = self._create_term_blank(mc_question, term_info, len(variants), mc_id)
                if fb:
                    variants.append(fb)

        return variants

    def _create_answer_blank(
        self, mc: dict, correct_text: str, idx: int, mc_id: str
    ) -> dict | None:
        """정답 선지를 빈칸으로 만든 FB 문제."""
        content = mc.get("content", "")
        fb_content = f"{content}\n\n정답: ____"

        # Yes/No 유형 답변이면 유사 표현 모두 허용
        accept = self._build_yesno_accept(correct_text)

        return self._build_fb_dict(
            mc, fb_content, correct_text, idx, mc_id,
            difficulty_delta=0, accept_formats=accept
        )

    @staticmethod
    def _build_yesno_accept(answer: str) -> list[str]:
        """답변이 긍정/부정 표현이면 유사 표현 목록 반환."""
        answer_lower = answer.strip().rstrip(".")
        # 긍정 표현 감지
        for v in _YES_VARIANTS:
            if v in answer_lower or answer_lower in v:
                return list(set([answer] + _YES_VARIANTS))
        # 부정 표현 감지
        for v in _NO_VARIANTS:
            if v in answer_lower or answer_lower in v:
                return list(set([answer] + _NO_VARIANTS))
        return [answer]

    def _extract_calculation_results(self, explanation: str) -> list[dict]:
        """해설에서 '= 숫자' 패턴의 계산 결과를 추출."""
        results = []
        seen = set()
        for match in _RESULT_PATTERN.finditer(explanation):
            num_str = match.group(1)
            if num_str in seen or len(num_str) <= 1:
                continue
            seen.add(num_str)
            results.append({
                "number": num_str,
                "full_match": match.group(0),
                "start": match.start(),
                "end": match.end(),
            })
        return results

    @staticmethod
    def _get_line_at(text: str, pos: int) -> str:
        """텍스트에서 pos 위치가 포함된 줄을 반환."""
        line_start = text.rfind('\n', 0, pos) + 1
        line_end = text.find('\n', pos)
        if line_end == -1:
            line_end = len(text)
        return text[line_start:line_end]

    def _create_result_blank(
        self, mc: dict, result_info: dict, idx: int, mc_id: str
    ) -> dict | None:
        """해설의 계산 결과를 빈칸으로 만든 FB 문제."""
        explanation = mc.get("explanation", "")
        content = mc.get("content", "")
        number = result_info["number"]

        # 해당 줄이 단순 사칙연산이면 스킵 (예: "382 + 149 = 531 입니다")
        line = self._get_line_at(explanation, result_info["start"])
        if _TRIVIAL_CALC_LINE.match(line.strip()):
            return None

        # "= 42" → "= ____" 로 교체
        full = result_info["full_match"]
        blanked = full.replace(number, "____", 1)
        fb_explanation = explanation.replace(full, blanked, 1)

        # 원래 해설과 같으면 스킵
        if fb_explanation == explanation:
            return None

        # 원본 문제 + 빈칸 풀이로 문맥 제공
        fb_content = f"{content}\n\n[풀이]\n{fb_explanation}"

        accept = [number]
        try:
            num = float(number)
            if num == int(num):
                accept.append(str(int(num)))
                if str(int(num)) != number:
                    accept.append(str(num))
        except ValueError:
            pass

        return self._build_fb_dict(
            mc, fb_content, number, idx, mc_id,
            difficulty_delta=1, accept_formats=accept
        )

    def _extract_key_terms(self, explanation: str) -> list[dict]:
        """해설에서 핵심 수학 용어만 추출 (동사 어미 매칭 방지)."""
        all_terms: list[dict] = []
        priority_map = {"concept": 0, "shape": 1, "formula": 2, "number": 3}

        for term_type, pattern in _PATTERNS:
            for match in pattern.finditer(explanation):
                term = match.group(1)

                # 2글자 미만 스킵
                if len(term) < 2:
                    continue

                # 숫자는 2자리 이상만
                if term_type == "number" and len(term) <= 1:
                    continue

                # 한글 용어의 경우, 뒤에 동사 어미가 바로 오면 스킵
                # 예: "적용해" → "해"가 매칭되지만 "적용" + "해"이므로 스킵
                end_pos = match.end()
                remaining = explanation[end_pos:]
                if remaining and _VERB_SUFFIXES.match(remaining):
                    continue

                # 앞에 한글이 바로 붙어있으면 스킵 (부분 매칭 방지)
                start_pos = match.start()
                if start_pos > 0:
                    prev_char = explanation[start_pos - 1]
                    if '\uac00' <= prev_char <= '\ud7a3':  # 한글 음절
                        continue

                all_terms.append({
                    "term": term,
                    "type": term_type,
                    "priority": priority_map.get(term_type, 99),
                    "start": match.start(),
                    "end": match.end(),
                })

        # 우선순위 정렬, 같은 우선순위면 긴 것 우선
        all_terms.sort(key=lambda t: (t["priority"], -len(t["term"])))

        # 중복 제거
        seen = set()
        unique = []
        for t in all_terms:
            if t["term"] not in seen:
                seen.add(t["term"])
                unique.append(t)
        return unique

    def _create_term_blank(
        self, mc: dict, term_info: dict, idx: int, mc_id: str
    ) -> dict | None:
        """해설 내 수학 용어를 빈칸으로 만든 FB 문제."""
        term = term_info["term"]
        explanation = mc.get("explanation", "")
        content = mc.get("content", "")

        if term not in explanation:
            return None

        fb_explanation = explanation.replace(term, "____", 1)
        if fb_explanation == explanation:
            return None

        # 원본 문제 + 빈칸 풀이로 문맥 제공
        fb_content = f"{content}\n\n[풀이]\n{fb_explanation}"

        accept = [term]

        return self._build_fb_dict(
            mc, fb_content, term, idx, mc_id,
            difficulty_delta=1, accept_formats=accept
        )

    def _build_fb_dict(
        self,
        mc: dict,
        content: str,
        answer: str,
        idx: int,
        mc_id: str,
        difficulty_delta: int = 0,
        accept_formats: list[str] | None = None,
    ) -> dict:
        """FB 문제 dict 생성."""
        difficulty = mc.get("difficulty", 5)
        difficulty = max(1, min(10, difficulty + difficulty_delta))
        accept = accept_formats or [answer]

        return {
            "id": f"fb-{mc_id}-{idx + 1:02d}",
            "concept_id": mc.get("concept_id", ""),
            "category": mc.get("category", "concept"),
            "part": mc.get("part", "calc"),
            "question_type": "fill_in_blank",
            "difficulty": difficulty,
            "content": content,
            "options": None,
            "correct_answer": answer,
            "explanation": mc.get("explanation", ""),
            "points": mc.get("points", 10),
            "blank_config": {
                "blank_count": 1,
                "accept_formats": accept,
            },
            "is_active": True,
            "source_question_id": mc_id,
        }
