import sys
import os
import json
from typing import Optional, Dict, Any, List

# Add root and backend to python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "backend"))

from mcp.server.mcpserver import MCPServer
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
import app.models
from app.models.complaint import ComplaintRecord
from app.models.triage import RoutingRecommendation
from app.services.rag import rag_engine
from app.services.triage_agent import triage_agent
from app.core.pii import pii_engine
from app.api.complaints import record_audit
from app.core.logging import logger

mcp = MCPServer("CivicResolve-Guardian-MCP")

@mcp.tool()
def search_policy(query: str, department: Optional[str] = None) -> str:
    """
    Searches municipal bylaws, citizen charters, and SLA circulars for relevant sections.
    Returns grounded citations with relevance scores and required evidence.
    """
    if not query or len(query.strip()) < 3:
        return json.dumps({"error": "Query too short. Minimum 3 characters required."})
        
    db = SessionLocal()
    try:
        results = rag_engine.search_policy(db, query=query, department=department, top_k=3)
        if not results:
            return json.dumps({
                "status": "insufficient_evidence",
                "message": "No municipal policy matched the query above relevance threshold.",
                "citations": []
            })
        return json.dumps({"status": "success", "citations": results})
    finally:
        db.close()

@mcp.tool()
def get_case_summary(case_id: str, caller_role: str = "officer") -> str:
    """
    Retrieves a sanitized summary of a grievance case.
    PII is strictly redacted for all callers.
    """
    if caller_role not in ["officer", "admin"]:
        return json.dumps({"error": "Access Denied: caller must have officer or admin role."})
        
    db = SessionLocal()
    try:
        complaint = db.query(ComplaintRecord).filter(ComplaintRecord.id == case_id).first()
        if not complaint:
            return json.dumps({"error": f"Complaint '{case_id}' not found."})
            
        summary = {
            "id": complaint.id,
            "status": complaint.status,
            "language": complaint.original_language,
            "category": complaint.category,
            "department": complaint.department,
            "ward": complaint.ward,
            "priority": complaint.priority,
            "redacted_content": complaint.redacted_content,
            "has_audio": complaint.has_audio,
            "transcription": complaint.transcription,
            "created_at": complaint.created_at.isoformat() if complaint.created_at else None,
            "sla_due_at": complaint.sla_due_at.isoformat() if complaint.sla_due_at else None,
            "evidence_count": len(complaint.evidence_items)
        }
        
        record_audit(
            db=db,
            case_id=complaint.id,
            actor_id="mcp-agent",
            actor_role="mcp_tool",
            action_type="MCP_TOOL_INVOKED",
            details={"tool": "get_case_summary", "caller_role": caller_role}
        )
        return json.dumps({"status": "success", "case": summary})
    finally:
        db.close()

@mcp.tool()
def suggest_routing(case_id: str, caller_role: str = "officer") -> str:
    """
    Runs the deterministic bounded triage agent on a case and returns
    department, category, priority, citations, and confidence.
    """
    if caller_role not in ["officer", "admin"]:
        return json.dumps({"error": "Access Denied: caller must have officer or admin role."})
        
    db = SessionLocal()
    try:
        complaint = db.query(ComplaintRecord).filter(ComplaintRecord.id == case_id).first()
        if not complaint:
            return json.dumps({"error": f"Complaint '{case_id}' not found."})
            
        rec = triage_agent.evaluate_complaint(db, complaint)
        output = {
            "case_id": complaint.id,
            "suggested_department": rec.suggested_department,
            "suggested_category": rec.suggested_category,
            "priority_score": rec.priority_score,
            "confidence": rec.confidence,
            "reasons": rec.reasons,
            "citations_count": len(rec.citations),
            "approval_required": rec.approval_required
        }
        
        record_audit(
            db=db,
            case_id=complaint.id,
            actor_id="mcp-agent",
            actor_role="mcp_tool",
            action_type="MCP_TOOL_INVOKED",
            details={"tool": "suggest_routing", "result": output}
        )
        return json.dumps({"status": "success", "recommendation": output})
    finally:
        db.close()

@mcp.tool()
def list_missing_evidence(case_id: str, caller_role: str = "officer") -> str:
    """
    Analyzes case text and attached files to detect missing evidence items
    (e.g., missing landmark, missing photo for hazardous road/sewer failure).
    """
    if caller_role not in ["officer", "admin"]:
        return json.dumps({"error": "Access Denied: caller must have officer or admin role."})
        
    db = SessionLocal()
    try:
        complaint = db.query(ComplaintRecord).filter(ComplaintRecord.id == case_id).first()
        if not complaint:
            return json.dumps({"error": f"Complaint '{case_id}' not found."})
            
        rec = triage_agent.evaluate_complaint(db, complaint)
        return json.dumps({
            "status": "success",
            "case_id": case_id,
            "missing_evidence": rec.missing_evidence
        })
    finally:
        db.close()

@mcp.tool()
def draft_citizen_update(case_id: str, caller_role: str = "officer") -> str:
    """
    Generates a polite, grounded citizen update message in English or Tamil (தமிழ்)
    explaining current status, assigned department, and expected SLA.
    """
    if caller_role not in ["officer", "admin"]:
        return json.dumps({"error": "Access Denied: caller must have officer or admin role."})
        
    db = SessionLocal()
    try:
        complaint = db.query(ComplaintRecord).filter(ComplaintRecord.id == case_id).first()
        if not complaint:
            return json.dumps({"error": f"Complaint '{case_id}' not found."})
            
        rec = triage_agent.evaluate_complaint(db, complaint)
        return json.dumps({
            "status": "success",
            "case_id": case_id,
            "language": complaint.original_language,
            "draft_message": rec.draft_citizen_response
        })
    finally:
        db.close()

@mcp.tool()
def request_human_approval(
    case_id: str,
    proposed_department: str,
    proposed_priority: str,
    officer_notes: Optional[str] = None,
    caller_role: str = "officer"
) -> str:
    """
    Stages a formal routing approval request for an authorized officer.
    Strictly gates state transitions: does NOT change official status autonomously.
    """
    if caller_role not in ["officer", "admin"]:
        return json.dumps({"error": "Access Denied: caller must have officer or admin role."})
        
    db = SessionLocal()
    try:
        complaint = db.query(ComplaintRecord).filter(ComplaintRecord.id == case_id).first()
        if not complaint:
            return json.dumps({"error": f"Complaint '{case_id}' not found."})
            
        prev_state = complaint.status
        complaint.status = "TRIAGED_PENDING_APPROVAL"
        complaint.department = proposed_department
        complaint.priority = proposed_priority
        if officer_notes:
            complaint.officer_notes = officer_notes
        db.commit()
        
        record_audit(
            db=db,
            case_id=complaint.id,
            actor_id="mcp-agent",
            actor_role="mcp_tool",
            action_type="MCP_TOOL_INVOKED",
            details={
                "tool": "request_human_approval",
                "proposed_department": proposed_department,
                "proposed_priority": proposed_priority,
                "approval_required": True
            },
            previous_state=prev_state,
            new_state="TRIAGED_PENDING_APPROVAL"
        )
        
        return json.dumps({
            "status": "staged_for_approval",
            "case_id": case_id,
            "current_status": "TRIAGED_PENDING_APPROVAL",
            "message": "Approval request staged. A human officer must confirm before dispatch."
        })
    finally:
        db.close()

if __name__ == "__main__":
    mcp.run()
