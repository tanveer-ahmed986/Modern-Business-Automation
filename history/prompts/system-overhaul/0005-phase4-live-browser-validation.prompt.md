# PHR 0005 — Phase 4 live browser validation (found & fixed 4 real bugs)

- **ID:** 0005
- **Stage:** green
- **Feature:** system-overhaul
- **Date:** 2026-11-13
- **Author:** tanveer030402@gmail.com (via Claude Code)

## Prompt

> start the dev server and try the new UI in a browser

(Follow-up, after the Claude in Chrome extension needed a restart/toggle to connect: "I installed the extension and I'm logged in, try again" / "I restarted Chrome, try again" / "try the extension toggle and try again".)

## Context

Phase 4 (PHR 0004) had been validated via `tsc -b && vite build`, `vitest`,
and `pytest` only — no one had actually clicked through the new UI in a
browser against a real, file-backed database yet. The user asked for exactly
that.

## What happened

Started the backend (`uvicorn`) and frontend (`vite dev`) and drove the app
through Claude in Chrome: login → forced password change → dashboard →
inventory CRUD → POS sale → sales history → refund/CSV export. This surfaced
four real bugs that the automated test suite had never exercised, all fixed
live and re-verified in the browser:

1. **`backend/src/core/db.py`** — Phase 3's `_ensure_column(session, "users",
   ...)` used the wrong table name (`"users"` instead of SQLModel's actual
   `"user"`), crashing the backend on startup against a real database. Test
   fixtures never call `init_db()`, so this was invisible until now.
2. **`frontend/vite.config.ts`** — the dev proxy's path list overlaps with
   frontend SPA route names (`/dashboard`, `/billing`, etc.); a hard
   navigation/refresh on those pages was silently routed to the backend
   instead of Vite's own `index.html`, producing a blank page. Fixed with a
   `bypass` that lets `Accept: text/html` navigations fall through.
3. **`frontend/src/features/inventory/ProductList.tsx`** — opening a
   Dialog/AlertDialog synchronously from inside a `DropdownMenuItem` raced
   Radix's body `pointer-events` lock between the closing menu and the
   opening dialog, freezing the entire page after any delete/edit action.
   Fixed by deferring the state update with `setTimeout(..., 0)`.
4. **`backend/src/api/billing.py`** — `GET /billing/sales` eagerly loaded
   `items`/`customer` but, once given `response_model=PaginatedResponse[SaleRead]`
   (a plausible-looking fix I tried first), silently dropped those nested
   fields during serialization — a SQLModel + pydantic-generics quirk,
   confirmed by direct `model_dump_json()` testing in a Python shell. This
   crashed `SalesHistoryPage` the moment a real sale existed to display (the
   new `ErrorBoundary` caught it cleanly, which was itself a nice confirmation
   that piece works). Fixed by manually materializing `SaleRead.model_validate(s)`
   instances in the endpoint instead of relying on the generic wrapper.

Full bug table, root-cause detail, and fix rationale recorded in
`specs/system-overhaul/plan.md` under Phase 4's new "Live browser validation"
section.

## Response summary

- Backend: 105/105 pytest passing — same count as before, since the fix for
  bug #4 is covered by *strengthening* the existing `test_list_sales`
  assertion (it now checks the nested `items`/`customer` fields survive
  serialization) rather than adding a new test.
- Frontend: `tsc -b` clean after the fixes.
- Bugs #2 and #3 are dev-tooling/UI timing issues not meaningfully
  unit-testable; both were manually re-verified live in the browser after
  their fixes (hard refresh on `/dashboard`, delete→reopen-dialog flow, full
  POS sale with the cash-tendered calculator and `Ctrl+Enter` shortcut, CSV
  export, refund confirm/cancel toggle) and confirmed working.
- Test servers (backend on a temporary port 8010, to avoid a collision with
  an unrelated pre-existing process on 8000; frontend dev server) were
  stopped at the end of the session. `vite.config.ts`'s proxy target was
  reverted from the temporary `8010` back to `8000`.
