import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
import joblib
from pathlib import Path
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).parent.parent / "data"
MODEL_PATH = DATA_PATH / "models"
MODEL_PATH.mkdir(parents=True, exist_ok=True)


def load_training_data():
    """Load training datasets"""
    datasets = []
    
    for lang in ['en', 'ru']:
        csv_file = DATA_PATH / "datasets" / f"training_data_{lang}.csv"
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            df['language'] = lang
            datasets.append(df)
            logger.info(f"Loaded {len(df)} samples from {lang} dataset")
    
    if datasets:
        return pd.concat(datasets, ignore_index=True)
    
    return None


def train_language_model(df, language):
    """Train model for specific language"""
    print(f"\n{'='*60}")
    print(f"Training model for {language.upper()}")
    print(f"{'='*60}")
    
    # Filter by language
    lang_data = df[df['language'] == language]
    
    if len(lang_data) == 0:
        logger.warning(f"No data for language {language}")
        return None, None
    
    X = lang_data['text'].values
    y = lang_data['label'].values
    
    print(f"\nDataset size: {len(X)} samples")
    print(f"Class distribution:")
    unique, counts = np.unique(y, return_counts=True)
    for u, c in zip(unique, counts):
        print(f"  Class {u}: {c} samples ({c/len(y)*100:.1f}%)")
    
    # Vectorize
    print("\nVectorizing text...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english' if language == 'en' else 'russian',
        ngram_range=(1, 3),
        min_df=1,
        max_df=1.0
    )
    X_vectorized = vectorizer.fit_transform(X)
    print(f"Feature vector shape: {X_vectorized.shape}")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Train
    print("\nTraining Gradient Boosting Classifier...")
    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42,
        verbose=1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    print("\nEvaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, digits=4))
    
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    print(f"\nWeighted Metrics:")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall: {recall:.4f}")
    print(f"  F1-Score: {f1:.4f}")
    
    # Save
    model_file = MODEL_PATH / f"classifier_{language}.pkl"
    vectorizer_file = MODEL_PATH / f"vectorizer_{language}.pkl"
    
    joblib.dump(model, model_file)
    joblib.dump(vectorizer, vectorizer_file)
    
    print(f"\n✓ Model saved: {model_file}")
    print(f"✓ Vectorizer saved: {vectorizer_file}")
    
    return model, vectorizer


def main():
    print("\n" + "="*60)
    print("CYBERBULLYING DETECTION - ADVANCED MODEL TRAINING")
    print("="*60)
    
    # Load data
    print("\nLoading training data...")
    df = load_training_data()
    
    if df is None:
        logger.error("No training data found")
        return
    
    print(f"\nTotal samples: {len(df)}")
    print(f"Languages: {df['language'].unique().tolist()}")
    
    # Train models
    for lang in ['en', 'ru']:
        train_language_model(df, lang)
    
    print(f"\n{'='*60}")
    print("✓ Training completed successfully!")
    print("✓ Обучение завершено успешно!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
