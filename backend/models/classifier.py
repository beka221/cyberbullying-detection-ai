"""
Machine Learning Classifier for Cyberbullying Detection
Классификатор машинного обучения для обнаружения кибербуллинга
"""

import pickle
import numpy as np
from pathlib import Path
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

logger = logging.getLogger(__name__)

MODEL_PATH = Path(__file__).parent.parent.parent / "data" / "models"
MODEL_PATH.mkdir(parents=True, exist_ok=True)


class CyberbullyingClassifier:
    """Cyberbullying text classifier"""
    
    LABELS = {
        0: "Not Bullying",
        1: "Harassment",
        2: "Hate Speech",
        3: "Insults",
        4: "Threats"
    }
    
    def __init__(self, model_path=None, vectorizer_path=None):
        """Initialize classifier"""
        self.model_path = model_path or MODEL_PATH / "classifier.pkl"
        self.vectorizer_path = vectorizer_path or MODEL_PATH / "vectorizer.pkl"
        
        self.model = None
        self.vectorizer = None
        self.is_trained = False
        
        self.load_or_create_model()
    
    def load_or_create_model(self):
        """Load existing model or create new one"""
        try:
            if self.model_path.exists() and self.vectorizer_path.exists():
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                self.is_trained = True
                logger.info("Model loaded successfully")
            else:
                logger.warning("Model files not found, using demo classifier")
                self.create_demo_model()
        except Exception as e:
            logger.error(f"Model loading error: {e}")
            self.create_demo_model()
    
    def create_demo_model(self):
        """Create demo model for testing"""
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Demo training data
        demo_texts = [
            "You are stupid", "I hope you die", "Go kill yourself",
            "You're an idiot", "I hate you", "You're worthless",
            "You suck", "Loser", "Pathetic", "Disgusting",
            "Hello how are you", "Have a great day", "Nice to meet you",
            "Thanks for your help", "Hope you're doing well", "See you later"
        ]
        
        demo_labels = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        
        # Vectorize texts
        X = self.vectorizer.fit_transform(demo_texts)
        
        # Train model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, demo_labels)
        
        self.is_trained = True
        logger.info("Demo model created and trained")
    
    def predict(self, text: str) -> dict:
        """
        Predict cyberbullying label for text
        
        Предсказать метку кибербуллинга для текста
        """
        if not self.is_trained:
            raise RuntimeError("Model is not trained")
        
        try:
            # Vectorize
            X = self.vectorizer.transform([text])
            
            # Predict
            prediction = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            
            # Get confidence
            confidence = float(np.max(probabilities))
            
            # Check if bullying
            is_bullying = prediction != 0
            
            return {
                "label": self.LABELS[prediction],
                "confidence": confidence,
                "is_bullying": is_bullying,
                "probabilities": {
                    self.LABELS[i]: float(prob)
                    for i, prob in enumerate(probabilities)
                }
            }
        
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {
                "label": "Error",
                "confidence": 0.0,
                "is_bullying": False,
                "probabilities": {}
            }
    
    def train(self, texts: list, labels: list):
        """Train the model with new data"""
        try:
            X = self.vectorizer.fit_transform(texts)
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X, labels)
            self.is_trained = True
            self.save_model()
            logger.info(f"Model trained on {len(texts)} samples")
        except Exception as e:
            logger.error(f"Training error: {e}")
            raise
    
    def save_model(self):
        """Save model and vectorizer"""
        try:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.vectorizer, self.vectorizer_path)
            logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Model save error: {e}")
