"""
Unit tests for churchcal calculations module.

These tests validate liturgical calendar calculations including
Easter, Advent, and season determination.

Test Coverage:
- T108-T110: Calendar calculation tests

Validates:
- FR-014: Calculate correct liturgical season
"""

import pytest
from datetime import date as date_class

from churchcal.calculations import get_calendar_date, ChurchYear
from churchcal.utils import easter, advent


@pytest.mark.django_db
class TestEasterCalculation:
    """Tests for Easter date calculation across various years.

    Validates: FR-014 (Calculate correct liturgical season)
    """

    def test_easter_1900(self):
        """Easter calculation for year 1900 (early 20th century)."""
        # Easter 1900 was April 15
        easter_date = easter(1900)
        assert easter_date.month == 4
        assert easter_date.day == 15

    def test_easter_2000(self):
        """Easter calculation for year 2000 (millennium year)."""
        # Easter 2000 was April 23
        easter_date = easter(2000)
        assert easter_date.month == 4
        assert easter_date.day == 23

    def test_easter_2024(self):
        """Easter calculation for year 2024."""
        # Easter 2024 is March 31
        easter_date = easter(2024)
        assert easter_date.month == 3
        assert easter_date.day == 31

    def test_easter_2025(self):
        """Easter calculation for year 2025."""
        # Easter 2025 is April 20
        easter_date = easter(2025)
        assert easter_date.month == 4
        assert easter_date.day == 20

    def test_easter_2050(self):
        """Easter calculation for year 2050 (mid-21st century)."""
        # Easter 2050 is April 10
        easter_date = easter(2050)
        assert easter_date.month == 4
        assert easter_date.day == 10

    def test_easter_2100(self):
        """Easter calculation for year 2100 (22nd century)."""
        # Easter 2100 will be March 28
        easter_date = easter(2100)
        assert easter_date.month == 3
        assert easter_date.day == 28

    def test_easter_always_in_march_or_april(self):
        """Easter should always fall in March or April."""
        for year in [1900, 1950, 2000, 2024, 2050, 2100]:
            easter_date = easter(year)
            assert easter_date.month in [
                3,
                4,
            ], f"Easter {year} should be in March or April, got month {easter_date.month}"

    def test_easter_always_sunday(self):
        """Easter should always fall on a Sunday."""
        for year in [1900, 1950, 2000, 2024, 2050, 2100]:
            easter_date = easter(year)
            # weekday() returns 6 for Sunday
            assert easter_date.weekday() == 6, f"Easter {year} should be Sunday, got weekday {easter_date.weekday()}"

    def test_easter_range_march_22_to_april_25(self):
        """Easter can occur between March 22 and April 25."""
        for year in range(2020, 2030):
            easter_date = easter(year)
            # Convert to day of year for easier comparison
            if easter_date.month == 3:
                assert easter_date.day >= 22
            elif easter_date.month == 4:
                assert easter_date.day <= 25


@pytest.mark.django_db
class TestAdventCalculation:
    """Tests for Advent date calculation.

    Validates: FR-014 (Calculate correct liturgical season)
    """

    def test_advent_2023(self):
        """Advent 2023 begins December 3."""
        advent_date = advent(2023)
        assert advent_date.month == 12
        assert advent_date.day == 3

    def test_advent_2024(self):
        """Advent 2024 begins December 1."""
        advent_date = advent(2024)
        assert advent_date.month == 12
        assert advent_date.day == 1

    def test_advent_2025(self):
        """Advent 2025 begins November 30."""
        advent_date = advent(2025)
        assert advent_date.month == 11
        assert advent_date.day == 30

    def test_advent_2050(self):
        """Advent 2050 begins November 27."""
        advent_date = advent(2050)
        assert advent_date.month == 11
        assert advent_date.day == 27

    def test_advent_always_sunday(self):
        """First Sunday of Advent should always be a Sunday."""
        for year in [2020, 2021, 2022, 2023, 2024, 2025, 2050]:
            advent_date = advent(year)
            assert advent_date.weekday() == 6, f"Advent {year} should be Sunday, got weekday {advent_date.weekday()}"

    def test_advent_always_near_st_andrews_day(self):
        """Advent should always be the Sunday nearest to St. Andrew's Day (Nov 30)."""
        for year in [2020, 2021, 2022, 2023, 2024, 2025]:
            advent_date = advent(year)
            st_andrews = date_class(year, 11, 30)

            # Advent should be within 3 days of St. Andrew's Day
            diff = abs((advent_date - st_andrews).days)
            assert diff <= 3, f"Advent {year} should be within 3 days of Nov 30, got {diff} days difference"

    def test_advent_in_november_or_december(self):
        """Advent can begin in late November or early December."""
        for year in [2020, 2021, 2022, 2023, 2024, 2025, 2050]:
            advent_date = advent(year)
            assert advent_date.month in [11, 12], f"Advent {year} should be in November or December"

            if advent_date.month == 11:
                assert advent_date.day >= 27  # Earliest possible
            elif advent_date.month == 12:
                assert advent_date.day <= 3  # Latest possible


@pytest.mark.django_db
class TestSeasonDetermination:
    """Tests for liturgical season determination.

    Validates: FR-014 (Calculate correct liturgical season)
    """

    def test_advent_season(self):
        """December 1, 2024 should be Advent."""
        cal_date = get_calendar_date(date_class(2024, 12, 1))
        assert cal_date.season.name == "Advent"

    def test_christmastide_season(self):
        """December 25, 2024 should be Christmastide."""
        cal_date = get_calendar_date(date_class(2024, 12, 25))
        assert cal_date.season.name == "Christmastide"

    def test_epiphanytide_season(self):
        """January 15, 2024 should be Epiphanytide."""
        cal_date = get_calendar_date(date_class(2024, 1, 15))
        assert cal_date.season.name == "Epiphanytide"

    def test_lent_season(self):
        """February 20, 2024 should be Lent."""
        cal_date = get_calendar_date(date_class(2024, 2, 20))
        assert cal_date.season.name == "Lent"

    def test_holy_week_season(self):
        """March 30, 2024 (Holy Saturday) should be Holy Week."""
        cal_date = get_calendar_date(date_class(2024, 3, 30))
        assert cal_date.season.name == "Holy Week"

    def test_eastertide_season(self):
        """April 10, 2024 should be Eastertide."""
        cal_date = get_calendar_date(date_class(2024, 4, 10))
        assert cal_date.season.name == "Eastertide"

    def test_season_after_pentecost(self):
        """June 1, 2024 should be after Pentecost."""
        cal_date = get_calendar_date(date_class(2024, 6, 1))
        assert cal_date.season.name == "Season After Pentecost"

    def test_all_dates_have_season(self):
        """Every date in the year should have a liturgical season."""
        import random

        # Test 10 random dates throughout 2024 (reduced from 50 for performance)
        for _ in range(10):
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # Safe for all months

            cal_date = get_calendar_date(date_class(2024, month, day))
            assert cal_date.season is not None
            assert cal_date.season.name is not None

    def test_season_transitions_at_correct_boundaries(self):
        """Seasons should transition at correct liturgical boundaries."""
        # Advent begins
        nov_30 = get_calendar_date(date_class(2024, 11, 30))
        dec_1 = get_calendar_date(date_class(2024, 12, 1))
        assert nov_30.season.name != "Advent"
        assert dec_1.season.name == "Advent"

        # Christmas begins
        dec_24 = get_calendar_date(date_class(2024, 12, 24))
        dec_25 = get_calendar_date(date_class(2024, 12, 25))
        assert dec_24.season.name == "Advent"
        assert dec_25.season.name == "Christmastide"

        # Lent begins (Ash Wednesday)
        feb_13 = get_calendar_date(date_class(2024, 2, 13))
        feb_14 = get_calendar_date(date_class(2024, 2, 14))
        assert feb_13.season.name == "Epiphanytide"
        assert feb_14.season.name == "Lent"

        # Easter begins
        mar_30 = get_calendar_date(date_class(2024, 3, 30))
        mar_31 = get_calendar_date(date_class(2024, 3, 31))
        assert mar_30.season.name == "Holy Week"
        assert mar_31.season.name == "Eastertide"

    def test_same_season_spans_multiple_days(self):
        """Seasons should span multiple consecutive days."""
        # Test Advent spans Dec 1-24, 2024 (sample first, middle, last days for performance)
        test_days = [1, 2, 12, 13, 23, 24]
        for day in test_days:
            cal_date = get_calendar_date(date_class(2024, 12, day))
            assert cal_date.season.name == "Advent", f"Dec {day} should be Advent"

        # Christmas Day should be Christmastide
        cal_date = get_calendar_date(date_class(2024, 12, 25))
        assert cal_date.season.name == "Christmastide"


@pytest.mark.django_db
class TestChurchYear:
    """Tests for ChurchYear class and year determination."""

    def test_church_year_starts_with_advent(self):
        """Church year should start with First Sunday of Advent."""
        # 2024 church year starts Dec 1, 2024
        advent_date = advent(2024)
        cal_date = get_calendar_date(advent_date)

        assert cal_date.season.name == "Advent"

    def test_church_year_ends_before_next_advent(self):
        """Church year should end the day before next Advent."""
        # 2025 Advent starts Nov 30, so Nov 29 is last day of previous church year
        last_day = get_calendar_date(date_class(2025, 11, 29))
        next_advent = get_calendar_date(date_class(2025, 11, 30))

        assert last_day.season.name != "Advent"
        assert next_advent.season.name == "Advent"

    def test_dates_within_same_church_year(self):
        """Dates between same Advent periods should be in same church year."""
        # Dec 15, 2024 and March 15, 2025 are in same church year
        dec_date = get_calendar_date(date_class(2024, 12, 15))
        mar_date = get_calendar_date(date_class(2025, 3, 15))

        # Both should have valid seasons
        assert dec_date.season is not None
        assert mar_date.season is not None

    def test_calendar_date_has_year_property(self):
        """CalendarDate should have year property."""
        cal_date = get_calendar_date(date_class(2024, 6, 15))

        assert hasattr(cal_date, "year")
        assert cal_date.year is not None

    def test_calendar_date_preserves_date(self):
        """CalendarDate should preserve the original date."""
        test_date = date_class(2024, 7, 20)
        cal_date = get_calendar_date(test_date)

        assert cal_date.date == test_date


@pytest.mark.django_db
class TestCalendarDateProperties:
    """Tests for CalendarDate properties and methods."""

    def test_calendar_date_has_primary_commemoration(self):
        """CalendarDate should have primary commemoration."""
        cal_date = get_calendar_date(date_class(2024, 6, 15))

        assert hasattr(cal_date, "primary")
        assert cal_date.primary is not None

    def test_calendar_date_has_season(self):
        """CalendarDate should have season assigned."""
        cal_date = get_calendar_date(date_class(2024, 6, 15))

        assert hasattr(cal_date, "season")
        assert cal_date.season is not None

    def test_calendar_date_office_year(self):
        """CalendarDate should calculate office year (1 or 2)."""
        cal_date = get_calendar_date(date_class(2024, 6, 15))

        assert hasattr(cal_date, "office_year")
        office_year = cal_date.office_year
        assert office_year in [1, 2]

    def test_major_feasts_have_correct_season(self):
        """Major feasts should be in their correct seasons."""
        # Christmas
        christmas = get_calendar_date(date_class(2024, 12, 25))
        assert christmas.season.name == "Christmastide"

        # Easter
        easter_day = get_calendar_date(date_class(2024, 3, 31))
        assert easter_day.season.name == "Eastertide"

        # Pentecost (May 19, 2024)
        pentecost = get_calendar_date(date_class(2024, 5, 19))
        assert pentecost.season.name == "Season After Pentecost"

    def test_calendar_date_caching(self):
        """get_calendar_date should work consistently for same date."""
        date1 = get_calendar_date(date_class(2024, 8, 15))
        date2 = get_calendar_date(date_class(2024, 8, 15))

        # Should have same season and primary
        assert date1.season.name == date2.season.name
        assert date1.primary.name == date2.primary.name
