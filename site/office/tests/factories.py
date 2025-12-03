"""
Test factories for Daily Office models using factory_boy.

Implements test infrastructure for Constitution Principle III.
Creates realistic test data for office generation testing.
"""

import factory
from datetime import date, timedelta
from factory.django import DjangoModelFactory
from office.models import (
    StandardOfficeDay,
    HolyDayOfficeDay,
    ThirtyDayPsalterDay,
    Scripture,
    Setting,
    SettingOption,
    Collect,
)
from churchcal.models import (
    SanctoraleCommemoration,
    TemporaleCommemoration,
    CommemorationRank,
    Season,
    Calendar,
    Denomination,
)
from psalter.models import Psalm, PsalmVerse


# Calendar and Denomination Factories


class DenominationFactory(DjangoModelFactory):
    """Factory for Denomination model."""

    class Meta:
        model = Denomination
        django_get_or_create = ("abbreviation",)

    name = "Anglican Church in North America"
    abbreviation = "ACNA"


class CalendarFactory(DjangoModelFactory):
    """Factory for Calendar model."""

    class Meta:
        model = Calendar
        django_get_or_create = ("abbreviation", "year")

    name = "ACNA Calendar 2019"
    denomination = factory.SubFactory(DenominationFactory)
    year = "2019"
    abbreviation = "ACNA2019"


class CommemorationRankFactory(DjangoModelFactory):
    """Factory for CommemorationRank model."""

    class Meta:
        model = CommemorationRank
        django_get_or_create = ("name", "calendar")

    name = "HOLY_DAY"
    formatted_name = "Holy Day"
    precedence_rank = 3
    required = True
    calendar = factory.SubFactory(CalendarFactory)


# Commemoration Factories


class SanctoraleCommemorationFactory(DjangoModelFactory):
    """Factory for SanctoraleCommemoration (fixed-date feasts)."""

    class Meta:
        model = SanctoraleCommemoration
        django_get_or_create = ("name", "month", "day", "calendar")

    name = factory.Sequence(lambda n: f"Saint Test {n}")
    month = 12
    day = 25
    rank = factory.SubFactory(CommemorationRankFactory)
    color = "White"
    calendar = factory.SubFactory(CalendarFactory)


class TemporaleCommemorationFactory(DjangoModelFactory):
    """Factory for TemporaleCommemoration (Easter-relative feasts)."""

    class Meta:
        model = TemporaleCommemoration
        django_get_or_create = ("name", "days_after_easter", "calendar")

    name = "Easter Day"
    days_after_easter = 0
    rank = factory.SubFactory(CommemorationRankFactory)
    color = "White"
    calendar = factory.SubFactory(CalendarFactory)


class SeasonFactory(DjangoModelFactory):
    """Factory for Season model."""

    class Meta:
        model = Season
        django_get_or_create = ("name", "calendar")

    order = 1
    name = "Advent"
    color = "Purple"
    rank = factory.SubFactory(CommemorationRankFactory)
    calendar = factory.SubFactory(CalendarFactory)


# Office Day Factories


class StandardOfficeDayFactory(DjangoModelFactory):
    """Factory for StandardOfficeDay (regular daily readings)."""

    class Meta:
        model = StandardOfficeDay
        django_get_or_create = ("month", "day")

    month = 1
    day = 1
    mp_psalms = "1,2,3"
    mp_reading_1 = "Genesis 1:1-5"
    mp_reading_1_testament = "OT"
    mp_reading_2 = "Matthew 1:1-17"
    mp_reading_2_testament = "NT"
    ep_psalms = "4,5,6"
    ep_reading_1 = "Genesis 1:6-13"
    ep_reading_1_testament = "OT"
    ep_reading_2 = "Matthew 1:18-25"
    ep_reading_2_testament = "NT"


class HolyDayOfficeDayFactory(DjangoModelFactory):
    """Factory for HolyDayOfficeDay (feast day readings)."""

    class Meta:
        model = HolyDayOfficeDay

    commemoration = factory.SubFactory(SanctoraleCommemorationFactory)
    order = 1
    mp_psalms = "19,67"
    mp_reading_1 = "Isaiah 9:2-7"
    mp_reading_1_testament = "OT"
    mp_reading_2 = "Luke 2:1-20"
    mp_reading_2_testament = "NT"
    ep_psalms = "89,110"
    ep_reading_1 = "Isaiah 7:10-14"
    ep_reading_1_testament = "OT"
    ep_reading_2 = "Luke 1:26-38"
    ep_reading_2_testament = "NT"


class ThirtyDayPsalterDayFactory(DjangoModelFactory):
    """Factory for ThirtyDayPsalterDay."""

    class Meta:
        model = ThirtyDayPsalterDay
        django_get_or_create = ("day",)

    day = factory.Sequence(lambda n: (n % 30) + 1)
    mp_psalms = factory.LazyAttribute(lambda obj: f"{obj.day},{obj.day+1}")
    ep_psalms = factory.LazyAttribute(lambda obj: f"{obj.day+30},{obj.day+31}")


# Scripture Cache Factory


class ScriptureFactory(DjangoModelFactory):
    """Factory for Scripture model (Bible passage cache)."""

    class Meta:
        model = Scripture
        django_get_or_create = ("passage",)

    passage = "John 3:16"
    esv = "<p>For God so loved the world...</p>"
    kjv = "<p>For God so loved the world...</p>"
    nrsvce = "<p>For God so loved the world...</p>"


# Settings Factories


class SettingFactory(DjangoModelFactory):
    """Factory for Setting model."""

    class Meta:
        model = Setting
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: f"test_setting_{n}")
    title = factory.LazyAttribute(lambda obj: obj.name.replace("_", " ").title())
    description = "Test setting description"
    order = 1
    setting_type = 1  # MAIN_SETTINGS
    site = 1  # DAILY_OFFICE_SITE


class SettingOptionFactory(DjangoModelFactory):
    """Factory for SettingOption model."""

    class Meta:
        model = SettingOption

    setting = factory.SubFactory(SettingFactory)
    order = 1
    name = "Test Option"
    description = "Test option description"
    value = "test_value"
    abbreviation = "T"


# Collect Factory


class CollectFactory(DjangoModelFactory):
    """Factory for Collect model."""

    class Meta:
        model = Collect

    title = factory.Sequence(lambda n: f"Test Collect {n}")
    text = "<p>Almighty God, grant us grace...</p>"
    normalized_text = "Almighty God, grant us grace..."
    traditional_text = "<p>Almighty God, who grantest us grace...</p>"
    order = 1


# Psalm Factories


class PsalmFactory(DjangoModelFactory):
    """Factory for Psalm model."""

    class Meta:
        model = Psalm
        django_get_or_create = ("number",)

    number = factory.Sequence(lambda n: n + 1)
    latin_title = factory.LazyAttribute(lambda obj: f"Psalm {obj.number}")


class PsalmVerseFactory(DjangoModelFactory):
    """Factory for PsalmVerse model."""

    class Meta:
        model = PsalmVerse
        django_get_or_create = ("psalm", "number")

    psalm = factory.SubFactory(PsalmFactory)
    number = factory.Sequence(lambda n: n + 1)
    first_half = "The Lord is my shepherd"
    second_half = "I shall not want"
    first_half_tle = "The Lord is my shepherd"
    second_half_tle = "I shall not want"


# Convenience functions for common test scenarios


def create_christmas_office_day():
    """Create complete Christmas Day office day with feast readings."""
    christmas = SanctoraleCommemorationFactory(
        name="The Nativity of Our Lord Jesus Christ (Christmas Day)",
        month=12,
        day=25,
        color="White",
    )

    return HolyDayOfficeDayFactory(
        commemoration=christmas,
        mp_psalms="19,45",
        mp_reading_1="Isaiah 9:2-7",
        mp_reading_2="Luke 2:1-20",
        ep_psalms="89,110",
        ep_reading_1="Isaiah 7:10-14",
        ep_reading_2="Luke 1:26-38",
    )


def create_easter_office_day():
    """Create complete Easter Day office day."""
    easter = TemporaleCommemorationFactory(
        name="Easter Day",
        days_after_easter=0,
        color="White",
    )

    return HolyDayOfficeDayFactory(
        commemoration=easter,
        mp_psalms="113,114",
        mp_reading_1="Isaiah 51:9-11",
        mp_reading_2="Luke 24:1-12",
        ep_psalms="136,117",
        ep_reading_1="Daniel 6:1-24",
        ep_reading_2="Luke 24:13-35",
    )


def create_regular_office_day(month=1, day=15):
    """Create standard office day for regular feria."""
    return StandardOfficeDayFactory(month=month, day=day)


def create_psalter_cycle():
    """Create complete 30-day Psalter cycle."""
    return [ThirtyDayPsalterDayFactory.create(day=i) for i in range(1, 31)]


def create_psalms_with_verses(psalm_numbers):
    """Create specified psalms with sample verses."""
    psalms = []
    for num in psalm_numbers:
        psalm = PsalmFactory.create(number=num)
        # Create 5 sample verses for each psalm
        for verse_num in range(1, 6):
            PsalmVerseFactory.create(psalm=psalm, number=verse_num)
        psalms.append(psalm)
    return psalms


def create_complete_settings():
    """Create common liturgical settings with options."""
    # Psalter setting
    psalter = SettingFactory.create(name="psalter", title="Psalter Cycle")
    SettingOptionFactory.create(setting=psalter, name="30-Day Cycle", value="30day", abbreviation="3")
    SettingOptionFactory.create(setting=psalter, name="60-Day Cycle", value="60day", abbreviation="6")

    # Lectionary setting
    lectionary = SettingFactory.create(name="lectionary", title="Lectionary Cycle")
    SettingOptionFactory.create(setting=lectionary, name="1-Year Cycle", value="1year", abbreviation="1")
    SettingOptionFactory.create(setting=lectionary, name="2-Year Cycle", value="2year", abbreviation="2")

    # Bible version setting
    bible = SettingFactory.create(name="bible_version", title="Bible Translation")
    SettingOptionFactory.create(setting=bible, name="ESV", value="esv", abbreviation="E")
    SettingOptionFactory.create(setting=bible, name="NRSVCE", value="nrsvce", abbreviation="N")
    SettingOptionFactory.create(setting=bible, name="KJV", value="kjv", abbreviation="K")

    return {
        "psalter": psalter,
        "lectionary": lectionary,
        "bible_version": bible,
    }
