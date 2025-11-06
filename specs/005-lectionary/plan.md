# Implementation Plan: Lectionary

**Branch**: `005-lectionary` (to be created for future enhancements) | **Date**: 2025-11-06 | **Spec**: [spec.md](spec.md)  
**Input**: Feature specification from `/specs/005-lectionary/spec.md`

**RETROACTIVE DOCUMENTATION NOTICE**: This specification and plan were created after the lectionary functionality was implemented. This plan documents the existing implementation and identifies any gaps between the specification and current code.

## Summary

The Daily Office 2019 lectionary system provides scripture reading assignments and full text for Morning Prayer, Evening Prayer, and Holy Eucharist following the Book of Common Prayer 2019. The system supports:

- **Daily Office Lectionary**: Two-year cycle (Year 1/Year 2) with psalm assignments (60-day cycle default, optional 30-day) and scripture readings for Morning Prayer and Evening Prayer
- **Eucharist Lectionary**: Three-year cycle (Years A/B/C) following Revised Common Lectionary pattern with Old Testament, Psalm, Epistle, and Gospel readings
- **Multiple Bible Translations**: ESV, RSV, KJV, NRSV, NRSVCE, NABRE, NIV, NASB, plus Coverdale and Renewed Coverdale for Psalms
- **Scripture Text Retrieval**: Integration with Bible Gateway API, cached in database with service worker support for offline access
- **Feast Day Proper Readings**: Special readings for feasts and holy days that replace ordinary daily readings

**Technical Approach**: Django backend with PostgreSQL database storing reading assignments and cached scripture text. Vue.js frontend with translation selection and date navigation. API endpoints serve reading assignments and scripture text with translation-specific handling for deuterocanonical books.

## Technical Context

**Language/Version**: Python 3.13 (Django 5.2+), JavaScript/TypeScript (Vue 3, Node 24.4+)  
**Primary Dependencies**:

- Backend: Django 5.2, psycopg-binary (PostgreSQL), beautifulsoup4 (scripture parsing), requests (Bible Gateway API), Arrow (date handling), scriptures (citation parsing)
- Frontend: Vue 3, Vite, Element Plus UI, FontAwesome Pro icons
  **Storage**: PostgreSQL 17.5+ with models: `office.OfficeDay`, `office.StandardOfficeDay`, `office.HolyDayOfficeDay`, `office.LectionaryItem`, `office.Scripture`, `churchcal.MassReading`, `churchcal.Commemoration`, `churchcal.Proper`, `churchcal.Common`  
  **Testing**: pytest (backend), Vitest + Cypress (frontend) - **NEEDS COMPREHENSIVE TEST COVERAGE**  
  **Target Platform**: Web application (responsive), iOS/Android (Capacitor), Progressive Web App  
  **Project Type**: Web application (Django + Vue.js monorepo)  
  **Performance Goals**:
- Display today's readings in under 2 seconds (SC-001)
- Retrieve full scripture text in under 3 seconds (SC-002)
- Translation switching in under 2 seconds (SC-005)
  **Constraints**:
- Must support offline access to previously viewed scripture passages
- Must gracefully handle translations lacking deuterocanonical books (ESV, NIV, NASB → fallback to NRSVCE)
- Must accurately follow BCP 2019 lectionary cycles
  **Scale/Scope**:
- Daily Office: ~365 days × 2 years = 730 day records with psalm and scripture assignments
- Eucharist: ~3 years × ~200 lectionary items (Sundays, feasts, propers) = 600 lectionary entries
- Scripture cache: ~2000 unique passages × 9 translations = ~18,000 cached scripture texts

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### Principle I: Glory to God

- [x] Feature enhances prayer, scripture engagement, or accessibility - **PASS**: Provides immediate access to appointed scripture readings for daily prayer and worship
- [x] Feature serves the spiritual purpose of the Daily Office - **PASS**: Core functionality enabling scripture reading as part of Daily Office and Eucharist
- [x] Technical decisions prioritize user spiritual experience over elegance - **PASS**: Caching strategy prioritizes offline access; translation fallback ensures deuterocanonical readings always available

### Principle II: Feature Branch Development

- [x] Feature branch created with format: `005-lectionary` - **RETROACTIVE**: Functionality implemented on main branch historically; future enhancements should use feature branches
- [x] Unique identifier assigned and documented - **PASS**: 005-lectionary identifier established
- [x] No direct commits to main branch planned - **PASS**: Future work will use feature branches per constitution

### Principle III: Comprehensive Testing (NON-NEGOTIABLE)

- [⚠️] Test plan includes 100% function coverage goal - **NEEDS ATTENTION**: Existing tests incomplete; comprehensive test plan required for future enhancements
- [⚠️] Unit tests planned for all new functions/methods - **NEEDS ATTENTION**: Key models have minimal test coverage
- [⚠️] Integration tests planned for component interactions - **NEEDS ATTENTION**: Bible API integration, translation fallback, cycle determination need integration tests
- [⚠️] End-to-end tests planned for critical user journeys - **NEEDS ATTENTION**: E2E tests for viewing readings, changing translations, navigating dates needed
- [x] Test-first approach confirmed (tests before implementation) - **FUTURE**: Apply to future enhancements

**ACTION REQUIRED**: Before any lectionary enhancements, comprehensive test suite MUST be developed covering:

1. Lectionary cycle determination (Year 1/2 for Daily Office, A/B/C for Eucharist)
2. Reading assignment retrieval for standard days, feast days, and transferred feasts
3. Translation fallback for deuterocanonical books
4. Scripture text caching and retrieval
5. Psalm cycle selection (30-day vs 60-day)
6. Date navigation and proper reading display

### Principle IV: Code Quality and Clarity

- [x] No "hacks" or workarounds planned - **MOSTLY PASS**: Code is generally clean; some complexity in cycle determination and feast precedence is documented
- [x] Code formatting standards identified (Black/ESLint) - **PASS**: Black for Python (119-char line length), ESLint for JavaScript/TypeScript
- [x] Pre-commit hooks will be used - **PASS**: Pre-commit hooks configured
- [x] Any complexity is justified and documented - **PASS**: Liturgical calendar complexity documented in churchcal/calculations.py

### Principle V: Atomic and Traceable Commits

- [⚠️] Commit strategy ensures atomic, reviewable changes - **FUTURE**: Apply to future enhancements
- [⚠️] Traceability plan: Code → Task ID → Requirement ID - **NEEDS ATTENTION**: Retroactive traceability mapping required; see Complexity Tracking section
- [x] Code comments will reference task/requirement IDs - **FUTURE**: Apply to future work

### Principle VI: Unique and Persistent Identifiers

- [x] Requirements use FR-###, NFR-###, SC-### format - **PASS**: Spec uses FR-001 through FR-017, SC-001 through SC-009
- [x] Tasks use T### format - **FUTURE**: Will be applied in tasks.md
- [x] User Stories use US# format - **PASS**: Spec uses US1 through US6
- [x] All IDs are unique and will not be reused - **PASS**: IDs established in spec

## Project Structure

### Documentation (this feature)

```text
specs/005-lectionary/
├── plan.md              # This file - retroactive implementation plan
├── research.md          # Phase 0 output - documents existing implementation decisions
├── data-model.md        # Phase 1 output - comprehensive data model documentation
├── quickstart.md        # Phase 1 output - developer guide for lectionary functionality
├── contracts/           # Phase 1 output - API endpoint documentation
│   └── README.md        # API contracts for lectionary endpoints
├── checklists/
│   └── requirements.md  # Requirements validation checklist
└── spec.md              # Feature specification (retroactive)
```

### Source Code (repository root)

```text
site/                           # Django backend
├── office/                     # Daily Office application
│   ├── models.py              # OfficeDay, StandardOfficeDay, HolyDayOfficeDay, LectionaryItem, Scripture
│   ├── api/
│   │   └── views/
│   │       └── index.py       # API endpoints for readings and scripture
│   ├── management/commands/
│   │   ├── import_scripture.py      # Scripture text import/caching
│   │   └── import_lectionary.py     # Lectionary data import
│   └── tests/                 # Unit and integration tests (NEEDS EXPANSION)
│
├── churchcal/                  # Liturgical calendar application
│   ├── models.py              # Commemoration, MassReading, Proper, Common, Calendar
│   ├── calculations.py        # Church calendar date calculations
│   └── api/                   # Calendar API endpoints
│
└── bible/                      # Bible passage retrieval
    ├── passage.py             # Scripture parsing and formatting
    └── sources.py             # Bible Gateway API integration

app/                            # Vue.js frontend
├── src/
│   ├── views/
│   │   └── Readings.vue       # Main readings view with service/translation selection
│   ├── components/
│   │   └── Reading.vue        # Individual reading display component
│   ├── router/
│   │   └── index.js           # Routes for /readings/* paths
│   └── store/                 # Vuex store for state management
│
└── tests/
    ├── unit/                   # Component unit tests (NEEDS EXPANSION)
    └── e2e/                    # End-to-end tests (NEEDS EXPANSION)
```

**Structure Decision**: Existing monorepo structure with separate Django backend and Vue.js frontend is appropriate for the lectionary feature. Backend handles data storage, scripture retrieval, and cycle calculations. Frontend provides user interface for date navigation, translation selection, and reading display.

## Retroactive Specification Analysis

### ✅ Spec Accurately Reflects Implementation

The following aspects of the specification accurately describe the existing implementation:

1. **FR-001 through FR-004**: Daily Office and Eucharist reading assignments fully implemented via `OfficeDay`, `StandardOfficeDay`, `HolyDayOfficeDay`, and `LectionaryItem` models
2. **FR-005**: Scripture text retrieval via Bible Gateway API with database caching implemented in `bible/sources.py` and `office/management/commands/import_scripture.py`
3. **FR-006, FR-007**: Multiple Bible translations supported (ESV, RSV, KJV, NRSV, NRSVCE, NABRE, NIV, NASB) with translation selection in `Readings.vue`
4. **FR-008**: Feast day proper readings implemented via `HolyDayOfficeDay` and `LectionaryItem` with commemoration relationships
5. **FR-009**: Office type indication (Morning Prayer, Evening Prayer, Eucharist) clearly implemented in models and frontend
6. **FR-012**: Date navigation fully functional in frontend router and API endpoints
7. **FR-013, FR-015**: Two-year Daily Office cycle and three-year Eucharist cycle implemented in `churchcal/calculations.py`
8. **FR-014**: Apocrypha fallback implemented in `Reading.vue` (lines 102-128) with automatic NRSVCE fallback
9. **FR-016**: Clear citations provided via `passage_to_citation()` utility function

### ⚠️ Spec Elements Requiring Verification

The following aspects need verification or may have minor implementation differences:

1. **FR-002**: Spec mentions "60-day psalter cycle by default with optional 30-day cycle selection" - Implementation has `ThirtyDayPsalterDay` model but 30-day cycle selection mechanism needs documentation
2. **FR-010, FR-011**: Spec mentions handling scripture passages spanning multiple chapters and discontinued passages - Implementation exists in `bible/passage.py` but specific behavior needs documentation
3. **FR-017**: Alternative/optional readings mentioned in spec - Implementation in `LectionaryItem.passages_for_year_and_number()` uses " or " separator, needs verification against BCP 2019 requirements
4. **Success Criteria SC-001, SC-002, SC-005**: Performance targets (2-3 second response times) are specified but not validated with automated performance tests

### 🔍 Spec Elements Needing Clarification or Enhancement

1. **Service Worker Caching**: Spec mentions service worker caching (FR-005 clarification) but implementation status in app/ needs documentation
2. **User Translation Preference Persistence (FR-015)**: Spec requires translation preference to persist across sessions - implementation uses localStorage/Vuex but needs explicit documentation
3. **Date Range Support (SC-008)**: Spec requires "dates from at least 2 years past to 2 years future" - actual supported range determined by database content needs documentation
4. **US6 - Access Lectionary by Season**: Spec includes P3 priority user story for browsing by liturgical season - this functionality may not be fully implemented and needs verification

### 📋 Testing Gap Analysis

The specification's Success Criteria and User Stories define clear acceptance criteria, but comprehensive automated tests are lacking:

**Missing Test Coverage**:

- Lectionary cycle determination for edge cases (transferred feasts, Advent Sunday year boundaries)
- Scripture text retrieval and caching for all supported translations
- Translation fallback behavior for deuterocanonical books
- Date navigation across year boundaries
- Proper reading assignment for all feast ranks and precedence rules
- Performance benchmarks for SC-001, SC-002, SC-005

**Action Required**: Before implementing any enhancements, develop comprehensive test suite mapping to User Stories US1-US6 and Success Criteria SC-001 through SC-009.

## Complexity Tracking

### Retroactive Code Traceability

Since the lectionary functionality was implemented before comprehensive traceability requirements (Constitution Principle V), the following mapping provides retroactive traceability:

| Code Component             | Implements Requirements | Location                                               |
| -------------------------- | ----------------------- | ------------------------------------------------------ |
| `OfficeDay` model          | FR-001, FR-002, FR-003  | `site/office/models.py:14-71`                          |
| `StandardOfficeDay` model  | FR-001, FR-012          | `site/office/models.py:72-76`                          |
| `HolyDayOfficeDay` model   | FR-008                  | `site/office/models.py:77-81`                          |
| `LectionaryItem` model     | FR-004, FR-008, FR-017  | `site/office/models.py:405-576`                        |
| `MassReading` model        | FR-004, FR-013          | `site/churchcal/models.py:421-454`                     |
| `Scripture` model          | FR-005, FR-006, FR-016  | `site/office/models.py` (not shown in excerpt)         |
| Bible Gateway integration  | FR-005                  | `site/bible/sources.py`                                |
| Scripture import command   | FR-005                  | `site/office/management/commands/import_scripture.py`  |
| Lectionary import command  | FR-001, FR-004          | `site/office/management/commands/import_lectionary.py` |
| Translation fallback logic | FR-014                  | `app/src/components/Reading.vue:102-128`               |
| Readings view              | US1, US2, US3, US4      | `app/src/views/Readings.vue`                           |
| Reading component          | US2, FR-016             | `app/src/components/Reading.vue`                       |
| Cycle calculations         | FR-013, FR-015          | `site/churchcal/calculations.py`                       |
| Psalm cycle models         | FR-002                  | `site/office/models.py:83-95`                          |

### Justified Complexity

| Complexity                                                 | Why Needed                                                                                                                                        | Simpler Alternative Rejected Because                                                                                                                                          |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Two separate lectionary systems (Daily Office + Eucharist) | BCP 2019 defines distinct two-year Daily Office cycle and three-year Eucharist cycle with different structures                                    | Single unified lectionary cannot represent both cycles accurately; cycles have different year boundaries (Advent) and reading patterns                                        |
| Scripture caching in database across 9 translations        | Offline access requirement (FR-005) and performance goals (SC-001, SC-002) require cached text                                                    | Always fetching from external API violates offline requirement and fails performance targets; service worker alone insufficient for initial load                              |
| Inheritance hierarchy for Commemoration types              | Church calendar has complex feast precedence rules and different commemoration types (sanctorale, proper, common) with different reading patterns | Flat model would require complex conditional logic throughout codebase; inheritance enables polymorphism for feast-specific behavior                                          |
| Cached properties on LectionaryItem for Years A/B/C        | Three-year Eucharist cycle requires year-specific reading assignments; caching optimizes repeated access                                          | Database queries for each year access would violate SC-001 performance target; computational cost of cycle determination requires caching                                     |
| Translation fallback for deuterocanonical books            | ESV, NIV, NASB do not include Apocrypha, but BCP 2019 lectionary appoints these readings (FR-014)                                                 | Removing apocryphal readings would violate BCP 2019 compliance; showing error messages would degrade user experience; NRSVCE fallback maintains both compliance and usability |

## Next Steps for Future Enhancements

Since this is retroactive documentation, future work on the lectionary should follow this process:

1. **Comprehensive Testing (PRIORITY 1)**: Develop full test suite covering all FR requirements and SC success criteria before making any changes
2. **Performance Validation (PRIORITY 2)**: Implement automated performance tests validating SC-001, SC-002, SC-005 targets
3. **Documentation Completion (PRIORITY 3)**: Complete research.md, data-model.md, contracts/README.md, and quickstart.md to provide full developer context
4. **Verification of Spec Accuracy (PRIORITY 4)**: Validate unclear spec elements (30-day psalm cycle selection, seasonal browsing US6, date range limits)
5. **Constitution Compliance (ONGOING)**: Ensure all future enhancements follow Constitution Principles I-VI, especially comprehensive testing (Principle III)

Any future enhancements must:

- Create feature branch: `005-lectionary-[enhancement-name]`
- Reference specific FR/SC requirements
- Include comprehensive tests before implementation
- Maintain backward compatibility with existing liturgical calendar data
- Document any changes to lectionary cycle logic or feast precedence rules

## Implementation Status Summary

**Overall Assessment**: The lectionary functionality is **substantially implemented** and operational. The retroactive specification accurately describes most of the existing implementation, with minor clarifications needed for psalm cycle selection, seasonal browsing, and service worker caching.

**Constitution Compliance**:

- ✅ Principles I, II, IV, VI: Generally compliant
- ⚠️ Principle III (Testing): **REQUIRES ATTENTION** - comprehensive test coverage needed
- ⚠️ Principle V (Traceability): **RETROACTIVE MAPPING** provided in Complexity Tracking section

**Recommendation**: Accept specification as accurate documentation of existing functionality. Prioritize comprehensive test development before implementing any enhancements. Use this plan as foundation for tasks.md generation in Phase 2.
