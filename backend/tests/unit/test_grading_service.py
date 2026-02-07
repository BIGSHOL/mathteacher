"""
Unit tests for GradingService.

Tests pure grading logic without database dependencies.
"""
import pytest
from app.services.grading_service import GradingService


class TestGradeAnswer:
    """Tests for GradingService.grade_answer method."""

    @pytest.fixture
    def grading_service(self):
        """Create GradingService instance (no DB needed)."""
        return GradingService()

    def test_correct_string_answer(self, grading_service):
        """Correct string answer returns full points."""
        result = grading_service.grade_answer(
            question_id=1,
            selected_answer="A",
            correct_answer="A",
            points=10
        )
        assert result["is_correct"] is True
        assert result["points_earned"] == 10

    def test_incorrect_string_answer(self, grading_service):
        """Incorrect string answer returns zero points."""
        result = grading_service.grade_answer(
            question_id=1,
            selected_answer="B",
            correct_answer="A",
            points=10
        )
        assert result["is_correct"] is False
        assert result["points_earned"] == 0

    def test_case_insensitive_correct(self, grading_service):
        """String comparison is case insensitive."""
        result = grading_service.grade_answer(
            question_id=1,
            selected_answer="a",
            correct_answer="A",
            points=10
        )
        assert result["is_correct"] is True
        assert result["points_earned"] == 10

    def test_whitespace_trimmed(self, grading_service):
        """Whitespace is trimmed before comparison."""
        result = grading_service.grade_answer(
            question_id=1,
            selected_answer="  A  ",
            correct_answer="A",
            points=10
        )
        assert result["is_correct"] is True
        assert result["points_earned"] == 10

    def test_dict_correct_answer_routes_to_fill_in_blank(self, grading_service):
        """Dict correct_answer routes to fill-in-blank grading."""
        result = grading_service.grade_answer(
            question_id=1,
            selected_answer={"blank1": "5", "blank2": "10"},
            correct_answer={"blank1": {"answer": "5"}, "blank2": {"answer": "10"}},
            points=10
        )
        assert result["is_correct"] is True
        assert result["points_earned"] == 10
        assert result["correct_count"] == 2
        assert result["total_blanks"] == 2


class TestGradeFillInBlank:
    """Tests for GradingService._grade_fill_in_blank method."""

    @pytest.fixture
    def grading_service(self):
        """Create GradingService instance (no DB needed)."""
        return GradingService()

    def test_all_blanks_correct(self, grading_service):
        """All blanks correct returns full points."""
        student_answers = {"blank1": "5", "blank2": "10"}
        correct_answers = {"blank1": {"answer": "5"}, "blank2": {"answer": "10"}}

        result = grading_service._grade_fill_in_blank(
            student_answers, correct_answers, points=10
        )

        assert result["is_correct"] is True
        assert result["points_earned"] == 10
        assert result["correct_count"] == 2
        assert result["total_blanks"] == 2

    def test_partial_blanks_correct(self, grading_service):
        """Partial correct blanks returns proportional points."""
        student_answers = {"blank1": "5", "blank2": "wrong"}
        correct_answers = {"blank1": {"answer": "5"}, "blank2": {"answer": "10"}}

        result = grading_service._grade_fill_in_blank(
            student_answers, correct_answers, points=10
        )

        assert result["is_correct"] is False
        assert result["points_earned"] == 5  # 1/2 * 10
        assert result["correct_count"] == 1
        assert result["total_blanks"] == 2

    def test_no_blanks_correct(self, grading_service):
        """No correct blanks returns zero points."""
        student_answers = {"blank1": "wrong", "blank2": "wrong"}
        correct_answers = {"blank1": {"answer": "5"}, "blank2": {"answer": "10"}}

        result = grading_service._grade_fill_in_blank(
            student_answers, correct_answers, points=10
        )

        assert result["is_correct"] is False
        assert result["points_earned"] == 0
        assert result["correct_count"] == 0
        assert result["total_blanks"] == 2

    def test_empty_student_answers(self, grading_service):
        """Empty student answers returns zero points."""
        student_answers = {}
        correct_answers = {"blank1": {"answer": "5"}, "blank2": {"answer": "10"}}

        result = grading_service._grade_fill_in_blank(
            student_answers, correct_answers, points=10
        )

        assert result["is_correct"] is False
        assert result["points_earned"] == 0
        assert result["correct_count"] == 0
        assert result["total_blanks"] == 2

    def test_non_dict_student_answers(self, grading_service):
        """Non-dict student answers treated as empty dict."""
        student_answers = "not a dict"
        correct_answers = {"blank1": {"answer": "5"}}

        result = grading_service._grade_fill_in_blank(
            student_answers, correct_answers, points=10
        )

        assert result["is_correct"] is False
        assert result["points_earned"] == 0
        assert result["correct_count"] == 0
        assert result["total_blanks"] == 1

    def test_zero_blanks(self, grading_service):
        """Zero blanks returns full points (edge case)."""
        student_answers = {}
        correct_answers = {}

        result = grading_service._grade_fill_in_blank(
            student_answers, correct_answers, points=10
        )

        assert result["is_correct"] is True
        assert result["points_earned"] == 10
        assert result["correct_count"] == 0
        assert result["total_blanks"] == 0

    def test_blank_case_insensitive(self, grading_service):
        """Blank comparison is case insensitive."""
        student_answers = {"blank1": "abc"}
        correct_answers = {"blank1": {"answer": "ABC"}}

        result = grading_service._grade_fill_in_blank(
            student_answers, correct_answers, points=10
        )

        assert result["is_correct"] is True
        assert result["points_earned"] == 10

    def test_blank_whitespace_trimmed(self, grading_service):
        """Blank whitespace is trimmed."""
        student_answers = {"blank1": "  5  "}
        correct_answers = {"blank1": {"answer": "5"}}

        result = grading_service._grade_fill_in_blank(
            student_answers, correct_answers, points=10
        )

        assert result["is_correct"] is True
        assert result["points_earned"] == 10

    def test_missing_blank_in_student_answers(self, grading_service):
        """Missing blank in student answers counted as incorrect."""
        student_answers = {"blank1": "5"}  # missing blank2
        correct_answers = {"blank1": {"answer": "5"}, "blank2": {"answer": "10"}}

        result = grading_service._grade_fill_in_blank(
            student_answers, correct_answers, points=10
        )

        assert result["is_correct"] is False
        assert result["points_earned"] == 5
        assert result["correct_count"] == 1
        assert result["total_blanks"] == 2


class TestCalculateComboBonus:
    """Tests for GradingService.calculate_combo_bonus method."""

    @pytest.fixture
    def grading_service(self):
        """Create GradingService instance (no DB needed)."""
        return GradingService()

    def test_combo_10_or_more(self, grading_service):
        """Combo >= 10 applies 3.0x multiplier."""
        result = grading_service.calculate_combo_bonus(combo_count=10, base_points=10)
        assert result == 30  # 10 * 3.0

        result = grading_service.calculate_combo_bonus(combo_count=15, base_points=10)
        assert result == 30

    def test_combo_5_to_9(self, grading_service):
        """Combo 5-9 applies 2.0x multiplier."""
        result = grading_service.calculate_combo_bonus(combo_count=5, base_points=10)
        assert result == 20  # 10 * 2.0

        result = grading_service.calculate_combo_bonus(combo_count=9, base_points=10)
        assert result == 20

    def test_combo_3_to_4(self, grading_service):
        """Combo 3-4 applies 1.5x multiplier."""
        result = grading_service.calculate_combo_bonus(combo_count=3, base_points=10)
        assert result == 15  # 10 * 1.5

        result = grading_service.calculate_combo_bonus(combo_count=4, base_points=10)
        assert result == 15

    def test_combo_below_3(self, grading_service):
        """Combo < 3 applies 1.0x multiplier (no bonus)."""
        result = grading_service.calculate_combo_bonus(combo_count=0, base_points=10)
        assert result == 10  # 10 * 1.0

        result = grading_service.calculate_combo_bonus(combo_count=2, base_points=10)
        assert result == 10

    def test_combo_bonus_integer_conversion(self, grading_service):
        """Combo bonus is converted to integer."""
        result = grading_service.calculate_combo_bonus(combo_count=3, base_points=11)
        assert result == 16  # int(11 * 1.5) = int(16.5) = 16
        assert isinstance(result, int)
