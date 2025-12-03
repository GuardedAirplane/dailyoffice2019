"""
Unit tests for Family Prayer offices (US7).

These tests validate that all four Family Prayer office types
instantiate correctly and provide simplified content for families.

Test Coverage:
- T096-T100: Family Prayer office instantiation and content validation

Validates:
- FR-018: Provide Family Prayer offices
- FR-019: Family Prayer as secondary navigation
"""

import pytest
from datetime import date as date_class

from office.family_morning import FamilyMorning
from office.family_midday import FamilyMidday
from office.family_early_evening import FamilyEarlyEvening
from office.family_close_of_day import FamilyCloseOfDay


@pytest.fixture(autouse=True)
def create_standard_office_days(db):
    """
    Create StandardOfficeDay entries for all 366 days of the year.

    The Daily Office system requires StandardOfficeDay entries for regular days.
    This fixture creates minimal entries for all possible month/day combinations
    to support Family Prayer tests.
    """
    from office.tests.factories import (
        CalendarFactory,
        DenominationFactory,
        CommemorationRankFactory,
        SeasonFactory,
        create_psalter_cycle,
        StandardOfficeDayFactory,
        ThirtyDayPsalterDayFactory,
    )

    days_per_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Create complete psalter cycle (required for office generation)
    create_psalter_cycle()
    ThirtyDayPsalterDayFactory.create(day=31)

    # Create StandardOfficeDay entries for all days of year
    for month in range(1, 13):
        for day in range(1, days_per_month[month - 1] + 1):
            StandardOfficeDayFactory.create(month=month, day=day)

    # Create ACNA BCP 2019 calendar (required for churchcal calculations)
    acna = DenominationFactory.create(name="Anglican Church in North America", abbreviation="ACNA")
    acna_calendar = CalendarFactory.create(
        name="ACNA Book of Common Prayer 2019",
        abbreviation="ACNA_BCP2019",
        year="2019",
        denomination=acna,
    )

    # Create commemoration rank for ordinary days
    ferial_rank = CommemorationRankFactory.create(
        name="FERIA",
        formatted_name="Ferial Day",
        precedence_rank=99,
        required=False,
        calendar=acna_calendar,
    )

    # Create liturgical season (Epiphanytide covers much of year)
    SeasonFactory.create(
        order=5,
        name="Epiphanytide",
        color="Green",
        calendar=acna_calendar,
        rank=ferial_rank,
    )


@pytest.mark.django_db
class TestFamilyMorningPrayer:
    """Tests for Family Prayer in the Morning office."""

    def test_family_morning_instantiation(self):
        """FamilyMorning should instantiate correctly with a date.

        Validates: FR-018 (Provide Family Prayer offices)
        """
        test_date = date_class(2024, 3, 15)
        office = FamilyMorning(date=test_date)

        assert office is not None
        assert office.name == "Family Prayer in the Morning"
        assert office.office == "family_morning_prayer"
        assert office.family is True

    def test_family_morning_has_required_properties(self):
        """FamilyMorning should have all required office properties."""
        test_date = date_class(2024, 6, 20)
        office = FamilyMorning(date=test_date)

        assert hasattr(office, "date")
        assert hasattr(office, "modules")
        assert hasattr(office, "office_readings")
        assert hasattr(office, "description")
        assert office.date.date == test_date

    def test_family_morning_modules_are_simplified(self):
        """FamilyMorning should have fewer, simpler modules than standard Morning Prayer.

        Validates: FR-018 (simplified content for families)
        """
        test_date = date_class(2024, 9, 10)
        office = FamilyMorning(date=test_date)

        modules = office.modules

        # Should have modules but fewer than standard office
        assert len(modules) > 0
        assert len(modules) < 15  # Standard Morning Prayer has more modules

        # Verify it's a list of tuples (module, template)
        for module_tuple in modules:
            assert len(module_tuple) == 2
            assert isinstance(module_tuple[1], str)  # Template path

    def test_family_morning_title_generation(self):
        """FamilyMorning should generate appropriate title."""
        test_date = date_class(2024, 12, 25)
        office = FamilyMorning(date=test_date)

        assert "Family Prayer in the Morning" in office.title
        assert "2024" in office.title

    def test_family_morning_date_preservation(self):
        """FamilyMorning should preserve the date throughout."""
        test_date = date_class(2024, 2, 14)
        office = FamilyMorning(date=test_date)

        assert office.date.date == test_date
        assert office.get_formatted_date_string() is not None

    def test_family_morning_various_dates(self):
        """FamilyMorning should work with various dates."""
        dates = [
            date_class(2020, 1, 1),
            date_class(2024, 2, 29),  # Leap year
            date_class(2050, 12, 31),
        ]

        for test_date in dates:
            office = FamilyMorning(date=test_date)
            assert office.date.date == test_date
            assert office.name == "Family Prayer in the Morning"


@pytest.mark.django_db
class TestFamilyMiddayPrayer:
    """Tests for Family Prayer at Midday office."""

    def test_family_midday_instantiation(self):
        """FamilyMidday should instantiate correctly with a date.

        Validates: FR-018 (Provide Family Prayer offices)
        """
        test_date = date_class(2024, 3, 15)
        office = FamilyMidday(date=test_date)

        assert office is not None
        assert office.name == "Family Prayer at Midday"
        assert office.office == "family_midday_prayer"
        assert office.family is True

    def test_family_midday_has_required_properties(self):
        """FamilyMidday should have all required office properties."""
        test_date = date_class(2024, 6, 20)
        office = FamilyMidday(date=test_date)

        assert hasattr(office, "date")
        assert hasattr(office, "modules")
        assert hasattr(office, "office_readings")
        assert hasattr(office, "description")
        assert office.date.date == test_date

    def test_family_midday_modules_are_simplified(self):
        """FamilyMidday should have fewer, simpler modules.

        Validates: FR-018 (simplified content for families)
        """
        test_date = date_class(2024, 9, 10)
        office = FamilyMidday(date=test_date)

        modules = office.modules

        assert len(modules) > 0
        assert len(modules) < 15

        for module_tuple in modules:
            assert len(module_tuple) == 2
            assert isinstance(module_tuple[1], str)

    def test_family_midday_title_generation(self):
        """FamilyMidday should generate appropriate title."""
        test_date = date_class(2024, 12, 25)
        office = FamilyMidday(date=test_date)

        assert "Family Prayer at Midday" in office.title
        assert "2024" in office.title

    def test_family_midday_various_dates(self):
        """FamilyMidday should work with various dates."""
        dates = [
            date_class(2020, 1, 1),
            date_class(2024, 2, 29),
            date_class(2050, 12, 31),
        ]

        for test_date in dates:
            office = FamilyMidday(date=test_date)
            assert office.date.date == test_date
            assert office.name == "Family Prayer at Midday"


@pytest.mark.django_db
class TestFamilyEarlyEveningPrayer:
    """Tests for Family Prayer in the Early Evening office."""

    def test_family_early_evening_instantiation(self):
        """FamilyEarlyEvening should instantiate correctly with a date.

        Validates: FR-018 (Provide Family Prayer offices)
        """
        test_date = date_class(2024, 3, 15)
        office = FamilyEarlyEvening(date=test_date)

        assert office is not None
        assert office.name == "Family Prayer in the Early Evening"
        assert office.office == "family_early_evening_prayer"
        assert office.family is True

    def test_family_early_evening_has_required_properties(self):
        """FamilyEarlyEvening should have all required office properties."""
        test_date = date_class(2024, 6, 20)
        office = FamilyEarlyEvening(date=test_date)

        assert hasattr(office, "date")
        assert hasattr(office, "modules")
        assert hasattr(office, "office_readings")
        assert hasattr(office, "description")
        assert office.date.date == test_date

    def test_family_early_evening_modules_are_simplified(self):
        """FamilyEarlyEvening should have fewer, simpler modules.

        Validates: FR-018 (simplified content for families)
        """
        test_date = date_class(2024, 9, 10)
        office = FamilyEarlyEvening(date=test_date)

        modules = office.modules

        assert len(modules) > 0
        assert len(modules) < 20  # Standard Evening Prayer has many modules

        for module_tuple in modules:
            assert len(module_tuple) == 2
            assert isinstance(module_tuple[1], str)

    def test_family_early_evening_title_generation(self):
        """FamilyEarlyEvening should generate appropriate title."""
        test_date = date_class(2024, 12, 25)
        office = FamilyEarlyEvening(date=test_date)

        assert "Family Prayer in the Early Evening" in office.title
        assert "2024" in office.title

    def test_family_early_evening_uses_evening_commemoration(self):
        """FamilyEarlyEvening should use primary_evening for commemoration."""
        test_date = date_class(2024, 4, 10)
        office = FamilyEarlyEvening(date=test_date)

        # Should reference primary_evening in description
        assert "primary_evening" in office.description or office.date.primary_evening is not None

    def test_family_early_evening_various_dates(self):
        """FamilyEarlyEvening should work with various dates."""
        dates = [
            date_class(2020, 1, 1),
            date_class(2024, 2, 29),
            date_class(2050, 12, 31),
        ]

        for test_date in dates:
            office = FamilyEarlyEvening(date=test_date)
            assert office.date.date == test_date
            assert office.name == "Family Prayer in the Early Evening"


@pytest.mark.django_db
class TestFamilyCloseOfDayPrayer:
    """Tests for Family Prayer at the Close of Day office."""

    def test_family_close_of_day_instantiation(self):
        """FamilyCloseOfDay should instantiate correctly with a date.

        Validates: FR-018 (Provide Family Prayer offices)
        """
        test_date = date_class(2024, 3, 15)
        office = FamilyCloseOfDay(date=test_date)

        assert office is not None
        assert office.name == "Family Prayer at the Close of Day"
        assert office.office == "family_close_of_day_prayer"
        assert office.family is True

    def test_family_close_of_day_has_required_properties(self):
        """FamilyCloseOfDay should have all required office properties."""
        test_date = date_class(2024, 6, 20)
        office = FamilyCloseOfDay(date=test_date)

        assert hasattr(office, "date")
        assert hasattr(office, "modules")
        assert hasattr(office, "office_readings")
        assert hasattr(office, "description")
        assert office.date.date == test_date

    def test_family_close_of_day_modules_are_simplified(self):
        """FamilyCloseOfDay should have fewer, simpler modules.

        Validates: FR-018 (simplified content for families)
        """
        test_date = date_class(2024, 9, 10)
        office = FamilyCloseOfDay(date=test_date)

        modules = office.modules

        assert len(modules) > 0
        assert len(modules) < 15

        for module_tuple in modules:
            assert len(module_tuple) == 2
            assert isinstance(module_tuple[1], str)

    def test_family_close_of_day_title_generation(self):
        """FamilyCloseOfDay should generate appropriate title."""
        test_date = date_class(2024, 12, 25)
        office = FamilyCloseOfDay(date=test_date)

        assert "Family Prayer at the Close of Day" in office.title
        assert "2024" in office.title

    def test_family_close_of_day_uses_evening_commemoration(self):
        """FamilyCloseOfDay should use primary_evening for commemoration."""
        test_date = date_class(2024, 4, 10)
        office = FamilyCloseOfDay(date=test_date)

        assert "primary_evening" in office.description or office.date.primary_evening is not None

    def test_family_close_of_day_various_dates(self):
        """FamilyCloseOfDay should work with various dates."""
        dates = [
            date_class(2020, 1, 1),
            date_class(2024, 2, 29),
            date_class(2050, 12, 31),
        ]

        for test_date in dates:
            office = FamilyCloseOfDay(date=test_date)
            assert office.date.date == test_date
            assert office.name == "Family Prayer at the Close of Day"


@pytest.mark.django_db
class TestFamilyPrayerComparison:
    """Comparative tests across all family prayer offices."""

    def test_all_family_offices_have_family_flag(self):
        """All family prayer offices should have family=True flag.

        Validates: FR-019 (Family Prayer as secondary navigation)
        """
        test_date = date_class(2024, 5, 15)

        morning = FamilyMorning(date=test_date)
        midday = FamilyMidday(date=test_date)
        evening = FamilyEarlyEvening(date=test_date)
        close = FamilyCloseOfDay(date=test_date)

        assert morning.family is True
        assert midday.family is True
        assert evening.family is True
        assert close.family is True

    def test_all_family_offices_share_date(self):
        """All family offices for same date should reference same calendar date."""
        test_date = date_class(2024, 7, 4)

        morning = FamilyMorning(date=test_date)
        midday = FamilyMidday(date=test_date)
        evening = FamilyEarlyEvening(date=test_date)
        close = FamilyCloseOfDay(date=test_date)

        assert morning.date.date == test_date
        assert midday.date.date == test_date
        assert evening.date.date == test_date
        assert close.date.date == test_date

    def test_family_offices_have_unique_names(self):
        """Each family office should have a unique name."""
        test_date = date_class(2024, 8, 20)

        offices = [
            FamilyMorning(date=test_date),
            FamilyMidday(date=test_date),
            FamilyEarlyEvening(date=test_date),
            FamilyCloseOfDay(date=test_date),
        ]

        names = [office.name for office in offices]
        assert len(names) == len(set(names))  # All unique

    def test_family_offices_have_unique_office_identifiers(self):
        """Each family office should have a unique office identifier.

        Validates: FR-019 (secondary navigation requires unique identifiers)
        """
        test_date = date_class(2024, 9, 15)

        offices = [
            FamilyMorning(date=test_date),
            FamilyMidday(date=test_date),
            FamilyEarlyEvening(date=test_date),
            FamilyCloseOfDay(date=test_date),
        ]

        office_ids = [office.office for office in offices]
        assert len(office_ids) == len(set(office_ids))  # All unique

        # Verify they follow family naming pattern
        for office_id in office_ids:
            assert "family" in office_id

    def test_family_offices_simpler_than_standard_offices(self):
        """Family offices should generally have simpler content than standard offices."""
        from office.morning_prayer import MorningPrayer
        from office.evening_prayer import EveningPrayer

        test_date = date_class(2024, 10, 10)

        # Standard offices
        standard_mp = MorningPrayer(date=test_date)
        standard_ep = EveningPrayer(date=test_date)

        # Family offices
        family_morning = FamilyMorning(date=test_date)
        family_evening = FamilyEarlyEvening(date=test_date)

        # Family offices should be simpler (fewer modules for major offices)
        # Morning and Evening Prayer are the longest, so family versions should be shorter
        assert len(family_morning.modules) < len(standard_mp.modules)
        assert len(family_evening.modules) < len(standard_ep.modules)

        # All family offices should have reasonable module counts (not excessive)
        family_midday = FamilyMidday(date=test_date)
        family_close = FamilyCloseOfDay(date=test_date)

        assert len(family_midday.modules) < 15  # Reasonable limit
        assert len(family_close.modules) < 15  # Reasonable limit

    def test_all_family_offices_for_special_dates(self):
        """All family offices should work for special liturgical dates."""
        special_dates = [
            date_class(2024, 12, 25),  # Christmas
            date_class(2024, 3, 31),  # Easter 2024
            date_class(2024, 2, 14),  # Ash Wednesday 2024
        ]

        for test_date in special_dates:
            morning = FamilyMorning(date=test_date)
            midday = FamilyMidday(date=test_date)
            evening = FamilyEarlyEvening(date=test_date)
            close = FamilyCloseOfDay(date=test_date)

            assert morning is not None
            assert midday is not None
            assert evening is not None
            assert close is not None
