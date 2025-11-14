# Quickstart Guide: Psalter Development

**Feature**: 004-psalter | **For**: New developers joining the psalter feature work

This guide gets you up and running with the Psalter feature in under 30 minutes.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Environment Setup](#environment-setup)
4. [Running the Application](#running-the-application)
5. [Testing](#testing)
6. [Common Tasks](#common-tasks)
7. [Troubleshooting](#troubleshooting)
8. [Next Steps](#next-steps)

---

## Overview

The **Psalter** feature provides access to all 150 psalms from the Book of Common Prayer 2019 in both Contemporary and Traditional Language Edition (TLE) translations. It includes:

- **Backend**: Django REST API serving psalm data from PostgreSQL
- **Frontend**: Vue.js SPA with individual psalm viewing, topic filtering, and language toggle
- **Database**: ~2,250 psalm verses across 150 psalms, organized by topics

**Key Technologies**:

- Backend: Django 5.2+, Python 3.13, PostgreSQL 17.5+
- Frontend: Vue 3, Vite, TypeScript, Element Plus
- Testing: pytest, Vitest, Playwright

---

## Prerequisites

Before starting, ensure you have:

- ✅ Python 3.13
- ✅ Node.js 20+
- ✅ PostgreSQL 17.5+ (running)
- ✅ Memcached 1.6+ (optional but recommended)
- ✅ Git access to the repository
- ✅ Code editor (VS Code recommended)

**Quick Check**:

```bash
python3 --version  # Should be 3.13+
node --version     # Should be 20+
psql --version     # Should be 17.5+
```

---

## Environment Setup

### 1. Bootstrap the Environment

**ALWAYS do this first** (per copilot-instructions.md):

```bash
# Navigate to repository root
cd /path/to/dailyoffice2019

# Create environment files
cp app/.env.development app/.env.local
cp site/website/.env.example site/website/.env

# Edit site/website/.env - Add development values for ALL variables
# See copilot-instructions.md for complete list
```

**Critical environment variables** for psalter:

```bash
DEBUG=True
POSTGRES_NAME=dailyoffice
POSTGRES_USER=dailyoffice
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
SECRET_KEY=development-secret-key-not-for-production
```

### 2. Start Required Services

```bash
# Start PostgreSQL
sudo service postgresql start

# Start Memcached (optional)
sudo service memcached start
```

### 3. Create and Load Database

**Takes ~4 seconds** (fast and reliable):

```bash
# Create database and user
sudo -u postgres psql -c "CREATE DATABASE dailyoffice;"
sudo -u postgres psql -c "CREATE USER dailyoffice WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE dailyoffice TO dailyoffice;"

# Import database dump (includes all psalm data)
unzip -p site/dailyoffice_2024_01_30.sql.zip dailyoffice_2024_01_30.sql | sudo -u postgres psql dailyoffice
```

**Verify database**:

```bash
psql -U dailyoffice -d dailyoffice -c "SELECT COUNT(*) FROM psalter_psalm;"
# Should return: 150

psql -U dailyoffice -d dailyoffice -c "SELECT COUNT(*) FROM psalter_psalmverse;"
# Should return: ~2250
```

### 4. Backend Python Setup

**Takes 5-45 minutes** (network dependent, NEVER CANCEL):

```bash
cd site
python3 -m venv env
source env/bin/activate

# Install dependencies (use long timeouts, retries expected)
pip install --timeout 1200 --retries 10 -r requirements.txt
```

**Quick validation**:

```bash
python manage.py check
# Should show: System check identified no issues (0 silenced).
```

### 5. Frontend Setup

**FontAwesome Pro authentication required** (see copilot-instructions.md for details):

```bash
# Configure FontAwesome Pro (one-time setup)
cd app
npm config set "@fortawesome:registry" https://npm.fontawesome.com/
npm config set "//npm.fontawesome.com/:_authToken" YOUR_GITHUB_TOKEN

# Install dependencies
npm install
```

**If npm install fails**: Contact project maintainers for FontAwesome Pro access.

---

## Running the Application

### Backend API Server

```bash
cd site
source env/bin/activate
python manage.py runsslserver
```

**Access**:

- API Base: https://127.0.0.1:8000/
- Swagger UI: https://127.0.0.1:8000/api/
- ReDoc: https://127.0.0.1:8000/api/redoc/

**Test the psalms endpoint**:

```bash
curl https://127.0.0.1:8000/api/v1/psalms/23/ | jq
```

### Frontend Development Server

```bash
cd app
npm run dev
```

**Access**: http://127.0.0.1:8080

**Test psalm viewing**:

1. Navigate to http://127.0.0.1:8080/psalm/23
2. Toggle Contemporary/Traditional switch
3. Click "Psalm 24" to test navigation
4. Click "All Psalms" to see topic filtering

---

## Testing

### Run Backend Tests

```bash
cd site
source env/bin/activate
pytest
```

**Run psalter-specific tests only**:

```bash
pytest psalter/tests.py -v
```

### Run Frontend Tests

```bash
cd app

# Unit tests (Vitest)
npm run test:unit

# E2E tests (Playwright)
npm run test:e2e
```

### Run Linting and Formatting

```bash
# Backend formatting
cd site
find . -iname "*.py" | xargs black --target-version=py313 --line-length=119

# Frontend linting
cd app
npm run lint
```

---

## Common Tasks

### Access the Django Admin Interface

```bash
# Make sure backend is running
cd site
source env/bin/activate
python manage.py runsslserver

# Navigate to: https://127.0.0.1:8000/admin/

# Default superuser (if exists): admin / password
# Or create superuser:
python manage.py createsuperuser
```

### Manage Psalm Topics (FR-016-017)

1. Access https://127.0.0.1:8000/admin/psalter/psalmtopic/
2. Click "Add Psalm Topic" to create new topic
3. Enter topic name (e.g., "Lament and Sorrow")
4. Set order number for display priority
5. Drag-and-drop to reorder topics (SortableAdminMixin)
6. Click "Save"

### Assign Psalms to Topics (FR-017)

1. Access https://127.0.0.1:8000/admin/psalter/psalmtopicpsalm/
2. Click "Add Psalm Topic Psalm"
3. Select psalm from dropdown
4. Select topic from dropdown
5. Set order within topic
6. Click "Save"

### Edit Psalm Verse Text (FR-018-019)

1. Access https://127.0.0.1:8000/admin/psalter/psalmverse/
2. Use filters to find verses (e.g., "Verses with Lord" filter)
3. Click on verse to edit
4. Update Contemporary fields (`first_half`, `second_half`)
5. Update Traditional fields (`first_half_tle`, `second_half_tle`)
6. Click "Save"
7. Clear cache to see changes: `python manage.py clearcache` (if available)

### View a Specific Psalm in the Database

```bash
psql -U dailyoffice -d dailyoffice

SELECT * FROM psalter_psalm WHERE number = 23;
SELECT * FROM psalter_psalmverse WHERE psalm_id = (SELECT id FROM psalter_psalm WHERE number = 23) ORDER BY number;
\q
```

### Add a New Topic (FR-016: Admin Interface)

**Use the Django admin interface** (preferred method):

1. Navigate to https://127.0.0.1:8000/admin/psalter/psalmtopic/
2. Click "Add Psalm Topic"
3. Enter topic name: "New Topic"
4. Enter psalms (legacy field, optional): "1,2,3"
5. Set order: 10
6. Click "Save"
7. Create associations via PsalmTopicPsalm admin

**Or add to database directly** (development only):

```bash
psql -U dailyoffice -d dailyoffice
INSERT INTO psalter_psalmtopic (id, topic_name, psalms, "order")
VALUES (gen_random_uuid(), 'New Topic', '1,2,3', 10);
```

Then create associations:

```bash
INSERT INTO psalter_psalmtopicpsalm (id, psalm_id, psalm_topic_id, "order")
VALUES (
  gen_random_uuid(),
  (SELECT id FROM psalter_psalm WHERE number = 1),
  (SELECT id FROM psalter_psalmtopic WHERE topic_name = 'New Topic'),
  1
);
```

### Test Psalm Range Backend Logic

The backend supports ranges but frontend UI is missing (FR-006/FR-007):

```python
# In Django shell
python manage.py shell

from psalter.utils import get_psalms

# Test range
html = get_psalms("1-3")
print(html)

# Test partial psalm
html = get_psalms("119:1-8")
print(html)
```

### Debug API Responses

```bash
# List all psalms (first verse only)
curl https://127.0.0.1:8000/api/v1/psalms/ | jq '.[0]'

# Get complete psalm
curl https://127.0.0.1:8000/api/v1/psalms/23/ | jq

# List topics
curl https://127.0.0.1:8000/api/v1/psalms/topics/ | jq
```

### Run Database Migrations

```bash
cd site
source env/bin/activate
python manage.py migrate
```

### Collect Static Assets

```bash
cd site
source env/bin/activate
python manage.py collectstatic --noinput
```

---

## Troubleshooting

### Issue: "relation 'psalter_psalm' does not exist"

**Cause**: Database not loaded or migrations not run.

**Solution**:

```bash
# Re-import database dump
unzip -p site/dailyoffice_2024_01_30.sql.zip dailyoffice_2024_01_30.sql | sudo -u postgres psql dailyoffice

# OR run migrations (if using empty database)
cd site && python manage.py migrate
```

### Issue: "No module named 'psalter'"

**Cause**: Not in virtual environment or dependencies not installed.

**Solution**:

```bash
cd site
source env/bin/activate
pip install -r requirements.txt
```

### Issue: Frontend shows "Error retrieving psalms"

**Cause**: Backend not running or CORS issue.

**Solution**:

1. Verify backend is running: `curl https://127.0.0.1:8000/api/v1/psalms/`
2. Check `app/.env.local` has correct `VITE_API_URL=https://127.0.0.1:8000`
3. Check browser console for CORS errors

### Issue: "ENOTFOUND npm.fontawesome.com"

**Cause**: FontAwesome Pro authentication not configured.

**Solution**: See copilot-instructions.md section "Frontend Setup - FONTAWESOME PRO AUTHENTICATION REQUIRED"

### Issue: pip install timeout

**Cause**: Network issues with PyPI (common).

**Solution**:

```bash
# Use maximum timeouts (NEVER CANCEL if running)
pip install --timeout 1200 --retries 10 -r requirements.txt

# If persistent, install core packages individually
pip install --timeout 600 --retries 5 Django==5.2 psycopg-binary
```

---

## Next Steps

### For Feature Development

1. **Read the specification**: `/specs/004-psalter/spec.md`
2. **Review the implementation plan**: `/specs/004-psalter/plan.md`
3. **Study the data model**: `/specs/004-psalter/data-model.md`
4. **Examine the API contracts**: `/specs/004-psalter/contracts/`
5. **Check the constitution**: `/.specify/memory/constitution.md`

### For Bug Fixes

1. **Write a failing test** that reproduces the bug
2. **Fix the bug** with minimal changes
3. **Verify all tests pass**
4. **Format code**: `black`, `eslint`
5. **Commit** with atomic, descriptive message

### For New Features

1. **Create a feature branch**: `git checkout -b 004-psalter-enhancement`
2. **Write tests first** (test-driven development)
3. **Implement the feature**
4. **Document changes** in commit messages
5. **Submit PR** with constitution compliance checklist

---

## Key Files Reference

### Backend (Django)

```
site/
├── psalter/
│   ├── models.py          # Psalm, PsalmVerse, PsalmTopic, PsalmTopicPsalm
│   ├── admin.py           # Admin interface (PsalmTopicAdmin violation of FR-011)
│   ├── utils.py           # get_psalms(), normalize_citations(), psalm_html()
│   ├── tests.py           # Unit tests (currently minimal)
│   └── management/
│       └── commands/      # Database loading scripts
├── office/api/views/
│   └── resources.py       # PsalmsViewSet (REST API endpoints)
└── website/
    └── api_urls.py        # URL routing for /api/v1/psalms
```

### Frontend (Vue)

```
app/
├── src/
│   ├── views/
│   │   ├── Psalm.vue      # Individual psalm view (/psalm/:number)
│   │   └── Psalms.vue     # All psalms list with topics (/psalms)
│   ├── router/
│   │   └── index.js       # Route definitions
│   └── helpers/
│       └── storage.js     # DynamicStorage for preferences
└── tests/
    ├── unit/              # Vitest unit tests
    └── e2e/               # Playwright E2E tests
```

### Documentation

```
specs/004-psalter/
├── spec.md                # Feature specification (requirements)
├── plan.md                # Implementation plan (this document's parent)
├── research.md            # Design decisions and unknowns resolved
├── data-model.md          # Database schema documentation
├── quickstart.md          # This file
└── contracts/
    ├── psalms-api.yaml    # OpenAPI 3.0 specification
    └── README.md          # API contract documentation
```

---

## Getting Help

- **Code questions**: Review copilot-instructions.md for project standards
- **Constitution questions**: See `.specify/memory/constitution.md`
- **API questions**: Check `/specs/004-psalter/contracts/README.md`
- **Setup issues**: Follow troubleshooting section above
- **Feature questions**: Read `/specs/004-psalter/spec.md`

---

**Welcome to the Daily Office 2019 Psalter development!** 🎉

This feature serves thousands of users in their daily prayer practice. Your work here has eternal significance.

_"Blessed is the one who does not walk in the counsel of the wicked..." - Psalm 1:1_
