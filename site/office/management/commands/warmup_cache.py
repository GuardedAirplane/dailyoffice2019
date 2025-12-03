"""
Management command to warm up caches before E2E tests.

This command pre-caches:
1. Church calendar data for specified years
2. API responses for key dates used in E2E tests
3. Optionally generates precompiled JSON files

The cache uses a dual-layer strategy:
- Memcached: Fast in-memory cache (lost on container restart)
- Persistent file cache: Survives restarts, can be loaded into memcached

Usage:
    python manage.py warmup_cache                    # Warm up caches for E2E test dates
    python manage.py warmup_cache --years 2024 2025  # Specific years
    python manage.py warmup_cache --all              # All dates for specified years
    python manage.py warmup_cache --precompile       # Also generate precompiled JSON
    python manage.py warmup_cache --load-persistent  # Load persistent cache into memcached
"""

import os
import sys
import json
import hashlib
import concurrent.futures
from datetime import date, timedelta
from typing import List, Tuple, Optional, Dict, Any

from django.conf import settings
from django.core.cache import cache, caches
from django.core.management.base import BaseCommand
from django.db import connections
from django.test import RequestFactory

from churchcal.calculations import ChurchYear, get_church_year


# Key dates that E2E tests access (from analyzing the test files)
E2E_TEST_DATES = [
    # *** PRIMARY TEST DATE - used by many tests including Compline ***
    (2024, 1, 30),  # Most common test date
    # Morning/Evening Prayer test dates
    (2024, 1, 15),  # Used by date-navigation tests
    (2025, 1, 1),  # Year boundary test (forward from 2024/12/31)
    (2024, 12, 31),  # Year boundary test (backward from 2025/1/1)
    # Month boundary test dates (from date-navigation.spec.ts)
    (2024, 1, 31),  # Month boundary forward test
    (2024, 2, 1),  # Month boundary backward test
    # Family prayer test dates (from family-prayer.spec.ts)
    (2024, 3, 15),  # Family Morning/Evening Prayer
    (2024, 5, 10),  # Family Midday Prayer
    (2024, 6, 20),  # Family Early Evening Prayer - failing test
    (2024, 7, 4),  # Family Close of Day Prayer
    (2024, 8, 15),  # Family Prayer various dates
    (2024, 9, 5),  # Family Prayer content validation
    (2024, 9, 20),  # Family Prayer URL patterns
    # Christmas dates
    (2020, 12, 25),
    (2024, 12, 25),
    (2025, 12, 25),
    (2026, 12, 25),
    (2030, 12, 25),
    # Day after Christmas (St. Stephen's)
    (2024, 12, 26),
    # Christmas Eve
    (2024, 12, 24),
    # Easter dates (movable feast)
    (2024, 3, 31),  # Easter 2024
    (2025, 4, 20),  # Easter 2025
    (2026, 4, 5),  # Easter 2026
    # Week after Easter
    (2024, 4, 7),
    # Epiphany (January 6)
    (2024, 1, 6),
    (2025, 1, 6),
    (2026, 1, 6),
    (2030, 1, 6),
    # Ascension Day (40 days after Easter)
    (2024, 5, 9),  # Ascension 2024
    (2025, 5, 29),  # Ascension 2025
    (2026, 5, 14),  # Ascension 2026
    # Pentecost (50 days after Easter)
    (2024, 5, 19),  # Pentecost 2024
    (2025, 6, 8),  # Pentecost 2025
    # Trinity Sunday (Sunday after Pentecost)
    (2024, 5, 26),
    (2025, 6, 15),
    # All Saints Day (November 1)
    (2023, 11, 1),
    (2024, 11, 1),
    (2025, 11, 1),
    (2030, 11, 1),
    # Ash Wednesday (46 days before Easter)
    (2024, 2, 14),  # Ash Wednesday 2024
    (2025, 3, 5),  # Ash Wednesday 2025
    (2026, 2, 18),  # Ash Wednesday 2026
    # Day before Ash Wednesday
    (2024, 2, 13),
    # Palm Sunday (Sunday before Easter)
    (2024, 3, 24),
    (2025, 4, 13),
    # Good Friday (Friday before Easter)
    (2024, 3, 29),
    (2025, 4, 18),
    # Maundy Thursday
    (2024, 3, 28),
    # Holy Saturday
    (2024, 3, 30),
    # First Sunday of Advent
    (2024, 12, 1),
    # Season After Pentecost
    (2024, 7, 15),
    # New Year's Day
    (2026, 1, 1),
]

# Default number of processes - ALWAYS use 1 for reliability
# ProcessPoolExecutor hangs in Docker containers due to multiprocessing issues
# The sequential approach is fast enough for the ~40 E2E test dates
DEFAULT_PROCESSES = 1

# Cache timeout (12 hours for memcached, 1 year for persistent)
MEMCACHED_TIMEOUT = 60 * 60 * 12
PERSISTENT_TIMEOUT = 60 * 60 * 24 * 365

# Timeout for generating a single office (seconds)
OFFICE_GENERATION_TIMEOUT = 30


class MockRequest:
    """Mock request object for generating office data."""

    def __init__(self, query_params=None):
        self.query_params = query_params or {}
        self.GET = self.query_params


def get_persistent_cache():
    """Get the persistent file-based cache, or None if not configured."""
    try:
        return caches["persistent"]
    except Exception:
        return None


def get_cache_key(office_name: str, year: int, month: int, day: int) -> str:
    """Generate a cache key for an office API response."""
    return f"office_api:{office_name}:{year}-{month:02d}-{day:02d}:default"


def warmup_date(date_tuple: Tuple[int, int, int], verbose: bool = False, persist: bool = True) -> str:
    """
    Warm up cache for a specific date by generating all office types.

    Stores results in both memcached and persistent file cache.
    Returns any error messages, or empty string on success.
    """
    import time

    # Import here to avoid issues with multiprocessing
    from office.api.views.index import (
        MorningPrayer,
        EveningPrayer,
        MiddayPrayer,
        Compline,
        FamilyMorningPrayer,
        FamilyMiddayPrayer,
        FamilyEarlyEveningPrayer,
        FamilyCloseOfDayPrayer,
        OfficeSerializer,
    )

    year, month, day = date_tuple
    errors = []
    date_str = f"{year}-{month:02d}-{day:02d}"

    offices = [
        ("morning_prayer", MorningPrayer),
        ("evening_prayer", EveningPrayer),
        ("midday_prayer", MiddayPrayer),
        ("compline", Compline),
        ("family_morning_prayer", FamilyMorningPrayer),
        ("family_midday_prayer", FamilyMiddayPrayer),
        ("family_early_evening_prayer", FamilyEarlyEveningPrayer),
        ("family_close_of_day_prayer", FamilyCloseOfDayPrayer),
    ]

    request = MockRequest()
    persistent_cache = get_persistent_cache()

    for name, office_class in offices:
        start_time = time.time()
        try:
            if verbose:
                print(f"    → {date_str} {name}...", end="", flush=True)

            # Generate office
            office = office_class(request, year, month, day)

            if verbose:
                print(f" office created ({time.time() - start_time:.1f}s)...", end="", flush=True)

            # Serialize
            serializer = OfficeSerializer(office)
            data = serializer.data

            if verbose:
                print(f" serialized ({time.time() - start_time:.1f}s)...", end="", flush=True)

            # Store in memcached
            cache_key = get_cache_key(name, year, month, day)
            cache.set(cache_key, data, MEMCACHED_TIMEOUT)

            # Store in persistent file cache if available
            if persist and persistent_cache:
                try:
                    persistent_cache.set(cache_key, data, PERSISTENT_TIMEOUT)
                except Exception:
                    pass  # Don't fail if persistent cache has issues

            elapsed = time.time() - start_time
            if verbose:
                print(f" ✓ ({elapsed:.1f}s)", flush=True)

        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = f"Error generating {name} for {date_str}: {e}"
            errors.append(error_msg)
            if verbose:
                print(f" ✗ ({elapsed:.1f}s) {e}", flush=True)

    return "\n".join(errors) if errors else ""


def warmup_calendar_years(years: List[int], stdout, persist: bool = True) -> None:
    """Pre-cache church calendar data for specified years."""
    persistent_cache = get_persistent_cache()

    for year in years:
        stdout.write(f"  Warming up calendar for year {year}...")
        try:
            church_year = ChurchYear(year)
            cache_key = str(year)

            # Store in memcached
            cache.set(cache_key, church_year, MEMCACHED_TIMEOUT)

            # Store in persistent cache
            if persist and persistent_cache:
                try:
                    persistent_cache.set(f"calendar:{cache_key}", church_year, PERSISTENT_TIMEOUT)
                except Exception:
                    pass

            stdout.write(f"    ✓ Church year {year} cached")
        except Exception as e:
            stdout.write(f"    ✗ Failed to cache year {year}: {e}")


def load_persistent_to_memcached(stdout) -> int:
    """
    Load cached data from persistent file cache into memcached.
    Returns the number of items loaded.
    """
    persistent_cache = get_persistent_cache()
    if not persistent_cache:
        stdout.write("  Persistent cache not configured")
        return 0

    loaded = 0
    cache_dir = getattr(settings, "CACHES", {}).get("persistent", {}).get("LOCATION")

    if not cache_dir or not os.path.exists(cache_dir):
        stdout.write(f"  Cache directory not found: {cache_dir}")
        return 0

    stdout.write(f"  Loading from cache directory: {cache_dir}")

    # Load calendar years
    for year in range(2020, 2035):
        cache_key = f"calendar:{year}"
        try:
            data = persistent_cache.get(cache_key)
            if data:
                cache.set(str(year), data, MEMCACHED_TIMEOUT)
                loaded += 1
        except Exception:
            pass

    # Load office data for E2E test dates
    office_names = [
        "morning_prayer",
        "evening_prayer",
        "midday_prayer",
        "compline",
        "family_morning_prayer",
        "family_midday_prayer",
        "family_early_evening_prayer",
        "family_close_of_day_prayer",
    ]

    for date_tuple in E2E_TEST_DATES:
        year, month, day = date_tuple
        for office_name in office_names:
            cache_key = get_cache_key(office_name, year, month, day)
            try:
                data = persistent_cache.get(cache_key)
                if data:
                    cache.set(cache_key, data, MEMCACHED_TIMEOUT)
                    loaded += 1
            except Exception:
                pass

    return loaded


class Command(BaseCommand):
    help = "Warms up caches for E2E tests by pre-generating calendar and office data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--years",
            nargs="+",
            type=int,
            default=None,
            help="Specific years to warm up (default: years used in E2E tests)",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Warm up all dates for specified years (not just E2E test dates)",
        )
        parser.add_argument(
            "--precompile",
            action="store_true",
            help="Also generate precompiled JSON files",
        )
        parser.add_argument(
            "--processes",
            type=int,
            default=DEFAULT_PROCESSES,
            help=f"Number of parallel processes (default: {DEFAULT_PROCESSES} = CPU count)",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Show detailed progress",
        )
        parser.add_argument(
            "--offices-only",
            action="store_true",
            help="Skip calendar warmup, only warm up office endpoints",
        )
        parser.add_argument(
            "--calendar-only",
            action="store_true",
            help="Only warm up calendar cache, skip office endpoints",
        )
        parser.add_argument(
            "--load-persistent",
            action="store_true",
            help="Load data from persistent file cache into memcached (fast startup)",
        )
        parser.add_argument(
            "--no-persist",
            action="store_true",
            help="Don't save to persistent file cache (only use memcached)",
        )

    def handle(self, *args, **options):
        verbose = options["verbose"]
        processes = options["processes"]
        offices_only = options["offices_only"]
        calendar_only = options["calendar_only"]
        all_dates = options["all"]
        precompile = options["precompile"]
        load_persistent = options["load_persistent"]
        persist = not options["no_persist"]

        # Ensure cache directory exists for persistent cache
        cache_config = getattr(settings, "CACHES", {}).get("persistent", {})
        cache_dir = cache_config.get("LOCATION") if cache_config else None
        if cache_dir and not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
            self.stdout.write(f"Created cache directory: {cache_dir}")

        # If --load-persistent, try to load from file cache first
        if load_persistent:
            self.stdout.write("\n💾 Loading from persistent cache...")
            loaded = load_persistent_to_memcached(self.stdout)
            if loaded > 0:
                self.stdout.write(self.style.SUCCESS(f"  Loaded {loaded} items from persistent cache"))
                self.stdout.write(self.style.SUCCESS("\n✅ Cache loaded from persistent storage!"))
                return
            else:
                self.stdout.write("  No persistent cache data found, will generate fresh cache")

        # Determine which years to warm up
        if options["years"]:
            years = options["years"]
        else:
            # Extract unique years from E2E test dates
            years = sorted(set(d[0] for d in E2E_TEST_DATES))

        self.stdout.write(self.style.SUCCESS(f"Cache warmup starting for years: {years}"))
        self.stdout.write(f"  Using {processes} parallel processes")
        if persist and cache_dir:
            self.stdout.write(f"  Persistent cache: {cache_dir}")

        # Step 1: Warm up calendar cache
        if not offices_only:
            self.stdout.write("\n📅 Warming up church calendar cache...")
            warmup_calendar_years(years, self.stdout, persist=persist)

        if calendar_only:
            self.stdout.write(self.style.SUCCESS("\n✅ Calendar cache warmup complete!"))
            return

        # Step 2: Determine which dates to warm up
        if all_dates:
            # Generate all dates for the specified years
            dates_to_warmup = []
            for year in years:
                start_date = date(year, 1, 1)
                end_date = date(year, 12, 31)
                current = start_date
                while current <= end_date:
                    dates_to_warmup.append((current.year, current.month, current.day))
                    current += timedelta(days=1)
        else:
            # Use E2E test dates only
            dates_to_warmup = [d for d in E2E_TEST_DATES if d[0] in years]

        self.stdout.write(f"\n📄 Warming up {len(dates_to_warmup)} dates with {processes} processes...")
        sys.stdout.flush()

        # Step 3: Warm up office endpoints
        if processes > 1 and len(dates_to_warmup) > 10:
            # Use parallel processing for large date sets
            # Note: This can hang in Docker - prefer processes=1 for reliability

            # Close DB connections before forking
            connections.close_all()

            try:
                with concurrent.futures.ProcessPoolExecutor(max_workers=processes) as executor:
                    # Submit all tasks
                    future_to_date = {executor.submit(warmup_date, d, verbose, persist): d for d in dates_to_warmup}

                    completed = 0
                    errors = []
                    # Use timeout to prevent hanging
                    for future in concurrent.futures.as_completed(future_to_date, timeout=300):
                        completed += 1
                        date_tuple = future_to_date[future]
                        try:
                            error = future.result(timeout=OFFICE_GENERATION_TIMEOUT)
                            if error:
                                errors.append(error)
                        except concurrent.futures.TimeoutError:
                            errors.append(f"Timeout for {date_tuple}")
                        except Exception as e:
                            errors.append(f"Exception for {date_tuple}: {e}")

                        if completed % 10 == 0 or completed == len(dates_to_warmup):
                            self.stdout.write(f"  Progress: {completed}/{len(dates_to_warmup)}")
                            sys.stdout.flush()

                    if errors:
                        self.stdout.write(self.style.WARNING(f"\n⚠️  {len(errors)} errors occurred:"))
                        for error in errors[:5]:  # Show first 5 errors
                            self.stdout.write(f"    {error}")
                        if len(errors) > 5:
                            self.stdout.write(f"    ... and {len(errors) - 5} more")
            except concurrent.futures.TimeoutError:
                self.stdout.write(self.style.WARNING("\n⚠️  Parallel processing timed out, falling back to sequential"))
                # Fall through to sequential processing
                processes = 1

        if processes == 1:
            # Sequential processing - more reliable in Docker
            errors = []
            for i, date_tuple in enumerate(dates_to_warmup, 1):
                year, month, day = date_tuple
                if verbose:
                    self.stdout.write(f"  [{i}/{len(dates_to_warmup)}] {year}-{month:02d}-{day:02d}")
                    sys.stdout.flush()
                error = warmup_date(date_tuple, verbose=verbose, persist=persist)
                if error:
                    errors.append(error)
                if not verbose and i % 5 == 0:
                    self.stdout.write(f"  Progress: {i}/{len(dates_to_warmup)}")
                    sys.stdout.flush()

            if errors:
                self.stdout.write(self.style.WARNING(f"\n⚠️  {len(errors)} errors occurred"))

        # Step 4: Optionally generate precompiled JSON
        if precompile:
            self.stdout.write("\n📁 Generating precompiled JSON files...")
            from django.core.management import call_command

            for year in years:
                self.stdout.write(f"  Precompiling year {year}...")
                try:
                    call_command("precompile_offices", year, processes=processes)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"    Failed: {e}"))

        self.stdout.write(self.style.SUCCESS("\n✅ Cache warmup complete!"))
        if persist and cache_dir:
            self.stdout.write(self.style.SUCCESS(f"  Data persisted to: {cache_dir}"))
            self.stdout.write("  Next time, use --load-persistent for faster startup")
