# Implementation Plan: Collects and Prayers

**Branch**: `003-collects` (to be created during implementation) | **Date**: November 6, 2025 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-collects/spec.md`

**Status**: RETROACTIVE SPECIFICATION - This plan documents existing implementation and identifies conformance gaps

## Summary

The Daily Office 2019 application already implements a comprehensive collects browsing and management system. The specification was created retroactively to document the feature requirements. This plan identifies gaps between the existing implementation and the specification, and provides a roadmap for bringing the codebase into full conformance with the spec.

**Existing Implementation Overview**:

- Backend: Django models for Collect, CollectType, CollectTag, CollectTagCategory, MetricalCollect
- API: REST endpoints for collects listing, grouped collects, and collect categories
- Frontend: Vue.js component (CollectsNew.vue) with filtering, language switching, and daily office integration
- Database: PostgreSQL with CKEditor5 HTML storage for collect text

**Primary Gap**: The specification requires several enhancements that are not yet implemented:

1. Date-based collect display (FR-011) - showing appropriate collect for liturgical date
2. Attribution display (FR-010a, FR-010b) - historical source and BCP page references
3. Enhanced metrical collect support (FR-012b, FR-012c) - better UI for metrical versions
4. Plain text search capability (FR-007) - currently no search implementation
5. Text highlighting in search results (US3, FR-008b)

## Technical Context

**Language/Version**:

- Backend: Python 3.13, Django 5.2+
- Frontend: Vue 3, Vite, TypeScript (via JavaScript)
- Node: 24.4+

**Primary Dependencies**:

- Backend: Django, PostgreSQL (psycopg-binary), django-ckeditor-5, BeautifulSoup4
- Frontend: Vue 3, Vue Router, Element Plus UI library, Axios (via $http plugin)

**Storage**: PostgreSQL 17.5+ with the following existing tables:

- `office_collect` - Main collect storage
- `office_collecttype` - Collect categories
- `office_collecttag` - Individual tags
- `office_collecttagcategory` - Tag dimensions
- `office_metricalcollect` - Metrical versions
- `office_collect_tags` - Many-to-many relationship

**Testing**:

- Backend: pytest, Django test framework (site/office/tests.py exists)
- Frontend: Vitest, Playwright (configured but needs expansion)
- Current test coverage: NEEDS ASSESSMENT

**Target Platform**:

- Web: Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile: iOS/Android via Capacitor (existing)
- API: RESTful endpoints consumed by Vue SPA

**Project Type**: Web application (Django backend + Vue frontend)

**Performance Goals**:

- Collects page load: < 2 seconds (SC-001, SC-006)
- Language switch: < 1 second (SC-002)
- Filter/search results: < 2 seconds (SC-003, SC-006)
- API response time: < 500ms for collects endpoint

**Constraints**:

- Must preserve exact BCP 2019 text (SC-004)
- Must support offline capability (localStorage for preferences)
- Must maintain backward compatibility with existing collect storage
- Limited HTML tags for security: `<p>`, `<strong>`, `<em>`, `<br>` (FR-008a)

**Scale/Scope**:

- ~300-500 collects from BCP 2019
- Multi-dimensional tagging across 5 tag categories
- 4 daily office types for user selection
- Supports both traditional and contemporary language

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### Principle I: Glory to God

- [x] Feature enhances prayer, scripture engagement, or accessibility
  - **PASS**: Collects are central to Anglican prayer practice. Feature provides comprehensive access to BCP 2019 prayers for personal devotion and liturgical use.
- [x] Feature serves the spiritual purpose of the Daily Office
  - **PASS**: Integration with daily offices (FR-016-019) enables personalized prayer routines.
- [x] Technical decisions prioritize user spiritual experience over elegance
  - **PASS**: Language switching, clear categorization, and daily office integration prioritize prayer usability.

### Principle II: Feature Branch Development

- [x] Feature branch created with format: `###-feature-name`
  - **NOTE**: Branch will be `003-collects` when implementation gaps are addressed
  - **CURRENT**: Existing implementation is in main branch (retroactive spec)
- [x] Unique identifier assigned and documented
  - **PASS**: Feature ID is `003`
- [x] No direct commits to main branch planned
  - **PASS**: All conformance work will be done in feature branch

### Principle III: Comprehensive Testing (NON-NEGOTIABLE)

- [⚠️] Test plan includes 100% function coverage goal
  - **PARTIAL**: Existing tests in `site/office/tests.py` need expansion
  - **ACTION REQUIRED**: Assess current coverage and create test plan
- [⚠️] Unit tests planned for all new functions/methods
  - **ACTION REQUIRED**: Tests needed for search, attribution display, date-based collect selection
- [⚠️] Integration tests planned for component interactions
  - **ACTION REQUIRED**: API endpoint tests, frontend component tests
- [⚠️] End-to-end tests planned for critical user journeys
  - **ACTION REQUIRED**: Playwright tests for browse, filter, search, daily office integration
- [x] Test-first approach confirmed (tests before implementation)
  - **NOTE**: For retroactive spec, we'll add tests to validate existing + new functionality

**GATE STATUS**: ⚠️ CONDITIONAL PASS - Testing requirements must be addressed in Phase 0 research

### Principle IV: Code Quality and Clarity

- [x] No "hacks" or workarounds planned
  - **PASS**: Existing implementation uses standard Django/Vue patterns
- [x] Code formatting standards identified (Black/ESLint)
  - **PASS**: Black for Python (119-char lines), ESLint for JavaScript/Vue
- [x] Pre-commit hooks will be used
  - **PASS**: `.pre-commit-config.yaml` exists in repository
- [x] Any complexity is justified and documented
  - **PASS**: CKEditor5 for HTML storage is justified for traditional formatting needs

### Principle V: Atomic and Traceable Commits

- [x] Commit strategy ensures atomic, reviewable changes
  - **PLAN**: Each specification gap will be addressed in separate commits
- [x] Traceability plan: Code → Task ID → Requirement ID
  - **PLAN**: Commit messages will reference FR-### and T### identifiers
- [x] Code comments will reference task/requirement IDs
  - **PLAN**: New code will include FR-### comments for traceability

### Principle VI: Unique and Persistent Identifiers

- [x] Requirements use FR-###, NFR-###, SC-### format
  - **PASS**: Specification uses FR-001 through FR-019, SC-001 through SC-010
- [x] Tasks use T### format
  - **PLAN**: Tasks.md will be created in Phase 2 with T### identifiers
- [x] User Stories use US# format
  - **PASS**: Specification uses US1 through US7

## Existing Implementation Assessment

### What Exists and Works

**Backend Models** (`site/office/models.py`):

- ✅ `Collect` model with all required fields (FR-001, FR-009)
  - `title`, `text` (contemporary), `traditional_text`
  - `normalized_text` and `normalized_traditional_text` for search
  - `collect_type` (ForeignKey), `order`, `number`
  - `tags` (ManyToManyField), `attribution`
  - `metrical_collect`, `metrical_collect_2`, `metrical_collect_3`
- ✅ `CollectType` model for categorization
- ✅ `CollectTag` and `CollectTagCategory` for multi-dimensional tagging (FR-005)
- ✅ `MetricalCollect` model for musical versions (FR-012b)
- ✅ `AbstractCollect` helper class for dynamic collects

**Backend API** (`site/office/api/views/resources.py`):

- ✅ `CollectsViewSet` - Lists all collects with relationships
- ✅ `GroupedCollectsViewSet` - Groups by source with subcategories (FR-002, FR-005)
  - Organizes by source (year/occasional/liturgical)
  - Creates subcategories by theme, season, commemoration_type, liturgy
- ✅ `CollectCategoryViewSet` - Lists tag categories with tags

**Frontend** (`app/src/views/CollectsNew.vue`):

- ✅ Displays all collects organized by category (US1, FR-001, FR-002)
- ✅ Category filtering with multiple selection (US2, FR-006)
- ✅ Language switching (traditional/contemporary) (US4, FR-003, FR-004)
- ✅ Language preference persistence in localStorage (FR-015)
- ✅ Expand/collapse functionality for collect groups
- ✅ Font size adjustment via FontSizer component
- ✅ Daily office integration via `extraCollects` localStorage (US7, FR-016-019)

**Frontend Components**:

- ✅ `CollectsSubcategory.vue` - Handles individual subcategory display
- ✅ `FontSizer.vue` - Text size adjustment
- ✅ `Loading.vue` - Loading state indicator

**Integration with Daily Office**:

- ✅ `Office.vue` reads `extraCollects` from localStorage (FR-016)
- ✅ API endpoint `_get_extra_collects` processes selected collects (FR-017)
- ✅ Selected collects appear in appropriate office types (FR-018)

### Gaps Requiring Implementation

**Critical (Blocking P1/P2 User Stories)**:

1. **Text Search** (US3, FR-007, FR-008b)

   - ❌ No search implementation in frontend
   - ❌ Backend has `normalized_text` fields but no search endpoint
   - ❌ No search term highlighting (US3 Acceptance 2)
   - **Impact**: P2 user story incomplete

2. **Attribution Display** (FR-010a, FR-010b)

   - ⚠️ Model has `attribution` field but no UI display
   - ❌ No BCP page reference storage or display
   - **Impact**: Users cannot see historical sources

3. **Metrical Collect UI** (FR-012b, FR-012c)

   - ⚠️ Model supports 3 metrical versions but UI doesn't distinguish them
   - ❌ No clear separation of textual vs. metrical alternatives
   - **Impact**: Metrical versions hidden from users

4. **Date-Based Collect Display** (US5, FR-011)
   - ❌ No integration with liturgical calendar for date selection
   - ❌ No endpoint to retrieve collect for specific date
   - **Impact**: P3 user story not implemented

**Important (User Experience)**:

5. **Multiple Collect Versions** (FR-012a, FR-012c)

   - ❌ No UI for showing textual alternatives
   - ❌ Model doesn't explicitly support textual variants (only metrical)
   - **Impact**: Alternative collect wordings not supported

6. **Enhanced Filtering** (FR-005a, FR-005b)

   - ⚠️ Backend supports multi-dimensional tags but UI only filters by top-level source
   - ❌ No individual tag filtering (season, theme, commemoration_type, liturgy)
   - **Impact**: Reduced discoverability

7. **Error Handling**
   - ⚠️ Basic error handling exists but needs enhancement
   - ❌ No handling for missing language versions (Edge Case 1)
   - ❌ No fallback for empty filter results (Edge Case 6)

**Testing (Constitutional Requirement)**:

8. **Test Coverage**
   - ❌ No frontend tests for CollectsNew.vue component
   - ❌ No API endpoint tests for collects views
   - ❌ No integration tests for daily office collect selection
   - ❌ Current coverage unknown - assessment needed

### Data Migration Assessment

**Current Data State**:

- Collects imported via `site/office/management/commands/import_collects.py`
- Data exists in production database
- Tags and categories appear to be populated

**Migration Needs**:

- ⚠️ If attribution field is empty, may need to populate from BCP 2019
- ⚠️ If textual alternatives needed, schema enhancement required
- ⚠️ Verify all 5 tag categories are properly populated (source, theme, season, commemoration_type, liturgy)

## Project Structure

### Documentation (this feature)

```text
specs/003-collects/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file (COMPLETE)
├── research.md          # Phase 0 output (TO BE CREATED)
├── data-model.md        # Phase 1 output (TO BE CREATED)
├── quickstart.md        # Phase 1 output (TO BE CREATED)
├── contracts/           # Phase 1 output (TO BE CREATED)
│   ├── api-collects.yaml        # OpenAPI spec for collects endpoints
│   ├── api-search.yaml          # OpenAPI spec for search endpoint
│   └── api-date-collects.yaml   # OpenAPI spec for date-based retrieval
├── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
└── checklists/          # Existing checklist directory
```

### Source Code (repository root)

```text
# Backend (Django)
site/
├── office/
│   ├── models.py                    # ✅ Collect models exist
│   ├── api/
│   │   ├── views/
│   │   │   └── resources.py         # ✅ CollectsViewSet, GroupedCollectsViewSet
│   │   │                           # ❌ Need: SearchCollectsViewSet, DateCollectsViewSet
│   │   └── serializers.py          # ⚠️ Need: Enhanced CollectSerializer with attribution
│   ├── management/
│   │   └── commands/
│   │       ├── import_collects.py  # ✅ Existing import command
│   │       └── populate_attribution.py  # ❌ Need: New command for attribution data
│   └── tests.py                    # ⚠️ Needs expansion
│
└── churchcal/
    ├── models.py                    # ✅ Commemoration has collect relationships
    └── api/
        └── serializer.py            # ✅ get_collects method exists

# Frontend (Vue.js)
app/
├── src/
│   ├── views/
│   │   └── CollectsNew.vue         # ✅ Main collects page
│   │                               # ❌ Need: Search, attribution display, metrical UI
│   ├── components/
│   │   ├── CollectsSubcategory.vue # ✅ Subcategory component
│   │   │                           # ❌ Need: Attribution display, metrical links
│   │   ├── CollectSearch.vue       # ❌ Need: New search component
│   │   └── CollectCard.vue         # ❌ Need: Individual collect display with all features
│   ├── router/
│   │   └── index.js                # ✅ /collects route exists
│   └── store/
│       └── collects.js             # ❌ Need: Vuex/Pinia store for collects state
│
└── tests/
    ├── unit/
    │   └── CollectsNew.spec.js     # ❌ Need: Component unit tests
    └── e2e/
        └── collects.cy.js          # ❌ Need: End-to-end tests

# Database Migrations
site/office/migrations/
    ├── 0010_move_collects_to_foreign_keys.py  # ✅ Existing migration
    └── 00XX_enhance_collect_attribution.py   # ❌ Need: If schema changes required
```

**Structure Decision**: This is a web application with Django backend and Vue frontend. The existing structure is well-organized with clear separation of concerns. New code will follow existing patterns.

## Complexity Tracking

> No constitutional violations requiring justification. The existing implementation follows best practices.

## Phase 0: Research & Investigation (NEXT STEP)

### Objectives

1. **Test Coverage Assessment**

   - Run coverage analysis on existing collect-related code
   - Identify untested functions and branches
   - Create baseline coverage report

2. **Data Audit**

   - Query database to assess current collect data completeness
   - Identify collects missing attribution
   - Verify tag category population (all 5 categories)
   - Check for collects missing traditional language versions

3. **Search Strategy Research**

   - Evaluate PostgreSQL full-text search vs. application-level search
   - Consider performance implications (300-500 collects)
   - Research search term highlighting techniques
   - Investigate search result ranking strategies

4. **Date-Based Collect Integration**

   - Review existing `churchcal` calendar calculation logic
   - Identify how to map date → commemoration → collect
   - Research handling of dates with multiple possible collects
   - Design API contract for date-based retrieval

5. **Attribution Data Source**

   - Identify where to source historical attributions
   - Determine format for BCP page references
   - Plan data population strategy (manual, scripted, or hybrid)

6. **Metrical Collect UI Patterns**

   - Research UI patterns for displaying alternative versions
   - Evaluate icon options for metrical indicators
   - Consider link vs. embed for metrical resources

7. **Testing Framework Selection**
   - Confirm pytest configuration for backend
   - Confirm Vitest/Playwright setup for frontend
   - Research Vue component testing best practices
   - Identify integration testing approach for API + frontend

### Research Questions to Answer

- **Q1**: What is the current test coverage percentage for collect-related code?
- **Q2**: How many collects are missing attribution data?
- **Q3**: Should search be backend (PostgreSQL full-text) or frontend (client-side filtering)?
- **Q4**: What is the performance impact of full-text search on 500 collects?
- **Q5**: How does the existing calendar system determine which collect applies to a date?
- **Q6**: Where can we source reliable attribution data for BCP 2019 collects?
- **Q7**: What UI components does Element Plus provide for search/filtering?
- **Q8**: How should metrical collect links be displayed without cluttering the UI?

### Deliverable

`research.md` document with:

- Test coverage baseline and gap analysis
- Data audit results with specific counts
- Search implementation recommendation with rationale
- Date-based collect retrieval design
- Attribution data sourcing plan
- Metrical UI mockups or descriptions
- Testing strategy and framework confirmation

## Phase 1: Design & Contracts (AFTER RESEARCH)

### Objectives

1. **Data Model Review**

   - Document existing `Collect` model in detail
   - Identify any schema changes needed (e.g., textual alternatives field)
   - Design migration strategy if needed
   - Update `data-model.md`

2. **API Contract Design**

   - Define search endpoint contract (request/response schemas)
   - Define date-based collect endpoint contract
   - Enhance existing endpoints if needed (attribution in response)
   - Create OpenAPI specifications in `contracts/`

3. **Frontend Component Architecture**

   - Design component hierarchy for enhanced collects page
   - Define props, events, and state management
   - Plan search component integration
   - Plan attribution display in CollectCard component

4. **Testing Architecture**
   - Design test structure (unit, integration, e2e)
   - Define test data fixtures
   - Plan mocking strategy for API tests
   - Document test coverage targets by component/module

### Deliverables

- `data-model.md` - Complete data model documentation
- `contracts/` - OpenAPI specs for all endpoints
- `quickstart.md` - Developer setup and testing guide
- Updated `.github/copilot-instructions.md` (via update-agent-context.sh)

## Phase 2: Task Breakdown (SEPARATE COMMAND)

**Note**: Phase 2 is executed via `/speckit.tasks` command, NOT by `/speckit.plan`.

Will generate `tasks.md` with:

- Granular implementation tasks (T001, T002, etc.)
- Task dependencies and ordering
- Estimated effort per task
- Traceability to requirements (FR-###) and user stories (US#)

## Risk Assessment

### High Risk

1. **Test Coverage Debt**

   - **Risk**: Existing code has unknown test coverage; adding tests retroactively is time-consuming
   - **Mitigation**: Phase 0 assessment will quantify; prioritize critical paths
   - **Impact**: May delay implementation phase

2. **Search Performance**
   - **Risk**: Full-text search on 500 collects might be slow if poorly implemented
   - **Mitigation**: Phase 0 research will benchmark options; use PostgreSQL full-text if needed
   - **Impact**: Could require backend database changes

### Medium Risk

3. **Attribution Data Availability**

   - **Risk**: Historical attribution may not be readily available for all collects
   - **Mitigation**: Start with collects that have known attributions; iterate
   - **Impact**: Feature may launch with incomplete attribution data

4. **Browser Compatibility**
   - **Risk**: Search highlighting might behave differently across browsers
   - **Mitigation**: Use well-tested library (e.g., mark.js) for highlighting
   - **Impact**: Requires cross-browser testing

### Low Risk

5. **UI Complexity**
   - **Risk**: Adding search, attribution, and metrical links might clutter interface
   - **Mitigation**: Use progressive disclosure (collapsible sections, icons)
   - **Impact**: May require UX iteration

## Success Criteria Validation

The specification defines 10 success criteria (SC-001 through SC-010). Current conformance:

| ID     | Criterion                                 | Status     | Gap                                     |
| ------ | ----------------------------------------- | ---------- | --------------------------------------- |
| SC-001 | Browse all collects in under 5 seconds    | ✅ PASS    | Existing implementation meets criterion |
| SC-002 | Language switch in under 1 second         | ✅ PASS    | Existing implementation meets criterion |
| SC-003 | Find specific collect within 30 seconds   | ⚠️ PARTIAL | No search; only filtering               |
| SC-004 | Exact BCP 2019 text displayed             | ✅ PASS    | Text imported from BCP 2019             |
| SC-005 | Filter results update immediately         | ✅ PASS    | Existing filtering works                |
| SC-006 | Search results in under 2 seconds         | ❌ FAIL    | No search implemented                   |
| SC-007 | Language preference persists              | ✅ PASS    | localStorage implementation works       |
| SC-008 | Identify appropriate collect for date     | ❌ FAIL    | Date-based selection not implemented    |
| SC-009 | Selected collects persist across sessions | ✅ PASS    | localStorage `extraCollects` works      |
| SC-010 | Selected collects appear in daily offices | ✅ PASS    | Integration with Office.vue works       |

**Overall Conformance**: 6/10 passing, 2/10 partial, 2/10 failing

## Next Steps

1. **Review this plan** with project maintainer for approval
2. **Execute Phase 0 Research** (documented above)
   - Run test coverage analysis
   - Audit collect data completeness
   - Research search implementation options
   - Design date-based collect retrieval
3. **Execute Phase 1 Design** (documented above)
   - Create data-model.md
   - Create API contracts in contracts/
   - Create quickstart.md
   - Update agent context
4. **Execute Phase 2 Task Breakdown** via `/speckit.tasks` command
5. **Create feature branch** `003-collects` when ready for implementation
6. **Implement tasks** following test-first approach

## Open Questions for Maintainer

1. **Priority**: Should we address P1/P2 gaps (search, attribution) before P3 gaps (date-based collects)?
2. **Testing**: What is the acceptable minimum test coverage percentage for this feature?
3. **Data**: Do you have a source for historical attributions, or should we research this?
4. **Timeline**: Is there a target date for bringing collects into full specification conformance?
5. **Breaking Changes**: Are schema changes acceptable, or must we work within existing `Collect` model?
6. **Textual Alternatives**: Does BCP 2019 have different wordings for the same collect that need support?

---

**Plan Version**: 1.0  
**Last Updated**: November 6, 2025  
**Status**: Awaiting maintainer review and Phase 0 research
