import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class ComplaintRecord(Base):
    __tablename__ = "complaints"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    citizen_id = Column(String(36), ForeignKey("users.id"), index=True, nullable=False)
    
    original_language = Column(String(10), default="en", nullable=False)  # en, ta
    raw_content = Column(Text, nullable=False)  # RESTRICTED VAULT
    redacted_content = Column(Text, nullable=False)  # PUBLIC & AI PROCESSING
    
    has_audio = Column(Boolean, default=False)
    audio_consent_stored = Column(Boolean, default=False)
    audio_storage_path = Column(String(255), nullable=True)
    transcription = Column(Text, nullable=True)
    
    category = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    ward = Column(String(50), nullable=True)
    zone = Column(String(50), nullable=True)
    priority = Column(String(20), default="MEDIUM")  # CRITICAL, HIGH, MEDIUM, LOW
    
    status = Column(
        String(50),
        default="SUBMITTED",
        index=True,
        nullable=False
    )
    # SUBMITTED, TRIAGED_PENDING_APPROVAL, ROUTED_ASSIGNED, IN_PROGRESS,
    # ACTION_PROPOSED, RESOLVED_PENDING_VERIFICATION, VERIFIED_RESOLVED, REOPENED, REJECTED
    
    assigned_officer_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    officer_notes = Column(Text, nullable=True)
    resolution_summary = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    sla_due_at = Column(DateTime, nullable=True)
    
    # Relationships
    evidence_items = relationship("EvidenceItem", back_populates="complaint", cascade="all, delete-orphan")
    recommendation = relationship("RoutingRecommendation", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    resolution_assessment = relationship("ResolutionAssessment", back_populates="complaint", uselist=False, cascade="all, delete-orphan")

class EvidenceItem(Base):
    __tablename__ = "evidence_items"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String(36), ForeignKey("complaints.id"), index=True, nullable=False)
    
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    storage_path = Column(String(255), nullable=False)
    is_redacted = Column(Boolean, default=False)
    sha256_hash = Column(String(64), nullable=True)
    description = Column(String(255), nullable=True)
    uploaded_by_role = Column(String(50), default="citizen")  # citizen, officer
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    complaint = relationship("ComplaintRecord", back_populates="evidence_items")
