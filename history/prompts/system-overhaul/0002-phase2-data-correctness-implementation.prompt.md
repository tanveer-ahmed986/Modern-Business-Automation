# PHR 0002 — Phase 2: Data correctness implementation

- **ID:** 0002
- **Stage:** green
- **Feature:** system-overhaul
- **Date:** 2026-11-12
- **Author:** tanveer030402@gmail.com (via Claude Code)

## Prompt

> start phase 2

## Context

Phase 1 (stability) complete and validated. Phase 2 per
`specs/system-overhaul/plan.md`: data correctness for inventory/invoicing.

## Scope executed

1. Transactional invoice sequence table (`invoice_sequences`) replacing
   count(*)-based generation; UNIQUE constraint on invoice_number retained as
   safety net.
2. Timezone-correct reporting: new `src/core/timeutils.py`; dashboard
   "today" and report date ranges computed over business-local days converted
   to UTC bounds (storage stays naive-UTC).
3. Decimal-safe money: all sale monetary computations quantized to 2 dp
   (ROUND_HALF_UP) in SaleService.
4. Soft-delete products: DELETE deactivates when referenced by sales or
   purchases; hard delete only when unreferenced.
5. Stock movement ledger (`stock_movements`): entries written on sale,
   refund, purchase receipt, manual adjustment, and initial stock.
6. Returns flow: `POST /billing/sales/{id}/refund` (Admin/Manager) restores
   stock, writes ledger entries, sets status REFUNDED.
7. Frontend: ProductList real server-side pagination; TanStack Query
   provider + migration of products/categories/dashboard queries.
8. Test suite: new tests for the above; repair of pre-existing stale tests.

## Response summary

Implementation + validation recorded in `specs/system-overhaul/plan.md`
(Phase 2 section, now marked COMPLETE). Schema changes limited to two NEW
tables (`stock_movements`, `invoice_sequences`) so existing customer
databases upgrade automatically via `create_all` (no ALTERs needed this
phase) — Alembic adoption itself is explicitly deferred to Phase 5, with
rationale recorded in the plan.

Final results:
- Backend: 92/92 pytest passing (0 failures), up from 51 passed/25
  documented-pre-existing-failed at end of Phase 1. All 25 stale failures
  repaired; 16 new Phase 2 tests added.
- Frontend: `npm run build` passes; `npx vitest run` 10/10 passing (after
  repairing a second stale nested esbuild binary under vitest's own
  node_modules, same class of issue as the Phase 1 build-time esbuild fix).
- In-memory smoke test confirmed invoice sequence allocation, Decimal
  rounding (HALF_UP to 2dp), stock ledger entries, and refund stock
  restoration all behave correctly end-to-end.
