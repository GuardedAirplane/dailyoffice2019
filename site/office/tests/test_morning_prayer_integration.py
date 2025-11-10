"""
Integration tests for Morning Prayer office generation.

Validates: FR-001 (Display Morning Prayer with all components)
User Story: US1 (View Morning Prayer)
Priority: P1 (High) - MVP Feature

Integration tests verify that Morning Prayer correctly assembles all components
for complete liturgical services on various types of days.

Constitution Requirements:
- FR-001: Display Morning Prayer with all required liturgical components
- FR-007: Proper collects and readings for feast days
- FR-011: Display commemorations and feast names
- FR-012: View offices for any date
"""

import pytest
from datetime import date as date_class

from office.morning_prayer import MorningPrayer
from office.models import StandardOfficeDay


@pytest.mark.integration
@pytest.mark.us1
class TestMorningPrayerFeastDay:
    """
    Test Morning Prayer on major feast days.
    
    Validates: FR-007 (Feast day readings), FR-011 (Commemorations)
    Tasks: T037
    """

    def test_morning_prayer_christmas_day(self, db):
        """Morning Prayer generates complete office for Christmas Day."""
        # Use Christmas Day 2024
        christmas_date = date_class(2024, 12, 25)
        
        # Act
        mp = MorningPrayer(date=christmas_date)
        
        # Assert - Basic structure
        assert mp is not None
        assert mp.name == "Morning Prayer"
        assert mp.date.date == christmas_date
        
        # Assert - Modules generated
        modules = mp.modules
        assert modules is not None
        assert len(modules) >= 20, "Christmas MP should have at least 20 modules"
        
        # Assert - Commemoration is Christmas
        assert "Christmas" in mp.date.primary.name or "Nativity" in mp.date.primary.name

    def test_morning_prayer_easter_day(self, db):
        """Morning Prayer generates complete office for Easter Day."""
        # Use Easter Sunday 2025
        easter_date = date_class(2025, 4, 20)
        
        # Act
        mp = MorningPrayer(date=easter_date)
        
        # Assert - Basic structure
        assert mp is not None
        assert mp.name == "Morning Prayer"
        assert mp.date.date == easter_date
        
        # Assert - Modules generated
        modules = mp.modules
        assert modules is not None
        assert len(modules) >= 20, "Easter MP should have at least 20 modules"
        
        # Assert - Easter season
        assert mp.date.season.name == "Eastertide"
        assert "Easter" in mp.date.primary.name

    def test_morning_prayer_epiphany(self, db):
        """Morning Prayer generates complete office for Epiphany."""
        # Use Epiphany 2025 (January 6)
        epiphany_date = date_class(2025, 1, 6)
        
        # Act
        mp = MorningPrayer(date=epiphany_date)
        
        # Assert - Basic structure
        assert mp is not None
        assert mp.date.date == epiphany_date
        
        # Assert - Commemoration is Epiphany
        assert "Epiphany" in mp.date.primary.name

    def test_morning_prayer_ash_wednesday(self, db):
        """Morning Prayer generates complete office for Ash Wednesday."""
        # Use Ash Wednesday 2025
        ash_wednesday = date_class(2025, 3, 5)
        
        # Act
        mp = MorningPrayer(date=ash_wednesday)
        
        # Assert - Basic structure
        assert mp is not None
        assert mp.date.date == ash_wednesday
        
        # Assert - Lenten season
        assert mp.date.season.name == "Lent"
        assert "Ash Wednesday" in mp.date.primary.name

    def test_morning_prayer_ascension(self, db):
        """Morning Prayer generates complete office for Ascension Day."""
        # Use Ascension Day 2025 (40 days after Easter = May 29)
        ascension_date = date_class(2025, 5, 29)
        
        # Act
        mp = MorningPrayer(date=ascension_date)
        
        # Assert - Basic structure
        assert mp is not None
        assert mp.date.date == ascension_date
        
        # Assert - Ascension commemoration
        assert "Ascension" in mp.date.primary.name

    def test_morning_prayer_pentecost(self, db):
        """Morning Prayer generates complete office for Pentecost."""
        # Use Pentecost 2025 (50 days after Easter = June 8)
        pentecost_date = date_class(2025, 6, 8)
        
        # Act
        mp = MorningPrayer(date=pentecost_date)
        
        # Assert - Basic structure
        assert mp is not None
        assert mp.date.date == pentecost_date
        
        # Assert - Pentecost commemoration
        assert "Pentecost" in mp.date.primary.name


@pytest.mark.integration
@pytest.mark.us1
class TestMorningPrayerRegularDay:
    """
    Test Morning Prayer on regular days (ferias).
    
    Validates: FR-001 (Complete Morning Prayer structure)
    Tasks: T038
    """

    def test_morning_prayer_ordinary_weekday(self, db):
        """Morning Prayer generates complete office for ordinary weekday."""
        # Use a regular Tuesday in ordinary time
        regular_date = date_class(2025, 6, 10)
        
        # Act
        mp = MorningPrayer(date=regular_date)
        
        # Assert - Basic structure
        assert mp is not None
        assert mp.name == "Morning Prayer"
        assert mp.date.date == regular_date
        
        # Assert - Modules generated
        modules = mp.modules
        assert modules is not None
        assert len(modules) >= 20, "Regular day MP should have at least 20 modules"
        
        # Assert - Office readings available
        assert mp.office_readings is not None
        assert isinstance(mp.office_readings, StandardOfficeDay)

    def test_morning_prayer_sunday_ordinary_time(self, db):
        """Morning Prayer generates complete office for Sunday in ordinary time."""
        # Use a Sunday in ordinary time (after Trinity Sunday)
        sunday_date = date_class(2025, 6, 15)
        
        # Act
        mp = MorningPrayer(date=sunday_date)
        
        # Assert - Basic structure
        assert mp is not None
        assert mp.date.date == sunday_date
        assert mp.date.date.weekday() == 6  # Sunday
        
        # Assert - Modules generated
        modules = mp.modules
        assert modules is not None
        assert len(modules) >= 20

    def test_morning_prayer_monday_epiphany_season(self, db):
        """Morning Prayer generates complete office for Monday in Epiphany season."""
        # Use Monday in Epiphany season
        monday_date = date_class(2025, 1, 13)
        
        # Act
        mp = MorningPrayer(date=monday_date)
        
        # Assert - Basic structure
        assert mp is not None
        assert mp.date.date == monday_date
        assert mp.date.date.weekday() == 0  # Monday
        
        # Assert - Epiphany season
        assert mp.date.season.name == "Epiphanytide"

    def test_morning_prayer_complete_modules_regular_day(self, db):
        """Morning Prayer includes all required modules on regular day."""
        # Use regular Wednesday
        regular_date = date_class(2025, 1, 15)
        
        # Act
        mp = MorningPrayer(date=regular_date)
        modules = mp.modules
        
        # Get module class names
        module_names = [m[0].__class__.__name__ for m in modules]
        
        # Assert - Essential sections present
        assert "MPHeading" in module_names
        assert "MPOpeningSentence" in module_names
        assert "Confession" in module_names
        assert "Invitatory" in module_names or "MPInvitatory" in module_names
        assert any("Psalm" in name for name in module_names)
        assert any("Reading" in name for name in module_names)
        assert any("Canticle" in name for name in module_names)
        assert "Creed" in module_names
        assert "Prayers" in module_names
        assert "Dismissal" in module_names

    def test_morning_prayer_weekday_variation(self, db):
        """Morning Prayer varies appropriately across weekdays."""
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
            mp = MorningPrayer(date=test_date)
            offices.append(mp)
        
        # Assert - All offices generated successfully
        assert len(offices) == 7
        
        # Assert - Each has complete module list
        for mp in offices:
            assert len(mp.modules) >= 20

    def test_morning_prayer_readings_present(self, db):
        """Morning Prayer includes both OT and NT readings on regular day."""
        # Use regular day
        regular_date = date_class(2025, 1, 15)
        
        # Act
        mp = MorningPrayer(date=regular_date)
        
        # Assert - Office readings include both readings
        assert mp.office_readings.mp_reading_1 is not None
        assert mp.office_readings.mp_reading_2 is not None
        assert len(mp.office_readings.mp_reading_1) > 0
        assert len(mp.office_readings.mp_reading_2) > 0

    def test_morning_prayer_psalms_present(self, db):
        """Morning Prayer includes psalm assignments on regular day."""
        # Use regular day
        regular_date = date_class(2025, 1, 15)
        
        # Act
        mp = MorningPrayer(date=regular_date)
        
        # Assert - Psalm assignments present
        assert mp.office_readings.mp_psalms is not None
        assert len(mp.office_readings.mp_psalms) > 0
        assert mp.thirty_day_psalter_day.mp_psalms is not None
        assert len(mp.thirty_day_psalter_day.mp_psalms) > 0
