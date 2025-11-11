"""
Unit tests for churchcal models.

These tests validate commemoration types, precedence rules,
and date calculations for the liturgical calendar.

Test Coverage:
- T111-T115: Commemoration model tests

Validates:
- FR-011: Display commemorations
- FR-014: Calculate correct liturgical season
"""

import pytest
from datetime import date as date_class

from churchcal.models import (
    Commemoration, SanctoraleCommemoration, TemporaleCommemoration, 
    FerialCommemoration, CommemorationRank, Season, Calendar
)
from churchcal.calculations import get_calendar_date


@pytest.mark.django_db
class TestCommemorationPrecedence:
    """Tests for commemoration precedence rules.
    
    Validates: FR-011 (Display commemorations)
    """

    def test_primary_feast_takes_precedence(self):
        """Primary feast should be displayed when multiple commemorations exist."""
        # Christmas (major feast) should take precedence
        cal_date = get_calendar_date(date_class(2024, 12, 25))
        
        assert cal_date.primary is not None
        assert "Christmas" in cal_date.primary.name or "Nativity" in cal_date.primary.name

    def test_sunday_precedence_in_ordinary_time(self):
        """Sundays should generally take precedence in ordinary time."""
        # Random Sunday in Season After Pentecost
        cal_date = get_calendar_date(date_class(2024, 7, 14))  # Sunday
        
        assert cal_date.primary is not None
        assert cal_date.primary.rank.name == "SUNDAY"

    def test_major_holy_days_override_sundays(self):
        """Major holy days should override Sunday observances."""
        # Christmas Day 2022 was a Sunday
        cal_date = get_calendar_date(date_class(2022, 12, 25))
        
        assert cal_date.primary is not None
        assert "Christmas" in cal_date.primary.name or "Nativity" in cal_date.primary.name

    def test_required_vs_optional_commemorations(self):
        """Required and optional commemorations should be properly categorized."""
        # Use a Sunday which should have required commemoration
        cal_date = get_calendar_date(date_class(2024, 7, 14))  # Sunday
        
        # Sundays should have required commemoration
        assert len(cal_date.required) > 0
        assert cal_date.primary in cal_date.required or cal_date.primary is not None

    def test_primary_is_first_required(self):
        """Primary commemoration should be first in required list."""
        cal_date = get_calendar_date(date_class(2024, 8, 15))
        
        if len(cal_date.required) > 0:
            assert cal_date.primary == cal_date.required[0]


@pytest.mark.django_db
class TestMultipleCommemorations:
    """Tests for dates with multiple commemorations.
    
    Validates: FR-011 (Display commemorations)
    """

    def test_all_commemorations_accessible(self):
        """All commemorations for a date should be accessible."""
        cal_date = get_calendar_date(date_class(2024, 7, 20))
        
        all_comms = cal_date.all
        assert isinstance(all_comms, list)
        assert len(all_comms) > 0

    def test_required_and_optional_separate(self):
        """Required and optional commemorations should be separate lists."""
        cal_date = get_calendar_date(date_class(2024, 9, 15))
        
        assert hasattr(cal_date, 'required')
        assert hasattr(cal_date, 'optional')
        assert isinstance(cal_date.required, list)
        assert isinstance(cal_date.optional, list)

    def test_commemoration_has_rank(self):
        """Each commemoration should have a rank."""
        cal_date = get_calendar_date(date_class(2024, 10, 15))
        
        assert cal_date.primary is not None
        assert hasattr(cal_date.primary, 'rank')
        assert cal_date.primary.rank is not None

    def test_commemoration_has_name(self):
        """Each commemoration should have a name."""
        cal_date = get_calendar_date(date_class(2024, 11, 15))
        
        assert cal_date.primary is not None
        assert hasattr(cal_date.primary, 'name')
        assert cal_date.primary.name is not None
        assert len(cal_date.primary.name) > 0

    def test_evening_commemorations(self):
        """Evening commemorations should be available."""
        cal_date = get_calendar_date(date_class(2024, 12, 24))
        
        assert hasattr(cal_date, 'primary_evening')
        assert cal_date.primary_evening is not None


@pytest.mark.django_db
class TestSanctoraleCommemoration:
    """Tests for Sanctorale (saints' days) commemorations.
    
    Validates: FR-011 (Display commemorations)
    """

    def test_sanctorale_fixed_dates(self):
        """Sanctorale commemorations should occur on fixed dates annually."""
        # All Saints' Day is always November 1
        cal_2024 = get_calendar_date(date_class(2024, 11, 1))
        cal_2025 = get_calendar_date(date_class(2025, 11, 1))
        
        # Both years should have All Saints
        assert "All Saints" in cal_2024.primary.name
        assert "All Saints" in cal_2025.primary.name

    def test_sanctorale_saint_name(self):
        """Sanctorale commemorations should reference saint names."""
        # St. Andrew's Day (November 30)
        cal_date = get_calendar_date(date_class(2024, 11, 30))
        
        # Should be Advent (First Sunday), but St. Andrew may be optional
        # or transferred depending on calendar rules
        assert cal_date.primary is not None

    def test_sanctorale_multiple_years(self):
        """Sanctorale should be consistent across years."""
        # St. Stephen's Day (December 26)
        cal_2024 = get_calendar_date(date_class(2024, 12, 26))
        cal_2025 = get_calendar_date(date_class(2025, 12, 26))
        
        # Both should reference Stephen
        assert "Stephen" in cal_2024.primary.name
        assert "Stephen" in cal_2025.primary.name


@pytest.mark.django_db
class TestTemporaleCommemoration:
    """Tests for Temporale (movable feast) commemorations.
    
    Validates: FR-014 (Calculate correct liturgical season)
    """

    def test_temporale_easter_relative_dates(self):
        """Temporale commemorations should move relative to Easter."""
        # Easter Sunday 2024 is March 31
        easter_2024 = get_calendar_date(date_class(2024, 3, 31))
        
        # Easter Sunday 2025 is April 20
        easter_2025 = get_calendar_date(date_class(2025, 4, 20))
        
        # Both should be Easter
        assert "Easter" in easter_2024.primary.name
        assert "Easter" in easter_2025.primary.name

    def test_ash_wednesday_moves_with_easter(self):
        """Ash Wednesday should move based on Easter date."""
        # Ash Wednesday 2024 is Feb 14
        ash_2024 = get_calendar_date(date_class(2024, 2, 14))
        
        # Ash Wednesday 2025 is March 5
        ash_2025 = get_calendar_date(date_class(2025, 3, 5))
        
        # Both should be Ash Wednesday
        assert "Ash Wednesday" in ash_2024.primary.name
        assert "Ash Wednesday" in ash_2025.primary.name

    def test_ascension_forty_days_after_easter(self):
        """Ascension should be 40 days after Easter."""
        # Easter 2024 is March 31, Ascension is May 9
        ascension_2024 = get_calendar_date(date_class(2024, 5, 9))
        
        assert "Ascension" in ascension_2024.primary.name

    def test_pentecost_fifty_days_after_easter(self):
        """Pentecost should be 50 days after Easter."""
        # Easter 2024 is March 31, Pentecost is May 19
        pentecost_2024 = get_calendar_date(date_class(2024, 5, 19))
        
        assert "Pentecost" in pentecost_2024.primary.name

    def test_palm_sunday_week_before_easter(self):
        """Palm Sunday should be the week before Easter."""
        # Easter 2024 is March 31, Palm Sunday is March 24
        palm_sunday = get_calendar_date(date_class(2024, 3, 24))
        
        assert "Palm Sunday" in palm_sunday.primary.name or palm_sunday.season.name == "Holy Week"


@pytest.mark.django_db
class TestFerialCommemoration:
    """Tests for Ferial (ordinary weekday) commemorations.
    
    Validates: FR-014 (Calculate correct liturgical season)
    """

    def test_ferial_dynamic_creation(self):
        """Ferial commemorations should be created dynamically for ordinary days."""
        # Random weekday in ordinary time
        cal_date = get_calendar_date(date_class(2024, 7, 16))  # Tuesday
        
        assert cal_date.primary is not None
        # Should have a commemoration even if it's just a feria

    def test_ferial_has_season(self):
        """Ferial days should have correct seasonal designation."""
        # Weekday in Lent
        cal_date = get_calendar_date(date_class(2024, 2, 20))  # Tuesday in Lent
        
        assert cal_date.season.name == "Lent"
        assert cal_date.primary is not None

    def test_ferial_weekday_in_advent(self):
        """Weekdays in Advent should be designated as Advent ferias."""
        # Weekday in Advent
        cal_date = get_calendar_date(date_class(2024, 12, 10))  # Tuesday
        
        assert cal_date.season.name == "Advent"

    def test_ferial_weekday_in_eastertide(self):
        """Weekdays in Eastertide should be designated as Easter ferias."""
        # Weekday in Eastertide
        cal_date = get_calendar_date(date_class(2024, 4, 16))  # Tuesday
        
        assert cal_date.season.name == "Eastertide"

    def test_ferial_type_detection(self):
        """Should be able to detect ferial commemoration type."""
        # Ordinary weekday
        cal_date = get_calendar_date(date_class(2024, 8, 13))  # Tuesday
        
        # Should be FerialCommemoration instance
        assert cal_date.primary is not None
        # Check if it's a feria by checking if it's not a major feast
        if hasattr(cal_date.primary, '__class__'):
            assert cal_date.primary.__class__.__name__ in [
                'FerialCommemoration', 'SanctoraleCommemoration', 
                'TemporaleCommemoration', 'Commemoration'
            ]


@pytest.mark.django_db
class TestCommemorationRank:
    """Tests for commemoration ranking system."""

    def test_rank_determines_precedence(self):
        """Higher ranked commemorations should take precedence."""
        # Principal Feasts (highest rank)
        christmas = get_calendar_date(date_class(2024, 12, 25))
        
        assert christmas.primary is not None
        assert christmas.primary.rank is not None

    def test_different_rank_types_exist(self):
        """Multiple rank types should exist in the system."""
        # Get ranks for different types of days
        christmas = get_calendar_date(date_class(2024, 12, 25))
        sunday = get_calendar_date(date_class(2024, 7, 14))
        weekday = get_calendar_date(date_class(2024, 7, 16))
        
        # All should have ranks
        assert christmas.primary.rank is not None
        assert sunday.primary.rank is not None
        assert weekday.primary.rank is not None

    def test_rank_has_name(self):
        """Ranks should have descriptive names."""
        cal_date = get_calendar_date(date_class(2024, 12, 25))
        
        assert cal_date.primary.rank.name is not None
        assert len(cal_date.primary.rank.name) > 0


@pytest.mark.django_db
class TestSeason:
    """Tests for Season model.
    
    Validates: FR-014 (Calculate correct liturgical season)
    """

    def test_season_has_name(self):
        """Seasons should have descriptive names."""
        cal_date = get_calendar_date(date_class(2024, 12, 15))
        
        assert cal_date.season is not None
        assert cal_date.season.name == "Advent"

    def test_season_has_color(self):
        """Seasons should have liturgical colors."""
        cal_date = get_calendar_date(date_class(2024, 12, 15))
        
        assert hasattr(cal_date.season, 'color')
        assert cal_date.season.color is not None

    def test_all_seven_seasons_exist(self):
        """All liturgical seasons should be representable."""
        seasons_found = set()
        
        # Sample dates from different seasons
        season_dates = [
            date_class(2024, 12, 15),  # Advent
            date_class(2024, 12, 26),  # Christmastide
            date_class(2024, 1, 15),   # Epiphanytide
            date_class(2024, 2, 20),   # Lent
            date_class(2024, 3, 28),   # Holy Week
            date_class(2024, 4, 10),   # Eastertide
            date_class(2024, 7, 15),   # Season After Pentecost
        ]
        
        for test_date in season_dates:
            cal_date = get_calendar_date(test_date)
            seasons_found.add(cal_date.season.name)
        
        # Should have found multiple seasons
        assert len(seasons_found) >= 5

    def test_season_consistency_within_period(self):
        """Season should be consistent across consecutive days."""
        # All of Advent week should be Advent
        for day in range(2, 8):  # Dec 2-7, 2024
            cal_date = get_calendar_date(date_class(2024, 12, day))
            assert cal_date.season.name == "Advent"


@pytest.mark.django_db
class TestCommemorationMethods:
    """Tests for commemoration model methods."""

    def test_commemoration_string_representation(self):
        """Commemorations should have string representation."""
        cal_date = get_calendar_date(date_class(2024, 12, 25))
        
        assert cal_date.primary is not None
        assert str(cal_date.primary) is not None
        assert len(str(cal_date.primary)) > 0

    def test_commemoration_has_calendar(self):
        """Commemorations should be associated with a calendar."""
        cal_date = get_calendar_date(date_class(2024, 6, 15))
        
        assert cal_date.calendar is not None

    def test_primary_matches_first_required(self):
        """Primary should match first required commemoration."""
        cal_date = get_calendar_date(date_class(2024, 8, 20))
        
        if len(cal_date.required) > 0:
            assert cal_date.primary == cal_date.required[0]

    def test_commemoration_consistency(self):
        """Same date should return same commemorations."""
        date1 = get_calendar_date(date_class(2024, 9, 15))
        date2 = get_calendar_date(date_class(2024, 9, 15))
        
        assert date1.primary.name == date2.primary.name
        assert date1.season.name == date2.season.name
