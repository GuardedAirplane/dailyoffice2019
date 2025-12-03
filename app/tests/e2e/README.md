# E2E Testing with Playwright and Docker Compose

This directory contains end-to-end tests using Playwright that run against the full application stack via Docker Compose.

## Prerequisites

- Docker or Podman with Docker Compose
- Node.js 20+ (for running Playwright tests)
- Playwright browsers installed: `npm run test:e2e:install`

## Running Tests

### 1. Start the Docker Compose stack

```bash
# From the project root
docker-compose up -d

# Wait for services to be healthy (about 30-60 seconds)
docker-compose ps
```

### 2. Run the E2E tests

```bash
# From the app/ directory
cd app

# Run all tests (headless mode)
npm run test:e2e

# Run tests with UI mode (interactive)
npm run test:e2e:ui

# Run tests in headed mode (see browser)
npm run test:e2e:headed

# Debug tests
npm run test:e2e:debug

# View test report
npm run test:e2e:report
```

### 3. Stop the Docker Compose stack

```bash
# From the project root
docker-compose down
```

## Test Structure

```
tests/e2e/
├── helpers/
│   └── axe.ts              # Accessibility testing helper
├── morning-prayer.spec.ts  # Morning Prayer E2E tests (T039, T040)
└── ... (other spec files)
```

## Writing Tests

```typescript
import { test, expect } from '@playwright/test';

test('my test', async ({ page }) => {
  await page.goto('/office/morning_prayer');
  await expect(page.locator('h1')).toContainText('Morning Prayer');
});
```

### With Accessibility Testing

```typescript
import { test, expect } from './helpers/axe';

test('page is accessible', async ({ page, makeAxeBuilder }) => {
  await page.goto('/');
  const accessibilityScanResults = await makeAxeBuilder().analyze();
  expect(accessibilityScanResults.violations).toEqual([]);
});
```

## Configuration

Tests are configured in `playwright.config.ts`:

- **Base URL**: `http://localhost:5173` (frontend service)
- **Backend API**: `http://localhost:8000` (accessed by frontend)
- **Browsers**: Chromium, Firefox, WebKit
- **Mobile**: Pixel 5, iPhone 12 emulation

## CI/CD

Tests run in GitHub Actions via `.github/workflows/test.yml`:

1. Starts Docker Compose services
2. Waits for services to be healthy
3. Runs Playwright tests
4. Uploads test reports as artifacts

## Troubleshooting

### Services not starting

```bash
# Check service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Restart services
docker-compose restart
```

### Tests failing with connection errors

```bash
# Verify services are accessible
curl http://localhost:5173
curl http://localhost:8000/api/
```

### Browser installation issues

```bash
# Reinstall Playwright browsers
npm run test:e2e:install
```

## Migration Notes

This project is transitioning from Cypress to Playwright:
- New tests should use Playwright (`*.spec.ts`)
- Legacy Cypress tests remain in `specs/` directory
- See `/specs/CYPRESS-TO-PLAYWRIGHT-MIGRATION.md` for details
