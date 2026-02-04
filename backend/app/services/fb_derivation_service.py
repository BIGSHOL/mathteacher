"""MC 문제에서 빈칸 채우기(FB) 문제를 자동 파생하는 서비스."""

import re
import logging
from uuid import uuid4

logger = logging.getLogger(__name__)

# 한국어 수학 핵심 용어 패턴 (중요도 순)
_CONCEPT_NAMES = (
    r"소인수분해|소인수|소수|합성수|"
    r"약수|배수|최대공약수|최소공배수|공약수|공배수|"
    r"약분|통분|기약분수|가분수|대분수|진분수|"
    r"정비례|반비례|비례식|비례|비율|"
    r"합동|대칭|선대칭|점대칭|대칭축|"
    r"동위각|엇각|맞꼭지각|"
    r"평균|중앙값|최빈값|분산|표준편차|상대도수|도수|계급값|"
    r"좌표평면|사분면|원점|좌표|순서쌍|"
    r"방정식|부등식|등식|미지수|해|"
    r"동류항|계수|상수항|차수|항|"
    r"대입|이항|전개|인수분해|"
    r"양의 정수|음의 정수|유리수|정수|자연수"
)

_SHAPE_NAMES = (
    r"정삼각형|이등변삼각형|직각삼각형|삼각형|"
    r"평행사변형|마름모|사다리꼴|직사각형|정사각형|사각형|"
    r"정다각형|다각형|"
    r"원기둥|원뿔|각뿔|직육면체|정육면체|구|"
    r"부채꼴|원|반원"
)

_FORMULA_PARTS = (
    r"밑변|높이|반지름|지름|둘레|넓이|부피|겉넓이|"
    r"모선|호의 길이|중심각|"
    r"면|모서리|꼭짓점|대각선|"
    r"기울기|절편|"
    r"내각|외각"
)

_PATTERNS = [
    ("concept", re.compile(f"({_CONCEPT_NAMES})", re.UNICODE)),
    ("shape", re.compile(f"({_SHAPE_NAMES})", re.UNICODE)),
    ("formula", re.compile(f"({_FORMULA_PARTS})", re.UNICODE)),
    ("number", re.compile(r"(?<![a-zA-Z\-])(\d+(?:\.\d+)?(?:/\d+)?)(?![a-zA-Z\-])")),
]


class FBDerivationService:
    """MC 문제에서 FB 변형 문제를 자동 파생."""

    def derive_from_mc(
        self,
        mc_question: dict,
        max_variants: int = 3,
    ) -> list[dict]:
        """MC 문제에서 FB 변형 문제들을 생성.

        Args:
            mc_question: MC question dict
            max_variants: 최대 파생 수

        Returns:
            FB question dict 리스트
        """
        # 정답 선지 텍스트 찾기
        correct_text = ""
        correct_label = mc_question.get("correct_answer", "")
        options = mc_question.get("options") or []
        for opt in options:
            if isinstance(opt, dict) and opt.get("label") == correct_label:
                correct_text = opt.get("text", "")
                break

        # 소스 텍스트: 해설 + 정답 선지에서 핵심 용어 추출
        explanation = mc_question.get("explanation", "")
        content = mc_question.get("content", "")

        # 해설 기반 파생 (해설 문장을 빈칸 문제로 변환)
        terms = self._extract_key_terms(explanation, correct_text)

        # 중복 제거 (같은 용어가 여러 번 나오면 첫 번째만)
        seen_terms = set()
        unique_terms = []
        for t in terms:
            if t["term"].lower() not in seen_terms:
                seen_terms.add(t["term"].lower())
                unique_terms.append(t)

        # 상위 N개 선택
        selected = unique_terms[:max_variants]

        if not selected:
            return []

        results = []
        mc_id = mc_question.get("id", "unknown")
        for idx, term_info in enumerate(selected):
            fb = self._create_blank_variant(mc_question, term_info, idx, mc_id)
            if fb:
                results.append(fb)

        return results

    def _extract_key_terms(self, explanation: str, correct_text: str) -> list[dict]:
        """해설과 정답 텍스트에서 핵심 수학 용어를 추출.

        Returns:
            [{"term": str, "source": "explanation"|"answer", "type": str, "priority": int}]
        """
        all_terms: list[dict] = []
        priority_map = {"concept": 0, "shape": 1, "formula": 2, "number": 3}

        # 해설에서 추출
        for term_type, pattern in _PATTERNS:
            for match in pattern.finditer(explanation):
                term = match.group(1)
                # 너무 짧은 숫자(1자리)나 일반적인 단어는 스킵
                if term_type == "number" and len(term) <= 1:
                    continue
                all_terms.append({
                    "term": term,
                    "source": "explanation",
                    "type": term_type,
                    "priority": priority_map.get(term_type, 99),
                    "start": match.start(),
                    "end": match.end(),
                })

        # 정답 텍스트에서 추출 (높은 우선순위)
        if correct_text and len(correct_text) >= 2:
            all_terms.append({
                "term": correct_text,
                "source": "answer",
                "type": "answer",
                "priority": -1,  # 최고 우선순위
                "start": 0,
                "end": len(correct_text),
            })

        # 우선순위로 정렬
        all_terms.sort(key=lambda t: t["priority"])
        return all_terms

    def _create_blank_variant(
        self,
        mc_question: dict,
        term_info: dict,
        variant_idx: int,
        mc_id: str,
    ) -> dict | None:
        """하나의 용어를 빈칸으로 만든 FB 문제 생성."""
        term = term_info["term"]
        source = term_info["source"]
        explanation = mc_question.get("explanation", "")

        if source == "answer":
            # 정답 선지를 빈칸으로: "다음 중 올바른 것은? → ____"
            fb_content = f"{mc_question.get('content', '')}\n\n정답: ____"
            answer = term
        else:
            # 해설 내 용어를 빈칸으로
            if term not in explanation:
                return None
            # 첫 번째 출현만 빈칸으로 교체
            fb_content = explanation.replace(term, "____", 1)
            answer = term

        # accept_formats 생성
        accept = [answer]
        # 숫자인 경우 다양한 표기 허용
        if term_info["type"] == "number":
            try:
                num = float(answer)
                if num == int(num):
                    accept.append(str(int(num)))
                accept.append(str(num))
            except ValueError:
                pass

        fb_id = f"fb-{mc_id}-{variant_idx + 1:02d}"

        difficulty = mc_question.get("difficulty", 5)
        # 해설 기반 빈칸은 살짝 더 어려울 수 있음
        if source == "explanation":
            difficulty = min(10, difficulty + 1)

        return {
            "id": fb_id,
            "concept_id": mc_question.get("concept_id", ""),
            "category": mc_question.get("category", "concept"),
            "part": mc_question.get("part", "calc"),
            "question_type": "fill_in_blank",
            "difficulty": difficulty,
            "content": fb_content,
            "options": None,
            "correct_answer": answer,
            "explanation": mc_question.get("explanation", ""),
            "points": mc_question.get("points", 10),
            "blank_config": {
                "blank_count": 1,
                "accept_formats": accept,
            },
            "is_active": True,
            "source_question_id": mc_id,
        }
