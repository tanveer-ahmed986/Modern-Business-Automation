# Modern Business Automation System (MBAS)

**MBAS v2.0.2** is a 100% offline, professional-grade Windows desktop application designed to empower small and medium businesses with high-performance inventory management, billing, and AI-driven insights.

Built for **2026** with a focus on speed, data privacy, and a modern "Quiet UI" aesthetic.

---

## 🚀 Key Features

- **100% Offline-First**: Zero external API dependencies. Your data stays on your machine. Fully offline installer with bundled Python wheels.
- **Role-Based Access Control (RBAC)**: Secure access for Admin, Manager, and Sales User roles.
- **High-Performance Billing**: POS-style interface with real-time tax/discount calculation and atomic stock updates.
- **Inventory & FTS5 Search**: Sub-millisecond global search across 100k+ products using SQLite's Full-Text Search.
- **Supplier & Purchase Management**: Track supplier balances, manage ledger history, and record purchases with automatic stock updates.
- **Modular Tiering**: Built-in feature gating for Basic, Standard, and Premium packages.
- **Local AI (Premium)**: Sales forecasting (scikit-learn) and natural language data queries (Local LLM/Phi-3) powered by your own CPU.
- **Professional Packaging**: Professional Inno Setup installer with offline installation support and automatic startup configuration.

## 📊 Project Status (Phase-Based Progress)

- [X] **Phase 1-2**: Project Scaffolding & Database Infrastructure.
- [X] **Phase 3**: Authentication & Role-Based Access Control (RBAC).
- [X] **Phase 4**: System Settings & Dynamic Rebranding.
- [X] **Phase 5**: Inventory & Stock Management (FTS5 Search).
- [X] **Phase 6**: Billing & Invoicing (Atomic Transactions).
- [X] **Phase 7**: Dashboard & Business Metrics.
- [X] **Phase 8**: Supplier & Purchase Module (Ledgers & Stock-In).
- [X] **Phase 9-12**: Reports, Backup/Restore, AI Assistant, and Professional Packaging.

## 🎯 What's New in v2.0.2

### Critical Fixes & Improvements
- ✅ **Offline Installer**: Bundled all Python dependencies as wheels for 100% offline installation
- ✅ **Batch Script Fixes**: Resolved installer hang issues caused by `pause` commands in background scripts
- ✅ **Database Path Handling**: Fixed SQLite database write issues with proper working directory management
- ✅ **Installer Optimization**: Improved file exclusion patterns (*.db, *.log, backups, config\secret.key)
- ✅ **Startup Automation**: Enhanced auto-start scripts with recovery mechanisms
- ✅ **Currency Synchronization**: Fixed currency display issues across Dashboard, Suppliers, and Purchases
- ✅ **Settings Integration**: Resolved billing settings and backup configuration issues

### Deployment Package
- Professional Inno Setup 6 installer (`MBAS_Installer_Professional_ZT.iss`)
- Complete client package ready for distribution (`MBAS_v2.0_CLIENT_PACKAGE/`)
- Comprehensive installation and troubleshooting guides
- Automated build and deployment scripts

## 🛠️ Tech Stack

- **Frontend**: [React 18+](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/) + [Vite](https://vitejs.dev/)
- **Styling**: [Tailwind CSS v3](https://tailwindcss.com/) + [Shadcn/ui](https://ui.shadcn.com/)
- **Desktop Wrapper**: [Tauri v2](https://tauri.app/) (Rust core)
- **Backend (Sidecar)**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12, Compiled with [Nuitka](https://nuitka.net/))
- **Database**: [SQLite](https://www.sqlite.org/) (WAL mode enabled, SQLModel ORM)
- **AI**: [scikit-learn](https://scikit-learn.org/) & [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)

## 📁 Project Structure

```text
├── backend/            # FastAPI source, AI services, and models
├── frontend/           # React/Vite dashboard source
├── tauri-app/          # Rust core, desktop config, and sidecar binaries
├── specs/              # Architectural plans, data models, and API contracts
└── history/            # Prompt history and architectural decision records (ADR)
```

## 🏁 Quickstart (Development)

### Prerequisites
- [Node.js](https://nodejs.org/) (v24+)
- [Python](https://www.python.org/) (3.12+)
- [Rust](https://www.rust-lang.org/) (1.77.2+)

### Installation

1. **Install Backend Dependencies**:
   ```powershell
   cd backend
   pip install -r requirements.txt
   ```

2. **Install Frontend Dependencies**:
   ```powershell
   cd frontend
   npm install
   ```

3. **Install Tauri CLI**:
   ```powershell
   npm install -D @tauri-apps/cli
   ```

### Running the App

1. **Start Backend (Manual)**:
   ```powershell
   cd backend/src
   python main.py
   ```

2. **Start Desktop Wrapper**:
   ```powershell
   # This will automatically start the React dev server
   npx tauri dev
   ```

## 📦 Production Build

The production build compiles the Python backend into a high-performance C executable (sidecar) and packages the entire app into a professional Windows installer.

```powershell
npm run tauri build
```

## ⚖️ License

All rights reserved. Professional Use License.

---
*Built with ❤️ for Modern Businesses.*
