import pytest
from app.models.complaint import ComplaintRecord, EvidenceItem
from app.services.resolution_checker import resolution_checker

def test_resolution_checker_verified_resolution(db_session):
    complaint = ComplaintRecord(
        citizen_id="usr-citizen-001",
        original_language="en",
        raw_content="Deep road pothole on 4th cross street.",
        redacted_content="Deep road pothole on 4th cross street.",
        status="IN_PROGRESS"
    )
    db_session.add(complaint)
    db_session.commit()
    db_session.refresh(complaint)
    
    # Add officer evidence
    evidence = EvidenceItem(
        complaint_id=complaint.id,
        file_name="pothole_repaired_photo.jpg",
        file_type="image/jpeg",
        file_size_bytes=102400,
        storage_path="/uploads/pothole_repaired.jpg",
        uploaded_by_role="officer"
    )
    db_session.add(evidence)
    db_session.commit()
    db_session.refresh(complaint)
    
    assessment = resolution_checker.evaluate_resolution(
        db=db_session,
        complaint=complaint,
        action_summary="Cold-mix bitumen patching completed on 4th cross street pothole. Site inspected.",
        officer_notes="Road surface leveled and cleared for traffic."
    )
    
    assert assessment.evaluation_verdict == "likely_resolved"
    assert assessment.deterministic_checks_passed is True
    assert assessment.contradiction_detected is False

def test_resolution_checker_contradiction_detected(db_session):
    complaint = ComplaintRecord(
        citizen_id="usr-citizen-001",
        original_language="en",
        raw_content="Open sewage overflow on main street.",
        redacted_content="Open sewage overflow on main street.",
        status="IN_PROGRESS"
    )
    db_session.add(complaint)
    db_session.commit()
    
    assessment = resolution_checker.evaluate_resolution(
        db=db_session,
        complaint=complaint,
        action_summary="Work cannot be repaired today due to funds awaited. Major tender called later.",
        officer_notes="Pending pipeline replacement."
    )
    
    assert assessment.evaluation_verdict == "contradiction_detected"
    assert assessment.contradiction_detected is True
