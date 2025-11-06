# Data Model: Liturgical Calendar

**Feature**: 002-liturgical-calendar  
**Created**: November 6, 2025  
**Status**: Design Phase

## Overview

This document describes the data model for the liturgical calendar feature. The model is **already implemented** in `site/churchcal/models.py` and `site/churchcal/calculations.py`. This document serves as design documentation for the existing implementation.

## Entity Relationship Diagram

```
Calendar (1) ──< (N) Commemoration
Calendar (1) ──< (N) CommemorationRank
Calendar (1) ──< (N) Season
Calendar (1) ──< (N) Proper

Commemoration (1) ──> (1) CommemorationRank
Commemoration (1) ──> (1) Season (via season assignment)
Commemoration (1) ──> (0..1) Commemoration (cannot_occur_after)

ChurchYear (1) ──> (1) Calendar
ChurchYear (1) ──< (N) CalendarDate

CalendarDate (1) ──> (1) Season
CalendarDate (1) ──< (N) Commemoration (required)
CalendarDate (1) ──< (N) Commemoration (optional)
CalendarDate (1) ──> (1) Commemoration (primary)
CalendarDate (1) ──> (0..1) Proper
```

## Core Entities

### Calendar

**Purpose**: Represents a specific liturgical calendar system (e.g., ACNA BCP 2019)  
**Database**: `churchcal_calendar` table  
**Implementation**: `churchcal.models.Calendar`

**Fields**:

- `id` (UUID): Primary key
- `name` (string): Calendar name (e.g., "Book of Common Prayer 2019")
- `denomination` (FK): Reference to Denomination
- `year` (string): Calendar version year
- `abbreviation` (string): Short code (e.g., "ACNA_BCP2019")
- `google_sheet_id` (string): Source data sheet ID

**Business Rules**:

- Abbreviation must be unique
- Used as cache key prefix

**Related Requirements**: FR-004

---

### Commemoration (Abstract)

**Purpose**: Base class for all liturgical commemorations (feasts, holy days, saints' days)  
**Database**: `churchcal_commemoration` table (polymorphic)  
**Implementation**: `churchcal.models.Commemoration` (abstract base class)

**Fields**:

- `id` (UUID): Primary key
- `name` (string): Full commemoration name
- `rank` (FK): Reference to CommemorationRank
- `cannot_occur_after` (FK): Self-reference for transfer rules
- `color` (string): Primary liturgical color
- `additional_color` (string): Secondary color option
- `alternate_color` (string): Alternate color (e.g., blue for Advent)
- `alternate_color_2` (string): Second alternate
- `collect_1` (FK): Reference to morning Collect
- `collect_2` (FK): Reference to evening Collect
- `collect_eve` (FK): Reference to First Vespers Collect
- `color_notes` (string): Notes about color usage
- `calendar` (FK): Reference to Calendar
- `biography` (rich text): Saint biography or feast description
- `image_link` (URL): Associated image

**AI-Enhanced Fields** (for User Story 5):

- `ai_one_sentence` (text): Brief description
- `ai_quote` (text): Relevant quote
- `ai_verse` (text): Associated Bible verse
- `ai_hagiography` (text): Detailed biography
- `ai_legend` (text): Traditional stories
- Various citation fields

**Subclasses**:

1. **SanctoraleCommemoration**: Fixed-date commemorations (e.g., January 1)
2. **TemporaleCommemoration**: Easter-based commemorations (e.g., Ascension)
3. **SanctoraleBasedCommemoration**: Commemorations relative to fixed dates
4. **FerialCommemoration**: Weekday feria (non-managed, computed)

**Business Rules**:

- Each commemoration belongs to exactly one Calendar
- Transferred commemorations maintain their original rank
- Colors cascade: primary → additional → alternate → alternate_2
- Cannot occur after another feast (enables transfer logic)

**Related Requirements**: FR-003, FR-004, FR-008, FR-009, FR-016

---

### SanctoraleCommemoration

**Purpose**: Fixed-date commemorations (saints' days, fixed feasts)  
**Database**: Inherits `churchcal_commemoration`  
**Implementation**: `churchcal.models.SanctoraleCommemoration`

**Additional Fields**:

- `month` (1-12): Month of commemoration
- `day` (1-31): Day of commemoration
- `saint_name` (string): Name of saint
- `saint_type` (choice): Type of saint (PASTOR, MARTYR, MISSIONARY, etc.)
- `saint_gender` (choice): M/F/P (plural)
- `saint_fill_in_the_blank` (string): Template variable
- `common` (FK): Reference to Common collect template

**Initial Date Calculation**:

```python
def initial_date(advent_year):
    year = _year_from_advent_year(advent_year, month, day)
    if type(year) == list:  # Spans two years
        return [date(year[0], month, day), date(year[1], month, day)]
    return date(year, month, day)
```

**Examples**:

- "The Confession of St. Peter the Apostle" (January 18)
- "The Annunciation of Our Lord" (March 25)
- "All Saints' Day" (November 1)

**Related Requirements**: FR-003, FR-004

---

### TemporaleCommemoration

**Purpose**: Easter-based moveable feasts  
**Database**: Inherits `churchcal_commemoration`  
**Implementation**: `churchcal.models.TemporaleCommemoration`

**Additional Fields**:

- `days_after_easter` (integer): Offset from Easter Day (can be negative)

**Initial Date Calculation**:

```python
def initial_date(advent_year):
    year = advent_year + 1
    easter_date = easter(year)
    return easter_date + timedelta(days=days_after_easter)
```

**Examples**:

- "Ash Wednesday" (days_after_easter = -46)
- "Ascension Day" (days_after_easter = 39)
- "The Day of Pentecost" (days_after_easter = 49)
- "Trinity Sunday" (days_after_easter = 56)

**Related Requirements**: FR-005

---

### SanctoraleBasedCommemoration

**Purpose**: Commemorations relative to fixed dates (e.g., Sunday after All Saints)  
**Database**: Inherits `churchcal_commemoration`  
**Implementation**: `churchcal.models.SanctoraleBasedCommemoration`

**Additional Fields**:

- `weekday` (string): Target day of week
- `number_after` (integer): Nth occurrence after reference date
- `month_after` (integer): Reference month
- `day_after` (integer): Reference day
- `additional_days_after` (integer): Additional offset

**Initial Date Calculation**:

```python
def initial_date(advent_year):
    early_year = weekday_after(weekday, month_after, day_after,
                                advent_year, number_after)
    advent_start = advent(advent_year)

    if early_year >= advent_start:
        return early_year + timedelta(days=additional_days_after)

    return_date = weekday_after(weekday, month_after, day_after,
                                advent_year + 1, number_after)
    return return_date + timedelta(days=additional_days_after)
```

**Business Rules**:

- Cannot occur if All Saints falls on Sunday (special rule)

**Examples**:

- "Sunday After All Saints" (Sunday after November 1)

**Related Requirements**: FR-005, FR-008

---

### CommemorationRank

**Purpose**: Defines precedence and importance of commemorations  
**Database**: `churchcal_commemorationrank` table  
**Implementation**: `churchcal.models.CommemorationRank`

**Fields**:

- `id` (UUID): Primary key
- `name` (string): Internal rank name (e.g., "PRINCIPAL_FEAST")
- `formatted_name` (string): Display name (e.g., "Principal Feast")
- `precedence_rank` (integer 1-9): Precedence level (1 = highest)
- `required` (boolean): Required vs. optional commemoration
- `calendar` (FK): Reference to Calendar

**Rank Hierarchy** (BCP 2019):

1. **PRINCIPAL_FEAST** (precedence_rank=1, required=True)
   - Easter Day, Christmas Day, Pentecost, Trinity Sunday, etc.
2. **SUNDAY** (precedence_rank=2, required=True)
   - All Sundays
3. **PRIVILEGED_OBSERVANCE** (precedence_rank=3, required=True)
   - Ash Wednesday, Holy Week days
4. **HOLY_DAY** (precedence_rank=4, required=True)
   - Major feasts (Epiphany, Ascension, etc.)
5. **PRIVILEGED_LESSER_FEAST** (precedence_rank varies, required=False)
   - Optional observances that can displace certain commemorations
6. **FERIA** (precedence_rank=8, required=False)
   - Weekday commemorations
7. **EMBER_DAY**, **ROGATION_DAY** (precedence_rank varies)
   - Traditional fasting days

**Business Rules**:

- Lower precedence_rank number = higher precedence
- Required commemorations cannot be displaced by optional ones
- Precedence determines which feast is observed when multiple fall on same date

**Related Requirements**: FR-008, FR-009, FR-012

---

### Season

**Purpose**: Defines liturgical seasons (Advent, Christmas, Lent, Easter, etc.)  
**Database**: `churchcal_season` table  
**Implementation**: `churchcal.models.Season`

**Fields**:

- `id` (UUID): Primary key
- `order` (integer 1-28): Display order
- `name` (string): Season name
- `start_commemoration` (FK): Commemoration that starts this season
- `color` (string): Primary liturgical color for season
- `alternate_color` (string): Alternate color option
- `rank` (FK): Default rank for ferias in this season
- `calendar` (FK): Reference to Calendar

**Season List** (BCP 2019):

1. **Advent** (color: purple or blue, 4 weeks before Christmas)
2. **Christmastide** (color: white, Christmas through Epiphany)
3. **Epiphany** (color: green, Epiphany through pre-Lent)
4. **Lent** (color: purple, Ash Wednesday through Holy Week)
5. **Holy Week** (color: red/purple, Palm Sunday through Easter Eve)
6. **Eastertide** (color: white/gold, Easter through Pentecost)
7. **Season After Pentecost** (color: green, Trinity Sunday through Advent)

**Business Rules**:

- Season changes on specific commemorations
- Feria (weekdays) inherit season color
- Privileged seasons (Advent, Lent, Holy Week, Eastertide) protect Sundays from displacement

**Related Requirements**: FR-002, FR-010

---

### Proper

**Purpose**: Sunday propers for Season After Pentecost (Proper 1-28)  
**Database**: `churchcal_proper` table  
**Implementation**: `churchcal.models.Proper`

**Fields**:

- `id` (UUID): Primary key
- `number` (integer 1-28): Proper number
- `start_date` (date): First Sunday this proper may be used
- `end_date` (date): Last Sunday this proper may be used
- `collect_1` (FK): Collect for this proper
- `calendar` (FK): Reference to Calendar

**Business Rules**:

- Propers apply to Sundays after Pentecost
- Date ranges overlap (actual proper depends on Easter date)
- Weekday ferias after Sunday use Sunday's proper

**Related Requirements**: FR-010

---

## Computed Entities (Non-Database)

### CalendarDate

**Purpose**: Represents a single day in the church year with all liturgical information  
**Implementation**: `churchcal.calculations.CalendarDate` (Python class, not Django model)

**Fields**:

- `date` (datetime.date): The calendar date
- `calendar` (Calendar): Reference to Calendar system
- `year` (ChurchYear): Reference to church year
- `season` (Season): Current liturgical season
- `evening_season` (Season): Season for evening (may differ for First Vespers)
- `required` (list[Commemoration]): Required commemorations for this day
- `optional` (list[Commemoration]): Optional commemorations for this day
- `evening_required` (list[Commemoration]): Required commemorations for evening
- `evening_optional` (list[Commemoration]): Optional commemorations for evening
- `primary` (Commemoration): The principal commemoration for the day
- `proper` (Proper): Associated proper (if applicable)
- `finalized` (bool): Whether transfers and rules have been applied

**Computed Properties**:

- `all`: Returns required + optional commemorations
- `all_evening`: Returns evening_required + evening_optional
- `primary_evening`: Returns first evening commemoration
- `office_year`: Returns 1 or 2 based on year parity
- `mass_readings`: Returns Mass readings for primary commemoration
- `fast_day`: Returns fasting level (NONE, PARTIAL, FULL)

**Business Logic**:

```python
def apply_rules():
    """Apply precedence rules and process transfers"""
    transfers = process_transfers()  # Return lower-precedence feasts
    finalize_day()  # Set primary, append feria if needed
    return transfers

def process_transfers():
    """When multiple required commemorations conflict, keep highest
    precedence and transfer others to next day"""
    if len(required) < 2:
        return []

    # Keep highest precedence, transfer rest
    transfers = required[1:]
    required = required[:1]

    for transfer in transfers:
        transfer.transferred = True

    return [feast for feast in transfers if feast.rank.name != "SUNDAY"]
```

**Related Requirements**: FR-001, FR-008, FR-009, FR-010, FR-016

---

### ChurchYear

**Purpose**: Represents one liturgical year (Advent to Advent)  
**Implementation**: `churchcal.calculations.ChurchYear`

**Fields**:

- `start_year` (integer): Year Advent begins (church year identifier)
- `end_year` (integer): start_year + 1
- `calendar` (Calendar): Calendar system
- `dates` (IndexedOrderedDict): All dates in the year (365/366 CalendarDate objects)
- `start_date` (date): First Sunday of Advent
- `end_date` (date): Day before next Advent
- `seasons` (dict): Season mapping

**Computed Properties**:

- `mass_year`: Returns "A", "B", or "C" based on start_year % 3
- `office_year`: Returns "I" or "II" based on start_year % 2
- `daily_mass_year`: Returns 1 or 2 based on end_year % 2

**Construction Process**:

1. Calculate Advent date for start_year
2. Create CalendarDate for each day from Advent to Advent
3. Query all Commemorations and add to appropriate dates
4. Iterate through all dates:
   - Set season for each date
   - Apply precedence rules (process transfers)
   - Apply First Vespers rules
   - Set names and collects
5. Cache the complete year

**Caching Strategy**:

- Cache key: `"{start_year}_{calendar.abbreviation}"`
- TTL: 12 hours
- Invalidation: Manual (rarely needed)

**Related Requirements**: FR-005, FR-008, FR-009, SC-008

---

### CalendarYear

**Purpose**: Represents a standard calendar year (Jan-Dec) spanning two church years  
**Implementation**: `churchcal.calculations.CalendarYear`

**Fields**:

- `dates` (IndexedOrderedDict): All dates for calendar year (365/366 CalendarDate objects)

**Construction**:

```python
def __init__(year, first_year, second_year):
    # Combine two ChurchYear objects
    dates = IndexedOrderedDict(**first_year.dates, **second_year.dates)
    # Filter to calendar year
    dates = {k: v for (k, v) in dates.items()
             if int(k.split("-")[0]) == year}
    self.dates = IndexedOrderedDict(**dates)
```

**Business Rules**:

- Calendar year 2024 includes:
  - Days from Church Year 2023 (Jan 1 - Advent 2024)
  - Days from Church Year 2024 (Advent 2024 - Dec 31)

**Related Requirements**: FR-001, SC-008

---

## API Data Transfer Objects

### DayDTO (Current Implementation)

**Purpose**: Serialized representation of CalendarDate for API responses  
**Implementation**: `churchcal.api.serializer.DaySerializer`

**Current Fields**:

```json
{
  "date": "2024-11-24",
  "season": {
    "name": "Season After Pentecost",
    "colors": ["green"]
  },
  "commemorations": [
    {
      "name": "The Sunday Next Before Advent",
      "colors": ["green"],
      "rank": {
        "name": "SUNDAY",
        "formatted_name": "Sunday",
        "precedence_rank": 2,
        "required": true
      }
    }
  ],
  "major_feast": "The Sunday Next Before Advent",
  "major_or_minor_feast": "The Sunday Next Before Advent",
  "proper": {
    "number": 28
  }
}
```

**Proposed Enhancement (for FR-016)**:

```json
{
  "date": "2024-12-24",
  "season": {
    "name": "Advent",
    "colors": ["purple", "blue"]
  },
  "evening_season": {
    "name": "Christmastide",
    "colors": ["white"]
  },
  "commemorations": [
    {
      "name": "Advent Feria",
      "colors": ["purple", "blue"],
      "rank": {...}
    }
  ],
  "evening_commemorations": [
    {
      "name": "Eve of The Nativity of Our Lord",
      "colors": ["white"],
      "rank": {...}
    }
  ],
  "major_feast": null,
  "evening_major_feast": "Eve of The Nativity of Our Lord",
  "has_first_vespers": true
}
```

**New Fields** (GAP-003):

- `evening_season`: Season object for evening
- `evening_commemorations`: List of evening commemorations
- `evening_major_feast`: Major feast for evening (if different)
- `has_first_vespers`: Boolean flag for UI

**Related Requirements**: FR-016

---

## Validation Rules

### Date Validation

- All dates must be valid Gregorian calendar dates
- Leap year handling: February 29 exists only in leap years
- Date ranges: System supports years 2018-2030 (configurable)

### Commemoration Validation

- Each commemoration must have valid rank
- Colors must be from approved list: red, white, green, purple, blue, rose, black
- Collect references must exist in office.Collect table
- cannot_occur_after must reference valid commemoration

### Precedence Validation

- precedence_rank must be 1-9
- Lower number = higher precedence
- Multiple commemorations on same date: higher precedence wins

### Transfer Validation

- Transferred commemorations keep original rank
- Transfers chain forward (if next day also conflicts)
- Sundays are never displaced except by Principal Feasts
- Privileged seasons (Advent, Lent, Holy Week, Eastertide) protect observances

### First Vespers Validation (FR-016)

- First Vespers applies to commemorations with precedence_rank ≤ 4
- First Vespers does NOT apply during privileged observances
- Evening before feast shows "Eve of [Feast Name]"
- Evening season and color match the upcoming feast

---

## State Transitions

### CalendarDate Lifecycle

1. **Created**: CalendarDate object instantiated with date and calendar
2. **Commemorations Added**: All matching commemorations added to required/optional lists
3. **Sorted**: Commemorations sorted by precedence_rank
4. **Season Applied**: Season determined based on position in church year
5. **Transfers Processed**: Lower-precedence commemorations transferred to next day
6. **Finalized**: Primary set, feria appended if needed, finalized=True
7. **First Vespers Applied**: Evening fields set for day before major feasts
8. **Names and Collects Set**: Display names and collects assigned
9. **Cached**: Complete CalendarDate cached as part of ChurchYear

**State Diagram**:

```
Created → Commemorations Added → Sorted → Season Applied
    ↓
Transfers Processed → Finalized → First Vespers Applied
    ↓
Names and Collects Set → Cached
```

---

## Performance Considerations

### Caching Strategy

- **ChurchYear**: Cached for 12 hours per calendar system
- **Cache Key**: `"{start_year}_{calendar_abbreviation}"`
- **Cache Backend**: Memcached
- **Cache Hit Rate**: Expected ~99% (years don't change often)

### Query Optimization

- Use `select_related()` for Commemoration queries (loads rank, season)
- Use `prefetch_related()` for Mass readings
- Avoid N+1 queries in serializer

### Lazy Evaluation

- Church year construction is eager (precomputes all dates)
- Individual date lookups use indexed dictionary (O(1))
- Collects and readings loaded on-demand via cached_property

---

## Migration Considerations

### Existing Data

- All tables already exist and populated
- No schema changes needed for FR-001 through FR-015
- FR-016 requires no schema changes (computed fields)

### Backward Compatibility

- API changes must be additive (new fields only)
- Existing API consumers must continue to work
- Evening fields optional in responses

### Data Integrity

- Foreign key constraints enforced at database level
- Cannot delete Calendar if Commemorations reference it
- Cannot delete CommemorationRank if Commemorations use it

---

## Testing Data

### Test Fixtures Needed

1. **Test Calendar**: Minimal calendar with essential commemorations
2. **Test Commemorations**:
   - At least one of each type (Sanctorale, Temporale, SanctoraleBased)
   - Commemorations with different ranks
   - Commemorations that conflict (for transfer testing)
3. **Test Dates**:
   - Easter date for test years (2024, 2025, 2026)
   - Leap year (February 29, 2024)
   - First Vespers examples (December 24, January 5)
   - Transfer examples (when multiple feasts conflict)

### Test Scenarios

1. **Date Calculation**:

   - Easter calculation for multiple years
   - Advent calculation for multiple years
   - Moveable feast calculations (Ascension, Pentecost)
   - Leap year handling

2. **Precedence**:

   - Two commemorations same day, different ranks
   - Principal Feast on Sunday (Feast wins)
   - Optional feast on Sunday (Sunday wins)

3. **Transfers**:

   - Required feast on Sunday (transferred to Monday)
   - Chain transfers (Monday also has conflict)
   - Cannot occur after logic

4. **First Vespers**:

   - Major feast with precedence ≤4 (has First Vespers)
   - Major feast during privileged season (no First Vespers)
   - Evening fields populated correctly

5. **Filtering**:
   - Show all feasts (all commemorations visible)
   - Show major feasts only (only required=True visible)

---

## References

- Implementation: `site/churchcal/models.py`
- Calculations: `site/churchcal/calculations.py`
- API Serializer: `site/churchcal/api/serializer.py`
- Specification: `specs/002-liturgical-calendar/spec.md`
- BCP 2019 Calendar: [ACNA Website](https://bcp2019.anglicanchurch.net/)

---

**Document Version**: 1.0  
**Last Updated**: November 6, 2025  
**Next Review**: Upon implementation start
