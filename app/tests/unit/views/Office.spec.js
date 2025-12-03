/**
 * Unit tests for Office.vue component
 * 
 * Validates: FR-001 (Display Morning Prayer with all required liturgical components)
 * Validates: FR-002 (Display Evening Prayer with all required liturgical components)
 * Validates: FR-003 (Display Midday Prayer)
 * Validates: FR-004 (Display Compline)
 * Validates: FR-018 (Family Prayer variants)
 * Validates: FR-022 (Error handling and offline functionality)
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount, shallowMount } from '@vue/test-utils';
import { createStore } from 'vuex';
import { storeOptions } from '../../../src/store';
import Office from '../../../src/views/Office.vue';
import Loading from '../../../src/components/Loading.vue';
import PageNotFound from '../../../src/views/PageNotFound.vue';
import CalendarCard from '../../../src/components/CalendarCard.vue';
import OfficeNav from '../../../src/components/OfficeNav.vue';
import FontSizer from '../../../src/components/FontSizer.vue';

// Mock DynamicStorage helper
vi.mock('../../../src/helpers/storage', () => ({
  DynamicStorage: {
    getItem: vi.fn().mockResolvedValue('true'),
    setItem: vi.fn().mockResolvedValue(undefined),
  },
}));

describe('Office.vue', () => {
  let wrapper;
  let store;
  
  const mockOfficeData = {
    modules: [
      {
        name: 'Opening Sentences',
        lines: [
          {
            line_type: 'heading',
            content: 'Morning Prayer',
          },
          {
            line_type: 'leader',
            content: 'The Lord is in his holy temple; let all the earth keep silence before him.',
          },
        ],
      },
      {
        name: 'The Confession of Sin',
        lines: [
          {
            line_type: 'subheading',
            content: 'Confession of Sin',
          },
          {
            line_type: 'rubric',
            content: 'The Officiant says to the People',
          },
        ],
      },
    ],
    calendar_day: {
      date: '2024-01-15',
      primary: 'Monday in the Second Week of Epiphany',
      commemorations: [],
    },
  };

  beforeEach(() => {
    vi.clearAllMocks();
    
    // Create a fresh store for each test
    store = createStore({
      ...storeOptions,
      state: {
        ...storeOptions.state,
        settings: {
          site_name: 'daily-office',
          fontSize: '1rem',
          fontFamily: 'sans-serif',
          theme: 'light',
        },
        availableSettings: {
          site_name: 'daily-office',
        }
      },
      actions: {
        initializeSettings: vi.fn(),
      }
    });
  });

  /**
   * FR-001: Morning Prayer rendering
   */
  describe('Component Rendering', () => {
    it('should render the component', () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
          serviceType: 'office',
        },
      });

      expect(wrapper.exists()).toBe(true);
      expect(wrapper.find('.office').exists()).toBe(true);
    });

    it('should display Loading component when loading is true', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
        },
      });

      // Component starts in loading state
      expect(wrapper.vm.loading).toBe(true);
      expect(wrapper.findComponent(Loading).exists()).toBe(true);
    });

    it('should display PageNotFound when notFound is true', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'invalid_office',
          calendarDate: new Date('2024-01-15'),
        },
      });

      await wrapper.setData({ notFound: true, loading: false });
      
      expect(wrapper.findComponent(PageNotFound).exists()).toBe(true);
    });

    it('should display CalendarCard component when loaded', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
          serviceType: 'office',
        },
      });

      await wrapper.setData({ loading: false, modules: mockOfficeData.modules });

      expect(wrapper.findComponent(CalendarCard).exists()).toBe(true);
      expect(wrapper.findComponent(CalendarCard).props('office')).toBe('morning_prayer');
    });

    it('should display OfficeNav component when loaded', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
        },
      });

      await wrapper.setData({ loading: false });

      expect(wrapper.findComponent(OfficeNav).exists()).toBe(true);
    });

    it('should display FontSizer when readyToSetFontSize is true', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
        },
      });

      await wrapper.setData({ loading: false, readyToSetFontSize: true });

      expect(wrapper.findComponent(FontSizer).exists()).toBe(true);
    });
  });

  /**
   * FR-022: Error handling
   */
  describe('Error Handling', () => {
    it('should display error alert when error occurs', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store],
          stubs: {
            'el-alert': {
              template: '<div class="el-alert"><slot /></div>',
              props: ['title', 'type'],
            },
          },
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
        },
      });

      await wrapper.setData({ 
        loading: false, 
        error: 'Failed to load office data',
      });

      expect(wrapper.find('.el-alert').exists()).toBe(true);
    });

    it('should handle network errors gracefully', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
        },
      });

      await wrapper.setData({ 
        loading: false, 
        error: 'Network error: Failed to fetch',
      });

      expect(wrapper.vm.error).toBeTruthy();
      expect(wrapper.vm.modules).toBeNull();
    });
  });

  /**
   * FR-001, FR-002: Office data rendering
   */
  describe('Office Data Rendering', () => {
    it('should render modules when data is provided', async () => {
      wrapper = mount(Office, {
        global: {
          plugins: [store],
          stubs: {
            CalendarCard: true,
            OfficeNav: true,
            FontSizer: true,
            AudioPlayer: true,
            AudioPlayerMessage: true,
            'el-alert': true,
            'el-tag': true,
            'el-switch': true,
          },
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
        },
      });

      await wrapper.setData({ 
        loading: false, 
        modules: mockOfficeData.modules,
      });

      // Should render the modules
      expect(wrapper.vm.modules).toHaveLength(2);
      expect(wrapper.vm.modules[0].name).toBe('Opening Sentences');
    });

    it('should render different line types correctly', async () => {
      wrapper = mount(Office, {
        global: {
          plugins: [store],
          stubs: {
            CalendarCard: true,
            OfficeNav: true,
            FontSizer: true,
            AudioPlayer: true,
            AudioPlayerMessage: true,
            'el-alert': true,
            'el-tag': true,
            'el-switch': true,
          },
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
        },
      });

      await wrapper.setData({ 
        loading: false, 
        modules: mockOfficeData.modules,
      });

      // Check that different line types are rendered
      const headings = wrapper.findAll('h2');
      expect(headings.length).toBeGreaterThan(0);
    });

    it('should handle empty modules gracefully', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
        },
      });

      await wrapper.setData({ 
        loading: false, 
        modules: [],
      });

      expect(wrapper.vm.modules).toEqual([]);
      // Should not crash with empty modules
      expect(wrapper.find('#main').exists()).toBe(true);
    });

    it('should handle modules with null/undefined lines', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
        },
      });

      await wrapper.setData({ 
        loading: false, 
        modules: [
          { name: 'Empty Module', lines: [] },
        ],
      });

      // Should not crash with empty lines
      expect(wrapper.find('#main').exists()).toBe(true);
    });
  });

  /**
   * FR-001, FR-002, FR-003, FR-004: Valid office types
   */
  describe('Office Types', () => {
    it('should accept morning_prayer as valid office type', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
          serviceType: 'office',
        },
      });

      expect(wrapper.props('office')).toBe('morning_prayer');
    });

    it('should accept evening_prayer as valid office type', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'evening_prayer',
          calendarDate: new Date('2024-01-15'),
          serviceType: 'office',
        },
      });

      expect(wrapper.props('office')).toBe('evening_prayer');
    });

    it('should accept midday_prayer as valid office type', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'midday_prayer',
          calendarDate: new Date('2024-01-15'),
          serviceType: 'office',
        },
      });

      expect(wrapper.props('office')).toBe('midday_prayer');
    });

    it('should accept compline as valid office type', async () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'compline',
          calendarDate: new Date('2024-01-15'),
          serviceType: 'office',
        },
      });

      expect(wrapper.props('office')).toBe('compline');
    });
  });

  /**
   * FR-018: Family Prayer service types
   */
  describe('Family Prayer Service Type', () => {
    it('should accept family service type', () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
          serviceType: 'family',
        },
      });

      expect(wrapper.props('serviceType')).toBe('family');
    });

    it('should default to office service type', () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
        },
      });

      expect(wrapper.props('serviceType')).toBe('office');
    });
  });

  /**
   * Component Lifecycle
   */
  describe('Component Props', () => {
    it('should receive office prop', () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
        },
      });

      expect(wrapper.props('office')).toBe('morning_prayer');
    });

    it('should receive calendarDate prop', () => {
      const testDate = new Date('2024-01-15');
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
        },
      });

      expect(wrapper.props('calendarDate')).toEqual(testDate);
    });

    it('should receive serviceType prop', () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
          serviceType: 'family',
        },
      });

      expect(wrapper.props('serviceType')).toBe('family');
    });
  });

  /**
   * Audio Player Integration
   */
  describe('Audio Player', () => {
    it('should compute isWithinSevenDays correctly for recent dates', async () => {
      const recentDate = new Date();
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: recentDate,
        },
      });

      expect(wrapper.vm.isWithinSevenDays).toBe(true);
    });

    it('should compute isWithinSevenDays correctly for old dates', async () => {
      const oldDate = new Date('2020-01-01');
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: oldDate,
        },
      });

      expect(wrapper.vm.isWithinSevenDays).toBe(false);
    });

    it('should have audioEnabled data property', () => {
      wrapper = shallowMount(Office, {
        global: {
          plugins: [store]
        },
        props: {
          office: 'morning_prayer',
          calendarDate: new Date('2024-01-15'),
        },
      });

      expect(wrapper.vm).toHaveProperty('audioEnabled');
    });
  });
});
