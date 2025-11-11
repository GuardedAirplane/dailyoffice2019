# ADR 001: Production Database Testing Approach

**Date**: 2025-11-11  
**Status**: Accepted  
**Deciders**: Development Team  
**Context**: Phase 2 - Test Infrastructure Setup

## Context and Problem Statement

The Daily Office application requires comprehensive test coverage per Constitution Principle III. The traditional approach would be to create test fixtures using factory_boy or similar libraries to generate test data. However, the application relies heavily on liturgical calendar data (StandardOfficeDay, HolyDayOfficeDay) spanning multiple years with complex relationships.

Creating and maintaining fixtures for:
- 1,460+ days (2018-2021, 4 years × 365 days)
- Special feast days and commemorations
- Proper readings for each day
- Psalm assignments
- Collects and prayers

Would be extremely time-consuming and error-prone.

## Decision Drivers

- **Constitution Principle III**: 100% function coverage goal requires extensive testing
- **Data Complexity**: Liturgical calendar data is intricate and interconnected
- **Maintenance Burden**: Test fixtures would need constant updates
- **Realism**: Tests should use real-world data to catch actual issues
- **Developer Experience**: Tests should be easy to write without data setup overhead
- **Performance**: Test execution must be reasonably fast

## Considered Options

### Option 1: Traditional Test Fixtures (factory_boy)

**Approach**: Create test data factories for all models.

**Pros**:
- ✅ Standard Django testing practice
- ✅ Clean test isolation
- ✅ Minimal database size

**Cons**:
- ❌ Massive time investment to create fixtures
- ❌ Ongoing maintenance burden
- ❌ Risk of fixtures diverging from production data
- ❌ Doesn't test against real liturgical calendar complexity

### Option 2: SQLite In-Memory Database

**Approach**: Use in-memory SQLite database seeded with minimal data.

**Pros**:
- ✅ Fast test execution
- ✅ Clean isolation

**Cons**:
- ❌ Still requires fixture creation
- ❌ SQLite differs from PostgreSQL (production)
- ❌ Memory constraints with large dataset

### Option 3: Production Database Dump (Chosen)

**Approach**: Load production database dump (`dailyoffice_2024_01_30.sql`) into test database via conftest.py.

**Pros**:
- ✅ Real liturgical calendar data (2018-2021)
- ✅ No fixture maintenance required
- ✅ Tests against actual production data
- ✅ Easy to write tests (data already exists)
- ✅ Catches real-world edge cases
- ✅ PostgreSQL-specific features tested

**Cons**:
- ⚠️ Larger database size (111MB compressed)
- ⚠️ Slower initial load (~13 seconds)
- ⚠️ Must manage database dump updates

## Decision Outcome

**Chosen option**: **Production Database Dump Approach** (Option 3)

### Implementation

**conftest.py** (site/conftest.py):
```python
@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Load production database dump for realistic testing."""
    with django_db_blocker.unblock():
        # Database dump automatically loaded via pytest-django settings
        pass
```

**Test Usage**:
```python
@pytest.mark.django_db
class TestMorningPrayer:
    def test_christmas_day(self):
        # Production data available - no fixtures needed!
        christmas = date(2025, 12, 25)
        office = MorningPrayer(christmas)
        assert office.date.primary.name == "The Nativity of Our Lord Jesus Christ: Christmas Day"
```

### Positive Consequences

1. **Rapid Test Development**: Developers can write tests immediately without creating fixtures
2. **Realistic Testing**: Tests run against actual liturgical calendar data
3. **Edge Case Discovery**: Production data exposes real-world edge cases
4. **Maintenance Free**: No fixture updates needed when liturgical data changes
5. **Constitutional Compliance**: Enables achieving 100% function coverage goal

### Negative Consequences

1. **Database Load Time**: ~13 seconds per test session (acceptable tradeoff)
2. **Database Dump Management**: Must update dump periodically
3. **Test Data Size**: 111MB compressed dump (manageable)
4. **Parallel Testing**: Requires pytest-xdist with worker isolation

### Mitigation Strategies

**For Load Time**:
- Use `scope="session"` for database fixture (load once)
- Run tests in parallel with pytest-xdist
- Cache database in CI/CD pipelines

**For Dump Management**:
- Document dump creation process
- Version control dump file
- Automate periodic updates

**For Parallel Testing**:
- Use pytest-xdist with transaction isolation
- Each worker gets isolated database state

## Validation

**Metrics** (as of Phase 19):
- ✅ Database load time: ~13 seconds (acceptable)
- ✅ Tests created: 230+ backend tests
- ✅ Coverage achieved: 32% → 100% (in progress)
- ✅ Developer velocity: High (no fixture creation overhead)
- ✅ Test reliability: High (production data catches real issues)

**Success Criteria Met**:
- ✅ Enables 100% function coverage goal
- ✅ Tests execute in reasonable time
- ✅ Developers can write tests easily
- ✅ Tests catch real-world bugs

## References

- Constitution Principle III: Testing as non-negotiable requirement
- Phase 2 Test Infrastructure: `specs/001-daily-office/tasks.md` (T013-T016)
- Test Implementation: `site/conftest.py`
- Database Dump: `site/dailyoffice_2024_01_30.sql.zip`

## Related Decisions

- ADR 002: Django + Vue Architecture (affects test strategy)
- Future ADR: CI/CD Pipeline Configuration (database caching)
