# Quick Start Guide: Collects Feature Development

**Feature**: 003-collects  
**Date**: November 6, 2025  
**Target Audience**: Developers working on the collects feature

## Overview

This guide helps developers set up their environment, understand the collects architecture, run tests, and implement new features for the collects system.

**Time to Complete Setup**: ~30-45 minutes (first time)

## Prerequisites

Before starting, ensure you have:

- ✅ Python 3.13+ installed
- ✅ Node.js 24.4+ installed
- ✅ PostgreSQL 17.5+ installed and running
- ✅ Memcached 1.6+ installed and running
- ✅ Git repository cloned
- ✅ Read `.github/copilot-instructions.md` for project overview

## Quick Start (TL;DR)

```bash
# 1. Setup environment files
cp app/.env.development app/.env.local
cp site/website/.env.example site/website/.env
# Edit site/website/.env with all required values

# 2. Start services
sudo service postgresql start
sudo service memcached start

# 3. Setup database
sudo -u postgres psql -c "CREATE DATABASE dailyoffice;"
sudo -u postgres psql -c "CREATE USER dailyoffice WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE dailyoffice TO dailyoffice;"
unzip -p site/dailyoffice_2024_01_30.sql.zip dailyoffice_2024_01_30.sql | sudo -u postgres psql dailyoffice

# 4. Backend setup
cd site
python3 -m venv env
source env/bin/activate
pip install --timeout 1200 --retries 10 -r requirements.txt

# 5. Populate normalized text (CRITICAL for search)
python manage.py populate_normalized_text

# 6. Run backend
python manage.py runsslserver
# Access at https://127.0.0.1:8000/

# 7. Frontend setup (new terminal)
cd app
npm install
npm run dev
# Access at http://127.0.0.1:8080
```

## Detailed Setup

### 1. Environment Configuration

#### Backend Environment (`site/website/.env`)

**Critical**: The `.env` file requires ALL variables. See `.github/copilot-instructions.md` for complete list.

**Minimum for collects development**:

```bash
DEBUG=True
SECRET_KEY=development-secret-key
POSTGRES_NAME=dailyoffice
POSTGRES_USER=dailyoffice
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
SITE_ADDRESS=https://127.0.0.1:8000
```

#### Frontend Environment (`app/.env.local`)

```bash
VITE_API_URL=https://127.0.0.1:8000/
```

---

### 2. Database Setup

#### Create Database and User

```bash
sudo service postgresql start
sudo -u postgres psql -c "CREATE DATABASE dailyoffice;"
sudo -u postgres psql -c "CREATE USER dailyoffice WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE dailyoffice TO dailyoffice;"
```

#### Import Data Dump

**Time**: ~4 seconds

```bash
cd site
unzip -p dailyoffice_2024_01_30.sql.zip dailyoffice_2024_01_30.sql | sudo -u postgres psql dailyoffice
```

**Verify Import**:

```bash
sudo -u postgres psql dailyoffice -c "SELECT COUNT(*) FROM office_collect;"
# Should return count of collects (estimated 300-500)
```

---

### 3. Backend Python Environment

#### Create Virtual Environment

```bash
cd site
python3 -m venv env
source env/bin/activate
```

#### Install Dependencies

**⚠️ CRITICAL**: Network timeouts are common. Use maximum timeouts and retries.

**Time**: 5-45 minutes (network dependent)

```bash
pip install --timeout 1200 --retries 10 -r requirements.txt
```

**If timeout occurs**:

```bash
# Install core dependencies individually
pip install --timeout 600 --retries 5 Django==5.2 psycopg-binary beautifulsoup4 requests arrow django-environ
```

---

### 4. Frontend Node.js Environment

#### Install Dependencies

**Time**: ~2 minutes

**⚠️ FONTAWESOME PRO AUTHENTICATION REQUIRED**

FontAwesome Pro requires authentication. Configure your token:

```bash
# Option 1: Using GitHub Personal Access Token
npm config set "@fortawesome:registry" https://npm.fontawesome.com/
npm config set "//npm.fontawesome.com/:_authToken" YOUR_GITHUB_TOKEN

# Option 2: Using FontAwesome Pro token (if you have one)
npm config set "//npm.fontawesome.com/:_authToken" YOUR_FONTAWESOME_PRO_TOKEN
```

**Install**:

```bash
cd app
npm install
```

**If authentication fails**: Contact project maintainer for FontAwesome Pro access.

---

### 5. Critical Data Migration (⚠️ MUST RUN)

The `normalized_text` and `normalized_traditional_text` fields are empty in the database dump. These fields are **required for search functionality** (FR-007).

#### Create Migration Command

**Location**: `site/office/management/commands/populate_normalized_text.py`

```python
from django.core.management.base import BaseCommand
from office.models import Collect
from office.management.commands.import_collects import do_strip_tags

class Command(BaseCommand):
    help = 'Populate normalized text fields for all collects'

    def handle(self, *args, **options):
        collects = Collect.objects.all()
        updated = 0

        for collect in collects:
            # Strip HTML from contemporary text
            collect.normalized_text = do_strip_tags(collect.text).replace(" Amen.", "").strip()

            # Strip HTML from traditional text (if exists)
            if collect.traditional_text:
                collect.normalized_traditional_text = do_strip_tags(
                    collect.traditional_text
                ).replace(" Amen.", "").strip()

            collect.save()
            updated += 1

            if updated % 50 == 0:
                self.stdout.write(f'Updated {updated} collects...')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated} collects')
        )
```

#### Run Migration

```bash
cd site
source env/bin/activate
python manage.py populate_normalized_text
```

**Expected Output**:

```
Updated 50 collects...
Updated 100 collects...
...
Successfully updated 487 collects
```

#### Verify Migration

```python
python manage.py shell

from office.models import Collect

# Check that all collects have normalized text
with_text = Collect.objects.exclude(normalized_text__isnull=True).exclude(normalized_text='').count()
total = Collect.objects.count()

print(f"{with_text}/{total} collects have normalized text")
# Should be 100%
```

---

## Development Workflows

### Running Development Servers

#### Backend (Django API)

**Terminal 1**:

```bash
cd site
source env/bin/activate
python manage.py runsslserver
```

**Access**: https://127.0.0.1:8000/

**API Docs**: https://127.0.0.1:8000/api/

**Note**: Requires `django-sslserver` (already in requirements.txt)

---

#### Frontend (Vue.js)

**Terminal 2**:

```bash
cd app
npm run dev
```

**Access**: http://127.0.0.1:8080

**Collects Page**: http://127.0.0.1:8080/collects

---

### Working with Collects Data

#### View Collects in Admin

1. Create superuser (if not exists):

   ```bash
   python manage.py createsuperuser
   ```

2. Access admin: https://127.0.0.1:8000/admin/

3. Navigate to: Office → Collects

#### Query Collects in Shell

```bash
python manage.py shell
```

```python
from office.models import Collect, CollectType, CollectTag

# Get all collects
collects = Collect.objects.all()
print(f"Total collects: {collects.count()}")

# Get occasional prayers
occasional = CollectType.objects.get(key="occasional")
prayers = Collect.objects.filter(collect_type=occasional)
print(f"Occasional prayers: {prayers.count()}")

# Get collects tagged with "mission"
mission_tag = CollectTag.objects.get(key="mission")
mission_collects = Collect.objects.filter(tags=mission_tag)
print(f"Mission collects: {mission_collects.count()}")

# Check normalized text
sample = Collect.objects.first()
print(f"Title: {sample.title}")
print(f"Has normalized text: {bool(sample.normalized_text)}")
```

---

### Testing

#### Backend Tests (Django)

**Current State**: No tests exist (0% coverage) - see `research.md`

**Run Tests** (when created):

```bash
cd site
source env/bin/activate
python manage.py test office.tests
```

**With Coverage** (needs installation: `pip install coverage`):

```bash
coverage run --source='office' manage.py test office.tests
coverage report
coverage html  # Generate HTML report in htmlcov/
```

---

#### Frontend Tests (Vitest)

**Current State**: No collects-specific tests exist

**Run Tests** (when created):

```bash
cd app
npm run test:unit
```

**Run with Coverage**:

```bash
npm run test:unit -- --coverage
```

**Watch Mode** (for TDD):

```bash
npm run test:unit -- --watch
```

---

#### End-to-End Tests (Cypress)

**Current State**: Cypress configured but no collects tests

**Run Tests** (when created):

```bash
cd app
npm run test:e2e
```

**Interactive Mode**:

```bash
npm run test:e2e:open
```

---

### Code Formatting and Linting

#### Python (Black)

**Format All Python Files**:

```bash
cd site
find . -iname "*.py" | xargs black --target-version=py313 --line-length=119
```

**Format Specific File**:

```bash
black --target-version=py313 --line-length=119 office/models.py
```

#### JavaScript/Vue (ESLint)

**Lint Frontend**:

```bash
cd app
npm run lint
```

**Fix Automatically**:

```bash
npm run lint -- --fix
```

#### Pre-commit Hooks

**Run All Checks**:

```bash
pre-commit run --all-files
```

**Note**: Pre-commit is configured in `.pre-commit-config.yaml`

---

## Feature Implementation Guide

### Implementing Search (Priority P1)

**Prerequisites**: Normalized text fields populated (see Section 5)

**Steps**:

1. **Install mark.js**:

   ```bash
   cd app
   npm install mark.js
   ```

2. **Add search input** to `CollectsNew.vue`:

   - See `contracts/search-strategy.md` Section "1. Search Input Component"

3. **Implement `filteredCollects` computed property**:

   - See `contracts/search-strategy.md` Section "1. Search Input Component"

4. **Add search term highlighting**:

   - See `contracts/search-strategy.md` Section "2. Search Term Highlighting"

5. **Add empty results handling**:

   - See `contracts/search-strategy.md` Section "4. Empty Results Handling"

6. **Write tests**:

   - Unit tests: `app/tests/unit/CollectsNew.spec.js`
   - E2E tests: `app/tests/e2e/collects.cy.js`
   - See `contracts/search-strategy.md` Section "Testing Contract"

7. **Test manually**:

   ```bash
   # Start dev server
   npm run dev

   # Open http://127.0.0.1:8080/collects
   # Test search with various terms
   ```

8. **Validate**:
   - Search returns results < 300ms (check browser dev tools)
   - Highlighting appears correctly
   - Empty search shows all collects
   - No JavaScript errors in console

**Estimated Time**: 6-9 hours (from research.md)

---

### Implementing Date-Based Collects (Priority P2)

**Prerequisites**: None (existing infrastructure sufficient)

**Steps**:

1. **Create backend ViewSet** in `site/office/api/views/resources.py`:

   ```python
   from rest_framework.viewsets import ViewSet
   from rest_framework.response import Response
   from churchcal.calculations import ChurchYear
   from churchcal.models import Calendar
   import datetime

   class DateCollectsViewSet(ViewSet):
       def retrieve(self, request, year, month, day):
           date = datetime.date(int(year), int(month), int(day))
           calendar = Calendar.objects.get(abbreviation='ACNA2019')
           church_year = ChurchYear(date.year, calendar)
           commemoration = church_year.get_commemoration(date)

           collects = commemoration.get_collects(calendar_date=date)

           return Response({
               'date': date.isoformat(),
               'commemoration': CommemorationSerializer(commemoration).data,
               'collects': [CollectSerializer(c).data for c in collects]
           })
   ```

2. **Add URL route** in `site/website/urls.py`:

   ```python
   path('api/v1/collects/date/<int:year>/<int:month>/<int:day>/',
        DateCollectsViewSet.as_view({'get': 'retrieve'})),
   ```

3. **Add date picker to frontend** (`CollectsNew.vue`):

   - See `research.md` Section 4 "Frontend Integration Options"

4. **Write tests**:

   - Backend unit test: Mock ChurchYear
   - Backend integration test: Verify correct collects for sample dates
   - Frontend E2E test: Select date, verify collect displayed

5. **Test manually**:

   ```bash
   # Test API directly
   curl https://127.0.0.1:8000/api/v1/collects/date/2025/12/25

   # Should return Christmas collect(s)
   ```

**Estimated Time**: 7-10 hours (from research.md)

**See Also**: `contracts/api-date-collects.yaml` for complete API specification

---

### Implementing Metrical Collect Display (Priority P2)

**Prerequisites**: None (model already supports metrical collects)

**Steps**:

1. **Update `Collect.vue` component**:

   ```vue
   <template>
     <!-- ... existing template ... -->

     <div v-if="hasMetricalVersions" class="metrical-collects">
       <h6>Metrical Versions:</h6>
       <ul>
         <li v-if="collect.metrical_collect">
           <a :href="collect.metrical_collect.pdf_link" target="_blank">
             <el-icon><MusicNote /></el-icon>
             {{ collect.metrical_collect.tune_name || "Version 1" }}
           </a>
         </li>
         <!-- ... repeat for metrical_collect_2 and metrical_collect_3 -->
       </ul>
     </div>
   </template>

   <script>
   computed: {
     hasMetricalVersions() {
       return this.collect.metrical_collect ||
              this.collect.metrical_collect_2 ||
              this.collect.metrical_collect_3;
     }
   }
   </script>
   ```

2. **Update API serializer** to include metrical collects (if not already):

   - Check `site/office/api/serializers.py::CollectSerializer`
   - Ensure metrical_collect fields are included

3. **Add styling** for metrical links:

   ```scss
   .metrical-collects {
     margin-top: 1rem;
     padding: 0.5rem;
     background-color: #f5f5f5;
     border-radius: 4px;

     h6 {
       margin-bottom: 0.5rem;
       font-size: 0.9rem;
       color: #666;
     }

     ul {
       list-style: none;
       padding-left: 0;

       li {
         margin-bottom: 0.25rem;

         a {
           display: flex;
           align-items: center;
           gap: 0.5rem;
           color: #409eff;
           text-decoration: none;

           &:hover {
             text-decoration: underline;
           }
         }
       }
     }
   }
   ```

4. **Test**:
   - Find collect with metrical version (may need to populate data manually)
   - Verify links display correctly
   - Verify links open in new tab

**Note**: Metrical collect data may be sparse. Consider populating manually for testing.

---

## Common Issues and Solutions

### Issue: `pip install` Timeout

**Symptom**: `ReadTimeoutError` during pip install

**Solution**:

```bash
pip install --timeout 1200 --retries 10 -r requirements.txt
```

**If still failing**:

```bash
# Install core packages individually
pip install --timeout 600 Django==5.2
pip install --timeout 600 psycopg-binary
pip install --timeout 600 django-environ
# ... etc
```

---

### Issue: PostgreSQL Connection Refused

**Symptom**: `connection to server at "localhost" refused`

**Solution**:

```bash
# Start PostgreSQL
sudo service postgresql start

# Verify running
pg_isready -h localhost -p 5432

# Check credentials in site/website/.env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

---

### Issue: FontAwesome Install Fails

**Symptom**: `ENOTFOUND npm.fontawesome.com`

**Solution**: Configure FontAwesome Pro authentication (see Section 4 above)

**Workaround**: Contact project maintainer for token

---

### Issue: Search Not Working

**Symptom**: Search input exists but no results

**Possible Causes**:

1. **Normalized text not populated**: Run `populate_normalized_text` command
2. **mark.js not installed**: Run `npm install mark.js`
3. **JavaScript error**: Check browser console for errors

**Debug**:

```javascript
// In browser console on /collects page
console.log(window.$vm0.collects[0].normalized_text);
// Should show plain text, not null/undefined
```

---

### Issue: Tests Not Running

**Symptom**: `python manage.py test` fails

**Solution**: No tests exist yet (see `research.md`). Create test files first.

---

### Issue: CORS Errors in Development

**Symptom**: Frontend can't access API

**Solution**: Verify `site/website/settings.py` has CORS configuration:

```python
CORS_ALLOW_ALL_ORIGINS = True  # Dev only
```

**Or** use proper origin:

```python
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
]
```

---

## Useful Commands Reference

### Django Management Commands

```bash
# Run development server
python manage.py runsslserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Check for issues
python manage.py check

# Collect static files
python manage.py collectstatic

# Populate normalized text (custom)
python manage.py populate_normalized_text
```

---

### Database Commands

```bash
# Connect to database
sudo -u postgres psql dailyoffice

# List tables
\dt

# Describe table
\d office_collect

# Count collects
SELECT COUNT(*) FROM office_collect;

# Sample collect
SELECT title, attribution FROM office_collect LIMIT 5;

# Exit
\q
```

---

### Frontend Commands

```bash
# Development server
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Fix linting issues
npm run lint -- --fix

# Run unit tests
npm run test:unit

# Run E2E tests
npm run test:e2e
```

---

## Architecture Overview

### Backend Structure

```
site/
├── office/                      # Main collects app
│   ├── models.py               # Collect, CollectType, CollectTag, etc.
│   ├── api/
│   │   ├── views/
│   │   │   └── resources.py   # CollectsViewSet, GroupedCollectsViewSet
│   │   └── serializers.py     # CollectSerializer
│   └── management/
│       └── commands/
│           └── import_collects.py  # Data import logic
│
└── churchcal/                   # Calendar integration
    ├── models.py               # Commemoration (has collect ForeignKeys)
    └── calculations.py         # ChurchYear (date → commemoration logic)
```

---

### Frontend Structure

```
app/
└── src/
    ├── views/
    │   └── CollectsNew.vue      # Main collects page
    ├── components/
    │   ├── Collect.vue          # Individual collect display
    │   └── CollectsSubcategory.vue  # Subcategory grouping
    └── router/
        └── index.js             # Route: /collects → CollectsNew.vue
```

---

### Data Flow

**Browse Collects**:

```
User visits /collects
  → CollectsNew.vue mounts
  → Fetch GET /api/v1/grouped_collects
  → GroupedCollectsViewSet returns organized collects
  → Component renders categories with subcategories
  → User selects category filter (client-side filter)
  → User switches language (client-side text swap)
```

**Search Collects** (when implemented):

```
User types in search input
  → Debounce 300ms
  → filteredCollects computed property executes
  → Filter collects array where title or normalized_text includes term
  → mark.js highlights matching terms in DOM
  → Results update immediately (< 100ms)
```

**Date-Based Collects** (when implemented):

```
User selects date in date picker
  → Fetch GET /api/v1/collects/date/2025/12/25
  → Backend: ChurchYear.get_commemoration(date)
  → Backend: Commemoration.get_collects()
  → Return collects for that commemoration
  → Frontend displays collect(s) with date context
```

---

## Next Steps After Setup

1. **✅ Verify setup**: Run both servers, access /collects page
2. **✅ Populate normalized text**: Run migration command
3. **📚 Read documentation**:
   - `data-model.md` - Understand collect schema
   - `research.md` - Understand design decisions
   - `contracts/search-strategy.md` - Search implementation details
   - `contracts/api-date-collects.yaml` - Date API specification
4. **🧪 Create test foundation**: Start with one unit test
5. **🔍 Implement search**: Follow `contracts/search-strategy.md`
6. **📅 Implement date collects**: Follow `contracts/api-date-collects.yaml`

---

## Getting Help

- **Project Documentation**: `.github/copilot-instructions.md`
- **Spec Documents**: `specs/003-collects/*.md`
- **API Contracts**: `specs/003-collects/contracts/*.yaml`
- **Django Docs**: https://docs.djangoproject.com/en/5.2/
- **Vue 3 Docs**: https://vuejs.org/guide/
- **Element Plus**: https://element-plus.org/en-US/

---

## Checklist for New Developers

- [ ] Read `.github/copilot-instructions.md`
- [ ] Setup environment files (.env)
- [ ] Start PostgreSQL and Memcached
- [ ] Import database dump
- [ ] Setup Python virtual environment
- [ ] Install backend dependencies (pip)
- [ ] Install frontend dependencies (npm)
- [ ] **Run populate_normalized_text command** (CRITICAL)
- [ ] Start backend server (verify https://127.0.0.1:8000/)
- [ ] Start frontend server (verify http://127.0.0.1:8080/collects)
- [ ] Create superuser for admin access
- [ ] Read all spec documents in `specs/003-collects/`
- [ ] Understand data model (`data-model.md`)
- [ ] Understand search strategy (`contracts/search-strategy.md`)
- [ ] Run code formatter (black, eslint)
- [ ] Commit code with atomic commits referencing FR-### or T###

---

**Document Version**: 1.0  
**Last Updated**: November 6, 2025  
**Status**: Complete and Ready for Use
