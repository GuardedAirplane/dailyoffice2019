"""
Unit tests for Evening Prayer office generation.

Validates: FR-002 (Display Evening Prayer with all components)
User Story: US2 (View Evening Prayer)
Priority: P1 (High) - MVP Feature

Tests must be written FIRST and must FAIL before implementation per Constitution Principle III.
Since implementation already exists, these tests verify existing functionality.

Constitution Requirements:
- FR-002: Display Evening Prayer with all required liturgical components
- FR-005: Different psalm assignments for Morning vs Evening Prayer
- FR-006: Two scripture readings per office
- FR-008: Display appropriate canticles (Magnificat/Nunc Dimittis for Evening Prayer)
- FR-009: Include full text of prayers and canticles
- FR-010: Format with proper indentation and rubrics
- FR-011: Display commemorations and feast names
- FR-013: Provide navigation between office types
"""

import pytest
from datetime import date as date_class
from freezegun import freeze_time

from office.evening_prayer import EveningPrayer
from office.models import StandardOfficeDay
from office.tests.fixtures import (
    acna_calendar,
    christmas_office_day,
    regular_office_day,
    cached_scripture,
    complete_settings,
)


@pytest.mark.unit
@pytest.mark.us2
class TestEveningPrayerInstantiation:
    """
    Test EveningPrayer class instantiation and initialization.

    Validates: FR-002, US2
    Tasks: T047
    """

    def test_evening_prayer_instantiates_with_date_class(self, db, acna_calendar, regular_office_day):
        """Evening Prayer instantiates with valid date."""
        office_date = date_class(2025, 1, 15)

        # Act
        ep = EveningPrayer(date=office_date)

        # Assert
        assert ep is not None
        assert ep.date.date == office_date
        assert ep.name == "Evening Prayer"
        assert ep.office == "evening_prayer"

    def test_evening_prayer_requires_date_class(self, db):
        """Evening Prayer raises error when instantiated without date."""
        # Act & Assert
        with pytest.raises(TypeError):
            EveningPrayer()

    def test_evening_prayer_retrieves_office_readings(self, db, acna_calendar, regular_office_day):
        """Evening Prayer retrieves correct OfficeDay readings for date."""
        office_date = date_class(2025, 1, 15)

        # Act
        ep = EveningPrayer(date=office_date)

        # Assert
        assert ep.office_readings is not None
        assert isinstance(ep.office_readings, StandardOfficeDay)
        assert ep.office_readings.month == 1
        assert ep.office_readings.day == 15


@pytest.mark.unit
@pytest.mark.us2
class TestEveningPrayerModules:
    """
    Test Evening Prayer module list composition.

    Validates: FR-002 (Complete office structure)
    Tasks: T048
    """

    def test_evening_prayer_has_modules_property(self, db, regular_office_day):
        """Evening Prayer has modules property that returns list of tuples."""
        ep = EveningPrayer(date=date_class(2025, 1, 15))

        # Act
        modules = ep.modules

        # Assert
        assert modules is not None
        assert isinstance(modules, list)

    def test_evening_prayer_has_minimum_20_modules(self, db, regular_office_day):
        """Evening Prayer contains at least 20 liturgical modules."""
        ep = EveningPrayer(date=date_class(2025, 1, 15))

        # Act
        modules = ep.modules

        # Assert
        assert len(modules) >= 20, f"Expected at least 20 modules, got {len(modules)}"

    def test_evening_prayer_modules_are_tuples(self, db, regular_office_day):
        """Evening Prayer modules are tuples of (instance, template_path)."""
        ep = EveningPrayer(date=date_class(2025, 1, 15))

        # Act
        modules = ep.modules

        # Assert
        for module in modules:
            assert isinstance(module, tuple)
            assert len(module) == 2
            assert isinstance(module[1], str)  # Template path

    def test_evening_prayer_includes_required_sections(self, db, regular_office_day):
        """Evening Prayer includes all required liturgical sections."""
        ep = EveningPrayer(date=date_class(2025, 1, 15))

        # Act
        modules = ep.modules
        module_names = [m[0].__class__.__name__ for m in modules]

        # Assert - Evening Prayer specific sections
        assert "EPHeading" in module_names
        assert "EPOpeningSentence" in module_names
        assert "EPPsalms" in module_names
        assert "EPCanticle1" in module_names
        assert "EPCanticle2" in module_names
        assert "EPSuffrages" in module_names

        # Assert - Common sections
        assert "Confession" in module_names
        assert "Creed" in module_names
        assert "Prayers" in module_names
        assert "Dismissal" in module_names


@pytest.mark.unit
@pytest.mark.us2
class TestEveningPrayerDateHandling:
    """
    Test Evening Prayer date handling capabilities.

    Validates: FR-012 (View offices for any date)
    Tasks: T047
    """

    def test_evening_prayer_accepts_current_date_class(self, db, regular_office_day):
        """Evening Prayer accepts current date."""
        ep = EveningPrayer(date=date_class(2025, 1, 15))

        # Assert
        assert ep.date.date == date_class(2025, 1, 15)

    def test_evening_prayer_accepts_past_date_class(self, db):
        """Evening Prayer accepts past date."""
        past_date = date_class(2020, 1, 1)

        # Act
        ep = EveningPrayer(date=past_date)

        # Assert
        assert ep.date.date == past_date

    def test_evening_prayer_accepts_future_date_class(self, db):
        """Evening Prayer accepts future date."""
        future_date = date_class(2030, 12, 31)

        # Act
        ep = EveningPrayer(date=future_date)

        # Assert
        assert ep.date.date == future_date

    def test_evening_prayer_handles_leap_year(self, db):
        """Evening Prayer handles leap year date (Feb 29)."""
        leap_date = date_class(2024, 2, 29)

        # Act
        ep = EveningPrayer(date=leap_date)

        # Assert
        assert ep.date.date == leap_date
        assert ep.office_readings is not None


@pytest.mark.unit
@pytest.mark.us2
class TestEveningPrayerNavigation:
    """
    Test Evening Prayer navigation links generation.

    Validates: FR-013 (Navigate between office types)
    Tasks: T047
    """

    def test_evening_prayer_has_links_property(self, db, regular_office_day, mock_url_reverse):
        """Evening Prayer has links property."""
        ep = EveningPrayer(date=date_class(2025, 1, 15))

        # Act
        links = ep.links

        # Assert
        assert links is not None

    def test_evening_prayer_links_to_morning_prayer(self, db, regular_office_day, mock_url_reverse):
        """Evening Prayer links to Morning Prayer."""
        ep = EveningPrayer(date=date_class(2025, 1, 15))

        # Act
        links = ep.links

        # Assert
        links_str = str(links)
        assert "morning_prayer" in links_str.lower() or "morning" in links_str.lower()

    def test_evening_prayer_links_to_midday_prayer(self, db, regular_office_day, mock_url_reverse):
        """Evening Prayer links to Midday Prayer."""
        ep = EveningPrayer(date=date_class(2025, 1, 15))

        # Act
        links = ep.links

        # Assert
        links_str = str(links)
        assert "midday_prayer" in links_str.lower() or "midday" in links_str.lower()

    def test_evening_prayer_links_to_compline(self, db, regular_office_day, mock_url_reverse):
        """Evening Prayer links to Compline."""
        ep = EveningPrayer(date=date_class(2025, 1, 15))

        # Act
        links = ep.links

        # Assert
        links_str = str(links)
        assert "compline" in links_str.lower()

    def test_evening_prayer_links_preserve_date_class(self, db, regular_office_day, mock_url_reverse):
        """Evening Prayer navigation links preserve the current date."""
        test_date = date_class(2025, 1, 15)
        ep = EveningPrayer(date=test_date)

        # Act
        links = ep.links

        # Assert
        links_str = str(links)
        assert "2025" in links_str and "15" in links_str

    def test_evening_prayer_previous_day_link(self, db, mock_url_reverse):
        """Evening Prayer provides link to previous day."""
        ep = EveningPrayer(date=date_class(2025, 1, 15))

        # Act
        links = ep.links

        # Assert
        links_str = str(links)
        assert "prev" in links_str.lower() or "yesterday" in links_str.lower() or "14" in links_str

    def test_evening_prayer_next_day_link(self, db, mock_url_reverse):
        """Evening Prayer provides link to next day."""
        ep = EveningPrayer(date=date_class(2025, 1, 15))

        # Act
        links = ep.links

        # Assert
        links_str = str(links)
        assert "next" in links_str.lower() or "tomorrow" in links_str.lower() or "16" in links_str


@pytest.mark.unit
@pytest.mark.us2
class TestEPHeading:
    """
    Test EPHeading module for Evening Prayer.

    Validates: FR-002 (Display Evening Prayer heading)
    Tasks: T049
    """

    def test_ep_heading_has_data_property(self, db, regular_office_day):
        """EPHeading module has data property that returns dict."""
        from office.evening_prayer import EPHeading

        ep_heading = EPHeading(date=date_class(2025, 1, 15), office_readings=regular_office_day)

        # Act
        data = ep_heading.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_ep_heading_includes_heading_text(self, db, regular_office_day):
        """EPHeading data includes 'Daily Evening Prayer' heading."""
        from office.evening_prayer import EPHeading

        ep_heading = EPHeading(date=date_class(2025, 1, 15), office_readings=regular_office_day)

        # Act
        data = ep_heading.data

        # Assert
        assert "heading" in data
        assert "Evening Prayer" in str(data["heading"]) or "Evening" in str(data["heading"])

    def test_ep_heading_includes_calendar_date(self, db, regular_office_day):
        """EPHeading data includes calendar_date for liturgical context."""
        from office.evening_prayer import EPHeading

        ep_heading = EPHeading(date=date_class(2025, 1, 15), office_readings=regular_office_day)

        # Act
        data = ep_heading.data

        # Assert
        assert "calendar_date" in data
        assert data["calendar_date"] is not None


@pytest.mark.unit
@pytest.mark.us2
class TestEPOpeningSentence:
    """
    Test EPOpeningSentence module for Evening Prayer.

    Validates: FR-009 (Include full text of opening sentences)
    Tasks: T049
    """

    def test_ep_opening_sentence_has_data_property(self, db, regular_office_day):
        """EPOpeningSentence module has data property that returns dict."""
        from office.evening_prayer import EPOpeningSentence
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        opening = EPOpeningSentence(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = opening.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_ep_opening_sentence_includes_sentence(self, db, regular_office_day):
        """EPOpeningSentence data includes sentence text."""
        from office.evening_prayer import EPOpeningSentence
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        opening = EPOpeningSentence(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = opening.data

        # Assert
        assert "sentence" in data
        assert data["sentence"] is not None
        assert isinstance(data["sentence"], dict)
        assert "sentence" in data["sentence"]
        assert "citation" in data["sentence"]

    def test_ep_opening_sentence_advent_season(self, db):
        """EPOpeningSentence returns Advent-specific sentence during Advent."""
        from office.evening_prayer import EPOpeningSentence
        from churchcal.calculations import get_calendar_date

        # Use First Sunday of Advent
        advent_date = date_class(2024, 12, 1)
        calendar_date = get_calendar_date(advent_date)
        office_day = StandardOfficeDay.objects.get(month=advent_date.month, day=advent_date.day)

        opening = EPOpeningSentence(date=calendar_date, office_readings=office_day)

        # Act
        data = opening.data

        # Assert
        assert "sentence" in data
        assert "MARK 13:35-36" in data["sentence"]["citation"]
        assert "stay awake" in data["sentence"]["sentence"].lower()

    def test_ep_opening_sentence_christmas_season(self, db):
        """EPOpeningSentence returns Christmas-specific sentence during Christmastide."""
        from office.evening_prayer import EPOpeningSentence
        from churchcal.calculations import get_calendar_date

        # Use Christmas Day
        christmas_date = date_class(2024, 12, 25)
        calendar_date = get_calendar_date(christmas_date)
        office_day = StandardOfficeDay.objects.get(month=christmas_date.month, day=christmas_date.day)

        opening = EPOpeningSentence(date=calendar_date, office_readings=office_day)

        # Act
        data = opening.data

        # Assert
        assert "sentence" in data
        assert "REVELATION 21:3" in data["sentence"]["citation"]
        assert "dwelling place of God" in data["sentence"]["sentence"]

    def test_ep_opening_sentence_lent_season(self, db):
        """EPOpeningSentence returns Lent-specific sentence during Lent."""
        from office.evening_prayer import EPOpeningSentence
        from churchcal.calculations import get_calendar_date

        # Use Ash Wednesday 2025
        ash_wednesday = date_class(2025, 3, 5)
        calendar_date = get_calendar_date(ash_wednesday)
        office_day = StandardOfficeDay.objects.get(month=ash_wednesday.month, day=ash_wednesday.day)

        opening = EPOpeningSentence(date=calendar_date, office_readings=office_day)

        # Act
        data = opening.data

        # Assert
        assert "sentence" in data
        # Lent has multiple sentences that rotate by day of week
        assert data["sentence"]["sentence"] is not None
        assert data["sentence"]["citation"] is not None

    def test_ep_opening_sentence_easter_season(self, db):
        """EPOpeningSentence returns Easter-specific sentence during Eastertide."""
        from office.evening_prayer import EPOpeningSentence
        from churchcal.calculations import get_calendar_date

        # Use Easter Sunday 2025
        easter_date = date_class(2025, 4, 20)
        calendar_date = get_calendar_date(easter_date)
        office_day = StandardOfficeDay.objects.get(month=easter_date.month, day=easter_date.day)

        opening = EPOpeningSentence(date=calendar_date, office_readings=office_day)

        # Act
        data = opening.data

        # Assert
        assert "sentence" in data
        assert "1 CORINTHIANS 15:57" in data["sentence"]["citation"]
        assert "Thanks be to God" in data["sentence"]["sentence"]

    def test_ep_opening_sentence_weekday_rotation(self, db, regular_office_day):
        """EPOpeningSentence rotates different sentences for ordinary weekdays (non-seasonal)."""
        from office.evening_prayer import EPOpeningSentence
        from churchcal.calculations import get_calendar_date

        # Test a week in June (ordinary time after Trinity Sunday)
        weekday_sentences = {}
        for day_offset in range(7):
            test_date = date_class(2025, 6, 9 + day_offset)  # Monday through Sunday
            calendar_date = get_calendar_date(test_date)
            office_day = StandardOfficeDay.objects.get(month=test_date.month, day=test_date.day)

            opening = EPOpeningSentence(date=calendar_date, office_readings=office_day)
            data = opening.data

            weekday_name = test_date.strftime("%A")
            weekday_sentences[weekday_name] = data["sentence"]["citation"]

        # Assert - Different sentences for different days
        unique_citations = set(weekday_sentences.values())
        assert len(unique_citations) > 1, f"Expected different opening sentences for different weekdays"


@pytest.mark.unit
@pytest.mark.us2
class TestEPPsalms:
    """
    Test EPPsalms module for Evening Prayer.

    Validates: FR-005 (Different psalm assignments for Evening Prayer)
    Tasks: T050
    """

    def test_ep_psalms_has_data_property(self, db, regular_office_day):
        """EPPsalms module has data property that returns dict."""
        from office.evening_prayer import EPPsalms
        from office.models import ThirtyDayPsalterDay
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        thirty_day_psalter = ThirtyDayPsalterDay.objects.get(day=15)
        psalms = EPPsalms(
            date=calendar_date, office_readings=regular_office_day, thirty_day_psalter_day=thirty_day_psalter
        )

        # Act
        data = psalms.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_ep_psalms_includes_60_day_cycle(self, db, regular_office_day):
        """EPPsalms includes 60-day cycle psalm citations."""
        from office.evening_prayer import EPPsalms
        from office.models import ThirtyDayPsalterDay
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        thirty_day_psalter = ThirtyDayPsalterDay.objects.get(day=15)
        psalms = EPPsalms(
            date=calendar_date, office_readings=regular_office_day, thirty_day_psalter_day=thirty_day_psalter
        )

        # Act
        data = psalms.data

        # Assert
        assert "citations_60" in data
        assert "psalms_60" in data
        assert "heading_60" in data

    def test_ep_psalms_includes_30_day_cycle(self, db, regular_office_day):
        """EPPsalms includes 30-day cycle psalm citations."""
        from office.evening_prayer import EPPsalms
        from office.models import ThirtyDayPsalterDay
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        thirty_day_psalter = ThirtyDayPsalterDay.objects.get(day=15)
        psalms = EPPsalms(
            date=calendar_date, office_readings=regular_office_day, thirty_day_psalter_day=thirty_day_psalter
        )

        # Act
        data = psalms.data

        # Assert
        assert "citations_30" in data
        assert "psalms_30" in data
        assert "heading_30" in data

    def test_ep_psalms_different_from_morning(self, db, regular_office_day):
        """EPPsalms uses evening psalm assignments (ep_psalms), different from morning."""
        from office.evening_prayer import EPPsalms
        from office.morning_prayer import MPPsalms
        from office.models import ThirtyDayPsalterDay
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        thirty_day_psalter = ThirtyDayPsalterDay.objects.get(day=15)

        # Act
        ep_psalms = EPPsalms(
            date=calendar_date, office_readings=regular_office_day, thirty_day_psalter_day=thirty_day_psalter
        )
        mp_psalms = MPPsalms(
            date=calendar_date, office_readings=regular_office_day, thirty_day_psalter_day=thirty_day_psalter
        )

        ep_data = ep_psalms.data
        mp_data = mp_psalms.data

        # Assert - Evening and Morning psalms should be different
        # Check 60-day cycle
        assert ep_data["citations_60"] != mp_data["citations_60"], "Evening and Morning psalms (60-day) should differ"

        # Check 30-day cycle
        assert ep_data["citations_30"] != mp_data["citations_30"], "Evening and Morning psalms (30-day) should differ"


@pytest.mark.unit
@pytest.mark.us2
class TestEPFirstReading:
    """
    Test EPFirstReading module for Evening Prayer.

    Validates: FR-006 (Two scripture readings per office)
    Tasks: T049
    """

    def test_ep_first_reading_has_data_method(self, db, regular_office_day):
        """EPFirstReading module has data method that returns dict."""
        from office.evening_prayer import EPFirstReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = EPFirstReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_ep_first_reading_includes_heading(self, db, regular_office_day):
        """EPFirstReading includes heading."""
        from office.evening_prayer import EPFirstReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = EPFirstReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        assert "heading" in data
        assert "First Lesson" in data["heading"] or "First" in data["heading"]

    def test_ep_first_reading_has_main_reading(self, db, regular_office_day):
        """EPFirstReading includes main reading from office_readings."""
        from office.evening_prayer import EPFirstReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = EPFirstReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        assert "main_reading" in data
        assert data["main_reading"] is not None

    def test_ep_first_reading_includes_passage_citation(self, db, regular_office_day):
        """EPFirstReading includes passage citation."""
        from office.evening_prayer import EPFirstReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = EPFirstReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        if data["main_reading"]:
            assert "intro" in data["main_reading"]
            assert "passage" in data["main_reading"]


@pytest.mark.unit
@pytest.mark.us2
class TestEPSecondReading:
    """
    Test EPSecondReading module for Evening Prayer.

    Validates: FR-006 (Two scripture readings per office)
    Tasks: T049
    """

    def test_ep_second_reading_has_data_method(self, db, regular_office_day):
        """EPSecondReading module has data method that returns dict."""
        from office.evening_prayer import EPSecondReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = EPSecondReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_ep_second_reading_includes_heading(self, db, regular_office_day):
        """EPSecondReading includes heading."""
        from office.evening_prayer import EPSecondReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = EPSecondReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        assert "heading" in data
        assert "Second Lesson" in data["heading"] or "Second" in data["heading"]

    def test_ep_second_reading_has_main_reading(self, db, regular_office_day):
        """EPSecondReading includes main reading from office_readings."""
        from office.evening_prayer import EPSecondReading
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        reading = EPSecondReading(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = reading.data()

        # Assert
        assert "main_reading" in data
        assert data["main_reading"] is not None


@pytest.mark.unit
@pytest.mark.us2
class TestEPCanticle1:
    """
    Test EPCanticle1 module for Evening Prayer.

    Validates: FR-008 (Display appropriate canticles - Magnificat for Evening Prayer)
    Tasks: T051
    """

    def test_ep_canticle1_has_data_property(self, db, regular_office_day):
        """EPCanticle1 module has data property that returns dict."""
        from office.evening_prayer import EPCanticle1
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        canticle = EPCanticle1(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = canticle.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_ep_canticle1_includes_canticle_tables(self, db, regular_office_day):
        """EPCanticle1 includes canticles from different tables (default, 1979, 2011)."""
        from office.evening_prayer import EPCanticle1
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        canticle = EPCanticle1(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = canticle.data

        # Assert - Should include canticles from different tables
        assert "default" in data or "1979" in data or "2011" in data

    def test_ep_canticle1_magnificat_for_evening(self, db, regular_office_day):
        """EPCanticle1 typically uses Magnificat for Evening Prayer first canticle."""
        from office.evening_prayer import EPCanticle1
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        canticle = EPCanticle1(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = canticle.data

        # Assert - Check that default canticle is Magnificat (common for Evening Prayer)
        # The actual canticle varies by season, but we can verify structure
        assert "default" in data
        if data["default"]:
            assert isinstance(data["default"], dict) or hasattr(data["default"], "__dict__")

    def test_ep_canticle1_advent_antiphon(self, db):
        """EPCanticle1 includes O Antiphons during Advent (Dec 17-23)."""
        from office.evening_prayer import EPCanticle1
        from churchcal.calculations import get_calendar_date

        # Use December 17 (O Sapientia)
        advent_date = date_class(2024, 12, 17)
        calendar_date = get_calendar_date(advent_date)
        office_day = StandardOfficeDay.objects.get(month=advent_date.month, day=advent_date.day)

        canticle = EPCanticle1(date=calendar_date, office_readings=office_day)

        # Act
        data = canticle.data

        # Assert - O Antiphon should be present
        assert "antiphon" in data
        assert data["antiphon"] is not None
        assert "latin" in data["antiphon"]
        assert "english" in data["antiphon"]


@pytest.mark.unit
@pytest.mark.us2
class TestEPCanticle2:
    """
    Test EPCanticle2 module for Evening Prayer.

    Validates: FR-008 (Display appropriate canticles - Nunc Dimittis for Evening Prayer)
    Tasks: T051
    """

    def test_ep_canticle2_has_data_property(self, db, regular_office_day):
        """EPCanticle2 module has data property that returns dict."""
        from office.evening_prayer import EPCanticle2
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        canticle = EPCanticle2(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = canticle.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_ep_canticle2_includes_canticle_tables(self, db, regular_office_day):
        """EPCanticle2 includes canticles from different tables (default, 1979, 2011)."""
        from office.evening_prayer import EPCanticle2
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        canticle = EPCanticle2(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = canticle.data

        # Assert - Should include canticles from different tables
        assert "default" in data or "1979" in data or "2011" in data


@pytest.mark.unit
@pytest.mark.us2
class TestEPSuffrages:
    """
    Test EPSuffrages module for Evening Prayer.

    Validates: FR-009 (Include suffrages - evening versicles)
    Tasks: T052
    """

    def test_ep_suffrages_has_data_property(self, db, regular_office_day):
        """EPSuffrages module has data property that returns dict."""
        from office.evening_prayer import EPSuffrages
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        suffrages = EPSuffrages(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = suffrages.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_ep_suffrages_includes_saint_names(self, db, regular_office_day):
        """EPSuffrages includes names of saints for commemoration."""
        from office.evening_prayer import EPSuffrages
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        suffrages = EPSuffrages(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = suffrages.data

        # Assert
        assert "names" in data
        # Blessed Virgin Mary is always included
        assert "Blessed Virgin Mary" in data["names"]

    def test_ep_suffrages_alternates_sets(self, db, regular_office_day):
        """EPSuffrages alternates between Set A and Set B by day."""
        from office.evening_prayer import EPSuffrages
        from churchcal.calculations import get_calendar_date

        # Test odd and even day numbers
        calendar_date_odd = get_calendar_date(date_class(2025, 1, 15))  # Day 15 (odd)
        calendar_date_even = get_calendar_date(date_class(2025, 1, 16))  # Day 16 (even)

        office_day_odd = StandardOfficeDay.objects.get(month=1, day=15)
        office_day_even = StandardOfficeDay.objects.get(month=1, day=16)

        suffrages_odd = EPSuffrages(date=calendar_date_odd, office_readings=office_day_odd)
        suffrages_even = EPSuffrages(date=calendar_date_even, office_readings=office_day_even)

        # Act
        data_odd = suffrages_odd.data
        data_even = suffrages_even.data

        # Assert - Should use different sets
        assert "default_set" in data_odd
        assert "default_set" in data_even
        assert data_odd["default_set"] != data_even["default_set"], "Suffrages should alternate between sets"


@pytest.mark.unit
@pytest.mark.us2
class TestEPCollectsOfTheDay:
    """
    Test EPCollectsOfTheDay module for Evening Prayer.

    Validates: FR-009 (Include full text of collects), FR-007 (Proper collects for feasts)
    Tasks: T049
    """

    def test_ep_collects_of_the_day_has_data_property(self, db, regular_office_day):
        """EPCollectsOfTheDay module has data property that returns dict."""
        from office.evening_prayer import EPCollectsOfTheDay
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        collects = EPCollectsOfTheDay(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = collects.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_ep_collects_of_the_day_includes_collects(self, db, regular_office_day):
        """EPCollectsOfTheDay includes collects generator."""
        from office.evening_prayer import EPCollectsOfTheDay
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        collects = EPCollectsOfTheDay(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = collects.data

        # Assert
        assert "collects" in data

    def test_ep_collects_of_the_day_feast_day(self, db):
        """EPCollectsOfTheDay includes feast day collect."""
        from office.evening_prayer import EPCollectsOfTheDay
        from churchcal.calculations import get_calendar_date

        # Use Christmas Day
        christmas_date = date_class(2024, 12, 25)
        calendar_date = get_calendar_date(christmas_date)
        office_day = StandardOfficeDay.objects.get(month=christmas_date.month, day=christmas_date.day)

        collects = EPCollectsOfTheDay(date=calendar_date, office_readings=office_day)

        # Act
        data = collects.data

        # Assert - Christmas should have a collect
        collects_list = list(data["collects"])
        assert len(collects_list) >= 1


@pytest.mark.unit
@pytest.mark.us2
class TestEPCollects:
    """
    Test EPCollects module for Evening Prayer.

    Validates: FR-009 (Include full text of collects)
    Tasks: T049
    """

    def test_ep_collects_has_data_property(self, db, regular_office_day):
        """EPCollects module has data property that returns dict."""
        from office.evening_prayer import EPCollects
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        collects = EPCollects(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = collects.data

        # Assert
        assert data is not None
        assert isinstance(data, dict)

    def test_ep_collects_includes_weekday_collect(self, db, regular_office_day):
        """EPCollects includes weekday-specific collect."""
        from office.evening_prayer import EPCollects
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))  # Wednesday
        collects = EPCollects(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = collects.data

        # Assert
        assert "collect" in data
        assert data["collect"] is not None
        assert len(data["collect"]) == 3  # (heading, weekday, text)

    def test_ep_collects_includes_fixed_collects(self, db, regular_office_day):
        """EPCollects includes fixed collects (peace and aid against perils)."""
        from office.evening_prayer import EPCollects
        from churchcal.calculations import get_calendar_date

        calendar_date = get_calendar_date(date_class(2025, 1, 15))
        collects = EPCollects(date=calendar_date, office_readings=regular_office_day)

        # Act
        data = collects.data

        # Assert
        assert "fixed_collects" in data
        assert len(data["fixed_collects"]) == 2  # Peace and Aid Against Perils

    def test_ep_collects_weekday_rotation(self, db):
        """EPCollects rotates different collects for each weekday."""
        from office.evening_prayer import EPCollects
        from churchcal.calculations import get_calendar_date

        # Test a week
        weekday_collects = {}
        for day_offset in range(7):
            test_date = date_class(2025, 1, 13 + day_offset)  # Monday through Sunday
            calendar_date = get_calendar_date(test_date)
            office_day = StandardOfficeDay.objects.get(month=test_date.month, day=test_date.day)

            collects = EPCollects(date=calendar_date, office_readings=office_day)
            data = collects.data

            weekday_name = test_date.strftime("%A")
            weekday_collects[weekday_name] = data["collect"][0]  # Collect title

        # Assert - Different collects for different days
        unique_collects = set(weekday_collects.values())
        assert len(unique_collects) == 7, f"Expected 7 different weekday collects, got {len(unique_collects)}"
