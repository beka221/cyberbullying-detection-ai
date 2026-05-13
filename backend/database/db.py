"""
Database configuration and initialization
Конфигурация и инициализация базы данных
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Create database URL
DATABASE_URL = settings.DATABASE_URL

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import models
from database.models import Base, Analysis


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database"""
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise
