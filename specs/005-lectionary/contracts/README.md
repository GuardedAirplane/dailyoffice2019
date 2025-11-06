# API Contracts: Lectionary

**Feature**: 005-lectionary  
**Date**: 2025-11-06  
**Status**: Retroactive Documentation  
**Base URL**: `https://api.dailyoffice2019.com` (production) or `https://127.0.0.1:8000` (development)

This document details the REST API endpoints supporting the lectionary functionality for Daily Office readings and Holy Eucharist readings according to BCP 2019.

## Table of Contents

1. [Overview](#overview)
2. [Daily Office Readings API](#daily-office-readings-api)
3. [Scripture Text API](#scripture-text-api)
4. [Calendar API](#calendar-api)
5. [Common Response Patterns](#common-response-patterns)
6. [Error Handling](#error-handling)

---

## Overview

### API Structure

The Daily Office 2019 API uses RESTful design with:

- **JSON responses**: All endpoints return JSON (or JSON-LD for specific endpoints)
- **Date-based routing**: Most endpoints use `YYYY-MM-DD` date format in URL path
- **Stateless**: No authentication required for read operations
- **CORS enabled**: Accessible from web applications

### API Documentation

- **Swagger UI**: `GET /api/` - Interactive API documentation
- **ReDoc**: `GET /api/redoc/` - Alternative documentation view
- **OpenAPI Schema**: `GET /api/openapi.json` - Machine-readable API spec

### Implements Requirements

- **FR-001**: Daily Office reading assignments
- **FR-004**: Eucharist reading assignments
- **FR-005**: Full scripture text retrieval
- **FR-006, FR-007**: Multiple translation support
- **FR-012**: View readings for any date

---

## Daily Office Readings API

### GET `/api/v1/readings/{year}-{month}-{day}`

Retrieve complete reading assignments (psalms and scripture) for both Morning Prayer and Evening Prayer for a specific date.

**Implements**: FR-001, FR-002, FR-003, FR-009, FR-012

#### Path Parameters

| Parameter | Type    | Description         | Example |
| --------- | ------- | ------------------- | ------- |
| `year`    | integer | Four-digit year     | `2025`  |
| `month`   | integer | Month (1-12)        | `11`    |
| `day`     | integer | Day of month (1-31) | `6`     |

#### Success Response (`200 OK`)

```json
{
  "date": "2025-11-06",
  "daily_office_year": 2,
  "week_of_year": 45,
  "season": "Ordinary Time after Pentecost",
  "readings": {
    "morning_prayer": {
      "psalms": {
        "cycle_60_day": "119:1-24",
        "cycle_30_day": "119:1-32",
        "current_cycle": "60_day"
      },
      "readings": [
        {
          "number": 1,
          "citation": "2 Kings 18:1-16",
          "testament": "OT",
          "passage": "2 Kings 18:1-16",
          "abbreviated": null,
          "full": {
            "citation": "2 Kings 18:1-16",
            "passage": "2 Kings 18:1-16",
            "testament": "OT",
            "deuterocanon": false
          }
        },
        {
          "number": 2,
          "citation": "Acts 26:1-23",
          "testament": "NT",
          "passage": "Acts 26:1-23",
          "abbreviated": null,
          "full": {
            "citation": "Acts 26:1-23",
            "passage": "Acts 26:1-23",
            "testament": "NT",
            "deuterocanon": false
          }
        }
      ]
    },
    "evening_prayer": {
      "psalms": {
        "cycle_60_day": "119:25-48",
        "cycle_30_day": "119:33-64",
        "current_cycle": "60_day"
      },
      "readings": [
        {
          "number": 1,
          "citation": "Wisdom 7:15-8:4",
          "testament": "DC",
          "passage": "Wisdom 7:15-8:4",
          "abbreviated": "Wisdom 7:22-8:1",
          "full": {
            "citation": "Wisdom 7:15-8:4",
            "passage": "Wisdom 7:15-8:4",
            "testament": "DC",
            "deuterocanon": true
          },
          "abbreviated_reading": {
            "citation": "Wisdom 7:22-8:1",
            "passage": "Wisdom 7:22-8:1",
            "testament": "DC",
            "deuterocanon": true
          }
        },
        {
          "number": 2,
          "citation": "John 14:15-31",
          "testament": "NT",
          "passage": "John 14:15-31",
          "abbreviated": null,
          "full": {
            "citation": "John 14:15-31",
            "passage": "John 14:15-31",
            "testament": "NT",
            "deuterocanon": false
          }
        }
      ]
    }
  },
  "feast_day": null,
  "commemoration": {
    "name": "Thursday in the Twenty-third Week after Pentecost",
    "rank": "FERIA",
    "color": "green"
  }
}
```

#### Field Descriptions

**Top-Level Fields**:

- `date`: ISO 8601 date string (YYYY-MM-DD)
- `daily_office_year`: Lectionary cycle year (1 or 2) for Daily Office
- `week_of_year`: Week number in liturgical year
- `season`: Current liturgical season name
- `commemoration`: Object with name, rank, and liturgical color for the day
- `feast_day`: Feast name if holy day, otherwise null

**Psalm Object**:

- `cycle_60_day`: Psalm citation for 60-day psalter cycle (BCP 2019 default)
- `cycle_30_day`: Psalm citation for 30-day psalter cycle (alternative)
- `current_cycle`: Which cycle is currently displayed ("60_day" or "30_day")

**Reading Object**:

- `number`: Reading position (1 or 2)
- `citation`: Full scripture citation
- `testament`: Testament code - "OT" (Old Testament), "NT" (New Testament), "DC" (Deuterocanon), "AP" (Apocrypha)
- `passage`: Passage identifier (same as citation typically)
- `abbreviated`: Shorter alternative reading citation, or null if none
- `full`: Object with full reading details
- `abbreviated_reading`: Object with abbreviated reading details (if exists)
- `deuterocanon`: Boolean - true if passage is from Apocrypha/Deuterocanonical books

**Translation Handling**: Frontend determines which translation to display based on user preference. If selected translation lacks deuterocanonical books (ESV, NIV, NASB) and `deuterocanon: true`, frontend automatically falls back to NRSVCE.

#### Error Responses

**404 Not Found** - Date outside supported range:

```json
{
  "error": "Readings not available for this date",
  "supported_range": {
    "start": "2018-12-02",
    "end": "2021-12-04"
  }
}
```

**400 Bad Request** - Invalid date:

```json
{
  "error": "Invalid date format. Use YYYY-MM-DD."
}
```

#### Usage Examples

```bash
# Get today's readings
curl https://api.dailyoffice2019.com/api/v1/readings/2025-11-06

# Get Christmas Day readings
curl https://api.dailyoffice2019.com/api/v1/readings/2025-12-25

# Get readings for a date in the past
curl https://api.dailyoffice2019.com/api/v1/readings/2023-06-15
```

---

## Scripture Text API

### GET `/api/v1/scripture/{passage}`

Retrieve cached scripture text for a specific passage in all available translations.

**Implements**: FR-005, FR-006, FR-010, FR-016

#### Path Parameters

| Parameter | Type   | Description                | Examples                                           |
| --------- | ------ | -------------------------- | -------------------------------------------------- |
| `passage` | string | Scripture citation or UUID | `"Genesis 1:1-31"`, `"Psalm 23"`, `"John 3:16-21"` |

**Note**: Passage must be URL-encoded if it contains special characters (spaces, colons, etc.).

#### Success Response (`200 OK`)

```json
{
  "uuid": "12345678-1234-5678-1234-567812345678",
  "passage": "Genesis 1:1-31",
  "esv": "<p><sup>1</sup>In the beginning, God created the heavens and the earth...</p>",
  "kjv": "<p><sup>1</sup>In the beginning God created the heaven and the earth...</p>",
  "rsv": "<p><sup>1</sup>In the beginning God created the heavens and the earth...</p>",
  "nrsv": "<p><sup>1</sup>In the beginning when God created the heavens and the earth...</p>",
  "nrsvce": "<p><sup>1</sup>In the beginning when God created the heavens and the earth...</p>",
  "nabre": "<p><sup>1</sup>In the beginning, when God created the heavens and the earth...</p>",
  "niv": "<p><sup>1</sup>In the beginning God created the heavens and the earth...</p>",
  "nasb": "<p><sup>1</sup>In the beginning God created the heavens and the earth...</p>",
  "coverdale": null,
  "renewed_coverdale": null
}
```

#### Field Descriptions

- `uuid`: Unique identifier for this Scripture record
- `passage`: Citation string
- `esv`, `kjv`, `rsv`, `nrsv`, `nrsvce`, `nabre`, `niv`, `nasb`: HTML-formatted scripture text in each translation
- `coverdale`, `renewed_coverdale`: Psalm text in traditional psalm translations (null for non-psalm passages)

#### HTML Structure

Scripture text includes:

- `<p>` tags for paragraphs
- `<sup>` tags for verse numbers
- `<h3>`, `<h4>` tags for section headings (from translation)
- Semantic HTML preserving translation formatting

Example HTML fragment:

```html
<p>
  <sup>1</sup>In the beginning, God created the heavens and the earth.
  <sup>2</sup>The earth was without form and void, and darkness was over the
  face of the deep.
</p>
<h3>The Creation of Light</h3>
<p><sup>3</sup>And God said, "Let there be light," and there was light.</p>
```

#### Error Responses

**404 Not Found** - Passage not in cache:

```json
{
  "error": "Scripture not found for passage",
  "passage": "Invalid Citation"
}
```

**400 Bad Request** - Invalid passage format:

```json
{
  "error": "Invalid scripture citation format"
}
```

#### Usage Examples

```bash
# Get Genesis 1
curl https://api.dailyoffice2019.com/api/v1/scripture/Genesis%201:1-31

# Get Psalm 23
curl https://api.dailyoffice2019.com/api/v1/scripture/Psalm%2023

# Get John's Gospel prologue
curl https://api.dailyoffice2019.com/api/v1/scripture/John%201:1-18

# Get by UUID
curl https://api.dailyoffice2019.com/api/v1/scripture/12345678-1234-5678-1234-567812345678
```

#### Special Considerations

**Deuterocanonical Books**: Passages from Wisdom, Sirach, Tobit, Judith, 1-2 Maccabees, Baruch, and additions to Esther/Daniel:

- Available in: `nrsvce`, `nabre`
- Not available in: `esv`, `kjv`, `niv`, `nasb`
- Frontend implements automatic fallback (see FR-014)

**Multi-Chapter Passages**: Passages spanning multiple chapters (e.g., "Genesis 1:1-2:3") are handled correctly with all verses included.

**Discontinued Passages**: Passages with omitted verses (e.g., "Matthew 1:1-17, omitting 1-5") are supported; citation reflects full range, text matches API provider's interpretation.

---

## Calendar API

### GET `/api/v1/calendar/{year}-{month}-{day}`

Retrieve full liturgical calendar information for a specific date, including commemorations, feasts, and Eucharist lectionary details.

**Implements**: FR-004 (Eucharist readings), FR-008 (feast day readings), FR-013 (cycles)

#### Path Parameters

| Parameter | Type    | Description         | Example |
| --------- | ------- | ------------------- | ------- |
| `year`    | integer | Four-digit year     | `2025`  |
| `month`   | integer | Month (1-12)        | `12`    |
| `day`     | integer | Day of month (1-31) | `25`    |

#### Success Response (`200 OK`)

```json
{
  "date": "2025-12-25",
  "season": {
    "name": "Christmas",
    "color": "white",
    "start_date": "2025-12-25",
    "end_date": "2026-01-05"
  },
  "week": {
    "name": "Christmas Day",
    "number": 0,
    "of_season": 1
  },
  "commemorations": [
    {
      "uuid": "...",
      "name": "The Nativity of Our Lord Jesus Christ (Christmas Day)",
      "rank": "PRINCIPAL_FEAST",
      "precedence": 1,
      "color": "white",
      "additional_color": "gold",
      "alternate_color": null,
      "color_notes": "White or Gold",
      "type": "sanctorale",
      "month": 12,
      "day": 25,
      "collects": [
        {
          "uuid": "...",
          "title": "Christmas Day",
          "text": "Almighty God, you have given your only-begotten Son...",
          "traditional_text": "Almighty God, who hast given us thy only-begotten Son..."
        }
      ]
    }
  ],
  "primary": {
    "uuid": "...",
    "name": "The Nativity of Our Lord Jesus Christ (Christmas Day)",
    "rank": "PRINCIPAL_FEAST",
    "color": "white"
  },
  "eucharist_lectionary": {
    "year": "B",
    "cycle_year": "B",
    "lectionary_items": [
      {
        "uuid": "...",
        "name": "Christmas Day",
        "service": "Principal Service",
        "readings": {
          "prophecy": [
            {
              "reading_number": 1,
              "reading_type": "prophecy",
              "citation": "Isaiah 9:2-7",
              "short_citation": null,
              "years": "ABC",
              "testament": "OT",
              "long_scripture_uuid": "...",
              "short_scripture_uuid": null
            }
          ],
          "psalm": [
            {
              "reading_number": 2,
              "reading_type": "psalm",
              "citation": "Psalm 96",
              "short_citation": "Psalm 96:1-9",
              "years": "ABC",
              "testament": "OT",
              "long_scripture_uuid": "...",
              "short_scripture_uuid": "..."
            }
          ],
          "epistle": [
            {
              "reading_number": 3,
              "reading_type": "epistle",
              "citation": "Titus 2:11-14",
              "short_citation": null,
              "years": "ABC",
              "testament": "NT",
              "long_scripture_uuid": "...",
              "short_scripture_uuid": null
            }
          ],
          "gospel": [
            {
              "reading_number": 4,
              "reading_type": "gospel",
              "citation": "Luke 2:1-20",
              "short_citation": "Luke 2:1-14",
              "years": "ABC",
              "testament": "NT",
              "long_scripture_uuid": "...",
              "short_scripture_uuid": "..."
            }
          ]
        }
      }
    ]
  },
  "daily_office_year": 2
}
```

#### Field Descriptions

**Top-Level Fields**:

- `date`: ISO 8601 date string
- `season`: Current liturgical season details
- `week`: Week information within liturgical year
- `commemorations`: Array of all commemorations for this date (may include multiple)
- `primary`: The primary commemoration determining readings and collects
- `eucharist_lectionary`: Holy Eucharist reading details
- `daily_office_year`: Daily Office lectionary cycle (1 or 2)

**Eucharist Lectionary Object**:

- `year`: Eucharist cycle year ("A", "B", or "C")
- `cycle_year`: Same as `year` (deprecated duplicate)
- `lectionary_items`: Array of lectionary sets (may have multiple services: Principal, Early, Evening)

**Lectionary Item Object**:

- `name`: Feast or proper name
- `service`: Service type ("Principal Service", "Early Service", "Evening Service", etc.)
- `readings`: Object with four reading types (prophecy, psalm, epistle, gospel)

**Reading Object**:

- `reading_number`: Position (1-4): 1=Prophecy/OT, 2=Psalm, 3=Epistle, 4=Gospel
- `reading_type`: "prophecy", "psalm", "epistle", or "gospel"
- `citation`: Full scripture citation for long reading
- `short_citation`: Abbreviated alternative citation, or null
- `years`: Which cycle years use this reading ("A", "B", "C", "AB", "AC", "BC", "ABC")
- `testament`: Testament code (OT/NT/DC/AP)
- `long_scripture_uuid`: UUID of Scripture object for full reading
- `short_scripture_uuid`: UUID of Scripture object for abbreviated reading, or null

#### Usage Examples

```bash
# Get calendar for Christmas
curl https://api.dailyoffice2019.com/api/v1/calendar/2025-12-25

# Get calendar for Easter
curl https://api.dailyoffice2019.com/api/v1/calendar/2025-04-20

# Get calendar for regular Sunday
curl https://api.dailyoffice2019.com/api/v1/calendar/2025-11-09
```

---

## Common Response Patterns

### Pagination

Endpoints returning lists do not implement pagination (all results returned).

### Date Formats

All dates use **ISO 8601** format: `YYYY-MM-DD`

### Testament Codes

| Code | Meaning                                     |
| ---- | ------------------------------------------- |
| `OT` | Old Testament                               |
| `NT` | New Testament                               |
| `DC` | Deuterocanon (Catholic/Orthodox canon)      |
| `AP` | Apocrypha (Anglican/Protestant term for DC) |

**Note**: `DC` and `AP` are used interchangeably depending on context; both indicate deuterocanonical books.

### Liturgical Colors

| Color    | Usage                                              |
| -------- | -------------------------------------------------- |
| `white`  | Feasts of our Lord, saints' days, Easter season    |
| `red`    | Pentecost, martyrs, Holy Week                      |
| `green`  | Ordinary Time                                      |
| `purple` | Advent, Lent                                       |
| `blue`   | Alternative for Advent (modern usage)              |
| `rose`   | Gaudete Sunday (Advent 3), Laetare Sunday (Lent 4) |
| `gold`   | Alternative for major feasts                       |

---

## Error Handling

### Standard Error Response Format

```json
{
  "error": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional context"
  }
}
```

### HTTP Status Codes

| Code  | Meaning               | Usage                                              |
| ----- | --------------------- | -------------------------------------------------- |
| `200` | OK                    | Successful request                                 |
| `400` | Bad Request           | Invalid date format, malformed parameters          |
| `404` | Not Found             | Date outside supported range, scripture not cached |
| `500` | Internal Server Error | Unexpected server error                            |

### Common Error Scenarios

**Date Outside Range**:

```json
{
  "error": "Readings not available for this date",
  "supported_range": {
    "start": "2018-12-02",
    "end": "2021-12-04"
  }
}
```

**Scripture Not Cached**:

```json
{
  "error": "Scripture not found for passage",
  "passage": "Invalid Citation",
  "suggestion": "Check citation format and try again"
}
```

---

## Additional Endpoints (Brief)

### GET `/api/v1/psalms/{number}`

Retrieve specific psalm text in Coverdale and Renewed Coverdale translations.

### GET `/api/v1/collects`

Retrieve list of all collects (prayers) in BCP 2019.

### GET `/api/v1/calendar/{year}-{month}`

Retrieve full month calendar with all commemorations.

### GET `/api/v1/calendar/{year}`

Retrieve full year calendar with all commemorations.

---

## Requirements Traceability

| Requirement                               | Endpoint(s)                                                  | Notes                             |
| ----------------------------------------- | ------------------------------------------------------------ | --------------------------------- |
| FR-001: Daily Office reading assignments  | `GET /api/v1/readings/{date}`                                | Returns MP and EP assignments     |
| FR-002: Psalm assignments (60-day/30-day) | `GET /api/v1/readings/{date}`                                | Returns both cycles               |
| FR-003: Two scripture readings per office | `GET /api/v1/readings/{date}`                                | Readings array has 2 items        |
| FR-004: Eucharist readings (3-year cycle) | `GET /api/v1/calendar/{date}`                                | eucharist_lectionary section      |
| FR-005: Full scripture text               | `GET /api/v1/scripture/{passage}`                            | All translations returned         |
| FR-006: Multiple translations             | `GET /api/v1/scripture/{passage}`                            | 9 translations supported          |
| FR-007: Translation selection             | (Frontend)                                                   | API returns all; frontend selects |
| FR-008: Feast day proper readings         | `GET /api/v1/readings/{date}`, `GET /api/v1/calendar/{date}` | Feast readings override standard  |
| FR-009: Office type indication            | Response structure                                           | Separate MP/EP sections           |
| FR-010: Multi-chapter passages            | `GET /api/v1/scripture/{passage}`                            | Handled by citation parsing       |
| FR-012: View any date                     | All date-based endpoints                                     | No date restrictions in API       |
| FR-016: Clear citations                   | All reading responses                                        | Citation field always present     |

---

## Performance Notes

**Target Performance** (per Success Criteria):

- **SC-001**: Display today's readings < 2 seconds → API response time ~50-100ms
- **SC-002**: Full scripture text < 3 seconds → API response time ~10-20ms (cached)
- **SC-005**: Translation switching < 2 seconds → No API call (all translations in response)

**Caching Strategy**:

- Database cache for all scripture text
- Memcached for full API responses (24-hour TTL)
- Frontend service worker for offline access

---

## References

- **OpenAPI Spec**: `GET /api/openapi.json`
- **Swagger UI**: https://api.dailyoffice2019.com/api/
- **ReDoc**: https://api.dailyoffice2019.com/api/redoc/
- **Source Code**: `site/office/api/views/`, `site/churchcal/api/views/`, `site/website/api_urls.py`

---

**Document Status**: Retroactive API documentation based on existing implementation. API is stable and in production use.
