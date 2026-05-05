from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pathlib import Path
from src.api import auth, settings, inventory, billing, dashboard, suppliers, purchases, reports, system, ai, users
from src.core.db import init_db
from src.core.license import LicenseValidator, set_license_validator, LicenseValidationError
from src.core.scheduler import start_scheduler, stop_scheduler

# Resolve paths relative to this file's location (works regardless of CWD)
_SRC_DIR = Path(__file__).resolve().parent          # backend/src/
_BACKEND_DIR = _SRC_DIR.parent                      # backend/
_PROJECT_DIR = _BACKEND_DIR.parent                  # project root or MBAS_Package/
_FRONTEND_DIST = _PROJECT_DIR / "frontend" / "dist" # pre-built frontend

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Step 1: Validate license before database init
    # Search for license in multiple locations
    license_path = None
    for candidate in [
        _PROJECT_DIR / "mbas.license",
        _BACKEND_DIR / "mbas.license",
        Path("mbas.license"),
    ]:
        if candidate.exists():
            license_path = candidate
            break

    # Search for public key in multiple locations
    public_key_path = None
    for candidate in [
        _SRC_DIR / "embedded" / "public_key.pem",
        _BACKEND_DIR / "src" / "embedded" / "public_key.pem",
        Path("backend/src/embedded/public_key.pem"),
        Path("src/embedded/public_key.pem"),
    ]:
        if candidate.exists():
            public_key_path = candidate
            break

    try:
        if license_path and public_key_path:
            validator = LicenseValidator(str(license_path), str(public_key_path))
            license_data = validator.validate()
            set_license_validator(validator)

            print(f"License validated: {license_data.licensee} ({license_data.tier.upper()})")
            if license_data.expiry_date:
                print(f"License expires: {license_data.expiry_date.date()}")
            else:
                print("License: PERPETUAL")
        else:
            if not license_path:
                print("License file not found - starting in Basic mode")
            if not public_key_path:
                print("Public key not found - starting in Basic mode")
            validator = None

    except LicenseValidationError as e:
        print(f"\nLICENSE ERROR: {e}")
        print("The application will start in Basic mode with core features.")
        print("Contact your vendor for a valid license.\n")
        validator = None

    # Step 2: Initialize database tables on startup
    init_db()

    # Step 3: Load license features into settings
    if validator and validator.get_license_info():
        from src.core.db import engine
        from src.models.core import Settings
        from sqlmodel import Session

        with Session(engine) as session:
            db_settings = session.get(Settings, 1)
            if db_settings:
                # Update feature flags from license
                license_info = validator.get_license_info()
                db_settings.feature_flags = license_info.features.model_dump()
                session.add(db_settings)
                session.commit()
                print(f"Feature flags loaded from license: {sum(db_settings.feature_flags.values())} enabled")

    # Step 4: Start automatic backup scheduler
    start_scheduler()
    print("Automatic backup scheduler started")

    yield

    # Cleanup on shutdown
    stop_scheduler()
    print("Automatic backup scheduler stopped")

app = FastAPI(title="MBAS API", version="1.0.0", lifespan=lifespan)

# CORS configuration for Tauri (React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, Tauri runs from a custom protocol (tauri://)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(settings.router)
app.include_router(inventory.router)
app.include_router(billing.router)
app.include_router(dashboard.router)
app.include_router(suppliers.router)
app.include_router(purchases.router)
app.include_router(reports.router)
app.include_router(system.router)
app.include_router(ai.router)
app.include_router(users.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Serve pre-built frontend static files (for deployment without Node.js)
if _FRONTEND_DIST.exists() and (_FRONTEND_DIST / "index.html").exists():
    # Mount static assets (JS, CSS, images)
    app.mount("/assets", StaticFiles(directory=str(_FRONTEND_DIST / "assets")), name="static-assets")

    # Serve other static files at root level (favicon, etc.)
    @app.get("/vite.svg")
    async def vite_svg():
        return FileResponse(str(_FRONTEND_DIST / "vite.svg"))

    # SPA catch-all: serve index.html for all non-API routes
    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        # Don't intercept API routes
        if full_path.startswith(("auth/", "settings/", "inventory/", "billing/",
                                  "dashboard/", "suppliers/", "purchases/",
                                  "reports/", "system/", "ai/", "users/", "health")):
            return {"detail": "Not found"}
        # Serve static files if they exist
        file_path = _FRONTEND_DIST / full_path
        if full_path and file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        # Default: serve index.html for SPA routing
        return FileResponse(str(_FRONTEND_DIST / "index.html"))

    print(f"Serving frontend from {_FRONTEND_DIST}")
else:
    @app.get("/")
    async def root():
        return {"message": "MBAS Backend API is running. Frontend not found - use http://localhost:5173 if running frontend dev server."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
