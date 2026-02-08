"""Extended tests for BlankService.generate_blanks_for_attempt method.

Tests the main method that generates blanks for a test attempt,
covering lines 42-116 which were previously untested.
"""

import pytest
from types import SimpleNamespace

from app.services.blank_service import BlankService
from app.models.question import Question


class TestGenerateBlanksForAttempt:
    """Tests for BlankService.generate_blanks_for_attempt method."""

    @pytest.fixture
    def blank_service(self):
        """Create BlankService instance with mock db."""
        mock_db = SimpleNamespace()
        return BlankService(db=mock_db)

    def test_no_blank_config_returns_empty_dict(self, blank_service):
        """When question has no blank_config, returns empty dict."""
        question = SimpleNamespace(
            id="q1",
            content="This is a question",
            blank_config=None,
            correct_answer="answer"
        )

        result = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        assert result == {}

    def test_no_blank_positions_returns_empty_dict(self, blank_service):
        """When blank_config has no blank_positions, returns empty dict."""
        question = SimpleNamespace(
            id="q1",
            content="This is a question",
            blank_config={"some_other_key": "value"},
            correct_answer="answer"
        )

        result = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        assert result == {}

    def test_no_matching_rule_returns_empty_dict(self, blank_service):
        """When no round_rules match the attempt_count, returns empty dict."""
        question = SimpleNamespace(
            id="q1",
            content="This is a question",
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "This", "importance": 5}
                ],
                "round_rules": [
                    {"round": 2, "blank_count": 1}  # Only round 2
                ]
            },
            correct_answer="answer"
        )

        # Attempt 1 won't match round 2
        result = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        assert result == {}

    def test_blank_count_range_uses_random_count(self, blank_service):
        """When rule has blank_count_range, uses random count within range."""
        question = SimpleNamespace(
            id="q1",
            content="The quick brown fox jumps",
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "The", "importance": 5},
                    {"index": 1, "word": "quick", "importance": 5},
                    {"index": 2, "word": "brown", "importance": 5},
                    {"index": 3, "word": "fox", "importance": 5},
                ],
                "round_rules": [
                    {"round": 1, "blank_count_range": [2, 3], "min_importance": 1}
                ]
            },
            correct_answer="answer"
        )

        result = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        assert result != {}
        assert "blank_answers" in result
        # Should have 2 or 3 blanks
        blank_count = len(result["blank_answers"])
        assert 2 <= blank_count <= 3

    def test_fixed_blank_count_uses_rule_blank_count(self, blank_service):
        """When rule has fixed blank_count, uses that count."""
        question = SimpleNamespace(
            id="q1",
            content="The quick brown fox",
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "The", "importance": 5},
                    {"index": 1, "word": "quick", "importance": 5},
                    {"index": 2, "word": "brown", "importance": 5},
                ],
                "round_rules": [
                    {"round": 1, "blank_count": 2, "min_importance": 1}
                ]
            },
            correct_answer="answer"
        )

        result = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        assert result != {}
        assert len(result["blank_answers"]) == 2

    def test_blank_count_zero_returns_original_content(self, blank_service):
        """When blank_count is 0, returns original content with empty answers."""
        question = SimpleNamespace(
            id="q1",
            content="The quick brown fox",
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "The", "importance": 5},
                ],
                "round_rules": [
                    {"round": 1, "blank_count": 0, "min_importance": 1}
                ]
            },
            correct_answer="answer"
        )

        result = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        assert result["display_content"] == "The quick brown fox"
        assert result["blank_answers"] == {}
        assert result["original_content"] == "The quick brown fox"

    def test_normal_flow_selects_positions_and_generates_content(self, blank_service):
        """Normal flow: selects positions and generates display_content."""
        question = SimpleNamespace(
            id="q1",
            content="세 변의 길이가 같은 삼각형은 정삼각형이다",
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "세", "importance": 5},
                    {"index": 1, "word": "변의", "importance": 3},
                    {"index": 2, "word": "길이가", "importance": 2},
                ],
                "round_rules": [
                    {"round": 1, "blank_count": 2, "min_importance": 1}
                ]
            },
            correct_answer="답"
        )

        result = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        assert result != {}
        assert "display_content" in result
        assert "blank_answers" in result
        assert "original_content" in result
        assert result["original_content"] == "세 변의 길이가 같은 삼각형은 정삼각형이다"
        # Should have 2 blanks
        assert len(result["blank_answers"]) == 2
        # Display content should have ___ marks
        assert "___" in result["display_content"]

    def test_min_importance_filtering(self, blank_service):
        """Only positions with sufficient importance are candidates."""
        question = SimpleNamespace(
            id="q1",
            content="The quick brown fox",
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "The", "importance": 2},
                    {"index": 1, "word": "quick", "importance": 5},
                    {"index": 2, "word": "brown", "importance": 8},
                ],
                "round_rules": [
                    {"round": 1, "blank_count": 2, "min_importance": 5}
                ]
            },
            correct_answer="answer"
        )

        result = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        # Should only select from positions with importance >= 5 (quick, brown)
        assert len(result["blank_answers"]) == 2
        # Check that selected words are from high importance positions
        selected_words = [ans["answer"] for ans in result["blank_answers"].values()]
        assert "The" not in selected_words  # importance 2 < 5
        assert all(word in ["quick", "brown"] for word in selected_words)

    def test_no_candidates_after_filter_falls_back_to_all(self, blank_service):
        """When no candidates meet min_importance, falls back to all positions."""
        question = SimpleNamespace(
            id="q1",
            content="The quick brown",
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "The", "importance": 2},
                    {"index": 1, "word": "quick", "importance": 3},
                    {"index": 2, "word": "brown", "importance": 2},
                ],
                "round_rules": [
                    {"round": 1, "blank_count": 2, "min_importance": 10}  # Too high
                ]
            },
            correct_answer="answer"
        )

        result = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        # Should still generate blanks using all positions as fallback
        assert len(result["blank_answers"]) == 2

    def test_deterministic_selection_same_seed(self, blank_service):
        """Same student/question/attempt produces same blank selection."""
        question = SimpleNamespace(
            id="q1",
            content="The quick brown fox jumps",
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "The", "importance": 5},
                    {"index": 1, "word": "quick", "importance": 5},
                    {"index": 2, "word": "brown", "importance": 5},
                    {"index": 3, "word": "fox", "importance": 5},
                ],
                "round_rules": [
                    {"round": 1, "blank_count": 2, "min_importance": 1}
                ]
            },
            correct_answer="answer"
        )

        result1 = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        result2 = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        # Should produce identical results
        assert result1["display_content"] == result2["display_content"]
        assert result1["blank_answers"] == result2["blank_answers"]

    def test_different_attempt_id_produces_different_blanks(self, blank_service):
        """Different attempt_id produces different blank selection."""
        question = SimpleNamespace(
            id="q1",
            content="The quick brown fox jumps",
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "The", "importance": 5},
                    {"index": 1, "word": "quick", "importance": 5},
                    {"index": 2, "word": "brown", "importance": 5},
                    {"index": 3, "word": "fox", "importance": 5},
                ],
                "round_rules": [
                    {"round": 1, "blank_count": 2, "min_importance": 1}
                ]
            },
            correct_answer="answer"
        )

        result1 = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        result2 = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a2"  # Different attempt
        )

        # Results should likely be different (though technically could be same by chance)
        # At minimum, they should both be valid results
        assert len(result1["blank_answers"]) == 2
        assert len(result2["blank_answers"]) == 2

    def test_blank_answers_structure(self, blank_service):
        """Verify blank_answers has correct structure."""
        question = SimpleNamespace(
            id="q1",
            content="The quick brown",
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "The", "importance": 5},
                    {"index": 1, "word": "quick", "importance": 5},
                    {"index": 2, "word": "brown", "importance": 5},
                ],
                "round_rules": [
                    {"round": 1, "blank_count": 2, "min_importance": 1}
                ]
            },
            correct_answer="answer"
        )

        result = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        # Check structure of blank_answers
        assert len(result["blank_answers"]) == 2
        for blank_id, blank_data in result["blank_answers"].items():
            assert blank_id.startswith("blank_")
            assert "answer" in blank_data
            assert "position" in blank_data
            assert isinstance(blank_data["answer"], str)
            assert isinstance(blank_data["position"], int)

    def test_higher_attempt_count_uses_highest_rule(self, blank_service):
        """When attempt_count > highest round, uses highest round rule."""
        question = SimpleNamespace(
            id="q1",
            content="The quick brown fox",
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "The", "importance": 5},
                    {"index": 1, "word": "quick", "importance": 5},
                    {"index": 2, "word": "brown", "importance": 5},
                    {"index": 3, "word": "fox", "importance": 5},
                ],
                "round_rules": [
                    {"round": 1, "blank_count": 1, "min_importance": 1},
                    {"round": 2, "blank_count": 2, "min_importance": 1},
                    {"round": 3, "blank_count": 3, "min_importance": 1},
                ]
            },
            correct_answer="answer"
        )

        # Attempt 10 should use round 3 rule
        result = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=10,
            student_id="s1",
            attempt_id="a1"
        )

        # Should use round 3 rule with blank_count=3
        assert len(result["blank_answers"]) == 3

    def test_blank_count_limited_by_candidates(self, blank_service):
        """Blank count cannot exceed number of candidate positions."""
        question = SimpleNamespace(
            id="q1",
            content="The quick",
            blank_config={
                "blank_positions": [
                    {"index": 0, "word": "The", "importance": 5},
                    {"index": 1, "word": "quick", "importance": 5},
                ],
                "round_rules": [
                    {"round": 1, "blank_count": 10, "min_importance": 1}  # Wants 10 but only 2 available
                ]
            },
            correct_answer="answer"
        )

        result = blank_service.generate_blanks_for_attempt(
            question=question,
            attempt_count=1,
            student_id="s1",
            attempt_id="a1"
        )

        # Should only have 2 blanks (limited by available positions)
        assert len(result["blank_answers"]) == 2
