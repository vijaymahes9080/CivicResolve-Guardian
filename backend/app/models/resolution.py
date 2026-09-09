import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Float, Boolean, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class ResolutionAssessment(Base):
    __tablename__ = "resolution_assessments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String(36), ForeignKey("complaints.id"), unique=True, nullable=False)
    
    evaluation_verdict = Column(String(50), nullable=False)
    # likely_resolved, weak_resolution, insufficient_evidence, contradiction_detected
    
    confidence = Column(Float, nullable=False)
    explanation = Column(Text, nullable=False)
    
    deterministic_checks_passed = Column(Boolean, default=False)
    checks_detail = Column(JSON, default=dict)
    
    contradiction_detected = Column(Boolean, default=False)
    contradiction_notes = Column(Text, nullable=True)
    evidence_references = Column(JSON, default=list)
    citizen_satisfaction_score = Column(Integer, nullable=True)
    
    evaluated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    complaint = relationship("ComplaintRecord", back_populates="resolution_assessment")
