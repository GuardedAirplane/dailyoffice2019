"""
Coverage tests for office/family_midday.py.

Targets uncovered lines to improve coverage from 62% to 90%+.
Focus: FNOpeningSentence, FNScripture rotation, FPCollect weekday logic.

Uncovered lines: 58, 69, 79, 85, 90, 97-111, 115, 126, 132, 137-157, 161-164
"""

import pytest
from datetime import date
from freezegun import freeze_time

from office.family_midday import (
    FamilyMidday,
    FNHeading,
    FNOpeningSentence,
    FNPsalms,
    FNScripture,
    FNIntercessions,
    Pater,
    FPCollect,
)


@pytest.mark.django_db
class TestFNHeadingData:
    """Test FNHeading.data property - covers line 58"""

    @freeze_time("2024-10-15")
    def test_heading_data_structure(self):
        """FNHeading.data returns heading, rubric, calendar_date - covers line 58"""
        fm = FamilyMidday(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FNHeading":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "rubric" in data
                assert "calendar_date" in data
                break


@pytest.mark.django_db
class TestFNOpeningSentenceVariations:
    """Test FNOpeningSentence sentence variations - covers lines 69, 79"""

    @freeze_time("2024-10-15")
    def test_opening_sentence_get_sentences(self):
        """FNOpeningSentence.get_sentences returns seasonal and fixed - covers line 69"""
        fm = FamilyMidday(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FNOpeningSentence":
                sentences = module[0].get_sentences()
                assert sentences is not None
                assert "seasonal" in sentences
                assert "fixed" in sentences
                break

    @freeze_time("2024-10-15")
    def test_opening_sentence_data(self):
        """FNOpeningSentence.data returns heading and sentences - covers line 79"""
        fm = FamilyMidday(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FNOpeningSentence":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "sentences" in data
                break


@pytest.mark.django_db
class TestFNPsalmsData:
    """Test FNPsalms.data property - covers line 85"""

    @freeze_time("2024-10-15")
    def test_psalms_data_structure(self):
        """FNPsalms.data returns heading and psalms - covers line 85"""
        fm = FamilyMidday(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FNPsalms":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "psalms" in data
                break


@pytest.mark.django_db
class TestFNScriptureRotation:
    """Test FNScripture day-of-year rotation - covers lines 90, 97-111, 115"""

    @freeze_time("2024-01-01")  # Day 1 of year, 1 % 2 = 1
    def test_scripture_rotation_odd_day(self):
        """Odd day of year uses Philippians 4:6-7 - covers lines 97-111"""
        fm = FamilyMidday(date=date(2024, 1, 1))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FNScripture":
                scripture = module[0].get_scripture()
                assert scripture is not None
                assert "citation" in scripture
                # Day 1: 1 % 2 = 1, so index [1] = Philippians
                assert "PHILIPPIANS" in scripture["citation"]
                break

    @freeze_time("2024-01-02")  # Day 2 of year, 2 % 2 = 0
    def test_scripture_rotation_even_day(self):
        """Even day of year uses John 15:4-5 - covers lines 97-111"""
        fm = FamilyMidday(date=date(2024, 1, 2))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FNScripture":
                scripture = module[0].get_scripture()
                assert scripture is not None
                assert "citation" in scripture
                # Day 2: 2 % 2 = 0, so index [0] = John
                assert "JOHN" in scripture["citation"]
                break

    @freeze_time("2024-06-15")
    def test_scripture_get_long_reading(self):
        """FNScripture.get_long returns mp_reading_2 - covers line 90"""
        fm = FamilyMidday(date=date(2024, 6, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FNScripture":
                long_reading = module[0].get_long()
                assert long_reading is not None
                assert "passage" in long_reading
                assert "text" in long_reading
                assert "deuterocanon" in long_reading
                break

    @freeze_time("2024-10-15")
    def test_scripture_data_structure(self):
        """FNScripture.data returns heading, long, brief - covers line 115"""
        fm = FamilyMidday(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FNScripture":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "long" in data
                assert "brief" in data
                assert "hide_closing" in data
                break


@pytest.mark.django_db
class TestFNIntercessionsData:
    """Test FNIntercessions.data property - covers line 126"""

    @freeze_time("2024-10-15")
    def test_intercessions_data_structure(self):
        """FNIntercessions.data returns title and rubric - covers line 126"""
        fm = FamilyMidday(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FNIntercessions":
                data = module[0].data
                assert data is not None
                assert "title" in data
                assert "rubric" in data
                break


@pytest.mark.django_db
class TestPaterData:
    """Test Pater (Lord's Prayer).data property - covers line 132"""

    @freeze_time("2024-10-15")
    def test_pater_data_structure(self):
        """Pater.data returns heading - covers line 132"""
        fm = FamilyMidday(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "Pater":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                break


@pytest.mark.django_db
class TestFPCollectWeekdayRotation:
    """Test FPCollect weekday rotation logic - covers lines 137-157, 161-164"""

    @freeze_time("2024-10-13")  # Sunday
    def test_collect_sunday(self):
        """Sunday uses collect[1] - covers lines 141-142"""
        fm = FamilyMidday(date=date(2024, 10, 13))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FPCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3  # (None, None, collect_text)
                break

    @freeze_time("2024-10-14")  # Monday
    def test_collect_monday(self):
        """Monday uses collect[2] - covers lines 144-145"""
        fm = FamilyMidday(date=date(2024, 10, 14))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FPCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                break

    @freeze_time("2024-10-15")  # Tuesday
    def test_collect_tuesday(self):
        """Tuesday uses collect[3] - covers lines 147-148"""
        fm = FamilyMidday(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FPCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                break

    @freeze_time("2024-10-16")  # Wednesday
    def test_collect_wednesday(self):
        """Wednesday uses collect[0] - covers lines 150-151"""
        fm = FamilyMidday(date=date(2024, 10, 16))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FPCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                break

    @freeze_time("2024-10-17")  # Thursday
    def test_collect_thursday(self):
        """Thursday uses collect[1] - covers lines 153-154"""
        fm = FamilyMidday(date=date(2024, 10, 17))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FPCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                break

    @freeze_time("2024-10-18")  # Friday
    def test_collect_friday(self):
        """Friday uses collect[0] - covers lines 156-157"""
        fm = FamilyMidday(date=date(2024, 10, 18))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FPCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                break

    @freeze_time("2024-10-19")  # Saturday
    def test_collect_saturday(self):
        """Saturday uses collect[2] - covers lines 144-145"""
        fm = FamilyMidday(date=date(2024, 10, 19))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FPCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                break

    @freeze_time("2024-10-15")
    def test_collect_data_structure(self):
        """FPCollect.data returns all collect types - covers lines 161-164"""
        fm = FamilyMidday(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FPCollect":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "time_of_day" in data
                assert "day_of_year" in data
                assert "day_of_week" in data
                break
