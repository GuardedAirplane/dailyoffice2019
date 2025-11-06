# Data Model: Lectionary

**Feature**: 005-lectionary  
**Date**: 2025-11-06  
**Status**: Retroactive Documentation

This document provides comprehensive documentation of the data models supporting the Daily Office 2019 lectionary functionality. The models are split across two Django applications: `office` (Daily Office readings and scripture cache) and `churchcal` (liturgical calendar and Eucharist readings).

## Table of Contents

1. [Overview](#overview)
2. [Daily Office Domain Models](#daily-office-domain-models)
3. [Eucharist Lectionary Domain Models](#eucharist-lectionary-domain-models)
4. [Liturgical Calendar Support Models](#liturgical-calendar-support-models)
5. [Scripture Storage Models](#scripture-storage-models)
6. [Model Relationships](#model-relationships)
7. [Database Schema](#database-schema)
8. [Requirements Traceability](#requirements-traceability)

---

## Overview

### Model Organization

The lectionary system uses a **dual-model architecture** to support two distinct lectionary cycles:

1. **Daily Office Models** (`office/models.py`): Support two-year cycle for Morning and Evening Prayer
2. **Eucharist Models** (`churchcal/models.py`, `office/models.py`): Support three-year cycle for Holy Eucharist

This separation reflects the fundamental structural differences in BCP 2019:

- Daily Office: Fixed reading structure (2 psalms + 2 scripture readings each service, consistent across years)
- Eucharist: Variable reading structure (1-4 readings, year-specific assignments for Years A/B/C)

### Key Design Principles

1. **Pre-computation**: Reading assignments stored in database, not calculated on-the-fly
2. **Denormalization**: Scripture text cached in database columns for each translation (optimizes read performance)
3. **Inheritance**: `OfficeDay` abstract base enables polymorphism for standard days vs. feast days
4. **Cached Properties**: Expensive computations cached per-request using Django's `@cached_property`
5. **Foreign Keys**: Link readings to commemorations, propers, and commons for flexibility

---

## Daily Office Domain Models

### OfficeDay (Abstract Base Model)

**Location**: `site/office/models.py:14-71`  
**Purpose**: Abstract base providing common structure for all daily office reading assignments  
**Implements**: FR-001, FR-002, FR-003, FR-009

#### Fields

| Field                           | Type           | Constraints           | Description                                          |
| ------------------------------- | -------------- | --------------------- | ---------------------------------------------------- |
| `holy_day_name`                 | CharField(255) | null=True, blank=True | Name of feast day if applicable                      |
| `mp_psalms`                     | CharField(255) | required              | Psalm citations for Morning Prayer (comma-separated) |
| `mp_reading_1`                  | CharField(255) | required              | First scripture reading for Morning Prayer           |
| `mp_reading_1_testament`        | CharField(2)   | choices=TESTAMENTS    | Testament indicator: OT/DC/AP/NT                     |
| `mp_reading_1_text`             | TextField      | blank=True, null=True | Cached text (deprecated, use Scripture model)        |
| `mp_reading_1_abbreviated`      | CharField(255) | null=True, blank=True | Shorter alternative reading                          |
| `mp_reading_1_abbreviated_text` | TextField      | blank=True, null=True | Cached abbreviated text                              |
| `mp_reading_2`                  | CharField(255) | required              | Second scripture reading for Morning Prayer          |
| `mp_reading_2_testament`        | CharField(2)   | choices=TESTAMENTS    | Testament indicator: OT/DC/AP/NT                     |
| `mp_reading_2_text`             | TextField      | blank=True, null=True | Cached text (deprecated)                             |
| `ep_psalms`                     | CharField(255) | required              | Psalm citations for Evening Prayer (comma-separated) |
| `ep_reading_1`                  | CharField(255) | required              | First scripture reading for Evening Prayer           |
| `ep_reading_1_testament`        | CharField(2)   | choices=TESTAMENTS    | Testament indicator: OT/DC/AP/NT                     |
| `ep_reading_1_text`             | TextField      | blank=True, null=True | Cached text (deprecated)                             |
| `ep_reading_1_abbreviated`      | CharField(255) | null=True, blank=True | Shorter alternative reading                          |
| `ep_reading_1_abbreviated_text` | TextField      | blank=True, null=True | Cached abbreviated text                              |
| `ep_reading_2`                  | CharField(255) | required              | Second scripture reading for Evening Prayer          |
| `ep_reading_2_testament`        | CharField(2)   | choices=TESTAMENTS    | Testament indicator: OT/DC/AP/NT                     |
| `ep_reading_2_text`             | TextField      | blank=True, null=True | Cached text (deprecated)                             |

#### Testament Choices

```python
TESTAMENTS = (
    ("OT", "Old Testament"),
    ("DC", "Deuterocanon"),
    ("AP", "Apocrypha"),
    ("NT", "New Testament")
)
```

**Usage**: The `testament` field enables automatic translation fallback for deuterocanonical readings (FR-014).

#### Properties and Methods

**`readings` (cached_property)**

- **Returns**: Dictionary mapping passage citations to `Scripture` objects
- **Purpose**: Eager-load all scripture text for this day's readings in one query
- **Optimization**: Reduces N+1 query problem when displaying multiple readings

**`passage_to_text(attribute, translation='esv')`**

- **Parameters**:
  - `attribute`: Field name (e.g., "mp_reading_1", "ep_reading_2")
  - `translation`: Bible translation code (default: "esv")
- **Returns**: HTML-formatted scripture text for specified reading
- **Fallback**: If text unavailable in selected translation, falls back to NRSVCE
- **Abbreviation handling**: If abbreviated reading specified, uses full reading if abbreviated not available

**`__getattribute__(attrname)`**

- **Override purpose**: Injects CSS class into scripture HTML headings
- **Behavior**: Replaces `<h3>` with `<h3 class='reading-heading off'>` in all text fields
- **Rationale**: Enables toggling section headings in frontend without modifying cached HTML

#### Relationships

- **Inheritance**: Base class for `StandardOfficeDay` and `HolyDayOfficeDay`
- **Related**: Links to `Scripture` objects via passage citations (not FK - lookup via citation string)

#### Example Usage

```python
# Retrieve today's reading assignments
office_day = StandardOfficeDay.objects.get(month=11, day=6)

# Access readings
mp_psalm_citation = office_day.mp_psalms  # "1, 2, 3"
mp_reading_1_citation = office_day.mp_reading_1  # "Genesis 1:1-31"
mp_reading_1_text = office_day.passage_to_text('mp_reading_1', 'nrsv')

# Check testament for apocrypha fallback
is_deuterocanon = office_day.mp_reading_1_testament == 'DC'
```

---

### StandardOfficeDay (Concrete Model)

**Location**: `site/office/models.py:72-76`  
**Purpose**: Stores reading assignments for regular calendar days (non-feast days)  
**Implements**: FR-001, FR-002, FR-003, FR-012

#### Fields

| Field                                  | Type         | Constraints | Description               |
| -------------------------------------- | ------------ | ----------- | ------------------------- |
| `month`                                | IntegerField | required    | Month number (1-12)       |
| `day`                                  | IntegerField | required    | Day of month (1-31)       |
| _(inherits all fields from OfficeDay)_ |              |             | See OfficeDay model above |

#### Database Coverage

- **Records**: 366 records (one per calendar day including February 29)
- **Two-Year Cycle**: Same records used for both Year 1 and Year 2 (cycle determined by calculation, not database)
- **Indexing**: Indexed on `(month, day)` for fast lookup

#### Query Patterns

```python
# Get readings for specific date
from datetime import date
today = date.today()
office_day = StandardOfficeDay.objects.get(month=today.month, day=today.day)

# Get readings for date range (e.g., all of Advent)
november_readings = StandardOfficeDay.objects.filter(month=11).order_by('day')
```

#### Relationships

- **Inherits**: `OfficeDay` abstract base class
- **Replaced By**: `HolyDayOfficeDay` when feast occurs on this calendar date

---

### HolyDayOfficeDay (Concrete Model)

**Location**: `site/office/models.py:77-81`  
**Purpose**: Stores proper readings for feast days and holy days that replace standard readings  
**Implements**: FR-008, FR-009

#### Fields

| Field                                  | Type                      | Constraints               | Description                                          |
| -------------------------------------- | ------------------------- | ------------------------- | ---------------------------------------------------- |
| `commemoration`                        | ForeignKey                | to Commemoration, CASCADE | The feast or holy day this reading set belongs to    |
| `order`                                | PositiveSmallIntegerField | default=0                 | Order when multiple reading sets exist for one feast |
| _(inherits all fields from OfficeDay)_ |                           |                           | See OfficeDay model above                            |

#### Usage Notes

- **Feast Precedence**: When feast occurs, `HolyDayOfficeDay` readings override `StandardOfficeDay` readings
- **Multiple Options**: Some major feasts have multiple reading sets (order field distinguishes)
- **Transferred Feasts**: Commemoration's observed date determines when these readings are used

#### Query Patterns

```python
# Get proper readings for a commemoration
from churchcal.models import SanctoraleCommemoration
christmas = SanctoraleCommemoration.objects.get(name__contains="Christmas Day")
christmas_readings = HolyDayOfficeDay.objects.filter(commemoration=christmas).first()

# Check if a date has proper readings
from churchcal.calculations import get_date  # Returns liturgical date with commemorations
liturgical_date = get_date(date(2025, 12, 25))
has_proper = HolyDayOfficeDay.objects.filter(
    commemoration=liturgical_date.primary
).exists()
```

---

### ThirtyDayPsalterDay (Concrete Model)

**Location**: `site/office/models.py:83-95`  
**Purpose**: Provides alternative 30-day psalm cycle (completes Psalter monthly instead of 60-day cycle)  
**Implements**: FR-002

#### Fields

| Field       | Type           | Constraints | Description                        |
| ----------- | -------------- | ----------- | ---------------------------------- |
| `day`       | IntegerField   | required    | Day of month (1-30)                |
| `mp_psalms` | CharField(255) | required    | Psalm citations for Morning Prayer |
| `ep_psalms` | CharField(255) | required    | Psalm citations for Evening Prayer |

#### Database Coverage

- **Records**: 30 records (one per day of month)
- **Usage**: Alternative to 60-day cycle embedded in `StandardOfficeDay`

#### Methods

**`psalm_string_to_list(psalms)`**

- **Parameters**: Psalm citation string (e.g., "1, 2, 3")
- **Returns**: List of individual psalm numbers
- **Note**: Implementation appears to have bug - calls `psalms.split(psalms)` which should be `psalms.split(', ')`

**`get_mp_psalms()`** and **`get_ep_psalms()`**

- **Returns**: List of psalm numbers for Morning/Evening Prayer
- **Uses**: `psalm_string_to_list()` method

#### Query Patterns

```python
# Get 30-day cycle psalms for today
day_of_month = date.today().day
if day_of_month > 30:
    day_of_month = 30  # Use day 30 for days 31+
thirty_day = ThirtyDayPsalterDay.objects.get(day=day_of_month)
mp_psalms = thirty_day.mp_psalms
```

---

## Eucharist Lectionary Domain Models

### LectionaryItem (Concrete Model)

**Location**: `site/office/models.py:405-576`  
**Purpose**: Links commemorations/propers/commons to their Eucharist mass readings; handles three-year cycle  
**Implements**: FR-004, FR-008, FR-017

#### Fields

| Field                      | Type                      | Constraints                                     | Description                                               |
| -------------------------- | ------------------------- | ----------------------------------------------- | --------------------------------------------------------- |
| `commemoration`            | ForeignKey                | to Commemoration, SET_NULL, null=True           | Specific feast day (e.g., Christmas, Easter)              |
| `sanctorale_commemoration` | ForeignKey                | to SanctoraleCommemoration, SET_NULL, null=True | Saints' day commemoration                                 |
| `proper`                   | ForeignKey                | to Proper, SET_NULL, null=True                  | Proper of the season (numbered Sunday sets)               |
| `common`                   | ForeignKey                | to Common, SET_NULL, null=True                  | Common of Saints (generic reading sets)                   |
| `order`                    | PositiveSmallIntegerField | default=0                                       | Ordering when multiple items exist                        |
| `service`                  | CharField(255)            | required                                        | Service type (e.g., "Principal Service", "Early Service") |

**Constraint**: At least one of `commemoration`, `sanctorale_commemoration`, `proper`, or `common` must be set.

#### Cached Properties

##### Name and Display Properties

**`name` (cached_property)**

- **Returns**: Human-readable name from linked commemoration/proper/common
- **Priority**: commemoration → proper → common → "Lectionary Entry"

**`name_and_service` (cached_property)**

- **Returns**: Name with service type in parentheses
- **Example**: "Christmas Day (Principal Service)"

**`date_string` (cached_property)**

- **Returns**: Formatted date range for proper readings
- **Examples**:
  - "December 25" (sanctorale)
  - "Sunday from June 5 to June 11" (proper)
  - "" (common - no specific date)

##### Mass Readings Properties

**`mass_readings` (cached_property)**

- **Returns**: QuerySet of `MassReading` objects for this lectionary item
- **Filters**: By service type if specified
- **Source**: commemoration.mass_readings or proper.mass_readings or common.mass_readings

**`mass_readings_by_year(year='A')` (method)**

- **Parameters**: year - 'A', 'B', or 'C'
- **Returns**: Filtered list of mass readings for specified year
- **Logic**: Filters `mass_readings` where year appears in reading's `years` field

**`year_a`, `year_b`, `year_c` (cached_properties)**

- **Returns**: Mass readings for Years A, B, or C respectively
- **Usage**: Pre-computed for performance when rendering year-specific readings

##### Reading Passage Methods

**`year_to_readings(year)` (method)**

- **Parameters**: year - 'A', 'B', or 'C' (case-insensitive)
- **Returns**: Appropriate year_a, year_b, or year_c property
- **Default**: Returns year_a if invalid year specified

**`combine_short_and_long_passage(reading, year)` (method)**

- **Parameters**:
  - `reading`: MassReading object with long_scripture and optional short_scripture
  - `year`: 'A', 'B', or 'C'
- **Returns**: HTML anchor link with passage citation and optional shorter alternative
- **Format**: `"Luke 2:1-20 [ or, 2:1-14 ]"` when short alternative exists
- **Purpose**: Display both full and abbreviated reading options (FR-017)

**`passages_for_year_and_number(year, number)` (method)**

- **Parameters**:
  - `year`: 'A', 'B', or 'C'
  - `number`: Reading number (1-4)
- **Returns**: HTML string with all passages for specified reading number, joined with " <em>or</em> " separator
- **Purpose**: Handle alternative readings appointed for same position

**`reading_1_passages(year)` through `reading_4_passages(year)` (methods)**

- **Parameters**: year - 'A', 'B', or 'C'
- **Returns**: Formatted passage string for reading position 1-4
- **Usage**: Retrieve specific reading (Old Testament, Psalm, Epistle, Gospel typically)

**`reading_1_a_passages` through `reading_4_c_passages` (cached_properties, 12 total)**

- **Returns**: Pre-computed passage strings for all combinations of reading number (1-4) and year (A/B/C)
- **Purpose**: Performance optimization - avoids repeated computation during rendering

##### Collect Properties

**`collects` (cached_property)**

- **Returns**: List of Collect objects associated with this lectionary item
- **Sources**: Collects from commemoration, proper, or common
- **Order**: collect_1, collect_2, collect_eve (where available)

#### Relationships

- **commemoration** → `Commemoration` (general commemorations)
- **sanctorale_commemoration** → `SanctoraleCommemoration` (saints' days)
- **proper** → `Proper` (proper of the season)
- **common** → `Common` (common of saints)
- **mass_readings** ← `MassReading` (reverse FK, multiple readings per item)

#### Query Patterns

```python
# Get lectionary items for Christmas
from churchcal.models import SanctoraleCommemoration
christmas = SanctoraleCommemoration.objects.get(name__contains="Christmas Day")
christmas_lectionary = LectionaryItem.objects.filter(
    sanctorale_commemoration=christmas
).select_related('sanctorale_commemoration')

# Get readings for specific year
for item in christmas_lectionary:
    year_a_readings = item.year_a  # Returns MassReading queryset
    old_testament = item.reading_1_a_passages  # Returns formatted citation HTML
```

---

### MassReading (Concrete Model)

**Location**: `site/churchcal/models.py:421-454`  
**Purpose**: Individual scripture reading for Holy Eucharist with year and reading type  
**Implements**: FR-004, FR-013, FR-017

#### Fields

| Field             | Type                      | Constraints                           | Description                                               |
| ----------------- | ------------------------- | ------------------------------------- | --------------------------------------------------------- |
| `long_citation`   | CharField(256)            | required                              | Full scripture citation (e.g., "Luke 2:1-20")             |
| `long_text`       | TextField                 | blank=True, null=True                 | Cached full text (deprecated - use Scripture model)       |
| `service`         | CharField(256)            | required                              | Service type (e.g., "Principal Service", "Early Service") |
| `short_citation`  | CharField(256)            | required                              | Abbreviated citation (may be same as long)                |
| `short_text`      | TextField                 | blank=True, null=True                 | Cached abbreviated text (deprecated)                      |
| `years`           | CharField(3)              | required                              | Year designation: A, B, C, AB, AC, BC, ABC                |
| `commemoration`   | ForeignKey                | to Commemoration, SET_NULL, null=True | Specific feast reading                                    |
| `proper`          | ForeignKey                | to Proper, SET_NULL, null=True        | Proper of season reading                                  |
| `common`          | ForeignKey                | to Common, SET_NULL, null=True        | Common of saints reading                                  |
| `reading_type`    | CharField(256)            | choices=READING_TYPES                 | prophecy, psalm, epistle, or gospel                       |
| `book`            | CharField(256)            | required                              | Bible book name                                           |
| `testament`       | CharField(4)              | required                              | OT, NT, AP, or DC                                         |
| `calendar`        | ForeignKey                | to Calendar, CASCADE                  | Calendar this reading belongs to                          |
| `abbreviation`    | CharField(256)            | blank=True, null=True                 | Service abbreviation                                      |
| `reading_number`  | PositiveSmallIntegerField | required                              | Position in sequence (1-4)                                |
| `order`           | PositiveSmallIntegerField | required                              | Sub-order within reading_number (for alternatives)        |
| `long_scripture`  | ForeignKey                | to Scripture, SET_NULL, null=True     | Full Scripture object                                     |
| `short_scripture` | ForeignKey                | to Scripture, SET_NULL, null=True     | Abbreviated Scripture object                              |

#### Reading Type Choices

```python
READING_TYPES = (
    ("prophecy", "prophecy"),  # Old Testament reading
    ("psalm", "psalm"),        # Responsorial psalm
    ("epistle", "epistle"),    # New Testament epistle
    ("gospel", "gospel")       # Gospel reading
)
```

#### Years Field Values

- **Single Year**: "A", "B", or "C" - Reading used only in that year
- **Two Years**: "AB", "AC", or "BC" - Reading used in both specified years
- **All Years**: "ABC" - Reading used in all three years (common pattern for major feasts)

#### Database Coverage

- **Records**: ~2000-3000 mass readings total
- **Coverage**: Sunday readings for all three years, major feast days, propers, commons

#### Relationships

- **commemoration** → `Commemoration` (for feast-specific readings)
- **proper** → `Proper` (for proper of season)
- **common** → `Common` (for common of saints)
- **calendar** → `Calendar` (BCP 2019 calendar)
- **long_scripture** → `Scripture` (full passage text)
- **short_scripture** → `Scripture` (abbreviated passage text)

#### Query Patterns

```python
# Get Year A Gospel readings for Advent
from churchcal.models import MassReading, Proper
advent_propers = Proper.objects.filter(name__contains="Advent")
advent_gospels = MassReading.objects.filter(
    proper__in=advent_propers,
    years__contains="A",
    reading_type="gospel"
).order_by("proper__number", "reading_number", "order")

# Get all readings for a commemoration
christmas_readings = MassReading.objects.filter(
    commemoration__name__contains="Christmas Day",
    service="Principal Service"
).order_by("reading_number", "order")
```

---

## Liturgical Calendar Support Models

### Commemoration (Abstract Base Model)

**Location**: `site/churchcal/models.py:48-102`  
**Purpose**: Abstract base for all commemorations (feasts, holy days, saints' days)  
**Supports**: FR-008 (proper feast readings)

#### Key Fields

| Field                                   | Type                            | Description                                        |
| --------------------------------------- | ------------------------------- | -------------------------------------------------- |
| `name`                                  | CharField(256)                  | Full name of commemoration                         |
| `rank`                                  | ForeignKey to CommemorationRank | Precedence rank (1-9, lower is higher precedence)  |
| `color`                                 | CharField(256)                  | Liturgical color (white, red, green, purple, blue) |
| `collect_1`, `collect_2`, `collect_eve` | ForeignKey to Collect           | Associated collects                                |
| `calendar`                              | ForeignKey to Calendar          | BCP 2019 calendar                                  |
| `biography`, `ai_hagiography`, etc.     | Various                         | Educational content about saint/feast              |

#### Subclasses

1. **SanctoraleCommemoration**: Fixed-date commemorations (saints' days, Christmas, etc.)
2. **MovableCommemoration**: Calculated-date commemorations (Easter, Ascension, etc.)
3. **SeasonalCommemoration**: Seasons (Advent, Christmas, Lent, Easter, etc.)

#### Methods

**`get_mass_readings_for_year(year, time='morning')`**

- **Returns**: QuerySet of MassReading objects for this commemoration in specified year
- **Fallback**: If no specific readings, uses common of saints based on `saint_type`

---

### SanctoraleCommemoration (Concrete Model)

**Location**: `site/churchcal/models.py:235-290`  
**Purpose**: Fixed-date commemorations (saints' days, solemnities on specific calendar dates)  
**Implements**: FR-008

#### Additional Fields

| Field                     | Type                      | Description                                              |
| ------------------------- | ------------------------- | -------------------------------------------------------- |
| `month`                   | PositiveSmallIntegerField | Month (1-12)                                             |
| `day`                     | PositiveSmallIntegerField | Day of month (1-31)                                      |
| `saint_name`              | CharField(256)            | Saint's name (for dynamic collect generation)            |
| `saint_type`              | CharField(256)            | Type: PASTOR, MARTYR, MISSIONARY, etc. (links to Common) |
| `saint_gender`            | CharField(1)              | M, F, or P (plural) - for collect grammar                |
| `saint_fill_in_the_blank` | CharField(256)            | Additional text for collect template                     |
| `common`                  | ForeignKey to Common      | Common of saints this falls under                        |

#### Methods

**`initial_date(advent_year, calendar_year=None)`**

- **Returns**: Date object for this commemoration's calendar date
- **Purpose**: Calculate observed date considering year context

**`build_collect(text)`**

- **Parameters**: Collect template text with format placeholders
- **Returns**: Formatted collect with saint-specific details filled in
- **Purpose**: Generate collect dynamically for lesser saints using common template

---

### Proper (Concrete Model)

**Location**: `site/churchcal/models.py` (not shown in excerpt)  
**Purpose**: Proper of the season (numbered Sunday reading sets, e.g., "Proper 1", "Proper 2")  
**Implements**: FR-004

#### Key Fields

| Field        | Type                  | Description                       |
| ------------ | --------------------- | --------------------------------- |
| `number`     | IntegerField          | Proper number (1-29 typically)    |
| `name`       | CharField             | Display name (e.g., "Proper 5")   |
| `start_date` | DateField             | First day this proper can be used |
| `end_date`   | DateField             | Last day this proper can be used  |
| `collect_1`  | ForeignKey to Collect | Collect for this proper           |

#### Relationships

- **mass_readings** ← `MassReading` (reverse FK)
- **lectionary_items** ← `LectionaryItem` (reverse FK)

---

### Common (Concrete Model)

**Location**: `site/churchcal/models.py:456-464`  
**Purpose**: Common of saints (generic reading sets for categories of saints)  
**Implements**: FR-008 (when specific saint has no proper readings)

#### Fields

| Field                    | Type                   | Description                             |
| ------------------------ | ---------------------- | --------------------------------------- |
| `abbreviation`           | CharField(256)         | Short code (PASTOR, MARTYR, etc.)       |
| `name`                   | CharField(256)         | Full name (e.g., "Of a Pastor")         |
| `collect_1`, `collect_2` | ForeignKey to Collect  | Generic collects for this category      |
| `collect_format_string`  | CharField(1024)        | Template for dynamic collect generation |
| `calendar`               | ForeignKey to Calendar | BCP 2019 calendar                       |

#### Relationships

- **mass_readings** ← `MassReading` (reverse FK)
- **lectionary_items** ← `LectionaryItem` (reverse FK)
- **saints** ← `SanctoraleCommemoration.common` (reverse FK)

---

## Scripture Storage Models

### Scripture (Concrete Model)

**Location**: `site/office/models.py:296-340`  
**Purpose**: Cache scripture text for all translations to enable offline access and performance  
**Implements**: FR-005, FR-006, FR-007, FR-010, FR-011, FR-016

#### Fields

| Field               | Type           | Constraints           | Description                                    |
| ------------------- | -------------- | --------------------- | ---------------------------------------------- |
| `passage`           | CharField(255) | required, unique      | Citation (e.g., "Genesis 1:1-31", "John 3:16") |
| `esv`               | TextField      | blank=True, null=True | English Standard Version text (HTML)           |
| `kjv`               | TextField      | blank=True, null=True | King James Version text (HTML)                 |
| `rsv`               | TextField      | blank=True, null=True | Revised Standard Version text (HTML)           |
| `nrsvce`            | TextField      | blank=True, null=True | NRSV Catholic Edition text (HTML)              |
| `nabre`             | TextField      | blank=True, null=True | New American Bible Revised Edition text (HTML) |
| `niv`               | TextField      | blank=True, null=True | New International Version text (HTML)          |
| `nasb`              | TextField      | blank=True, null=True | New American Standard Bible text (HTML)        |
| `coverdale`         | TextField      | blank=True, null=True | Coverdale Psalter text (HTML)                  |
| `renewed_coverdale` | TextField      | blank=True, null=True | Renewed Coverdale Psalter text (HTML)          |

#### HTML Structure

Scripture text stored as HTML with:

- `<p>` tags for paragraphs
- `<sup>` tags for verse numbers
- `<h3>`, `<h4>`, etc. for section headings (from Bible translation)
- Semantic HTML preserving translation's formatting

Example:

```html
<p>
  <sup>1</sup>In the beginning, God created the heavens and the earth.
  <sup>2</sup>The earth was without form and void...
</p>
<h3>The Creation of Light</h3>
<p><sup>3</sup>And God said, "Let there be light," and there was light.</p>
```

#### Methods

**`no_headings(markup)` (static method)**

- **Parameters**: HTML markup string
- **Returns**: Same markup with all heading tags (`<h1>` through `<h5>`) removed
- **Purpose**: Provide plain scripture text without section headings when desired
- **Implementation**: Uses BeautifulSoup to parse and remove heading tags

**Properties for Each Translation**

- `esv_no_headings`, `kjv_no_headings`, `rsv_no_headings`, etc.
- **Returns**: Translation text with section headings removed
- **Usage**: When rendering scripture without section heading clutter

#### Database Coverage

- **Records**: ~2000 unique passages (all Daily Office and major Eucharist readings)
- **Size**: ~18,000 text entries (2000 passages × 9 translations)
- **Indexing**: Indexed on `passage` for fast lookup

#### Query Patterns

```python
# Get scripture text for a citation
scripture = Scripture.objects.get(passage="Genesis 1:1-31")
esv_text = scripture.esv
nrsv_text = scripture.nrsvce

# Get scripture text without headings
esv_plain = scripture.esv_no_headings

# Bulk retrieve for multiple passages
citations = ["Genesis 1:1-31", "Psalm 1", "John 1:1-14"]
scriptures = Scripture.objects.filter(passage__in=citations)
scripture_dict = {s.passage: s for s in scriptures}
```

#### Relationships

- **Used by**: `OfficeDay` models (via passage citation matching)
- **Linked from**: `MassReading.long_scripture` and `MassReading.short_scripture` (ForeignKey)

---

## Model Relationships

### Entity-Relationship Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     DAILY OFFICE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   StandardOfficeDay ──(month/day)──> [specific date]       │
│          │                                                  │
│          └──inherits──> OfficeDay                          │
│                             │                               │
│                             ├─ mp_psalms (string)          │
│                             ├─ mp_reading_1 ───┐           │
│                             ├─ mp_reading_2 ───┼──> Scripture
│                             ├─ ep_reading_1 ───┤   (via citation)
│                             └─ ep_reading_2 ───┘           │
│                                                             │
│   HolyDayOfficeDay ──(FK)──> Commemoration                 │
│          │                        │                         │
│          └──inherits──> OfficeDay │                         │
│                                   │                         │
└───────────────────────────────────┼─────────────────────────┘
                                    │
┌───────────────────────────────────┼─────────────────────────┐
│                  EUCHARIST LECTIONARY                       │
├───────────────────────────────────┴─────────────────────────┤
│                                                             │
│   LectionaryItem ──(FK)──> Commemoration                   │
│        │         ──(FK)──> SanctoraleCommemoration          │
│        │         ──(FK)──> Proper                           │
│        │         ──(FK)──> Common                           │
│        │                                                     │
│        └──(reverse FK)──< MassReading                       │
│                               │                             │
│                               ├─ reading_type (prophecy/...) │
│                               ├─ years (A/B/C/ABC)          │
│                               ├─ long_scripture ──(FK)──┐   │
│                               └─ short_scripture ──(FK)─┼──> Scripture
│                                                         │   │
└─────────────────────────────────────────────────────────┼───┘
                                                          │
┌─────────────────────────────────────────────────────────┼───┐
│                  SCRIPTURE CACHE                        │   │
├─────────────────────────────────────────────────────────┴───┤
│                                                             │
│   Scripture                                                 │
│        ├─ passage (citation string) [INDEXED]              │
│        ├─ esv (HTML text)                                  │
│        ├─ kjv (HTML text)                                  │
│        ├─ rsv (HTML text)                                  │
│        ├─ nrsvce (HTML text)                               │
│        ├─ nabre (HTML text)                                │
│        ├─ niv (HTML text)                                  │
│        ├─ nasb (HTML text)                                 │
│        ├─ coverdale (HTML text)                            │
│        └─ renewed_coverdale (HTML text)                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Key Relationship Patterns

1. **OfficeDay → Scripture**: Indirect via citation string (no FK)

   - OfficeDay stores citation in `mp_reading_1`, `ep_reading_2`, etc.
   - Scripture lookup: `Scripture.objects.get(passage=citation)`
   - Rationale: Flexibility to reference passages not yet cached

2. **MassReading → Scripture**: Direct via ForeignKey

   - `long_scripture` FK for full reading
   - `short_scripture` FK for abbreviated alternative
   - Rationale: Pre-compute links during data import

3. **LectionaryItem → MassReading**: One-to-Many

   - One LectionaryItem has multiple MassReadings (1-4 typically)
   - MassReading.reading_number distinguishes position (1=OT, 2=Psalm, 3=Epistle, 4=Gospel typically)
   - MassReading.order handles alternatives at same position

4. **LectionaryItem → Commemoration/Proper/Common**: Polymorphic
   - Exactly one of these FKs must be set
   - Enables flexible reading assignment for different feast types
   - Query logic checks each in priority order

---

## Database Schema

### Indexes

**Critical indexes for performance (SC-001, SC-002, SC-005)**:

```sql
-- StandardOfficeDay fast lookup by date
CREATE INDEX office_standardofficeday_month_day_idx
ON office_standardofficeday (month, day);

-- Scripture fast lookup by citation
CREATE INDEX office_scripture_passage_idx
ON office_scripture (passage);

-- HolyDayOfficeDay fast lookup by commemoration
CREATE INDEX office_holydayofficeday_commemoration_idx
ON office_holydayofficeday (commemoration_id);

-- MassReading fast lookup by commemoration/proper/common
CREATE INDEX churchcal_massreading_commemoration_idx
ON churchcal_massreading (commemoration_id);
CREATE INDEX churchcal_massreading_proper_idx
ON churchcal_massreading (proper_id);
CREATE INDEX churchcal_massreading_common_idx
ON churchcal_massreading (common_id);

-- LectionaryItem fast lookup
CREATE INDEX office_lectionaryitem_commemoration_idx
ON office_lectionaryitem (commemoration_id);
CREATE INDEX office_lectionaryitem_sanctorale_commemoration_idx
ON office_lectionaryitem (sanctorale_commemoration_id);
```

### Storage Requirements

**Estimated database size**:

- **StandardOfficeDay**: 366 records × ~1 KB = ~366 KB
- **HolyDayOfficeDay**: ~150 records × ~1 KB = ~150 KB
- **ThirtyDayPsalterDay**: 30 records × ~0.5 KB = ~15 KB
- **Scripture**: ~2000 records × ~10 KB avg (HTML text) = ~20 MB
- **LectionaryItem**: ~600 records × ~0.5 KB = ~300 KB
- **MassReading**: ~2500 records × ~1 KB = ~2.5 MB
- **SanctoraleCommemoration**: ~400 records × ~2 KB = ~800 KB

**Total Lectionary Data**: ~25 MB (excluding collects, calendar metadata)

---

## Requirements Traceability

### Functional Requirements Mapping

| Requirement                                | Models                                 | Fields/Methods                                         | Notes                                                                       |
| ------------------------------------------ | -------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------- |
| FR-001: Daily Office reading assignments   | StandardOfficeDay, HolyDayOfficeDay    | All fields                                             | 366 standard days + feast days                                              |
| FR-002: Psalm assignments (60-day cycle)   | StandardOfficeDay, ThirtyDayPsalterDay | mp_psalms, ep_psalms                                   | 60-day in StandardOfficeDay, 30-day alternative in ThirtyDayPsalterDay      |
| FR-003: Two scripture readings per office  | OfficeDay                              | mp_reading_1, mp_reading_2, ep_reading_1, ep_reading_2 | Consistent structure                                                        |
| FR-004: Eucharist readings (3-year cycle)  | LectionaryItem, MassReading            | years field, year_a/b/c properties                     | Year-specific querying                                                      |
| FR-005: Full scripture text                | Scripture                              | Translation fields (esv, nrsv, etc.)                   | HTML-formatted, cached                                                      |
| FR-006: Multiple translations              | Scripture                              | 9 translation fields                                   | ESV, RSV, KJV, NRSV, NRSVCE, NABRE, NIV, NASB, Coverdale, Renewed Coverdale |
| FR-007: Translation selection              | (Frontend)                             | N/A                                                    | Model provides all translations; frontend selects                           |
| FR-008: Feast day proper readings          | HolyDayOfficeDay, LectionaryItem       | commemoration FK                                       | Feast-specific readings                                                     |
| FR-009: Office type indication             | OfficeDay, LectionaryItem              | Model structure, service field                         | Separate MP/EP fields; service distinguishes Eucharist types                |
| FR-010: Multi-chapter passages             | Scripture                              | passage field                                          | Citation parsing handles "Book C:V-C:V" format                              |
| FR-011: Discontinued passages              | Scripture                              | passage field                                          | Stored in citation string, Bible Gateway handles                            |
| FR-012: View any date                      | StandardOfficeDay                      | month, day fields                                      | Query by any month/day combination                                          |
| FR-013: Two-year Daily Office cycle        | StandardOfficeDay                      | (Calculation, not DB)                                  | Same records for Year 1/2; cycle calculated                                 |
| FR-014: Apocrypha fallback                 | OfficeDay, MassReading                 | testament field                                        | Frontend detects DC/AP testament, switches to NRSVCE                        |
| FR-015: Translation preference persistence | (Frontend)                             | N/A                                                    | LocalStorage, not model                                                     |
| FR-016: Clear citations                    | OfficeDay, MassReading                 | Reading fields store citation strings                  | Always visible                                                              |
| FR-017: Alternative/optional readings      | MassReading, LectionaryItem            | short_scripture, passages_for_year_and_number()        | " or " separator                                                            |

### Success Criteria Mapping

| Criterion                                            | Database Support                                       | Performance            |
| ---------------------------------------------------- | ------------------------------------------------------ | ---------------------- |
| SC-001: Display today's readings < 2 seconds         | Indexed lookup on (month, day)                         | ~5ms query             |
| SC-002: Full scripture text < 3 seconds              | Pre-cached in Scripture model                          | ~10ms query            |
| SC-003: Correct BCP 2019 assignments                 | Complete StandardOfficeDay + HolyDayOfficeDay coverage | N/A                    |
| SC-004: 95% of users read without external resources | All translations cached in Scripture                   | N/A                    |
| SC-005: Translation switching < 2 seconds            | All translations in same row                           | ~0ms (no query needed) |
| SC-006: Correct feast day readings                   | HolyDayOfficeDay + Commemoration relationship          | ~20ms query            |
| SC-007: Accurate scripture text                      | HTML from Bible Gateway, preserved                     | N/A                    |
| SC-008: Support 2 years past/future                  | StandardOfficeDay agnostic to year                     | N/A                    |
| SC-009: Translation preference persists              | (Frontend LocalStorage)                                | N/A                    |

---

## Data Import and Maintenance

### Import Commands

1. **`python manage.py import_office_days`** (hypothetical - not shown in excerpts)

   - Imports StandardOfficeDay records from CSV/JSON
   - Sources: BCP 2019 Daily Office Lectionary tables

2. **`python manage.py import_lectionary`** (`site/office/management/commands/import_lectionary.py`)

   - Imports LectionaryItem and MassReading records
   - Sources: BCP 2019 Eucharist Lectionary, Revised Common Lectionary

3. **`python manage.py import_scripture`** (`site/office/management/commands/import_scripture.py`)
   - Fetches scripture text from Bible Gateway API
   - Populates Scripture model for all lectionary passages
   - Iterates: OfficeDay readings + MassReading citations
   - Translations: esv, rsv, kjv, nrsvce, nabre, niv, nasb, coverdale, renewed_coverdale

### Data Maintenance

- **Scripture Cache Refresh**: Re-run `import_scripture` when Bible Gateway updates translations
- **Lectionary Updates**: Re-run import commands if BCP revises lectionary tables (rare)
- **New Translations**: Add column to Scripture model, update import command

---

## Conclusion

The lectionary data model architecture successfully supports:

- ✅ Dual lectionary cycles (2-year Daily Office, 3-year Eucharist)
- ✅ Multi-translation scripture text caching
- ✅ Feast precedence and proper reading handling
- ✅ Performance requirements via indexing and caching
- ✅ Offline access via database storage

**Future Enhancements** should maintain backward compatibility with existing data structure while addressing test coverage gaps and documentation needs outlined in plan.md.
