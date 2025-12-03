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
    SeasonFactory,
    CommemorationRankFactory,
    SanctoraleCommemorationFactory,
    ThirtyDayPsalterDayFactory,
)
from churchcal.models import Calendar, Denomination


@pytest.fixture(autouse=True)
def acna_calendar(db):
    """
    Create ACNA 2019 calendar for testing.

    Returns the ACNA_BCP2019 calendar created via factories.
    Uses get_or_create to ensure calendar exists without duplicates.
    """
    from churchcal.models import Calendar, Denomination

    # Create or get ACNA denomination
    denomination, _ = Denomination.objects.get_or_create(
        abbreviation="ACNA", defaults={"name": "Anglican Church in North America"}
    )

    # Create or get ACNA BCP 2019 calendar
    calendar, _ = Calendar.objects.get_or_create(
        abbreviation="ACNA_BCP2019",
        defaults={
            "name": "ACNA Book of Common Prayer 2019",
            "denomination": denomination,
            "year": "2019",
        },
    )

    # Create Ranks
    principal_feast = CommemorationRankFactory(
        name="PRINCIPAL_FEAST", formatted_name="Principal Feast", precedence_rank=1, calendar=calendar
    )

    # Create Epiphany Commemoration (needed for Jan 15 season)
    epiphany_day = SanctoraleCommemorationFactory(
        name="The Epiphany", month=1, day=6, rank=principal_feast, calendar=calendar, color="White"
    )

    # Create Epiphany Season
    SeasonFactory(
        name="Epiphany",
        order=2,
        color="White",
        start_commemoration=epiphany_day,
        rank=principal_feast,
        calendar=calendar,
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
def regular_office_day(db, acna_calendar):
    """Regular feria office day (January 15)."""
    # Create psalter cycle (required for office generation)
    create_psalter_cycle()
    return create_regular_office_day(month=1, day=15)


@pytest.fixture
def compline_office_data(db, acna_calendar):
    """
    Ensure StandardOfficeDay and Psalter data exist for Compline tests.

    Compline tests exercise specific calendar dates (mostly in January 2024 plus
    Holy Days) that require both OfficeDay readings and thirty-day psalter data.
    The production dump isn't available in CI, so we seed just the required rows.
    """
    from office.tests.factories import (
        CalendarFactory,
        DenominationFactory,
        SanctoraleCommemorationFactory,
        TemporaleCommemorationFactory,
        CommemorationRankFactory,
        SeasonFactory,
    )
    from churchcal.models import (
        Calendar,
        Denomination,
        CommemorationRank,
        Season,
        SanctoraleCommemoration,
        TemporaleCommemoration,
    )

    compline_dates = {
        (1, 15),
        (1, 16),
        (1, 17),
        (1, 18),
        (1, 20),
        (1, 21),
        (1, 31),  # Month boundary test
        (12, 31),  # Year boundary test
        (2, 14),
        (3, 15),
        (3, 31),
        (4, 15),
        (12, 15),
        (12, 25),
    }

    # Ensure complete psalter coverage (days 1-31)
    create_psalter_cycle()
    ThirtyDayPsalterDayFactory.create(day=31)

    # Create Compline psalms with verses (required for psalm rendering)
    create_psalms_with_verses([4, 31, 91, 134])

    # acna_calendar is passed in via fixture

    # Create commemoration rank for holy days
    holy_day_rank, _ = CommemorationRank.objects.get_or_create(
        name="PRINCIPAL_FEAST",
        calendar=acna_calendar,
        defaults={
            "formatted_name": "Principal Feast",
            "precedence_rank": 1,
            "required": True,
        },
    )

    # Create a ferial rank for ordinary days
    ferial_rank, _ = CommemorationRank.objects.get_or_create(
        name="FERIA",
        calendar=acna_calendar,
        defaults={
            "formatted_name": "Ferial Day",
            "precedence_rank": 99,
            "required": False,
        },
    )

    # Create seasons (required for ferial commemorations)
    # Christmastide covers Dec 25 - Jan 6
    christmastide, _ = Season.objects.get_or_create(
        name="Christmastide",
        calendar=acna_calendar,
        defaults={
            "order": 4,
            "color": "White",
            "rank": ferial_rank,
        },
    )

    # Season after Epiphany covers most of January-February
    epiphany_season, _ = Season.objects.get_or_create(
        name="Season After Epiphany",
        calendar=acna_calendar,
        defaults={
            "order": 5,
            "color": "Green",
            "rank": ferial_rank,
        },
    )

    # Lent season (starts on Ash Wednesday)
    lent_season, _ = Season.objects.get_or_create(
        name="Lent",
        calendar=acna_calendar,
        defaults={
            "order": 6,
            "color": "Purple",
            "rank": ferial_rank,
        },
    )

    # Eastertide season (starts on Easter Day)
    eastertide, _ = Season.objects.get_or_create(
        name="Eastertide",
        calendar=acna_calendar,
        defaults={
            "order": 8,
            "color": "White",
            "rank": ferial_rank,
        },
    )

    # Seed StandardOfficeDay entries for every date Compline tests touch
    for month, day in compline_dates:
        StandardOfficeDayFactory.create(month=month, day=day)

    # Create Epiphany commemoration (starts the Epiphany season)
    epiphany, _ = SanctoraleCommemoration.objects.get_or_create(
        name="The Epiphany",
        calendar=acna_calendar,
        defaults={
            "month": 1,
            "day": 6,
            "color": "White",
            "rank": holy_day_rank,
        },
    )
    epiphany_season.start_commemoration = epiphany
    epiphany_season.save()

    # Create Ash Wednesday commemoration (starts Lent)
    # Ash Wednesday 2024 is February 14
    ash_wednesday, _ = TemporaleCommemoration.objects.get_or_create(
        name="Ash Wednesday",
        calendar=acna_calendar,
        defaults={
            "days_after_easter": -46,  # 46 days before Easter
            "color": "Purple",
            "rank": holy_day_rank,
        },
    )
    lent_season.start_commemoration = ash_wednesday
    lent_season.save()

    # Create Easter Day commemoration (starts Eastertide)
    # Easter 2024 is March 31
    easter, _ = TemporaleCommemoration.objects.get_or_create(
        name="Easter Day",
        calendar=acna_calendar,
        defaults={
            "days_after_easter": 0,
            "color": "White",
            "rank": holy_day_rank,
        },
    )
    eastertide.start_commemoration = easter
    eastertide.save()

    # Create Christmas Day commemoration for feast day test
    christmas, _ = SanctoraleCommemoration.objects.get_or_create(
        name="The Nativity of Our Lord Jesus Christ (Christmas Day)",
        calendar=acna_calendar,
        defaults={
            "month": 12,
            "day": 25,
            "color": "White",
            "rank": holy_day_rank,
        },
    )
    christmastide.start_commemoration = christmas
    christmastide.save()


@pytest.fixture
def summer_office_day(db, acna_calendar):
    """Summer office day (July 20)."""
    # Create psalter cycle (required for office generation)
    create_psalter_cycle()
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
    return [StandardOfficeDayFactory.create(month=1, day=i) for i in range(1, 8)]


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
