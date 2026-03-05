# Tasks: Modern Business Automation System (MBAS)

**Feature**: MBAS Master Plan  
**Status**: Ready for Implementation  
**Strategy**: Phase-based delivery starting with project scaffolding, followed by foundational RBAC and Settings, then core business modules (Inventory, Billing) ending with Premium AI features.

## Phase 1: Setup (Project Scaffolding)
*Goal: Initialize the monorepo structure with Tauri, FastAPI, and React.*

- [X] T001 Initialize backend FastAPI project in `backend/` with `main.py`
- [X] T002 Configure Python virtual environment and `requirements.txt` in `backend/`
- [X] T003 [P] Initialize frontend React/Vite project in `frontend/`
- [X] T004 [P] Install Tailwind CSS and Shadcn/ui in `frontend/`
- [X] T005 [P] Initialize Tauri project in `tauri-app/` pointing to `frontend/dist`
- [X] T006 [P] Configure Tauri `tauri.conf.json` for sidecar execution of Python backend
- [X] T007 Create shared configuration file for API base URL in `frontend/src/config.ts`

## Phase 2: Foundational (Database & Auth Infrastructure)
*Goal: Establish the core database schema, authentication logic, and feature toggle system.*

- [X] T008 [P] Implement SQLModel base and engine configuration in `backend/src/core/db.py`
- [X] T009 [P] Define `User` and `Settings` models in `backend/src/models/core.py`
- [X] T010 [P] Implement BCrypt password hashing utility in `backend/src/core/security.py`
- [X] T011 [P] Implement JWT token generation and validation in `backend/src/core/auth.py`
- [X] T012 Implement feature toggle middleware/dependency in `backend/src/core/features.py`
- [X] T013 Create database initialization script (bootstrap admin) in `backend/src/scripts/init_db.py`

## Phase 3: User Story 1 - Authentication & RBAC (P1)
*Story Goal: Secure login for Admin, Manager, and Sales User with role-based UI.*

- [X] T014 [US1] Implement `/auth/login` endpoint in `backend/src/api/auth.py`
- [X] T015 [US1] Create Auth service for state management in `frontend/src/services/auth.service.ts`
- [X] T016 [US1] Design Login page in `frontend/src/features/auth/LoginPage.tsx`
- [X] T017 [US1] Implement Role-based route guards in `frontend/src/components/routing/ProtectedRoute.tsx`
- [X] T018 [US1] Create sidebar navigation with role-based visibility in `frontend/src/components/layout/Sidebar.tsx`

## Phase 4: User Story 2 - System Settings & Rebranding (P1)
*Story Goal: Allow businesses to configure identity and manage package feature toggles.*

- [X] T019 [US2] Implement GET/PUT `/settings` endpoints in `backend/src/api/settings.py`
- [X] T020 [US2] Create Settings service in `frontend/src/services/settings.service.ts`
- [X] T021 [US2] Design Settings UI for branding (Name, Logo, Tax) in `frontend/src/features/settings/SettingsPage.tsx`
- [X] T022 [US2] Implement dynamic branding hook (useBranding) in `frontend/src/hooks/useBranding.ts`

## Phase 5: User Story 3 - Inventory & Stock Management (P1)
*Story Goal: Manage products, categories, and track stock levels with FTS5 search.*

- [X] T023 [US3] Define `Category` and `Product` models in `backend/src/models/inventory.py`
- [X] T024 [US3] Implement FTS5 virtual table trigger logic in `backend/src/core/db.py`
- [X] T025 [US3] Implement CRUD endpoints for `/inventory/products` in `backend/src/api/inventory.py`
- [X] T026 [US3] Create Inventory service in `frontend/src/services/inventory.service.ts`
- [X] T027 [US3] Design Product Management table with TanStack Table in `frontend/src/features/inventory/ProductList.tsx`
- [X] T028 [US3] Design "Add/Edit Product" modal in `frontend/src/features/inventory/ProductForm.tsx`

## Phase 6: User Story 4 - Billing & Invoicing (P1)
*Story Goal: Process sales, generate invoices, and auto-deduct stock in atomic transactions.*

- [X] T029 [US4] Define `Customer`, `Sale`, and `SaleItem` models in `backend/src/models/sales.py`
- [X] T030 [US4] Implement atomic Sale service with stock deduction in `backend/src/services/sale_service.py`
- [X] T031 [US4] Implement `/billing/invoices` POST endpoint in `backend/src/api/billing.py`
- [X] T032 [US4] Design POS-style billing interface in `frontend/src/features/billing/BillingPage.tsx`
- [X] T033 [US4] Implement real-time subtotal/tax/discount calculator in `frontend/src/features/billing/useCalculator.ts`
- [X] T034 [US4] Create printable invoice template using Tailwind Print classes in `frontend/src/features/billing/InvoiceTemplate.tsx`

## Phase 7: User Story 5 - Dashboard & Metrics (P1)
*Story Goal: Visual overview of business health based on user role.*

- [X] T035 [US5] Implement `/dashboard/metrics` logic with aggregation in `backend/src/api/dashboard.py`
- [X] T036 [US5] Create Dashboard service in `frontend/src/services/dashboard.service.ts`
- [X] T037 [US5] Design card-based metric layout in `frontend/src/features/dashboard/DashboardPage.tsx`
- [X] T038 [US5] Implement "Low Stock" alert widget in `frontend/src/features/dashboard/LowStockWidget.tsx`

## Phase 8: User Story 6 - Supplier & Purchase (P2 - Standard/Premium)
*Story Goal: Manage supplier balances and track purchase invoices.*

- [X] T039 [US6] Define `Supplier`, `Purchase`, and `PurchaseItem` models in `backend/src/models/purchases.py`
- [X] T040 [US6] Implement Purchase service with stock addition in `backend/src/services/purchase_service.py`
- [X] T041 [US6] Implement `/suppliers` CRUD endpoints in `backend/src/api/suppliers.py`
- [X] T042 [US6] Design Purchase entry form in `frontend/src/features/purchases/PurchasePage.tsx`
- [X] T043 [US6] Design Supplier ledger view in `frontend/src/features/suppliers/SupplierLedger.tsx`

## Phase 9: User Story 7 - Reports Module (P2)
*Story Goal: Exportable sales and financial reports with tiered depth.*

- [X] T044 [US7] Implement `/reports/sales` with date filtering in `backend/src/api/reports.py`
- [X] T045 [US7] Implement Profit & Loss report logic (Premium only) in `backend/src/services/report_service.py`
- [X] T046 [US7] Create CSV/PDF export utility in `backend/src/core/export.py`
- [X] T047 [US7] Design Reports dashboard in `frontend/src/features/reports/ReportsPage.tsx`

## Phase 10: User Story 8 - Backup & Restore (P2 - Standard/Premium)
*Story Goal: Ensure data safety via offline SQLite file exports.*

- [X] T048 [US8] Implement backup utility (SQLite vacuum into file) in `backend/src/core/backup.py`
- [X] T049 [US8] Implement `/system/backup` and `/system/restore` endpoints in `backend/src/api/system.py`
- [X] T050 [US8] Design Backup management UI in `frontend/src/features/settings/BackupSection.tsx`

## Phase 11: User Story 9 - AI Assistant (P3 - Premium)
*Story Goal: Local sales forecasting and natural language SQL queries.*

- [X] T051 [US9] Set up `scikit-learn` forecasting pipeline in `backend/src/ai/forecasting.py`
- [X] T052 [US9] Integrate `llama-cpp-python` with Phi-3 GGUF model in `backend/src/ai/llm.py`
- [X] T053 [US9] Implement `/ai/predict` and `/ai/query` endpoints in `backend/src/api/ai.py`
- [X] T054 [US9] Design AI Chat sidebar in `frontend/src/features/ai/AIChatPanel.tsx`

## Phase 12: Polish & Packaging
*Goal: Final aesthetics, optimizations, and professional installer generation.*

- [X] T055 Implement "Command Palette" (Ctrl+K) for global search in `frontend/src/components/layout/CommandPalette.tsx`
- [X] T056 Apply "Quiet UI" glassmorphism styles in `frontend/src/index.css`
- [X] T057 Configure Nuitka build script for backend in `backend/scripts/build.py`
- [X] T058 Run full E2E test suite in `tauri-app/tests/`
- [X] T059 Generate professional MSI installer using `npm run tauri build`

## Dependencies & Parallel Execution

### Dependency Graph
1. **Setup (Phase 1)** -> **Foundational (Phase 2)**
2. **Foundational** -> **Auth (US1)** & **Settings (US2)**
3. **Auth (US1)** -> All other User Stories
4. **Inventory (US3)** -> **Billing (US4)** & **Purchase (US6)**
5. **Billing (US4)** & **Purchase (US6)** -> **Dashboard (US5)** & **Reports (US7)**
6. **Reports (US7)** -> **AI Assistant (US9)**

### Parallel Opportunities
- T003, T004, T005 can be done in parallel once structure is set.
- T019, T020 (Settings) can be done in parallel with T014, T015 (Auth).
- Frontend UI development (T027, T028) can run in parallel with Backend API development (T025).
- AI research/setup (T051, T052) can run in parallel with Phase 8/9/10.

## Implementation Strategy
- **MVP Range**: Phase 1 to Phase 7 (Auth, Settings, Inventory, Billing, Dashboard). This provides a fully functional Basic/Standard system.
- **Incremental Delivery**: Each User Story phase results in a functional UI module that can be tested independently.
- **Toggles**: Implement `feature_flags` early in Phase 2 to ensure modules can be hidden/shown correctly during development.
