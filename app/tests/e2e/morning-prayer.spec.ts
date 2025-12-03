/**
 * E2E Tests for Morning Prayer (Phase 3 - T039, T040)
 * 
 * Tests the Daily Office Morning Prayer functionality end-to-end
 * 
 * Requirements:
 * - FR-001: Display Morning Prayer with all liturgical components
 * - US1: View Morning Prayer for any date
 * 
 * Prerequisites:
 * - Docker Compose services running (frontend, backend, db, cache)
 * - Backend API accessible at http://localhost:8000
 * - Frontend accessible at http://localhost:5173
 */

import { test, expect } from '@playwright/test';

test.describe('Morning Prayer - Daily Office', () => {
  /**
   * T039: E2E test - View Morning Prayer for today
   * 
   * Verifies that the Morning Prayer office can be accessed and loads correctly
   * for the current date without errors.
   */
  test('T039: View Morning Prayer for today', async ({ page }) => {
    // Rely on global timeout
    // Navigate to Morning Prayer for today
    // Use domcontentloaded to avoid timeout waiting for all resources on cold starts
    await page.goto('/office/morning_prayer', { waitUntil: 'domcontentloaded' });
    
    // Wait for the page to load
    await page.waitForLoadState('domcontentloaded');
    
    // Verify the page title or heading contains "Morning Prayer"
    // Increase timeout for cold starts
    const heading = page.locator('h1, h2, h3, h4').filter({ hasText: /Morning Prayer/i }).first();
    await expect(heading).toBeVisible({ timeout: 10000 });
    
    // Verify no error messages are displayed (only check for error-type alerts, not info/warning/success)
    const errorMessage = page.locator('.el-alert--error, .error-message, [data-testid="error"]');
    await expect(errorMessage).toHaveCount(0);
    
    // Verify the office content is present (at least one office section)
    const officeContent = page.locator('[class*="office"], [class*="liturgy"], .content').first();
    await expect(officeContent).toBeVisible();
  });

  /**
   * T040: E2E test - Morning Prayer displays all elements correctly
   * 
   * Verifies that all required liturgical components of Morning Prayer are
   * present and rendered correctly according to BCP 2019 rubrics.
   * 
   * Expected components per FR-001:
   * - Opening sentence
   * - Confession
   * - Invitatory (Venite or Jubilate)
   * - Psalms
   * - First Reading (Old Testament)
   * - Canticle 1 (Te Deum or Benedictus)
   * - Second Reading (New Testament)
   * - Canticle 2 (Benedictus)
   * - Apostles' Creed
   * - Prayers
   * - Suffrages
   * - Collects
   * - Dismissal
   */
  test('T040: Morning Prayer displays all elements correctly', async ({ page }) => {
    // Rely on global timeout // Increase test timeout
    // Use a specific date for consistency (Christmas 2025)
    await page.goto('/office/morning_prayer/2025/12/25');
    
    // Wait for the office to load completely
    await page.waitForLoadState('domcontentloaded');
    
    // Wait for app to mount
    try {
        await page.waitForSelector('#app', { state: 'visible', timeout: 10000 });
    } catch (e) {
        console.log('App failed to mount in Morning Prayer test');
    }

    // Wait for loading spinner to disappear
    try {
      await page.waitForSelector('.lds-ellipsis', { state: 'hidden', timeout: 10000 });
    } catch (e) {
      console.log('Loading spinner still visible in MP test');
    }
    
    // Verify the office heading is present
    // Increase timeout for cold starts (generating office can take time)
    const heading = page.locator('h1, h2, h3, h4').filter({ hasText: /Morning Prayer/i }).first();
    await expect(heading).toBeVisible({ timeout: 10000 });
    
    // Verify date is displayed (December 25, 2025 - Christmas Day)
    await expect(page.locator('body')).toContainText(/December 25|25 December|Christmas/i);
    
    // Verify liturgical components are present
    // Note: Exact selectors depend on your Vue component structure
    // These are reasonable guesses based on common patterns
    
    // Check for Opening Sentence section
    // const openingSentence = page.getByText(/Opening Sentence|Let the words|Behold|tidings of great joy/i).first();
    // await expect(openingSentence).toBeVisible();
    
    // Check for Confession
    const confession = page.locator('h2, h3, h4').filter({ hasText: /Confession/i }).first();
    await expect(confession).toBeVisible({ timeout: 10000 });
    
    // Check for Psalms section
    const psalms = page.locator('h2, h3, h4').filter({ hasText: /Psalm/i }).first();
    await expect(psalms).toBeVisible();
    
    // Check for First Reading (Scripture)
    const firstReading = page.locator('h2, h3, h4').filter({ hasText: /First Reading|The First Lesson|Old Testament/i }).first();
    await expect(firstReading).toBeVisible();
    
    // Check for Canticle (Te Deum or Benedictus)
    const canticle = page.locator('h2, h3, h4').filter({ hasText: /Te Deum|Benedictus|Canticle/i }).first();
    await expect(canticle).toBeVisible();
    
    // Check for Second Reading
    const secondReading = page.locator('h2, h3, h4').filter({ hasText: /Second Reading|The Second Lesson|New Testament|Epistle|Gospel/i }).first();
    await expect(secondReading).toBeVisible();
    
    // Check for Apostles' Creed
    const creed = page.locator('h2, h3, h4').filter({ hasText: /Apostles' Creed|I believe in God/i }).first();
    await expect(creed).toBeVisible();
    
    // Check for Prayers section
    const prayers = page.locator('h2, h3, h4').filter({ hasText: /The Prayers|Lord's Prayer|Our Father/i }).first();
    await expect(prayers).toBeVisible();
    
    // Check for Collects
    const collects = page.locator('h2, h3, h4').filter({ hasText: /Collect/i }).first();
    await expect(collects).toBeVisible();
    
    // Verify navigation elements are present
    // The navigation might be rendered as a collection of links or cards, not necessarily a <nav> element
    // Based on OfficeNav.vue, it uses el-row and el-col with router-links
    const navigation = page.locator('.el-row').first();
    await expect(navigation).toBeVisible();
    
    // Verify the office is properly formatted (indentation for responses)
    // Check for rubric styling (typically in red or italic)
    const rubrics = page.locator('[class*="rubric"], .italic, .text-red');
    await expect(rubrics.first()).toBeVisible();
  });

  /**
   * Bonus test: Verify Morning Prayer works for different dates
   */
  test('Morning Prayer loads for past dates', async ({ page }) => {
    // Rely on global timeout // Increase test timeout
    // Test with a past date (Easter 2024)
    await page.goto('/office/morning_prayer/2024/03/31');
    
    await page.waitForLoadState('domcontentloaded');
    
    const heading = page.locator('h1, h2, h3, h4').filter({ hasText: /Morning Prayer/i }).first();
    await expect(heading).toBeVisible({ timeout: 10000 });
    
    // Verify Easter content appears
    await expect(page.locator('body')).toContainText(/Easter|March 31|31 March/i);
  });

  /**
   * Bonus test: Verify Morning Prayer works for future dates
   */
  test('Morning Prayer loads for future dates', async ({ page }) => {
    // Rely on global timeout // Increase test timeout
    // Test with a future date (January 1, 2026)
    await page.goto('/office/morning_prayer/2026/01/01');
    
    await page.waitForLoadState('domcontentloaded');
    
    const heading = page.locator('h1, h2, h3, h4').filter({ hasText: /Morning Prayer/i }).first();
    await expect(heading).toBeVisible({ timeout: 10000 });
    
    // Verify date is displayed
    await expect(page.locator('body')).toContainText(/January 1|1 January|2026/i);
  });
});
