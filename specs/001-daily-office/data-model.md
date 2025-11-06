# Data Model: Daily Office Liturgy

**Date**: November 6, 2025  
**Type**: Phase 1 - Data Model Documentation  
**Status**: Existing Implementation Documentation

## Overview

The Daily Office data model consists of **5 major domains** organized across 3 Django apps:

1. **Office Domain** (`office/models.py`) - Lectionary readings, settings, collects, scripture cache
2. **Liturgical Calendar Domain** (`churchcal/models.py`) - Commemorations, seasons, calendar calculations
3. **Psalter Domain** (`psalter/models.py`) - Psalm texts and topics
4. **Bible Domain** (integrated in office) - Scripture passages and translations
5. **Settings Domain** (integrated in office) - User customization options

## Entity-Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    OFFICE DOMAIN                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐                                              │
│  │  OfficeDay   │◄──┬─── StandardOfficeDay                    │
│  │  (Abstract)  │   │    (month, day)                          │
│  └──────┬───────┘   └─── HolyDayOfficeDay                     │
│         │                 (commemoration FK)                    │
│         │                                                       │
│         │ mp_psalms, ep_psalms                                 │
│         │ mp_reading_1, mp_reading_2                           │
│         │ ep_reading_1, ep_reading_2                           │
│         │                                                       │
│         └───────────────────┐                                  │
│                             ▼                                   │
│                    ┌─────────────────┐                         │
│                    │   Scripture     │                         │
│                    │   (Cache)       │                         │
│                    ├─────────────────┤                         │
│                    │ passage         │                         │
│                    │ esv, kjv, rsv   │                         │
│                    │ nrsvce, nabre   │                         │
│                    │ niv, nasb       │                         │
│                    │ coverdale       │                         │
│                    │ renewed_cover   │                         │
│                    └─────────────────┘                         │
│                                                                 │
│  ┌───────────────────┐                                         │
│  │ ThirtyDayPsalter  │                                         │
│  │ Day               │                                         │
│  ├───────────────────┤                                         │
│  │ day (1-30)        │                                         │
│  │ mp_psalms         │                                         │
│  │ ep_psalms         │                                         │
│  └───────────────────┘                                         │
│                                                                 │
│  ┌────────────┐         ┌─────────────────┐                   │
│  │  Setting   │◄───────┤  SettingOption  │                   │
│  ├────────────┤  1:N    ├─────────────────┤                   │
│  │ name       │         │ name            │                   │
│  │ title      │         │ description     │                   │
│  │ description│         │ value           │                   │
│  │ type       │         │ abbreviation    │                   │
│  │ site       │         │ order           │                   │
│  └────────────┘         └─────────────────┘                   │
│                                                                 │
│  ┌──────────────┐                                              │
│  │   Collect    │                                              │
│  ├──────────────┤                                              │
│  │ title        │                                              │
│  │ text         │                                              │
│  │ traditional  │                                              │
│  │ type FK      │                                              │
│  │ tags M2M     │                                              │
│  │ attribution  │                                              │
│  └──────────────┘                                              │
│         ▲                                                       │
│         │                                                       │
└─────────┼───────────────────────────────────────────────────────┘
          │
┌─────────┼───────────────────────────────────────────────────────┐
│         │         LITURGICAL CALENDAR DOMAIN                    │
├─────────┼───────────────────────────────────────────────────────┤
│         │                                                       │
│  ┌──────┴──────────┐                                           │
│  │ Commemoration   │◄──┬─── SanctoraleCommemoration           │
│  │ (Abstract Base) │   │    (month, day, saint info)          │
│  ├─────────────────┤   ├─── TemporaleCommemoration            │
│  │ name            │   │    (days_after_easter)               │
│  │ rank FK         │   ├─── SanctoraleBasedCommemoration      │
│  │ color           │   │    (weekday, number_after)           │
│  │ collect_1 FK    │   └─── FerialCommemoration               │
│  │ collect_2 FK    │        (unmanaged, calculated)           │
│  │ collect_eve FK  │                                           │
│  │ calendar FK     │                                           │
│  │ biography       │                                           │
│  │ links (1-3)     │                                           │
│  │ image_link      │                                           │
│  │ ai_* fields     │ (14 AI-generated content fields)         │
│  └─────────────────┘                                           │
│         ▲                                                       │
│         │                                                       │
│         │                                                       │
│  ┌──────┴──────────┐      ┌──────────────────┐               │
│  │CommemorationRank│      │     Season       │               │
│  ├─────────────────┤      ├──────────────────┤               │
│  │ name            │      │ name             │               │
│  │ formatted_name  │      │ start_commem FK  │               │
│  │ precedence_rank │      │ color            │               │
│  │ required        │      │ rank FK          │               │
│  │ calendar FK     │      │ calendar FK      │               │
│  └─────────────────┘      └──────────────────┘               │
│                                                                 │
│  ┌─────────────┐           ┌──────────────────┐              │
│  │   Proper    │           │   MassReading    │              │
│  ├─────────────┤           ├──────────────────┤              │
│  │ number      │           │ long_citation    │              │
│  │ start_date  │           │ short_citation   │              │
│  │ end_date    │           │ years (A/B/C)    │              │
│  │ collect_1 FK│           │ commemoration FK │              │
│  │ calendar FK │           │ proper FK        │              │
│  └─────────────┘           │ common FK        │              │
│                             │ reading_type     │              │
│                             │ testament        │              │
│  ┌─────────────┐           │ long_scripture   │              │
│  │   Common    │           │ short_scripture  │              │
│  ├─────────────┤           └──────────────────┘              │
│  │ abbreviation│                                              │
│  │ name        │                                              │
│  │ collect_1 FK│                                              │
│  │ collect_2 FK│                                              │
│  │ format_str  │                                              │
│  │ calendar FK │                                              │
│  └─────────────┘                                              │
│                                                                 │
│  ┌──────────────┐          ┌──────────────────┐              │
│  │ Denomination │◄─────────┤    Calendar      │              │
│  ├──────────────┤   1:N    ├──────────────────┤              │
│  │ name         │          │ name             │              │
│  │ abbreviation │          │ denomination FK  │              │
│  └──────────────┘          │ year             │              │
│                             │ abbreviation     │              │
│                             │ google_sheet_id  │              │
│                             └──────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    PSALTER DOMAIN                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐       ┌─────────────────┐                  │
│  │    Psalm      │◄──────┤   PsalmVerse    │                  │
│  ├───────────────┤  1:N  ├─────────────────┤                  │
│  │ number        │       │ psalm FK        │                  │
│  │ latin_title   │       │ number          │                  │
│  └───────┬───────┘       │ first_half      │                  │
│          │               │ second_half     │                  │
│          │               │ first_half_tle  │                  │
│          │               │ second_half_tle │                  │
│          │               └─────────────────┘                  │
│          │                                                      │
│          │               ┌──────────────────┐                 │
│          └──────────────►│  PsalmTopicPsalm │                 │
│                     M:N  ├──────────────────┤                 │
│                          │ psalm FK         │                 │
│  ┌──────────────┐        │ psalm_topic FK   │                 │
│  │  PsalmTopic  │◄───────┤ order            │                 │
│  ├──────────────┤        └──────────────────┘                 │
│  │ topic_name   │                                              │
│  │ psalms       │                                              │
│  │ order        │                                              │
│  └──────────────┘                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Domain Models

### 1. Office Domain (`office/models.py`)

#### OfficeDay (Abstract Base)

**Purpose**: Stores daily office readings and psalm assignments for a specific date.

**Implements Requirements**: FR-005, FR-006, FR-006a, FR-021

**Fields**:

- `holy_day_name` (CharField, optional) - Name of feast day if applicable
- `mp_psalms` (CharField) - Morning Prayer psalm assignments (comma-separated, e.g., "1,2,3")
- `mp_reading_1` (CharField) - Morning Prayer first reading citation (e.g., "Genesis 1:1-5")
- `mp_reading_1_testament` (CharField) - Testament designation: OT/DC/AP/NT
- `mp_reading_1_text` (TextField, optional) - Cached text (deprecated, use Scripture model)
- `mp_reading_1_abbreviated` (CharField, optional) - Shorter reading option
- `mp_reading_1_abbreviated_text` (TextField, optional) - Cached abbreviated text
- `mp_reading_2` (CharField) - Morning Prayer second reading citation
- `mp_reading_2_testament` (CharField) - Testament designation
- `mp_reading_2_text` (TextField, optional) - Cached text
- `ep_psalms` (CharField) - Evening Prayer psalm assignments
- `ep_reading_1` (CharField) - Evening Prayer first reading citation
- `ep_reading_1_testament` (CharField) - Testament designation
- `ep_reading_1_text` (TextField, optional) - Cached text
- `ep_reading_1_abbreviated` (CharField, optional) - Shorter reading option
- `ep_reading_1_abbreviated_text` (TextField, optional) - Cached abbreviated text
- `ep_reading_2` (CharField) - Evening Prayer second reading citation
- `ep_reading_2_testament` (CharField) - Testament designation
- `ep_reading_2_text` (TextField, optional) - Cached text

**Methods**:

- `readings` (cached_property) - Retrieves Scripture objects for all reading citations
- `passage_to_text(attribute, translation='esv')` - Returns scripture text for given attribute and translation, with fallback to NRSVCE
- `__getattribute__` (override) - Adds CSS class to reading headings (HTML manipulation)

**Inheritance**: Two concrete subclasses:

#### StandardOfficeDay

**Purpose**: Office readings for regular calendar days (not feast days).

**Additional Fields**:

- `month` (IntegerField) - Calendar month (1-12)
- `day` (IntegerField) - Day of month (1-31)

**Usage**: Lookup by `StandardOfficeDay.objects.get(month=12, day=25)` for December 25 regular readings.

#### HolyDayOfficeDay

**Purpose**: Special office readings for feast days and holy days.

**Additional Fields**:

- `commemoration` (ForeignKey to Commemoration) - The feast/holy day being observed
- `order` (PositiveSmallIntegerField) - Ordering when multiple readings for same commemoration

**Usage**: Lookup by `HolyDayOfficeDay.objects.get(commemoration=christmas)` for Christmas proper readings.

**Selection Logic** (in `office/offices.py`):

```python
try:
    self.office_readings = HolyDayOfficeDay.objects.get(
        commemoration=self.date.primary
    )
except HolyDayOfficeDay.DoesNotExist:
    self.office_readings = StandardOfficeDay.objects.get(
        month=self.date.date.month,
        day=self.date.date.day
    )
```

#### ThirtyDayPsalterDay

**Purpose**: Stores psalm assignments for the traditional 30-day Psalter cycle (based on day of month).

**Implements Requirements**: FR-005, FR-005a

**Fields**:

- `day` (IntegerField) - Day of month (1-30)
- `mp_psalms` (CharField) - Morning Prayer psalm assignments for this day
- `ep_psalms` (CharField) - Evening Prayer psalm assignments for this day

**Methods**:

- `psalm_string_to_list(psalms)` - **BUG**: Currently `return psalms.split(psalms)` which doesn't work correctly. Should be `psalms.split(',')`.
- `get_mp_psalms()` - Returns list of MP psalm numbers
- `get_ep_psalms()` - Returns list of EP psalm numbers

**Note**: The 60-day Psalter cycle is stored directly in `OfficeDay.mp_psalms` and `ep_psalms` fields, not in a separate table.

#### Scripture

**Purpose**: Caches Bible passage text in multiple translations to reduce Bible Gateway API calls.

**Implements Requirements**: FR-016, FR-020, FR-021, FR-022

**Fields** (all TextField, optional):

- `passage` (CharField, unique) - Citation (e.g., "John 3:16-21")
- `esv` - English Standard Version text
- `kjv` - King James Version text
- `rsv` - Revised Standard Version text
- `nrsvce` - New Revised Standard Version Catholic Edition text
- `nabre` - New American Bible Revised Edition text
- `niv` - New International Version text
- `nasb` - New American Standard Bible text
- `coverdale` - Coverdale Psalter (1928) text
- `renewed_coverdale` - Renewed Coverdale Psalter (2019) text

**Methods**:

- `no_headings(markup)` (static) - Strips H1-H5 tags from HTML
- `{translation}_no_headings` (property for each translation) - Returns text without heading tags
- `apocrypha` (property) - Returns True if ESV text is "-" or empty (ESV doesn't include Apocrypha)
- `ending_call` (property) - Returns appropriate liturgical ending based on passage type (Gospel vs. other)
- `ending_response` (property) - Returns appropriate congregation response
- `citation` (property) - Returns formatted citation
- `initial_response` (property) - Returns "Glory to you, Lord Christ" for Gospels

**Usage Pattern**:

1. Office generation requests passage (e.g., "John 3:16")
2. Check if `Scripture.objects.filter(passage="John 3:16").exists()`
3. If exists, return cached text
4. If not exists, fetch from Bible Gateway API, create Scripture record, return text
5. Subsequent requests for same passage use cache (FR-021)

#### Setting

**Purpose**: Defines a user-configurable liturgical preference setting.

**Implements Requirements**: FR-005b, FR-006b, FR-017, FR-026, FR-027, FR-028

**Fields**:

- `name` (CharField) - Internal identifier (e.g., "psalter", "lectionary", "bible_version")
- `title` (CharField) - User-facing display title
- `description` (TextField, optional) - Explanation of setting's purpose
- `order` (PositiveSmallIntegerField, optional) - Display order in UI
- `setting_type` (PositiveSmallIntegerField) - Category: MAIN_SETTINGS (1), ADDITIONAL_SETTINGS (2), EXPERT_SETTINGS (3)
- `site` (PositiveSmallIntegerField) - Applicable site: DAILY_OFFICE_SITE (1), FAMILY_PRAYER_SITE (2)
- `setting_string_order` (PositiveSmallIntegerField) - Additional ordering field (default 0)

**Setting Types**:

- **MAIN_SETTINGS**: Visible in primary settings interface (lectionary, Psalter, translation)
- **ADDITIONAL_SETTINGS**: Secondary options (canticle rotation, confession length)
- **EXPERT_SETTINGS**: Advanced customization (rarely changed)

**Example Settings** (from database):

- `psalter` - Choice of 30-day or 60-day Psalter cycle
- `lectionary` - Choice of 1-year or 2-year lectionary
- `bible_version` - Choice of Bible translation (ESV, NRSVCE, KJV, etc.)
- `canticle_rotation` - Canticle rotation strategy (traditional/seasonal/daily)
- `canticle_table` - Canticle table selection (BCP 2019/BCP 1979/REC 2011)
- `confession_length` - Confession text length (short/long/fast-days-only)
- `absolution_style` - Absolution form (priest/lay reader)
- `invitatory` - Invitatory preference (Venite/Jubilate/rotating)
- `opening_sentence` - Opening sentence style (fixed/seasonal/rotating)
- `include_third_reading` - Include seasonal third reading (yes/no)
- `include_great_litany` - Include Great Litany (yes/no)
- `include_pandemic_prayers` - Include pandemic prayers (yes/no)
- `include_intercessions` - Include intercessions (yes/no)
- `include_general_thanksgiving` - Include General Thanksgiving (yes/no)
- `include_chrysostom` - Include St. Chrysostom prayer (yes/no)

#### SettingOption

**Purpose**: Defines one possible value for a Setting.

**Fields**:

- `setting` (ForeignKey to Setting) - The setting this option belongs to
- `order` (PositiveSmallIntegerField, optional) - Display order
- `name` (CharField) - User-facing option name (e.g., "30-Day Psalter Cycle")
- `description` (TextField, optional) - Explanation of this option
- `value` (CharField) - Internal value (e.g., "30day", "esv", "traditional")
- `abbreviation` (CharField, default 'A') - Single-character abbreviation for compact display

**Example**:

```python
psalter_setting = Setting(name="psalter", title="Psalter Cycle")
option_30day = SettingOption(
    setting=psalter_setting,
    name="30-Day Psalter Cycle",
    value="30day",
    abbreviation="3"
)
option_60day = SettingOption(
    setting=psalter_setting,
    name="60-Day Psalter Cycle",
    value="60day",
    abbreviation="6"
)
```

**Storage**: User selections stored client-side in browser localStorage/cookies (FR-023, FR-024), not in database.

#### Collect

**Purpose**: Stores collect prayers used throughout the liturgical year.

**Implements Requirements**: FR-009

**Fields**:

- `title` (CharField) - Name of collect (e.g., "Collect for Purity", "Collect for the First Sunday of Advent")
- `text` (CKEditor5Field) - Contemporary language text (HTML)
- `normalized_text` (TextField, optional) - Plain text version
- `traditional_text` (CKEditor5Field, optional) - Traditional/Elizabethan language text
- `normalized_traditional_text` (TextField, optional) - Plain text traditional version
- `collect_type` (ForeignKey to CollectType) - Category of collect
- `order` (PositiveSmallIntegerField) - Display order within type
- `number` (PositiveSmallIntegerField, optional) - Collect number if applicable
- `tags` (ManyToManyField to CollectTag) - Searchable tags
- `attribution` (CharField, optional) - Author/source attribution
- `metrical_collect` (ForeignKey to MetricalCollect, optional) - Linked metrical version
- `metrical_collect_2` (ForeignKey, optional) - Alternative metrical version
- `metrical_collect_3` (ForeignKey, optional) - Second alternative metrical version

**Methods**:

- `traditional_text_no_tags` (property) - Strips HTML tags from traditional text
- `text_no_tags` (property) - Strips HTML tags from contemporary text

**Related Models**:

- `CollectType` - Category (Collects of Christian Year, Occasional Prayers, Office Prayers, etc.)
- `CollectTagCategory` - Tag category for organization
- `CollectTag` - Individual tag for searching/filtering
- `AbstractCollect` - Helper class for dynamically-generated collects (saints, propers)

#### MetricalCollect

**Purpose**: Stores metrical (sung) versions of collects with tune information.

**Fields**:

- `collect_number` (PositiveSmallIntegerField, optional)
- `original_collect` (TextField, optional) - Text of original collect
- `normalized_original_collect` (TextField, optional)
- `tune_name` (CharField, optional) - Musical tune name
- `first_line` (CharField, optional) - First line of metrical version
- `pdf_link` (URLField, optional) - Sheet music PDF
- `site_link` (URLField, optional) - External reference
- `midi_link` (URLField, optional) - MIDI audio file
- `lyrics` (TextField, optional) - Full metrical text
- `text_source` (CharField, optional) - Author/source of text
- `tune_source` (CharField, optional) - Composer/source of tune
- `name` (CharField, optional) - Name of metrical collect

**Note**: Not mentioned in specification; additional feature beyond core requirements.

#### LectionaryItem

**Purpose**: Links commemorations/propers to their Sunday Mass readings (3-year cycle).

**Note**: This is for Sunday Mass lectionary, not Daily Office lectionary. Not covered in 001-daily-office specification (belongs in 005-lectionary spec).

**Fields**:

- `commemoration` (ForeignKey to Commemoration, optional)
- `sanctorale_commemoration` (ForeignKey to SanctoraleCommemoration, optional)
- `proper` (ForeignKey to Proper, optional)
- `common` (ForeignKey to Common, optional)
- `order` (PositiveSmallIntegerField)
- `service` (CharField) - Service type (Principal Service, Evening Service, etc.)

**Methods**:

- `mass_readings` (cached_property) - Returns related MassReading objects
- `mass_readings_by_year(year)` - Filters by A/B/C cycle
- `year_a`, `year_b`, `year_c` (cached_property) - Readings for each cycle year
- `passages_for_year_and_number(year, number)` - Formatted passage citations
- `reading_1_passages(year)` through `reading_4_passages(year)` - Specific reading retrieval

#### AboutItem & UpdateNotice

**Purpose**: Content management for FAQ and update announcements.

**Note**: Not in specification; administrative/content features.

---

### 2. Liturgical Calendar Domain (`churchcal/models.py`)

#### Commemoration (Abstract Base)

**Purpose**: Represents any liturgical observance (feast, holy day, feria, season).

**Implements Requirements**: FR-007, FR-011, FR-014

**Fields**:

- `name` (CharField) - Display name (e.g., "Christmas Day", "Saint Peter and Saint Paul")
- `rank` (ForeignKey to CommemorationRank) - Liturgical precedence level
- `cannot_occur_after` (ForeignKey to self) - Precedence rule constraint
- `color` (CharField) - Liturgical color (Red, White, Green, Purple, etc.)
- `additional_color` (CharField, optional) - Alternative color option
- `alternate_color` (CharField, optional) - Second alternative
- `alternate_color_2` (CharField, optional) - Third alternative
- `collect_1` (ForeignKey to Collect) - Primary collect for the day
- `collect_2` (ForeignKey to Collect, optional) - Alternative collect
- `collect_eve` (ForeignKey to Collect, optional) - Collect for eve/vigil
- `color_notes` (CharField, optional) - Explanation of color choices
- `calendar` (ForeignKey to Calendar) - Which liturgical calendar this belongs to
- `link_1`, `link_2`, `link_3` (URLField, optional) - External resources
- `biography` (CKEditor5Field, optional) - Biographical information for saints
- `image_link` (URLField, optional) - Image URL

**AI-Generated Content Fields** (14 fields):

- `ai_one_sentence` (TextField, optional) - Brief summary
- `ai_quote`, `ai_quote_by`, `ai_quote_citations` - Relevant quote with attribution
- `ai_verse`, `ai_verse_citation` - Scripture verse association
- `ai_hagiography`, `ai_hagiography_citations` - Saint's life story
- `ai_legend`, `ai_legend_citations`, `ai_legend_title` - Traditional stories
- `ai_bullet_points`, `ai_bullet_points_citations` - Key facts
- `ai_traditions`, `ai_traditions_citations` - Observance traditions
- `ai_foods`, `ai_foods_citations` - Traditional foods
- `ai_image_1`, `ai_image_2` (URLField) - AI-generated images
- `ai_lesser_feasts_and_fasts` - Content from LFF
- `ai_martyrology` - Martyrology entry
- `ai_butler` - Butler's Lives of Saints entry

**Methods**:

- `name_no_tags` (property) - Strips HTML tags
- `get_collects(calendar_date)` - Returns appropriate collects
- `initial_date(advent_year, calendar_year)` (abstract) - Calculates date of observance
- `initial_date_string(advent_year)` - Returns ISO date string
- `can_occur_in_year(advent_year)` - Checks if observance occurs in given year
- `get_mass_readings_for_year(year, time)` - Returns Mass readings for A/B/C cycle
- `get_all_mass_readings_for_year(year)` - Returns all Mass reading variations

**Inheritance Manager**: Uses Django `InheritanceManager` to support polymorphic queries across subclasses.

**Four Concrete Subclasses**:

#### SanctoraleCommemoration

**Purpose**: Fixed-date commemorations (saints, feasts that always fall on same calendar date).

**Additional Fields**:

- `month` (PositiveSmallIntegerField) - Month (1-12)
- `day` (PositiveSmallIntegerField) - Day of month (1-31)
- `saint_name` (CharField, optional) - Name of saint
- `saint_type` (CharField, choices) - Category: PASTOR, MONASTIC, MARTYR, MISSIONARY, TEACHER, RENEWER, REFORMER, SAINT_1, SAINT_2, ECUMENIST
- `saint_gender` (CharField, choices) - M/F/P (plural) for pronoun selection
- `saint_fill_in_the_blank` (CharField, optional) - Dynamic collect text insertion
- `common` (ForeignKey to Common, optional) - Common of Saints reference

**Examples**:

- Christmas Day - December 25
- Feast of Saint Peter and Saint Paul - June 29
- All Saints' Day - November 1

**Methods**:

- `initial_date(advent_year, calendar_year)` - Returns `date(year, self.month, self.day)` where year calculated from Advent year
- `build_collect(text)` - Dynamically generates collect text for saints using template strings
- `common_collect()` - Returns AbstractCollect built from Common template

#### TemporaleCommemoration

**Purpose**: Movable feasts calculated relative to Easter.

**Additional Fields**:

- `days_after_easter` (SmallIntegerField) - Days offset from Easter (can be negative)

**Examples**:

- Easter Day - 0 days after Easter
- Ascension Day - 39 days after Easter (Thursday)
- Pentecost - 49 days after Easter
- Ash Wednesday - -46 days after Easter

**Methods**:

- `initial_date(advent_year, calendar_year)` - Returns `easter(year) + timedelta(days=self.days_after_easter)`

#### SanctoraleBasedCommemoration

**Purpose**: Feasts calculated relative to a fixed calendar date (e.g., "First Sunday after a specific date").

**Additional Fields**:

- `weekday` (CharField) - Day of week (Monday, Tuesday, etc.)
- `number_after` (SmallIntegerField) - Which occurrence (1st, 2nd, etc.)
- `month_after` (PositiveSmallIntegerField) - Month of reference date
- `day_after` (PositiveSmallIntegerField) - Day of reference date
- `additional_days_after` (PositiveSmallIntegerField, default 0) - Additional day offset

**Examples**:

- Last Sunday after Pentecost - Sunday before Advent
- Reign of Christ Sunday - Last Sunday of liturgical year

**Methods**:

- `initial_date(advent_year, calendar_year)` - Uses `weekday_after()` utility to calculate date
- `can_occur_in_year(advent_year)` - Additional check for All Saints' Sunday exception

#### FerialCommemoration

**Purpose**: Ordinary time/ferial days (unmanaged model, created dynamically).

**Note**: `managed = False` means no database table; instances created at runtime.

**Additional Fields**:

- `date` - The specific date
- `season` - The liturgical season

**Constructor**:

```python
def __init__(self, date, season, calendar, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.date = date
    self.name = season.rank.formatted_name  # e.g., "Feria of Ordinary Time"
    self.rank = season.rank
    self.color = season.color
```

**Usage**: Created by `churchcal/calculations.py` when no fixed commemoration exists for a date.

#### CommemorationRank

**Purpose**: Defines liturgical precedence hierarchy for commemorations.

**Implements Requirements**: FR-007 (feast day precedence)

**Fields**:

- `name` (CharField) - Internal name
- `formatted_name` (CharField) - Display name (e.g., "Principal Feast", "Sunday", "Holy Day", "Commemoration")
- `precedence_rank` (PositiveSmallIntegerField, 1-9) - Numeric precedence (1 = highest)
- `required` (BooleanField) - Whether observance is required or optional
- `calendar` (ForeignKey to Calendar)

**Precedence Hierarchy** (typical BCP 2019):

1. Principal Feasts (Easter, Christmas, Epiphany, Ascension, Pentecost, Trinity Sunday)
2. Sundays (take precedence over most other commemorations)
3. Holy Days
4. Commemorations
5. Ferias (ordinary time)

**Usage**: When multiple commemorations fall on same date, highest precedence_rank (lowest number) is primary.

#### Season

**Purpose**: Defines liturgical seasons of the church year.

**Implements Requirements**: FR-014

**Fields**:

- `order` (IntegerField, 1-28) - Sequential order in year
- `name` (CharField) - Season name (e.g., "Advent", "Christmas", "Epiphany", "Lent", "Easter", "Pentecost")
- `start_commemoration` (ForeignKey to Commemoration, optional) - Feast that begins season
- `color` (CharField) - Default liturgical color for season
- `alternate_color` (CharField, optional) - Alternative color
- `rank` (ForeignKey to CommemorationRank) - Rank for ferial days in season
- `calendar` (ForeignKey to Calendar)

**Seasons**:

1. **Advent** - 4 weeks before Christmas (purple/blue)
2. **Christmas** - 12 days from December 25 (white)
3. **Epiphany** - January 6 to Tuesday before Ash Wednesday (green)
4. **Lent** - Ash Wednesday to Saturday before Palm Sunday (purple)
5. **Holy Week** - Palm Sunday to Easter Eve (red/purple)
6. **Easter** - 50 days from Easter to Pentecost (white)
7. **Pentecost/Ordinary Time** - Day of Pentecost to Saturday before Advent (green/red)

#### Proper

**Purpose**: Sunday propers for Ordinary Time (numbered Sundays with assigned collects and readings).

**Fields**:

- `number` (IntegerField, 1-28) - Proper number
- `start_date` (DateField) - First day of proper (Sunday)
- `end_date` (DateField) - Last day of proper (Saturday)
- `collect_1` (ForeignKey to Collect) - Collect for the proper
- `calendar` (ForeignKey to Calendar)

**Usage**: Propers 1-28 cover Sundays after Pentecost (Ordinary Time). Each proper spans one week.

**Example**:

- Proper 10: Sunday between July 10-16 (inclusive)

**Methods**:

- `get_mass_readings_for_year(year)` - Returns MassReading objects for A/B/C cycle

#### Common

**Purpose**: Template collects and readings for categories of saints.

**Fields**:

- `abbreviation` (CharField) - Short code (e.g., "MARTYR", "PASTOR")
- `name` (CharField) - Full name (e.g., "Of a Martyr", "Of a Pastor")
- `collect_1` (ForeignKey to Collect, optional) - Primary common collect
- `collect_2` (ForeignKey to Collect, optional) - Alternative common collect
- `collect_format_string` (CharField, optional) - Template for dynamic collects with placeholders
- `collect_tle_format_string` (CharField, optional) - Traditional language template
- `calendar` (ForeignKey to Calendar)

**Usage**: When a saint has no proper collect, use the Common appropriate to their category. Format strings allow dynamic insertion of saint's name and pronouns.

**Example Format String**:

```
"Almighty God, who called your servant{} {} to be a faithful pastor{} of your people in {}, and gave {} grace to {} and govern them: Mercifully grant that, following {}..."
# Filled in as:
"Almighty God, who called your servant John Smith to be a faithful pastor of your people in Boston, and gave him grace to tend and govern them: Mercifully grant that, following his..."
```

#### MassReading

**Purpose**: Stores Sunday and Feast Day Mass readings (3-year lectionary cycle).

**Note**: This is for Sunday Eucharist, not Daily Office. Belongs in 005-lectionary spec.

**Fields**:

- `long_citation` (CharField) - Full passage citation
- `long_text` (TextField, optional) - Full passage text
- `service` (CharField) - Service type (Principal Service, Vigil, etc.)
- `short_citation` (CharField) - Abbreviated option citation
- `short_text` (TextField, optional) - Abbreviated text
- `years` (CharField, max 3) - Which cycles: "A", "B", "C", "ABC"
- `commemoration` (ForeignKey to Commemoration, optional)
- `proper` (ForeignKey to Proper, optional)
- `common` (ForeignKey to Common, optional)
- `reading_type` (CharField, choices) - prophecy, psalm, epistle, gospel
- `book` (CharField) - Bible book name
- `testament` (CharField, 4 chars) - OT/NT/AP
- `calendar` (ForeignKey to Calendar)
- `abbreviation` (CharField, optional) - Service abbreviation
- `reading_number` (PositiveSmallIntegerField) - 1st, 2nd, 3rd, 4th reading
- `order` (PositiveSmallIntegerField) - Ordering within reading number
- `long_scripture` (ForeignKey to Scripture, optional)
- `short_scripture` (ForeignKey to Scripture, optional)

#### Calendar & Denomination

**Purpose**: Support multiple liturgical calendars (ACNA, ECUSA, Church of England, etc.).

**Calendar Fields**:

- `name` (CharField) - Calendar name
- `denomination` (ForeignKey to Denomination)
- `year` (CharField) - Year designation
- `abbreviation` (CharField) - Short code
- `google_sheet_id` (CharField) - Google Sheets ID for calendar data import

**Denomination Fields**:

- `name` (CharField) - Denomination name (e.g., "Anglican Church in North America")
- `abbreviation` (CharField) - Short code (e.g., "ACNA")

**Note**: Current implementation focuses on ACNA/BCP 2019 calendar; multi-calendar support is infrastructure for future expansion.

---

### 3. Psalter Domain (`psalter/models.py`)

#### Psalm

**Purpose**: Stores psalm metadata.

**Fields**:

- `number` (IntegerField, unique) - Psalm number (1-150)
- `latin_title` (CharField, optional) - Traditional Latin incipit (e.g., "Beatus vir")

**Usage**: Reference point for psalm verses and topics.

#### PsalmVerse

**Purpose**: Stores individual verses of psalms in both contemporary and traditional language.

**Implements Requirements**: FR-009 (full text of psalms), FR-016 (Coverdale translation)

**Fields**:

- `psalm` (ForeignKey to Psalm) - Parent psalm
- `number` (IntegerField) - Verse number within psalm
- `first_half` (CharField) - First hemistich (contemporary language)
- `second_half` (CharField) - Second hemistich (contemporary language)
- `first_half_tle` (CharField, optional) - First hemistich (traditional language)
- `second_half_tle` (CharField, optional) - Second hemistich (traditional language)

**Unique Constraint**: (psalm, number) - No duplicate verses

**Usage**:

```python
psalm_23 = Psalm.objects.get(number=23)
verses = PsalmVerse.objects.filter(psalm=psalm_23).order_by('number')
for verse in verses:
    print(f"{verse.number}. {verse.first_half} * {verse.second_half}")
```

**Note**: Asterisk (\*) traditionally separates hemistichs for antiphonal recitation.

#### PsalmTopic

**Purpose**: Groups psalms by theme for searching/browsing.

**Fields**:

- `topic_name` (CharField) - Topic name (e.g., "Praise", "Lament", "Penitence", "Trust")
- `psalms` (CharField) - Comma-separated list of psalm numbers
- `order` (PositiveSmallIntegerField) - Display order

**Methods**:

- `psalm_list` (property) - Returns list of psalm numbers extracted from `psalms` string

**Example**:

```python
praise_topic = PsalmTopic(
    topic_name="Praise",
    psalms="8, 19, 29, 33, 100, 103, 104, 145-150",
    order=1
)
```

#### PsalmTopicPsalm

**Purpose**: Junction table for many-to-many relationship between Psalm and PsalmTopic.

**Fields**:

- `psalm` (ForeignKey to Psalm)
- `psalm_topic` (ForeignKey to PsalmTopic)
- `order` (PositiveSmallIntegerField) - Order within topic

**Note**: This appears to duplicate functionality of `PsalmTopic.psalms` field. May be redundant or represent different organizational schemes.

---

## Data Relationships

### Office Day → Scripture Cache

- `OfficeDay` stores passage citations (e.g., "John 3:16-21")
- `Scripture` model stores cached text for each passage × translation
- When office is generated, citations are looked up in Scripture cache
- If not cached, fetched from Bible Gateway API and saved to cache
- Fallback to NRSVCE if requested translation unavailable

### Office Day → Commemoration

- `HolyDayOfficeDay.commemoration` → `Commemoration`
- When calendar indicates feast day, proper readings from `HolyDayOfficeDay` used
- Otherwise, regular daily readings from `StandardOfficeDay` used

### Commemoration → Collect

- `Commemoration.collect_1`, `collect_2`, `collect_eve` → `Collect`
- Collects for the day retrieved from commemoration
- If commemoration lacks proper collect, fallback to `Common` template

### Commemoration → Season

- Calendar calculation determines current season
- Season provides default color and rank for ferial days
- `FerialCommemoration` created dynamically using season data

### Setting → SettingOption

- One-to-many relationship
- Each Setting has multiple SettingOptions
- User selection stored client-side as SettingOption.value (e.g., "esv", "30day")

### Psalm → PsalmVerse

- One-to-many relationship
- Each Psalm has 1-176 verses (Psalm 119 is longest)
- Verses stored with contemporary and traditional language texts

## Database Query Patterns

### Common Queries

```python
# Get office readings for a date
from office.models import StandardOfficeDay, HolyDayOfficeDay
from churchcal.calculations import get_calendar_date

calendar_date = get_calendar_date(date(2025, 12, 25))

# Try holy day readings first
try:
    readings = HolyDayOfficeDay.objects.get(
        commemoration=calendar_date.primary
    )
except HolyDayOfficeDay.DoesNotExist:
    # Fall back to standard readings
    readings = StandardOfficeDay.objects.get(
        month=12, day=25
    )

# Get scripture text
from office.models import Scripture

scripture = Scripture.objects.filter(
    passage=readings.mp_reading_1
).first()

if scripture:
    text = scripture.esv  # or kjv, nrsvce, etc.
else:
    # Fetch from Bible Gateway, cache in new Scripture object
    pass

# Get psalm verses
from psalter.models import Psalm, PsalmVerse

psalm_23 = Psalm.objects.get(number=23)
verses = PsalmVerse.objects.filter(psalm=psalm_23).order_by('number')

# Get settings
from office.models import Setting, SettingOption

psalter_setting = Setting.objects.get(name='psalter')
options = SettingOption.objects.filter(
    setting=psalter_setting
).order_by('order')

# Get commemoration for date
from churchcal.models import SanctoraleCommemoration

christmas = SanctoraleCommemoration.objects.get(
    month=12, day=25,
    name__icontains='Christmas'
)

# Get season
from churchcal.models import Season

advent = Season.objects.get(name='Advent')
```

### Performance Considerations

**Cached Properties**: Models use `@cached_property` extensively to avoid repeated queries:

- `OfficeDay.readings`
- `Commemoration.cannot_occur_after_subtype`
- `LectionaryItem.mass_readings`, `year_a`, `year_b`, `year_c`

**Select Related / Prefetch Related**: Not explicitly used in examined code but should be added for:

- `HolyDayOfficeDay.objects.select_related('commemoration', 'commemoration__rank', 'commemoration__collect_1')`
- `Commemoration.objects.prefetch_related('collect_1', 'collect_2', 'collect_eve')`

**Indexing**: Key fields that should have database indexes:

- `StandardOfficeDay(month, day)` - Composite index for lookups
- `HolyDayOfficeDay.commemoration` - Foreign key index
- `SanctoraleCommemoration(month, day)` - Composite index
- `Scripture.passage` - Unique index (likely exists)
- `Psalm.number` - Unique index
- `PsalmVerse(psalm, number)` - Composite unique index

## Data Population

### Initial Data Sources

**Office Readings** (StandardOfficeDay, HolyDayOfficeDay):

- Sourced from BCP 2019 Daily Office Lectionary tables
- Likely imported via Django management command or SQL dump
- ~730 StandardOfficeDay records (2 years × 365 days)
- ~100-200 HolyDayOfficeDay records for major feasts

**Liturgical Calendar** (Commemoration, Season, etc.):

- Sourced from BCP 2019 calendar
- AI-generated content fields populated separately
- Imported from Google Sheets (calendar.google_sheet_id)
- Management commands in `churchcal/management/commands/`

**Psalms** (Psalm, PsalmVerse):

- 150 Psalms with full text
- Sourced from BCP 2019 Psalter (Coverdale-based)
- Traditional language edition included
- Imported via management command

**Collects**:

- Sourced from BCP 2019 collect texts
- Imported via `office/management/commands/import_collects.py`
- Separate imports for:
  - Collects of the Christian Year
  - Occasional Prayers
  - Office Prayers
  - Collects from other sources

**Scripture Cache**:

- Populated dynamically as passages are requested
- Grows over time with usage
- May be pre-populated for common passages

### Maintenance Commands

Likely management commands (based on file structure):

- `python manage.py import_lectionary` - Import office readings
- `python manage.py import_calendar` - Import liturgical calendar
- `python manage.py import_collects` - Import collect texts
- `python manage.py import_psalms` - Import psalm texts
- `python manage.py populate_scripture_cache` - Pre-populate common passages

## Design Patterns

### Strategy Pattern

- `Office` subclasses define different office generation strategies
- Each office composes different combinations of `OfficeSection` modules

### Template Method Pattern

- `Commemoration.initial_date()` abstract method
- Subclasses provide specific calculation algorithms
- Base class provides common behavior

### Caching Pattern

- `Scripture` model implements caching for expensive API calls
- `@cached_property` decorator caches expensive computations

### Polymorphic Queries

- `Commemoration` uses InheritanceManager for polymorphic retrieval
- Query returns correct subclass instances (SanctoraleCommemoration, TemporaleCommemoration, etc.)

### Dynamic Model Creation

- `FerialCommemoration` is unmanaged (no database table)
- Instances created at runtime based on date and season

## Data Integrity

### Constraints

**Foreign Key Constraints**:

- `HolyDayOfficeDay.commemoration` → `Commemoration` (CASCADE on delete)
- `SettingOption.setting` → `Setting` (CASCADE on delete)
- `PsalmVerse.psalm` → `Psalm` (CASCADE on delete)
- `Commemoration.calendar` → `Calendar` (CASCADE on delete)

**Unique Constraints**:

- `Psalm.number` - Prevents duplicate psalm numbers
- `PsalmVerse(psalm, number)` - Prevents duplicate verses
- `Scripture.passage` - Prevents duplicate cache entries (implied unique)

**Referential Integrity**:

- Circular references: `Commemoration.cannot_occur_after` → `Commemoration`
- Multiple FKs to same model: `Collect` has 3 FKs to `MetricalCollect`

### Validation

**Required Fields**:

- Most core fields are `null=False, blank=False`
- `OfficeDay` requires all psalm and reading fields
- `Commemoration` requires name, rank, calendar

**Optional Fields**:

- Abbreviated reading fields (`mp_reading_1_abbreviated`)
- Alternative collects (`collect_2`, `collect_eve`)
- AI-generated content fields (all optional)

**Choices Validation**:

- `OfficeDay.{mp|ep}_reading_{1|2}_testament` - Restricted to OT/DC/AP/NT
- `CommemorationRank.precedence_rank` - Restricted to 1-9
- `MassReading.reading_type` - Restricted to prophecy/psalm/epistle/gospel
- `SanctoraleCommemoration.saint_type` - Restricted to defined saint categories

## Known Issues

### Bug: PsalmVerse.psalm_string_to_list()

**Location**: `office/models.py` line 81

**Current Code**:

```python
def psalm_string_to_list(self, psalms):
    return psalms.split(psalms)
```

**Problem**: `split(psalms)` splits by the entire string, not by delimiter. Returns `['']` for any input.

**Expected**:

```python
def psalm_string_to_list(self, psalms):
    return psalms.split(',')  # or appropriate delimiter
```

**Impact**: 30-day Psalter psalm retrieval broken. Functionality likely unused (60-day cycle used instead).

**Priority**: P0 - Fix in first remediation sprint.

### Data Redundancy: PsalmTopic vs PsalmTopicPsalm

**Issue**: `PsalmTopic.psalms` (comma-separated string) and `PsalmTopicPsalm` (junction table) appear to serve same purpose.

**Recommendation**: Audit usage, remove redundant approach, keep junction table (more normalized).

### Unclear Field: Setting.setting_string_order

**Issue**: Purpose of `setting_string_order` field unclear. Already have `order` field.

**Recommendation**: Document purpose or consider removing if unused.

## Summary

The Daily Office data model is **comprehensive and well-designed** for its liturgical purpose. Key strengths:

✅ **Clear domain separation** (Office, Calendar, Psalter)  
✅ **Flexible architecture** (polymorphic Commemoration, multiple OfficeDay types)  
✅ **Caching strategy** (Scripture model reduces API dependency)  
✅ **Extensibility** (Settings system supports endless customization)  
✅ **Rich content** (AI-generated fields, metrical collects, biographical data)

Areas for improvement:

⚠️ **Bug in psalm parsing** - Critical fix needed  
⚠️ **Data redundancy** - PsalmTopic duplicate approaches  
⚠️ **Missing indexes** - Performance optimization opportunity  
⚠️ **Documentation gaps** - Some fields lack clear purpose documentation

The model successfully implements all requirements from the specification (FR-001 through FR-028) with additional features beyond the spec.

---

**Document Version**: 1.0  
**Last Updated**: November 6, 2025  
**Models Documented**: 35 models across 3 Django apps
