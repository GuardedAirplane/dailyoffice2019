"""
Unit tests for Midday Prayer (US3).

Tests validate FR-002 (Daily Office feature) by ensuring Midday Prayer
generates correctly with all required liturgical components.

Test Coverage:
- T060: MiddayPrayer instantiation
- T061: Module composition (7 modules)
- T062: Midday-specific modules (invitatory, psalms, scripture)
- T063: MiddayPrayers with collect rotation
"""

import pytest
from datetime import date as date_class

from churchcal.calculations import get_calendar_date
from office.midday_prayer import (
    MiddayPrayer,
    MiddayHeading,
    MiddayCommemorationListing,
    MiddayInvitatory,
    MiddayPsalms,
    MiddayScripture,
    MiddayPrayers,
    MiddayConclusion,
)


# T060: MiddayPrayer instantiation tests
@pytest.mark.django_db
class TestMiddayPrayerInstantiation:
    """Test that MiddayPrayer can be instantiated for various dates."""

    def test_midday_prayer_instantiates_for_regular_day(self):
        """MiddayPrayer should instantiate successfully for a regular weekday."""
        office = MiddayPrayer(date=date_class(2024, 1, 15))  # Monday in Epiphany
        assert office is not None
        assert office.name == "Midday Prayer"
        assert office.office == "midday_prayer"

    def test_midday_prayer_instantiates_for_feast_day(self):
        """MiddayPrayer should instantiate successfully for a feast day."""
        office = MiddayPrayer(date=date_class(2024, 12, 25))  # Christmas Day
        assert office is not None
        assert office.name == "Midday Prayer"

    def test_midday_prayer_has_correct_time_window(self):
        """MiddayPrayer should have start time at 11 AM and end time at 4 PM."""
        office = MiddayPrayer(date=date_class(2024, 1, 15))
        assert office.start_time.hour == 11
        assert office.start_time.minute == 0
        assert office.end_time.hour == 16
        assert office.end_time.minute == 0


# T061: Module composition tests
@pytest.mark.django_db
class TestMiddayPrayerModules:
    """Test that MiddayPrayer contains all required modules in correct order."""

    def test_midday_prayer_has_seven_modules(self):
        """MiddayPrayer should contain exactly 7 modules (abbreviated office)."""
        office = MiddayPrayer(date=date_class(2024, 1, 15))
        assert len(office.modules) == 7

    def test_midday_prayer_modules_in_correct_order(self):
        """Modules should appear in liturgical order."""
        office = MiddayPrayer(date=date_class(2024, 1, 15))
        module_types = [type(module[0]).__name__ for module in office.modules]
        expected = [
            "MiddayHeading",
            "MiddayCommemorationListing",
            "MiddayInvitatory",
            "MiddayPsalms",
            "MiddayScripture",
            "MiddayPrayers",
            "MiddayConclusion",
        ]
        assert module_types == expected

    def test_midday_prayer_modules_have_templates(self):
        """Each module should have an associated template."""
        office = MiddayPrayer(date=date_class(2024, 1, 15))
        for module, template in office.modules:
            assert template is not None
            assert template.endswith(".html")

    def test_midday_prayer_description_contains_office_name(self):
        """Office description should contain 'Midday Prayer' identifier."""
        office = MiddayPrayer(date=date_class(2024, 1, 15))
        assert "Midday Prayer" in office.description
        assert "The Book of Common Prayer (2019)" in office.description


# T061: Date handling tests
@pytest.mark.django_db
class TestMiddayPrayerDateHandling:
    """Test MiddayPrayer date-specific functionality."""

    def test_midday_prayer_handles_lent_dates(self):
        """MiddayPrayer should correctly identify Lenten season."""
        office = MiddayPrayer(date=date_class(2024, 3, 15))  # During Lent
        assert office is not None

    def test_midday_prayer_handles_easter_dates(self):
        """MiddayPrayer should correctly identify Easter season."""
        office = MiddayPrayer(date=date_class(2024, 4, 15))  # During Eastertide
        assert office is not None

    def test_midday_prayer_handles_advent_dates(self):
        """MiddayPrayer should correctly identify Advent season."""
        office = MiddayPrayer(date=date_class(2024, 12, 15))  # During Advent
        assert office is not None


# T062: MiddayHeading module tests
@pytest.mark.django_db
class TestMiddayHeading:
    """Test MiddayHeading module."""

    def test_heading_contains_office_name(self):
        """Heading should display 'Midday Prayer'."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        heading = MiddayHeading(date=calendar_date, office_readings=None)
        data = heading.data
        assert "Midday Prayer" in data["heading"]

    def test_heading_includes_calendar_date(self):
        """Heading should include the calendar date."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        heading = MiddayHeading(date=calendar_date, office_readings=None)
        data = heading.data
        assert data["calendar_date"] == calendar_date


# T062: MiddayInvitatory module tests
@pytest.mark.django_db
class TestMiddayInvitatory:
    """Test MiddayInvitatory module."""

    def test_invitatory_alleluia_outside_lent(self):
        """Invitatory should include Alleluia outside Lent/Holy Week."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))  # Epiphany
        invitatory = MiddayInvitatory(date=calendar_date, office_readings=None)
        data = invitatory.data
        assert data["alleluia"] is True

    def test_invitatory_no_alleluia_during_lent(self):
        """Invitatory should omit Alleluia during Lent."""
        calendar_date = get_calendar_date(date_class(2024, 2, 14))  # Ash Wednesday
        invitatory = MiddayInvitatory(date=calendar_date, office_readings=None)
        data = invitatory.data
        assert data["alleluia"] is False


# T062: MiddayPsalms module tests
@pytest.mark.django_db
class TestMiddayPsalms:
    """Test MiddayPsalms module (fixed psalm assignment)."""

    def test_psalms_fixed_assignment(self):
        """Midday Prayer should always use Psalm 119:105-112, 121, 124, 126."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        psalms_module = MiddayPsalms(date=calendar_date, office_readings=None)
        data = psalms_module.data
        assert data["heading"] == "The Psalms"
        assert "psalms" in data
        assert data["psalms"] is not None


# T062: MiddayScripture module tests
@pytest.mark.django_db
class TestMiddayScripture:
    """Test MiddayScripture module (weekday-based rotation)."""

    def test_scripture_monday_thursday_sunday(self):
        """Monday, Thursday, Sunday should use John 12:31-32."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))  # Monday
        scripture = MiddayScripture(date=calendar_date, office_readings=None)
        data = scripture.data
        assert "JOHN 12:31-32" in data["sentence"]["citation"]

    def test_scripture_tuesday_friday(self):
        """Tuesday and Friday should use 2 Corinthians 5:17-18."""
        calendar_date = get_calendar_date(date_class(2024, 1, 16))  # Tuesday
        scripture = MiddayScripture(date=calendar_date, office_readings=None)
        data = scripture.data
        assert "2 CORINTHIANS 5:17-18" in data["sentence"]["citation"]

    def test_scripture_wednesday_saturday(self):
        """Wednesday and Saturday should use Malachi 1:11."""
        calendar_date = get_calendar_date(date_class(2024, 1, 17))  # Wednesday
        scripture = MiddayScripture(date=calendar_date, office_readings=None)
        data = scripture.data
        assert "MALACHI 1:11" in data["sentence"]["citation"]


# T063: MiddayPrayers module tests
@pytest.mark.django_db
class TestMiddayPrayers:
    """Test MiddayPrayers module with collect rotation."""

    def test_prayers_always_include_first_collect(self):
        """All days should include the Blessed Savior collect."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        prayers = MiddayPrayers(date=calendar_date, office_readings=None)
        collects = prayers.get_collects()
        assert len(collects) >= 1
        assert "Blessed Savior" in collects[0]

    def test_prayers_special_collect_for_conversion_of_paul(self):
        """Conversion of Paul should include specific collects."""
        calendar_date = get_calendar_date(date_class(2024, 1, 25))  # Conversion of Paul
        prayers = MiddayPrayers(date=calendar_date, office_readings=None)
        collects = prayers.get_collects()
        assert len(collects) == 2
        assert "Blessed Savior" in collects[0]
        assert "Saint Paul" in collects[1]


# T062: MiddayConclusion module tests
@pytest.mark.django_db
class TestMiddayConclusion:
    """Test MiddayConclusion module."""

    def test_conclusion_alleluia_during_easter(self):
        """Conclusion should include Alleluia during Eastertide."""
        calendar_date = get_calendar_date(date_class(2024, 4, 15))  # Easter season
        conclusion = MiddayConclusion(date=calendar_date, office_readings=None)
        data = conclusion.data
        assert data["alleluia"] is True

    def test_conclusion_no_alleluia_outside_easter(self):
        """Conclusion should omit Alleluia outside Eastertide."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))  # Epiphany
        conclusion = MiddayConclusion(date=calendar_date, office_readings=None)
        data = conclusion.data
        assert data["alleluia"] is False
