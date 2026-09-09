import pytest
from app.models.complaint import ComplaintRecord
from app.services.triage_agent import triage_agent

def test_triage_water_leak_complaint(db_session):
    complaint = ComplaintRecord(
        citizen_id="usr-citizen-001",
        original_language="en",
        raw_content="Drinking water pipeline burst near Gandhi statue, Ward 12. Heavy leakage on street.",
        redacted_content="Drinking water pipeline burst near Gandhi statue, Ward 12. Heavy leakage on street.",
        ward="Ward 12",
        status="SUBMITTED"
    )
    db_session.add(complaint)
    db_session.commit()
    db_session.refresh(complaint)
    
    rec = triage_agent.evaluate_complaint(db_session, complaint)
    
    assert rec.suggested_department == "Water Supply & Sewerage Board"
    assert rec.priority_score in ["HIGH", "CRITICAL"]
    assert rec.confidence > 0.60
    assert rec.approval_required is True
    assert len(rec.citations) > 0
    assert "Ward 12" in rec.draft_citizen_response or "Water Supply" in rec.draft_citizen_response

def test_triage_tamil_street_light_complaint(db_session):
    complaint = ComplaintRecord(
        citizen_id="usr-citizen-001",
        original_language="ta",
        raw_content="எங்கள் தெருவில் தெரு விளக்கு எரியவில்லை. இருட்டாக உள்ளது.",
        redacted_content="எங்கள் தெருவில் தெரு விளக்கு எரியவில்லை. இருட்டாக உள்ளது.",
        ward="Ward 14",
        status="SUBMITTED"
    )
    db_session.add(complaint)
    db_session.commit()
    db_session.refresh(complaint)
    
    rec = triage_agent.evaluate_complaint(db_session, complaint)
    
    assert rec.suggested_department == "Electrical & Street Lighting"
    assert rec.approval_required is True
    assert "வணக்கம்" in rec.draft_citizen_response
