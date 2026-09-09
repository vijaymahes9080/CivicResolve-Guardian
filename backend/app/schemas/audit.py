from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class AuditEventOut(BaseModel):
    id: str
    case_id: str
    actor_id: str
    actor_role: str
    action_type: str
    details: Dict[str, Any] = {}
    previous_state: Optional[str] = None
    new_state: Optional[str] = None
    timestamp: datetime
    signature: str

    class Config:
        from_attributes = True
