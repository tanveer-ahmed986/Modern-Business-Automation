from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.src.api import auth, settings, inventory, billing, dashboard, suppliers, purchases
from backend.src.core.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    init_db()
    yield

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

@app.get("/")
async def root():
    return {"message": "MBAS Backend API is running offline."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
