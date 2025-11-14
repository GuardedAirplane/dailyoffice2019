# Search Implementation Strategy

**Feature**: 003-collects  
**Date**: November 6, 2025  
**Decision**: Client-Side Search (No Backend API)

## Overview

This document defines the implementation contract for collects search functionality. Based on research (see `research.md`), search will be implemented **client-side** using JavaScript filtering, not as a backend API endpoint.

## Decision Rationale

**Client-side search was chosen over backend search** for the following reasons:

1. **Performance**: 10-50ms response time vs 200ms+ for API calls
2. **Simplicity**: Fewer moving parts, easier maintenance
3. **User Experience**: Instant feedback as user types
4. **Dataset Size**: ~500 collects (~500 KB JSON) is trivial for modern browsers
5. **Development Cost**: 40% less implementation time (6-9 hours vs 11-15 hours)
6. **Highlighting**: Much easier to implement search term highlighting in DOM
7. **Architecture Fit**: CollectsNew.vue already loads all collects on mount

See `research.md` Section 3 for complete analysis.

## Requirements

### Functional Requirements

**From Specification**:

- **FR-007**: System MUST provide text search functionality to find collects containing specific words or phrases
- **FR-008b**: System MUST maintain parallel normalized plain text versions of collects for search indexing
- **US3 Acceptance 1**: Search collects containing term in title or text
- **US3 Acceptance 2**: Highlight search term in results
- **US3 Acceptance 3**: Clear search to return to full collection
- **SC-006**: Search results appear in under 2 seconds

### Non-Functional Requirements

- **Performance**: Search must complete in < 100ms for 500 collects
- **Responsiveness**: Search input must debounce to avoid excessive filtering (300ms)
- **Accessibility**: Search must work with keyboard navigation and screen readers
- **Mobile**: Search must work on mobile devices (touch-friendly)

## Implementation Contract

### Data Requirements

**CRITICAL PREREQUISITE**: `normalized_text` and `normalized_traditional_text` fields MUST be populated.

**Current State**: Fields exist in schema but are empty (see `research.md` Section 2).

**Fix Required Before Search Implementation**:

```bash
# Run data migration to populate normalized text
python manage.py populate_normalized_text
```

### Frontend Component Structure

#### 1. Search Input Component

**Location**: `app/src/views/CollectsNew.vue` (integrated into existing component)

**HTML Structure**:

```vue
<template>
  <div class="search-container">
    <el-input
      v-model="searchTerm"
      placeholder="Search collects by title or text..."
      clearable
      @input="onSearchInput"
      @clear="clearSearch"
    >
      <template #prefix>
        <el-icon><Search /></el-icon>
      </template>
    </el-input>

    <div v-if="searchTerm" class="search-results-count">
      Showing {{ filteredCollects.length }} of {{ totalCollects }} collects
    </div>
  </div>
</template>
```

**Props**: None (uses component data)

**Data**:

```javascript
data() {
  return {
    searchTerm: '',  // User input
    searchDebounceTimeout: null,  // Debounce timer
  }
}
```

**Computed Properties**:

```javascript
computed: {
  filteredCollects() {
    if (!this.searchTerm) {
      return this.displayedCollects;  // No search, show filtered by category
    }

    const term = this.searchTerm.toLowerCase().trim();

    return this.displayedCollects.filter(collect => {
      // Search in title
      if (collect.title.toLowerCase().includes(term)) {
        return true;
      }

      // Search in contemporary text
      const searchableText = this.traditional
        ? (collect.normalized_traditional_text || collect.traditional_text)
        : (collect.normalized_text || collect.text);

      return searchableText.toLowerCase().includes(term);
    });
  },

  totalCollects() {
    return this.collects.length;
  }
}
```

**Methods**:

```javascript
methods: {
  onSearchInput(value) {
    // Debounce search to avoid excessive filtering
    clearTimeout(this.searchDebounceTimeout);
    this.searchDebounceTimeout = setTimeout(() => {
      this.searchTerm = value;
    }, 300);  // 300ms debounce
  },

  clearSearch() {
    this.searchTerm = '';
  }
}
```

---

#### 2. Search Term Highlighting

**Library**: `mark.js` (https://markjs.io/)

**Installation**:

```bash
cd app
npm install mark.js
```

**Integration**:

```javascript
import Mark from "mark.js";

export default {
  // ... other options

  watch: {
    searchTerm(newTerm, oldTerm) {
      this.$nextTick(() => {
        this.highlightSearchTerm();
      });
    },
  },

  methods: {
    highlightSearchTerm() {
      const context = document.querySelector("#collects-content");
      const marker = new Mark(context);

      // Clear previous highlights
      marker.unmark();

      // Apply new highlights
      if (this.searchTerm) {
        marker.mark(this.searchTerm, {
          separateWordSearch: false,
          accuracy: "partially",
          className: "search-highlight",
          ignoreCase: true,
        });
      }
    },
  },
};
```

**CSS for Highlighting**:

```scss
.search-highlight {
  background-color: #ffeb3b; // Yellow highlight
  color: #000;
  font-weight: 600;
  padding: 2px 0;
  border-radius: 2px;
}

// Ensure good contrast in dark mode
@media (prefers-color-scheme: dark) {
  .search-highlight {
    background-color: #ffd54f;
    color: #000;
  }
}
```

---

#### 3. Search Results Display

**Integration with Existing Structure**:

The `filteredCollects` computed property replaces `displayedCollects` in the template:

**Before** (current implementation):

```vue
<div v-for="category in collectCategoriesToShow" :key="category.uuid">
  <h3>{{ category.name }}</h3>
  <div v-for="subcategory in category.subcategories" :key="subcategory.uuid">
    <CollectsSubcategory :subcategory="subcategory" ... />
  </div>
</div>
```

**After** (with search integration):

```vue
<div v-if="searchTerm" class="search-results">
  <!-- Flat list when searching -->
  <h3>Search Results ({{ filteredCollects.length }})</h3>
  <el-collapse v-model="openedItems">
    <Collect
      v-for="collect in filteredCollects"
      :key="collect.uuid"
      :collect="collect"
      :traditional="traditional"
      :extra-collects="extraCollects"
      @extra-collects-changed="setExtraCollects"
    />
  </el-collapse>
</div>

<div v-else>
  <!-- Normal category browsing when not searching -->
  <div v-for="category in collectCategoriesToShow" :key="category.uuid">
    <!-- ... existing structure ... -->
  </div>
</div>
```

---

#### 4. Empty Results Handling

**Template Addition**:

```vue
<div v-if="searchTerm && filteredCollects.length === 0" class="no-results">
  <el-empty description="No collects match your search">
    <el-button type="primary" @click="clearSearch">Clear Search</el-button>
  </el-empty>
</div>
```

**CSS**:

```scss
.no-results {
  padding: 40px;
  text-align: center;

  .el-empty {
    margin: 40px 0;
  }
}
```

---

### Search Algorithm

#### 1. Basic String Matching

**Algorithm**: Case-insensitive substring match

**Fields Searched**:

1. `collect.title` (always)
2. `collect.normalized_text` (if contemporary language selected)
3. `collect.normalized_traditional_text` (if traditional language selected)
4. Fallback to HTML fields if normalized fields empty (during transition)

**Pseudocode**:

```javascript
function matchesSearch(collect, searchTerm, useTraditional) {
  const term = searchTerm.toLowerCase().trim();

  // Search title
  if (collect.title.toLowerCase().includes(term)) {
    return true;
  }

  // Select appropriate text field
  const textField = useTraditional
    ? collect.normalized_traditional_text || collect.traditional_text
    : collect.normalized_text || collect.text;

  // Search text (case-insensitive)
  return textField.toLowerCase().includes(term);
}
```

---

#### 2. Performance Optimization

**Technique**: Debouncing

**Implementation**:

```javascript
// Debounce search input to avoid filtering on every keystroke
const DEBOUNCE_DELAY = 300; // milliseconds

onSearchInput(value) {
  clearTimeout(this.searchDebounceTimeout);
  this.searchDebounceTimeout = setTimeout(() => {
    this.searchTerm = value;
  }, DEBOUNCE_DELAY);
}
```

**Why 300ms?**

- Balances responsiveness vs. performance
- User typically types 4-5 chars/second
- Reduces filter calls by ~80%

---

#### 3. Filter Interaction

**Question**: What happens when user has category filters AND search active?

**Answer**: Search applies to already-filtered results (logical AND).

**Example**:

```javascript
computed: {
  displayedCollects() {
    // Step 1: Filter by selected categories
    let collects = this.collects.filter(collect => {
      return this.selectedCollectTypes.includes(collect.collect_type.uuid);
    });

    // Step 2: Apply search filter (if active)
    if (this.searchTerm) {
      const term = this.searchTerm.toLowerCase();
      collects = collects.filter(collect => this.matchesSearch(collect, term));
    }

    return collects;
  }
}
```

**User Flow**:

1. User filters to "Occasional Prayers" → 200 collects shown
2. User searches "mission" → 15 collects shown (from the 200)
3. User clears search → Back to 200 collects
4. User clears category filter → All collects shown again

---

### Edge Cases and Error Handling

#### 1. Special Characters in Search

**Scenario**: User searches for `"God's mercy"`

**Handling**:

- Smart quotes (`'`, `"`) should be normalized to straight quotes (`'`, `"`)
- Both versions should match (normalize input and text)

**Implementation**:

```javascript
function normalizeText(text) {
  return text
    .replace(/[\u2018\u2019]/g, "'") // Smart single quotes
    .replace(/[\u201C\u201D]/g, '"') // Smart double quotes
    .toLowerCase();
}
```

---

#### 2. Empty Search Term

**Scenario**: User clears search (empty string or whitespace only)

**Handling**: Show all collects (no filtering)

```javascript
if (!searchTerm || searchTerm.trim() === "") {
  return this.collects; // No filter
}
```

---

#### 3. Search with No Results

**Scenario**: User searches for `"xyz123"` (term not in any collect)

**Handling**:

- Display: "No collects match your search"
- Provide "Clear Search" button
- Do NOT reset category filters

**See Section 4 above** for template implementation.

---

#### 4. Missing Normalized Text

**Scenario**: `normalized_text` field is NULL or empty (during migration period)

**Handling**: Fallback to HTML fields (slower but functional)

```javascript
const searchableText = this.traditional
  ? collect.normalized_traditional_text || collect.traditional_text
  : collect.normalized_text || collect.text;
```

**Note**: This is a **temporary fallback**. Normalized text MUST be populated.

---

#### 5. Very Long Search Terms

**Scenario**: User pastes entire paragraph into search (> 100 chars)

**Handling**:

- No special handling needed (substring match works)
- May want to truncate display to first 50 chars in UI
- Performance not impacted (still simple string comparison)

---

### Accessibility Requirements

#### 1. Keyboard Navigation

**Requirements**:

- `Tab` to focus search input
- `Enter` to keep focus after typing (don't trigger form submission)
- `Escape` to clear search
- Arrow keys to navigate results (via existing el-collapse keyboard support)

**Implementation**:

```vue
<el-input
  v-model="searchTerm"
  @keyup.esc="clearSearch"
  @keydown.enter.prevent
  aria-label="Search collects"
/>
```

---

#### 2. Screen Reader Support

**Requirements**:

- Announce search results count
- Announce when results change
- Label search input properly

**Implementation**:

```vue
<el-input
  v-model="searchTerm"
  aria-label="Search collects by title or text"
  aria-describedby="search-results-count"
/>

<div
  id="search-results-count"
  aria-live="polite"
  aria-atomic="true"
  class="search-results-count"
>
  <span v-if="searchTerm">
    Showing {{ filteredCollects.length }} of {{ totalCollects }} collects
  </span>
</div>
```

**`aria-live="polite"`** causes screen readers to announce count changes after current task.

---

#### 3. Focus Management

**Requirement**: After clearing search, focus should return to search input (optional) or stay on clear button.

**Implementation**:

```javascript
clearSearch() {
  this.searchTerm = '';
  this.$nextTick(() => {
    this.$refs.searchInput.focus();  // Return focus to search input
  });
}
```

```vue
<el-input ref="searchInput" ... />
```

---

### Performance Benchmarks

#### Expected Performance Metrics

| Metric                                   | Target  | Measured               |
| ---------------------------------------- | ------- | ---------------------- |
| Search execution time                    | < 100ms | ~10-50ms (estimated)   |
| Highlight rendering time                 | < 200ms | ~50-150ms (estimated)  |
| Total response time (search + highlight) | < 300ms | ~100-200ms (estimated) |
| Debounce delay                           | 300ms   | 300ms (configured)     |
| Dataset size                             | < 1 MB  | ~500-800 KB (current)  |

**Success Criteria SC-006**: Search results in under 2 seconds ✅ (< 300ms expected)

---

#### Performance Monitoring

**Add Performance Logging** (dev mode only):

```javascript
methods: {
  onSearchInput(value) {
    clearTimeout(this.searchDebounceTimeout);
    this.searchDebounceTimeout = setTimeout(() => {
      const startTime = performance.now();

      this.searchTerm = value;

      this.$nextTick(() => {
        const endTime = performance.now();
        console.debug(`Search took ${endTime - startTime}ms`);
      });
    }, 300);
  }
}
```

---

### Testing Contract

#### Unit Tests (Vitest)

**Location**: `app/tests/unit/CollectsNew.spec.js`

**Required Tests**:

1. **Search input updates searchTerm after debounce**

   ```javascript
   it("should update searchTerm after 300ms debounce", async () => {
     const wrapper = mount(CollectsNew);
     const input = wrapper.find("el-input");

     input.setValue("grace");
     await new Promise((resolve) => setTimeout(resolve, 350));

     expect(wrapper.vm.searchTerm).toBe("grace");
   });
   ```

2. **filteredCollects returns matching collects**

   ```javascript
   it("should filter collects by title", () => {
     const wrapper = mount(CollectsNew, {
       data() {
         return {
           searchTerm: "Purity",
           collects: [
             { title: "Collect for Purity", text: "..." },
             { title: "Collect for Mission", text: "..." },
           ],
         };
       },
     });

     expect(wrapper.vm.filteredCollects).toHaveLength(1);
     expect(wrapper.vm.filteredCollects[0].title).toBe("Collect for Purity");
   });
   ```

3. **filteredCollects returns matching collects by text**

4. **clearSearch resets searchTerm**

5. **Search works with normalized_text field**

6. **Search falls back to HTML field if normalized_text empty**

7. **Search respects traditional language toggle**

8. **Special characters are normalized**

---

#### Integration Tests (Vitest)

**Required Tests**:

1. **Search + category filter work together (AND logic)**

2. **Search term highlighting applies correctly**

3. **Search results count updates**

4. **Empty search shows all collects**

---

#### End-to-End Tests (Playwright)

**Location**: `app/tests/e2e/collects.cy.js`

**Required Tests**:

1. **User searches for collect and sees results**

   ```javascript
   it("should search for collect by term", () => {
     cy.visit("/collects");
     cy.get('[aria-label="Search collects"]').type("grace");
     cy.wait(350); // Wait for debounce

     cy.contains("Search Results").should("be.visible");
     cy.get(".search-highlight").should("exist");
   });
   ```

2. **User clears search and sees all collects**

3. **User searches with no results sees empty state**

4. **Search works on mobile viewport**

5. **Keyboard navigation works (Tab, Escape, Enter)**

---

### Migration Path

#### Phase 1: Data Migration (Prerequisite)

```bash
# Create and run management command
python manage.py populate_normalized_text
```

**Verify**:

```python
from office.models import Collect

# Check that all collects have normalized text
collects_with_text = Collect.objects.exclude(normalized_text__isnull=True).count()
total_collects = Collect.objects.count()

print(f"{collects_with_text}/{total_collects} collects have normalized text")
# Should be 100%
```

---

#### Phase 2: Frontend Implementation

**Tasks** (from tasks.md, to be created in Phase 2):

1. Install mark.js dependency
2. Add search input to CollectsNew.vue
3. Implement filteredCollects computed property
4. Add search term highlighting
5. Add empty results handling
6. Add results count display
7. Write unit tests
8. Write integration tests
9. Write E2E tests
10. Test on mobile devices
11. Test with screen reader

**Estimated Effort**: 6-9 hours (from research.md)

---

#### Phase 3: Monitoring and Optimization

**Add Analytics** (if applicable):

- Track search terms used (for UX insights)
- Track search result counts (0 results = bad UX)
- Track search performance (catch regressions)

**Optimization Opportunities** (if needed):

- Add search suggestions (autocomplete)
- Add search history (localStorage)
- Add fuzzy matching (Fuse.js library)
- Add advanced search operators (AND, OR, NOT)

---

## Alternatives Considered (Not Implemented)

### 1. Backend PostgreSQL Full-Text Search

**Why Not**:

- Overkill for 500 records
- Slower (network latency)
- More complex (new API endpoint, GIN indexes)
- Harder to highlight terms in frontend

**When to Reconsider**:

- If dataset exceeds 2 MB (> 2000 collects)
- If search needs ranking/relevance scoring
- If search needs stemming (e.g., "pray" matches "prayer")

---

### 2. Elasticsearch / Algolia

**Why Not**:

- Way too complex for this use case
- External dependencies
- Additional cost
- Maintenance burden

**When to Reconsider**: Never for this feature.

---

### 3. WebAssembly Search Library

**Why Not**:

- Added complexity
- No significant performance benefit for this dataset
- JavaScript is fast enough

---

## Summary

**Implementation**: Client-side JavaScript search with mark.js highlighting

**Key Decisions**:

- ✅ Filter `filteredCollects` in Vue computed property
- ✅ Debounce input (300ms)
- ✅ Search title + normalized_text fields
- ✅ Highlight with mark.js
- ✅ Show results count
- ✅ Integrate with category filtering (AND logic)
- ✅ Handle empty results gracefully
- ✅ Full accessibility support

**Prerequisites**:

- ⚠️ Populate `normalized_text` fields (data migration)
- ⚠️ Install mark.js npm package

**Estimated Implementation**: 6-9 hours

**Performance**: < 300ms total (meets SC-006: < 2 seconds)

---

**Document Version**: 1.0  
**Last Updated**: November 6, 2025  
**Status**: Ready for Implementation
