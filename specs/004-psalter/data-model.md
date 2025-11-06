# Data Model: Psalter

**Feature**: 004-psalter | **Phase**: 1 (Design) | **Date**: November 6, 2025

This document describes the database schema for the Psalter feature, mapping specification requirements to entity relationships and constraints.

## Entity Relationship Diagram

```
┌─────────────────┐
│   PsalmTopic    │
│─────────────────│
│ id (UUID, PK)   │
│ topic_name      │◄────────┐
│ psalms (legacy) │          │
│ order           │          │
└─────────────────┘          │
                             │
                             │ many-to-many
                             │
                    ┌────────────────────┐
                    │ PsalmTopicPsalm    │
                    │────────────────────│
                    │ id (UUID, PK)      │
                    │ psalm_id (FK)      │
                    │ psalm_topic_id (FK)│
                    │ order              │
                    └────────────────────┘
                             │
                             │
                             │
┌─────────────────┐         │
│     Psalm       │◄────────┘
│─────────────────│
│ id (UUID, PK)   │
│ number (UNIQUE) │
│ latin_title     │
└─────────────────┘
        │
        │ one-to-many
        │
        ▼
┌─────────────────┐
│   PsalmVerse    │
│─────────────────│
│ id (UUID, PK)   │
│ psalm_id (FK)   │
│ number          │
│ first_half      │
│ second_half     │
│ first_half_tle  │
│ second_half_tle │
└─────────────────┘
UNIQUE(psalm_id, number)
```

## Entities

### Psalm

**Purpose**: Represents one of the 150 psalms from the Book of Common Prayer 2019 Psalter.

**Requirements Mapping**:

- FR-001: Store all 150 psalms
- FR-002: View individual psalm by number
- FR-005: Display Latin titles
- FR-010: Complete text with superscriptions

**Schema**:

| Column        | Type          | Constraints                     | Description                   | Example              |
| ------------- | ------------- | ------------------------------- | ----------------------------- | -------------------- |
| `id`          | UUID          | PRIMARY KEY, NOT NULL           | Unique identifier             | `a1b2c3d4-...`       |
| `number`      | INTEGER       | UNIQUE, NOT NULL, CHECK (1-150) | Psalm number (1-150)          | `23`                 |
| `latin_title` | VARCHAR(1000) | NULL                            | Traditional Latin designation | `"Dominus regit me"` |

**Indexes**:

- Primary key on `id` (clustered)
- Unique index on `number` (for fast lookup by number)

**Relationships**:

- One-to-many with `PsalmVerse` (verses)
- Many-to-many with `PsalmTopic` through `PsalmTopicPsalm` (topics)

**Validation Rules**:

- `number` must be between 1 and 150 (inclusive)
- `number` must be unique across all records
- `latin_title` can be NULL (not all psalms have Latin titles)

**Sample Data**:

```json
{
  "id": "uuid-here",
  "number": 23,
  "latin_title": "Dominus regit me"
}
```

**State Transitions**: None (immutable after initial load)

---

### PsalmVerse

**Purpose**: Represents a single numbered verse within a psalm, with both Contemporary and Traditional Language Edition (TLE) text.

**Requirements Mapping**:

- FR-003: Verse numbering
- FR-004: Proper indentation for parallelism (first_half/second_half split)
- FR-009: Exact Coverdale translation preserved
- FR-012: Contemporary and TLE support
- FR-014: Pointing marks (stored as text, asterisk \* between halves)

**Schema**:

| Column            | Type          | Constraints                      | Description                     | Example                           |
| ----------------- | ------------- | -------------------------------- | ------------------------------- | --------------------------------- |
| `id`              | UUID          | PRIMARY KEY, NOT NULL            | Unique identifier               | `b2c3d4e5-...`                    |
| `psalm_id`        | UUID          | FOREIGN KEY (Psalm.id), NOT NULL | Parent psalm                    | `a1b2c3d4-...`                    |
| `number`          | INTEGER       | NOT NULL, CHECK (> 0)            | Verse number within psalm       | `1`                               |
| `first_half`      | VARCHAR(1000) | NOT NULL                         | First half-line (Contemporary)  | `"The Lord is my shepherd,"`      |
| `second_half`     | VARCHAR(1000) | NOT NULL                         | Second half-line (Contemporary) | `"therefore can I lack nothing."` |
| `first_half_tle`  | VARCHAR(1000) | NULL                             | First half-line (Traditional)   | `"The Lord is my shepherd,"`      |
| `second_half_tle` | VARCHAR(1000) | NULL                             | Second half-line (Traditional)  | `"therefore can I lack nothing."` |

**Indexes**:

- Primary key on `id`
- Foreign key index on `psalm_id`
- Unique composite index on `(psalm_id, number)` (one verse #1, one verse #2, etc. per psalm)
- Index on `psalm_id` for fast verse retrieval

**Relationships**:

- Many-to-one with `Psalm` (each verse belongs to exactly one psalm)

**Validation Rules**:

- `psalm_id` must reference an existing `Psalm.id`
- `number` must be positive (1, 2, 3, ...)
- Combination of `(psalm_id, number)` must be unique (no duplicate verse numbers within a psalm)
- `first_half` and `second_half` are required (Contemporary edition is primary)
- `first_half_tle` and `second_half_tle` are optional (Traditional edition may not exist for all verses)

**Sample Data**:

```json
{
  "id": "uuid-here",
  "psalm_id": "a1b2c3d4-...",
  "number": 1,
  "first_half": "The Lord is my shepherd,",
  "second_half": "therefore can I lack nothing.",
  "first_half_tle": "The Lord is my shepherd,",
  "second_half_tle": "therefore can I lack nothing."
}
```

**State Transitions**: None (immutable after initial load)

**Notes**:

- The pointing mark (\*) is added at display time, not stored in the database
- First/second half split enables proper HTML formatting with hanging indent and indent classes
- Contemporary vs Traditional primarily differ in pronouns (you/your vs thou/thee)

---

### PsalmTopic

**Purpose**: Represents a thematic category for organizing psalms (e.g., "Praise and Thanksgiving", "Morning Prayer"). Managed through Django admin interface.

**Requirements Mapping**:

- FR-011: Thematic categories for topic search
- FR-016: Admin interface for managing topics
- FR-017: Assign psalms and reorder topics
- US4: Search psalms by topic
- US6: Manage psalm topics (admin)

**Schema**:

| Column       | Type          | Constraints           | Description                               | Example                             |
| ------------ | ------------- | --------------------- | ----------------------------------------- | ----------------------------------- |
| `id`         | UUID          | PRIMARY KEY, NOT NULL | Unique identifier                         | `c3d4e5f6-...`                      |
| `topic_name` | VARCHAR(255)  | NOT NULL              | Display name of topic                     | `"Praise and Thanksgiving"`         |
| `psalms`     | VARCHAR(2000) | NULL                  | **LEGACY**: Comma-separated psalm numbers | `"100,103,145,146,147,148,149,150"` |
| `order`      | INTEGER       | NOT NULL              | Display order (sorting)                   | `1`                                 |

**Indexes**:

- Primary key on `id`
- Index on `order` (for sorted topic lists)

**Relationships**:

- Many-to-many with `Psalm` through `PsalmTopicPsalm` (topic contains multiple psalms, psalm can be in multiple topics)

**Validation Rules**:

- `topic_name` must not be empty
- `order` must be unique (enforced in application layer, not database)
- Topics are **mutable via admin interface** (FR-016: admin can create, edit, delete topics)

**Sample Data**:

```json
{
  "id": "uuid-here",
  "topic_name": "Praise and Thanksgiving",
  "psalms": "100,103,145,146,147,148,149,150",
  "order": 1
}
```

**State Transitions**:

- Created/edited/deleted via Django admin interface
- Changes take effect immediately (with cache invalidation per SC-010)

**Notes**:

- `psalms` field is **LEGACY**: Used in initial implementation, now superseded by `PsalmTopicPsalm` join table
- Topics are managed via Django admin interface (FR-016: PsalmTopicAdmin with SortableAdminMixin)
- Changes to topics via admin take effect immediately with cache clearing
- Typical topics: Praise, Thanksgiving, Morning, Evening, Penitence, Comfort, Trust, Deliverance

---

### PsalmTopicPsalm

**Purpose**: Join table for the many-to-many relationship between `Psalm` and `PsalmTopic`, allowing psalms to appear in multiple topics and topics to contain multiple psalms.

**Requirements Mapping**:

- FR-011: Topic categorization
- FR-017: Assign psalms to topics
- US4: Search/filter psalms by topic
- US6: Manage psalm topics (admin)

**Schema**:

| Column           | Type    | Constraints                           | Description                 | Example        |
| ---------------- | ------- | ------------------------------------- | --------------------------- | -------------- |
| `id`             | UUID    | PRIMARY KEY, NOT NULL                 | Unique identifier           | `d4e5f6g7-...` |
| `psalm_id`       | UUID    | FOREIGN KEY (Psalm.id), NOT NULL      | Psalm in this topic         | `a1b2c3d4-...` |
| `psalm_topic_id` | UUID    | FOREIGN KEY (PsalmTopic.id), NOT NULL | Topic containing this psalm | `c3d4e5f6-...` |
| `order`          | INTEGER | NOT NULL                              | Display order within topic  | `1`            |

**Indexes**:

- Primary key on `id`
- Foreign key index on `psalm_id`
- Foreign key index on `psalm_topic_id`
- Composite index on `(psalm_topic_id, order)` (for sorted psalm lists within a topic)
- Unique composite index on `(psalm_id, psalm_topic_id)` (prevent duplicate associations)

**Relationships**:

- Many-to-one with `Psalm`
- Many-to-one with `PsalmTopic`

**Validation Rules**:

- `psalm_id` must reference an existing `Psalm.id`
- `psalm_topic_id` must reference an existing `PsalmTopic.id`
- Combination of `(psalm_id, psalm_topic_id)` must be unique (a psalm can appear in a topic only once)
- `order` determines display sequence within a topic (e.g., Psalm 23 before Psalm 121)

**Sample Data**:

```json
{
  "id": "uuid-here",
  "psalm_id": "a1b2c3d4-...",
  "psalm_topic_id": "c3d4e5f6-...",
  "order": 3
}
```

**State Transitions**: Created/edited/deleted via Django admin interface when managing topic-psalm associations

---

## Database Constraints Summary

### Referential Integrity

```sql
-- PsalmVerse to Psalm
ALTER TABLE psalter_psalmverse
ADD CONSTRAINT fk_psalmverse_psalm
FOREIGN KEY (psalm_id) REFERENCES psalter_psalm(id)
ON DELETE CASCADE;

-- PsalmTopicPsalm to Psalm
ALTER TABLE psalter_psalmtopicpsalm
ADD CONSTRAINT fk_psalmtopicpsalm_psalm
FOREIGN KEY (psalm_id) REFERENCES psalter_psalm(id)
ON DELETE CASCADE;

-- PsalmTopicPsalm to PsalmTopic
ALTER TABLE psalter_psalmtopicpsalm
ADD CONSTRAINT fk_psalmtopicpsalm_topic
FOREIGN KEY (psalm_topic_id) REFERENCES psalter_psalmtopic(id)
ON DELETE CASCADE;
```

### Unique Constraints

```sql
-- Psalm number uniqueness (1-150)
ALTER TABLE psalter_psalm
ADD CONSTRAINT uq_psalm_number
UNIQUE (number);

-- Verse number uniqueness within psalm
ALTER TABLE psalter_psalmverse
ADD CONSTRAINT uq_psalmverse_number
UNIQUE (psalm_id, number);

-- Psalm-topic association uniqueness
ALTER TABLE psalter_psalmtopicpsalm
ADD CONSTRAINT uq_psalmtopicpsalm_association
UNIQUE (psalm_id, psalm_topic_id);
```

### Check Constraints

```sql
-- Psalm number range
ALTER TABLE psalter_psalm
ADD CONSTRAINT chk_psalm_number_range
CHECK (number >= 1 AND number <= 150);

-- Verse number positive
ALTER TABLE psalter_psalmverse
ADD CONSTRAINT chk_verse_number_positive
CHECK (number > 0);
```

---

## Data Loading Strategy

### Initial Database Population

**Source**: Database dump (`dailyoffice_2024_01_30.sql.zip`) or fixtures

**Steps**:

1. Load `Psalm` records (150 psalms)
2. Load `PsalmVerse` records (~2,250 verses)
3. Load `PsalmTopic` records (~10-15 topics)
4. Load `PsalmTopicPsalm` records (associations)

**Idempotency**: Use `number` field for psalms (unique), `(psalm_id, number)` for verses

### Test Fixtures

**Location**: `site/psalter/fixtures/test_psalms.json`

**Contents**:

- Psalms 1, 23, 119 (short, medium, long examples)
- 3 sample topics: "Praise", "Morning Prayer", "Comfort"
- Verse associations for test scenarios

**Usage**:

```bash
python manage.py loaddata test_psalms
```

---

## Data Volume and Performance

**Estimated Record Counts**:

- `Psalm`: 150 records (tiny)
- `PsalmVerse`: ~2,250 records (150 psalms × 15 verses average)
- `PsalmTopic`: ~15 records (tiny)
- `PsalmTopicPsalm`: ~500 records (psalms appear in 3-5 topics on average)

**Total Storage**: ~2MB of text data (negligible)

**Performance Characteristics**:

- **Read-heavy**: 99.9% reads, 0.1% writes (immutable after initial load)
- **Query patterns**:
  - Single psalm by number: `SELECT * FROM psalter_psalm WHERE number = 23` (indexed, instant)
  - Psalm with verses: Prefetch relationship (N+1 query prevention)
  - Topics for psalm: Join through `PsalmTopicPsalm` (indexed foreign keys)
- **Caching strategy**: Entire dataset fits in memory, consider aggressive caching (Memcached)

**Optimization Notes**:

- Indexes on all foreign keys (automatic in Django)
- Prefetch relationships in API queries (already implemented in `PsalmsViewSet`)
- No need for partitioning or sharding (tiny dataset)

---

## Migration Strategy

### Current State

**Assumption**: Database already contains all psalter data (verified from code analysis)

**No schema changes needed** for FR-011 compliance (admin removal is application-layer only)

### Future Changes

If psalm text corrections are needed:

```python
# Example migration for text correction
from django.db import migrations

def correct_psalm_text(apps, schema_editor):
    PsalmVerse = apps.get_model('psalter', 'PsalmVerse')
    verse = PsalmVerse.objects.get(psalm__number=23, number=1)
    verse.first_half = "Corrected text"
    verse.save()

class Migration(migrations.Migration):
    dependencies = [
        ('psalter', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(correct_psalm_text),
    ]
```

---

## Data Integrity Rules

### Business Rules

1. **Psalm Text Stability**: Psalm text should be carefully edited via admin interface (FR-018), with changes documented
2. **Completeness**: All 150 psalms must exist (validation in tests)
3. **Consistency**: Contemporary edition (`first_half`/`second_half`) is always present; TLE is optional
4. **Topic Assignment**: Psalms can belong to 0-N topics (not enforced, but typical is 2-5 topics per psalm)
5. **Admin Access**: Only authorized staff can modify topics and psalm text (Django permissions)

### Validation Checklist

- [ ] Psalm numbers 1-150 all exist and are unique
- [ ] Every psalm has at least one verse
- [ ] Every verse has non-empty `first_half` and `second_half`
- [ ] No orphaned verses (all `psalm_id` values reference existing psalms)
- [ ] No orphaned topic associations (all foreign keys valid)
- [ ] Topic `order` values are unique and sequential
- [ ] Admin users have appropriate permissions for topic and verse management

**Validation Script**: `site/psalter/management/commands/validate_psalter.py` (to be created in Phase 2)

---

## API Response Shapes

These data models map to API responses documented in `contracts/psalms-api.yaml`:

**GET /api/v1/psalms/{number}**:

```json
{
  "id": "uuid",
  "number": 23,
  "latin_title": "Dominus regit me",
  "verses": [
    {
      "id": "uuid",
      "number": 1,
      "first_half": "The Lord is my shepherd,",
      "second_half": "therefore can I lack nothing.",
      "first_half_tle": "...",
      "second_half_tle": "..."
    }
  ],
  "topics": [
    {
      "id": "uuid",
      "topic_name": "Comfort and Trust"
    }
  ]
}
```

**GET /api/v1/psalms/topics/**:

```json
[
  {
    "id": "uuid",
    "topic_name": "Praise and Thanksgiving",
    "order": 1
  }
]
```

---

## Summary

This data model:

- ✅ Supports all functional requirements (FR-001 through FR-019)
- ✅ Enables all user stories (US1 through US6, including admin workflows)
- ✅ Uses Django best practices (UUIDs, foreign keys, unique constraints)
- ✅ Optimized for read-heavy workloads (indexes, prefetch patterns)
- ✅ Flexible admin interface for topic management (FR-016-019)
- ✅ Minimal storage requirements (~2MB, fits entirely in memory)

**Admin Interface**: Properly registered in Django admin for topic and verse management per FR-016 through FR-019.
