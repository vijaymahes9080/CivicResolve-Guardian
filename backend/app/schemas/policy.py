from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PolicyChunkOut(BaseModel):
    id: str
    policy_id: str
    section_id: str
    section_title: str
    content: str
    evidence_required: List[str] = []
    escalation_path: Optional[str] = None
    keywords: Optional[str] = None

    class Config:
        from_attributes = True

class PolicyDocumentOut(BaseModel):
    id: str
    title: str
    department: str
    jurisdiction: str
    version: str
    effective_date: Optional[str] = None
    sla_hours: int
    summary: Optional[str] = None

    class Config:
        from_attributes = True

class PolicyCitation(BaseModel):
    policy_id: str
    section_id: str
    title: str
    excerpt: str
    relevance_score: float
