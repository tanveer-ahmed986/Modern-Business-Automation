from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MBAS API", version="1.0.0")

# CORS configuration for Tauri (React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, Tauri runs from a custom protocol (tauri://)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "MBAS Backend API is running offline."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
