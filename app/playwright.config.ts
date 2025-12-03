import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for E2E testing with Docker Compose
 * 
 * This configuration assumes services are running via docker-compose:
 * - Frontend: http://localhost:5173
 * - Backend API: http://localhost:8000
 * 
 * To run tests:
 * 1. Start services: docker-compose up -d
 * 2. Wait for services to be healthy
 * 3. Run tests: npm run test:e2e
 */
export default defineConfig({
  testDir: './tests/e2e',
  
  /* Maximum time one test can run for. */
  timeout: 60 * 1000,

  expect: {
    /**
     * Maximum time expect() should wait for the condition to be met.
     * For example in `await expect(locator).toHaveText();`
     */
    timeout: 30000
  },
  
  /* Run tests in files in parallel */
  fullyParallel: true,
  
  /* Fail the build on CI if you accidentally left test.only in the source code */
  forbidOnly: !!process.env.CI,
  
  /* Retry flaky tests - twice to handle browser rendering variability */
  retries: 2,
  
  /* Use 2 workers locally for stable parallel testing (12 was causing resource exhaustion) */
  workers: process.env.CI ? 1 : 2,
  
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['list'],
    process.env.CI ? ['github'] : ['line'],
  ],

  /* Shared settings for all the projects below */
  use: {
    /* Base URL to use in actions like `await page.goto('/')` */
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:5173',

    /* Maximum time each action such as `click()` can take. Defaults to 0 (no limit). */
    actionTimeout: 30000,

    /* Maximum time navigation can take. */
    navigationTimeout: 30000,
    
    /* Collect trace when retrying the failed test */
    trace: 'on-first-retry',
    
    /* Screenshot on failure */
    screenshot: 'only-on-failure',
    
    /* Video on failure - disabled for speed */
    video: 'off',
  },

  /* Configure projects for major browsers - reduced for speed */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },

    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    /* Mobile viewports - using same browsers to reduce overhead */
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  /* 
   * DO NOT use webServer here - services should be started via docker-compose
   * This allows proper networking between frontend/backend containers
   */
});
