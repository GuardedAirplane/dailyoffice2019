# ADR 002: Django Backend + Vue 3 SPA Frontend Architecture

**Date**: 2025-11-11  
**Status**: Accepted  
**Deciders**: Development Team, Based on Existing Implementation  
**Context**: Inherited Architecture - Daily Office 2019 Initial Design

## Context and Problem Statement

The Daily Office 2019 application requires delivering Anglican/Episcopal daily prayer liturgies with:

- Complex liturgical calendar calculations (Easter, feast days, commemorations)
- Dynamic liturgy assembly from BCP 2019 rules
- Bible passage retrieval from Bible Gateway API
- Psalm selections from 30-day Psalter
- Canticle rotation logic
- Collect assignment rules
- Multi-platform delivery (web, iOS, Android via Capacitor)

The architecture must support both traditional web access and modern SPA experience while maintaining liturgical accuracy and enabling offline-capable mobile apps.

## Decision Drivers

- **Liturgical Complexity**: BCP 2019 rubrics require sophisticated server-side logic
- **API-First Design**: Mobile apps need RESTful API access
- **Modern UX**: Users expect responsive, app-like experience
- **Code Reusability**: Logic should be centralized, not duplicated across platforms
- **Developer Expertise**: Python (Django) for backend, JavaScript (Vue) for frontend
- **Offline Capability**: Mobile apps need client-side routing and caching
- **Deployment Flexibility**: Static frontend to Cloudflare, dynamic backend separately

## Considered Options

### Option 1: Django Monolith (Server-Side Rendering)

**Approach**: Django templates with server-side rendering, traditional multi-page app.

**Pros**:
- ✅ Simpler deployment (single application)
- ✅ SEO-friendly out of the box
- ✅ No API versioning complexity

**Cons**:
- ❌ Poor mobile app integration
- ❌ No offline capability
- ❌ Full page reloads (slower UX)
- ❌ Duplicate logic for mobile apps
- ❌ Limited interactivity

### Option 2: Full-Stack JavaScript (Next.js/Nuxt.js)

**Approach**: JavaScript everywhere with SSR/SSG framework.

**Pros**:
- ✅ Unified language (JavaScript)
- ✅ Modern developer experience
- ✅ SSR/SSG for SEO

**Cons**:
- ❌ Requires rewriting Django backend
- ❌ JavaScript less suited for complex liturgical calculations
- ❌ Team expertise is Python-based
- ❌ Migration risk for existing codebase

### Option 3: Django Backend + Vue 3 SPA Frontend (Chosen)

**Approach**: Separate concerns with RESTful API layer.

**Backend**: Django 5.2+ with Django REST Framework
**Frontend**: Vue 3 SPA with Vite + TypeScript  
**Mobile**: Capacitor wrapping Vue SPA

**Pros**:
- ✅ Clean separation of concerns
- ✅ API-first design supports all platforms
- ✅ Modern SPA experience (fast, responsive)
- ✅ Offline-capable mobile apps via Capacitor
- ✅ Independent deployment (Cloudflare for frontend, separate for backend)
- ✅ Leverages team expertise (Python + JavaScript)
- ✅ Code reuse across web and mobile
- ✅ Scalable (frontend and backend scale independently)

**Cons**:
- ⚠️ More complex deployment (two applications)
- ⚠️ API versioning required
- ⚠️ CORS configuration needed
- ⚠️ SEO requires SSG or pre-rendering

## Decision Outcome

**Chosen option**: **Django Backend + Vue 3 SPA Frontend** (Option 3)

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENTS                              │
├──────────────┬──────────────────┬─────────────────────────┬──┤
│ Web Browser  │  iOS App         │  Android App            │  │
│ (Vue 3 SPA)  │  (Capacitor)     │  (Capacitor)           │  │
└──────────────┴──────────────────┴─────────────────────────┴──┘
       │                  │                    │
       │                  └────────┬───────────┘
       │                           │
       ▼                           ▼
┌─────────────────────┐   ┌──────────────────────┐
│   Static Frontend   │   │  Mobile Apps         │
│   (Cloudflare)      │   │  (App Stores)        │
│                     │   │                      │
│ - Vue 3 SPA         │   │ - Capacitor Wrapper  │
│ - Vue Router        │   │ - Same Vue SPA       │
│ - Vuex Store        │   │ - Offline Storage    │
│ - Tailwind CSS      │   │ - Native Features    │
└─────────────────────┘   └──────────────────────┘
       │                           │
       │         HTTPS/REST API    │
       └────────────┬──────────────┘
                    ▼
         ┌─────────────────────────┐
         │   Django Backend API    │
         │   (API Server)          │
         │                         │
         │ - Django 5.2+           │
         │ - Django REST Framework │
         │ - Office Generation     │
         │ - Church Calendar       │
         │ - Bible Gateway API     │
         │ - PostgreSQL Database   │
         └─────────────────────────┘
```

### Backend Implementation

**Location**: `/site/`

**Core Apps**:
- `office/`: Daily office generation logic (FR-001, FR-002)
- `churchcal/`: Liturgical calendar calculations (FR-003)
- `bible/`: Scripture passage retrieval (FR-006)
- `psalter/`: Psalm selections from 30-day cycle (FR-007)

**API Endpoints** (site/office/api/):
```python
# Morning Prayer
GET /api/morning-prayer/<date>/
    → Returns complete Morning Prayer liturgy JSON

# Evening Prayer  
GET /api/evening-prayer/<date>/
    → Returns complete Evening Prayer liturgy JSON

# Midday Prayer
GET /api/midday-prayer/<date>/
    → Returns Midday Prayer liturgy JSON

# Compline
GET /api/compline/<date>/
    → Returns Compline liturgy JSON
```

**Response Format**:
```json
{
  "date": "2025-12-25",
  "office_type": "morning_prayer",
  "liturgical_date": {
    "name": "The Nativity of Our Lord Jesus Christ: Christmas Day",
    "rank": "PRINCIPAL_FEAST",
    "color": "WHITE"
  },
  "opening": { "sentences": [...], "antiphon": "..." },
  "psalms": [{"number": 2, "text": "...", "gloria": "..."}],
  "lessons": [{"citation": "Isaiah 9:2-7", "text": "..."}],
  "canticles": [{"name": "Te Deum", "text": "..."}],
  "prayers": { "collect": "...", "intercessions": "..." }
}
```

### Frontend Implementation

**Location**: `/app/`

**Stack**:
- Vue 3 Composition API
- Vite (build tool)
- TypeScript
- Vue Router (client-side routing)
- Vuex (state management)
- Tailwind CSS (styling)

**Key Components** (app/src/components/):
```
OfficeView.vue          - Main office display container
PsalmText.vue           - Psalm rendering with formatting
LessonText.vue          - Bible passage display
CanticleText.vue        - Canticle rendering
CollectDisplay.vue      - Collect and prayers
CalendarNavigation.vue  - Date selection interface
```

**Routing** (app/src/router/):
```javascript
{
  path: '/morning-prayer/:date?',
  component: () => import('@/views/MorningPrayerView.vue')
},
{
  path: '/evening-prayer/:date?',
  component: () => import('@/views/EveningPrayerView.vue')
}
```

### Mobile Integration

**Location**: `/app/android/`, `/app/ios/`

**Capacitor Configuration** (app/capacitor.config.ts):
```typescript
{
  appId: 'org.dailyoffice2019',
  webDir: 'dist',
  server: {
    url: 'https://api.dailyoffice2019.com',
    cleartext: false
  }
}
```

**Offline Strategy**:
- Service workers cache API responses
- Local storage for user preferences
- Progressive Web App (PWA) capabilities

### Deployment Architecture

**Frontend**:
- Build: `npm run build` → static files in `app/dist/`
- Deploy: Cloudflare Pages (CDN-distributed)
- URL: `https://www.dailyoffice2019.com`

**Backend**:
- Deploy: Git push hooks to API server
- URL: `https://api.dailyoffice2019.com`
- Database: PostgreSQL with Memcached

### Positive Consequences

1. **API Reusability**: Web and mobile apps share same backend
2. **Independent Scaling**: Frontend (CDN) and backend scale separately
3. **Developer Velocity**: Frontend and backend teams can work independently
4. **Modern UX**: SPA provides fast, app-like experience
5. **Offline Support**: Mobile apps work without connectivity
6. **Cost Efficiency**: Static frontend on Cloudflare (free tier)
7. **Testability**: Backend API easily tested in isolation

### Negative Consequences

1. **Deployment Complexity**: Two separate deployment pipelines
2. **CORS Configuration**: Required for cross-origin API requests
3. **API Versioning**: Breaking changes require version management
4. **SEO Challenges**: SPA requires SSG or pre-rendering (mitigated by Netlify pre-rendering)
5. **Authentication Complexity**: Token-based auth (JWT) vs session-based

### Mitigation Strategies

**For Deployment**:
- Automate with CI/CD pipelines
- Frontend: Cloudflare Pages auto-deploy on git push
- Backend: Git post-receive hooks

**For CORS**:
- Django CORS headers middleware
- Whitelist frontend domains

**For SEO**:
- Pre-render SPA with Netlify
- robots.txt and sitemap.xml
- Meta tags in index.html

**For Authentication**:
- JWT tokens with refresh mechanism
- Capacitor Secure Storage for mobile

## Validation

**Metrics**:
- ✅ API response time: 700-800ms (acceptable for liturgy generation)
- ✅ Frontend build time: ~2 minutes
- ✅ Mobile app size: ~15MB (iOS), ~20MB (Android)
- ✅ Offline capability: Yes (via service workers)
- ✅ Cross-platform code reuse: ~95% (Vue SPA shared across web/mobile)

**Success Criteria Met**:
- ✅ Web, iOS, and Android apps from single codebase
- ✅ API-first design enables future integrations
- ✅ Modern UX with fast page transitions
- ✅ Independent frontend/backend deployment

## References

- FR-001: Morning Prayer Generation (`specs/001-daily-office/requirements.md`)
- FR-002: Evening Prayer Generation
- Backend Implementation: `site/office/`
- Frontend Implementation: `app/src/`
- API Documentation: `specs/001-daily-office/contracts/README.md`

## Related Decisions

- ADR 001: Production Database Testing (affects API testing strategy)
- ADR 003: BCP 2019 Modular Structure (backend organization)
- ADR 005: Performance Monitoring (API instrumentation)
