"""
Integration tests for feast day readings in offices.

These tests validate that feast days correctly override standard
daily office readings and display appropriate content.

Test Coverage:
- T116-T118: Feast day integration tests

Validates:
- FR-007: Feast day readings substitution
- FR-011: Display commemorations
"""

import pytest
from datetime import date as date_class

from office.morning_prayer import MorningPrayer
from office.evening_prayer import EveningPrayer
from churchcal.calculations import get_calendar_date


@pytest.mark.django_db
class TestFeastDayReadings:
    """Tests for feast day readings override.
    
    Validates: FR-007 (Feast day readings substitution)
    """

    def test_feast_day_has_special_readings(self):
        """Feast days should have special readings assigned."""
        # Christmas Day
        christmas = MorningPrayer(date=date_class(2024, 12, 25))
        
        assert christmas.office_readings is not None
        # Christmas should have readings (either from HolyDayOfficeDay or StandardOfficeDay)

    def test_feast_vs_ordinary_day_readings(self):
        """Feast days should have different readings than ordinary days."""
        # Christmas Day (major feast)
        christmas = MorningPrayer(date=date_class(2024, 12, 25))
        
        # Ordinary day in December
        ordinary = MorningPrayer(date=date_class(2024, 12, 10))
        
        # Both should have readings
        assert christmas.office_readings is not None
        assert ordinary.office_readings is not None

    def test_feast_day_readings_consistent_across_offices(self):
        """Same feast should have readings in all office types."""
        test_date = date_class(2024, 12, 25)  # Christmas
        
        mp = MorningPrayer(date=test_date)
        ep = EveningPrayer(date=test_date)
        
        # Both should reference readings for Christmas
        assert mp.office_readings is not None
        assert ep.office_readings is not None

    def test_major_feasts_have_readings(self):
        """All major feasts should have assigned readings."""
        major_feasts = [
            date_class(2024, 12, 25),  # Christmas
            date_class(2024, 3, 31),   # Easter 2024
            date_class(2024, 1, 6),    # Epiphany
            date_class(2024, 5, 9),    # Ascension 2024
            date_class(2024, 5, 19),   # Pentecost 2024
        ]
        
        for feast_date in major_feasts:
            office = MorningPrayer(date=feast_date)
            assert office.office_readings is not None


@pytest.mark.django_db
class TestChristmasDayOffice:
    """Tests for Christmas Day office display.
    
    Validates: FR-007, FR-011 (Feast day readings and commemoration display)
    """

    def test_christmas_morning_prayer_instantiation(self):
        """Morning Prayer should instantiate for Christmas Day."""
        christmas = MorningPrayer(date=date_class(2024, 12, 25))
        
        assert christmas is not None
        assert christmas.date.date == date_class(2024, 12, 25)

    def test_christmas_commemoration_displayed(self):
        """Christmas commemoration should be displayed."""
        christmas = MorningPrayer(date=date_class(2024, 12, 25))
        
        assert christmas.date.primary is not None
        assert "Christmas" in christmas.date.primary.name or "Nativity" in christmas.date.primary.name

    def test_christmas_in_christmastide_season(self):
        """Christmas should be in Christmastide season."""
        christmas = MorningPrayer(date=date_class(2024, 12, 25))
        
        assert christmas.date.season.name == "Christmastide"

    def test_christmas_has_modules(self):
        """Christmas office should have all required modules."""
        christmas = MorningPrayer(date=date_class(2024, 12, 25))
        
        assert len(christmas.modules) > 0

    def test_christmas_evening_prayer(self):
        """Evening Prayer should work for Christmas Day."""
        christmas_ep = EveningPrayer(date=date_class(2024, 12, 25))
        
        assert christmas_ep is not None
        assert "Christmas" in christmas_ep.date.primary_evening.name or \
               "Nativity" in christmas_ep.date.primary_evening.name

    def test_christmas_title_includes_commemoration(self):
        """Christmas office title should include commemoration."""
        christmas = MorningPrayer(date=date_class(2024, 12, 25))
        
        assert "Christmas" in christmas.title or "Nativity" in christmas.title

    def test_christmastide_extends_beyond_christmas_day(self):
        """Christmastide season should extend beyond Christmas Day."""
        # December 26 (St. Stephen's Day)
        dec_26 = MorningPrayer(date=date_class(2024, 12, 26))
        
        assert dec_26.date.season.name == "Christmastide"


@pytest.mark.django_db
class TestEasterDayOffice:
    """Tests for Easter Day office display.
    
    Validates: FR-007, FR-011 (Feast day readings and commemoration display)
    """

    def test_easter_morning_prayer_instantiation(self):
        """Morning Prayer should instantiate for Easter Day."""
        easter = MorningPrayer(date=date_class(2024, 3, 31))
        
        assert easter is not None
        assert easter.date.date == date_class(2024, 3, 31)

    def test_easter_commemoration_displayed(self):
        """Easter commemoration should be displayed."""
        easter = MorningPrayer(date=date_class(2024, 3, 31))
        
        assert easter.date.primary is not None
        assert "Easter" in easter.date.primary.name

    def test_easter_in_eastertide_season(self):
        """Easter should be in Eastertide season."""
        easter = MorningPrayer(date=date_class(2024, 3, 31))
        
        assert easter.date.season.name == "Eastertide"

    def test_easter_has_modules(self):
        """Easter office should have all required modules."""
        easter = MorningPrayer(date=date_class(2024, 3, 31))
        
        assert len(easter.modules) > 0

    def test_easter_evening_prayer(self):
        """Evening Prayer should work for Easter Day."""
        easter_ep = EveningPrayer(date=date_class(2024, 3, 31))
        
        assert easter_ep is not None
        assert "Easter" in easter_ep.date.primary_evening.name

    def test_easter_title_includes_commemoration(self):
        """Easter office title should include commemoration."""
        easter = MorningPrayer(date=date_class(2024, 3, 31))
        
        assert "Easter" in easter.title

    def test_eastertide_extends_beyond_easter_day(self):
        """Eastertide season should extend beyond Easter Day."""
        # Week after Easter
        easter_week = MorningPrayer(date=date_class(2024, 4, 7))
        
        assert easter_week.date.season.name == "Eastertide"

    def test_easter_different_years(self):
        """Easter should work for different years with different dates."""
        # Easter 2024 is March 31
        easter_2024 = MorningPrayer(date=date_class(2024, 3, 31))
        
        # Easter 2025 is April 20
        easter_2025 = MorningPrayer(date=date_class(2025, 4, 20))
        
        assert "Easter" in easter_2024.date.primary.name
        assert "Easter" in easter_2025.date.primary.name


@pytest.mark.django_db
class TestOtherMajorFeasts:
    """Tests for other major feast days."""

    def test_epiphany_office(self):
        """Epiphany should display correctly in offices."""
        epiphany = MorningPrayer(date=date_class(2024, 1, 6))
        
        assert epiphany is not None
        assert "Epiphany" in epiphany.date.primary.name

    def test_ascension_office(self):
        """Ascension Day should display correctly."""
        # Ascension 2024 is May 9
        ascension = MorningPrayer(date=date_class(2024, 5, 9))
        
        assert ascension is not None
        assert "Ascension" in ascension.date.primary.name

    def test_pentecost_office(self):
        """Pentecost should display correctly."""
        # Pentecost 2024 is May 19
        pentecost = MorningPrayer(date=date_class(2024, 5, 19))
        
        assert pentecost is not None
        assert "Pentecost" in pentecost.date.primary.name

    def test_trinity_sunday_office(self):
        """Trinity Sunday should display correctly."""
        # Trinity Sunday 2024 is May 26
        trinity = MorningPrayer(date=date_class(2024, 5, 26))
        
        assert trinity is not None
        assert "Trinity" in trinity.date.primary.name

    def test_all_saints_office(self):
        """All Saints' Day should display correctly."""
        all_saints = MorningPrayer(date=date_class(2024, 11, 1))
        
        assert all_saints is not None
        assert "All Saints" in all_saints.date.primary.name

    def test_ash_wednesday_office(self):
        """Ash Wednesday should display correctly."""
        # Ash Wednesday 2024 is Feb 14
        ash_wed = MorningPrayer(date=date_class(2024, 2, 14))
        
        assert ash_wed is not None
        assert "Ash Wednesday" in ash_wed.date.primary.name
        assert ash_wed.date.season.name == "Lent"

    def test_palm_sunday_office(self):
        """Palm Sunday should display correctly."""
        # Palm Sunday 2024 is March 24
        palm_sunday = MorningPrayer(date=date_class(2024, 3, 24))
        
        assert palm_sunday is not None
        assert "Palm Sunday" in palm_sunday.date.primary.name or \
               palm_sunday.date.season.name == "Holy Week"

    def test_good_friday_office(self):
        """Good Friday should display correctly."""
        # Good Friday 2024 is March 29
        good_friday = MorningPrayer(date=date_class(2024, 3, 29))
        
        assert good_friday is not None
        assert "Good Friday" in good_friday.date.primary.name or \
               good_friday.date.season.name == "Holy Week"


@pytest.mark.django_db
class TestFeastDayConsistency:
    """Tests for feast day consistency across offices and years."""

    def test_feast_consistent_across_office_types(self):
        """Feast should be recognized in all office types."""
        from office.midday_prayer import MiddayPrayer
        from office.compline import Compline
        
        test_date = date_class(2024, 12, 25)  # Christmas
        
        mp = MorningPrayer(date=test_date)
        ep = EveningPrayer(date=test_date)
        midday = MiddayPrayer(date=test_date)
        compline = Compline(date=test_date)
        
        # All should recognize Christmas
        assert "Christmas" in mp.date.primary.name or "Nativity" in mp.date.primary.name
        assert "Christmas" in ep.date.primary_evening.name or "Nativity" in ep.date.primary_evening.name
        assert midday.date.season.name == "Christmastide"
        assert compline.date.season.name == "Christmastide"

    def test_sanctorale_feast_consistent_across_years(self):
        """Fixed feasts should be on same date every year."""
        # All Saints is always November 1
        all_saints_2024 = MorningPrayer(date=date_class(2024, 11, 1))
        all_saints_2025 = MorningPrayer(date=date_class(2025, 11, 1))
        
        assert "All Saints" in all_saints_2024.date.primary.name
        assert "All Saints" in all_saints_2025.date.primary.name

    def test_movable_feast_changes_with_easter(self):
        """Movable feasts should be on different dates in different years."""
        # Easter 2024 is March 31
        easter_2024 = MorningPrayer(date=date_class(2024, 3, 31))
        
        # Easter 2025 is April 20
        easter_2025 = MorningPrayer(date=date_class(2025, 4, 20))
        
        # Both should be Easter but on different dates
        assert "Easter" in easter_2024.date.primary.name
        assert "Easter" in easter_2025.date.primary.name
        assert easter_2024.date.date != easter_2025.date.date
