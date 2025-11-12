"""
Coverage tests for office/family_early_evening.py.

Targets uncovered lines to improve coverage from 74% to 100%.
Focus: FEEOpeningSentence, FEEScripture rotation (3-day cycle), FPCollect.

Uncovered lines: 62, 68, 77, 89, 94, 109-127, 131, 142, 153, 159-162
"""

import pytest
from datetime import date
from freezegun import freeze_time

from office.family_early_evening import (
    FamilyEarlyEvening,
    FEEHeading,
    FEERubricSection,
    FEEOpeningSentence,
    FEEScripture,
    FEEIntercessions,
    Pater,
    FPCollect,
)


@pytest.mark.django_db
class TestFEEHeadingData:
    """Test FEEHeading.data property - covers line 62"""

    @freeze_time("2024-10-15")
    def test_heading_data_structure(self):
        """FEEHeading.data returns heading and calendar_date - covers line 62"""
        fee = FamilyEarlyEvening(date=date(2024, 10, 15))

        for module in fee.modules:
            if module[0].__class__.__name__ == "FEEHeading":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "calendar_date" in data
                break


@pytest.mark.django_db
class TestFEERubricSectionData:
    """Test FEERubricSection.data property - covers line 68"""

    @freeze_time("2024-10-15")
    def test_rubric_section_data(self):
        """FEERubricSection.data returns rubric - covers line 68"""
        fee = FamilyEarlyEvening(date=date(2024, 10, 15))

        for module in fee.modules:
            if module[0].__class__.__name__ == "FEERubricSection":
                data = module[0].data
                assert data is not None
                assert "rubric" in data
                break


@pytest.mark.django_db
class TestFEEOpeningSentenceVariations:
    """Test FEEOpeningSentence sentence variations - covers lines 77, 89"""

    @freeze_time("2024-10-15")
    def test_opening_sentence_get_sentences(self):
        """FEEOpeningSentence.get_sentences returns seasonal and fixed - covers line 77"""
        fee = FamilyEarlyEvening(date=date(2024, 10, 15))

        for module in fee.modules:
            if module[0].__class__.__name__ == "FEEOpeningSentence":
                sentences = module[0].get_sentences()
                assert sentences is not None
                assert "seasonal" in sentences
                assert "fixed" in sentences
                assert "PSALM 36:7, 9" in sentences["fixed"]["citation"]
                break

    @freeze_time("2024-10-15")
    def test_opening_sentence_data(self):
        """FEEOpeningSentence.data returns heading and sentences - covers line 89"""
        fee = FamilyEarlyEvening(date=date(2024, 10, 15))

        for module in fee.modules:
            if module[0].__class__.__name__ == "FEEOpeningSentence":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "sentences" in data
                break


@pytest.mark.django_db
class TestFEEScriptureRotation:
    """Test FEEScripture 3-day rotation - covers lines 94, 109-127, 131"""

    @freeze_time("2024-01-01")  # Day 1 of year, 1 % 3 = 1
    def test_scripture_rotation_day_1_mod_3(self):
        """Day 1: 1 % 3 = 1 uses John 8:12 - covers lines 109-127"""
        fee = FamilyEarlyEvening(date=date(2024, 1, 1))

        for module in fee.modules:
            if module[0].__class__.__name__ == "FEEScripture":
                scripture = module[0].get_scripture()
                assert scripture is not None
                assert "citation" in scripture
                # Index [1] = John 8:12
                assert "JOHN" in scripture["citation"]
                break

    @freeze_time("2024-01-02")  # Day 2 of year, 2 % 3 = 2
    def test_scripture_rotation_day_2_mod_3(self):
        """Day 2: 2 % 3 = 2 uses Revelation 3:20 - covers lines 109-127"""
        fee = FamilyEarlyEvening(date=date(2024, 1, 2))

        for module in fee.modules:
            if module[0].__class__.__name__ == "FEEScripture":
                scripture = module[0].get_scripture()
                assert scripture is not None
                assert "citation" in scripture
                # Index [2] = Revelation
                assert "REVELATION" in scripture["citation"]
                break

    @freeze_time("2024-01-03")  # Day 3 of year, 3 % 3 = 0
    def test_scripture_rotation_day_0_mod_3(self):
        """Day 3: 3 % 3 = 0 uses 2 Corinthians 4:5-6 - covers lines 109-127"""
        fee = FamilyEarlyEvening(date=date(2024, 1, 3))

        for module in fee.modules:
            if module[0].__class__.__name__ == "FEEScripture":
                scripture = module[0].get_scripture()
                assert scripture is not None
                assert "citation" in scripture
                # Index [0] = 2 Corinthians
                assert "CORINTHIANS" in scripture["citation"]
                break

    @freeze_time("2024-06-15")
    def test_scripture_get_long_reading(self):
        """FEEScripture.get_long returns ep_reading_1 - covers line 94"""
        fee = FamilyEarlyEvening(date=date(2024, 6, 15))

        for module in fee.modules:
            if module[0].__class__.__name__ == "FEEScripture":
                long_reading = module[0].get_long()
                assert long_reading is not None
                assert "passage" in long_reading
                assert "text" in long_reading
                assert "deuterocanon" in long_reading
                break

    @freeze_time("2024-10-15")
    def test_scripture_data_structure(self):
        """FEEScripture.data returns heading, long, brief - covers line 131"""
        fee = FamilyEarlyEvening(date=date(2024, 10, 15))

        for module in fee.modules:
            if module[0].__class__.__name__ == "FEEScripture":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "long" in data
                assert "brief" in data
                assert "hide_closing" in data
                break


@pytest.mark.django_db
class TestFEEIntercessionsData:
    """Test FEEIntercessions.data property - covers line 142"""

    @freeze_time("2024-10-15")
    def test_intercessions_data_structure(self):
        """FEEIntercessions.data returns title and rubric - covers line 142"""
        fee = FamilyEarlyEvening(date=date(2024, 10, 15))

        for module in fee.modules:
            if module[0].__class__.__name__ == "FEEIntercessions":
                data = module[0].data
                assert data is not None
                assert "title" in data
                assert "rubric" in data
                break


@pytest.mark.django_db
class TestPaterData:
    """Test Pater (Lord's Prayer).data property - covers line 153"""

    @freeze_time("2024-10-15")
    def test_pater_data_structure(self):
        """Pater.data returns heading - covers line 153"""
        fee = FamilyEarlyEvening(date=date(2024, 10, 15))

        for module in fee.modules:
            if module[0].__class__.__name__ == "Pater":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                break


@pytest.mark.django_db
class TestFPCollectData:
    """Test FPCollect.data property - covers lines 159-162"""

    @freeze_time("2024-10-15")
    def test_collect_data_structure(self):
        """FPCollect.data returns all collect types - covers lines 159-162"""
        fee = FamilyEarlyEvening(date=date(2024, 10, 15))

        for module in fee.modules:
            if module[0].__class__.__name__ == "FPCollect":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "time_of_day" in data
                assert "day_of_year" in data
                assert "day_of_week" in data
                break
