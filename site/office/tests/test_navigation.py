"""
Unit tests for office navigation between different office types.

These tests validate that navigation links preserve dates correctly
and generate proper URLs for all office types.

Test Coverage:
- T078: Office.links property generates correct URLs
- T079: Navigation preserves date across offices
"""

import pytest
from datetime import date as date_class

from office.morning_prayer import MorningPrayer
from office.evening_prayer import EveningPrayer
from office.midday_prayer import MiddayPrayer
from office.compline import Compline

pytestmark = pytest.mark.usefixtures("compline_office_data")


@pytest.mark.django_db
class TestOfficeLinks:
    """Unit tests for Office.links property URL generation."""

    def test_links_property_exists(self, mock_url_reverse):
        """All offices should have a links property."""
        office = MorningPrayer(date=date_class(2024, 1, 15))
        assert hasattr(office, "links")
        assert office.links is not None

    def test_links_contains_all_office_types(self, mock_url_reverse):
        """Links should include all four main office types."""
        office = MorningPrayer(date=date_class(2024, 1, 15))
        links = office.links

        assert "morning_prayer" in links
        assert "evening_prayer" in links
        assert "midday_prayer" in links
        assert "compline" in links

    def test_links_contains_date_navigation(self, mock_url_reverse):
        """Links should include yesterday and tomorrow navigation."""
        office = MorningPrayer(date=date_class(2024, 1, 15))
        links = office.links

        assert "yesterday" in links
        assert "tomorrow" in links

    def test_links_contains_current_office(self, mock_url_reverse):
        """Links should indicate the current office type."""
        morning = MorningPrayer(date=date_class(2024, 1, 15))
        evening = EveningPrayer(date=date_class(2024, 1, 15))
        midday = MiddayPrayer(date=date_class(2024, 1, 15))
        compline = Compline(date=date_class(2024, 1, 15))

        assert morning.links["current"] == "morning_prayer"
        assert evening.links["current"] == "evening_prayer"
        assert midday.links["current"] == "midday_prayer"
        assert compline.links["current"] == "compline"

    def test_links_contains_date_string(self, mock_url_reverse):
        """Links should include formatted date string."""
        office = MorningPrayer(date=date_class(2024, 1, 15))
        links = office.links

        assert "date" in links
        assert "January 15, 2024" in links["date"]

    def test_links_have_labels(self, mock_url_reverse):
        """All navigation links should have labels."""
        office = MorningPrayer(date=date_class(2024, 1, 15))
        links = office.links

        assert links["morning_prayer"]["label"] == "Morning"
        assert links["evening_prayer"]["label"] == "Evening"
        assert links["midday_prayer"]["label"] == "Midday"
        assert links["compline"]["label"] == "Compline"
        assert links["yesterday"]["label"] == "Sun"  # Jan 14, 2024 is Sunday
        assert links["tomorrow"]["label"] == "Tue"  # Jan 16, 2024 is Tuesday


@pytest.mark.django_db
class TestDatePreservation:
    """Unit tests for date preservation across office navigation."""

    def test_morning_prayer_preserves_date_in_links(self, mock_url_reverse):
        """Morning Prayer links should preserve the current date for all offices."""
        office = MorningPrayer(date=date_class(2024, 1, 15))
        links = office.links

        # Verify all office type links preserve the same date (format: /office_type/year-month-day/)
        assert "2024-1-15" in links["morning_prayer"]["link"]
        assert "2024-1-15" in links["evening_prayer"]["link"]
        assert "2024-1-15" in links["midday_prayer"]["link"]
        assert "2024-1-15" in links["compline"]["link"]

    def test_evening_prayer_preserves_date_in_links(self, mock_url_reverse):
        """Evening Prayer links should preserve the current date for all offices."""
        office = EveningPrayer(date=date_class(2024, 1, 15))
        links = office.links

        assert "2024-1-15" in links["morning_prayer"]["link"]
        assert "2024-1-15" in links["evening_prayer"]["link"]
        assert "2024-1-15" in links["midday_prayer"]["link"]
        assert "2024-1-15" in links["compline"]["link"]

    def test_midday_prayer_preserves_date_in_links(self, mock_url_reverse):
        """Midday Prayer links should preserve the current date for all offices."""
        office = MiddayPrayer(date=date_class(2024, 1, 15))
        links = office.links

        assert "2024-1-15" in links["morning_prayer"]["link"]
        assert "2024-1-15" in links["evening_prayer"]["link"]
        assert "2024-1-15" in links["midday_prayer"]["link"]
        assert "2024-1-15" in links["compline"]["link"]

    def test_compline_preserves_date_in_links(self, mock_url_reverse):
        """Compline links should preserve the current date for all offices."""
        office = Compline(date=date_class(2024, 1, 15))
        links = office.links

        assert "2024-1-15" in links["morning_prayer"]["link"]
        assert "2024-1-15" in links["evening_prayer"]["link"]
        assert "2024-1-15" in links["midday_prayer"]["link"]
        assert "2024-1-15" in links["compline"]["link"]

    def test_yesterday_link_decrements_date(self, mock_url_reverse):
        """Yesterday link should point to previous day."""
        office = MorningPrayer(date=date_class(2024, 1, 15))
        links = office.links

        assert "2024-1-14" in links["yesterday"]["link"]

    def test_tomorrow_link_increments_date(self, mock_url_reverse):
        """Tomorrow link should point to next day."""
        office = MorningPrayer(date=date_class(2024, 1, 15))
        links = office.links

        assert "2024-1-16" in links["tomorrow"]["link"]

    def test_date_navigation_crosses_month_boundary(self, mock_url_reverse):
        """Date navigation should correctly handle month boundaries."""
        office = MorningPrayer(date=date_class(2024, 1, 31))
        links = office.links

        # Tomorrow from Jan 31 should be Feb 1
        assert "2024-2-1" in links["tomorrow"]["link"]

    def test_date_navigation_crosses_year_boundary(self, mock_url_reverse):
        """Date navigation should correctly handle year boundaries."""
        office = MorningPrayer(date=date_class(2024, 12, 31))
        links = office.links

        # Tomorrow from Dec 31 should be Jan 1 of next year
        assert "2025-1-1" in links["tomorrow"]["link"]


@pytest.mark.django_db
class TestFamilyOfficeLinks:
    """Unit tests for family office navigation links."""

    def test_links_contain_family_offices(self, mock_url_reverse):
        """Links should include family office types."""
        office = MorningPrayer(date=date_class(2024, 1, 15))
        links = office.links

        assert "family_morning_prayer" in links
        assert "family_midday_prayer" in links
        assert "family_early_evening_prayer" in links
        assert "family_close_of_day_prayer" in links

    def test_family_office_links_have_labels(self, mock_url_reverse):
        """Family office links should have descriptive labels."""
        office = MorningPrayer(date=date_class(2024, 1, 15))
        links = office.links

        assert links["family_morning_prayer"]["label"] == "Morning"
        assert links["family_midday_prayer"]["label"] == "Midday"
        assert links["family_early_evening_prayer"]["label"] == "Early Evening"
        assert links["family_close_of_day_prayer"]["label"] == "Close of Day"

    def test_family_offices_preserve_date(self, mock_url_reverse):
        """Family office links should preserve the current date."""
        office = MorningPrayer(date=date_class(2024, 1, 15))
        links = office.links

        assert "2024-1-15" in links["family_morning_prayer"]["link"]
        assert "2024-1-15" in links["family_midday_prayer"]["link"]
        assert "2024-1-15" in links["family_early_evening_prayer"]["link"]
        assert "2024-1-15" in links["family_close_of_day_prayer"]["link"]
