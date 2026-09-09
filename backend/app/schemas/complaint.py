from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.schemas.triage import RoutingRecommendationOut
from app.schemas.resolution import ResolutionAssessmentOut

class EvidenceItemOut(BaseModel):
    id: str
    complaint_id: str
    file_name: str
    file_type: str
    file_size_bytes: int
    storage_path: str
    is_redacted: bool
    sha256_hash: Optional[str] = None
    description: Optional[str] = None
    uploaded_by_role: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class ComplaintCreate(BaseModel):
    content: str
    language: Optional[str] = None  # en, ta, or auto-detect
    ward: Optional[str] = None
    zone: Optional[str] = None
    has_audio: bool = False
    audio_consent_stored: bool = False

class ComplaintOut(BaseModel):
    id: str
    citizen_id: str
    original_language: str
    redacted_content: str
    # Raw content is only accessible to authorized officers/admin
    raw_content: Optional[str] = None
    has_audio: bool
    audio_consent_stored: bool
    transcription: Optional[str] = None
    category: Optional[str] = None
    department: Optional[str] = None
    ward: Optional[str] = None
    zone: Optional[str] = None
    priority: str
    status: str
    assigned_officer_id: Optional[str] = None
    officer_notes: Optional[str] = None
    resolution_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    sla_due_at: Optional[datetime] = None
    evidence_items: List[EvidenceItemOut] = []
    recommendation: Optional[RoutingRecommendationOut] = None
    resolution_assessment: Optional[ResolutionAssessmentOut] = None

    class Config:
        from_attributes = True
