"""
Integration tests for Evening Prayer office generation.

Validates: FR-002 (Display Evening Prayer with all components)
User Story: US2 (View Evening Prayer)
Priority: P1 (High) - MVP Feature

Integration tests verify that Evening Prayer correctly assembles all components
for complete liturgical services on various types of days.

Constitution Requirements:
- FR-002: Display Evening Prayer with all required liturgical components
- FR-005: Different psalm assignments for Evening Prayer vs Morning Prayer
- FR-007: Proper collects and readings for feast days
- FR-011: Display commemorations and feast names
- FR-012: View offices for any date
"""

import pytest
from datetime import date as date_class

from office.evening_prayer import EveningPrayer
from office.models import StandardOfficeDay


@pytest.mark.integration
@pytest.mark.us2
class TestEveningPrayerFeastDay:
    """
    Test Evening Prayer on major feast days.
    
    Validates: FR-007 (Feast day readings), FR-011 (Commemorations)
    Tasks: T053
    """

    def test_evening_prayer_christmas_day(self, db):
        """Evening Prayer generates complete office for Christmas Day."""
        # Use Christmas Day 2024
        christmas_date = date_class(2024, 12, 25)
        
        # Act
        ep = EveningPrayer(date=christmas_date)
        
        # Assert - Basic structure
        assert ep is not None
        assert ep.name == "Evening Prayer"
        assert ep.date.date == christmas_date
        
        # Assert - Modules generated
        modules = ep.modules
        assert modules is not None
        assert len(modules) >= 20, "Christmas EP should have at least 20 modules"
        
        # Assert - Commemoration is Christmas
        assert "Christmas" in ep.date.primary_evening.name or "Nativity" in ep.date.primary_evening.name

    def test_evening_prayer_easter_day(self, db):
        """Evening Prayer generates complete office for Easter Day."""
        # Use Easter Sunday 2025
        easter_date = date_class(2025, 4, 20)
        
        # Act
        ep = EveningPrayer(date=easter_date)
        
        # Assert - Basic structure
        assert ep is not None
        assert ep.name == "Evening Prayer"
        assert ep.date.date == easter_date
        
        # Assert - Modules generated
        modules = ep.modules
        assert modules is not None
        assert len(modules) >= 20, "Easter EP should have at least 20 modules"
        
        # Assert - Easter season
        assert ep.date.evening_season.name == "Eastertide"
        assert "Easter" in ep.date.primary_evening.name

    def test_evening_prayer_epiphany(self, db):
        """Evening Prayer generates complete office for Epiphany."""
        # Use Epiphany 2025 (January 6)
        epiphany_date = date_class(2025, 1, 6)
        
        # Act
        ep = EveningPrayer(date=epiphany_date)
        
        # Assert - Basic structure
        assert ep is not None
        assert ep.date.date == epiphany_date
        
        # Assert - Commemoration is Epiphany
        assert "Epiphany" in ep.date.primary_evening.name

    def test_evening_prayer_ash_wednesday(self, db):
        """Evening Prayer generates complete office for Ash Wednesday."""
        # Use Ash Wednesday 2025
        ash_wednesday = date_class(2025, 3, 5)
        
        # Act
        ep = EveningPrayer(date=ash_wednesday)
        
        # Assert - Basic structure
        assert ep is not None
        assert ep.date.date == ash_wednesday
        
        # Assert - Lenten season
        assert ep.date.evening_season.name == "Lent"
        assert "Ash Wednesday" in ep.date.primary_evening.name

    def test_evening_prayer_ascension(self, db):
        """Evening Prayer generates complete office for Ascension Day."""
        # Use Ascension Day 2025 (40 days after Easter = May 29)
        ascension_date = date_class(2025, 5, 29)
        
        # Act
        ep = EveningPrayer(date=ascension_date)
        
        # Assert - Basic structure
        assert ep is not None
        assert ep.date.date == ascension_date
        
        # Assert - Ascension commemoration
        assert "Ascension" in ep.date.primary_evening.name

    def test_evening_prayer_pentecost(self, db):
        """Evening Prayer generates complete office for Pentecost."""
        # Use Pentecost 2025 (50 days after Easter = June 8)
        pentecost_date = date_class(2025, 6, 8)
        
        # Act
        ep = EveningPrayer(date=pentecost_date)
        
        # Assert - Basic structure
        assert ep is not None
        assert ep.date.date == pentecost_date
        
        # Assert - Pentecost commemoration
        assert "Pentecost" in ep.date.primary_evening.name


@pytest.mark.integration
@pytest.mark.us2
class TestEveningPrayerRegularDay:
    """
    Test Evening Prayer on regular days (ferias).
    
    Validates: FR-002 (Complete Evening Prayer structure)
    Tasks: T053
    """

    def test_evening_prayer_ordinary_weekday(self, db):
        """Evening Prayer generates complete office for ordinary weekday."""
        # Use a regular Tuesday in ordinary time
        regular_date = date_class(2025, 6, 10)
        
        # Act
        ep = EveningPrayer(date=regular_date)
        
        # Assert - Basic structure
        assert ep is not None
        assert ep.name == "Evening Prayer"
        assert ep.date.date == regular_date
        
        # Assert - Modules generated
        modules = ep.modules
        assert modules is not None
        assert len(modules) >= 20, "Regular day EP should have at least 20 modules"
        
        # Assert - Office readings available
        assert ep.office_readings is not None
        assert isinstance(ep.office_readings, StandardOfficeDay)

    def test_evening_prayer_sunday_ordinary_time(self, db):
        """Evening Prayer generates complete office for Sunday in ordinary time."""
        # Use a Sunday in ordinary time (after Trinity Sunday)
        sunday_date = date_class(2025, 6, 15)
        
        # Act
        ep = EveningPrayer(date=sunday_date)
        
        # Assert - Basic structure
        assert ep is not None
        assert ep.date.date == sunday_date
        assert ep.date.date.weekday() == 6  # Sunday
        
        # Assert - Modules generated
        modules = ep.modules
        assert modules is not None
        assert len(modules) >= 20

    def test_evening_prayer_monday_epiphany_season(self, db):
        """Evening Prayer generates complete office for Monday in Epiphany season."""
        # Use Monday in Epiphany season
        monday_date = date_class(2025, 1, 13)
        
        # Act
        ep = EveningPrayer(date=monday_date)
        
        # Assert - Basic structure
        assert ep is not None
        assert ep.date.date == monday_date
        assert ep.date.date.weekday() == 0  # Monday
        
        # Assert - Epiphany season
        assert ep.date.evening_season.name == "Epiphanytide"

    def test_evening_prayer_complete_modules_regular_day(self, db):
        """Evening Prayer includes all required modules on regular day."""
        # Use regular Wednesday
        regular_date = date_class(2025, 1, 15)
        
        # Act
        ep = EveningPrayer(date=regular_date)
        modules = ep.modules
        
        # Get module class names
        module_names = [m[0].__class__.__name__ for m in modules]
        
        # Assert - Essential sections present
        assert "EPHeading" in module_names
        assert "EPOpeningSentence" in module_names
        assert "Confession" in module_names
        assert "Invitatory" in module_names or "EPInvitatory" in module_names
        assert any("Psalm" in name for name in module_names)
        assert any("Reading" in name for name in module_names)
        assert any("Canticle" in name for name in module_names)
        assert "Creed" in module_names
        assert "Prayers" in module_names
        assert "Dismissal" in module_names

    def test_evening_prayer_weekday_variation(self, db):
        """Evening Prayer varies appropriately across weekdays."""
        # Test several different weekdays
        dates = [
            date_class(2025, 1, 13),  # Monday
            date_class(2025, 1, 14),  # Tuesday
            date_class(2025, 1, 15),  # Wednesday
            date_class(2025, 1, 16),  # Thursday
            date_class(2025, 1, 17),  # Friday
            date_class(2025, 1, 18),  # Saturday
            date_class(2025, 1, 19),  # Sunday
        ]
        
        offices = []
        for test_date in dates:
            ep = EveningPrayer(date=test_date)
            offices.append(ep)
        
        # Assert - All offices generated successfully
        assert len(offices) == 7
        
        # Assert - Each has complete module list
        for ep in offices:
            assert len(ep.modules) >= 20

    def test_evening_prayer_readings_present(self, db):
        """Evening Prayer includes both OT and NT readings on regular day."""
        # Use regular day
        regular_date = date_class(2025, 1, 15)
        
        # Act
        ep = EveningPrayer(date=regular_date)
        
        # Assert - Office readings include both readings
        assert ep.office_readings.ep_reading_1 is not None
        assert ep.office_readings.ep_reading_2 is not None
        assert len(ep.office_readings.ep_reading_1) > 0
        assert len(ep.office_readings.ep_reading_2) > 0

    def test_evening_prayer_psalms_present(self, db):
        """Evening Prayer includes psalm assignments on regular day."""
        # Use regular day
        regular_date = date_class(2025, 1, 15)
        
        # Act
        ep = EveningPrayer(date=regular_date)
        
        # Assert - Psalm assignments present
        assert ep.office_readings.ep_psalms is not None
        assert len(ep.office_readings.ep_psalms) > 0
        assert ep.thirty_day_psalter_day.ep_psalms is not None
        assert len(ep.thirty_day_psalter_day.ep_psalms) > 0

    def test_evening_prayer_psalms_differ_from_morning(self, db):
        """Evening Prayer has different psalm assignments than Morning Prayer."""
        from office.morning_prayer import MorningPrayer
        
        # Use regular day
        regular_date = date_class(2025, 1, 15)
        
        # Act
        ep = EveningPrayer(date=regular_date)
        mp = MorningPrayer(date=regular_date)
        
        # Assert - Psalm assignments should be different
        # 60-day cycle
        assert ep.office_readings.ep_psalms != mp.office_readings.mp_psalms, \
            "Evening and Morning psalms (60-day) should differ"
        
        # 30-day cycle
        assert ep.thirty_day_psalter_day.ep_psalms != mp.thirty_day_psalter_day.mp_psalms, \
            "Evening and Morning psalms (30-day) should differ"
