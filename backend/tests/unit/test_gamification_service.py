"""
Unit tests for GamificationService pure methods.

Tests business logic without database dependencies.
"""

import types
from datetime import date, timedelta

import pytest

from app.services.gamification_service import (
    GamificationService,
    LEVEL_XP_REQUIREMENTS,
    MAX_LEVEL,
    MAX_DEFENSE,
)


class TestGetStreakBonusRate:
    """Tests for get_streak_bonus_rate static method."""

    def test_streak_30_or_more_returns_50_percent(self):
        """Streak of 30+ days returns 0.50 bonus rate."""
        assert GamificationService.get_streak_bonus_rate(30) == 0.50
        assert GamificationService.get_streak_bonus_rate(50) == 0.50
        assert GamificationService.get_streak_bonus_rate(100) == 0.50

    def test_streak_14_to_29_returns_35_percent(self):
        """Streak of 14-29 days returns 0.35 bonus rate."""
        assert GamificationService.get_streak_bonus_rate(14) == 0.35
        assert GamificationService.get_streak_bonus_rate(20) == 0.35
        assert GamificationService.get_streak_bonus_rate(29) == 0.35

    def test_streak_7_to_13_returns_20_percent(self):
        """Streak of 7-13 days returns 0.20 bonus rate."""
        assert GamificationService.get_streak_bonus_rate(7) == 0.20
        assert GamificationService.get_streak_bonus_rate(10) == 0.20
        assert GamificationService.get_streak_bonus_rate(13) == 0.20

    def test_streak_3_to_6_returns_10_percent(self):
        """Streak of 3-6 days returns 0.10 bonus rate."""
        assert GamificationService.get_streak_bonus_rate(3) == 0.10
        assert GamificationService.get_streak_bonus_rate(5) == 0.10
        assert GamificationService.get_streak_bonus_rate(6) == 0.10

    def test_streak_below_3_returns_zero(self):
        """Streak below 3 days returns 0.0 bonus rate."""
        assert GamificationService.get_streak_bonus_rate(0) == 0.0
        assert GamificationService.get_streak_bonus_rate(1) == 0.0
        assert GamificationService.get_streak_bonus_rate(2) == 0.0


class TestApplyStreakBonus:
    """Tests for apply_streak_bonus method."""

    def test_applies_50_percent_bonus_for_long_streak(self):
        """30+ day streak adds 50% bonus to base XP."""
        service = GamificationService()
        total_xp, rate = service.apply_streak_bonus(100, 30)
        assert rate == 0.50
        assert total_xp == 150

    def test_applies_35_percent_bonus_for_medium_streak(self):
        """14-29 day streak adds 35% bonus to base XP."""
        service = GamificationService()
        total_xp, rate = service.apply_streak_bonus(100, 14)
        assert rate == 0.35
        assert total_xp == 135

    def test_applies_no_bonus_for_short_streak(self):
        """Streak below 3 days adds no bonus."""
        service = GamificationService()
        total_xp, rate = service.apply_streak_bonus(100, 2)
        assert rate == 0.0
        assert total_xp == 100

    def test_rounds_down_fractional_bonus(self):
        """Bonus XP is rounded down to nearest integer."""
        service = GamificationService()
        total_xp, rate = service.apply_streak_bonus(55, 7)  # 55 * 0.20 = 11
        assert total_xp == 66


class TestGetLevelForXP:
    """Tests for get_level_for_xp method."""

    def test_zero_xp_returns_level_1(self):
        """0 XP returns level 1."""
        service = GamificationService()
        assert service.get_level_for_xp(0) == 1

    def test_xp_below_level_2_threshold_returns_level_1(self):
        """XP below 60 returns level 1."""
        service = GamificationService()
        assert service.get_level_for_xp(30) == 1
        assert service.get_level_for_xp(59) == 1

    def test_xp_at_threshold_returns_next_level(self):
        """XP at exact threshold returns that level."""
        service = GamificationService()
        assert service.get_level_for_xp(60) == 2
        assert service.get_level_for_xp(160) == 3
        assert service.get_level_for_xp(300) == 4

    def test_max_level_capped_at_15(self):
        """Level is capped at MAX_LEVEL even with excessive XP."""
        service = GamificationService()
        assert service.get_level_for_xp(7000) == 15
        assert service.get_level_for_xp(10000) == 15
        assert service.get_level_for_xp(999999) == 15

    def test_mid_range_levels(self):
        """Mid-range XP values return correct levels."""
        service = GamificationService()
        assert service.get_level_for_xp(500) == 5
        assert service.get_level_for_xp(1050) == 7
        assert service.get_level_for_xp(3600) == 12


class TestCheckLevelUp:
    """Tests for check_level_up method."""

    def test_no_level_up_when_xp_insufficient(self):
        """No level up when new total XP doesn't reach next threshold."""
        service = GamificationService()
        result = service.check_level_up(current_level=1, current_xp=30, xp_earned=20)
        assert result["level_up"] is False
        assert result["new_level"] is None
        assert result["total_xp"] == 50

    def test_level_up_when_threshold_reached(self):
        """Level up occurs when new total XP reaches next level threshold."""
        service = GamificationService()
        result = service.check_level_up(current_level=1, current_xp=50, xp_earned=10)
        assert result["level_up"] is True
        assert result["new_level"] == 2
        assert result["total_xp"] == 60

    def test_multiple_level_ups_from_large_xp_gain(self):
        """Can skip multiple levels with large XP gain."""
        service = GamificationService()
        result = service.check_level_up(current_level=1, current_xp=0, xp_earned=300)
        assert result["level_up"] is True
        assert result["new_level"] == 4
        assert result["total_xp"] == 300

    def test_no_level_up_when_already_at_max_level(self):
        """No level up when already at MAX_LEVEL."""
        service = GamificationService()
        result = service.check_level_up(current_level=15, current_xp=7000, xp_earned=1000)
        assert result["level_up"] is False
        assert result["new_level"] is None
        assert result["total_xp"] == 8000


class TestUpdateStreak:
    """Tests for update_streak method."""

    def test_first_activity_starts_streak_at_1(self):
        """First activity with no previous date starts streak at 1."""
        service = GamificationService()
        today = "2026-02-07"
        result = service.update_streak(current_streak=0, last_activity_date=None, today=today)
        assert result["new_streak"] == 1
        assert result["streak_broken"] is False

    def test_same_day_activity_maintains_streak(self):
        """Activity on same day maintains current streak."""
        service = GamificationService()
        today = "2026-02-07"
        result = service.update_streak(current_streak=5, last_activity_date=today, today=today)
        assert result["new_streak"] == 5
        assert result["streak_broken"] is False

    def test_next_day_activity_increments_streak(self):
        """Activity on consecutive day increments streak by 1."""
        service = GamificationService()
        yesterday = "2026-02-06"
        today = "2026-02-07"
        result = service.update_streak(current_streak=5, last_activity_date=yesterday, today=today)
        assert result["new_streak"] == 6
        assert result["streak_broken"] is False

    def test_gap_of_two_days_breaks_streak(self):
        """Gap of 2+ days breaks streak and resets to 1."""
        service = GamificationService()
        two_days_ago = "2026-02-05"
        today = "2026-02-07"
        result = service.update_streak(current_streak=10, last_activity_date=two_days_ago, today=today)
        assert result["new_streak"] == 1
        assert result["streak_broken"] is True

    def test_long_gap_breaks_streak(self):
        """Long absence breaks streak."""
        service = GamificationService()
        long_ago = "2026-01-01"
        today = "2026-02-07"
        result = service.update_streak(current_streak=20, last_activity_date=long_ago, today=today)
        assert result["new_streak"] == 1
        assert result["streak_broken"] is True


class TestCalculateAdaptiveLevel:
    """Tests for calculate_adaptive_level method."""

    def test_zero_questions_returns_none(self):
        """No questions answered returns None (no level change)."""
        service = GamificationService()
        result = service.calculate_adaptive_level(
            current_level=3, final_difficulty=5, correct_count=0, total_count=0
        )
        assert result is None

    def test_low_accuracy_returns_none(self):
        """Accuracy below 50% returns None (no level increase)."""
        service = GamificationService()
        result = service.calculate_adaptive_level(
            current_level=3, final_difficulty=5, correct_count=4, total_count=10
        )
        assert result is None

    def test_high_accuracy_demonstrates_final_difficulty(self):
        """Accuracy >= 70% demonstrates mastery of final difficulty."""
        service = GamificationService()
        result = service.calculate_adaptive_level(
            current_level=3, final_difficulty=5, correct_count=7, total_count=10
        )
        assert result == 5

    def test_medium_accuracy_demonstrates_one_below_final(self):
        """Accuracy 50-69% demonstrates final_difficulty - 1."""
        service = GamificationService()
        result = service.calculate_adaptive_level(
            current_level=3, final_difficulty=5, correct_count=6, total_count=10
        )
        assert result == 4

    def test_medium_accuracy_capped_at_minimum_level_1(self):
        """Demonstrated level cannot go below 1."""
        service = GamificationService()
        result = service.calculate_adaptive_level(
            current_level=1, final_difficulty=1, correct_count=6, total_count=10
        )
        assert result is None  # demonstrated = max(1-1, 1) = 1, not > current

    def test_demonstrated_level_not_higher_returns_none(self):
        """No level increase if demonstrated level <= current level."""
        service = GamificationService()
        result = service.calculate_adaptive_level(
            current_level=5, final_difficulty=4, correct_count=8, total_count=10
        )
        assert result is None

    def test_demonstrated_level_capped_at_max_level(self):
        """Demonstrated level cannot exceed MAX_LEVEL."""
        service = GamificationService()
        result = service.calculate_adaptive_level(
            current_level=14, final_difficulty=20, correct_count=8, total_count=10
        )
        assert result == 15


class TestCheckLevelDown:
    """Tests for check_level_down method."""

    def test_zero_questions_returns_no_action(self):
        """No questions answered returns no action."""
        service = GamificationService()
        user = types.SimpleNamespace(level=5, level_down_defense=2)
        result = service.check_level_down(
            user, final_difficulty=3, correct_count=0, total_count=0
        )
        assert result["action"] == "none"

    def test_good_accuracy_restores_defense_when_not_full(self):
        """Accuracy >= 60% restores defense by 1 if not at max."""
        service = GamificationService()
        user = types.SimpleNamespace(level=5, level_down_defense=2)
        result = service.check_level_down(
            user, final_difficulty=3, correct_count=6, total_count=10
        )
        assert result["action"] == "defense_restored"
        assert result["defense_remaining"] == 3

    def test_good_accuracy_no_action_when_defense_full(self):
        """Accuracy >= 60% with full defense returns no action."""
        service = GamificationService()
        user = types.SimpleNamespace(level=5, level_down_defense=MAX_DEFENSE)
        result = service.check_level_down(
            user, final_difficulty=3, correct_count=7, total_count=10
        )
        assert result["action"] == "none"

    def test_medium_accuracy_returns_no_action(self):
        """Accuracy 30-59% returns no action (safe zone)."""
        service = GamificationService()
        user = types.SimpleNamespace(level=5, level_down_defense=2)
        result = service.check_level_down(
            user, final_difficulty=3, correct_count=4, total_count=10
        )
        assert result["action"] == "none"

    def test_small_gap_returns_no_action(self):
        """Gap < 2 between user level and final difficulty returns no action."""
        service = GamificationService()
        user = types.SimpleNamespace(level=5, level_down_defense=2)
        result = service.check_level_down(
            user, final_difficulty=4, correct_count=2, total_count=10
        )
        assert result["action"] == "none"

    def test_level_1_returns_no_action(self):
        """Level 1 users cannot level down."""
        service = GamificationService()
        user = types.SimpleNamespace(level=1, level_down_defense=2)
        result = service.check_level_down(
            user, final_difficulty=5, correct_count=1, total_count=10
        )
        assert result["action"] == "none"

    def test_poor_accuracy_consumes_defense(self):
        """Accuracy < 30% with gap >= 2 consumes one defense point."""
        service = GamificationService()
        user = types.SimpleNamespace(level=5, level_down_defense=2)
        result = service.check_level_down(
            user, final_difficulty=3, correct_count=2, total_count=10
        )
        assert result["action"] == "defense_consumed"
        assert result["defense_remaining"] == 1

    def test_poor_accuracy_with_zero_defense_causes_level_down(self):
        """Accuracy < 30% with no defense causes level down and restores full defense."""
        service = GamificationService()
        user = types.SimpleNamespace(level=5, level_down_defense=0)
        result = service.check_level_down(
            user, final_difficulty=3, correct_count=2, total_count=10
        )
        assert result["action"] == "level_down"
        assert result["new_level"] == 4
        assert result["defense_remaining"] == MAX_DEFENSE

    def test_exact_30_percent_accuracy_returns_none(self):
        """Exact 30% accuracy (>= 0.3) does NOT trigger level down."""
        service = GamificationService()
        user = types.SimpleNamespace(level=5, level_down_defense=3)
        result = service.check_level_down(
            user, final_difficulty=3, correct_count=3, total_count=10
        )
        # accuracy = 0.3, condition is accuracy >= 0.3 → returns "none"
        assert result["action"] == "none"

    def test_exact_60_percent_accuracy_restores_defense(self):
        """Exact 60% accuracy restores defense."""
        service = GamificationService()
        user = types.SimpleNamespace(level=5, level_down_defense=1)
        result = service.check_level_down(
            user, final_difficulty=3, correct_count=6, total_count=10
        )
        assert result["action"] == "defense_restored"
        assert result["defense_remaining"] == 2
