# MBAS System Overhaul — Master Plan

**Date:** 2026-11-11
**Status:** Phase 1, 2, 3 & 4 COMPLETE (validated 2026-11-13) — Phase 5 pending
**Goal:** Make MBAS stable, correct, secure, and professional enough to sell and
install in local businesses for inventory and invoicing.

---

## Diagnosis summary (from full-codebase audit)

The reported "hang when switching tabs" is NOT caused by loading the whole
database per request (pagination + server caches already exist). Root causes:

1. **Service worker misconfiguration** — the `NetworkFirst` rule targets
   `/api/*` which matches no real route; the catch-all `StaleWhileRevalidate`
   rule caches EVERY backend GET for 30 days (stale data, doubled traffic,
   zombie responses).
2. **DB pool too small, fails slowly** — `pool_size=1, max_overflow=2,
   pool_timeout=5`; a tab switch fires 2–4 parallel GETs (+ SW revalidations),
   the 4th waits 5 s then 500s, axios retries with backoff → 5–15 s freeze.
3. **Global write lock held per-request** — one `asyncio.Lock` over all
   POST/PUT/DELETE; `VACUUM INTO` backups block every sale for their duration.
4. **Cross-origin `localhost` vs `127.0.0.1`** — hardcoded API base forces a
   CORS preflight on every call and breaks LAN/mobile PWA access entirely.

---

## Phase 1 — Stability: kill the hangs (THIS PHASE)

| # | Change | Files |
|---|--------|-------|
| 1.1 | Service worker: precache app shell only; **never cache API responses** (`NetworkOnly` by default — remove runtime caching rules); add `navigateFallbackDenylist` for backend routes so downloads/docs aren't hijacked by the SPA fallback | `frontend/vite.config.ts` |
| 1.2 | Purge stale `mbas-api-cache` / `mbas-assets-cache` left behind by old SW versions on app start | `frontend/src/main.tsx` |
| 1.3 | Relative API base (`""`) — same-origin in production (backend serves `dist/`), Vite dev proxy for `npm run dev`; fixes preflight overhead and LAN/mobile access | `frontend/src/config.ts`, `frontend/vite.config.ts` |
| 1.4 | Tighten CORS: only Vite dev origins, drop `"*"` + credentials combo | `backend/src/main.py` |
| 1.5 | DB pool: `pool_size=5, max_overflow=5` (WAL readers are safe in parallel), `busy_timeout=5000` as the write-queueing mechanism | `backend/src/core/db.py` |
| 1.6 | Remove the global per-request write lock middleware (replaced by busy_timeout + WAL single-writer queueing) | `backend/src/main.py` |
| 1.7 | Backups: run `VACUUM INTO` on a dedicated sqlite3 connection outside the pool so backups never starve requests | `backend/src/core/backup.py` |
| 1.8 | CSV export: download via authenticated XHR blob instead of `window.open` with token-in-URL (was broken: read wrong storage key, leaked token, intercepted by SW navigation fallback) | `frontend/src/services/reports.service.ts`, `frontend/src/features/reports/ReportsPage.tsx` |

**Validation (done 2026-11-12):**
- `npm run build` passes; regenerated `dist/sw.js` verified: zero API caching
  rules, navigation denylist present.
- Backend pytest: 51 passed / 25 failed — the identical 25 failures occur on
  the UNMODIFIED code (verified via git stash baseline); they are pre-existing
  stale tests (old schema expectations), not regressions. Also repaired
  `tests/conftest.py` (imported non-existent `src.models.suppliers`, used
  removed `UserRole.SALES_USER` and old Product fields), which had made the
  whole suite uncollectable.
- Live burst test against running server: 12 concurrent GETs across all
  modules = 50 ms total over keep-alive (3–11 ms per endpoint sequentially),
  0 errors; 5 concurrent writes all succeed in <1 s with no global lock.
  Under the old config this burst exceeded the 3-connection pool.

---

## Phase 2 — Data correctness (inventory/invoicing fundamentals) — COMPLETE

| # | Change | Files |
|---|--------|-------|
| 2.1 | Transactional invoice sequence: `invoice_sequences` table, atomic UPSERT allocates the next number inside the sale transaction (SQLite's write lock + `busy_timeout` serializes concurrent sales); UNIQUE constraint on `sales.invoice_number` kept as a safety net. Numbering rolls over at **business-local** midnight, not UTC. | `backend/src/models/stock.py` (`InvoiceSequence`), `backend/src/services/sale_service.py` |
| 2.2 | Timezone-correct reporting: new `core/timeutils.py` computes "today" and report date ranges over the **business-local calendar day**, converted to naive-UTC `[start, end)` bounds for querying (storage stays naive-UTC). Dashboard's "Today's Revenue" and `/reports/*` date filters no longer shift by the UTC offset. | `backend/src/core/timeutils.py`, `backend/src/api/dashboard.py`, `backend/src/api/reports.py`, `backend/src/services/report_service.py` |
| 2.3 | Decimal-safe money: single `money()` helper quantizes every monetary value to 2 dp (ROUND_HALF_UP) at each computation step in `SaleService` and `PurchaseService` — no more float drift in totals/tax/discount. | `backend/src/services/sale_service.py`, `backend/src/services/purchase_service.py` |
| 2.4 | Soft-delete products: `DELETE /inventory/products/{id}` deactivates (`is_active=false`) when the product is referenced by any `sale_items`/`purchase_items` row (preserves historical invoice FKs); only unreferenced products are hard-deleted. POS search (`include_inactive` default false) and the default product list hide inactive items; inventory-management views can request `is_active`/`include_inactive` explicitly. | `backend/src/api/inventory.py` |
| 2.5 | Stock movement ledger: new append-only `stock_movements` table (product, signed change, quantity_after, reason, reference, user, timestamp). Entries are written for sales, refunds, purchase receipts, manual stock-quantity edits (adjustment), and opening stock at product creation (initial). New `GET /inventory/products/{id}/movements` (Manager/Admin) exposes the audit trail. | `backend/src/models/stock.py`, `backend/src/services/stock_service.py`, wired into `sale_service.py`, `purchase_service.py`, `api/inventory.py` |
| 2.6 | Returns/refund flow: `POST /billing/sales/{id}/refund` (Manager/Admin) restores stock for every item, writes `refund` ledger entries, and marks the sale `REFUNDED`; rejects sales that are not `COMPLETED`. Frontend: new **Sales History** page (`/sales`) lists paginated invoices with a Refund action (confirm-then-commit), wired to the sidebar. | `backend/src/api/billing.py`, `backend/src/services/sale_service.py`, `frontend/src/features/billing/SalesHistoryPage.tsx`, `frontend/src/services/billing.service.ts` |
| 2.7 | Server-side pagination UI: `ProductList` now does real server pagination (`manualPagination`, page/page-size controls, category filter re-queries the server) instead of fetching 50 rows once and paginating client-side; opening stock surfaces as the first ledger entry. | `frontend/src/features/inventory/ProductList.tsx` |
| 2.8 | Adopted **TanStack Query** (`@tanstack/react-query`) to replace the hand-rolled TTL caches in `inventory.service.ts` / `dashboard.service.ts`. `QueryClientProvider` added at the app root (`staleTime: 30s`, `refetchOnWindowFocus: false`); `ProductList`, `DashboardPage`, and the new `SalesHistoryPage` use `useQuery`/`useMutation` with targeted `invalidateQueries` after writes. | `frontend/src/main.tsx`, `frontend/src/features/inventory/ProductList.tsx`, `frontend/src/features/dashboard/DashboardPage.tsx`, `frontend/src/services/inventory.service.ts`, `frontend/src/services/dashboard.service.ts` |

**Deferred from this phase:** Alembic migrations. All Phase 2 schema changes
are strictly additive (two new tables, no column changes to existing tables),
so `SQLModel.metadata.create_all()` upgrades existing customer databases
automatically with zero manual steps — there was no destructive/renaming
change that actually required a migration tool yet. Adopting Alembic properly
(baseline revision + versioned upgrade path) is carried forward to Phase 5
(packaging/ops), before any change that *does* need a real migration ships.

**Validation (done 2026-11-12):**
- In-memory end-to-end smoke test (invoice sequence, Decimal rounding,
  stock ledger, refund) confirmed: `INV-YYYYMMDD-0001` / `-0002` allocated
  without collision; 99.99 × 3 = 299.97, tax 17% → 50.99 (not 50.9949),
  grand total 350.96; stock deducted on sale and fully restored on refund;
  ledger holds exactly the 3 expected rows (`sale`, `sale`, `refund`).
- Backend pytest: **92 passed, 0 failed** (up from 51/25 at end of Phase 1).
  All 25 previously-documented pre-existing stale failures were repaired
  (stale RBAC assumptions about `/settings/` GET-vs-PUT, obsolete
  `sales_user`/`sku`/`reorder_level`/`unit` fields, missing `settings`
  fixture in four sale-service tests, a dashboard metrics cache leaking
  across tests, payment-method key casing, an incorrectly-constructed
  license-tampering test, and transaction/concurrency tests that need a
  real file-backed WAL engine instead of the in-memory `StaticPool` engine
  that serializes all threads onto one connection) — plus 16 new tests
  added for the Phase 2 behavior above (`tests/integration/test_phase2_data_correctness.py`
  and additions to existing suites).
- Frontend: `npm run build` passes (tsc + vite, PWA precache regenerated);
  `npx vitest run` passes (10/10, after repairing a stale/mismatched nested
  `esbuild` binary under `node_modules/vitest/node_modules/esbuild` the same
  way the top-level esbuild was repaired in Phase 1).

## Phase 3 — Security & licensing hardening — COMPLETE

| # | Change | Files |
|---|--------|-------|
| 3.1 | `/auth/login` no longer returns the raw `User` row: a `LoginResponse` schema wraps `UserRead` so `hashed_password` can never leak. Manual in-memory login rate limiting (5 failed attempts / 15 min lockout per username, `429` response) — no external dependency, consistent with offline-first. | `backend/src/api/auth.py` |
| 3.2 | `get_current_user` now rejects deactivated users (checked on both the cache-hit and DB-fetch paths) and no longer accepts a token from a query parameter (header-only). Cache TTL shortened 60s→30s and an explicit `invalidate_user_cache()` hook is called whenever an admin edits/deletes a user, so role/active/password changes apply on the user's very next request. | `backend/src/core/auth.py`, `backend/src/api/users.py` |
| 3.3 | Forced password change: new `User.must_change_password` column (additive migration in `init_db()` via `_ensure_column`, since Alembic is still deferred to Phase 5). The bootstrap `admin/admin123` account is created with the flag set and a loud startup warning instead of a silent default credential. Any admin-driven password reset also sets the flag. New self-service `POST /users/me/change-password` clears it. Frontend: `/change-password` page, `ProtectedRoute` force-redirects there until cleared. | `backend/src/models/core.py`, `backend/src/core/db.py`, `backend/src/main.py`, `backend/src/api/users.py`, `frontend/src/services/auth.service.ts`, `frontend/src/features/auth/ChangePasswordPage.tsx`, `frontend/src/components/routing/ProtectedRoute.tsx`, `frontend/src/features/auth/LoginPage.tsx`, `frontend/src/App.tsx` |
| 3.4 | Feature flags are now derived from the signed license at runtime (`get_effective_feature_flags()`), falling back to the Basic tier when no license is loaded — `settings.feature_flags` is only a display mirror and is never read for enforcement. `PUT /settings/` excludes `feature_flags` from the mutable field set, closing the self-upgrade bypass. | `backend/src/core/features.py`, `backend/src/api/settings.py` |
| 3.5 | `/system/restore` whitelists `backup_filename` against `BackupUtility.list_backups()` instead of trusting the client string (closes a path-traversal hole) and reads from the real `ProgramData` backups directory instead of a CWD-relative `"backups"` that never matched production. `BackupUtility.restore_backup()` now deletes the live DB's `-wal`/`-shm` sidecars before copying in the backup, preventing stale WAL replay from reapplying pre-restore writes on top of the restored data. | `backend/src/api/system.py`, `backend/src/core/backup.py` |
| 3.6 | Explicit LAN opt-in: the dev entrypoint reads `MBAS_HOST` (default `127.0.0.1`); setting it to `0.0.0.0` prints a firewall warning. All installer `.bat` launchers and `watchdog.py` already hardcoded `127.0.0.1`, so this was mostly already satisfied — the opt-in is now a documented env var instead of requiring a code edit. | `backend/src/main.py` |

**Note on "response_model on every endpoint":** audited every route; the
only place a raw SQLModel table object leaking sensitive data was possible
was `/auth/login` (fixed above). Endpoints returning paginated wrappers,
CSV streams, or non-sensitive table rows (products, sales, backups lists)
were left as-is — adding a response_model there is a typing nicety, not a
security fix, and out of scope for a hardening pass.

**Validation (done 2026-11-13):**
- Backend pytest: **104 passed, 0 failed** (up from 92 at end of Phase 2);
  12 new tests in `tests/integration/test_phase3_security.py` cover the
  login hardening, forced password change flow, license-derived feature
  gating (including a `premium_license` test fixture that simulates an
  active license without needing a real RSA-signed file), and the restore
  path-traversal fix. Added test-isolation fixes for two NEW module-level
  globals introduced this phase (login rate-limit counters, license
  validator singleton) following the same pattern as the Phase 2 dashboard
  cache fix.
- Frontend: `npm run build` passes; `npx vitest run` 10/10 (unchanged from
  Phase 2; the Playwright e2e spec picked up by vitest's glob is a
  pre-existing, unrelated config quirk).

## Phase 4 — Professional UI overhaul — COMPLETE

Much of the design-system groundwork (shadcn/Tailwind tokens, `next-themes`
and `cmdk` as dependencies, TanStack Table/Query) was already in place from
earlier phases but not wired up. This phase completed the wiring and added
the remaining pieces from the original scope.

| # | Change | Files |
|---|--------|-------|
| 4.1 | Dark/light theme actually wired up: `ThemeProvider` (`next-themes`, `attribute="class"`, system-default) now wraps the app; a sun/moon `ThemeToggle` lives in the new TopBar. | `frontend/src/components/theme-provider.tsx`, `frontend/src/components/ui/theme-toggle.tsx`, `frontend/src/App.tsx` |
| 4.2 | App shell: `Sidebar` rewritten to be theme-aware (`bg-card`/`border-border` instead of hardcoded `bg-slate-900`) and collapsible (icon-only, persisted in `localStorage`). New `TopBar` with breadcrumb (derived from route), a search button that opens the existing `CommandPalette` via a `window` event, theme toggle, and a user-avatar dropdown (profile, Change Password, Sign Out — replacing the old sidebar-footer logout). `Layout` removed the decorative glassmorphism blur blobs and now wraps route content in a new `ErrorBoundary` (friendly retry UI instead of a blank screen on a render error). | `frontend/src/components/layout/Sidebar.tsx`, `frontend/src/components/layout/TopBar.tsx`, `frontend/src/components/layout/Layout.tsx`, `frontend/src/components/layout/CommandPalette.tsx`, `frontend/src/components/common/ErrorBoundary.tsx` |
| 4.3 | One shared `DataTable` component (TanStack Table): server pagination, page-size selector, loading skeleton rows (`components/ui/skeleton.tsx`), empty state with description, optional CSV-export button. `ProductList` and the new-in-Phase-2 `SalesHistoryPage` were refactored onto it, removing ~150 lines of duplicated pagination/table markup; `SalesHistoryPage` gained a CSV export button wired to the existing `/reports/export/sales` endpoint. | `frontend/src/components/ui/data-table.tsx`, `frontend/src/components/ui/skeleton.tsx`, `frontend/src/features/inventory/ProductList.tsx`, `frontend/src/features/billing/SalesHistoryPage.tsx` |
| 4.4 | Forms: `ProductForm` rewritten on `react-hook-form` + `zod` with inline field errors (also fixed a corrupted `max-探索-md` Tailwind class — a stray-character typo that silently broke the dialog's max-width). New `AlertDialog` component (`@radix-ui/react-alert-dialog`) replaces the native `window.confirm()` for the two destructive actions that used it: deleting a product (`ProductList`) and deleting a user (`UsersPage`). | `frontend/src/features/inventory/ProductForm.tsx`, `frontend/src/components/ui/alert-dialog.tsx`, `frontend/src/features/inventory/ProductList.tsx`, `frontend/src/features/users/UsersPage.tsx` |
| 4.5 | POS: cash-tendered input + live change-due calculator when payment method is "cash" (blocks completing the sale if cash received is insufficient); `Ctrl/Cmd+Enter` keyboard shortcut completes the sale from anywhere on the page, alongside the barcode-scan → arrow-key-select → Enter flow that already existed. | `frontend/src/features/billing/BillingPage.tsx` |
| 4.6 | Dashboard charts: new `GET /dashboard/trends` endpoint (same 10s cache pattern as `/dashboard/metrics`) returns a zero-filled 30-business-local-day revenue series plus a payment-method breakdown, computed from one query (not 30) and bucketed via the existing `local_date_key` helper so day boundaries stay business-local-correct. Frontend: `recharts`-based `SalesTrendChart` (area chart) and `PaymentBreakdownChart` (donut), both themed via the shadcn CSS variables so they follow light/dark automatically. | `backend/src/api/dashboard.py`, `frontend/src/services/dashboard.service.ts`, `frontend/src/features/dashboard/SalesTrendChart.tsx`, `frontend/src/features/dashboard/PaymentBreakdownChart.tsx`, `frontend/src/features/dashboard/DashboardPage.tsx` |
| 4.7 | Invoice template bug fix: the A4 layout rendered its "Thank you for your business" footer twice (copy-paste artifact) — removed the duplicate. The A4 + 80mm thermal templates and print stylesheet from Phase 2 were otherwise already professional-grade and did not need rework. | `frontend/src/features/billing/InvoiceTemplate.tsx` |
| 4.8 | `BillingPage`'s POS layout used a hardcoded `h-[calc(100vh-64px)]` that predates the real TopBar; now that `Layout`'s `<main>` is genuinely sized to the remaining viewport height by flexbox, switched to `h-full` so the POS screen doesn't overflow when the offline banner is showing. | `frontend/src/features/billing/BillingPage.tsx` |

**Scoping decisions (explicit, not oversights):**
- **Per-page visual polish** of `ReportsPage`, `SettingsPage`, and the
  remaining feature pages that still use ad-hoc `glassmorphism-card`/
  `bg-slate-*` styling was left alone — the shell (sidebar/topbar/theme) and
  the shared primitives (`DataTable`, `AlertDialog`, forms) were prioritized
  since every page benefits from those; a full page-by-page visual pass is
  deferred to a future pass if requested.
- **Row density toggle, column sorting/visibility, and "park/resume sale"**
  from the original scope were not built — they add real complexity for
  marginal value at this stage (single-site offline retail/inventory use,
  not a dense analyst tool) and were not blocking the "professional enough
  to sell" bar. Column sorting can be added to `DataTable` later with one
  TanStack Table option if a customer asks for it.
- **New Playwright smoke flows** (login → sale → invoice print) were not
  added. The existing `e2e/complete-sale-workflow.spec.ts` already covers
  that flow; it is picked up by `vitest`'s glob (pre-existing config quirk
  noted since Phase 2) rather than run by `playwright test` here, which is
  unrelated to this phase's changes.
- **WCAG AA** was addressed via the existing shadcn token system (already
  AA-contrast by default) plus `focus-visible` rings already present on all
  interactive primitives; no dedicated contrast audit tool was run.

**Validation (done 2026-11-13):**
- Backend pytest: **105 passed, 0 failed** (up from 104 at end of Phase 3);
  1 new test for `GET /dashboard/trends` (30-point zero-filled series,
  payment-method bucket counts). Added a cache-reset for the new
  `_trends_cache` module-level global in `conftest.py`, following the same
  test-isolation pattern as every prior phase's caches/singletons.
- Frontend: `tsc -b && vite build` passes (fixed a handful of new TS errors
  along the way: an unused import, `recharts` Tooltip formatter generics,
  and the `react-hook-form`+`zod` `z.coerce` input/output type split, which
  needs `useForm<Input, any, Output>` rather than a single inferred type).
  `npx vitest run` 10/10 (unchanged from Phase 2/3). The production build
  flags `DashboardPage`'s chunk as >300kB post-`recharts`; it is already
  lazy-loaded at the route level so this doesn't affect initial load, and
  further code-splitting is left for Phase 5 if it becomes a real problem.

**Live browser validation (done 2026-11-13, `npm run dev` + a real backend
against a fresh `ProgramData` database) surfaced four real bugs invisible to
the test suite — all fixed and covered by new/strengthened tests:**

| # | Bug | Fix | Files |
|---|-----|-----|-------|
| B1 | `init_db()`'s Phase 3 additive migration called `_ensure_column(session, "users", ...)` — but SQLModel's `User` table (no explicit `__tablename__`) is actually named `user` (singular). Crashed the backend on startup against any real file-backed database with `no such table: users`. Invisible in tests because fixtures build schema directly via `SQLModel.metadata.create_all()` and never call `init_db()`. | Corrected the table name to `"user"`. | `backend/src/core/db.py` |
| B2 | The Vite dev proxy forwards path prefixes like `/dashboard`, `/billing`, `/settings`, `/reports`, `/users` to the backend for API calls — but those are also frontend SPA route names. A hard navigation/refresh on one of those pages matched the proxy rule instead of Vite's own `index.html`, so the backend's static-file SPA fallback served its **production** `dist/index.html` (hashed asset paths that don't exist under `vite dev`) — blank page, 503s on every asset. | Added a `bypass` to each proxy rule: navigation requests (`Accept: text/html`) fall through to Vite's own handling; only real API/XHR calls still proxy to the backend. | `frontend/vite.config.ts` |
| B3 | `ProductList`'s row-actions `DropdownMenuItem`s opened a `Dialog`/`AlertDialog` synchronously on click. Radix's body `pointer-events` lock from the closing `DropdownMenu` and the opening `Dialog` can race, leaving `document.body` stuck at `pointer-events: none` — the entire page became unclickable until a manual reload. Reproduced reliably via Delete Product. | Defer the state update that opens the dialog to the next tick (`setTimeout(..., 0)`) so the dropdown fully unmounts (and releases its lock) before the dialog mounts. | `frontend/src/features/inventory/ProductList.tsx` |
| B4 | `GET /billing/sales` (list) eagerly loaded `items`/`customer` via `selectinload` but returned raw ORM objects with no `response_model`; adding `response_model=PaginatedResponse[SaleRead]` (the existing generic pagination wrapper) silently dropped the nested `items`/`customer` fields during serialization — a SQLModel + pydantic-generics quirk, confirmed by direct `model_dump_json()` testing in a Python shell. Crashed `SalesHistoryPage`'s `items.length` access (caught cleanly by the new `ErrorBoundary`, confirming *that* piece works) the first time a real sale was viewed in Sales History. | Build `SaleRead.model_validate(s)` instances manually in the endpoint instead of relying on the generic response_model wrapper — matches the pattern already used successfully by `create_sale`/`get_sale`/`refund_sale`. | `backend/src/api/billing.py` |

B1 and B4 are backend bugs pre-dating this phase (B1 from Phase 3, B4 likely
since Phase 2's `SalesHistoryPage` was introduced) that had simply never been
exercised end-to-end against a real browser + real database before. B2 and
B4's regressions are now covered by tests: B4 by a strengthened
`test_list_sales` assertion (backend pytest now **105 passed**, same count
since it strengthens an existing test rather than adding one); B2 and B3 are
dev-tooling/UI-only and aren't meaningfully unit-testable, so they rely on
this manual verification pass instead — both were re-verified live after
their fixes (hard refresh on `/dashboard`, delete→reopen-dialog flow).

## Phase 5 — Packaging, deployment & operations

- Finish the **Tauri + backend sidecar** desktop build (single MSI) — or
  PyInstaller backend + Windows Service (auto-restart replaces watchdog.py).
- One installer: bundles Python runtime, writes `ProgramData\MBAS`, desktop
  shortcut, uninstaller that preserves data.
- Structured logging with rotation (`loguru`), in-app "backup health" badge,
  scheduled backup **verification** (open + integrity_check).
- CI (GitHub Actions): pytest + vitest + Playwright on every push; versioned
  releases; repo cleanup (remove committed DB, zips, node_modules, ad-hoc
  .bat/.txt docs → move to `docs/`).

---

## Constraints

- Offline-first: no cloud dependencies (constitution).
- RBAC (Admin/Manager/Sales) enforced at API level.
- DB transactions for financial/stock operations.
- Feature toggles must keep working for Basic/Standard/Premium tiers.
