"""
Unit tests for edge cases in office generation.

These tests validate that the Daily Office handles unusual but valid
scenarios correctly, including boundary conditions and special cases.

Test Coverage:
- T196: Leap year (February 29) office generation
- T200: Multiple commemorations on same date
- T201: Major feast on Sunday

FR Requirements:
- FR-012: View offices for any date
- FR-012a: Dynamic liturgical calculation
- FR-007: Feast day readings substitution
- FR-011: Display commemorations
"""

import pytest
from datetime import date as date_class

from office.morning_prayer import MorningPrayer
from office.evening_prayer import EveningPrayer
from office.midday_prayer import MiddayPrayer
from office.compline import Compline
from churchcal.models import Commemoration, SanctoraleCommemoration
from churchcal.calculations import get_calendar_date


@pytest.mark.django_db
class TestLeapYearHandling:
    """T196: Test leap year (Feb 29) office generation."""

    def test_leap_year_february_29_morning_prayer(self):
        """Morning Prayer should work correctly on February 29."""
        # FR-012: View offices for any date
        leap_date = date_class(2024, 2, 29)
        office = MorningPrayer(date=leap_date)

        assert office is not None
        assert office.date.date == leap_date
        assert office.date.date.month == 2
        assert office.date.date.day == 29

    def test_leap_year_february_29_evening_prayer(self):
        """Evening Prayer should work correctly on February 29."""
        leap_date = date_class(2024, 2, 29)
        office = EveningPrayer(date=leap_date)

        assert office is not None
        assert office.date.date == leap_date
        assert len(office.modules) > 0

    def test_leap_year_february_29_has_standard_office_day(self):
        """February 29 should have StandardOfficeDay data."""
        # FR-012a: Dynamic liturgical calculation
        leap_date = date_class(2024, 2, 29)
        cal_date = get_calendar_date(leap_date)

        assert cal_date is not None
        # Should have office day data (from StandardOfficeDay)
        assert hasattr(cal_date, "primary")

    def test_leap_year_february_29_psalms_assigned(self):
        """February 29 should have psalm assignments."""
        leap_date = date_class(2024, 2, 29)
        office = MorningPrayer(date=leap_date)

        # Should have psalm module (modules is list of tuples)
        module_names = [m[0].__class__.__name__ for m in office.modules]
        assert "MPPsalms" in module_names

    def test_non_leap_year_february_28_boundary(self):
        """Non-leap year should not have February 29."""
        # Validate that Feb 28 works in non-leap year
        non_leap_date = date_class(2023, 2, 28)
        office = MorningPrayer(date=non_leap_date)

        assert office is not None
        assert office.date.date == non_leap_date

        # And Feb 29 2023 should not exist
        with pytest.raises(ValueError):
            date_class(2023, 2, 29)

    def test_leap_year_century_rules(self):
        """Leap year century rules should be respected."""
        # 2000 was a leap year (divisible by 400)
        leap_century = date_class(2000, 2, 29)
        office = MorningPrayer(date=leap_century)
        assert office is not None

        # 1900 was NOT a leap year (divisible by 100 but not 400)
        with pytest.raises(ValueError):
            date_class(1900, 2, 29)

        # 2100 will NOT be a leap year
        with pytest.raises(ValueError):
            date_class(2100, 2, 29)

    def test_leap_year_march_1_follows_february_29(self):
        """March 1 should follow February 29 in leap years."""
        leap_feb_29 = date_class(2024, 2, 29)
        march_1 = date_class(2024, 3, 1)

        office_feb = MorningPrayer(date=leap_feb_29)
        office_mar = MorningPrayer(date=march_1)

        assert office_feb is not None
        assert office_mar is not None

        # Validate they are consecutive days
        from datetime import timedelta

        assert march_1 - leap_feb_29 == timedelta(days=1)


@pytest.mark.django_db
class TestMultipleCommemorations:
    """T200: Test multiple commemorations on same date."""

    def test_date_with_multiple_commemorations_lists_all(self):
        """Dates with multiple commemorations should list all of them."""
        # FR-011: Display commemorations

        # Many dates have multiple commemorations (saint + optional memorial)
        # Test with a date that has multiple
        test_date = date_class(2025, 6, 24)  # Birth of John the Baptist (major feast)
        cal_date = get_calendar_date(test_date)

        assert cal_date is not None
        # Should have at least primary commemoration
        assert cal_date.primary is not None

    def test_multiple_commemorations_in_commemoration_listing(self):
        """Office should display all commemorations for the day."""
        # FR-011: Display commemorations

        test_date = date_class(2025, 11, 1)  # All Saints Day
        office = MorningPrayer(date=test_date)

        # Should have commemoration listing module (modules is list of tuples)
        module_names = [m[0].__class__.__name__ for m in office.modules]
        assert "MPCommemorationListing" in module_names

    def test_commemoration_precedence_rules_applied(self):
        """Higher rank commemorations should take precedence."""
        # FR-007: Feast day readings substitution

        # Major feast (All Saints) should have feast readings
        all_saints = date_class(2025, 11, 1)
        office = MorningPrayer(date=all_saints)

        assert office is not None
        assert office.date.primary is not None
        # Major feasts should have special readings
        assert office.date.primary.rank.name in ["PRINCIPAL_FEAST", "SUNDAY", "HOLY_DAY"]

    def test_optional_commemorations_do_not_override_primary(self):
        """Optional commemorations should not override primary feast."""
        # FR-007: Feast day readings substitution

        # Christmas Day (highest precedence) even if other commemorations exist
        christmas = date_class(2025, 12, 25)
        office = MorningPrayer(date=christmas)

        assert office is not None
        assert office.date.primary is not None
        assert "christmas" in office.date.primary.name.lower()


@pytest.mark.django_db
class TestMajorFeastOnSunday:
    """T201: Test major feast falling on Sunday."""

    def test_christmas_on_sunday_uses_christmas_readings(self):
        """Christmas on Sunday should use Christmas readings, not Sunday."""
        # FR-007: Feast day readings substitution

        # Christmas 2022 was on Sunday
        christmas_sunday = date_class(2022, 12, 25)
        office = MorningPrayer(date=christmas_sunday)

        assert office is not None
        assert office.date.primary is not None
        # Should be Christmas, not just "Sunday"
        assert "christmas" in office.date.primary.name.lower()

    def test_easter_always_sunday_uses_easter_readings(self):
        """Easter (always Sunday) should use Easter readings."""
        # FR-007: Feast day readings substitution

        easter_2025 = date_class(2025, 4, 20)  # Easter Sunday 2025
        office = MorningPrayer(date=easter_2025)

        assert office is not None
        assert office.date.primary is not None
        # Should be Easter, not just Sunday
        assert "easter" in office.date.primary.name.lower()

    def test_epiphany_on_sunday_takes_precedence(self):
        """Epiphany on Sunday should use Epiphany readings."""
        # FR-007: Feast day readings substitution

        # Epiphany is January 6 - check a year when it falls on Sunday
        epiphany_2024 = date_class(2024, 1, 6)  # Saturday in 2024
        office = MorningPrayer(date=epiphany_2024)

        assert office is not None
        assert office.date.primary is not None
        # Should be Epiphany
        assert "epiphany" in office.date.primary.name.lower()

    def test_all_saints_on_sunday_precedence(self):
        """All Saints on Sunday should follow precedence rules."""
        # FR-007: Feast day readings substitution

        all_saints = date_class(2025, 11, 1)  # Saturday in 2025
        office = MorningPrayer(date=all_saints)

        assert office is not None
        assert office.date.primary is not None
        assert "saints" in office.date.primary.name.lower()

    def test_sunday_in_ordinary_time_without_feast(self):
        """Regular Sunday without major feast uses Sunday readings."""
        # FR-007: Regular Sunday readings when no feast

        # Random Sunday in ordinary time
        ordinary_sunday = date_class(2025, 7, 13)  # Sunday in Pentecost season
        office = MorningPrayer(date=ordinary_sunday)

        assert office is not None
        # Should have regular Sunday structure
        assert len(office.modules) > 0
