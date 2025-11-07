# Feature Specification: Cross-Platform Access and Settings

**Feature Branch**: `006-general-design`  
**Created**: November 6, 2025  
**Status**: Draft  
**Last Updated**: November 7, 2025 (Consolidation Pass)  
**Input**: User description: "General Design: Supports a web hosted version as well as mobile apps. Also supports a wide array of settings and the ability to share them with others"

**Authoritative Responsibilities** (referenced by other specs):

- Settings persistence mechanism (localStorage, Capacitor Preferences, DynamicStorage) (FR-007, FR-012)
- Settings sharing and URL encoding (FR-008, FR-008a)
- Cross-platform storage strategies (FR-012)

**Note**: This spec is referenced by 001-daily-office, 003-collects, 004-psalter, and 005-lectionary for their respective settings persistence needs.

## Clarifications

### Session 2025-11-06

- Q: What is the offline caching implementation for web vs mobile apps? → A: Mobile apps cache via Capacitor; web relies on browser caching
- Q: What level of WCAG accessibility compliance is required? → A: Basic keyboard navigation and semantic HTML as MVP; comprehensive WCAG 2.1 AA as future enhancement
- Q: What browser versions must be supported and how should older browsers be handled? → A: Support last 2 major versions of modern browsers; graceful degradation is aspirational
- Q: How should settings conflicts be resolved when a user accesses a shared settings link? → A: Settings applied immediately with notification; history tracking is future enhancement
- Q: What metric defines the "3 seconds" initial content load time target? → A: Time to First Contentful Paint; monitoring is future enhancement

### Session 2025-11-07 - Conformance Audit

**Status**: Specification revised to match current implementation state as of November 2025.

**Current Implementation vs. Original Spec**:

- ✅ **Implemented**: Web + mobile apps, settings persistence, settings sharing via URL, responsive design, deep linking
- 🔄 **Partial**: Basic accessibility (semantic HTML exists), offline support (mobile only via Capacitor)
- ❌ **Not Implemented**: Service worker/PWA, settings history, settings confirmation prompts, performance monitoring, browser detection
- ❌ **Testing Gap**: Minimal test coverage exists; comprehensive testing required per Constitution Principle III

**Revision Approach**: Requirements marked as "MUST" represent current implementation. Requirements marked as "SHOULD" or "MAY" represent future enhancements. New section added documenting future roadmap items.

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Access on Web Browser (Priority: P1)

A user wants to access the Daily Office application through a web browser on their desktop or laptop computer without installing any software.

**Why this priority**: Web access is the most universal platform, requiring no installation and working across all operating systems. This is the foundation for all other access methods.

**Independent Test**: Can be fully tested by accessing the application URL in any modern web browser and verifying all features work correctly.

**Acceptance Scenarios**:

1. **Given** a user opens a web browser, **When** they navigate to the application URL, **Then** the Daily Office application loads and displays the current day's office
2. **Given** a user accesses the web application, **When** they interact with features (viewing offices, calendar, collects, etc.), **Then** all features function correctly in the browser
3. **Given** a user uses different web browsers (Chrome, Firefox, Safari, Edge), **When** they access the application, **Then** the application works consistently across all browsers

---

### User Story 2 - Access on Mobile Device (Priority: P1)

A user wants to access the Daily Office application on their smartphone or tablet through a mobile browser or dedicated mobile app for convenient prayer access anywhere.

**Why this priority**: Mobile access is essential as users pray throughout the day in various locations. Many users primarily or exclusively access via mobile devices.

**Independent Test**: Can be tested independently by accessing the application on iOS and Android devices and verifying proper mobile display and touch interactions.

**Acceptance Scenarios**:

1. **Given** a user opens their mobile device, **When** they access the application via mobile browser or app, **Then** the interface adapts to the mobile screen size with readable text and accessible controls
2. **Given** a user interacts with the mobile version, **When** they tap on elements or scroll, **Then** touch gestures work smoothly and responsively
3. **Given** a user views offices on mobile, **When** they scroll through liturgical content, **Then** the text remains readable without horizontal scrolling required

---

### User Story 3 - Customize Display Settings (Priority: P2)

A user wants to adjust various display and content settings such as font size, language style (traditional vs. contemporary), translations, and which optional elements to include or exclude.

**Why this priority**: Customization significantly enhances user experience but the application provides value with default settings. Preferences matter more after initial use.

**Independent Test**: Can be tested by changing various settings and verifying the application updates accordingly with changes persisting across sessions.

**Acceptance Scenarios**:

1. **Given** a user accesses settings, **When** they increase font size, **Then** all liturgical text displays larger for easier reading
2. **Given** a user selects traditional language, **When** they view prayers and canticles, **Then** thee/thou forms are used throughout
3. **Given** a user changes Bible translation to NRSV, **When** they view scripture readings, **Then** all passages display in NRSV
4. **Given** a user saves settings, **When** they close and reopen the application, **Then** all their preferences are remembered

---

### User Story 4 - Share Settings with Others (Priority: P2)

A user wants to share their customized settings with others (family members, congregation, small group) so everyone can use the same preferences and see identical content.

**Why this priority**: Settings sharing enables coordinated group prayer, which is central to the Daily Office's communal purpose. Currently implemented and actively used.

**Independent Test**: Can be tested by generating a shareable settings link (via URL or QR code), having another user access that link, and verifying they receive the same settings configuration.

**Implementation Note**: Settings sharing is currently implemented via URL parameters with a compact encoding scheme. QR code generation is also available. Settings are applied immediately when accessing a shared link, with a success notification displayed. Future enhancements may include confirmation prompts and history tracking.

**Acceptance Scenarios**:

1. **Given** a user has customized their settings, **When** they select "Share Settings", **Then** a shareable link is generated encoding their current configuration
2. **Given** another user clicks the shared settings link, **When** the page loads, **Then** the settings are automatically applied and a notification confirms the settings were received
3. **Given** a user wants to share via mobile device, **When** they open the share panel, **Then** they can use the native share dialog or display a QR code
4. **Given** settings are shared with a group, **When** each member uses the shared link, **Then** they all see the same content and preferences
5. **Given** a user wants to share via QR code, **When** they view the QR code in the share panel, **Then** others can scan it to receive the settings link

---

### User Story 5 - Responsive Design Across Devices (Priority: P2)

A user wants the application to automatically adapt its layout and design to whatever device they're using (phone, tablet, laptop, desktop) without manual adjustment.

**Why this priority**: Responsive design is important for usability but initial support for web and mobile covers the fundamental need. Advanced responsiveness enhances polish.

**Independent Test**: Can be tested by accessing the application on devices of various screen sizes and verifying appropriate layout adaptations.

**Acceptance Scenarios**:

1. **Given** a user accesses on a small phone screen, **When** the application loads, **Then** navigation condenses to a mobile menu and content displays in a single column
2. **Given** a user accesses on a tablet, **When** the application loads, **Then** the layout uses available space efficiently with appropriate text size and spacing
3. **Given** a user accesses on a large desktop monitor, **When** the application loads, **Then** content is centered or formatted to avoid excessively long line lengths

---

### User Story 6 - Offline Access (Priority: P3)

A user wants to access previously loaded offices and content when internet connectivity is unavailable, allowing prayer in areas without signal or during outages.

**Why this priority**: Offline access enhances reliability but requires the online version to work first. Most users have regular connectivity but offline is valuable for specific situations like travel or poor connectivity areas.

**Independent Test**: Can be tested by loading content while online in mobile app, disconnecting from internet, and verifying previously accessed content remains available.

**Implementation Note**: Native mobile apps (iOS/Android) have basic offline capability through Capacitor's built-in caching. Settings are persisted via Capacitor Preferences API on mobile and localStorage on web. Web version relies on browser caching but does not implement a service worker for comprehensive offline support (future enhancement).

**Acceptance Scenarios**:

1. **Given** a user has viewed content in the mobile app while online, **When** they lose internet connection, **Then** some previously loaded content may remain accessible via browser/WebView caching
2. **Given** a user's settings are saved, **When** they access the app offline (mobile), **Then** their settings preferences are retained and applied
3. **Given** a user is using the web version offline, **When** they try to navigate, **Then** behavior depends on browser caching and may show cached pages or connection errors

---

### Edge Cases

- What occurs when settings are shared but include options not available in all versions (e.g., mobile-specific features)?
- How does the application behave on very small screens (smartwatches) or very large screens (4K monitors)?
- What happens when a user's device storage is full and offline caching fails or settings history cannot be saved?
- What occurs when the user's device has different language or regional settings than the application?
- How does the application handle service worker update conflicts when a user has an old cached version?
- What happens if a user attempts to restore a settings history entry that is no longer compatible with the current app version?

## Requirements _(mandatory)_

### Functional Requirements

#### Core Platform Access (Currently Implemented)

- **FR-001**: System MUST be accessible via web browser on desktop and laptop computers without requiring software installation
- **FR-002**: System MUST be accessible via mobile web browser on iOS and Android smartphones and tablets
- **FR-003**: System MUST provide native mobile app versions for iOS and Android devices via Capacitor
- **FR-004**: System MUST automatically adapt layout and design to different screen sizes and device types (responsive design) using Tailwind CSS and responsive breakpoints
- **FR-005**: System MUST support modern web browsers (Chrome, Firefox, Safari, Edge) on desktop and mobile platforms
- **FR-016**: System MUST maintain consistent functionality across all supported platforms (web, iOS, Android)
- **FR-017**: System MUST support deep linking to specific dates, offices, or content for sharing and bookmarking (implemented for mobile apps)

#### Settings & Customization (Currently Implemented)

**Note**: This spec is the **authoritative source** for settings persistence and management across all features. Other specs (001-daily-office, 003-collects, 004-psalter, 005-lectionary) reference these requirements for their specific settings domains.

- **FR-006**: System MUST provide customizable settings including:
  - Font size adjustment
  - Language style (traditional/contemporary) - see **003-collects** FR-003, **004-psalter** FR-012 for feature-specific details
  - Bible translation selection - see **005-lectionary** FR-006, FR-007 for authoritative translation requirements
  - Psalm translation selection - see **004-psalter** FR-012, FR-013 for Coverdale edition details
  - Psalter cycle selection (30-day/60-day) - see **005-lectionary** FR-002a, FR-002b
  - Lectionary cycle selection (1-year/2-year) - see **005-lectionary** FR-013a, FR-013b
  - Optional liturgical elements (collects, canticles, etc.) - see **001-daily-office** FR-026 for Daily Office customizations
  - Calendar tracking options
  - Display preferences
- **FR-007**: System MUST persist user settings across sessions without requiring account creation, using:
  - localStorage for web browsers
  - Capacitor Preferences API for native mobile apps
  - DynamicStorage abstraction layer for unified access
- **FR-008**: System MUST allow users to generate shareable links that encode their current settings using:
  - URL parameter encoding with compact abbreviation scheme
  - QR code generation for mobile sharing
  - Native share dialog integration on mobile platforms
- **FR-008a**: System MUST apply shared settings when users access settings-encoded URLs, with success notification displayed
- **FR-014**: System MUST allow users to adjust which optional liturgical elements are included or excluded in offices through the settings interface

#### User Interface & Interaction (Currently Implemented)

- **FR-010**: System MUST provide touch-friendly controls and interactions on mobile devices with appropriate tap targets and gesture support
- **FR-011**: System MUST display readable text without requiring horizontal scrolling on any device
- **FR-013**: System MUST provide basic accessibility features including:
  - Semantic HTML5 structure (nav, main, article, section elements)
  - Responsive navigation patterns
  - Font size customization
  - Dark/light theme support

#### Storage & Persistence (Currently Implemented)

- **FR-012**: System MUST persist settings across sessions using:
  - Capacitor Preferences API for native mobile apps
  - localStorage for web browsers
  - DynamicStorage helper providing unified storage interface

#### Future Enhancements (Not Yet Implemented)

- **FR-005a** _(Future)_: System SHOULD display a graceful degradation message for unsupported older browsers, informing users of minimum browser requirements and suggesting upgrade options
- **FR-005b** _(Future)_: Browser detection SHOULD identify unsupported browsers on application load and present clear upgrade guidance without breaking the page layout
- **FR-009** _(Future)_: System SHOULD prompt users for confirmation before applying shared settings from a link, displaying what changes will occur
- **FR-009a** _(Future)_: System MAY maintain a timestamped history of previous settings configurations to allow rollback
- **FR-009b** _(Future)_: System MAY allow users to view their settings history and restore any previous timestamped configuration
- **FR-009c** _(Future)_: Settings history MAY store at minimum the last 10 configurations with timestamps, automatically pruning older entries
- **FR-012a** _(Future)_: Web version SHOULD implement service worker for offline content caching, asset caching, and network request interception to enable PWA functionality
- **FR-012b** _(Future)_: System SHOULD provide comprehensive offline content caching beyond basic settings persistence
- **FR-013a** _(Future)_: System SHOULD progress toward WCAG 2.1 Level AA compliance in future enhancements including comprehensive screen reader support, skip links, focus indicators, high contrast mode, and full ARIA labeling
- **FR-015** _(Future)_: System SHOULD achieve Time to First Contentful Paint (FCP) under 3 seconds on standard internet connections (broadband 5+ Mbps or 4G mobile)
- **FR-015a** _(Future)_: System MAY implement client-side performance monitoring to track FCP metrics using browser Performance API or equivalent
- **FR-015b** _(Future)_: Performance metrics MAY be captured for analysis to identify optimization opportunities and track performance regressions

### Key Entities

#### Currently Implemented

- **User Settings**: Collection of user preferences including font size, language style, translations, optional elements, and display preferences. Stored as JSON in localStorage (web) or Capacitor Preferences (mobile)
- **Settings Profile**: A shareable configuration of settings that can be distributed via URL parameters using compact abbreviation encoding scheme
- **Settings Abbreviation Map**: Mapping between setting names/values and compact URL-safe abbreviations for efficient sharing
- **DynamicStorage**: Abstraction layer providing unified storage interface across platforms (wraps localStorage for web, Capacitor Preferences for mobile)
- **Platform**: The environment where the application runs (web browser, iOS app, Android app), detected via Capacitor.getPlatform()
- **Device Type**: Classification of the user's device (phone, tablet, desktop) affecting layout and interaction patterns, determined by viewport width
- **Responsive Breakpoint**: Screen size thresholds where layout adapts (Tailwind CSS breakpoints: sm, md, lg, xl, 2xl)
- **Share Dialog**: Native platform share sheet (mobile) or custom sharing interface (web) for distributing settings links
- **QR Code**: Visual representation of settings link for easy scanning and sharing
- **Extra Collects**: Additional collect prayers selected by user, stored separately from main settings, encoded in URL parameters

#### Future Enhancements

- **Settings History** _(Future)_: Timestamped log of previous settings configurations allowing users to revert to earlier preferences
- **Settings History Entry** _(Future)_: Single record containing complete settings snapshot and ISO 8601 timestamp
- **Offline Cache** _(Future)_: Locally stored content beyond settings, enabling access without internet connectivity via service worker
- **Service Worker** _(Future)_: Background script enabling PWA features including offline caching and asset caching
- **Performance Metrics** _(Future)_: Client-side measurements of application load times (FCP, LCP, etc.)
- **Accessibility Feature** _(Future)_: Enhanced functionality supporting users with disabilities (comprehensive ARIA, skip links, screen reader optimization)

## Success Criteria _(mandatory)_

### Measurable Outcomes

#### Currently Implemented & Verified

- **SC-001**: Application loads and displays correctly in modern browsers (Chrome, Firefox, Safari, Edge) on both desktop and mobile platforms
- **SC-002**: Users can access full Daily Office functionality on iOS and Android mobile devices via Capacitor-wrapped apps with touch interactions working smoothly
- **SC-003**: Layout automatically adapts appropriately across devices from small phones (320px width) to large desktop monitors (2560px+ width) using Tailwind CSS responsive utilities
- **SC-004**: User settings persist across sessions with 100% reliability without requiring accounts or login, using DynamicStorage abstraction (localStorage + Capacitor Preferences)
- **SC-005**: Users can share their settings via URL link or QR code; recipients automatically receive shared settings when accessing the link with success notification displayed
- **SC-009**: Settings interface provides intuitive controls allowing users to adjust preferences efficiently
- **SC-010**: Font size adjustments (via FontSizer component) make text readable for users with visual impairments without breaking layout
- **SC-011**: Settings sharing works across platforms - links generated on web work on mobile apps and vice versa through URL parameter encoding

#### Future Enhancement Targets

- **SC-001a** _(Future)_: Graceful degradation messages for unsupported older browsers
- **SC-005a** _(Future)_: Confirmation prompt before applying shared settings
- **SC-005b** _(Future)_: Settings history with ability to restore previous configurations
- **SC-006** _(Future)_: Time to First Contentful Paint (FCP) under 3 seconds for 95% of users on standard connections, measured via Performance API
- **SC-007** _(Future)_: Comprehensive offline content access on web via service worker (mobile apps have basic offline capability)
- **SC-008** _(Future)_: WCAG 2.1 Level AA accessibility compliance with comprehensive screen reader support, skip links, and full ARIA labeling

## Implementation Roadmap

### Phase 1: Testing Infrastructure (CURRENT PRIORITY)

**Timeline**: 3-4 weeks  
**Rationale**: Constitution Principle III requires comprehensive testing; this is non-negotiable

**Objectives**:

- Establish test coverage baseline for existing functionality
- Achieve 90%+ function coverage for utility functions and helpers
- Implement component tests for key Vue components
- Create E2E tests for critical user journeys
- Set up CI/CD test automation

**Key Deliverables**:

- Unit tests for: DynamicStorage, settings encoding/decoding, storage helpers
- Component tests for: Settings.vue, ShareSettings.vue, SettingsPanel.vue
- E2E tests for: Settings persistence, settings sharing, cross-platform consistency
- Test coverage reporting integrated into build process

### Phase 2: Accessibility Enhancements

**Timeline**: 2-3 weeks  
**Rationale**: Aligns with Constitution Principle I (Glory to God) - ensuring all users can participate in daily prayer

**Objectives**:

- Audit current accessibility state against WCAG 2.1 Level AA
- Add ARIA labels to interactive elements
- Implement keyboard navigation improvements
- Add skip links and focus management
- Test with screen readers
- Document accessibility features

**Key Deliverables**:

- Accessibility audit report
- Enhanced keyboard navigation
- ARIA labels on all interactive components
- Skip links for main content navigation
- Screen reader testing results
- Accessibility testing integrated into CI/CD

### Phase 3: Settings Confirmation & History

**Timeline**: 2-3 weeks  
**Rationale**: Improves user safety when accepting shared settings; provides rollback capability

**Objectives**:

- Implement confirmation dialog before applying shared settings
- Create settings history data model (timestamped snapshots)
- Build settings history UI for viewing and restoring configurations
- Extend DynamicStorage to support history management
- Automatic pruning of old history entries (keep last 10)

**Key Deliverables**:

- SettingsConfirmation.vue component showing diff preview
- SettingsHistory.vue component with restore capability
- Enhanced store mutations for history tracking
- Tests for history functionality

### Phase 4: Progressive Web App (PWA)

**Timeline**: 2-3 weeks  
**Rationale**: Brings web version closer to mobile app experience with offline capability

**Objectives**:

- Implement service worker with cache strategies
- Enable offline access to previously viewed content
- Add PWA manifest and icons
- Implement cache versioning and invalidation
- Create offline fallback pages

**Key Deliverables**:

- Service worker registration and lifecycle management
- Caching strategies for static assets and API responses
- Complete PWA manifest with all required fields
- Offline fallback UI
- Service worker tests

### Phase 5: Performance Monitoring

**Timeline**: 1-2 weeks  
**Rationale**: Enables data-driven optimization; validates performance goals

**Objectives**:

- Implement client-side performance tracking
- Capture Time to First Contentful Paint (FCP)
- Optional: Report metrics to analytics or backend
- Create performance dashboard/monitoring

**Key Deliverables**:

- Performance monitoring utility using Performance API
- FCP tracking and logging
- Optional: Performance metrics reporting endpoint
- Performance regression tests

### Phase 6: Browser Detection & Graceful Degradation

**Timeline**: 3-5 days  
**Rationale**: Low priority; quick win for user experience on unsupported browsers

**Objectives**:

- Implement browser version detection
- Create warning banner for unsupported browsers
- Provide clear upgrade guidance
- Ensure banner doesn't break layout

**Key Deliverables**:

- Browser detection utility
- UnsupportedBrowserBanner.vue component
- Supported browser version configuration
- Tests for detection logic

### Total Estimated Timeline

**Thorough Implementation**: 16-20 weeks total

## Assumptions

- Users access the application from a variety of devices and prefer seamless experience across all of them
- Most users have regular internet connectivity but occasional offline access is valuable
- Settings preferences are personal and vary significantly between users
- Some users (families, congregations, groups) want to coordinate settings for unified experience (settings sharing actively used)
- Users should not be required to create accounts or log in for basic functionality
- Touch interactions on mobile devices require larger tap targets than mouse clicks on desktop
- Responsive design should optimize content layout for the available screen space
- Accessibility is important to ensure all users can participate in daily prayer regardless of disabilities
- Settings should persist using browser storage mechanisms without server-side accounts
- Mobile apps provide benefits over mobile web including offline support, home screen presence, and platform integration
- Users expect modern web application performance (fast loading, smooth interactions)
- Deep linking allows users to share specific dates or content with others via URL (implemented for mobile)
- The application should work across time zones, automatically using the user's local time for "today"
- Testing infrastructure must be established before implementing new features (Constitution Principle III)
