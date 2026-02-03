"""빈칸 채우기 문제 생성 서비스."""

import random
import hashlib
from sqlalchemy.orm import Session

from app.models.question import Question


class BlankService:
    """빈칸 채우기 문제 생성 및 관리."""

    def __init__(self, db: Session):
        self.db = db

    def generate_blanks_for_attempt(
        self,
        question: Question,
        attempt_count: int,
        student_id: str,
        attempt_id: str
    ) -> dict:
        """
        회차에 맞는 빈칸 생성.

        Args:
            question: 문제 객체
            attempt_count: 시도 회차 (1, 2, 3, ...)
            student_id: 학생 ID
            attempt_id: 시도 ID (랜덤 시드용)

        Returns:
            {
                "display_content": "___의 ___가 같은 ___은 정삼각형이다.",
                "blank_answers": {
                    "blank_0": {"answer": "세", "position": 0},
                    "blank_1": {"answer": "변의", "position": 2}
                },
                "original_content": "세 변의 길이가 같은 삼각형은 정삼각형이다."
            }
        """
        if not question.blank_config:
            return {}

        blank_config = question.blank_config
        blank_positions = blank_config.get("blank_positions", [])
        round_rules = blank_config.get("round_rules", [])

        # 회차에 맞는 규칙 선택
        rule = self._get_rule_for_round(round_rules, attempt_count)
        if not rule:
            return {}

        # 중요도 기준으로 후보 위치 필터링
        min_importance = rule.get("min_importance", 1)
        candidates = [
            pos for pos in blank_positions
            if pos.get("importance", 1) >= min_importance
        ]

        if not candidates:
            # 후보가 없으면 모든 위치 사용
            candidates = blank_positions

        # 빈칸 개수 결정
        blank_count_range = rule.get("blank_count_range")
        if blank_count_range:
            # blank_count_range가 있으면 범위 내에서 랜덤 선택
            min_count, max_count = blank_count_range
            # 실제 빈칸 개수는 후보 수를 초과할 수 없음
            max_count = min(max_count, len(candidates))
            min_count = min(min_count, max_count)

            # 랜덤 시드 기반으로 개수 선택
            seed = self._generate_seed(student_id, question.id, attempt_id)
            rng = random.Random(seed)
            blank_count = rng.randint(min_count, max_count)
        else:
            # blank_count_range가 없으면 고정 개수 사용
            blank_count = rule.get("blank_count", 0)

        # 빈칸 개수가 0이면 원본 그대로 반환
        if blank_count == 0:
            return {
                "display_content": question.content,
                "blank_answers": {},
                "original_content": question.content
            }

        # 선택할 빈칸 개수 제한
        blank_count = min(blank_count, len(candidates))

        # 랜덤으로 위치 선택
        seed = self._generate_seed(student_id, question.id, attempt_id)
        rng = random.Random(seed)
        selected_positions = rng.sample(candidates, blank_count)

        # 위치를 index 순으로 정렬
        selected_positions.sort(key=lambda x: x.get("index", 0))

        # 빈칸 답안 생성
        blank_answers = {}
        for i, pos in enumerate(selected_positions):
            blank_id = f"blank_{i}"
            blank_answers[blank_id] = {
                "answer": pos.get("word", ""),
                "position": pos.get("index", 0)
            }

        # 빈칸이 적용된 content 생성
        display_content = self._create_display_content(
            question.content,
            selected_positions
        )

        return {
            "display_content": display_content,
            "blank_answers": blank_answers,
            "original_content": question.content
        }

    def _get_rule_for_round(self, round_rules: list, attempt_count: int) -> dict | None:
        """회차에 맞는 규칙 찾기."""
        # 정확히 일치하는 규칙 찾기
        for rule in round_rules:
            if rule.get("round") == attempt_count:
                return rule

        # 없으면 가장 높은 회차 규칙 사용
        if round_rules:
            highest_rule = max(round_rules, key=lambda r: r.get("round", 0))
            if attempt_count >= highest_rule.get("round", 0):
                return highest_rule

        return None

    def _generate_seed(self, student_id: str, question_id: str, attempt_id: str) -> int:
        """일관된 랜덤 시드 생성."""
        seed_string = f"{student_id}_{question_id}_{attempt_id}"
        hash_object = hashlib.md5(seed_string.encode())
        return int(hash_object.hexdigest(), 16) % (2**31)

    def _create_display_content(self, original_content: str, selected_positions: list) -> str:
        """
        선택된 위치를 빈칸으로 치환한 content 생성.

        간단한 구현: 단어를 공백으로 분리하고 index에 해당하는 단어를 ___ 로 치환
        """
        words = original_content.split()

        # 선택된 위치의 index 집합
        blank_indices = {pos.get("index", -1) for pos in selected_positions}

        # 빈칸 적용
        for i in range(len(words)):
            if i in blank_indices:
                words[i] = "___"

        return " ".join(words)
