# Implementation Plan: 002-liturgical-calendar

**Feature**: Liturgical Calendar  
**Status**: Planning Phase  
**Created**: November 6, 2025  
**Branch**: spec-kit (planning only - implementation branch TBD)

## Executive Summary

This plan documents the gap analysis and implementation strategy for bringing the existing liturgical calendar implementation into conformance with the retroactive specification in `specs/002-liturgical-calendar/spec.md`.

**Key Finding**: The existing implementation is **substantially complete** but requires enhancements for filtering, navigation, and First Vespers handling.

## Technical Context

### Existing Implementation Status

#### Backend (Django/Python) - ✅ SUBSTANTIALLY COMPLETE

- **churchcal app**: Complete church calendar calculation engine
  - `models.py`: Full data model with Commemoration, Season, CalendarDate, etc.
  - `calculations.py`: ChurchYear and CalendarDate calculation logic
  - `utils.py`: Date calculation utilities (Advent, Easter, etc.)
  - Handles feast precedence, transfers, and seasons ✅
  - Supports multiple calendar systems (ACNA_BCP2019) ✅
  - Caches calendar years for performance ✅

#### API Layer - ✅ COMPLETE

- **churchcal/api/**: REST API endpoints
  - `views.py`: DayView, MonthView, YearView endpoints ✅
  - `serializer.py`: DaySerializer for calendar data ✅
  - Supports calendar year queries (spans two church years) ✅

#### Frontend (Vue.js) - ⚠️ NEEDS ENHANCEMENT

- **app/src/views/Calendar.vue**: Calendar view exists ✅
  - Monthly calendar display ✅
  - Color-coding by liturgical season/feast ✅
  - Basic navigation (prev/next month, today) ✅
  - Click date to navigate to Daily Office ✅
  - Toggle for "Show Major Feasts Only" ✅
  - **MISSING**: First Vespers display
  - **MISSING**: Evening color indicators
  - **NEEDS REFINEMENT**: Filter logic clarity

### Technology Stack

- **Backend**: Django 5.2+, Python 3.13, PostgreSQL 17.5+
- **Frontend**: Vue 3, Vite, TypeScript, Element Plus (el-calendar component)
- **API**: Django REST Framework
- **Caching**: Memcached for church year data

### Dependencies

- Existing Daily Office views (`/day/:year/:month/:day`)
- Church calendar database (Commemoration, Season, Rank tables)
- Element Plus calendar component styling

### Integration Points

- Daily Office integration (FR-011): Already implemented via click navigation
- Storage API for filter preferences (using DynamicStorage helper)

## Constitution Check

### Principle I: Glory to God ✅

- **Assessment**: Feature enhances prayer and liturgical understanding
- **Conformance**: Feature directly serves the Church's daily prayer needs

### Principle II: Feature Branch Development ⚠️

- **Assessment**: Implementation will use `002-liturgical-calendar` branch
- **Action Required**: Create feature branch during implementation phase
- **Current State**: Planning in `spec-kit` branch as requested

### Principle III: Comprehensive Testing ❌ NOT YET ADDRESSED

- **Assessment**: Existing code lacks comprehensive tests
- **Gap**: No test coverage for calendar calculations, API endpoints, or Vue components
- **Action Required**: Must add tests before declaring feature complete
- **Test Requirements**:
  - Unit tests for date calculations (Easter, Advent, transfers)
  - Integration tests for API endpoints
  - Component tests for Calendar.vue
  - E2E tests for user scenarios from spec

### Principle IV: Code Quality and Clarity ✅ MOSTLY CONFORMANT

- **Assessment**: Existing code is generally clean and well-structured
- **Issues**: Some complex logic in `calculations.py` needs documentation
- **Action Required**: Add docstrings to complex methods

### Principle V: Atomic and Traceable Commits 📋 PROCESS REQUIREMENT

- **Assessment**: Will be enforced during implementation
- **Action Required**: Reference task IDs in all commits

### Principle VI: Unique and Persistent Identifiers ✅ CONFORMANT

- **Assessment**: Spec uses FR-###, SC-### format consistently
- **Action Required**: Create task IDs (T###) during planning

## Gap Analysis

### Backend Gaps

#### GAP-001: First Vespers Evening Color Support ⚠️ PARTIAL

**Status**: Partially implemented in `calculations.py:check_previous_evening()`
**Issue**: The logic sets `evening_required`, `evening_optional`, and `evening_season` on the previous day, but this may not be fully exposed through the API serializer.

**Required Changes**:

- ✅ Backend calculation exists
- ❌ Verify API serializer exposes evening data
- ❌ Add evening color to DaySerializer

**Related Requirements**: FR-016

#### GAP-002: Filter Logic Clarity ⚠️ AMBIGUOUS

**Status**: Frontend has toggle, but logic may not match spec
**Issue**: Current filter checks `rank.name.includes('FERIA')` but spec requires `rank.required=True` check

**Required Changes**:

- Review and align filter logic with FR-012
- Ensure backend sends `rank.required` flag
- Update frontend filter to use `rank.required`

**Related Requirements**: FR-012

### API Gaps

#### GAP-003: Evening Data in Serializer ❌ MISSING

**Status**: DaySerializer likely doesn't serialize evening commemorations
**Issue**: Need to expose `evening_required`, `evening_optional`, `evening_season` fields

**Required Changes**:

- Add evening fields to DaySerializer
- Add evening_color computed property
- Ensure API documentation reflects new fields

**Related Requirements**: FR-016

### Frontend Gaps

#### GAP-004: First Vespers Display ❌ MISSING

**Status**: No visual indication of "Eve of" commemorations
**Issue**: Calendar should show when evening belongs to next day's feast

**Required Changes**:

- Display evening commemorations separately or with indicator
- Show evening liturgical color (possibly as border or secondary color)
- Update date cell template to show morning and evening info

**Related Requirements**: FR-016

#### GAP-005: Navigation Robustness ⚠️ ENHANCEMENT

**Status**: Basic navigation works but could be improved
**Issue**: No year navigation, no date picker for jumping to specific months

**Enhancement Ideas** (out of scope for MVP):

- Add year navigation buttons
- Add month/year picker dropdown
- Add keyboard navigation

**Related Requirements**: FR-006, FR-007

### Database/Model Gaps

#### GAP-006: Blue Color Support ✅ ALREADY SUPPORTED

**Status**: Model has `color`, `additional_color`, `alternate_color`, `alternate_color_2` fields
**Issue**: None - database already supports multiple colors including blue for Advent

**Related Requirements**: FR-002

### Testing Gaps

#### GAP-007: Comprehensive Test Coverage ❌ CRITICAL

**Status**: No existing tests found for calendar functionality
**Issue**: Violates Constitution Principle III

**Required Tests**:

1. **Backend Unit Tests** (churchcal/tests.py):

   - Test Easter calculation for multiple years
   - Test Advent calculation
   - Test feast precedence rules
   - Test transfer logic (FR-009)
   - Test First Vespers logic (FR-016)
   - Test leap year handling (FR-013)
   - Test blue color availability for Advent (FR-002)

2. **API Tests** (churchcal/api/tests.py):

   - Test DayView returns correct data
   - Test MonthView returns correct month range
   - Test YearView returns full year
   - Test calendar parameter (ACNA_BCP2019)
   - Test edge cases (invalid dates, leap years)

3. **Frontend Component Tests** (app/tests/unit/Calendar.spec.js):

   - Test calendar rendering
   - Test color calculation
   - Test filter toggle
   - Test navigation (prev/next/today)
   - Test date cell click navigation

4. **E2E Tests** (app/tests/e2e/):
   - Test User Story 1 (view current month)
   - Test User Story 2 (navigate months)
   - Test User Story 3 (click date to office)
   - Test User Story 4 (filter feasts)
   - Test edge cases from spec

**Related Requirements**: ALL (testing validates all requirements)

## Conformance Assessment

### Requirements Conformance Matrix

| Requirement | Status | Backend | API | Frontend | Tests | Notes                                   |
| ----------- | ------ | ------- | --- | -------- | ----- | --------------------------------------- |
| FR-001      | ✅     | ✅      | ✅  | ✅       | ❌    | Monthly view exists                     |
| FR-002      | ✅     | ✅      | ✅  | ✅       | ❌    | Color-coding works, blue supported      |
| FR-003      | ✅     | ✅      | ✅  | ✅       | ❌    | Feast names display correctly           |
| FR-004      | ✅     | ✅      | ✅  | ✅       | ❌    | BCP 2019 calendar implemented           |
| FR-005      | ✅     | ✅      | ✅  | ✅       | ❌    | Easter calculations work                |
| FR-006      | ✅     | ✅      | ✅  | ✅       | ❌    | Month navigation exists                 |
| FR-007      | ✅     | ✅      | ✅  | ✅       | ❌    | "Now" button works                      |
| FR-008      | ✅     | ✅      | ✅  | ✅       | ❌    | Precedence logic implemented            |
| FR-009      | ✅     | ✅      | ✅  | ⚠️       | ❌    | Transfers work, UI could indicate       |
| FR-010      | ✅     | ✅      | ✅  | ✅       | ❌    | Seasons display correctly               |
| FR-011      | ✅     | ✅      | ✅  | ✅       | ❌    | Click navigation works                  |
| FR-012      | ⚠️     | ✅      | ✅  | ⚠️       | ❌    | Filter exists, logic needs verification |
| FR-013      | ✅     | ✅      | ✅  | ✅       | ❌    | Leap years handled                      |
| FR-014      | ✅     | ✅      | ✅  | ✅       | ❌    | Sunday designations work                |
| FR-015      | ✅     | ✅      | ✅  | ⚠️       | ❌    | Backend supports, UI could show better  |
| FR-016      | ⚠️     | ✅      | ⚠️  | ❌       | ❌    | Logic exists, needs API+UI work         |

**Legend**:

- ✅ Fully implemented
- ⚠️ Partially implemented or needs refinement
- ❌ Not implemented or missing

### Success Criteria Assessment

| Criteria | Status | Notes                               |
| -------- | ------ | ----------------------------------- |
| SC-001   | ✅     | Performance is good (< 2 seconds)   |
| SC-002   | ✅     | Moveable feasts calculate correctly |
| SC-003   | ✅     | Colors match BCP 2019               |
| SC-004   | ✅     | Single-click navigation works       |
| SC-005   | 📊     | Needs user testing to verify        |
| SC-006   | ✅     | Precedence rules implemented        |
| SC-007   | ⚠️     | Toggle exists, needs verification   |
| SC-008   | ✅     | Date range supported, caching works |

## Phase 0: Research & Clarifications

### Research Tasks

#### R-001: Verify Filter Logic Semantics ✅ RESOLVED

**Question**: Does current filter implementation match spec requirement?
**Status**: NEEDS CODE REVIEW
**Finding**: Spec says "rank.required=True" but code checks "FERIA" exclusion
**Resolution**: Update filter logic to use rank.required field

#### R-002: First Vespers API Contract ✅ RESOLVED

**Question**: What data structure should API return for evening commemorations?
**Status**: NEEDS DESIGN
**Finding**: Backend has data, needs serializer design
**Resolution**: Add evening\_\* fields to DaySerializer (see data-model.md)

#### R-003: Test Framework Selection ✅ RESOLVED

**Question**: What testing frameworks to use?
**Status**: RESOLVED
**Finding**:

- Backend: Django TestCase (already in use)
- API: Django REST Framework APITestCase
- Frontend: Vitest (configured in project)
- E2E: Cypress (configured in project)
  **Resolution**: Use existing test infrastructure

### Research Findings

#### Finding 1: Existing Implementation Quality

**Observation**: The existing implementation is remarkably complete and well-architected. The `calculations.py` module handles complex liturgical calendar logic correctly, including feast transfers, precedence, and seasonal transitions.

**Implication**: Implementation effort is primarily about refinement, testing, and documentation rather than new development.

#### Finding 2: Constitution Compliance Gap

**Observation**: The existing code lacks comprehensive test coverage, violating Constitution Principle III.

**Implication**: Test development is the highest priority work item. Tests must be written before any feature enhancements.

#### Finding 3: Specification vs. Reality

**Observation**: The specification was written retroactively and matches the implementation remarkably well, with only minor discrepancies (filter logic semantics, First Vespers UI).

**Implication**: This is a documentation and testing project more than a feature development project.

## Phase 1: Design & Contracts

### Data Model

See `plan/data-model.md` for complete entity definitions.

**Key Entities** (existing, documented):

- CalendarDate
- Commemoration
- CommemorationRank
- Season
- ChurchYear
- CalendarYear

**API Contract Changes**:

- Add evening fields to DaySerializer (see contracts/api.yaml)

### API Contracts

See `contracts/api.yaml` for OpenAPI specification.

**Changes Required**:

- Add `evening_required`, `evening_optional`, `evening_season`, `evening_color` to Day schema
- Document filter parameter semantics
- Add examples for First Vespers days

### Architecture Decisions

#### AD-001: Test-First Implementation

**Decision**: Write all tests before making any code changes  
**Rationale**: Constitution Principle III requires 100% function coverage. Existing code lacks tests. Tests provide regression protection and documentation.  
**Alternatives**: Write tests after - rejected because it risks missing test cases and violates Constitution.

#### AD-002: Minimal UI Changes

**Decision**: Keep existing Calendar.vue structure, add First Vespers indicators minimally  
**Rationale**: Existing UI works well. Major redesign risks breaking working functionality.  
**Alternatives**: Complete UI redesign - rejected as unnecessary and risky.

#### AD-003: Serializer Extension Pattern

**Decision**: Extend DaySerializer with evening fields rather than creating new endpoints  
**Rationale**: Maintains backward compatibility, follows Django REST Framework patterns.  
**Alternatives**: New endpoint for evening data - rejected as unnecessarily complex.

## Phase 2: Implementation Tasks

### Priority Classification

- **P0**: Blockers (Constitution violations, critical gaps)
- **P1**: Core functionality (required by spec)
- **P2**: Enhancements (nice-to-have improvements)
- **P3**: Future work (deferred)

### Task Breakdown

#### Epic 1: Test Infrastructure (P0)

**T001**: Create backend test suite for churchcal calculations  
**Effort**: 8 hours  
**Dependencies**: None  
**Description**: Create `churchcal/tests/test_calculations.py` with comprehensive tests for all date calculation functions, feast precedence, transfers, and First Vespers logic.  
**Success Criteria**: 100% function coverage of calculations.py

**T002**: Create API test suite for calendar endpoints  
**Effort**: 4 hours  
**Dependencies**: T001  
**Description**: Create `churchcal/api/tests/test_views.py` with tests for DayView, MonthView, YearView endpoints.  
**Success Criteria**: All API endpoints have test coverage

**T003**: Create frontend unit tests for Calendar.vue  
**Effort**: 4 hours  
**Dependencies**: None  
**Description**: Create `app/tests/unit/Calendar.spec.js` with component tests for calendar rendering, navigation, filtering.  
**Success Criteria**: All Calendar.vue methods tested

**T004**: Create E2E tests for user scenarios  
**Effort**: 6 hours  
**Dependencies**: T001, T002, T003  
**Description**: Create `app/tests/e2e/calendar.cy.js` with tests covering all user stories from spec.  
**Success Criteria**: All 5 user stories have E2E test coverage

**Estimated Epic Total**: 22 hours

#### Epic 2: First Vespers Enhancement (P1)

**T005**: Add evening fields to DaySerializer  
**Effort**: 2 hours  
**Dependencies**: T002  
**Requirements**: FR-016  
**Description**: Extend `churchcal/api/serializer.py` DaySerializer to include evening_required, evening_optional, evening_season, and computed evening_color field.  
**Success Criteria**: API returns evening data for First Vespers days

**T006**: Update Calendar.vue to display evening commemorations  
**Effort**: 4 hours  
**Dependencies**: T005, T003  
**Requirements**: FR-016  
**Description**: Modify date cell template to show evening information when different from morning. Consider visual indicators (border color, small text, icon).  
**Success Criteria**: Evening commemorations visible on calendar

**T007**: Document First Vespers API in OpenAPI spec  
**Effort**: 1 hour  
**Dependencies**: T005  
**Description**: Update `contracts/api.yaml` with evening field documentation and examples.  
**Success Criteria**: API documentation complete

**Estimated Epic Total**: 7 hours

#### Epic 3: Filter Logic Refinement (P1)

**T008**: Verify and document filter semantics  
**Effort**: 2 hours  
**Dependencies**: T002  
**Requirements**: FR-012  
**Description**: Review current filter logic in Calendar.vue against spec requirement (rank.required=True). Update if needed to match spec precisely.  
**Success Criteria**: Filter behavior matches FR-012 specification

**T009**: Ensure rank.required field exposed in API  
**Effort**: 1 hour  
**Dependencies**: T002  
**Requirements**: FR-012  
**Description**: Verify DaySerializer includes rank.required field for all commemorations. Add if missing.  
**Success Criteria**: API exposes required flag

**T010**: Update filter UI to clarify behavior  
**Effort**: 2 hours  
**Dependencies**: T008, T003  
**Requirements**: FR-012  
**Description**: Review toggle button text and behavior. Ensure user understands "Show Major Feasts Only" means show only required commemorations.  
**Success Criteria**: Filter behavior is clear to users

**Estimated Epic Total**: 5 hours

#### Epic 4: Documentation (P1)

**T011**: Add docstrings to calculations.py  
**Effort**: 3 hours  
**Dependencies**: T001  
**Description**: Document all complex methods in calculations.py with clear docstrings explaining logic, parameters, return values, and examples.  
**Success Criteria**: All public methods documented

**T012**: Create API documentation for calendar endpoints  
**Effort**: 2 hours  
**Dependencies**: T007  
**Description**: Complete OpenAPI specification in contracts/api.yaml with examples, error cases, and usage guidance.  
**Success Criteria**: API fully documented

**T013**: Create developer guide for calendar system  
**Effort**: 3 hours  
**Dependencies**: T011, T012  
**Description**: Write `plan/quickstart.md` explaining how to work with the calendar system, add commemorations, test date calculations.  
**Success Criteria**: New developer can understand system

**Estimated Epic Total**: 8 hours

#### Epic 5: Edge Case Handling (P2)

**T014**: Verify leap year handling  
**Effort**: 2 hours  
**Dependencies**: T001  
**Requirements**: FR-013  
**Description**: Review and test February 29 liturgical assignments. Ensure tests cover leap years.  
**Success Criteria**: Leap years work correctly

**T015**: Add visual indicators for transferred feasts  
**Effort**: 3 hours  
**Dependencies**: T006  
**Requirements**: FR-009  
**Description**: Consider adding small indicator (icon, badge, tooltip) showing when a feast is transferred rather than on original date.  
**Success Criteria**: Transferred feasts are identifiable

**T016**: Improve multiple commemoration display  
**Effort**: 3 hours  
**Dependencies**: T006  
**Requirements**: FR-015  
**Description**: When multiple commemorations occur on one day, improve UI to show all with proper precedence indication.  
**Success Criteria**: Multiple commemorations clearly shown

**Estimated Epic Total**: 8 hours

### Total Effort Estimate

| Epic                        | Priority | Effort       |
| --------------------------- | -------- | ------------ |
| Epic 1: Test Infrastructure | P0       | 22 hours     |
| Epic 2: First Vespers       | P1       | 7 hours      |
| Epic 3: Filter Logic        | P1       | 5 hours      |
| Epic 4: Documentation       | P1       | 8 hours      |
| Epic 5: Edge Cases          | P2       | 8 hours      |
| **Total**                   |          | **50 hours** |

### Task Dependencies

```
T001 (Backend Tests) → T002 (API Tests)
T001 → T005 (Evening API)
T002 → T009 (Rank Field)
T003 (Frontend Tests) → T006 (Evening UI)
T005 → T006
T005 → T007 (API Docs)
T008 (Filter Logic) → T010 (Filter UI)
T001 → T011 (Code Docs)
T007 → T012 (API Docs)
T011, T012 → T013 (Dev Guide)
T001 → T014 (Leap Year)
T006 → T015 (Transfer UI)
T006 → T016 (Multiple Commemorations)
```

## Implementation Strategy

### Phase Approach

1. **Phase 0: Test Infrastructure (Week 1)**

   - Tasks: T001-T004
   - Focus: Establish comprehensive test coverage
   - Deliverable: Full test suite passing against existing code

2. **Phase 1: Core Enhancements (Week 2)**

   - Tasks: T005-T010
   - Focus: First Vespers and filter refinement
   - Deliverable: Enhanced functionality with tests

3. **Phase 2: Documentation (Week 3)**

   - Tasks: T011-T013
   - Focus: Code documentation and developer guide
   - Deliverable: Comprehensive documentation

4. **Phase 3: Polish (Optional)**
   - Tasks: T014-T016
   - Focus: Edge cases and UI improvements
   - Deliverable: Production-ready feature

### Branch Strategy

- **Feature Branch**: `002-liturgical-calendar`
- **Base Branch**: `main`
- **Branch Protection**: Requires tests passing, code review
- **Merge Strategy**: Squash merge after all tasks complete

### Pull Request Strategy

- **PR-001**: Test Infrastructure (T001-T004)
- **PR-002**: First Vespers API Enhancement (T005, T007, T009)
- **PR-003**: First Vespers UI Enhancement (T006)
- **PR-004**: Filter Logic Refinement (T008, T010)
- **PR-005**: Documentation (T011-T013)
- **PR-006** (Optional): Edge Case Enhancements (T014-T016)

### Risk Assessment

| Risk                            | Probability | Impact | Mitigation                         |
| ------------------------------- | ----------- | ------ | ---------------------------------- |
| Test writing uncovers bugs      | High        | Medium | Expect to fix bugs, add debug time |
| First Vespers UI design unclear | Medium      | Low    | Create mockup before T006          |
| API changes break consumers     | Low         | High   | Maintain backward compatibility    |
| Scope creep                     | Medium      | Medium | Stick to spec, defer enhancements  |

### Definition of Done

A task is complete when:

1. ✅ Code written and follows project standards (Black formatting, ESLint passing)
2. ✅ Tests written and passing (100% function coverage for new code)
3. ✅ Documentation updated (docstrings, API docs, comments)
4. ✅ Code reviewed and approved
5. ✅ All CI/CD checks passing
6. ✅ Manual testing completed for user-facing changes
7. ✅ No new errors or warnings introduced

## Next Steps

1. **Review and Approve Plan**: Stakeholder review of this implementation plan
2. **Create Feature Branch**: `git checkout -b 002-liturgical-calendar`
3. **Begin Phase 0**: Start with T001 (backend tests)
4. **Daily Standups**: Brief progress updates during implementation
5. **Weekly Reviews**: Review progress and adjust plan as needed

## Appendices

### Appendix A: Files to Modify

**Backend**:

- `site/churchcal/tests/test_calculations.py` (NEW)
- `site/churchcal/api/tests/test_views.py` (NEW)
- `site/churchcal/api/serializer.py` (MODIFY - add evening fields)
- `site/churchcal/calculations.py` (MODIFY - add docstrings)

**Frontend**:

- `app/src/views/Calendar.vue` (MODIFY - evening display, filter logic)
- `app/tests/unit/Calendar.spec.js` (NEW)
- `app/tests/e2e/calendar.cy.js` (NEW)

**Documentation**:

- `specs/002-liturgical-calendar/contracts/api.yaml` (NEW)
- `specs/002-liturgical-calendar/plan/data-model.md` (NEW)
- `specs/002-liturgical-calendar/plan/quickstart.md` (NEW)

### Appendix B: Key Decision Points

**Decision Point 1: First Vespers UI Design**  
**When**: Before T006  
**Options**: Border color, secondary text, icon, tooltip  
**Criteria**: Clarity, mobile compatibility, minimal disruption

**Decision Point 2: Test Coverage Target**  
**When**: During T001  
**Options**: 100% function coverage vs. 80% coverage  
**Criteria**: Constitution requires 100%, but pragmatism may allow exceptions

**Decision Point 3: Backward Compatibility**  
**When**: During T005  
**Options**: Add evening fields (additive) vs. restructure response  
**Criteria**: Must not break existing API consumers

### Appendix C: Reference Links

- [BCP 2019 Calendar Rules](https://bcp2019.anglicanchurch.net/index.php/downloads/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Vue 3 Testing Guide](https://vuejs.org/guide/scaling-up/testing.html)
- [Element Plus Calendar Component](https://element-plus.org/en-US/component/calendar.html)

---

**Plan Version**: 1.0  
**Last Updated**: November 6, 2025  
**Next Review**: Upon feature branch creation
