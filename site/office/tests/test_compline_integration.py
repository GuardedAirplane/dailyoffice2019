"""
Integration tests for Compline (US4).

These tests validate that Compline generates complete offices
for various liturgical scenarios using production database fixtures.

Test Coverage:
- T072: Integration tests for feast days and regular days
"""

import pytest
from datetime import date as date_class

from office.compline import Compline


@pytest.mark.django_db
class TestComplineFeastDay:
    """Integration tests for Compline on feast days."""

    def test_compline_christmas_day(self):
        """Compline should generate correctly for Christmas Day."""
        office = Compline(date=date_class(2024, 12, 25))

        assert office is not None
        assert len(office.modules) == 10
        assert "Christmas" in office.description

        # Verify all modules generate data successfully
        for module, template in office.modules:
            data = module.data
            assert data is not None

    def test_compline_easter_day(self):
        """Compline should generate correctly for Easter Day."""
        office = Compline(date=date_class(2024, 3, 31))

        assert office is not None
        assert len(office.modules) == 10

        # Easter should have Alleluia in canticle and conclusion
        canticle_module = office.modules[8][0]
        assert canticle_module.data["alleluia"] is True

        conclusion_module = office.modules[9][0]
        assert conclusion_module.data["alleluia"] is True

    def test_compline_ash_wednesday(self):
        """Compline should generate correctly for Ash Wednesday."""
        office = Compline(date=date_class(2024, 2, 14))

        assert office is not None

        # Lent should omit Alleluia in invitatory
        invitatory_module = office.modules[4][0]
        assert invitatory_module.data["alleluia"] is False


@pytest.mark.django_db
class TestComplineRegularDay:
    """Integration tests for Compline on regular days."""

    def test_compline_monday(self):
        """Compline should generate correctly for a Monday."""
        office = Compline(date=date_class(2024, 1, 15))  # Monday

        assert office is not None
        assert len(office.modules) == 10

        # Monday should use Jeremiah 14:9
        scripture_module = office.modules[6][0]
        assert "JEREMIAH 14:9" in scripture_module.data["sentence"]["citation"]

        # Monday should use collects 2, 3, 5
        prayers_module = office.modules[7][0]
        collects = prayers_module.data["collects"]
        assert len(collects) == 3

    def test_compline_tuesday(self):
        """Compline should generate correctly for a Tuesday."""
        office = Compline(date=date_class(2024, 1, 16))  # Tuesday

        assert office is not None

        # Tuesday should use Matthew 11:28-30
        scripture_module = office.modules[6][0]
        assert "MATTHEW 11:28-30" in scripture_module.data["sentence"]["citation"]

    def test_compline_wednesday(self):
        """Compline should generate correctly for a Wednesday."""
        office = Compline(date=date_class(2024, 1, 17))  # Wednesday

        assert office is not None

        # Wednesday should use Hebrews 13:20-21
        scripture_module = office.modules[6][0]
        assert "HEBREWS 13:20-21" in scripture_module.data["sentence"]["citation"]

    def test_compline_thursday(self):
        """Compline should generate correctly for a Thursday."""
        office = Compline(date=date_class(2024, 1, 18))  # Thursday

        assert office is not None

        # Thursday should use 1 Peter 5:8-9
        scripture_module = office.modules[6][0]
        assert "1 PETER 5:8-9" in scripture_module.data["sentence"]["citation"]

    def test_compline_saturday(self):
        """Compline should use Paschal mystery collect on Saturday."""
        office = Compline(date=date_class(2024, 1, 20))  # Saturday

        assert office is not None

        # Saturday should include the Paschal mystery collect
        prayers_module = office.modules[7][0]
        collects = prayers_module.data["collects"]
        assert len(collects) == 3
        assert "Paschal mystery" in collects[1][1]

    def test_compline_sunday(self):
        """Compline should generate correctly for a Sunday."""
        office = Compline(date=date_class(2024, 1, 21))  # Sunday

        assert office is not None
        assert len(office.modules) == 10

        # Sunday should use Hebrews 13:20-21
        scripture_module = office.modules[6][0]
        assert "HEBREWS 13:20-21" in scripture_module.data["sentence"]["citation"]

    def test_compline_weekday_in_lent(self):
        """Compline should handle Lenten weekdays correctly."""
        office = Compline(date=date_class(2024, 3, 15))  # Friday in Lent

        assert office is not None

        # Lent should omit Alleluia
        invitatory_module = office.modules[4][0]
        assert invitatory_module.data["alleluia"] is False

    def test_compline_weekday_in_easter(self):
        """Compline should handle Easter weekdays correctly."""
        office = Compline(date=date_class(2024, 4, 15))  # Monday in Eastertide

        assert office is not None

        # Eastertide should have Alleluia in canticle and conclusion
        canticle_module = office.modules[8][0]
        assert canticle_module.data["alleluia"] is True

        conclusion_module = office.modules[9][0]
        assert conclusion_module.data["alleluia"] is True
