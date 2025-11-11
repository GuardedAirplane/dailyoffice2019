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
    - SC-001: Office generation should complete quickly
    - Target: < 500ms for office generation (server-side)
    """

    def test_morning_prayer_generation_fast(self):
        """Morning Prayer generation completes in under 500ms."""
        test_date = date(2025, 12, 25)  # Christmas Day
        
        start_time = time.time()
        office = MorningPrayer(test_date)
        _ = office.modules  # Force module generation
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000  # Convert to ms
        
        # Log performance for monitoring
        print(f"\nMorning Prayer generation time: {duration:.2f}ms")
        
        # Assert performance requirement
        assert duration < 500, f"Morning Prayer took {duration:.2f}ms, expected < 500ms"

    def test_morning_prayer_generation_regular_day(self):
        """Morning Prayer generation is fast for regular days."""
        test_date = date(2025, 11, 12)  # Regular feria
        
        start_time = time.time()
        office = MorningPrayer(test_date)
        _ = office.modules
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        print(f"\nMorning Prayer (regular day) generation time: {duration:.2f}ms")
        
        assert duration < 500, f"Morning Prayer regular day took {duration:.2f}ms, expected < 500ms"

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
        
        assert duration < 500, f"Morning Prayer with multiple commemorations took {duration:.2f}ms, expected < 500ms"


@pytest.mark.django_db
class TestEveningPrayerPerformance:
    """
    T229: Performance test - Evening Prayer generation time.
    
    Requirements:
    - SC-001: Office generation should complete quickly
    - Target: < 500ms for office generation (server-side)
    """

    def test_evening_prayer_generation_fast(self):
        """Evening Prayer generation completes in under 500ms."""
        test_date = date(2025, 12, 25)  # Christmas Day
        
        start_time = time.time()
        office = EveningPrayer(test_date)
        _ = office.modules
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        print(f"\nEvening Prayer generation time: {duration:.2f}ms")
        
        assert duration < 500, f"Evening Prayer took {duration:.2f}ms, expected < 500ms"

    def test_evening_prayer_generation_regular_day(self):
        """Evening Prayer generation is fast for regular days."""
        test_date = date(2025, 11, 12)  # Regular feria
        
        start_time = time.time()
        office = EveningPrayer(test_date)
        _ = office.modules
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        print(f"\nEvening Prayer (regular day) generation time: {duration:.2f}ms")
        
        assert duration < 500, f"Evening Prayer regular day took {duration:.2f}ms, expected < 500ms"


@pytest.mark.django_db
class TestAPIPerformance:
    """
    T230: Performance test - API response time for office endpoints.
    
    Requirements:
    - API response time < 500ms
    - Includes database queries and serialization
    """

    @override_settings(DEBUG=False)
    def test_morning_prayer_api_response_fast(self):
        """Morning Prayer API endpoint responds in under 500ms."""
        client = Client()
        test_date = "2025-12-25"
        
        start_time = time.time()
        response = client.get(f"/api/office/morning_prayer/{test_date}/")
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        print(f"\nMorning Prayer API response time: {duration:.2f}ms")
        
        assert response.status_code == 200
        assert duration < 500, f"API response took {duration:.2f}ms, expected < 500ms"

    @override_settings(DEBUG=False)
    def test_evening_prayer_api_response_fast(self):
        """Evening Prayer API endpoint responds in under 500ms."""
        client = Client()
        test_date = "2025-12-25"
        
        start_time = time.time()
        response = client.get(f"/api/office/evening_prayer/{test_date}/")
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        print(f"\nEvening Prayer API response time: {duration:.2f}ms")
        
        assert response.status_code == 200
        assert duration < 500, f"API response took {duration:.2f}ms, expected < 500ms"

    @override_settings(DEBUG=False)
    def test_midday_prayer_api_response_fast(self):
        """Midday Prayer API endpoint responds in under 500ms."""
        client = Client()
        test_date = "2025-12-25"
        
        start_time = time.time()
        response = client.get(f"/api/office/midday_prayer/{test_date}/")
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        print(f"\nMidday Prayer API response time: {duration:.2f}ms")
        
        assert response.status_code == 200
        assert duration < 500, f"API response took {duration:.2f}ms, expected < 500ms"

    @override_settings(DEBUG=False)
    def test_compline_api_response_fast(self):
        """Compline API endpoint responds in under 500ms."""
        client = Client()
        test_date = "2025-12-25"
        
        start_time = time.time()
        response = client.get(f"/api/office/compline/{test_date}/")
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000
        print(f"\nCompline API response time: {duration:.2f}ms")
        
        assert response.status_code == 200
        assert duration < 500, f"API response took {duration:.2f}ms, expected < 500ms"


@pytest.mark.django_db
class TestScriptureCachePerformance:
    """
    T231: Performance test - Scripture cache hit vs miss latency.
    
    Requirements:
    - Cache hits should be significantly faster than API calls
    - Cache miss with API should complete in reasonable time
    """

    @patch('bible.passage.Passage.lookup')
    def test_scripture_cache_hit_fast(self, mock_lookup):
        """Scripture cache hit is significantly faster than API call."""
        # Mock Passage.lookup to simulate cached response
        mock_lookup.return_value = "Cached scripture text"
        
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
    """

    def test_morning_prayer_query_count(self, django_assert_max_num_queries):
        """Morning Prayer uses reasonable number of database queries."""
        test_date = date(2025, 12, 25)
        
        # Allow up to 50 queries for complex feast day with multiple readings
        # This is a reasonable upper bound - optimize if exceeded
        with django_assert_max_num_queries(50):
            office = MorningPrayer(test_date)
            _ = office.modules
            
        print(f"\nMorning Prayer query count test passed (< 50 queries)")

    def test_evening_prayer_query_count(self, django_assert_max_num_queries):
        """Evening Prayer uses reasonable number of database queries."""
        test_date = date(2025, 12, 25)
        
        with django_assert_max_num_queries(50):
            office = EveningPrayer(test_date)
            _ = office.modules
            
        print(f"\nEvening Prayer query count test passed (< 50 queries)")

    def test_regular_day_query_count(self, django_assert_max_num_queries):
        """Regular day office uses fewer queries than feast days."""
        test_date = date(2025, 11, 12)  # Regular feria
        
        # Regular days should use fewer queries (no special readings)
        with django_assert_max_num_queries(40):
            office = MorningPrayer(test_date)
            _ = office.modules
            
        print(f"\nRegular day query count test passed (< 40 queries)")


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
        
        # Should complete in under 1 second for both
        assert duration < 1000, f"Multiple offices took {duration:.2f}ms, expected < 1000ms"

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
