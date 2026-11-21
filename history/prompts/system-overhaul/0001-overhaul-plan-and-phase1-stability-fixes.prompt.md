---
id: 0001
title: overhaul-plan-and-phase1-stability-fixes
stage: plan
date: 2026-11-11
surface: claude-code-cli
model: claude-fable-5
feature: system-overhaul
branch: master
user: tanveer030402@gmail.com
command: (free-form prompt)
labels: [performance, pwa, sqlite, ui-overhaul, plan]
links:
  spec: specs/system-overhaul/plan.md
  ticket: n/a
  adr: n/a
  pr: n/a
files:
  - frontend/vite.config.ts
  - frontend/src/config.ts
  - frontend/src/main.tsx
  - frontend/src/services/reports.service.ts
  - frontend/src/features/reports/ReportsPage.tsx
  - backend/src/main.py
  - backend/src/core/db.py
  - backend/src/core/backup.py
tests:
  - frontend: npm run build (tsc + vite + SW regeneration)
  - backend: pytest suite
---

## Prompt

yes, implement phase 1 fixes but first make plan for all phases which also
include improvement in UI of the system, make it a professional look

## Response snapshot

Created master plan `specs/system-overhaul/plan.md` covering 5 phases:
Phase 1 stability (hang fixes — implemented in this session), Phase 2 data
correctness, Phase 3 security/licensing, Phase 4 professional UI overhaul
(design system, app shell, DataTable, POS flow, dashboard charts, print
invoices), Phase 5 packaging/CI/ops. Implemented Phase 1: fixed service
worker API caching, purged stale SW caches, relative API base + dev proxy,
tightened CORS, resized SQLite pool (5+5, busy_timeout 5000), removed global
write-lock middleware, backup via dedicated connection, CSV export via
authenticated blob download.

## Outcome

- ✅ Impact: tab-switch hang root causes removed; LAN/mobile PWA unblocked
- 🧪 Tests: frontend build + backend pytest run as validation
- 📁 Files: see files list above
- 🔁 Next prompts: implement Phase 2 (pagination UI, invoice sequence, stock ledger)
- 🧠 Reflection: hang was SW cache + pool starvation + CORS preflights, not "full DB loads"

## Evaluation notes (flywheel)

- Failure modes observed: dead `/api/*` SW rule; catch-all 30-day API cache; pool_timeout 500s; token-in-URL export
- Graders run and results (PASS/FAIL): build/test results recorded in session
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): measure tab-switch latency before/after on client hardware
