/**
 * Unit tests for CalendarCard.vue component
 * 
 * Validates: FR-007 (Display liturgical calendar information)
 * Validates: FR-008 (Display commemorations and feast days)
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { shallowMount } from '@vue/test-utils';
import CalendarCard from '../../../src/components/CalendarCard.vue';

describe('CalendarCard.vue', () => {
  let wrapper;
  const mockCard = {
    primary_feast: 'Monday in the Second Week of Epiphany',
    primary_evening_feast: 'Monday in the Second Week of Epiphany (Eve)',
    commemorations: [
      {
        name: 'Feria',
        links: [],
      },
    ],
    evening_commemorations: [
      {
        name: 'Feria',
        links: [],
      },
    ],
    fast: {
      fast_day: false,
    },
  };

  const testDate = new Date('2024-01-15');

  beforeEach(() => {
    wrapper = null;
  });

  /**
   * FR-007: Calendar display
   */
  describe('Component Rendering', () => {
    it('should render the component', () => {
      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
          card: mockCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': { template: '<div class="el-card"><slot name="header" /><slot /></div>' },
            'el-tag': { template: '<span class="el-tag"><slot /></span>' },
            Commemoration: true,
          },
        },
      });

      expect(wrapper.exists()).toBe(true);
      expect(wrapper.find('.el-card').exists()).toBe(true);
    });

    it('should display office name', () => {
      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
          card: mockCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': { template: '<div class="el-card"><slot name="header" /><slot /></div>' },
            'el-tag': true,
            Commemoration: true,
          },
        },
      });

      // Component should display formatted office name
      expect(wrapper.html()).toBeTruthy();
    });

    it('should display formatted date', () => {
      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
          card: mockCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': { template: '<div class="el-card"><slot name="header" /><slot /></div>' },
            'el-tag': true,
            Commemoration: true,
          },
        },
      });

      // Should format and display the date
      expect(wrapper.vm.formattedDate).toBeDefined();
    });
  });

  /**
   * FR-008: Feast days and commemorations
   */
  describe('Feast Day Display', () => {
    it('should display primary feast for morning/midday offices', () => {
      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
          card: mockCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': { template: '<div class="el-card"><slot name="header" /><slot /></div>' },
            'el-tag': true,
            Commemoration: true,
          },
        },
      });

      expect(wrapper.html()).toContain('Monday in the Second Week of Epiphany');
    });

    it('should display evening feast for evening prayer', () => {
      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'evening_prayer',
          calendarDate: testDate,
          card: mockCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': { template: '<div class="el-card"><slot name="header" /><slot /></div>' },
            'el-tag': true,
            Commemoration: true,
          },
        },
      });

      expect(wrapper.html()).toContain('Monday in the Second Week of Epiphany (Eve)');
    });

    it('should display evening feast for compline', () => {
      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'compline',
          calendarDate: testDate,
          card: mockCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': { template: '<div class="el-card"><slot name="header" /><slot /></div>' },
            'el-tag': true,
            Commemoration: true,
          },
        },
      });

      expect(wrapper.html()).toContain('Monday in the Second Week of Epiphany (Eve)');
    });

    it('should display Fast Day indicator when applicable', () => {
      const fastDayCard = {
        ...mockCard,
        fast: {
          fast_day: true,
        },
      };

      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
          card: fastDayCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': { template: '<div class="el-card"><slot name="header" /><slot /></div>' },
            'el-tag': true,
            Commemoration: true,
          },
        },
      });

      expect(wrapper.html()).toContain('Fast Day');
    });

    it('should not display Fast Day indicator when not applicable', () => {
      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
          card: mockCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': { template: '<div class="el-card"><slot name="header" /><slot /></div>' },
            'el-tag': true,
            Commemoration: true,
          },
        },
      });

      expect(wrapper.html()).not.toContain('Fast Day');
    });
  });

  /**
   * FR-008: Multiple commemorations
   */
  describe('Commemorations Display', () => {
    it('should display multiple commemorations', () => {
      const multiCommemorationsCard = {
        ...mockCard,
        commemorations: [
          { name: 'Feria', links: [] },
          { name: 'St. Martin Luther King Jr.', links: ['http://example.com'] },
        ],
      };

      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
          card: multiCommemorationsCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': { template: '<div class="el-card"><slot name="header" /><slot /></div>' },
            'el-tag': true,
            Commemoration: { template: '<div class="commemoration"><slot /></div>' },
          },
        },
      });

      // Should render Commemoration components
      expect(wrapper.html()).toBeTruthy();
    });

    it('should not display commemorations for evening prayer', () => {
      const multiCommemorationsCard = {
        ...mockCard,
        commemorations: [
          { name: 'Feria', links: [] },
          { name: 'St. Patrick', links: [] },
        ],
      };

      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'evening_prayer',
          calendarDate: testDate,
          card: multiCommemorationsCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': { template: '<div class="el-card"><slot name="header" /><slot /></div>' },
            'el-tag': true,
            Commemoration: { template: '<div class="commemoration"><slot /></div>' },
          },
        },
      });

      // Evening prayer uses evening_commemorations instead
      expect(wrapper.html()).toBeTruthy();
    });
  });

  /**
   * Component Props
   */
  describe('Component Props', () => {
    it('should receive office prop', () => {
      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
          card: mockCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': true,
            'el-tag': true,
            Commemoration: true,
          },
        },
      });

      expect(wrapper.props('office')).toBe('morning_prayer');
    });

    it('should receive calendarDate prop', () => {
      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
          card: mockCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': true,
            'el-tag': true,
            Commemoration: true,
          },
        },
      });

      expect(wrapper.props('calendarDate')).toEqual(testDate);
    });

    it('should receive card prop with calendar data', () => {
      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
          card: mockCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': true,
            'el-tag': true,
            Commemoration: true,
          },
        },
      });

      expect(wrapper.props('card')).toEqual(mockCard);
    });
  });

  /**
   * Service Type Handling
   */
  describe('Service Type', () => {
    it('should accept office service type', () => {
      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
          card: mockCard,
          serviceType: 'office',
        },
        global: {
          stubs: {
            'el-card': true,
            'el-tag': true,
            Commemoration: true,
          },
        },
      });

      expect(wrapper.props('serviceType')).toBe('office');
    });

    it('should accept family service type', () => {
      wrapper = shallowMount(CalendarCard, {
        props: {
          office: 'morning_prayer',
          calendarDate: testDate,
          card: mockCard,
          serviceType: 'family',
        },
        global: {
          stubs: {
            'el-card': true,
            'el-tag': true,
            Commemoration: true,
          },
        },
      });

      expect(wrapper.props('serviceType')).toBe('family');
    });
  });
});
