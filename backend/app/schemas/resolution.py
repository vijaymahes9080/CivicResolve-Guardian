from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ResolutionSubmissionRequest(BaseModel):
    action_taken_summary: str
    field_worker_name: Optional[str] = None
    materials_used: Optional[str] = None
    completion_notes: Optional[str] = None

class ResolutionAssessmentOut(BaseModel):
    id: str
    complaint_id: str
    evaluation_verdict: str
    confidence: float
    explanation: str
    deterministic_checks_passed: bool
    checks_detail: Dict[str, Any] = {}
    contradiction_detected: bool
    contradiction_notes: Optional[str] = None
    evidence_references: List[str] = []
    citizen_satisfaction_score: Optional[int] = None
    evaluated_at: datetime

    class Config:
        from_attributes = True
