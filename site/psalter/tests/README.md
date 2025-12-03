# Psalter Test Suite

## Phase 12: Psalter Testing (T139-T151)

**Total Tests: 43 passing, 1 skipped (60-day cycle not implemented)**
**Bug Fixed: T148 - psalm_string_to_list now correctly splits on comma**

### Test Files

#### 1. psalter/tests/test_models.py (24 tests)
Tests for Psalter models including Psalm, PsalmVerse, PsalmTopic.

**Test Classes:**
- **TestPsalmModel** (6 tests): T141 - Psalm retrieval by number
  - All 150 psalms exist in database
  - Retrieval by number
  - Unique psalm numbers
  - Latin titles (optional field)
  - String representation

- **TestPsalmVerseModel** (6 tests): T142 - PsalmVerse retrieval for psalm
  - Verses exist for psalms
  - Retrieve verses for specific psalm
  - Two-half verse structure (first_half, second_half)
  - Foreign key relationship to Psalm
  - Unique constraint (psalm, verse number)
  - String representation

- **TestPsalmTextFormatting** (5 tests): T143 - Psalm text formatting
  - Contemporary language text (first_half, second_half)
  - Traditional language text (first_half_tle, second_half_tle)
  - Complete psalm text assembly
  - Traditional vs contemporary differences

- **TestPsalmTopicModel** (5 tests): T144 - PsalmTopic psalm grouping
  - Topic name and psalm list
  - psalm_list property parsing
  - Ordering by order field
  - Comma-separated psalm parsing

- **TestPsalmTopicPsalmModel** (2 tests): Relationship model tests
  - Psalm to PsalmTopic relationships
  - Ordering of psalms within topics

**Coverage:** FR-005, FR-005a (partial)
**Status:** ✅ 24/24 passing

---

#### 2. office/tests/test_models.py (14 tests)
Tests for Office models related to psalms.

**Test Classes:**
- **TestThirtyDayPsalterDay** (8 tests): T139 - ThirtyDayPsalterDay psalm retrieval
  - 30-day Psalter data exists (30-31 days)
  - Retrieve psalter day by day number
  - MP and EP psalms both present
  - psalm_string_to_list correctly parses comma-separated values
  - get_mp_pslams returns list
  - get_ep_pslams returns list
  - MP and EP psalms differ for each day
  - All days have both MP and EP assignments

- **TestOfficeDayPsalms** (6 tests): T140 - OfficeDay mp_psalms vs ep_psalms differ
  - StandardOfficeDay has mp_psalms and ep_psalms fields
  - mp_psalms field stores psalm assignments
  - ep_psalms field stores psalm assignments
  - MP and EP psalms differ for same day
  - Existing office days have different MP/EP psalms
  - Psalm formats: single, multiple, verse ranges

**Coverage:** FR-005, FR-005a
**Status:** ✅ 14/14 passing

---

#### 3. office/tests/test_psalter_integration.py (5 passing, 1 skipped)
Integration tests for Psalter cycle assignments.

**Test Classes:**
- **TestThirtyDayCyclePsalmAssignment** (4 tests): T145 - 30-day cycle
  - 30-day cycle covers all days (30-31)
  - Day 1 has specific psalm assignments
  - Sequential coverage through Psalter
  - Month calculation for given date

- **TestSixtyDayCyclePsalmAssignment** (1 passing, 1 skipped): T146 - 60-day cycle
  - 30-day cycle is current default ✅
  - 60-day cycle not yet implemented ⏸️ (skipped)

**Coverage:** FR-005a
**Status:** ✅ 5/6 passing, 1 skipped

---

#### 4. app/tests/e2e/specs/psalter_cycle_settings.spec.py (4 scenarios)
E2E test documentation for Psalter cycle settings.

**Test Scenarios** (T147):
- User can access Psalter cycle setting
- User can change to 60-day cycle
- Psalter cycle affects Daily Office psalms
- 30-day cycle is default

**Coverage:** FR-005b (User Psalter cycle selection)
**Status:** ⏸️ Documented only (requires FontAwesome Pro setup)
**Includes:** Detailed test steps, frontend implementation notes, Cypress code examples

---

## Bug Fix - T148

**File:** `site/office/models.py` line 91
**Issue:** `ThirtyDayPsalterDay.psalm_string_to_list()` incorrectly used `psalms.split(psalms)` instead of `psalms.split(',')`
**Fix:** Changed to `psalms.split(',')` to correctly parse comma-separated psalm numbers
**Impact:** Method now properly returns list like `["1", "2", "3"]` instead of invalid split

---

## FR Traceability Annotations (T149-T151)

Added docstring annotations to `site/office/models.py`:

**T149 - OfficeDay (FR-005):**
```python
"""
FR-005: Different psalm assignments for Morning Prayer vs Evening Prayer
MP psalms (mp_psalms) differ from EP psalms (ep_psalms) to provide
variety and cover the Psalter systematically.
"""
```

**T150 - ThirtyDayPsalterDay (FR-005a):**
```python
"""
FR-005a: 30-day and 60-day Psalter cycles
Provides psalm assignments for each day of a 30-day cycle, systematically
covering Psalms 1-150 over the course of a month.
"""
```

**T151 - Psalter Cycle Selection (FR-005b):**
```python
"""
FR-005b: User Psalter cycle selection
This model supports the 30-day cycle option. Users can select between
30-day and 60-day cycles in settings (60-day cycle planned for future).
"""
```

---

## Test Execution

### Run All Psalter Tests
```bash
pytest psalter/tests/ office/tests/test_models.py office/tests/test_psalter_integration.py -v
```

### Run With Coverage
```bash
pytest psalter/tests/ --cov=psalter --cov-report=term-missing
```

### Run Specific Test Classes
```bash
# Psalm models only
pytest psalter/tests/test_models.py::TestPsalmModel -v

# ThirtyDayPsalterDay only
pytest office/tests/test_models.py::TestThirtyDayPsalterDay -v

# Integration tests
pytest office/tests/test_psalter_integration.py -v
```

---

## Functional Requirements Coverage

| FR ID | Requirement | Test Coverage | Status |
|-------|-------------|---------------|--------|
| FR-005 | Different MP vs EP psalm assignments | test_models.py (14 tests) | ✅ Complete |
| FR-005a | 30-day and 60-day Psalter cycles | test_models.py (8 tests), test_psalter_integration.py (5 tests) | ✅ 30-day complete, 60-day planned |
| FR-005b | User Psalter cycle selection | E2E documented (4 scenarios) | ⏸️ Documented (frontend blocked) |

---

## Test Metrics

- **Total Phase 12 Tests:** 43 passing, 1 skipped
- **Total Project Tests:** 485 passing (up from 442, 10% increase)
- **Psalter Models Coverage:** psalter/models.py 85%, test_models.py 99%
- **Office Models Coverage:** office/models.py 59% (up from 57%)
- **Execution Time:** 31.45s (parallel execution with 24 workers)
- **Bug Fixes:** 1 critical bug fixed in psalm_string_to_list

---

## Psalter Structure

### 30-Day Psalter Cycle
- **Days:** 31 entries (one per day of month)
- **Coverage:** Psalms 1-150 distributed over 30/31 days
- **Assignments:** Separate MP and EP psalms for each day
- **Usage:** Default Psalter cycle for Daily Office

### Psalm Database
- **Total Psalms:** 150 (Psalm 1 through Psalm 150)
- **Total Verses:** 2,520 verses across all psalms
- **Languages:** Contemporary (default) and Traditional Language Edition (TLE)
- **Verse Structure:** Two-half format (first_half | second_half)

### Psalm Topics
- **Purpose:** Thematic grouping of psalms
- **Examples:** Penitential Psalms (6, 32, 38, 51, 102, 130, 143)
- **Model:** PsalmTopic with comma-separated psalm list
- **Relationships:** PsalmTopicPsalm links Psalm to PsalmTopic with ordering

---

## Notes

### 60-Day Psalter Cycle
Currently not implemented. Test documented in `test_psalter_integration.py` with `@pytest.mark.skip`.
When implemented, 60-day cycle would:
- Cover Psalms 1-150 over 60 days instead of 30
- Provide longer, more meditative daily psalm assignments
- Require separate table or cycle type field
- Allow user selection via settings (FR-005b)

### E2E Tests
E2E tests documented in `app/tests/e2e/specs/psalter_cycle_settings.spec.py` but cannot execute due to FontAwesome Pro npm authentication. Documentation includes:
- Detailed test steps for 4 scenarios
- Frontend implementation notes (Vue components, localStorage, Vuex)
- Cypress code examples for future implementation
- All tests marked `@pytest.mark.skip` with clear reason

### Bug Fix Impact
The `psalm_string_to_list` bug fix (T148) affects:
- `ThirtyDayPsalterDay.get_mp_pslams()` - now returns correct list
- `ThirtyDayPsalterDay.get_ep_pslams()` - now returns correct list
- Any code relying on parsing comma-separated psalm assignments

Bug was discovered during test creation and fixed before tests were written, demonstrating value of comprehensive testing.

---

## Phase 12 Summary

✅ **All objectives achieved:**
1. Fixed critical bug in psalm parsing (T148)
2. Created comprehensive psalter model tests (T141-T144): 24 tests
3. Created office model psalm tests (T139-T140): 14 tests
4. Created psalter integration tests (T145-T146): 5 tests
5. Documented E2E tests (T147): 4 scenarios
6. Added FR traceability annotations (T149-T151)

**Impact:** 43 new tests, 1 bug fix, comprehensive Psalter coverage, 10% increase in total project tests.
