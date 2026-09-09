from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.schemas.policy import PolicyCitation

class RoutingRecommendationOut(BaseModel):
    id: str
    complaint_id: str
    suggested_category: str
    suggested_department: str
    priority_score: str
    confidence: float
    reasons: List[str] = []
    citations: List[PolicyCitation] = []
    duplicate_candidates: List[Dict[str, Any]] = []
    missing_evidence: List[str] = []
    draft_citizen_response: Optional[str] = None
    approval_required: bool = True
    is_approved: bool = False
    is_overridden: bool = False
    override_reason: Optional[str] = None
    created_at: datetime
    approved_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RoutingApprovalRequest(BaseModel):
    approved_department: Optional[str] = None
    approved_priority: Optional[str] = None
    override_reason: Optional[str] = None
    officer_notes: Optional[str] = None
