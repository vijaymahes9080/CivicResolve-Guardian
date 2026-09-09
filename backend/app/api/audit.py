from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.audit import AuditEvent
from app.schemas.audit import AuditEventOut
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/audit", tags=["Audit Log"])

@router.get("/{case_id}", response_model=List[AuditEventOut])
def get_audit_trail_for_case(
    case_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    events = db.query(AuditEvent).filter(AuditEvent.case_id == case_id).order_by(AuditEvent.timestamp.asc()).all()
    return events
