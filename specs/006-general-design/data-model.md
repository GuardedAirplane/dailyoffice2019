# Data Model: 006-General-Design

**Version**: 1.0  
**Date**: November 7, 2025  
**Status**: Phase 1 - Design & Contracts

## Overview

This document defines the data structures and schemas for the cross-platform access and settings management features. All data is stored client-side using the DynamicStorage abstraction (localStorage on web, Capacitor Preferences on mobile).

## Storage Strategy

- **Primary Storage**: Client-side only (DynamicStorage)
- **Backend Reporting**: Optional for performance metrics (Phase 6)
- **Persistence**: All settings persisted to survive app restarts
- **Sync**: URL-based settings sharing (existing implementation)

---

## 1. Settings Data Model

### 1.1 Current Settings (Existing Implementation)

**Storage Key**: Various keys via DynamicStorage

**Structure**: Individual key-value pairs

```typescript
// Daily Office Settings
interface DailyOfficeSettings {
  // Office Type
  office_type:
    | "morning_prayer"
    | "midday_prayer"
    | "evening_prayer"
    | "compline";

  // Readings Configuration
  reading_length: "abbreviated" | "standard" | "extended";
  psalms_style: "coverdale" | "contemporary";

  // Calendar Options
  calendar_year: number; // e.g., 2025
  commemoration_preference: "primary" | "alternate";

  // Display Options
  show_rubrics: boolean;
  font_size: "small" | "medium" | "large";
  theme: "light" | "dark" | "auto";
}

// Family Prayer Settings
interface FamilyPrayerSettings {
  // Office Type
  family_office: "morning" | "midday" | "evening" | "close_of_day";

  // Reading Configuration
  include_psalms: boolean;
  include_readings: boolean;

  // Display Options
  font_size: "small" | "medium" | "large";
}
```

**URL Encoding**: Compact query string format (existing implementation)

- Example: `?office=mp&length=std&year=2025`

---

## 2. Settings History (Phase 4 Enhancement)

### 2.1 History Entry Schema

**Storage Key**: `settings_history`

**Structure**: Array of timestamped snapshots

```typescript
interface SettingsHistoryEntry {
  // Metadata
  id: string; // UUID v4
  timestamp: number; // Unix timestamp (milliseconds)
  source: "manual" | "url_import" | "restore" | "default";

  // Optional Label
  label?: string; // User-provided label (e.g., "Advent Morning Prayer")

  // Settings Snapshot
  settings: {
    office_type?: string;
    reading_length?: string;
    psalms_style?: string;
    calendar_year?: number;
    commemoration_preference?: string;
    show_rubrics?: boolean;
    font_size?: string;
    theme?: string;
    // ... all other settings fields
  };

  // Computed Properties
  settings_hash?: string; // SHA-256 hash for duplicate detection
  url_encoded?: string; // Compact URL representation
}

interface SettingsHistory {
  version: 1; // Schema version for migrations
  entries: SettingsHistoryEntry[];
  max_entries: number; // Default: 50
}
```

**Storage Operations**:

- **Create**: Add new entry when settings change
- **Read**: Retrieve full history or filtered by date range
- **Update**: Modify entry label
- **Delete**: Remove individual entry or clear all history
- **Restore**: Apply settings from history entry

**Constraints**:

- Maximum 50 entries (configurable)
- Oldest entries auto-pruned when limit reached
- Duplicate detection via settings_hash

### 2.2 History Metadata

```typescript
interface HistoryMetadata {
  last_saved: number; // Timestamp of most recent save
  total_saves: number; // Lifetime count of settings changes
  auto_save_enabled: boolean; // Auto-save on every change
  retention_days?: number; // Auto-delete entries older than X days
}
```

---

## 3. Pending Settings (Phase 4 Enhancement)

### 3.1 Pending State Schema

**Storage**: Vuex store state (not persisted)

**Purpose**: Hold settings imported from URL before user confirmation

```typescript
interface PendingSettings {
  // Pending State
  has_pending: boolean;
  source: "url_import" | "qr_scan";
  imported_at: number; // Timestamp

  // Pending Settings
  settings: Partial<DailyOfficeSettings | FamilyPrayerSettings>;

  // Diff Information
  changes: SettingChange[];
}

interface SettingChange {
  key: string;
  label: string; // Human-readable label
  old_value: any;
  new_value: any;
  category: "office" | "readings" | "display" | "calendar";
}
```

**Workflow**:

1. URL with settings → Parse → Store in pending state
2. Display confirmation dialog with diff
3. User confirms → Apply to active settings + Save to history
4. User cancels → Clear pending state

---

## 4. Performance Metrics (Phase 6 Enhancement)

### 4.1 Core Web Vitals Schema

**Storage Key**: `performance_metrics`

**Structure**: Time-series data with aggregation

```typescript
interface PerformanceMetric {
  // Metadata
  id: string; // UUID v4
  timestamp: number; // Unix timestamp
  session_id: string; // Browser session identifier

  // Device Context
  user_agent: string;
  viewport: {
    width: number;
    height: number;
  };
  connection_type?: "slow-2g" | "2g" | "3g" | "4g" | "wifi" | "unknown";

  // Core Web Vitals
  metrics: {
    // First Contentful Paint
    FCP?: {
      value: number; // milliseconds
      rating: "good" | "needs-improvement" | "poor";
    };

    // Largest Contentful Paint
    LCP?: {
      value: number; // milliseconds
      rating: "good" | "needs-improvement" | "poor";
    };

    // First Input Delay
    FID?: {
      value: number; // milliseconds
      rating: "good" | "needs-improvement" | "poor";
    };

    // Cumulative Layout Shift
    CLS?: {
      value: number; // unitless score
      rating: "good" | "needs-improvement" | "poor";
    };

    // Time to First Byte
    TTFB?: {
      value: number; // milliseconds
      rating: "good" | "needs-improvement" | "poor";
    };
  };

  // Page Context
  page: {
    path: string; // e.g., "/morning-prayer"
    office_type?: string;
    is_offline?: boolean;
  };
}

interface PerformanceMetricsStore {
  version: 1;
  metrics: PerformanceMetric[];
  max_entries: number; // Default: 100
  aggregated?: AggregatedMetrics;
}
```

### 4.2 Aggregated Metrics

```typescript
interface AggregatedMetrics {
  period: "day" | "week" | "month";
  start_date: number; // Unix timestamp
  end_date: number;

  summary: {
    total_samples: number;

    FCP: MetricSummary;
    LCP: MetricSummary;
    FID: MetricSummary;
    CLS: MetricSummary;
    TTFB: MetricSummary;
  };
}

interface MetricSummary {
  count: number;
  min: number;
  max: number;
  median: number;
  p75: number; // 75th percentile
  p95: number; // 95th percentile

  ratings: {
    good: number; // count
    needs_improvement: number;
    poor: number;
  };
}
```

**Rating Thresholds** (from research.md):

- **FCP**: Good ≤ 1.8s, Poor > 3.0s
- **LCP**: Good ≤ 2.5s, Poor > 4.0s
- **FID**: Good ≤ 100ms, Poor > 300ms
- **CLS**: Good ≤ 0.1, Poor > 0.25
- **TTFB**: Good ≤ 800ms, Poor > 1800ms

---

## 5. Service Worker Cache (Phase 5 Enhancement)

### 5.1 Cache Structure

**Workbox Caches** (managed by service worker):

```typescript
interface CacheConfiguration {
  caches: {
    // Static Assets Cache
    "static-assets-v1": {
      strategy: "CacheFirst";
      max_entries: 100;
      max_age_seconds: 2592000; // 30 days
      patterns: ["/assets/**", "/fonts/**", "/images/**", "*.css", "*.js"];
    };

    // API Cache
    "api-cache-v1": {
      strategy: "NetworkFirst";
      max_entries: 50;
      max_age_seconds: 86400; // 24 hours
      network_timeout: 3000; // 3 seconds
      patterns: ["/api/**"];
    };

    // HTML Cache
    "html-cache-v1": {
      strategy: "NetworkFirst";
      max_entries: 20;
      max_age_seconds: 3600; // 1 hour
      patterns: [
        "/",
        "/morning-prayer",
        "/evening-prayer",
        "/compline",
        "/settings"
      ];
    };

    // Image Cache
    "image-cache-v1": {
      strategy: "CacheFirst";
      max_entries: 50;
      max_age_seconds: 2592000; // 30 days
      patterns: ["*.jpg", "*.png", "*.svg", "*.webp"];
    };
  };
}
```

### 5.2 Offline Fallback

```typescript
interface OfflineFallback {
  // Offline Page
  html: "/offline.html"; // Static fallback page

  // Cached Routes
  precache: [
    "/",
    "/offline.html",
    "/manifest.json",
    "/assets/app.css",
    "/assets/app.js"
  ];
}
```

---

## 6. PWA Manifest Enhancement (Phase 5)

### 6.1 Manifest Schema

**File**: `/public/manifest.json`

```json
{
  "name": "Daily Office 2019",
  "short_name": "Daily Office",
  "description": "Book of Common Prayer 2019 Daily Office",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#1a365d",
  "orientation": "portrait-primary",

  "icons": [
    {
      "src": "/assets/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/assets/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/assets/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/assets/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/assets/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/assets/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/assets/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/assets/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],

  "shortcuts": [
    {
      "name": "Morning Prayer",
      "url": "/morning-prayer",
      "description": "Open Morning Prayer"
    },
    {
      "name": "Evening Prayer",
      "url": "/evening-prayer",
      "description": "Open Evening Prayer"
    },
    {
      "name": "Compline",
      "url": "/compline",
      "description": "Open Compline"
    }
  ],

  "categories": ["religion", "lifestyle"],
  "prefer_related_applications": false
}
```

---

## 7. Browser Feature Detection (Phase 7)

### 7.1 Feature Detection Results

**Storage**: Not persisted, runtime detection only

```typescript
interface BrowserCapabilities {
  // Core Features
  localStorage: boolean;
  serviceWorker: boolean;
  pushNotifications: boolean;

  // Modern APIs
  intersectionObserver: boolean;
  webShare: boolean;
  clipboard: boolean;

  // Capacitor APIs (mobile)
  capacitor: {
    available: boolean;
    platform?: "ios" | "android" | "web";
    plugins: {
      preferences: boolean;
      share: boolean;
      clipboard: boolean;
    };
  };

  // CSS Features
  gridLayout: boolean;
  customProperties: boolean;

  // Detected Issues
  unsupported: string[]; // List of missing critical features
  warnings: string[]; // List of missing optional features
}
```

### 7.2 Browser Support Matrix

**Minimum Requirements** (from constitution.md):

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Critical Features**:

- ES6+ JavaScript
- CSS Grid
- Flexbox
- localStorage
- Fetch API

**Optional Features**:

- Service Workers (for PWA)
- Web Share API (for native sharing)
- Clipboard API (for copy functionality)

---

## 8. Migration Strategy

### 8.1 Version Management

All persisted data structures include a `version` field for schema migrations.

```typescript
interface VersionedData {
  version: number; // Current: 1
  // ... data fields
}
```

### 8.2 Migration Functions

```typescript
type MigrationFunction = (oldData: any) => any;

const migrations: Record<string, MigrationFunction[]> = {
  settings_history: [
    // Version 1 → 2 (example future migration)
    (data) => {
      // Add new fields, transform data
      return { ...data, version: 2 };
    },
  ],
  performance_metrics: [
    // Version 1 → 2 (example future migration)
    (data) => {
      // Add new fields, transform data
      return { ...data, version: 2 };
    },
  ],
};
```

---

## 9. Data Constraints & Validation

### 9.1 Storage Limits

- **localStorage**: ~5-10 MB per origin (browser-dependent)
- **Capacitor Preferences**: No strict limit (iOS/Android native storage)

**Quotas**:

- Settings History: Max 50 entries (~100 KB)
- Performance Metrics: Max 100 entries (~500 KB)
- Total estimated usage: < 1 MB

### 9.2 Validation Rules

```typescript
interface ValidationRules {
  settings_history: {
    max_entries: 50;
    max_label_length: 100;
    required_fields: ["id", "timestamp", "source", "settings"];
  };

  performance_metrics: {
    max_entries: 100;
    retention_days: 30; // Auto-delete older entries
    required_fields: ["id", "timestamp", "metrics"];
  };
}
```

---

## 10. Error Handling

### 10.1 Storage Errors

```typescript
interface StorageError {
  type: "quota_exceeded" | "parse_error" | "permission_denied" | "unknown";
  key: string;
  message: string;
  timestamp: number;
}
```

**Fallback Strategy**:

1. Quota exceeded → Prune oldest entries
2. Parse error → Clear corrupted data, log error
3. Permission denied → Disable persistence, warn user
4. Unknown → Log error, continue with in-memory state

---

## 11. Privacy & Security

### 11.1 Data Privacy

- **No PII**: No personal identifiable information stored
- **No Tracking**: No user analytics or tracking
- **Local Only**: All data stays on device (except optional performance reporting)
- **User Control**: Users can clear all data via Settings

### 11.2 Optional Backend Reporting

**Performance Metrics API** (Phase 6 - Optional):

```typescript
interface PerformanceReportPayload {
  // Anonymized data only
  metrics: PerformanceMetric[];

  // No user identification
  session_id: string; // Ephemeral, not linked to user

  // Device context (aggregated only)
  user_agent: string;
  connection_type?: string;
}
```

**Endpoint**: `POST /api/performance/report` (optional, to be designed)

**Privacy**:

- No cookies or authentication
- No IP address logging
- Aggregated data only
- User opt-in required

---

## 12. Testing Data

### 12.1 Test Fixtures

```typescript
// Example Settings History Entry
const testHistoryEntry: SettingsHistoryEntry = {
  id: "test-uuid-1234",
  timestamp: 1699372800000,
  source: "manual",
  label: "Test Advent Morning Prayer",
  settings: {
    office_type: "morning_prayer",
    reading_length: "standard",
    psalms_style: "coverdale",
    calendar_year: 2025,
    show_rubrics: true,
    font_size: "medium",
    theme: "light",
  },
  settings_hash: "abc123...",
  url_encoded: "?office=mp&length=std&year=2025",
};

// Example Performance Metric
const testMetric: PerformanceMetric = {
  id: "test-metric-5678",
  timestamp: 1699372800000,
  session_id: "session-abc",
  user_agent: "Mozilla/5.0...",
  viewport: { width: 1920, height: 1080 },
  connection_type: "4g",
  metrics: {
    FCP: { value: 1200, rating: "good" },
    LCP: { value: 2100, rating: "good" },
    FID: { value: 50, rating: "good" },
    CLS: { value: 0.05, rating: "good" },
    TTFB: { value: 500, rating: "good" },
  },
  page: {
    path: "/morning-prayer",
    office_type: "morning_prayer",
    is_offline: false,
  },
};
```

---

## 13. Future Enhancements

Potential future data model extensions (not in current scope):

1. **Settings Sync**: Cloud sync across devices
2. **Custom Prayers**: User-created prayer templates
3. **Prayer Journals**: Daily prayer notes/reflections
4. **Reading Plans**: Custom lectionary schedules
5. **Audio Preferences**: Recorded audio settings

---

## Related Documents

- [spec.md](./spec.md) - Feature specification
- [plan.md](./plan.md) - Implementation plan
- [research.md](./research.md) - Technology research
- [quickstart.md](./quickstart.md) - Developer onboarding (Phase 1)

---

**Status**: ✅ Phase 1 Complete - Data models defined and validated
