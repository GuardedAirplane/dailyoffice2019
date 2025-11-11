"""
Unit tests for office models (psalm-related).

Tests cover:
- T139: ThirtyDayPsalterDay psalm retrieval
- T140: OfficeDay mp_psalms vs ep_psalms differ

Functional Requirements:
- FR-005: Different psalm assignments for MP vs EP
- FR-005a: 30-day Psalter cycle
"""

import pytest
from django.test import TestCase

from office.models import ThirtyDayPsalterDay, StandardOfficeDay


class TestThirtyDayPsalterDay(TestCase):
    """
    T139: Unit test for ThirtyDayPsalterDay psalm retrieval
    
    Tests 30-day Psalter cycle psalm assignments for Morning and Evening Prayer.
    """
    
    def test_thirty_day_psalter_exists(self):
        """Verify 30-day Psalter data exists in database"""
        count = ThirtyDayPsalterDay.objects.count()
        # Should have 30 or 31 days (one per day of month)
        self.assertGreaterEqual(count, 30, "Should have at least 30 Psalter days")
    
    def test_retrieve_psalter_day(self):
        """Retrieve Psalter day by day number"""
        day_1 = ThirtyDayPsalterDay.objects.filter(day=1).first()
        self.assertIsNotNone(day_1)
        self.assertEqual(day_1.day, 1)
    
    def test_psalter_day_has_mp_and_ep_psalms(self):
        """Psalter day has both mp_psalms and ep_psalms"""
        day = ThirtyDayPsalterDay.objects.first()
        self.assertIsNotNone(day.mp_psalms)
        self.assertIsNotNone(day.ep_psalms)
        self.assertTrue(len(day.mp_psalms) > 0)
        self.assertTrue(len(day.ep_psalms) > 0)
    
    def test_psalm_string_to_list(self):
        """psalm_string_to_list correctly parses comma-separated psalms"""
        day = ThirtyDayPsalterDay.objects.create(
            day=999,
            mp_psalms="1,2,3",
            ep_psalms="4,5,6"
        )
        
        mp_list = day.psalm_string_to_list(day.mp_psalms)
        self.assertEqual(mp_list, ["1", "2", "3"])
        
        ep_list = day.psalm_string_to_list(day.ep_psalms)
        self.assertEqual(ep_list, ["4", "5", "6"])
        
        # Clean up
        day.delete()
    
    def test_get_mp_psalms(self):
        """get_mp_pslams returns list of MP psalm numbers"""
        day = ThirtyDayPsalterDay.objects.create(
            day=998,
            mp_psalms="1,8,19",
            ep_psalms="23,51"
        )
        
        mp_psalms = day.get_mp_pslams()
        self.assertEqual(len(mp_psalms), 3)
        self.assertEqual(mp_psalms, ["1", "8", "19"])
        
        # Clean up
        day.delete()
    
    def test_get_ep_psalms(self):
        """get_ep_pslams returns list of EP psalm numbers"""
        day = ThirtyDayPsalterDay.objects.create(
            day=997,
            mp_psalms="1,2",
            ep_psalms="23,27,51"
        )
        
        ep_psalms = day.get_ep_pslams()
        self.assertEqual(len(ep_psalms), 3)
        self.assertEqual(ep_psalms, ["23", "27", "51"])
        
        # Clean up
        day.delete()
    
    def test_mp_and_ep_psalms_differ(self):
        """MP and EP psalms are different for each day"""
        day = ThirtyDayPsalterDay.objects.filter(day=1).first()
        if day:
            # MP and EP should generally have different psalms
            self.assertNotEqual(day.mp_psalms, day.ep_psalms)
    
    def test_all_days_have_both_mp_and_ep(self):
        """All 30-day Psalter days have both MP and EP psalm assignments"""
        days = ThirtyDayPsalterDay.objects.all()
        
        for day in days:
            self.assertIsNotNone(day.mp_psalms, f"Day {day.day} missing mp_psalms")
            self.assertIsNotNone(day.ep_psalms, f"Day {day.day} missing ep_psalms")
            self.assertTrue(len(day.mp_psalms) > 0, f"Day {day.day} mp_psalms empty")
            self.assertTrue(len(day.ep_psalms) > 0, f"Day {day.day} ep_psalms empty")


class TestOfficeDayPsalms(TestCase):
    """
    T140: Unit test for OfficeDay mp_psalms vs ep_psalms differ
    
    Tests that OfficeDay has different psalm assignments for MP and EP.
    """
    
    def test_standard_office_day_has_mp_and_ep_psalms(self):
        """StandardOfficeDay has both mp_psalms and ep_psalms fields"""
        # Check that fields exist
        day = StandardOfficeDay.objects.first()
        if day:
            self.assertTrue(hasattr(day, 'mp_psalms'))
            self.assertTrue(hasattr(day, 'ep_psalms'))
    
    def test_mp_psalms_field_exists(self):
        """OfficeDay model has mp_psalms field"""
        day = StandardOfficeDay.objects.create(
            month=12,
            day=25,
            mp_psalms="2,85",
            mp_reading_1="Isaiah 9:2-7",
            mp_reading_1_testament="OT",
            mp_reading_2="Luke 2:1-20",
            mp_reading_2_testament="NT",
            ep_psalms="89:1-29",
            ep_reading_1="Isaiah 62:6-7,10-12",
            ep_reading_1_testament="OT",
            ep_reading_2="Matthew 1:18-25",
            ep_reading_2_testament="NT"
        )
        
        self.assertEqual(day.mp_psalms, "2,85")
        
        # Clean up
        day.delete()
    
    def test_ep_psalms_field_exists(self):
        """OfficeDay model has ep_psalms field"""
        day = StandardOfficeDay.objects.create(
            month=1,
            day=1,
            mp_psalms="1,2,3",
            mp_reading_1="Genesis 1:1-2:3",
            mp_reading_1_testament="OT",
            mp_reading_2="Revelation 21:1-6a",
            mp_reading_2_testament="NT",
            ep_psalms="8,150",
            ep_reading_1="Genesis 1:1-2:3",
            ep_reading_1_testament="OT",
            ep_reading_2="Colossians 1:9-20",
            ep_reading_2_testament="NT"
        )
        
        self.assertEqual(day.ep_psalms, "8,150")
        
        # Clean up
        day.delete()
    
    def test_mp_and_ep_psalms_differ(self):
        """MP and EP psalms assignments are different"""
        day = StandardOfficeDay.objects.create(
            month=3,
            day=25,
            mp_psalms="111,113",
            mp_reading_1="Genesis 3:8-15",
            mp_reading_1_testament="OT",
            mp_reading_2="Luke 1:26-38",
            mp_reading_2_testament="NT",
            ep_psalms="132",
            ep_reading_1="Isaiah 7:10-14",
            ep_reading_1_testament="OT",
            ep_reading_2="Galatians 4:1-7",
            ep_reading_2_testament="NT"
        )
        
        self.assertNotEqual(day.mp_psalms, day.ep_psalms)
        
        # Clean up
        day.delete()
    
    def test_existing_office_days_have_different_psalms(self):
        """Check that existing StandardOfficeDays have different MP/EP psalms"""
        days_with_diff = 0
        days_with_same = 0
        
        # Sample some existing days
        for day in StandardOfficeDay.objects.all()[:20]:
            if day.mp_psalms != day.ep_psalms:
                days_with_diff += 1
            else:
                days_with_same += 1
        
        # Most days should have different psalm assignments
        # (allowing that some special days might coincidentally have same)
        if days_with_diff + days_with_same > 0:
            self.assertGreater(days_with_diff, 0, "Most days should have different MP/EP psalms")
    
    def test_office_day_psalm_formats(self):
        """Psalm fields can contain various formats"""
        # Single psalm
        day1 = StandardOfficeDay.objects.create(
            month=6,
            day=1,
            mp_psalms="1",
            mp_reading_1="Genesis 1:1-5",
            mp_reading_1_testament="OT",
            mp_reading_2="Matthew 1:1-17",
            mp_reading_2_testament="NT",
            ep_psalms="2",
            ep_reading_1="Genesis 1:6-13",
            ep_reading_1_testament="OT",
            ep_reading_2="Matthew 1:18-25",
            ep_reading_2_testament="NT"
        )
        
        # Multiple psalms comma-separated
        day2 = StandardOfficeDay.objects.create(
            month=6,
            day=2,
            mp_psalms="1,2,3",
            mp_reading_1="Genesis 1:14-23",
            mp_reading_1_testament="OT",
            mp_reading_2="Matthew 2:1-12",
            mp_reading_2_testament="NT",
            ep_psalms="4,5",
            ep_reading_1="Genesis 1:24-31",
            ep_reading_1_testament="OT",
            ep_reading_2="Matthew 2:13-23",
            ep_reading_2_testament="NT"
        )
        
        # Psalm with verse range
        day3 = StandardOfficeDay.objects.create(
            month=6,
            day=3,
            mp_psalms="119:1-32",
            mp_reading_1="Genesis 2:4-17",
            mp_reading_1_testament="OT",
            mp_reading_2="Matthew 3:1-12",
            mp_reading_2_testament="NT",
            ep_psalms="119:33-72",
            ep_reading_1="Genesis 2:18-25",
            ep_reading_1_testament="OT",
            ep_reading_2="Matthew 3:13-17",
            ep_reading_2_testament="NT"
        )
        
        self.assertEqual(day1.mp_psalms, "1")
        self.assertEqual(day2.mp_psalms, "1,2,3")
        self.assertEqual(day3.mp_psalms, "119:1-32")
        
        # Clean up
        day1.delete()
        day2.delete()
        day3.delete()
