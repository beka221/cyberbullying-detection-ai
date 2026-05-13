"""
API Request/Response schemas
Схемы запросов и ответов API
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TextAnalysisRequest(BaseModel):
    """Request model for text analysis"""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to analyze")
    language: Optional[str] = Field("en", description="Text language (en/ru/kk)")


class ClassificationResult(BaseModel):
    """Classification result"""
    label: str = Field(..., description="Classification label")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    probability: dict = Field(..., description="Probabilities for all classes")


class TextAnalysisResponse(BaseModel):
    """Response model for text analysis"""
    id: Optional[int] = None
    text: str
    is_cyberbullying: bool
    classification: ClassificationResult
    severity: Optional[str] = Field(None, description="Severity level: low/medium/high")
    timestamp: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AnalysisHistory(BaseModel):
    """Analysis history item"""
    id: int
    text: str
    is_cyberbullying: bool
    label: str
    confidence: float
    severity: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class StatisticsResponse(BaseModel):
    """Statistics response"""
    total_analyses: int
    bullying_detected: int
    not_bullying: int
    detection_rate: float
    average_confidence: float
    by_category: dict
    by_severity: dict
    timestamp: datetime


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    service: str
