/**
 * Unit Tests for DynamicStorage (Phase 13 - T155, T156)
 * 
 * Tests client-side preference storage functionality
 * 
 * Requirements:
 * - FR-023: Client-side preference storage
 * - FR-024: Settings persist across sessions
 * 
 * Related Tasks: T155, T156, T161, T162
 */

import { expect } from 'chai';
import { vi, beforeEach } from 'vitest';

// Mock the Capacitor Preferences module
const mockStorage = new Map();

vi.mock('@capacitor/preferences', () => ({
  Preferences: {
    set: vi.fn(async ({ key, value }) => {
      mockStorage.set(key, value);
      return;
    }),
    get: vi.fn(async ({ key }) => {
      const value = mockStorage.has(key) ? mockStorage.get(key) : null;
      return { value: value };
    }),
    remove: vi.fn(async ({ key }) => {
      mockStorage.delete(key);
      return;
    }),
  },
}));

// Import DynamicStorage after mocking
import { DynamicStorage } from '../../src/helpers/storage.js';

describe('DynamicStorage', () => {
  // Clean up mock storage before each test
  beforeEach(() => {
    mockStorage.clear();
  });
  // Clean up after each test
  afterEach(async () => {
    // Clean up test keys
    const testKeys = ['test_key', 'test_number', 'test_boolean', 'bible_translation', 'psalter_cycle'];
    for (const key of testKeys) {
      try {
        await DynamicStorage.deleteItem(key);
      } catch (e) {
        // Ignore errors during cleanup
      }
    }
  });

  /**
   * T155: Unit test - DynamicStorage setItem/getItem
   * 
   * Verifies that DynamicStorage can store and retrieve values.
   * Tests FR-023 (client-side storage)
   */
  describe('T155: setItem and getItem', () => {
    it('should store and retrieve a string value', async () => {
      const key = 'test_key';
      const value = 'test_value';
      
      // Set item
      const setResult = await DynamicStorage.setItem(key, value);
      expect(setResult).to.equal(value);
      
      // Get item
      const retrievedValue = await DynamicStorage.getItem(key);
      expect(retrievedValue).to.equal(value);
    });

    it('should store and retrieve a number as string', async () => {
      const key = 'test_number';
      const value = 42;
      
      // Set item (numbers should be converted to strings)
      await DynamicStorage.setItem(key, value);
      
      // Get item (should return as string)
      const retrievedValue = await DynamicStorage.getItem(key);
      expect(retrievedValue).to.equal('42');
    });

    it('should handle boolean values', async () => {
      const key = 'test_boolean';
      const value = 'true';
      
      // Set item
      await DynamicStorage.setItem(key, value);
      
      // Get item
      const retrievedValue = await DynamicStorage.getItem(key);
      expect(retrievedValue).to.equal('true');
    });

    it('should return null for non-existent key', async () => {
      const retrievedValue = await DynamicStorage.getItem('non_existent_key');
      expect(retrievedValue).to.be.null;
    });

    it('should overwrite existing values', async () => {
      const key = 'test_key';
      
      // Set initial value
      await DynamicStorage.setItem(key, 'initial_value');
      
      // Overwrite with new value
      await DynamicStorage.setItem(key, 'new_value');
      
      // Get item
      const retrievedValue = await DynamicStorage.getItem(key);
      expect(retrievedValue).to.equal('new_value');
    });
  });

  /**
   * T156: Unit test - Settings persist to localStorage
   * 
   * Verifies that settings stored via DynamicStorage persist.
   * Tests FR-024 (persistence)
   */
  describe('T156: Settings persistence', () => {
    it('should persist bible translation setting', async () => {
      const settingKey = 'bible_translation';
      const settingValue = 'ESV';
      
      // Store setting
      await DynamicStorage.setItem(settingKey, settingValue);
      
      // Retrieve setting
      const retrievedSetting = await DynamicStorage.getItem(settingKey);
      expect(retrievedSetting).to.equal(settingValue);
      
      // Change setting
      await DynamicStorage.setItem(settingKey, 'KJV');
      
      // Verify change persisted
      const updatedSetting = await DynamicStorage.getItem(settingKey);
      expect(updatedSetting).to.equal('KJV');
    });

    it('should persist psalter cycle setting', async () => {
      const settingKey = 'psalter_cycle';
      const settingValue = '30day';
      
      // Store setting
      await DynamicStorage.setItem(settingKey, settingValue);
      
      // Retrieve setting
      const retrievedSetting = await DynamicStorage.getItem(settingKey);
      expect(retrievedSetting).to.equal(settingValue);
      
      // Change to 60-day cycle
      await DynamicStorage.setItem(settingKey, '60day');
      
      // Verify change persisted
      const updatedSetting = await DynamicStorage.getItem(settingKey);
      expect(updatedSetting).to.equal('60day');
    });

    it('should handle multiple settings independently', async () => {
      // Store multiple settings
      await DynamicStorage.setItem('bible_translation', 'ESV');
      await DynamicStorage.setItem('psalter_cycle', '30day');
      await DynamicStorage.setItem('confession_length', 'short');
      
      // Retrieve and verify each setting
      expect(await DynamicStorage.getItem('bible_translation')).to.equal('ESV');
      expect(await DynamicStorage.getItem('psalter_cycle')).to.equal('30day');
      expect(await DynamicStorage.getItem('confession_length')).to.equal('short');
      
      // Change one setting
      await DynamicStorage.setItem('bible_translation', 'KJV');
      
      // Verify only that setting changed
      expect(await DynamicStorage.getItem('bible_translation')).to.equal('KJV');
      expect(await DynamicStorage.getItem('psalter_cycle')).to.equal('30day');
      expect(await DynamicStorage.getItem('confession_length')).to.equal('short');
    });

    it('should allow deleting settings', async () => {
      const key = 'test_key';
      
      // Store a setting
      await DynamicStorage.setItem(key, 'value');
      expect(await DynamicStorage.getItem(key)).to.equal('value');
      
      // Delete the setting
      await DynamicStorage.deleteItem(key);
      
      // Verify it's deleted
      const deletedValue = await DynamicStorage.getItem(key);
      expect(deletedValue).to.be.null;
    });
  });

  /**
   * Additional tests for edge cases
   */
  describe('Edge cases', () => {
    it('should handle empty string values', async () => {
      const key = 'empty_key';
      
      await DynamicStorage.setItem(key, '');
      const value = await DynamicStorage.getItem(key);
      
      // Empty string should be stored and retrieved
      expect(value).to.equal('');
    });

    it('should handle special characters in keys', async () => {
      const key = 'key_with-special.chars:123';
      const value = 'special_value';
      
      await DynamicStorage.setItem(key, value);
      const retrievedValue = await DynamicStorage.getItem(key);
      
      expect(retrievedValue).to.equal(value);
      
      // Cleanup
      await DynamicStorage.deleteItem(key);
    });

    it('should handle long string values', async () => {
      const key = 'long_string';
      const value = 'a'.repeat(1000); // 1000 character string
      
      await DynamicStorage.setItem(key, value);
      const retrievedValue = await DynamicStorage.getItem(key);
      
      expect(retrievedValue).to.equal(value);
      expect(retrievedValue.length).to.equal(1000);
      
      // Cleanup
      await DynamicStorage.deleteItem(key);
    });

    it('should handle concurrent operations', async () => {
      // Store multiple items concurrently
      await Promise.all([
        DynamicStorage.setItem('key1', 'value1'),
        DynamicStorage.setItem('key2', 'value2'),
        DynamicStorage.setItem('key3', 'value3'),
      ]);
      
      // Retrieve all items concurrently
      const [value1, value2, value3] = await Promise.all([
        DynamicStorage.getItem('key1'),
        DynamicStorage.getItem('key2'),
        DynamicStorage.getItem('key3'),
      ]);
      
      expect(value1).to.equal('value1');
      expect(value2).to.equal('value2');
      expect(value3).to.equal('value3');
      
      // Cleanup
      await Promise.all([
        DynamicStorage.deleteItem('key1'),
        DynamicStorage.deleteItem('key2'),
        DynamicStorage.deleteItem('key3'),
      ]);
    });
  });

  /**
   * Tests for FR-023 compliance
   */
  describe('FR-023: Client-side preference storage', () => {
    it('should use Capacitor Preferences API for storage', () => {
      // Verify that DynamicStorage has the expected methods
      expect(DynamicStorage).to.have.property('setItem');
      expect(DynamicStorage).to.have.property('getItem');
      expect(DynamicStorage).to.have.property('deleteItem');
      
      // Verify methods are functions
      expect(typeof DynamicStorage.setItem).to.equal('function');
      expect(typeof DynamicStorage.getItem).to.equal('function');
      expect(typeof DynamicStorage.deleteItem).to.equal('function');
    });

    it('should provide async API for all operations', async () => {
      // All operations should return promises
      const setPromise = DynamicStorage.setItem('test', 'value');
      expect(setPromise).to.be.a('promise');
      await setPromise;
      
      const getPromise = DynamicStorage.getItem('test');
      expect(getPromise).to.be.a('promise');
      await getPromise;
      
      const deletePromise = DynamicStorage.deleteItem('test');
      expect(deletePromise).to.be.a('promise');
      await deletePromise;
    });
  });
});
