# Feature Specification: Lectionary

**Feature Branch**: `005-lectionary`  
**Created**: November 6, 2025  
**Status**: Draft  
**Input**: User description: "Lectionary: Supports showing the various scripture readings and when to read them according to the 2019 Book of Common Prayer"

## User Scenarios & Testing _(mandatory)_

### User Story 1 - View Today's Readings (Priority: P1)

A user wants to see which scripture passages are appointed for today's Daily Office (Morning and Evening Prayer) and Holy Eucharist according to the BCP 2019 lectionary.

**Why this priority**: Viewing today's readings is the fundamental use case that provides immediate practical value for daily scripture reading and worship preparation.

**Independent Test**: Can be fully tested by displaying today's reading assignments with psalm numbers and scripture citations for Morning Prayer, Evening Prayer, and Eucharist.

**Acceptance Scenarios**:

1. **Given** a user views today's readings, **When** the page loads, **Then** psalm assignments from the 60-day cycle and scripture citations appear for both Morning Prayer and Evening Prayer
2. **Given** a user views today's readings, **When** Eucharist readings are appointed, **Then** Old Testament, Psalm, Epistle, and Gospel citations are displayed
3. **Given** today is a feast day, **When** a user views readings, **Then** proper feast day readings replace or supplement the regular daily readings

---

### User Story 2 - View Reading Text (Priority: P1)

A user wants to read the full text of any appointed scripture passage, not just see the citation, so they can read the passage directly without looking it up elsewhere.

**Why this priority**: Displaying full scripture text is essential for the lectionary to be useful for actual Bible reading, not just knowing the citations.

**Independent Test**: Can be tested independently by clicking any scripture citation and verifying the complete passage text appears in a readable format.

**Acceptance Scenarios**:

1. **Given** a user views reading citations, **When** they select a scripture reading, **Then** the full text of that passage appears
2. **Given** a user reads a scripture passage, **When** the passage spans multiple chapters, **Then** all verses in the range display correctly
3. **Given** a user views scripture text, **When** the text includes section headings, **Then** headings are displayed to provide context

---

### User Story 3 - Choose Bible Translation (Priority: P2)

A user wants to select their preferred Bible translation (ESV, NRSV, NIV, KJV, etc.) for viewing scripture readings because different communities and individuals use different translations.

**Why this priority**: Translation selection enhances flexibility but the lectionary provides value with any single translation. Multiple translations are important but not blocking.

**Independent Test**: Can be tested by changing the translation setting and verifying all scripture passages update to display in the selected translation.

**Acceptance Scenarios**:

1. **Given** a user views readings in ESV, **When** they select "NRSV", **Then** all scripture passages update to display in NRSV
2. **Given** a user selects a translation, **When** they navigate to different dates, **Then** the selected translation persists for all readings
3. **Given** a user changes translation, **When** they return to the app later, **Then** their translation preference is remembered

---

### User Story 4 - View Readings for Any Date (Priority: P2)

A user wants to see reading assignments for past or future dates to prepare ahead, catch up on missed readings, or plan liturgies in advance.

**Why this priority**: Date flexibility enhances planning and preparation but viewing today's readings must work first. Historical and future access adds significant value.

**Independent Test**: Can be tested by selecting various past and future dates and verifying correct reading assignments appear for each date based on the liturgical calendar.

**Acceptance Scenarios**:

1. **Given** a user selects a future date, **When** the readings load, **Then** appropriate psalm and scripture assignments for that date are displayed
2. **Given** a user selects a past date, **When** the readings load, **Then** the correct historical reading assignments for that date appear
3. **Given** a user views readings for a date, **When** that date is a major feast, **Then** proper readings for the feast are shown

---

### User Story 5 - Compare Daily Office and Eucharist Readings (Priority: P3)

A user wants to see both Daily Office (Morning/Evening Prayer) readings and Holy Eucharist readings for the same day to understand the full lectionary for that date.

**Why this priority**: Complete lectionary information is valuable but users typically focus on either Daily Office or Eucharist. Comparison enhances completeness.

**Independent Test**: Can be tested by viewing a date and verifying both Daily Office and Eucharist reading assignments are clearly displayed and distinguished.

**Acceptance Scenarios**:

1. **Given** a user views readings for Sunday, **When** both Daily Office and Eucharist readings are appointed, **Then** both sets of readings are clearly labeled and displayed separately
2. **Given** a user views readings for a weekday, **When** they compare Daily Office and Eucharist readings, **Then** any overlap or connection between the readings is apparent
3. **Given** a user views readings, **When** Daily Office and Eucharist have different psalm assignments, **Then** both psalm assignments are shown with clear labels

---

### User Story 6 - Access Lectionary by Season (Priority: P3)

A user wants to browse readings organized by liturgical season (Advent, Christmas, Epiphany, Lent, Easter, Pentecost) to understand the thematic progression of scripture throughout the church year.

**Why this priority**: Seasonal organization provides educational value and helps with long-term planning but is not essential for daily reading.

**Independent Test**: Can be tested by selecting a season and viewing a list of all reading assignments throughout that season.

**Acceptance Scenarios**:

1. **Given** a user selects "Advent", **When** the seasonal readings load, **Then** all reading assignments for each week of Advent are displayed
2. **Given** a user views seasonal readings, **When** they select a specific date within the season, **Then** the detailed readings for that date appear
3. **Given** a user explores seasons, **When** they move between seasons, **Then** the character and focus of readings appropriate to each season is apparent

---

### Edge Cases

- What happens when a reading spans a chapter break (e.g., Genesis 1:1-2:3)? System displays complete passage text across chapter boundaries.
- How does the system handle discontinued passages (verses that are skipped in the reading)? Citation reflects the full range; implementation may include or exclude discontinued verses based on BCP 2019 specification.
- What occurs when multiple possible readings exist for the same date (e.g., optional Old Testament alternatives)? System displays all options with "or" separator, allowing user to view either reading.
- How does the system display readings for dates with transferred feasts? System shows transferred feast readings on the observed date.
- What happens when viewing dates outside the supported lectionary range? System displays appropriate message indicating date is outside supported range.
- How does the system handle apocryphal/deuterocanonical readings that may not be available in all translations? System automatically falls back to NRSVCE when selected translation lacks apocryphal content.
- What occurs when the user's selected Bible translation doesn't include a particular reading (e.g., Sirach in ESV)? System displays notice "Not available in [translation], showing NRSVCE" and shows NRSVCE text.

## Clarifications

### Session 2025-11-06

- Q: Data Model - Lectionary Cycle Year Determination: The spec mentions "two-year Daily Office Lectionary cycle" but doesn't specify how the system determines which year of the cycle applies to a given date. → A: Cycle year determined automatically from Advent year - Year 1 starts on Advent Sunday of even calendar years, Year 2 starts on Advent Sunday in odd calendar years
- Q: Integration & External Dependencies - Scripture Text Retrieval Strategy: The implementation shows multiple Bible sources and the spec mentions internet connectivity for retrieving scripture text, but the primary strategy is unclear. → A: Service worker caching (cache API responses in browser, periodic refresh)
- Q: Edge Cases & Failure Handling - Missing Apocryphal Text Fallback: The spec mentions handling when a translation doesn't include apocryphal readings but doesn't specify what the user should see. → A: Automatic fallback to NRSV/NRSVCE with notice
- Q: Non-Functional Quality Attributes - Eucharist Lectionary Cycle: The spec mentions Holy Eucharist readings but doesn't specify the lectionary cycle used. → A: Three-year cycle (Years A, B, C) following Revised Common Lectionary pattern
- Q: Interaction & UX Flow - Psalm Cycle Selection: The implementation shows references to both "30 day cycle" and "60 day cycle" for psalms but the spec doesn't clarify which is used. → A: 60-day cycle as default, user can optionally select 30-day alternative

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST display scripture reading assignments for any date following the Book of Common Prayer 2019 Daily Office Lectionary
- **FR-002**: System MUST show psalm assignments for Morning Prayer and Evening Prayer for each day, using the 60-day psalter cycle by default with optional 30-day cycle selection
- **FR-003**: System MUST show two scripture readings (typically Old Testament/Apocrypha and New Testament) for both Morning Prayer and Evening Prayer
- **FR-004**: System MUST display Holy Eucharist readings (Old Testament, Psalm, Epistle, Gospel) when they are appointed, following the three-year lectionary cycle (Years A, B, C)
- **FR-005**: System MUST display the full text of any appointed scripture reading retrieved via external Bible APIs with service worker caching for offline access and performance
- **FR-006**: System MUST support multiple Bible translations (at minimum ESV, NRSV, and optionally NIV, KJV, etc.)
- **FR-007**: System MUST allow users to select their preferred Bible translation with all readings updating accordingly
- **FR-008**: System MUST display proper feast day readings when feasts occur, replacing or supplementing daily readings
- **FR-009**: System MUST indicate which readings are for Morning Prayer vs. Evening Prayer vs. Eucharist
- **FR-010**: System MUST handle scripture passages that span multiple chapters or books
- **FR-011**: System MUST support discontinued passages (verses within a range that are skipped)
- **FR-012**: System MUST allow users to view readings for any date, not just today
- **FR-013**: System MUST follow the BCP 2019 two-year Daily Office Lectionary cycle, where Year 1 begins on Advent Sunday in even calendar years and Year 2 begins on Advent Sunday in odd calendar years
- **FR-014**: System MUST display apocryphal/deuterocanonical readings when appointed in the lectionary, automatically falling back to NRSVCE translation with a notice when the user's selected translation doesn't include these books
- **FR-015**: System MUST remember user's translation preference across sessions
- **FR-016**: System MUST provide clear citations for all readings (book, chapter, verse range)
- **FR-017**: System MUST handle alternative or optional readings when they are provided in the lectionary

### Key Entities

- **Lectionary**: The systematic plan for reading through scripture over a specific cycle according to BCP 2019 (two-year cycle for Daily Office, three-year cycle for Holy Eucharist)
- **Reading Assignment**: The psalm and scripture passages appointed for a specific date and office type (Morning Prayer, Evening Prayer, or Eucharist)
- **Scripture Reading**: A specific passage of scripture identified by book, chapter, and verse range, with full text in multiple translations
- **Office Type**: The service for which readings are appointed (Morning Prayer, Evening Prayer, Holy Eucharist)
- **Bible Translation**: A specific version of the Bible (ESV, NRSV, NIV, KJV, etc.)
- **Lectionary Cycle**: The two-year cycle of the Daily Office Lectionary in BCP 2019, where Year 1 begins on Advent Sunday in even calendar years (e.g., 2024) and Year 2 begins on Advent Sunday in odd calendar years (e.g., 2025)
- **Psalter Cycle**: The cycle for reading through the Book of Psalms; BCP 2019 uses a 60-day cycle (completing Psalter every two months) as default, with an optional 30-day cycle (completing Psalter monthly) available
- **Eucharist Lectionary Cycle**: The three-year cycle (Years A, B, C) for Holy Eucharist readings following the Revised Common Lectionary pattern, with Year A focusing on Matthew, Year B on Mark, Year C on Luke, and John interspersed throughout
- **Discontinued Passage**: Verses within a reading range that are omitted from public reading
- **Proper Readings**: Special scripture readings appointed for specific feast days or seasons that replace the ordinary daily readings

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Users can view today's complete reading assignments (psalms and scripture citations) for Morning and Evening Prayer in under 2 seconds
- **SC-002**: Users can read the full text of any appointed scripture passage in their chosen translation in under 3 seconds
- **SC-003**: System correctly displays reading assignments matching the BCP 2019 Daily Office Lectionary for any date within the supported range
- **SC-004**: 95% of users can read their daily scripture assignments without needing external Bible resources or references
- **SC-005**: Users can switch between Bible translations with all readings updating in under 2 seconds
- **SC-006**: System correctly displays feast day proper readings, replacing daily readings on all major feasts and holy days
- **SC-007**: Scripture text displays accurately matching the selected translation with no verses missing or misnumbered
- **SC-008**: Users can view readings for dates from at least 2 years past to 2 years future
- **SC-009**: Translation preference persists across user sessions without requiring re-selection

## Assumptions

- Users need both reading citations (for planning and bulletin preparation) and full scripture text (for actual reading)
- The BCP 2019 Daily Office Lectionary is the authoritative source for reading assignments
- Multiple Bible translations are necessary because different communities use different translations
- Users primarily access readings for today but also need future dates for planning and past dates for catching up
- Internet connectivity is available for initial scripture text retrieval, with service worker caching providing offline access to previously viewed passages
- Apocryphal/deuterocanonical books (Wisdom, Sirach, etc.) are important because they appear in the BCP 2019 lectionary
- Some Bible translations (like ESV) do not include apocryphal books and the system must handle this gracefully
- Reading assignments follow a two-year cycle, though users typically don't need to know which year of the cycle they're in
- Scripture text should include section headings from the translation to provide context
- Users value having Daily Office and Eucharist readings accessible in the same place
