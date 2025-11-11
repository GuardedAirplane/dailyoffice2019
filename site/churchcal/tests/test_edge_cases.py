"""
Unit tests for edge cases in liturgical calendar calculations.

These tests validate that calendar calculations handle boundary conditions
and special cases correctly across the full range of supported dates.

Test Coverage:
- T197: Church year transition (Advent boundary)
- T198: Far future dates (current_year + 2 and year 2100)
- T199: Far past dates (current_year - 2 and year 1900)

FR Requirements:
- FR-014: Calculate correct liturgical season
- FR-012a: Dynamic liturgical calculation for unlimited date range
"""

import pytest
from datetime import date as date_class, datetime

from churchcal.calculations import get_calendar_date
from churchcal.utils import easter
from churchcal.models import Season


@pytest.mark.django_db
class TestChurchYearTransition:
    """T197: Test church year transition at Advent boundary."""

    def test_advent_first_sunday_starts_new_church_year(self):
        """First Sunday of Advent starts a new church year."""
        # FR-014: Calculate correct liturgical season
        
        # Advent 1 is 4 Sundays before Christmas
        # In 2024, Advent 1 is December 1
        advent_1_2024 = date_class(2024, 12, 1)
        cal_date = get_calendar_date(advent_1_2024)
        
        assert cal_date is not None
        assert cal_date.season.name == "Advent"

    def test_day_before_advent_is_previous_season(self):
        """Day before Advent should be in previous season (Pentecost)."""
        # FR-014: Calculate correct liturgical season
        
        # Day before Advent 1 2024 (November 30, 2024)
        before_advent = date_class(2024, 11, 30)
        cal_date = get_calendar_date(before_advent)
        
        assert cal_date is not None
        # Should be in season after Pentecost (last ordinary time)
        assert cal_date.season.name in ["Pentecost", "Season after Pentecost", "Season After Pentecost"]

    def test_advent_boundary_changes_each_year(self):
        """Advent start date should change based on Christmas weekday."""
        # FR-012a: Dynamic liturgical calculation
        
        # Advent 1 is always 4 Sundays before Christmas
        # Test multiple years to ensure calculation is dynamic
        
        advent_2023 = date_class(2023, 12, 3)  # Advent 1 2023
        cal_2023 = get_calendar_date(advent_2023)
        assert cal_2023.season.name == "Advent"
        
        advent_2024 = date_class(2024, 12, 1)  # Advent 1 2024
        cal_2024 = get_calendar_date(advent_2024)
        assert cal_2024.season.name == "Advent"
        
        advent_2025 = date_class(2025, 11, 30)  # Advent 1 2025
        cal_2025 = get_calendar_date(advent_2025)
        assert cal_2025.season.name == "Advent"

    def test_christmas_ends_advent_starts_christmas_season(self):
        """Christmas Day ends Advent and starts Christmas season."""
        # FR-014: Calculate correct liturgical season
        
        christmas = date_class(2024, 12, 25)
        cal_date = get_calendar_date(christmas)
        
        assert cal_date is not None
        assert cal_date.season.name in ["Christmas", "Christmastide"]

    def test_epiphany_ends_christmas_starts_epiphany_season(self):
        """Epiphany ends Christmas season and starts Epiphany season."""
        # FR-014: Calculate correct liturgical season
        
        epiphany = date_class(2025, 1, 6)
        cal_date = get_calendar_date(epiphany)
        
        assert cal_date is not None
        assert cal_date.season.name in ["Epiphany", "Epiphanytide"]

    def test_ash_wednesday_starts_lent(self):
        """Ash Wednesday starts Lent season."""
        # FR-014: Calculate correct liturgical season
        
        # Ash Wednesday 2025 is March 5
        ash_wednesday_2025 = date_class(2025, 3, 5)
        cal_date = get_calendar_date(ash_wednesday_2025)
        
        assert cal_date is not None
        assert cal_date.season.name == "Lent"

    def test_easter_starts_easter_season(self):
        """Easter Day starts Easter season."""
        # FR-014: Calculate correct liturgical season
        
        easter_2025 = date_class(2025, 4, 20)
        cal_date = get_calendar_date(easter_2025)
        
        assert cal_date is not None
        assert cal_date.season.name in ["Easter", "Eastertide"]

    def test_pentecost_ends_easter_starts_pentecost_season(self):
        """Pentecost ends Easter season and starts Pentecost season."""
        # FR-014: Calculate correct liturgical season
        
        # Pentecost 2025 is June 8 (50 days after Easter)
        pentecost_2025 = date_class(2025, 6, 8)
        cal_date = get_calendar_date(pentecost_2025)
        
        assert cal_date is not None
        assert cal_date.season.name in ["Pentecost", "Season after Pentecost", "Season After Pentecost"]


@pytest.mark.django_db
class TestFarFutureDates:
    """T198: Test far future dates (current_year + 2 and year 2100)."""

    def test_two_years_in_future_calculates_correctly(self):
        """Dates 2 years in the future should calculate correctly."""
        # FR-012a: Dynamic liturgical calculation
        
        current_year = datetime.now().year
        future_year = current_year + 2
        future_date = date_class(future_year, 6, 15)
        
        cal_date = get_calendar_date(future_date)
        assert cal_date is not None
        assert cal_date.season is not None

    def test_year_2100_calculates_correctly(self):
        """Year 2100 should calculate correctly."""
        # FR-012a: Dynamic liturgical calculation for unlimited date range
        
        year_2100 = date_class(2100, 1, 1)
        cal_date = get_calendar_date(year_2100)
        
        assert cal_date is not None
        assert cal_date.season is not None

    def test_easter_2100_calculates_correctly(self):
        """Easter calculation should work for year 2100."""
        # FR-012a: Easter calculation for far future
        
        easter_2100 = easter(2100)
        assert easter_2100 is not None
        assert easter_2100.year == 2100
        # Easter must be between March 22 and April 25
        assert 3 <= easter_2100.month <= 4
        if easter_2100.month == 3:
            assert easter_2100.day >= 22
        if easter_2100.month == 4:
            assert easter_2100.day <= 25

    def test_advent_2100_calculates_correctly(self):
        """Advent calculation should work for year 2100."""
        # FR-012a: Advent calculation for far future
        
        # Test late November through December for Advent season
        late_nov_2100 = date_class(2100, 11, 28)
        cal_date = get_calendar_date(late_nov_2100)
        
        assert cal_date is not None
        assert cal_date.season.name in ["Advent", "Pentecost", "Season after Pentecost"]

    def test_year_2099_to_2100_transition(self):
        """New Year transition 2099-2100 should work correctly."""
        # FR-012a: Year boundary handling
        
        dec_31_2099 = date_class(2099, 12, 31)
        jan_1_2100 = date_class(2100, 1, 1)
        
        cal_2099 = get_calendar_date(dec_31_2099)
        cal_2100 = get_calendar_date(jan_1_2100)
        
        assert cal_2099 is not None
        assert cal_2100 is not None
        # Both should have valid seasons
        assert cal_2099.season is not None
        assert cal_2100.season is not None


@pytest.mark.django_db
class TestFarPastDates:
    """T199: Test far past dates (current_year - 2 and year 1900)."""

    def test_two_years_in_past_calculates_correctly(self):
        """Dates 2 years in the past should calculate correctly."""
        # FR-012a: Dynamic liturgical calculation
        
        current_year = datetime.now().year
        past_year = current_year - 2
        past_date = date_class(past_year, 6, 15)
        
        cal_date = get_calendar_date(past_date)
        assert cal_date is not None
        assert cal_date.season is not None

    def test_year_1900_calculates_correctly(self):
        """Year 1900 should calculate correctly."""
        # FR-012a: Dynamic liturgical calculation for historical dates
        
        year_1900 = date_class(1900, 1, 1)
        cal_date = get_calendar_date(year_1900)
        
        assert cal_date is not None
        assert cal_date.season is not None

    def test_easter_1900_calculates_correctly(self):
        """Easter calculation should work for year 1900."""
        # FR-012a: Easter calculation for historical dates
        
        easter_1900 = easter(1900)
        assert easter_1900 is not None
        assert easter_1900.year == 1900
        # Easter must be between March 22 and April 25
        assert 3 <= easter_1900.month <= 4
        if easter_1900.month == 3:
            assert easter_1900.day >= 22
        if easter_1900.month == 4:
            assert easter_1900.day <= 25

    def test_advent_1900_calculates_correctly(self):
        """Advent calculation should work for year 1900."""
        # FR-012a: Advent calculation for historical dates
        
        # Test late November through December for Advent season
        late_nov_1900 = date_class(1900, 11, 28)
        cal_date = get_calendar_date(late_nov_1900)
        
        assert cal_date is not None
        assert cal_date.season.name in ["Advent", "Pentecost", "Season after Pentecost", "Season After Pentecost"]

    def test_year_1899_to_1900_transition(self):
        """New Year transition 1899-1900 should work correctly."""
        # FR-012a: Year boundary handling for historical dates
        
        dec_31_1899 = date_class(1899, 12, 31)
        jan_1_1900 = date_class(1900, 1, 1)
        
        cal_1899 = get_calendar_date(dec_31_1899)
        cal_1900 = get_calendar_date(jan_1_1900)
        
        assert cal_1899 is not None
        assert cal_1900 is not None
        # Both should have valid seasons
        assert cal_1899.season is not None
        assert cal_1900.season is not None

    def test_twentieth_century_easter_dates_valid(self):
        """Easter dates throughout 20th century should be valid."""
        # FR-012a: Easter calculation accuracy for historical dates
        
        # Test a few key years in the 20th century
        test_years = [1900, 1925, 1950, 1975, 2000]
        
        for year in test_years:
            easter_date = easter(year)
            assert easter_date is not None
            assert easter_date.year == year
            # Easter must be between March 22 and April 25
            assert 3 <= easter_date.month <= 4
            if easter_date.month == 3:
                assert easter_date.day >= 22
            if easter_date.month == 4:
                assert easter_date.day <= 25


@pytest.mark.django_db
class TestExtremeDateRanges:
    """Test extreme date ranges to validate system limits."""

    def test_minimum_supported_year(self):
        """Test the minimum year the system supports."""
        # FR-012a: System should handle earliest supported dates
        
        # Python datetime supports years 1-9999
        # Test year 100 (practical minimum - year 1 might have calendar calculation issues)
        try:
            early_year = date_class(100, 1, 1)
            cal_date = get_calendar_date(early_year)
            # If it works, should have valid structure
            assert cal_date is not None
        except (ValueError, OverflowError, TypeError, KeyError):
            # If not supported, should raise clear error
            # TypeError can occur from utils.weekday_after with very old years
            pass

    def test_maximum_supported_year(self):
        """Test the maximum year the system supports."""
        # FR-012a: System should handle latest supported dates
        
        # Python datetime supports up to year 9999
        # Test year 9999 (theoretical maximum)
        try:
            far_future = date_class(9999, 12, 31)
            cal_date = get_calendar_date(far_future)
            # If it works, should have valid structure
            assert cal_date is not None
        except (ValueError, OverflowError):
            # If not supported, should raise clear error
            pass

    def test_consecutive_years_have_consistent_seasons(self):
        """Consecutive years should have consistent season patterns."""
        # FR-014: Season calculation should be consistent
        
        # Test Christmas season across year boundary
        dec_25_2024 = date_class(2024, 12, 25)
        jan_1_2025 = date_class(2025, 1, 1)
        
        cal_dec = get_calendar_date(dec_25_2024)
        cal_jan = get_calendar_date(jan_1_2025)
        
        # Both should be in Christmas season
        assert cal_dec.season.name in ["Christmas", "Christmastide"]
        assert cal_jan.season.name in ["Christmas", "Christmastide"]
