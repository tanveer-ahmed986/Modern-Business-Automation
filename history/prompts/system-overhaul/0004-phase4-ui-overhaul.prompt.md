# PHR 0004 — Phase 4: Professional UI overhaul

- **ID:** 0004
- **Stage:** green
- **Feature:** system-overhaul
- **Date:** 2026-11-13
- **Author:** tanveer030402@gmail.com (via Claude Code)

## Prompt

> start phase 4

## Context

Phase 1 (stability), Phase 2 (data correctness), and Phase 3 (security &
licensing hardening) complete and validated. Phase 4 per
`specs/system-overhaul/plan.md`: professional UI overhaul (design system,
app shell, shared DataTable, forms, POS, dashboard charts, invoices, quality
bar).

Audit before implementing found the frontend already had a decent shadcn +
Tailwind foundation (cmdk command palette, TanStack Table/Query, an existing
A4 + 80mm thermal invoice template with print stylesheet, a keyboard-first
POS search flow) that the original scope didn't account for — `next-themes`
and `cmdk` were installed but never wired up, and there was no shared
DataTable, no AlertDialog, no RHF/zod, no charts, and no real app shell
(topbar/breadcrumbs/user menu). Scope was adjusted accordingly: finish the
wiring and build what was genuinely missing, rather than rebuild what
already existed.

## Scope executed

1. Wired up `next-themes` (`ThemeProvider` + `ThemeToggle`) — previously an
   unused dependency.
2. App shell: collapsible, theme-aware `Sidebar`; new `TopBar` (breadcrumb,
   command-palette trigger, theme toggle, user avatar dropdown with Change
   Password / Sign Out); `Layout` dropped the decorative glassmorphism blobs
   and now wraps routed content in a new `ErrorBoundary`.
3. Shared `DataTable` component (TanStack Table: server pagination,
   page-size selector, skeleton loading rows, empty state, optional CSV
   export) — refactored `ProductList` and `SalesHistoryPage` onto it.
4. Forms: `ProductForm` rewritten on `react-hook-form` + `zod` (fixed a
   corrupted `max-探索-md` class along the way); new `AlertDialog` component
   replaces the two remaining `window.confirm()` call sites (delete product,
   delete user).
5. POS: cash-tendered input + live change-due calculator for cash sales
   (blocks checkout if insufficient); `Ctrl/Cmd+Enter` completes the sale.
6. Dashboard charts: new backend `GET /dashboard/trends` (30-day zero-filled
   revenue series + payment-method breakdown, one query, business-local day
   bucketing via the existing `local_date_key` helper, same cache pattern as
   `/metrics`); `recharts`-based area + donut charts on the frontend, themed
   to the CSS variable design tokens.
7. Fixed a duplicated footer bug in the A4 invoice template.
8. Explicitly scoped out (documented in `plan.md`): per-page visual polish
   of Reports/Settings, column sorting/density toggle/park-resume-sale, new
   Playwright specs (an existing e2e spec already covers the flow), and a
   dedicated WCAG contrast audit tool — the existing shadcn tokens are
   AA-contrast by default.

## Response summary

Implementation + validation recorded in `specs/system-overhaul/plan.md`
(Phase 4 section, now marked COMPLETE), including the scoping-decisions
list above.

Final results:
- Backend: 105/105 pytest passing (0 failures), up from 104 at the end of
  Phase 3. 1 new test for `/dashboard/trends`; added a cache reset for the
  new `_trends_cache` global in `conftest.py`.
- Frontend: `tsc -b && vite build` passes after fixing new-code TS errors
  (unused import, `recharts` Tooltip formatter generics, the
  `react-hook-form` + `zod` `z.coerce` input/output split needing
  `useForm<Input, any, Output>`). `npx vitest run` 10/10 (unchanged).
- No backend schema changes this phase, so no migration concerns; Alembic
  adoption remains deferred to Phase 5 per prior phases' rationale.
