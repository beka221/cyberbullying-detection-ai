import pickle
import numpy as np
from pathlib import Path
import logging
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import joblib
import json
import re

logger = logging.getLogger(__name__)

MODEL_PATH = Path(__file__).parent.parent.parent / "data" / "models"
MODEL_PATH.mkdir(parents=True, exist_ok=True)


class AdvancedCyberbullyingClassifier:
    """Advanced cyberbullying classifier with keyword highlighting"""
    
    CATEGORIES = {
        0: "Not Bullying",
        1: "Harassment",
        2: "Hate Speech",
        3: "Insults",
        4: "Threats",
        5: "Exclusion"
    }
    
    SEVERITY_LEVELS = {
        "critical": 5,
        "high": 4,
        "medium": 3,
        "low": 2,
        "none": 0
    }
    
    def __init__(self, language='en'):
        """Initialize classifier"""
        self.language = language
        self.model = None
        self.vectorizer = None
        self.bullying_keywords = {}
        self.is_trained = False
        
        self.load_keywords()
        self.load_or_create_model()
    
    def load_keywords(self):
        """Load bullying keywords"""
        try:
            if self.language == 'en':
                keyword_file = Path(__file__).parent.parent.parent / "data" / "datasets" / "english_bullying_keywords.json"
            else:
                keyword_file = Path(__file__).parent.parent.parent / "data" / "datasets" / "russian_bullying_keywords.json"
            
            if keyword_file.exists():
                with open(keyword_file, 'r', encoding='utf-8') as f:
                    self.bullying_keywords = json.load(f)
                logger.info(f"Keywords loaded for language: {self.language}")
            else:
                logger.warning(f"Keywords file not found: {keyword_file}")
                self.bullying_keywords = {"harassment": [], "hate_speech": [], "threats": [], "insults": []}
        except Exception as e:
            logger.error(f"Error loading keywords: {e}")
            self.bullying_keywords = {}
    
    def load_or_create_model(self):
        """Load model or create new one"""
        try:
            model_file = MODEL_PATH / f"classifier_{self.language}.pkl"
            vectorizer_file = MODEL_PATH / f"vectorizer_{self.language}.pkl"
            
            if model_file.exists() and vectorizer_file.exists():
                self.model = joblib.load(model_file)
                self.vectorizer = joblib.load(vectorizer_file)
                self.is_trained = True
                logger.info(f"Model loaded for language: {self.language}")
            else:
                logger.warning("Model files not found, using demo model")
                self.create_demo_model()
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.create_demo_model()
    
    def create_demo_model(self):
        """Create demo model for testing"""
        demo_texts = [
            # Bullying
            "you are stupid", "i hate you", "you will regret",
            "go away", "nobody likes you", "you're worthless",
            "ты дебил", "сдохни", "я найду тебя",
            "уходи", "никто тебя не любит", "ты ничтожество",
            # Normal
            "hello how are you", "thank you so much", "have a great day",
            "привет как дела", "спасибо большое", "хорошего дня"
        ]
        
        demo_labels = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english' if self.language == 'en' else 'russian',
            ngram_range=(1, 3),
            min_df=1
        )
        
        X = self.vectorizer.fit_transform(demo_texts)
        
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.model.fit(X, demo_labels)
        self.is_trained = True
        logger.info("Demo model created")
    
    def find_bullying_words(self, text):
        """Find bullying keywords in text"""
        text_lower = text.lower()
        found_words = []
        
        for category, keywords in self.bullying_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    found_words.append({
                        "word": keyword,
                        "category": category,
                        "position": text_lower.find(keyword.lower())
                    })
        
        return sorted(found_words, key=lambda x: x['position'])
    
    def highlight_text(self, text, bullying_words):
        """Create highlighted version of text"""
        if not bullying_words:
            return [{"text": text, "highlight": False}]
        
        highlighted = []
        last_pos = 0
        
        for item in bullying_words:
            keyword = item['word']
            pos = text.lower().find(keyword.lower(), last_pos)
            
            if pos != -1:
                # Add normal text before keyword
                if pos > last_pos:
                    highlighted.append({
                        "text": text[last_pos:pos],
                        "highlight": False
                    })
                
                # Add keyword
                highlighted.append({
                    "text": text[pos:pos + len(keyword)],
                    "highlight": True,
                    "category": item['category']
                })
                
                last_pos = pos + len(keyword)
        
        # Add remaining text
        if last_pos < len(text):
            highlighted.append({
                "text": text[last_pos:],
                "highlight": False
            })
        
        return highlighted
    
    def predict(self, text):
        """Predict cyberbullying label"""
        if not self.is_trained:
            raise RuntimeError("Model is not trained")
        
        try:
            # Find bullying words
            bullying_words = self.find_bullying_words(text)
            
            # Vectorize
            X = self.vectorizer.transform([text])
            
            # Predict
            prediction = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            confidence = float(np.max(probabilities))
            
            # Determine if bullying
            is_bullying = prediction != 0
            
            # Highlight text
            highlighted = self.highlight_text(text, bullying_words)
            
            # Determine severity
            severity = self.determine_severity(prediction, confidence, bullying_words)
            
            return {
                "label": self.CATEGORIES[prediction],
                "confidence": confidence,
                "is_bullying": is_bullying,
                "probabilities": {
                    self.CATEGORIES[i]: float(prob)
                    for i, prob in enumerate(probabilities)
                },
                "bullying_words": bullying_words,
                "highlighted_text": highlighted,
                "severity": severity
            }
        
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {
                "label": "Error",
                "confidence": 0.0,
                "is_bullying": False,
                "bullying_words": [],
                "highlighted_text": [{"text": text, "highlight": False}],
                "severity": "none"
            }
    
    def determine_severity(self, prediction, confidence, bullying_words):
        """Determine severity level"""
        if prediction == 0:
            return "none"
        
        if prediction == 4:  # Threats
            return "critical" if confidence > 0.7 else "high"
        
        if prediction == 2:  # Hate speech
            return "high" if confidence > 0.6 else "medium"
        
        if len(bullying_words) > 5:
            return "high"
        elif len(bullying_words) > 2:
            return "medium"
        else:
            return "low"
    
    def save_model(self):
        """Save model"""
        try:
            model_file = MODEL_PATH / f"classifier_{self.language}.pkl"
            vectorizer_file = MODEL_PATH / f"vectorizer_{self.language}.pkl"
            
            joblib.dump(self.model, model_file)
            joblib.dump(self.vectorizer, vectorizer_file)
            logger.info(f"Model saved for language: {self.language}")
        except Exception as e:
            logger.error(f"Model save error: {e}")
