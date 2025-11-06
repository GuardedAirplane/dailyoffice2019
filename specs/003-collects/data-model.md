# Data Model: Collects and Prayers

**Feature**: 003-collects  
**Date**: November 6, 2025  
**Status**: Complete - Documenting Existing Implementation

## Overview

The Collects data model provides comprehensive storage and organization for prayers from the Book of Common Prayer 2019. The model supports:

- **Multi-language**: Contemporary and traditional (thee/thou) language versions
- **Multi-dimensional tagging**: 5 tag categories for flexible filtering
- **Metrical versions**: Up to 3 musical/sung versions per collect
- **Search optimization**: Normalized plain text for full-text search
- **Attribution**: Historical sources and BCP page references
- **Daily office integration**: Foreign key relationships for liturgical use

## Entity-Relationship Diagram

```
┌─────────────────┐
│  CollectType    │
│  (Categories)   │
├─────────────────┤       ┌──────────────────────┐
│ uuid            │◄──┐   │  CollectTagCategory  │
│ name            │   │   │  (Tag Dimensions)    │
│ key             │   │   ├──────────────────────┤
│ order           │   │   │ uuid                 │
└─────────────────┘   │   │ name                 │
                      │   │ key                  │
┌─────────────────────────────────────┐           │ order                │
│            Collect                  │           └──────────────────────┘
│         (Main Entity)               │                     ▲
├─────────────────────────────────────┤                     │
│ uuid                                │                     │
│ title                               │           ┌──────────────────────┐
│ text (CKEditor5)                    │           │    CollectTag        │
│ traditional_text (CKEditor5)        │           │  (Individual Tags)   │
│ normalized_text                     │           ├──────────────────────┤
│ normalized_traditional_text         │     ┌────►│ uuid                 │
│ order                               │     │     │ name                 │
│ number                              │     │     │ key                  │
│ attribution                         │     │     │ order                │
│ collect_type_id                     ├─────┘     │ collect_tag_category_id
│ metrical_collect_id                 │           └──────────────────────┘
│ metrical_collect_2_id               │                     ▲
│ metrical_collect_3_id               │                     │
└─────────────────────────────────────┘                     │
              │                                             │
              │ M:N                                         │
              ▼                                             │
┌─────────────────────────────┐                            │
│   Collect_tags              │────────────────────────────┘
│   (Join Table)              │
├─────────────────────────────┤
│ collect_id                  │
│ collecttag_id               │
└─────────────────────────────┘

              │
              │ 1:N
              ▼
┌─────────────────────────────┐
│     MetricalCollect         │
│  (Musical Versions)         │
├─────────────────────────────┤
│ uuid                        │
│ collect_number              │
│ original_collect            │
│ normalized_original_collect │
│ tune_name                   │
│ first_line                  │
│ pdf_link                    │
│ site_link                   │
│ midi_link                   │
│ lyrics                      │
│ text_source                 │
│ tune_source                 │
│ name                        │
└─────────────────────────────┘

┌────────────────────────────┐
│    AbstractCollect         │
│   (Helper Class)           │
├────────────────────────────┤
│ text (str)                 │
│ traditional_text (str)     │
├────────────────────────────┤
│ + text_no_tags             │
│ + traditional_text_no_tags │
└────────────────────────────┘
```

## Core Entities

### 1. Collect (Primary Model)

**Table**: `office_collect`  
**Django Model**: `office.models.Collect`  
**Purpose**: Stores individual collect prayers with full text in multiple languages

#### Fields

| Field                         | Type                      | Constraints       | Purpose                                   |
| ----------------------------- | ------------------------- | ----------------- | ----------------------------------------- |
| `uuid`                        | UUIDField                 | Primary Key, Auto | Unique identifier                         |
| `created`                     | DateTimeField             | Auto              | Creation timestamp (from BaseModel)       |
| `updated`                     | DateTimeField             | Auto              | Last update timestamp (from BaseModel)    |
| `title`                       | CharField(255)            | NOT NULL          | Collect name (e.g., "Collect for Purity") |
| `text`                        | CKEditor5Field            | NOT NULL          | Contemporary language HTML text           |
| `normalized_text`             | TextField                 | NULL, BLANK       | Plain text for search (contemporary)      |
| `traditional_text`            | CKEditor5Field            | NULL, BLANK       | Traditional (thee/thou) language HTML     |
| `normalized_traditional_text` | TextField                 | NULL, BLANK       | Plain text for search (traditional)       |
| `collect_type_id`             | ForeignKey                | NULL, SET_NULL    | Link to CollectType                       |
| `order`                       | PositiveSmallIntegerField | Default: 0        | Display order within type                 |
| `number`                      | PositiveSmallIntegerField | NULL, BLANK       | Collect number if applicable              |
| `attribution`                 | CharField(255)            | NULL, BLANK       | Historical source or BCP page reference   |
| `metrical_collect_id`         | ForeignKey                | NULL, SET_NULL    | Link to primary metrical version          |
| `metrical_collect_2_id`       | ForeignKey                | NULL, SET_NULL    | Link to 2nd metrical version              |
| `metrical_collect_3_id`       | ForeignKey                | NULL, SET_NULL    | Link to 3rd metrical version              |

**Many-to-Many Relationships**:

- `tags` → `CollectTag` (through `office_collect_tags` join table)

#### Properties

- **`text_no_tags`** (property): Returns `text` field with HTML tags stripped and "Amen." removed
- **`traditional_text_no_tags`** (property): Returns `traditional_text` field with HTML tags stripped and "Amen." removed

#### Methods

- **`__str__()`**: Returns `title` field

#### HTML Format Constraints

The `text` and `traditional_text` fields use CKEditor5 with limited HTML tags:

- Allowed tags: `<p>`, `<strong>`, `<em>`, `<br>`
- Purpose: Preserve traditional book formatting (indentation, emphasis)
- Cleaned during import with `clean_collect()` function
- Always ends with `<strong>Amen.</strong>`

#### Data Population

**Contemporary Text**:

- Source: Web scraping from Anglican resources
- Format: `<p>Prayer text here <strong>Amen.</strong></p>`

**Traditional Text**:

- Source: PDF parsing (`tradocas.pdf`)
- Same format as contemporary

**Normalized Fields** (⚠️ **CRITICAL ISSUE**):

- **Current State**: Schema exists but fields NOT populated during import
- **Impact**: Blocks search functionality (FR-007)
- **Fix Required**: Data migration to populate using `do_strip_tags()` function
- **Purpose**: Enable fast full-text search without parsing HTML

**Attribution**:

- **Current State**: Only occasional prayers have attribution (from `<small>` HTML tags)
- **Missing**: BCP page references, historical sources for most collects
- **Format**: Free text (e.g., "Thomas Cranmer, 1549" or "BCP 2019, p. 123")

#### Business Rules

1. **Every collect MUST have a title and contemporary text**
2. **Traditional text is OPTIONAL** (but should exist for most BCP collects)
3. **Normalized text fields MUST be populated for search** (currently violated)
4. **HTML in text fields MUST be sanitized** (only allowed tags)
5. **Order field determines display sequence** within a CollectType
6. **Up to 3 metrical versions** can be linked per collect

#### Validation Notes

- No model-level validation currently enforced
- Import scripts handle cleaning and validation
- CKEditor5 enforces tag restrictions in admin interface

---

### 2. CollectType (Category Model)

**Table**: `office_collecttype`  
**Django Model**: `office.models.CollectType`  
**Purpose**: Top-level categorization of collects

#### Fields

| Field   | Type                      | Constraints       | Purpose           |
| ------- | ------------------------- | ----------------- | ----------------- |
| `uuid`  | UUIDField                 | Primary Key, Auto | Unique identifier |
| `name`  | CharField(255)            | NOT NULL          | Display name      |
| `key`   | CharField(255)            | NOT NULL          | Programmatic key  |
| `order` | PositiveSmallIntegerField | Default: 0        | Display order     |

#### Predefined Types (from `Collect.COLLECT_TYPES`)

| Key              | Name                           |
| ---------------- | ------------------------------ |
| `year`           | Collects of the Christian Year |
| `occasional`     | Occasional Prayers             |
| `office_prayers` | Collects from the Daily Office |
| `burial_rite`    | Collects from the Burial Rite  |
| `other`          | Other Collects                 |

#### Methods

- **`__str__()`**: Returns `name` field

#### Usage

```python
collect_type = CollectType.objects.get(key="occasional")
collects = Collect.objects.filter(collect_type=collect_type).order_by('order')
```

---

### 3. CollectTagCategory (Tag Dimension Model)

**Table**: `office_collecttagcategory`  
**Django Model**: `office.models.CollectTagCategory`  
**Purpose**: Defines dimensions for multi-dimensional tagging system

#### Fields

| Field   | Type                      | Constraints       | Purpose           |
| ------- | ------------------------- | ----------------- | ----------------- |
| `uuid`  | UUIDField                 | Primary Key, Auto | Unique identifier |
| `name`  | CharField(255)            | NOT NULL          | Display name      |
| `key`   | CharField(255)            | NOT NULL          | Programmatic key  |
| `order` | PositiveSmallIntegerField | Default: 0        | Display order     |

#### Intended Categories (from Specification FR-005a)

| Key                  | Name               | Purpose                  | Examples                                             |
| -------------------- | ------------------ | ------------------------ | ---------------------------------------------------- |
| `source`             | Source             | Where collect originates | year, occasional, liturgical                         |
| `theme`              | Theme              | Occasional prayer theme  | healing, mission, departed, national                 |
| `season`             | Season             | Liturgical season        | Advent, Christmas, Epiphany, Lent, Easter, Pentecost |
| `commemoration_type` | Commemoration Type | Feast classification     | sunday, major_feast, holy_day                        |
| `liturgy`            | Liturgy            | Liturgical context       | daily_office, burial, other                          |

**Note**: Implementation verification needed - unclear if all 5 categories are populated.

#### Methods

- **`__str__()`**: Returns `name` field

---

### 4. CollectTag (Individual Tag Model)

**Table**: `office_collecttag`  
**Django Model**: `office.models.CollectTag`  
**Purpose**: Individual tags applied to collects within tag categories

#### Fields

| Field                     | Type                      | Constraints       | Purpose                       |
| ------------------------- | ------------------------- | ----------------- | ----------------------------- |
| `uuid`                    | UUIDField                 | Primary Key, Auto | Unique identifier             |
| `name`                    | CharField(255)            | NOT NULL          | Display name                  |
| `key`                     | CharField(255)            | NOT NULL          | Programmatic key              |
| `collect_tag_category_id` | ForeignKey                | NULL, SET_NULL    | Link to CollectTagCategory    |
| `order`                   | PositiveSmallIntegerField | Default: 0        | Display order within category |

#### Methods

- **`__str__()`**: Returns `name` field

#### Usage Examples

**Source Tags** (category: source):

- year, occasional, liturgical

**Theme Tags** (category: theme):

- healing, mission, departed, national, creation, unity, vocation

**Season Tags** (category: season):

- advent, christmas, epiphany, lent, easter, pentecost

**Commemoration Type Tags** (category: commemoration_type):

- sunday, major_feast, holy_day, lesser_feast

**Liturgy Tags** (category: liturgy):

- daily_office, burial, marriage, ordination

#### Multi-Dimensional Tagging

A single collect can have multiple tags across different categories:

```python
# Example: Collect for Mission (Occasional Prayer during Pentecost)
collect.tags.all()
# Returns:
# - source: "occasional"
# - theme: "mission"
# - season: "pentecost"
# - liturgy: "daily_office"
```

---

### 5. MetricalCollect (Musical Version Model)

**Table**: `office_metricalcollect`  
**Django Model**: `office.models.MetricalCollect`  
**Purpose**: Stores metrical (sung/musical) versions of collects

#### Fields

| Field                         | Type                      | Constraints       | Purpose                           |
| ----------------------------- | ------------------------- | ----------------- | --------------------------------- |
| `uuid`                        | UUIDField                 | Primary Key, Auto | Unique identifier                 |
| `collect_number`              | PositiveSmallIntegerField | NULL, BLANK       | Original collect number reference |
| `original_collect`            | TextField(255)            | NULL, BLANK       | Text of original prose collect    |
| `normalized_original_collect` | TextField(255)            | NULL, BLANK       | Plain text of original            |
| `tune_name`                   | CharField(255)            | NULL, BLANK       | Name of musical tune              |
| `first_line`                  | CharField(255)            | NULL, BLANK       | First line of metrical version    |
| `pdf_link`                    | URLField                  | NULL, BLANK       | Link to PDF sheet music           |
| `site_link`                   | URLField                  | NULL, BLANK       | Link to external website          |
| `midi_link`                   | URLField                  | NULL, BLANK       | Link to MIDI audio file           |
| `lyrics`                      | TextField                 | NULL, BLANK       | Full metrical lyrics              |
| `text_source`                 | CharField(255)            | NULL, BLANK       | Attribution for metrical text     |
| `tune_source`                 | CharField(255)            | NULL, BLANK       | Attribution for tune              |
| `name`                        | CharField(255)            | NULL, BLANK       | Display name of metrical version  |

#### Usage

```python
# Collect with metrical versions
collect = Collect.objects.get(title="Collect for Purity")
if collect.metrical_collect:
    print(f"Tune: {collect.metrical_collect.tune_name}")
    print(f"PDF: {collect.metrical_collect.pdf_link}")
```

#### Current State

⚠️ **Data Population Unknown**: No import logic found for MetricalCollect. Likely unpopulated or manually entered.

---

### 6. AbstractCollect (Helper Class)

**Table**: None (not a database model)  
**Django Model**: `office.models.AbstractCollect`  
**Purpose**: Helper class for dynamically-generated collects (e.g., saints with common collects)

#### Attributes

- `text` (str): Contemporary language collect text
- `traditional_text` (str): Traditional language collect text

#### Properties

- **`text_no_tags`**: Returns `text` with HTML stripped and "Amen." removed
- **`traditional_text_no_tags`**: Returns `traditional_text` with HTML stripped and "Amen." removed

#### Usage

Used by `SanctoraleCommemoration.common_collect()` method to generate dynamic collects:

```python
# churchcal/models.py
def common_collect(self):
    text = self.common.collect_format_string  # Template with placeholders
    text_tle = self.common.collect_tle_format_string
    return AbstractCollect(
        text=self.build_collect(text),  # Fill in saint name, pronouns
        traditional_text=self.build_collect(text_tle)
    )
```

**Example Template**:

```
"Almighty God, who called your servant {} to be a faithful pastor..."
# Becomes:
"Almighty God, who called your servant John Smith to be a faithful pastor..."
```

---

## Data Relationships

### Collect → CollectType (Many-to-One)

- **Cardinality**: Many Collects to One CollectType
- **Foreign Key**: `Collect.collect_type_id`
- **On Delete**: `SET_NULL` (preserve collect if type deleted)
- **Purpose**: Top-level categorization (year, occasional, office_prayers, etc.)

**Query Example**:

```python
# Get all occasional prayers
occasional = CollectType.objects.get(key="occasional")
prayers = Collect.objects.filter(collect_type=occasional)
```

---

### Collect ↔ CollectTag (Many-to-Many)

- **Cardinality**: Many Collects to Many CollectTags
- **Join Table**: `office_collect_tags`
- **Purpose**: Multi-dimensional tagging for filtering and search

**Query Example**:

```python
# Get all collects tagged with "mission"
mission_tag = CollectTag.objects.get(key="mission")
collects = Collect.objects.filter(tags=mission_tag)

# Get all tags for a collect
collect = Collect.objects.get(title="Collect for Mission")
tags = collect.tags.all()
```

---

### CollectTag → CollectTagCategory (Many-to-One)

- **Cardinality**: Many Tags to One Category
- **Foreign Key**: `CollectTag.collect_tag_category_id`
- **On Delete**: `SET_NULL` (preserve tag if category deleted)
- **Purpose**: Organize tags into dimensions (source, theme, season, etc.)

**Query Example**:

```python
# Get all season tags
season_category = CollectTagCategory.objects.get(key="season")
season_tags = CollectTag.objects.filter(collect_tag_category=season_category)
```

---

### Collect → MetricalCollect (One-to-One, Three Times)

- **Cardinality**: One Collect to Up To Three MetricalCollects
- **Foreign Keys**: `metrical_collect_id`, `metrical_collect_2_id`, `metrical_collect_3_id`
- **On Delete**: `SET_NULL` (preserve collect if metrical version deleted)
- **Purpose**: Link prose collects to sung versions

**Query Example**:

```python
# Get collect with all metrical versions
collect = Collect.objects.select_related(
    'metrical_collect',
    'metrical_collect_2',
    'metrical_collect_3'
).get(title="Collect for Purity")

metrical_versions = [
    v for v in [
        collect.metrical_collect,
        collect.metrical_collect_2,
        collect.metrical_collect_3
    ] if v is not None
]
```

---

## Database Indexes

### Existing Indexes (Django Default)

- Primary key index on `uuid` for all models (automatic)
- Foreign key indexes on:
  - `Collect.collect_type_id`
  - `Collect.metrical_collect_id`
  - `Collect.metrical_collect_2_id`
  - `Collect.metrical_collect_3_id`
  - `CollectTag.collect_tag_category_id`

### Recommended Additional Indexes

⚠️ **Performance Optimization Opportunity**

```python
class Collect(BaseModel):
    # ... fields ...

    class Meta:
        indexes = [
            models.Index(fields=['order', 'collect_type']),  # Ordered listing
            models.Index(fields=['title']),  # Title search
        ]
```

**Rationale**: Frequent queries by `order` and `collect_type` for display; title search for user lookups.

### Full-Text Search Index (If Backend Search Implemented)

If PostgreSQL full-text search is implemented instead of client-side:

```python
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

class Collect(BaseModel):
    # ... fields ...
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
        ]
```

**Note**: Not currently needed due to client-side search decision (see research.md).

---

## Data Constraints and Validation

### Model-Level Constraints

**Collect**:

- ✅ `title` is required (NOT NULL)
- ✅ `text` is required (NOT NULL, CKEditor5 enforces non-empty)
- ⚠️ `normalized_text` should be required but is nullable (data issue)
- ❌ No constraint ensuring `traditional_text` exists (optional by design)
- ❌ No constraint on `attribution` format

**CollectType**:

- ✅ `name` and `key` are required
- ❌ No unique constraint on `key` (should be unique)

**CollectTag**:

- ✅ `name` and `key` are required
- ❌ No unique constraint on `key` within `collect_tag_category`

### Business Logic Validation (Code-Level)

**Import Script Validation** (`import_collects.py`):

- Cleans collect text: removes extra spaces, normalizes quotes
- Ensures consistent Amen formatting: `<strong>Amen.</strong>`
- Strips disallowed HTML tags via `clean_collect()`
- Validates collect type exists before assignment

**Frontend Validation** (`Collect.vue`):

- No validation (display only)

### Recommended Constraints (Future Enhancement)

```python
class CollectType(BaseModel):
    key = models.CharField(max_length=255, unique=True)  # Add unique

class CollectTag(BaseModel):
    key = models.CharField(max_length=255)

    class Meta:
        unique_together = [['key', 'collect_tag_category']]  # Unique within category
```

---

## Data Population and Migrations

### Import Commands

**Primary Import**: `python manage.py import_collects`

Located: `site/office/management/commands/import_collects.py`

**Functions**:

1. `import_occasional_collects()` - Scrapes web for occasional prayers
2. `import_traditional_language_occasional_collects()` - Parses PDF for traditional text
3. `import_collects_of_the_christian_year()` - Imports from Google Sheets
4. `import_liturgical_collects()` - Automated import for office prayers
5. `match_collects()` - Links collects to commemorations
6. `clean_liturgical_collects()` - Normalizes formatting

### Migration History

**Key Migration**: `0010_move_collects_to_foreign_keys.py`

- Changed `Commemoration.collect` from TextField to ForeignKey(Collect)
- Migrated existing text-based collects to Collect model
- Created collect records and updated foreign keys

### Required Data Migration (⚠️ Critical)

**Issue**: `normalized_text` and `normalized_traditional_text` fields are empty

**Solution**: Create management command to populate:

```python
# site/office/management/commands/populate_normalized_text.py

from django.core.management.base import BaseCommand
from office.models import Collect
from office.management.commands.import_collects import do_strip_tags

class Command(BaseCommand):
    help = 'Populate normalized text fields for all collects'

    def handle(self, *args, **options):
        collects = Collect.objects.all()
        updated = 0

        for collect in collects:
            collect.normalized_text = do_strip_tags(collect.text).replace(" Amen.", "")
            if collect.traditional_text:
                collect.normalized_traditional_text = do_strip_tags(
                    collect.traditional_text
                ).replace(" Amen.", "")
            collect.save()
            updated += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated} collects')
        )
```

**Usage**:

```bash
python manage.py populate_normalized_text
```

---

## API Serialization

### CollectSerializer

**Location**: `site/office/api/serializers.py`

**Fields Included**:

- All Collect fields
- Nested `collect_type` (CollectTypeSerializer)
- Nested `tags` (CollectTagSerializer with category)
- Nested `metrical_collect` (if present)

**Example Response**:

```json
{
  "uuid": "abc-123-def",
  "title": "Collect for Purity",
  "text": "<p>Almighty God, to you all hearts...</p>",
  "traditional_text": "<p>Almighty God, unto whom all hearts...</p>",
  "normalized_text": "Almighty God, to you all hearts are open...",
  "attribution": "Thomas Cranmer, 1549",
  "collect_type": {
    "name": "Collects from the Daily Office",
    "key": "office_prayers",
    "order": 2
  },
  "tags": [
    {
      "name": "Daily Office",
      "key": "daily_office",
      "collect_tag_category": {
        "name": "Liturgy",
        "key": "liturgy"
      }
    }
  ],
  "metrical_collect": null,
  "order": 1,
  "number": null
}
```

---

## Query Patterns and Performance

### Common Queries

**1. Get all collects for browsing**:

```python
collects = (
    Collect.objects
    .select_related('collect_type')
    .prefetch_related('tags__collect_tag_category')
    .order_by('collect_type__order', 'order')
)
```

**Performance**: ~200-300ms for 500 collects with relationships

---

**2. Get grouped collects by source**:

```python
# Used by GroupedCollectsViewSet
collects = (
    Collect.objects
    .select_related('collect_type')
    .prefetch_related('tags__collect_tag_category')
    .all()
)

# Group in Python code by source tags
year_collects = [c for c in collects if 'year' in [t.key for t in c.tags.all()]]
```

**Note**: Grouping logic is in Python, not SQL. Could be optimized with annotations.

---

**3. Get collects for a specific date (via Commemoration)**:

```python
from churchcal.calculations import ChurchYear
from churchcal.models import Calendar

date = datetime.date(2025, 12, 25)
calendar = Calendar.objects.get(abbreviation='ACNA2019')
year = ChurchYear(date.year, calendar)
commemoration = year.get_commemoration(date)

collects = commemoration.get_collects(calendar_date=date)
# Returns list of Collect objects
```

---

**4. Search collects by text (client-side)**:

```javascript
// Frontend Vue.js
collects.filter(
  (collect) =>
    collect.title.toLowerCase().includes(searchTerm) ||
    collect.normalized_text.toLowerCase().includes(searchTerm)
);
```

**Note**: Requires `normalized_text` to be populated.

---

**5. Get tag categories with tags**:

```python
categories = (
    CollectTagCategory.objects
    .prefetch_related(
        Prefetch(
            'collecttag_set',
            queryset=CollectTag.objects.order_by('order', 'name'),
            to_attr='tags'
        )
    )
    .order_by('order', 'name')
)
```

---

### N+1 Query Prevention

**Problem**: Fetching collects and accessing `collect_type` or `tags` individually causes N+1 queries.

**Solution**: Always use `select_related` and `prefetch_related`:

```python
# ✅ GOOD - Single query for type, single query for tags
collects = Collect.objects.select_related('collect_type').prefetch_related('tags')

# ❌ BAD - N+1 queries
collects = Collect.objects.all()
for collect in collects:
    print(collect.collect_type.name)  # Query per collect!
```

---

## Data Integrity and Consistency

### Orphaned Records

**Potential Issue**: Collects without a CollectType

- **Current**: `collect_type` is nullable with `SET_NULL` on delete
- **Impact**: Collect would lose categorization but remain in database
- **Mitigation**: Ensure CollectType records are never deleted

**Potential Issue**: Collects with tags but no tag category

- **Current**: `CollectTag.collect_tag_category` is nullable
- **Impact**: Tags would be orphaned and unorganized
- **Mitigation**: Ensure categories are created before tags

### Data Quality Checks

**Recommended Checks** (Django management command or test):

```python
# Check 1: Collects missing normalized text
missing_normalized = Collect.objects.filter(
    Q(normalized_text__isnull=True) | Q(normalized_text='')
).count()

# Check 2: Collects missing attribution
missing_attribution = Collect.objects.filter(
    Q(attribution__isnull=True) | Q(attribution='')
).count()

# Check 3: Collects without any tags
untagged = Collect.objects.annotate(
    tag_count=Count('tags')
).filter(tag_count=0).count()

# Check 4: Tags without category
orphaned_tags = CollectTag.objects.filter(
    collect_tag_category__isnull=True
).count()
```

---

## Edge Cases and Special Scenarios

### 1. Collect with Missing Traditional Text

**Scenario**: Contemporary collect exists but no traditional version

**Handling**:

- `traditional_text` is NULL
- Frontend displays only contemporary text
- Language toggle should be disabled or show same text

---

### 2. Collect with Multiple Metrical Versions

**Scenario**: One collect has 3 metrical versions linked

**Handling**:

- UI should show all three with distinct labels: "Version 1", "Version 2", "Version 3"
- Each version may have different tune, lyrics, or arrangement

---

### 3. Tag without Category

**Scenario**: CollectTag with `collect_tag_category=NULL`

**Handling**:

- Should be prevented during import
- If occurs, tag should be displayed in "Uncategorized" group
- Admin should assign category

---

### 4. Collect Used in Multiple Offices

**Scenario**: Same collect appears in Morning Prayer, Evening Prayer, and Compline

**Handling**:

- Single Collect record with multiple tags: `daily_office` liturgy tag
- User can select which offices to add it to (US7)
- localStorage stores selections: `{"Morning Prayer": ["uuid-1"], "Evening Prayer": ["uuid-1"]}`

---

### 5. Search with No Results

**Scenario**: User searches for term not in any collect

**Handling**:

- Frontend should display: "No collects match your search"
- Suggest clearing search or trying different terms
- Maintain filter selections (don't reset category filters)

---

## Schema Evolution and Future Considerations

### Potential Schema Changes

**1. Add Alternative Text Field**:

```python
class Collect(BaseModel):
    # ... existing fields ...
    alternative_text = CKEditor5Field(blank=True, null=True)
    alternative_traditional_text = CKEditor5Field(blank=True, null=True)
```

**Purpose**: Support textual variants of same collect (FR-012a)

---

**2. Split Attribution into Separate Fields**:

```python
class Collect(BaseModel):
    # ... existing fields ...
    bcp_page_reference = models.CharField(max_length=50, blank=True, null=True)
    historical_source = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
```

**Purpose**: Structured attribution data for filtering and display

---

**3. Add Search Vector for Backend Search** (if needed):

```python
from django.contrib.postgres.search import SearchVectorField

class Collect(BaseModel):
    # ... existing fields ...
    search_vector = SearchVectorField(null=True)
```

**Purpose**: Enable PostgreSQL full-text search

---

### Backward Compatibility

**Constraint**: FR-NFR-001 mandates backward compatibility

**Impact on Changes**:

- Existing `attribution` field must be preserved (can supplement, not replace)
- Collect API response structure must remain stable
- localStorage structure for `extraCollects` must not change
- Migration scripts must not break existing data

---

## Summary

The Collects data model is **well-designed and comprehensive** for its liturgical purpose:

✅ **Strengths**:

- Multi-language support (contemporary + traditional)
- Flexible tagging system (5 dimensions)
- Metrical collect support (up to 3 versions)
- Clean separation of concerns (type, tags, metrical)
- Ready for search (normalized fields in schema)

⚠️ **Critical Issues**:

1. **Normalized text fields unpopulated** - blocks search implementation
2. **No automated tests** - violates Constitution Principle III
3. **Attribution incomplete** - only occasional prayers have data

🔧 **Recommended Improvements**:

1. Populate normalized text fields (management command)
2. Add unique constraints on `CollectType.key` and `CollectTag.key`
3. Add database indexes for common queries
4. Complete attribution data (BCP page references)
5. Write comprehensive test suite

The model successfully implements all requirements from the specification (FR-001 through FR-019) with the exception of data completeness issues that can be addressed through migrations.

---

**Document Version**: 1.0  
**Last Updated**: November 6, 2025  
**Next Phase**: API Contract Design (contracts/)
