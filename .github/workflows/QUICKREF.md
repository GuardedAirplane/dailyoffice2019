# GitHub Actions Quick Reference

## 🚀 Running Tests Locally (Mimicking CI)

### Backend Tests
```bash
# Start services
docker-compose up -d db cache backend

# Wait for DB to be ready
until docker exec dailyoffice2019_db_1 pg_isready -U dailyoffice; do sleep 2; done

# Load database dump (if not already loaded)
unzip -p site/dailyoffice_2024_01_30.sql.zip dailyoffice_2024_01_30.sql | \
  docker exec -i dailyoffice2019_db_1 psql -U dailyoffice dailyoffice

# Run Django system check
docker exec dailyoffice2019_backend_1 python manage.py check

# Run tests with coverage
docker exec dailyoffice2019_backend_1 python -m pytest \
  --cov=office --cov=churchcal --cov=bible --cov=psalter \
  --cov-report=html --cov-report=term-missing

# View coverage report
# Open site/htmlcov/index.html in browser

# Cleanup
docker-compose down -v
```

### Frontend Unit Tests
```bash
# Start frontend
docker-compose up -d frontend

# Wait for npm install
sleep 30

# Run tests
docker exec dailyoffice2019_frontend_1 npm run test:unit

# Cleanup
docker-compose down -v
```

### Frontend E2E Tests
```bash
# Start all services
docker-compose up -d

# Wait for services
sleep 60

# Load database
unzip -p site/dailyoffice_2024_01_30.sql.zip dailyoffice_2024_01_30.sql | \
  docker exec -i dailyoffice2019_db_1 psql -U dailyoffice dailyoffice

# Run E2E tests
docker exec dailyoffice2019_frontend_1 npm run test:e2e

# Cleanup
docker-compose down -v
```

### Python Formatting
```bash
# Start backend
docker-compose up -d backend

# Check formatting
docker exec dailyoffice2019_backend_1 \
  find . -iname "*.py" -not -path "*/migrations/*" -not -path "*/__pycache__/*" | \
  xargs black --check --target-version=py313 --line-length=119

# Apply formatting
docker exec dailyoffice2019_backend_1 \
  find . -iname "*.py" -not -path "*/migrations/*" -not -path "*/__pycache__/*" | \
  xargs black --target-version=py313 --line-length=119

# Cleanup
docker-compose down -v
```

### JavaScript Linting
```bash
# Start frontend
docker-compose up -d frontend

# Wait for npm install
sleep 30

# Run ESLint
docker exec dailyoffice2019_frontend_1 npm run lint

# Cleanup
docker-compose down -v
```

## 📊 Workflow Status Badges

Add these to your README.md:

```markdown
![Backend Tests](https://github.com/GuardedAirplane/dailyoffice2019/workflows/Backend%20Tests/badge.svg)
![Frontend Tests](https://github.com/GuardedAirplane/dailyoffice2019/workflows/Frontend%20Tests/badge.svg)
![Code Formatting](https://github.com/GuardedAirplane/dailyoffice2019/workflows/Code%20Formatting%20%26%20Linting/badge.svg)
![CI](https://github.com/GuardedAirplane/dailyoffice2019/workflows/CI%20-%20Full%20Test%20Suite/badge.svg)
```

## 🔧 Troubleshooting Common Issues

### Issue: "Container not found"
**Solution:** Check container names match docker-compose.yml:
```bash
docker ps -a | grep dailyoffice
```

### Issue: "Database connection failed"
**Solution:** Ensure PostgreSQL is ready:
```bash
docker exec dailyoffice2019_db_1 pg_isready -U dailyoffice
```

### Issue: "npm install fails in frontend"
**Solution:** Requires FontAwesome Pro authentication. See main README for setup.

### Issue: "Tests pass locally but fail in CI"
**Solution:** 
1. Rebuild containers: `docker-compose build --no-cache`
2. Verify database dump exists: `ls -lh site/dailyoffice_2024_01_30.sql.zip`
3. Check environment variables match between local and CI

### Issue: "Coverage report not generated"
**Solution:**
1. Ensure pytest runs successfully
2. Check for coverage.xml in site/ directory after test run
3. Verify coverage packages installed: `docker exec dailyoffice2019_backend_1 pip list | grep cov`

## 📦 Artifacts & Reports

After each CI run, the following artifacts are available:

### Backend Tests
- `coverage.xml` - Coverage data for Codecov
- `pytest-results.xml` - Test results in JUnit format
- `htmlcov/` - HTML coverage report (browse index.html)

### Frontend Unit Tests
- `frontend-coverage/` - Vitest coverage report

### Frontend E2E Tests
- `cypress-videos/` - Screen recordings of test runs
- `cypress-screenshots/` - Screenshots of failures

**Download from:** GitHub Actions → Workflow run → Artifacts section

## 🎯 Pre-commit Checklist

Before pushing code, run locally:

```bash
# 1. Format Python code
find site -iname "*.py" -not -path "*/migrations/*" | \
  xargs black --target-version=py313 --line-length=119

# 2. Run backend tests
cd site && python -m pytest --cov --cov-report=term-missing

# 3. Run frontend tests (if changed)
cd app && npm run test:unit

# 4. Run linter (if JS/Vue changed)
cd app && npm run lint

# 5. Verify Django checks
cd site && python manage.py check
```

Or use pre-commit hooks:
```bash
pre-commit run --all-files
```

## 📝 Adding New Workflows

1. Create new YAML file in `.github/workflows/`
2. Use existing workflows as template
3. Test locally first with Docker
4. Add documentation to this README
5. Add status badge to main README

## 🔐 Required Secrets

Configure in GitHub: Settings → Secrets and variables → Actions

| Secret | Required? | Purpose |
|--------|-----------|---------|
| `CODECOV_TOKEN` | Optional | Upload coverage to Codecov.io |
| `GITHUB_TOKEN` | Auto | GitHub API access (auto-provided) |

## 🚦 Branch Protection

Recommended settings for `main` branch:

1. **Require status checks before merging:**
   - `Backend Tests & Coverage / test`
   - `Frontend Tests / unit-tests`  
   - `Code Formatting Check / black-formatting`

2. **Require branches to be up to date**

3. **Require linear history**

4. **Block force pushes**

## 📈 Coverage Requirements

Per Constitution Principle III:

| Priority | Coverage Required | Components |
|----------|------------------|------------|
| P0 (Critical) | 100% | Morning Prayer, Evening Prayer, core office generation |
| P1 (High) | 90% | Midday Prayer, Compline, Family Prayer |
| P2 (Medium) | 80% | Settings, utilities, helpers |

Track in `.github/copilot-instructions.md` → Test Coverage Status section.

## ⚡ Performance Targets

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Office generation | < 500ms | 700-800ms | ⚠️ Needs optimization |
| Page load time (SC-001) | < 3 seconds | ~2 seconds | ✅ Pass |
| Backend tests | < 10 min | ~5-7 min | ✅ Pass |
| Frontend unit tests | < 5 min | ~2-3 min | ✅ Pass |
| Full CI suite | < 30 min | ~20-25 min | ✅ Pass |

---

**Quick Access Links:**
- [Workflows Directory](./)
- [Workflow README](./README.md)
- [Main Project README](../../README.md)
- [Test Coverage Status](../ copilot-instructions.md#test-coverage-status)
