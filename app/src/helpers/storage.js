import { Preferences } from '@capacitor/preferences';

/**
 * DynamicStorage - Client-side preference storage
 * 
 * Implements FR-023 (Client-side preference storage) and FR-024 (Settings persistence)
 * 
 * Provides a unified interface for storing user preferences using Capacitor Preferences API.
 * Preferences persist across browser sessions and app restarts.
 * 
 * Used for:
 * - Bible translation selection (FR-017)
 * - Liturgical customization settings (FR-026)
 * - All user-configurable settings
 * 
 * Related Tasks: T155, T156, T161, T162
 */
export const DynamicStorage = {
  setItem: async (key, value) => {
    // console.log("SET ITEM", key, value, typeof value);
    if (typeof value === 'number') {
      value = value.toString();
    }
    await Preferences.set({
      key: key,
      value: value,
    });
    return value;
  },
  getItem: async (key) => {
    try {
      const { value } = await Preferences.get({ key: key });
      // console.log("GET ITEM", key, value);
      return value;
    } catch {
      // console.log("ERROR", error);
      return '';
    }
  },
  deleteItem: async (key) => {
    await Preferences.remove({ key: key });
  },
};
