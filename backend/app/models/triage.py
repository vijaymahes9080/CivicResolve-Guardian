import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class RoutingRecommendation(Base):
    __tablename__ = "routing_recommendations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String(36), ForeignKey("complaints.id"), unique=True, nullable=False)
    
    suggested_category = Column(String(100), nullable=False)
    suggested_department = Column(String(100), nullable=False)
    priority_score = Column(String(20), nullable=False)  # CRITICAL, HIGH, MEDIUM, LOW
    confidence = Column(Float, nullable=False)  # 0.0 - 1.0
    
    reasons = Column(JSON, default=list)  # List[str]
    citations = Column(JSON, default=list)  # List[Dict] with policy_id, section_id, excerpt
    duplicate_candidates = Column(JSON, default=list)  # List[Dict]
    missing_evidence = Column(JSON, default=list)  # List[str]
    draft_citizen_response = Column(String(1000), nullable=True)
    
    approval_required = Column(Boolean, default=True, nullable=False)
    approved_by_officer_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    is_approved = Column(Boolean, default=False)
    is_overridden = Column(Boolean, default=False)
    override_reason = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    approved_at = Column(DateTime, nullable=True)
    
    complaint = relationship("ComplaintRecord", back_populates="recommendation")
