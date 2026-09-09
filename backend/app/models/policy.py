import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime, JSON
from app.db.base import Base

class PolicyDocument(Base):
    __tablename__ = "policy_documents"
    
    id = Column(String(50), primary_key=True)  # e.g., POL-WATER-001
    title = Column(String(255), nullable=False)
    department = Column(String(100), index=True, nullable=False)
    jurisdiction = Column(String(100), default="Tamil Nadu Municipal Administration", nullable=False)
    version = Column(String(20), default="1.0")
    effective_date = Column(String(20), nullable=True)
    sla_hours = Column(Integer, default=48, nullable=False)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class PolicyChunk(Base):
    __tablename__ = "policy_chunks"
    
    id = Column(String(100), primary_key=True)  # e.g., POL-WATER-001-C1
    policy_id = Column(String(50), index=True, nullable=False)
    section_id = Column(String(50), nullable=False)
    section_title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    evidence_required = Column(JSON, default=list)
    escalation_path = Column(String(255), nullable=True)
    keywords = Column(String(500), nullable=True)
    embedding_vector = Column(JSON, nullable=True)  # Stored as serialized float list
