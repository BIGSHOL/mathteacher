"""
Unit tests for AdaptiveService difficulty calculation.

Tests pure difficulty adjustment logic without database dependencies.
"""
import pytest
from types import SimpleNamespace
from app.services.adaptive_service import AdaptiveService, MIN_DIFFICULTY, MAX_DIFFICULTY


class TestCalculateNextDifficulty:
    """Tests for AdaptiveService._calculate_next_difficulty method."""

    @pytest.fixture
    def adaptive_service(self):
        """Create AdaptiveService instance with mock db."""
        return AdaptiveService(db=None)

    def test_empty_logs_returns_current(self, adaptive_service):
        """Empty logs returns current difficulty unchanged."""
        result = adaptive_service._calculate_next_difficulty(current=5, logs=[])
        assert result == 5

    def test_last_correct_increases_by_1(self, adaptive_service):
        """Last answer correct increases difficulty by 1."""
        logs = [
            SimpleNamespace(is_correct=True, question_difficulty=5)
        ]
        result = adaptive_service._calculate_next_difficulty(current=5, logs=logs)
        assert result == 6

    def test_last_incorrect_decreases_by_1(self, adaptive_service):
        """Last answer incorrect decreases difficulty by 1."""
        logs = [
            SimpleNamespace(is_correct=False, question_difficulty=5)
        ]
        result = adaptive_service._calculate_next_difficulty(current=5, logs=logs)
        assert result == 4

    def test_two_consecutive_correct_at_current_increases_by_2(self, adaptive_service):
        """Two consecutive correct at current difficulty increases by 2."""
        logs = [
            SimpleNamespace(is_correct=True, question_difficulty=5),
            SimpleNamespace(is_correct=True, question_difficulty=5)
        ]
        result = adaptive_service._calculate_next_difficulty(current=5, logs=logs)
        assert result == 7  # 5 + 2

    def test_two_consecutive_incorrect_at_current_decreases_by_2(self, adaptive_service):
        """Two consecutive incorrect at current difficulty decreases by 2."""
        logs = [
            SimpleNamespace(is_correct=False, question_difficulty=5),
            SimpleNamespace(is_correct=False, question_difficulty=5)
        ]
        result = adaptive_service._calculate_next_difficulty(current=5, logs=logs)
        assert result == 3  # 5 - 2

    def test_two_correct_but_different_difficulties_increases_by_1(self, adaptive_service):
        """Two correct but at different difficulties only increases by 1."""
        logs = [
            SimpleNamespace(is_correct=True, question_difficulty=4),
            SimpleNamespace(is_correct=True, question_difficulty=5)
        ]
        result = adaptive_service._calculate_next_difficulty(current=5, logs=logs)
        assert result == 6  # Only last correct matters, +1

    def test_clamped_to_min_difficulty(self, adaptive_service):
        """Result is clamped to MIN_DIFFICULTY."""
        logs = [
            SimpleNamespace(is_correct=False, question_difficulty=1),
            SimpleNamespace(is_correct=False, question_difficulty=1)
        ]
        result = adaptive_service._calculate_next_difficulty(current=1, logs=logs)
        assert result == MIN_DIFFICULTY
        assert result == 1

    def test_clamped_to_max_difficulty(self, adaptive_service):
        """Result is clamped to MAX_DIFFICULTY."""
        logs = [
            SimpleNamespace(is_correct=True, question_difficulty=10),
            SimpleNamespace(is_correct=True, question_difficulty=10)
        ]
        result = adaptive_service._calculate_next_difficulty(current=10, logs=logs)
        assert result == MAX_DIFFICULTY
        assert result == 10

    def test_mixed_results_uses_last_answer(self, adaptive_service):
        """Mixed results uses last answer for single increment."""
        logs = [
            SimpleNamespace(is_correct=True, question_difficulty=5),
            SimpleNamespace(is_correct=False, question_difficulty=5),
            SimpleNamespace(is_correct=True, question_difficulty=5)
        ]
        result = adaptive_service._calculate_next_difficulty(current=5, logs=logs)
        assert result == 6  # Last is correct, +1

    def test_consecutive_check_requires_same_difficulty(self, adaptive_service):
        """Consecutive bonus requires both at SAME difficulty as current."""
        logs = [
            SimpleNamespace(is_correct=True, question_difficulty=4),  # Different difficulty
            SimpleNamespace(is_correct=True, question_difficulty=5)   # Current difficulty
        ]
        result = adaptive_service._calculate_next_difficulty(current=5, logs=logs)
        assert result == 6  # Not consecutive at same difficulty, only +1
