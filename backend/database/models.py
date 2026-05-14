from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Analysis(Base):
    """Analysis record in database"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    processed_text = Column(Text, nullable=False)
    is_cyberbullying = Column(Boolean, nullable=False)
    label = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False)
    bullying_words = Column(Text, default="")
    language = Column(String(10), default="en")
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, label={self.label}, severity={self.severity})>"
