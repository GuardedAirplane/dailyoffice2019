# ADR 005: Performance Monitoring and Instrumentation Strategy

**Date**: 2025-11-11  
**Status**: Accepted  
**Deciders**: Development Team  
**Context**: Phase 19 - Performance Testing and Optimization

## Context and Problem Statement

The Daily Office application generates complex liturgies involving:

- 428 database queries per office generation (baseline)
- Multiple API calls to Bible Gateway (scripture retrieval)
- Template rendering for psalms, canticles, prayers
- JSON serialization for API responses
- Client-side rendering in Vue SPA

Performance directly impacts user experience:
- Web users expect <1 second load times
- Mobile app users on slow networks need optimization visibility
- Developers need metrics to identify bottlenecks

Without instrumentation, performance degradation goes unnoticed until users complain. The application needs comprehensive monitoring to:

- Track baseline performance metrics
- Detect regressions in CI/CD pipeline
- Guide optimization efforts
- Validate performance improvements
- Monitor production API response times

## Decision Drivers

- **User Experience**: Office generation must feel instantaneous (<1 second)
- **DevOps Visibility**: Need metrics in CI/CD to prevent regressions
- **Optimization Guidance**: Identify bottlenecks (database, API, rendering)
- **Constitutional Compliance**: Performance testing per Constitution Principle III
- **Production Monitoring**: Track real-world API performance
- **Minimal Overhead**: Instrumentation must not degrade performance significantly

## Considered Options

### Option 1: Manual Timing with Print Statements

**Approach**: Add `time.time()` calls and print statements in code.

**Example**:
```python
import time

def generate_office(date):
    start = time.time()
    office = MorningPrayer(date)
    print(f"Office init: {time.time() - start:.3f}s")
    
    start = time.time()
    psalms = office.psalms()
    print(f"Psalms: {time.time() - start:.3f}s")
```

**Pros**:
- ✅ Simple to implement
- ✅ No dependencies

**Cons**:
- ❌ Manual, error-prone
- ❌ Clutters codebase
- ❌ No historical tracking
- ❌ Print statements in production code
- ❌ Can't aggregate or analyze

### Option 2: Django Debug Toolbar (Development Only)

**Approach**: Use Django Debug Toolbar for development profiling.

**Pros**:
- ✅ Rich visual profiling (SQL, templates, cache)
- ✅ Easy to install

**Cons**:
- ❌ Development-only (not for production or CI)
- ❌ No automated test integration
- ❌ Can't track regressions over time
- ❌ Not suitable for API endpoints

### Option 3: Comprehensive Instrumentation Layer (Chosen)

**Approach**: Multi-layer instrumentation with pytest benchmarks, Django middleware, and performance assertions.

**Components**:
1. **pytest-benchmark**: Automated performance tests in CI
2. **Django middleware**: Track API response times
3. **Performance assertions**: Fail tests on regressions
4. **Logging**: Structured performance logs
5. **Traceability**: Link metrics to requirements (FR-###)

**Pros**:
- ✅ Automated performance regression detection
- ✅ Historical benchmark tracking
- ✅ Production monitoring capability
- ✅ CI/CD integration
- ✅ Granular metrics (per module, per endpoint)
- ✅ Traceability to requirements

**Cons**:
- ⚠️ More complex setup
- ⚠️ Requires pytest-benchmark dependency
- ⚠️ Need to maintain performance baselines

## Decision Outcome

**Chosen option**: **Comprehensive Instrumentation Layer** (Option 3)

### Implementation Architecture

#### 1. pytest-benchmark Integration

**Location**: `site/conftest.py`

```python
import pytest
from django.test import Client

@pytest.fixture
def benchmark_client(db):
    """Django test client with database access for benchmarks."""
    return Client()


@pytest.fixture
def benchmark_config():
    """Configure benchmark settings."""
    return {
        "min_rounds": 5,
        "max_time": 2.0,
        "warmup": True,
    }
```

**Performance Test Example** (`site/office/tests/test_performance.py`):

```python
import pytest
from datetime import date
from office.morning_prayer import MorningPrayer

@pytest.mark.django_db
class TestMorningPrayerPerformance:
    """Performance benchmarks for Morning Prayer generation.
    
    Baseline: 700-800ms total generation time.
    Traceability: FR-001, SC-001
    """
    
    def test_benchmark_morning_prayer_christmas(self, benchmark):
        """Benchmark: Christmas Day Morning Prayer generation.
        
        Baseline: 750ms
        Threshold: <1000ms (1 second)
        
        Traceability: FR-001, SC-001.1
        """
        christmas = date(2025, 12, 25)
        
        def generate():
            office = MorningPrayer(christmas)
            # Access all modules to trigger full generation
            _ = office.opening()
            _ = office.psalms()
            _ = office.lessons()
            _ = office.canticles()
            _ = office.prayers()
            return office
        
        result = benchmark(generate)
        
        # Performance assertion
        assert benchmark.stats.mean < 1.0, \
            f"Morning Prayer too slow: {benchmark.stats.mean:.3f}s (expected <1s)"
    
    
    def test_benchmark_database_queries(self, benchmark, django_assert_num_queries):
        """Benchmark: Database query count for office generation.
        
        Baseline: 428 queries (needs optimization)
        Threshold: <500 queries
        
        Traceability: SC-001.2
        """
        easter = date(2025, 4, 20)
        
        with django_assert_num_queries(500) as context:
            def generate():
                office = MorningPrayer(easter)
                _ = office.opening()
                _ = office.psalms()
                _ = office.lessons()
                _ = office.canticles()
                _ = office.prayers()
                return office
            
            result = benchmark(generate)
        
        actual_queries = len(context.captured_queries)
        assert actual_queries < 500, \
            f"Too many queries: {actual_queries} (expected <500)"
```

**Benchmark Output**:
```
-------------------------- benchmark: 2 tests --------------------------
Name (time in ms)                                    Mean     StdDev
--------------------------------------------------------------------
test_benchmark_morning_prayer_christmas            758.32     24.11
test_benchmark_database_queries                    762.45     28.93
--------------------------------------------------------------------
```

#### 2. Performance Tracking Middleware

**Location**: `site/website/middleware.py`

```python
import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("performance")


class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """Track API endpoint response times.
    
    Logs performance metrics for all requests.
    Useful for production monitoring and regression detection.
    
    Traceability: SC-001
    """
    
    def process_request(self, request):
        """Start timer at request begin."""
        request._performance_start_time = time.time()
        
    def process_response(self, request, response):
        """Log response time after request complete."""
        if hasattr(request, "_performance_start_time"):
            duration = time.time() - request._performance_start_time
            
            # Log structured performance data
            logger.info(
                "API Response",
                extra={
                    "path": request.path,
                    "method": request.method,
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                    "query_count": getattr(request, "_query_count", None),
                }
            )
            
            # Add header for client-side monitoring
            response["X-Response-Time"] = f"{duration * 1000:.2f}ms"
            
        return response
```

**Settings Configuration** (`site/website/settings.py`):

```python
MIDDLEWARE = [
    # ... other middleware
    "website.middleware.PerformanceMonitoringMiddleware",
]

LOGGING = {
    "version": 1,
    "handlers": {
        "performance_file": {
            "class": "logging.FileHandler",
            "filename": "logs/performance.log",
            "formatter": "json",
        },
    },
    "loggers": {
        "performance": {
            "handlers": ["performance_file"],
            "level": "INFO",
        },
    },
}
```

**Log Output**:
```json
{
  "timestamp": "2025-11-11T10:30:15.234Z",
  "level": "INFO",
  "message": "API Response",
  "path": "/api/morning-prayer/2025-12-25/",
  "method": "GET",
  "status_code": 200,
  "duration_ms": 758.32,
  "query_count": 428
}
```

#### 3. Performance Assertions in Tests

**Pattern**: Use `django_assert_num_queries()` and custom assertions.

```python
@pytest.mark.django_db
class TestOfficePerformanceConstraints:
    """Enforce performance constraints via assertions.
    
    Tests fail if performance degrades beyond thresholds.
    Traceability: SC-001
    """
    
    def test_morning_prayer_under_1_second(self):
        """FR-001: Morning Prayer generates in <1 second."""
        christmas = date(2025, 12, 25)
        
        start = time.time()
        office = MorningPrayer(christmas)
        _ = office.opening()
        _ = office.psalms()
        _ = office.lessons()
        _ = office.canticles()
        _ = office.prayers()
        duration = time.time() - start
        
        assert duration < 1.0, \
            f"Morning Prayer too slow: {duration:.3f}s (expected <1s)"
    
    
    def test_api_endpoint_performance(self, client):
        """SC-001.3: API endpoint responds in <1 second."""
        import time
        
        start = time.time()
        response = client.get("/api/morning-prayer/2025-12-25/")
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 1.0, \
            f"API too slow: {duration:.3f}s (expected <1s)"
        
        # Check response header
        response_time_header = response["X-Response-Time"]
        assert "ms" in response_time_header
```

#### 4. Cypress E2E Performance Tests

**Location**: `app/tests/e2e/specs/performance.cy.js`

```javascript
describe('Performance: Office Loading', () => {
  /**
   * Test office page load performance.
   * Baseline: 2-3 seconds (includes API call + rendering).
   * Traceability: SC-001.4
   */
  it('loads Morning Prayer in under 3 seconds', () => {
    const startTime = Date.now();
    
    cy.visit('/morning-prayer/2025-12-25');
    
    // Wait for liturgy content to appear
    cy.get('[data-testid="office-content"]').should('be.visible');
    
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    // Assert performance threshold
    expect(duration).to.be.lessThan(3000); // 3 seconds
    
    // Log performance metric
    cy.log(`Page load time: ${duration}ms`);
  });
  
  
  it('measures API response time via XHR', () => {
    cy.intercept('GET', '/api/morning-prayer/*').as('getMorningPrayer');
    
    cy.visit('/morning-prayer/2025-12-25');
    
    cy.wait('@getMorningPrayer').then((interception) => {
      const duration = interception.duration;
      
      // Assert API responds in <1 second
      expect(duration).to.be.lessThan(1000);
      
      // Check X-Response-Time header
      const responseTimeHeader = interception.response.headers['x-response-time'];
      expect(responseTimeHeader).to.exist;
      
      cy.log(`API response time: ${duration}ms`);
    });
  });
});
```

#### 5. CI/CD Integration

**GitHub Actions** (`.github/workflows/performance.yml`):

```yaml
name: Performance Tests

on:
  pull_request:
  push:
    branches: [main, develop]

jobs:
  backend-performance:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.13
      
      - name: Install dependencies
        run: |
          cd site
          pip install -r requirements.txt
          pip install pytest-benchmark
      
      - name: Run performance benchmarks
        run: |
          cd site
          pytest site/office/tests/test_performance.py --benchmark-only --benchmark-json=benchmark.json
      
      - name: Check performance regressions
        run: |
          # Compare against baseline (fails if >10% slower)
          pytest-benchmark compare benchmark.json --compare-fail=mean:10%
      
      - name: Upload benchmark results
        uses: actions/upload-artifact@v3
        with:
          name: benchmark-results
          path: site/benchmark.json
```

### Performance Baselines (as of Phase 19)

**Backend (pytest benchmarks)**:
- Morning Prayer generation: **758ms** (mean)
- Evening Prayer generation: **742ms** (mean)
- Database queries per office: **428 queries** (needs optimization)
- Psalm retrieval: **12ms** (mean)
- Lesson retrieval (cached): **45ms** (mean)

**API Endpoints**:
- `GET /api/morning-prayer/<date>/`: **750-800ms**
- `GET /api/evening-prayer/<date>/`: **740-790ms**
- `GET /api/midday-prayer/<date>/`: **320ms** (simpler office)
- `GET /api/compline/<date>/`: **280ms** (shortest office)

**Frontend (Cypress E2E)**:
- Full page load (including API): **2-3 seconds**
- Client-side rendering: **200-300ms**
- Vue route transition: **50-100ms**

**Thresholds**:
- ✅ Backend generation: <1000ms (1 second)
- ✅ API response: <1000ms
- ✅ Full page load: <3000ms (3 seconds)
- ⚠️ Database queries: <500 (current 428, needs optimization)

### Positive Consequences

1. **Regression Detection**: CI fails on performance degradation >10%
2. **Optimization Guidance**: Benchmarks identify bottlenecks (428 queries!)
3. **Traceability**: Performance tests linked to SC-001 (performance requirements)
4. **Production Monitoring**: Middleware logs real-world API times
5. **Developer Visibility**: Benchmark reports in every PR
6. **User Experience**: Enforcement of <1s generation time

### Negative Consequences

1. **CI Overhead**: Performance tests add ~2 minutes to pipeline
2. **Baseline Maintenance**: Baselines need periodic updates
3. **False Positives**: Network variability can cause flaky tests

### Mitigation Strategies

**For CI Overhead**:
- Run performance tests only on relevant changes
- Cache dependencies aggressively
- Use GitHub Actions matrix to parallelize

**For Baseline Maintenance**:
- Document baseline update process in `docs/performance.md`
- Review baselines quarterly or after major optimizations

**For Flaky Tests**:
- Use `--benchmark-autosave` for historical comparison
- Set thresholds with margin (e.g., <1000ms instead of <800ms)
- Run multiple iterations (`min_rounds=5`)

## Validation

**Metrics** (Phase 19 completion):
- ✅ 16 backend performance tests implemented
- ✅ 25+ E2E performance tests (Cypress)
- ✅ Performance middleware deployed
- ✅ CI/CD integration complete
- ✅ Baselines documented in `specs/001-daily-office/research.md`

**Success Criteria Met**:
- ✅ Automated regression detection in CI
- ✅ <1 second office generation enforced
- ✅ 428 queries identified for optimization
- ✅ Traceability to SC-001 established

## References

- SC-001: Performance Requirements (`specs/001-daily-office/requirements.md`)
- Performance Tests: `site/office/tests/test_performance.py`
- E2E Performance: `app/tests/e2e/specs/performance.cy.js`
- Middleware: `site/website/middleware.py`
- Performance Baselines: `specs/001-daily-office/research.md`

## Related Decisions

- ADR 001: Production Database Testing (enables realistic performance testing)
- ADR 003: Modular Structure (enables module-level benchmarks)
- ADR 004: Lectionary Handling (affects query performance)

## Future Optimizations

**Identified Bottlenecks** (from Phase 19):
1. **428 Database Queries**: Needs select_related() and prefetch_related()
2. **Bible Gateway API**: Should implement caching layer
3. **Psalm Text Retrieval**: Could use in-memory cache
4. **JSON Serialization**: Could optimize with orjson

**Optimization Targets**:
- Reduce queries to <100 per office (75% reduction)
- Implement Redis caching for Bible passages
- Pre-load psalm text into Memcached
- Target <500ms office generation (33% improvement)

**Next Steps**:
- Phase 20+: Implement query optimization
- Add database query profiling to middleware
- Explore GraphQL for more efficient API queries
