# Modern Business Automation System (MBAS)

**MBAS** is a 100% offline, professional-grade Windows desktop application designed to empower small and medium businesses with high-performance inventory management, billing, and AI-driven insights.

Built for **2026** with a focus on speed, data privacy, and a modern "Quiet UI" aesthetic.

---

## 🚀 Key Features

- **100% Offline-First**: Zero external API dependencies. Your data stays on your machine.
- **Role-Based Access Control (RBAC)**: Secure access for Admin, Manager, and Sales User roles.
- **High-Performance Billing**: POS-style interface with real-time tax/discount calculation and atomic stock updates.
- **Inventory & FTS5 Search**: Sub-millisecond global search across 100k+ products using SQLite's Full-Text Search.
- **Modular Tiering**: Built-in feature gating for Basic, Standard, and Premium packages.
- **Local AI (Premium)**: Sales forecasting (scikit-learn) and natural language data queries (Local LLM/Phi-3) powered by your own CPU.
- **Professional Packaging**: Single-binary Windows installer (.msi) with high security (Nuitka-compiled sidecars).

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
