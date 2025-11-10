"""
Pytest configuration for Daily Office tests.

Loads production database data (data-only dump) for realistic testing environment.
The Daily Office requires extensive calendar data to function properly.
"""

import pytest
import subprocess
import os


@pytest.fixture(scope='session')
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
    """
    with django_db_blocker.unblock():
        from django.conf import settings
        from django.db import connection
        
        # Get the actual test database name from the connection
        test_db_name = connection.settings_dict['NAME']
        db_settings = settings.DATABASES['default']
        
        # Use data-only dump (no schema, only data)
        data_dump = '/workspace/site/dailyoffice_data_only.sql'
        
        if os.path.exists(data_dump):
            env = os.environ.copy()
            env['PGPASSWORD'] = db_settings['PASSWORD']
            
            print(f"\n{'='*60}")
            print(f"Loading production data into test database")
            print(f"Data dump: {data_dump}")
            print(f"Target database: {test_db_name}")
            print(f"{'='*60}\n")
            
            # Create a temporary SQL file that disables triggers, loads data, then re-enables
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as tmp:
                tmp.write("-- Disable triggers to handle circular FK constraints\n")
                tmp.write("SET session_replication_role = replica;\n\n")
                
                # Read and write the data dump
                with open(data_dump, 'r') as f:
                    tmp.write(f.read())
                
                tmp.write("\n\n-- Re-enable triggers\n")
                tmp.write("SET session_replication_role = DEFAULT;\n")
                tmp_sql_file = tmp.name
            
            try:
                # Import using psql
                result = subprocess.run(
                    [
                        'psql',
                        '-h', db_settings['HOST'],
                        '-p', str(db_settings['PORT']),
                        '-U', db_settings['USER'],
                        '-d', test_db_name,
                        '-f', tmp_sql_file,
                        '-v', 'ON_ERROR_STOP=0',  # Continue on errors
                        '--quiet',  # Suppress output of INSERT statements
                    ],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout for large dump
                )
                
                if result.returncode == 0:
                    print("✓ Database data loaded successfully")
                else:
                    print(f"⚠ Database import completed with return code: {result.returncode}")
                    if result.stderr:
                        # Show only errors, not all the INSERT statements
                        errors = [line for line in result.stderr.split('\n') if 'ERROR' in line or 'FATAL' in line]
                        if errors:
                            print(f"Errors (first 5):")
                            for error in errors[:5]:
                                print(f"  {error}")
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_sql_file):
                    os.unlink(tmp_sql_file)
        else:
            print(f"\n⚠ Warning: Data dump not found at {data_dump}")
            print("Tests will run with empty database - some tests may fail")
            print("To create the dump, run:")
            print("  podman exec dailyoffice2019_db_1 pg_dump -U dailyoffice -d dailyoffice \\")
            print("    --data-only --inserts --column-inserts -f /tmp/dailyoffice_data_only.sql")
            print("  podman cp dailyoffice2019_db_1:/tmp/dailyoffice_data_only.sql \\")
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
    monkeypatch.setattr('django.urls.reverse', mock_reverse)
    monkeypatch.setattr('office.offices.reverse', mock_reverse)
    
    return mock_reverse
