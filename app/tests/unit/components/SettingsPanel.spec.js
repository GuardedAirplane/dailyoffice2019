/**
 * Unit tests for SettingsPanel.vue component
 * 
 * Validates: FR-016 (User-configurable liturgical settings)
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { shallowMount } from '@vue/test-utils';
import SettingsPanel from '../../../src/components/SettingsPanel.vue';

// Mock store
const mockStore = {
  state: {
    settings: {
      'Bible Translation': 'ESV',
      'Psalter': 'BCP 2019',
    },
  },
  commit: vi.fn(),
};

// Mock ElMessage
vi.mock('element-plus', () => ({
  ElMessage: vi.fn(),
}));

// Mock helper
vi.mock('../../../src/helpers/getMessageOffest', () => ({
  getMessageOffset: vi.fn(() => 50),
}));

describe('SettingsPanel.vue', () => {
  let wrapper;
  const mockAvailableSettings = [
    {
      uuid: '1',
      name: 'Bible Translation',
      title: 'Bible Translation',
      description: 'Select your preferred Bible translation',
      setting_type: 1,
      setting_string_order: 1,
      active: 'ESV',
      options: [
        {
          uuid: 'opt1',
          name: 'ESV',
          value: 'ESV',
          description: 'English Standard Version',
        },
        {
          uuid: 'opt2',
          name: 'NRSV',
          value: 'NRSV',
          description: 'New Revised Standard Version',
        },
        {
          uuid: 'opt3',
          name: 'KJV',
          value: 'KJV',
          description: 'King James Version',
        },
      ],
    },
    {
      uuid: '2',
      name: 'Psalter',
      title: 'Psalter Translation',
      description: 'Select your preferred Psalter',
      setting_type: 1,
      setting_string_order: 2,
      active: 'BCP 2019',
      options: [
        {
          uuid: 'opt4',
          name: 'BCP 2019',
          value: 'BCP 2019',
          description: 'Book of Common Prayer 2019 Psalter',
        },
        {
          uuid: 'opt5',
          name: 'Coverdale',
          value: 'Coverdale',
          description: 'Coverdale Psalter',
        },
      ],
    },
  ];

  beforeEach(() => {
    vi.clearAllMocks();
  });

  /**
   * FR-016: Settings panel rendering
   */
  describe('Component Rendering', () => {
    it('should render the component', () => {
      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: mockAvailableSettings,
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: false,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      expect(wrapper.exists()).toBe(true);
      expect(wrapper.find('form').exists()).toBe(true);
    });

    it('should render all available settings', () => {
      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: mockAvailableSettings,
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: false,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      const radioGroups = wrapper.findAll('.radio-group');
      expect(radioGroups.length).toBeGreaterThan(0);
    });

    it('should display setting titles', () => {
      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: mockAvailableSettings,
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: false,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      expect(wrapper.text()).toContain('Bible Translation');
      expect(wrapper.text()).toContain('Psalter Translation');
    });

    it('should display setting descriptions', () => {
      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: mockAvailableSettings,
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: false,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      expect(wrapper.text()).toContain('Select your preferred Bible translation');
      expect(wrapper.text()).toContain('Select your preferred Psalter');
    });
  });

  /**
   * FR-016: Setting options
   */
  describe('Setting Options', () => {
    it('should display all options for each setting', () => {
      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: mockAvailableSettings,
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: false,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      // Check Bible Translation options
      expect(wrapper.text()).toContain('ESV');
      expect(wrapper.text()).toContain('NRSV');
      expect(wrapper.text()).toContain('KJV');

      // Check Psalter options
      expect(wrapper.text()).toContain('BCP 2019');
      expect(wrapper.text()).toContain('Coverdale');
    });

    it('should display option descriptions', () => {
      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: mockAvailableSettings,
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: false,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      expect(wrapper.text()).toContain('English Standard Version');
      expect(wrapper.text()).toContain('New Revised Standard Version');
      expect(wrapper.text()).toContain('King James Version');
    });
  });

  /**
   * FR-016: Minor settings indicator
   */
  describe('Setting Types', () => {
    it('should display minor setting tag for type 2 settings', () => {
      const minorSetting = [
        {
          uuid: '3',
          name: 'Advanced Option',
          title: 'Advanced Setting',
          description: 'An advanced liturgical option',
          setting_type: 2, // Minor setting
          setting_string_order: 3,
          active: 'option1',
          options: [
            {
              uuid: 'opt6',
              name: 'Option 1',
              value: 'option1',
              description: 'First option',
            },
          ],
        },
      ];

      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: minorSetting,
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: false,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      expect(wrapper.text()).toContain('Minor Setting');
    });
  });

  /**
   * Component Props
   */
  describe('Component Props', () => {
    it('should receive availableSettings prop', () => {
      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: mockAvailableSettings,
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: false,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      expect(wrapper.props('availableSettings')).toEqual(mockAvailableSettings);
    });

    it('should receive site prop', () => {
      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: mockAvailableSettings,
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: false,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      expect(wrapper.props('site')).toBe('daily-office');
    });

    it('should receive advanced prop', () => {
      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: mockAvailableSettings,
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: true,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      expect(wrapper.props('advanced')).toBe(true);
    });
  });

  /**
   * FR-016: Settings interaction
   */
  describe('Settings Interaction', () => {
    it('should have changeSetting method', () => {
      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: mockAvailableSettings,
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: false,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      expect(wrapper.vm.changeSetting).toBeDefined();
      expect(typeof wrapper.vm.changeSetting).toBe('function');
    });

    it('should have showSetting method', () => {
      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: mockAvailableSettings,
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: false,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      expect(wrapper.vm.showSetting).toBeDefined();
      expect(typeof wrapper.vm.showSetting).toBe('function');
    });
  });

  /**
   * Empty State
   */
  describe('Empty State', () => {
    it('should handle empty availableSettings array', () => {
      wrapper = shallowMount(SettingsPanel, {
        props: {
          availableSettings: [],
          site: 'daily-office',
          name: 'Daily Office Settings',
          advanced: false,
        },
        global: {
          mocks: {
            $store: mockStore,
          },
          stubs: {
            RadioGroup: { template: '<div class="radio-group"><slot /></div>' },
            RadioGroupLabel: { template: '<div class="radio-group-label"><slot /></div>' },
            RadioGroupOption: { template: '<div class="radio-group-option"><slot /></div>' },
            RadioGroupDescription: { template: '<div class="radio-group-description"><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
          },
        },
      });

      expect(wrapper.find('form').exists()).toBe(true);
      // Should not crash with empty settings
    });
  });
});
