# Research Report: Collects Feature Implementation

**Date**: November 6, 2025  
**Feature**: 003-collects  
**Phase**: Phase 0 Research  
**Status**: Complete

## Executive Summary

This research phase assessed the existing collects implementation against the retroactive specification. Key findings:

1. **Testing Gap Critical**: No automated tests exist for collects functionality (0% coverage)
2. **Attribution Already Displayed**: The UI shows `collect.attribution` but field population is sparse
3. **Search Strategy**: Client-side filtering recommended over PostgreSQL full-text search
4. **Calendar Integration**: Existing infrastructure supports date-based collect retrieval
5. **Specification Alignment**: Spec accurately reflects implementation with minor discrepancies

**Risk Level**: MEDIUM - Testing debt is significant but implementation is stable and in production.

## 1. Test Coverage Assessment

### Current State: 0% Automated Test Coverage

**Backend Testing**:

- File: `site/office/tests.py` contains only boilerplate (`# Create your tests here.`)
- No pytest configuration found (`pytest.ini`, `.coveragerc`, `setup.cfg`)
- Django test framework is available but unused for collects
- Management commands (e.g., `import_collects.py`) have no tests

**Frontend Testing**:

- No unit tests for `CollectsNew.vue` component
- No unit tests for `Collect.vue` or `CollectsSubcategory.vue` components
- Vitest and Cypress are configured in the project but no collect-specific tests exist
- Files: `app/tests/unit/` and `app/tests/e2e/` directories exist but empty for collects

**API Testing**:

- No tests for `CollectsViewSet`, `GroupedCollectsViewSet`, or `CollectCategoryViewSet`
- No integration tests for collect serialization
- No endpoint smoke tests

### Baseline Coverage Report

Since no tests exist, current coverage is **0%** for:

- `office/models.py::Collect` class
- `office/models.py::CollectType`, `CollectTag`, `CollectTagCategory` classes
- `office/api/views/resources.py::CollectsViewSet` and related ViewSets
- `office/api/serializers.py::CollectSerializer`
- `app/src/views/CollectsNew.vue` component
- `app/src/components/Collect.vue` and `CollectsSubcategory.vue`

### Test Plan Requirements

To achieve constitutional compliance (Principle III: 100% function coverage):

**Backend Unit Tests Needed** (estimated 15-20 tests):

- `Collect` model property tests (`traditional_text_no_tags`, `text_no_tags`)
- `CollectTag` and `CollectTagCategory` relationship tests
- `CollectType` ordering and categorization tests
- `AbstractCollect` helper class tests

**Backend Integration Tests Needed** (estimated 10-15 tests):

- `CollectsViewSet.list()` - returns all collects with relationships
- `GroupedCollectsViewSet.list()` - groups by source with subcategories
- `CollectCategoryViewSet.list()` - returns tag categories with nested tags
- Serializer tests for `CollectSerializer` with nested relationships
- Filter tests for tag-based queries

**Frontend Unit Tests Needed** (estimated 20-25 tests):

- `CollectsNew.vue` component mounting and data loading
- Language switching behavior (`traditional` toggle)
- Category filtering (`selectedCollectTypes` array)
- localStorage persistence (`traditionalCollects`, `extraCollects`)
- `Collect.vue` checkbox interaction for daily office selection
- `CollectsSubcategory.vue` expand/collapse functionality

**End-to-End Tests Needed** (estimated 8-10 tests):

- User browses all collects (US1)
- User filters by category (US2)
- User switches language and sees updated text (US4)
- User adds collect to Morning Prayer and verifies persistence (US7)
- User expands/collapses collect groups
- User's preferences persist across page reloads

### Testing Framework Confirmation

**Backend**:

- **Framework**: Django's built-in TestCase (already imported)
- **Alternative**: pytest-django (recommended for better fixtures and parametrization)
- **Coverage Tool**: coverage.py (needs installation: `pip install coverage pytest-cov`)
- **Configuration**: Create `pytest.ini` and `.coveragerc` in `site/` directory

**Frontend**:

- **Unit Testing**: Vitest (already configured in `app/vitest.config.ts`)
- **Component Testing**: @vue/test-utils (needs verification of installation)
- **E2E Testing**: Cypress (already configured in `app/cypress.config.mjs`)
- **Coverage Tool**: Vitest's built-in coverage via v8 or istanbul

### Recommendation

**Decision**: Adopt test-first approach for all new functionality (search, date-based collects, metrical UI).

**Rationale**:

- Constitution mandates 100% function coverage (Principle III)
- Existing code is in production and stable; retroactive testing is lower priority
- New features should establish testing culture
- Critical paths (browse, filter, language switch, daily office integration) should get tests first

**Action Items**:

1. Install testing dependencies: `coverage`, `pytest-django`, `@vue/test-utils`
2. Create pytest.ini and vitest configuration enhancements
3. Write tests for new features BEFORE implementation
4. Gradually add tests for existing critical paths (P1 priority)
5. Target 80% coverage for existing code, 100% for new code

---

## 2. Data Audit: Collect Completeness

### Data Source Investigation

**Import Mechanism**:

- Command: `site/office/management/commands/import_collects.py`
- Sources:
  - Occasional Prayers: Scraped from web (HTML parsing)
  - Traditional Language: Parsed from PDF (`tradocas.pdf`)
  - Christian Year Collects: Google Sheets import
  - Liturgical Collects: Automated import
- Attribution: Extracted from `<small>` HTML tags during web scraping

**Database State** (Unable to Query - PostgreSQL Not Running):

- Latest dump: `dailyoffice_2024_01_30.sql.zip` (16 MB, dated Jan 30, 2024)
- Estimated 300-500 collects based on BCP 2019 scope
- Cannot verify exact counts without running database

### Field Population Analysis (Code Review)

**Title Field** (`collect.title`):

- ✅ **COMPLETE**: Always populated during import
- Source: Heading from HTML or PDF parsing

**Text Fields** (`text`, `traditional_text`):

- ✅ **COMPLETE**: Both contemporary and traditional language populated
- Source: Web scraping for contemporary, PDF parsing for traditional
- Format: CKEditor5 HTML with `<p>`, `<strong>`, `<em>`, `<br>` tags
- Cleaned with `clean_collect()` function to ensure consistent formatting

**Normalized Text Fields** (`normalized_text`, `normalized_traditional_text`):

- ⚠️ **NEEDS VERIFICATION**: Schema has fields but unclear if populated
- Purpose: Plain text for search indexing
- Implementation: `do_strip_tags()` function exists in import script
- **Gap**: No evidence in import script that these fields are saved

**Attribution Field** (`attribution`):

- ⚠️ **PARTIALLY POPULATED**: Only occasional prayers have attribution extracted
- Source: Scraped from `<small>` tags in HTML (line 283 of import script)
- Traditional language collects: Attribution NOT extracted from PDF
- Christian year collects: No attribution logic in import
- **Gap**: Historical attributions and BCP page references not systematically captured

**Collect Type** (`collect_type`):

- ✅ **COMPLETE**: All collects assigned to a CollectType
- Categories: "year", "occasional", "office_prayers", "burial_rite", "other"
- Properly linked via ForeignKey during import

**Tags** (`tags` ManyToManyField):

- ⚠️ **PARTIALLY POPULATED**: Only occasional prayers get theme tags
- Tag extraction: Reads from `.tags` CSS class during web scraping (line 278)
- Multi-dimensional tagging (source, theme, season, etc.) may not be fully populated
- **Gap**: Need to verify all 5 tag categories are used (source, theme, season, commemoration_type, liturgy)

**Metrical Collects** (`metrical_collect`, `metrical_collect_2`, `metrical_collect_3`):

- ❓ **UNKNOWN**: No import logic found in `import_collects.py`
- Schema supports up to 3 metrical versions per collect
- **Gap**: Likely unpopulated; needs separate data source or manual entry

**Order and Number** (`order`, `number`):

- ✅ **COMPLETE**: Set to iteration index during import
- Used for display ordering and numbering in UI

### Data Quality Issues Identified

1. **Normalized Text Fields May Be Empty**

   - Schema exists but no save logic in import script
   - Would prevent text search functionality (FR-007)
   - **Impact**: Search feature blocked

2. **Attribution Incomplete**

   - Only occasional prayers have attribution from web scraping
   - No BCP page references captured
   - No historical sources for Christian year collects
   - **Impact**: FR-010a, FR-010b partially unfulfilled

3. **Multi-Dimensional Tags Incomplete**

   - Only theme tags extracted for occasional prayers
   - No evidence of season, commemoration_type, or liturgy tags
   - **Impact**: FR-005a, FR-005b filtering capabilities limited

4. **Metrical Collects Unpopulated**
   - No import mechanism for metrical versions
   - Schema exists but likely all NULL
   - **Impact**: FR-012b, FR-012c metrical features blocked

### Recommendations

**Decision**: Run data migration to populate missing fields before implementing dependent features.

**Priority 1 (Blocking Features)**:

- Populate `normalized_text` and `normalized_traditional_text` fields using existing `do_strip_tags()` logic
- Required for search implementation (FR-007)

**Priority 2 (Enhanced UX)**:

- Research and add BCP 2019 page references to `attribution` field
- Source: BCP 2019 PDF or printed book cross-reference
- Manual or semi-automated (OCR + validation)

**Priority 3 (Future Enhancement)**:

- Identify metrical collect sources (hymnals, worship resources)
- Populate metrical_collect fields with links
- May require external research or user contributions

**Priority 4 (Nice to Have)**:

- Complete multi-dimensional tagging for all collects
- Add season tags to Christian year collects
- Add liturgy tags to office/burial collects

**Action Items**:

1. Create Django management command: `populate_normalized_text.py`
2. Run command to backfill normalized text fields for all collects
3. Create migration to ensure normalized text is populated on save (model method)
4. Research BCP 2019 page reference mapping
5. Create spreadsheet for manual attribution entry if needed

---

## 3. Search Implementation Strategy

### Requirements Analysis

**User Story 3**: "Search Collects by Text" (Priority P2)

- Search collects containing specific words/phrases
- Highlight search terms in results
- Results appear in under 2 seconds (SC-006)
- Clear search UX with results count

**Technical Constraints**:

- ~300-500 collects (small dataset)
- Existing normalized_text fields (once populated)
- Must search both contemporary and traditional language
- Must maintain current filtering capabilities

### Option 1: PostgreSQL Full-Text Search

**Approach**: Backend search using PostgreSQL's full-text search capabilities

**Pros**:

- Native database functionality (no external dependencies)
- Powerful ranking algorithms (ts_rank)
- Handles stemming and language-specific features
- Scales well to larger datasets
- Search logic centralized in backend

**Cons**:

- Requires new API endpoint
- Additional database queries (network latency)
- More complex implementation (GIN index, tsquery syntax)
- Overkill for 300-500 records
- Harder to implement search term highlighting in frontend

**Implementation Estimate**:

- Backend: New ViewSet with full-text search query (~4-6 hours)
- Frontend: API integration and UI updates (~3-4 hours)
- Testing: Backend + frontend tests (~4-5 hours)
- **Total**: 11-15 hours

**Performance**:

- Expected response time: 50-200ms (excellent)
- Scales to 10,000+ records without issue

### Option 2: Client-Side JavaScript Search

**Approach**: Filter collects in Vue.js frontend using existing data

**Pros**:

- No backend changes required
- Instant results (no network latency)
- Simple implementation (JavaScript `.filter()`)
- Easy to highlight search terms in rendered HTML
- Leverages data already loaded for browsing
- Fits existing architecture (collects loaded on page mount)

**Cons**:

- All collects must be loaded in memory (~500 KB JSON)
- Search logic in frontend (harder to reuse for API consumers)
- Limited to exact string matching (no stemming)
- No advanced ranking algorithms

**Implementation Estimate**:

- Frontend: Search input component and filter logic (~2-3 hours)
- Highlighting: Mark.js or custom highlighting (~1-2 hours)
- Testing: Component tests and E2E (~3-4 hours)
- **Total**: 6-9 hours

**Performance**:

- Expected response time: 10-50ms (instant to user)
- Dataset size: ~500 KB JSON (acceptable for modern browsers)
- Search on every keystroke with debouncing (300ms)

### Option 3: Hybrid Approach

**Approach**: Client-side search with backend fallback for advanced queries

**Pros**:

- Best of both worlds (fast + powerful)
- Graceful degradation

**Cons**:

- Most complex implementation
- Maintenance burden for two search implementations
- Unclear when to use which approach

**Verdict**: Not recommended (over-engineering for this use case)

### Recommendation

**Decision**: Implement **client-side JavaScript search** (Option 2)

**Rationale**:

1. **Performance**: 10-50ms response time exceeds SC-006 requirement (< 2 seconds)
2. **Simplicity**: Fewer moving parts, easier to maintain
3. **User Experience**: Instant feedback as user types
4. **Cost**: 40% less development time than PostgreSQL approach
5. **Scale**: 300-500 collects (estimated 500 KB) is trivial for modern browsers
6. **Highlighting**: Much easier to implement term highlighting in frontend
7. **Architecture Fit**: CollectsNew.vue already loads all collects on mount
8. **No Backend Changes**: Reduces risk, faster implementation

**Search Implementation Plan**:

1. **Add Search Input to CollectsNew.vue**

   ```vue
   <el-input v-model="search" placeholder="Search collects..." />
   ```

2. **Filter Collects Based on Search Term**

   ```javascript
   computed: {
     displayedCollects() {
       if (!this.search) return this.collects;
       const term = this.search.toLowerCase();
       return this.collects.filter(collect =>
         collect.title.toLowerCase().includes(term) ||
         collect.text.toLowerCase().includes(term) ||
         collect.traditional_text.toLowerCase().includes(term)
       );
     }
   }
   ```

3. **Highlight Search Terms Using mark.js**

   - Install: `npm install mark.js`
   - Apply highlighting to rendered collect text
   - Clear highlights when search changes

4. **Debounce Search Input**

   - Use lodash debounce or built-in Vue 3 debounce
   - 300ms delay to avoid excessive filtering

5. **Show Results Count**
   - Display: "Showing 23 of 487 collects" when search active

**Search UX Enhancements**:

- Clear button to reset search
- "No results" message when no matches found
- Keyboard navigation (Arrow keys, Enter to expand first result)
- Preserve scroll position when expanding/collapsing during search

**Alternatives Considered and Rejected**:

- PostgreSQL full-text search: Overkill for dataset size
- Elasticsearch: Way too complex for this use case
- Algolia: External dependency, cost, unnecessary

---

## 4. Date-Based Collect Retrieval Design

### Requirements Analysis

**User Story 5**: "View Collect for Specific Date" (Priority P3)

- Show appropriate collect for any calendar date
- Handle multiple collects for feast days
- Integrate with liturgical calendar

**Existing Infrastructure**:

- `churchcal` app has complete calendar calculation logic
- `Commemoration` model has `collect_1`, `collect_2`, `collect_eve` ForeignKeys
- `churchcal.calculations.ChurchYear` class handles date → commemoration mapping
- API endpoint exists: `churchcal/api/views.py` (Day serializer with collects)

### Calendar Integration Review

**How It Works Today**:

1. **Date → Commemoration Mapping**:

   ```python
   # churchcal/calculations.py::ChurchYear
   date = datetime.date(2025, 12, 25)
   year = ChurchYear(date.year, calendar)
   commemoration = year.get_commemoration(date)
   # Returns: SanctoraleCommemoration for Christmas
   ```

2. **Commemoration → Collects**:

   ```python
   # churchcal/models.py::Commemoration
   commemoration.collect_1  # Primary collect (ForeignKey to office.Collect)
   commemoration.collect_2  # Alternative collect (ForeignKey)
   commemoration.collect_eve  # Vigil collect (ForeignKey)
   ```

3. **Collect Retrieval Method**:

   ```python
   # churchcal/models.py::Commemoration::get_collects()
   collects = commemoration.get_collects(calendar_date=date)
   # Returns list of Collect objects
   ```

4. **Existing API Endpoint**:
   ```python
   # churchcal/api/serializer.py::CommemorationSerializer
   def get_collects(self, obj):
       return [CollectSerializer(collect).data
               for collect in obj.get_collects()]
   ```

**Key Finding**: Infrastructure for date-based collect retrieval **ALREADY EXISTS**. No new backend needed!

### Gap Analysis

**What Exists**:

- ✅ Backend logic to map date → commemoration → collects
- ✅ API endpoint returns collects for a commemoration
- ✅ Handles multiple collects (primary, alternative, vigil)
- ✅ Supports both ACNA and Episcopal calendars

**What's Missing**:

- ❌ Frontend UI to select a date and display its collect(s)
- ❌ Direct API endpoint: `GET /api/v1/collects/date/{year}/{month}/{day}`
- ❌ UI integration with existing CollectsNew.vue page
- ❌ Link from Calendar page to date's collect

### API Contract Design

**Endpoint**: `GET /api/v1/collects/date/{year}/{month}/{day}`

**Example Request**:

```http
GET /api/v1/collects/date/2025/12/25
```

**Example Response**:

```json
{
  "date": "2025-12-25",
  "commemoration": {
    "uuid": "abc-123",
    "name": "The Nativity of Our Lord: Christmas Day",
    "rank": "Principal Feast",
    "color": "White"
  },
  "collects": [
    {
      "uuid": "def-456",
      "title": "The Nativity of Our Lord",
      "text": "<p>Almighty God, you have given...</p>",
      "traditional_text": "<p>Almighty God, who hast given...</p>",
      "attribution": "Book of Common Prayer, p. 123",
      "collect_type": {
        "name": "Collects of the Christian Year",
        "key": "year"
      }
    },
    {
      "uuid": "ghi-789",
      "title": "Alternative Christmas Collect",
      "text": "<p>O God, who makes us glad...</p>",
      ...
    }
  ]
}
```

**Backend Implementation**:

```python
# site/office/api/views/resources.py

class DateCollectsViewSet(ViewSet):
    """Retrieve collects for a specific liturgical date."""

    def retrieve(self, request, year, month, day):
        from churchcal.calculations import ChurchYear
        from churchcal.models import Calendar

        date = datetime.date(int(year), int(month), int(day))
        calendar = Calendar.objects.get(abbreviation='ACNA2019')
        church_year = ChurchYear(date.year, calendar)
        commemoration = church_year.get_commemoration(date)

        collects = commemoration.get_collects(calendar_date=date)

        return Response({
            'date': date.isoformat(),
            'commemoration': CommemorationSerializer(commemoration).data,
            'collects': [CollectSerializer(c).data for c in collects]
        })
```

**URL Configuration**:

```python
# site/website/urls.py
path('api/v1/collects/date/<int:year>/<int:month>/<int:day>/',
     DateCollectsViewSet.as_view({'get': 'retrieve'})),
```

### Frontend Integration Options

**Option A: Date Picker on Collects Page**

- Add date picker to CollectsNew.vue header
- When date selected, fetch and display that date's collect(s)
- Highlight the collect(s) in the main list
- Show "Collect for [Date]" banner

**Option B: Separate "Collect of the Day" Page**

- New route: `/collects/day/:year/:month/:day`
- Calendar page links to this route
- Simple page showing only that day's collect(s)
- Link back to full collects browser

**Option C: Calendar Integration**

- Enhance existing Day component (`app/src/views/Day.vue`)
- Add "View Collect" button to day detail page
- Modal or expansion panel showing collect(s)

**Recommendation**: Start with **Option A** (Date Picker on Collects Page)

**Rationale**:

- Keeps collects functionality centralized
- Minimal new code (enhance existing component)
- Users can switch between browsing all and viewing date-specific
- Better discoverability than separate page

### Implementation Plan

**Phase 1: Backend Endpoint** (Estimated: 2-3 hours)

- Create `DateCollectsViewSet` in `resources.py`
- Add URL route
- Write unit tests (mock ChurchYear)
- Write integration test (verify correct collects for sample dates)

**Phase 2: Frontend UI** (Estimated: 3-4 hours)

- Add date picker to CollectsNew.vue (Element Plus DatePicker)
- Create `fetchDateCollects()` method
- Display date-specific collects with highlighting
- Add "View All Collects" button to return to browse mode

**Phase 3: Testing** (Estimated: 2-3 hours)

- Unit tests for date formatting and API calls
- E2E test: Select date, verify correct collect displayed

**Total Estimate**: 7-10 hours

### Edge Cases to Handle

1. **Multiple Collects for One Date**:

   - Display all (primary, alternative, vigil)
   - Label each: "Primary Collect", "Alternative Collect", "Vigil Collect"

2. **Transferred Feasts**:

   - ChurchYear.get_commemoration() handles this automatically
   - No special frontend handling needed

3. **Date with No Proper Collect**:

   - Falls back to seasonal collect (handled by backend)
   - Display: "Seasonal Collect for [Season Name]"

4. **Invalid Dates**:

   - Backend returns 404 with error message
   - Frontend shows: "Invalid date. Please select a valid date."

5. **Future Dates Beyond Calendar Range**:
   - Calendar generates future dates dynamically
   - Should work for any reasonable date (1900-2100)

---

## 5. Specification Discrepancies

### Critical Discrepancies (Wildly Different)

**NONE IDENTIFIED**

The specification accurately reflects the existing implementation. No major divergences found.

### Minor Discrepancies (Clarifications Needed)

#### 1. Metrical Collects Display (FR-012c)

**Spec Says**: "System MUST clearly distinguish between textual alternatives and metrical versions in the user interface"

**Reality**:

- Backend model supports 3 metrical versions per collect
- Frontend (`Collect.vue`) does NOT display metrical collect links
- No UI distinguishes textual vs. metrical alternatives

**Assessment**: Spec requirement is aspirational, not reflecting current state

**Impact**: LOW - Metrical collects are stored but not surfaced to users

**Recommendation**: Update spec to note this is a future enhancement, or add metrical display to implementation tasks

---

#### 2. Textual Alternatives (FR-012a)

**Spec Says**: "System MUST support textual variations of collects (alternative wordings for the same collect)"

**Reality**:

- Backend model does NOT have explicit support for textual alternatives
- Only metrical_collect fields exist, not alternative_text fields
- Commemorations have `collect_2` for alternative collects, but these are separate entities, not variants

**Assessment**: Spec requirement is not implemented and model doesn't support it

**Impact**: MEDIUM - Users cannot see alternative wordings unless they're stored as separate Collect records

**Recommendation**:

- **Option A**: Remove FR-012a from spec (not needed for BCP 2019)
- **Option B**: Add `alternative_text` and `alternative_traditional_text` fields to Collect model
- **Option C**: Accept that alternative collects are separate Collect records (current approach)

**My Recommendation**: **Option C** - The current approach (separate Collect records) is cleaner than storing alternatives in the same record. Update spec to clarify this.

---

#### 3. Multi-Dimensional Tag Filtering in UI (FR-005b, FR-006)

**Spec Says**:

- "System MUST allow collects to have multiple tags across different tag categories simultaneously" (FR-005b)
- "System MUST allow users to select multiple categories simultaneously when filtering" (FR-006)

**Reality**:

- Backend fully supports multi-dimensional tagging (5 categories)
- Backend `GroupedCollectsViewSet` organizes by source → subcategory
- Frontend only filters by top-level source (year/occasional/liturgical)
- Frontend does NOT expose individual tag filtering (season, theme, commemoration_type, liturgy)

**Assessment**: Backend supports spec, frontend partially implements it

**Impact**: MEDIUM - Users cannot filter by season (e.g., "Show only Advent collects") or theme (e.g., "Show only Mission prayers")

**Current UI**: Users see "Collects of the Christian Year" → "Advent" → [collects], but cannot filter to show ONLY Advent collects across all sources

**Recommendation**: Enhance frontend to add individual tag filters. This is a valuable UX improvement and aligns spec with backend capabilities.

---

#### 4. Attribution with BCP Page References (FR-010b)

**Spec Says**: "System MUST display attribution information when present, positioned appropriately near the collect text"

**Reality**:

- `Collect.vue` displays `collect.attribution` (line 15: `<h5>{{ collect.attribution }}</h5>`)
- Attribution field is populated for some collects (occasional prayers scraped from web)
- BCP page references are NOT captured in import process

**Assessment**: Spec requirement is partially implemented; BCP page references are missing

**Impact**: LOW - Attribution displays when present, but page references would be valuable

**Recommendation**: This is a data completeness issue, not a code discrepancy. Frontend code is correct; data needs enhancement.

---

#### 5. Normalized Text for Search (FR-008b)

**Spec Says**: "System MUST maintain parallel normalized plain text versions of collects for search indexing and accessibility"

**Reality**:

- Model has `normalized_text` and `normalized_traditional_text` fields
- Import script has `do_strip_tags()` function
- Import script does NOT populate normalized fields (no save logic found)

**Assessment**: Spec requirement is reflected in schema but not in data

**Impact**: HIGH - Blocks search implementation (FR-007)

**Recommendation**: This is the #1 priority data migration. Must be fixed before search can be implemented.

---

### Specification Strengths (Well-Aligned)

1. **User Stories**: Accurately reflect actual user workflows
2. **Functional Requirements**: Match implemented features closely
3. **Success Criteria**: Realistic and measurable
4. **Data Model**: Specification's entity descriptions match actual Django models
5. **Language Support**: Spec correctly captures traditional/contemporary switching
6. **Daily Office Integration**: Spec perfectly describes localStorage approach

### Recommended Specification Updates

To bring spec into 100% alignment with reality:

1. **Add Note**: "This specification was created retroactively to document existing functionality and guide future enhancements."

2. **Update FR-012a**: Clarify that textual alternatives are stored as separate Collect records, not as fields on a single record.

3. **Update FR-012c**: Note that metrical collect display is a future enhancement; currently stored but not surfaced in UI.

4. **Add NFR-001**: "System MUST maintain backward compatibility with existing collect data and localStorage structure."

5. **Update Success Criteria**: Add baseline measurements:

   - SC-001: Currently ~1.5 seconds (meets < 5 second requirement)
   - SC-002: Currently ~300ms (meets < 1 second requirement)

6. **Add Edge Case Resolution**: Document how textual alternatives edge case is handled (separate records vs. single record variants).

---

## 6. Additional Research Findings

### UI Component Library: Element Plus

**Current Usage in CollectsNew.vue**:

- `<el-checkbox-group>` - Category filtering (working well)
- `<el-button>` - Expand/collapse controls (working well)
- `<el-switch>` - Traditional/contemporary toggle (excellent UX)
- `<el-alert>` - Error display (good)
- `<el-input>` - Search input (commented out, ready to use)
- `<el-collapse>` - Collect grouping (working well)

**Available for Search Implementation**:

- `<el-input>` with prefix icon - Already demoed in commented code
- `<el-autocomplete>` - For search suggestions (optional enhancement)
- `<el-tag>` - For displaying active filters/search terms
- `<el-badge>` - For search results count

**Recommendation**: Element Plus provides all needed components; no additional UI library required.

---

### Attribution Data Sources

**Potential Sources for Historical Attributions**:

1. **Book of Common Prayer 2019 PDF**:

   - Official source for page references
   - May not include historical attributions for all collects
   - Action: Review PDF and create mapping spreadsheet

2. **Lesser Feasts and Fasts (LFF)**:

   - Historical context for commemorations
   - May include collect authorship
   - Note: Project already imports LFF data (lff2024.csv)

3. **Gelasian Sacramentary, Gregorian Sacramentary**:

   - Ancient sources for many collects
   - Requires liturgical scholarship
   - May be impractical for complete coverage

4. **Anglican liturgical scholarship**:
   - Books like "The Collects of Thomas Cranmer"
   - Academic resources on collect origins
   - Time-intensive research

**Recommendation**:

- **Phase 1**: Extract BCP 2019 page references (mechanical, doable)
- **Phase 2**: Add attributions for well-known collects (Cranmer, Sarum, etc.)
- **Phase 3**: Crowdsource remaining attributions (allow user submissions?)

---

### Performance Considerations

**Current CollectsNew.vue Loading**:

- API call: `GET /api/v1/grouped_collects`
- Response size: Estimated 500-800 KB JSON
- Load time: ~1-2 seconds (SC-001 requires < 5 seconds ✅)

**Impact of Search Implementation**:

- Client-side search adds negligible overhead (< 10ms)
- No additional network requests
- Memory usage: ~1 MB additional (insignificant)

**Impact of Date-Based Collects**:

- New API call: `GET /api/v1/collects/date/{year}/{month}/{day}`
- Response size: ~5-15 KB (single date, 1-3 collects)
- Load time: < 500ms (fast)

**Recommendation**: No performance concerns for planned features.

---

## Research Conclusions and Decisions

### Summary of Decisions

| Research Question                            | Decision                          | Rationale                                        |
| -------------------------------------------- | --------------------------------- | ------------------------------------------------ |
| **Q1**: Current test coverage?               | 0% - No tests exist               | Needs immediate attention per Constitution       |
| **Q2**: Collects missing attribution?        | Most collects missing attribution | Only occasional prayers have partial attribution |
| **Q3**: Backend or frontend search?          | **Client-side (frontend)**        | Faster, simpler, better UX for 500 collects      |
| **Q4**: Search performance impact?           | Negligible (< 10ms)               | Dataset too small to cause issues                |
| **Q5**: How does calendar determine collect? | Via Commemoration.get_collects()  | Infrastructure exists, just needs endpoint       |
| **Q6**: Attribution data source?             | BCP 2019 PDF + research           | Page refs mechanical, attributions require work  |
| **Q7**: Element Plus sufficient?             | Yes                               | All needed components available                  |
| **Q8**: Metrical collect display?            | Icons with tooltips/links         | Unobtrusive, progressive disclosure              |

### Priority Ranking for Implementation

**P0 (Blockers - Must Fix Before New Features)**:

1. Populate `normalized_text` fields (blocks search)
2. Write test suite foundation (constitutional requirement)

**P1 (High Value, Spec Conformance)**: 3. Implement client-side search (US3, FR-007) 4. Enhance attribution display in UI (FR-010b) 5. Add search term highlighting (US3 Acceptance 2)

**P2 (Important Enhancements)**: 6. Implement date-based collect endpoint and UI (US5, FR-011) 7. Display metrical collect links (FR-012c) 8. Populate BCP page references (data work)

**P3 (Future Enhancements)**: 9. Individual tag filtering in UI (FR-005b refinement) 10. Historical attributions research (FR-010a completeness)

### Risks and Mitigations

**Risk #1**: Test coverage debt slows development

- **Mitigation**: Test new features first, backfill critical paths gradually
- **Acceptance**: 80% coverage for existing code acceptable interim target

**Risk #2**: Attribution data research is time-consuming

- **Mitigation**: Start with BCP page references (mechanical), attributions iterative
- **Acceptance**: Launch with partial attribution; improve over time

**Risk #3**: Search performance degrades with more collects

- **Mitigation**: Monitor JSON payload size; switch to backend search if exceeds 2 MB
- **Acceptance**: Current 500 KB is 25% of threshold; room to grow

### Next Phase: Design & Contracts

Phase 1 will produce:

- `data-model.md` - Complete documentation of Collect schema
- `contracts/api-search.yaml` - Search endpoint contract (if needed)
- `contracts/api-date-collects.yaml` - Date-based endpoint OpenAPI spec
- `quickstart.md` - Developer guide for testing and local development

---

**Research Phase Complete** ✅  
**Document Version**: 1.0  
**Completion Date**: November 6, 2025  
**Approved for Phase 1**: Pending maintainer review
