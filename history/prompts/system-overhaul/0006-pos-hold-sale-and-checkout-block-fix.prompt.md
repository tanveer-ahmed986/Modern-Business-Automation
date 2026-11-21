# PHR 0006 — POS: fix Complete Sale blocking bug, add Hold/Resume Sale

- **ID:** 0006
- **Stage:** green
- **Feature:** system-overhaul
- **Date:** 2026-11-21
- **Author:** tanveer030402@gmail.com (via Claude Code)

## Prompt

> in billing page, when i enter items, complete sale button is blocked, sales
> didn't complete,also hold sale(if someone forget some items to purchase
> then pause sale for a while so that he can add items into his cart) and
> start new sale option is not available

## Context

"Park sale / resume sale" was explicitly scoped out of Phase 4 (see PHR 0004,
plan.md). The "Complete Sale blocked" report was a separate, real bug in the
same page.

## Root cause (checkout block)

`BillingPage.tsx`'s `cashInsufficient` guard disabled "Complete Sale" whenever
`paymentMethod === "cash"` (the default) and the typed cash-tendered amount
was less than the total — but `cashTendered` starts as an **empty string**,
so `tenderedAmount` parsed to `0`, making the button permanently disabled the
moment any item was added, unless the cashier proactively typed an exact/over
amount into "Cash Received" (a field most cashiers would treat as optional,
since its only visible purpose is the change-due calculator).

## Fixes

1. **`frontend/src/features/billing/BillingPage.tsx`** — `cashInsufficient`
   now also requires `cashTendered !== ""`, so an empty field never blocks
   checkout; it only blocks when the cashier has typed an amount that's
   actually short of the total.
2. **Hold Sale / Held Sales** — new feature:
   - `useCalculator.ts` gained `loadCart(items, discount)` to bulk-restore
     cart state (vs. `addItem`'s merge-by-id semantics).
   - `BillingPage.tsx` added a `HeldSale[]` list persisted to
     `localStorage` (`mbas_held_sales`), so held sales survive a page
     refresh/navigation.
   - "Hold Sale" button (cart header) snapshots the current cart, discount,
     customer, and payment method into the held list and clears the active
     sale for a new customer.
   - "Held Sales" button (with a count badge) opens a `Dialog` listing
     parked sales (customer, item count, subtotal, held time) with
     Resume/Delete actions. Resume is blocked with a toast if the active
     cart isn't empty, to avoid silently clobbering in-progress work.

## Validation

- `npx tsc -b` clean.
- Live browser test (existing authenticated dev session): added "Soda Can"
  to cart → Complete Sale button rendered enabled immediately (previously
  would have stayed disabled) → held the sale (toast confirmed, cart
  cleared, Held Sales badge → 1) → reopened Held Sales dialog, confirmed
  entry (Walk-in, 1 item, PKR 150.00) → Resume → item restored to cart →
  Complete Sale → "Sale Completed! Invoice #2" rendered correctly end-to-end.
