# Developer Quickstart: Liturgical Calendar

**Feature**: 002-liturgical-calendar  
**Created**: November 6, 2025  
**Audience**: Developers new to the Daily Office calendar system

## Overview

This guide helps you understand and work with the Daily Office 2019 liturgical calendar system. The calendar calculates commemorations, feast days, seasons, and liturgical colors according to the Book of Common Prayer 2019.

## System Architecture

```
┌─────────────────┐
│   Vue Frontend  │
│  (Calendar.vue) │
└────────┬────────┘
         │ HTTP GET
         ▼
┌─────────────────┐
│   Django API    │
│ (calendar/views)│
└────────┬────────┘
         │ Function Call
         ▼
┌─────────────────┐
│  Calculations   │
│(ChurchYear class)│
└────────┬────────┘
         │ Queries
         ▼
┌─────────────────┐
│   PostgreSQL    │
│  (Commemorations)│
└─────────────────┘
```

## Key Concepts

### Church Year vs. Calendar Year

- **Church Year**: Advent to Advent (e.g., Church Year 2024 = Dec 1, 2024 - Nov 30, 2025)
- **Calendar Year**: January to December (spans two church years)
- **Cache Strategy**: Cache church years separately, combine for calendar year queries

### Date Calculation

The system calculates three types of dates:

1. **Fixed Dates** (Sanctorale): Always same calendar date

   - Example: Christmas (December 25)
   - Class: `SanctoraleCommemoration`

2. **Easter-Based** (Temporale): Relative to Easter

   - Example: Ascension Day (39 days after Easter)
   - Class: `TemporaleCommemoration`

3. **Relative to Fixed Date** (Sanctorale-Based): Nth weekday after fixed date
   - Example: Sunday after All Saints
   - Class: `SanctoraleBasedCommemoration`

### Precedence and Transfers

When multiple commemorations fall on the same date:

1. Sort by `precedence_rank` (1 = highest)
2. Keep highest-precedence commemoration
3. Transfer lower-precedence to next available day
4. Exception: Sundays and privileged seasons are protected

### First Vespers

Major feasts (precedence ≤ 4) have First Vespers on the evening before:

- Evening of December 24 → "Eve of Christmas Day" (uses Christmas colors)
- Morning of December 24 → Regular Advent (purple/blue)

## Working with the Code

### Get Calendar Data for a Date

```python
from churchcal.calculations import get_calendar_date
from datetime import date

# Get a specific date
calendar_date = get_calendar_date(date(2024, 12, 25))

# Access properties
print(calendar_date.primary.name)  # "The Nativity of Our Lord..."
print(calendar_date.season.name)   # "Christmastide"
print(calendar_date.primary.color) # "white"

# Check for multiple commemorations
for commemoration in calendar_date.all:
    print(f"{commemoration.name} ({commemoration.rank.formatted_name})")

# Check evening (First Vespers)
if hasattr(calendar_date, 'evening_required'):
    for evening_comm in calendar_date.evening_required:
        print(f"Evening: {evening_comm.name}")
```

### Get Entire Month

```python
from churchcal.calculations import get_calendar_year

# Get calendar year (Jan-Dec)
calendar_year = get_calendar_year(2024, "ACNA_BCP2019")

# Filter to specific month
december_dates = [
    date for date in calendar_year
    if date.date.month == 12 and date.date.year == 2024
]

# Iterate through month
for calendar_date in december_dates:
    print(f"{calendar_date.date}: {calendar_date.primary.name}")
```

### Access Church Year

```python
from churchcal.calculations import ChurchYear

# Get church year (Advent to Advent)
church_year = ChurchYear(2024)  # Advent 2024 - November 2025

# Properties
print(church_year.mass_year)      # "A", "B", or "C"
print(church_year.office_year)    # "I" or "II"
print(church_year.start_date)     # First Sunday of Advent 2024
print(church_year.end_date)       # Day before Advent 2025

# Iterate through year
for calendar_date in church_year:
    if calendar_date.primary.rank.name == "PRINCIPAL_FEAST":
        print(f"{calendar_date.date}: {calendar_date.primary.name}")
```

### Query Commemorations

```python
from churchcal.models import Commemoration, CommemorationRank, Calendar

# Get calendar system
calendar = Calendar.objects.get(abbreviation="ACNA_BCP2019")

# Query by rank
principal_feasts = Commemoration.objects.filter(
    calendar=calendar,
    rank__name="PRINCIPAL_FEAST"
).select_related('rank')

for feast in principal_feasts:
    print(f"{feast.name} - {feast.color}")

# Query by date (Sanctorale only)
from churchcal.models import SanctoraleCommemoration

christmas = SanctoraleCommemoration.objects.get(
    calendar=calendar,
    month=12,
    day=25
)
print(christmas.name)  # "The Nativity of Our Lord..."
```

### Calculate Easter and Advent

```python
from churchcal.utils import easter, advent

# Easter calculation
easter_2024 = easter(2024)  # March 31, 2024
easter_2025 = easter(2025)  # April 20, 2025

# Advent calculation
advent_2024 = advent(2024)  # December 1, 2024
advent_2025 = advent(2025)  # November 30, 2025

# Calculate moveable feast
from datetime import timedelta
ascension_2024 = easter_2024 + timedelta(days=39)  # May 9, 2024
```

## API Usage

### Get a Single Day

```bash
curl https://api.dailyoffice2019.com/api/v1/calendar/2024/12/25
```

Response:

```json
{
  "date": "2024-12-25",
  "season": {
    "name": "Christmastide",
    "colors": ["white"]
  },
  "commemorations": [
    {
      "name": "The Nativity of Our Lord Jesus Christ: Christmas Day",
      "colors": ["white"],
      "rank": {
        "name": "PRINCIPAL_FEAST",
        "formatted_name": "Principal Feast",
        "precedence_rank": 1,
        "required": true
      }
    }
  ],
  "major_feast": "The Nativity of Our Lord Jesus Christ: Christmas Day",
  "proper": null
}
```

### Get an Entire Month

```bash
curl https://api.dailyoffice2019.com/api/v1/calendar/2024-12
```

Returns array of Day objects for all dates in December 2024.

### Get a Church Year

```bash
curl https://api.dailyoffice2019.com/api/v1/calendar/year/2024
```

Returns array of Day objects from Advent 2024 through November 2025.

## Frontend Integration

### Display Calendar Colors

```javascript
// In Vue component
getColorForDate(day) {
  const commemorations = this.days[day].commemorations;

  if (this.includeMinorFeasts) {
    // Show all commemorations, exclude feria
    const filtered = commemorations.filter(c =>
      !c.rank.name.includes('FERIA')
    );
    if (filtered.length === 0) {
      return this.days[day].season.colors[0];
    }
    return filtered[0].colors[0];
  } else {
    // Show only required commemorations
    if (this.days[day].major_feast) {
      return commemorations[0].colors[0];
    }
    return this.days[day].season.colors[0];
  }
}
```

### Navigate to Daily Office

```javascript
async clickDateCell(data, event) {
  event.preventDefault();
  const day = data.day.split('-');
  await this.$router.push({
    name: 'day',
    params: {
      year: day[0],
      month: day[1],
      day: day[2]
    }
  });
}
```

## Testing

### Unit Test: Date Calculations

```python
from django.test import TestCase
from churchcal.utils import easter, advent
from datetime import date

class DateCalculationTest(TestCase):
    def test_easter_2024(self):
        """Easter 2024 should be March 31"""
        result = easter(2024)
        self.assertEqual(result, date(2024, 3, 31))

    def test_advent_2024(self):
        """Advent 2024 should be December 1"""
        result = advent(2024)
        self.assertEqual(result, date(2024, 12, 1))
```

### Integration Test: API Endpoint

```python
from rest_framework.test import APITestCase
from django.utils import timezone

class CalendarAPITest(APITestCase):
    def test_get_day(self):
        """Test retrieving a specific day"""
        response = self.client.get('/api/v1/calendar/2024/12/25')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['date'], '2024-12-25')
        self.assertIn('commemorations', data)
        self.assertEqual(data['season']['name'], 'Christmastide')
```

### Component Test: Calendar.vue

```javascript
import { mount } from "@vue/test-utils";
import Calendar from "@/views/Calendar.vue";

describe("Calendar.vue", () => {
  it("displays correct color for feast day", () => {
    const wrapper = mount(Calendar, {
      data() {
        return {
          days: {
            "2024-12-25": {
              season: { colors: ["white"] },
              commemorations: [
                {
                  colors: ["white"],
                  rank: { name: "PRINCIPAL_FEAST", required: true },
                },
              ],
              major_feast: "Christmas Day",
            },
          },
          includeMinorFeasts: false,
        };
      },
    });

    const color = wrapper.vm.getColorForDate("2024-12-25");
    expect(color).toBe("white");
  });
});
```

## Database Schema Reference

### Key Tables

```sql
-- Calendar systems
CREATE TABLE churchcal_calendar (
    id UUID PRIMARY KEY,
    name VARCHAR(256),
    abbreviation VARCHAR(256) UNIQUE,
    year VARCHAR(256)
);

-- Commemoration ranks
CREATE TABLE churchcal_commemorationrank (
    id UUID PRIMARY KEY,
    name VARCHAR(256),
    formatted_name VARCHAR(256),
    precedence_rank SMALLINT CHECK (precedence_rank BETWEEN 1 AND 9),
    required BOOLEAN,
    calendar_id UUID REFERENCES churchcal_calendar
);

-- Base commemoration table (polymorphic)
CREATE TABLE churchcal_commemoration (
    id UUID PRIMARY KEY,
    name VARCHAR(256),
    rank_id UUID REFERENCES churchcal_commemorationrank,
    color VARCHAR(256),
    alternate_color VARCHAR(256),
    calendar_id UUID REFERENCES churchcal_calendar,
    -- Polymorphic type fields for inheritance
    month SMALLINT,  -- SanctoraleCommemoration
    day SMALLINT,    -- SanctoraleCommemoration
    days_after_easter SMALLINT  -- TemporaleCommemoration
);

-- Seasons
CREATE TABLE churchcal_season (
    id UUID PRIMARY KEY,
    name VARCHAR(1024),
    color VARCHAR(255),
    alternate_color VARCHAR(255),
    calendar_id UUID REFERENCES churchcal_calendar
);
```

### Add a New Commemoration

```python
from churchcal.models import (
    SanctoraleCommemoration,
    CommemorationRank,
    Calendar
)

calendar = Calendar.objects.get(abbreviation="ACNA_BCP2019")
rank = CommemorationRank.objects.get(
    calendar=calendar,
    name="FEAST"
)

# Add fixed-date commemoration
new_saint = SanctoraleCommemoration.objects.create(
    name="St. New Saint",
    month=6,
    day=15,
    color="white",
    rank=rank,
    calendar=calendar,
    saint_name="New Saint",
    saint_type="MARTYR"
)
```

## Common Patterns

### Pattern 1: Get Today's Commemorations

```python
from churchcal.calculations import get_calendar_date
from datetime import date

def get_todays_commemorations():
    today = date.today()
    calendar_date = get_calendar_date(today)
    return {
        'primary': calendar_date.primary.name,
        'season': calendar_date.season.name,
        'color': calendar_date.primary.color,
        'all': [c.name for c in calendar_date.all]
    }
```

### Pattern 2: Find Next Major Feast

```python
from churchcal.calculations import ChurchYear
from datetime import date

def next_major_feast(start_date=None):
    if start_date is None:
        start_date = date.today()

    church_year = ChurchYear(start_date.year)

    for calendar_date in church_year:
        if calendar_date.date <= start_date:
            continue

        if calendar_date.primary.rank.precedence_rank <= 4:
            return {
                'date': calendar_date.date,
                'name': calendar_date.primary.name,
                'color': calendar_date.primary.color
            }

    return None
```

### Pattern 3: List All Sundays in Season

```python
from churchcal.calculations import ChurchYear

def sundays_in_season(year, season_name):
    church_year = ChurchYear(year)
    sundays = []

    for calendar_date in church_year:
        if calendar_date.season.name == season_name:
            if calendar_date.date.weekday() == 6:  # Sunday
                sundays.append({
                    'date': calendar_date.date,
                    'name': calendar_date.primary.name,
                    'proper': calendar_date.proper.number if calendar_date.proper else None
                })

    return sundays

# Usage
advent_sundays = sundays_in_season(2024, "Advent")
for sunday in advent_sundays:
    print(f"{sunday['date']}: {sunday['name']}")
```

## Performance Tips

### 1. Use Caching

Church years are cached for 12 hours. Don't bypass the cache unless necessary.

```python
# Good - uses cache
from churchcal.calculations import get_calendar_date
calendar_date = get_calendar_date(date(2024, 12, 25))

# Bad - bypasses cache (don't do this)
church_year = ChurchYear(2024)  # Forces recalculation
```

### 2. Batch Queries

Get a month at once rather than individual days.

```python
# Good
calendar_year = get_calendar_year(2024, "ACNA_BCP2019")
december = [d for d in calendar_year if d.date.month == 12]

# Bad
days = [get_calendar_date(date(2024, 12, d)) for d in range(1, 32)]
```

### 3. Use select_related()

When querying commemorations, load related objects.

```python
# Good
commemorations = Commemoration.objects.filter(
    calendar=calendar
).select_related('rank', 'season')

# Bad - causes N+1 queries
commemorations = Commemoration.objects.filter(calendar=calendar)
for comm in commemorations:
    print(comm.rank.name)  # Separate query each time
```

## Debugging Tips

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from churchcal.calculations import get_calendar_date
calendar_date = get_calendar_date(date(2024, 12, 25))
```

### Inspect CalendarDate

```python
calendar_date = get_calendar_date(date(2024, 12, 25))

# Print full details
print(repr(calendar_date))

# Check all commemorations
print("Required:", [c.name for c in calendar_date.required])
print("Optional:", [c.name for c in calendar_date.optional])

# Check transfers
for comm in calendar_date.required:
    if hasattr(comm, 'transferred') and comm.transferred:
        print(f"Transferred: {comm.name}")
```

### Check First Vespers Logic

```python
calendar_date = get_calendar_date(date(2024, 12, 24))

print("Morning season:", calendar_date.season.name)
print("Morning primary:", calendar_date.primary.name)

if hasattr(calendar_date, 'evening_season'):
    print("Evening season:", calendar_date.evening_season.name)
    print("Evening commemorations:",
          [c.name for c in calendar_date.evening_required])
```

## Troubleshooting

### Issue: Date not found in ChurchYear

**Problem**: `KeyError` when accessing date in church year.

**Solution**: Date may be outside church year range. Use `CalendarYear` for calendar year queries.

```python
# Wrong - date outside church year 2024
church_year = ChurchYear(2024)
date_obj = church_year.get_date("2024-01-15")  # KeyError

# Right - use calendar year
calendar_year = get_calendar_year(2024, "ACNA_BCP2019")
date_obj = calendar_year.dates["2024-01-15"]
```

### Issue: Commemoration not appearing

**Problem**: Added new commemoration to database but doesn't show on calendar.

**Solution**: Clear cache and verify commemoration can occur in that year.

```python
from django.core.cache import cache
cache.clear()  # Clear all cached church years

# Check if commemoration can occur
from churchcal.models import Commemoration
comm = Commemoration.objects.get(name="...")
print(comm.can_occur_in_year(2024))  # Should be True
```

### Issue: Wrong color displaying

**Problem**: UI shows wrong liturgical color.

**Solution**: Check color cascade logic (primary → additional → alternate).

```python
commemoration = calendar_date.primary
print("Primary color:", commemoration.color)
print("Additional:", commemoration.additional_color)
print("Alternate:", commemoration.alternate_color)
print("Alternate 2:", commemoration.alternate_color_2)
```

## Next Steps

1. **Read the Specification**: See `specs/002-liturgical-calendar/spec.md` for requirements
2. **Review Data Model**: See `plan/data-model.md` for entity details
3. **Check API Contract**: See `contracts/api.yaml` for API documentation
4. **Run Tests**: `python manage.py test churchcal` (after tests are added)
5. **Explore Frontend**: Review `app/src/views/Calendar.vue` for UI implementation

## Additional Resources

- **BCP 2019 Calendar Rules**: https://bcp2019.anglicanchurch.net/
- **Django Documentation**: https://docs.djangoproject.com/
- **Vue.js Guide**: https://vuejs.org/guide/
- **Element Plus Calendar**: https://element-plus.org/en-US/component/calendar.html

---

**Document Version**: 1.0  
**Last Updated**: November 6, 2025  
**Questions?**: Open an issue or ask in team chat
