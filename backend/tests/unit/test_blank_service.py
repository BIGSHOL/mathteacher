"""
Unit tests for BlankService pure methods.

Tests rule selection, seed generation, and display content creation.
"""
import pytest
from types import SimpleNamespace
from app.services.blank_service import BlankService


class TestGetRuleForRound:
    """Tests for BlankService._get_rule_for_round method."""

    @pytest.fixture
    def blank_service(self):
        """Create BlankService instance with mock db."""
        mock_db = SimpleNamespace()
        return BlankService(db=mock_db)

    def test_exact_match_by_round_number(self, blank_service):
        """Exact match by round number returns that rule."""
        round_rules = [
            {"round": 1, "blank_count": 2},
            {"round": 2, "blank_count": 4},
            {"round": 3, "blank_count": 6}
        ]
        result = blank_service._get_rule_for_round(round_rules, attempt_count=2)
        assert result == {"round": 2, "blank_count": 4}

    def test_attempt_greater_than_highest_round(self, blank_service):
        """Attempt >= highest round returns highest round rule."""
        round_rules = [
            {"round": 1, "blank_count": 2},
            {"round": 2, "blank_count": 4},
            {"round": 3, "blank_count": 6}
        ]
        result = blank_service._get_rule_for_round(round_rules, attempt_count=5)
        assert result == {"round": 3, "blank_count": 6}

    def test_attempt_less_than_all_rounds_returns_none(self, blank_service):
        """Attempt < all rounds returns None."""
        round_rules = [
            {"round": 2, "blank_count": 4},
            {"round": 3, "blank_count": 6}
        ]
        result = blank_service._get_rule_for_round(round_rules, attempt_count=1)
        assert result is None

    def test_empty_rules_returns_none(self, blank_service):
        """Empty rules returns None."""
        result = blank_service._get_rule_for_round([], attempt_count=1)
        assert result is None

    def test_single_rule_match(self, blank_service):
        """Single rule exact match works."""
        round_rules = [{"round": 1, "blank_count": 2}]
        result = blank_service._get_rule_for_round(round_rules, attempt_count=1)
        assert result == {"round": 1, "blank_count": 2}

    def test_single_rule_attempt_greater(self, blank_service):
        """Single rule with attempt > round returns that rule."""
        round_rules = [{"round": 1, "blank_count": 2}]
        result = blank_service._get_rule_for_round(round_rules, attempt_count=10)
        assert result == {"round": 1, "blank_count": 2}


class TestGenerateSeed:
    """Tests for BlankService._generate_seed method."""

    @pytest.fixture
    def blank_service(self):
        """Create BlankService instance with mock db."""
        mock_db = SimpleNamespace()
        return BlankService(db=mock_db)

    def test_deterministic_same_inputs(self, blank_service):
        """Same inputs produce same seed."""
        seed1 = blank_service._generate_seed(
            student_id=1, question_id=10, attempt_id=100
        )
        seed2 = blank_service._generate_seed(
            student_id=1, question_id=10, attempt_id=100
        )
        assert seed1 == seed2

    def test_different_student_id(self, blank_service):
        """Different student_id produces different seed."""
        seed1 = blank_service._generate_seed(
            student_id=1, question_id=10, attempt_id=100
        )
        seed2 = blank_service._generate_seed(
            student_id=2, question_id=10, attempt_id=100
        )
        assert seed1 != seed2

    def test_different_question_id(self, blank_service):
        """Different question_id produces different seed."""
        seed1 = blank_service._generate_seed(
            student_id=1, question_id=10, attempt_id=100
        )
        seed2 = blank_service._generate_seed(
            student_id=1, question_id=20, attempt_id=100
        )
        assert seed1 != seed2

    def test_different_attempt_id(self, blank_service):
        """Different attempt_id produces different seed."""
        seed1 = blank_service._generate_seed(
            student_id=1, question_id=10, attempt_id=100
        )
        seed2 = blank_service._generate_seed(
            student_id=1, question_id=10, attempt_id=200
        )
        assert seed1 != seed2


class TestCreateDisplayContent:
    """Tests for BlankService._create_display_content method."""

    @pytest.fixture
    def blank_service(self):
        """Create BlankService instance with mock db."""
        mock_db = SimpleNamespace()
        return BlankService(db=mock_db)

    def test_replace_single_word(self, blank_service):
        """Single word replacement works."""
        content = "The quick brown fox"
        positions = [{"index": 1, "word": "quick"}]
        result = blank_service._create_display_content(content, positions)
        assert result == "The ___ brown fox"

    def test_replace_multiple_words(self, blank_service):
        """Multiple word replacements work."""
        content = "The quick brown fox jumps"
        positions = [{"index": 1, "word": "quick"}, {"index": 3, "word": "fox"}]
        result = blank_service._create_display_content(content, positions)
        assert result == "The ___ brown ___ jumps"

    def test_empty_positions_returns_original(self, blank_service):
        """Empty positions returns original content."""
        content = "The quick brown fox"
        positions = []
        result = blank_service._create_display_content(content, positions)
        assert result == "The quick brown fox"

    def test_replace_first_word(self, blank_service):
        """Replace first word (index 0)."""
        content = "The quick brown fox"
        positions = [{"index": 0, "word": "The"}]
        result = blank_service._create_display_content(content, positions)
        assert result == "___ quick brown fox"

    def test_replace_last_word(self, blank_service):
        """Replace last word."""
        content = "The quick brown fox"
        positions = [{"index": 3, "word": "fox"}]
        result = blank_service._create_display_content(content, positions)
        assert result == "The quick brown ___"

    def test_replace_all_words(self, blank_service):
        """Replace all words."""
        content = "The quick brown"
        positions = [{"index": 0, "word": "The"}, {"index": 1, "word": "quick"}, {"index": 2, "word": "brown"}]
        result = blank_service._create_display_content(content, positions)
        assert result == "___ ___ ___"
