# Implementation Plan: Cross-Platform Access and Settings

**Branch**: `006-general-design` | **Date**: 2025-11-06 | **Spec**: [specs/006-general-design/spec.md](./spec.md)  
**Input**: Feature specification from `/specs/006-general-design/spec.md`

**Status**: ✅ PHASE 1 COMPLETE - Design & Contracts finished, ready for Phase 2 (Testing Infrastructure)

**Last Updated**: 2025-11-07

## Summary

This is a **conformance plan** for the Daily Office 2019 cross-platform architecture. The specification has been revised to accurately reflect the current implementation while documenting a clear roadmap for future enhancements.

The application currently supports:

- Web access via Vue 3 SPA with responsive design
- Native iOS and Android apps via Capacitor
- Extensive settings customization stored in browser/device storage
- Settings sharing via URL parameters
- Basic responsive design with mobile-first approach

**Specification Revision Completed**: The specification now distinguishes between currently implemented features (marked as "MUST") and future enhancements (marked as "SHOULD" or "MAY"). This provides a clear foundation for phased implementation.

**Current Implementation**:

- ✅ Web and mobile apps fully functional
- ✅ Capacitor integration for iOS/Android with Firebase Analytics
- ✅ Settings storage via DynamicStorage (wraps Capacitor Preferences for mobile, localStorage for web)
- ✅ Settings sharing via URL parameters (compact encoding scheme)
- ✅ Responsive design with Tailwind CSS and Element Plus
- ✅ Deep linking support for mobile apps
- ✅ Settings QR code generation for easy sharing

## Technical Context

**Language/Version**:

- Frontend: JavaScript (ES2015+), Vue 3 Composition API
- Backend: Python 3.13, Django 5.2+

**Primary Dependencies**:

- Vue 3 + Vue Router + Vuex
- Vite 6.x (build tool)
- Capacitor 7.4.3 (mobile wrapper)
- Element Plus (UI framework)
- Tailwind CSS 3.x (styling)
- Firebase Analytics (mobile apps)
- Django REST Framework (API)

**Storage**:

- PostgreSQL 17.5+ (backend database)
- Capacitor Preferences API (mobile settings persistence)
- localStorage (web settings persistence)
- Memcached 1.6+ (backend caching)

**Testing**:

- Frontend: Vitest (unit tests), Cypress (e2e tests)
- Backend: pytest, Django test framework
- Current Status: Minimal test coverage exists

**Target Platform**:

- Web: Modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions specified but not enforced)
- Mobile: iOS 14+ and Android via Capacitor
- Deployment: Cloudflare CDN (static frontend), Django API server

**Project Type**: Web + Mobile application (multi-platform)

**Performance Goals**:

- Target: Time to First Contentful Paint (FCP) < 3 seconds on standard connections
- Current: No monitoring in place to verify

**Constraints**:

- No user accounts required - settings stored locally
- Must work offline after initial content load (mobile apps have this, web does not)
- Cross-platform settings compatibility (URL-based sharing must work across web/iOS/Android)

**Scale/Scope**:

- User base: Unknown current scale
- Codebase: ~50k LOC across frontend/backend
- Features: 40+ customizable settings across Daily Office and Family Prayer
- Screens: ~15 main views/routes

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### Principle I: Glory to God

- [x] Feature enhances prayer, scripture engagement, or accessibility
  - **Current**: Application serves daily prayer across multiple platforms
  - **Gap**: Accessibility features are minimal (violates spirit of principle)
- [x] Feature serves the spiritual purpose of the Daily Office
  - **Current**: Core functionality well-implemented
- [⚠️] Technical decisions prioritize user spiritual experience over elegance
  - **Gap**: Missing offline web support and performance monitoring suggests technical priorities may not fully align

**Verdict**: MOSTLY COMPLIANT with gaps in accessibility and offline reliability

### Principle II: Feature Branch Development

- [x] Feature branch created with format: `006-general-design`
- [x] Unique identifier assigned and documented
- [x] No direct commits to main branch planned

**Verdict**: COMPLIANT (for future work; this is retroactive documentation)

### Principle III: Comprehensive Testing (NON-NEGOTIABLE)

- [❌] Test plan includes 100% function coverage goal
  - **Gap**: Minimal test coverage exists in codebase
- [❌] Unit tests planned for all new functions/methods
  - **Gap**: Only example test files found
- [❌] Integration tests planned for component interactions
  - **Gap**: No integration tests detected
- [❌] End-to-end tests planned for critical user journeys
  - **Gap**: Cypress configured but no substantial tests found
- [❌] Test-first approach confirmed (tests before implementation)
  - **Gap**: Feature already implemented without tests

**Verdict**: CRITICAL VIOLATION - Testing requirements not met

### Principle IV: Code Quality and Clarity

- [x] No "hacks" or workarounds detected
- [x] Code formatting standards identified (Black for Python, ESLint for JS/TS)
- [⚠️] Pre-commit hooks configured but enforcement unclear
- [x] Code is generally clean and maintainable

**Verdict**: MOSTLY COMPLIANT

### Principle V: Atomic and Traceable Commits

- [⚠️] Commit strategy ensures atomic, reviewable changes
  - **Note**: Historical commits exist; future work will follow this principle
- [⚠️] Traceability plan: Code → Task ID → Requirement ID
  - **Gap**: Retroactive specification creates traceability challenge
- [⚠️] Code comments reference task/requirement IDs
  - **Gap**: Existing code lacks requirement traceability

**Verdict**: NOT APPLICABLE (retroactive) - MUST BE APPLIED GOING FORWARD

### Principle VI: Unique and Persistent Identifiers

- [x] Requirements use FR-###, NFR-###, SC-### format
- [x] User Stories use US# format
- [x] All IDs are unique and will not be reused

**Verdict**: COMPLIANT (in specification)

### Overall Constitution Compliance

**Status**: ⚠️ PARTIAL COMPLIANCE

**Critical Gaps**:

1. **Testing** (Principle III): Comprehensive testing missing - BLOCKS future changes
2. **Traceability** (Principle V): Existing code lacks requirement linkage
3. **Accessibility** (Principle I): Minimal implementation affects spiritual mission

**Recommendation**: Before implementing new features from spec, must:

1. Achieve test coverage for existing functionality
2. Add requirement traceability comments to key code sections
3. Audit and enhance accessibility features

## Project Structure

### Documentation (this feature)

```text
specs/006-general-design/
├── spec.md              # Feature specification (COMPLETED)
├── plan.md              # This file (IN PROGRESS)
├── research.md          # Phase 0 output (REQUIRED NEXT)
├── data-model.md        # Phase 1 output (REQUIRED)
├── quickstart.md        # Phase 1 output (REQUIRED)
├── contracts/           # Phase 1 output (API contracts)
└── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
```

### Source Code (repository root)

The project uses a **Web + Mobile application** structure:

```text
app/                           # Vue 3 Frontend Application
├── src/
│   ├── main.js               # App entry point with router/store initialization
│   ├── App.vue               # Root component with top navigation
│   ├── router/
│   │   └── index.js          # Vue Router configuration (15+ routes)
│   ├── store/
│   │   └── index.js          # Vuex store (settings management)
│   ├── components/
│   │   ├── Settings*.vue     # Settings-related components
│   │   ├── ShareSettings.vue # Settings sharing with QR codes
│   │   ├── ThemeSwitcher.vue # Dark/light mode
│   │   ├── FontSizer.vue     # Font size adjustment
│   │   └── Loading.vue       # Loading states
│   ├── views/
│   │   ├── Settings.vue      # Settings page with tabs
│   │   ├── Today.vue         # Home page
│   │   ├── About.vue         # About page
│   │   └── [others]          # Office views, calendar, etc.
│   ├── helpers/
│   │   ├── storage.js        # DynamicStorage abstraction
│   │   ├── createSettingsString.js
│   │   ├── decodeSettingsString.js
│   │   └── getMessageOffest.js
│   └── plugins/              # Vue plugins configuration
├── public/
│   ├── robots.txt
│   ├── site.webmanifest      # PWA manifest (partial)
│   └── assets/               # Static assets
├── ios/                      # iOS Capacitor project
│   └── App/
│       ├── App/
│       │   ├── AppDelegate.swift    # Firebase initialization
│       │   └── GoogleService-Info.plist
│       └── CapApp-SPM/       # Swift Package Manager dependencies
│           └── Package.swift # Capacitor plugins
├── android/                  # Android Capacitor project
│   └── app/
│       └── google-services.json
├── tests/
│   ├── unit/
│   │   └── example.spec.js   # Minimal unit test example
│   └── e2e/                  # Cypress e2e tests directory
├── capacitor.config.ts       # Capacitor configuration
├── vite.config.mjs          # Vite build configuration
├── vitest.config.ts         # Vitest test configuration
├── cypress.config.mjs       # Cypress e2e configuration
├── tailwind.config.mjs      # Tailwind CSS configuration
├── package.json             # Node.js dependencies
└── README.md                # Frontend documentation

site/                         # Django Backend Application
├── website/
│   ├── settings.py          # Django settings (Webpack, caching, etc.)
│   └── urls.py              # URL routing
├── office/
│   ├── models.py            # Office data models
│   ├── views.py             # Office views (API endpoints)
│   ├── api/                 # REST API endpoints
│   ├── templates/           # Django templates
│   └── src/
│       └── office/
│           ├── js/
│           │   ├── settings.js      # Settings management (legacy)
│           │   ├── app.js           # Capacitor App/Analytics setup
│           │   ├── redirect.js      # Office navigation logic
│           │   └── index.js         # Entry point
│           └── css/
│               └── index.scss
├── churchcal/               # Church calendar calculations
├── bible/                   # Bible passage retrieval
├── psalter/                 # Psalm handling
├── manage.py                # Django management
├── requirements.txt         # Python dependencies
├── package.json             # Node.js dependencies (build tools)
├── webpack.config.js        # Webpack configuration
└── Makefile                 # Build automation

specs/                       # Feature specifications
├── README.md
└── 006-general-design/      # This feature
    └── spec.md
```

**Structure Decision**: The application uses a clear separation between frontend (Vue 3 SPA in `/app`) and backend (Django API in `/site`). The frontend is wrapped in Capacitor for mobile deployment. This structure is appropriate for the cross-platform requirements but needs enhancement for:

1. Service worker implementation (web PWA functionality)
2. Comprehensive test suite structure
3. Performance monitoring infrastructure
4. Accessibility testing framework

**Future Enhancements** (documented in spec as SHOULD/MAY):

- Service Worker/PWA for offline web support (Phase 4)
- Settings History with rollback capability (Phase 3)
- Settings Confirmation Prompts (Phase 3)
- Performance Monitoring (FCP tracking) (Phase 5)
- Enhanced Accessibility (WCAG 2.1 AA) (Phase 2)
- Browser Detection & Graceful Degradation (Phase 6)

## Implementation Phases

The plan follows a 6-phase approach over 16-20 weeks (thorough timeline as decided):

### Phase 0: Research & Planning (CURRENT - Week 1-2)

### Phase 1: Testing Infrastructure (PRIORITY - Week 3-6)

### Phase 2: Accessibility Enhancements (Week 7-9)

### Phase 3: Settings Confirmation & History (Week 10-12)

### Phase 4: Progressive Web App (Week 13-15)

### Phase 5: Performance Monitoring (Week 16-17)

### Phase 6: Browser Detection (Week 18)

## Enhancement Details: Future Features

### Major Enhancements to Implement

#### 1. Service Worker & PWA Support (FR-012a)

**Priority**: HIGH - Required for offline web support

**Current State**: No service worker detected. Web application relies on browser caching only.

**Required Implementation**:

- Service worker registration in `main.js`
- Cache strategies for static assets
- Runtime caching for API responses
- Offline fallback pages
- Service worker lifecycle management
- Cache versioning and invalidation

**Impact**: Large - New infrastructure component

#### 2. Settings History System (FR-009a, FR-009b, FR-009c)

**Priority**: MEDIUM - Enhances user experience but not blocking

**Current State**: Settings are stored and can be overwritten, but no history tracking exists.

**Required Implementation**:

- Settings history data structure (timestamped snapshots)
- History storage mechanism (extend DynamicStorage)
- History UI in Settings view
- Restore functionality
- Automatic pruning (keep last 10 entries)

**Impact**: Medium - New feature requiring data model and UI

#### 3. Settings Confirmation Prompt (FR-009)

**Priority**: MEDIUM - Safety feature for settings sharing

**Current State**: Shared settings are applied immediately with only a success notification.

**Required Implementation**:

- Intercept settings application in store
- Show diff/preview of changes before applying
- Confirmation dialog component
- Auto-save previous settings to history before applying new ones
- User choice: Accept/Reject

**Impact**: Medium - Requires store refactoring and new UI component

#### 4. Performance Monitoring (FR-015a, FR-015b)

**Priority**: MEDIUM - Needed to verify performance goals

**Current State**: No client-side performance tracking.

**Required Implementation**:

- Browser Performance API integration
- FCP measurement capture
- Optional: Report to analytics or backend
- Dashboard/monitoring view (optional)

**Impact**: Small - Primarily telemetry code

#### 5. Browser Detection & Graceful Degradation (FR-005a, FR-005b)

**Priority**: LOW - Nice to have but not critical

**Current State**: Application loads in all browsers without version checking.

**Required Implementation**:

- Browser version detection utility
- Supported browser version configuration
- Warning banner component for unsupported browsers
- Graceful degradation message with upgrade suggestions

**Impact**: Small - Detection logic and banner component

#### 6. Comprehensive Accessibility (FR-013, FR-013a)

**Priority**: HIGH - Mission-critical per Principle I

**Current State**: Basic semantic HTML exists, but accessibility audit needed.

**Required Implementation**:

- ARIA labels for interactive elements
- Skip links for navigation
- Focus indicators and keyboard navigation audit
- Screen reader testing
- High contrast mode support
- Accessibility testing in CI/CD

**Impact**: Medium-Large - Requires comprehensive audit and incremental fixes

### Minor Gaps & Enhancements

#### 7. Deep Linking Documentation (FR-017)

**Current State**: Deep linking exists for mobile apps (see `site/office/src/office/js/app.js`)
**Required**: Document existing implementation, ensure web URLs work consistently

#### 8. Test Coverage (Principle III - CRITICAL)

**Current State**: Minimal tests exist
**Required**:

- Unit tests for all utility functions
- Component tests for Vue components
- Integration tests for store/router
- E2E tests for critical user journeys
- Backend API tests

**Impact**: LARGE - Comprehensive testing effort

## Complexity Tracking

| Violation                                                       | Why Needed                                                                                   | Simpler Alternative Rejected Because                                                                                          |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Service Worker Complexity**                                   | Offline web support requires background script with complex lifecycle and caching strategies | Native browser caching insufficient; users need offline access similar to mobile apps per FR-012a                             |
| **Settings History Data Model**                                 | Timestamped history with restore capability requires structured storage and UI               | Simple overwrite insufficient; users need safety net when accepting shared settings per FR-009a-c                             |
| **Dual Storage Systems** (localStorage + Capacitor Preferences) | Must support both web and mobile platforms with unified API                                  | Single storage layer impossible; platforms have different APIs requiring abstraction (DynamicStorage exists and handles this) |
| **Testing Debt**                                                | Retroactive specification creates gap between existing code and testing requirements         | Cannot simplify; comprehensive testing is NON-NEGOTIABLE per Principle III                                                    |

## Implementation Progress

**Current Phase**: Phase 0 ✅ COMPLETE  
**Next Phase**: Phase 1 (Design & Contracts)  
**Overall Timeline**: Week 1-2 of 18 (Thorough implementation track)

### Phase 0: Research & Planning ✅ COMPLETE

**Timeline**: Week 1-2 (COMPLETED 2025-11-07)  
**Goal**: Understand gaps, research solutions, create detailed technical designs

**Activities** (COMPLETED):

1. ✅ Generated `research.md` covering:
   - Service worker best practices for Vue 3 + Vite (vite-plugin-pwa + Workbox)
   - Settings history data model design patterns (timestamped snapshots)
   - Performance monitoring approaches (web-vitals + Performance API)
   - WCAG 2.1 AA compliance audit checklist (axe-core)
   - Browser detection libraries and approaches (feature detection)
2. ✅ Audited existing architecture and technology stack
3. ✅ Identified testing framework capabilities (Vitest, Cypress, Vue Test Utils)
4. ✅ Documented implementation strategies for all enhancement phases

**Deliverables**:

- ✅ `research.md` (comprehensive 600+ line research document)
- ✅ Technology decisions documented and justified
- ✅ Implementation patterns identified for all phases
- ✅ Dependency list compiled
- ✅ Alternatives considered and documented

**Key Decisions Made**:

- **Testing**: Vitest + Vue Test Utils + Cypress + axe-core for accessibility
- **PWA**: vite-plugin-pwa + Workbox for service worker management
- **Performance**: web-vitals library + Performance API for metrics tracking
- **Browser Detection**: Feature detection primary, minimal UA parsing fallback
- **Settings History**: Extend DynamicStorage abstraction with timestamped snapshots
- **Focus Management**: focus-trap-vue library for modal/drawer focus trapping
- **Accessibility**: axe-core automated testing + manual screen reader testing

**Status**: ✅ COMPLETE - Phase 0 deliverables finished

### Phase 1: Design & Contracts (1 week) ✅ COMPLETE

**Goal**: Design new features and document API contracts

**Activities**:

1. ✅ Create `data-model.md`:
   - Settings History Entry schema
   - Service Worker cache structure
   - Performance metrics data model
   - PWA manifest schema
   - Browser feature detection
2. ✅ Design API contracts in `contracts/`:
   - Performance metrics reporting API (optional, Phase 6)
   - Privacy-first design with user opt-in
3. ✅ Create `quickstart.md` for new developers:
   - Setup instructions (~30 minutes)
   - Architecture overview
   - Testing guide
   - Development workflow
   - Troubleshooting
4. ✅ Update agent context (copilot-instructions.md):
   - Added Phase 0 technology decisions
   - Documented testing patterns and organization
   - Added links to specification documents

**Deliverables**:

- ✅ `data-model.md` (complete with 13 sections, TypeScript schemas)
- ✅ `contracts/performance-api.md` (optional backend API contract)
- ✅ `quickstart.md` (comprehensive developer onboarding)
- ✅ Updated `.github/copilot-instructions.md` with Phase 0 findings

**Status**: ✅ COMPLETE - Ready to proceed to Phase 2 (Testing Infrastructure)

### Phase 2: Test Infrastructure (2-3 weeks)

**Goal**: Establish comprehensive testing before implementing new features

**Activities**:

1. Set up test coverage reporting (Istanbul/nyc)
2. Write unit tests for existing utilities:
   - `storage.js` (DynamicStorage)
   - `createSettingsString.js` / `decodeSettingsString.js`
   - Settings store mutations/actions
3. Write component tests for key components:
   - Settings.vue
   - ShareSettings.vue
   - SettingsPanel.vue
4. Write E2E tests for critical flows:
   - Settings persistence
   - Settings sharing
   - Cross-platform consistency

**Deliverables**: Test suite with >80% coverage of existing code

### Phase 3: Accessibility Enhancements (2 weeks)

**Goal**: Meet basic WCAG 2.1 AA requirements

**Activities**:

1. Add ARIA labels to all interactive elements
2. Implement skip links
3. Enhance keyboard navigation
4. Add focus indicators
5. Test with screen readers
6. Add accessibility tests to CI/CD

**Deliverables**: WCAG 2.1 AA compliant application (MVP level)

### Phase 4: New Feature Implementation (4-6 weeks)

**Goal**: Implement missing features from specification

**Priority Order**:

1. **Service Worker & PWA** (2 weeks)
   - Highest value for users (offline web access)
   - Complex but well-documented pattern
2. **Settings Confirmation & History** (1-2 weeks)
   - Improves user safety and experience
   - Moderate complexity
3. **Performance Monitoring** (1 week)
   - Enables validation of performance goals
   - Low complexity
4. **Browser Detection** (2-3 days)
   - Low priority, quick win
   - Minimal complexity

**Deliverables**: Fully conforming implementation per specification

### Phase 5: Documentation & Training (1 week)

**Goal**: Document new features and update onboarding materials

**Activities**:

1. Update user-facing documentation
2. Create developer guides for new systems
3. Update README files
4. Record demo videos for new features

**Deliverables**: Complete documentation suite

## Success Metrics

To validate the implementation plan achieves specification goals:

| Success Criterion                        | Current State                  | Target State                       | Measurement Method       |
| ---------------------------------------- | ------------------------------ | ---------------------------------- | ------------------------ |
| **SC-001**: Browser compatibility        | ✅ Works but unverified        | ✅ Verified + graceful degradation | Automated browser tests  |
| **SC-002**: Mobile touch interactions    | ✅ Implemented                 | ✅ Verified                        | E2E tests on iOS/Android |
| **SC-003**: Responsive layout            | ✅ Implemented                 | ✅ Verified                        | Visual regression tests  |
| **SC-004**: Settings persistence         | ✅ 100% reliable               | ✅ Verified                        | Unit + integration tests |
| **SC-005**: Settings sharing with prompt | ⚠️ Partial (no prompt/history) | ✅ With confirmation + history     | E2E test + manual QA     |
| **SC-006**: FCP < 3 seconds              | ❓ Unknown                     | ✅ 95th percentile < 3s            | Performance monitoring   |
| **SC-007**: Offline access               | ⚠️ Mobile only                 | ✅ Web + mobile                    | Service worker tests     |
| **SC-008**: Accessibility                | ⚠️ Basic                       | ✅ WCAG 2.1 AA MVP                 | axe-core automated tests |
| **SC-009**: Settings usability           | ✅ Likely met                  | ✅ Verified                        | User testing             |
| **SC-010**: Font size adjustments        | ✅ Implemented                 | ✅ Verified                        | Visual regression tests  |
| **SC-011**: Cross-platform sharing       | ✅ Implemented                 | ✅ Verified                        | Integration tests        |
| **Test Coverage**                        | ❌ Minimal                     | ✅ >90% function coverage          | Istanbul/nyc reports     |

## Critical Decision Points

Before proceeding with implementation, project owner must decide:

### Decision 1: Specification Conformance Level

**Question**: Should we implement ALL features in the specification or prioritize a subset?

**Options**:
A. **Full Conformance**: Implement all FR requirements including service worker, settings history, performance monitoring, etc.
B. **Pragmatic Subset**: Focus on testing and accessibility gaps; defer service worker and monitoring
C. **Revision Path**: Update specification to match current implementation more closely

**Recommendation**: Option A (Full Conformance) over ~3 months, starting with testing infrastructure

### Decision 2: Testing Strategy

**Question**: Test retroactively or test-first for new features?

**Options**:
A. **Test Existing First**: Achieve high coverage of current code before adding new features
B. **Test-First for New**: Skip retroactive testing, use TDD only for new features
C. **Hybrid**: Basic retroactive tests for critical paths, TDD for all new code

**Recommendation**: Option A (Test Existing First) - aligns with Principle III

### Decision 3: Breaking Changes

**Question**: Can we make breaking changes to improve architecture?

**Examples**:

- Refactor settings store to support confirmation prompts
- Change settings URL parameter format for history support
- Modify DynamicStorage API for history tracking

**Recommendation**: Minimize breaking changes; use feature flags for new behavior; maintain backward compatibility for URL-based settings sharing

### Decision 4: Timeline vs. Quality Trade-off

**Question**: What is the acceptable timeline for full conformance?

**Options**:
A. **Rapid (6-8 weeks)**: Cut scope, focus on critical gaps only
B. **Balanced (10-14 weeks)**: Phase 0-5 as outlined above
C. **Thorough (16-20 weeks)**: Include comprehensive WCAG 2.1 AA compliance and extensive testing

**Recommendation**: Option B (Balanced) - provides time for quality without excessive delay

## Next Steps

1. **Project Owner Review**: Review this plan and make decisions on critical decision points above
2. **Specification Alignment**: Discuss gaps between spec and implementation - revise spec or proceed with full implementation?
3. **Phase 0 Kickoff**: If proceeding, begin research phase:
   ```bash
   # Generate research documentation
   cd /workspaces/dailyoffice2019
   # Create research.md following Phase 0 guidelines
   ```
4. **Test Infrastructure Setup**: Before any new development, establish testing framework
5. **Constitution Compliance**: Address testing and traceability gaps to meet Principle III and V

## Open Questions for Project Owner

1. **Scope Clarity**: Is this specification intended to be aspirational (future roadmap) or prescriptive (must implement now)?
2. **User Impact**: Which gaps cause the most user friction currently? (Prioritization input)
3. **Resource Availability**: What is the development capacity for this work? (Affects timeline)
4. **Backward Compatibility**: How important is maintaining existing URL-based settings sharing format?
5. **Service Worker Strategy**: Is offline web access a real user need or nice-to-have?
6. **Accessibility Priority**: Is WCAG 2.1 AA compliance required for any specific reason (legal, organizational policy)?
7. **Testing ROI**: What is the risk tolerance for untested code? Should we stop new features until testing is in place?

## Appendix: Key Files for Gap Implementation

### Service Worker Implementation

**New Files Needed**:

- `app/public/sw.js` - Service worker script
- `app/src/registerServiceWorker.js` - Registration logic
- `app/public/offline.html` - Offline fallback page

**Modified Files**:

- `app/src/main.js` - Add service worker registration
- `app/vite.config.mjs` - Configure service worker in build
- `app/public/site.webmanifest` - Complete PWA manifest

### Settings History Implementation

**New Files Needed**:

- `app/src/helpers/settingsHistory.js` - History management utility
- `app/src/components/SettingsHistory.vue` - History UI component
- `app/src/components/SettingsConfirmation.vue` - Confirmation dialog

**Modified Files**:

- `app/src/store/index.js` - Add history mutations/actions
- `app/src/views/Settings.vue` - Integrate history UI
- `app/src/helpers/storage.js` - Extend for history storage

### Performance Monitoring Implementation

**New Files Needed**:

- `app/src/helpers/performanceMonitoring.js` - FCP tracking utility

**Modified Files**:

- `app/src/main.js` - Initialize performance monitoring
- `app/src/App.vue` - Optional: Display performance metrics

### Browser Detection Implementation

**New Files Needed**:

- `app/src/helpers/browserDetection.js` - Detection utility
- `app/src/components/UnsupportedBrowserBanner.vue` - Warning banner

**Modified Files**:

- `app/src/App.vue` - Add browser warning banner

### Testing Infrastructure

**New Files Needed**:

- `app/tests/unit/helpers/storage.spec.js`
- `app/tests/unit/helpers/createSettingsString.spec.js`
- `app/tests/unit/helpers/decodeSettingsString.spec.js`
- `app/tests/unit/store/index.spec.js`
- `app/tests/unit/components/ShareSettings.spec.js`
- `app/tests/e2e/settings-persistence.cy.js`
- `app/tests/e2e/settings-sharing.cy.js`
- `app/tests/e2e/cross-platform.cy.js`

**Modified Files**:

- `app/vitest.config.ts` - Add coverage configuration
- `app/package.json` - Add test coverage scripts
- `.github/workflows/` - Add CI/CD test jobs (if not exists)

---

**Plan Status**: ⚠️ REQUIRES PROJECT OWNER DECISION - Specification significantly exceeds current implementation. Must clarify intent before proceeding to research phase.
