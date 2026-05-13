"""
API routes for cyberbullying detection
API маршруты для обнаружения кибербуллинга
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import logging

from database.db import get_db
from database.models import Analysis
from models.classifier import CyberbullyingClassifier
from api.schemas import (
    TextAnalysisRequest,
    TextAnalysisResponse,
    AnalysisHistory,
    StatisticsResponse,
    HealthResponse
)
from utils.text_processor import TextProcessor

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize classifier and text processor
classifier = CyberbullyingClassifier()
text_processor = TextProcessor()


def get_severity(confidence: float) -> str:
    """Determine severity based on confidence"""
    if confidence >= 0.8:
        return "high"
    elif confidence >= 0.6:
        return "medium"
    else:
        return "low"


@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(
    request: TextAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze text for cyberbullying
    
    Анализировать текст на наличие кибербуллинга
    """
    try:
        # Clean and preprocess text
        cleaned_text = text_processor.clean_text(request.text)
        
        # Get prediction
        prediction = classifier.predict(cleaned_text)
        
        # Determine severity
        severity = get_severity(prediction['confidence'])
        
        # Save to database
        analysis = Analysis(
            original_text=request.text,
            processed_text=cleaned_text,
            is_cyberbullying=prediction['is_bullying'],
            label=prediction['label'],
            confidence=prediction['confidence'],
            severity=severity,
            language=request.language,
            timestamp=datetime.utcnow()
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        logger.info(f"Analysis completed: {analysis.id}")
        
        return TextAnalysisResponse(
            id=analysis.id,
            text=request.text,
            is_cyberbullying=prediction['is_bullying'],
            classification={
                "label": prediction['label'],
                "confidence": prediction['confidence'],
                "probability": prediction['probabilities']
            },
            severity=severity,
            timestamp=analysis.timestamp
        )
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=List[AnalysisHistory])
async def get_history(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Get analysis history
    
    Получить историю анализов
    """
    try:
        analyses = db.query(Analysis)\
            .order_by(Analysis.timestamp.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        return [
            AnalysisHistory(
                id=a.id,
                text=a.original_text,
                is_cyberbullying=a.is_cyberbullying,
                label=a.label,
                confidence=a.confidence,
                severity=a.severity,
                timestamp=a.timestamp
            )
            for a in analyses
        ]
    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=StatisticsResponse)
async def get_statistics(
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get statistics for the last N days
    
    Получить статистику за последние N дней
    """
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        analyses = db.query(Analysis)\
            .filter(Analysis.timestamp >= start_date)\
            .all()
        
        if not analyses:
            raise HTTPException(status_code=404, detail="No data found")
        
        total = len(analyses)
        bullying = sum(1 for a in analyses if a.is_cyberbullying)
        not_bullying = total - bullying
        
        avg_confidence = sum(a.confidence for a in analyses) / total if total > 0 else 0
        
        by_category = {}
        by_severity = {}
        
        for analysis in analyses:
            by_category[analysis.label] = by_category.get(analysis.label, 0) + 1
            by_severity[analysis.severity] = by_severity.get(analysis.severity, 0) + 1
        
        return StatisticsResponse(
            total_analyses=total,
            bullying_detected=bullying,
            not_bullying=not_bullying,
            detection_rate=bullying / total if total > 0 else 0,
            average_confidence=avg_confidence,
            by_category=by_category,
            by_severity=by_severity,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Statistics error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history/{analysis_id}")
async def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete analysis from history
    
    Удалить анализ из истории
    """
    try:
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        db.delete(analysis)
        db.commit()
        
        return {"message": "Analysis deleted successfully"}
        
    except Exception as e:
        logger.error(f"Delete error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
