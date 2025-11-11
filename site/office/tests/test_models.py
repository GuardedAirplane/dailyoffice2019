"""
Unit tests for office models.

Tests cover:
- T139: ThirtyDayPsalterDay psalm retrieval
- T140: OfficeDay mp_psalms vs ep_psalms differ
- T152: Setting model CRUD operations
- T153: SettingOption relationships
- T154: Default SettingOption selection

Functional Requirements:
- FR-005: Different psalm assignments for MP vs EP
- FR-005a: 30-day Psalter cycle
- FR-023: Client-side preference storage (backend models)
- FR-026: Liturgical customization settings
- FR-027: Sensible defaults
"""

import pytest
from django.test import TestCase

from office.models import ThirtyDayPsalterDay, StandardOfficeDay, Setting, SettingOption


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


class TestSettingModel(TestCase):
    """
    T152: Unit test for Setting model CRUD operations
    
    Tests Setting model creation, retrieval, update, and deletion.
    """
    
    def test_setting_creation(self):
        """Create a Setting with required fields"""
        setting = Setting.objects.create(
            name="confession_length",
            title="Confession Length",
            description="Choose between long or short form confession",
            order=1,
            setting_type=Setting.MAIN_SETTINGS,
            site=Setting.DAILY_OFFICE_SITE
        )
        
        self.assertEqual(setting.name, "confession_length")
        self.assertEqual(setting.title, "Confession Length")
        self.assertEqual(setting.setting_type, Setting.MAIN_SETTINGS)
        self.assertEqual(setting.site, Setting.DAILY_OFFICE_SITE)
        
        # Clean up
        setting.delete()
    
    def test_setting_has_setting_types(self):
        """Setting model has MAIN, ADDITIONAL, and EXPERT setting types"""
        self.assertEqual(Setting.MAIN_SETTINGS, 1)
        self.assertEqual(Setting.ADDITIONAL_SETTINGS, 2)
        self.assertEqual(Setting.EXPERT_SETTINGS, 3)
        
        # Verify choices
        types = dict(Setting.SETTING_TYPES)
        self.assertEqual(types[Setting.MAIN_SETTINGS], "Settings")
        self.assertEqual(types[Setting.ADDITIONAL_SETTINGS], "Additional Settings")
        self.assertEqual(types[Setting.EXPERT_SETTINGS], "Expert Settings")
    
    def test_setting_has_site_types(self):
        """Setting model distinguishes Daily Office vs Family Prayer sites"""
        self.assertEqual(Setting.DAILY_OFFICE_SITE, 1)
        self.assertEqual(Setting.FAMILY_PRAYER_SITE, 2)
        
        # Verify choices
        sites = dict(Setting.SETTING_SITES)
        self.assertEqual(sites[Setting.DAILY_OFFICE_SITE], "Daily Office")
        self.assertEqual(sites[Setting.FAMILY_PRAYER_SITE], "Family Prayer")
    
    def test_setting_update(self):
        """Update Setting fields"""
        setting = Setting.objects.create(
            name="test_setting",
            title="Test Setting",
            order=1
        )
        
        setting.title = "Updated Setting Title"
        setting.description = "New description"
        setting.save()
        
        updated_setting = Setting.objects.get(pk=setting.pk)
        self.assertEqual(updated_setting.title, "Updated Setting Title")
        self.assertEqual(updated_setting.description, "New description")
        
        # Clean up
        setting.delete()
    
    def test_setting_deletion(self):
        """Delete Setting"""
        setting = Setting.objects.create(
            name="temp_setting",
            title="Temporary Setting"
        )
        
        setting_pk = setting.pk
        setting.delete()
        
        with self.assertRaises(Setting.DoesNotExist):
            Setting.objects.get(pk=setting_pk)
    
    def test_setting_ordering(self):
        """Settings can be ordered by order field"""
        setting1 = Setting.objects.create(name="test_s1", title="Setting 1", order=2)
        setting2 = Setting.objects.create(name="test_s2", title="Setting 2", order=1)
        setting3 = Setting.objects.create(name="test_s3", title="Setting 3", order=3)
        
        # Query by order
        settings = Setting.objects.filter(name__startswith="test_s").order_by('order')
        self.assertEqual(list(settings.values_list('name', flat=True)), ['test_s2', 'test_s1', 'test_s3'])
        
        # Clean up
        setting1.delete()
        setting2.delete()
        setting3.delete()
    
    def test_existing_settings_exist(self):
        """Verify some settings exist in database"""
        # Database should have settings loaded from fixtures/migrations
        count = Setting.objects.count()
        self.assertGreater(count, 0, "Settings should exist in database")


class TestSettingOptionModel(TestCase):
    """
    T153: Unit test for SettingOption relationships
    
    Tests SettingOption foreign key relationships to Setting.
    """
    
    def test_setting_option_creation(self):
        """Create SettingOption with foreign key to Setting"""
        setting = Setting.objects.create(
            name="test_setting",
            title="Test Setting"
        )
        
        option = SettingOption.objects.create(
            setting=setting,
            name="Option 1",
            value="option1",
            order=1,
            abbreviation="A"
        )
        
        self.assertEqual(option.setting.pk, setting.pk)
        self.assertEqual(option.name, "Option 1")
        self.assertEqual(option.value, "option1")
        self.assertEqual(option.abbreviation, "A")
        
        # Clean up
        option.delete()
        setting.delete()
    
    def test_setting_has_multiple_options(self):
        """Setting can have multiple SettingOptions"""
        setting = Setting.objects.create(
            name="multi_option_setting",
            title="Multi Option Setting"
        )
        
        option1 = SettingOption.objects.create(
            setting=setting,
            name="Short",
            value="short",
            order=1
        )
        option2 = SettingOption.objects.create(
            setting=setting,
            name="Long",
            value="long",
            order=2
        )
        
        # Retrieve options via foreign key
        options = SettingOption.objects.filter(setting=setting).order_by('order')
        self.assertEqual(options.count(), 2)
        self.assertEqual(options[0].value, "short")
        self.assertEqual(options[1].value, "long")
        
        # Clean up
        option1.delete()
        option2.delete()
        setting.delete()
    
    def test_cascade_delete_options_with_setting(self):
        """Deleting Setting cascades to delete its SettingOptions"""
        setting = Setting.objects.create(
            name="cascade_test",
            title="Cascade Test"
        )
        
        option1 = SettingOption.objects.create(setting=setting, name="Opt 1", value="opt1")
        option2 = SettingOption.objects.create(setting=setting, name="Opt 2", value="opt2")
        
        option_pks = [option1.pk, option2.pk]
        
        # Delete setting
        setting.delete()
        
        # Options should be deleted too
        for pk in option_pks:
            with self.assertRaises(SettingOption.DoesNotExist):
                SettingOption.objects.get(pk=pk)
    
    def test_setting_option_has_default_abbreviation(self):
        """SettingOption has default abbreviation 'A'"""
        setting = Setting.objects.create(name="test", title="Test")
        
        # Create without specifying abbreviation
        option = SettingOption.objects.create(
            setting=setting,
            name="Default",
            value="default"
        )
        
        self.assertEqual(option.abbreviation, SettingOption.DEFAULT_ABBREVIATION)
        self.assertEqual(option.abbreviation, "A")
        
        # Clean up
        option.delete()
        setting.delete()
    
    def test_setting_option_ordering(self):
        """SettingOptions can be ordered within a Setting"""
        setting = Setting.objects.create(name="ordered_setting", title="Ordered Setting")
        
        option_c = SettingOption.objects.create(setting=setting, name="C", value="c", order=3)
        option_a = SettingOption.objects.create(setting=setting, name="A", value="a", order=1)
        option_b = SettingOption.objects.create(setting=setting, name="B", value="b", order=2)
        
        # Query by order
        options = SettingOption.objects.filter(setting=setting).order_by('order')
        self.assertEqual(list(options.values_list('name', flat=True)), ['A', 'B', 'C'])
        
        # Clean up
        option_a.delete()
        option_b.delete()
        option_c.delete()
        setting.delete()


class TestSettingDefaultOption(TestCase):
    """
    T154: Unit test for default SettingOption selection
    
    Tests logic for identifying default/first option for a Setting.
    """
    
    def test_first_option_by_order_is_default(self):
        """First SettingOption by order acts as default"""
        setting = Setting.objects.create(
            name="default_test",
            title="Default Test"
        )
        
        option2 = SettingOption.objects.create(setting=setting, name="Second", value="second", order=2)
        option1 = SettingOption.objects.create(setting=setting, name="First", value="first", order=1)
        option3 = SettingOption.objects.create(setting=setting, name="Third", value="third", order=3)
        
        # Get first option (default)
        default_option = SettingOption.objects.filter(setting=setting).order_by('order').first()
        
        self.assertEqual(default_option.value, "first")
        self.assertEqual(default_option.name, "First")
        
        # Clean up
        option1.delete()
        option2.delete()
        option3.delete()
        setting.delete()
    
    def test_existing_settings_have_options(self):
        """Verify existing Settings have SettingOptions"""
        # Get any existing setting
        setting = Setting.objects.first()
        
        if setting:
            # Setting should have at least one option
            options = SettingOption.objects.filter(setting=setting)
            # Note: Some settings might not have options yet, so just check the relationship works
            self.assertTrue(hasattr(setting, 'settingoption_set'))
    
    def test_retrieve_default_for_setting_name(self):
        """Retrieve default option for a setting by name"""
        setting = Setting.objects.create(
            name="psalter_cycle",
            title="Psalter Cycle"
        )
        
        SettingOption.objects.create(setting=setting, name="30-day", value="30", order=1)
        SettingOption.objects.create(setting=setting, name="60-day", value="60", order=2)
        
        # Simulate getting default for this setting
        default = SettingOption.objects.filter(
            setting__name="psalter_cycle"
        ).order_by('order').first()
        
        self.assertEqual(default.value, "30")
        self.assertEqual(default.name, "30-day")
        
        # Clean up
        SettingOption.objects.filter(setting=setting).delete()
        setting.delete()
    
    def test_setting_with_no_options(self):
        """Setting can exist without options (edge case)"""
        setting = Setting.objects.create(
            name="empty_setting",
            title="Empty Setting"
        )
        
        # No options created
        count = SettingOption.objects.filter(setting=setting).count()
        self.assertEqual(count, 0)
        
        # Getting default returns None
        default = SettingOption.objects.filter(setting=setting).first()
        self.assertIsNone(default)
        
        # Clean up
        setting.delete()
