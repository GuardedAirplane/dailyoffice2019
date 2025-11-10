# Code Coverage Configuration

This document describes the code coverage requirements and reporting setup for the Daily Office project, implementing Constitution Principle III.

## Coverage Requirements

Per the Constitution, coverage requirements are based on priority levels:

- **P0 (Critical)**: 100% function coverage required
- **P1 (High)**: 90% function coverage required
- **P2 (Medium)**: 80% function coverage required

## Backend Coverage (pytest-cov)

### Configuration

Coverage is configured in `pytest.ini`:

```ini
[coverage:run]
source = office,churchcal,bible,psalter
omit =
    */migrations/*
    */tests/*
    */test_*.py
    */__pycache__/*

[coverage:report]
precision = 2
skip_covered = False
skip_empty = True
sort = Cover
```

### Running Coverage Reports

```bash
# Run tests with coverage
cd site
pytest --cov --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html

# Check specific module coverage
pytest --cov=office.morning_prayer --cov-report=term

# Fail if coverage below threshold
pytest --cov --cov-fail-under=90
```

### Coverage Targets

| Module | Target | Priority | Status |
|--------|--------|----------|--------|
| office.morning_prayer | 100% | P0 | 🔴 Not Started |
| office.evening_prayer | 100% | P1 | 🔴 Not Started |
| office.midday_prayer | 90% | P2 | 🔴 Not Started |
| office.compline | 90% | P2 | 🔴 Not Started |
| churchcal.calculations | 100% | P0 | 🔴 Not Started |
| bible.passage | 90% | P1 | 🔴 Not Started |
| office.models | 80% | P2 | 🔴 Not Started |

## Frontend Coverage (Vitest)

### Configuration

Coverage is configured in `vitest.config.ts`:

```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '*.config.*',
      ],
    },
  },
});
```

### Running Coverage Reports

```bash
# Run tests with coverage
cd app
npm run test:unit -- --coverage

# View HTML report
open coverage/index.html
```

## CI/CD Integration

Coverage is automatically checked on every pull request via GitHub Actions:

1. **Backend Tests**: Run pytest with coverage, upload to Codecov
2. **Frontend Tests**: Run Vitest with coverage, upload to Codecov
3. **PR Comments**: Codecov bot comments on PR with coverage changes
4. **Merge Blocking**: PR cannot be merged if coverage drops

### Branch Protection Rules

Configure in GitHub repository settings:

- Require status checks to pass before merging
- Require "backend-tests" check
- Require "frontend-tests" check
- Require "lint" check

## Codecov Configuration

Create `.codecov.yml` in repository root:

```yaml
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 1%
    patch:
      default:
        target: 90%
```

## Viewing Coverage Locally

### Backend (HTML Report)

```bash
cd site
pytest --cov --cov-report=html
open htmlcov/index.html
```

### Frontend (HTML Report)

```bash
cd app
npm run test:unit -- --coverage
open coverage/index.html
```

## Coverage Badges

Add coverage badges to README.md:

```markdown
[![Backend Coverage](https://codecov.io/gh/your-org/dailyoffice2019/branch/main/graph/badge.svg?flag=backend)](https://codecov.io/gh/your-org/dailyoffice2019)
[![Frontend Coverage](https://codecov.io/gh/your-org/dailyoffice2019/branch/main/graph/badge.svg?flag=frontend)](https://codecov.io/gh/your-org/dailyoffice2019)
```

## Troubleshooting

### Coverage not generated

**Problem**: `coverage.xml` file not created

**Solution**: Ensure `pytest-cov` is installed:

```bash
pip install pytest-cov
```

### Coverage report shows 0%

**Problem**: Source code not in coverage scope

**Solution**: Check `source` setting in `pytest.ini` matches your module paths

### Tests pass but coverage fails CI

**Problem**: Coverage dropped below threshold

**Solution**: Add tests to cover uncovered lines or adjust threshold temporarily

## Maintenance

### Updating Coverage Thresholds

As test coverage improves, gradually increase thresholds:

1. Check current coverage: `pytest --cov --cov-report=term`
2. Update `--cov-fail-under` in pytest.ini
3. Update GitHub Actions workflow threshold
4. Update this document

### Excluding Code from Coverage

Add `# pragma: no cover` to exclude specific lines:

```python
def debug_only_function():  # pragma: no cover
    """Only used during development."""
    pass
```

Add patterns to `exclude_lines` in pytest.ini for broader exclusions.
