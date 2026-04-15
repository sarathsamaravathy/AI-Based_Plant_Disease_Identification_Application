"""Database Models - SQLAlchemy ORM"""

from sqlalchemy import Column, String, Float, Integer, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class DiagnosisRecord(Base):
    """Record of disease diagnosis."""
    
    __tablename__ = "diagnoses"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=True)
    
    detected_disease = Column(String(100), nullable=False)
    confidence_score = Column(Float, nullable=False)
    symptoms_detected = Column(JSON, nullable=True)
    
    severity_level = Column(String(20), nullable=True)
    treatment_recommendations = Column(JSON, nullable=True)
    preventive_measures = Column(JSON, nullable=True)
    
    target_language = Column(String(10), default="en")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DiagnosisRecord(id={self.id}, disease={self.detected_disease})>"

class FeedbackRecord(Base):
    """User feedback for model improvement (RLHF)."""
    
    __tablename__ = "feedback"
    
    id = Column(String(36), primary_key=True)
    diagnosis_id = Column(String(36), nullable=False)
    user_id = Column(String(36), nullable=True)
    
    diagnosis_correct = Column(Boolean, nullable=True)
    recommendation_helpful = Column(Boolean, nullable=True)
    user_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
