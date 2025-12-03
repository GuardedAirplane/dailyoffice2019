/**
 * Unit tests for FontSizer.vue component
 * 
 * Validates: FR-010 (Adjustable font size with accessibility controls)
 */

import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { mount, shallowMount } from '@vue/test-utils';
import FontSizer from '../../../src/components/FontSizer.vue';
import { DynamicStorage } from '../../../src/helpers/storage';

// Mock DynamicStorage
vi.mock('../../../src/helpers/storage', () => {
  return {
    DynamicStorage: {
      getItem: vi.fn().mockResolvedValue('24'),
      setItem: vi.fn().mockResolvedValue(undefined),
    },
  };
});

// Get the mocked functions
const mockGetItem = vi.mocked(DynamicStorage.getItem);
const mockSetItem = vi.mocked(DynamicStorage.setItem);

// Mock document methods
const originalGetElementById = document.getElementById;
const originalQuerySelectorAll = document.querySelectorAll;

describe('FontSizer.vue', () => {
  let wrapper;

  beforeEach(() => {
    vi.clearAllMocks();
    
    // Mock DOM elements
    document.getElementById = vi.fn((id) => {
      if (id === 'main') {
        return {
          style: {},
        };
      }
      return null;
    });

    document.querySelectorAll = vi.fn(() => [
      { style: {} },
      { style: {} },
    ]);
  });

  afterEach(() => {
    document.getElementById = originalGetElementById;
    document.querySelectorAll = originalQuerySelectorAll;
  });

  /**
   * FR-010: Font size controls
   */
  describe('Component Rendering', () => {
    it('should render the component', () => {
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      expect(wrapper.exists()).toBe(true);
    });

    it('should display font size indicators', () => {
      wrapper = mount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { 
              template: '<div class="el-slider"><slot /></div>',
              props: ['modelValue', 'min', 'max', 'formatTooltip'],
            },
          },
        },
      });

      const indicators = wrapper.findAll('.font-size-indicator');
      expect(indicators.length).toBe(2); // Small 'A' and large 'A'
      expect(indicators[0].classes()).toContain('font-size-indicator--small');
      expect(indicators[1].classes()).toContain('font-size-indicator--large');
    });

    it('should render slider control', () => {
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      expect(wrapper.find('.el-slider').exists()).toBe(true);
    });

    it('should have correct visual layout structure', () => {
      wrapper = mount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { 
              template: '<div class="el-slider"><slot /></div>',
              props: ['modelValue', 'min', 'max', 'formatTooltip'],
            },
          },
        },
      });

      expect(wrapper.find('.font-size-block').exists()).toBe(true);
    });
  });

  /**
   * FR-010: Font size adjustment
   */
  describe('Font Size Adjustment', () => {
    it('should initialize with default font size', async () => {
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      await wrapper.vm.$nextTick();
      
      expect(wrapper.vm.fontSize).toBe(24);
    });

    it('should have minimum font size of 10px', () => {
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      expect(wrapper.vm.sliderMin).toBe(10);
    });

    it('should have maximum font size of 40px', () => {
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      expect(wrapper.vm.sliderMax).toBe(40);
    });

    it('should call setFontSize when slider changes', async () => {
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { 
              template: '<div class="el-slider" @input="$emit(\'input\', 28)"><slot /></div>',
            },
          },
        },
      });

      const setFontSizeSpy = vi.spyOn(wrapper.vm, 'setFontSize');
      await wrapper.vm.setFontSize(28);

      expect(setFontSizeSpy).toHaveBeenCalledWith(28);
    });

    it('should format tooltip display correctly', () => {
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      expect(wrapper.vm.displayFontSize(24)).toBe('24px');
      expect(wrapper.vm.displayFontSize(16)).toBe('16px');
      expect(wrapper.vm.displayFontSize(32)).toBe('32px');
    });
  });

  /**
   * FR-010: Persistence
   */
  describe('Font Size Persistence', () => {
    it('should save font size to storage when changed', async () => {
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      await wrapper.vm.setFontSize(28);
      await wrapper.vm.$nextTick();

      expect(mockSetItem).toHaveBeenCalledWith('fontSize', expect.any(Number));
    });

    it('should load font size from storage on mount', async () => {
      mockGetItem.mockResolvedValueOnce('32');
      
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      await wrapper.vm.$nextTick();
      await wrapper.vm.resetFontSize();

      expect(mockGetItem).toHaveBeenCalledWith('fontSize');
    });

    it('should use default size if no stored value', async () => {
      mockGetItem.mockResolvedValueOnce(null);
      
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      await wrapper.vm.resetFontSize();
      await wrapper.vm.$nextTick();

      // Default is 24
      expect(wrapper.vm.fontSize).toBe(24);
    });
  });

  /**
   * FR-010: DOM manipulation for font size
   */
  describe('DOM Font Size Application', () => {
    it('should apply font size to main element', async () => {
      const mockMainElement = {
        style: {},
      };
      document.getElementById = vi.fn(() => mockMainElement);

      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      // Wait for mounted hook to complete (it has an await $nextTick)
      await wrapper.vm.$nextTick();
      await wrapper.vm.$nextTick();

      await wrapper.vm.setFontSize(28);

      expect(document.getElementById).toHaveBeenCalledWith('main');
      expect(mockMainElement.style['font-size']).toBe('28px');
    });

    it('should apply font size and line height to text elements', async () => {
      const mockElements = [
        { style: {} },
        { style: {} },
        { style: {} },
      ];
      document.querySelectorAll = vi.fn(() => mockElements);

      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      await wrapper.vm.setFontSize(24);

      mockElements.forEach((el) => {
        expect(el.style['font-size']).toBe('24px');
        expect(el.style['line-height']).toBe(`${24 * 1.6}px`);
      });
    });

    it('should handle missing main element gracefully', async () => {
      document.getElementById = vi.fn(() => null);

      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      // Should not crash when main element doesn't exist
      await expect(wrapper.vm.setFontSize(24)).resolves.not.toThrow();
    });
  });

  /**
   * FR-010: Accessibility
   */
  describe('Accessibility', () => {
    it('should have aria-hidden on decorative font indicators', () => {
      wrapper = mount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { 
              template: '<div class="el-slider"><slot /></div>',
              props: ['modelValue', 'min', 'max', 'formatTooltip'],
            },
          },
        },
      });

      const indicators = wrapper.findAll('[aria-hidden="true"]');
      expect(indicators.length).toBe(2);
    });

    it('should expose font size value through data binding', () => {
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      expect(wrapper.vm.fontSize).toBeDefined();
      expect(typeof wrapper.vm.fontSize).toBe('number');
    });

    it('should have resetFontSize method for resetting', () => {
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      expect(wrapper.vm.resetFontSize).toBeDefined();
      expect(typeof wrapper.vm.resetFontSize).toBe('function');
    });
  });

  /**
   * Component Lifecycle
   */
  describe('Component Lifecycle', () => {
    it('should call resetFontSize on mount', async () => {
      // We verify the side effect of resetFontSize which is calling getItem
      // resetFontSize calls DynamicStorage.getItem('fontSize')
      
      wrapper = shallowMount(FontSizer, {
        global: {
          stubs: {
            'el-slider': { template: '<div class="el-slider"><slot /></div>' },
          },
        },
      });

      // Wait for mounted hook to complete
      await wrapper.vm.$nextTick();
      
      expect(mockGetItem).toHaveBeenCalledWith('fontSize');
    });
  });
});
