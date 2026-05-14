from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class TextAnalysisRequest(BaseModel):
    """Request model for text analysis"""
    text: str = Field(..., min_length=1, max_length=5000)
    language: str = Field("en", description="Language: en or ru")


class BullyingWord(BaseModel):
    """Bullying word found in text"""
    word: str
    category: str
    position: int


class HighlightedSegment(BaseModel):
    """Highlighted text segment"""
    text: str
    highlight: bool
    category: Optional[str] = None


class ClassificationResult(BaseModel):
    """Classification result"""
    label: str
    confidence: float = Field(..., ge=0, le=1)
    probability: Dict[str, float]


class TextAnalysisResponse(BaseModel):
    """Response model for text analysis"""
    id: Optional[int] = None
    text: str
    is_cyberbullying: bool
    classification: ClassificationResult
    severity: str
    severity_color: Optional[str] = None
    bullying_words: List[BullyingWord] = []
    highlighted_text: List[HighlightedSegment] = []
    explanation: str
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
    by_category: Dict[str, int]
    by_severity: Dict[str, int]
    timestamp: datetime
