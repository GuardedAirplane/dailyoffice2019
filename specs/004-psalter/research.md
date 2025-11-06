# Research: Psalter Implementation

**Feature**: 004-psalter | **Phase**: 0 (Research & Decisions) | **Date**: November 6, 2025

This document resolves all "NEEDS CLARIFICATION" items from the implementation plan and documents design decisions. The specification has been updated to accurately reflect the existing implementation.

## Research Questions

### Q1: Admin Interface Documentation and Best Practices

**Question**: How should administrators use the Django admin interface for managing psalm topics and editing psalm text?

**Context**: FR-016 through FR-019 specify admin interface capabilities. Need to document proper usage patterns and best practices.

**Research Findings**:

1. **Topic Management Workflow**

   - **Create Topic**: Django Admin → Psalter → Psalm Topics → Add
   - **Assign Psalms**: Use PsalmTopicPsalm inline or separate form
   - **Reorder Topics**: Drag-and-drop with SortableAdminMixin (order field)
   - **Edit Topic Name**: Simple text field update

2. **Psalm Text Editing**

   - **Access**: Django Admin → Psalter → Psalm Verses
   - **Filter**: Use "Verses with Lord" filter for bulk review
   - **Edit Fields**: Contemporary (first_half/second_half) and TLE (first_half_tle/second_half_tle)
   - **Use Cases**: Correct transcription errors, update translations

3. **Admin Permissions**

   - Only superusers and staff with psalm permissions
   - Read-only for most users (frontend displays only)
   - Change tracking via Django's built-in audit log

4. **Best Practices**
   - **Backup before bulk edits**: Database dump before major changes
   - **Clear cache after edits**: Ensure frontend reflects changes (FR-SC-010: within 10 seconds)
   - **Document rationale**: Add comments for why changes were made
   - **Test after edits**: Verify psalm displays correctly on frontend

**Decision**:

- **Create admin user guide** in Phase 1 documentation
- **Document common workflows** (create topic, assign psalms, fix typos)
- **Include screenshots** of admin interface in quickstart.md
- **Add troubleshooting** for cache invalidation

**Rationale**: Admin interface is a key feature (FR-016-019) that needs proper documentation for effective use. Good documentation prevents mistakes and ensures consistent topic curation.

**Alternatives Considered**:

- Custom admin UI: Overkill, Django admin is powerful and familiar
- No documentation: Leads to misuse and support burden

---

### Q2: Psalm Range UI Design (FR-006/FR-007)

**Question**: What's the best user interface for accessing psalm ranges and partial psalms?

**Context**: Backend supports ranges like "1-3" and "119:1-32" but frontend has no UI for this.

**Research Findings**:

1. **URL Structure Options**

   - **Path-based**: `/psalms/1-3` or `/psalm/119:1-32`
     - ✅ Clean, bookmarkable, RESTful
     - ✅ Works with existing `get_psalms()` backend function
     - ❌ Requires new route and view component
   - **Query parameter**: `/psalms?range=1-3`
     - ✅ Reuses existing `/psalms` route
     - ❌ Less intuitive, harder to bookmark
   - **Fragment**: `/psalms#1-3`
     - ❌ Not SEO-friendly, poor UX

2. **Input Method Options**

   - **Text input with search button**: User types "1-3" or "119:1-32"
     - ✅ Flexible, supports all backend parsing
     - ✅ Familiar pattern (like Bible search)
     - ❌ Requires validation and error handling
   - **Dual dropdown**: "From Psalm X" to "To Psalm Y"
     - ✅ No parsing errors possible
     - ❌ Can't do partial psalms (119:1-32)
     - ❌ Verbose UI for simple ranges
   - **Smart input with autocomplete**: Suggests as you type
     - ✅ Best UX but highest complexity
     - ❌ Overkill for this use case

3. **Integration Points**

   - Add search bar to existing `/psalms` (Psalms.vue) page
   - Navigate to new route `/psalms/[range]` on submit
   - Create new `PsalmRange.vue` component to display results
   - Reuse `psalm_html` backend utility (already supports ranges)

4. **User Scenarios from Spec**
   - US3: "View Psalms 120-134" (Songs of Ascent) - common in lectionary
   - US3: "View Psalm 119:1-32" (Aleph section) - longer psalm portions
   - Edge case: Spanning multiple psalms partially (uncommon, deprioritize)

**Decision**:

- **URL structure**: Path-based `/psalms/[range]` (e.g., `/psalms/1-3`, `/psalms/119:1-32`)
- **Input method**: Simple text input on Psalms.vue with "View Range" button
- **New component**: `PsalmRange.vue` displays range results (similar to Psalm.vue)
- **Priority**: P2 (not critical for MVP, backend already works, low user demand verified)

**Rationale**: Path-based URLs are most intuitive and align with REST principles. Text input is simplest to implement and leverages existing backend parsing. This is a minor enhancement that shouldn't block core psalter functionality.

**Alternatives Considered**:

- Query parameters: Less bookmarkable, breaks REST conventions
- Dropdown selectors: Too restrictive, can't handle verse ranges
- Modal dialog: Adds complexity without UX benefit

---

### Q3: Testing Strategy and Priorities (Constitution III)

**Question**: What tests to write first to achieve 100% function coverage while being pragmatic about effort?

**Context**: Current implementation has minimal tests. Constitution III mandates comprehensive testing before modifications.

**Research Findings**:

1. **Test Pyramid for This Feature**

   ```
   E2E (Cypress)          [5-10 tests]  ← Critical user journeys
       ↑
   Integration (pytest)   [15-20 tests] ← API contracts, DB queries
       ↑
   Unit (pytest/Vitest)   [30-40 tests] ← Pure functions, components
   ```

2. **Priority Matrix**
   | Code Area | User Impact | Change Risk | Test Priority |
   |-----------|-------------|-------------|---------------|
   | `normalize_citations()` | High | Medium | **P0** |
   | `get_psalms()` | High | Medium | **P0** |
   | `PsalmsViewSet` | High | Low | **P1** |
   | `Psalm.vue` | High | Medium | **P0** |
   | `Psalms.vue` | Medium | Medium | **P1** |
   | Admin (being removed) | Low | High | **P2** |

3. **Test Writing Sequence**

   1. **Phase 2a**: Unit tests for utils.py functions (pure logic, no DB)
   2. **Phase 2b**: Integration tests for API endpoints (with test DB)
   3. **Phase 2c**: Component unit tests (Vue components with mocks)
   4. **Phase 2d**: E2E tests for critical paths (full stack)

4. **Test Data Fixtures**

   - Use first 10 psalms (1-10) for test database
   - Include one long psalm (119) for edge cases
   - Create 2-3 test topics with known psalm associations
   - Use factory pattern (e.g., `factory_boy`) for object creation

5. **Coverage Targets**
   - **Unit**: 100% of pure functions (`normalize_citations`, `psalm_html`, etc.)
   - **Integration**: All API endpoints, all database queries
   - **E2E**: 5 critical paths (view psalm, navigate, switch language, filter topic, range)
   - **Threshold**: Enforce 90% minimum in CI/CD

**Decision**:

- **Test-first for new code**: Admin removal, range UI must have tests before implementation
- **Test-after for existing code**: Write tests for current implementation first, then modify
- **Sequence**: Unit → Integration → Component → E2E
- **Tools**: pytest + pytest-django + pytest-factoryboy (backend), Vitest (frontend unit), Cypress (E2E)
- **CI/CD gate**: All tests must pass before merge, coverage report required

**Rationale**: Testing existing code first creates safety net before modifications. Test-first for new code prevents regressions. This pragmatic approach balances constitutional mandate with practical delivery.

**Alternatives Considered**:

- Pure test-first for all code: Would block urgent fixes, impractical for legacy code
- Manual testing only: Violates Constitution III, creates technical debt
- 100% coverage or nothing: Perfect is enemy of good, 90% is pragmatic threshold

---

### Q4: Database Fixtures Best Practices (Data Management)

**Question**: What's the best way to version control and load psalm data and topics?

**Context**: Need to ensure psalm text, verses, and topics are reproducible across environments.

**Research Findings**:

1. **Django Data Loading Options**

   - **Initial fixtures**: `python manage.py loaddata psalter/fixtures/initial_data.json`
   - **Custom management command**: `python manage.py load_psalms`
   - **Database dump**: Direct SQL import (current approach per copilot-instructions.md)
   - **Migrations with RunPython**: Data in migration files (anti-pattern for large datasets)

2. **Current State Analysis**

   - Per copilot-instructions.md: Database dump exists (`dailyoffice_2024_01_30.sql.zip`)
   - This includes all psalms, verses, and topics
   - Development setup: Import full database (4 seconds, fast and reliable)
   - Likely no fixtures currently exist in `psalter/fixtures/`

3. **Version Control Strategy**

   - **Large datasets** (150 psalms × 15 verses = 2,250 records): Database dump or compressed fixture
   - **Small datasets** (10-15 topics): JSON fixture in Git
   - **Hybrid approach**: Fixtures for schema, dump for bulk data

4. **Idempotent Loading**

   - Use `get_or_create()` in management commands
   - Add unique constraints to models (already exists: `Psalm.number` is unique)
   - Handle updates vs inserts gracefully

5. **Production Deployment**
   - Initial deployment: Load from fixtures/dump
   - Updates: Migrations handle schema, management command for data
   - Psalm text changes: Rare, would be a migration with data update

**Decision**:

- **Keep current database dump approach** for development (fast, proven)
- **Create JSON fixture for topics only** (small, frequently referenced in tests)
- **Extract sample fixture** (Psalms 1-10) for test suite
- **Document loading process** in quickstart.md
- **Management command** as alternative to dump for CI/CD environments

**Rationale**: Current approach works well for development. Adding fixtures for topics and test data improves testability without disrupting existing workflow. Aligns with "don't fix what isn't broken" principle.

**Alternatives Considered**:

- Pure fixtures for everything: 2,250+ records in JSON is unwieldy, slow to load
- Pure database dump: Hard to version control diffs, poor for automated testing
- Migration-based data: Anti-pattern for large datasets, bloats migration history

---

### Q5: API Contract Documentation (OpenAPI Specification)

**Question**: How should we document the existing Psalms API endpoints?

**Context**: Constitution requires API contracts. Need OpenAPI spec for existing endpoints.

**Research Findings**:

1. **Current API Endpoints** (from code analysis)

   ```
   GET /api/v1/psalms              - List all psalms
   GET /api/v1/psalms/{number}     - Retrieve single psalm
   GET /api/v1/psalms/topics/      - List all topics
   ```

2. **OpenAPI Generation Tools**

   - **drf-spectacular**: Django REST Framework integration, auto-generates from serializers
   - **Manual YAML**: More control, must stay in sync with code
   - **Swagger/ReDoc**: UI for testing API (already configured per api_urls.py)

3. **Schema Location**

   - Current: `api_urls.py` has schema view configured with drf-yasg
   - Proposed: Add `specs/004-psalter/contracts/psalms-api.yaml` for documentation
   - Both: Auto-generated schema for accuracy, manual YAML for spec documentation

4. **Response Schema Elements**

   ```yaml
   Psalm:
     - id (UUID)
     - number (integer 1-150)
     - latin_title (string, nullable)
     - verses (array of PsalmVerse)
     - topics (array of PsalmTopic, via PsalmTopicPsalm)

   PsalmVerse:
     - id (UUID)
     - number (integer)
     - first_half (string, contemporary)
     - second_half (string, contemporary)
     - first_half_tle (string, traditional)
     - second_half_tle (string, traditional)

   PsalmTopic:
     - id (UUID)
     - topic_name (string)
     - order (integer)
   ```

**Decision**:

- **Use drf-spectacular** to auto-generate accurate OpenAPI schema from code
- **Create manual YAML** in `specs/004-psalter/contracts/psalms-api.yaml` documenting spec intent
- **Keep both in sync**: Generated schema is source of truth for implementation
- **Add examples**: Include sample responses with real psalm data

**Rationale**: Auto-generated schemas stay accurate as code evolves. Manual spec documents intent and requirements. Both serve different audiences (developers vs. stakeholders).

**Alternatives Considered**:

- Manual YAML only: High risk of drift from actual implementation
- Auto-generated only: Lacks context, requirements, and design rationale
- Postman collections: Good for testing, poor for documentation

---

## Technology Stack Validation

**Confirmed Technologies**:

- ✅ Django 5.2+ with Django REST Framework (backend API)
- ✅ PostgreSQL 17.5+ (data persistence)
- ✅ Vue 3 with TypeScript (frontend SPA)
- ✅ Element Plus (UI component library)
- ✅ Vite (frontend build tool)
- ✅ pytest + pytest-django (backend testing)
- ✅ Vitest (frontend unit testing)
- ✅ Cypress (E2E testing)
- ✅ Black (Python formatting, 119-char lines)
- ✅ ESLint (TypeScript/Vue linting)

**No Changes Needed**: Current stack fully supports all specification requirements.

---

## Implementation Risk Mitigation

| Risk                                 | Mitigation Strategy                                 | Success Metric                                  |
| ------------------------------------ | --------------------------------------------------- | ----------------------------------------------- |
| Breaking existing psalm viewing      | Write comprehensive tests before any changes        | All tests pass                                  |
| Topic admin removal causes data loss | Remove registration only, don't touch model or data | Psalm topic associations unchanged              |
| Range UI is unused                   | Mark as P2, implement only if user requests         | Analytics show 0 usage = success (low priority) |
| Test suite takes too long            | Parallel test execution, factory fixtures           | Test suite runs in <60 seconds                  |
| Spec doesn't match real requirements | **USER VALIDATION REQUIRED**                        | User approves plan before Phase 1               |

---

## Summary of Decisions

1. **Admin Interface**: Document usage patterns, create admin user guide, include in quickstart
2. **Range UI**: Path-based URLs, text input, new component, **P2 priority** (optional enhancement)
3. **Testing**: Test existing code comprehensively, test-first for new code, 90% coverage minimum
4. **Fixtures**: Keep database dump, add topic fixtures for tests, extract test sample
5. **API Docs**: Auto-generate with drf-spectacular, supplement with manual YAML

**All "NEEDS CLARIFICATION" items from plan.md are now resolved.**

**Next Phase**: Generate data-model.md, contracts/, and quickstart.md (Phase 1).

---

**Specification Status**: ✅ **Updated and aligned with implementation**. No code changes required except optional enhancements (range UI, comprehensive tests).
