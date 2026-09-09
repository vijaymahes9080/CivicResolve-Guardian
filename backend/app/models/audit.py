import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON
from app.db.base import Base

class AuditEvent(Base):
    __tablename__ = "audit_events"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String(36), index=True, nullable=False)
    actor_id = Column(String(36), nullable=False)
    actor_role = Column(String(50), nullable=False)  # citizen, officer, admin, system, mcp_tool
    action_type = Column(String(50), index=True, nullable=False)
    
    details = Column(JSON, default=dict)
    previous_state = Column(String(50), nullable=True)
    new_state = Column(String(50), nullable=True)
    
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    signature = Column(String(64), nullable=False)  # HMAC-SHA256 signature
