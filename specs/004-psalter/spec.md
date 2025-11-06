# Feature Specification: Psalter

**Feature Branch**: `004-psalter`  
**Created**: November 6, 2025  
**Status**: Draft  
**Input**: User description: "Psalter: Supports showing all of the various Psalms from the 2019 Book of Common Prayer"

## User Scenarios & Testing _(mandatory)_

### User Story 1 - View Individual Psalm (Priority: P1)

A user wants to read a specific psalm from the Psalter in the Book of Common Prayer 2019 Coverdale translation, formatted with proper verse structure and pointing marks for chanting.

**Why this priority**: Viewing individual psalms is the fundamental use case for the Psalter feature, providing immediate devotional and liturgical value.

**Independent Test**: Can be fully tested by selecting any psalm number (1-150) and verifying the complete psalm text appears in the Coverdale translation with proper formatting.

**Acceptance Scenarios**:

1. **Given** a user selects Psalm 23, **When** the psalm loads, **Then** all verses of Psalm 23 appear in the Coverdale translation with the traditional text ("The Lord is my shepherd, therefore can I lack nothing")
2. **Given** a user views any psalm, **When** they scroll through it, **Then** each verse is numbered and formatted with proper indentation for parallelism
3. **Given** a user views a psalm, **When** the psalm includes a Latin title (e.g., "Deus, Deus meus"), **Then** the Latin title appears at the beginning

---

### User Story 2 - Browse Psalms by Number (Priority: P1)

A user wants to navigate through all 150 psalms in numerical order to find specific psalms or browse the complete Psalter.

**Why this priority**: Navigation is essential for users to access any psalm they need. Without navigation, only viewing a single psalm has limited value.

**Independent Test**: Can be tested independently by navigating through psalm numbers and verifying each psalm loads correctly with proper numbering.

**Acceptance Scenarios**:

1. **Given** a user views the Psalter, **When** they select a psalm number from the list, **Then** that psalm displays with complete text
2. **Given** a user views Psalm 50, **When** they navigate to the next psalm, **Then** Psalm 51 displays
3. **Given** a user views Psalm 100, **When** they navigate to the previous psalm, **Then** Psalm 99 displays

---

### User Story 3 - View Psalm Ranges (Priority: P2)

A user wants to view multiple consecutive psalms or psalm ranges (e.g., "Psalms 120-134" or "Psalm 119:1-32") as they are often appointed together in the Daily Office.

**Why this priority**: Psalm ranges are commonly appointed in the lectionary, but individual psalm viewing must work first. This enhances Daily Office integration.

**Independent Test**: Can be tested by specifying a psalm range and verifying all psalms in that range display sequentially.

**Acceptance Scenarios**:

1. **Given** a user specifies "Psalms 1-3", **When** the range loads, **Then** Psalms 1, 2, and 3 display in sequence
2. **Given** a user views a psalm range, **When** they scroll, **Then** clear markers indicate where each psalm begins and ends
3. **Given** a user specifies Psalm 119:1-32 (a portion of a long psalm), **When** the text loads, **Then** only verses 1-32 of Psalm 119 appear

---

### User Story 4 - Search Psalms by Topic (Priority: P2)

A user wants to find psalms related to specific themes or topics (e.g., comfort, praise, thanksgiving, morning, evening) using thematic categories.

**Why this priority**: Thematic access helps users find appropriate psalms for specific situations but is secondary to basic psalm viewing and navigation.

**Independent Test**: Can be tested by selecting a topic category and verifying a curated list of relevant psalms appears.

**Acceptance Scenarios**:

1. **Given** a user selects the topic "Praise and Thanksgiving", **When** the results appear, **Then** a list of psalms appropriate for praise (e.g., Psalms 100, 103, 145-150) is displayed
2. **Given** a user selects "Morning Prayer", **When** the results appear, **Then** psalms traditionally used for morning (e.g., Psalms 3, 5, 63) are shown
3. **Given** a user views topic results, **When** they select any psalm from the list, **Then** that psalm's full text displays

---

### User Story 5 - Choose Psalm Translation (Priority: P3)

A user wants to switch between different psalm translations (Coverdale from BCP 2019, ESV, NRSV, etc.) to compare texts or use their preferred version.

**Why this priority**: While multiple translations enhance flexibility, the BCP 2019 Coverdale translation is the primary requirement. Other translations are supplementary.

**Independent Test**: Can be tested by switching translation options and verifying psalm text updates to the selected translation.

**Acceptance Scenarios**:

1. **Given** a user views a psalm in Coverdale translation, **When** they select "ESV", **Then** the same psalm displays in the English Standard Version
2. **Given** a user views a psalm in one translation, **When** they navigate to a different psalm, **Then** the new psalm displays in the same translation
3. **Given** a user changes translation, **When** they return later, **Then** their translation preference is remembered

---

### User Story 6 - Manage Psalm Topics (Admin) (Priority: P2)

An administrator wants to create, edit, and organize thematic psalm topics to help users discover psalms by subject matter.

**Why this priority**: Topic management enables content curation without code deployments. Secondary to core user-facing psalm viewing features.

**Independent Test**: Can be tested by accessing Django admin, creating a new topic, assigning psalms, and verifying it appears in the frontend topic filter.

**Acceptance Scenarios**:

1. **Given** an administrator accesses Django admin, **When** they create a new topic "Lament and Sorrow" with psalms 6, 13, 22, **Then** the topic appears in the frontend topic list
2. **Given** an administrator edits a topic, **When** they reorder topics using drag-and-drop, **Then** the frontend displays topics in the new order
3. **Given** an administrator needs to correct a typo, **When** they edit a psalm verse in the admin interface, **Then** the corrected text displays immediately to users
4. **Given** an administrator wants to review all verses containing "Lord", **When** they apply the "Verses with Lord" filter, **Then** only matching verses appear for bulk editing

---

### Edge Cases

- What happens when a user requests a psalm number outside the range of 1-150?
- How does the system handle partial psalm ranges (e.g., Psalm 119:1-8 when verse breaks don't align)?
- What occurs when viewing very long psalms like Psalm 119 (176 verses)?
- How does the system display psalm titles that include musical directions (e.g., "To the Chief Musician")?
- What happens when a psalm range spans from the middle of one psalm to the middle of another?
- How does the system handle psalms with textual variations between translations?
- What occurs when displaying psalms that include selah marks or other Hebrew musical notations?

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST store all 150 psalms from the Psalter in the Book of Common Prayer 2019 Coverdale translation in a database
- **FR-002**: System MUST allow users to view any individual psalm by selecting its number (1-150)
- **FR-003**: System MUST display each psalm with proper verse numbering
- **FR-004**: System MUST format psalm verses with proper indentation to reflect Hebrew parallelism
- **FR-005**: System MUST display Latin titles for psalms where they are included in BCP 2019 (e.g., "Deus, Deus meus" for Psalm 22)
- **FR-006**: System MUST allow users to view consecutive psalm ranges (e.g., Psalms 1-3 or Psalms 120-134)
- **FR-007**: System MUST allow users to view partial psalms by verse range (e.g., Psalm 119:1-32)
- **FR-008**: System MUST provide navigation between consecutive psalms (next/previous)
- **FR-009**: System MUST preserve the exact Coverdale translation text as it appears in BCP 2019
- **FR-010**: System MUST display the complete text of the psalm including any superscriptions or musical directions
- **FR-011**: System MUST provide thematic categories to help users find psalms by topic (praise, thanksgiving, morning, evening, comfort, etc.)
- **FR-012**: System MUST support both Contemporary and Traditional Language Edition (TLE) versions of the Coverdale Psalter from BCP 2019, where Contemporary uses modern pronouns (you/your) and Traditional uses traditional pronouns (thou/thee)
- **FR-013**: System MUST allow users to switch between Contemporary and Traditional Language Edition psalm texts
- **FR-014**: System MUST always display pointing marks (asterisk \*) between the first and second half of each verse to indicate the pause point for Anglican chanting
- **FR-015**: System MUST remember user preferences for language edition (Contemporary vs Traditional) across sessions
- **FR-016**: System MUST provide an admin interface for managing psalm topics, including creating, editing, and deleting topic categories
- **FR-017**: System MUST allow administrators to assign psalms to topics and reorder topics for display priority
- **FR-018**: System MUST provide an admin interface for editing psalm verse text (Contemporary and Traditional editions) to correct any transcription errors
- **FR-019**: System MUST allow administrators to filter psalm verses by those containing specific words (e.g., "Lord") for bulk review and editing

### Key Entities

- **Psalm**: One of the 150 psalms from the Book of Psalms with its complete text, verses, title, and metadata
- **Psalm Verse**: A single numbered verse within a psalm with first and second half-lines for parallelism
- **Psalm Translation**: A specific version of the Coverdale Psalter (Contemporary or Traditional Language Edition/TLE), distinguished by pronoun usage (you/your vs. thou/thee)
- **Psalm Range**: A specification of multiple consecutive psalms or verses to be displayed together (e.g., "1-3" or "119:1-32")
- **Psalm Topic**: A thematic category grouping psalms by subject matter (praise, thanksgiving, morning, evening, penitence, etc.); managed through Django admin interface
- **Pointing**: Musical/chant marks (asterisk \*) that indicate the pause point between the first and second half of each verse for singing psalms in Anglican chant; always displayed
- **Latin Title**: Traditional Latin designation for some psalms (e.g., "Deus, Deus meus")
- **Admin Interface**: Django admin panel for managing psalm topics and editing psalm verse text for corrections

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Users can view any individual psalm (1-150) with complete text in the Coverdale translation loading in under 2 seconds
- **SC-002**: System displays psalm text exactly matching the printed Book of Common Prayer 2019 Psalter
- **SC-003**: Users can navigate between consecutive psalms with immediate display of the next or previous psalm
- **SC-004**: Users can view psalm ranges specified in the Daily Office lectionary (e.g., Psalms 148-150) with all psalms displaying correctly
- **SC-005**: 90% of users can find an appropriate psalm for a specific need (comfort, praise, morning prayer) using topic categories within 1 minute
- **SC-006**: Users can switch between Contemporary and Traditional Language Edition with text updating in under 1 second
- **SC-007**: Pointing marks (asterisks) display correctly between the first and second half of every verse for Anglican chanting
- **SC-008**: Language edition preference (Contemporary vs Traditional) persists across user sessions
- **SC-009**: Administrators can create a new psalm topic, assign 5 psalms, and reorder topics within 2 minutes using the admin interface
- **SC-010**: Administrators can correct a psalm verse text error and see the change reflected in the frontend immediately (within 10 seconds with cache clearing)

## Clarifications

### Session 2025-11-06

- Q: What are the two Coverdale versions called? → A: Both are Coverdale from BCP 2019; "Contemporary" uses modern pronouns (you/your), "Traditional" uses traditional pronouns (thou/thee) - This is the Traditional Language Edition (TLE)
- Q: Pointing marks display behavior? → A: Always display - pointing marks are always visible and cannot be hidden
- Q: How are the 150 psalms stored and accessed? → A: Psalms are stored in a database
- Q: Should leader/congregation styling be specified? → A: Not in scope - this is an implementation detail that doesn't need specification
- Q: How are psalm topic categories created and maintained? → A: Topics are managed through Django admin interface, allowing authorized administrators to create, edit, reorder, and assign psalms to topics without code deployment
- Q: Can administrators edit psalm text? → A: Yes, the admin interface allows editing of both Contemporary and Traditional edition verse text to correct transcription errors or update translations

## Assumptions

- The primary psalm text is the Coverdale translation from the Book of Common Prayer 2019
- Psalms are stored in a database for fast, reliable access without dependency on external APIs
- Users are primarily accessing psalms for personal devotion, Daily Office prayer, or liturgical planning
- Many users are familiar with psalm numbering and can navigate by psalm number
- Some users need thematic access when they don't know specific psalm numbers
- Psalm topic categories are curated by administrators through the admin interface, allowing flexibility to add new topics without code deployments
- Only authorized administrators have access to the Django admin interface for managing topics and editing psalm text
- Anglican psalm pointing conventions are understood by users (pointing marks always displayed)
- Users may want to compare traditional pronouns (thou/thee) with contemporary pronouns (you/your)
- Internet connectivity is available for accessing the application
- Psalm formatting (verse structure, parallelism) is important for proper reading and chanting
- The Coverdale translation's distinctive language (e.g., "therefore can I lack nothing" vs. "I shall not want") is valued by BCP 2019 users
- Transcription errors may exist in psalm text and need to be correctable without database migrations
