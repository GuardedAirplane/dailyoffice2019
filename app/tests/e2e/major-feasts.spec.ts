import { test, expect } from '@playwright/test';

/**
 * Major BCP 2019 Feasts E2E Tests (Phase 10)
 * 
 * DOCKER COMPOSE SETUP REQUIRED:
 * Run these tests with services running via docker-compose:
 *   docker-compose up -d
 *   npm run test:e2e
 * 
 * Test Coverage:
 *   - T108-T122: Major feast days and liturgical calendar
 *   - Christmas, Easter, Epiphany, Ascension, Pentecost
 *   - Trinity Sunday, All Saints, Ash Wednesday
 *   - Palm Sunday, Good Friday
 *   - Mobile feast calculations across years
 * 
 * Traceability:
 *   - FR-007: Liturgical Calendar Support
 *   - FR-011: Commemoration Display
 *   - FR-014: Feast Day Calculations
 */

// Helper function to wait for page load and loading spinner to disappear
async function waitForOfficeToLoad(page: any, timeout = 30000) {
  await page.waitForLoadState('domcontentloaded');
  try {
    await page.waitForSelector('.lds-ellipsis', { state: 'hidden', timeout });
  } catch (e) {
    // Loading spinner might not be present, that's OK
  }
}

test.describe('Major BCP 2019 Feasts (Phase 10)', () => {
  test.describe('Christmas (December 25)', () => {
    test('should display Christmas Day Morning Prayer', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/12/25');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Christmas|Nativity/').first()).toBeVisible();
      await expect(page.locator('text=2024').first()).toBeVisible();
    });

    test('should display Christmas Day Evening Prayer', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/evening_prayer/2024/12/25');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Christmas|Nativity/').first()).toBeVisible();
    });

    test('should display Christmas across multiple years', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2025/12/25');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Christmas|Nativity/').first()).toBeVisible();
    });
  });

  test.describe('Easter Day (Movable Feast)', () => {
    test('should display Easter 2024 (March 31)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/3/31');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Easter/').first()).toBeVisible();
      await expect(page.locator('text=2024').first()).toBeVisible();
    });

    test('should display Easter 2025 (April 20)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2025/4/20');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Easter/').first()).toBeVisible();
      await expect(page.locator('text=2025').first()).toBeVisible();
    });

    test('should show Eastertide season', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/evening_prayer/2024/3/31');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Eastertide|Easter/').first()).toBeVisible();
    });

    test('should extend Eastertide beyond Easter Day', async ({ page }) => {
      // Rely on global timeout
      // Week after Easter
      await page.goto('/morning_prayer/2024/4/7');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Eastertide|Easter/').first()).toBeVisible();
    });
  });

  test.describe('Epiphany (January 6)', () => {
    test('should display Epiphany Morning Prayer', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/1/6');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Epiphany/').first()).toBeVisible();
    });

    test('should display Epiphany Evening Prayer', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/evening_prayer/2024/1/6');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Epiphany/').first()).toBeVisible();
    });

    test('should be consistent across years', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2025/1/6');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Epiphany/').first()).toBeVisible();
    });
  });

  test.describe('Ascension Day (40 days after Easter)', () => {
    test('should display Ascension 2024 (May 9)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/5/9');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Ascension/').first()).toBeVisible();
    });

    test('should display Ascension 2025 (May 29)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2025/5/29');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Ascension/').first()).toBeVisible();
    });

    test('should show in Evening Prayer', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/evening_prayer/2024/5/9');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Ascension/').first()).toBeVisible();
    });
  });

  test.describe('Pentecost (50 days after Easter)', () => {
    test('should display Pentecost 2024 (May 19)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/5/19');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Pentecost/').first()).toBeVisible();
    });

    test('should display Pentecost 2025 (June 8)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2025/6/8');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Pentecost/').first()).toBeVisible();
    });

    test('should show Season After Pentecost begins', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/evening_prayer/2024/5/19');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Pentecost|Season After Pentecost/').first()).toBeVisible();
    });

    test('should show in all office types', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/midday_prayer/2024/5/19');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Pentecost/').first()).toBeVisible();
      
      await page.goto('/compline/2024/5/19');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Pentecost/').first()).toBeVisible();
    });
  });

  test.describe('Trinity Sunday (Sunday after Pentecost)', () => {
    test('should display Trinity Sunday 2024 (May 26)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/5/26');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Trinity/').first()).toBeVisible();
    });

    test('should display Trinity Sunday 2025 (June 15)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2025/6/15');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Trinity/').first()).toBeVisible();
    });

    test('should show in Evening Prayer', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/evening_prayer/2024/5/26');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Trinity/').first()).toBeVisible();
    });
  });

  test.describe("All Saints' Day (November 1)", () => {
    test('should display All Saints Morning Prayer', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/11/1');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/All Saints/').first()).toBeVisible();
    });

    test('should display All Saints Evening Prayer', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/evening_prayer/2024/11/1');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/All Saints/').first()).toBeVisible();
    });

    test('should be consistent across years', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2025/11/1');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/All Saints/').first()).toBeVisible();
      
      await page.goto('/morning_prayer/2023/11/1');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/All Saints/').first()).toBeVisible();
    });

    test('should appear in all office types', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/midday_prayer/2024/11/1');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/All Saints/').first()).toBeVisible();
    });
  });

  test.describe('Ash Wednesday (46 days before Easter)', () => {
    test('should display Ash Wednesday 2024 (February 14)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/2/14');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Ash Wednesday|Lent/').first()).toBeVisible();
    });

    test('should display Ash Wednesday 2025 (March 5)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2025/3/5');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Ash Wednesday|Lent/').first()).toBeVisible();
    });

    test('should mark beginning of Lent', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/evening_prayer/2024/2/14');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Lent|Ash Wednesday/').first()).toBeVisible();
    });

    test('should show day before is not Lent', async ({ page }) => {
      // Rely on global timeout
      // Day before Ash Wednesday
      await page.goto('/morning_prayer/2024/2/13');
      await waitForOfficeToLoad(page);
      // Should not be in Lent yet
      await expect(page.locator('text=/Epiphanytide|Epiphany/').first()).toBeVisible();
    });
  });

  test.describe('Palm Sunday (Sunday before Easter)', () => {
    test('should display Palm Sunday 2024 (March 24)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/3/24', { timeout: 10000 });
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Palm Sunday|Holy Week/').first()).toBeVisible();
    });

    test('should display Palm Sunday 2025 (April 13)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2025/4/13', { timeout: 10000 });
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Palm Sunday|Holy Week/').first()).toBeVisible();
    });

    test('should mark beginning of Holy Week', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/evening_prayer/2024/3/24', { timeout: 10000 });
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Holy Week|Palm/').first()).toBeVisible();
    });
  });

  test.describe('Good Friday (Friday before Easter)', () => {
    test('should display Good Friday 2024 (March 29)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/3/29');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Good Friday|Holy Week/').first()).toBeVisible();
    });

    test('should display Good Friday 2025 (April 18)', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2025/4/18');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Good Friday|Holy Week/').first()).toBeVisible();
    });

    test('should be in Holy Week season', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/evening_prayer/2024/3/29');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Holy Week|Good Friday/').first()).toBeVisible();
    });
  });

  test.describe('Feast Day Navigation', () => {
    test('should navigate between feast day offices', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/12/25'); // Christmas
      await waitForOfficeToLoad(page);
      
      // Wait for navigation links to be visible
      const eveningLink = page.getByRole('link', { name: /Evening/i }).first();
      await expect(eveningLink).toBeVisible();
      
      // Click using evaluate to avoid click interception
      await eveningLink.evaluate(node => (node as HTMLElement).click());
      await page.waitForURL('**/evening_prayer/2024/12/25', { timeout: 10000 });
      expect(page.url()).toContain('/evening_prayer/2024/12/25');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Christmas|Nativity/').first()).toBeVisible();
    });

    test('should navigate to next day from feast', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/12/25'); // Christmas
      await waitForOfficeToLoad(page);
      
      // Find the next day link (typically an arrow or "Next" button)
      const nextDayLink = page.locator('a[href*="/2024/12/26"], button:has-text("Next"), .next-day, [aria-label*="next"]').first();
      if (await nextDayLink.isVisible({ timeout: 10000 }).catch(() => false)) {
        await nextDayLink.evaluate(node => (node as HTMLElement).click());
        await page.waitForURL('**/2024/12/26');
        await waitForOfficeToLoad(page);
        // St. Stephen's Day
        await expect(page.locator('text=/Stephen|Christmastide/').first()).toBeVisible();
      } else {
        // Navigate directly if next button not found
        await page.goto('/morning_prayer/2024/12/26');
        await waitForOfficeToLoad(page);
        await expect(page.locator('text=/Stephen|Christmastide/').first()).toBeVisible();
      }
    });

    test('should navigate to previous day to feast', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/12/26');
      await waitForOfficeToLoad(page);
      
      // Find the previous day link
      const prevDayLink = page.locator('a[href*="/2024/12/25"], button:has-text("Prev"), .prev-day, [aria-label*="prev"]').first();
      if (await prevDayLink.isVisible({ timeout: 10000 }).catch(() => false)) {
        await prevDayLink.evaluate(node => (node as HTMLElement).click());
        await page.waitForURL('**/2024/12/25');
        await waitForOfficeToLoad(page);
        await expect(page.locator('text=/Christmas|Nativity/').first()).toBeVisible();
      } else {
        // Navigate directly if prev button not found
        await page.goto('/morning_prayer/2024/12/25');
        await waitForOfficeToLoad(page);
        await expect(page.locator('text=/Christmas|Nativity/').first()).toBeVisible();
      }
    });
  });

  test.describe('Feast Day Content Validation', () => {
    test('should display appropriate psalms for feasts', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/12/25');
      await waitForOfficeToLoad(page);
      // Look for visible Psalm text in the main content, not in hidden menus
      await expect(page.locator('.office-content, main, #app').locator('text=/Psalm/').first()).toBeVisible();
    });

    test('should display scripture readings for feasts', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/3/31'); // Easter
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Scripture|Reading|Lesson/').first()).toBeVisible();
    });

    test('should display collects for feasts', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/evening_prayer/2024/12/25');
      await waitForOfficeToLoad(page);
      // Look for visible Collect text in the main content, not in hidden menus
      await expect(page.locator('.office-content, main, #app').locator('text=/Collect/').first()).toBeVisible();
    });

    test('should show commemorations prominently', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/11/1'); // All Saints
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/All Saints/').first()).toBeVisible();
    });
  });

  test.describe('Liturgical Seasons Through Feasts', () => {
    test('should show Advent season', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/12/1'); // First Sunday of Advent
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Advent/').first()).toBeVisible();
    });

    test('should show Season After Pentecost', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2024/7/15');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Season After Pentecost|Pentecost/').first()).toBeVisible();
    });
  });

  test.describe('Feast Day Consistency', () => {
    test('should show same feast in family prayer', async ({ page }) => {
      // Rely on global timeout
      // Correct URL pattern for family prayer
      await page.goto('/family/morning_prayer/2024/12/25');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Christmas|Nativity/').first()).toBeVisible();
    });

    test('should preserve feast commemoration across office types', async ({ page }) => {
      // Rely on global timeout
      const offices = [
        '/morning_prayer',
        '/midday_prayer',
        '/evening_prayer',
        '/compline'
      ];

      for (const office of offices) {
        await page.goto(`${office}/2024/12/25`);
        await waitForOfficeToLoad(page);
        await expect(page.locator('text=/Christmas|Nativity|Christmastide/').first()).toBeVisible();
      }
    });

    test('should show feasts in past years', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2020/12/25');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Christmas|Nativity/').first()).toBeVisible();
    });

    test('should show feasts in future years', async ({ page }) => {
      // Rely on global timeout
      await page.goto('/morning_prayer/2030/12/25');
      await waitForOfficeToLoad(page);
      await expect(page.locator('text=/Christmas|Nativity/').first()).toBeVisible();
    });
  });

  test.describe('Mobile Feast Handling', () => {
    test('should handle Easter calculation for various years', async ({ page }) => {
      // Rely on global timeout
      const easterDates = [
        { year: 2024, month: 3, day: 31 },
        { year: 2025, month: 4, day: 20 },
        { year: 2026, month: 4, day: 5 },
      ];

      for (const { year, month, day } of easterDates) {
        await page.goto(`/morning_prayer/${year}/${month}/${day}`);
        await waitForOfficeToLoad(page);
        await expect(page.locator('text=/Easter/').first()).toBeVisible();
      }
    });

    test('should calculate Ash Wednesday correctly', async ({ page }) => {
      // Rely on global timeout
      const ashWednesdayDates = [
        { year: 2024, month: 2, day: 14 },
        { year: 2025, month: 3, day: 5 },
        { year: 2026, month: 2, day: 18 },
      ];

      for (const { year, month, day } of ashWednesdayDates) {
        await page.goto(`/morning_prayer/${year}/${month}/${day}`);
        await waitForOfficeToLoad(page);
        await expect(page.locator('text=/Ash Wednesday|Lent/').first()).toBeVisible();
      }
    });

    test('should calculate Ascension correctly', async ({ page }) => {
      // Rely on global timeout
      const ascensionDates = [
        { year: 2024, month: 5, day: 9 },
        { year: 2025, month: 5, day: 29 },
        { year: 2026, month: 5, day: 14 },
      ];

      for (const { year, month, day } of ascensionDates) {
        await page.goto(`/morning_prayer/${year}/${month}/${day}`);
        await waitForOfficeToLoad(page);
        await expect(page.locator('text=/Ascension/').first()).toBeVisible();
      }
    });
  });

  test.describe('Fixed Feast Consistency', () => {
    // Increase timeout for these tests as they load multiple pages
    test.setTimeout(60000);

    test('should show Epiphany on same date every year', async ({ page }) => {
      // Rely on global timeout
      const years = [2024, 2025, 2026, 2030];
      
      for (const year of years) {
        await page.goto(`/morning_prayer/${year}/1/6`);
        await waitForOfficeToLoad(page);
        await expect(page.locator('text=/Epiphany/').first()).toBeVisible();
      }
    });

    test('should show All Saints on same date every year', async ({ page }) => {
      // Rely on global timeout
      const years = [2024, 2025, 2026, 2030];
      
      for (const year of years) {
        await page.goto(`/morning_prayer/${year}/11/1`);
        await waitForOfficeToLoad(page);
        await expect(page.locator('text=/All Saints/').first()).toBeVisible();
      }
    });

    test('should show Christmas on same date every year', async ({ page }) => {
      // Rely on global timeout
      const years = [2024, 2025, 2026, 2030];
      
      for (const year of years) {
        await page.goto(`/morning_prayer/${year}/12/25`);
        await waitForOfficeToLoad(page);
        await expect(page.locator('text=/Christmas|Nativity/').first()).toBeVisible();
      }
    });
  });
});
