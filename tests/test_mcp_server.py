import pytest
import json
import sys
import os

# Add root and backend to python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "backend"))
sys.path.insert(0, os.path.join(ROOT_DIR, "mcp-server"))

from server import search_policy, get_case_summary, suggest_routing, list_missing_evidence, draft_citizen_update, request_human_approval
from app.models.complaint import ComplaintRecord
from app.db.session import SessionLocal

def test_mcp_search_policy():
    res_str = search_policy(query="Drinking water contamination with foul smell")
    res = json.loads(res_str)
    assert res["status"] == "success"
    assert len(res["citations"]) > 0
    assert "WATER" in res["citations"][0]["policy_id"]

def test_mcp_search_policy_insufficient_evidence():
    res_str = search_policy(query="Intergalactic spaceship repair grant")
    res = json.loads(res_str)
    assert res["status"] == "insufficient_evidence"
    assert len(res["citations"]) == 0

def test_mcp_get_case_summary_officer_allowed():
    db = SessionLocal()
    try:
        complaint = db.query(ComplaintRecord).first()
        assert complaint is not None
        case_id = complaint.id
    finally:
        db.close()

    res_str = get_case_summary(case_id=case_id, caller_role="officer")
    res = json.loads(res_str)
    assert res["status"] == "success"
    assert res["case"]["id"] == case_id
    assert "[PHONE_REDACTED]" in res["case"]["redacted_content"] or "9840123456" not in res["case"]["redacted_content"]

def test_mcp_unauthorized_role_rejected():
    res_str = get_case_summary(case_id="dummy-id", caller_role="citizen")
    res = json.loads(res_str)
    assert "error" in res
    assert "Access Denied" in res["error"]

def test_mcp_request_human_approval_staged():
    db = SessionLocal()
    try:
        complaint = db.query(ComplaintRecord).first()
        case_id = complaint.id
    finally:
        db.close()

    res_str = request_human_approval(
        case_id=case_id,
        proposed_department="Water Supply & Sewerage Board",
        proposed_priority="HIGH",
        officer_notes="Staged via MCP tool",
        caller_role="officer"
    )
    res = json.loads(res_str)
    assert res["status"] == "staged_for_approval"
    assert res["current_status"] == "TRIAGED_PENDING_APPROVAL"
