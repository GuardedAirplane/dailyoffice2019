# Feature Specification: Liturgical Calendar

**Feature Branch**: `002-liturgical-calendar`  
**Created**: November 6, 2025  
**Status**: Draft  
**Input**: User description: "Liturgical Calendar: A Calendar showing the liturgical significance of each day of the year"

## Clarifications

### Session 2025-11-06

- Q: When filtering is OFF (Show Major Feasts Only), which commemorations should be displayed vs. hidden? → A: When filtering OFF, show only required commemorations (rank.required=True); all other dates show season color only
- Q: How does the system handle calendar year requests that span two liturgical church years (which begin at Advent)? → A: Calendar supports any calendar year by combining two overlapping church years (Advent-based); cache separately
- Q: When and how is the liturgical color blue used in the BCP 2019 calendar? → A: Blue is an alternate color option for Advent season only (traditional purple is primary); churches may choose
- Q: What are the rules for transferring feasts when multiple required commemorations fall on the same date? → A: When 2+ required commemorations conflict, keep highest precedence; transfer lower-ranked to next day (unless Sunday/privileged season)
- Q: How does the system handle First Vespers (Evening Prayer on the eve of major feasts)? → A: Major feasts (precedence ≤4, non-privileged) have First Vespers on evening before; previous day shows "Eve of [Feast]"

## User Scenarios & Testing _(mandatory)_

### User Story 1 - View Current Month Calendar (Priority: P1)

A user wants to view a calendar for the current month showing which days are feast days, holy days, or commemorations, color-coded by liturgical season and feast rank.

**Why this priority**: Viewing the current month is the primary use case and provides immediate value for understanding today's and this week's liturgical context.

**Independent Test**: Can be fully tested by displaying the current month's calendar and verifying each date shows correct feast names, liturgical colors, and season designations according to BCP 2019 calendar.

**Acceptance Scenarios**:

1. **Given** a user views the current month, **When** the calendar loads, **Then** all dates display with appropriate liturgical colors (red, white, green, purple, etc.) based on the season or feast
2. **Given** a user views the calendar, **When** they see a feast day, **Then** the feast name appears on that date with the correct liturgical color
3. **Given** a user views a regular weekday, **When** no special commemoration occurs, **Then** the date displays in the color of the current liturgical season

---

### User Story 2 - Navigate to Different Months (Priority: P1)

A user wants to navigate forward and backward to view liturgical calendars for past and future months to plan ahead or review previous commemorations.

**Why this priority**: Month navigation is essential for the calendar to be useful beyond just the current month. Users need to see upcoming feasts and prepare for future celebrations.

**Independent Test**: Can be tested independently by navigating to previous and next months and verifying all dates display correct liturgical information for those months.

**Acceptance Scenarios**:

1. **Given** a user views the current month, **When** they select "next month", **Then** the calendar displays the following month with all feast days and colors correctly shown
2. **Given** a user views any month, **When** they select "previous month", **Then** the calendar displays the prior month with accurate liturgical information
3. **Given** a user navigates across months, **When** they cross from one liturgical season to another, **Then** the calendar colors update to reflect the new season

---

### User Story 3 - Click Date to View Daily Office (Priority: P2)

A user wants to click on any date in the calendar to navigate directly to the Daily Office for that date, providing quick access to prayers and readings.

**Why this priority**: This integration enhances user workflow but requires the Daily Office feature to exist first. The calendar provides value independently.

**Independent Test**: Can be tested by clicking any date and verifying navigation to the Daily Office page for that specific date with the correct liturgical content.

**Acceptance Scenarios**:

1. **Given** a user views the calendar, **When** they click on any date, **Then** they navigate to the Daily Office view for that selected date
2. **Given** a user clicks on a feast day, **When** they view the Daily Office, **Then** the proper readings and collects for that feast are displayed
3. **Given** a user clicks on a regular weekday, **When** they view the Daily Office, **Then** the standard daily readings for that date are shown

---

### User Story 4 - Filter Calendar Display (Priority: P3)

A user wants to filter the calendar to show only major feasts and hide minor commemorations for a cleaner view focused on principal holy days.

**Why this priority**: Filtering improves usability for some users but is not essential for basic calendar functionality. All feasts should display by default.

**Independent Test**: Can be tested by toggling filter options and verifying the calendar display updates to show or hide minor feasts based on user selection.

**Acceptance Scenarios**:

1. **Given** a user views the full calendar with all commemorations, **When** they select "Show Major Feasts Only", **Then** minor commemorations are hidden and only principal feasts and holy days remain visible
2. **Given** a user has filtering enabled, **When** they select "Show All Feasts", **Then** all commemorations reappear including minor feasts and saints' days
3. **Given** a user applies a filter, **When** they navigate to different months, **Then** the filter setting persists across all months

---

### User Story 5 - View Feast Day Details (Priority: P3)

A user wants to see additional information about a feast day, saint, or commemoration when viewing it on the calendar, such as a brief description or biography.

**Why this priority**: Detailed information enhances the educational value but is not necessary for basic calendar viewing and liturgical planning.

**Independent Test**: Can be tested by selecting a commemoration and verifying additional details appear, such as description, biography, or historical context.

**Acceptance Scenarios**:

1. **Given** a user views a saint's feast day, **When** they hover over or click the feast name, **Then** a brief description or biography of the saint appears
2. **Given** a user views a major feast, **When** they access feast details, **Then** information about the feast's significance and traditions appears
3. **Given** a user views multiple commemorations on one day, **When** they review the day's details, **Then** all commemorations for that day are listed with their descriptions

---

### Edge Cases

- What happens when multiple feasts occur on the same day (e.g., a major feast and a saint's day)? **Resolved**: System applies precedence rules; highest-ranked commemoration is observed on the original date, lower-ranked commemorations are transferred to the next available day (see FR-009)
- How does the system display transferred feasts (when a feast is moved due to Sunday or another major feast)? **Resolved**: Transferred feasts appear on their observed date with their original rank and are marked as transferred
- What occurs when viewing February in a leap year vs. non-leap year?
- How does the calendar handle the transition from one church year to the next (Advent marks the beginning)?
- What happens when a moveable feast (like Easter) falls on different dates in different years?
- How does the system display feasts with variable dates (e.g., Ascension Day, always 40 days after Easter)?
- What occurs when viewing dates outside the range of available calendar data?

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST display a monthly calendar view showing all dates with liturgical significance
- **FR-002**: System MUST color-code each calendar date based on the liturgical season or feast day color (red, white, green, purple, rose, black). Blue (Sarum blue) is available as an alternate color for Advent season, with traditional purple as the primary color
- **FR-003**: System MUST display feast names, holy days, and commemorations on the appropriate dates
- **FR-004**: System MUST follow the Book of Common Prayer 2019 liturgical calendar including all Principal Feasts, Sundays, Holy Days, and commemorations
- **FR-005**: System MUST calculate moveable feasts correctly (Easter-dependent dates like Ascension, Pentecost, Trinity Sunday)
- **FR-006**: System MUST allow users to navigate between months (previous/next navigation)
- **FR-007**: System MUST allow users to jump to the current month with a single action
- **FR-008**: System MUST handle feast day precedence correctly when multiple commemorations fall on the same date
- **FR-009**: System MUST display transferred feasts on their observed date, not just their nominal date. When multiple required commemorations fall on the same date, the system keeps the commemoration with the highest precedence rank and transfers lower-ranked commemorations to the next available day. Sundays and commemorations during privileged seasons (Advent, Lent, Holy Week, Eastertide) are never displaced. Transferred commemorations retain their rank but are marked as transferred
- **FR-010**: System MUST show the liturgical season for any given date (Advent, Christmas, Epiphany, Lent, Easter, Pentecost/Ordinary Time)
- **FR-011**: System MUST allow users to click on any date to navigate to related content (Daily Office for that date)
- **FR-012**: System MUST support filtering to show only major feasts and hide minor commemorations. When filtering is OFF (Show Major Feasts Only), the system displays only commemorations with rank.required=True; all other dates display the liturgical season color without feast text. When filtering is ON (Show All Feasts), the system displays all commemorations including optional ones (rank.required=False)
- **FR-013**: System MUST correctly handle leap years (February 29) and its liturgical assignment
- **FR-014**: System MUST display Sundays with their proper liturgical designation (e.g., "2nd Sunday of Advent", "Easter Day")
- **FR-015**: System MUST indicate when multiple commemorations occur on the same day and show the order of precedence
- **FR-016**: System MUST support First Vespers (Evening Prayer) for major feasts with precedence rank ≤4 that are not during privileged observances. The evening before such a feast is designated "Eve of [Feast Name]" and uses the liturgical season and color of the upcoming feast. Evening Prayer collects may differ from Morning Prayer collects for the same commemoration

### Key Entities

- **Calendar Day**: A specific date with its liturgical season, color, and any associated commemorations. Each day may have separate morning and evening commemorations, particularly when a major feast has First Vespers (evening before the feast)
- **Liturgical Season**: One of the major seasons of the church year (Advent, Christmas, Epiphany, Lent, Easter, Pentecost/Ordinary Time) with associated colors and characteristics
- **Commemoration**: A feast, holy day, saint's day, or other liturgical observance occurring on a specific date with an assigned rank
- **Commemoration Rank**: The level of importance of a feast or commemoration (Principal Feast, Sunday, Holy Day, Feast, Major Holy Day, etc.)
- **Liturgical Color**: The color associated with a season or feast (red, white, green, purple, rose, black, and optionally blue for Advent) used for vestments and altar hangings. Each commemoration or season may have a primary color and one or more alternate colors
- **Moveable Feast**: A feast or holy day whose date changes each year based on the date of Easter (e.g., Ascension Day, Pentecost)
- **Church Year**: The annual cycle of liturgical seasons beginning with Advent and ending the day before the next Advent. Identified by the calendar year in which Advent begins (e.g., "Church Year 2024" runs from Advent 2024 through November 2025)
- **Calendar Year**: A standard January-December year that spans portions of two Church Years. The system constructs Calendar Year data by combining the relevant portions of two consecutive Church Years

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Users can view any month's liturgical calendar with all feast days correctly displayed and color-coded in under 2 seconds
- **SC-002**: System accurately calculates and displays all moveable feasts for any year within the supported date range
- **SC-003**: Calendar correctly displays liturgical colors matching the Book of Common Prayer 2019 for 100% of dates
- **SC-004**: Users can navigate from any calendar date to the corresponding Daily Office in a single click
- **SC-005**: 90% of users can identify upcoming major feasts within the next two weeks by viewing the calendar
- **SC-006**: System correctly handles feast day precedence for all dates, matching the precedence rules in BCP 2019
- **SC-007**: Users can toggle between full calendar (all commemorations) and filtered calendar (major feasts only) with immediate visual update
- **SC-008**: Calendar supports viewing dates from at least 2 years past to 5 years future. The system generates calendar year data by combining two overlapping church years (Advent-based) and caches each church year separately for performance

## Assumptions

- Users understand basic liturgical terminology such as "feast day", "commemoration", and liturgical seasons
- The liturgical calendar follows the Anglican Church in North America (ACNA) Book of Common Prayer 2019 calendar
- Users primarily view the calendar on the web or mobile devices with varying screen sizes
- Liturgical color conventions (red, white, green, purple, etc.) are familiar to users from their worship experience
- Internet connectivity is available for loading calendar data
- The calendar should emphasize visual clarity with color coding to make feast days immediately recognizable
- Users may want to plan ahead for major feasts and holy days
- Calendar data includes all necessary commemoration information, ranks, and precedence rules
