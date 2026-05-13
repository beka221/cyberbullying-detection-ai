"""
Configuration settings for the application
Параметры конфигурации приложения
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./cyberbullying.db"
    )
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    # ML Models
    MODEL_PATH: str = os.getenv("MODEL_PATH", "data/models")
    VECTORIZER_PATH: str = os.getenv("VECTORIZER_PATH", "data/models/vectorizer.pkl")
    CLASSIFIER_PATH: str = os.getenv("CLASSIFIER_PATH", "data/models/classifier.pkl")
    
    # Thresholds
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", 0.5))
    
    # Telegram Bot
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    
    # Discord Bot
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    """Get cached settings"""
    return Settings()


settings = get_settings()
