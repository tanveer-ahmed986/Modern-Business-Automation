# Research: Modern Business Automation System (MBAS)

## Desktop Packaging Strategy

**Decision**: **Tauri + Nuitka (Sidecar Pattern)**.
- **Rationale**: 
    - **Performance/Size**: Tauri uses the system's native WebView2 (Edge), resulting in extremely small binary sizes (~10MB) compared to Electron (~150MB+).
    - **Professionalism**: Provides a native Windows experience with professional installers (.msi/.exe).
    - **Security**: Rust core provides a safe bridge between the UI and the Python backend.
    - **Backend Packaging**: Nuitka compiles the FastAPI backend to C, improving performance and obfuscating source code compared to PyInstaller.
- **Alternatives Considered**: 
    - **Electron**: Rejected due to high RAM/disk bloat.
    - **PyWebView**: Considered for simplicity, but Tauri provides better window management and a more robust ecosystem for "impressive" UIs.

## Frontend UI/UX Architecture

**Decision**: **React 18+ with Vite, Tailwind CSS, and Shadcn/ui**.
- **Rationale**: 
    - **Visual Impact**: Tailwind and Shadcn/ui enable rapid development of "highly professional and impressive" dashboards with modern aesthetics (Exaggerated Minimalism, Glassmorphism).
    - **Interactivity**: React's component-based architecture is ideal for complex, real-time data-heavy dashboards.
    - **Performance**: Vite provides near-instant HMR during development and optimized production builds.
    - **Data Handling**: Libraries like `TanStack Table` (React Table) with virtualization will handle 100k+ records smoothly.
- **UI Trends to Implement**:
    - **Command Palette (Ctrl+K)**: Search-first navigation for power users.
    - **Virtualized Lists/Tables**: Ensuring 60fps scrolling on large datasets.
    - **Role-Based Views**: Dynamic UI rendering based on the active feature toggles (Basic, Standard, Premium).

## Offline AI & Analytics

**Decision**: **Hybrid AI Approach (scikit-learn + llama-cpp-python)**.
- **Rationale**: 
    - **Tabular Predictions**: For sales forecasting and inventory optimization, specialized ML models (Random Forest / ARIMA via `scikit-learn`/`statsmodels`) are significantly more accurate and efficient than LLMs.
    - **Natural Query Assistant**: For the optional natural query feature, a small, quantized LLM (**Phi-3 Mini GGUF**) via `llama-cpp-python` will be used. It is capable of translating natural language to SQL queries locally.
    - **Efficiency**: Phi-3 Mini (quantized) runs comfortably on modern consumer CPUs without needing a high-end GPU.
- **Data Privacy**: 100% offline ensure no business data ever leaves the machine.

## Database Optimization

**Decision**: **SQLite with WAL Mode and FTS5**.
- **Rationale**: 
    - **Speed**: `PRAGMA journal_mode=WAL;` and `PRAGMA synchronous=NORMAL;` ensure high write throughput.
    - **Scalability**: Proper indexing on all Foreign Keys and filtered columns will easily handle 100k+ records with sub-millisecond query times.
    - **Search**: `FTS5` (Full-Text Search) will be used for instantaneous global searching across products, invoices, and customers.
    - **Reliability**: SQLite is battle-tested for embedded and desktop applications.

## Conclusion

The combination of a high-performance Rust-based wrapper (Tauri), a compiled Python backend (Nuitka), and a modern React frontend provides the best balance of user experience, performance, and developer productivity for a professional 2026 business automation system.
