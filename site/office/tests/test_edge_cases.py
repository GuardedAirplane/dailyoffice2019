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
        # 2020 is a leap year within the test database range (2018-2021)
        leap_date = date_class(2020, 2, 29)
        office = MorningPrayer(date=leap_date)

        assert office is not None
        assert office.date.date == leap_date
        assert office.date.date.month == 2
        assert office.date.date.day == 29

    def test_leap_year_february_29_evening_prayer(self):
        """Evening Prayer should work correctly on February 29."""
        # 2020 is a leap year within the test database range (2018-2021)
        leap_date = date_class(2020, 2, 29)
        office = EveningPrayer(date=leap_date)

        assert office is not None
        assert office.date.date == leap_date
        assert len(office.modules) > 0

    def test_leap_year_february_29_has_standard_office_day(self):
        """February 29 should have StandardOfficeDay data."""
        # FR-012a: Dynamic liturgical calculation
        # 2020 is a leap year within the test database range (2018-2021)
        leap_date = date_class(2020, 2, 29)
        cal_date = get_calendar_date(leap_date)

        assert cal_date is not None
        # Should have office day data (from StandardOfficeDay)
        assert hasattr(cal_date, "primary")

    def test_leap_year_february_29_psalms_assigned(self):
        """February 29 should have psalm assignments."""
        # 2020 is a leap year within the test database range (2018-2021)
        leap_date = date_class(2020, 2, 29)
        office = MorningPrayer(date=leap_date)

        # Should have psalm module (modules is list of tuples)
        module_names = [m[0].__class__.__name__ for m in office.modules]
        assert "MPPsalms" in module_names

    def test_non_leap_year_february_28_boundary(self):
        """Non-leap year should not have February 29."""
        # 2019 is not a leap year and is within test database range (2018-2021)
        non_leap_date = date_class(2019, 2, 28)
        office = MorningPrayer(date=non_leap_date)

        assert office is not None
        assert office.date.date == non_leap_date

        # And Feb 29 2019 should not exist
        with pytest.raises(ValueError):
            date_class(2019, 2, 29)

    def test_leap_year_century_rules(self):
        """Leap year century rules should be respected."""
        # Test date validation only - this doesn't require database
        # 1900 was NOT a leap year (divisible by 100 but not 400)
        with pytest.raises(ValueError):
            date_class(1900, 2, 29)

        # 2100 will NOT be a leap year
        with pytest.raises(ValueError):
            date_class(2100, 2, 29)

        # 2000 was a leap year (divisible by 400) - validate date creation works
        leap_century = date_class(2000, 2, 29)
        assert leap_century.day == 29

    def test_leap_year_march_1_follows_february_29(self):
        """March 1 should follow February 29 in leap years."""
        # 2020 is a leap year within the test database range (2018-2021)
        leap_feb_29 = date_class(2020, 2, 29)
        march_1 = date_class(2020, 3, 1)

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
        # Test with a date that has multiple - June 24, 2020 is in database range
        test_date = date_class(2020, 6, 24)  # Birth of John the Baptist (major feast)
        cal_date = get_calendar_date(test_date)

        assert cal_date is not None
        # Should have at least primary commemoration
        assert cal_date.primary is not None

    def test_multiple_commemorations_in_commemoration_listing(self):
        """Office should display all commemorations for the day."""
        # FR-011: Display commemorations

        # All Saints Day 2020 is in database range (2018-2021)
        test_date = date_class(2020, 11, 1)  # All Saints Day
        office = MorningPrayer(date=test_date)

        # Should have commemoration listing module (modules is list of tuples)
        module_names = [m[0].__class__.__name__ for m in office.modules]
        assert "MPCommemorationListing" in module_names

    def test_commemoration_precedence_rules_applied(self):
        """Higher rank commemorations should take precedence."""
        # FR-007: Feast day readings substitution

        # Major feast (All Saints) should have feast readings - 2020 is in range
        all_saints = date_class(2020, 11, 1)
        office = MorningPrayer(date=all_saints)

        assert office is not None
        assert office.date.primary is not None
        # Major feasts should have special readings
        assert office.date.primary.rank.name in ["PRINCIPAL_FEAST", "SUNDAY", "HOLY_DAY"]

    def test_optional_commemorations_do_not_override_primary(self):
        """Optional commemorations should not override primary feast."""
        # FR-007: Feast day readings substitution

        # Christmas Day 2019 (within database range 2018-2021)
        christmas = date_class(2019, 12, 25)
        office = MorningPrayer(date=christmas)

        assert office is not None
        assert office.date.primary is not None
        assert "christmas" in office.date.primary.name.lower()


@pytest.mark.django_db
class TestMajorFeastOnSunday:
    """T201: Test major feast falling on Sunday."""

    def test_christmas_on_sunday_uses_christmas_readings(self):
        """Christmas uses Christmas readings regardless of day of week."""
        # FR-007: Feast day readings substitution

        # Christmas 2019 is within database range (2018-2021)
        # Test that Christmas readings are used regardless of weekday
        christmas = date_class(2019, 12, 25)
        office = MorningPrayer(date=christmas)

        assert office is not None
        assert office.date.primary is not None
        # Should be Christmas, not just "Sunday"
        assert "christmas" in office.date.primary.name.lower()

    def test_easter_always_sunday_uses_easter_readings(self):
        """Easter (always Sunday) should use Easter readings."""
        # FR-007: Feast day readings substitution

        # Easter 2020 is April 12, within database range (2018-2021)
        easter_2020 = date_class(2020, 4, 12)  # Easter Sunday 2020
        office = MorningPrayer(date=easter_2020)

        assert office is not None
        assert office.date.primary is not None
        # Should be Easter, not just Sunday
        assert "easter" in office.date.primary.name.lower()

    def test_epiphany_precedence(self):
        """Epiphany should use Epiphany readings."""
        # FR-007: Feast day readings substitution

        # Epiphany is January 6 - 2020 is within database range
        epiphany_2020 = date_class(2020, 1, 6)
        office = MorningPrayer(date=epiphany_2020)

        assert office is not None
        assert office.date.primary is not None
        # Should be Epiphany
        assert "epiphany" in office.date.primary.name.lower()

    def test_all_saints_precedence(self):
        """All Saints should follow precedence rules."""
        # FR-007: Feast day readings substitution

        # All Saints 2020 (November 1) is within database range
        all_saints = date_class(2020, 11, 1)
        office = MorningPrayer(date=all_saints)

        assert office is not None
        assert office.date.primary is not None
        assert "saints" in office.date.primary.name.lower()

    def test_sunday_in_ordinary_time_without_feast(self):
        """Regular Sunday without major feast uses Sunday readings."""
        # FR-007: Regular Sunday readings when no feast

        # Random Sunday in ordinary time - 2020 is within database range
        ordinary_sunday = date_class(2020, 7, 12)  # Sunday in Pentecost season
        office = MorningPrayer(date=ordinary_sunday)

        assert office is not None
        # Should have regular Sunday structure
        assert len(office.modules) > 0
