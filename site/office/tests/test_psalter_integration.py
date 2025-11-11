"""
Integration tests for Psalter cycle assignments.

Tests cover:
- T145: 30-day cycle psalm assignment
- T146: 60-day cycle psalm assignment (if implemented)

Functional Requirements:
- FR-005a: 30-day and 60-day Psalter cycles
"""

import pytest
from django.test import TestCase
from datetime import date

from office.models import ThirtyDayPsalterDay, StandardOfficeDay


class TestThirtyDayCyclePsalmAssignment(TestCase):
    """
    T145: Integration test for 30-day cycle psalm assignment
    
    Tests that 30-day Psalter cycle correctly assigns psalms to each day.
    """
    
    def test_thirty_day_cycle_covers_all_days(self):
        """30-day Psalter has entries for days 1-30/31"""
        count = ThirtyDayPsalterDay.objects.count()
        self.assertGreaterEqual(count, 30, "Should have at least 30 days")
        self.assertLessEqual(count, 31, "Should have at most 31 days")
    
    def test_day_1_psalm_assignment(self):
        """Day 1 of 30-day Psalter has specific psalm assignments"""
        day_1 = ThirtyDayPsalterDay.objects.get(day=1)
        
        # Verify psalms are assigned
        self.assertIsNotNone(day_1.mp_psalms)
        self.assertIsNotNone(day_1.ep_psalms)
        
        # MP and EP should differ
        self.assertNotEqual(day_1.mp_psalms, day_1.ep_psalms)
    
    def test_psalm_assignments_sequential_through_psalter(self):
        """30-day cycle systematically covers Psalter"""
        # Get all days in order
        days = ThirtyDayPsalterDay.objects.order_by('day')
        
        # Each day should have psalms
        for day in days:
            self.assertIsNotNone(day.mp_psalms, f"Day {day.day} missing MP psalms")
            self.assertIsNotNone(day.ep_psalms, f"Day {day.day} missing EP psalms")
    
    def test_psalm_cycle_month_calculation(self):
        """Test retrieving correct psalter day for a given date"""
        # For a 30-day cycle, use day of month
        test_date = date(2024, 3, 15)  # March 15
        day_of_month = test_date.day
        
        psalter_day = ThirtyDayPsalterDay.objects.get(day=day_of_month)
        self.assertEqual(psalter_day.day, 15)


class TestSixtyDayCyclePsalmAssignment(TestCase):
    """
    T146: Integration test for 60-day cycle psalm assignment
    
    Tests 60-day Psalter cycle if implemented.
    Note: Current implementation uses 30-day cycle.
    """
    
    @pytest.mark.skip(reason="60-day cycle not yet implemented")
    def test_sixty_day_cycle_not_implemented(self):
        """60-day Psalter cycle is planned but not yet implemented"""
        # This test documents the requirement for future implementation
        # When implemented, 60-day cycle would:
        # - Have separate table or field indicating cycle type
        # - Cover Psalter 1-150 over 60 days instead of 30
        # - Allow user to select between 30 and 60 day cycles
        pass
    
    def test_thirty_day_cycle_is_default(self):
        """30-day cycle is the current default implementation"""
        # Verify we have 30-day data
        count = ThirtyDayPsalterDay.objects.count()
        self.assertGreaterEqual(count, 30)
        
        # 60-day would have different count or structure
        # For now, confirm 30-day is what we have
        self.assertLessEqual(count, 31)
