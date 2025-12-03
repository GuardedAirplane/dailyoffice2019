/**
 * Accessibility testing helper using axe-core
 * 
 * Usage:
 * import { test, expect } from './helpers/axe';
 * 
 * test('page should be accessible', async ({ page, makeAxeBuilder }) => {
 *   await page.goto('/');
 *   const accessibilityScanResults = await makeAxeBuilder().analyze();
 *   expect(accessibilityScanResults.violations).toEqual([]);
 * });
 */

import { test as base, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

type AxeFixture = {
  makeAxeBuilder: () => AxeBuilder;
};

export const test = base.extend<AxeFixture>({
  makeAxeBuilder: async ({ page }, use) => {
    await use(() => new AxeBuilder({ page }));
  },
});

export { expect };
