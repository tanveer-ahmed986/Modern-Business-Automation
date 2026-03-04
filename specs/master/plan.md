# Implementation Plan: Modern Business Automation System (MBAS)

**Branch**: `master` | **Date**: 2026-03-04 | **Spec**: [specs/spec.md](specs/spec.md)
**Input**: Feature specification from `specs/spec.md`

## Summary

The MBAS is a fully offline Windows desktop system designed for small and medium businesses. It will use a **Tauri + FastAPI + React** architecture, packaged as a single executable for ease of deployment. The UI will focus on high information density with a "highly professional" aesthetic (minimalism, command palettes, virtualization).

## Technical Context

**Language/Version**: Python 3.12 (Backend), React 18+ / Vite (Frontend)
**Primary Dependencies**: FastAPI (Backend API), SQLModel (ORM), Pydantic v2 (Validation), Tauri (Desktop Wrapper), Nuitka (Compilation), scikit-learn (AI Predictions), llama-cpp-python (Local LLM), Shadcn/ui (UI Components).
**Storage**: SQLite (Index-optimized, WAL mode enabled).
**Testing**: pytest (Backend), Vitest + Playwright (Frontend).
**Target Platform**: Windows 10/11 (Offline).
**Project Type**: Desktop Application (Monolith with Sidecar).
**Performance Goals**: Load time < 3s, sub-100ms interaction latency, handle 100k+ records.
**Constraints**: 100% offline, low memory footprint, no external API dependencies.
**Scale/Scope**: ~12 Core Modules, 12-15 Tables, 3 Role levels, 3 Package tiers.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Offline-First**: All dependencies and AI models are local.
- [x] **Modular Feature Toggles**: `feature_flags` in `Settings` table will gate UI and Backend logic.
- [x] **Financial Integrity**: Atomic database transactions planned for all sales and purchases.
- [x] **RBAC**: Enforced via FastAPI dependencies and UI route guards.
- [x] **Rebrandability**: Dynamic loading of identity from `Settings` table.

## Project Structure

### Documentation (this feature)

```text
specs/master/
├── plan.md              # This file
├── research.md          # Packaging, UI trends, AI strategy
├── data-model.md        # SQLModel table definitions
├── quickstart.md        # Setup and run instructions
├── contracts/           
│   └── openapi.yaml     # API Endpoints
└── tasks.md             # To be created by /sp.tasks
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/             # FastAPI routers
│   ├── core/            # Auth, Config, Security
│   ├── models/          # SQLModel classes
│   ├── services/        # Business logic, Stock updates
│   ├── ai/              # scikit-learn & llama-cpp integration
│   └── main.py          # Entry point
└── tests/

frontend/
├── src/
│   ├── components/      # UI components (Shadcn)
│   ├── features/        # Billing, Inventory, Reports
│   ├── hooks/           # Data fetching, Auth
│   ├── services/        # API client
│   └── main.tsx         # Entry point
└── tests/

tauri-app/
├── src-tauri/           # Rust core and packaging logic
└── [tauri config files]
```

**Structure Decision**: Option 2 (Web application structure with backend/frontend) inside a Tauri desktop wrapper.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Tauri + Nuitka | Professional offline distribution | Direct PyInstaller build is less robust and has larger footprint |
| Local LLM (Phi-3) | Natural query capability | Rule-based NLP is too rigid for dynamic data questions |
