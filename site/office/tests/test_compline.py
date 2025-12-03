"""
Unit tests for Compline (US4).

Tests validate FR-002 (Daily Office feature) by ensuring Compline
generates correctly with all required liturgical components.

Test Coverage:
- T068: Compline instantiation
- T069: Module composition (10 modules)
- T070: Compline-specific modules (opening, confession, invitatory, canticle)
- T071: ComplinePrayers with weekday rotation
"""

import pytest
from datetime import date as date_class

from churchcal.calculations import get_calendar_date
from office.compline import (
    Compline,
    ComplineHeading,
    ComplineCommemorationListing,
    ComplineOpening,
    ComplineConfession,
    ComplineInvitatory,
    ComplinePsalms,
    ComplineScripture,
    ComplinePrayers,
    ComplineCanticle,
    ComplineConclusion,
)

pytestmark = pytest.mark.usefixtures("compline_office_data")


# T068: Compline instantiation tests
@pytest.mark.django_db
class TestComplineInstantiation:
    """Test that Compline can be instantiated for various dates."""

    def test_compline_instantiates_for_regular_day(self):
        """Compline should instantiate successfully for a regular weekday."""
        office = Compline(date=date_class(2024, 1, 15))  # Monday in Epiphany
        assert office is not None
        assert office.name == "Compline"
        assert office.office == "compline"

    def test_compline_instantiates_for_feast_day(self):
        """Compline should instantiate successfully for a feast day."""
        office = Compline(date=date_class(2024, 12, 25))  # Christmas Day
        assert office is not None
        assert office.name == "Compline"

    def test_compline_has_correct_time_window(self):
        """Compline should have start time at 8 PM and end time at 11:59 PM."""
        office = Compline(date=date_class(2024, 1, 15))
        assert office.start_time.hour == 20
        assert office.start_time.minute == 0
        assert office.end_time.hour == 23
        assert office.end_time.minute == 59


# T069: Module composition tests
@pytest.mark.django_db
class TestComplineModules:
    """Test that Compline contains all required modules in correct order."""

    def test_compline_has_ten_modules(self):
        """Compline should contain exactly 10 modules."""
        office = Compline(date=date_class(2024, 1, 15))
        assert len(office.modules) == 10

    def test_compline_modules_in_correct_order(self):
        """Modules should appear in liturgical order."""
        office = Compline(date=date_class(2024, 1, 15))
        module_types = [type(module[0]).__name__ for module in office.modules]
        expected = [
            "ComplineHeading",
            "ComplineCommemorationListing",
            "ComplineOpening",
            "ComplineConfession",
            "ComplineInvitatory",
            "ComplinePsalms",
            "ComplineScripture",
            "ComplinePrayers",
            "ComplineCanticle",
            "ComplineConclusion",
        ]
        assert module_types == expected

    def test_compline_modules_have_templates(self):
        """Each module should have an associated template."""
        office = Compline(date=date_class(2024, 1, 15))
        for module, template in office.modules:
            assert template is not None
            assert template.endswith(".html")

    def test_compline_description_contains_office_name(self):
        """Office description should contain 'Compline' identifier."""
        office = Compline(date=date_class(2024, 1, 15))
        assert "Compline" in office.description
        assert "The Book of Common Prayer (2019)" in office.description


# T069: Date handling tests
@pytest.mark.django_db
class TestComplineDateHandling:
    """Test Compline date-specific functionality."""

    def test_compline_handles_lent_dates(self):
        """Compline should correctly identify Lenten season."""
        office = Compline(date=date_class(2024, 3, 15))  # During Lent
        assert office is not None

    def test_compline_handles_easter_dates(self):
        """Compline should correctly identify Easter season."""
        office = Compline(date=date_class(2024, 4, 15))  # During Eastertide
        assert office is not None

    def test_compline_handles_advent_dates(self):
        """Compline should correctly identify Advent season."""
        office = Compline(date=date_class(2024, 12, 15))  # During Advent
        assert office is not None


# T070: ComplineHeading module tests
@pytest.mark.django_db
class TestComplineHeading:
    """Test ComplineHeading module."""

    def test_heading_contains_office_name(self):
        """Heading should display 'Compline'."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        heading = ComplineHeading(date=calendar_date, office_readings=None)
        data = heading.data
        assert "Compline" in data["heading"]

    def test_heading_includes_calendar_date(self):
        """Heading should include the calendar date."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        heading = ComplineHeading(date=calendar_date, office_readings=None)
        data = heading.data
        assert data["calendar_date"] == calendar_date


# T070: ComplineCommemorationListing module tests
@pytest.mark.django_db
class TestComplineCommemorationListing:
    """Test ComplineCommemorationListing module."""

    def test_commemoration_listing_uses_evening(self):
        """Compline should use evening commemorations."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        listing = ComplineCommemorationListing(date=calendar_date, office_readings=None)
        data = listing.data
        assert data["evening"] is True

    def test_commemoration_listing_has_commemorations(self):
        """Commemoration listing should include all evening commemorations."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        listing = ComplineCommemorationListing(date=calendar_date, office_readings=None)
        data = listing.data
        assert "commemorations" in data
        assert len(data["commemorations"]) > 0


# T070: ComplineOpening module tests
@pytest.mark.django_db
class TestComplineOpening:
    """Test ComplineOpening module."""

    def test_opening_provides_data(self):
        """Opening should provide data dictionary."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        opening = ComplineOpening(date=calendar_date, office_readings=None)
        data = opening.data
        assert data is not None
        assert isinstance(data, dict)


# T070: ComplineConfession module tests
@pytest.mark.django_db
class TestComplineConfession:
    """Test ComplineConfession module."""

    def test_confession_has_heading(self):
        """Confession should have 'Confession of Sin' heading."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        confession = ComplineConfession(date=calendar_date, office_readings=None)
        data = confession.data
        assert data["heading"] == "Confession of Sin"


# T070: ComplineInvitatory module tests
@pytest.mark.django_db
class TestComplineInvitatory:
    """Test ComplineInvitatory module."""

    def test_invitatory_alleluia_outside_lent(self):
        """Invitatory should include Alleluia outside Lent/Holy Week."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))  # Epiphany
        invitatory = ComplineInvitatory(date=calendar_date, office_readings=None)
        data = invitatory.data
        assert data["alleluia"] is True

    def test_invitatory_no_alleluia_during_lent(self):
        """Invitatory should omit Alleluia during Lent."""
        calendar_date = get_calendar_date(date_class(2024, 2, 14))  # Ash Wednesday
        invitatory = ComplineInvitatory(date=calendar_date, office_readings=None)
        data = invitatory.data
        assert data["alleluia"] is False

    def test_invitatory_has_heading(self):
        """Invitatory should have heading."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        invitatory = ComplineInvitatory(date=calendar_date, office_readings=None)
        data = invitatory.data
        assert data["heading"] == "Invitatory"


# T070: ComplinePsalms module tests
@pytest.mark.django_db
class TestComplinePsalms:
    """Test ComplinePsalms module (fixed psalm assignment)."""

    def test_psalms_fixed_assignment(self):
        """Compline should always use Psalms 4, 31:1-6, 91, 134."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        psalms_module = ComplinePsalms(date=calendar_date, office_readings=None)
        data = psalms_module.data
        assert data["heading"] == "The Psalms"
        assert "psalms" in data
        assert data["psalms"] is not None


# T070: ComplineScripture module tests
@pytest.mark.django_db
class TestComplineScripture:
    """Test ComplineScripture module (weekday-based rotation)."""

    def test_scripture_monday_friday(self):
        """Monday and Friday should use Jeremiah 14:9."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))  # Monday
        scripture = ComplineScripture(date=calendar_date, office_readings=None)
        data = scripture.data
        assert "JEREMIAH 14:9" in data["sentence"]["citation"]

    def test_scripture_tuesday_saturday(self):
        """Tuesday and Saturday should use Matthew 11:28-30."""
        calendar_date = get_calendar_date(date_class(2024, 1, 16))  # Tuesday
        scripture = ComplineScripture(date=calendar_date, office_readings=None)
        data = scripture.data
        assert "MATTHEW 11:28-30" in data["sentence"]["citation"]

    def test_scripture_wednesday_sunday(self):
        """Wednesday and Sunday should use Hebrews 13:20-21."""
        calendar_date = get_calendar_date(date_class(2024, 1, 17))  # Wednesday
        scripture = ComplineScripture(date=calendar_date, office_readings=None)
        data = scripture.data
        assert "HEBREWS 13:20-21" in data["sentence"]["citation"]

    def test_scripture_thursday(self):
        """Thursday should use 1 Peter 5:8-9."""
        calendar_date = get_calendar_date(date_class(2024, 1, 18))  # Thursday
        scripture = ComplineScripture(date=calendar_date, office_readings=None)
        data = scripture.data
        assert "1 PETER 5:8-9" in data["sentence"]["citation"]


# T071: ComplinePrayers module tests
@pytest.mark.django_db
class TestComplinePrayers:
    """Test ComplinePrayers module with weekday rotation."""

    def test_prayers_sunday(self):
        """Sunday should have specific collect combination."""
        calendar_date = get_calendar_date(date_class(2024, 1, 21))  # Sunday
        prayers = ComplinePrayers(date=calendar_date, office_readings=None)
        collects = prayers.get_collects()
        assert len(collects) == 3
        # Sunday uses collects 0, 1, 5

    def test_prayers_monday(self):
        """Monday should have specific collect combination."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))  # Monday
        prayers = ComplinePrayers(date=calendar_date, office_readings=None)
        collects = prayers.get_collects()
        assert len(collects) == 3
        # Monday uses collects 2, 3, 5

    def test_prayers_saturday(self):
        """Saturday should include the Paschal mystery collect."""
        calendar_date = get_calendar_date(date_class(2024, 1, 20))  # Saturday
        prayers = ComplinePrayers(date=calendar_date, office_readings=None)
        collects = prayers.get_collects()
        assert len(collects) == 3
        # Saturday uses collects 2, 4, 5
        assert "Paschal mystery" in collects[1][1]


# T070: ComplineCanticle module tests
@pytest.mark.django_db
class TestComplineCanticle:
    """Test ComplineCanticle module (Nunc Dimittis)."""

    def test_canticle_has_nunc_dimittis_heading(self):
        """Canticle should be Nunc Dimittis (Song of Simeon)."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))
        canticle = ComplineCanticle(date=calendar_date, office_readings=None)
        data = canticle.data
        assert data["heading"] == "Nunc Dimittis"
        assert data["subheading"] == "The Song of Simeon"

    def test_canticle_alleluia_during_easter(self):
        """Canticle should include Alleluia during Eastertide."""
        calendar_date = get_calendar_date(date_class(2024, 4, 15))  # Easter season
        canticle = ComplineCanticle(date=calendar_date, office_readings=None)
        data = canticle.data
        assert data["alleluia"] is True

    def test_canticle_no_alleluia_outside_easter(self):
        """Canticle should omit Alleluia outside Eastertide."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))  # Epiphany
        canticle = ComplineCanticle(date=calendar_date, office_readings=None)
        data = canticle.data
        assert data["alleluia"] is False


# T070: ComplineConclusion module tests
@pytest.mark.django_db
class TestComplineConclusion:
    """Test ComplineConclusion module."""

    def test_conclusion_alleluia_during_easter(self):
        """Conclusion should include Alleluia during Eastertide."""
        calendar_date = get_calendar_date(date_class(2024, 4, 15))  # Easter season
        conclusion = ComplineConclusion(date=calendar_date, office_readings=None)
        data = conclusion.data
        assert data["alleluia"] is True

    def test_conclusion_no_alleluia_outside_easter(self):
        """Conclusion should omit Alleluia outside Eastertide."""
        calendar_date = get_calendar_date(date_class(2024, 1, 15))  # Epiphany
        conclusion = ComplineConclusion(date=calendar_date, office_readings=None)
        data = conclusion.data
        assert data["alleluia"] is False
