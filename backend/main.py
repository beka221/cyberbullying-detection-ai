"""
Cyberbullying Detection System - Main FastAPI Application
Система обнаружения кибербуллинга - основное приложение FastAPI
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from api.routes import router as api_router
from database.db import init_db, engine, Base
from config import settings
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

# Create FastAPI instance
app = FastAPI(
    title="Cyberbullying Detection API",
    description="AI-based system for early detection and classification of cyberbullying",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
Base.metadata.create_all(bind=engine)
init_db()

logger.info("Database initialized successfully")

# Include API routes
app.include_router(api_router, prefix="/api", tags=["analysis"])

# Serve static files
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    logger.info(f"Frontend mounted from {frontend_path}")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve main HTML page"""
    frontend_file = Path(__file__).parent.parent / "frontend" / "index.html"
    if frontend_file.exists():
        with open(frontend_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    return """
    <html>
        <head>
            <title>Cyberbullying Detection AI</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>🚀 Cyberbullying Detection System</h1>
            <p>API is running! Visit <a href="/docs">/docs</a> for API documentation</p>
            <p>🇷🇺 <a href="/docs">Документация API</a></p>
        </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Cyberbullying Detection API"
    }


@app.get("/info")
async def get_info():
    """Get system information"""
    return {
        "name": "Cyberbullying Detection and Classification System",
        "version": "1.0.0",
        "description": "AI-based system for early detection and classification of cyberbullying",
        "languages": ["English", "Russian", "Kazakh"],
        "models": ["Logistic Regression", "Random Forest", "BERT (optional)"],
        "endpoints": {
            "analyze": "/api/analyze",
            "history": "/api/history",
            "stats": "/api/stats",
            "health": "/health"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("🚀 Cyberbullying Detection System started")
    logger.info(f"Server running on {settings.API_HOST}:{settings.API_PORT}")
    logger.info(f"API Docs available at http://{settings.API_HOST}:{settings.API_PORT}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("🛑 Shutting down Cyberbullying Detection System")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
