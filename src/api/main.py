"""FastAPI Application - Main REST API"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Plant Disease Identifier API",
    description="AI-powered multilingual plant disease identification",
    version="0.1.0"
)

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/v1/diagnose")
async def diagnose(
    file: UploadFile = File(...),
    language: str = Form(default="en"),
    plant_type: Optional[str] = Form(default=None)
):
    """Upload image for disease diagnosis."""
    try:
        if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        logger.info(f"Diagnosis request for language: {language}")
        
        return {
            "status": "processing",
            "message": "Pipeline implementation pending"
        }
        
    except Exception as e:
        logger.error(f"Diagnosis endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/diagnose/text")
async def diagnose_text(
    description: str,
    language: str = "en",
    plant_type: Optional[str] = None
):
    """Text-based diagnosis endpoint."""
    try:
        logger.info(f"Text diagnosis request: {description}")
        return {"status": "processing", "message": "Text pipeline implementation pending"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/languages")
async def get_supported_languages():
    """Get list of supported languages."""
    return {
        "languages": {
            "en": "English",
            "hi": "Hindi",
            "ta": "Tamil",
            "te": "Telugu",
            "ka": "Kannada",
            "ml": "Malayalam",
            "mr": "Marathi",
            "gu": "Gujarati",
            "bn": "Bengali"
        }
    }

@app.post("/api/v1/feedback")
async def submit_feedback(diagnosis_id: str, feedback: dict):
    """Submit feedback for diagnosis (RLHF)."""
    try:
        logger.info(f"Feedback received for diagnosis {diagnosis_id}")
        return {"status": "feedback_recorded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup."""
    logger.info("Starting Plant Disease Identifier API...")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Plant Disease Identifier API...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
    )
