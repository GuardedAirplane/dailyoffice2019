"""
Unit tests for date handling across all office types (US6).

These tests validate that offices correctly handle edge cases
in date processing and liturgical calculations.

Test Coverage:
- T085-T089: Date edge cases and boundary conditions
"""

import pytest
from datetime import date as date_class

from office.morning_prayer import MorningPrayer
from office.evening_prayer import EveningPrayer
from office.midday_prayer import MiddayPrayer
from office.compline import Compline
from churchcal.calculations import get_calendar_date


@pytest.mark.django_db
class TestOfficeAcceptsAnyDate:
    """Tests that all office types accept any valid date."""

    def test_morning_prayer_accepts_far_past_date(self):
        """Morning Prayer should accept dates from early 20th century."""
        # Database has StandardOfficeDay for all days of year
        old_date = date_class(1900, 1, 1)
        office = MorningPrayer(date=old_date)

        assert office is not None
        assert office.date.date == old_date

    def test_evening_prayer_accepts_far_future_date(self):
        """Evening Prayer should accept dates far in the future."""
        future_date = date_class(2100, 12, 31)
        office = EveningPrayer(date=future_date)

        assert office is not None
        assert office.date.date == future_date

    def test_midday_prayer_accepts_current_century(self):
        """Midday Prayer should accept dates throughout 21st century."""
        mid_century = date_class(2050, 6, 15)
        office = MiddayPrayer(date=mid_century)

        assert office is not None
        assert office.date.date == mid_century

    def test_compline_accepts_various_decades(self):
        """Compline should accept dates from various decades."""
        dates = [
            date_class(1950, 1, 1),
            date_class(1975, 6, 15),
            date_class(2000, 12, 25),
            date_class(2025, 3, 15),
            date_class(2075, 9, 30),
        ]

        for test_date in dates:
            office = Compline(date=test_date)
            assert office is not None
            assert office.date.date == test_date


@pytest.mark.django_db
class TestLiturgicalCalculations:
    """Tests for dynamic liturgical calculations."""

    def test_future_easter_calculation(self):
        """Liturgical calendar should calculate Easter for future years."""
        # Easter 2050 is April 10
        easter_2050 = date_class(2050, 4, 10)
        calendar_date = get_calendar_date(easter_2050)

        assert calendar_date is not None
        assert "Easter" in calendar_date.primary.name

    def test_past_easter_calculation(self):
        """Liturgical calendar should calculate Easter for past years."""
        # Easter 2020 was April 12
        easter_2020 = date_class(2020, 4, 12)
        calendar_date = get_calendar_date(easter_2020)

        assert calendar_date is not None
        assert "Easter" in calendar_date.primary.name

    def test_future_advent_calculation(self):
        """Liturgical calendar should calculate Advent for future years."""
        # First Sunday of Advent 2050 is November 27
        advent_2050 = date_class(2050, 11, 27)
        calendar_date = get_calendar_date(advent_2050)

        assert calendar_date is not None
        assert calendar_date.season.name == "Advent"

    def test_season_transitions_correctly(self):
        """Liturgical seasons should transition at correct boundaries."""
        # Test transition from one season to another
        dates_and_seasons = [
            (date_class(2024, 2, 13), "Epiphanytide"),  # Day before Ash Wednesday
            (date_class(2024, 2, 14), "Lent"),  # Ash Wednesday
            (date_class(2024, 3, 30), "Holy Week"),  # Holy Saturday
            (date_class(2024, 3, 31), "Eastertide"),  # Easter Day
            (date_class(2024, 12, 1), "Advent"),  # First Sunday of Advent 2024
        ]

        for test_date, expected_season in dates_and_seasons:
            calendar_date = get_calendar_date(test_date)
            assert (
                calendar_date.season.name == expected_season
            ), f"Date {test_date} should be in {expected_season}, got {calendar_date.season.name}"


@pytest.mark.django_db
class TestLeapYearHandling:
    """Tests for leap year date handling."""

    def test_leap_year_feb_29_all_offices(self):
        """All offices should handle Feb 29 in leap years."""
        leap_date = date_class(2024, 2, 29)

        mp = MorningPrayer(date=leap_date)
        ep = EveningPrayer(date=leap_date)
        midday = MiddayPrayer(date=leap_date)
        compline = Compline(date=leap_date)

        assert mp.date.date == leap_date
        assert ep.date.date == leap_date
        assert midday.date.date == leap_date
        assert compline.date.date == leap_date

    def test_leap_year_2000(self):
        """Century leap year (2000) should be handled correctly."""
        leap_date = date_class(2000, 2, 29)
        office = MorningPrayer(date=leap_date)

        assert office.date.date == leap_date

    def test_leap_year_far_future(self):
        """Future leap years should be handled correctly."""
        leap_date = date_class(2048, 2, 29)
        office = EveningPrayer(date=leap_date)

        assert office.date.date == leap_date

    def test_non_leap_year_feb_28(self):
        """Non-leap years should handle Feb 28 correctly."""
        feb_28 = date_class(2023, 2, 28)
        office = MiddayPrayer(date=feb_28)

        assert office.date.date == feb_28


@pytest.mark.django_db
class TestChurchYearTransitions:
    """Tests for church year boundary transitions."""

    def test_advent_starts_new_church_year(self):
        """First Sunday of Advent begins new church year."""
        # Last day of previous church year (day before Advent)
        last_day_old_year = date_class(2024, 11, 30)  # Saturday before Advent
        first_day_new_year = date_class(2024, 12, 1)  # First Sunday of Advent

        old_cal = get_calendar_date(last_day_old_year)
        new_cal = get_calendar_date(first_day_new_year)

        # Before Advent should not be Advent
        assert old_cal.season.name != "Advent"
        # Advent Sunday should be Advent
        assert new_cal.season.name == "Advent"

    def test_epiphany_to_lent_transition(self):
        """Transition from Epiphanytide to Lent on Ash Wednesday."""
        # 2024: Ash Wednesday is Feb 14
        before_ash_wed = date_class(2024, 2, 13)
        ash_wednesday = date_class(2024, 2, 14)

        before_cal = get_calendar_date(before_ash_wed)
        ash_cal = get_calendar_date(ash_wednesday)

        assert before_cal.season.name == "Epiphanytide"
        assert ash_cal.season.name == "Lent"

    def test_lent_to_easter_transition(self):
        """Transition from Holy Week to Eastertide on Easter Day."""
        # 2024: Easter is March 31
        holy_saturday = date_class(2024, 3, 30)
        easter_day = date_class(2024, 3, 31)

        sat_cal = get_calendar_date(holy_saturday)
        easter_cal = get_calendar_date(easter_day)

        assert sat_cal.season.name == "Holy Week"
        assert easter_cal.season.name == "Eastertide"

    def test_eastertide_to_ordinary_time_transition(self):
        """Transition from Eastertide to Season After Pentecost."""
        # 2024: Pentecost is May 19, Trinity Sunday is May 26
        pentecost = date_class(2024, 5, 19)
        trinity_sunday = date_class(2024, 5, 26)
        day_after_trinity = date_class(2024, 5, 27)

        pentecost_cal = get_calendar_date(pentecost)
        trinity_cal = get_calendar_date(trinity_sunday)
        after_trinity_cal = get_calendar_date(day_after_trinity)

        # Pentecost begins Season After Pentecost
        assert pentecost_cal.season.name == "Season After Pentecost"
        # Trinity Sunday itself
        assert "Trinity" in trinity_cal.primary.name
        # Day after Trinity is still Season After Pentecost
        assert after_trinity_cal.season.name == "Season After Pentecost"


@pytest.mark.django_db
class TestDateFormatting:
    """Tests for date formatting and display."""

    def test_formatted_date_string_generation(self):
        """Offices should generate properly formatted date strings."""
        test_date = date_class(2024, 1, 15)
        office = MorningPrayer(date=test_date)

        formatted = office.get_formatted_date_string()

        assert "Monday" in formatted  # Day of week
        assert "January" in formatted  # Month name
        assert "15" in formatted  # Day
        assert "2024" in formatted  # Year

    def test_various_date_formats(self):
        """Test date formatting for various dates."""
        dates_and_expected = [
            (date_class(2024, 12, 25), ["Wednesday", "December", "25", "2024"]),
            (date_class(2024, 7, 4), ["Thursday", "July", "4", "2024"]),
            (date_class(2024, 2, 29), ["Thursday", "February", "29", "2024"]),
        ]

        for test_date, expected_parts in dates_and_expected:
            office = EveningPrayer(date=test_date)
            formatted = office.get_formatted_date_string()

            for part in expected_parts:
                assert part in formatted


@pytest.mark.django_db
class TestOfficeReadingsAssignment:
    """Tests for office readings assignment across dates."""

    def test_readings_assigned_for_past_dates(self):
        """Office readings should be assigned for past dates."""
        past_date = date_class(2020, 6, 15)
        office = MorningPrayer(date=past_date)

        assert office.office_readings is not None
        assert office.office_readings.month == past_date.month
        assert office.office_readings.day == past_date.day

    def test_readings_assigned_for_future_dates(self):
        """Office readings should be assigned for future dates."""
        future_date = date_class(2050, 9, 20)
        office = EveningPrayer(date=future_date)

        assert office.office_readings is not None
        assert office.office_readings.month == future_date.month
        assert office.office_readings.day == future_date.day

    def test_readings_consistent_across_office_types(self):
        """All office types should use same readings for same date."""
        test_date = date_class(2024, 3, 15)

        mp = MorningPrayer(date=test_date)
        ep = EveningPrayer(date=test_date)
        midday = MiddayPrayer(date=test_date)
        compline = Compline(date=test_date)

        # All should reference same StandardOfficeDay record
        assert mp.office_readings.month == test_date.month
        assert ep.office_readings.month == test_date.month
        assert midday.office_readings.month == test_date.month
        assert compline.office_readings.month == test_date.month
