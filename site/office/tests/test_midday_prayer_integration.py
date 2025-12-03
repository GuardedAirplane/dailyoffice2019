"""
Integration tests for Midday Prayer (US3).

These tests validate that MiddayPrayer generates complete offices
for various liturgical scenarios using production database fixtures.

Test Coverage:
- T064: Integration tests for feast days and regular days
"""

import pytest
from datetime import date as date_class

from office.midday_prayer import MiddayPrayer


@pytest.mark.django_db
class TestMiddayPrayerFeastDay:
    """Integration tests for Midday Prayer on feast days."""

    def test_midday_prayer_christmas_day(self):
        """Midday Prayer should generate correctly for Christmas Day."""
        office = MiddayPrayer(date=date_class(2024, 12, 25))

        assert office is not None
        assert len(office.modules) == 7
        assert "Christmas" in office.description

        # Verify all modules generate data successfully
        for module, template in office.modules:
            data = module.data
            assert data is not None

    def test_midday_prayer_easter_day(self):
        """Midday Prayer should generate correctly for Easter Day."""
        office = MiddayPrayer(date=date_class(2024, 3, 31))

        assert office is not None
        assert len(office.modules) == 7

        # Easter should have Alleluia in conclusion
        conclusion_module = office.modules[6][0]
        assert conclusion_module.data["alleluia"] is True

    def test_midday_prayer_ash_wednesday(self):
        """Midday Prayer should generate correctly for Ash Wednesday."""
        office = MiddayPrayer(date=date_class(2024, 2, 14))

        assert office is not None

        # Lent should omit Alleluia in invitatory
        invitatory_module = office.modules[2][0]
        assert invitatory_module.data["alleluia"] is False


@pytest.mark.django_db
class TestMiddayPrayerRegularDay:
    """Integration tests for Midday Prayer on regular days."""

    def test_midday_prayer_monday(self):
        """Midday Prayer should generate correctly for a Monday."""
        office = MiddayPrayer(date=date_class(2024, 1, 15))  # Monday

        assert office is not None
        assert len(office.modules) == 7

        # Monday should use John 12:31-32
        scripture_module = office.modules[4][0]
        assert "JOHN 12:31-32" in scripture_module.data["sentence"]["citation"]

    def test_midday_prayer_tuesday(self):
        """Midday Prayer should generate correctly for a Tuesday."""
        office = MiddayPrayer(date=date_class(2024, 1, 16))  # Tuesday

        assert office is not None

        # Tuesday should use 2 Corinthians 5:17-18
        scripture_module = office.modules[4][0]
        assert "2 CORINTHIANS 5:17-18" in scripture_module.data["sentence"]["citation"]

    def test_midday_prayer_conversion_of_paul(self):
        """Midday Prayer should use special collects for Conversion of Paul."""
        office = MiddayPrayer(date=date_class(2024, 1, 25))

        assert office is not None

        # Should have 2 collects including Saint Paul collect
        prayers_module = office.modules[5][0]
        collects = prayers_module.data["collects"]
        assert len(collects) == 2
        assert "Saint Paul" in collects[1]
