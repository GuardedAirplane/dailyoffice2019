# Daily Office Developer Quickstart Guide

**Date**: November 6, 2025  
**Type**: Phase 1 - Developer Onboarding  
**Status**: Existing Implementation Documentation  
**Audience**: New developers joining the project

---

## Overview

This guide provides everything you need to get the Daily Office development environment running and start contributing. The Daily Office is a Django + Vue.js application that generates Anglican/Episcopal daily prayer offices based on the Book of Common Prayer (2019).

**Tech Stack**:

- **Backend**: Django 5.2+ with Python 3.13
- **Frontend**: Vue 3 + Vite 5+ with TypeScript
- **Database**: PostgreSQL 17.5+
- **Cache**: Memcached 1.6+
- **Mobile**: Capacitor 6+ (iOS/Android)

**Project Philosophy**: This project follows a [constitutional framework](../../.specify/constitution.md) with six core principles emphasizing quality, testing, documentation, and traceability.

---

## Prerequisites

Install these tools before starting:

### Required Software

```bash
# macOS (using Homebrew)
brew install python@3.13 node@20 postgresql@17 memcached

# Ubuntu/Debian (using apt)
sudo apt-get update
sudo apt-get install -y python3.13 python3-venv python3-pip nodejs npm postgresql memcached
```

### Verify Installations

```bash
python3 --version  # Should be 3.13+
node --version     # Should be 20+
psql --version     # Should be 17.5+
```

---

## Quick Setup (5 Minutes)

### 1. Clone and Configure

```bash
# Clone repository
git clone https://github.com/your-org/dailyoffice2019.git
cd dailyoffice2019

# Copy environment templates
cp app/.env.development app/.env.local
cp site/website/.env.example site/website/.env

# Edit site/website/.env and set required variables
# Minimum required for development:
DEBUG=True
SECRET_KEY=development-secret-key-not-for-production
POSTGRES_NAME=dailyoffice
POSTGRES_USER=dailyoffice
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
# ... (see "Environment Variables" section below)
```

### 2. Database Setup (~4 seconds)

```bash
# Start PostgreSQL
sudo service postgresql start  # Linux
brew services start postgresql  # macOS

# Create database and user
sudo -u postgres psql -c "CREATE DATABASE dailyoffice;"
sudo -u postgres psql -c "CREATE USER dailyoffice WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE dailyoffice TO dailyoffice;"
sudo -u postgres psql -c "ALTER DATABASE dailyoffice OWNER TO dailyoffice;"

# Import database dump (contains lectionary, calendar, psalms, etc.)
unzip -p site/dailyoffice_2024_01_30.sql.zip dailyoffice_2024_01_30.sql | sudo -u postgres psql dailyoffice
```

**Note**: Database import takes about 4 seconds. The dump includes all lectionary readings, church calendar data, psalms, and pre-cached scripture passages.

### 3. Backend Setup

```bash
cd site

# Create virtual environment
python3 -m venv env
source env/bin/activate  # bash/zsh
# or: . env/bin/activate.fish  # fish shell

# Install Python dependencies (5-45 minutes depending on network)
# Network timeouts are common - use long timeout and retries
pip install --timeout 1200 --retries 10 -r requirements.txt

# Install Node.js build dependencies (~2 minutes)
npm install

# Collect static assets
python manage.py collectstatic --noinput

# Verify setup
python manage.py check
```

**Expected Issues**:

- `pip install` frequently fails with `ReadTimeoutError` - this is normal, just retry with `--timeout 1200 --retries 10`
- If repeated failures, install core packages individually: `pip install Django==5.2 psycopg-binary beautifulsoup4 requests arrow django-environ`

### 4. Frontend Setup

```bash
cd ../app

# Install frontend dependencies
npm install
```

**Expected Issue**: Will fail with `ENOTFOUND npm.fontawesome.com` due to FontAwesome Pro authentication requirement.

**Solution - Configure FontAwesome Pro**:

```bash
# Option 1: GitHub Personal Access Token (recommended)
npm config set "@fortawesome:registry" https://npm.fontawesome.com/
npm config set "//npm.fontawesome.com/:_authToken" YOUR_GITHUB_PAT_WITH_READ_PACKAGES

# Option 2: FontAwesome Pro token
npm config set "@fortawesome:registry" https://npm.fontawesome.com/
npm config set "//npm.fontawesome.com/:_authToken" YOUR_FONTAWESOME_PRO_TOKEN

# Then retry
npm install
```

**Get GitHub PAT**: GitHub Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token with `read:packages` scope

### 5. Start Development Servers

```bash
# Terminal 1: Backend API server (with SSL)
cd site
source env/bin/activate
python manage.py runsslserver
# Access at https://127.0.0.1:8000/

# Terminal 2: Frontend dev server (after FontAwesome resolved)
cd app
npm run dev
# Access at http://127.0.0.1:8080
```

**First Visit**: Navigate to https://127.0.0.1:8000/office/morning_prayer/ to see a generated Morning Prayer office. Frontend at http://127.0.0.1:8080 will consume the API.

---

## Environment Variables Reference

Edit `site/website/.env` with these development values:

```bash
# Core Django Settings
DEBUG=True
DEBUG_DATES=False
SECRET_KEY=development-secret-key-not-for-production
SECURE_SSL_REDIRECT=False
SECURE_PROXY_SSL_HEADER=http

# Database Configuration
POSTGRES_NAME=dailyoffice
POSTGRES_USER=dailyoffice
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Liturgical Calendar Range
FIRST_BEGINNING_YEAR=2018
LAST_BEGINNING_YEAR=2021
FIRST_BEGINNING_YEAR_APP=2019
LAST_BEGINNING_YEAR_APP=2020

# External API Keys (optional for development)
GOOGLE_API_KEY=development-api-key
GOOGLE_CUSTOM_SEARCH_ENGINE_KEY=development-search-key
OPENAI_API_KEY=development-openai-key
BUGSNAG_KEY=development-bugsnag-key

# Email Configuration (optional for development)
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_PORT=465
EMAIL_HOST_USER=development@example.com
EMAIL_HOST_PASSWORD=development-email-password

# Mailgun Configuration (optional)
MAILGUN_PUBLIC_KEY=development-mailgun-public
MAILGUN_PRIVATE_KEY=development-mailgun-private
MAILGUN_SMTP_PASSWORD=development-mailgun-smtp

# MJML Configuration (optional)
MJML_APPLICATION_ID=development-mjml-app
MJML_PUBLIC_KEY=development-mjml-public
MJML_SECRET_KEY=development-mjml-secret

# MailChimp Configuration (optional)
MAILCHIMP_API_KEY=development-mailchimp-key
MAILCHIMP_PREFIX=us4
MAILCHIMP_LIST_ID=development-list-id

# Misc Configuration
SITE_ADDRESS=https://127.0.0.1:8000
ZOOM_LINK=https://zoom.us/development

# Media API Keys (optional - for AI content generation)
OMDB_API_KEY=development-omdb-key
UTELLY_API_KEY=development-utelly-key
IMDB_API_KEY=development-imdb-key
YOUTUBE_API_KEY=development-youtube-key
```

**Critical Variables**: Only `DEBUG`, `SECRET_KEY`, and `POSTGRES_*` variables are required for basic functionality. Other keys can use placeholder values for local development.

---

## Project Structure

```
dailyoffice2019/
├── site/                      # Django backend
│   ├── website/              # Main project settings
│   │   ├── settings.py       # Django configuration
│   │   ├── urls.py           # URL routing
│   │   └── .env              # Environment variables
│   ├── office/               # Daily Office generation logic
│   │   ├── models.py         # Office domain models (OfficeDay, Setting, Collect, etc.)
│   │   ├── offices.py        # Base Office class and ModuleFactory
│   │   ├── morning_prayer.py # Morning Prayer implementation
│   │   ├── evening_prayer.py # Evening Prayer implementation
│   │   ├── midday_prayer.py  # Midday Prayer implementation
│   │   ├── compline.py       # Compline implementation
│   │   ├── family_*.py       # Family prayer implementations
│   │   ├── canticles.py      # Canticle tables and logic
│   │   ├── api/              # REST API
│   │   │   ├── serializers.py # DRF serializers
│   │   │   └── views/        # DRF ViewSets
│   │   └── management/       # Django management commands
│   ├── churchcal/            # Liturgical calendar calculations
│   │   ├── models.py         # Commemoration, Season, Proper, Common
│   │   ├── calculations.py   # Easter date, liturgical year logic
│   │   └── api/              # Calendar REST API
│   ├── bible/                # Scripture passage retrieval
│   │   ├── passage.py        # Bible Gateway API integration
│   │   └── sources.py        # Translation configuration
│   ├── psalter/              # Psalter (Book of Psalms)
│   │   ├── models.py         # Psalm, PsalmVerse models
│   │   └── api/              # Psalms REST API
│   └── manage.py             # Django management CLI
│
├── app/                       # Vue.js frontend
│   ├── src/
│   │   ├── main.js           # Vue app entry point
│   │   ├── App.vue           # Root component
│   │   ├── router/           # Vue Router configuration
│   │   ├── store/            # Vuex state management
│   │   ├── views/            # Page components
│   │   ├── components/       # Reusable Vue components
│   │   └── helpers/          # Utility functions
│   ├── public/               # Static assets
│   ├── package.json          # Frontend dependencies
│   └── vite.config.mjs       # Vite build configuration
│
├── specs/                     # Technical specifications
│   └── 001-daily-office/     # Daily Office spec (retroactive)
│       ├── README.md         # Functional requirements
│       ├── plan.md           # Implementation plan
│       ├── research.md       # Architecture audit
│       ├── data-model.md     # Data model documentation
│       └── contracts/        # API contracts
│
└── .specify/                  # Project governance
    ├── constitution.md       # Six core principles
    └── scripts/              # Automation scripts
```

---

## Common Development Workflows

### Workflow 1: View Generated Office

**Task**: See what a Morning Prayer office looks like for a specific date.

```bash
# Start Django dev server
cd site
source env/bin/activate
python manage.py runsslserver

# Visit in browser
# https://127.0.0.1:8000/office/morning_prayer/2025/12/25/
# https://127.0.0.1:8000/office/evening_prayer/2025/12/25/
# https://127.0.0.1:8000/office/midday_prayer/2025/12/25/
# https://127.0.0.1:8000/office/compline/2025/12/25/

# With settings
# https://127.0.0.1:8000/office/morning_prayer/2025/12/25/?bible_version=kjv&psalter=30day
```

**What You'll See**: Fully formatted liturgical office with headings, prayers, scripture readings, psalms, collects, and rubrics.

### Workflow 2: Test API Endpoints

**Task**: Retrieve data via REST API for frontend consumption.

```bash
# Get all collects
curl https://127.0.0.1:8000/api/collects/ | jq

# Get specific psalm
curl https://127.0.0.1:8000/api/psalms/23/ | jq

# Get psalm topics
curl https://127.0.0.1:8000/api/psalms/topics/ | jq

# Get scripture passage
curl https://127.0.0.1:8000/api/scripture/John%203:16-21/ | jq

# Get settings
curl https://127.0.0.1:8000/api/settings/ | jq

# Get generated office as JSON
curl https://127.0.0.1:8000/api/office/morning_prayer/2025/12/25/ | jq
```

**API Documentation**: See `contracts/README.md` for complete API reference.

### Workflow 3: Run Django Management Commands

```bash
cd site
source env/bin/activate

# Run migrations
python manage.py migrate

# Create superuser (for Django admin)
python manage.py createsuperuser

# Django shell (for testing queries)
python manage.py shell
>>> from office.models import StandardOfficeDay
>>> office_day = StandardOfficeDay.objects.get_date(2025, 12, 25)
>>> office_day.primary_evening_psalms
'19,46'

# Custom management commands
python manage.py check_lectionary  # Verify lectionary data integrity
python manage.py import_collects   # Import collects from CSV
```

### Workflow 4: Format Code Before Committing

**Required by Constitution Principle I (Code Quality)**

```bash
# Python formatting (from site/ directory)
cd site
source env/bin/activate
find . -iname "*.py" | xargs black --target-version=py313 --line-length=119

# Or use pre-commit hooks
pre-commit install
pre-commit run --all-files

# Frontend linting (from app/ directory)
cd app
npm run lint
npm run lint:fix
```

**Code Standards**:

- Python: Black formatter, line length 119
- JavaScript/Vue: ESLint with Vue 3 rules
- Always run formatters before committing

### Workflow 5: Access Django Admin

```bash
# Create superuser (first time only)
cd site
source env/bin/activate
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (your choice)

# Start server and visit
python manage.py runsslserver
# Navigate to https://127.0.0.1:8000/admin/
```

**Admin Capabilities**:

- Edit commemorations, seasons, propers
- Manage collects and their tags
- View/edit psalms and topics
- Manage settings and options
- View cached scripture passages

---

## How To: Add New Office Type

**Example**: Add "Night Prayer" office type (hypothetical).

### Step 1: Create Office Module

```python
# site/office/night_prayer.py

from office.offices import Office
from office.canticles import CanticleTableFactory

class NightPrayer(Office):
    """
    Night Prayer office (Compline variant).

    Implements: FR-XXX (Night Prayer Office)
    """

    name = "Night Prayer"
    office_type = "night_prayer"

    def modules(self):
        """Define liturgical modules in order."""
        return [
            self.get_heading(),
            self.get_opening_sentence(),
            self.get_confession(),
            self.get_psalms(),
            self.get_scripture(),
            self.get_prayers(),
            self.get_collects(),
            self.get_dismissal(),
        ]

    def get_heading(self):
        """Return heading module."""
        from office.offices import Module, Line
        module = Module(self.settings)
        module.append(Line(
            content=f"Night<br>Prayer",
            line_type="heading",
        ))
        return module

    def get_opening_sentence(self):
        """Return opening sentence module."""
        # Implementation here
        pass

    # ... implement other get_* methods
```

### Step 2: Add URL Route

```python
# site/website/urls.py

from office.night_prayer import NightPrayer

urlpatterns = [
    # ... existing patterns

    # Night Prayer
    path(
        'office/night_prayer/<int:year>/<int:month>/<int:day>/',
        OfficeView.as_view(office_class=NightPrayer),
        name='night_prayer'
    ),
]
```

### Step 3: Add API Endpoint

```python
# site/office/api/views/index.py

class NightPrayerView(OfficeAPIView):
    """
    Generate Night Prayer office for specified date.

    Implements: FR-XXX (Night Prayer API)
    """
    office_class = NightPrayer

# Add to urlpatterns in router
router.register(r'night_prayer', NightPrayerView, basename='night_prayer')
```

### Step 4: Add Frontend Route

```javascript
// app/src/router/index.js

export default createRouter({
  routes: [
    // ... existing routes

    {
      path: "/office/night_prayer/:year/:month/:day",
      name: "NightPrayer",
      component: () => import("@/views/OfficeView.vue"),
      props: (route) => ({
        officeType: "night_prayer",
        year: parseInt(route.params.year),
        month: parseInt(route.params.month),
        day: parseInt(route.params.day),
      }),
    },
  ],
});
```

### Step 5: Add Tests

```python
# site/office/tests/test_night_prayer.py

import pytest
from datetime import date
from office.night_prayer import NightPrayer
from office.models import StandardOfficeDay

class TestNightPrayer:
    """
    Test Night Prayer office generation.

    Validates: FR-XXX (Night Prayer Office)
    """

    def test_generates_basic_structure(self):
        """Night prayer generates all required modules."""
        office_day = StandardOfficeDay.objects.get_date(2025, 12, 25)
        office = NightPrayer(office_day, date(2025, 12, 25))

        modules = office.modules()
        module_names = [m.name for m in modules]

        assert "Heading" in module_names
        assert "Opening Sentence" in module_names
        assert "Confession" in module_names
        assert "Psalms" in module_names
        assert "Dismissal" in module_names

    def test_uses_night_prayer_psalms(self):
        """Night prayer uses correct psalms (e.g., 134)."""
        office_day = StandardOfficeDay.objects.get_date(2025, 12, 25)
        office = NightPrayer(office_day, date(2025, 12, 25))

        psalms_module = [m for m in office.modules() if m.name == "Psalms"][0]
        content = " ".join([line.content for line in psalms_module.lines])

        assert "Psalm 134" in content

    # Add more tests...
```

### Step 6: Update Documentation

```markdown
<!-- specs/001-daily-office/README.md -->

### FR-XXX: Night Prayer Office

**Priority**: P2 (Medium)  
**Status**: ✅ Implemented

The system shall provide a Night Prayer office...

**Implementation**: `site/office/night_prayer.py`
```

---

## How To: Modify Liturgical Settings

**Example**: Add a new setting for "Include Metrical Psalms" option.

### Step 1: Create Setting in Database

```python
# Use Django shell or create migration
cd site
source env/bin/activate
python manage.py shell

from office.models import Setting, SettingOption

# Create setting
setting = Setting.objects.create(
    name="metrical_psalms",
    title="Metrical Psalms",
    description="Include metrical psalm versions alongside prose psalms.",
    setting_type=2,  # Additional Settings
    site=1,  # Daily Office
    order=15,
)

# Create options
SettingOption.objects.create(
    setting=setting,
    name="Include Metrical Psalms",
    description="Show metrical psalm versions",
    value="include",
    abbreviation="M",
    order=1,
)

SettingOption.objects.create(
    setting=setting,
    name="Prose Only",
    description="Show only prose psalms",
    value="prose_only",
    abbreviation="P",
    order=2,
)
```

### Step 2: Handle Setting in Office Generation

```python
# site/office/offices.py

class Office:
    def __init__(self, office_day, date, **kwargs):
        # ... existing code

        # Add new setting
        self.metrical_psalms = kwargs.get('metrical_psalms', 'prose_only')

    def get_psalms(self):
        """Generate psalms module with optional metrical versions."""
        module = Module(self.settings)

        # Add prose psalms
        for psalm_number in self.get_psalm_numbers():
            psalm = Psalm.objects.get(number=psalm_number)
            # ... add psalm verses

        # Add metrical version if enabled
        if self.metrical_psalms == 'include':
            metrical_collect = MetricalCollect.objects.filter(
                psalm_number=psalm_number
            ).first()
            if metrical_collect:
                module.append(Line(
                    content=f"<em>Metrical Version:</em>",
                    line_type="rubric",
                ))
                module.append(Line(
                    content=metrical_collect.text,
                    line_type="html",
                ))

        return module
```

### Step 3: Update API to Accept Setting

Settings automatically passed via query parameters:

```bash
# Use new setting
curl "https://127.0.0.1:8000/api/office/morning_prayer/2025/12/25/?metrical_psalms=include"
```

### Step 4: Update Frontend to Use Setting

```javascript
// app/src/store/modules/settings.js

export default {
  state: {
    // ... existing settings
    metrical_psalms: "prose_only",
  },

  mutations: {
    SET_METRICAL_PSALMS(state, value) {
      state.metrical_psalms = value;
      localStorage.setItem("office_settings", JSON.stringify(state));
    },
  },

  actions: {
    updateMetricalPsalms({ commit }, value) {
      commit("SET_METRICAL_PSALMS", value);
    },
  },
};
```

```vue
<!-- app/src/components/SettingsPanel.vue -->

<template>
  <div class="setting">
    <label>Metrical Psalms</label>
    <select v-model="metricalPsalms" @change="updateSetting">
      <option value="prose_only">Prose Only</option>
      <option value="include">Include Metrical Psalms</option>
    </select>
  </div>
</template>

<script>
export default {
  computed: {
    metricalPsalms: {
      get() {
        return this.$store.state.settings.metrical_psalms;
      },
      set(value) {
        this.$store.dispatch("settings/updateMetricalPsalms", value);
      },
    },
  },
};
</script>
```

### Step 5: Add Tests

```python
# site/office/tests/test_settings.py

def test_metrical_psalms_setting():
    """Metrical psalms setting includes metrical versions when enabled."""
    office_day = StandardOfficeDay.objects.get_date(2025, 1, 1)

    # With setting disabled
    office = MorningPrayer(office_day, date(2025, 1, 1), metrical_psalms='prose_only')
    modules = office.modules()
    content = " ".join([line.content for line in modules if module.name == "Psalms"])
    assert "Metrical Version:" not in content

    # With setting enabled
    office = MorningPrayer(office_day, date(2025, 1, 1), metrical_psalms='include')
    modules = office.modules()
    content = " ".join([line.content for line in modules if module.name == "Psalms"])
    assert "Metrical Version:" in content
```

---

## How To: Debug Common Issues

### Issue 1: Office Not Generating

**Symptoms**: Blank page, 500 error, or missing modules.

**Debug Steps**:

```python
# Django shell debugging
cd site
source env/bin/activate
python manage.py shell

from office.morning_prayer import MorningPrayer
from office.models import StandardOfficeDay
from datetime import date

# Get office day
office_day = StandardOfficeDay.objects.get_date(2025, 12, 25)
print(f"Office Day: {office_day}")
print(f"Primary: {office_day.primary_office_date}")
print(f"Evening Psalms: {office_day.primary_evening_psalms}")

# Try to generate office
office = MorningPrayer(office_day, date(2025, 12, 25))
modules = office.modules()
print(f"Modules Generated: {len(modules)}")

# Check each module
for module in modules:
    print(f"\nModule: {module.name}")
    print(f"Lines: {len(module.lines)}")
    if len(module.lines) == 0:
        print("  ^ WARNING: Empty module!")
```

**Common Causes**:

- Missing `StandardOfficeDay` for date → Import database dump
- Missing scripture cache → Run office once to populate cache from Bible Gateway API
- Invalid psalm references → Check `office_day.primary_morning_psalms` format
- Missing commemoration → Check `churchcal` app data

### Issue 2: Scripture Not Loading

**Symptoms**: Empty scripture readings or API errors.

**Debug Steps**:

```python
# Check scripture cache
from office.models import Scripture

# See what's cached
cached = Scripture.objects.filter(passage__icontains="John 3:16")
print(f"Cached passages: {cached.count()}")

# Try fetching from Bible Gateway
from bible.passage import PassageRetrieval

retrieval = PassageRetrieval("John 3:16-21", "esv")
text = retrieval.get_passage()
print(f"Retrieved: {text[:100]}...")

# Check API key configuration
from django.conf import settings
print(f"Bible Gateway configured: {hasattr(settings, 'BIBLE_GATEWAY_API_KEY')}")
```

**Solutions**:

- Scripture cache missing → Let office generation populate cache automatically
- Bible Gateway API timeout → Check network, retry
- Invalid passage format → Ensure proper citation format (e.g., "Genesis 1:1-5")

### Issue 3: Calendar Calculations Wrong

**Symptoms**: Wrong season, collect, or lectionary reading for a date.

**Debug Steps**:

```python
from churchcal.calculations import ChurchYear
from datetime import date

year = ChurchYear(2025)
print(f"Easter: {year.easter}")
print(f"Advent 1: {year.advent_1}")
print(f"Epiphany Season Start: {year.epiphany_season_start}")

# Check specific date
check_date = date(2025, 12, 25)
print(f"\nDate: {check_date}")
print(f"Season: {year.get_season(check_date)}")
print(f"Week: {year.get_week(check_date)}")

# Check commemoration
from churchcal.models import TemporaleCommemoration
commemoration = TemporaleCommemoration.objects.filter(
    date=check_date
).first()
print(f"Commemoration: {commemoration.name if commemoration else 'None'}")
```

**Common Issues**:

- Easter calculation off → Verify `calculations.py` computus algorithm
- Feast day not in database → Import commemorations data
- Season boundaries incorrect → Check `ChurchYear` class logic

### Issue 4: Frontend Not Connecting to API

**Symptoms**: Vue app shows no content, API calls fail.

**Debug Steps**:

```javascript
// Browser console
// Check API configuration
console.log("API Base:", import.meta.env.VITE_API_BASE_URL);

// Test API connection
fetch("https://127.0.0.1:8000/api/settings/")
  .then((r) => r.json())
  .then((d) => console.log("API working:", d))
  .catch((e) => console.error("API failed:", e));

// Check stored settings
console.log("Stored settings:", localStorage.getItem("office_settings"));
```

**Solutions**:

- CORS error → Configure CORS in Django settings
- SSL certificate error → Accept self-signed cert in browser (dev only)
- Wrong API URL → Check `app/.env.local` has correct `VITE_API_BASE_URL`
- Network timeout → Ensure backend server running

---

## Testing Guide

### Running Tests

```bash
# Backend tests (pytest)
cd site
source env/bin/activate
pytest

# Run specific test file
pytest office/tests/test_morning_prayer.py

# Run with coverage
pytest --cov=office --cov-report=html

# Frontend tests (Vitest)
cd app
npm run test

# E2E tests (Playwright)
cd app
npm run test:e2e
```

### Writing Tests

**Test Structure** (following Constitution Principle III):

```python
# site/office/tests/test_feature.py

import pytest
from datetime import date
from office.models import StandardOfficeDay
from office.morning_prayer import MorningPrayer

class TestFeatureName:
    """
    Test suite for [feature name].

    Validates: FR-XXX ([requirement name])
    """

    def test_basic_functionality(self):
        """[Feature] performs basic function correctly."""
        # Arrange
        office_day = StandardOfficeDay.objects.get_date(2025, 1, 1)
        office = MorningPrayer(office_day, date(2025, 1, 1))

        # Act
        result = office.some_method()

        # Assert
        assert result == expected_value
        assert result.has_property

    def test_edge_case_1(self):
        """[Feature] handles [edge case] correctly."""
        # Test edge case
        pass

    def test_error_handling(self):
        """[Feature] raises appropriate errors for invalid input."""
        with pytest.raises(ValueError):
            # Code that should raise error
            pass
```

**Test Coverage Targets** (per Constitution):

- **P0 (Critical)**: 100% coverage required
- **P1 (High)**: 90% coverage required
- **P2 (Medium)**: 80% coverage required

**Requirement Traceability**:

- Every test docstring should reference FR-XXX requirement
- Test class docstring should include "Validates: FR-XXX"
- This enables automated traceability reporting

---

## Code Quality Standards

### Python Code Standards

**Black Formatting**:

```bash
black --target-version=py313 --line-length=119 site/
```

**Type Hints** (encouraged):

```python
from typing import List, Dict, Optional
from datetime import date

def get_psalms_for_date(office_date: date, psalter: str = "60day") -> List[int]:
    """
    Retrieve psalm numbers for specified date.

    Implements: FR-007 (Psalter Assignment)

    Args:
        office_date: Date to retrieve psalms for
        psalter: Psalter cycle ("30day" or "60day")

    Returns:
        List of psalm numbers to pray

    Raises:
        ValueError: If psalter value invalid
    """
    if psalter not in ["30day", "60day"]:
        raise ValueError(f"Invalid psalter: {psalter}")

    # Implementation
    return [1, 2, 3]
```

**Docstring Requirements** (per Constitution Principle I):

- Every public function/method must have docstring
- Include "Implements: FR-XXX" for requirement traceability
- Document parameters, return values, exceptions
- Use Google-style or NumPy-style docstrings

### Vue/JavaScript Standards

**ESLint Configuration** (already configured in `app/eslint.config.mjs`):

```javascript
// Follow Vue 3 composition API patterns
import { ref, computed, onMounted } from "vue";

export default {
  name: "ComponentName",

  setup() {
    // Reactive state
    const count = ref(0);

    // Computed properties
    const doubled = computed(() => count.value * 2);

    // Lifecycle hooks
    onMounted(() => {
      console.log("Component mounted");
    });

    // Return public API
    return {
      count,
      doubled,
    };
  },
};
```

**Component Documentation**:

```vue
<template>
  <!-- Component template -->
</template>

<script>
/**
 * ComponentName: Brief description.
 *
 * Implements: FR-XXX (Requirement Name)
 *
 * Props:
 *   - officeType (string): Type of office to display
 *   - date (Date): Office date
 *
 * Events:
 *   - settingsChanged: Emitted when user changes settings
 */
export default {
  name: "ComponentName",
  // ... implementation
};
</script>
```

---

## Deployment

### Production Build

```bash
# Backend: Collect static assets
cd site
source env/bin/activate
python manage.py collectstatic --noinput

# Frontend: Build for production
cd app
npm run build
# Output in app/dist/
```

### Deploy to Cloudflare (Frontend)

```bash
# Frontend deployment handled via Cloudflare Pages
# Connected to GitHub repository
# Automatic deploys on push to main branch

# Manual deploy
cd app
npm run build
wrangler pages deploy dist/
```

### Deploy API (Backend)

```bash
# Backend deployment uses git deploy hooks
# See deploy/post-receive for deployment script

# Push to production remote
git push production main

# Post-receive hook automatically:
# - Activates virtualenv
# - Installs dependencies
# - Runs migrations
# - Collects static files
# - Restarts gunicorn/uwsgi
```

---

## Getting Help

### Resources

- **API Documentation**: `specs/001-daily-office/contracts/README.md`
- **Data Model**: `specs/001-daily-office/data-model.md`
- **Architecture**: `specs/001-daily-office/research.md`
- **Constitution**: `.specify/constitution.md`
- **Functional Requirements**: `specs/001-daily-office/README.md`

### Common Commands Cheatsheet

```bash
# Start development servers
cd site && source env/bin/activate && python manage.py runsslserver
cd app && npm run dev

# Format code
black --target-version=py313 --line-length=119 site/
cd app && npm run lint:fix

# Run tests
cd site && pytest
cd app && npm run test

# Django shell
cd site && python manage.py shell

# Check for errors
cd site && python manage.py check

# View logs (in development)
# Backend: Terminal running runsslserver
# Frontend: Terminal running npm run dev
```

### Debugging Tips

1. **Use Django Debug Toolbar**: Install `django-debug-toolbar` for SQL query analysis
2. **Vue DevTools**: Install browser extension for Vue debugging
3. **Print statements**: Use `print()` in Python, `console.log()` in JavaScript for quick debugging
4. **Django shell**: Best tool for testing queries and models interactively
5. **Git bisect**: Use `git bisect` to find commit that introduced bug

### Project Status

**Current State** (as of November 6, 2025):

- ✅ **Functionally complete**: All 28 functional requirements implemented (93% accuracy)
- ⚠️ **Test coverage**: Critically insufficient (~5-10% coverage, need 80-90%)
- ⚠️ **Traceability**: Missing FR-XXX annotations in code (need 50+ files annotated)
- ⚠️ **Documentation**: API docs and data model now complete, code docstrings need improvement

**Known Issues**:

- Psalm parsing bug: `office/models.py` line 81 - `psalms.split(psalms)` should be `psalms.split(',')`
- Test suite absent: 200-280 tests needed (155-440 hours effort)
- Traceability absent: 50 files need FR-XXX annotations (17.5 hours effort)

**Contribution Priorities**:

1. **P0 (Critical)**: Add comprehensive test suite (Constitution violation)
2. **P1 (High)**: Add FR-XXX requirement traceability annotations
3. **P2 (Medium)**: Fix psalm parsing bug, improve docstrings, reduce code duplication

---

## Next Steps

After getting your environment running:

1. **Explore the codebase**: Read `research.md` for architecture overview
2. **Run the tests**: `cd site && pytest` (currently minimal, needs expansion)
3. **Generate an office**: Visit https://127.0.0.1:8000/office/morning_prayer/
4. **Read the API docs**: `contracts/README.md` for API details
5. **Pick an issue**: Check GitHub issues or help with test coverage

**Welcome to the Daily Office project!** 🙏

---

**Document Version**: 1.0  
**Last Updated**: November 6, 2025  
**Target Audience**: New developers joining the project
