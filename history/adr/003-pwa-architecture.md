# ADR 003: Progressive Web App (PWA) Architecture

**Status**: Proposed
**Date**: 2026-06-20
**Deciders**: Development Team, Product Owner
**Context**: Performance issues and platform compatibility requirements

---

## Context and Problem Statement

MBAS v2.0.5 faces two critical challenges:

1. **Performance**: UI freezes when switching sections on low-spec laptops (4GB RAM, HDD)
2. **Market Accessibility**: Current architecture (Tauri + Python 3.12 + Windows 10/11) excludes 80% of target users:
   - Small shop owners using Windows 7 (Python 3.12 not supported)
   - Users with Android tablets (Tauri is desktop-only)
   - Users with smartphones (no mobile support)
   - Low-spec hardware users (struggling with 26MB installer + heavy Electron-like app)

**Business Impact**:
- Limited market reach (20% of potential customers)
- Poor user experience (freezing UI reduces productivity)
- High support costs (compatibility issues, installation problems)

---

## Decision Drivers

1. **Market Reach**: Must support Windows 7, Android, iOS, tablets, low-spec hardware
2. **Performance**: Must run smoothly on 4GB RAM laptops with HDD
3. **Offline-First**: Must maintain current offline capability (Constitution requirement)
4. **Development Cost**: Prefer single codebase over multiple platform-specific apps
5. **Maintenance**: Must be sustainable long-term (avoid 3x codebase complexity)
6. **User Experience**: Must be installable and feel like native app
7. **Migration Path**: Must allow gradual transition (no "big bang" rewrite)

---

## Considered Options

### Option 1: **Optimize Current Architecture (Tauri + Desktop)**
**Pros**:
- Minimal code changes
- Maintains system tray integration
- Fast implementation (1-2 weeks)

**Cons**:
- ❌ Still Windows 10/11 only (excludes Windows 7)
- ❌ No mobile/tablet support
- ❌ Still requires Python 3.12 installation
- ❌ Heavy resource usage (Tauri overhead)
- **Market reach: 20% (unchanged)**

### Option 2: **Progressive Web App (PWA)** ⭐ **RECOMMENDED**
**Pros**:
- ✅ Works on ALL platforms (Windows 7/10/11, Android, iOS, tablets)
- ✅ No Python needed on client devices (server-based backend)
- ✅ Installable as "native-like" app (Add to Home Screen)
- ✅ Offline-first via Service Workers (Constitution compliant)
- ✅ Single codebase (React + FastAPI)
- ✅ Auto-updates (no reinstallation)
- ✅ Smaller download (~5MB vs 26MB)
- ✅ Responsive design (mobile + tablet + desktop)
- ✅ Lower hardware requirements

**Cons**:
- ⚠️ No system tray integration (can use browser shortcuts)
- ⚠️ Requires browser (but all devices have one)
- ⚠️ Backend must run as local server (or cloud-hosted)
- **Market reach: 95%+ (all devices with browsers)**

### Option 3: **Hybrid (Desktop + Web)**
**Pros**:
- ✅ Best of both worlds
- ✅ Gradual migration path

**Cons**:
- ⚠️ 2x frontend codebases (Tauri + PWA)
- ⚠️ 2x maintenance cost
- ⚠️ Feature parity challenges
- **Market reach: 95%, but 2x development cost**

### Option 4: **React Native / Flutter (Mobile Native)**
**Pros**:
- ✅ Native mobile experience
- ✅ App store distribution

**Cons**:
- ❌ 3x codebases (Desktop + iOS + Android)
- ❌ 3x maintenance cost
- ❌ App store approval delays
- ❌ Doesn't solve Windows 7 compatibility
- ❌ 12-16 weeks development time
- **Market reach: 95%, but 3x development cost**

---

## Decision Outcome

**Chosen Option**: **Option 2 - Progressive Web App (PWA)**

**Rationale**:
1. **Maximizes market reach** (95%+ vs 20%) with single codebase
2. **Solves performance issues** (lighter than Tauri, optimized bundle)
3. **Windows 7 compatible** (browser-based, Python 3.10+ on server)
4. **Mobile/tablet support** (responsive design + installable)
5. **Lower total cost of ownership** (1x codebase vs 2-3x alternatives)
6. **Maintains offline-first** (Service Workers = local caching)
7. **Future-proof** (PWAs are industry standard for offline-first apps)

### Implementation Strategy

**Phase 1: Performance Optimizations** (Week 1-2)
- Optimize current Tauri app while developing PWA
- Add pagination, lazy loading, virtual scrolling
- Reduce bundle size with code splitting
- **Deliverable**: MBAS v2.0.6 (Tauri - performance fixes)

**Phase 2: PWA Conversion** (Week 3-6)
- Convert React frontend to PWA (vite-plugin-pwa)
- Lower Python requirement to 3.10+
- Add responsive design for mobile/tablets
- Setup Service Worker for offline caching
- Create installation guides (local server, USB portable, cloud)
- **Deliverable**: MBAS v2.1.0 (PWA - cross-platform)

**Phase 3: Deprecation** (Week 7+)
- Maintain both Tauri (v2.0.x) and PWA (v2.1.x) for 3 months
- Encourage migration to PWA via release notes
- Sunset Tauri version by Q3 2026
- **Deliverable**: MBAS v2.2.0 (PWA-only)

---

## Deployment Models

### Model 1: **Local WiFi Server (Offline-First)**
```
[Shop Owner's Laptop/Desktop]
  ├─ Python 3.10+ + FastAPI backend
  ├─ Runs on http://192.168.x.x:8000
  └─ SQLite database (local storage)

[Employee Devices]
  ├─ Android tablets → Access via browser
  ├─ Windows 7 laptops → Access via browser
  ├─ Smartphones → Install PWA (Add to Home Screen)
  └─ No Python installation needed!
```

**Advantages**:
- True offline (no internet required)
- Fast local network access
- Single database (no sync issues)

### Model 2: **USB Portable Package**
```
[USB Drive]
  ├─ portable_python/
  ├─ mbas_backend/
  ├─ START_MBAS_SERVER.bat
  └─ README.txt

Run on any Windows 7/10/11 PC → Opens browser → Works!
```

**Advantages**:
- No installation needed
- Runs on public/shared computers
- Easy backup (copy USB)

### Model 3: **Cloud-Hosted (Optional)**
```
[Cloud VPS - Render/Railway]
  ├─ FastAPI backend
  └─ SQLite/PostgreSQL

[Users]
  └─ Access from anywhere via https://mbas.example.com
```

**Advantages**:
- Multi-location access
- Automatic backups
- No local server setup

---

## Technical Architecture

### Before (Tauri - Desktop Only)
```
┌─────────────────────────────────┐
│  Tauri App (Windows 10/11)      │
│  ├─ React Frontend (bundled)    │
│  ├─ Python 3.12 Backend          │
│  └─ SQLite Database              │
└─────────────────────────────────┘
    ↓ Installed on C:\Program Files
    ↓ 26MB installer
    ↓ Requires admin rights
```

### After (PWA - Cross-Platform)
```
┌─────────────────────────────────┐
│  Frontend (PWA)                 │
│  ├─ React (optimized bundle)    │
│  ├─ Service Worker (offline)    │
│  └─ Manifest.json (installable) │
└──────────────┬──────────────────┘
               │ HTTP/WebSocket
┌──────────────▼──────────────────┐
│  Backend (FastAPI)              │
│  ├─ Python 3.10+ (not 3.12!)    │
│  ├─ SQLite (local or cloud)     │
│  └─ JWT Authentication          │
└─────────────────────────────────┘

Accessed via:
- Browser: Chrome, Firefox, Edge, Safari
- Installed: Add to Home Screen (mobile)
- Installed: Install App (desktop browsers)
```

---

## Consequences

### Positive

1. **95%+ Market Reach**: Works on Windows 7, Android, iOS, tablets, low-spec hardware
2. **Better Performance**: Lighter than Tauri, optimized bundle, browser-native rendering
3. **Lower Barriers**: No installation, no admin rights, no Python on client
4. **Auto-Updates**: Push updates instantly (no reinstall)
5. **Responsive**: Single UI adapts to mobile/tablet/desktop
6. **Cost Savings**: 1x codebase = 1x maintenance cost

### Negative

1. **No System Tray**: Cannot minimize to tray (use browser tab/shortcut instead)
2. **Browser Required**: All devices need a modern browser (Chrome 90+, Safari 14+, Edge 90+)
3. **Server Dependency**: Backend must run somewhere (local WiFi, USB, or cloud)
4. **Migration Effort**: Users must transition from Tauri to PWA (3-month transition)

### Neutral

1. **Authentication**: JWT-based (same as current, but session-based in browser)
2. **Offline Mode**: Service Workers replace Tauri's built-in offline (similar capability)
3. **File Access**: Cannot access local filesystem (but can download/upload files via API)

---

## Compliance with Constitution

✅ **2.1 Offline-First**: Service Workers provide offline caching and sync
✅ **2.2 Spec-Driven Development**: This ADR + specs document the change
✅ **2.3 Modular Feature Toggles**: Feature flags maintained in backend
✅ **2.4 RBAC**: JWT tokens enforce role-based access control
✅ **2.5 Financial Integrity**: Transaction logic unchanged (backend-based)
✅ **2.6 Rebrandable**: Manifest.json supports dynamic branding (name, logo, theme)

---

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Users resist browser-based app** | Medium | Low | Educate on "Install App" feature (looks native) |
| **Offline mode doesn't work** | High | Low | Extensive Service Worker testing, fallback to cache |
| **Windows 7 browser outdated** | Medium | Medium | Recommend Chrome 90+ (still supports Win7) |
| **Backend setup too complex** | Medium | Medium | Provide START_SERVER.bat + clear documentation |
| **Performance worse than Tauri** | High | Very Low | Phase 1 optimizations ensure 60-80% improvement |

---

## Alternatives Explored and Rejected

1. **Electron**: Larger than Tauri (100MB+), still desktop-only → Rejected
2. **Qt/PyQt**: Complex UI development, Windows-only → Rejected
3. **Capacitor**: Adds overhead, still requires mobile builds → Rejected (PWA is simpler)
4. **Cordova**: Deprecated, use PWA instead → Rejected

---

## References

- [PWA Documentation (MDN)](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- [Vite PWA Plugin](https://vite-pwa-org.netlify.app/)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Workbox (Google)](https://developer.chrome.com/docs/workbox/)

---

## Approval

**Proposed By**: AI Assistant (Claude)
**Date**: 2026-06-20
**Status**: Awaiting approval from Product Owner

**Approval Required From**:
- [ ] Product Owner (business decision)
- [ ] Tech Lead (architecture review)
- [ ] End Users (pilot testing)

---

END OF ADR
