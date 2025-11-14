# Cypress to Playwright Migration Guide

**Date**: November 13, 2025  
**Status**: Planned - Not Yet Executed  
**Impact**: All E2E tests across all specs (001-006)

## Overview

This document outlines the complete migration from Cypress to Playwright for E2E testing across the Daily Office 2019 project. This migration affects all specification plans (001-006) and requires coordinated changes to the codebase.

## Rationale for Migration

**Why Playwright over Cypress:**

1. **Multi-Browser Support**: Playwright supports Chromium, Firefox, and WebKit out of the box with consistent APIs
2. **Modern Architecture**: Built by Microsoft with active development and modern tooling
3. **Superior Tooling**: Built-in trace viewer, UI mode, and codegen for test creation
4. **Parallel Execution**: Native support for parallel test execution without additional configuration
5. **Auto-Wait**: Better auto-waiting and retry mechanisms reduce test flakiness
6. **TypeScript First**: First-class TypeScript support with excellent type definitions
7. **Performance**: Generally faster test execution compared to Cypress

## Migration Phases

### Phase 1: Preparation (1-2 days)

**Goals**: Set up Playwright infrastructure without removing Cypress

**Tasks**:

1. **Install Playwright dependencies**:
   ```bash
   cd app
   npm install -D @playwright/test @axe-core/playwright
   npx playwright install --with-deps
   ```

2. **Create Playwright configuration** (`app/playwright.config.ts`):
   ```typescript
   import { defineConfig, devices } from '@playwright/test';

   export default defineConfig({
     testDir: './tests/e2e',
     fullyParallel: true,
     forbidOnly: !!process.env.CI,
     retries: process.env.CI ? 2 : 0,
     workers: process.env.CI ? 1 : undefined,
     reporter: 'html',
     use: {
       baseURL: 'http://127.0.0.1:8080',
       trace: 'on-first-retry',
       screenshot: 'only-on-failure',
     },

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
       // Mobile testing
       {
         name: 'Mobile Chrome',
         use: { ...devices['Pixel 5'] },
       },
       {
         name: 'Mobile Safari',
         use: { ...devices['iPhone 12'] },
       },
     ],

     webServer: {
       command: 'npm run dev',
       url: 'http://127.0.0.1:8080',
       reuseExistingServer: !process.env.CI,
     },
   });
   ```

3. **Create accessibility testing helper** (`app/tests/e2e/helpers/axe.ts`):
   ```typescript
   import { test as base, expect } from '@playwright/test';
   import AxeBuilder from '@axe-core/playwright';

   export const test = base.extend({
     makeAxeBuilder: async ({ page }, use) => {
       await use(() => new AxeBuilder({ page }));
     },
   });

   export { expect };
   ```

4. **Update package.json scripts**:
   ```json
   {
     "scripts": {
       "test:e2e": "playwright test",
       "test:e2e:ui": "playwright test --ui",
       "test:e2e:headed": "playwright test --headed",
       "test:e2e:debug": "playwright test --debug",
       "test:e2e:report": "playwright show-report"
     }
   }
   ```

**Deliverables**:
- ✅ Playwright installed and configured
- ✅ Helper utilities created
- ✅ Scripts added to package.json
- ⚠️ Cypress still installed and functional

### Phase 2: Test Migration (1-2 weeks)

**Goals**: Port existing Cypress tests to Playwright

**Migration Pattern**:

**Cypress Pattern**:
```javascript
// tests/e2e/settings-persistence.cy.js
describe('Settings Persistence', () => {
  beforeEach(() => {
    cy.visit('/settings');
  });

  it('should persist settings after reload', () => {
    cy.get('[data-testid="font-size-slider"]').type('18');
    cy.get('[data-testid="save-button"]').click();
    cy.reload();
    cy.get('[data-testid="font-size-slider"]').should('have.value', '18');
  });
});
```

**Playwright Equivalent**:
```typescript
// tests/e2e/settings-persistence.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Settings Persistence', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/settings');
  });

  test('should persist settings after reload', async ({ page }) => {
    await page.getByTestId('font-size-slider').fill('18');
    await page.getByTestId('save-button').click();
    await page.reload();
    await expect(page.getByTestId('font-size-slider')).toHaveValue('18');
  });
});
```

**Key Differences**:

| Cypress | Playwright | Notes |
|---------|------------|-------|
| `cy.visit()` | `page.goto()` | Playwright requires async/await |
| `cy.get()` | `page.locator()` or `page.getByTestId()` | Playwright has more specific locator methods |
| `.type()` | `.fill()` or `.type()` | `.fill()` is faster, `.type()` simulates keypress |
| `.should()` | `expect().to*()` | Playwright uses Jest/Vitest-style assertions |
| Auto-retry | Auto-retry | Both frameworks auto-retry, but Playwright is more configurable |

**Tests to Migrate** (based on spec analysis):

1. **006-general-design** (Priority):
   - `settings-persistence.spec.ts` - Settings storage across reloads
   - `settings-sharing.spec.ts` - URL parameter sharing
   - `responsive-design.spec.ts` - Responsive layouts
   - `accessibility.spec.ts` - WCAG compliance checks
   - `cross-platform.spec.ts` - Web/mobile compatibility

2. **001-daily-office**:
   - Daily office generation tests (8 office types)
   - Navigation between offices
   - Date selection

3. **002-liturgical-calendar**:
   - Calendar navigation
   - Season/feast day display
   - Year transitions

4. **003-collects**:
   - Browse collects
   - Filter by occasion
   - Search functionality
   - Daily office integration

5. **004-psalter**:
   - View psalms
   - Navigate between psalms
   - Language switching
   - Topic filtering

6. **005-lectionary**:
   - Lectionary display
   - Bible passage navigation

**Deliverables**:
- ✅ All Cypress tests ported to Playwright
- ✅ Tests passing in all browsers (Chromium, Firefox, WebKit)
- ✅ Accessibility tests integrated
- ⚠️ Cypress tests still present but deprecated

### Phase 3: CI/CD Integration (1-2 days)

**Goals**: Update GitHub Actions to run Playwright tests

**Update `.github/workflows/test.yml`**:

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: |
          cd app
          npm ci
      
      - name: Install Playwright Browsers
        run: |
          cd app
          npx playwright install --with-deps
      
      - name: Run unit tests
        run: |
          cd app
          npm run test:unit -- --coverage
      
      - name: Run E2E tests
        run: |
          cd app
          npm run test:e2e
      
      - name: Upload Playwright Report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: app/playwright-report/
          retention-days: 30
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./app/coverage/lcov.info
```

**Deliverables**:
- ✅ Playwright tests running in CI/CD
- ✅ Test reports uploaded as artifacts
- ✅ Coverage reporting configured

### Phase 4: Cleanup (1 day)

**Goals**: Remove Cypress infrastructure

**Tasks**:

1. **Uninstall Cypress packages**:
   ```bash
   cd app
   npm uninstall cypress cypress-axe
   ```

2. **Remove Cypress files**:
   ```bash
   rm -f app/cypress.config.mjs
   rm -rf app/cypress/  # If this directory exists
   ```

3. **Remove Cypress scripts from package.json**:
   - Remove any `cy:*` scripts
   - Remove Cypress-related npm scripts

4. **Update documentation**:
   - Update all README files
   - Update `.github/copilot-instructions.md`
   - Update all spec documents (already done in this PR)

5. **Clean up old test files**:
   ```bash
   # Remove old .cy.js files if they still exist
   find app/tests/e2e -name "*.cy.js" -type f -delete
   ```

**Deliverables**:
- ✅ Cypress completely removed
- ✅ All references updated
- ✅ Clean git history

## File Changes Summary

### Files to Create

```
app/
├── playwright.config.ts          # NEW: Playwright configuration
└── tests/
    └── e2e/
        ├── helpers/
        │   └── axe.ts            # NEW: Accessibility testing helper
        ├── settings-persistence.spec.ts   # MIGRATED from .cy.js
        ├── settings-sharing.spec.ts       # MIGRATED from .cy.js
        ├── responsive-design.spec.ts      # MIGRATED from .cy.js
        ├── accessibility.spec.ts          # MIGRATED from .cy.js
        └── cross-platform.spec.ts         # MIGRATED from .cy.js
```

### Files to Modify

```
app/
├── package.json                  # Update scripts, remove Cypress deps, add Playwright deps
└── vitest.config.ts             # May need updates for coverage integration

.github/
└── workflows/
    └── test.yml                  # Update CI/CD to use Playwright
```

### Files to Delete

```
app/
├── cypress.config.mjs            # DELETE: Cypress configuration
└── tests/
    └── e2e/
        └── *.cy.js               # DELETE: Old Cypress test files
```

### Documentation to Update

All spec documents have been updated in this PR:
- ✅ `specs/001-daily-office/*.md`
- ✅ `specs/002-liturgical-calendar/plan/*.md`
- ✅ `specs/003-collects/*.md`
- ✅ `specs/004-psalter/*.md`
- ✅ `specs/005-lectionary/plan.md`
- ✅ `specs/006-general-design/*.md`

## Dependencies

### Remove (Cypress)

```json
{
  "devDependencies": {
    "cypress": "^13.0.0",
    "cypress-axe": "^1.5.0"
  }
}
```

### Add (Playwright)

```json
{
  "devDependencies": {
    "@playwright/test": "^1.40.0",
    "@axe-core/playwright": "^4.8.0"
  }
}
```

## Testing Strategy

### Cross-Browser Testing

Playwright will test across:
- **Desktop**: Chromium, Firefox, WebKit
- **Mobile**: Mobile Chrome (Pixel 5), Mobile Safari (iPhone 12)

### Test Categories

1. **Functional Tests**: Core user journeys (settings, navigation, etc.)
2. **Accessibility Tests**: WCAG 2.1 AA compliance using axe-core
3. **Responsive Tests**: Layout at various breakpoints
4. **Cross-Platform Tests**: Web vs. mobile behavior

### Coverage Goals

- **E2E Coverage**: All critical user journeys
- **Browser Coverage**: 3 desktop + 2 mobile browsers
- **Accessibility**: 100% of pages scanned with axe-core

## Risks and Mitigation

### Risk 1: Test Breakage During Migration

**Mitigation**: Keep Cypress tests running until all Playwright tests pass

### Risk 2: CI/CD Pipeline Delays

**Mitigation**: Test Playwright in separate workflow first, merge after validation

### Risk 3: Learning Curve

**Mitigation**: Provide comprehensive examples and documentation (this guide)

### Risk 4: Missing Edge Cases

**Mitigation**: Run both test suites in parallel during transition period

## Rollback Plan

If migration fails:

1. **Revert Playwright changes**:
   ```bash
   git revert <migration-commit-hash>
   ```

2. **Reinstall Cypress**:
   ```bash
   cd app
   npm install -D cypress cypress-axe
   ```

3. **Restore Cypress configuration**:
   ```bash
   git checkout main -- app/cypress.config.mjs
   ```

## Timeline

| Phase | Duration | Blockers |
|-------|----------|----------|
| Phase 1: Preparation | 1-2 days | None |
| Phase 2: Test Migration | 1-2 weeks | Requires Phase 1 complete |
| Phase 3: CI/CD Integration | 1-2 days | Requires Phase 2 complete |
| Phase 4: Cleanup | 1 day | Requires Phase 3 complete |
| **Total** | **2-3 weeks** | |

## Success Criteria

- ✅ All Cypress tests successfully migrated to Playwright
- ✅ All tests passing across 3 desktop + 2 mobile browsers
- ✅ CI/CD pipeline running Playwright tests
- ✅ Test execution time equal or better than Cypress
- ✅ Accessibility testing integrated with axe-core
- ✅ Cypress completely removed from codebase
- ✅ All documentation updated

## Post-Migration Benefits

1. **Multi-Browser Coverage**: Automatic testing across Chromium, Firefox, and WebKit
2. **Better Developer Experience**: UI mode, trace viewer, and codegen
3. **Faster Execution**: Parallel test execution by default
4. **Modern Tooling**: Active development and community support
5. **Mobile Testing**: Built-in mobile device emulation
6. **Accessibility**: First-class axe-core integration
7. **TypeScript Support**: Better type safety and IDE support

## References

- [Playwright Documentation](https://playwright.dev/)
- [Playwright vs Cypress Comparison](https://playwright.dev/docs/why-playwright)
- [Migrating from Cypress](https://playwright.dev/docs/migration)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Accessibility Testing with Playwright](https://playwright.dev/docs/accessibility-testing)

---

**Status**: 📋 Planning Complete - Ready for Implementation  
**Next Step**: Begin Phase 1 (Preparation)  
**Owner**: Development Team  
**Estimated Completion**: 2-3 weeks from start
