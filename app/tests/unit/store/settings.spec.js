/**
 * Unit tests for Vuex settings store module
 * 
 * Validates: FR-016 (User-configurable liturgical settings with persistence)
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createStore } from 'vuex';

// Mock dependencies
vi.mock('../../../src/helpers/storage', () => ({
  DynamicStorage: {
    getItem: vi.fn(),
    setItem: vi.fn(),
  },
}));

vi.mock('../../../src/router', () => ({
  default: {
    currentRoute: {
      _value: {
        query: {},
        fullPath: '/morning_prayer/2024/1/15',
      },
    },
    push: vi.fn(),
  },
}));

vi.mock('element-plus', () => ({
  ElMessage: {
    success: vi.fn(),
    warning: vi.fn(),
  },
}));

vi.mock('../../../src/helpers/getMessageOffest', () => ({
  getMessageOffset: vi.fn(() => 50),
}));

vi.mock('../../../src/helpers/decodeSettingsString', () => ({
  decodeSettingsString: vi.fn(() => []),
}));

// Import after mocks are set up
import { storeOptions } from '../../../src/store/index.js';
import { DynamicStorage } from '../../../src/helpers/storage';
import router from '../../../src/router';
import { ElMessage } from 'element-plus';

const mockDynamicStorage = vi.mocked(DynamicStorage);
const mockRouter = vi.mocked(router);
const mockElMessage = vi.mocked(ElMessage);

describe('Settings Store Module', () => {
  let store;

  beforeEach(() => {
    vi.clearAllMocks();
    mockDynamicStorage.getItem.mockResolvedValue(null);
    mockDynamicStorage.setItem.mockResolvedValue(undefined);
    mockRouter.currentRoute._value.query = {};
    
    // Create fresh store instance
    store = createStore(storeOptions);
  });

  /**
   * FR-016: Store state initialization
   */
  describe('Store State', () => {
    it('should initialize with default state', () => {
      expect(store.state.settings).toBe(false);
      expect(store.state.availableSettings).toBe(false);
    });

    it('should have settings property in state', () => {
      expect(store.state).toHaveProperty('settings');
    });

    it('should have availableSettings property in state', () => {
      expect(store.state).toHaveProperty('availableSettings');
    });
  });

  /**
   * FR-016: Mutations
   */
  describe('Mutations', () => {
    it('should have saveAvailableSettings mutation', () => {
      const availableSettings = [
        {
          name: 'Bible Translation',
          title: 'Bible Translation',
          options: [
            { value: 'ESV', abbreviation: 'esv' },
            { value: 'NRSV', abbreviation: 'nrsv' },
          ],
          setting_string_order: 1,
        },
      ];

      store.commit('saveAvailableSettings', availableSettings);

      expect(store.state.availableSettings).toEqual(availableSettings);
    });

    it('should have saveSettings mutation', async () => {
      const settings = {
        'Bible Translation': 'ESV',
        'Psalter': 'BCP 2019',
      };

      await store.commit('saveSettings', settings);

      expect(store.state.settings).toEqual(settings);
      expect(mockDynamicStorage.setItem).toHaveBeenCalledWith(
        'settings',
        JSON.stringify(settings)
      );
    });

    it('should persist settings to storage when saveSettings is called', async () => {
      const settings = {
        'Bible Translation': 'NRSV',
      };

      await store.commit('saveSettings', settings);

      expect(mockDynamicStorage.setItem).toHaveBeenCalledWith(
        'settings',
        JSON.stringify(settings)
      );
    });
  });

  /**
   * FR-016: Actions - Initialize settings
   */
  describe('Actions', () => {
    it('should have initializeSettings action', () => {
      expect(store._actions.initializeSettings).toBeDefined();
    });

    it('should initialize settings from storage', async () => {
      const storedSettings = JSON.stringify({
        'Bible Translation': 'KJV',
        'Psalter': 'Coverdale',
      });
      mockDynamicStorage.getItem.mockResolvedValueOnce(storedSettings);
      mockDynamicStorage.getItem.mockResolvedValueOnce(storedSettings);

      store.state.availableSettings = [
        {
          name: 'Bible Translation',
          title: 'Bible Translation',
          options: [{ value: 'ESV', abbreviation: 'esv' }],
          setting_string_order: 1,
        },
      ];

      await store.dispatch('initializeSettings');

      expect(mockDynamicStorage.getItem).toHaveBeenCalledWith('settings');
    });

    it('should set default values when no stored settings exist', async () => {
      mockDynamicStorage.getItem.mockResolvedValue(null);

      store.state.availableSettings = [
        {
          name: 'Bible Translation',
          title: 'Bible Translation',
          options: [
            { value: 'ESV', abbreviation: 'esv' },
            { value: 'NRSV', abbreviation: 'nrsv' },
          ],
          setting_string_order: 1,
        },
        {
          name: 'Psalter',
          title: 'Psalter',
          options: [
            { value: 'BCP 2019', abbreviation: 'bcp' },
            { value: 'Coverdale', abbreviation: 'cvd' },
          ],
          setting_string_order: 2,
        },
      ];

      await store.dispatch('initializeSettings');

      expect(store.state.settings['Bible Translation']).toBe('ESV');
      expect(store.state.settings['Psalter']).toBe('BCP 2019');
    });

    it('should save initialized settings to storage', async () => {
      mockDynamicStorage.getItem.mockResolvedValue(null);

      store.state.availableSettings = [
        {
          name: 'Bible Translation',
          title: 'Bible Translation',
          options: [{ value: 'ESV', abbreviation: 'esv' }],
          setting_string_order: 1,
        },
      ];

      await store.dispatch('initializeSettings');

      expect(mockDynamicStorage.setItem).toHaveBeenCalledWith(
        'settings',
        expect.any(String)
      );
    });

    it('should save setting abbreviations', async () => {
      mockDynamicStorage.getItem.mockResolvedValue(null);

      store.state.availableSettings = [
        {
          name: 'Bible Translation',
          title: 'Bible Translation',
          options: [
            { value: 'ESV', abbreviation: 'esv' },
            { value: 'NRSV', abbreviation: 'nrsv' },
          ],
          setting_string_order: 1,
        },
      ];

      await store.dispatch('initializeSettings');

      expect(mockDynamicStorage.setItem).toHaveBeenCalledWith(
        'settingAbbreviations',
        expect.any(String)
      );
    });

    it('should clear query parameters after initialization', async () => {
      mockDynamicStorage.getItem.mockResolvedValue(null);
      mockRouter.currentRoute._value.query = { 'Bible Translation': 'ESV' };

      store.state.availableSettings = [
        {
          name: 'Bible Translation',
          title: 'Bible Translation',
          options: [{ value: 'ESV', abbreviation: 'esv' }],
          setting_string_order: 1,
        },
      ];

      await store.dispatch('initializeSettings');

      expect(mockRouter.push).toHaveBeenCalledWith({
        path: '/morning_prayer/2024/1/15',
        query: {},
      });
    });
  });

  /**
   * FR-016: Query parameter settings
   */
  describe('Query Parameter Settings', () => {
    it('should apply settings from query parameters', async () => {
      mockDynamicStorage.getItem.mockResolvedValue(null);
      mockRouter.currentRoute._value.query = {
        'Bible Translation': 'KJV',
      };

      store.state.availableSettings = [
        {
          name: 'Bible Translation',
          title: 'Bible Translation',
          options: [
            { value: 'ESV', abbreviation: 'esv' },
            { value: 'KJV', abbreviation: 'kjv' },
          ],
          setting_string_order: 1,
        },
      ];

      await store.dispatch('initializeSettings');

      expect(store.state.settings['Bible Translation']).toBe('KJV');
    });

    it('should show success message when settings are applied from URL', async () => {
      mockDynamicStorage.getItem.mockResolvedValue(null);
      mockRouter.currentRoute._value.query = {
        'Bible Translation': 'NRSV',
      };

      store.state.availableSettings = [
        {
          name: 'Bible Translation',
          title: 'Bible Translation',
          options: [
            { value: 'ESV', abbreviation: 'esv' },
            { value: 'NRSV', abbreviation: 'nrsv' },
          ],
          setting_string_order: 1,
        },
      ];

      await store.dispatch('initializeSettings');

      expect(mockElMessage.success).toHaveBeenCalled();
    });
  });

  /**
   * FR-016: Additional collects from query
   */
  describe('Additional Collects', () => {
    it('should initialize extra collects from query parameters', async () => {
      mockDynamicStorage.getItem.mockResolvedValue(null);
      mockRouter.currentRoute._value.query = {
        morning_prayer_collects: 'collect1,collect2',
      };

      store.state.availableSettings = [
        {
          name: 'Bible Translation',
          title: 'Bible Translation',
          options: [{ value: 'ESV', abbreviation: 'esv' }],
          setting_string_order: 1,
        },
      ];

      await store.dispatch('initializeSettings');

      expect(mockDynamicStorage.setItem).toHaveBeenCalledWith(
        'extraCollects',
        expect.stringContaining('Morning Prayer')
      );
    });

    it('should handle multiple office collects from query', async () => {
      mockDynamicStorage.getItem.mockResolvedValue(null);
      mockRouter.currentRoute._value.query = {
        morning_prayer_collects: 'collect1',
        evening_prayer_collects: 'collect2',
      };

      store.state.availableSettings = [
        {
          name: 'Bible Translation',
          title: 'Bible Translation',
          options: [{ value: 'ESV', abbreviation: 'esv' }],
          setting_string_order: 1,
        },
      ];

      await store.dispatch('initializeSettings');

      expect(mockDynamicStorage.setItem).toHaveBeenCalledWith(
        'extraCollects',
        expect.any(String)
      );
    });
  });

  /**
   * Store structure validation
   */
  describe('Store Structure', () => {
    it('should have mutations object', () => {
      expect(store._mutations).toBeDefined();
    });

    it('should have actions object', () => {
      expect(store._actions).toBeDefined();
    });

    it('should have modules object', () => {
      expect(storeOptions.modules).toBeDefined();
      expect(storeOptions.modules).toEqual({});
    });

    it('should return state from initializeSettings action', async () => {
      mockDynamicStorage.getItem.mockResolvedValue(null);
      store.state.availableSettings = [];

      const result = await store.dispatch('initializeSettings');

      expect(result).toHaveProperty('settings');
      expect(result).toHaveProperty('availableSettings');
    });
  });
});
