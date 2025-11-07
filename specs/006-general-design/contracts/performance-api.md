# API Contracts: 006-General-Design

**Version**: 1.0  
**Date**: November 7, 2025  
**Status**: Phase 1 - Optional Contracts

## Overview

This document defines optional backend API contracts for Phase 6 enhancements. **All features in Phases 1-5 are client-side only** and do not require backend APIs.

---

## Decision: Backend APIs Are Optional

### Current Architecture (Phases 1-5)

- **Storage**: 100% client-side using DynamicStorage
- **Settings**: Stored in localStorage/Capacitor Preferences
- **Settings History**: Stored client-side only
- **Performance Metrics**: Collected and stored client-side only
- **PWA/Service Worker**: Client-side caching only

**No backend APIs required** for core functionality.

### Optional Backend (Phase 6+)

The **only potential backend API** is for **optional performance metrics reporting** to enable:

- Aggregated performance analytics across all users
- Trend analysis over time
- Performance regression detection

**This is entirely optional and requires user opt-in.**

---

## Optional API: Performance Metrics Reporting

### Endpoint: `POST /api/performance/report`

**Purpose**: Optional reporting of anonymized performance metrics for aggregate analysis.

**Status**: NOT IMPLEMENTED - Optional future enhancement

**Privacy Requirements**:

- ✅ User opt-in required
- ✅ No cookies or authentication
- ✅ No personal identifiable information (PII)
- ✅ No IP address logging
- ✅ Ephemeral session IDs only
- ✅ User can disable at any time

---

### Request Contract

#### HTTP Method

```
POST /api/performance/report
```

#### Headers

```
Content-Type: application/json
User-Agent: <client user agent string>
```

**No authentication headers** - This is an anonymous endpoint.

#### Request Body Schema

```typescript
interface PerformanceReportPayload {
  // Client Context (anonymized)
  client_version: string; // e.g., "2.1.0"
  platform: "web" | "ios" | "android";
  session_id: string; // Ephemeral UUID, not linked to user

  // Device Context (aggregated only)
  user_agent: string; // Browser user agent
  viewport: {
    width: number;
    height: number;
  };
  connection_type?: "slow-2g" | "2g" | "3g" | "4g" | "wifi" | "unknown";

  // Metrics (batch of up to 10 metrics)
  metrics: PerformanceMetric[];
}

interface PerformanceMetric {
  // Timing
  timestamp: number; // Unix timestamp (milliseconds)

  // Core Web Vitals
  metrics: {
    FCP?: MetricValue; // First Contentful Paint
    LCP?: MetricValue; // Largest Contentful Paint
    FID?: MetricValue; // First Input Delay
    CLS?: MetricValue; // Cumulative Layout Shift
    TTFB?: MetricValue; // Time to First Byte
  };

  // Page Context
  page: {
    path: string; // e.g., "/morning-prayer"
    office_type?: string; // e.g., "morning_prayer"
    is_offline?: boolean; // Was page loaded offline?
  };
}

interface MetricValue {
  value: number; // Metric value
  rating: "good" | "needs-improvement" | "poor"; // Rating based on thresholds
}
```

#### Example Request

```json
{
  "client_version": "2.1.0",
  "platform": "web",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "viewport": {
    "width": 1920,
    "height": 1080
  },
  "connection_type": "4g",
  "metrics": [
    {
      "timestamp": 1699372800000,
      "metrics": {
        "FCP": {
          "value": 1200,
          "rating": "good"
        },
        "LCP": {
          "value": 2100,
          "rating": "good"
        },
        "FID": {
          "value": 50,
          "rating": "good"
        },
        "CLS": {
          "value": 0.05,
          "rating": "good"
        },
        "TTFB": {
          "value": 500,
          "rating": "good"
        }
      },
      "page": {
        "path": "/morning-prayer",
        "office_type": "morning_prayer",
        "is_offline": false
      }
    }
  ]
}
```

---

### Response Contract

#### Success Response (201 Created)

```json
{
  "status": "success",
  "received": 1,
  "message": "Performance metrics received"
}
```

#### Rate Limited Response (429 Too Many Requests)

```json
{
  "status": "rate_limited",
  "message": "Too many requests. Please try again later.",
  "retry_after": 60
}
```

#### Validation Error Response (400 Bad Request)

```json
{
  "status": "error",
  "message": "Invalid request body",
  "errors": [
    {
      "field": "metrics",
      "message": "Metrics array must contain 1-10 items"
    }
  ]
}
```

#### Server Error Response (500 Internal Server Error)

```json
{
  "status": "error",
  "message": "Internal server error"
}
```

---

### Validation Rules

**Request Validation**:

- `client_version`: Required, semver format (e.g., "2.1.0")
- `platform`: Required, enum: ['web', 'ios', 'android']
- `session_id`: Required, valid UUID v4
- `user_agent`: Required, string, max 500 chars
- `viewport`: Required, width/height must be positive integers
- `connection_type`: Optional, enum: ['slow-2g', '2g', '3g', '4g', 'wifi', 'unknown']
- `metrics`: Required, array of 1-10 items

**Metrics Validation**:

- `timestamp`: Required, Unix timestamp (milliseconds)
- `metrics`: At least one metric (FCP, LCP, FID, CLS, or TTFB) required
- `metrics.*.value`: Required, positive number
- `metrics.*.rating`: Required, enum: ['good', 'needs-improvement', 'poor']
- `page.path`: Required, string, max 200 chars
- `page.office_type`: Optional, string, max 100 chars
- `page.is_offline`: Optional, boolean

---

### Rate Limiting

**Limits**:

- **Per IP**: 100 requests per hour
- **Per session_id**: 50 requests per hour
- **Global**: No global limit (scales horizontally)

**Headers**:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1699376400
```

---

### Privacy & Security

#### Data Minimization

**NOT COLLECTED**:

- ❌ User accounts or authentication
- ❌ Email addresses or names
- ❌ IP addresses (not logged)
- ❌ Cookies or tracking identifiers
- ❌ Settings or prayer content
- ❌ Location data

**COLLECTED (Anonymized)**:

- ✅ Ephemeral session ID (not linked to user)
- ✅ User agent string (for browser/device aggregation)
- ✅ Viewport dimensions (for responsive design analysis)
- ✅ Connection type (for performance context)
- ✅ Performance metrics (FCP, LCP, FID, CLS, TTFB)
- ✅ Page context (office type, offline status)

#### Data Retention

- **Raw metrics**: Retained for 90 days
- **Aggregated data**: Retained indefinitely (no PII)
- **Session IDs**: Not stored beyond 90 days

#### User Control

- **Opt-in required**: Feature disabled by default
- **Disable anytime**: User can disable in Settings
- **No impact**: Disabling does not affect app functionality

---

### Implementation Notes

#### Backend Implementation (Django)

```python
# site/office/api/performance.py
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from django.core.cache import cache
import uuid

class PerformanceReportThrottle(AnonRateThrottle):
    rate = '100/hour'

@api_view(['POST'])
@throttle_classes([PerformanceReportThrottle])
def report_performance(request):
    """
    Optional endpoint for collecting anonymized performance metrics.

    Privacy:
    - No authentication required
    - No user identification
    - No IP logging
    - Ephemeral session IDs only
    """
    try:
        payload = request.data

        # Validate payload
        validator = PerformanceReportValidator(data=payload)
        if not validator.is_valid():
            return Response(
                {
                    'status': 'error',
                    'message': 'Invalid request body',
                    'errors': validator.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Additional rate limiting by session_id
        session_id = payload.get('session_id')
        cache_key = f'perf_report_session_{session_id}'
        request_count = cache.get(cache_key, 0)

        if request_count >= 50:
            return Response(
                {
                    'status': 'rate_limited',
                    'message': 'Too many requests for this session.',
                    'retry_after': 3600
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Store metrics (without IP address)
        metrics = payload.get('metrics', [])
        for metric in metrics:
            PerformanceMetric.objects.create(
                client_version=payload.get('client_version'),
                platform=payload.get('platform'),
                session_id=session_id,
                user_agent=payload.get('user_agent'),
                viewport_width=payload.get('viewport', {}).get('width'),
                viewport_height=payload.get('viewport', {}).get('height'),
                connection_type=payload.get('connection_type'),
                timestamp=metric.get('timestamp'),
                fcp_value=metric.get('metrics', {}).get('FCP', {}).get('value'),
                fcp_rating=metric.get('metrics', {}).get('FCP', {}).get('rating'),
                lcp_value=metric.get('metrics', {}).get('LCP', {}).get('value'),
                lcp_rating=metric.get('metrics', {}).get('LCP', {}).get('rating'),
                fid_value=metric.get('metrics', {}).get('FID', {}).get('value'),
                fid_rating=metric.get('metrics', {}).get('FID', {}).get('rating'),
                cls_value=metric.get('metrics', {}).get('CLS', {}).get('value'),
                cls_rating=metric.get('metrics', {}).get('CLS', {}).get('rating'),
                ttfb_value=metric.get('metrics', {}).get('TTFB', {}).get('value'),
                ttfb_rating=metric.get('metrics', {}).get('TTFB', {}).get('rating'),
                page_path=metric.get('page', {}).get('path'),
                office_type=metric.get('page', {}).get('office_type'),
                is_offline=metric.get('page', {}).get('is_offline', False)
            )

        # Increment session rate limit counter
        cache.set(cache_key, request_count + 1, timeout=3600)

        return Response(
            {
                'status': 'success',
                'received': len(metrics),
                'message': 'Performance metrics received'
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        # Log error without exposing details
        logger.error(f'Performance report error: {str(e)}')
        return Response(
            {
                'status': 'error',
                'message': 'Internal server error'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

#### Frontend Implementation (Vue.js)

```javascript
// app/src/helpers/performance-reporter.js
import { getWebVitals } from "web-vitals";
import DynamicStorage from "./storage";

class PerformanceReporter {
  constructor() {
    this.enabled = false;
    this.metricsQueue = [];
    this.sessionId = this.generateSessionId();
  }

  async init() {
    // Check user opt-in
    this.enabled =
      (await DynamicStorage.getItem("performance_reporting_enabled")) ===
      "true";

    if (!this.enabled) {
      return;
    }

    // Collect Core Web Vitals
    this.collectWebVitals();
  }

  collectWebVitals() {
    getWebVitals((metric) => {
      this.metricsQueue.push({
        timestamp: Date.now(),
        metrics: {
          [metric.name]: {
            value: metric.value,
            rating: metric.rating,
          },
        },
        page: {
          path: window.location.pathname,
          office_type: this.detectOfficeType(),
          is_offline: !navigator.onLine,
        },
      });

      // Report batch when queue reaches 5 metrics
      if (this.metricsQueue.length >= 5) {
        this.reportMetrics();
      }
    });
  }

  async reportMetrics() {
    if (!this.enabled || this.metricsQueue.length === 0) {
      return;
    }

    const payload = {
      client_version: process.env.VUE_APP_VERSION,
      platform: this.detectPlatform(),
      session_id: this.sessionId,
      user_agent: navigator.userAgent,
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight,
      },
      connection_type: this.detectConnectionType(),
      metrics: this.metricsQueue.splice(0, 10), // Max 10 metrics per request
    };

    try {
      const response = await fetch(
        "https://api.dailyoffice2019.com/api/performance/report",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        }
      );

      if (!response.ok) {
        console.warn("Performance reporting failed:", response.status);
      }
    } catch (error) {
      console.warn("Performance reporting error:", error);
      // Silently fail - don't disrupt user experience
    }
  }

  generateSessionId() {
    return crypto.randomUUID();
  }

  detectPlatform() {
    if (window.Capacitor) {
      return window.Capacitor.getPlatform();
    }
    return "web";
  }

  detectConnectionType() {
    if ("connection" in navigator) {
      return navigator.connection.effectiveType;
    }
    return "unknown";
  }

  detectOfficeType() {
    const path = window.location.pathname;
    if (path.includes("morning-prayer")) return "morning_prayer";
    if (path.includes("evening-prayer")) return "evening_prayer";
    if (path.includes("compline")) return "compline";
    if (path.includes("midday-prayer")) return "midday_prayer";
    return null;
  }
}

export default new PerformanceReporter();
```

---

## Database Schema (Optional Backend)

### Performance Metrics Table

```sql
CREATE TABLE office_performancemetric (
    id SERIAL PRIMARY KEY,

    -- Client Context
    client_version VARCHAR(20) NOT NULL,
    platform VARCHAR(20) NOT NULL,
    session_id UUID NOT NULL,

    -- Device Context
    user_agent VARCHAR(500) NOT NULL,
    viewport_width INTEGER,
    viewport_height INTEGER,
    connection_type VARCHAR(20),

    -- Timestamp
    timestamp BIGINT NOT NULL,

    -- Core Web Vitals
    fcp_value FLOAT,
    fcp_rating VARCHAR(20),
    lcp_value FLOAT,
    lcp_rating VARCHAR(20),
    fid_value FLOAT,
    fid_rating VARCHAR(20),
    cls_value FLOAT,
    cls_rating VARCHAR(20),
    ttfb_value FLOAT,
    ttfb_rating VARCHAR(20),

    -- Page Context
    page_path VARCHAR(200) NOT NULL,
    office_type VARCHAR(100),
    is_offline BOOLEAN DEFAULT FALSE,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Indexes
    INDEX idx_timestamp (timestamp),
    INDEX idx_platform (platform),
    INDEX idx_page_path (page_path),
    INDEX idx_created_at (created_at)
);

-- Retention policy: Delete records older than 90 days
-- Implemented via cron job or Django management command
```

---

## Testing Contracts

### Unit Tests

```javascript
// tests/unit/helpers/performance-reporter.spec.js
describe("PerformanceReporter", () => {
  it("should generate valid session ID", () => {
    // Test UUID v4 generation
  });

  it("should detect platform correctly", () => {
    // Test web/iOS/Android detection
  });

  it("should respect user opt-in setting", () => {
    // Test enabled/disabled state
  });

  it("should batch metrics correctly", () => {
    // Test queue management (max 10 per request)
  });

  it("should construct valid API payload", () => {
    // Test payload schema compliance
  });
});
```

### Integration Tests

```python
# site/office/tests/test_performance_api.py
from rest_framework.test import APITestCase

class PerformanceReportAPITestCase(APITestCase):
    def test_valid_report(self):
        """Test successful performance report submission"""
        payload = {
            'client_version': '2.1.0',
            'platform': 'web',
            'session_id': '550e8400-e29b-41d4-a716-446655440000',
            # ... full payload
        }
        response = self.client.post('/api/performance/report', payload, format='json')
        self.assertEqual(response.status_code, 201)

    def test_rate_limiting(self):
        """Test rate limiting enforcement"""
        # Submit 101 requests and verify 429 response

    def test_invalid_payload(self):
        """Test validation error handling"""
        # Submit invalid payload and verify 400 response
```

---

## Summary

- ✅ **Phase 1-5**: No backend APIs required (client-side only)
- ⏳ **Phase 6**: Optional performance reporting API (user opt-in)
- 🔒 **Privacy-first**: No PII, no tracking, user control
- 📊 **Purpose**: Aggregate performance analytics only

**Status**: Contracts defined, implementation deferred to Phase 6 (optional)

---

## Related Documents

- [spec.md](../spec.md) - Feature specification
- [plan.md](../plan.md) - Implementation plan
- [research.md](../research.md) - Technology research
- [data-model.md](../data-model.md) - Data schemas
- [quickstart.md](../quickstart.md) - Developer onboarding

---

**Last Updated**: November 7, 2025  
**Phase**: Phase 1 (Design & Contracts)  
**Status**: ✅ Complete - Contracts defined for optional backend API
