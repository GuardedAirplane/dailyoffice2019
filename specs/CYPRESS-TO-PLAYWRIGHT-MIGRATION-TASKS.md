# Tasks: Cypress to Playwright Migration

**Input**: Migration guide from `/specs/CYPRESS-TO-PLAYWRIGHT-MIGRATION.md`
**Prerequisites**: Migration plan complete, spec documents updated (001-006)
**Branch**: `cypress-to-playwright-migration`

**Tests**: E2E tests will be migrated and verified across all browsers

**Organization**: Tasks follow the 4-phase migration plan, organized to enable parallel work where possible

## Format: `[ID] [P?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions

- Frontend: `app/`
- E2E Tests: `app/tests/e2e/`
- Configuration: `app/playwright.config.ts`, `app/package.json`
- CI/CD: `.github/workflows/test.yml`

---

## Phase 1: Preparation (1-2 days)

**Purpose**: Set up Playwright infrastructure without removing Cypress

**Goal**: Playwright installed and configured alongside existing Cypress setup

- [ ] T001 Install Playwright dependencies in app/package.json (`@playwright/test`, `@axe-core/playwright`)
- [ ] T002 Run `npx playwright install --with-deps` to install browser binaries
- [ ] T003 Create Playwright configuration in app/playwright.config.ts with multi-browser support
- [ ] T004 [P] Create accessibility testing helper in app/tests/e2e/helpers/axe.ts
- [ ] T005 [P] Add Playwright npm scripts to app/package.json (test:e2e, test:e2e:ui, test:e2e:headed, test:e2e:debug, test:e2e:report)
- [ ] T006 Verify Playwright configuration with sample test in app/tests/e2e/sample.spec.ts
- [ ] T007 Document Playwright setup in app/README.md

**Checkpoint**: Playwright installed and functional, Cypress still operational

---

## Phase 2: Test Migration (1-2 weeks)

**Purpose**: Port all existing Cypress tests to Playwright

**Goal**: All E2E tests converted and passing in Chromium, Firefox, and WebKit

### 2.1: Spec 006-general-design Tests (Priority 1)

- [ ] T008 [P] Create settings-persistence.spec.ts in app/tests/e2e/settings-persistence.spec.ts
- [ ] T009 [P] Create settings-sharing.spec.ts in app/tests/e2e/settings-sharing.spec.ts
- [ ] T010 [P] Create responsive-design.spec.ts in app/tests/e2e/responsive-design.spec.ts
- [ ] T011 [P] Create accessibility.spec.ts in app/tests/e2e/accessibility.spec.ts using axe helper
- [ ] T012 [P] Create cross-platform.spec.ts in app/tests/e2e/cross-platform.spec.ts
- [ ] T013 Verify all 006-general-design tests pass in Chromium
- [ ] T014 Verify all 006-general-design tests pass in Firefox
- [ ] T015 Verify all 006-general-design tests pass in WebKit

**Checkpoint**: Core settings and accessibility tests migrated and passing

### 2.2: Spec 001-daily-office Tests (Priority 2)

- [ ] T016 [P] Create daily-office-generation.spec.ts for 8 office types in app/tests/e2e/daily-office-generation.spec.ts
- [ ] T017 [P] Create office-navigation.spec.ts in app/tests/e2e/office-navigation.spec.ts
- [ ] T018 [P] Create date-selection.spec.ts in app/tests/e2e/date-selection.spec.ts
- [ ] T019 Verify all 001-daily-office tests pass across all browsers

**Checkpoint**: Daily office core functionality tests migrated

### 2.3: Spec 002-liturgical-calendar Tests (Priority 3)

- [ ] T020 [P] Create calendar-navigation.spec.ts in app/tests/e2e/calendar-navigation.spec.ts
- [ ] T021 [P] Create season-feast-display.spec.ts in app/tests/e2e/season-feast-display.spec.ts
- [ ] T022 [P] Create year-transitions.spec.ts in app/tests/e2e/year-transitions.spec.ts
- [ ] T023 Verify all 002-liturgical-calendar tests pass across all browsers

**Checkpoint**: Liturgical calendar tests migrated

### 2.4: Spec 003-collects Tests (Priority 4)

- [ ] T024 [P] Create collects-browse.spec.ts in app/tests/e2e/collects-browse.spec.ts
- [ ] T025 [P] Create collects-filter.spec.ts in app/tests/e2e/collects-filter.spec.ts
- [ ] T026 [P] Create collects-search.spec.ts in app/tests/e2e/collects-search.spec.ts
- [ ] T027 [P] Create collects-office-integration.spec.ts in app/tests/e2e/collects-office-integration.spec.ts
- [ ] T028 Verify all 003-collects tests pass across all browsers

**Checkpoint**: Collects functionality tests migrated

### 2.5: Spec 004-psalter Tests (Priority 5)

- [ ] T029 [P] Create psalter-view.spec.ts in app/tests/e2e/psalter-view.spec.ts
- [ ] T030 [P] Create psalter-navigation.spec.ts in app/tests/e2e/psalter-navigation.spec.ts
- [ ] T031 [P] Create psalter-language-switch.spec.ts in app/tests/e2e/psalter-language-switch.spec.ts
- [ ] T032 [P] Create psalter-topic-filter.spec.ts in app/tests/e2e/psalter-topic-filter.spec.ts
- [ ] T033 Verify all 004-psalter tests pass across all browsers

**Checkpoint**: Psalter tests migrated

### 2.6: Spec 005-lectionary Tests (Priority 6)

- [ ] T034 [P] Create lectionary-display.spec.ts in app/tests/e2e/lectionary-display.spec.ts
- [ ] T035 [P] Create lectionary-navigation.spec.ts in app/tests/e2e/lectionary-navigation.spec.ts
- [ ] T036 Verify all 005-lectionary tests pass across all browsers

**Checkpoint**: All E2E tests migrated to Playwright

### 2.7: Mobile Device Testing

- [ ] T037 [P] Verify critical tests pass on Mobile Chrome (Pixel 5 emulation)
- [ ] T038 [P] Verify critical tests pass on Mobile Safari (iPhone 12 emulation)

**Checkpoint**: Mobile testing validated

---

## Phase 3: CI/CD Integration (1-2 days)

**Purpose**: Update GitHub Actions to run Playwright tests

**Goal**: CI/CD pipeline running Playwright with artifact uploads

- [ ] T039 Create or update .github/workflows/test.yml to include Playwright setup
- [ ] T040 Add Playwright browser installation step to CI workflow
- [ ] T041 Add Playwright test execution step to CI workflow
- [ ] T042 Configure Playwright report upload as artifact in CI workflow
- [ ] T043 Update coverage reporting to include Playwright in CI workflow
- [ ] T044 Test CI/CD pipeline with a test commit
- [ ] T045 Verify Playwright reports are accessible in GitHub Actions artifacts
- [ ] T046 [P] Update CI timeout settings to accommodate browser installation (60 minutes)

**Checkpoint**: CI/CD running Playwright successfully

---

## Phase 4: Cleanup (1 day)

**Purpose**: Remove Cypress infrastructure completely

**Goal**: Cypress removed, all references updated, clean codebase

### 4.1: Uninstall and Remove Files

- [ ] T047 Uninstall Cypress packages from app/package.json (`cypress`, `cypress-axe`)
- [ ] T048 Remove app/cypress.config.mjs file
- [ ] T049 Remove app/cypress/ directory if it exists
- [ ] T050 Remove any old .cy.js test files in app/tests/e2e/
- [ ] T051 Remove Cypress-related npm scripts from app/package.json
- [ ] T052 Remove app/tests/e2e/sample.spec.ts (Playwright verification test)

### 4.2: Documentation Updates

- [ ] T053 [P] Update app/README.md to reference Playwright instead of Cypress
- [ ] T054 [P] Update .github/copilot-instructions.md to reference Playwright
- [ ] T055 [P] Verify all spec documents (001-006) reference Playwright (already done)
- [ ] T056 [P] Add migration completion note to specs/CYPRESS-TO-PLAYWRIGHT-MIGRATION.md

### 4.3: Verification

- [ ] T057 Run full Playwright test suite to ensure nothing broken
- [ ] T058 Verify no Cypress references remain in codebase (`git grep -i cypress`)
- [ ] T059 Verify CI/CD pipeline still passes
- [ ] T060 Run `npm audit` to check for any remaining Cypress-related dependencies

**Checkpoint**: Cypress completely removed, Playwright fully operational

---

## Phase 5: Final Validation (0.5 days)

**Purpose**: Comprehensive testing and documentation

**Goal**: Migration complete and validated

- [ ] T061 Run complete Playwright test suite across all browsers (Chromium, Firefox, WebKit)
- [ ] T062 Run mobile device tests (Pixel 5, iPhone 12)
- [ ] T063 Verify accessibility tests passing with axe-core
- [ ] T064 Confirm test execution time is acceptable (record baseline)
- [ ] T065 Review and update migration guide with actual completion dates
- [ ] T066 Create migration completion report documenting:
  - Total tests migrated
  - Browser coverage achieved
  - Performance comparison (if applicable)
  - Lessons learned
  - Known issues or limitations

**Checkpoint**: Migration validated and documented

---

## Dependencies & Execution Order

### Phase Dependencies

- **Preparation (Phase 1)**: No dependencies - can start immediately
- **Test Migration (Phase 2)**: Depends on Preparation complete
- **CI/CD Integration (Phase 3)**: Depends on at least Priority 1 tests migrated (T008-T015)
- **Cleanup (Phase 4)**: Depends on ALL test migration complete (T008-T038)
- **Final Validation (Phase 5)**: Depends on Cleanup complete

### Within Test Migration (Phase 2)

- Spec tests can be migrated in parallel by different developers
- Within each spec, test files can be created in parallel (all marked [P])
- Browser verification must happen after test creation
- Mobile testing happens after all desktop tests pass

### Parallel Opportunities

**Phase 1 Preparation**:
- T004 (axe helper) and T005 (npm scripts) can run in parallel

**Phase 2 Test Migration**:
- All test file creation tasks within each spec group are parallelizable
- Different spec groups (2.1-2.6) can be worked on in parallel
- Example: Developer A works on 006-general-design while Developer B works on 001-daily-office

**Phase 3 CI/CD**:
- T046 (timeout settings) can run in parallel with main workflow updates

**Phase 4 Cleanup**:
- All documentation updates (T053-T056) can run in parallel

---

## Parallel Example: Test Migration

```bash
# Multiple developers can work simultaneously:

# Developer A: Spec 006 tests
Task T008: "Create settings-persistence.spec.ts"
Task T009: "Create settings-sharing.spec.ts"
Task T010: "Create responsive-design.spec.ts"
Task T011: "Create accessibility.spec.ts"
Task T012: "Create cross-platform.spec.ts"

# Developer B: Spec 001 tests  
Task T016: "Create daily-office-generation.spec.ts"
Task T017: "Create office-navigation.spec.ts"
Task T018: "Create date-selection.spec.ts"

# Developer C: Spec 003 tests
Task T024: "Create collects-browse.spec.ts"
Task T025: "Create collects-filter.spec.ts"
Task T026: "Create collects-search.spec.ts"
Task T027: "Create collects-office-integration.spec.ts"
```

---

## Implementation Strategy

### MVP Approach (Minimum Viable Migration)

1. Complete Phase 1: Preparation (T001-T007)
2. Complete Phase 2.1: Priority 1 Tests Only (T008-T015)
3. Complete Phase 3: CI/CD Integration (T039-T046)
4. **STOP and VALIDATE**: Ensure core tests working in CI/CD
5. If successful, proceed with remaining test migration

### Full Migration (Recommended)

1. Complete Phase 1: Preparation → Playwright ready
2. Complete Phase 2: All Test Migration → All tests ported
3. Complete Phase 3: CI/CD Integration → Pipeline updated
4. Complete Phase 4: Cleanup → Cypress removed
5. Complete Phase 5: Final Validation → Migration complete

### Parallel Team Strategy

With 3 developers:

1. All complete Phase 1 together (1-2 days)
2. Phase 2 in parallel:
   - Developer A: Specs 006 + 001 (T008-T019)
   - Developer B: Specs 002 + 003 (T020-T028)
   - Developer C: Specs 004 + 005 (T029-T036)
3. Developer A handles Phase 3 (CI/CD) while B & C do mobile testing
4. All complete Phase 4 & 5 together

---

## Rollback Plan

If migration encounters critical issues:

1. **Before Cleanup (Phase 4)**: Cypress still installed
   - Simply continue using Cypress
   - Playwright can coexist
   - No rollback needed

2. **After Cleanup**: If issues found after Cypress removal
   - Execute rollback tasks from migration guide
   - `git revert` cleanup commits
   - Reinstall Cypress: `npm install -D cypress cypress-axe`
   - Restore config: `git checkout main -- app/cypress.config.mjs`

---

## Success Criteria

- ✅ All tasks T001-T066 completed
- ✅ All Cypress tests successfully migrated to Playwright
- ✅ Tests passing across 3 desktop browsers (Chromium, Firefox, WebKit)
- ✅ Tests passing on 2 mobile emulators (Pixel 5, iPhone 12)
- ✅ CI/CD pipeline running Playwright tests
- ✅ Test execution time equal or better than Cypress
- ✅ Accessibility testing with axe-core functional
- ✅ Cypress completely removed from codebase
- ✅ All documentation updated
- ✅ No Cypress references in codebase (`git grep -i cypress` returns nothing)

---

## Estimated Timeline

- **Phase 1**: 1-2 days (T001-T007)
- **Phase 2**: 1-2 weeks (T008-T038) - varies by test count
- **Phase 3**: 1-2 days (T039-T046)
- **Phase 4**: 1 day (T047-T060)
- **Phase 5**: 0.5 days (T061-T066)

**Total**: 2-3 weeks (depends on test volume and team size)

---

## Notes

- [P] tasks = different files, can run in parallel
- All test files use .spec.ts extension (TypeScript)
- Maintain test coverage during migration - both suites should pass until cleanup
- Use Playwright's codegen tool to help with complex test conversions
- Reference migration guide for Cypress→Playwright pattern conversions
- Commit after each completed spec group (2.1, 2.2, etc.)
- Tag major milestones (Preparation complete, Migration complete, Cleanup complete)
