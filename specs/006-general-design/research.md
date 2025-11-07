# Research: Cross-Platform Access and Settings

**Date**: 2025-11-07  
**Status**: In Progress  
**Related**: [spec.md](./spec.md) | [plan.md](./plan.md)

## Research Overview

This document consolidates research findings for implementing the future enhancements outlined in the 006-general-design specification. The current implementation is stable and well-architected; this research focuses on best practices for the planned enhancements.

## Current Architecture Analysis

### Technology Stack Assessment

**Frontend Stack** ✅ Well-Chosen:

- **Vue 3 with Composition API**: Modern, performant, excellent TypeScript support
- **Vite 6.x**: Fast build tool with excellent HMR and production optimization
- **Tailwind CSS 3.x**: Utility-first CSS framework providing responsive design
- **Element Plus**: Mature UI component library with good accessibility baseline
- **Capacitor 7.4.3**: Industry-standard solution for web-to-mobile wrapping

**Backend Stack** ✅ Appropriate:

- **Django 5.2+**: Mature Python web framework with excellent ORM
- **PostgreSQL 17.5+**: Robust relational database
- **Memcached**: Fast in-memory caching layer

**Decision: Maintain Current Stack** - No technology migrations needed. All future enhancements can be built on existing foundation.

### Storage Architecture Review

**Current Implementation** (`app/src/helpers/storage.js` - DynamicStorage):

```javascript
// Abstraction providing unified API across platforms
export class DynamicStorage {
  static async setItem(key, value) {
    // Uses Capacitor Preferences on mobile, localStorage on web
  }
  static async getItem(key) {
    // Platform-aware retrieval
  }
  static async removeItem(key) {
    // Platform-aware deletion
  }
}
```

**Strengths**:

- Clean abstraction hiding platform differences
- Async-first API (future-proof for IndexedDB migration if needed)
- Used consistently throughout codebase

**Decision: Extend DynamicStorage** - Build settings history and other storage features as extensions to this proven abstraction.

### Settings Encoding Scheme

**Current Implementation**:

- Settings encoded as URL parameters using compact abbreviations
- Each setting has `setting_string_order` defining position in encoded string
- Options have `abbreviation` values for compact encoding
- Decoded in `decodeSettingsString.js` helper

**Example**: `settings=2a1b3c` decodes to specific setting values

**Strengths**:

- Extremely compact (good for URLs and QR codes)
- Deterministic encoding/decoding
- Cross-platform compatible

**Decision: Maintain Encoding Scheme** - Do not change for backward compatibility. Settings history can store full JSON internally.

## Phase 1: Testing Infrastructure Research

### Test Coverage Goals

**Constitution Principle III Requirement**: 100% function coverage for new code

**Current State**:

- Vitest configured (`vitest.config.ts`)
- Cypress configured (`cypress.config.mjs`)
- Minimal test files exist (`tests/unit/example.spec.js`)

### Testing Framework Evaluation

#### Unit Testing: Vitest ✅ SELECTED

**Rationale**:

- Already configured in project
- Excellent Vite integration (same config, fast HMR)
- Jest-compatible API (low learning curve)
- Built-in coverage via c8/istanbul
- Fast execution (powered by Vite)

**Configuration Enhancement Needed**:

```typescript
// vitest.config.ts additions
export default defineConfig({
  test: {
    globals: true,
    environment: "jsdom", // For DOM testing
    coverage: {
      provider: "istanbul",
      reporter: ["text", "json", "html", "lcov"],
      exclude: ["node_modules/", "tests/", "**/*.config.*", "**/dist/**"],
      lines: 90,
      functions: 90,
      branches: 85,
      statements: 90,
    },
    setupFiles: ["./vitest.setup.js"],
  },
});
```

**Decision**: Use Vitest with coverage thresholds enforced.

#### Component Testing: Vue Test Utils + Vitest ✅ SELECTED

**Rationale**:

- Official Vue.js testing library
- Works seamlessly with Vitest
- Supports Composition API
- Can test Element Plus components

**Example Test Structure**:

```javascript
import { mount } from "@vue/test-utils";
import { describe, it, expect, beforeEach } from "vitest";
import Settings from "@/views/Settings.vue";

describe("Settings.vue", () => {
  it("loads available settings from store", async () => {
    // Test implementation
  });
});
```

**Decision**: Use Vue Test Utils for all component testing.

#### E2E Testing: Cypress ✅ SELECTED

**Rationale**:

- Already configured in project
- Excellent developer experience (time-travel debugging)
- Strong community and documentation
- Good mobile viewport testing

**Critical E2E Test Scenarios Needed**:

1. Settings persistence across page reloads
2. Settings sharing via URL parameters
3. Settings sharing via QR code (mobile)
4. Cross-platform settings compatibility
5. Responsive layout at various breakpoints
6. Dark/light theme switching
7. Font size adjustment
8. Deep linking (mobile apps)

**Decision**: Use Cypress for E2E tests with mobile viewport testing.

### Test Organization Strategy

```
app/tests/
├── unit/
│   ├── helpers/
│   │   ├── storage.spec.js          # DynamicStorage tests
│   │   ├── createSettingsString.spec.js
│   │   ├── decodeSettingsString.spec.js
│   │   └── performanceMonitoring.spec.js (future)
│   ├── store/
│   │   └── index.spec.js            # Vuex store tests
│   └── components/
│       ├── ShareSettings.spec.js
│       ├── SettingsPanel.spec.js
│       ├── FontSizer.spec.js
│       └── ThemeSwitcher.spec.js
├── integration/                      # For testing component interactions
│   └── settings-flow.spec.js
└── e2e/
    ├── settings-persistence.cy.js
    ├── settings-sharing.cy.js
    ├── responsive-design.cy.js
    ├── accessibility.cy.js
    └── cross-platform.cy.js
```

**Decision**: Use this hierarchical organization with clear separation of concerns.

### Mock Strategies

**Capacitor Mocking**:

```javascript
// vitest.setup.js
import { vi } from "vitest";

// Mock Capacitor for web environment testing
vi.mock("@capacitor/core", () => ({
  Capacitor: {
    getPlatform: () => "web",
    isNativePlatform: () => false,
  },
}));

vi.mock("@capacitor/preferences", () => ({
  Preferences: {
    set: vi.fn(),
    get: vi.fn(),
    remove: vi.fn(),
  },
}));
```

**Decision**: Create comprehensive Capacitor mocks for unit tests; use real Capacitor in E2E tests.

### CI/CD Integration

**GitHub Actions Workflow** (recommended):

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "20"
      - run: npm ci
      - run: npm run test:unit -- --coverage
      - run: npm run test:e2e
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

**Decision**: Implement GitHub Actions workflow with coverage reporting.

## Phase 2: Accessibility Enhancement Research

### WCAG 2.1 Level AA Requirements

**Current Baseline Assessment**:

- ✅ Semantic HTML structure exists (nav, main, article, section)
- ✅ Responsive design supports zoom/text scaling
- ✅ Font size customization available
- ⚠️ Partial keyboard navigation
- ❌ Missing ARIA labels on many controls
- ❌ No skip links
- ❌ Inconsistent focus indicators
- ❌ Not tested with screen readers

### Accessibility Audit Tools

#### Automated Testing: axe-core ✅ SELECTED

**Rationale**:

- Industry standard (used by Deque, Microsoft, Google)
- Can integrate into unit tests AND E2E tests
- Comprehensive rule set for WCAG 2.1
- Actionable error messages

**Integration with Vitest**:

```javascript
import { axe, toHaveNoViolations } from "jest-axe";
expect.extend(toHaveNoViolations);

it("has no accessibility violations", async () => {
  const { container } = mount(Settings);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

**Integration with Cypress**:

```javascript
// cypress/support/commands.js
import "cypress-axe";

// In test
cy.injectAxe();
cy.checkA11y();
```

**Decision**: Use axe-core in both unit and E2E tests.

#### Manual Testing Checklist

**Screen Readers to Test**:

- **macOS**: VoiceOver (built-in)
- **Windows**: NVDA (free, open source)
- **iOS**: VoiceOver (built-in)
- **Android**: TalkBack (built-in)

**Keyboard Navigation Checklist**:

- [ ] All interactive elements reachable via Tab/Shift+Tab
- [ ] Visible focus indicators on all focusable elements
- [ ] Skip links to main content
- [ ] Escape key closes modals/dialogs
- [ ] Enter/Space activates buttons
- [ ] Arrow keys navigate within component groups (tabs, menus)
- [ ] No keyboard traps

**Color Contrast Checklist**:

- [ ] Text contrast ≥4.5:1 for normal text
- [ ] Text contrast ≥3:1 for large text (18pt+ or 14pt+ bold)
- [ ] Interactive element contrast ≥3:1
- [ ] Test in both light and dark themes

**Decision**: Create accessibility test checklist integrated into PR process.

### ARIA Implementation Strategy

**Principles**:

1. Use semantic HTML first (button over div with role="button")
2. Add ARIA only where semantic HTML insufficient
3. Follow ARIA Authoring Practices Guide (APG) patterns

**Priority ARIA Additions Needed**:

```html
<!-- Settings Toggle Example -->
<el-switch
  v-model="openTab"
  active-value="family"
  inactive-value="office"
  role="switch"
  :aria-checked="openTab === 'family'"
  aria-label="Switch between Daily Office and Family Prayer settings"
/>

<!-- Share Settings Button -->
<button
  @click="toggleSharePanel"
  aria-label="Open settings sharing panel"
  aria-expanded="false"
  aria-controls="share-panel"
>
  Share Settings
</button>

<!-- Settings Panel -->
<div
  id="share-panel"
  role="region"
  aria-label="Settings sharing options"
  aria-live="polite"
>
  <!-- Panel content -->
</div>
```

**Decision**: Audit all interactive components and add appropriate ARIA labels following APG patterns.

### Accessibility-First Component Library

**Element Plus Accessibility**:

- ✅ Generally good accessibility baseline
- ⚠️ Requires explicit ARIA labels in many cases
- ✅ Keyboard navigation support in most components

**Action Items**:

1. Audit all Element Plus component usage
2. Add missing aria-label props
3. Verify keyboard navigation in all dialogs/drawers
4. Test with screen readers

**Decision**: Continue using Element Plus, enhance with explicit ARIA attributes.

### Focus Management

**Vue Focus Management Library**: Focus-trap-vue ✅ SELECTED

**Rationale**:

- Handles focus trapping in modals/dialogs
- Returns focus to trigger element on close
- Lightweight and Vue-compatible

```javascript
import { FocusTrap } from 'focus-trap-vue';

<FocusTrap :active="drawerOpen">
  <el-drawer v-model="drawerOpen">
    <!-- Drawer content -->
  </el-drawer>
</FocusTrap>
```

**Decision**: Add focus-trap-vue for modal/drawer focus management.

## Phase 3: Settings History & Confirmation Research

### Settings History Data Model

**Design Decision**: Store history as array of timestamped snapshots

**Schema**:

```typescript
interface SettingsHistoryEntry {
  timestamp: string; // ISO 8601 format
  settings: Record<string, any>; // Full settings object
  source: "manual" | "shared_link" | "import"; // How settings were applied
  label?: string; // Optional user-provided label
}

interface SettingsHistory {
  entries: SettingsHistoryEntry[];
  maxEntries: number; // Default 10
}
```

**Storage Strategy**:

```javascript
// Extend DynamicStorage
export class SettingsHistoryStorage {
  static async addEntry(settings, source) {
    const history = await this.getHistory();
    const entry = {
      timestamp: new Date().toISOString(),
      settings: { ...settings },
      source,
    };

    history.entries.unshift(entry); // Add to beginning

    // Prune old entries
    if (history.entries.length > history.maxEntries) {
      history.entries = history.entries.slice(0, history.maxEntries);
    }

    await DynamicStorage.setItem("settingsHistory", JSON.stringify(history));
  }

  static async getHistory(): Promise<SettingsHistory> {
    const stored = await DynamicStorage.getItem("settingsHistory");
    return stored ? JSON.parse(stored) : { entries: [], maxEntries: 10 };
  }

  static async restoreEntry(timestamp: string) {
    const history = await this.getHistory();
    const entry = history.entries.find((e) => e.timestamp === timestamp);
    if (entry) {
      return entry.settings;
    }
    return null;
  }
}
```

**Decision**: Implement settings history as timestamped array with automatic pruning.

### Settings Confirmation UI Design

**User Flow**:

1. User clicks shared settings link
2. Application decodes settings from URL
3. **[NEW]** Show confirmation dialog with:
   - Current settings preview
   - New settings preview
   - Diff highlighting changes
   - Accept/Reject buttons
4. If accepted: Save current to history, apply new settings
5. If rejected: Keep current settings, show "Settings not changed" message

**Component Structure**:

```vue
<template>
  <el-dialog
    v-model="visible"
    title="Apply Shared Settings?"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <div class="settings-comparison">
      <div class="current-settings">
        <h3>Your Current Settings</h3>
        <SettingsList :settings="currentSettings" />
      </div>

      <div class="changes-indicator">
        <font-awesome-icon icon="arrow-right" />
      </div>

      <div class="new-settings">
        <h3>Shared Settings</h3>
        <SettingsList :settings="newSettings" :highlight-changes="true" />
      </div>
    </div>

    <div class="changes-summary">
      <p>{{ changeCount }} settings will be changed</p>
    </div>

    <template #footer>
      <el-button @click="reject">Keep My Settings</el-button>
      <el-button type="primary" @click="accept"
        >Apply Shared Settings</el-button
      >
    </template>
  </el-dialog>
</template>
```

**Decision**: Implement modal confirmation dialog with side-by-side comparison.

### Settings Diff Algorithm

**Approach**: Simple object comparison highlighting changed keys

```javascript
export function compareSettings(current, incoming) {
  const changes = [];

  for (const [key, newValue] of Object.entries(incoming)) {
    const currentValue = current[key];

    if (currentValue !== newValue) {
      changes.push({
        setting: key,
        from: currentValue,
        to: newValue,
      });
    }
  }

  return changes;
}
```

**Decision**: Implement simple key-based diff for settings comparison.

### Store Refactoring for Confirmation

**Current Flow** (app/src/store/index.js):

```javascript
// Settings applied immediately when URL params detected
if (router.currentRoute._value.query[key]) {
  applied = true;
  settings[key] = router.currentRoute._value.query[key];
}
```

**New Flow**:

```javascript
// Detect shared settings
const sharedSettings = extractSharedSettings(router.currentRoute._value.query);

if (sharedSettings && Object.keys(sharedSettings).length > 0) {
  // Trigger confirmation dialog instead of immediate apply
  commit("SET_PENDING_SHARED_SETTINGS", sharedSettings);
  // Dialog component watches this state and shows confirmation
} else {
  // Normal settings loading
  await loadSettingsFromStorage();
}
```

**Decision**: Refactor store to support pending settings state for confirmation flow.

## Phase 4: Progressive Web App (PWA) Research

### Service Worker Strategy

**Workbox Library** ✅ SELECTED

**Rationale**:

- Google-maintained, battle-tested
- Excellent Vite integration via `vite-plugin-pwa`
- Provides caching strategies out of the box
- Handles service worker lifecycle automatically

**Installation**:

```bash
npm install -D vite-plugin-pwa workbox-window
```

**Vite Configuration** (vite.config.mjs):

```javascript
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["favicon.ico", "robots.txt", "assets/**/*"],
      manifest: {
        name: "Daily Office 2019",
        short_name: "Daily Office",
        description:
          "Pray the Daily Office from the 2019 Book of Common Prayer",
        theme_color: "#1a202c",
        background_color: "#ffffff",
        display: "standalone",
        scope: "/",
        start_url: "/",
        icons: [
          {
            src: "/assets/icon-192.png",
            sizes: "192x192",
            type: "image/png",
          },
          {
            src: "/assets/icon-512.png",
            sizes: "512x512",
            type: "image/png",
          },
          {
            src: "/assets/icon-512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "any maskable",
          },
        ],
      },
      workbox: {
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\.dailyoffice2019\.com\/.*/i,
            handler: "NetworkFirst",
            options: {
              cacheName: "api-cache",
              expiration: {
                maxEntries: 100,
                maxAgeSeconds: 60 * 60 * 24, // 24 hours
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
            handler: "CacheFirst",
            options: {
              cacheName: "image-cache",
              expiration: {
                maxEntries: 100,
                maxAgeSeconds: 60 * 60 * 24 * 30, // 30 days
              },
            },
          },
        ],
      },
    }),
  ],
});
```

**Decision**: Use vite-plugin-pwa with Workbox for service worker implementation.

### Caching Strategies

**Strategy Selection**:

| Resource Type          | Strategy     | Rationale                                       |
| ---------------------- | ------------ | ----------------------------------------------- |
| HTML pages             | NetworkFirst | Always try fresh content, fallback to cache     |
| API responses          | NetworkFirst | Office data changes daily, prefer fresh         |
| Static assets (JS/CSS) | CacheFirst   | Versioned by Vite, safe to cache aggressively   |
| Images                 | CacheFirst   | Rarely change, large files benefit from caching |
| Fonts                  | CacheFirst   | Never change once loaded                        |

**Offline Fallback**:

Create `public/offline.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Offline - Daily Office 2019</title>
    <style>
      body {
        font-family: system-ui, sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        margin: 0;
        padding: 20px;
        text-align: center;
      }
    </style>
  </head>
  <body>
    <div>
      <h1>You're Offline</h1>
      <p>This page requires an internet connection.</p>
      <p>Previously viewed content may be available in your browser history.</p>
      <button onclick="window.location.reload()">Try Again</button>
    </div>
  </body>
</html>
```

**Decision**: Use NetworkFirst for HTML/API, CacheFirst for static assets, provide offline fallback page.

### Service Worker Lifecycle Management

**Registration** (app/src/main.js):

```javascript
import { registerSW } from "virtual:pwa-register";

const updateSW = registerSW({
  onNeedRefresh() {
    // Show notification to user that update is available
    if (confirm("New version available! Reload to update?")) {
      updateSW(true); // Force reload
    }
  },
  onOfflineReady() {
    console.log("App ready to work offline");
  },
});
```

**Update Strategy**: Prompt user for updates rather than auto-reload (preserves prayer in progress)

**Decision**: Use prompt-based update strategy to avoid interrupting users during prayer.

### PWA Manifest Enhancements

**Current State**: Basic manifest exists at `public/site.webmanifest`

**Enhancements Needed**:

```json
{
  "name": "Daily Office 2019",
  "short_name": "Daily Office",
  "description": "Pray the Daily Office from the 2019 Book of Common Prayer",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#1a202c",
  "orientation": "portrait-primary",
  "categories": ["lifestyle", "utilities"],
  "icons": [
    {
      "src": "/assets/icon-72.png",
      "sizes": "72x72",
      "type": "image/png"
    },
    {
      "src": "/assets/icon-96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/assets/icon-128.png",
      "sizes": "128x128",
      "type": "image/png"
    },
    {
      "src": "/assets/icon-144.png",
      "sizes": "144x144",
      "type": "image/png"
    },
    {
      "src": "/assets/icon-152.png",
      "sizes": "152x152",
      "type": "image/png"
    },
    {
      "src": "/assets/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/assets/icon-384.png",
      "sizes": "384x384",
      "type": "image/png"
    },
    {
      "src": "/assets/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    },
    {
      "src": "/assets/icon-512-maskable.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ],
  "shortcuts": [
    {
      "name": "Morning Prayer",
      "short_name": "Morning",
      "description": "Go directly to Morning Prayer",
      "url": "/family/morning_prayer",
      "icons": [{ "src": "/assets/morning-icon-96.png", "sizes": "96x96" }]
    },
    {
      "name": "Evening Prayer",
      "short_name": "Evening",
      "description": "Go directly to Evening Prayer",
      "url": "/family/evening_prayer",
      "icons": [{ "src": "/assets/evening-icon-96.png", "sizes": "96x96" }]
    }
  ],
  "screenshots": [
    {
      "src": "/assets/screenshot-mobile-1.png",
      "sizes": "540x720",
      "type": "image/png",
      "form_factor": "narrow"
    },
    {
      "src": "/assets/screenshot-desktop-1.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide"
    }
  ]
}
```

**Decision**: Create comprehensive manifest with icons, shortcuts, and screenshots.

### PWA Testing Tools

**Lighthouse** ✅ SELECTED for PWA audits

**Checklist**:

- [ ] Service worker registered and active
- [ ] Manifest valid and includes all required fields
- [ ] Icons for all required sizes (72, 96, 128, 144, 152, 192, 384, 512)
- [ ] Maskable icon for adaptive icon support
- [ ] Offline fallback page works
- [ ] App installable on desktop and mobile
- [ ] Update prompt appears when new version deployed

**Decision**: Use Lighthouse PWA audit in CI/CD pipeline.

## Phase 5: Performance Monitoring Research

### Performance API Integration

**Metrics to Track**:

| Metric                         | Description                     | Target  |
| ------------------------------ | ------------------------------- | ------- |
| FCP (First Contentful Paint)   | Time to first visible content   | < 1.8s  |
| LCP (Largest Contentful Paint) | Time to largest content element | < 2.5s  |
| FID (First Input Delay)        | Time to first interaction       | < 100ms |
| CLS (Cumulative Layout Shift)  | Visual stability                | < 0.1   |
| TTFB (Time To First Byte)      | Server response time            | < 600ms |

**Implementation**:

```javascript
// app/src/helpers/performanceMonitoring.js

export class PerformanceMonitor {
  static measureFCP() {
    const fcpEntry = performance.getEntriesByName("first-contentful-paint")[0];
    if (fcpEntry) {
      return fcpEntry.startTime;
    }
    return null;
  }

  static measureLCP() {
    return new Promise((resolve) => {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        resolve(lastEntry.startTime);
        observer.disconnect();
      });
      observer.observe({ entryTypes: ["largest-contentful-paint"] });

      // Timeout after 10 seconds
      setTimeout(() => {
        observer.disconnect();
        resolve(null);
      }, 10000);
    });
  }

  static measureCLS() {
    let clsScore = 0;
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) {
          clsScore += entry.value;
        }
      }
    });
    observer.observe({ entryTypes: ["layout-shift"] });

    // Return function to get current CLS
    return () => {
      observer.disconnect();
      return clsScore;
    };
  }

  static async captureMetrics() {
    const metrics = {
      timestamp: new Date().toISOString(),
      url: window.location.href,
      userAgent: navigator.userAgent,
      connection: navigator.connection?.effectiveType,
      fcp: this.measureFCP(),
      lcp: await this.measureLCP(),
      ttfb: performance.timing.responseStart - performance.timing.requestStart,
    };

    return metrics;
  }

  static async reportMetrics(metrics) {
    // Option 1: Log to console in development
    if (import.meta.env.DEV) {
      console.table(metrics);
    }

    // Option 2: Send to analytics (Firebase, Google Analytics, etc.)
    if (window.gtag) {
      window.gtag("event", "performance_metrics", metrics);
    }

    // Option 3: Send to custom backend endpoint
    if (import.meta.env.VITE_PERFORMANCE_ENDPOINT) {
      try {
        await fetch(import.meta.env.VITE_PERFORMANCE_ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(metrics),
        });
      } catch (error) {
        console.error("Failed to report metrics:", error);
      }
    }
  }
}
```

**Decision**: Implement Performance API monitoring with optional reporting to analytics/backend.

### Web Vitals Library

**web-vitals** ✅ RECOMMENDED for simplified metrics

```javascript
import { onCLS, onFID, onFCP, onLCP, onTTFB } from "web-vitals";

export function initPerformanceMonitoring() {
  onCLS(console.log);
  onFID(console.log);
  onFCP(console.log);
  onLCP(console.log);
  onTTFB(console.log);
}
```

**Decision**: Use web-vitals library for simplified Core Web Vitals tracking.

### Performance Budget

**Establish Baselines**:

```javascript
// vite.config.mjs
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          "vue-vendor": ["vue", "vue-router", "vuex"],
          "ui-vendor": ["element-plus"],
          utils: ["axios", "@capacitor/core"],
        },
      },
    },
    chunkSizeWarningLimit: 500, // KB
  },
});
```

**Bundle Size Targets**:

- Initial JS bundle: < 200 KB (gzipped)
- Total page weight: < 1 MB
- CSS bundle: < 50 KB (gzipped)

**Decision**: Set build-time warnings for bundle size violations.

### Performance Regression Testing

**Lighthouse CI** ✅ RECOMMENDED

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [pull_request]
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci && npm run build
      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v9
        with:
          urls: |
            http://localhost:5000/
            http://localhost:5000/settings
          uploadArtifacts: true
          temporaryPublicStorage: true
```

**Decision**: Add Lighthouse CI to PR checks to prevent performance regressions.

## Phase 6: Browser Detection Research

### Browser Detection Strategy

**Avoid User-Agent Parsing** (unreliable, easily spoofed)

**Use Feature Detection Instead**:

```javascript
export function isModernBrowser() {
  // Check for required modern APIs
  return (
    "fetch" in window &&
    "Promise" in window &&
    "IntersectionObserver" in window &&
    "ResizeObserver" in window &&
    "URLSearchParams" in window &&
    CSS.supports("display", "grid") &&
    CSS.supports("display", "flex")
  );
}

export function getSupportedVersion() {
  // Check for browser version if needed
  const ua = navigator.userAgent;

  // Only if feature detection fails, check specific versions
  if (ua.includes("Chrome/")) {
    const version = parseInt(ua.match(/Chrome\/(\d+)/)[1]);
    return { browser: "Chrome", version, supported: version >= 90 };
  }

  // Similar for other browsers...

  return { browser: "Unknown", version: null, supported: false };
}
```

**Decision**: Use feature detection primarily; browser version check as fallback.

### Unsupported Browser Banner

**UI Pattern**: Non-intrusive banner at top of page

```vue
<template>
  <div v-if="!isSupported" class="unsupported-banner" role="alert">
    <div class="banner-content">
      <font-awesome-icon icon="exclamation-triangle" />
      <div>
        <strong>Unsupported Browser</strong>
        <p>
          For the best experience, please use a modern browser like
          <a href="https://www.google.com/chrome/" target="_blank">Chrome</a>,
          <a href="https://www.mozilla.org/firefox/" target="_blank">Firefox</a
          >, <a href="https://www.apple.com/safari/" target="_blank">Safari</a>,
          or <a href="https://www.microsoft.com/edge" target="_blank">Edge</a>.
        </p>
      </div>
      <button @click="dismiss" aria-label="Dismiss banner">×</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isSupported: true,
      dismissed: false,
    };
  },
  mounted() {
    this.isSupported = isModernBrowser();
    this.dismissed = localStorage.getItem("browserWarningDismissed") === "true";
  },
  methods: {
    dismiss() {
      this.dismissed = true;
      localStorage.setItem("browserWarningDismissed", "true");
    },
  },
};
</script>
```

**Decision**: Show dismissible banner for unsupported browsers; store dismissal in localStorage.

### Polyfill Strategy

**Core Decision**: Do NOT add polyfills

**Rationale**:

- Target modern browsers only (per spec: "last 2 major versions")
- Polyfills add significant bundle size
- Better to show warning than degrade performance for all users
- Current tech stack (Vue 3, Vite) already targets modern browsers

**Graceful Degradation**:

- Application still loads on old browsers
- Warning banner shown
- Some features may not work
- No JavaScript errors that break entire page

**Decision**: No polyfills; rely on graceful degradation and user warning.

## Technology Decision Summary

| Area                  | Technology                             | Rationale                                         |
| --------------------- | -------------------------------------- | ------------------------------------------------- |
| **Testing**           | Vitest + Vue Test Utils + Cypress      | Seamless Vite integration, comprehensive coverage |
| **Coverage**          | Istanbul (c8) via Vitest               | Built-in, proven solution                         |
| **Accessibility**     | axe-core + manual testing              | Industry standard, covers automated + manual      |
| **Focus Management**  | focus-trap-vue                         | Lightweight, Vue-compatible                       |
| **Settings Storage**  | Extend DynamicStorage                  | Proven abstraction, maintains consistency         |
| **PWA**               | vite-plugin-pwa + Workbox              | Battle-tested, excellent Vite integration         |
| **Performance**       | web-vitals + Performance API           | Google-recommended, comprehensive metrics         |
| **Browser Detection** | Feature detection + minimal UA parsing | Reliable, future-proof approach                   |

## Implementation Dependencies

```json
{
  "devDependencies": {
    "vitest": "^1.0.0",
    "@vue/test-utils": "^2.4.0",
    "@vitest/coverage-istanbul": "^1.0.0",
    "cypress": "^13.0.0",
    "cypress-axe": "^1.5.0",
    "jest-axe": "^8.0.0",
    "vite-plugin-pwa": "^0.17.0",
    "workbox-window": "^7.0.0",
    "@types/web-vitals": "^2.0.0"
  },
  "dependencies": {
    "focus-trap-vue": "^1.0.0",
    "web-vitals": "^3.5.0"
  }
}
```

## Alternatives Considered and Rejected

### Service Worker Alternatives

**Rejected**: Manual service worker without Workbox

- **Why**: Too complex, error-prone, reinventing wheel
- **Decision**: Use Workbox/vite-plugin-pwa

**Rejected**: AppCache (deprecated)

- **Why**: Deprecated API, service workers are modern replacement
- **Decision**: Service workers only

### Testing Alternatives

**Rejected**: Jest instead of Vitest

- **Why**: Vitest better Vite integration, faster, modern
- **Decision**: Vitest

**Rejected**: Playwright instead of Cypress

- **Why**: Cypress already configured, team familiarity
- **Decision**: Cypress (but Playwright is valid alternative)

### Performance Monitoring Alternatives

**Rejected**: Third-party APM (New Relic, Datadog, etc.)

- **Why**: Cost, complexity, overkill for current needs
- **Decision**: Custom implementation with web-vitals

**Rejected**: Real User Monitoring (RUM) service

- **Why**: Can add later if needed; start simple with client-side metrics
- **Decision**: Client-side only initially

## Next Steps: Phase 1 Execution

With research complete, proceed to Phase 1 implementation:

1. **Install Dependencies**:

   ```bash
   cd app
   npm install -D vitest @vue/test-utils @vitest/coverage-istanbul cypress-axe jest-axe
   npm install -D vite-plugin-pwa workbox-window
   npm install focus-trap-vue web-vitals
   ```

2. **Configure Testing Infrastructure**:

   - Update `vitest.config.ts` with coverage thresholds
   - Create `vitest.setup.js` with Capacitor mocks
   - Add coverage scripts to `package.json`
   - Configure Cypress for accessibility testing

3. **Begin Writing Tests**:

   - Start with utility functions (DynamicStorage, encoding/decoding)
   - Move to store tests
   - Then component tests
   - Finally E2E tests

4. **Set Up CI/CD**:
   - Create GitHub Actions workflow for tests
   - Add coverage reporting
   - Set up Lighthouse CI

## Research Conclusions

**Key Findings**:

- Current architecture is solid and well-suited for enhancements
- No major refactoring or technology changes needed
- Chosen technologies (Vue 3, Vite, Capacitor) all have excellent PWA/testing support
- Can achieve all enhancement goals incrementally without breaking changes

**Risk Assessment**: LOW

- All planned enhancements are additive, not destructive
- Technologies are mature and well-documented
- Team already familiar with core stack
- Backward compatibility maintainable throughout

**Confidence Level**: HIGH

- Clear implementation paths identified for all phases
- Established patterns and best practices available
- Existing codebase provides good foundation

**Ready to Proceed**: ✅ YES

---

**Research Status**: COMPLETE  
**Next Action**: Begin Phase 1 (Testing Infrastructure) implementation  
**Estimated Phase 1 Duration**: 3-4 weeks
