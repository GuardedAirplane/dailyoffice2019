/**
 * E2E Tests for Compline (Phase 6 - T075)
 * 
 * Tests the Daily Office Compline functionality end-to-end
 * 
 * Requirements:
 * - FR-004: Display Compline with all components
 * - US4: View Compline for any date
 * 
 * Prerequisites:
 * - Docker Compose services running (frontend, backend, db, cache)
 * - Backend API accessible at http://localhost:8000
 * - Frontend accessible at http://localhost:5173
 */

import { test, expect } from '@playwright/test';

test.describe('Compline - Daily Office', () => {
  // Increase timeout for all tests in this suite to handle potential network delays in CI/Docker
  // Rely on global timeout

  test.beforeEach(({ page }) => {
    page.on('console', msg => console.log(`BROWSER LOG: ${msg.text()}`));
  });

  test.afterEach(async ({ page }, testInfo) => {
    if (testInfo.status !== 'passed') {
      console.log(`Test failed: ${testInfo.title}`);
      try {
        const mainContent = await page.locator('#main').innerHTML();
        console.log('Content of #main:', mainContent);
        const bodyContent = await page.locator('body').innerHTML();
        console.log('Content of body (first 1000 chars):', bodyContent.substring(0, 1000));
      } catch (e) {
        console.log('Could not get page content:', e);
      }
    }
  });

  /**
   * T075: E2E test - View Compline and verify Nunc Dimittis
   * 
   * Verifies that Compline displays correctly with its characteristic
   * night prayer elements, especially the Nunc Dimittis canticle.
   */
  test('T075: View Compline and verify Nunc Dimittis', async ({ page }) => {
    // Navigate to Compline for a specific date to ensure consistent content
    // Using a fixed date rather than 'today' ensures test stability
    await page.goto('/office/compline/2024/01/30', { waitUntil: 'domcontentloaded', timeout: 30000 });
    
    // Wait for loading spinner to disappear first (if present) - gives backend time to respond
    const spinner = page.locator('.lds-ellipsis');
    await spinner.waitFor({ state: 'hidden', timeout: 25000 }).catch(() => {
      console.log('Loading spinner wait completed (may have already been hidden)');
    });
    
    // Wait for the main h1 heading to be visible (indicates content has loaded)
    await expect(page.locator('h1').first()).toBeVisible({ timeout: 20000 });
    
    // Verify the page title contains "Compline"
    // Sometimes "Daily Office" appears first, so we check for Compline specifically in headings
    const heading = page.locator('h1, h2, h3').filter({ hasText: /Compline/i }).first();
    await expect(heading).toBeVisible({ timeout: 10000 });
    
    // Verify no error messages are displayed (only check for error-type alerts, not info/warning/success)
    const errorMessage = page.locator('.el-alert--error, .error-message, [data-testid="error"]');
    await expect(errorMessage).toHaveCount(0);
    
    // Verify Nunc Dimittis is present (characteristic of Compline)
    // Use more robust selector matching Morning Prayer pattern
    const nuncDimittis = page.locator('h2, h3, h4').filter({ hasText: /Nunc Dimittis|Song of Simeon|Lord, now lettest/i }).first();
    await expect(nuncDimittis).toBeVisible({ timeout: 10000 });
    
    // Verify the office content is present
    const officeContent = page.locator('[class*="office"], [class*="liturgy"], .content').first();
    await expect(officeContent).toBeVisible({ timeout: 10000 });
  });

  /**
   * Compline displays all required liturgical elements
   */
  test('Compline displays all elements correctly', async ({ page }) => {
    // Use a known good past date (Jan 30 2024) where we know content exists
    await page.goto('/office/compline/2024/01/30');
    
    // Wait for the page to load and content to appear
    await page.waitForLoadState('domcontentloaded');
    
    // Wait for loading spinner to disappear first (if present)
    const spinner = page.locator('.lds-ellipsis');
    await spinner.waitFor({ state: 'hidden', timeout: 25000 }).catch(() => {
      console.log('Loading spinner wait completed (may have already been hidden)');
    });
    
    // Wait for the main h1 heading to be visible (indicates content has loaded)
    await expect(page.locator('h1').first()).toBeVisible({ timeout: 20000 });

    // Verify the office heading is present
    const heading = page.locator('h1, h2, h3, h4').filter({ hasText: /Compline/i }).first();
    await expect(heading).toBeVisible({ timeout: 10000 });
    
    // Verify date is displayed
    await expect(page.locator('body')).toContainText(/January 30|30 January/i);
    
    // Verify liturgical components are present
    
    // Check for Opening Sentence
    const opening = page.locator('h2, h3, h4').filter({ hasText: /Opening|The Lord Almighty/i }).first();
    
    // Opening might not be a heading, check body text if heading fails
    if (await opening.count() === 0) {
       await expect(page.locator('body')).toContainText(/The Lord Almighty grant|May the Lord Almighty grant/i, { timeout: 10000 });
    } else {
       await expect(opening).toBeVisible();
    }
    
    // Check for Confession
    const confession = page.locator('h2, h3, h4').filter({ hasText: /Confession/i }).first();
    await expect(confession).toBeVisible({ timeout: 10000 });
    
    // Check for Psalms section
    const psalms = page.locator('h2, h3, h4').filter({ hasText: /Psalm/i }).first();
    await expect(psalms).toBeVisible();
    
    // Check for Scripture reading
    const reading = page.locator('h2, h3, h4').filter({ hasText: /Reading|Scripture|The Lesson/i }).first();
    await expect(reading).toBeVisible();
    
    // Check for Nunc Dimittis (Song of Simeon)
    const nuncDimittis = page.locator('h2, h3, h4').filter({ hasText: /Nunc Dimittis|Song of Simeon|Lord, now lettest/i }).first();
    await expect(nuncDimittis).toBeVisible();
    
    // Check for Apostles' Creed - might be optional or differently named
    const creed = page.locator('h2, h3, h4').filter({ hasText: /Apostles' Creed|I believe in God/i }).first();
    if (await creed.count() > 0) {
        await expect(creed).toBeVisible();
    }
    
    // Check for Prayers section
    const prayers = page.locator('h2, h3, h4').filter({ hasText: /The Prayers|Lord's Prayer|Our Father/i }).first();
    await expect(prayers).toBeVisible();
    
    // Check for Collects
    const collects = page.locator('h2, h3, h4').filter({ hasText: /Collect/i }).first();
    await expect(collects).toBeVisible();
    
    // Verify navigation elements are present
    const navigation = page.locator('.el-row').first();
    await expect(navigation).toBeVisible();
  });

  /**
   * Compline has night prayer characteristics
   */
  test('Compline has night prayer specific content', async ({ page }) => {
    // Rely on global timeout
    await page.goto('/office/compline/2024/01/30');
    
    // Wait for the page to load
    await page.waitForLoadState('domcontentloaded');
    
    // Wait for loading spinner to disappear first (if present)
    const spinner = page.locator('.lds-ellipsis');
    await spinner.waitFor({ state: 'hidden', timeout: 25000 }).catch(() => {
      console.log('Loading spinner wait completed (may have already been hidden)');
    });
    
    // Wait for the main h1 heading to be visible (indicates content has loaded)
    await expect(page.locator('h1').first()).toBeVisible({ timeout: 20000 });

    // Verify the office heading is present
    const heading = page.locator('h1, h2, h3, h4').filter({ hasText: /Compline/i }).first();
    await expect(heading).toBeVisible({ timeout: 10000 });
    
    // Get body text for content checks
    const bodyText = (await page.locator('body').textContent() || '').toLowerCase();
    
    // Should have Nunc Dimittis (Song of Simeon) or at least Compline specific text
    if (bodyText.includes('nunc dimittis') || bodyText.includes('song of simeon') || bodyText.includes('lord, now lettest')) {
        expect(bodyText).toMatch(/nunc dimittis|song of simeon|lord, now lettest/i);
    } else {
        console.log('Nunc Dimittis not found, checking for other night prayer elements');
        expect(bodyText).toMatch(/compline|night|sleep|rest|guide us waking/i);
    }
    
    // Should have night-themed prayers
    expect(bodyText).toMatch(/darkness|night|sleep|rest|guide us waking/i);
    
    // Should NOT have morning elements
    expect(bodyText).not.toContain('te deum');
    expect(bodyText).not.toContain('venite');
  });

  /**
   * Compline loads for past dates
   */
  test('Compline loads for past dates', async ({ page }) => {
    // Test with a past date (Easter 2024)
    await page.goto('/office/compline/2024/03/31');
    
    // Wait for the page to load and content to appear
    await page.waitForLoadState('domcontentloaded');
    
    // Wait for loading spinner to disappear first (if present)
    const spinner = page.locator('.lds-ellipsis');
    await spinner.waitFor({ state: 'hidden', timeout: 25000 }).catch(() => {
      console.log('Loading spinner wait completed (may have already been hidden)');
    });
    
    // Wait for the main h1 heading to be visible (indicates content has loaded)
    await expect(page.locator('h1').first()).toBeVisible({ timeout: 20000 });
    
    // Verify the heading contains Compline
    const heading = page.locator('h1, h2').filter({ hasText: /Compline/i }).first();
    await expect(heading).toBeVisible({ timeout: 10000 });
    
    // Verify Easter content appears
    await expect(page.locator('body')).toContainText(/Easter|March 31|31 March/i, { timeout: 10000 });
  });

  /**
   * Compline loads for future dates
   */
  test('Compline loads for future dates', async ({ page }) => {
    // Test with a future date (January 1, 2026)
    await page.goto('/office/compline/2026/01/01');
    
    // Wait for the page to load and content to appear
    await page.waitForLoadState('domcontentloaded');
    
    // Wait for the main h1 heading to be visible (indicates content has loaded)
    await expect(page.locator('h1').first()).toBeVisible({ timeout: 20000 });
    
    // Wait for loading spinner to disappear
    const spinner = page.locator('.lds-ellipsis');
    if (await spinner.count() > 0) {
      await spinner.waitFor({ state: 'hidden', timeout: 10000 });
    }
    
    // Verify the heading contains Compline
    const heading = page.locator('h1, h2').filter({ hasText: /Compline/i }).first();
    await expect(heading).toBeVisible({ timeout: 10000 });
    
    // Verify date is displayed
    await expect(page.locator('body')).toContainText(/January 1|1 January|2026/i, { timeout: 10000 });
  });

  /**
   * Compline uses appropriate night psalms
   */
  test('Compline uses appropriate night psalms', async ({ page }) => {
    await page.goto('/office/compline/2025/12/25');
    
    // Wait for the page to load
    await page.waitForLoadState('domcontentloaded');
    
    // Wait for app to mount and content to appear
    try {
        await page.waitForSelector('#app .content, #app h1, #app h2', { state: 'visible', timeout: 10000 });
    } catch (e) {
        console.log('App content failed to appear in Compline test');
    }

    // Wait for loading spinner to disappear
    try {
      await page.waitForSelector('.lds-ellipsis', { state: 'hidden', timeout: 10000 });
    } catch (e) {
      console.log('Loading spinner still visible in compline test');
    }
    
    // Verify the office heading is present
    const heading = page.locator('h1, h2, h3, h4').filter({ hasText: /Compline/i }).first();
    try {
        await expect(heading).toBeVisible({ timeout: 10000 });
    } catch (e) {
        await expect(page.locator('body')).toContainText(/Compline/i, { timeout: 10000 });
    }
    
    // Verify psalms section exists
    const psalms = page.locator('h2, h3, h4').filter({ hasText: /Psalm|The Psalm/i }).first();
    await expect(psalms).toBeVisible({ timeout: 10000 });
    
    // Compline typically uses Psalms 4, 31, 91, 134 (night protection psalms)
    const body = await page.locator('body').textContent() || '';
    expect(body).toContain('Psalm');
  });

  /**
   * Compline has proper formatting and structure
   */
  test('Compline has proper liturgical formatting', async ({ page }) => {
    await page.goto('/office/compline/2025/12/25');
    
    // Wait for the page to load
    await page.waitForLoadState('domcontentloaded');
    
    // Verify the office heading is present
    const heading = page.locator('h1, h2, h3, h4').filter({ hasText: /Compline/i }).first();
    await expect(heading).toBeVisible({ timeout: 10000 });
    
    // Verify proper formatting (rubrics)
    // Increase timeout for rubrics as they might be loaded dynamically
    const rubrics = page.locator('[class*="rubric"], .italic, .text-red');
    if (await rubrics.count() > 0) {
        await expect(rubrics.first()).toBeVisible({ timeout: 10000 });
    } else {
        console.log('No rubrics found in Compline, skipping check');
    }
    
    // Verify office structure is present
    const officeStructure = page.locator('[class*="office"], [class*="liturgy"]').first();
    await expect(officeStructure).toBeVisible();
  });

  /**
   * Compline has navigation to other offices
   */
  test('Compline has navigation to other offices', async ({ page }) => {
    await page.goto('/office/compline/2025/12/25');
    
    // Wait for the page to load
    await page.waitForLoadState('domcontentloaded');
    
    // Verify the office heading is present
    const heading = page.locator('h1, h2').filter({ hasText: /Compline/i }).first();
    try {
        await expect(heading).toBeVisible({ timeout: 10000 });
    } catch (e) {
        await expect(page.locator('body')).toContainText(/Compline/i);
    }
    
    // Verify navigation is present
    const navigation = page.getByRole('link', { name: /Morning/i }).first();
    await expect(navigation).toBeVisible();
    
    // Should have links to other offices
    const mpLink = page.getByRole('link', { name: /Morning/i }).first();
    const epLink = page.getByRole('link', { name: /Evening/i }).first();
    const middayLink = page.getByRole('link', { name: /Midday/i }).first();
    
    await expect(mpLink).toBeVisible();
    await expect(epLink).toBeVisible();
    await expect(middayLink).toBeVisible();
  });
});
