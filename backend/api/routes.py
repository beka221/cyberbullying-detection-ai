from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import logging

from database.db import get_db
from database.models import Analysis
from models.advanced_classifier import AdvancedCyberbullyingClassifier
from api.schemas import (
    TextAnalysisRequest,
    TextAnalysisResponse,
    AnalysisHistory,
    StatisticsResponse
)
from utils.text_processor import TextProcessor

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize classifiers for both languages
classifiers = {
    'en': AdvancedCyberbullyingClassifier(language='en'),
    'ru': AdvancedCyberbullyingClassifier(language='ru')
}

text_processor = TextProcessor()


def get_severity_color(severity: str) -> str:
    """Get color for severity level"""
    colors = {
        "critical": "#dc3545",
        "high": "#fd7e14",
        "medium": "#ffc107",
        "low": "#0dcaf0",
        "none": "#198754"
    }
    return colors.get(severity, "#6c757d")


@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(
    request: TextAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze text for cyberbullying with detailed results"""
    try:
        # Get classifier for language
        classifier = classifiers.get(request.language, classifiers['en'])
        
        # Clean text
        cleaned_text = text_processor.clean_text(request.text)
        
        # Get prediction with detailed results
        prediction = classifier.predict(request.text)  # Use original for highlighting
        
        # Save to database
        analysis = Analysis(
            original_text=request.text,
            processed_text=cleaned_text,
            is_cyberbullying=prediction['is_bullying'],
            label=prediction['label'],
            confidence=prediction['confidence'],
            severity=prediction['severity'],
            bullying_words=str(prediction['bullying_words']),
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
            severity=prediction['severity'],
            severity_color=get_severity_color(prediction['severity']),
            bullying_words=prediction['bullying_words'],
            highlighted_text=prediction['highlighted_text'],
            explanation=generate_explanation(prediction, request.language),
            timestamp=analysis.timestamp
        )
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def generate_explanation(prediction: dict, language: str) -> str:
    """Generate explanation for the prediction"""
    if not prediction['is_bullying']:
        return "This text appears to be safe and respectful." if language == 'en' else "Этот текст безопасный и вежливый."
    
    label = prediction['label']
    severity = prediction['severity']
    word_count = len(prediction['bullying_words'])
    
    explanations = {
        'en': {
            'Harassment': f"This text contains {word_count} harassment keyword(s) and has {severity} severity. The tone is disrespectful and may cause emotional harm.",
            'Hate_Speech': f"This text contains hate speech. {word_count} harmful word(s) detected with {severity} severity. This type of content is harmful and unacceptable.",
            'Threats': f"This text contains threats. {word_count} threatening word(s) detected. This is serious and should be reported.",
            'Insults': f"This text contains {word_count} insult(s) with {severity} severity. The language is derogatory and offensive.",
            'Exclusion': f"This text attempts to exclude or alienate. {word_count} exclusionary phrase(s) detected with {severity} severity."
        },
        'ru': {
            'Harassment': f"Текст содержит {word_count} оскорбление(я) с уровнем серьезности {severity}. Тон неуважительный и может причинить вред.",
            'Hate_Speech': f"Текст содержит речь ненависти. Обнаружено {word_count} вредоносное(ых) слово(а) с уровнем {severity}. Это содержание вредно и неприемлемо.",
            'Threats': f"Текст содержит угрозы. Обнаружено {word_count} угрожающее(ых) слово(а). Это серьезно и должно быть сообщено.",
            'Insults': f"Текст содержит {word_count} оскорбление(я) с уровнем {severity}. Язык унизительный и оскорбительный.",
            'Exclusion': f"Текст пытается исключить или отчуждать. Обнаружено {word_count} исключающее(их) выражение(я) с уровнем {severity}."
        }
    }
    
    lang_expl = explanations.get(language, explanations['en'])
    return lang_expl.get(label, "Unable to generate explanation.")


@router.get("/history", response_model=List[AnalysisHistory])
async def get_history(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get analysis history"""
    try:
        analyses = db.query(Analysis).order_by(Analysis.timestamp.desc()).limit(limit).offset(offset).all()
        
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
        logger.error(f"History error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=StatisticsResponse)
async def get_statistics(
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get statistics"""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        analyses = db.query(Analysis).filter(Analysis.timestamp >= start_date).all()
        
        if not analyses:
            raise HTTPException(status_code=404, detail="No data found")
        
        total = len(analyses)
        bullying = sum(1 for a in analyses if a.is_cyberbullying)
        
        by_category = {}
        by_severity = {}
        
        for analysis in analyses:
            by_category[analysis.label] = by_category.get(analysis.label, 0) + 1
            by_severity[analysis.severity] = by_severity.get(analysis.severity, 0) + 1
        
        avg_confidence = sum(a.confidence for a in analyses) / total if total > 0 else 0
        
        return StatisticsResponse(
            total_analyses=total,
            bullying_detected=bullying,
            not_bullying=total - bullying,
            detection_rate=bullying / total if total > 0 else 0,
            average_confidence=avg_confidence,
            by_category=by_category,
            by_severity=by_severity,
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Statistics error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
