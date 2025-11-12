"""
Pytest configuration for Daily Office tests.

Loads production database data (data-only dump) for realistic testing environment.
The Daily Office requires extensive calendar data to function properly.

## Database Fixture Strategy

This conftest provides production database fixtures for integration testing. The fixture
loads real liturgical calendar data to ensure tests validate against complete, realistic data.

### When to Use Production Fixtures (default)

**Integration Tests** - Use standard `pytest.mark.django_db` for tests that:
- Validate office generation with real calendar dates
- Test cross-module integration (calendar + readings + collects)
- Require complete liturgical data (seasons, commemorations, lectionary)
- Test realistic scenarios users will encounter

Example:
```python
@pytest.mark.django_db
class TestMorningPrayerIntegration:
    def test_epiphany_office(self, client):
        # Uses production data - Epiphany exists in database
        response = client.get("/api/v1/office/morning_prayer/2024-1-6")
        assert response.status_code == 200
```

### When to Use Clean Database (TransactionTestCase)

**Unit Tests** - Use `TransactionTestCase` for tests that:
- Test model creation/validation in isolation
- Need predictable, controlled test data
- Would fail with production data interference
- Test edge cases not in production data

Example:
```python
from django.test import TransactionTestCase

class TestCollectModel(TransactionTestCase):
    def setUp(self):
        # Clean database - create only what you need
        self.collect_type = CollectType.objects.create(name="Test", key="test")
    
    def test_collect_creation(self):
        collect = Collect.objects.create(
            title="Test Collect",
            text="<p>Test text</p>",
            collect_type=self.collect_type
        )
        assert collect.title == "Test Collect"
```

### Database Fixture Implementation Notes

- **Production Data**: Loaded once per test session from `dailyoffice_data_only.sql`
- **Clean Data**: `TransactionTestCase` bypasses fixture, provides clean DB per test
- **Skip Pattern**: Tests requiring clean DB should use `@pytest.mark.skip` if data conflicts

For more details, see:
- `.github/copilot-instructions.md` - Test Coverage Status section
- `docs/testing/phase_21_polish_and_cross_cutting.md` - Database fixture strategy
"""

import pytest
import subprocess
import os


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Load production database data into test database.

    The Daily Office requires a complete liturgical calendar to function:
    - Denominations, Calendars, and Commemoration Ranks
    - Seasons and Commemorations (both fixed and movable)
    - Office readings (StandardOfficeDay, HolyDayOfficeDay)
    - Psalter data
    - Collects and other liturgical texts

    We import from a data-only production database dump to ensure tests run
    against realistic, complete data without schema conflicts.

    The dump is imported AFTER Django migrations create the schema, ensuring
    compatibility with the current codebase.

    Unit tests that need a clean database should use Django's TransactionTestCase
    instead of TestCase to bypass this fixture.
    """
    with django_db_blocker.unblock():
        from django.conf import settings
        from django.db import connection

        # Get the actual test database name from the connection
        test_db_name = connection.settings_dict["NAME"]
        db_settings = settings.DATABASES["default"]

        # Use data-only dump (no schema, only data)
        # Try workspace path (Docker) first, then relative path (CI/local)
        data_dump_paths = [
            "/workspace/site/dailyoffice_data_only.sql",  # Docker container
            os.path.join(os.path.dirname(__file__), "dailyoffice_data_only.sql"),  # CI/local relative
        ]
        
        data_dump = None
        for path in data_dump_paths:
            if os.path.exists(path):
                data_dump = path
                break

        if data_dump and os.path.exists(data_dump):
            env = os.environ.copy()
            env["PGPASSWORD"] = db_settings["PASSWORD"]

            print(f"\n{'='*60}")
            print(f"Loading production data into test database")
            print(f"Data dump: {data_dump}")
            print(f"Target database: {test_db_name}")
            print(f"{'='*60}\n")

            # Create a temporary SQL file that disables triggers, loads data, then re-enables
            import tempfile

            with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as tmp:
                tmp.write("-- Disable triggers to handle circular FK constraints\n")
                tmp.write("SET session_replication_role = replica;\n\n")

                # Read and write the data dump
                with open(data_dump, "r") as f:
                    tmp.write(f.read())

                tmp.write("\n\n-- Re-enable triggers\n")
                tmp.write("SET session_replication_role = DEFAULT;\n")
                tmp_sql_file = tmp.name

            try:
                # Import using psql
                result = subprocess.run(
                    [
                        "psql",
                        "-h",
                        db_settings["HOST"],
                        "-p",
                        str(db_settings["PORT"]),
                        "-U",
                        db_settings["USER"],
                        "-d",
                        test_db_name,
                        "-f",
                        tmp_sql_file,
                        "-v",
                        "ON_ERROR_STOP=0",  # Continue on errors
                        "--quiet",  # Suppress output of INSERT statements
                    ],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minute timeout for large dump
                )

                if result.returncode == 0:
                    print("✓ Database data loaded successfully")
                else:
                    print(f"⚠ Database import completed with return code: {result.returncode}")
                    if result.stderr:
                        # Show only errors, not all the INSERT statements
                        errors = [line for line in result.stderr.split("\n") if "ERROR" in line or "FATAL" in line]
                        if errors:
                            print(f"Errors (first 5):")
                            for error in errors[:5]:
                                print(f"  {error}")
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_sql_file):
                    os.unlink(tmp_sql_file)
        else:
            print(f"\n⚠ Warning: Data dump not found")
            print(f"Searched paths:")
            for path in data_dump_paths:
                print(f"  - {path}")
            print("Assuming database is already loaded (e.g., in CI workflow)")
            print("If tests fail, check that database was loaded before pytest ran")
            print("    site/dailyoffice_data_only.sql\n")


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Enable database access for all tests automatically.

    This fixture is automatically used by all tests, so individual tests
    don't need to explicitly request the 'db' fixture.
    """
    pass


@pytest.fixture
def mock_url_reverse(monkeypatch):
    """
    Mock django.urls.reverse for navigation tests.

    Daily Office is a SPA - URL routing is handled by Vue.js frontend.
    Tests should validate navigation data structure without requiring
    Django URL configuration.

    Returns a function that generates mock URLs in the expected format:
    /<office_type>/<year>-<month>-<day>/
    """

    def mock_reverse(view_name, args=None, kwargs=None):
        """Generate mock URL for office type and date."""
        if args and len(args) == 3:
            year, month, day = args
            return f"/{view_name}/{year}-{month}-{day}/"
        return f"/{view_name}/"

    # Patch reverse in both django.urls and office.offices module
    monkeypatch.setattr("django.urls.reverse", mock_reverse)
    monkeypatch.setattr("office.offices.reverse", mock_reverse)

    return mock_reverse
