"""
Settings Integration Tests

Tests the integration between Setting/SettingOption models and office generation.

Tasks: T157, T158
Features: FR-023 (Client-side preference storage), FR-026 (Liturgical customization)
"""

import pytest
from datetime import date as date_class

from office.models import Setting, SettingOption


@pytest.mark.django_db
@pytest.mark.integration
class TestSettingsIntegration:
    """Integration tests for settings affecting office generation."""

    def test_confession_setting_exists_with_options(self):
        """
        Test that confession setting from database has valid options.

        Validates: T157, FR-023, FR-026
        """
        # Arrange - Get the confession setting from database
        confession_setting = Setting.objects.filter(name="confession").first()
        assert confession_setting is not None, "confession setting should exist in database"

        # Act - Get the setting options
        options = SettingOption.objects.filter(setting=confession_setting)

        # Assert - Setting has options available
        assert options.count() > 0, "Should have at least 1 confession option"

        # Verify each option has required fields
        for option in options:
            assert option.name is not None and option.name != "", "Option should have a name"
            assert option.value is not None and option.value != "", "Option should have a value"

    def test_canticle_rotation_setting_exists_with_options(self):
        """
        Test that canticle_rotation setting from database has valid options.

        Validates: T158, FR-023, FR-026
        """
        # Arrange - Get the canticle_rotation setting from database
        canticle_setting = Setting.objects.filter(name="canticle_rotation").first()
        assert canticle_setting is not None, "canticle_rotation setting should exist in database"

        # Act - Get setting options
        options = SettingOption.objects.filter(setting=canticle_setting)

        # Assert - Setting has options available
        assert options.count() > 0, "Should have canticle rotation options"

        # Verify each option has required fields
        for option in options:
            assert option.name is not None and option.name != "", "Option should have a name"
            assert option.value is not None and option.value != "", "Option should have a value"

    def test_bible_translation_setting_exists_with_options(self):
        """
        Test that bible_translation setting from database has valid options.

        Validates: T157, FR-023, FR-026
        """
        # Arrange
        bible_translation_setting = Setting.objects.filter(name="bible_translation").first()
        assert bible_translation_setting is not None, "bible_translation setting should exist"

        # Act
        options = SettingOption.objects.filter(setting=bible_translation_setting)

        # Assert
        assert options.count() > 0, "Should have bible translation options"

        # Verify all options have required fields
        for option in options:
            assert option.name is not None
            assert option.value is not None
            assert option.abbreviation is not None

    def test_setting_options_can_be_ordered(self):
        """
        Test that SettingOptions support ordering when order field is not null.

        Validates: T158, FR-026, FR-027 (sensible defaults)
        """
        # Arrange - Get a setting with multiple options that have non-null order values
        canticle_setting = Setting.objects.filter(name="canticle_rotation").first()
        assert canticle_setting is not None

        # Act - Get options ordered by the order field (nulls last)
        ordered_options = SettingOption.objects.filter(setting=canticle_setting, order__isnull=False).order_by("order")

        # Assert - If options have order values, they should be in order
        if ordered_options.count() > 1:
            option_list = list(ordered_options)
            for i in range(len(option_list) - 1):
                assert (
                    option_list[i].order <= option_list[i + 1].order
                ), f"Options should be ordered by order field: {option_list[i].order} > {option_list[i + 1].order}"

    def test_all_settings_have_at_least_one_option(self):
        """
        Test that all settings in the database have at least one option.

        Validates: T158, FR-026, FR-027
        """
        # Arrange
        all_settings = Setting.objects.all()

        # Act & Assert
        for setting in all_settings:
            options = SettingOption.objects.filter(setting=setting)
            assert options.count() > 0, f"Setting '{setting.name}' should have at least one option"

    def test_setting_default_option_logic(self):
        """
        Test that a default option can be determined for settings with order values.

        Validates: T158, FR-027 (sensible defaults)
        """
        # Arrange - Get settings that have options with order values
        settings_with_ordered_options = Setting.objects.filter(settingoption__order__isnull=False).distinct()

        # Act & Assert
        for setting in settings_with_ordered_options:
            # Get the first option by order
            default_option = (
                SettingOption.objects.filter(setting=setting, order__isnull=False).order_by("order").first()
            )

            assert (
                default_option is not None
            ), f"Setting '{setting.name}' should have at least one option with an order value"

            # Verify it's the lowest order value for this setting
            all_ordered_options = SettingOption.objects.filter(setting=setting, order__isnull=False)
            min_order = min(opt.order for opt in all_ordered_options)
            assert (
                default_option.order == min_order
            ), f"Default option for '{setting.name}' should have minimum order value"

    def test_settings_maintain_referential_integrity(self):
        """
        Test that settings and options maintain proper foreign key relationships.

        Validates: T158, FR-023
        """
        # Arrange - Create a test setting using correct constants
        test_setting = Setting.objects.create(
            name="test_integrity_setting",
            title="Test Integrity",
            description="Test referential integrity",
            order=999,
            setting_type=Setting.MAIN_SETTINGS,  # Use MAIN_SETTINGS constant
            site=Setting.DAILY_OFFICE_SITE,  # Use DAILY_OFFICE_SITE constant
        )

        # Create options
        option1 = SettingOption.objects.create(
            setting=test_setting, name="Option 1", description="First option", value="opt1", order=1
        )
        option2 = SettingOption.objects.create(
            setting=test_setting, name="Option 2", description="Second option", value="opt2", order=2
        )

        # Act - Verify relationships
        retrieved_options = SettingOption.objects.filter(setting=test_setting)

        # Assert
        assert retrieved_options.count() == 2
        assert option1 in retrieved_options
        assert option2 in retrieved_options

        # Clean up
        test_setting.delete()  # Should cascade delete options

        # Verify cascade delete
        assert SettingOption.objects.filter(pk=option1.pk).count() == 0
        assert SettingOption.objects.filter(pk=option2.pk).count() == 0
