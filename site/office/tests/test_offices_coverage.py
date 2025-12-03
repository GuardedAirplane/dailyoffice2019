"""
Coverage tests for Office base class uncovered code paths.

Targets uncovered lines to improve coverage from 69% to 85%+.
Focus on: navigation links, pandemic collects rotation, election collects, Reading base class.
"""

import pytest
from datetime import date
from freezegun import freeze_time
from office.morning_prayer import MorningPrayer
from office.evening_prayer import EveningPrayer
from office.offices import PandemicPrayers, Reading


@pytest.mark.django_db
class TestOfficeNavigationLinks:
    """Test Office.links property navigation generation."""

    @freeze_time("2024-01-15")
    def test_links_include_yesterday_tomorrow(self, mock_url_reverse):
        """Navigation links include yesterday and tomorrow - covers links property"""
        mp = MorningPrayer(date=date(2024, 1, 15))

        # Access links property to trigger navigation generation
        links = mp.links

        assert "yesterday" in links
        assert "tomorrow" in links
        assert links["yesterday"]["label"] == "Sun"  # Jan 14, 2024 is Sunday
        assert links["tomorrow"]["label"] == "Tue"  # Jan 16, 2024 is Tuesday

    @freeze_time("2024-01-15")
    def test_links_include_all_office_types(self, mock_url_reverse):
        """Navigation links include all office types"""
        mp = MorningPrayer(date=date(2024, 1, 15))

        links = mp.links

        # Standard offices
        assert "morning_prayer" in links
        assert "midday_prayer" in links
        assert "evening_prayer" in links
        assert "compline" in links

        # Family offices
        assert "family_morning_prayer" in links
        assert "family_midday_prayer" in links
        assert "family_early_evening_prayer" in links
        assert "family_close_of_day_prayer" in links

    @freeze_time("2024-01-15")
    def test_links_current_office_marker(self, mock_url_reverse):
        """Links include current office marker"""
        mp = MorningPrayer(date=date(2024, 1, 15))

        links = mp.links

        assert links["current"] == "morning_prayer"


@pytest.mark.django_db
class TestPandemicCollectsRotation:
    """Test PandemicPrayers collect rotation logic."""

    @freeze_time("2024-01-01")  # Day 1 of year (tm_yday=1, 1%2=1)
    def test_collect_1_morning_prayer_day_1(self):
        """Morning Prayer on day 1 uses collect index 1 - covers lines 492-494"""
        mp = MorningPrayer(date=date(2024, 1, 1))

        # Find PandemicPrayers module and access data
        for module in mp.modules:
            if module[0].__class__.__name__ == "PandemicPrayers":
                data = module[0].data
                collect_1 = data["collect_1"]
                # Day 1: tm_yday=1, 1%2=1, so morning uses index 1
                assert "Common Plague or Sickness" in collect_1["title"]
                break

    @freeze_time("2024-01-02")  # Day 2 of year (tm_yday=2, 2%2=0)
    def test_collect_1_morning_prayer_day_2(self):
        """Morning Prayer on day 2 uses collect index 0 - covers lines 492-494"""
        mp = MorningPrayer(date=date(2024, 1, 2))

        for module in mp.modules:
            if module[0].__class__.__name__ == "PandemicPrayers":
                data = module[0].data
                collect_1 = data["collect_1"]
                # Day 2: tm_yday=2, 2%2=0, so morning uses index 0
                assert "Great Sickness and Mortality" in collect_1["title"]
                break

    @freeze_time("2024-01-01")
    def test_collect_1_evening_prayer_opposite_rotation(self):
        """Evening Prayer uses opposite collect from Morning Prayer - covers lines 495-496"""
        ep = EveningPrayer(date=date(2024, 1, 1))

        for module in ep.modules:
            if module[0].__class__.__name__ == "PandemicPrayers":
                data = module[0].data
                collect_1 = data["collect_1"]
                # Day 1: tm_yday=1, 1%2=1, evening uses 1-1=0
                assert "Great Sickness and Mortality" in collect_1["title"]
                break

    @freeze_time("2024-01-01")  # Monday (weekday 0)
    def test_collect_2_weekday_rotation_monday(self):
        """Collect 2 rotates by weekday - Monday uses index 0 - covers lines 498-540"""
        mp = MorningPrayer(date=date(2024, 1, 1))

        for module in mp.modules:
            if module[0].__class__.__name__ == "PandemicPrayers":
                data = module[0].data
                collect_2 = data["collect_2"]
                # Monday (weekday 0) -> morning uses index 0
                assert "Natural Disaster" in collect_2["title"]
                break

    @freeze_time("2024-01-07")  # Sunday (weekday 6)
    def test_collect_2_weekday_rotation_sunday(self):
        """Collect 2 on Sunday uses index 6 for morning - covers line 540"""
        mp = MorningPrayer(date=date(2024, 1, 7))

        for module in mp.modules:
            if module[0].__class__.__name__ == "PandemicPrayers":
                data = module[0].data
                collect_2 = data["collect_2"]
                # Sunday (weekday 6) -> morning uses index 6
                assert "Trustfulness in Times of Worry" in collect_2["title"]
                break

    @freeze_time("2024-01-07")  # Sunday (weekday 6)
    def test_collect_2_evening_opposite_weekday(self):
        """Evening Prayer uses opposite weekday rotation - covers line 540"""
        ep = EveningPrayer(date=date(2024, 1, 7))

        for module in ep.modules:
            if module[0].__class__.__name__ == "PandemicPrayers":
                data = module[0].data
                collect_2 = data["collect_2"]
                # Sunday (weekday 6) -> evening uses 6-6=0
                assert "Natural Disaster" in collect_2["title"]
                break


@pytest.mark.django_db
class TestElectionCollects:
    """Test election-period collects (Oct 27 - Nov 4, 2020)."""

    @freeze_time("2020-10-27")  # First day of election period
    def test_collect_3_during_election_period(self):
        """Collect 3 appears during election period - covers lines 549-556"""
        mp = MorningPrayer(date=date(2020, 10, 27))

        for module in mp.modules:
            if module[0].__class__.__name__ == "PandemicPrayers":
                data = module[0].data
                collect_3 = data["collect_3"]
                assert collect_3 is not None
                assert "Election" in collect_3["title"]
                break

    @freeze_time("2020-11-04")  # Last day of election period
    def test_collect_4_during_election_period(self):
        """Collect 4 appears during election period - covers lines 565-572"""
        mp = MorningPrayer(date=date(2020, 11, 4))

        for module in mp.modules:
            if module[0].__class__.__name__ == "PandemicPrayers":
                data = module[0].data
                collect_4 = data["collect_4"]
                assert collect_4 is not None
                assert "Our Nation" in collect_4["title"]
                break

    @freeze_time("2020-10-26")  # Day before election period
    def test_collect_3_before_election_period(self):
        """Collect 3 is None before election period - covers lines 549, 556"""
        mp = MorningPrayer(date=date(2020, 10, 26))

        for module in mp.modules:
            if module[0].__class__.__name__ == "PandemicPrayers":
                data = module[0].data
                collect_3 = data["collect_3"]
                assert collect_3 is None
                break

    @freeze_time("2020-11-05")  # Day after election period
    def test_collect_4_after_election_period(self):
        """Collect 4 is None after election period - covers lines 565, 572"""
        mp = MorningPrayer(date=date(2020, 11, 5))

        for module in mp.modules:
            if module[0].__class__.__name__ == "PandemicPrayers":
                data = module[0].data
                collect_4 = data["collect_4"]
                assert collect_4 is None
                break

    @freeze_time("2024-10-27")  # Same date but wrong year
    def test_election_collects_2020_only(self):
        """Election collects only appear in 2020 - covers date range logic"""
        mp = MorningPrayer(date=date(2024, 10, 27))

        for module in mp.modules:
            if module[0].__class__.__name__ == "PandemicPrayers":
                data = module[0].data
                # Election collects hardcoded to 2020 dates
                assert data["collect_3"] is None
                assert data["collect_4"] is None
                break


@pytest.mark.django_db
class TestReadingClosingFormulas:
    """Test Reading.closing() static method for different testaments."""

    def test_closing_old_testament(self):
        """Old Testament reading has standard closing - covers line 225-227"""
        closing = Reading.closing("OT")

        assert closing["reader"] == "The Word of the Lord."
        assert closing["people"] == "Thanks be to God."

    def test_closing_new_testament(self):
        """New Testament reading has standard closing - covers line 225-227"""
        closing = Reading.closing("NT")

        assert closing["reader"] == "The Word of the Lord."
        assert closing["people"] == "Thanks be to God."

    def test_closing_deuterocanon(self):
        """Deuterocanon reading has alternate closing - covers line 225-227"""
        closing = Reading.closing("DC")

        assert closing["reader"] == "Here ends the Reading."
        assert closing["people"] == ""

    def test_closing_psalms(self):
        """Psalms reading has standard closing - covers line 225-227"""
        closing = Reading.closing("PS")

        assert closing["reader"] == "The Word of the Lord."
        assert closing["people"] == "Thanks be to God."


@pytest.mark.django_db
class TestReadingDataCompilation:
    """Test Reading.data() method for compiling reading variants."""

    @freeze_time("2024-01-15")
    def test_reading_data_structure(self):
        """Reading.data() returns complete structure - covers lines 234-252"""
        mp = MorningPrayer(date=date(2024, 1, 15))

        # Find a reading module and access its data
        for module in mp.modules:
            if module[0].__class__.__name__ in ["MPFirstReading", "MPSecondReading"]:
                data = module[0].data()

                # Verify all expected keys exist
                assert "heading" in data
                assert "has_main_reading" in data
                assert "has_abbreviated_reading" in data
                assert "has_alternate_reading" in data
                assert "has_alternate_abbreviated_reading" in data
                assert "has_mass_reading" in data
                assert "has_abbreviated_mass_reading" in data
                assert "main_reading" in data
                assert "abbreviated_reading" in data
                assert "alternate_reading" in data
                assert "alternate_abbreviated_reading" in data
                assert "mass_reading" in data
                assert "abbreviated_mass_reading" in data
                assert "tag_prefix" in data
                break


@pytest.mark.django_db
class TestThirdReadingAvailability:
    """Test ThirdReading only appears on major feast days."""

    @freeze_time("2024-12-25")  # Christmas - major feast
    def test_third_reading_on_major_feast(self):
        """Third reading appears on Christmas - covers ThirdReading class"""
        mp = MorningPrayer(date=date(2024, 12, 25))

        module_names = [m[0].__class__.__name__ for m in mp.modules]

        # Third reading should appear on major feasts
        assert "ThirdReading" in module_names

        # Access the ThirdReading data to trigger coverage
        for module in mp.modules:
            if module[0].__class__.__name__ == "ThirdReading":
                data = module[0].data()
                # ThirdReading.has_main_reading should be False
                assert "has_main_reading" in data
                break
