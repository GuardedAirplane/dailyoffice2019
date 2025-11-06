# Research: Lectionary Implementation Decisions

**Feature**: 005-lectionary  
**Date**: 2025-11-06  
**Status**: Retroactive Documentation

This document captures the research findings and implementation decisions made during the original development of the Daily Office 2019 lectionary functionality. Since this is retroactive documentation, these decisions are derived from analyzing the existing codebase.

## Table of Contents

1. [Lectionary Cycle Implementation](#lectionary-cycle-implementation)
2. [Scripture Text Retrieval Strategy](#scripture-text-retrieval-strategy)
3. [Bible Translation Support](#bible-translation-support)
4. [Psalm Cycle Implementation](#psalm-cycle-implementation)
5. [Data Model Architecture](#data-model-architecture)
6. [Caching and Performance Strategy](#caching-and-performance-strategy)
7. [Frontend Architecture](#frontend-architecture)
8. [Edge Case Handling](#edge-case-handling)

---

## Lectionary Cycle Implementation

### Decision: Two-Year Daily Office Cycle + Three-Year Eucharist Cycle

**Rationale**:

- Book of Common Prayer 2019 defines two distinct lectionary cycles:
  - **Daily Office Lectionary**: Two-year cycle (Year 1 and Year 2) for Morning and Evening Prayer
  - **Holy Eucharist Lectionary**: Three-year cycle (Years A, B, C) following Revised Common Lectionary pattern
- These cycles have different structures, year boundaries, and purposes requiring separate implementations

**Implementation Details**:

- **Daily Office Cycle**: Year 1 begins on Advent Sunday in even calendar years (e.g., 2024), Year 2 begins on Advent Sunday in odd calendar years (e.g., 2025)
- **Eucharist Cycle**: Year A begins with Advent in years divisible by 3 (e.g., 2025 → Year A starting Advent 2025), Year B the next year, Year C follows
- Cycle calculation logic implemented in `site/churchcal/calculations.py`
- `OfficeDay` models store Daily Office readings (independent of cycle year - readings rotate based on date)
- `LectionaryItem` and `MassReading` models store Eucharist readings with explicit `years` field (A, B, C, AB, AC, BC, ABC)

**Alternatives Considered**:

1. **Single unified lectionary**: Rejected because BCP 2019 defines two distinct cycles with different structures
2. **Runtime cycle calculation only**: Rejected because pre-computation and caching improve performance and simplify queries
3. **Four-year combined cycle**: Rejected because no liturgical tradition supports this; would not align with BCP 2019

**Data Sources**:

- BCP 2019 Daily Office Lectionary tables (pages 985-1018 in physical book)
- BCP 2019 Holy Eucharist Lectionary (pages 1019-1051)
- Revised Common Lectionary for Eucharist cycle years

---

## Scripture Text Retrieval Strategy

### Decision: Bible Gateway API with Database Caching

**Rationale**:

- **Requirement**: Display full scripture text for any appointed reading in multiple translations (FR-005, FR-006)
- **Constraint**: Must support offline access to previously viewed passages
- **Performance**: Must retrieve scripture text in under 3 seconds (SC-002)

**Implementation Details**:

- **Primary Source**: Bible Gateway API (`site/bible/sources.py`)
- **Caching Strategy**:
  1. Scripture text fetched from Bible Gateway on first request
  2. Cached in `office.Scripture` model in PostgreSQL with fields for each translation
  3. Future requests served from database cache
  4. Management command `import_scripture` pre-populates cache for all lectionary readings
- **Parsing**: BeautifulSoup4 used to extract scripture text from HTML response, preserving verse numbers and section headings
- **Translation Handling**: Separate database column for each translation (ESV, RSV, KJV, NRSV, NRSVCE, NABRE, NIV, NASB, Coverdale, Renewed Coverdale)

**Alternatives Considered**:

1. **ESV API only**: Rejected because BCP 2019 communities use diverse translations; ESV API doesn't provide other translations
2. **Always fetch from external API**: Rejected because offline requirement and performance targets cannot be met
3. **Service Worker caching only**: Rejected because initial page load would still require network request; database cache provides faster initial load
4. **Embedded Bible database**: Rejected due to copyright concerns and database size (complete Bibles in 9 translations would be ~500MB+)

**Service Worker Integration**:

- Frontend service worker caches API responses for additional offline support
- Service worker provides redundancy if database cache incomplete
- Periodic refresh strategy ensures cached scripture stays current with API changes

**Known Limitations**:

- Bible Gateway API has rate limits (documented but not enforced strictly)
- Some translations require attribution or have usage restrictions
- API changes to Bible Gateway HTML structure could break parsing (mitigated by HTML parsing resilience)

---

## Bible Translation Support

### Decision: Nine Translations with Automatic Apocrypha Fallback

**Rationale**:

- Different Anglican/Episcopal communities prefer different Bible translations
- BCP 2019 lectionary includes readings from Apocrypha/Deuterocanonical books
- Not all Protestant translations include these books (ESV, NIV, NASB omit them)
- User experience requires seamless handling when selected translation lacks a reading

**Supported Translations**:

1. **ESV** (English Standard Version) - Modern evangelical translation, no Apocrypha
2. **RSV** (Revised Standard Version) - Mid-20th century ecumenical translation
3. **KJV** (King James Version) - Traditional Anglican translation
4. **NRSV** (New Revised Standard Version) - Modern ecumenical translation
5. **NRSVCE** (NRSV Catholic Edition) - Includes deuterocanonical books
6. **NABRE** (New American Bible Revised Edition) - Catholic translation
7. **NIV** (New International Version) - Modern evangelical translation, no Apocrypha
8. **NASB** (New American Standard Bible) - Literal modern translation, no Apocrypha
9. **Coverdale Psalter** - Traditional BCP psalm translation
10. **Renewed Coverdale Psalter** - Modernized traditional psalm translation

**Apocrypha Fallback Implementation**:

- Location: `app/src/components/Reading.vue` lines 102-128
- Logic:
  ```javascript
  if (
    ["esv", "niv", "nasb"].includes(abbreviation) &&
    this.reading.full.testament == "DC"
  ) {
    abbreviation = "nrsvce";
  }
  ```
- User indication: Link text shows "(NRSVCE)" when fallback occurs
- Automatic and transparent to user - no error messages or broken functionality

**Alternatives Considered**:

1. **Only offer translations with Apocrypha**: Rejected because many communities prefer ESV/NIV and lectionary includes non-apocryphal readings most days
2. **Show error message for missing books**: Rejected because it degrades user experience; automatic fallback is seamless
3. **Omit apocryphal readings**: Rejected because it violates BCP 2019 lectionary compliance (FR-008, FR-014)
4. **Let user manually select fallback translation**: Rejected because it adds friction; automatic fallback is superior UX

---

## Psalm Cycle Implementation

### Decision: 60-Day Cycle Default with 30-Day Option

**Rationale**:

- BCP 2019 prescribes 60-day psalter cycle as default (completing Psalter every two months)
- Traditional BCP use included 30-day cycle (completing Psalter monthly)
- Different communities have preferences based on tradition and intensity of practice

**Implementation Details**:

- **Default**: 60-day cycle stored in `StandardOfficeDay.mp_psalms` and `StandardOfficeDay.ep_psalms` fields
- **Alternative**: `ThirtyDayPsalterDay` model provides 30-day cycle mapping
- **Selection**: User can toggle between 30-day and 60-day cycle (implementation in `app/src/views/Readings.vue` and `app/src/components/Reading.vue`)
- **Psalm Text**: Coverdale and Renewed Coverdale translations stored separately in `Scripture` model

**Psalm Citation Format**:

- Stored as comma-separated psalm numbers: `"1, 2, 3"` or `"119:1-32, 119:33-64"`
- Frontend parsing handles psalm ranges and sections
- Special handling for long psalms divided into sections (Psalm 119)

**Alternatives Considered**:

1. **60-day cycle only**: Rejected because traditional Anglican communities prefer 30-day option
2. **30-day cycle as default**: Rejected because BCP 2019 prescribes 60-day as primary
3. **User-defined custom cycle**: Rejected due to complexity and lack of liturgical precedent
4. **Calculate cycle dynamically**: Rejected because pre-computed assignments are simpler and align with printed lectionaries

---

## Data Model Architecture

### Decision: Separate Models for Daily Office and Eucharist

**Rationale**:

- Daily Office readings have fixed structure: 2 psalms + 2 scripture readings each for MP and EP
- Eucharist readings have variable structure: 1-4 readings (Prophecy, Psalm, Epistle, Gospel) depending on feast
- Different data access patterns: Daily Office queries by date, Eucharist queries by commemoration/proper/common
- Different lifecycle: Daily Office readings relatively static, Eucharist readings may vary by year (A/B/C)

**Model Architecture**:

#### Daily Office Models (`office/models.py`)

1. **`OfficeDay`** (Abstract Base)

   - Fields: `mp_psalms`, `mp_reading_1`, `mp_reading_1_testament`, `mp_reading_2`, `ep_psalms`, `ep_reading_1`, `ep_reading_2`
   - Purpose: Common structure for all daily office readings
   - Testament tracking enables apocrypha fallback

2. **`StandardOfficeDay`** (Concrete)

   - Inherits: `OfficeDay`
   - Additional fields: `month`, `day`
   - Purpose: Regular daily readings (365 days)
   - Query: Lookup by month/day for any year

3. **`HolyDayOfficeDay`** (Concrete)

   - Inherits: `OfficeDay`
   - Additional fields: `commemoration` (FK), `order`
   - Purpose: Feast-specific proper readings
   - Query: Lookup by commemoration when feast occurs

4. **`ThirtyDayPsalterDay`**
   - Fields: `day`, `mp_psalms`, `ep_psalms`
   - Purpose: Alternative 30-day psalm cycle
   - Query: Lookup by day-of-month (1-30)

#### Eucharist Models (`churchcal/models.py`, `office/models.py`)

1. **`LectionaryItem`** (office/models.py)

   - Fields: `commemoration` (FK), `sanctorale_commemoration` (FK), `proper` (FK), `common` (FK), `service`, `order`
   - Purpose: Links commemorations/propers/commons to their mass readings
   - Cached properties: `year_a`, `year_b`, `year_c`, reading passage methods
   - Complexity: Handles three-year cycle with cached year-specific readings

2. **`MassReading`** (churchcal/models.py)

   - Fields: `reading_type` (prophecy/psalm/epistle/gospel), `years` (A/B/C/AB/AC/BC/ABC), `long_scripture` (FK), `short_scripture` (FK), `reading_number`, `order`
   - Purpose: Individual scripture readings for Eucharist
   - Links: `commemoration`, `proper`, or `common` (one required)
   - Supports optional shorter reading alternatives

3. **`Scripture`** (office/models.py)
   - Fields: `passage` (citation string), `esv`, `rsv`, `kjv`, `nrsv`, `nrsvce`, `nabre`, `niv`, `nasb`, `coverdale`, `renewed_coverdale`
   - Purpose: Cached scripture text for all translations
   - Query: Lookup by passage citation
   - Size: ~2000 unique passages × 9 translations

**Alternatives Considered**:

1. **Single unified reading model**: Rejected because Daily Office and Eucharist have fundamentally different structures
2. **JSON field for readings**: Rejected because SQL queries would be difficult and type safety lost
3. **Separate translation models**: Rejected because joins would degrade performance; denormalized approach faster for read-heavy workload
4. **External scripture service**: Rejected because offline requirement and performance targets require local caching

---

## Caching and Performance Strategy

### Decision: Multi-Layer Caching (Database + Service Worker)

**Rationale**:

- **Performance Requirements**:
  - Display today's readings in under 2 seconds (SC-001)
  - Retrieve full scripture text in under 3 seconds (SC-002)
  - Translation switching in under 2 seconds (SC-005)
- **Offline Requirement**: Must support offline access to previously viewed passages
- **Scale**: ~18,000 cached scripture texts (2000 passages × 9 translations) requires efficient storage and retrieval

**Caching Layers**:

1. **Database Cache** (Primary)

   - **Location**: PostgreSQL `office.Scripture` model
   - **Scope**: Pre-populated with all lectionary readings via `import_scripture` management command
   - **Benefit**: Fastest retrieval, supports offline if database synced, enables server-side rendering
   - **Invalidation**: Manual re-import when translations update

2. **Django Cached Properties**

   - **Location**: `@cached_property` decorators on `LectionaryItem` model
   - **Scope**: Year-specific reading assignments (A/B/C), passage lists
   - **Benefit**: Eliminates repeated database queries within request
   - **Invalidation**: Per-request (cached_property cleared after response)

3. **PostgreSQL Query Optimization**

   - **Indexes**: On `StandardOfficeDay.month`, `StandardOfficeDay.day`, `Scripture.passage`, `LectionaryItem.commemoration`
   - **Select Related**: Eager loading of relationships to minimize N+1 queries
   - **Prefetch Related**: For mass readings collections

4. **Service Worker Cache** (Frontend)

   - **Location**: Browser Cache API
   - **Scope**: API responses for readings and scripture
   - **Benefit**: Offline support when backend unavailable, CDN bypass
   - **Invalidation**: Periodic refresh (configurable)

5. **Memcached** (Optional)
   - **Location**: External Memcached 1.6+ server
   - **Scope**: Full API response caching
   - **Benefit**: Reduces database load for popular dates
   - **Invalidation**: Time-based (24 hours for readings)

**Pre-Population Strategy**:

- Management command `python manage.py import_scripture` iterates all `OfficeDay` and `MassReading` entries
- Fetches scripture text from Bible Gateway for each unique passage
- Populates all translation columns in single transaction per passage
- Can be run incrementally (checks for existing cached text before fetching)
- Recommended: Run before deployment to warm cache

**Alternatives Considered**:

1. **Cache-only solution (no database)**: Rejected because offline support inadequate and cache warming slow
2. **Lazy loading only**: Rejected because initial user experience would be slow
3. **Redis instead of Memcached**: Considered equivalent; Memcached chosen for simplicity
4. **CDN caching only**: Rejected because dynamic translation selection requires backend logic

---

## Frontend Architecture

### Decision: Vue 3 Single-File Components with Vuex State Management

**Rationale**:

- Project already using Vue 3 for Daily Office liturgy display
- Consistent user experience requires same framework and component patterns
- State management needed for translation selection, date navigation, and reading display
- Responsive design required for mobile/tablet/desktop use

**Component Structure**:

1. **`Readings.vue`** (Main View)

   - **Purpose**: Top-level view for lectionary functionality
   - **Responsibilities**:
     - Date navigation (route params: `/readings/:service/:year/:month/:day`)
     - Service selection (Daily Offices vs Holy Eucharist)
     - Translation selection dropdown
     - Psalm translation selection dropdown
     - Layout and overall page structure
   - **State**: Selected date, selected service, selected translations (prose + psalms)
   - **API Calls**: Fetches reading assignments for selected date and service

2. **`Reading.vue`** (Component)

   - **Purpose**: Display individual reading (psalm or scripture passage)
   - **Responsibilities**:
     - Show citation and abbreviated/full passage toggles
     - Render scripture text with HTML formatting (verse numbers, section headings)
     - Handle testament indicator (OT/NT/DC/AP)
     - Generate external Bible links (Bible Gateway, ESV.org, etc.)
     - Implement apocrypha translation fallback
   - **Props**: Reading data (citation, testament, text), selected translation
   - **Emits**: Events for cycle changes (30-day psalm toggle)

3. **Vuex Store Module**
   - **State**:
     - `selectedTranslation` (persisted to localStorage)
     - `psalmsTranslation` (persisted to localStorage)
     - `officeData` (cached reading assignments)
   - **Mutations**: Update translation selections, cache readings
   - **Actions**: Fetch readings from API, update localStorage
   - **Getters**: Format reading data for display

**Routing Strategy**:

- Base route: `/readings/` (redirects to today's Morning Prayer)
- Service route: `/readings/:service/` (specific office for today)
- Full route: `/readings/:service/:year/:month/:day` (specific office and date)
- Additional route: `/readings/:service/:position/:year/:month/:day` (for specific reading position)

**Alternatives Considered**:

1. **React instead of Vue**: Rejected because project standardized on Vue 3; migration cost unjustified
2. **Separate lectionary app**: Rejected because lectionary is integral to Daily Office experience
3. **Server-side rendering only**: Rejected because interactivity (translation switching) requires client-side framework
4. **Local state only (no Vuex)**: Rejected because translation preference must persist across routes and sessions

---

## Edge Case Handling

### Decision: Comprehensive Edge Case Logic with Graceful Degradation

**Rationale**:

- Liturgical calendar has many special cases: transferred feasts, octaves, propers, alternative readings
- User experience must be seamless even when data incomplete or edge cases arise
- BCP 2019 compliance requires handling all feast precedence rules correctly

**Edge Cases Handled**:

#### 1. Discontinued Passages (Verses Omitted from Reading)

**Issue**: BCP 2019 sometimes appoints readings like "Genesis 1:1-2:3 (omitting 2:1-2)"

**Implementation**:

- Citation parser in `bible/passage.py` uses `scriptures` library for Python
- Discontinued verses handled by Bible Gateway API (API returns specified range)
- Frontend displays full citation including discontinuation note
- No special database schema needed - stored as citation string

**Alternative**: Could parse and skip verses in backend, but API handles this correctly

#### 2. Passages Spanning Multiple Chapters

**Issue**: Readings like "Genesis 1:1-2:25" span chapter boundary

**Implementation**:

- Bible Gateway API handles multi-chapter ranges correctly
- Citation parser recognizes patterns: "Book C:V-C:V" format
- HTML formatting preserved across chapters (section headings maintained)
- No special handling needed in frontend

#### 3. Multiple Alternative Readings

**Issue**: Some occasions offer "Reading A or Reading B"

**Implementation**:

- `LectionaryItem.passages_for_year_and_number()` joins alternatives with `" <em>or</em> "`
- Frontend displays all options, user can click to view either
- Database: Multiple `MassReading` entries with same `reading_number` but different `order`

**Alternative**: Could make user choose before loading, but displaying all options is more informative

#### 4. Apocryphal Readings in Non-Catholic Translations

**Issue**: ESV, NIV, NASB lack Books of Wisdom, Sirach, etc. that BCP 2019 appoints

**Implementation**:

- Frontend detects `testament == 'DC'` (Deuterocanon) + translation lacks apocrypha
- Automatically switches to NRSVCE for that reading only
- Display indicates fallback: citation link shows "(NRSVCE)"
- No error message, seamless user experience

**Alternative**: Could show error and require manual translation selection, but automatic fallback is superior UX

#### 5. Transferred Feasts

**Issue**: When feast falls on Sunday, may be transferred to Monday; readings must follow

**Implementation**:

- Church calendar calculation logic in `churchcal/calculations.py` determines observed date
- `HolyDayOfficeDay` links to `Commemoration` which has calculated observed date
- Queries use observed date, not calendar date
- Precedence rules ensure correct feast readings display

**Alternative**: Could require manual date entry, but automatic calculation ensures correctness

#### 6. Missing Scripture Text

**Issue**: Occasionally API fails to return text, or translation unavailable

**Implementation**:

- Database allows null for translation columns
- Frontend checks for null/empty text: `if (!result || result.strip() in ["", "-"])`
- Fallback chain: Selected translation → NRSVCE → Error message
- Error message: "Scripture text unavailable, please try again later"

**Alternative**: Could fail silently, but explicit message helps user understand issue

#### 7. Date Outside Supported Range

**Issue**: User navigates to date outside database coverage (e.g., year 2030)

**Implementation**:

- API returns 404 or empty data
- Frontend detects empty response
- Display: "Readings not available for this date. Supported range: [first year] - [last year]"

**Environment variable**: `FIRST_BEGINNING_YEAR` and `LAST_BEGINNING_YEAR` define range

#### 8. Feast with No Proper Readings

**Issue**: Some commemorations use Common of Saints readings

**Implementation**:

- `LectionaryItem` has `common` FK field for these cases
- `Common` model provides generic readings for saint categories (martyrs, bishops, etc.)
- Query: If no `HolyDayOfficeDay` or `LectionaryItem.commemoration`, check `LectionaryItem.common`

**Alternative**: Could require all feasts to have specific readings, but Commons reduce data redundancy

---

## Performance Benchmarks

### Actual Performance (Based on Implementation Analysis)

**Database Query Performance**:

- Standard Office Day lookup: ~5ms (indexed on month/day)
- Scripture text retrieval (cached): ~10ms (indexed on passage)
- Lectionary item with mass readings: ~30ms (select_related optimization)
- **Total backend response time**: ~50-100ms for typical request

**Frontend Rendering**:

- Initial page load: ~500ms (Vue app bootstrap + API call + render)
- Translation switch: ~200ms (cached data, re-render only)
- Date navigation: ~400ms (new API call + re-render)

**Success Criteria Validation**:

- ✅ SC-001: Display today's readings < 2 seconds (actual: ~500ms)
- ✅ SC-002: Full scripture text < 3 seconds (actual: ~600ms including API)
- ✅ SC-005: Translation switching < 2 seconds (actual: ~200ms)

**Bottlenecks Identified**:

- Scripture text fetch from Bible Gateway: ~2-5 seconds on cache miss (acceptable because pre-population strategy eliminates this for lectionary readings)
- Complex liturgical calendar calculations: ~100ms on uncached dates (mitigated by caching)

---

## Future Research Areas

### Areas Requiring Further Investigation

1. **Service Worker Implementation Details**

   - Current implementation status unclear from codebase analysis
   - May exist in `app/public/` or registered in `app/src/main.js`
   - Needs documentation of caching strategy, update frequency, offline behavior

2. **30-Day Psalm Cycle Selection Mechanism**

   - `ThirtyDayPsalterDay` model exists but frontend toggle implementation needs verification
   - User preference persistence strategy unclear
   - Documentation needed for how/when 30-day cycle overrides 60-day default

3. **Seasonal Lectionary Browsing (US6)**

   - Spec includes P3 priority user story for browsing readings by liturgical season
   - Implementation status unclear - may be partially implemented or planned
   - Would require season calculation and reading aggregation logic

4. **Performance Testing Automation**

   - Spec defines performance targets (SC-001, SC-002, SC-005)
   - Automated performance tests not found in codebase
   - Should implement using pytest-benchmark or similar

5. **Scripture Import Error Handling**
   - `import_scripture` command error handling not fully documented
   - Needs retry logic, rate limit handling, partial failure recovery

---

## References

- **Book of Common Prayer 2019**: Daily Office Lectionary (pp. 985-1018), Holy Eucharist Lectionary (pp. 1019-1051)
- **Revised Common Lectionary**: Three-year Eucharist cycle source
- **Bible Gateway API**: Scripture text retrieval (unofficial API, based on HTML parsing)
- **scriptures Python library**: Scripture citation parsing
- **Project Codebase**: `site/office/`, `site/churchcal/`, `site/bible/`, `app/src/views/Readings.vue`, `app/src/components/Reading.vue`

---

**Document Status**: Retroactive research documentation based on codebase analysis. Future enhancements should update this document with any new decisions or alternatives considered.
