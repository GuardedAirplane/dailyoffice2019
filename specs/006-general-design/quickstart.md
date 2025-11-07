# Developer Quickstart Guide: Daily Office 2019

**Version**: 1.0  
**Date**: November 7, 2025  
**Audience**: New developers joining the project

## Welcome! 👋

This guide will help you get up and running with the Daily Office 2019 project. The application provides the Book of Common Prayer 2019 Daily Office services accessible via web and mobile apps.

---

## 📋 Prerequisites

Before you begin, ensure you have these installed:

- **Python 3.13** - Backend Django API
- **Node.js 24.4+** - Frontend build system (tested with Node 20)
- **PostgreSQL 17.5+** - Database
- **Memcached 1.6+** - Caching layer
- **Git** - Version control

### Ubuntu/Debian Installation

```bash
sudo apt-get update
sudo apt-get install -y postgresql memcached python3-venv python3-pip
```

---

## 🚀 Quick Setup (30 minutes)

### Step 1: Clone the Repository

```bash
git clone https://github.com/GuardedAirplane/dailyoffice2019.git
cd dailyoffice2019
```

### Step 2: Environment Configuration

```bash
# Frontend environment
cp app/.env.development app/.env.local

# Backend environment
cp site/website/.env.example site/website/.env

# Edit site/website/.env with development values
# See "Environment Variables" section below
```

### Step 3: Database Setup (~4 seconds)

```bash
# Start PostgreSQL
sudo service postgresql start

# Create database and user
sudo -u postgres psql -c "CREATE DATABASE dailyoffice;"
sudo -u postgres psql -c "CREATE USER dailyoffice WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE dailyoffice TO dailyoffice;"

# Import database dump
unzip -p site/dailyoffice_2024_01_30.sql.zip dailyoffice_2024_01_30.sql | sudo -u postgres psql dailyoffice
```

### Step 4: Backend Setup

```bash
cd site

# Create Python virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies (5-45 minutes, network-dependent)
# IMPORTANT: Use maximum timeouts, NEVER CANCEL
pip install --timeout 1200 --retries 10 -r requirements.txt

# Install Node dependencies for backend (~2 minutes)
npm install

# Collect static assets
python manage.py collectstatic --noinput
```

### Step 5: Frontend Setup

```bash
cd ../app

# Install dependencies
npm install
```

**Note**: If you encounter FontAwesome Pro authentication errors, see "Troubleshooting" section below.

### Step 6: Start Development Servers

**Backend (Django API)**:

```bash
cd site
source env/bin/activate
python manage.py runsslserver
# Accessible at https://127.0.0.1:8000/
```

**Frontend (Vue.js)**:

```bash
cd app
npm run dev
# Accessible at http://127.0.0.1:8080
```

---

## 🏗️ Architecture Overview

### Technology Stack

**Frontend**:

- **Vue 3** - Progressive JavaScript framework
- **Vite 6.x** - Fast build tool with HMR
- **Capacitor 7.4.3** - Mobile app wrapper (iOS/Android)
- **Element Plus** - UI component library
- **Tailwind CSS 3.x** - Utility-first CSS framework
- **Vuex** - State management

**Backend**:

- **Django 5.2+** - Python web framework
- **PostgreSQL 17.5+** - Relational database
- **Memcached 1.6+** - Caching layer

**Mobile**:

- **Capacitor** - Native iOS/Android wrappers
- **DynamicStorage** - Unified storage abstraction (localStorage/Capacitor Preferences)

### Project Structure

```
dailyoffice2019/
├── app/                      # Frontend Vue.js application
│   ├── src/
│   │   ├── components/       # Reusable Vue components
│   │   ├── views/            # Page components
│   │   ├── router/           # Vue Router configuration
│   │   ├── store/            # Vuex store
│   │   └── helpers/          # Utility functions
│   ├── public/               # Static assets
│   └── tests/                # Frontend tests (unit + e2e)
│
├── site/                     # Backend Django application
│   ├── website/              # Main Django app (settings, URLs)
│   ├── office/               # Daily Office generation logic
│   ├── churchcal/            # Church calendar calculations
│   ├── bible/                # Bible passage retrieval
│   ├── psalter/              # Psalm passage handling
│   └── hymnal/               # Hymnal integration
│
├── specs/                    # Feature specifications
│   └── 006-general-design/   # Cross-platform access spec
│       ├── spec.md           # Feature specification
│       ├── plan.md           # Implementation plan
│       ├── research.md       # Technology research
│       ├── data-model.md     # Data schemas
│       └── quickstart.md     # This file
│
└── keystore/                 # Android signing keys
```

### Key Directories Explained

- **`app/src/helpers/storage.js`** - DynamicStorage abstraction for unified storage API
- **`app/src/store/index.js`** - Vuex store managing application settings
- **`app/src/views/Settings.vue`** - Main settings page
- **`app/src/components/ShareSettings.vue`** - Settings sharing with QR codes
- **`site/office/`** - Core office generation (Morning Prayer, Evening Prayer, Compline)
- **`site/churchcal/`** - Liturgical calendar support (BCP 2019)

---

## 🧪 Testing Guide

### Current State (Phase 0)

⚠️ **IMPORTANT**: The project currently has **minimal test coverage**. Phase 2 (Testing Infrastructure) will address this before any new features are built.

### Running Existing Tests

**Backend Tests**:

```bash
cd site
source env/bin/activate
python manage.py test
```

**Frontend Tests** (limited):

```bash
cd app
npm run test:unit
npm run test:e2e
```

### Testing Strategy (Phase 2 - Coming Soon)

The project will implement comprehensive testing:

1. **Unit Tests** (Vitest + Vue Test Utils)

   - Helpers: `storage.js`, encoding functions
   - Store: Vuex actions and mutations
   - Components: Settings panels, modals

2. **Component Tests** (Vitest + Vue Test Utils)

   - `Settings.vue` - Settings page
   - `ShareSettings.vue` - Settings sharing

3. **E2E Tests** (Cypress)
   - Settings persistence
   - Settings sharing via URL
   - Responsive design
   - Mobile app functionality

**Coverage Targets**:

- Existing code: 90%+ function coverage, 85%+ branch coverage
- New code: 100% coverage required

See [research.md](./research.md#phase-1-testing-infrastructure) for detailed testing patterns.

---

## 🔧 Development Workflow

### Daily Development

1. **Pull latest changes**:

   ```bash
   git pull origin main
   ```

2. **Create feature branch** (Constitution Principle II):

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Start services**:

   ```bash
   # Terminal 1: Backend
   cd site && source env/bin/activate && python manage.py runsslserver

   # Terminal 2: Frontend
   cd app && npm run dev
   ```

4. **Make changes** following Constitution principles (see below)

5. **Format code before committing**:

   ```bash
   # Python formatting
   cd site
   find . -iname "*.py" | xargs black --target-version=py313 --line-length=119

   # Pre-commit hooks (all formatting)
   pre-commit run --all-files
   ```

6. **Test your changes**:

   ```bash
   # Backend
   cd site && python manage.py check

   # Frontend
   cd app && npm run lint
   ```

7. **Commit and push**:
   ```bash
   git add .
   git commit -m "feat: your feature description"
   git push origin feature/your-feature-name
   ```

### Code Style

**Python**:

- Black formatter with Python 3.13 target
- Line length: 119 characters
- Django best practices

**JavaScript/Vue**:

- ESLint configuration (see `app/eslint.config.mjs`)
- Vue 3 Composition API preferred
- TypeScript for type safety (optional)

---

## 📖 Constitution Principles

All development **MUST** follow these principles:

### I. Glory to God

- User spiritual experience > Technical elegance
- Accessibility is a priority
- Prayer functionality is sacred

### II. Feature Branch Development

- All work in feature branches
- Proper branch naming: `feature/`, `bugfix/`, `hotfix/`
- No direct commits to `main`

### III. Comprehensive Testing (NON-NEGOTIABLE)

- **NEW CODE**: 100% test coverage required
- **EXISTING CODE**: 90%+ coverage target (Phase 2)
- Tests written BEFORE implementation (for new features)
- No exceptions

### IV. Code Quality

- Code reviews required
- Formatting standards enforced
- Documentation required

See [constitution.md](../README.md) for full details.

---

## 🛠️ Common Tasks

### Running Django Shell

```bash
cd site
source env/bin/activate
python manage.py shell
```

### Database Migrations

```bash
cd site
source env/bin/activate

# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate
```

### Adding a New Vue Component

```bash
# Create component file
touch app/src/components/YourComponent.vue

# Component template:
```

```vue
<template>
  <div>
    <!-- Your template -->
  </div>
</template>

<script>
export default {
  name: "YourComponent",
  props: {
    // Your props
  },
  setup(props) {
    // Composition API logic
  },
};
</script>

<style scoped>
/* Component styles */
</style>
```

### Using DynamicStorage

```javascript
import DynamicStorage from "@/helpers/storage";

// Store data
await DynamicStorage.setItem("key", "value");

// Retrieve data
const value = await DynamicStorage.getItem("key");

// Remove data
await DynamicStorage.removeItem("key");
```

**Note**: DynamicStorage automatically uses Capacitor Preferences on mobile and localStorage on web.

### Building Mobile Apps

```bash
cd app

# Build for iOS
npm run build:ios
npx cap sync ios
npx cap open ios

# Build for Android
npm run build:android
npx cap sync android
npx cap open android
```

---

## 🐛 Troubleshooting

### Issue: FontAwesome Pro Authentication Error

**Error**: `ENOTFOUND npm.fontawesome.com`

**Solution**: Configure FontAwesome Pro credentials:

```bash
# Option 1: Using GitHub Personal Access Token
npm config set "@fortawesome:registry" https://npm.fontawesome.com/
npm config set "//npm.fontawesome.com/:_authToken" YOUR_GITHUB_TOKEN

# Option 2: Using .npmrc file
echo "@fortawesome:registry=https://npm.fontawesome.com/
//npm.fontawesome.com/:_authToken=\${FONTAWESOME_TOKEN}" > app/.npmrc

# Option 3: Environment variable
export FONTAWESOME_TOKEN=your_github_token
cd app && npm install
```

**GitHub Token Setup**:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `read:packages` scope
3. Copy token and use above

### Issue: pip install Timeout

**Error**: `ReadTimeoutError`

**Solution**: Use maximum timeouts and retries:

```bash
pip install --timeout 1200 --retries 10 -r requirements.txt
```

**Important**: Do NOT cancel the installation. It can take 5-45 minutes depending on network conditions.

### Issue: Database Connection Error

**Error**: `could not connect to server`

**Solution**: Ensure PostgreSQL is running:

```bash
sudo service postgresql start
sudo service postgresql status
```

Verify connection settings in `site/website/.env`:

```
POSTGRES_NAME=dailyoffice
POSTGRES_USER=dailyoffice
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Issue: Memcached Not Running

**Error**: Django cache errors

**Solution**:

```bash
sudo service memcached start
sudo service memcached status
```

### Issue: Port Already in Use

**Error**: `Address already in use`

**Solution**:

```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
python manage.py runsslserver 0.0.0.0:8001
```

---

## 🔐 Environment Variables

Edit `site/website/.env` with these development values:

```bash
# Django Settings
DEBUG=True
DEBUG_DATES=False
SECRET_KEY=development-secret-key-not-for-production

# Security
SECURE_SSL_REDIRECT=False
SECURE_PROXY_SSL_HEADER=http

# Database
POSTGRES_NAME=dailyoffice
POSTGRES_USER=dailyoffice
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Calendar Configuration
FIRST_BEGINNING_YEAR=2018
LAST_BEGINNING_YEAR=2021
FIRST_BEGINNING_YEAR_APP=2019
LAST_BEGINNING_YEAR_APP=2020

# External APIs (development placeholders)
GOOGLE_API_KEY=development-api-key
GOOGLE_CUSTOM_SEARCH_ENGINE_KEY=development-search-key
BUGSNAG_KEY=development-bugsnag-key
OPENAI_API_KEY=development-openai-key
OMDB_API_KEY=development-omdb-key
UTELLY_API_KEY=development-utelly-key
IMDB_API_KEY=development-imdb-key
YOUTUBE_API_KEY=development-youtube-key

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_PORT=465
EMAIL_HOST_USER=development@example.com
EMAIL_HOST_PASSWORD=development-email-password

# Mailgun
MAILGUN_PUBLIC_KEY=development-mailgun-public
MAILGUN_PRIVATE_KEY=development-mailgun-private
MAILGUN_SMTP_PASSWORD=development-mailgun-smtp

# MJML
MJML_APPLICATION_ID=development-mjml-app
MJML_PUBLIC_KEY=development-mjml-public
MJML_SECRET_KEY=development-mjml-secret

# MailChimp
MAILCHIMP_API_KEY=development-mailchimp-key
MAILCHIMP_PREFIX=us4
MAILCHIMP_LIST_ID=development-list-id

# Application URLs
SITE_ADDRESS=https://127.0.0.1:8000
ZOOM_LINK=https://zoom.us/development
```

---

## 📚 Key Documentation

### Project Documentation

- **[spec.md](./spec.md)** - Feature specification for cross-platform access
- **[plan.md](./plan.md)** - Implementation plan with 8 phases
- **[research.md](./research.md)** - Comprehensive technology research
- **[data-model.md](./data-model.md)** - Data schemas and structures
- **[constitution.md](../README.md)** - Project principles (NON-NEGOTIABLE)

### Technology Documentation

**Frontend**:

- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Capacitor Documentation](https://capacitorjs.com/)
- [Element Plus Documentation](https://element-plus.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

**Backend**:

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

**Testing** (Phase 2):

- [Vitest Documentation](https://vitest.dev/)
- [Cypress Documentation](https://www.cypress.io/)
- [Vue Test Utils Documentation](https://test-utils.vuejs.org/)

---

## 🎯 Current Development Phase

### Phase 1: Design & Contracts (Week 3) - **IN PROGRESS**

✅ **Completed**:

- Phase 0: Research & Planning
- Technology decisions documented
- Data models defined

🚧 **Current Tasks**:

- ✅ Create `data-model.md`
- ✅ Create `quickstart.md` (this file)
- ⏳ Update `copilot-instructions.md`
- ⏳ Design API contracts (optional)

### Phase 2: Testing Infrastructure (Week 4-6) - **NEXT PRIORITY**

This is the **HIGHEST PRIORITY** phase before any new features:

1. Set up Vitest with coverage reporting
2. Write unit tests for existing code:
   - `app/src/helpers/storage.js` (DynamicStorage)
   - `app/src/helpers/` (encoding functions)
   - `app/src/store/index.js` (Vuex store)
3. Write component tests:
   - `app/src/views/Settings.vue`
   - `app/src/components/ShareSettings.vue`
4. Write E2E tests with Cypress:
   - Settings persistence
   - Settings sharing
   - Responsive design
5. Achieve 90%+ coverage

**No new features will be built until Phase 2 is complete** (Constitution Principle III).

---

## 💡 Pro Tips

1. **Read the Constitution**: Seriously. It's not optional. See `constitution.md`.

2. **Test First, Code Second**: For Phase 2 onwards, write tests BEFORE implementing features.

3. **Use DynamicStorage**: Don't use localStorage directly. Use the DynamicStorage abstraction for cross-platform compatibility.

4. **Follow URL Encoding**: Maintain backward compatibility with existing settings URL format.

5. **Respect Prayer Time**: Don't interrupt ongoing prayer with breaking changes or forced updates.

6. **Ask Questions**: Join the project chat or open a GitHub discussion.

7. **Run Formatters**: Always run `black` and `pre-commit` before committing.

8. **Check Django System**: Run `python manage.py check` frequently.

---

## 🤝 Getting Help

### Resources

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community support
- **Project Documentation**: `specs/` directory
- **Code Comments**: Inline documentation

### Contact

- **Project Maintainer**: GuardedAirplane (GitHub)
- **Repository**: https://github.com/GuardedAirplane/dailyoffice2019

---

## 🎉 You're Ready!

You should now have:

- ✅ Development environment set up
- ✅ Understanding of project architecture
- ✅ Knowledge of development workflow
- ✅ Familiarity with testing strategy
- ✅ Awareness of Constitution principles

**Next Steps**:

1. Explore the codebase: `app/src/` and `site/`
2. Read the research document: [research.md](./research.md)
3. Review the current implementation plan: [plan.md](./plan.md)
4. Check out Phase 2 testing tasks
5. Pick an issue and start coding!

**Welcome to the Daily Office 2019 project!** 🙏

---

**Last Updated**: November 7, 2025  
**Phase**: Phase 1 (Design & Contracts)  
**Status**: Active Development
