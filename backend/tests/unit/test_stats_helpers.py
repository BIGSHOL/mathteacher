"""
Unit tests for stats service helper functions.

Tests KST timezone conversions and accuracy calculations.
"""
import pytest
from datetime import datetime, date, timezone, timedelta
from app.services.stats_service import _kst_day_utc_range, _to_kst_date, StatsService


class TestKstDayUtcRange:
    """Tests for _kst_day_utc_range helper function."""

    def test_kst_day_to_utc_range(self):
        """KST day converts to correct UTC range."""
        kst_day = date(2024, 1, 15)
        start_utc, end_utc = _kst_day_utc_range(kst_day)

        # KST 2024-01-15 00:00 = UTC 2024-01-14 15:00 (naive datetime)
        expected_start = datetime(2024, 1, 14, 15, 0, 0)
        # KST 2024-01-16 00:00 = UTC 2024-01-15 15:00
        expected_end = datetime(2024, 1, 15, 15, 0, 0)

        assert start_utc == expected_start
        assert end_utc == expected_end

    def test_span_is_exactly_24_hours(self):
        """UTC range spans exactly 24 hours."""
        kst_day = date(2024, 3, 10)
        start_utc, end_utc = _kst_day_utc_range(kst_day)

        delta = end_utc - start_utc
        assert delta == timedelta(hours=24)

    def test_different_dates(self):
        """Different KST dates produce different UTC ranges."""
        day1 = date(2024, 1, 15)
        day2 = date(2024, 1, 16)

        start1, end1 = _kst_day_utc_range(day1)
        start2, end2 = _kst_day_utc_range(day2)

        assert start1 != start2
        assert end1 != end2
        assert (start2 - start1) == timedelta(days=1)


class TestToKstDate:
    """Tests for _to_kst_date helper function."""

    def test_none_returns_none(self):
        """None input returns None."""
        result = _to_kst_date(None)
        assert result is None

    def test_utc_before_kst_midnight(self):
        """UTC datetime before KST midnight converts to same date."""
        # UTC 2024-01-15 14:00 -> KST 2024-01-15 23:00 (same day)
        dt = datetime(2024, 1, 15, 14, 0, 0, tzinfo=timezone.utc)
        result = _to_kst_date(dt)
        assert result == date(2024, 1, 15)

    def test_utc_after_kst_midnight(self):
        """UTC datetime after KST midnight converts to next date."""
        # UTC 2024-01-15 16:00 -> KST 2024-01-16 01:00 (next day)
        dt = datetime(2024, 1, 15, 16, 0, 0, tzinfo=timezone.utc)
        result = _to_kst_date(dt)
        assert result == date(2024, 1, 16)

    def test_utc_exactly_at_kst_midnight(self):
        """UTC datetime exactly at KST midnight (UTC 15:00)."""
        # UTC 2024-01-15 15:00 -> KST 2024-01-16 00:00
        dt = datetime(2024, 1, 15, 15, 0, 0, tzinfo=timezone.utc)
        result = _to_kst_date(dt)
        assert result == date(2024, 1, 16)


class TestCalculateAccuracyRate:
    """Tests for StatsService.calculate_accuracy_rate method."""

    @pytest.fixture
    def stats_service(self):
        """Create StatsService instance with mock db."""
        return StatsService(db=None)

    def test_zero_total_returns_zero(self, stats_service):
        """Zero total returns 0.0 accuracy."""
        result = stats_service.calculate_accuracy_rate(correct=0, total=0)
        assert result == 0.0

    def test_perfect_accuracy(self, stats_service):
        """All correct returns 100.0 accuracy."""
        result = stats_service.calculate_accuracy_rate(correct=10, total=10)
        assert result == 100.0

    def test_partial_accuracy(self, stats_service):
        """Partial correct returns proper percentage."""
        result = stats_service.calculate_accuracy_rate(correct=8, total=10)
        assert result == 80.0

    def test_accuracy_with_rounding(self, stats_service):
        """Accuracy is rounded to one decimal place."""
        result = stats_service.calculate_accuracy_rate(correct=3, total=7)
        assert result == 42.9  # 42.857... rounded to 42.9

    def test_zero_correct(self, stats_service):
        """Zero correct returns 0.0 accuracy."""
        result = stats_service.calculate_accuracy_rate(correct=0, total=10)
        assert result == 0.0
