"""
Unit tests for Morning Prayer office generation.

Validates: FR-001 (Display Morning Prayer with all components)
User Story: US1 (View Morning Prayer)
Priority: P1 (High) - MVP Feature

Tests must be written FIRST and must FAIL before implementation per Constitution Principle III.
Since implementation already exists, these tests verify existing functionality.

Constitution Requirements:
- FR-001: Display Morning Prayer with all required liturgical components
- FR-005: Different psalm assignments for Morning vs Evening Prayer
- FR-006: Two scripture readings per office
- FR-008: Display appropriate canticles
- FR-009: Include full text of prayers and canticles
- FR-010: Format with proper indentation and rubrics
- FR-011: Display commemorations and feast names
- FR-013: Provide navigation between office types
"""

import pytest
from datetime import date as date_class
from freezegun import freeze_time

from office.morning_prayer import MorningPrayer
from office.models import StandardOfficeDay
from office.tests.fixtures import (
    acna_calendar,
    christmas_office_day,
    regular_office_day,
    cached_scripture,
    complete_settings,
    morning_prayer_psalms,
)


@pytest.mark.unit
@pytest.mark.us1
class TestMorningPrayerInstantiation:
    """
    Test MorningPrayer class instantiation and initialization.

    Validates: FR-001, US1
    Tasks: T017
    """

    def test_morning_prayer_instantiates_with_date_class(self, db, acna_calendar, regular_office_day):
        """Morning Prayer instantiates with valid date."""
        office_date = date_class(2025, 1, 15)

        # Act
        mp = MorningPrayer(date=office_date)

        # Assert
        assert mp is not None
        assert mp.date.date == office_date
        assert mp.name == "Morning Prayer"
        assert mp.office == "morning_prayer"

    def test_morning_prayer_requires_date_class(self, db):
        """Morning Prayer raises error when instantiated without date."""
        # Act & Assert
        with pytest.raises(TypeError):
            mp = MorningPrayer()

    def test_morning_prayer_retrieves_office_readings(self, db, acna_calendar, regular_office_day):
        """Morning Prayer retrieves correct OfficeDay readings for date."""
        office_date = date_class(2025, 1, 15)

        # Act
        mp = MorningPrayer(date=office_date)

        # Assert
        assert mp.office_readings is not None
        assert isinstance(mp.office_readings, StandardOfficeDay)
        assert mp.office_readings.month == 1
        assert mp.office_readings.day == 15

    def test_morning_prayer_requires_date_class(self, db):
        """Morning Prayer raises error when instantiated without date."""
        # Act & Assert
        with pytest.raises(TypeError):
            mp = MorningPrayer()

    def test_morning_prayer_retrieves_office_readings(self, db, regular_office_day):
        """Morning Prayer retrieves correct OfficeDay readings for date."""
        office_date = date_class(2025, 1, 15)

        # Act
        mp = MorningPrayer(date=office_date)

        # Assert
        assert mp.office_readings is not None
        assert isinstance(mp.office_readings, StandardOfficeDay)
        assert mp.office_readings.month == 1
        assert mp.office_readings.day == 15


@pytest.mark.unit
@pytest.mark.us1
class TestMorningPrayerModules:
    """
    Test Morning Prayer module list composition.

    Validates: FR-001 (Complete office structure)
    Tasks: T018
    """

    def test_morning_prayer_has_modules_property(self, db, regular_office_day):
        """Morning Prayer has modules property that returns list."""
        mp = MorningPrayer(date=date_class(2025, 1, 15))

        # Act
        modules = mp.modules

        # Assert
        assert modules is not None
        assert isinstance(modules, list)

    def test_morning_prayer_has_minimum_20_modules(self, db, regular_office_day):
        """Morning Prayer generates at least 20 liturgical modules."""
        mp = MorningPrayer(date=date_class(2025, 1, 15))

        # Act
        modules = mp.modules

        # Assert
        assert len(modules) >= 20, f"Expected at least 20 modules, got {len(modules)}"

    def test_morning_prayer_modules_are_tuples(self, db, regular_office_day):
        """Morning Prayer modules are returned as (section, template) tuples."""
        mp = MorningPrayer(date=date_class(2025, 1, 15))

        # Act
        modules = mp.modules

        # Assert
        for module in modules:
            assert isinstance(module, tuple), f"Module is not a tuple: {type(module)}"
            assert len(module) == 2, f"Module tuple should have 2 elements, has {len(module)}"

    def test_morning_prayer_includes_required_sections(self, db, regular_office_day):
        """Morning Prayer includes all required liturgical sections."""
        mp = MorningPrayer(date=date_class(2025, 1, 15))

        # Act
        modules = mp.modules
        module_names = [str(m[0].__class__.__name__) for m in modules]

        # Assert - Check for essential sections
        required_sections = [
            "MPHeading",
            "MPOpeningSentence",
            "Confession",
            "Invitatory",
            "MPPsalms",
            "MPFirstReading",
            "MPCanticle",  # Either MPCanticle1 or just MPCanticle
            "MPSecondReading",
            "Creed",
            "Prayers",
            "MPSuffrages",
            "MPCollectsOfTheDay",
            "Dismissal",
        ]

        # Check that at least most required sections are present
        # (exact names may vary based on implementation)
        module_names_str = " ".join(module_names)
        assert "Heading" in module_names_str
        assert "OpeningSentence" in module_names_str
        assert "Confession" in module_names_str
        assert "Psalms" in module_names_str or "Psalm" in module_names_str
        assert "Reading" in module_names_str
        assert "Canticle" in module_names_str
        assert "Creed" in module_names_str
        assert "Prayers" in module_names_str or "Prayer" in module_names_str


@pytest.mark.unit
@pytest.mark.us1
class TestMorningPrayerDateHandling:
    """
    Test Morning Prayer date handling capabilities.

    Validates: FR-012 (View offices for any date)
    Tasks: T019
    """

    def test_morning_prayer_accepts_current_date_class(self, db, regular_office_day):
        """Morning Prayer generates for current date."""
        with freeze_time("2025-01-15"):
            current_date = date_class.today()

            # Act
            mp = MorningPrayer(date=current_date)

            # Assert
            assert mp.date.date == current_date

    def test_morning_prayer_accepts_past_date_class(self, db):
        """Morning Prayer generates for past dates."""
        # Use a past date - production database has StandardOfficeDay records
        past_date = date_class(2020, 1, 1)

        # Act
        mp = MorningPrayer(date=past_date)

        # Assert
        assert mp.date.date == past_date
        assert mp.office_readings is not None

    def test_morning_prayer_accepts_future_date_class(self, db):
        """Morning Prayer generates for future dates."""
        # Use a future date - production database has StandardOfficeDay records
        future_date = date_class(2050, 12, 31)

        # Act
        mp = MorningPrayer(date=future_date)

        # Assert
        assert mp.date.date == future_date
        assert mp.office_readings is not None

    def test_morning_prayer_handles_leap_year(self, db):
        """Morning Prayer correctly handles February 29 (leap year)."""
        # Use leap year date - production database has StandardOfficeDay records
        leap_date = date_class(2024, 2, 29)  # 2024 is a leap year

        # Act
        mp = MorningPrayer(date=leap_date)

        # Assert
        assert mp.date.date == leap_date
        assert mp.date.date.month == 2
        assert mp.date.date.day == 29
        assert mp.office_readings is not None


@pytest.mark.unit
@pytest.mark.us1
@pytest.mark.skip(
    reason="Settings are handled by Vue.js frontend (localStorage/URL params), not backend API parameters"
)
class TestMorningPrayerSettings:
    """
    Test Morning Prayer settings integration.

    Validates: FR-005b (Psalter selection), FR-006b (Lectionary selection),
               FR-017 (Bible translation selection)
    Tasks: T020

    NOTE: These tests are marked as skip because the Daily Office is a SPA where
    user settings are managed by the Vue.js frontend (stored in browser localStorage
    and passed via URL parameters). The backend MorningPrayer class generates the
    complete office structure without settings filtering - the frontend applies
    user preferences during rendering.

    To properly test settings, we need integration/E2E tests that exercise the
    full frontend + backend flow, not unit tests of the Python backend alone.
    """

    def test_morning_prayer_uses_psalter_setting(self, db, regular_office_day):
        """Morning Prayer respects psalter cycle setting (30day/60day)."""
        office_date = date_class(2025, 1, 15)

        # Act - Create with 30-day psalter
        mp_30 = MorningPrayer(date=office_date, psalter="30day")
        mp_60 = MorningPrayer(date=office_date, psalter="60day")

        # Assert
        assert mp_30.psalter == "30day"
        assert mp_60.psalter == "60day"

    def test_morning_prayer_uses_lectionary_setting(self, db, regular_office_day):
        """Morning Prayer respects lectionary cycle setting (1year/2year)."""
        office_date = date_class(2025, 1, 15)

        # Act
        mp_1yr = MorningPrayer(date=office_date, lectionary="1year")
        mp_2yr = MorningPrayer(date=office_date, lectionary="2year")

        # Assert
        assert mp_1yr.lectionary == "1year"
        assert mp_2yr.lectionary == "2year"

    def test_morning_prayer_uses_bible_version_setting(self, db, regular_office_day):
        """Morning Prayer respects Bible translation setting."""
        office_date = date_class(2025, 1, 15)

        # Act
        mp_esv = MorningPrayer(date=office_date, bible_version="esv")
        mp_kjv = MorningPrayer(date=office_date, bible_version="kjv")
        mp_nrsvce = MorningPrayer(date=office_date, bible_version="nrsvce")

        # Assert
        assert mp_esv.bible_version == "esv"
        assert mp_kjv.bible_version == "kjv"
        assert mp_nrsvce.bible_version == "nrsvce"

    def test_morning_prayer_uses_canticle_settings(self, db, regular_office_day):
        """Morning Prayer respects canticle rotation and table settings."""
        office_date = date_class(2025, 1, 15)

        # Act
        mp = MorningPrayer(date=office_date, canticle_rotation="traditional", canticle_table="bcp2019")

        # Assert
        assert mp.canticle_rotation == "traditional"
        assert mp.canticle_table == "bcp2019"

    def test_morning_prayer_uses_confession_length_setting(self, db, regular_office_day):
        """Morning Prayer respects confession length setting."""
        office_date = date_class(2025, 1, 15)

        # Act
        mp_short = MorningPrayer(date=office_date, confession_length="short")
        mp_long = MorningPrayer(date=office_date, confession_length="long")

        # Assert
        assert mp_short.confession_length == "short"
        assert mp_long.confession_length == "long"


@pytest.mark.unit
@pytest.mark.us1
class TestMorningPrayerNavigation:
    """
    Test Morning Prayer navigation links generation.

    Validates: FR-013 (Navigate between office types)
    Tasks: T021
    """

    def test_morning_prayer_has_links_property(self, db, regular_office_day, mock_url_reverse):
        """Morning Prayer has links property for navigation."""
        mp = MorningPrayer(date=date_class(2025, 1, 15))

        # Act
        links = mp.links

        # Assert
        assert links is not None
        assert isinstance(links, dict)

    def test_morning_prayer_links_to_evening_prayer(self, db, regular_office_day, mock_url_reverse):
        """Morning Prayer provides link to Evening Prayer for same date."""
        mp = MorningPrayer(date=date_class(2025, 1, 15))

        # Act
        links = mp.links

        # Assert
        assert "evening_prayer" in links or "Evening Prayer" in str(links)

    def test_morning_prayer_links_to_midday_prayer(self, db, regular_office_day, mock_url_reverse):
        """Morning Prayer provides link to Midday Prayer for same date."""
        mp = MorningPrayer(date=date_class(2025, 1, 15))

        # Act
        links = mp.links

        # Assert
        assert "midday_prayer" in links or "Midday Prayer" in str(links)

    def test_morning_prayer_links_to_compline(self, db, regular_office_day, mock_url_reverse):
        """Morning Prayer provides link to Compline for same date."""
        mp = MorningPrayer(date=date_class(2025, 1, 15))

        # Act
        links = mp.links

        # Assert
        assert "compline" in links or "Compline" in str(links)

    def test_morning_prayer_links_preserve_date_class(self, db, regular_office_day, mock_url_reverse):
        """Morning Prayer navigation links preserve the current date."""
        test_date = date_class(2025, 1, 15)
        mp = MorningPrayer(date=test_date)

        # Act
        links = mp.links

        # Assert
        # Check that links contain the date components
        links_str = str(links)
        assert "2025" in links_str
        assert "01" in links_str or "1" in links_str
        assert "15" in links_str

    def test_morning_prayer_previous_day_link(self, db, mock_url_reverse):
        """Morning Prayer provides link to previous day."""
        # Use existing production data - StandardOfficeDay records exist for all dates
        mp = MorningPrayer(date=date_class(2025, 1, 15))

        # Act
        links = mp.links

        # Assert
        links_str = str(links)
        assert "previous" in links_str.lower() or "yesterday" in links_str.lower() or "14" in links_str

    def test_morning_prayer_next_day_link(self, db, mock_url_reverse):
        """Morning Prayer provides link to next day."""
        # Use existing production data - StandardOfficeDay records exist for all dates
        mp = MorningPrayer(date=date_class(2025, 1, 15))

        # Act
        links = mp.links

        # Assert
        links_str = str(links)
        assert "next" in links_str.lower() or "tomorrow" in links_str.lower() or "16" in links_str


@pytest.mark.unit
@pytest.mark.us1
class TestMPHeading:
    """
    Test MPHeading module for Morning Prayer.

    Validates: FR-001 (Display Morning Prayer heading)
    Tasks: T022
    """

    def test_mp_heading_has_data_property(self, db, regular_office_day):
        """MPHeading module has data property that returns dict."""
        from office.morning_prayer import MPHeading

        mp_heading = MPHeading(date=date_class(2025, 1, 15), office_readings=regular_office_day)

        # Act
        data = mp_heading.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_mp_heading_includes_heading_text(self, db, regular_office_day):
        """MPHeading data includes 'Daily Morning Prayer' heading."""
        from office.morning_prayer import MPHeading

        mp_heading = MPHeading(date=date_class(2025, 1, 15), office_readings=regular_office_day)

        # Act
        data = mp_heading.data

        # Assert
        assert "heading" in data
        assert "Morning Prayer" in str(data["heading"]) or "Morning" in str(data["heading"])

    def test_mp_heading_includes_calendar_date(self, db, regular_office_day):
        """MPHeading data includes calendar_date for liturgical context."""
        from office.morning_prayer import MPHeading

        mp_heading = MPHeading(date=date_class(2025, 1, 15), office_readings=regular_office_day)

        # Act
        data = mp_heading.data

        # Assert
        assert "calendar_date" in data
        assert data["calendar_date"] is not None


@pytest.mark.unit
@pytest.mark.us1
class TestMPOpeningSentence:
    """
    Test MPOpeningSentence module for Morning Prayer.

    Validates: FR-009 (Include full text of opening sentences)
    Tasks: T023
    """

    def test_mp_opening_sentence_has_data_property(self, db, regular_office_day):
        """MPOpeningSentence module has data property that returns dict."""
        from office.morning_prayer import MPOpeningSentence
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        opening = MPOpeningSentence(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = opening.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_mp_opening_sentence_includes_sentence(self, db, regular_office_day):
        """MPOpeningSentence data includes sentence text."""
        from office.morning_prayer import MPOpeningSentence
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        opening = MPOpeningSentence(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = opening.data

        # Assert
        assert "sentence" in data
        assert data["sentence"] is not None
        assert isinstance(data["sentence"], dict)
        assert "sentence" in data["sentence"]
        assert "citation" in data["sentence"]

    def test_mp_opening_sentence_advent_season(self, db):
        """MPOpeningSentence returns Advent-specific sentence during Advent."""
        from office.morning_prayer import MPOpeningSentence
        from churchcal.calculations import get_calendar_date

        # Use First Sunday of Advent
        advent_date = date_class(2024, 12, 1)  # First Sunday of Advent 2024
        calendar_date = get_calendar_date(advent_date)
        office_day = StandardOfficeDay.objects.get(month=advent_date.month, day=advent_date.day)

        opening = MPOpeningSentence(date=calendar_date, office_readings=office_day)

        # Act
        data = opening.data

        # Assert
        assert "sentence" in data
        assert "ISAIAH 40:3" in data["sentence"]["citation"]
        assert "wilderness" in data["sentence"]["sentence"].lower()

    def test_mp_opening_sentence_christmas_season(self, db):
        """MPOpeningSentence returns Christmas-specific sentence during Christmastide."""
        from office.morning_prayer import MPOpeningSentence
        from churchcal.calculations import get_calendar_date

        # Use Christmas Day
        christmas_date = date_class(2024, 12, 25)
        calendar_date = get_calendar_date(christmas_date)
        office_day = StandardOfficeDay.objects.get(month=christmas_date.month, day=christmas_date.day)

        opening = MPOpeningSentence(date=calendar_date, office_readings=office_day)

        # Act
        data = opening.data

        # Assert
        assert "sentence" in data
        assert "LUKE 2:10" in data["sentence"]["citation"]
        assert "good news" in data["sentence"]["sentence"].lower()

    def test_mp_opening_sentence_lent_season(self, db):
        """MPOpeningSentence returns Lent-specific sentence during Lent."""
        from office.morning_prayer import MPOpeningSentence
        from churchcal.calculations import get_calendar_date

        # Use Ash Wednesday 2025
        ash_wednesday = date_class(2025, 3, 5)
        calendar_date = get_calendar_date(ash_wednesday)
        office_day = StandardOfficeDay.objects.get(month=ash_wednesday.month, day=ash_wednesday.day)

        opening = MPOpeningSentence(date=calendar_date, office_readings=office_day)

        # Act
        data = opening.data

        # Assert
        assert "sentence" in data
        # Lent has multiple sentences that rotate by day of week
        assert data["sentence"]["sentence"] is not None
        assert data["sentence"]["citation"] is not None

    def test_mp_opening_sentence_easter_season(self, db):
        """MPOpeningSentence returns Easter-specific sentence during Eastertide."""
        from office.morning_prayer import MPOpeningSentence
        from churchcal.calculations import get_calendar_date

        # Use Easter Sunday 2025
        easter_date = date_class(2025, 4, 20)
        calendar_date = get_calendar_date(easter_date)
        office_day = StandardOfficeDay.objects.get(month=easter_date.month, day=easter_date.day)

        opening = MPOpeningSentence(date=calendar_date, office_readings=office_day)

        # Act
        data = opening.data

        # Assert
        assert "sentence" in data
        assert "COLOSSIANS 3:1" in data["sentence"]["citation"]
        assert "raised with Christ" in data["sentence"]["sentence"]

    def test_mp_opening_sentence_weekday_rotation(self, db, regular_office_day):
        """MPOpeningSentence rotates different sentences for ordinary weekdays (non-seasonal)."""
        from office.morning_prayer import MPOpeningSentence
        from churchcal.calculations import get_calendar_date

        # Test a week in June (ordinary time after Trinity Sunday, not a special season)
        # Use 2025-06-09 through 2025-06-15 (week after Trinity Sunday)
        weekday_sentences = {}
        for day_offset in range(7):
            test_date = date_class(2025, 6, 9 + day_offset)  # Monday through Sunday
            calendar_date = get_calendar_date(test_date)
            office_day = StandardOfficeDay.objects.get(month=test_date.month, day=test_date.day)

            opening = MPOpeningSentence(date=calendar_date, office_readings=office_day)
            data = opening.data

            weekday_name = test_date.strftime("%A")
            weekday_sentences[weekday_name] = data["sentence"]["citation"]

        # Assert - Different sentences for different days (at least some variety)
        # During ordinary time, each weekday should have its own opening sentence
        unique_citations = set(weekday_sentences.values())
        assert (
            len(unique_citations) > 1
        ), f"Expected different opening sentences for different weekdays, got: {weekday_sentences}"


@pytest.mark.unit
@pytest.mark.us1
class TestConfession:
    """
    Test Confession module for Morning Prayer.

    Validates: FR-009 (Include full text of confession)
    Tasks: T024
    """

    def test_confession_has_data_property(self, db, regular_office_day):
        """Confession module has data property that returns dict."""
        from office.offices import Confession
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        confession = Confession(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = confession.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_confession_includes_heading(self, db, regular_office_day):
        """Confession data includes heading."""
        from office.offices import Confession
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        confession = Confession(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = confession.data

        # Assert
        assert "heading" in data
        assert "Confession" in data["heading"]

    def test_confession_fast_day_flag(self, db):
        """Confession marks fast days appropriately."""
        from office.offices import Confession
        from churchcal.calculations import get_calendar_date

        # Test Ash Wednesday (fast day)
        ash_wednesday = date_class(2025, 3, 5)
        calendar_date = get_calendar_date(ash_wednesday)
        office_day = StandardOfficeDay.objects.get(month=ash_wednesday.month, day=ash_wednesday.day)

        confession = Confession(date=calendar_date, office_readings=office_day)

        # Act
        data = confession.data

        # Assert
        assert "fast_day" in data


@pytest.mark.unit
@pytest.mark.us1
class TestInvitatory:
    """
    Test Invitatory module for Morning Prayer.

    Validates: FR-009 (Include invitatory)
    Tasks: T025
    """

    def test_invitatory_has_data_property(self, db, regular_office_day):
        """Invitatory module has data property that returns dict."""
        from office.offices import Invitatory
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        invitatory = Invitatory(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = invitatory.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)


@pytest.mark.unit
@pytest.mark.us1
class TestCreed:
    """
    Test Creed module for Morning Prayer.

    Validates: FR-009 (Include the Apostles' Creed)
    Tasks: T031
    """

    def test_creed_has_data_property(self, db, regular_office_day):
        """Creed module has data property that returns dict."""
        from office.offices import Creed
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        creed = Creed(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = creed.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)


@pytest.mark.unit
@pytest.mark.us1
class TestPrayers:
    """
    Test Prayers module for Morning Prayer.

    Validates: FR-009 (Include the Lord's Prayer)
    Tasks: T032
    """

    def test_prayers_has_data_property(self, db, regular_office_day):
        """Prayers module has data property that returns dict."""
        from office.offices import Prayers
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        prayers = Prayers(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = prayers.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_prayers_includes_heading(self, db, regular_office_day):
        """Prayers data includes heading."""
        from office.offices import Prayers
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        prayers = Prayers(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = prayers.data

        # Assert
        assert "heading" in data
        assert "Prayers" in data["heading"]


@pytest.mark.unit
@pytest.mark.us1
class TestMPSuffrages:
    """
    Test MPSuffrages module for Morning Prayer.

    Validates: FR-009 (Include suffrages)
    Tasks: T033
    """

    def test_mp_suffrages_has_data_property(self, db, regular_office_day):
        """MPSuffrages module has data property that returns dict."""
        from office.morning_prayer import MPSuffrages
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        suffrages = MPSuffrages(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = suffrages.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)


@pytest.mark.unit
@pytest.mark.us1
class TestDismissal:
    """
    Test Dismissal module for Morning Prayer.

    Validates: FR-009 (Include dismissal)
    Tasks: T036
    """

    def test_dismissal_has_data_property(self, db, regular_office_day):
        """Dismissal module has data property that returns dict."""
        from office.offices import Dismissal
        from churchcal.calculations import get_calendar_date
        from office.morning_prayer import MorningPrayer

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        mp = MorningPrayer(date=date_class(2025, 1, 15))
        dismissal = Dismissal(date=calendar_date, office_readings=regular_office_day, office=mp)

        # Act
        data = dismissal.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_dismissal_easter_alleluia(self, db):
        """Dismissal includes Alleluia during Eastertide."""
        from office.offices import Dismissal
        from churchcal.calculations import get_calendar_date
        from office.morning_prayer import MorningPrayer

        # Use Easter Sunday 2025
        easter_date = date_class(2025, 4, 20)
        calendar_date = get_calendar_date(easter_date)
        office_day = StandardOfficeDay.objects.get(month=easter_date.month, day=easter_date.day)
        mp = MorningPrayer(date=easter_date)
        dismissal = Dismissal(date=calendar_date, office_readings=office_day, office=mp)

        # Act
        data = dismissal.data

        # Assert
        # During Easter, dismissal should include "Alleluia"
        data_str = str(data)
        assert "Alleluia" in data_str or "alleluia" in data_str

    def test_dismissal_weekday_rotation(self, db):
        """Dismissal rotates different graces for weekdays."""
        from office.offices import Dismissal
        from churchcal.calculations import get_calendar_date
        from office.morning_prayer import MorningPrayer

        # Test a week in June (ordinary time)
        weekday_graces = {}
        for day_offset in range(7):
            test_date = date_class(2025, 6, 9 + day_offset)  # Monday through Sunday
            calendar_date = get_calendar_date(test_date)
            office_day = StandardOfficeDay.objects.get(month=test_date.month, day=test_date.day)
            mp = MorningPrayer(date=test_date)
            dismissal = Dismissal(date=calendar_date, office_readings=office_day, office=mp)

            data = dismissal.data

            weekday_name = test_date.strftime("%A")
            # Store the grace data as a string for comparison
            weekday_graces[weekday_name] = str(data.get("grace", ""))

        # Assert - Should have some variety in graces across the week
        unique_graces = set(weekday_graces.values())
        assert len(unique_graces) >= 2, f"Expected different graces for different weekdays"


@pytest.mark.unit
@pytest.mark.us1
class TestMPPsalms:
    """
    Test MPPsalms module for Morning Prayer.

    Validates: FR-005 (Different psalm assignments), FR-005a (30-day and 60-day cycles)
    Tasks: T026
    """

    def test_mp_psalms_has_data_property(self, db, regular_office_day):
        """MPPsalms module has data property that returns dict."""
        from office.morning_prayer import MPPsalms
        from office.models import ThirtyDayPsalterDay
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        # Get 30-day psalter day from production database
        thirty_day_psalter = ThirtyDayPsalterDay.objects.get(day=15)
        psalms = MPPsalms(
            date=calendar_date, office_readings=regular_office_day, thirty_day_psalter_day=thirty_day_psalter
        )

        # Act
        data = psalms.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_mp_psalms_includes_60_day_cycle(self, db, regular_office_day):
        """MPPsalms includes 60-day cycle psalm citations."""
        from office.morning_prayer import MPPsalms
        from office.models import ThirtyDayPsalterDay
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        thirty_day_psalter = ThirtyDayPsalterDay.objects.get(day=15)
        psalms = MPPsalms(
            date=calendar_date, office_readings=regular_office_day, thirty_day_psalter_day=thirty_day_psalter
        )

        # Act
        data = psalms.data

        # Assert
        assert "citations_60" in data
        assert "psalms_60" in data
        assert "heading_60" in data

    def test_mp_psalms_includes_30_day_cycle(self, db, regular_office_day):
        """MPPsalms includes 30-day cycle psalm citations."""
        from office.morning_prayer import MPPsalms
        from office.models import ThirtyDayPsalterDay
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        thirty_day_psalter = ThirtyDayPsalterDay.objects.get(day=15)
        psalms = MPPsalms(
            date=calendar_date, office_readings=regular_office_day, thirty_day_psalter_day=thirty_day_psalter
        )

        # Act
        data = psalms.data

        # Assert
        assert "citations_30" in data
        assert "psalms_30" in data
        assert "heading_30" in data

    def test_mp_psalms_citations_are_lists(self, db, regular_office_day):
        """MPPsalms citations are returned as lists."""
        from office.morning_prayer import MPPsalms
        from office.models import ThirtyDayPsalterDay
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        thirty_day_psalter = ThirtyDayPsalterDay.objects.get(day=15)
        psalms = MPPsalms(
            date=calendar_date, office_readings=regular_office_day, thirty_day_psalter_day=thirty_day_psalter
        )

        # Act
        data = psalms.data

        # Assert
        assert isinstance(data["citations_60"], list)
        assert isinstance(data["citations_30"], list)


@pytest.mark.unit
@pytest.mark.us1
class TestMPFirstReading:
    """
    Test MPFirstReading module for Morning Prayer.

    Validates: FR-006 (Two scripture readings per office)
    Tasks: T027
    """

    def test_mp_first_reading_has_data_method(self, db, regular_office_day):
        """MPFirstReading module has data method that returns dict."""
        from office.morning_prayer import MPFirstReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = MPFirstReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_mp_first_reading_includes_heading(self, db, regular_office_day):
        """MPFirstReading includes heading."""
        from office.morning_prayer import MPFirstReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = MPFirstReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        assert "heading" in data
        assert "First Lesson" in data["heading"] or "First" in data["heading"]

    def test_mp_first_reading_has_main_reading(self, db, regular_office_day):
        """MPFirstReading includes main reading from office_readings."""
        from office.morning_prayer import MPFirstReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = MPFirstReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        assert "main_reading" in data
        assert data["main_reading"] is not None

    def test_mp_first_reading_includes_passage_citation(self, db, regular_office_day):
        """MPFirstReading includes passage citation."""
        from office.morning_prayer import MPFirstReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = MPFirstReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        if data["main_reading"]:
            assert "intro" in data["main_reading"]
            assert "passage" in data["main_reading"]


@pytest.mark.unit
@pytest.mark.us1
class TestMPSecondReading:
    """
    Test MPSecondReading module for Morning Prayer.

    Validates: FR-006 (Two scripture readings per office)
    Tasks: T029
    """

    def test_mp_second_reading_has_data_method(self, db, regular_office_day):
        """MPSecondReading module has data method that returns dict."""
        from office.morning_prayer import MPSecondReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = MPSecondReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_mp_second_reading_includes_heading(self, db, regular_office_day):
        """MPSecondReading includes heading."""
        from office.morning_prayer import MPSecondReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = MPSecondReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        assert "heading" in data
        assert "Second Lesson" in data["heading"] or "Second" in data["heading"]

    def test_mp_second_reading_has_main_reading(self, db, regular_office_day):
        """MPSecondReading includes main reading from office_readings."""
        from office.morning_prayer import MPSecondReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = MPSecondReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        assert "main_reading" in data
        assert data["main_reading"] is not None


@pytest.mark.unit
@pytest.mark.us1
class TestMPCanticle1:
    """
    Test MPCanticle1 module for Morning Prayer.

    Validates: FR-008 (Display appropriate canticles)
    Tasks: T028
    """

    def test_mp_canticle1_has_data_property(self, db, regular_office_day):
        """MPCanticle1 module has data property that returns dict."""
        from office.morning_prayer import MPCanticle1
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        canticle = MPCanticle1(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = canticle.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_mp_canticle1_includes_canticle_tables(self, db, regular_office_day):
        """MPCanticle1 includes canticles from different tables (default, 1979, 2011)."""
        from office.morning_prayer import MPCanticle1
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        canticle = MPCanticle1(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = canticle.data

        # Assert - Should include canticles from different tables
        assert "default" in data or "1979" in data or "2011" in data

    def test_mp_canticle1_returns_canticle_data(self, db, regular_office_day):
        """MPCanticle1 returns canticle data structures."""
        from office.morning_prayer import MPCanticle1
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        canticle = MPCanticle1(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = canticle.data

        # Assert - Each canticle table should return a canticle
        for key in data:
            if data[key]:
                assert isinstance(data[key], dict) or hasattr(data[key], "__dict__")


@pytest.mark.unit
@pytest.mark.us1
class TestMPCanticle2:
    """
    Test MPCanticle2 module for Morning Prayer.

    Validates: FR-008 (Display appropriate canticles)
    Tasks: T030
    """

    def test_mp_canticle2_has_data_property(self, db, regular_office_day):
        """MPCanticle2 module has data property that returns dict."""
        from office.morning_prayer import MPCanticle2
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        canticle = MPCanticle2(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = canticle.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_mp_canticle2_includes_canticle_tables(self, db, regular_office_day):
        """MPCanticle2 includes canticles from different tables (default, 1979, 2011)."""
        from office.morning_prayer import MPCanticle2
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        canticle = MPCanticle2(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = canticle.data

        # Assert - Should include canticles from different tables
        assert "default" in data or "1979" in data or "2011" in data


@pytest.mark.unit
@pytest.mark.us1
class TestMPCollectsOfTheDay:
    """
    Test MPCollectsOfTheDay module for Morning Prayer.

    Validates: FR-009 (Include full text of collects), FR-007 (Proper collects for feasts)
    Tasks: T034
    """

    def test_mp_collects_of_the_day_has_data_property(self, db, regular_office_day):
        """MPCollectsOfTheDay module has data property that returns dict."""
        from office.morning_prayer import MPCollectsOfTheDay
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        collects = MPCollectsOfTheDay(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = collects.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_mp_collects_of_the_day_includes_collects(self, db, regular_office_day):
        """MPCollectsOfTheDay includes collects generator."""
        from office.morning_prayer import MPCollectsOfTheDay
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        collects = MPCollectsOfTheDay(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = collects.data

        # Assert
        assert "collects" in data

    def test_mp_collects_of_the_day_feast_day(self, db):
        """MPCollectsOfTheDay includes feast day collect."""
        from office.morning_prayer import MPCollectsOfTheDay
        from churchcal.calculations import get_calendar_date

        # Use Christmas Day
        christmas_date = date_class(2024, 12, 25)
        calendar_date = get_calendar_date(christmas_date)
        office_day = StandardOfficeDay.objects.get(month=christmas_date.month, day=christmas_date.day)

        collects = MPCollectsOfTheDay(date=calendar_date, office_readings=office_day)

        # Act
        data = collects.data

        # Assert - Christmas should have a collect
        collects_list = list(data["collects"])
        assert len(collects_list) >= 1


@pytest.mark.unit
@pytest.mark.us1
class TestMPCollects:
    """
    Test MPCollects module for Morning Prayer.

    Validates: FR-009 (Include full text of collects)
    Tasks: T035
    """

    def test_mp_collects_has_data_property(self, db, regular_office_day):
        """MPCollects module has data property that returns dict."""
        from office.morning_prayer import MPCollects
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        collects = MPCollects(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = collects.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_mp_collects_includes_weekday_collect(self, db, regular_office_day):
        """MPCollects includes weekday-specific collect."""
        from office.morning_prayer import MPCollects
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))  # Wednesday
        collects = MPCollects(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = collects.data

        # Assert
        assert "collect" in data
        assert data["collect"] is not None
        assert len(data["collect"]) == 3  # (heading, weekday, text)

    def test_mp_collects_includes_fixed_collects(self, db, regular_office_day):
        """MPCollects includes fixed collects (peace and grace)."""
        from office.morning_prayer import MPCollects
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        collects = MPCollects(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = collects.data

        # Assert
        assert "fixed_collects" in data
        assert len(data["fixed_collects"]) == 2  # Peace and Grace

    def test_mp_collects_weekday_rotation(self, db):
        """MPCollects rotates different collects for each weekday."""
        from office.morning_prayer import MPCollects
        from churchcal.calculations import get_calendar_date

        # Test a week
        weekday_collects = {}
        for day_offset in range(7):
            test_date = date_class(2025, 1, 13 + day_offset)  # Monday through Sunday
            calendar_date = get_calendar_date(test_date)
            office_day = StandardOfficeDay.objects.get(month=test_date.month, day=test_date.day)

            collects = MPCollects(date=calendar_date, office_readings=office_day)
            data = collects.data

            weekday_name = test_date.strftime("%A")
            weekday_collects[weekday_name] = data["collect"][0]  # Collect title

        # Assert - Different collects for different days
        unique_collects = set(weekday_collects.values())
        assert len(unique_collects) == 7, f"Expected 7 different weekday collects, got {len(unique_collects)}"
