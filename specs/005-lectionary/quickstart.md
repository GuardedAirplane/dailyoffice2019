# Quickstart Guide: Lectionary Development

**Feature**: 005-lectionary  
**Date**: 2025-11-06  
**Audience**: Developers working with lectionary functionality

This guide provides practical instructions for working with the Daily Office 2019 lectionary system, including viewing readings, importing data, adding translations, and testing changes.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Viewing Readings](#viewing-readings)
3. [Working with Scripture Text](#working-with-scripture-text)
4. [Managing Lectionary Data](#managing-lectionary-data)
5. [Testing Lectionary Functionality](#testing-lectionary-functionality)
6. [Common Development Tasks](#common-development-tasks)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

Before working with lectionary functionality, ensure you have:

1. **Environment Set Up**: Follow `.github/copilot-instructions.md` bootstrap steps
2. **Database Populated**: Import database dump with lectionary data
3. **Backend Running**: Django development server at `https://127.0.0.1:8000/`
4. **Frontend Running** (optional): Vue dev server at `http://127.0.0.1:8080`

### Quick Environment Check

```bash
# Verify database has lectionary data
cd site
source env/bin/activate
python manage.py shell

>>> from office.models import StandardOfficeDay, Scripture
>>> StandardOfficeDay.objects.count()
366  # Should have 366 records (one per calendar day)
>>> Scripture.objects.count()
~2000  # Should have ~2000 cached scripture passages
>>> exit()
```

---

## Viewing Readings

### Via API (Backend)

```bash
# Get today's readings
curl https://127.0.0.1:8000/api/v1/readings/2025-11-06 | jq

# Get readings for specific date
curl https://127.0.0.1:8000/api/v1/readings/2025-12-25 | jq

# Get calendar with Eucharist readings
curl https://127.0.0.1:8000/api/v1/calendar/2025-12-25 | jq
```

### Via Frontend (Development)

```bash
# Start frontend dev server
cd app
npm run dev

# Open in browser
open http://127.0.0.1:8080/readings/
```

**Navigation**:

- `/readings/` - Today's readings for all offices
- `/readings/morning_prayer/` - Today's Morning Prayer readings
- `/readings/morning_prayer/2025/11/6` - Morning Prayer for specific date

### Via Django Admin

```bash
# Access admin interface
open https://127.0.0.1:8000/admin/

# Navigate to:
# - Office → Standard Office Days - View daily readings
# - Office → Holy Day Office Days - View feast readings
# - Office → Lectionary Items - View Eucharist readings
# - Office → Scriptures - View cached scripture text
```

---

## Working with Scripture Text

### Retrieve Scripture Text Programmatically

**Python (Django Shell)**:

```python
from office.models import Scripture

# Get cached scripture
scripture = Scripture.objects.get(passage="Genesis 1:1-31")
print(scripture.esv)  # HTML-formatted ESV text
print(scripture.nrsv)  # HTML-formatted NRSV text

# Check if passage is cached
try:
    scripture = Scripture.objects.get(passage="Wisdom 7:15-29")
    print(f"Cached: {scripture.passage}")
except Scripture.DoesNotExist:
    print("Not cached - needs import")
```

**API (cURL)**:

```bash
# Get scripture via API
curl -X GET "https://127.0.0.1:8000/api/v1/scripture/Genesis%201:1-31" | jq

# Response includes all translations
{
  "uuid": "...",
  "passage": "Genesis 1:1-31",
  "esv": "<p><sup>1</sup>In the beginning...",
  "kjv": "<p><sup>1</sup>In the beginning...",
  # ...all 9 translations
}
```

### Import New Scripture Text

**Import All Lectionary Passages**:

```bash
cd site
source env/bin/activate

# Import all Daily Office and Eucharist readings
# WARNING: Takes 30-60 minutes for full import
python manage.py import_scripture

# Import specific translations only
# (Not currently supported - imports all translations)
```

**Import Single Passage** (Manual):

```python
from office.models import Scripture
from bible.sources import get_passage

# Fetch from Bible Gateway API
passage = "John 3:16-21"
scripture, created = Scripture.objects.get_or_create(passage=passage)

# Import each translation
for translation in ['esv', 'nrsv', 'kjv', 'nrsvce']:
    text = get_passage(passage, translation)
    setattr(scripture, translation, text)

scripture.save()
print(f"Imported: {passage}")
```

### Add Support for New Translation

**Step 1: Add Database Column**:

```python
# site/office/models.py
class Scripture(BaseModel):
    passage = models.CharField(max_length=255)
    # ... existing translations ...
    new_translation = models.TextField(blank=True, null=True)  # Add this
```

**Step 2: Create Migration**:

```bash
cd site
python manage.py makemigrations office
python manage.py migrate office
```

**Step 3: Update Import Command**:

```python
# site/office/management/commands/import_scripture.py
def handle(self, *args, **options):
    translations = [
        "esv", "rsv", "kjv", "nrsvce", "nabre", "niv", "nasb",
        "coverdale", "renewed_coverdale",
        "new_translation"  # Add this
    ]
    # ... rest of command
```

**Step 4: Update API Serializer**:

```python
# site/office/api/serializers.py
class ScriptureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scripture
        fields = [
            'uuid', 'passage', 'esv', 'kjv', 'rsv', 'nrsv', 'nrsvce',
            'nabre', 'niv', 'nasb', 'coverdale', 'renewed_coverdale',
            'new_translation'  # Add this
        ]
```

**Step 5: Update Frontend**:

```javascript
// app/src/components/Reading.vue or app/src/store/index.js
const translations = [
  { value: "esv", label: "ESV" },
  { value: "nrsv", label: "NRSV" },
  // ... existing translations
  { value: "new_translation", label: "New Translation" }, // Add this
];
```

**Step 6: Import Data**:

```bash
python manage.py import_scripture  # Imports for new translation field
```

---

## Managing Lectionary Data

### View Current Readings

**Standard Day Readings**:

```python
from office.models import StandardOfficeDay
from datetime import date

# Get readings for November 6
day = StandardOfficeDay.objects.get(month=11, day=6)
print(f"Morning Prayer Psalms: {day.mp_psalms}")
print(f"Morning Prayer Reading 1: {day.mp_reading_1}")
print(f"Morning Prayer Reading 2: {day.mp_reading_2}")
print(f"Evening Prayer Psalms: {day.ep_psalms}")
print(f"Evening Prayer Reading 1: {day.ep_reading_1}")
print(f"Evening Prayer Reading 2: {day.ep_reading_2}")
```

**Feast Day Readings**:

```python
from office.models import HolyDayOfficeDay
from churchcal.models import SanctoraleCommemoration

# Get Christmas readings
christmas = SanctoraleCommemoration.objects.get(name__contains="Christmas Day")
christmas_readings = HolyDayOfficeDay.objects.filter(commemoration=christmas).first()
if christmas_readings:
    print(f"Christmas MP Reading 1: {christmas_readings.mp_reading_1}")
```

**Eucharist Readings**:

```python
from office.models import LectionaryItem
from churchcal.models import MassReading

# Get Sunday Eucharist readings for Year A
items = LectionaryItem.objects.filter(proper__number=5)  # Proper 5
for item in items:
    print(f"\n{item.name_and_service}")
    for reading in item.year_a:
        print(f"  {reading.reading_type}: {reading.long_citation}")
```

### Import Lectionary Data

**Import Full Lectionary**:

```bash
cd site
source env/bin/activate
python manage.py import_lectionary

# This imports:
# - LectionaryItem records (links to commemorations/propers/commons)
# - MassReading records (individual Eucharist readings)
```

**Data Sources**:

- CSV files or database dumps with BCP 2019 lectionary tables
- Located in `site/office/management/commands/import_lectionary.py`

### Modify Existing Readings

**Update Standard Day Reading**:

```python
from office.models import StandardOfficeDay

# Update November 6 readings
day = StandardOfficeDay.objects.get(month=11, day=6)
day.mp_reading_1 = "Genesis 1:1-5"  # Change reading
day.mp_reading_1_testament = "OT"
day.save()
print("Updated!")

# NOTE: Must also import new scripture text if passage not cached
```

**Update Feast Day Readings**:

```python
from office.models import HolyDayOfficeDay
from churchcal.models import SanctoraleCommemoration

christmas = SanctoraleCommemoration.objects.get(name__contains="Christmas Day")
christmas_readings = HolyDayOfficeDay.objects.filter(commemoration=christmas).first()
christmas_readings.mp_reading_1 = "Isaiah 9:2-7"
christmas_readings.save()
```

---

## Testing Lectionary Functionality

### Manual Testing Checklist

**Daily Office Readings**:

- [ ] View today's readings via API: `curl /api/v1/readings/{today}`
- [ ] Verify Morning Prayer has 2 scripture readings
- [ ] Verify Evening Prayer has 2 scripture readings
- [ ] Verify psalms appear for both offices
- [ ] Check testament field (OT/NT/DC/AP) is correct
- [ ] Test abbreviated readings display when available

**Eucharist Readings**:

- [ ] View calendar for Sunday: `curl /api/v1/calendar/{sunday}`
- [ ] Verify Eucharist lectionary section present
- [ ] Check Year A/B/C determined correctly
- [ ] Verify 4 readings: Prophecy, Psalm, Epistle, Gospel
- [ ] Test alternative readings display when present

**Scripture Text**:

- [ ] Retrieve scripture: `curl /api/v1/scripture/Genesis%201:1-31`
- [ ] Verify HTML formatting (paragraphs, verse numbers, headings)
- [ ] Check all 9 translations present in response
- [ ] Test deuterocanonical passage (e.g., Wisdom 7)
- [ ] Verify ESV/NIV/NASB are null for apocryphal books

**Translation Handling**:

- [ ] Frontend displays selected translation correctly
- [ ] Apocrypha fallback to NRSVCE works for ESV/NIV/NASB
- [ ] Translation preference persists across page reloads
- [ ] Section headings can be toggled on/off

**Feast Days**:

- [ ] Christmas (Dec 25) shows proper readings
- [ ] Easter (varies) shows proper readings
- [ ] Transferred feast readings appear on correct date
- [ ] Commons of Saints used when no specific readings

### Automated Testing (TBD)

**Unit Tests** (To Be Written):

```python
# site/office/tests/test_models.py
from django.test import TestCase
from office.models import StandardOfficeDay, Scripture
from datetime import date

class StandardOfficeDayTestCase(TestCase):
    def test_november_6_readings(self):
        """Test November 6 has correct reading assignments"""
        day = StandardOfficeDay.objects.get(month=11, day=6)
        self.assertEqual(day.mp_psalms, "119:1-24")
        self.assertIsNotNone(day.mp_reading_1)
        self.assertIsNotNone(day.mp_reading_2)

    def test_passage_to_text_fallback(self):
        """Test NRSVCE fallback for missing translation"""
        day = StandardOfficeDay.objects.get(month=11, day=6)
        # Mock scenario where translation missing
        text = day.passage_to_text('mp_reading_1', 'esv')
        self.assertIsNotNone(text)
```

**Integration Tests** (To Be Written):

```python
# site/office/tests/test_api.py
from django.test import TestCase, Client
from datetime import date

class ReadingsAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_readings_success(self):
        """Test GET /api/v1/readings/{date} returns 200"""
        response = self.client.get('/api/v1/readings/2025-11-06')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('readings', data)
        self.assertIn('morning_prayer', data['readings'])

    def test_scripture_retrieval(self):
        """Test GET /api/v1/scripture/{passage} returns cached text"""
        response = self.client.get('/api/v1/scripture/Genesis%201:1-31')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data['esv'])
```

---

## Common Development Tasks

### Task 1: Add New Feast Day Readings

```python
from office.models import HolyDayOfficeDay
from churchcal.models import SanctoraleCommemoration

# Get or create commemoration
feast, created = SanctoraleCommemoration.objects.get_or_create(
    month=1, day=6,
    defaults={
        'name': 'The Epiphany',
        'rank': 'PRINCIPAL_FEAST',
        'color': 'white'
    }
)

# Create readings for feast
readings = HolyDayOfficeDay.objects.create(
    commemoration=feast,
    mp_psalms="46, 47",
    mp_reading_1="Isaiah 60:1-9",
    mp_reading_1_testament="OT",
    mp_reading_2="Luke 2:22-40",
    mp_reading_2_testament="NT",
    ep_psalms="96, 97",
    ep_reading_1="Isaiah 60:10-22",
    ep_reading_1_testament="OT",
    ep_reading_2="John 1:29-34",
    ep_reading_2_testament="NT",
    order=0
)
print(f"Created readings for {feast.name}")
```

### Task 2: Update Psalm Cycle

**Modify 60-Day Cycle**:

```python
from office.models import StandardOfficeDay

# Update November 6 psalms
day = StandardOfficeDay.objects.get(month=11, day=6)
day.mp_psalms = "119:1-32"  # Change psalm assignment
day.ep_psalms = "119:33-64"
day.save()
```

**Modify 30-Day Cycle**:

```python
from office.models import ThirtyDayPsalterDay

# Update day 6 of month
day = ThirtyDayPsalterDay.objects.get(day=6)
day.mp_psalms = "31, 32"
day.ep_psalms = "33, 34"
day.save()
```

### Task 3: Fix Scripture Import Issues

**Check Missing Passages**:

```python
from office.models import OfficeDay, Scripture

# Find uncached passages
all_passages = set()
for day in OfficeDay.objects.all():
    all_passages.add(day.mp_reading_1)
    all_passages.add(day.mp_reading_2)
    all_passages.add(day.ep_reading_1)
    all_passages.add(day.ep_reading_2)

cached_passages = set(Scripture.objects.values_list('passage', flat=True))
missing = all_passages - cached_passages
print(f"Missing {len(missing)} passages")
for passage in list(missing)[:10]:
    print(f"  - {passage}")
```

**Import Missing Passages**:

```bash
# Run import command to fill gaps
python manage.py import_scripture

# Or import specific passages in Django shell
from office.models import Scripture
from bible.sources import get_passage

passage = "Missing Passage"
scripture = Scripture.objects.create(passage=passage)
for translation in ['esv', 'nrsv', 'kjv']:
    text = get_passage(passage, translation)
    setattr(scripture, translation, text)
scripture.save()
```

---

## Troubleshooting

### Issue: Readings Not Appearing

**Symptom**: API returns empty readings or 404

**Diagnosis**:

```python
from office.models import StandardOfficeDay
from datetime import date

# Check if date has reading record
try:
    day = StandardOfficeDay.objects.get(month=11, day=6)
    print("Record exists")
except StandardOfficeDay.DoesNotExist:
    print("No record for this date")
```

**Solution**: Import lectionary data or create record manually

### Issue: Scripture Text Missing

**Symptom**: API returns scripture with null translations

**Diagnosis**:

```python
from office.models import Scripture

scripture = Scripture.objects.get(passage="Problem Passage")
if not scripture.esv:
    print("ESV text missing - needs import")
```

**Solution**: Run `python manage.py import_scripture` or import specific passage

### Issue: Wrong Eucharist Year Displayed

**Symptom**: Wrong cycle year (A/B/C) shown for Sunday

**Diagnosis**:

```python
from churchcal.calculations import get_date
from datetime import date

liturgical_date = get_date(date(2025, 11, 9))
print(f"Eucharist Year: {liturgical_date.eucharist_year}")  # Should be B for 2025
```

**Solution**: Verify cycle calculation in `churchcal/calculations.py`

### Issue: Apocrypha Not Displaying

**Symptom**: Deuterocanonical readings show error

**Diagnosis**:

- Check `testament` field is "DC" or "AP"
- Verify ESV/NIV/NASB fallback logic in frontend
- Confirm NRSVCE text exists in Scripture model

**Solution**: Import NRSVCE if missing, verify frontend fallback code

---

## Resources

### Code Locations

- **Models**: `site/office/models.py`, `site/churchcal/models.py`
- **API Views**: `site/office/api/views/index.py`, `site/office/api/views/resources.py`
- **API URLs**: `site/website/api_urls.py`
- **Import Commands**: `site/office/management/commands/import_scripture.py`, `import_lectionary.py`
- **Frontend**: `app/src/views/Readings.vue`, `app/src/components/Reading.vue`

### Documentation

- **Plan**: `specs/005-lectionary/plan.md`
- **Research**: `specs/005-lectionary/research.md`
- **Data Model**: `specs/005-lectionary/data-model.md`
- **API Contracts**: `specs/005-lectionary/contracts/README.md`
- **This Guide**: `specs/005-lectionary/quickstart.md`

### External References

- **BCP 2019**: Daily Office Lectionary (pp. 985-1018), Eucharist Lectionary (pp. 1019-1051)
- **Bible Gateway**: Scripture text source (unofficial API via HTML parsing)
- **Revised Common Lectionary**: Source for three-year Eucharist cycle

---

**Last Updated**: 2025-11-06  
**Status**: Retroactive documentation - guides working with existing implementation
