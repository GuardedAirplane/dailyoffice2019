# Daily Office 2019 - Feature Specifications Summary

**Created**: November 6, 2025  
**Purpose**: Retroactive documentation of major feature categories

This document provides an overview of the six major feature specifications created for the Daily Office 2019 application based on analysis of the existing codebase.

## Overview

The Daily Office 2019 application is a comprehensive liturgical prayer resource based on the Anglican Church in North America's Book of Common Prayer 2019. It provides web and mobile access to daily prayer offices, liturgical calendar, scripture readings, psalms, and collects.

## Feature Specifications

### 001 - Daily Office Liturgy

**Branch**: `001-daily-office`  
**Spec**: [specs/001-daily-office/spec.md](specs/001-daily-office/spec.md)

Core liturgical functionality supporting four daily prayer offices:

- Morning Prayer (P1 priority)
- Evening Prayer (P1 priority)
- Midday Prayer (P2 priority)
- Compline/Night Prayer (P2 priority)

Each office includes complete liturgical content: opening sentences, confession, psalms, scripture readings, canticles, creeds, prayers, and closing. Follows BCP 2019 exactly with proper feast day variations.

**Key Success Criteria**:

- Display complete offices in under 3 seconds
- 95% of users pray without external resources
- Accurate feast day readings for all BCP 2019 holy days
- Support dates 2 years past to 2 years future

---

### 002 - Liturgical Calendar

**Branch**: `002-liturgical-calendar`  
**Spec**: [specs/002-liturgical-calendar/spec.md](specs/002-liturgical-calendar/spec.md)

Visual calendar showing liturgical significance of each day:

- Color-coded by season and feast day (P1 priority)
- Month navigation (P1 priority)
- Click-through to Daily Office (P2 priority)
- Filtering by feast importance (P3 priority)

Displays all commemorations, feast days, and holy days from the BCP 2019 calendar with proper liturgical colors (red, white, green, purple, blue, rose, black).

**Key Success Criteria**:

- Load any month in under 2 seconds
- 100% accurate liturgical colors matching BCP 2019
- Correct moveable feast calculations for any year
- Navigate to Daily Office in one click

---

### 003 - Collects and Prayers

**Branch**: `003-collects`  
**Spec**: [specs/003-collects/spec.md](specs/003-collects/spec.md)

Complete collection of prayers from BCP 2019:

- Browse all collects by category (P1 priority)
- Filter by category (P1 priority)
- Search by text (P2 priority)
- Traditional/contemporary language toggle (P2 priority)

Includes collects for the church year, holy days, various occasions, and pastoral offices. Both traditional (thee/thou) and contemporary (you/your) language versions.

**Key Success Criteria**:

- Browse all collects in under 5 seconds
- Switch languages in under 1 second
- 90% of users find needed collect within 30 seconds
- Exact text matching printed BCP 2019

---

### 004 - Psalter

**Branch**: `004-psalter`  
**Spec**: [specs/004-psalter/spec.md](specs/004-psalter/spec.md)

Complete Psalter from BCP 2019:

- View individual psalms (P1 priority)
- Navigate by number 1-150 (P1 priority)
- View psalm ranges (P2 priority)
- Search by topic/theme (P2 priority)

Primary text is the Coverdale translation from BCP 2019, with optional additional translations (ESV, NRSV). Includes Latin titles and optional pointing marks for chanting.

**Key Success Criteria**:

- Load any psalm in under 2 seconds
- Exact Coverdale translation matching BCP 2019
- Support psalm ranges for lectionary integration
- 90% of users find topical psalms within 1 minute

---

### 005 - Lectionary

**Branch**: `005-lectionary`  
**Spec**: [specs/005-lectionary/spec.md](specs/005-lectionary/spec.md)

Scripture reading assignments and full text:

- Today's reading assignments (P1 priority)
- Full scripture text display (P1 priority)
- Bible translation selection (P2 priority)
- Any date access (P2 priority)

Follows BCP 2019 two-year Daily Office Lectionary with psalm and scripture assignments for Morning Prayer, Evening Prayer, and Holy Eucharist. Multiple Bible translations supported.

**Key Success Criteria**:

- Display today's readings in under 2 seconds
- Full scripture text in under 3 seconds
- 95% of users read daily scripture without external resources
- Correct feast day proper readings
- Support dates 2 years past to 2 years future

---

### 006 - Cross-Platform Access and Settings

**Branch**: `006-general-design`  
**Spec**: [specs/006-general-design/spec.md](specs/006-general-design/spec.md)

Multi-platform support and customization:

- Web browser access (P1 priority)
- Mobile device access (P1 priority)
- Customizable settings (P2 priority)
- Settings sharing (P3 priority)

Responsive design across desktop, tablet, and mobile. Native iOS and Android apps. Extensive customization: font size, language style, translations, optional elements. Shareable settings links for coordinated group use.

**Key Success Criteria**:

- Work in all major browsers
- Mobile touch interactions smooth and responsive
- Load in under 3 seconds for 95% of users
- Settings persist without accounts
- WCAG 2.1 Level AA accessibility compliance
- Settings sharing works across platforms

---

## Feature Dependencies

```
006 General Design (Platform/Foundation)
    └── Supports all other features across web/mobile

001 Daily Office
    ├── Requires: 002 Calendar (for feast days)
    ├── Requires: 004 Psalter (for psalm assignments)
    ├── Requires: 005 Lectionary (for readings)
    └── Requires: 003 Collects (for prayers)

002 Liturgical Calendar
    └── Links to: 001 Daily Office (click-through)

003 Collects
    └── Used by: 001 Daily Office

004 Psalter
    └── Used by: 001 Daily Office and 005 Lectionary

005 Lectionary
    └── Integrates with: 001 Daily Office
```

## Development Approach

All specifications are written to be:

- **Technology-agnostic**: Focus on WHAT users need, not HOW to implement
- **Testable**: Every requirement has clear acceptance criteria
- **Prioritized**: P1 features provide MVP, P2 enhance value, P3 complete experience
- **Independently implementable**: Each user story can be developed and tested alone

## Quality Validation

All specifications have passed quality checklists verifying:

- ✅ No implementation details
- ✅ User-focused value proposition
- ✅ Non-technical stakeholder language
- ✅ Testable requirements
- ✅ Measurable success criteria
- ✅ Edge cases identified
- ✅ Clear scope boundaries

## Next Steps

Each specification is now ready for:

1. `/speckit.clarify` - Further refinement if needed
2. `/speckit.plan` - Technical planning and implementation design
3. Implementation - Development following the specification

## Notes

These specifications document existing functionality that has been implemented in the Daily Office 2019 application. They serve as authoritative reference for understanding feature scope, user needs, and acceptance criteria for ongoing development and maintenance.

The specifications align with the actual implementation found in:

- Backend: Django app in `/site/` directory
- Frontend: Vue.js app in `/app/` directory
- Mobile: Capacitor iOS/Android apps

For technical implementation details, see:

- [Project README](../README.md)
- [Developer Instructions](../.github/copilot-instructions.md)
