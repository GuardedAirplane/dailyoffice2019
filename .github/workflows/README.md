# GitHub Actions Workflows

This directory contains GitHub Actions CI/CD workflows for the Daily Office 2019 project. All workflows leverage the existing Docker infrastructure defined in `docker-compose.yml` to ensure consistency between local development and CI environments.

## Available Workflows

### 1. Backend Tests (`backend-tests.yml`)

**Triggers:**
- Push to `main`, `develop`, or any `*-daily-office` branch
- Pull requests to `main` or `develop`
- Changes to `site/**` or `docker-compose.yml`

**What it does:**
- Starts PostgreSQL, Memcached, and Django backend via Docker Compose
- Loads production database dump for realistic test data
- Runs Django system check
- Executes pytest with coverage for:
  - `office/` (Daily Office generation)
  - `churchcal/` (Liturgical calendar)
  - `bible/` (Scripture retrieval)
  - `psalter/` (Psalm handling)
- Generates coverage reports (XML, HTML, terminal)
- Uploads coverage to Codecov (optional)
- Publishes test results and PR comments

**Coverage Requirements (per Constitution Principle III):**
- P0 (Critical): 100% function coverage required
- P1 (High): 90% coverage required
- P2 (Medium): 80% coverage required

**Local equivalent:**
```bash
# Start services
docker-compose up -d db cache backend

# Run tests
docker-compose exec -T backend python -m pytest \
  --cov=office --cov=churchcal --cov=bible --cov=psalter \
  --cov-report=html --cov-report=term-missing
```

### 2. Frontend Tests (`frontend-tests.yml`)

**Triggers:**
- Push to `main`, `develop`, or any `*-daily-office` branch
- Pull requests to `main` or `develop`
- Changes to `app/**`

**Two jobs:**

#### a) Unit Tests (Vitest)
- Runs Vue component unit tests
- Generates coverage reports
- Fast feedback (<5 minutes)

**Local equivalent:**
```bash
docker-compose up -d frontend
docker-compose exec -T frontend npm run test:unit
```

#### b) E2E Tests (Cypress)
- Starts full stack (database, backend, frontend)
- Loads database dump
- Runs browser-based integration tests
- Captures screenshots and videos of failures
- Slower but comprehensive (~15-30 minutes)

**Local equivalent:**
```bash
docker-compose up -d
docker-compose exec -T frontend npm run test:e2e
```

### 3. Code Formatting & Linting (`formatting.yml`)

**Triggers:**
- Push to any branch
- Pull requests to `main` or `develop`

**Three jobs:**

#### a) Black Formatting (Python)
- Checks Python code against Black formatter
- Uses `--target-version=py313 --line-length=119`
- Excludes migrations and `__pycache__`
- Auto-creates PR with fixes if formatting fails (on pull requests)

**Local equivalent:**
```bash
docker-compose exec -T backend \
  find . -iname "*.py" -not -path "*/migrations/*" | \
  xargs black --target-version=py313 --line-length=119
```

#### b) ESLint (JavaScript/Vue)
- Checks JavaScript and Vue code
- Reports issues but doesn't auto-fix (requires manual review)

**Local equivalent:**
```bash
docker-compose exec -T frontend npm run lint
```

#### c) Pre-commit Hooks
- Runs all configured pre-commit hooks
- Ensures consistency with local development

**Local equivalent:**
```bash
pre-commit run --all-files
```

### 4. Full CI Suite (`ci.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main` or `develop`

**What it does:**
- Runs all tests in parallel:
  - Backend tests with coverage
  - Frontend unit tests
  - Code formatting checks
- Generates unified test report
- Caches Docker images for faster runs
- Provides single pass/fail status for PR merging

**Use case:** Primary CI check for pull requests and merges.

## Workflow Architecture

All workflows follow this pattern:

```
1. Checkout code
2. Verify Docker installation
3. Start required services via docker-compose
4. Wait for services to be healthy
5. Load database dump (if needed)
6. Run tests/checks inside Docker containers
7. Copy results out of containers
8. Upload artifacts/reports
9. Clean up (stop containers)
```

### Why Docker?

- **Consistency**: Same containers locally and in CI
- **Isolation**: Each job runs in clean environment
- **Reproducibility**: Exact same dependencies and versions
- **Native support**: Widely supported across CI/CD platforms

## Configuration

### Required Secrets (Optional)

- `CODECOV_TOKEN`: For uploading coverage to Codecov.io
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

### Docker Compose Setup

The workflows use the existing `docker-compose.yml` which defines:
- `db`: PostgreSQL 17 database
- `cache`: Memcached 1.6
- `backend`: Django 5.2+ application
- `frontend`: Vue 3 + Vite application

### Database Dump

Tests require the production database dump:
- **Location**: `site/dailyoffice_2024_01_30.sql.zip`
- **Size**: 111MB compressed
- **Load time**: ~13 seconds
- **Contains**: StandardOfficeDay, HolyDayOfficeDay, Commemorations, Collects, Psalms

## Troubleshooting

### Tests fail locally but pass in CI (or vice versa)

1. Ensure your local Docker images are up to date:
   ```bash
   docker-compose build --no-cache
   ```

2. Check Docker Compose version matches CI:
   ```bash
   docker-compose --version
   ```

3. Verify database dump is loaded:
   ```bash
   docker-compose exec -T db psql -U dailyoffice -d dailyoffice -c "SELECT COUNT(*) FROM office_standardofficeday;"
   ```

### Docker commands fail in CI

- Check service names match `docker-compose.yml`
- Verify container names: `docker-compose ps`

### Coverage upload fails

- Codecov upload is optional (won't fail workflow)
- Check `CODECOV_TOKEN` secret if using Codecov
- Coverage reports still uploaded as artifacts

### Frontend tests timeout

- Increase wait times in workflow if services are slow
- Check that frontend can reach backend API
- Verify environment variables in `app/.env.development`

## Adding New Tests

### Backend (pytest)

1. Add test file in appropriate directory:
   - `site/office/tests/test_*.py`
   - `site/churchcal/tests/test_*.py`
   - `site/bible/tests/test_*.py`

2. Use pytest markers from `pytest.ini`:
   ```python
   @pytest.mark.unit  # Fast, no DB
   @pytest.mark.integration  # Uses DB
   @pytest.mark.us1  # User Story 1
   ```

3. Coverage will automatically include new files

### Frontend (Vitest)

1. Add test file: `app/tests/unit/**/*.spec.js`
2. Follow Vue Test Utils patterns
3. Run locally: `npm run test:unit`

### Frontend (Cypress)

1. Add test file: `app/tests/e2e/specs/**/*.spec.js`
2. Use Cypress best practices
3. Run locally: `npm run test:e2e:open`

## Performance

**Typical run times:**
- Backend tests: 5-10 minutes
- Frontend unit tests: 2-5 minutes
- Frontend E2E tests: 15-30 minutes
- Formatting checks: 2-3 minutes
- Full CI suite (parallel): 15-30 minutes

**Optimization tips:**
- Use workflow caching for Podman images
- Run only affected workflows (path filtering)
- Parallelize independent jobs
- Skip E2E tests on formatting-only changes

## Constitutional Compliance

These workflows enforce Constitution Principle III (Comprehensive Testing):

✅ **Automated test execution** on every push/PR  
✅ **100% function coverage goal** tracked via coverage reports  
✅ **Block merge if tests fail** (required status checks)  
✅ **Test results visible** in PR comments and summaries  
✅ **Coverage trends tracked** over time

To make tests required for merging:
1. Go to repository Settings → Branches
2. Add branch protection rule for `main`
3. Require status checks:
   - `Backend Tests & Coverage / test`
   - `Frontend Tests / unit-tests`
   - `Code Formatting Check / black-formatting`

## Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Compose](https://docs.docker.com/compose/)
- [pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [Cypress Documentation](https://docs.cypress.io/)
- [Black Formatter](https://black.readthedocs.io/)

## Support

For issues with workflows:
1. Check workflow logs in GitHub Actions tab
2. Run equivalent command locally with Docker
3. Verify `docker-compose.yml` is valid
4. Ensure database dump is present and loadable

---

**Last Updated**: November 2025  
**Maintained By**: Daily Office 2019 Development Team
