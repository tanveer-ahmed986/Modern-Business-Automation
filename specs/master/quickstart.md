# Quickstart: Modern Business Automation System (MBAS)

## Development Environment Setup

1. **Backend (Python 3.12)**:
   - Create virtual env: `python -m venv venv`
   - Activate: `.\venv\Scripts\activate` (Windows)
   - Install dependencies: `pip install fastapi sqlmodel uvicorn pydantic-settings scikit-learn llama-cpp-python bcrypt pyjwt`
2. **Frontend (React/Vite)**:
   - `cd frontend`
   - `npm install`
   - `npm install tailwindcss lucide-react shadcn-ui` (Follow shadcn/ui setup)
3. **Desktop (Tauri)**:
   - Install Rust: [rustup.rs](https://rustup.rs/)
   - `cd tauri-app`
   - `npm install @tauri-apps/api @tauri-apps/cli`

## Initial Run (Dev Mode)

1. **Start Backend**: 
   - `uvicorn main:app --reload --port 8000`
2. **Start Frontend**:
   - `npm run dev` (in frontend dir)
3. **Launch Tauri Window**:
   - `npx tauri dev` (in tauri-app dir)

## Packaging for Release

1. **Build React App**: `npm run build` (outputs to `dist/`)
2. **Compile Python Backend**:
   - `python -m nuitka --standalone --onefile --include-data-dir=dist=dist --windows-disable-console main.py`
3. **Bundle as Tauri Sidecar**:
   - Move the compiled `.exe` to `src-tauri/binaries/`
   - Run `npx tauri build` to generate the final `.msi` or `.exe` installer.

## Database Initialization
- The app will automatically create `mbas.db` (SQLite) on first run using SQLModel's `create_all()`.
- Initial Admin user will be created via a bootstrap script.
