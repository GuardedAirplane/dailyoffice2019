# Feature Specification: Collects and Prayers

**Feature Branch**: `003-collects`  
**Created**: November 6, 2025  
**Status**: Draft  
**Last Updated**: November 7, 2025 (Consolidation Pass)  
**Input**: User description: "Collects: Supports showing all of the various collects/prayers found in the 2019 Book of Common Prayer"

**Cross-Spec Dependencies**:

- **006-general-design**: Settings persistence for language preferences (traditional/contemporary)

## Clarifications

### Session 2025-11-06

- Q: How should collect text formatting be stored and preserved (HTML, plain text, or both)? → A: Allow limited HTML formatting (p, strong, em, br) for traditional book formatting
- Q: What classification/taxonomy system should organize collects? → A: Multi-dimensional tagging with source, theme, season, commemoration_type, and liturgy categories
- Q: Should users be able to select collects to add to their daily office prayers? → A: Yes, with localStorage persistence for daily office integration
- Q: What types of collect alternatives/versions should be supported? → A: Both textual variations and metrical alternatives
- Q: What attribution information should be captured and displayed for collects? → A: Historical attribution (author/source) and BCP page reference

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Browse All Collects (Priority: P1)

A user wants to browse through all collects and prayers available in the Book of Common Prayer 2019, organized by category, to find prayers for specific occasions or needs.

**Why this priority**: Browsing the complete collection of collects is the fundamental use case that delivers immediate value for prayer and devotional needs.

**Independent Test**: Can be fully tested by displaying all collects organized by categories (Sundays, Feasts, Various Occasions, etc.) and verifying complete content from BCP 2019.

**Acceptance Scenarios**:

1. **Given** a user views the collects page, **When** the page loads, **Then** all collects are displayed organized by their categories (Sundays of the Church Year, Holy Days, Various Occasions, etc.)
2. **Given** a user scrolls through collects, **When** they view any collect, **Then** the full prayer text is displayed with proper formatting and attribution (including historical source/author and BCP 2019 page reference when available)
3. **Given** a user views collects, **When** they see multiple categories, **Then** each category is clearly labeled with all collects in that category listed together

---

### User Story 2 - Filter Collects by Category (Priority: P1)

A user wants to filter collects by category to focus on specific types of prayers such as seasonal collects, occasional prayers, or prayers for mission.

**Why this priority**: Filtering is essential for finding relevant prayers quickly among hundreds of collects. Without filtering, users waste time searching.

**Independent Test**: Can be tested independently by selecting category filters and verifying only collects matching those categories are displayed.

**Acceptance Scenarios**:

1. **Given** a user views all collects, **When** they select a specific category filter (e.g., "Sundays"), **Then** only collects from that category are displayed
2. **Given** a user has applied filters, **When** they select multiple categories, **Then** collects from all selected categories appear
3. **Given** a user has active filters, **When** they clear all filters, **Then** the full collection of collects appears again

---

### User Story 3 - Search Collects by Text (Priority: P2)

A user wants to search for collects containing specific words or phrases to find prayers related to particular themes, needs, or occasions.

**Why this priority**: Text search enhances discoverability but category filtering provides the primary organization. Search adds convenience for power users.

**Independent Test**: Can be tested by entering search terms and verifying matching collects appear with search terms highlighted or clearly identified.

**Acceptance Scenarios**:

1. **Given** a user enters a search term, **When** they submit the search, **Then** all collects containing that term in their title or text are displayed
2. **Given** a user performs a search, **When** results appear, **Then** the search term is highlighted or emphasized in the displayed collects
3. **Given** a user has search results, **When** they clear the search, **Then** the full collection of collects reappears

---

### User Story 4 - Switch Language Style (Priority: P2)

A user wants to switch between traditional language (thee/thou) and contemporary language versions of collects based on their personal or congregational preference.

**Why this priority**: Both language styles are important to different users, but the feature works with either style displayed. This is valuable but not blocking.

**Independent Test**: Can be tested by toggling between traditional and contemporary language and verifying all collect texts update to the selected style.

**Acceptance Scenarios**:

1. **Given** a user views collects in contemporary language, **When** they select "Traditional", **Then** all collects update to traditional language with thee/thou forms
2. **Given** a user views collects in traditional language, **When** they select "Contemporary", **Then** all collects update to contemporary language with you/your forms
3. **Given** a user changes language preference, **When** they navigate away and return, **Then** their language preference is remembered

---

### User Story 5 - View Collect for Specific Date (Priority: P3)

A user wants to see which collect is appropriate for a specific calendar date, automatically showing the collect for that day's feast, season, or Sunday.

**Why this priority**: This provides contextual value but depends on calendar integration. Browsing and filtering must work first.

**Independent Test**: Can be tested by selecting any date and verifying the appropriate collect for that day's liturgical observance is displayed.

**Acceptance Scenarios**:

1. **Given** a user selects a specific date, **When** the collect for that day is displayed, **Then** it matches the appropriate feast, Sunday, or seasonal collect from the BCP 2019 calendar
2. **Given** a user views a feast day collect, **When** that feast has multiple collects, **Then** all appropriate collects for that feast are shown
3. **Given** a user views a collect for a date, **When** they navigate to different dates, **Then** the appropriate collect for each date is displayed

---

### User Story 6 - Access Collects by Type (Priority: P3)

A user wants to browse collects by type such as collects for the sick, for the departed, for national life, for the mission of the church, etc.

**Why this priority**: Thematic organization enhances usability for pastoral and occasional use but is secondary to basic browsing and filtering.

**Independent Test**: Can be tested by selecting collect types and verifying collects matching that theme are displayed together.

**Acceptance Scenarios**:

1. **Given** a user browses collect types, **When** they select "Prayers for the Sick", **Then** all collects related to healing and sickness are displayed
2. **Given** a user views collect types, **When** they select "Prayers for Mission", **Then** all collects focused on evangelism and mission work appear
3. **Given** a user explores collect types, **When** they view the available types, **Then** major themes like "Various Occasions", "Pastoral Offices", and "National Life" are represented

---

### User Story 7 - Add Collects to Daily Office (Priority: P2)

A user wants to select additional collects to include in their daily office prayers (Morning Prayer, Midday Prayer, Evening Prayer, Compline) and have those selections persist across sessions.

**Why this priority**: This integrates collects with the core daily office feature, enabling personalized prayer routines. Essential for daily office users but not required for standalone collects browsing.

**Independent Test**: Can be tested by selecting collects for specific offices, verifying they appear in the daily office views, and confirming selections persist after closing/reopening the app.

**Acceptance Scenarios**:

1. **Given** a user browses collects, **When** they select a collect to add to Morning Prayer, **Then** that collect appears in their next Morning Prayer session
2. **Given** a user has added collects to multiple offices, **When** they view each office, **Then** the appropriate selected collects appear in each respective office
3. **Given** a user has selected collects for daily offices, **When** they close and reopen the application, **Then** their collect selections are still active
4. **Given** a user views their selected collects, **When** they remove a collect from an office, **Then** it no longer appears in that office but remains available for browsing

---

### Edge Cases

- What happens when a collect exists in traditional language but not contemporary (or vice versa)?
- How does the system display both textual alternatives and metrical versions for the same collect?
- Should metrical collects be filterable/searchable separately from regular collects?
- What occurs when searching for very common words that appear in many collects?
- How does the system display collects for dates that have multiple possible collects (e.g., a feast with a proper collect and optional alternatives)?
- What happens when filtering produces no matching results?
- How does the system handle special characters or formatting in collect text (italics, small caps, indentation)?
- What happens when a collect has metrical versions but the user is viewing traditional vs contemporary language - do metrical versions correspond to language style?

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST display all collects and prayers from the Book of Common Prayer 2019
- **FR-002**: System MUST organize collects into categories including: Collects for the Church Year (Sundays and Seasons), Collects for Holy Days, Collects for Various Occasions, and other BCP 2019 categories
- **FR-003**: System MUST provide both traditional language (thee/thou) and contemporary language (you/your) versions of each collect (Note: This is specific to liturgical prayers; scripture translation selection is specified in **005-lectionary** FR-006, FR-007)
- **FR-004**: System MUST allow users to switch between traditional and contemporary language with all collects updating accordingly (preference persistence mechanism specified in **006-general-design** FR-007)
- **FR-005**: System MUST allow users to filter collects by category using a multi-dimensional tagging system
- **FR-005a**: System MUST support the following tag categories: source (year/occasional/liturgical), theme (for occasional prayers), season (Advent/Christmas/Epiphany/Lent/Easter/Pentecost), commemoration_type (sunday/major_feast/holy_day), and liturgy (daily office/burial/other liturgical contexts)
- **FR-005b**: System MUST allow collects to have multiple tags across different tag categories simultaneously
- **FR-006**: System MUST allow users to select multiple categories simultaneously when filtering
- **FR-007**: System MUST provide text search functionality to find collects containing specific words or phrases
- **FR-008**: System MUST display the complete text of each collect with proper formatting including indentation, line breaks, and emphasis
- **FR-008a**: System MUST store collect text in rich HTML format (using CKEditor5) with allowed elements: `<p>`, `<strong>`, `<em>`, `<br>` to preserve traditional book formatting
- **FR-008b**: System MUST maintain parallel normalized plain text versions of collects for search indexing and accessibility
- **FR-009**: System MUST preserve the exact wording of collects as they appear in the BCP 2019
- **FR-010**: System MUST display collect titles or numbers to help identify specific prayers
- **FR-010a**: System MUST support attribution field for collects to capture historical source/authorship (e.g., "Thomas Cranmer, 1549") and/or BCP 2019 page references
- **FR-010b**: System MUST display attribution information when present, positioned appropriately near the collect text
- **FR-011**: System MUST show which collect is appropriate for any given liturgical date when date context is provided
- **FR-012**: System MUST handle collects that have multiple acceptable versions or alternatives
- **FR-012a**: System MUST support textual variations of collects (alternative wordings for the same collect)
- **FR-012b**: System MUST support metrical (sung/musical) alternatives for collects, with links to up to 3 metrical versions per collect
- **FR-012c**: System MUST clearly distinguish between textual alternatives and metrical versions in the user interface
- **FR-013**: System MUST maintain the traditional closing forms of collects (e.g., "through Jesus Christ our Lord")
- **FR-014**: System MUST display collects organized by type for occasional use (prayers for the sick, departed, mission, national life, etc.)
- **FR-015**: System MUST remember user's language preference (traditional vs. contemporary) across sessions (persistence mechanism specified in **006-general-design** FR-007, FR-012)
- **FR-016**: System MUST allow users to select individual collects to add to their daily office prayers (Morning Prayer, Midday Prayer, Evening Prayer, Compline)
- **FR-017**: System MUST store user's selected extra collects in localStorage, persisting across sessions without requiring authentication
- **FR-018**: System MUST allow users to view and manage which collects are selected for each daily office type
- **FR-019**: System MUST allow users to remove collects from their daily office selections

### Key Entities

- **Collect**: A formal prayer with traditional structure (address, petition, aspiration, pleading, doxology) from the Book of Common Prayer 2019. Stored with both rich HTML text (for display) and normalized plain text (for search/accessibility).
- **CollectTag**: Individual classification label (e.g., "Advent", "Occasional Prayers", "Mission", "Sunday") applied to collects. Multiple tags can be applied to each collect.
- **CollectTagCategory**: Organizational dimension for tags. Categories include: source (year/occasional/liturgical), theme (healing/mission/departed/etc.), season (Advent/Christmas/etc.), commemoration_type (sunday/major_feast/holy_day), and liturgy (daily office/burial/etc.).
- **Collect Type**: Top-level grouping field (year/occasional/office_prayers/burial_rite/other) used for primary collect organization.
- **Language Style**: Whether a collect is in traditional language (thee/thou forms) or contemporary language (you/your forms). Each collect has separate text and traditional_text fields in HTML and normalized formats.
- **Metrical Collect**: Musical/sung version of a collect with links to sheet music, audio, or other resources. A collect may have up to 3 metrical versions.
- **Attribution**: Optional field capturing historical source/authorship (e.g., "Thomas Cranmer, 1549", "Gelasian Sacramentary") and/or BCP 2019 page reference for scholarly and practical coordination with printed books.
- **Collect Association**: Link between a collect and a specific liturgical day, season, or occasion when it is used

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Users can browse and view all collects from BCP 2019 organized by category in under 5 seconds
- **SC-002**: Users can switch between traditional and contemporary language with all collects updating in under 1 second
- **SC-003**: 90% of users can find a specific collect they're looking for using filters or search within 30 seconds
- **SC-004**: System displays exact text matching the printed Book of Common Prayer 2019 for all collects
- **SC-005**: Users can filter collects by category and see results update immediately with appropriate collects displayed
- **SC-006**: Text search returns relevant collects containing the search term with results appearing in under 2 seconds
- **SC-007**: Language preference (traditional/contemporary) persists across user sessions
- **SC-008**: Users can identify the appropriate collect for any liturgical date when viewing date-specific collects
- **SC-009**: Users can add collects to daily offices and have those selections persist across sessions via localStorage
- **SC-010**: Selected extra collects appear correctly in the appropriate daily office contexts (Morning/Midday/Evening/Compline)

## Assumptions

- Users have access to both traditional and contemporary language styles, with contemporary as the default
- The complete collection includes hundreds of collects covering the full church year and various occasions
- Users may be clergy preparing liturgy, individuals seeking personal prayers, or study groups exploring prayer traditions
- Collect text formatting (indentation, line breaks) is important for readability and traditional presentation
- Users are familiar with terms like "collect" in the liturgical sense
- Internet connectivity is available for loading collect content
- Some users strongly prefer traditional language while others prefer contemporary language
- Collects should be easily copyable for use in bulletins, personal prayer books, or other applications
