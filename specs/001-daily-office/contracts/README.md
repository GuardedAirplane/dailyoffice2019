# API Contracts: Daily Office Liturgy REST API

**Date**: November 6, 2025  
**Type**: Phase 1 - API Documentation  
**Status**: Existing Implementation Documentation  
**API Version**: 1.0 (implied)

## Overview

The Daily Office REST API provides JSON responses for liturgical content, settings, resources, and calendar data. The API is consumed primarily by the Vue 3 frontend but is also available for third-party integrations.

**Base URL**: `https://dailyoffice2019.com/api/` (production) or `https://127.0.0.1:8000/api/` (development)

**Architecture**: Django REST Framework (DRF) with custom ViewSets

**Authentication**: None required (public API)

**Response Format**: JSON

**API Style**: REST with some RPC-style endpoints

## API Endpoints Summary

| Endpoint                                      | Method | Purpose                           | Implements         |
| --------------------------------------------- | ------ | --------------------------------- | ------------------ |
| `/office/{office_type}/{year}/{month}/{day}/` | GET    | Generate complete office for date | FR-001-004, FR-012 |
| `/family/{office_type}/{year}/{month}/{day}/` | GET    | Generate family prayer office     | FR-018             |
| `/calendar/`                                  | GET    | Get liturgical calendar data      | FR-014             |
| `/collects/`                                  | GET    | List all collects                 | FR-009             |
| `/collects/grouped/`                          | GET    | Collects grouped by source/theme  | -                  |
| `/collects/categories/`                       | GET    | Collect categories and tags       | -                  |
| `/psalms/`                                    | GET    | List all psalms                   | FR-009             |
| `/psalms/{id}/`                               | GET    | Get specific psalm with verses    | FR-009             |
| `/psalms/topics/`                             | GET    | Get psalm topics                  | -                  |
| `/scripture/{passage}/`                       | GET    | Get scripture passage text        | FR-020, FR-021     |
| `/settings/`                                  | GET    | Get all settings and options      | FR-026-028         |
| `/about/`                                     | GET    | Get FAQ/about items               | -                  |
| `/updates/`                                   | GET    | Get update notices                | -                  |

## Core Office Endpoints

### GET `/office/{office_type}/{year}/{month}/{day}/`

Generate a complete daily office for a specific date.

**Implements Requirements**: FR-001 (Morning Prayer), FR-002 (Evening Prayer), FR-003 (Midday Prayer), FR-004 (Compline), FR-012 (view any date)

**Path Parameters**:

- `office_type` (string, required) - Office type identifier
  - Values: `morning_prayer`, `evening_prayer`, `midday_prayer`, `compline`
- `year` (integer, required) - Calendar year (e.g., 2025)
- `month` (integer, required) - Month (1-12)
- `day` (integer, required) - Day of month (1-31)

**Query Parameters** (all optional):

- `psalter` (string) - Psalter cycle: `30day` or `60day` (default from settings)
- `lectionary` (string) - Lectionary cycle: `1year` or `2year` (default from settings)
- `bible_version` (string) - Bible translation: `esv`, `kjv`, `rsv`, `nrsvce`, `nabre`, `niv`, `nasb` (default: `esv`)
- `canticle_rotation` (string) - Canticle rotation: `traditional`, `seasonal`, `daily`
- `canticle_table` (string) - Canticle table: `bcp2019`, `bcp1979`, `rec2011`
- `confession_length` (string) - Confession length: `short`, `long`, `fast_days_only`
- `absolution_style` (string) - Absolution: `priest`, `lay`
- `invitatory` (string) - Invitatory: `venite`, `jubilate`, `rotating`
- `opening_sentence` (string) - Opening sentence: `fixed`, `seasonal`, `rotating`
- `include_third_reading` (boolean) - Include third reading: `true`/`false`
- `include_great_litany` (boolean) - Include Great Litany: `true`/`false`
- `include_pandemic_prayers` (boolean) - Include pandemic prayers: `true`/`false`
- `include_intercessions` (boolean) - Include intercessions: `true`/`false`
- `include_general_thanksgiving` (boolean) - Include General Thanksgiving: `true`/`false`
- `include_chrysostom` (boolean) - Include St. Chrysostom prayer: `true`/`false`
- `extra_collects` (string) - Comma-separated collect UUIDs to include

**Example Request**:

```http
GET /api/office/morning_prayer/2025/12/25/?bible_version=esv&psalter=60day HTTP/1.1
Host: dailyoffice2019.com
Accept: application/json
```

**Success Response** (`200 OK`):

```json
{
  "office": "morning_prayer",
  "date": "2025-12-25",
  "formatted_date": "Thursday December 25, 2025",
  "calendar_date": {
    "date": "2025-12-25",
    "primary": {
      "name": "The Nativity of Our Lord Jesus Christ: Christmas Day",
      "rank": "Principal Feast",
      "color": "White",
      "collect_1": { "uuid": "...", "title": "...", "text": "..." }
    },
    "season": "Christmas",
    "commemorations": [...]
  },
  "settings": {
    "psalter": "60day",
    "lectionary": "1year",
    "bible_version": "esv",
    "canticle_rotation": "traditional",
    ...
  },
  "modules": [
    {
      "name": "Heading",
      "lines": [
        {
          "id": "heading_0_abc123",
          "content": "Daily<br>Morning Prayer",
          "line_type": "heading",
          "indented": false,
          "audio_id": "abc123"
        }
      ]
    },
    {
      "name": "Commemoration Listing",
      "lines": [
        {
          "id": "commemoration_0_def456",
          "content": "The Nativity of Our Lord Jesus Christ: Christmas Day",
          "line_type": "subheading",
          "indented": false,
          "audio_id": "def456"
        }
      ]
    },
    {
      "name": "Opening Sentence",
      "lines": [
        {
          "id": "opening_0_ghi789",
          "content": "Behold, I bring you good news of great joy...",
          "line_type": "leader",
          "indented": false,
          "audio_id": "ghi789"
        }
      ]
    },
    {
      "name": "Confession",
      "lines": [
        {
          "id": "confession_0_jkl012",
          "content": "Dearly beloved, the Scriptures teach us...",
          "line_type": "rubric",
          "indented": false,
          "audio_id": "jkl012"
        },
        {
          "id": "confession_1_mno345",
          "content": "Let us humbly confess our sins to Almighty God.",
          "line_type": "leader",
          "indented": false,
          "audio_id": "mno345"
        },
        {
          "id": "confession_2_pqr678",
          "content": "Almighty and most merciful Father...",
          "line_type": "congregation",
          "indented": "indent",
          "audio_id": "pqr678"
        }
      ]
    },
    {
      "name": "Invitatory",
      "lines": [
        {
          "id": "invitatory_0_stu901",
          "content": "Lord, open our lips.",
          "line_type": "leader",
          "indented": false,
          "audio_id": "stu901"
        },
        {
          "id": "invitatory_1_vwx234",
          "content": "And our mouth shall proclaim your praise.",
          "line_type": "congregation",
          "indented": false,
          "audio_id": "vwx234"
        }
      ]
    },
    {
      "name": "Invitatory Psalm",
      "lines": [
        {
          "id": "invitatory_psalm_0_yza567",
          "content": "Venite: Psalm 95:1-7",
          "line_type": "citation",
          "indented": false,
          "audio_id": "yza567"
        },
        {
          "id": "invitatory_psalm_1_bcd890",
          "content": "O come, let us sing to the Lord; *",
          "line_type": "congregation",
          "indented": false,
          "audio_id": "bcd890"
        },
        {
          "id": "invitatory_psalm_2_efg123",
          "content": "let us make a joyful noise to the rock of our salvation!",
          "line_type": "congregation",
          "indented": "indent",
          "audio_id": "efg123"
        }
      ]
    },
    {
      "name": "Psalms",
      "lines": [
        {
          "id": "psalms_0_hij456",
          "content": "Psalm 19",
          "line_type": "citation",
          "indented": false,
          "audio_id": "hij456"
        },
        {
          "id": "psalms_1_klm789",
          "content": "The heavens declare the glory of God, *",
          "line_type": "congregation",
          "indented": false,
          "audio_id": "klm789"
        },
        {
          "id": "psalms_2_nop012",
          "content": "and the firmament shows his handiwork.",
          "line_type": "congregation",
          "indented": "indent",
          "audio_id": "nop012"
        }
      ]
    },
    {
      "name": "First Reading",
      "lines": [
        {
          "id": "first_reading_0_qrs345",
          "content": "Isaiah 9:2-7",
          "line_type": "citation",
          "indented": false,
          "audio_id": "qrs345"
        },
        {
          "id": "first_reading_1_tuv678",
          "content": "<p>The people who walked in darkness have seen a great light...</p>",
          "line_type": "html",
          "indented": false,
          "audio_id": "tuv678"
        },
        {
          "id": "first_reading_2_wxy901",
          "content": "The Word of the Lord.",
          "line_type": "leader",
          "indented": false,
          "audio_id": "wxy901"
        },
        {
          "id": "first_reading_3_zab234",
          "content": "Thanks be to God.",
          "line_type": "congregation",
          "indented": false,
          "audio_id": "zab234"
        }
      ]
    },
    {
      "name": "Canticle",
      "lines": [
        {
          "id": "canticle_0_cde567",
          "content": "Benedictus: The Song of Zechariah (Luke 1:68-79)",
          "line_type": "citation",
          "indented": false,
          "audio_id": "cde567"
        },
        {
          "id": "canticle_1_fgh890",
          "content": "Blessed be the Lord, the God of Israel, *",
          "line_type": "congregation",
          "indented": false,
          "audio_id": "fgh890"
        }
      ]
    },
    {
      "name": "Second Reading",
      "lines": [...]
    },
    {
      "name": "Canticle",
      "lines": [...]
    },
    {
      "name": "Creed",
      "lines": [...]
    },
    {
      "name": "Prayers",
      "lines": [...]
    },
    {
      "name": "Suffrages",
      "lines": [...]
    },
    {
      "name": "Collects of the Day",
      "lines": [...]
    },
    {
      "name": "Collects",
      "lines": [...]
    },
    {
      "name": "Mission Collect",
      "lines": [...]
    },
    {
      "name": "Dismissal",
      "lines": [...]
    }
  ],
  "audio_links": [
    {"url": "https://...", "duration": 180, "module": "Psalms"},
    ...
  ],
  "navigation": {
    "yesterday": {
      "label": "Wed",
      "link": "/office/morning_prayer/2025/12/24/"
    },
    "tomorrow": {
      "label": "Fri",
      "link": "/office/morning_prayer/2025/12/26/"
    },
    "morning_prayer": {
      "label": "Morning",
      "link": "/office/morning_prayer/2025/12/25/"
    },
    "evening_prayer": {
      "label": "Evening",
      "link": "/office/evening_prayer/2025/12/25/"
    },
    "midday_prayer": {
      "label": "Midday",
      "link": "/office/midday_prayer/2025/12/25/"
    },
    "compline": {
      "label": "Compline",
      "link": "/office/compline/2025/12/25/"
    },
    "current": "morning_prayer",
    "date": "December 25, 2025"
  }
}
```

**Line Types**:

- `heading` - Main heading
- `subheading` - Secondary heading
- `citation` - Scripture/psalm citation
- `html` - HTML content (scripture text, formatted content)
- `leader` - Priest/leader text
- `congregation` - Congregation responses
- `rubric` - Instructional text (italicized)
- `leader_dialogue` - Leader in antiphonal exchange
- `congregation_dialogue` - Congregation in antiphonal exchange
- `spacer` - Vertical spacing

**Indentation Values**:

- `false` - No indentation
- `"indent"` - Standard indentation
- `"indent-2"` - Double indentation (for psalm hemistichs, etc.)

**Error Responses**:

`404 Not Found` - Invalid date or office type:

```json
{
  "detail": "Not found."
}
```

`400 Bad Request` - Invalid query parameters:

```json
{
  "detail": "Invalid setting value provided."
}
```

**Example: Evening Prayer**:

```http
GET /api/office/evening_prayer/2025/08/15/ HTTP/1.1
Host: dailyoffice2019.com
Accept: application/json
```

**Response** (200 OK) - Abbreviated structure (similar to Morning Prayer with Evening-specific content):

```json
{
  "office": "evening_prayer",
  "date": "2025-08-15",
  "formatted_date": "Friday August 15, 2025",
  "calendar_date": {
    "date": "2025-08-15",
    "primary": {
      "name": "Saint Mary the Virgin, Mother of Our Lord",
      "rank": "Major Holy Day",
      "color": "White"
    },
    "season": "Pentecost"
  },
  "modules": [
    {
      "name": "Heading",
      "lines": [{"content": "Daily<br>Evening Prayer", "line_type": "heading"}]
    },
    {
      "name": "Opening Sentence",
      "lines": [{"content": "I will bless the Lord who gives me counsel...", "line_type": "leader"}]
    },
    {
      "name": "Invitatory",
      "lines": [
        {"content": "O God, make speed to save us.", "line_type": "leader"},
        {"content": "O Lord, make haste to help us.", "line_type": "congregation"}
      ]
    },
    {
      "name": "Phos Hilaron",
      "lines": [
        {"content": "Phos Hilaron: O Gladsome Light", "line_type": "citation"},
        {"content": "O gladsome light of the holy glory of the immortal Father, *", "line_type": "congregation"},
        {"content": "heavenly, holy, blessed Jesus Christ.", "line_type": "congregation", "indented": "indent"}
      ]
    },
    {
      "name": "Psalms",
      "lines": [{"content": "Psalm 113, 115", "line_type": "citation"}, ...]
    },
    {
      "name": "First Reading",
      "lines": [{"content": "Galatians 4:4-7", "line_type": "citation"}, ...]
    },
    {
      "name": "Canticle",
      "lines": [
        {"content": "Magnificat: The Song of Mary (Luke 1:46-55)", "line_type": "citation"},
        {"content": "My soul magnifies the Lord, *", "line_type": "congregation"}
      ]
    },
    {
      "name": "Second Reading",
      "lines": [{"content": "Luke 1:26-38", "line_type": "citation"}, ...]
    },
    {
      "name": "Canticle",
      "lines": [
        {"content": "Nunc Dimittis: The Song of Simeon (Luke 2:29-32)", "line_type": "citation"},
        {"content": "Lord, now let your servant depart in peace, *", "line_type": "congregation"}
      ]
    },
    {
      "name": "Apostles' Creed",
      "lines": [...]
    },
    {
      "name": "Prayers",
      "lines": [...]
    }
  ]
}
```

**Key Differences from Morning Prayer**:

- **Invitatory**: "O God, make speed to save us" (vs. "Lord, open our lips")
- **Invitatory Psalm**: Phos Hilaron (O Gladsome Light) instead of Venite/Jubilate
- **Canticles**: Magnificat and Nunc Dimittis (vs. Te Deum and Benedictus)
- **Psalm Selection**: Evening psalms from 30-day or 60-day cycle
- **Lessons**: Different lectionary assignments from Morning Prayer

---

**Example: Midday Prayer**:

```http
GET /api/office/midday_prayer/2025/06/10/ HTTP/1.1
Host: dailyoffice2019.com
Accept: application/json
```

**Response** (200 OK) - Abbreviated structure:

```json
{
  "office": "midday_prayer",
  "date": "2025-06-10",
  "formatted_date": "Tuesday June 10, 2025",
  "calendar_date": {
    "date": "2025-06-10",
    "primary": {
      "name": "Tuesday in the Second Week after Pentecost",
      "rank": "Ordinary Time",
      "color": "Green"
    },
    "season": "Pentecost"
  },
  "modules": [
    {
      "name": "Heading",
      "lines": [{"content": "Daily<br>Midday Prayer", "line_type": "heading"}]
    },
    {
      "name": "Opening",
      "lines": [
        {"content": "O God, make speed to save us.", "line_type": "leader"},
        {"content": "O Lord, make haste to help us.", "line_type": "congregation"},
        {"content": "Glory be to the Father, and to the Son, and to the Holy Spirit; *", "line_type": "congregation"},
        {"content": "as it was in the beginning, is now, and ever shall be, world without end. Amen.", "line_type": "congregation", "indented": "indent"},
        {"content": "Alleluia.", "line_type": "congregation"}
      ]
    },
    {
      "name": "Psalm",
      "lines": [
        {"content": "Psalm 119:105-112", "line_type": "citation"},
        {"content": "Your word is a lantern to my feet *", "line_type": "congregation"},
        {"content": "and a light upon my path.", "line_type": "congregation", "indented": "indent"}
      ]
    },
    {
      "name": "Reading",
      "lines": [
        {"content": "Ephesians 4:1-6", "line_type": "citation"},
        {"content": "<p>I therefore, a prisoner for the Lord...</p>", "line_type": "html"}
      ]
    },
    {
      "name": "Prayers",
      "lines": [
        {"content": "Lord, have mercy upon us.", "line_type": "congregation"},
        {"content": "Christ, have mercy upon us.", "line_type": "congregation"},
        {"content": "Lord, have mercy upon us.", "line_type": "congregation"},
        {"content": "Our Father, who art in heaven...", "line_type": "congregation"}
      ]
    },
    {
      "name": "Collect",
      "lines": [
        {"content": "Blessed Savior, at this hour you hung upon the Cross...", "line_type": "leader"}
      ]
    },
    {
      "name": "Dismissal",
      "lines": [
        {"content": "Let us bless the Lord.", "line_type": "leader"},
        {"content": "Thanks be to God.", "line_type": "congregation"}
      ]
    }
  ]
}
```

**Midday Prayer Characteristics**:

- **Shorter Office**: Fewer modules than Morning/Evening Prayer
- **No Canticles**: Only psalms and one short scripture reading
- **Simple Structure**: Opening → Psalm → Reading → Prayers → Collect → Dismissal
- **Kyrie**: Uses "Lord, have mercy" instead of longer intercessions
- **Time-Specific Collects**: Different collects for morning (9am), noon, and afternoon (3pm)
- **No Confession**: Penitential elements omitted

---

**Example: Compline**:

```http
GET /api/office/compline/2025/03/20/ HTTP/1.1
Host: dailyoffice2019.com
Accept: application/json
```

**Response** (200 OK) - Abbreviated structure:

```json
{
  "office": "compline",
  "date": "2025-03-20",
  "formatted_date": "Thursday March 20, 2025",
  "calendar_date": {
    "date": "2025-03-20",
    "primary": {
      "name": "Thursday in the Third Week of Lent",
      "rank": "Lenten Weekday",
      "color": "Purple"
    },
    "season": "Lent"
  },
  "modules": [
    {
      "name": "Heading",
      "lines": [{"content": "Compline", "line_type": "heading"}]
    },
    {
      "name": "Opening Sentence",
      "lines": [
        {"content": "The Lord Almighty grant us a peaceful night and a perfect end.", "line_type": "leader"},
        {"content": "Amen.", "line_type": "congregation"}
      ]
    },
    {
      "name": "Confession",
      "lines": [
        {"content": "Let us humbly confess our sins to Almighty God.", "line_type": "leader"},
        {"content": "Almighty God and Father, we confess to you, to one another, and to the whole company of heaven, that we have sinned, through our own fault, in thought, word, and deed, and through what we have left undone. For the sake of your Son our Lord Jesus Christ, have mercy upon us, forgive us our sins, and by the power of your Holy Spirit raise us up to serve you in newness of life, to the glory of your Name. Amen.", "line_type": "congregation", "indented": "indent"}
      ]
    },
    {
      "name": "Absolution",
      "lines": [
        {"content": "May Almighty God grant us forgiveness of all our sins, and the grace and comfort of the Holy Spirit.", "line_type": "leader"},
        {"content": "Amen.", "line_type": "congregation"}
      ]
    },
    {
      "name": "Invitatory",
      "lines": [
        {"content": "O God, make speed to save us.", "line_type": "leader"},
        {"content": "O Lord, make haste to help us.", "line_type": "congregation"},
        {"content": "Glory be to the Father...", "line_type": "congregation"}
      ]
    },
    {
      "name": "Psalm",
      "lines": [
        {"content": "Psalm 4", "line_type": "citation"},
        {"content": "Answer me when I call, O God of my righteousness; *", "line_type": "congregation"}
      ]
    },
    {
      "name": "Reading",
      "lines": [
        {"content": "1 Peter 5:8-9a", "line_type": "citation"},
        {"content": "<p>Be sober-minded; be watchful...</p>", "line_type": "html"}
      ]
    },
    {
      "name": "Hymn",
      "lines": [
        {"content": "Te lucis ante terminum: Before the Ending of the Day", "line_type": "citation"},
        {"content": "Before the ending of the day, *", "line_type": "congregation"},
        {"content": "Creator of the world, we pray", "line_type": "congregation", "indented": "indent"}
      ]
    },
    {
      "name": "Prayers",
      "lines": [
        {"content": "Into your hands, O Lord, I commend my spirit.", "line_type": "congregation"},
        {"content": "For you have redeemed me, O Lord, O God of truth.", "line_type": "congregation"},
        {"content": "Keep me, O Lord, as the apple of your eye.", "line_type": "congregation"},
        {"content": "Hide me under the shadow of your wings.", "line_type": "congregation"}
      ]
    },
    {
      "name": "Lord's Prayer",
      "lines": [
        {"content": "Our Father, who art in heaven...", "line_type": "congregation"}
      ]
    },
    {
      "name": "Collect",
      "lines": [
        {"content": "Lighten our darkness, we beseech thee, O Lord...", "line_type": "leader"}
      ]
    },
    {
      "name": "Nunc Dimittis",
      "lines": [
        {"content": "Nunc Dimittis: The Song of Simeon", "line_type": "citation"},
        {"content": "Lord, now let your servant depart in peace, *", "line_type": "congregation"},
        {"content": "according to your word.", "line_type": "congregation", "indented": "indent"}
      ]
    },
    {
      "name": "Dismissal",
      "lines": [
        {"content": "Glory be to the Father, and to the Son, and to the Holy Spirit; *", "line_type": "congregation"},
        {"content": "The Lord Almighty grant us a peaceful night and a perfect end.", "line_type": "leader"},
        {"content": "Amen.", "line_type": "congregation"}
      ]
    }
  ]
}
```

**Compline Characteristics**:

- **Night Prayer**: Designed for end of day, before sleep
- **Penitential**: Includes confession and absolution
- **Fixed Psalms**: Psalm 4, 31, 91, or 134 (rotates by day of week)
- **Te lucis ante terminum**: Traditional Latin hymn "Before the Ending of the Day"
- **Nunc Dimittis**: Song of Simeon (same as Evening Prayer second canticle)
- **Collect for Protection**: "Lighten our darkness" or seasonal alternative
- **No Lectionary**: Short, fixed scripture passages
- **Peaceful Dismissal**: Blessing for peaceful night and perfect end

---

### GET `/family/{office_type}/{year}/{month}/{day}/`

Generate a family prayer office for a specific date.

**Implements Requirements**: FR-018, FR-019

**Path Parameters**:

- `office_type` (string, required) - Family office type
  - Values: `morning`, `midday`, `early_evening`, `close_of_day`
- `year`, `month`, `day` - Same as standard office endpoints

**Query Parameters**: Same as standard office endpoint (most settings apply)

**Response**: Same structure as standard office endpoint, but with simplified/family-appropriate liturgical content.

**Example Request**:

```http
GET /api/family/morning/2025/12/25/ HTTP/1.1
Host: dailyoffice2019.com
Accept: application/json
```

---

## Resource Endpoints

### GET `/collects/`

Retrieve all collects (prayers).

**Implements Requirements**: FR-009

**Query Parameters**: None

**Success Response** (`200 OK`):

```json
[
  {
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Collect for Purity",
    "text": "<p>Almighty God, to you all hearts are open...</p>",
    "traditional_text": "<p>Almighty God, unto whom all hearts be open...</p>",
    "order": 1,
    "number": null,
    "attribution": "Book of Common Prayer (2019)",
    "tags": [
      {
        "uuid": "...",
        "name": "Morning Prayer",
        "key": "morning_prayer",
        "order": 1,
        "category_name": "Liturgy",
        "category_key": "liturgy",
        "category_order": 1,
        "category_uuid": "..."
      }
    ],
    "title_and_tags": "Collect for Purity Morning Prayer Liturgy"
  },
  ...
]
```

**Field Descriptions**:

- `uuid` - Unique identifier
- `title` - Collect name
- `text` - Contemporary language HTML
- `traditional_text` - Traditional/Elizabethan language HTML (optional)
- `order` - Display order within collect type
- `number` - Collect number if applicable (e.g., Collect for First Sunday of Advent = 1)
- `attribution` - Source attribution
- `tags` - Array of tags for filtering/searching
- `title_and_tags` - Searchable concatenated string

---

### GET `/collects/grouped/`

Retrieve collects organized by source and subcategories.

**Query Parameters**: None

**Success Response** (`200 OK`):

```json
[
  {
    "uuid": "...",
    "key": "year",
    "name": "Collects of the Christian Year",
    "subcategories": [
      {
        "uuid": "...",
        "name": "Advent",
        "key": "advent",
        "order": 1,
        "collects": [
          {
            "uuid": "...",
            "title": "Collect for the First Sunday of Advent",
            "text": "<p>Almighty God, give us grace...</p>",
            ...
          },
          ...
        ]
      },
      {
        "uuid": "...",
        "name": "Christmas",
        "key": "christmas",
        "order": 2,
        "collects": [...]
      },
      ...
    ]
  },
  {
    "uuid": "...",
    "key": "occasional",
    "name": "Occasional Prayers",
    "subcategories": [
      {
        "uuid": "...",
        "name": "For the Church",
        "key": "church",
        "order": 1,
        "collects": [...]
      },
      ...
    ]
  },
  {
    "uuid": "...",
    "key": "liturgical",
    "name": "Collects from Liturgies",
    "subcategories": [...]
  }
]
```

**Grouping Logic**:

- **Collects of the Christian Year**: Grouped by season (Advent, Christmas, Epiphany, Lent, Easter, Pentecost) and commemoration type
- **Occasional Prayers**: Grouped by theme (Church, Nation, Mission, Peace, etc.)
- **Liturgical Collects**: Grouped by liturgy (Morning Prayer, Evening Prayer, Eucharist, etc.)

---

### GET `/collects/categories/`

Retrieve collect tag categories with their tags.

**Success Response** (`200 OK`):

```json
[
  {
    "uuid": "...",
    "name": "Season",
    "key": "season",
    "order": 1,
    "tags": [
      {"uuid": "...", "name": "Advent", "key": "advent", "order": 1},
      {"uuid": "...", "name": "Christmas", "key": "christmas", "order": 2},
      {"uuid": "...", "name": "Epiphany", "key": "epiphany", "order": 3},
      ...
    ]
  },
  {
    "uuid": "...",
    "name": "Theme",
    "key": "theme",
    "order": 2,
    "tags": [
      {"uuid": "...", "name": "Mission", "key": "mission", "order": 1},
      {"uuid": "...", "name": "Peace", "key": "peace", "order": 2},
      ...
    ]
  },
  ...
]
```

---

### GET `/psalms/`

Retrieve all 150 psalms with their verses and topics.

**Implements Requirements**: FR-009

**Success Response** (`200 OK`):

```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "number": 1,
    "latin_title": "Beatus vir",
    "topics": [
      {"id": "...", "topic_name": "Righteousness", "order": 1},
      {"id": "...", "topic_name": "Wisdom", "order": 2}
    ],
    "verses": [
      {
        "id": "...",
        "number": 1,
        "first_half": "Blessed is the man who has not walked in the counsel of the ungodly, *",
        "second_half": "nor stood in the way of sinners, and has not sat in the seat of the scornful;",
        "first_half_tle": "Blessed is the man that hath not walked in the counsel of the ungodly, *",
        "second_half_tle": "nor stood in the way of sinners, and hath not sat in the seat of the scornful;"
      },
      {
        "id": "...",
        "number": 2,
        "first_half": "But his delight is in the law of the Lord, *",
        "second_half": "and on that law will he meditate day and night.",
        "first_half_tle": "But his delight is in the law of the Lord, *",
        "second_half_tle": "and in his law will he exercise himself day and night."
      },
      ...
    ]
  },
  ...
]
```

**Field Descriptions**:

- `id` - Unique identifier (UUID)
- `number` - Psalm number (1-150)
- `latin_title` - Traditional Latin incipit (optional)
- `topics` - Array of thematic topics this psalm belongs to
- `verses` - Array of all verses in the psalm
  - `number` - Verse number within psalm
  - `first_half` - First hemistich (contemporary language)
  - `second_half` - Second hemistich (contemporary language)
  - `first_half_tle` - First hemistich (traditional language edition)
  - `second_half_tle` - Second hemistich (traditional language edition)

**Note**: Asterisk (\*) traditionally marks the metrical pause between hemistichs for antiphonal recitation.

---

### GET `/psalms/{id}/`

Retrieve a specific psalm by ID or number.

**Path Parameters**:

- `id` (string|integer, required) - Psalm UUID or psalm number (1-150)

**Success Response** (`200 OK`):

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "number": 23,
  "latin_title": "Dominus regit me",
  "topics": [
    {"id": "...", "topic_name": "Trust", "order": 3},
    {"id": "...", "topic_name": "Comfort", "order": 5}
  ],
  "verses": [
    {
      "id": "...",
      "number": 1,
      "first_half": "The Lord is my shepherd; *",
      "second_half": "therefore I shall not be in want.",
      "first_half_tle": "The Lord is my shepherd; *",
      "second_half_tle": "therefore can I lack nothing."
    },
    ...
  ]
}
```

**Error Response** (`404 Not Found`):

```json
{
  "detail": "Not found."
}
```

---

### GET `/psalms/topics/`

Retrieve all psalm topics.

**Success Response** (`200 OK`):

```json
[
  {
    "id": "...",
    "topic_name": "Praise",
    "order": 1
  },
  {
    "id": "...",
    "topic_name": "Lament",
    "order": 2
  },
  {
    "id": "...",
    "topic_name": "Trust",
    "order": 3
  },
  ...
]
```

---

### GET `/scripture/{passage}/`

Retrieve cached scripture text for a specific passage.

**Implements Requirements**: FR-020, FR-021, FR-022

**Path Parameters**:

- `passage` (string, required) - Scripture citation (e.g., "John 3:16-21", "Genesis 1:1-5")
  - Can also be UUID of Scripture object
  - Passage must be URL-encoded if it contains special characters

**Success Response** (`200 OK`):

```json
{
  "uuid": "...",
  "passage": "John 3:16-21",
  "esv": "<p><sup>16</sup> For God so loved the world...</p>",
  "kjv": "<p><sup>16</sup> For God so loved the world...</p>",
  "rsv": "<p><sup>16</sup> For God so loved the world...</p>"
}
```

**Field Descriptions**:

- `uuid` - Unique identifier
- `passage` - Citation string
- `esv`, `kjv`, `rsv`, (etc.) - HTML-formatted scripture text for each translation
  - Only includes translations present in cache
  - May be `null` if translation not yet cached

**Error Response** (`404 Not Found`):

```json
{
  "detail": "Not found."
}
```

**Note**: This endpoint returns cached scripture only. If passage not in cache, returns 404. Office generation automatically populates cache from Bible Gateway API when rendering offices.

---

### GET `/settings/`

Retrieve all settings and their options.

**Implements Requirements**: FR-026, FR-027, FR-028

**Success Response** (`200 OK`):

```json
[
  {
    "uuid": "...",
    "name": "psalter",
    "title": "Psalter Cycle",
    "description": "Choose between the 30-day Psalter cycle (based on day of month) or the 60-day Psalter cycle (based on the liturgical calendar).",
    "setting_type": 1,
    "site": 1,
    "order": 1,
    "options": [
      {
        "uuid": "...",
        "name": "30-Day Psalter Cycle",
        "description": "Traditional monthly cycle, repeating every 30 days",
        "value": "30day",
        "abbreviation": "3",
        "order": 1
      },
      {
        "uuid": "...",
        "name": "60-Day Psalter Cycle",
        "description": "BCP 2019 cycle following the liturgical calendar",
        "value": "60day",
        "abbreviation": "6",
        "order": 2
      }
    ]
  },
  {
    "uuid": "...",
    "name": "lectionary",
    "title": "Lectionary Cycle",
    "description": "Choose 1-year cycle if praying one office per day, or 2-year cycle if praying both Morning and Evening Prayer daily.",
    "setting_type": 1,
    "site": 1,
    "order": 2,
    "options": [
      {
        "uuid": "...",
        "name": "One-Year Lectionary",
        "description": "For those praying one office per day",
        "value": "1year",
        "abbreviation": "1",
        "order": 1
      },
      {
        "uuid": "...",
        "name": "Two-Year Lectionary",
        "description": "For those praying both Morning and Evening Prayer",
        "value": "2year",
        "abbreviation": "2",
        "order": 2
      }
    ]
  },
  {
    "uuid": "...",
    "name": "bible_version",
    "title": "Bible Translation",
    "description": "Select your preferred Bible translation for scripture readings.",
    "setting_type": 1,
    "site": 1,
    "order": 3,
    "options": [
      {"uuid": "...", "name": "English Standard Version", "value": "esv", "abbreviation": "E", "order": 1},
      {"uuid": "...", "name": "King James Version", "value": "kjv", "abbreviation": "K", "order": 2},
      {"uuid": "...", "name": "Revised Standard Version", "value": "rsv", "abbreviation": "R", "order": 3},
      {"uuid": "...", "name": "New Revised Standard Version Catholic Edition", "value": "nrsvce", "abbreviation": "N", "order": 4},
      {"uuid": "...", "name": "New American Bible Revised Edition", "value": "nabre", "abbreviation": "A", "order": 5},
      {"uuid": "...", "name": "New International Version", "value": "niv", "abbreviation": "I", "order": 6},
      {"uuid": "...", "name": "New American Standard Bible", "value": "nasb", "abbreviation": "S", "order": 7}
    ]
  },
  ...
]
```

**Field Descriptions**:

- `setting_type`:
  - `1` - Main Settings (primary UI)
  - `2` - Additional Settings
  - `3` - Expert Settings
- `site`:
  - `1` - Daily Office
  - `2` - Family Prayer
- `options[0]` - Default option (first in array)

---

### GET `/about/`

Retrieve FAQ/about items.

**Success Response** (`200 OK`):

```json
[
  {
    "uuid": "...",
    "question": "What is the Daily Office?",
    "question_for_web": "What is the Daily Office?",
    "question_for_app": "What is the Daily Office?",
    "answer": "<p>The Daily Office is...</p>",
    "answer_for_web": "<p>The Daily Office is...</p>",
    "answer_for_app": "<p>The Daily Office is...</p>",
    "order": 1,
    "mode": "both",
    "app_mode": true,
    "web_mode": true
  },
  ...
]
```

**Field Descriptions**:

- `mode`: `"web"`, `"app"`, or `"both"` - Where item should display
- `{field}_for_web` / `{field}_for_app` - Platform-specific variations (replaces `{medium}` placeholder)

---

### GET `/updates/`

Retrieve update notices.

**Success Response** (`200 OK`):

```json
[
  {
    "uuid": "...",
    "notice": "<p>Version 2.5.0 adds...</p>",
    "app_mode": true,
    "web_mode": true,
    "version": 2.5
  },
  ...
]
```

**Note**: Ordered by version descending (newest first).

---

## Calendar Endpoint

### GET `/calendar/`

**Note**: This endpoint is handled by a separate `churchcal` app API. Documentation would be in `002-liturgical-calendar` spec.

**Brief Description**: Returns liturgical calendar data including commemorations, seasons, and church year information.

---

## Common Patterns

### UUID vs. ID Lookups

Many endpoints accept both UUID and alternate identifiers:

- `/psalms/{id}/` accepts psalm number (1-150) or UUID
- `/scripture/{passage}/` accepts passage citation or UUID

**Implementation**: Try UUID parse first; if fails, fall back to alternate identifier.

### Prefetching and Performance

Viewsets use `select_related` and `prefetch_related` to optimize queries:

```python
queryset = Collect.objects.order_by('collect_type__order', 'order') \
    .select_related('collect_type') \
    .prefetch_related('tags__collect_tag_category') \
    .all()
```

### CORS

**Status**: Not explicitly configured in reviewed code.

**Recommendation**: If API intended for third-party use, configure CORS:

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://dailyoffice2019.com",
    "capacitor://localhost",  # Capacitor mobile apps
    "http://localhost:8080",  # Vue dev server
]
```

### Rate Limiting

**Status**: Not implemented in reviewed code.

**Recommendation**: Implement rate limiting for public API:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

### Caching

**Status**: Caching implemented at model level (`@cached_property`) but not at HTTP level.

**Recommendation**: Add HTTP caching for immutable resources:

```python
# Add cache headers for collects, psalms, settings
@method_decorator(cache_page(60 * 60 * 24))  # 24 hours
def list(self, request):
    ...
```

---

## Error Handling

### Standard Error Response Format

```json
{
  "detail": "Error message describing what went wrong."
}
```

### HTTP Status Codes

- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters or request data
- `404 Not Found` - Resource not found (invalid ID, date, or office type)
- `500 Internal Server Error` - Server error (should be rare; indicates bug)

### Validation Errors

When query parameters invalid:

```json
{
  "detail": "Invalid setting value provided.",
  "errors": {
    "bible_version": [
      "Value 'invalid' is not a valid choice. Choose from: esv, kjv, rsv, nrsvce, nabre, niv, nasb"
    ]
  }
}
```

---

## Client-Side Integration

### Vue 3 Frontend Usage

The Vue 3 frontend consumes this API using Axios or Fetch:

```javascript
// Example: Fetch Morning Prayer for today
const response = await fetch(
  `/api/office/morning_prayer/${year}/${month}/${day}/?bible_version=esv`,
  { headers: { Accept: "application/json" } }
);
const office = await response.json();

// Render modules
office.modules.forEach((module) => {
  console.log(`Module: ${module.name}`);
  module.lines.forEach((line) => {
    console.log(`  [${line.line_type}] ${line.content}`);
  });
});
```

### Settings Application

Settings applied via query parameters:

```javascript
const settings = localStorage.getItem("office_settings");
const params = new URLSearchParams(JSON.parse(settings));
const url = `/api/office/morning_prayer/${year}/${month}/${day}/?${params}`;
```

### Client-Side Storage (FR-023, FR-024)

Settings stored in `localStorage`:

```javascript
// Save settings
localStorage.setItem('office_settings', JSON.stringify({
  psalter: '60day',
  lectionary: '2year',
  bible_version: 'esv',
  ...
}));

// Retrieve settings
const settings = JSON.parse(localStorage.getItem('office_settings') || '{}');

// Apply defaults from API
const settingsResponse = await fetch('/api/settings/');
const allSettings = await settingsResponse.json();
const defaults = Object.fromEntries(
  allSettings.map(s => [s.name, s.options[0].value])
);
const mergedSettings = { ...defaults, ...settings };
```

---

## API Versioning

**Current Status**: No explicit API versioning.

**URL Structure**: No `/v1/` prefix currently used.

**Recommendation**: Add API versioning for future-proofing:

```
/api/v1/office/...
/api/v1/collects/...
```

**Breaking Changes**: If API structure changes, version bump required.

---

## Authentication & Authorization

**Current Status**: No authentication required. All endpoints are public.

**Future Considerations**:

- User accounts for syncing settings across devices
- Saved prayer lists / bookmarks
- Personalized liturgical content
- Usage analytics (opt-in)

**Implementation Path** (if adding auth):

1. Django REST Framework Token Authentication
2. JWT for mobile apps (capacitor)
3. OAuth2 for third-party integrations

---

## API Design Principles

### RESTful Resources

The API follows REST principles:

- Resources identified by URLs (`/collects/`, `/psalms/{id}/`)
- Standard HTTP methods (GET primarily; POST/PUT/DELETE not exposed)
- Stateless requests
- JSON representations

### RPC-Style Endpoints

Some endpoints are more RPC-like:

- `/office/{type}/{year}/{month}/{day}/` - Generates office (action-oriented)
- `/collects/grouped/` - Custom action beyond simple resource retrieval
- `/psalms/topics/` - Sub-resource action

This hybrid approach balances REST purity with pragmatic frontend needs.

### Hypermedia (HATEOAS)

Limited hypermedia implementation:

- `navigation` object in office response includes related office links
- No `_links` or HAL-style hypermedia throughout

**Recommendation**: Consider adding more hypermedia for discoverability:

```json
{
  "_links": {
    "self": {"href": "/api/office/morning_prayer/2025/12/25/"},
    "evening": {"href": "/api/office/evening_prayer/2025/12/25/"},
    "calendar": {"href": "/api/calendar/2025/12/25/"}
  },
  ...
}
```

---

## API Documentation Tools

**Current Status**: No OpenAPI/Swagger documentation UI.

**Recommendation**: Add DRF Spectacular for auto-generated OpenAPI docs:

```python
# settings.py
INSTALLED_APPS += ['drf_spectacular']

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

This would provide interactive API documentation at `/api/docs/`.

---

## Summary

The Daily Office REST API is **comprehensive and well-structured** for its primary purpose (serving the Vue 3 frontend). Key strengths:

✅ **Complete functionality** - All spec requirements covered  
✅ **Rich data model** - Detailed liturgical content  
✅ **Flexible customization** - 20+ settings with query param support  
✅ **Efficient queries** - Good use of select_related/prefetch_related  
✅ **Clear response structure** - Consistent JSON format

Areas for improvement:

⚠️ **No formal API documentation** - OpenAPI/Swagger recommended  
⚠️ **No API versioning** - Future-proofing needed  
⚠️ **No rate limiting** - Public API should have limits  
⚠️ **Limited caching** - HTTP cache headers would improve performance  
⚠️ **No CORS configuration** - Limits third-party usage  
⚠️ **Authentication not implemented** - Limits feature potential (syncing, personalization)

The API successfully supports the Daily Office frontend application and is suitable for third-party integrations with minor enhancements.

---

**Document Version**: 1.0  
**Last Updated**: November 6, 2025  
**API Endpoints Documented**: 15+ endpoints across 6 ViewSets
