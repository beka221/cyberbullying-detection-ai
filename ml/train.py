"""
Machine Learning Model Training
Обучение моделей машинного обучения
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
from pathlib import Path
import logging
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Data paths
DATA_PATH = Path(__file__).parent.parent / "data"
RAW_DATA = DATA_PATH / "raw" / "cyberbullying_tweets.csv"
MODEL_PATH = DATA_PATH / "models"

MODEL_PATH.mkdir(parents=True, exist_ok=True)


def load_data(file_path):
    """Load cyberbullying dataset"""
    if not file_path.exists():
        logging.info("Data file not found, creating synthetic dataset...")
        return create_synthetic_data()
    
    df = pd.read_csv(file_path)
    return df


def create_synthetic_data():
    """Create synthetic training data"""
    
    texts = [
        "You are so stupid and worthless", "I hate you, die", "You're a loser",
        "Kill yourself", "Everyone hates you", "You're disgusting",
        "You should be ashamed", "You're pathetic", "Nobody likes you",
        "You're an idiot", "Go away", "You're trash", "I despise you",
        "You're ugly", "You're fat", "You're weird", "You suck",
        "You're annoying", "Shut up", "You're dumb",
        "Hello, how are you?", "Have a great day", "Thanks for your help",
        "I appreciate your kindness", "Nice to meet you", "See you later",
        "Good morning", "Happy birthday", "Congratulations", "Well done",
        "You did great", "I'm proud of you", "Keep up the good work",
        "Let's be friends", "I like your idea", "That's cool",
    ]
    
    labels = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    
    return pd.DataFrame({
        'text': texts,
        'label': labels
    })


def train_model(df):
    """Train machine learning models"""
    
    X = df['text'].values
    y = df['label'].values
    
    # Vectorize text
    print("Vectorizing text...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=1,
        max_df=1.0
    )
    X_vectorized = vectorizer.fit_transform(X)
    
    # Split data
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
    
    # Train Random Forest
    print("Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "="*50)
    print("MODEL PERFORMANCE / ПРОИЗВОДИТЕЛЬНОСТЬ МОДЕЛИ")
    print("="*50)
    print(f"Accuracy / Точность: {accuracy:.4f}")
    print("\nClassification Report / Отчет о классификации:")
    print(classification_report(y_test, y_pred))
    
    # Save models
    print("\nSaving models...")
    joblib.dump(vectorizer, MODEL_PATH / "vectorizer.pkl")
    joblib.dump(rf_model, MODEL_PATH / "classifier.pkl")
    
    print(f"✓ Models saved to {MODEL_PATH}")
    
    return vectorizer, rf_model


def main():
    """Main training function"""
    print("="*50)
    print("CYBERBULLYING DETECTION MODEL TRAINING")
    print("ОБУЧЕНИЕ МОДЕЛИ ОБНАРУЖЕНИЯ КИБЕРБУЛЛИНГА")
    print("="*50)
    
    # Load data
    print("\nLoading data...")
    df = load_data(RAW_DATA)
    print(f"Dataset size: {len(df)} samples / Размер датасета: {len(df)} образцов")
    print(f"Classes distribution / Распределение классов:")
    print(df['label'].value_counts())
    
    # Train model
    vectorizer, model = train_model(df)
    
    print("\n✓ Training completed successfully!")
    print("✓ Обучение завершено успешно!")


if __name__ == "__main__":
    main()
