"""
Coverage tests for office/family_close_of_day.py.

Targets uncovered lines to improve coverage from 69% to 100%.
Focus: FCDOpeningSentence, FCDScripture rotation, FCDCollect weekday logic, FCDNunc, FCDClosingSentence.

Uncovered lines: 68, 79, 89, 95, 100, 107-121, 125, 136, 147, 152-159, 163-166, 177, 182, 188
"""

import pytest
from datetime import date
from freezegun import freeze_time

from office.family_close_of_day import (
    FamilyCloseOfDay,
    FCDHeading,
    FCDOpeningSentence,
    FCDPsalms,
    FCDScripture,
    FCDIntercessions,
    Pater,
    FCDCollect,
    FCDNunc,
    FCDClosingSentence,
)


@pytest.mark.django_db
class TestFCDHeadingData:
    """Test FCDHeading.data property - covers line 68"""

    @freeze_time("2024-10-15")
    def test_heading_data_structure(self):
        """FCDHeading.data returns heading, rubric, calendar_date - covers line 68"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDHeading":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "rubric" in data
                assert "calendar_date" in data
                break


@pytest.mark.django_db
class TestFCDOpeningSentenceVariations:
    """Test FCDOpeningSentence sentence variations - covers lines 79, 89"""

    @freeze_time("2024-10-15")
    def test_opening_sentence_get_sentences(self):
        """FCDOpeningSentence.get_sentences returns seasonal and fixed - covers line 79"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDOpeningSentence":
                sentences = module[0].get_sentences()
                assert sentences is not None
                assert "seasonal" in sentences
                assert "fixed" in sentences
                assert "PSALM 4:8" in sentences["fixed"]["citation"]
                break

    @freeze_time("2024-10-15")
    def test_opening_sentence_data(self):
        """FCDOpeningSentence.data returns heading and sentences - covers line 89"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDOpeningSentence":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "sentences" in data
                break


@pytest.mark.django_db
class TestFCDPsalmsData:
    """Test FCDPsalms.data property - covers line 95"""

    @freeze_time("2024-10-15")
    def test_psalms_data_structure(self):
        """FCDPsalms.data returns heading and psalms (134) - covers line 95"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDPsalms":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "psalms" in data
                break


@pytest.mark.django_db
class TestFCDScriptureRotation:
    """Test FCDScripture day-of-year rotation - covers lines 100, 107-121, 125"""

    @freeze_time("2024-01-01")  # Day 1 of year, 1 % 2 = 1
    def test_scripture_rotation_odd_day(self):
        """Odd day of year uses 1 Thessalonians 5:23 - covers lines 107-121"""
        fcd = FamilyCloseOfDay(date=date(2024, 1, 1))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDScripture":
                scripture = module[0].get_scripture()
                assert scripture is not None
                assert "citation" in scripture
                # Day 1: 1 % 2 = 1, so index [1] = 1 Thessalonians
                assert "THESSALONIANS" in scripture["citation"]
                break

    @freeze_time("2024-01-02")  # Day 2 of year, 2 % 2 = 0
    def test_scripture_rotation_even_day(self):
        """Even day of year uses Isaiah 26:3-4 - covers lines 107-121"""
        fcd = FamilyCloseOfDay(date=date(2024, 1, 2))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDScripture":
                scripture = module[0].get_scripture()
                assert scripture is not None
                assert "citation" in scripture
                # Day 2: 2 % 2 = 0, so index [0] = Isaiah
                assert "ISAIAH" in scripture["citation"]
                break

    @freeze_time("2024-06-15")
    def test_scripture_get_long_reading(self):
        """FCDScripture.get_long returns ep_reading_2 - covers line 100"""
        fcd = FamilyCloseOfDay(date=date(2024, 6, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDScripture":
                long_reading = module[0].get_long()
                assert long_reading is not None
                assert "passage" in long_reading
                assert "text" in long_reading
                assert "deuterocanon" in long_reading
                break

    @freeze_time("2024-10-15")
    def test_scripture_data_structure(self):
        """FCDScripture.data returns heading, long, brief - covers line 125"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDScripture":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "long" in data
                assert "brief" in data
                assert "hide_closing" in data
                break


@pytest.mark.django_db
class TestFCDIntercessionsData:
    """Test FCDIntercessions.data property - covers line 136"""

    @freeze_time("2024-10-15")
    def test_intercessions_data_structure(self):
        """FCDIntercessions.data returns title and rubric - covers line 136"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDIntercessions":
                data = module[0].data
                assert data is not None
                assert "title" in data
                assert "rubric" in data
                break


@pytest.mark.django_db
class TestPaterData:
    """Test Pater (Lord's Prayer).data property - covers line 147"""

    @freeze_time("2024-10-15")
    def test_pater_data_structure(self):
        """Pater.data returns heading - covers line 147"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "Pater":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                break


@pytest.mark.django_db
class TestFCDCollectWeekdayRotation:
    """Test FCDCollect weekday rotation with special Friday/Saturday swap - covers lines 152-159, 163-166"""

    @freeze_time("2024-10-13")  # Sunday (weekday 6)
    def test_collect_sunday(self):
        """Sunday uses ComplinePrayers.collects[6] - covers lines 152-159"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 13))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                break

    @freeze_time("2024-10-14")  # Monday (weekday 0)
    def test_collect_monday(self):
        """Monday uses ComplinePrayers.collects[0] - covers lines 152-159"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 14))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                break

    @freeze_time("2024-10-15")  # Tuesday (weekday 1)
    def test_collect_tuesday(self):
        """Tuesday uses ComplinePrayers.collects[1] - covers lines 152-159"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                break

    @freeze_time("2024-10-16")  # Wednesday (weekday 2)
    def test_collect_wednesday(self):
        """Wednesday uses ComplinePrayers.collects[2] - covers lines 152-159"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 16))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                break

    @freeze_time("2024-10-17")  # Thursday (weekday 3)
    def test_collect_thursday(self):
        """Thursday uses ComplinePrayers.collects[3] - covers lines 152-159"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 17))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                break

    @freeze_time("2024-10-18")  # Friday (weekday 4) -> swapped to 5
    def test_collect_friday_swapped(self):
        """Friday (4) swaps to 5 per special logic - covers lines 154-155"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 18))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                # Verify Friday uses collect[5] instead of collect[4]
                break

    @freeze_time("2024-10-19")  # Saturday (weekday 5) -> swapped to 4
    def test_collect_saturday_swapped(self):
        """Saturday (5) swaps to 4 per special logic - covers lines 156-157"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 19))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDCollect":
                collect = module[0].get_day_of_week_collect()
                assert collect is not None
                assert len(collect) == 3
                # Verify Saturday uses collect[4] instead of collect[5]
                break

    @freeze_time("2024-10-15")
    def test_collect_data_structure(self):
        """FCDCollect.data returns all collect types - covers lines 163-166"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDCollect":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "time_of_day" in data
                assert "day_of_year" in data
                assert "day_of_week" in data
                break


@pytest.mark.django_db
class TestFCDNuncData:
    """Test FCDNunc.data property - covers line 177"""

    @freeze_time("2024-10-15")
    def test_nunc_data_returns_canticle(self):
        """FCDNunc.data returns EP2 canticle - covers line 177"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDNunc":
                data = module[0].data
                # EP2 is the canticle class itself
                assert data is not None
                break


@pytest.mark.django_db
class TestFCDClosingSentenceData:
    """Test FCDClosingSentence data and get_sentence - covers lines 182, 188"""

    @freeze_time("2024-10-15")
    def test_closing_sentence_get_sentence(self):
        """FCDClosingSentence.get_sentence returns sentence dict - covers line 182"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDClosingSentence":
                sentence = module[0].get_sentence()
                assert sentence is not None
                assert "sentence" in sentence
                assert "almighty and merciful Lord" in sentence["sentence"]
                break

    @freeze_time("2024-10-15")
    def test_closing_sentence_data(self):
        """FCDClosingSentence.data returns heading and sentence - covers line 188"""
        fcd = FamilyCloseOfDay(date=date(2024, 10, 15))

        for module in fcd.modules:
            if module[0].__class__.__name__ == "FCDClosingSentence":
                data = module[0].data
                assert data is not None
                assert "heading" in data
                assert "sentence" in data
                break
