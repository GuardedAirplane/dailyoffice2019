"""
Coverage tests for office/family_morning.py.

Targets uncovered lines to improve coverage from 75% to 100%.
Focus: FMOpeningSentence, FMScripture rotation (3-day cycle), FMCollect.

Uncovered lines: 57, 62, 72, 78, 83, 98-116, 120, 131, 142, 148-151
"""

import pytest
from datetime import date
from freezegun import freeze_time

from office.family_morning import (
    FamilyMorning,
    FMHeading,
    FMOpeningSentence,
    FMPsalms,
    FMScripture,
    FMIntercessions,
    Pater,
    FMCollect,
)


@pytest.mark.django_db
class TestFMHeadingData:
    """Test FMHeading.data property - covers line 57"""

    @freeze_time("2024-10-15")
    def test_heading_data_structure(self):
        """FMHeading.data returns heading and calendar_date - covers line 57"""
        fm = FamilyMorning(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FMHeading":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "calendar_date" in data
                break


@pytest.mark.django_db
class TestFMOpeningSentenceVariations:
    """Test FMOpeningSentence sentence variations - covers lines 62, 72"""

    @freeze_time("2024-10-15")
    def test_opening_sentence_get_sentences(self):
        """FMOpeningSentence.get_sentences returns seasonal and fixed - covers line 62"""
        fm = FamilyMorning(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FMOpeningSentence":
                sentences = module[0].get_sentences()
                assert sentences is not None
                assert "seasonal" in sentences
                assert "fixed" in sentences
                assert "PSALM 51:15" in sentences["fixed"]["citation"]
                break

    @freeze_time("2024-10-15")
    def test_opening_sentence_data(self):
        """FMOpeningSentence.data returns heading and sentences - covers line 72"""
        fm = FamilyMorning(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FMOpeningSentence":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "sentences" in data
                break


@pytest.mark.django_db
class TestFMPsalmsData:
    """Test FMPsalms.data property - covers line 78"""

    @freeze_time("2024-10-15")
    def test_psalms_data_structure(self):
        """FMPsalms.data returns heading and psalms (51:10-12) - covers line 78"""
        fm = FamilyMorning(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FMPsalms":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "psalms" in data
                break


@pytest.mark.django_db
class TestFMScriptureRotation:
    """Test FMScripture 3-day rotation - covers lines 83, 98-116, 120"""

    @freeze_time("2024-01-01")  # Day 1 of year, 1 % 3 = 1
    def test_scripture_rotation_day_1_mod_3(self):
        """Day 1: 1 % 3 = 1 uses Colossians 1:12-14 - covers lines 98-116"""
        fm = FamilyMorning(date=date(2024, 1, 1))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FMScripture":
                scripture = module[0].get_scripture()
                assert scripture is not None
                assert "citation" in scripture
                # Index [1] = Colossians 1:12-14
                assert "COLOSSIANS 1:12-14" in scripture["citation"]
                break

    @freeze_time("2024-01-02")  # Day 2 of year, 2 % 3 = 2
    def test_scripture_rotation_day_2_mod_3(self):
        """Day 2: 2 % 3 = 2 uses Colossians 3:1-4 - covers lines 98-116"""
        fm = FamilyMorning(date=date(2024, 1, 2))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FMScripture":
                scripture = module[0].get_scripture()
                assert scripture is not None
                assert "citation" in scripture
                # Index [2] = Colossians 3:1-4
                assert "COLOSSIANS 3:1-4" in scripture["citation"]
                break

    @freeze_time("2024-01-03")  # Day 3 of year, 3 % 3 = 0
    def test_scripture_rotation_day_0_mod_3(self):
        """Day 3: 3 % 3 = 0 uses 1 Peter 1:3 - covers lines 98-116"""
        fm = FamilyMorning(date=date(2024, 1, 3))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FMScripture":
                scripture = module[0].get_scripture()
                assert scripture is not None
                assert "citation" in scripture
                # Index [0] = 1 Peter
                assert "1 PETER" in scripture["citation"]
                break

    @freeze_time("2024-06-15")
    def test_scripture_get_long_reading(self):
        """FMScripture.get_long returns mp_reading_1 - covers line 83"""
        fm = FamilyMorning(date=date(2024, 6, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FMScripture":
                long_reading = module[0].get_long()
                assert long_reading is not None
                assert "passage" in long_reading
                assert "text" in long_reading
                assert "deuterocanon" in long_reading
                break

    @freeze_time("2024-10-15")
    def test_scripture_data_structure(self):
        """FMScripture.data returns heading, long, brief - covers line 120"""
        fm = FamilyMorning(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FMScripture":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "long" in data
                assert "brief" in data
                assert "hide_closing" in data
                break


@pytest.mark.django_db
class TestFMIntercessionsData:
    """Test FMIntercessions.data property - covers line 131"""

    @freeze_time("2024-10-15")
    def test_intercessions_data_structure(self):
        """FMIntercessions.data returns title and rubric - covers line 131"""
        fm = FamilyMorning(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FMIntercessions":
                data = module[0].data
                assert data is not None
                assert "title" in data
                assert "rubric" in data
                break


@pytest.mark.django_db
class TestPaterData:
    """Test Pater (Lord's Prayer).data property - covers line 142"""

    @freeze_time("2024-10-15")
    def test_pater_data_structure(self):
        """Pater.data returns heading - covers line 142"""
        fm = FamilyMorning(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "Pater":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                break


@pytest.mark.django_db
class TestFMCollectData:
    """Test FMCollect.data property - covers lines 148-151"""

    @freeze_time("2024-10-15")
    def test_collect_data_structure(self):
        """FMCollect.data returns all collect types - covers lines 148-151"""
        fm = FamilyMorning(date=date(2024, 10, 15))

        for module in fm.modules:
            if module[0].__class__.__name__ == "FMCollect":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "time_of_day" in data
                assert "day_of_year" in data
                assert "day_of_week" in data
                break
