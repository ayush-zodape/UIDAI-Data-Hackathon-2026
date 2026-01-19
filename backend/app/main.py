from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, analysis, chat
from app.config import settings

app = FastAPI(
    title="UIDAI BLI Analyzer",
    description="Biometric Lag Index Analysis Platform",
    version="1.0.0"
)

# CORS Configuration - IMPORTANT for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chatbot"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "uidai-bli-analyzer"}
