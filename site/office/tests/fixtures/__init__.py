"""
Test fixtures for common liturgical scenarios.

Provides pytest fixtures for frequently-used test data:
- Christmas Day office
- Easter Day office
- Regular feria
- Complete Psalter cycle
- Settings configurations

Implements: Test Infrastructure (Phase 2)
"""

import pytest
from datetime import date
from freezegun import freeze_time
from office.tests.factories import (
    create_christmas_office_day,
    create_easter_office_day,
    create_regular_office_day,
    create_psalter_cycle,
    create_psalms_with_verses,
    create_complete_settings,
    StandardOfficeDayFactory,
    HolyDayOfficeDayFactory,
    ScriptureFactory,
)
from churchcal.models import Calendar, Denomination


@pytest.fixture
def acna_calendar(db):
    """
    Create ACNA 2019 calendar for testing.
    
    Returns the ACNA_BCP2019 calendar created via factories.
    Uses get_or_create to ensure calendar exists without duplicates.
    """
    from churchcal.models import Calendar, Denomination
    
    # Create or get ACNA denomination
    denomination, _ = Denomination.objects.get_or_create(
        abbreviation="ACNA",
        defaults={"name": "Anglican Church in North America"}
    )
    
    # Create or get ACNA BCP 2019 calendar
    calendar, _ = Calendar.objects.get_or_create(
        abbreviation="ACNA_BCP2019",
        defaults={
            "name": "ACNA Book of Common Prayer 2019",
            "denomination": denomination,
            "year": "2019",
        }
    )
    
    return calendar


@pytest.fixture
def christmas_office_day(db, acna_calendar):
    """Christmas Day office readings (December 25)."""
    return create_christmas_office_day()


@pytest.fixture
def easter_office_day(db, acna_calendar):
    """Easter Day office readings (movable feast)."""
    return create_easter_office_day()


@pytest.fixture
def regular_office_day(db):
    """Regular feria office day (January 15)."""
    return create_regular_office_day(month=1, day=15)


@pytest.fixture
def summer_office_day(db):
    """Summer office day (July 20)."""
    return create_regular_office_day(month=7, day=20)


@pytest.fixture
def psalter_cycle(db):
    """Complete 30-day Psalter cycle."""
    return create_psalter_cycle()


@pytest.fixture
def morning_prayer_psalms(db):
    """Common Morning Prayer psalms (1, 2, 3, 5, 95) with verses."""
    return create_psalms_with_verses([1, 2, 3, 5, 95])


@pytest.fixture
def evening_prayer_psalms(db):
    """Common Evening Prayer psalms (4, 8, 134, 141) with verses."""
    return create_psalms_with_verses([4, 8, 134, 141])


@pytest.fixture
def compline_psalms(db):
    """Compline psalms (4, 31, 91, 134) with verses."""
    return create_psalms_with_verses([4, 31, 91, 134])


@pytest.fixture
def complete_settings(db):
    """Standard liturgical settings (psalter, lectionary, bible version)."""
    return create_complete_settings()


@pytest.fixture
def cached_scripture(db):
    """Pre-cached scripture passages for common readings."""
    passages = {
        "Genesis 1:1-5": "In the beginning God created the heavens and the earth...",
        "Matthew 1:1-17": "The book of the genealogy of Jesus Christ...",
        "John 3:16": "For God so loved the world...",
        "Psalm 23": "The Lord is my shepherd...",
        "Isaiah 9:2-7": "The people who walked in darkness...",
        "Luke 2:1-20": "In those days a decree went out...",
    }

    return {
        passage: ScriptureFactory.create(
            passage=passage,
            esv=f"<p>{text}</p>",
            kjv=f"<p>{text}</p>",
            nrsvce=f"<p>{text}</p>",
        )
        for passage, text in passages.items()
    }


@pytest.fixture
def frozen_christmas(db):
    """Freeze time to Christmas Day 2025."""
    with freeze_time("2025-12-25"):
        yield date(2025, 12, 25)


@pytest.fixture
def frozen_easter(db):
    """Freeze time to Easter Day 2025 (April 20)."""
    with freeze_time("2025-04-20"):
        yield date(2025, 4, 20)


@pytest.fixture
def frozen_january(db):
    """Freeze time to January 15, 2025."""
    with freeze_time("2025-01-15"):
        yield date(2025, 1, 15)


@pytest.fixture
def office_day_sequence(db):
    """Create sequence of 7 consecutive office days (week of readings)."""
    return [
        StandardOfficeDayFactory.create(month=1, day=i)
        for i in range(1, 8)
    ]


@pytest.fixture
def major_feasts(db, acna_calendar):
    """Create all major BCP 2019 feast days."""
    from office.tests.factories import (
        SanctoraleCommemorationFactory,
        TemporaleCommemorationFactory,
    )

    feasts = {
        "christmas": SanctoraleCommemorationFactory.create(
            name="The Nativity of Our Lord Jesus Christ",
            month=12,
            day=25,
            color="White",
            calendar=acna_calendar,
        ),
        "epiphany": SanctoraleCommemorationFactory.create(
            name="The Epiphany",
            month=1,
            day=6,
            color="White",
            calendar=acna_calendar,
        ),
        "easter": TemporaleCommemorationFactory.create(
            name="Easter Day",
            days_after_easter=0,
            color="White",
            calendar=acna_calendar,
        ),
        "ascension": TemporaleCommemorationFactory.create(
            name="Ascension Day",
            days_after_easter=39,
            color="White",
            calendar=acna_calendar,
        ),
        "pentecost": TemporaleCommemorationFactory.create(
            name="The Day of Pentecost",
            days_after_easter=49,
            color="Red",
            calendar=acna_calendar,
        ),
        "ash_wednesday": TemporaleCommemorationFactory.create(
            name="Ash Wednesday",
            days_after_easter=-46,
            color="Purple",
            calendar=acna_calendar,
        ),
        "palm_sunday": TemporaleCommemorationFactory.create(
            name="Palm Sunday",
            days_after_easter=-7,
            color="Red",
            calendar=acna_calendar,
        ),
        "good_friday": TemporaleCommemorationFactory.create(
            name="Good Friday",
            days_after_easter=-2,
            color="Red",
            calendar=acna_calendar,
        ),
        "all_saints": SanctoraleCommemorationFactory.create(
            name="All Saints' Day",
            month=11,
            day=1,
            color="White",
            calendar=acna_calendar,
        ),
        "trinity_sunday": TemporaleCommemorationFactory.create(
            name="Trinity Sunday",
            days_after_easter=56,
            color="White",
            calendar=acna_calendar,
        ),
    }

    return feasts


@pytest.fixture
def liturgical_settings_defaults():
    """Default setting values for liturgical customization."""
    return {
        "psalter": "60day",
        "lectionary": "1year",
        "bible_version": "esv",
        "canticle_rotation": "traditional",
        "canticle_table": "bcp2019",
        "confession_length": "long",
        "absolution_style": "priest",
        "invitatory": "venite",
        "opening_sentence": "seasonal",
    }
