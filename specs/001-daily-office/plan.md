# Implementation Plan: Daily Office Liturgy (Conformance Audit)

**Branch**: `001-daily-office` (Retroactive Documentation) | **Date**: November 6, 2025 | **Spec**: [spec.md](./spec.md)  
**Type**: Conformance Audit & Constitution Alignment  
**Status**: Existing Feature - Documentation & Compliance Review

**Note**: This feature was implemented prior to the establishment of the project constitution (2025-11-06). This plan documents the existing implementation and identifies gaps for constitutional compliance.

## Summary

The Daily Office feature is **fully implemented and production-ready**, providing all four traditional offices (Morning Prayer, Evening Prayer, Midday Prayer, Compline) plus four Family Prayer variants. The system dynamically generates liturgical content based on the Book of Common Prayer 2019, the Anglican liturgical calendar, and multi-year lectionary cycles. This plan audits the existing implementation against the retroactive specification and identifies areas requiring constitutional compliance improvements, particularly comprehensive testing, documentation, and traceability.

**Primary Requirement**: Display complete daily prayer services with proper readings, psalms, canticles, and prayers according to BCP 2019.

**Technical Approach**: Django backend generates liturgical content via modular `Office` classes, Vue 3 frontend consumes REST API, Bible Gateway integration with local caching, client-side preference storage.

## Technical Context

**Language/Version**:

- Backend: Python 3.13
- Frontend: JavaScript ES2020+ with TypeScript support

**Primary Dependencies**:

- Backend: Django 5.2+, psycopg-binary (PostgreSQL adapter), Arrow (date handling), BeautifulSoup4 (HTML parsing), django-environ (environment config)
- Frontend: Vue 3.4+, Vite 5+, Vue Router 4, Element Plus (UI components), Pinia (state management)
- Mobile: Capacitor 6+ for iOS/Android apps

**Storage**: PostgreSQL 17.5+ (liturgical calendar data, office readings, psalm assignments, scripture cache, settings)

**Testing**:

- Backend: pytest (framework present but coverage unknown)
- Frontend: Vitest + Cypress (configured but test status unknown)
- **CRITICAL GAP**: Test coverage status unknown - Constitution Principle III violation

**Target Platform**:

- Web: Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile: iOS 15+, Android 8+
- API: Linux server (Debian/Ubuntu)

**Project Type**: Full-stack web application with mobile apps (backend Django API + frontend Vue SPA + Capacitor mobile)

**Performance Goals**:

- Office page load: < 3 seconds (SC-001)
- API response: < 500ms for office generation
- Bible Gateway API: < 2 seconds (with fallback to cache)
- Frontend rendering: < 1 second

**Constraints**:

- Must match printed BCP 2019 text exactly (FR-015)
- Internet required for uncached Bible passages (FR-020, FR-022)
- Client-side storage only for preferences (FR-023, FR-024)
- Dynamic liturgical calculation for any date (FR-012a)

**Scale/Scope**:

- 8 office types (4 traditional + 4 family prayer)
- 9 Bible translations supported
- ~365 days × 2 years of lectionary data pre-populated
- Unlimited date range via dynamic calculation
- 20+ liturgical settings per user
- 10+ Django apps, ~50 Python modules, ~40 Vue components

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### Principle I: Glory to God

- [x] Feature enhances prayer, scripture engagement, or accessibility
  - **Status**: ✅ COMPLIANT - Core purpose is daily prayer and scripture
- [x] Feature serves the spiritual purpose of the Daily Office
  - **Status**: ✅ COMPLIANT - Entire app dedicated to this purpose
- [x] Technical decisions prioritize user spiritual experience over elegance
  - **Status**: ⚠️ MOSTLY COMPLIANT - Some complexity exists (e.g., audio features, multiple canticle tables) but justified by liturgical requirements

**Overall**: ✅ COMPLIANT

### Principle II: Feature Branch Development

- [x] Feature branch created with format: `###-feature-name`
  - **Status**: ⚠️ RETROACTIVE - Feature predates constitution; branch `001-daily-office` created retroactively for documentation
- [x] Unique identifier assigned and documented
  - **Status**: ✅ COMPLIANT - Feature ID 001 assigned
- [x] No direct commits to main branch planned
  - **Status**: ⚠️ HISTORICAL ISSUE - Original development likely had direct main commits; future work will follow branch workflow

**Overall**: ⚠️ RETROACTIVE COMPLIANCE - Cannot change history, but documented for future reference

### Principle III: Comprehensive Testing (NON-NEGOTIABLE)

- [ ] Test plan includes 100% function coverage goal
  - **Status**: ❌ VIOLATION - No evidence of comprehensive test plan
- [ ] Unit tests planned for all new functions/methods
  - **Status**: ❌ VIOLATION - Test files exist (`site/office/tests.py`) but coverage unknown
- [ ] Integration tests planned for component interactions
  - **Status**: ❌ VIOLATION - No integration test evidence found
- [ ] End-to-end tests planned for critical user journeys
  - **Status**: ⚠️ PARTIAL - Cypress configured in `app/` but test status unknown
- [ ] Test-first approach confirmed (tests before implementation)
  - **Status**: ❌ VIOLATION - Feature already implemented without known test-first approach

**Overall**: ❌ **CRITICAL VIOLATION** - This is NON-NEGOTIABLE per constitution and requires immediate remediation

### Principle IV: Code Quality and Clarity

- [x] No "hacks" or workarounds planned
  - **Status**: ⚠️ NEEDS REVIEW - Code appears clean but requires audit for undocumented workarounds
- [x] Code formatting standards identified (Black/ESLint)
  - **Status**: ✅ COMPLIANT - Black configured (119 char lines), ESLint configured for frontend
- [x] Pre-commit hooks will be used
  - **Status**: ✅ COMPLIANT - `.pre-commit-config.yaml` present
- [x] Any complexity is justified and documented
  - **Status**: ⚠️ NEEDS REVIEW - Some complex logic in office generation requires documentation audit

**Overall**: ⚠️ MOSTLY COMPLIANT - Requires code clarity audit

### Principle V: Atomic and Traceable Commits

- [ ] Commit strategy ensures atomic, reviewable changes
  - **Status**: ⚠️ HISTORICAL - Cannot retroactively fix commit history
- [ ] Traceability plan: Code → Task ID → Requirement ID
  - **Status**: ❌ VIOLATION - No task IDs or requirement IDs in existing code
- [ ] Code comments will reference task/requirement IDs
  - **Status**: ❌ VIOLATION - No FR-### references found in code

**Overall**: ❌ VIOLATION - Requires retroactive traceability addition via code comments and documentation

### Principle VI: Unique and Persistent Identifiers

- [x] Requirements use FR-###, NFR-###, SC-### format
  - **Status**: ✅ COMPLIANT - Spec uses FR-001 through FR-028, SC-001 through SC-008
- [x] Tasks use T### format
  - **Status**: ⚠️ PENDING - No tasks.md created yet (Phase 2)
- [x] User Stories use US# format
  - **Status**: ✅ COMPLIANT - Spec uses US1 through US7
- [x] All IDs are unique and will not be reused
  - **Status**: ✅ COMPLIANT - No duplicate IDs found

**Overall**: ✅ COMPLIANT in specification; enforcement in code needed

### Constitution Summary

| Principle            | Status          | Priority | Action Required                            |
| -------------------- | --------------- | -------- | ------------------------------------------ |
| I. Glory to God      | ✅ Compliant    | -        | None                                       |
| II. Feature Branches | ⚠️ Retroactive  | P3       | Document historical context only           |
| III. Testing         | ❌ **CRITICAL** | P0       | **Create comprehensive test suite**        |
| IV. Code Quality     | ⚠️ Mostly       | P2       | Audit code clarity and document complexity |
| V. Traceability      | ❌ Violation    | P1       | Add FR-### comments to code                |
| VI. Identifiers      | ✅ Compliant    | -        | Enforce in future changes                  |

**GATE STATUS**: ⚠️ **CONDITIONAL PASS** - Proceed with audit while planning remediation for Principles III and V

## Project Structure

### Documentation (this feature)

```text
specs/001-daily-office/
├── spec.md              # Feature specification (COMPLETED)
├── plan.md              # This file - conformance audit plan (IN PROGRESS)
├── research.md          # Phase 0: Architecture documentation (PENDING)
├── data-model.md        # Phase 1: Existing data models documentation (PENDING)
├── quickstart.md        # Phase 1: Developer guide (PENDING)
├── contracts/           # Phase 1: API documentation (PENDING)
│   ├── openapi.yaml     # REST API specification
│   └── README.md        # API overview
└── tasks.md             # Phase 2: Remediation tasks (FUTURE - created by /speckit.tasks)
```

### Source Code (existing implementation)

```text
site/                           # Django backend
├── office/                     # Daily Office Django app
│   ├── models.py              # Data models: OfficeDay, StandardOfficeDay, HolyDayOfficeDay,
│   │                          #   ThirtyDayPsalterDay, Setting, SettingOption, Scripture
│   ├── offices.py             # Base Office class and OfficeSection base class
│   ├── morning_prayer.py      # MorningPrayer implementation (FR-001)
│   ├── evening_prayer.py      # EveningPrayer implementation (FR-002)
│   ├── midday_prayer.py       # MiddayPrayer implementation (FR-003)
│   ├── compline.py            # Compline implementation (FR-004)
│   ├── family_morning.py      # FamilyMorningPrayer (FR-018)
│   ├── family_midday.py       # FamilyMiddayPrayer (FR-018)
│   ├── family_early_evening.py # FamilyEarlyEveningPrayer (FR-018)
│   ├── family_close_of_day.py # FamilyCloseOfDay (FR-018)
│   ├── canticles.py           # Canticle management (FR-008)
│   ├── utils.py               # Utility functions
│   ├── views.py               # Django template views
│   ├── api/                   # REST API
│   │   ├── serializers.py     # DRF serializers
│   │   └── views/             # API viewsets and endpoints
│   ├── management/            # Django management commands
│   │   └── commands/          # Custom commands
│   └── templates/             # Django templates (legacy)
├── bible/                      # Bible passage retrieval (FR-016, FR-020-022)
│   ├── passage.py             # Passage class and BibleVersions
│   └── sources.py             # Bible Gateway adapter
├── churchcal/                  # Liturgical calendar (FR-007, FR-014)
│   ├── models.py              # Commemoration, Season, CalendarDate models
│   ├── calculations.py        # Easter calculation, season determination
│   └── management/            # Data import commands
├── psalter/                    # Psalm assignments and text (FR-005, FR-005a, FR-005b)
│   ├── models.py              # Psalm models
│   └── utils.py               # Psalm retrieval utilities
└── website/                    # Main site configuration
    ├── settings.py            # Django settings
    ├── urls.py                # URL routing
    └── .env                   # Environment variables

app/                            # Vue 3 frontend
├── src/
│   ├── views/
│   │   ├── Office.vue         # Main office display component
│   │   └── Today.vue          # Auto-select current office
│   ├── components/
│   │   ├── OfficeNav.vue      # Office navigation (FR-013)
│   │   ├── CalendarCard.vue   # Date display
│   │   ├── FontSizer.vue      # Accessibility feature
│   │   └── office/            # Office line type components
│   ├── router/                # Vue Router configuration
│   ├── store/                 # Pinia state management
│   └── helpers/
│       └── DynamicStorage.js  # Client-side preferences (FR-023, FR-024)
├── android/                    # Capacitor Android app
└── ios/                        # Capacitor iOS app
```

**Structure Decision**: This is a **full-stack web application with mobile apps** architecture. The Django backend serves both traditional template-based views and a REST API. The Vue 3 frontend is a Single Page Application (SPA) that consumes the API. Capacitor wraps the web app for iOS and Android. This structure supports both web browsers and native mobile apps from a single codebase.

## Complexity Tracking

> **Constitution Principle IV violations requiring justification**

| Complexity                                           | Why Needed                                                                               | Simpler Alternative Rejected                                            | Justification Status                                            |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------- |
| Multiple Canticle Tables (BCP1979, REC2011, Default) | Support different liturgical traditions and user preferences (FR-008, FR-026)            | Single canticle table would not support required liturgical flexibility | ✅ JUSTIFIED - Liturgical requirement                           |
| Dynamic Date Calculation (unlimited range)           | Users need access to any date past or future (FR-012, FR-012a)                           | Pre-populate database for fixed range (e.g., 100 years)                 | ✅ JUSTIFIED - Storage and maintenance burden of pre-population |
| Client-Side Preference Storage                       | No user authentication required; respects privacy (FR-023, FR-024)                       | Server-side storage with user accounts                                  | ✅ JUSTIFIED - Simplifies deployment and respects user privacy  |
| Bible Gateway API + Local Cache                      | Cannot redistribute copyrighted Bible texts; cache improves performance (FR-020, FR-021) | Local Bible database                                                    | ✅ JUSTIFIED - Copyright compliance                             |
| 8 Office Types                                       | BCP 2019 specifies all 8 (4 traditional + 4 family prayer) (FR-001-004, FR-018)          | Implement only 4 traditional offices                                    | ✅ JUSTIFIED - Spec requirement for full BCP 2019 support       |
| Module-Based Office Generation                       | Each office composed of 15-25 modules; enables customization and reuse                   | Monolithic template per office                                          | ✅ JUSTIFIED - Enables setting customization (FR-026)           |

**Complexity Verdict**: All identified complexity is **justified by liturgical requirements** or **practical constraints** (copyright, privacy, storage). No gratuitous complexity identified.

## Phase 0: Conformance Audit & Architecture Research

**Objective**: Document the existing implementation architecture, map code to requirements, and identify gaps between specification and reality.

### Research Tasks

1. **Architecture Inventory** (T001)

   - Document the modular office generation system (Office → OfficeSection → rendered output)
   - Map each Office class to specification requirements
   - Document the Django-Vue communication pattern (API vs. template-based)
   - Identify all data models and their relationships

2. **Requirement Mapping** (T002)

   - For each FR-### requirement, identify implementing code files and functions
   - Document which requirements are fully implemented, partially implemented, or missing
   - Create traceability matrix: Requirement ID → Code Files → Functions/Classes

3. **Gap Analysis** (T003)

   - Compare spec requirements with actual implementation
   - Identify features in code not mentioned in spec (audio player, settings system depth)
   - Identify spec requirements not fully implemented
   - Document discrepancies and propose resolution (update spec vs. update code)

4. **Test Coverage Analysis** (T004)

   - Inventory existing test files and test cases
   - Run test suite and capture coverage report
   - Identify untested code paths and critical user journeys lacking E2E tests
   - Estimate effort required for 100% function coverage

5. **Code Quality Audit** (T005)

   - Review code for "hacks," workarounds, or non-idiomatic patterns
   - Identify complex logic requiring additional documentation
   - Run Black and ESLint and document any formatting violations
   - Identify opportunities for simplification

6. **Traceability Assessment** (T006)
   - Search codebase for any existing task/requirement references
   - Identify key functions/classes that need FR-### comment annotations
   - Estimate effort required to add full traceability comments

**Deliverable**: `research.md` containing:

- Architecture diagram and description
- Full requirement mapping table (FR-### → files → functions)
- Gap analysis with recommendations
- Test coverage report and remediation plan
- Code quality findings
- Traceability roadmap

## Phase 1: Documentation & API Contracts

**Objective**: Create developer documentation for the existing implementation, formalize API contracts, and provide quickstart guide.

### Documentation Tasks

1. **Data Model Documentation** (T007)

   - Document all Django models in `office/models.py` with field descriptions
   - Document relationships between models (OfficeDay → Commemoration, etc.)
   - Document the calendar calculation system (churchcal.calculations)
   - Create entity-relationship diagram

2. **API Contract Extraction** (T008)

   - Document all REST API endpoints from `office/api/views/`
   - Create OpenAPI 3.0 specification for the API
   - Document request/response schemas from serializers
   - Document authentication (if any) and error responses

3. **Quickstart Guide** (T009)

   - Write developer setup instructions (database, environment, dependencies)
   - Document how to add a new office type
   - Document how to modify liturgical settings
   - Document testing procedures
   - Document common debugging scenarios

4. **Agent Context Update** (T010)
   - Run `.specify/scripts/bash/update-agent-context.sh copilot`
   - Add Daily Office architectural knowledge to agent context
   - Preserve existing manual context entries

**Deliverables**:

- `data-model.md` - Complete data model documentation with ER diagram
- `contracts/openapi.yaml` - REST API specification
- `contracts/README.md` - API usage guide with examples
- `quickstart.md` - Developer onboarding guide
- Updated `.github/copilot-instructions.md` (via script)

## Phase 2: Constitutional Compliance Remediation

**Note**: Phase 2 details will be specified in `tasks.md` (created by `/speckit.tasks` command). The following is a preview of remediation areas:

### Test Coverage Remediation (CRITICAL - P0)

- Create comprehensive unit test suite for all office generation logic
- Create integration tests for Bible Gateway API + caching
- Create E2E tests for all 8 office types with Cypress
- Achieve 100% function coverage per Principle III
- Estimated effort: 40-80 hours (depends on current coverage)

### Traceability Addition (HIGH - P1)

- Add FR-### code comments to all functions implementing requirements
- Add T### comments for future modifications
- Update docstrings with requirement references
- Estimated effort: 10-20 hours

### Code Quality Improvements (MEDIUM - P2)

- Document any identified complexity
- Add docstrings to complex functions
- Create Architecture Decision Records (ADRs) for major design choices
- Estimated effort: 20-30 hours

## Success Criteria

This conformance audit and remediation plan is successful when:

1. **Documentation Complete**: All Phase 0 and Phase 1 deliverables are created and reviewed
2. **Gap Analysis Resolved**: All discrepancies between spec and implementation are documented with resolution path
3. **Test Coverage Roadmap**: Clear plan exists to achieve 100% function coverage (Principle III)
4. **Traceability Established**: All code implementing FR-### requirements has traceable comments
5. **Constitution Compliance**: All violations identified with remediation tasks in `tasks.md`
6. **Developer Onboarding**: New developer can set up and understand the Daily Office codebase using `quickstart.md`

## Next Steps

1. ✅ **Plan Approval**: Review and approve this conformance audit plan
2. 🔄 **Execute Phase 0**: Run research tasks T001-T006, produce `research.md`
3. ⏳ **Execute Phase 1**: Run documentation tasks T007-T010, produce data-model.md, contracts/, quickstart.md
4. ⏳ **Generate tasks.md**: Run `/speckit.tasks` command to create detailed remediation task list
5. ⏳ **Execute Phase 2**: Implement test coverage, traceability, and code quality improvements
6. ⏳ **Verification**: Run full test suite, verify 100% coverage, validate traceability

## Timeline Estimate

| Phase                       | Duration  | Dependencies                          |
| --------------------------- | --------- | ------------------------------------- |
| Phase 0: Research           | 3-5 days  | Database access, codebase review      |
| Phase 1: Documentation      | 2-3 days  | Phase 0 complete                      |
| Phase 2: Testing (CRITICAL) | 2-3 weeks | Phase 1 complete, test infrastructure |
| Phase 2: Traceability       | 3-5 days  | Phase 0 complete                      |
| Phase 2: Code Quality       | 1-2 weeks | Phase 0 complete                      |

**Total Estimate**: 4-6 weeks for full constitutional compliance

## Notes

- This is a **retroactive specification and constitutional compliance** effort, not new feature development
- The existing implementation is **production-ready and functional**
- Primary risk is **test coverage gap** (Principle III violation - NON-NEGOTIABLE)
- Secondary risk is **code traceability** (Principle V violation)
- The spec accurately reflects the existing implementation with high fidelity
- Some features exist in code but not spec (audio player) - to be documented in Phase 0
