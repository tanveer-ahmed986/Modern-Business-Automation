# Performance Optimization Specification

**Feature**: MBAS Phase 1 Performance Optimizations
**Version**: 2.0.6
**Status**: In Progress
**Created**: 2026-06-20
**Owner**: Development Team

---

## 1. Overview

### 1.1 Purpose
Optimize MBAS v2.0.5 to eliminate UI freezing and improve responsiveness on low-spec laptops (4GB RAM, HDD, older CPUs).

### 1.2 Problem Statement
Current MBAS v2.0.5 experiences:
- **UI freezing** when switching between sections (Dashboard → Inventory → Billing)
- **Slow page loads** (2-4 seconds on low-spec hardware)
- **Laggy interactions** (500ms-1s delay on search, filtering, table sorting)
- **High memory usage** (300MB+ RAM for frontend alone)

**Root Causes**:
1. Large JavaScript bundle (396KB vendor + 91KB ProductList)
2. No pagination (loading 1000+ products at once)
3. No lazy loading (all routes loaded upfront)
4. No virtual scrolling (rendering all table rows)
5. No search debouncing (API spam on every keystroke)

### 1.3 Success Criteria
- [ ] Frontend bundle size reduced to <250KB (main vendor)
- [ ] Page switches complete in <300ms (4GB RAM laptop)
- [ ] Initial page load <1.5s (cold cache)
- [ ] Search inputs respond instantly (no lag)
- [ ] Tables with 1000+ items scroll smoothly (60 FPS)
- [ ] Memory usage <150MB for frontend

---

## 2. Functional Requirements

### FR-1: Vite Build Optimization
**Priority**: High
**Description**: Optimize Vite build configuration to reduce bundle size and improve load times.

**Requirements**:
- FR-1.1: Split vendor libraries into separate chunks (react, ui components, table library)
- FR-1.2: Configure `optimizeDeps` to pre-bundle frequently used dependencies
- FR-1.3: Set chunk size warning limit to 300KB
- FR-1.4: Enable build compression (gzip)

**Acceptance Criteria**:
- Main vendor bundle <250KB (down from 396KB)
- Page-specific bundles <50KB each
- Build time <30 seconds

---

### FR-2: API Pagination
**Priority**: High
**Description**: Add pagination support to all endpoints that return lists.

**Requirements**:
- FR-2.1: Add `page` and `page_size` query parameters to endpoints
- FR-2.2: Default page size = 50 items
- FR-2.3: Return pagination metadata (total_count, page, page_size, total_pages)
- FR-2.4: Support search/filter with pagination

**Endpoints to Update**:
- `GET /inventory/products` → Paginate products
- `GET /billing/sales` → Paginate sales
- `GET /purchases` → Paginate purchases
- `GET /suppliers/{id}/payments` → Paginate payments
- `GET /suppliers/{id}/ledger` → Paginate ledger entries

**Response Format**:
```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "page_size": 50,
    "total_count": 1234,
    "total_pages": 25
  }
}
```

**Acceptance Criteria**:
- Initial page load fetches only 50 items (not 1000+)
- Pagination controls work (next, previous, jump to page)
- Search results are paginated
- Database queries use LIMIT/OFFSET

---

### FR-3: Lazy Loading Routes
**Priority**: High
**Description**: Implement lazy loading for all route components to reduce initial bundle size.

**Requirements**:
- FR-3.1: Wrap all page imports with `React.lazy()`
- FR-3.2: Add `<Suspense>` boundaries with loading fallback
- FR-3.3: Preload next likely route (e.g., Dashboard → Inventory)

**Routes to Lazy Load**:
- `/dashboard` → DashboardPage
- `/inventory` → ProductList
- `/billing` → BillingPage
- `/purchases` → PurchasePage
- `/suppliers` → SupplierLedger
- `/reports` → ReportsPage
- `/users` → UsersPage
- `/settings` → SettingsPage

**Acceptance Criteria**:
- Initial bundle loads <150KB JavaScript
- Page components load on-demand (<200ms)
- Loading spinner shown during route transition
- No flash of unstyled content (FOUC)

---

### FR-4: Virtual Scrolling
**Priority**: Medium
**Description**: Implement virtual scrolling for tables with 100+ rows to render only visible items.

**Requirements**:
- FR-4.1: Install `@tanstack/react-virtual`
- FR-4.2: Replace ProductList table with virtual scrolling
- FR-4.3: Maintain existing functionality (sorting, filtering, row selection)
- FR-4.4: Render only visible rows + 10 buffer rows

**Acceptance Criteria**:
- Tables with 1000+ items render instantly
- Only 10-20 DOM nodes (not 1000+)
- Smooth scrolling at 60 FPS
- Sorting and filtering still work

---

### FR-5: Search Debouncing
**Priority**: Medium
**Description**: Add debouncing to search inputs to prevent API spam and improve responsiveness.

**Requirements**:
- FR-5.1: Create reusable `useDebounce` hook
- FR-5.2: Apply 500ms debounce to all search inputs
- FR-5.3: Show loading indicator during search
- FR-5.4: Cancel pending requests on input change

**Search Inputs to Update**:
- ProductList search (line 82)
- BillingPage customer search
- PurchasePage supplier search
- SupplierLedger payment search

**Acceptance Criteria**:
- Search triggers only after 500ms of inactivity
- No API calls on every keystroke
- Loading indicator shown during debounce
- Previous requests cancelled (AbortController)

---

### FR-6: React Re-render Optimization
**Priority**: Low
**Description**: Optimize React components to reduce unnecessary re-renders.

**Requirements**:
- FR-6.1: Wrap expensive components with `React.memo()`
- FR-6.2: Use `useMemo()` for computed values
- FR-6.3: Use `useCallback()` for event handlers
- FR-6.4: Avoid inline object/array creation in JSX

**Components to Optimize**:
- ProductList table cells
- Dashboard metric cards
- BillingPage cart items

**Acceptance Criteria**:
- React DevTools shows <10 re-renders per interaction
- No unnecessary re-renders on state changes
- Smoother animations (Framer Motion)

---

## 3. Non-Functional Requirements

### NFR-1: Performance
- **Initial Load**: <1.5s (cold cache, 4G connection)
- **Page Switch**: <300ms (warm cache)
- **Search Response**: <500ms (after debounce)
- **Table Scroll**: 60 FPS (smooth)
- **Memory Usage**: <150MB (frontend)

### NFR-2: Compatibility
- **Browsers**: Chrome 90+, Firefox 88+, Edge 90+, Safari 14+
- **Devices**: Desktop (Windows 10/11), Laptop (4GB+ RAM)
- **Screen Sizes**: 1024x768 minimum

### NFR-3: Maintainability
- **Code Quality**: ESLint rules pass, no warnings
- **Type Safety**: TypeScript strict mode
- **Testing**: Unit tests for hooks, integration tests for pagination

### NFR-4: Backward Compatibility
- **API**: Pagination is opt-in (default page_size=1000 for legacy clients)
- **UI**: No breaking changes to existing components
- **Data**: No database schema changes

---

## 4. Technical Design

### 4.1 Frontend Architecture

**Before**:
```
App.tsx (eager import all routes)
  ├─ DashboardPage (loaded on startup)
  ├─ ProductList (loaded on startup)
  ├─ BillingPage (loaded on startup)
  └─ ... (8 routes, 500KB bundle)
```

**After**:
```
App.tsx (lazy import routes)
  ├─ Suspense
  │   └─ lazy(() => import('./features/dashboard/DashboardPage'))
  ├─ Suspense
  │   └─ lazy(() => import('./features/inventory/ProductList'))
  └─ ... (8 routes, <150KB initial + 50KB per route)
```

### 4.2 Backend API Pagination

**Endpoint**: `GET /inventory/products?page=1&page_size=50&search=laptop`

**Implementation**:
```python
from typing import Optional
from fastapi import Query

@router.get("/products")
def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    search: Optional[str] = None,
    session: Session = Depends(get_session)
):
    # Base query
    query = select(Product).where(Product.is_active == True)

    # Search filter
    if search:
        query = query.where(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.barcode.ilike(f"%{search}%")
            )
        )

    # Count total (before pagination)
    total_count = session.scalar(select(func.count()).select_from(query.subquery()))

    # Apply pagination
    offset = (page - 1) * page_size
    items = session.exec(query.offset(offset).limit(page_size)).all()

    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": (total_count + page_size - 1) // page_size
        }
    }
```

### 4.3 Virtual Scrolling Implementation

**Library**: `@tanstack/react-virtual`

**Implementation**:
```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

const ProductList = () => {
  const parentRef = useRef<HTMLDivElement>(null);
  const [products, setProducts] = useState<Product[]>([]);

  const rowVirtualizer = useVirtualizer({
    count: products.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // row height in px
    overscan: 10 // render 10 extra rows above/below viewport
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: `${rowVirtualizer.getTotalSize()}px`, position: 'relative' }}>
        {rowVirtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`
            }}
          >
            {/* Row content: products[virtualRow.index] */}
          </div>
        ))}
      </div>
    </div>
  );
};
```

### 4.4 Debounce Hook

**Implementation**:
```typescript
import { useEffect, useState } from 'react';

export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Usage:
const [searchQuery, setSearchQuery] = useState('');
const debouncedSearch = useDebounce(searchQuery, 500);

useEffect(() => {
  if (debouncedSearch) {
    fetchProducts(debouncedSearch);
  }
}, [debouncedSearch]);
```

---

## 5. Testing Strategy

### 5.1 Unit Tests
- [ ] `useDebounce` hook (500ms delay, cleanup)
- [ ] Pagination helper functions
- [ ] Virtual scrolling calculations

### 5.2 Integration Tests
- [ ] Pagination API endpoints (page 1, page 2, search + pagination)
- [ ] Lazy loading routes (load on navigation)
- [ ] Virtual scrolling (scroll to row 500)

### 5.3 Performance Tests
- [ ] Lighthouse score >90 (performance)
- [ ] Bundle size <250KB (main vendor)
- [ ] Page switch <300ms (React DevTools)
- [ ] Memory usage <150MB (Chrome DevTools)

### 5.4 User Acceptance Tests
- [ ] Test on 4GB RAM laptop (Celeron processor)
- [ ] Test with 1000+ products
- [ ] Test with slow HDD (not SSD)
- [ ] Test search responsiveness

---

## 6. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Pagination breaks existing workflows** | Medium | Default page_size=1000 for backward compatibility |
| **Virtual scrolling breaks TanStack Table** | High | Use TanStack Virtual (compatible with TanStack Table) |
| **Lazy loading causes FOUC** | Low | Add loading spinner, preload critical routes |
| **Debounce feels slow** | Low | Show loading indicator, reduce to 300ms if needed |

---

## 7. Rollout Plan

### Phase 1: Development (Week 1)
- [ ] Day 1-2: Vite optimization + lazy loading
- [ ] Day 3-4: API pagination backend
- [ ] Day 5: Virtual scrolling + debouncing

### Phase 2: Testing (Week 2)
- [ ] Day 1-2: Unit + integration tests
- [ ] Day 3: Performance testing (Lighthouse, DevTools)
- [ ] Day 4-5: UAT on low-spec hardware

### Phase 3: Deployment
- [ ] Release v2.0.6 (Tauri - performance fixes)
- [ ] Monitor performance metrics
- [ ] Gather user feedback

---

## 8. Metrics and Monitoring

### Key Performance Indicators (KPIs)
- **Bundle Size**: Target <250KB (current 396KB)
- **Page Load Time**: Target <1.5s (current 3-4s)
- **Page Switch Time**: Target <300ms (current 1-2s)
- **Memory Usage**: Target <150MB (current 300MB)
- **User Satisfaction**: Target 90%+ (survey after update)

### Monitoring Tools
- Lighthouse CI (automated performance testing)
- Chrome DevTools Performance tab
- React DevTools Profiler
- Sentry (error tracking)

---

## 9. Documentation

### 9.1 User Documentation
- [ ] Release notes (What's New in v2.0.6)
- [ ] Performance improvements guide
- [ ] Troubleshooting (slow page loads)

### 9.2 Developer Documentation
- [ ] Pagination API usage
- [ ] Lazy loading best practices
- [ ] Virtual scrolling component guide
- [ ] Debounce hook documentation

---

## 10. Success Validation

### Before (v2.0.5)
- Bundle: 396KB vendor + 91KB ProductList = **487KB**
- Page load: **3-4 seconds**
- Page switch: **1-2 seconds**
- Memory: **300MB**

### After (v2.0.6)
- Bundle: 250KB vendor + 50KB ProductList = **300KB** (38% reduction)
- Page load: **1.5 seconds** (60% faster)
- Page switch: **<300ms** (80% faster)
- Memory: **150MB** (50% reduction)

---

## 11. Constitution Compliance

✅ **2.1 Offline-First**: No changes to offline capability
✅ **2.2 Spec-Driven Development**: This spec documents all changes
✅ **2.3 Modular Feature Toggles**: No impact on feature flags
✅ **2.4 RBAC**: No changes to authentication/authorization
✅ **2.5 Financial Integrity**: No changes to transaction logic
✅ **2.6 Rebrandable**: No impact on branding system

---

END OF SPEC
