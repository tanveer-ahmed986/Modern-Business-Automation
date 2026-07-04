from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from contextlib import asynccontextmanager
from pathlib import Path
from datetime import datetime
import asyncio
from src.api import auth, settings, inventory, billing, dashboard, suppliers, purchases, reports, system, ai, users, version
from src.core.db import init_db, cleanup_connections
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
    # Check if license validation should be skipped (for beta testing)
    import os
    skip_license = os.environ.get("MBAS_SKIP_LICENSE", "0") == "1"

    if skip_license:
        print("License validation skipped (Beta/Testing mode)")
        print("Running with STANDARD tier features")
        validator = None
    else:
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

    # Step 2b: Ensure default admin user and settings exist
    # (INSTALL_MBAS.bat bootstrap may have failed silently during install)
    try:
        from src.core.db import engine
        from src.models.core import User, UserRole, Settings
        from src.core.security import get_password_hash
        from src.models.license import get_tier_features
        from sqlmodel import Session, select

        with Session(engine) as session:
            # Ensure Settings exist
            db_settings = session.get(Settings, 1)
            if not db_settings:
                print("Creating default system settings...")
                db_settings = Settings(
                    id=1,
                    business_name="MBAS Demo Store",
                    tax_rate=0.0,
                    feature_flags=get_tier_features("basic").model_dump()
                )
                session.add(db_settings)

            # Ensure admin user exists
            admin = session.exec(
                select(User).where(User.username == "admin")
            ).first()
            if not admin:
                print("Creating default administrator account...")
                admin = User(
                    username="admin",
                    full_name="System Administrator",
                    role=UserRole.ADMIN,
                    hashed_password=get_password_hash("admin123")
                )
                session.add(admin)

            session.commit()
    except Exception as e:
        print(f"Warning: Failed to ensure default data: {e}")

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
    cleanup_connections()
    print("Database connections cleaned up")

app = FastAPI(
    title="MBAS API - Z&T Technologies",
    version="2.1.0",  # PWA Update
    description="Modern Business Automation System - A Product of Z&T Technologies | State-of-the-Art Business Solutions | www.zttechnologies.org | Now with PWA support for cross-platform compatibility",
    contact={
        "name": "Z&T Technologies",
        "url": "https://www.zttechnologies.org",
        "email": "zttechnologies12@gmail.com"
    },
    lifespan=lifespan
)

# GZip compression - reduces JSON payload sizes by ~80%, critical for performance
app.add_middleware(GZipMiddleware, minimum_size=500)

# CORS configuration for PWA (supports local WiFi access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Vite dev server
        "http://localhost:4173",      # Vite preview
        "http://localhost:8000",      # PWA served from same origin
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
        "http://127.0.0.1:8000",
        # Allow local WiFi access (192.168.x.x for PWA on mobile devices)
        "*"  # For simplicity, allow all origins (offline-first app = low security risk)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# SQLite write-serialization middleware
# ---------------------------------------------------------------------------
# SQLite allows only ONE writer at a time. Without serialization, concurrent
# POST/PUT/DELETE requests race for the write lock; losers block for up to
# busy_timeout (seconds) while holding a DB connection, which starves reads
# and causes the UI to hang.  By funnelling all mutating HTTP methods through
# a single asyncio.Lock we guarantee:
#   1. Only one write request touches the DB at a time (no SQLITE_BUSY).
#   2. Read requests (GET/HEAD/OPTIONS) are never blocked.
#   3. Connections are short-lived (NullPool) so no pool exhaustion.
# ---------------------------------------------------------------------------
_sqlite_write_lock = asyncio.Lock()

@app.middleware("http")
async def serialize_write_requests(request: Request, call_next):
    if request.method in ("POST", "PUT", "DELETE", "PATCH"):
        async with _sqlite_write_lock:
            return await call_next(request)
    return await call_next(request)

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
app.include_router(version.router)

@app.get("/health")
def health_check():
    """Enhanced health check endpoint for monitoring and auto-recovery."""
    try:
        # Check database connectivity
        from src.core.db import engine
        from sqlmodel import Session, text

        with Session(engine) as session:
            session.exec(text("SELECT 1")).first()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "database": "connected",
                "version": "2.0.5",
                "vendor": "Z&T Technologies",
                "website": "www.zttechnologies.org"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "database": "disconnected",
                "error": str(e),
                "version": "2.0.5"
            }
        )

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
        # no-cache ensures browser always gets latest after updates
        return FileResponse(
            str(_FRONTEND_DIST / "index.html"),
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )

    print(f"Serving frontend from {_FRONTEND_DIST}")
else:
    @app.get("/")
    async def root():
        return {"message": "MBAS Backend API is running. Frontend not found - use http://localhost:5173 if running frontend dev server."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000)
