# Feature Specification: Daily Office Liturgy

**Feature Branch**: `001-daily-office`  
**Created**: November 6, 2025  
**Status**: Draft  
**Last Updated**: November 7, 2025 (Consolidation Pass)  
**Input**: User description: "Daily Office: Supports displaying all the various liturgy components for doing the Daily Office found in the 2019 Book of Common Prayer (Morning, Midday, Evening, and Compline)"

**Cross-Spec Dependencies**:

- **005-lectionary**: Authoritative source for Bible translations, API integration, lectionary/psalter cycles
- **006-general-design**: Authoritative source for settings persistence and storage mechanisms

## User Scenarios & Testing _(mandatory)_

### User Story 1 - View Morning Prayer (Priority: P1)

A user wants to pray Morning Prayer for the current day, following the complete liturgy from the Book of Common Prayer 2019. They need to see all components in proper order: opening sentences, confession, psalms, scripture readings, canticles, collects, and closing prayers.

**Why this priority**: Morning Prayer is the primary daily office and represents the core value proposition. Without this, the application has no minimum viable functionality.

**Independent Test**: Can be fully tested by navigating to Morning Prayer for any date and verifying all liturgical elements appear in the correct sequence with appropriate content for that day.

**Acceptance Scenarios**:

1. **Given** a user selects today's date, **When** they view Morning Prayer, **Then** the complete liturgy displays with opening sentence, confession, invitatory psalm, appointed psalms for the day, two scripture readings (Old Testament and New Testament), canticles, prayers, and closing
2. **Given** a user views Morning Prayer, **When** they scroll through the service, **Then** each liturgical component appears in the proper order according to BCP 2019 rubrics
3. **Given** the liturgical calendar indicates a feast day, **When** a user views Morning Prayer, **Then** proper readings, collects, and commemorations for that feast appear instead of the regular daily office readings

---

### User Story 2 - View Evening Prayer (Priority: P1)

A user wants to pray Evening Prayer for the current day, with all appropriate evening-specific elements including evening psalms, scripture readings, Magnificat or alternative canticle, and evening collects.

**Why this priority**: Evening Prayer is equally fundamental to the daily office practice and must be available for the MVP alongside Morning Prayer. Many users pray both offices daily.

**Independent Test**: Can be tested independently by accessing Evening Prayer for any date and confirming all evening-specific liturgical components are present and correctly ordered.

**Acceptance Scenarios**:

1. **Given** a user selects today's date, **When** they view Evening Prayer, **Then** the service displays with opening sentence, confession, evening psalms, two scripture readings, the Magnificat or alternative evening canticle, prayers, and closing
2. **Given** a user views Evening Prayer on a feast day, **When** they review the content, **Then** proper feast-day readings and collects replace the standard daily readings
3. **Given** a user compares Morning and Evening Prayer, **When** they view both services, **Then** the psalm and scripture reading assignments differ appropriately between services

---

### User Story 3 - View Midday Prayer (Priority: P2)

A user wants to pray the shorter Midday Prayer office during their lunch break or middle of the workday, featuring abbreviated psalms, a short scripture reading, and brief prayers.

**Why this priority**: Midday Prayer is important for complete daily office coverage but is briefer and used less frequently than Morning/Evening Prayer. It can be added after core offices are functional.

**Independent Test**: Can be tested by accessing Midday Prayer and verifying it contains the abbreviated liturgical structure appropriate for midday: short opening, one or more brief psalms, short scripture passage, and concluding prayers.

**Acceptance Scenarios**:

1. **Given** a user selects Midday Prayer, **When** they view the service, **Then** it displays with a shorter format including opening, appointed midday psalms, one brief scripture reading, and closing prayers
2. **Given** a user views Midday Prayer, **When** they compare it to Morning or Evening Prayer, **Then** the service is noticeably shorter and suitable for a brief prayer pause

---

### User Story 4 - View Compline (Priority: P2)

A user wants to pray Compline (Night Prayer) before bed, featuring penitential elements, evening psalms, scripture, the Nunc Dimittis, and prayers for protection through the night.

**Why this priority**: Compline completes the full cycle of daily offices but is optional for many users. It should be available after the primary morning and evening offices are functional.

**Independent Test**: Can be tested by accessing Compline and verifying it contains the nighttime liturgical elements: confession, late-evening psalms, short reading, Nunc Dimittis canticle, and prayers for the night.

**Acceptance Scenarios**:

1. **Given** a user selects Compline, **When** they view the service, **Then** it displays with confession, appointed evening psalms, a brief reading, the Nunc Dimittis canticle, and prayers for protection and rest
2. **Given** a user prays Compline, **When** they reach the end, **Then** the service concludes with a blessing appropriate for the end of the day

---

### User Story 5 - Navigate Between Offices (Priority: P2)

A user wants to switch between different daily offices (Morning, Midday, Evening, Compline) for the same day without re-entering the date.

**Why this priority**: Users often pray multiple offices throughout the day and need easy navigation. However, each office must work independently first.

**Independent Test**: Can be tested by viewing one office and using navigation to switch to another office for the same date, verifying the new office loads with correct content.

**Acceptance Scenarios**:

1. **Given** a user is viewing Morning Prayer, **When** they select Evening Prayer from the navigation, **Then** the application displays Evening Prayer for the same date
2. **Given** a user is viewing any office, **When** they select a different office, **Then** the liturgical content updates appropriately while maintaining the same calendar date

---

### User Story 6 - View Office for Different Dates (Priority: P3)

A user wants to view daily offices for past or future dates to prepare ahead, catch up on missed prayers, or review historical liturgies.

**Why this priority**: Date navigation enhances the user experience but is not essential for basic daily prayer. The current date functionality must work first.

**Independent Test**: Can be tested by selecting various past and future dates and verifying appropriate liturgical content loads for each date based on the church calendar.

**Acceptance Scenarios**:

1. **Given** a user selects a future date, **When** they view Morning Prayer, **Then** the service displays with appropriate readings and commemorations for that future date
2. **Given** a user selects a past date, **When** they view any office, **Then** historical liturgical content for that date appears correctly
3. **Given** a user changes dates, **When** they switch between dates, **Then** all liturgical elements update to reflect the selected date's calendar position

---

### User Story 7 - View Family Prayer Offices (Priority: P3)

A user wants to access simplified Family Prayer offices (Family Morning Prayer, Family Midday Prayer, Family Early Evening Prayer, Family Close of Day) designed for praying with children and families.

**Why this priority**: Family Prayer offices are included in BCP 2019 and serve families with young children, but are secondary to traditional offices. They should be accessible but not prominently featured in the primary navigation.

**Independent Test**: Can be tested by accessing any Family Prayer office and verifying simplified liturgical content appropriate for families with children.

**Acceptance Scenarios**:

1. **Given** a user selects a Family Prayer office, **When** they view the service, **Then** it displays with simplified, family-appropriate liturgical content as specified in BCP 2019
2. **Given** a user views the navigation, **When** they look for office options, **Then** Family Prayer offices appear as secondary options (not in primary navigation)

---

### Edge Cases

- **Leap years**: System must correctly handle February 29 in leap years, including appropriate psalm and reading assignments
- **Far future/past dates**: System must dynamically calculate liturgical data for any date requested, including dates far in the future (e.g., year 2050) or past, by computing Easter date, season boundaries, and commemoration occurrences
- **Church year transitions**: System must correctly handle Advent as the start of the new church year, with proper season and Sunday counting across the December 31/January 1 boundary
- **Multiple commemorations**: System must follow BCP 2019 precedence rules when multiple commemorations fall on the same date, selecting the highest-ranked commemoration as primary
- **Missing translation data**: System must fall back to a default translation (NRSVCE) when requested translation is unavailable for a specific passage
- **API unavailability**: When Bible Gateway API is unavailable and passage not cached, system must display error message with offline indicator, provide retry option, and allow continued access to cached content
- **API rate limiting**: System must implement exponential backoff retry logic and respect Bible Gateway rate limits, serving cached content during rate limit periods
- What occurs when a major feast falls on a Sunday (e.g., Christmas) and special precedence rules apply?
- How does the system display content when multiple commemorations occur on the same day?
- What happens if scripture reading data is unavailable for a particular translation?
- How does the system handle the transition between church years (Advent begins the new church year)?
- What occurs when Bible Gateway API is temporarily unavailable and the passage is not in the cache?
- How does the system handle rate limiting from Bible Gateway API?

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST display Morning Prayer with all required liturgical components: opening sentence, confession, invitatory, psalms, two scripture readings, canticles, apostles' creed, prayers, and closing
- **FR-002**: System MUST display Evening Prayer with all required liturgical components: opening sentence, confession, psalms, two scripture readings, evening canticle (Magnificat or alternative), apostles' creed, prayers, and closing
- **FR-003**: System MUST display Midday Prayer with abbreviated liturgical components: opening, psalms, one scripture reading, and prayers
- **FR-004**: System MUST display Compline with required liturgical components: confession, psalms, scripture reading, Nunc Dimittis, and night prayers
- **FR-005**: System MUST assign different psalm readings to Morning Prayer and Evening Prayer for each day as specified in **005-lectionary** (see FR-002)
- **FR-005a**: _(Psalter cycle details consolidated into 005-lectionary FR-002)_
- **FR-005b**: _(Psalter cycle selection consolidated into 005-lectionary FR-002)_
- **FR-006**: System MUST assign two scripture readings (Old Testament/Apocrypha and New Testament) to each of Morning Prayer and Evening Prayer as specified in **005-lectionary** (see FR-003)
- **FR-006a**: _(Lectionary cycle details consolidated into 005-lectionary FR-013)_
- **FR-006b**: _(Lectionary cycle selection consolidated into 005-lectionary FR-013)_
- **FR-007**: System MUST substitute proper readings, psalms, and collects when the liturgical calendar indicates a feast day or holy day
- **FR-008**: System MUST display appropriate canticles for each office type (e.g., Benedictus for Morning Prayer, Magnificat for Evening Prayer, Nunc Dimittis for Compline)
- **FR-009**: System MUST include the full text of prayers, canticles, and liturgical responses so users can pray without referencing other resources
- **FR-010**: System MUST format liturgical text with proper indentation, versicles and responses, and rubrics (instructional text)
- **FR-011**: System MUST display commemorations and feast names when applicable to the selected date
- **FR-012**: System MUST allow users to view offices for any date, not just the current day
- **FR-012a**: System MUST calculate liturgical data (season, commemorations, readings, psalms) dynamically for any requested date without predetermined date range limits
- **FR-013**: System MUST provide navigation between different office types (Morning, Midday, Evening, Compline) while maintaining the same date selection
- **FR-014**: System MUST calculate and display the correct liturgical season and associated elements for any given date
- **FR-015**: System MUST follow the Book of Common Prayer 2019 text and rubrics exactly as published
- **FR-016**: System MUST support scripture readings in multiple Bible translations as specified in **005-lectionary** (see FR-006, FR-007 in that spec)
- **FR-017**: System MUST allow users to select their preferred Bible translation for scripture readings as specified in **005-lectionary**
- **FR-018**: System MUST provide Family Prayer offices (Family Morning, Midday, Early Evening, Close of Day) as specified in BCP 2019
- **FR-019**: System MUST present Family Prayer offices as secondary navigation options, not in primary office navigation
- **FR-020**: System MUST retrieve scripture text via the strategy specified in **005-lectionary** (see FR-005, FR-014 for Bible Gateway API integration and caching)
- **FR-021**: _(Consolidated into 005-lectionary FR-005)_
- **FR-022**: _(Consolidated into 005-lectionary FR-005, FR-014)_
- **FR-022a**: _(Consolidated into 005-lectionary FR-014)_
- **FR-022b**: _(Consolidated into 005-lectionary FR-014)_
- **FR-022c**: _(Consolidated into 005-lectionary FR-014)_
- **FR-023**: System MUST store user preferences as specified in **006-general-design** (see FR-007, FR-012 for comprehensive settings persistence strategy using localStorage/Capacitor Preferences)
- **FR-024**: _(Consolidated into 006-general-design FR-007)_
- **FR-025**: _(Consolidated into 006-general-design FR-007)_
- **FR-026**: System MUST provide user-accessible settings for liturgical customization options including: confession introduction length (short/long/fast-days-only), absolution style (priest/lay), invitatory preference (traditional/celebratory/rotating), canticle rotation (traditional/seasonal/daily), opening sentence style (fixed/seasonal), and collect rotation (high-level requirements in **006-general-design** FR-006; Daily Office-specific customizations detailed here)
- **FR-027**: System MUST provide sensible defaults for all liturgical customization options that follow traditional BCP usage patterns
- **FR-028**: System MUST make liturgical customization settings accessible from the main settings interface without requiring advanced/expert mode

### Key Entities

- **Office**: Represents one of the four daily prayer services (Morning Prayer, Midday Prayer, Evening Prayer, Compline) with its specific liturgical structure and components
- **Office Day**: Represents a specific date with assigned readings, psalms, and commemorations for that day
- **Liturgical Component**: Individual elements of the office such as opening sentence, confession, invitatory, psalm, reading, canticle, prayers, etc.
- **Psalm Assignment**: Links specific psalms to be read at Morning or Evening Prayer on a particular day
- **Scripture Reading**: Bible passage assigned to a particular office and date, identified by book, chapter, and verse range
- **Canticle**: Biblical song or hymn used in the office (e.g., Benedictus, Magnificat, Nunc Dimittis, Te Deum)
- **Collect**: Prayer associated with the day, week, or season
- **Commemoration**: Recognition of a saint, feast day, or holy day occurring on a particular date

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Users can view complete Morning Prayer or Evening Prayer for any date with all liturgical components displayed correctly in under 3 seconds
- **SC-002**: System accurately displays proper feast day readings and collects for all major feasts and holy days in the BCP 2019 calendar
- **SC-003**: Users can navigate between all four office types (Morning, Midday, Evening, Compline) for any date without errors
- **SC-004**: 95% of daily office users successfully complete their prayer service without needing to reference external resources or encounter missing content
- **SC-005**: System displays liturgical content accurately matching the printed Book of Common Prayer 2019 for any randomly selected date
- **SC-006**: Users can access offices for dates ranging from at least 2 years in the past to 2 years in the future
- **SC-007**: All psalm assignments follow either the 30-day or 60-day Psalter cycle (user-selected) or appointed ferial psalms correctly based on the date
- **SC-008**: System handles all liturgical precedence rules correctly when multiple commemorations or feasts occur on the same date

## Clarifications

### Session 2025-11-06

- Q: Which Bible translation is the default, and what alternatives are supported? → A: ESV is the default translation, with user-selectable alternatives from the 9 supported translations
- Q: How should Family Prayer offices be prioritized? → A: Secondary UI options per BCP
- Q: Which Psalter cycles are supported? → A: Support both 30-day and 60-day Psalter cycles with user selection between them
- Q: What is the scripture text source and connectivity requirement? → A: Bible Gateway is the primary source with local database caching; internet required for new passages
- Q: Should audio playback features be specified? → A: Audio should not be mentioned in the spec (implementation detail only)
- Q: How should user preferences (Psalter cycle, lectionary cycle, Bible translation, canticle rotation, etc.) be stored and managed? → A: Client-side browser storage only (localStorage/cookies) with no server sync
- Q: What determines which lectionary cycle (1-year vs 2-year) a user should use? → A: 1-year cycle for those praying only one office per day; 2-year cycle for those praying both Morning and Evening Prayer daily
- Q: What is the valid date range for the application? → A: Unlimited range; calculate liturgical data for any date requested
- Q: Should liturgical customization options (confession style, absolution style, invitatory rotation, canticle rotation, etc.) be considered core or advanced features? → A: Core features with sensible defaults, visible in main settings
- Q: What should happen when Bible Gateway API is unavailable and a passage is not yet cached? → A: Display error message with offline indicator and retry option; allow viewing other cached content

## Assumptions

- Users are familiar with Anglican liturgical terminology and the basic structure of daily prayer offices
- The application has access to complete psalm texts, scripture readings, and liturgical content from the Book of Common Prayer 2019
- The liturgical calendar data includes feast days, holy days, and commemorations for the date range being supported
- Users expect liturgical content to match the printed Book of Common Prayer 2019 exactly
- Internet connectivity is available for retrieving scripture passages from Bible Gateway API for passages not in the local cache
- Bible Gateway API remains available and maintains current scripture text and translation offerings
- The system can dynamically calculate liturgical data for any date without requiring pre-populated database entries for future years
- Easter date calculation algorithm is accurate for all Gregorian calendar years
