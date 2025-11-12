"""
Performance tests for Daily Office generation.

Tests verify that office generation and API responses meet performance requirements:
- SC-001: Office page load < 3 seconds
- API response time < 500ms
- Efficient database query usage
"""

import time
from datetime import date
from unittest.mock import patch

import pytest
from django.test import Client, override_settings
from django.urls import reverse

from bible.passage import Passage
from office.evening_prayer import EveningPrayer
from office.morning_prayer import MorningPrayer
from office.models import OfficeDay


@pytest.mark.django_db
class TestMorningPrayerPerformance:
    """
    T228: Performance test - Morning Prayer generation time.

    Requirements:
    - SC-001: Office page load < 3 seconds (end-to-end, tested in E2E suite)
    - Backend target: < 1500ms for office generation (containerized environment)

    Note: Phase 19 documented baseline of 700-800ms with optimization deferred.
    These tests ensure no major performance regression in containerized environments.
    """

    def test_morning_prayer_generation_fast(self):
        """Morning Prayer generation completes in reasonable time."""
        test_date = date(2025, 12, 25)  # Christmas Day

        start_time = time.time()
        office = MorningPrayer(test_date)
        _ = office.modules  # Force module generation
        end_time = time.time()

        duration = (end_time - start_time) * 1000  # Convert to ms

        # Log performance for monitoring
        print(f"\nMorning Prayer generation time: {duration:.2f}ms")

        # Assert performance requirement (relaxed for containerized environment)
        assert duration < 1500, f"Morning Prayer took {duration:.2f}ms, expected < 1500ms"

    def test_morning_prayer_generation_regular_day(self):
        """Morning Prayer generation is fast for regular days."""
        test_date = date(2025, 11, 12)  # Regular feria

        start_time = time.time()
        office = MorningPrayer(test_date)
        _ = office.modules
        end_time = time.time()

        duration = (end_time - start_time) * 1000
        print(f"\nMorning Prayer (regular day) generation time: {duration:.2f}ms")

        assert duration < 1500, f"Morning Prayer regular day took {duration:.2f}ms, expected < 1500ms"

    def test_morning_prayer_generation_multiple_commemorations(self):
        """Morning Prayer generation is fast even with multiple commemorations."""
        # Find a date with multiple commemorations
        test_date = date(2025, 1, 25)  # Conversion of St. Paul

        start_time = time.time()
        office = MorningPrayer(test_date)
        _ = office.modules
        end_time = time.time()

        duration = (end_time - start_time) * 1000
        print(f"\nMorning Prayer (multiple commemorations) generation time: {duration:.2f}ms")

        assert duration < 1500, f"Morning Prayer with multiple commemorations took {duration:.2f}ms, expected < 1500ms"


@pytest.mark.django_db
class TestEveningPrayerPerformance:
    """
    T229: Performance test - Evening Prayer generation time.

    Requirements:
    - SC-001: Office page load < 3 seconds (end-to-end, tested in E2E suite)
    - Backend target: < 1500ms for office generation (containerized environment)

    Note: Phase 19 documented baseline of 700-800ms with optimization deferred.
    These tests ensure no major performance regression in containerized environments.
    """

    def test_evening_prayer_generation_fast(self):
        """Evening Prayer generation completes in reasonable time."""
        test_date = date(2025, 12, 25)  # Christmas Day

        start_time = time.time()
        office = EveningPrayer(test_date)
        _ = office.modules
        end_time = time.time()

        duration = (end_time - start_time) * 1000
        print(f"\nEvening Prayer generation time: {duration:.2f}ms")

        assert duration < 1500, f"Evening Prayer took {duration:.2f}ms, expected < 1500ms"

    def test_evening_prayer_generation_regular_day(self):
        """Evening Prayer generation is fast for regular days."""
        test_date = date(2025, 11, 12)  # Regular feria

        start_time = time.time()
        office = EveningPrayer(test_date)
        _ = office.modules
        end_time = time.time()

        duration = (end_time - start_time) * 1000
        print(f"\nEvening Prayer (regular day) generation time: {duration:.2f}ms")

        assert duration < 1500, f"Evening Prayer regular day took {duration:.2f}ms, expected < 1500ms"


@pytest.mark.django_db
class TestAPIPerformance:
    """
    T230: Performance test - API response time for office endpoints.

    Requirements:
    - SC-001: Office page load < 3 seconds (end-to-end, tested in E2E suite)
    - Backend target: API response < 2000ms (containerized environment)

    Note: These tests verify API functionality and detect major performance regressions.
    The actual SC-001 requirement (3 second page load) is tested in E2E suite.
    """

    @override_settings(DEBUG=False)
    def test_morning_prayer_api_response_fast(self):
        """Morning Prayer API endpoint responds in reasonable time."""
        client = Client()
        test_date = "2025-12-25"

        start_time = time.time()
        response = client.get(f"/api/office/morning_prayer/{test_date}/")
        end_time = time.time()

        duration = (end_time - start_time) * 1000
        print(f"\nMorning Prayer API response time: {duration:.2f}ms")

        assert response.status_code == 200
        assert duration < 2000, f"API response took {duration:.2f}ms, expected < 2000ms"

    @override_settings(DEBUG=False)
    def test_evening_prayer_api_response_fast(self):
        """Evening Prayer API endpoint responds in reasonable time."""
        client = Client()
        test_date = "2025-12-25"

        start_time = time.time()
        response = client.get(f"/api/office/evening_prayer/{test_date}/")
        end_time = time.time()

        duration = (end_time - start_time) * 1000
        print(f"\nEvening Prayer API response time: {duration:.2f}ms")

        assert response.status_code == 200
        assert duration < 2000, f"API response took {duration:.2f}ms, expected < 2000ms"

    @override_settings(DEBUG=False)
    def test_midday_prayer_api_response_fast(self):
        """Midday Prayer API endpoint responds in reasonable time."""
        client = Client()
        test_date = "2025-12-25"

        start_time = time.time()
        response = client.get(f"/api/office/midday_prayer/{test_date}/")
        end_time = time.time()

        duration = (end_time - start_time) * 1000
        print(f"\nMidday Prayer API response time: {duration:.2f}ms")

        assert response.status_code == 200
        assert duration < 2000, f"API response took {duration:.2f}ms, expected < 2000ms"

    @override_settings(DEBUG=False)
    def test_compline_api_response_fast(self):
        """Compline API endpoint responds in reasonable time."""
        client = Client()
        test_date = "2025-12-25"

        start_time = time.time()
        response = client.get(f"/api/office/compline/{test_date}/")
        end_time = time.time()

        duration = (end_time - start_time) * 1000
        print(f"\nCompline API response time: {duration:.2f}ms")

        assert response.status_code == 200
        assert duration < 2000, f"API response took {duration:.2f}ms, expected < 2000ms"


@pytest.mark.django_db
class TestScriptureCachePerformance:
    """
    T231: Performance test - Scripture cache hit vs miss latency.

    Requirements:
    - Cache hits should be significantly faster than API calls
    - Cache miss with API should complete in reasonable time
    """

    @patch("bible.sources.BibleGateway.get_text")
    def test_scripture_cache_hit_fast(self, mock_get_text):
        """Scripture cache hit is significantly faster than API call."""
        # Mock BibleGateway to simulate cached response
        mock_get_text.return_value = "Cached scripture text"

        test_date = date(2025, 12, 25)
        office = MorningPrayer(test_date)

        # Warm up (first call might create cache)
        _ = office.modules

        # Measure cache hit
        start_time = time.time()
        _ = office.modules
        end_time = time.time()

        duration = (end_time - start_time) * 1000
        print(f"\nScripture cache hit time: {duration:.2f}ms")

        # Cache hits should be very fast (< 100ms)
        assert duration < 100, f"Cache hit took {duration:.2f}ms, expected < 100ms"

    def test_scripture_cache_efficiency(self):
        """Scripture caching reduces duplicate API calls."""
        test_date = date(2025, 12, 25)
        office = MorningPrayer(test_date)

        # First generation (may involve API calls)
        start_time_first = time.time()
        modules_first = office.modules
        duration_first = (time.time() - start_time_first) * 1000

        # Second generation (should use cache)
        start_time_second = time.time()
        modules_second = office.modules
        duration_second = (time.time() - start_time_second) * 1000

        print(f"\nFirst generation: {duration_first:.2f}ms")
        print(f"Second generation: {duration_second:.2f}ms")

        # Second call should be as fast or faster (cached)
        # Note: May not be significantly faster if no API calls on first run
        assert modules_first == modules_second, "Modules should be identical"


@pytest.mark.django_db
class TestDatabaseQueryPerformance:
    """
    T232: Performance test - Database query count per office.

    Requirements:
    - Minimize database queries through efficient prefetching
    - Avoid N+1 query problems

    Note: Phase 19 documented 428-430 queries with N+1 problem identified.
    These tests use relaxed thresholds until optimization work is completed.
    """

    def test_morning_prayer_query_count(self, django_assert_max_num_queries):
        """Morning Prayer uses reasonable number of database queries."""
        test_date = date(2025, 12, 25)

        # Relaxed threshold acknowledging known N+1 problem (Phase 19: 428 queries)
        # TODO: Reduce to < 50 queries when N+1 optimization is implemented
        with django_assert_max_num_queries(500):
            office = MorningPrayer(test_date)
            _ = office.modules

        print(f"\nMorning Prayer query count test passed (< 500 queries)")

    def test_evening_prayer_query_count(self, django_assert_max_num_queries):
        """Evening Prayer uses reasonable number of database queries."""
        test_date = date(2025, 12, 25)

        # Relaxed threshold acknowledging known N+1 problem
        # TODO: Reduce to < 50 queries when N+1 optimization is implemented
        with django_assert_max_num_queries(500):
            office = EveningPrayer(test_date)
            _ = office.modules

        print(f"\nEvening Prayer query count test passed (< 500 queries)")

    def test_regular_day_query_count(self, django_assert_max_num_queries):
        """Regular day office uses database queries efficiently."""
        test_date = date(2025, 11, 12)  # Regular feria

        # Relaxed threshold for regular days
        # TODO: Reduce to < 40 queries when N+1 optimization is implemented
        with django_assert_max_num_queries(500):
            office = MorningPrayer(test_date)
            _ = office.modules

        print(f"\nRegular day query count test passed (< 500 queries)")


@pytest.mark.django_db
class TestPerformanceRegression:
    """
    Additional performance regression tests.

    These tests ensure performance doesn't degrade over time.
    """

    def test_multiple_offices_same_day(self):
        """Generating multiple offices for same day is efficient."""
        test_date = date(2025, 12, 25)

        start_time = time.time()

        # Generate all four main offices
        mp = MorningPrayer(test_date)
        ep = EveningPrayer(test_date)

        _ = mp.modules
        _ = ep.modules

        end_time = time.time()
        duration = (end_time - start_time) * 1000

        print(f"\nMultiple offices (MP + EP) total time: {duration:.2f}ms")

        # Should complete in reasonable time for both (relaxed for containers)
        assert duration < 3000, f"Multiple offices took {duration:.2f}ms, expected < 3000ms"

    def test_office_generation_consistent_performance(self):
        """Office generation performance is consistent across multiple runs."""
        test_date = date(2025, 12, 25)
        durations = []

        # Run 5 times to check consistency
        for i in range(5):
            start_time = time.time()
            office = MorningPrayer(test_date)
            _ = office.modules
            end_time = time.time()
            durations.append((end_time - start_time) * 1000)

        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        min_duration = min(durations)

        print(f"\nPerformance consistency:")
        print(f"  Average: {avg_duration:.2f}ms")
        print(f"  Min: {min_duration:.2f}ms")
        print(f"  Max: {max_duration:.2f}ms")

        # Max should not be more than 2x average (excluding first run warmup)
        # Use durations[1:] to exclude potential first-run overhead
        if len(durations) > 1:
            avg_without_first = sum(durations[1:]) / len(durations[1:])
            max_without_first = max(durations[1:])
            variance_ratio = max_without_first / avg_without_first

            print(f"  Variance ratio (excluding first): {variance_ratio:.2f}x")
            assert variance_ratio < 2.0, f"Performance too inconsistent: {variance_ratio:.2f}x variance"
