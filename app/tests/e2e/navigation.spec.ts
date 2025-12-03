/**
 * E2E Tests for Office Navigation (Phase 7 - T080, T081, T082)
 * 
 * Tests navigation between different Daily Office types
 * 
 * Requirements:
 * - FR-013: Navigation between office types
 * - US5: Navigate between offices while preserving date
 * 
 * Prerequisites:
 * - Docker Compose services running (frontend, backend, db, cache)
 * - Backend API accessible at http://localhost:8000
 * - Frontend accessible at http://localhost:5173
 */

import { test, expect } from '@playwright/test';

test.describe('Office Navigation', () => {
  /**
   * T080: E2E test - Navigate from Morning to Evening Prayer
   * 
   * Verifies that users can navigate from Morning Prayer to Evening Prayer
   * while maintaining the same date.
   */
  test('T080: Navigate from Morning to Evening Prayer', async ({ page }) => {
    const testDate = '2025/12/25';
    
    // Start at Morning Prayer
    await page.goto(`/office/morning_prayer/${testDate}`);
    
    // Wait for page to fully load and content to be visible
    await page.waitForLoadState('domcontentloaded');
    await expect(page.locator('h1').first()).toBeVisible({ timeout: 15000 });
    
    // Verify we're on Morning Prayer
    const mpHeading = page.locator('h1').first();
    await expect(mpHeading).toContainText(/Morning Prayer/i);
    
    // Scroll to top to ensure navigation links are visible
    await page.evaluate(() => window.scrollTo(0, 0));
    
    // Find and click Evening Prayer link
    const epLink = page.locator('a[href*="evening_prayer"]').first();
    await expect(epLink).toBeVisible({ timeout: 10000 });
    await epLink.scrollIntoViewIfNeeded();
    await epLink.click();
    
    // Wait for navigation to complete
    await page.waitForURL(/evening_prayer/, { timeout: 15000 });
    
    // Verify we're now on Evening Prayer
    const epHeading = page.locator('h1').first();
    await expect(epHeading).toContainText(/Evening Prayer/i);
    
    // Verify the date is preserved
    await expect(page.locator('body')).toContainText(/December 25|25 December|Christmas/i);
    
    // Verify URL contains the same date
    await expect(page).toHaveURL(/evening_prayer/);
    await expect(page).toHaveURL(new RegExp(testDate));
  });

  /**
   * T081: E2E test - Navigate from Evening to Midday Prayer
   * 
   * Verifies that users can navigate from Evening Prayer to Midday Prayer
   * while maintaining the same date.
   */
  test('T081: Navigate from Evening to Midday Prayer', async ({ page }) => {
    const testDate = '2025/12/25';
    
    // Start at Evening Prayer
    await page.goto(`/office/evening_prayer/${testDate}`);
    
    // Wait for page to fully load and content to be visible
    await page.waitForLoadState('domcontentloaded');
    await expect(page.locator('h1').first()).toBeVisible({ timeout: 15000 });
    
    // Verify we're on Evening Prayer
    const epHeading = page.locator('h1').first();
    await expect(epHeading).toContainText(/Evening Prayer/i);
    
    // Scroll to top to ensure navigation links are visible
    await page.evaluate(() => window.scrollTo(0, 0));
    
    // Find and click Midday Prayer link
    const middayLink = page.locator('a[href*="midday_prayer"]').first();
    await expect(middayLink).toBeVisible({ timeout: 10000 });
    await middayLink.scrollIntoViewIfNeeded();
    await middayLink.click();
    
    // Wait for navigation to complete
    await page.waitForURL(/midday_prayer/, { timeout: 15000 });
    
    // Verify we're now on Midday Prayer
    const middayHeading = page.locator('h1').first();
    await expect(middayHeading).toContainText(/Midday Prayer|Noonday Prayer/i);
    
    // Verify the date is preserved
    await expect(page.locator('body')).toContainText(/December 25|25 December|Christmas/i);
    
    // Verify URL contains the same date
    await expect(page).toHaveURL(/midday_prayer/);
    await expect(page).toHaveURL(new RegExp(testDate));
  });

  /**
   * T082: E2E test - Navigate from Midday to Compline
   * 
   * Verifies that users can navigate from Midday Prayer to Compline
   * while maintaining the same date.
   */
  test('T082: Navigate from Midday to Compline', async ({ page }) => {
    const testDate = '2025/12/25';
    
    // Start at Midday Prayer
    await page.goto(`/office/midday_prayer/${testDate}`);
    
    // Wait for page to fully load and content to be visible
    await page.waitForLoadState('domcontentloaded');
    await expect(page.locator('h1').first()).toBeVisible({ timeout: 15000 });

    // Verify we're on Midday Prayer
    const middayHeading = page.locator('h1').first();
    await expect(middayHeading).toContainText(/Midday Prayer|Noonday Prayer/i);
    
    // Scroll to top to ensure navigation links are visible
    await page.evaluate(() => window.scrollTo(0, 0));
    
    // Find and click Compline link
    const complineLink = page.locator('a[href*="compline"]').first();
    await expect(complineLink).toBeVisible({ timeout: 10000 });
    await complineLink.scrollIntoViewIfNeeded();
    await complineLink.click();
    
    // Wait for navigation to complete
    await page.waitForURL(/compline/, { timeout: 15000 });
    
    // Verify we're now on Compline
    const complineHeading = page.locator('h1').first();
    await expect(complineHeading).toContainText(/Compline/i);
    
    // Verify the date is preserved
    await expect(page.locator('body')).toContainText(/December 25|25 December|Christmas/i);
    
    // Verify URL contains the same date
    await expect(page).toHaveURL(/compline/);
    await expect(page).toHaveURL(new RegExp(testDate));
  });

  /**
   * Navigate from Compline back to Morning Prayer
   */
  test('Navigate from Compline to Morning Prayer', async ({ page }) => {
    const testDate = '2025/12/25';
    
    // Start at Compline
    await page.goto(`/office/compline/${testDate}`);
    
    // Wait for page to fully load and content to be visible
    await page.waitForLoadState('domcontentloaded');
    await expect(page.locator('h1').first()).toBeVisible({ timeout: 15000 });

    // Scroll to top to ensure navigation links are visible
    await page.evaluate(() => window.scrollTo(0, 0));

    // Find and click Morning Prayer link
    const mpLink = page.locator('a[href*="morning_prayer"]').first();
    await expect(mpLink).toBeVisible({ timeout: 10000 });
    await mpLink.scrollIntoViewIfNeeded();
    await mpLink.click();
    
    // Wait for navigation to complete
    await page.waitForURL(/morning_prayer/, { timeout: 15000 });
    
    // Verify we're now on Morning Prayer
    const mpHeading = page.locator('h1').first();
    await expect(mpHeading).toContainText(/Morning Prayer/i);
    
    // Verify the date is preserved
    await expect(page).toHaveURL(/morning_prayer/);
    await expect(page).toHaveURL(new RegExp(testDate));
  });

  /**
   * All navigation links are present and functional
   */
  test('All office navigation links are present', async ({ page }) => {
    await page.goto('/office/morning_prayer/2025/12/25');
    
    // Wait for hydration and nav links
    try {
      await page.waitForSelector('#app', { timeout: 10000 });
      await page.waitForSelector('a[href*="morning_prayer"]', { timeout: 10000 });
    } catch (e) {
      console.log('Wait timed out, continuing anyway');
    }

    // Check for links to all main offices
    // Use a more relaxed check for mobile where links might be in a scrollable area
    await expect(page.locator('a[href*="morning_prayer"]').first()).toBeVisible();
    await expect(page.locator('a[href*="evening_prayer"]').first()).toBeVisible();
    await expect(page.locator('a[href*="midday_prayer"]').first()).toBeVisible();
    await expect(page.locator('a[href*="compline"]').first()).toBeVisible();
  });

  /**
   * Date is preserved across multiple navigation steps
   */
  test('Date persists through multiple navigation steps', async ({ page }) => {
    const testDate = '2024/3/31'; // Easter 2024
    
    // Start at Morning Prayer
    await page.goto(`/office/morning_prayer/${testDate}`);
    await expect(page).toHaveURL(new RegExp(testDate));
    
    // Navigate to Evening Prayer
    await page.locator('a[href*="evening_prayer"]').first().click();
    await expect(page).toHaveURL(new RegExp(testDate));
    await expect(page.locator('body')).toContainText(/Easter|March 31|31 March/i);
    
    // Navigate to Compline
    await page.locator('a[href*="compline"]').first().click();
    await expect(page).toHaveURL(new RegExp(testDate));
    await expect(page.locator('body')).toContainText(/Easter|March 31|31 March/i);
    
    // Navigate back to Morning Prayer
    await page.locator('a[href*="morning_prayer"]').first().click();
    await expect(page).toHaveURL(new RegExp(testDate));
    await expect(page.locator('body')).toContainText(/Easter|March 31|31 March/i);
  });

  /**
   * Navigation works from today's office (no date in URL)
   */
  test('Navigation works from current day office', async ({ page }) => {
    // Go to today's Morning Prayer (no date specified)
    await page.goto('/office/morning_prayer');
    
    // Navigate to Evening Prayer
    await page.locator('a[href*="evening_prayer"]').first().click();
    
    // Verify we're on Evening Prayer
    const heading = page.locator('h1').first();
    await expect(heading).toContainText(/Evening Prayer/i);
    
    // Verify no errors (only check for error-type alerts, not info/warning/success)
    const errorMessage = page.locator('.el-alert--error, .error-message, [data-testid="error"]');
    await expect(errorMessage).toHaveCount(0);
  });

  /**
   * Navigation menu is accessible and properly labeled
   */
  test('Navigation menu is properly labeled', async ({ page }) => {
    await page.goto('/office/morning_prayer/2025/12/25');
    
    // Wait for hydration and nav links
    try {
      await page.waitForSelector('#app', { timeout: 10000 });
      await page.waitForSelector('a[href*="morning_prayer"]', { timeout: 10000 });
    } catch (e) {
      console.log('Wait timed out, continuing anyway');
    }

    // Check that navigation links have meaningful text
    const mpLink = page.locator('a[href*="morning_prayer"]').first();
    await expect(mpLink).toBeVisible();
    const mpText = await mpLink.textContent();
    expect(mpText?.toLowerCase()).toMatch(/morning/i);
    
    const epLink = page.locator('a[href*="evening_prayer"]').first();
    await expect(epLink).toBeVisible();
    const epText = await epLink.textContent();
    expect(epText?.toLowerCase()).toMatch(/evening/i);
  });

  /**
   * Browser back button works correctly
   */
  test('Browser back button navigates correctly', async ({ page }) => {
    const testDate = '2025/12/25';
    
    // Start at Morning Prayer
    await page.goto(`/office/morning_prayer/${testDate}`);
    
    // Navigate to Evening Prayer
    await page.locator('a[href*="evening_prayer"]').first().click();
    
    // Verify we are on Evening Prayer before going back
    const epHeading = page.locator('h1').first();
    await expect(epHeading).toContainText(/Evening Prayer/i);

    // Use browser back button
    await page.goBack();
    
    // Should be back on Morning Prayer
    const heading = page.locator('h1').first();
    await expect(heading).toContainText(/Morning Prayer/i);
    await expect(page).toHaveURL(/morning_prayer/);
  });
});
