/**
 * Unit tests for OfficeNav.vue component
 * 
 * Validates: FR-013 (Calendar navigation - previous/next days, jump to date)
 * Validates: FR-018 (Family Prayer mode switching)
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount, shallowMount } from '@vue/test-utils';
import OfficeNav from '../../../src/components/OfficeNav.vue';

// Mock router
const mockRouter = {
  push: vi.fn(),
  currentRoute: {
    _value: {
      query: {},
    },
  },
};

// Mock DynamicStorage
vi.mock('../../../src/helpers/storage', () => ({
  DynamicStorage: {
    getItem: vi.fn().mockResolvedValue('office'),
    setItem: vi.fn().mockResolvedValue(undefined),
  },
}));

describe('OfficeNav.vue', () => {
  let wrapper;
  const testDate = new Date('2024-01-15'); // Monday

  beforeEach(() => {
    vi.clearAllMocks();
  });

  /**
   * FR-013: Navigation rendering
   */
  describe('Component Rendering', () => {
    it('should render the component', () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-row': { template: '<div><slot /></div>' },
            'el-col': { template: '<div><slot /></div>' },
            'el-card': { template: '<div class="el-card"><slot /></div>' },
            'router-link': { template: '<a><slot /></a>' },
          },
        },
      });

      expect(wrapper.exists()).toBe(true);
    });

    it('should display office type switcher for office mode', async () => {
      wrapper = mount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-row': { template: '<div class="el-row"><slot /></div>' },
            'el-col': { template: '<div class="el-col"><slot /></div>' },
            'el-card': { template: '<div class="el-card"><slot /></div>' },
            'router-link': { template: '<a><slot /></a>' },
          },
        },
      });

      await wrapper.vm.$nextTick();

      expect(wrapper.text()).toContain('Full Daily Office mode');
      expect(wrapper.text()).toContain('Switch to Family Prayer');
    });

    it('should display office type switcher for family mode', async () => {
      wrapper = mount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'family',
        },
        global: {
          stubs: {
            'el-row': { template: '<div class="el-row"><slot /></div>' },
            'el-col': { template: '<div class="el-col"><slot /></div>' },
            'el-card': { template: '<div class="el-card"><slot /></div>' },
            'router-link': { template: '<a><slot /></a>' },
          },
        },
      });

      await wrapper.vm.$nextTick();

      expect(wrapper.text()).toContain('Shorter Family Prayer mode');
      expect(wrapper.text()).toContain('Switch to full Daily Office');
    });
  });

  /**
   * FR-001, FR-002, FR-003, FR-004: Office navigation links
   */
  describe('Office Type Links', () => {
    it('should create links for all daily office types in office mode', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      await wrapper.vm.$nextTick();

      expect(wrapper.vm.links).toHaveLength(4);
      expect(wrapper.vm.links[0].name).toBe('morning_prayer');
      expect(wrapper.vm.links[1].name).toBe('midday_prayer');
      expect(wrapper.vm.links[2].name).toBe('evening_prayer');
      expect(wrapper.vm.links[3].name).toBe('compline');
    });

    it('should create correct URL paths for office links', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      await wrapper.vm.$nextTick();

      expect(wrapper.vm.links[0].to).toBe('/morning_prayer/2024/1/15');
      expect(wrapper.vm.links[1].to).toBe('/midday_prayer/2024/1/15');
      expect(wrapper.vm.links[2].to).toBe('/evening_prayer/2024/1/15');
      expect(wrapper.vm.links[3].to).toBe('/compline/2024/1/15');
    });

    it('should have text labels for office types', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      await wrapper.vm.$nextTick();

      expect(wrapper.vm.links[0].text).toContain('Morning');
      expect(wrapper.vm.links[1].text).toContain('Midday');
      expect(wrapper.vm.links[2].text).toContain('Evening');
      expect(wrapper.vm.links[3].text).toContain('Compline');
    });
  });

  /**
   * FR-018: Family Prayer navigation
   */
  describe('Family Prayer Links', () => {
    it('should create links for all family prayer types in family mode', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'family',
        },
      });

      await wrapper.vm.$nextTick();

      expect(wrapper.vm.links).toHaveLength(4);
      expect(wrapper.vm.links[0].name).toBe('morning_prayer');
      expect(wrapper.vm.links[1].name).toBe('midday_prayer');
      expect(wrapper.vm.links[2].name).toBe('early_evening_prayer');
      expect(wrapper.vm.links[3].name).toBe('close_of_day_prayer');
    });

    it('should create correct URL paths for family prayer links', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'family',
        },
      });

      await wrapper.vm.$nextTick();

      expect(wrapper.vm.links[0].to).toBe('/family/morning_prayer/2024/1/15');
      expect(wrapper.vm.links[1].to).toBe('/family/midday_prayer/2024/1/15');
      expect(wrapper.vm.links[2].to).toBe('/family/early_evening_prayer/2024/1/15');
      expect(wrapper.vm.links[3].to).toBe('/family/close_of_day_prayer/2024/1/15');
    });
  });

  /**
   * FR-013: Date navigation (previous/next/today)
   */
  describe('Date Navigation', () => {
    it('should create day navigation links', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      await wrapper.vm.$nextTick();

      expect(wrapper.vm.dayLinks).toHaveLength(3);
      expect(wrapper.vm.dayLinks[0].icon).toBe('left'); // Yesterday
      expect(wrapper.vm.dayLinks[1].selected).toBe(true); // Today
      expect(wrapper.vm.dayLinks[2].icon).toBe('right'); // Tomorrow
    });

    it('should format weekday names correctly', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate, // Monday, Jan 15, 2024
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      await wrapper.vm.$nextTick();

      expect(wrapper.vm.dayLinks[0].text).toBe('Sunday'); // Yesterday
      expect(wrapper.vm.dayLinks[1].text).toBe('Monday'); // Today
      expect(wrapper.vm.dayLinks[2].text).toBe('Tuesday'); // Tomorrow
    });

    it('should create correct paths for previous day', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      await wrapper.vm.$nextTick();

      // Previous day (Jan 14, 2024 - Sunday)
      expect(wrapper.vm.dayLinks[0].to).toBe('/morning_prayer/2024/1/14');
    });

    it('should create correct paths for next day', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      await wrapper.vm.$nextTick();

      // Next day (Jan 16, 2024 - Tuesday)
      expect(wrapper.vm.dayLinks[2].to).toBe('/morning_prayer/2024/1/16');
    });

    it('should handle month boundaries correctly', async () => {
      const endOfMonth = new Date('2024-01-31');
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: endOfMonth,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      await wrapper.vm.$nextTick();

      // Next day should be Feb 1
      expect(wrapper.vm.dayLinks[2].to).toBe('/morning_prayer/2024/2/1');
    });

    it('should handle year boundaries correctly', async () => {
      const endOfYear = new Date('2024-12-31');
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: endOfYear,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      await wrapper.vm.$nextTick();

      // Next day should be Jan 1, 2025
      expect(wrapper.vm.dayLinks[2].to).toBe('/morning_prayer/2025/1/1');
    });
  });

  /**
   * FR-013: Active state highlighting
   */
  describe('Active State Highlighting', () => {
    it('should apply selected class to current office', () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      expect(wrapper.vm.selectedClass('morning_prayer')).toBe('selected');
      expect(wrapper.vm.selectedClass('evening_prayer')).toBe('');
    });

    it('should apply hover class to non-selected offices', () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      expect(wrapper.vm.hoverClass('morning_prayer')).toBe('always');
      expect(wrapper.vm.hoverClass('evening_prayer')).toBe('hover');
    });
  });

  /**
   * FR-018: Service type switching
   */
  describe('Service Type Switching', () => {
    it('should toggle from office to family mode', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
        global: {
          mocks: {
            $router: mockRouter,
          },
        },
      });

      await wrapper.vm.toggleServiceType();

      expect(wrapper.vm.currentServiceType).toBe('family');
      expect(wrapper.vm.links).toHaveLength(4);
      expect(wrapper.vm.links[0].to).toContain('/family/');
    });

    it('should toggle from family to office mode', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'family',
        },
        global: {
          mocks: {
            $router: mockRouter,
          },
        },
      });

      await wrapper.vm.toggleServiceType();

      expect(wrapper.vm.currentServiceType).toBe('office');
      expect(wrapper.vm.links).toHaveLength(4);
      expect(wrapper.vm.links[0].to).not.toContain('/family/');
    });

    it('should redirect to daily office when switching from family', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'family',
        },
        global: {
          mocks: {
            $router: mockRouter,
          },
        },
      });

      await wrapper.vm.toggleServiceType();

      expect(mockRouter.push).toHaveBeenCalledWith(
        expect.stringContaining('/office/morning_prayer/')
      );
    });

    it('should redirect to family prayer when switching from office', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
        global: {
          mocks: {
            $router: mockRouter,
          },
        },
      });

      await wrapper.vm.toggleServiceType();

      expect(mockRouter.push).toHaveBeenCalledWith(
        expect.stringContaining('/family/morning_prayer/')
      );
    });

    it('should map evening_prayer to early_evening_prayer when switching to family', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'evening_prayer',
          serviceType: 'office',
        },
        global: {
          mocks: {
            $router: mockRouter,
          },
        },
      });

      await wrapper.vm.toggleServiceType();

      expect(mockRouter.push).toHaveBeenCalledWith(
        expect.stringContaining('/family/early_evening_prayer/')
      );
    });

    it('should map compline to close_of_day_prayer when switching to family', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'compline',
          serviceType: 'office',
        },
        global: {
          mocks: {
            $router: mockRouter,
          },
        },
      });

      await wrapper.vm.toggleServiceType();

      expect(mockRouter.push).toHaveBeenCalledWith(
        expect.stringContaining('/family/close_of_day_prayer/')
      );
    });
  });

  /**
   * Readings Link
   */
  describe('Readings Link', () => {
    it('should create readings link for current date', async () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      await wrapper.vm.$nextTick();

      expect(wrapper.vm.readingsLink).toBeDefined();
      expect(wrapper.vm.readingsLink.to).toBe('/readings/2024/1/15');
      expect(wrapper.vm.readingsLink.text).toContain("Day's Readings");
    });
  });

  /**
   * Component Props
   */
  describe('Component Props', () => {
    it('should receive calendarDate prop', () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      expect(wrapper.props('calendarDate')).toEqual(testDate);
    });

    it('should receive selectedOffice prop', () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      expect(wrapper.props('selectedOffice')).toBe('morning_prayer');
    });

    it('should receive serviceType prop with default value', () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
        },
      });

      expect(wrapper.props('serviceType')).toBe('office');
    });
  });

  /**
   * Scroll behavior
   */
  describe('Scroll Behavior', () => {
    it('should have scrollToTop method', () => {
      wrapper = shallowMount(OfficeNav, {
        props: {
          calendarDate: testDate,
          selectedOffice: 'morning_prayer',
          serviceType: 'office',
        },
      });

      expect(wrapper.vm.scrollToTop).toBeDefined();
      expect(typeof wrapper.vm.scrollToTop).toBe('function');
    });
  });
});
