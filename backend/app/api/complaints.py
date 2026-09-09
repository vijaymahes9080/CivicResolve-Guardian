import os
import hashlib
import json
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.complaint import ComplaintRecord, EvidenceItem
from app.models.triage import RoutingRecommendation
from app.models.resolution import ResolutionAssessment
from app.models.audit import AuditEvent
from app.schemas.complaint import ComplaintCreate, ComplaintOut, EvidenceItemOut
from app.schemas.triage import RoutingRecommendationOut, RoutingApprovalRequest
from app.schemas.resolution import ResolutionSubmissionRequest, ResolutionAssessmentOut
from app.core.pii import pii_engine
from app.core.security import compute_audit_signature
from app.core.config import settings
from app.api.deps import get_current_user, get_current_officer
from app.services.language import LanguageDetector
from app.services.audio import AudioAdapter
from app.services.triage_agent import triage_agent
from app.services.resolution_checker import resolution_checker

router = APIRouter(prefix="/complaints", tags=["Complaints"])

def record_audit(
    db: Session,
    case_id: str,
    actor_id: str,
    actor_role: str,
    action_type: str,
    details: dict,
    previous_state: Optional[str] = None,
    new_state: Optional[str] = None
):
    now_str = datetime.now(timezone.utc).isoformat()
    details_str = json.dumps(details, sort_keys=True)
    sig = compute_audit_signature(case_id, action_type, actor_id, now_str, details_str)
    
    event = AuditEvent(
        case_id=case_id,
        actor_id=actor_id,
        actor_role=actor_role,
        action_type=action_type,
        details=details,
        previous_state=previous_state,
        new_state=new_state,
        signature=sig
    )
    db.add(event)
    db.commit()

@router.post("", response_model=ComplaintOut, status_code=status.HTTP_201_CREATED)
def create_complaint(
    payload: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Detect language if not provided
    lang = payload.language or LanguageDetector.detect(payload.content)
    
    # Redact PII
    redacted_text, pii_audit = pii_engine.redact(payload.content)
    
    complaint = ComplaintRecord(
        citizen_id=current_user.id,
        original_language=lang,
        raw_content=payload.content,  # Encrypted / Restricted Vault
        redacted_content=redacted_text,  # Public & AI Processing layer
        ward=payload.ward,
        zone=payload.zone,
        has_audio=payload.has_audio,
        audio_consent_stored=payload.audio_consent_stored,
        status="SUBMITTED",
        priority="MEDIUM",
        sla_due_at=datetime.now(timezone.utc) + timedelta(hours=48)
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    
    record_audit(
        db=db,
        case_id=complaint.id,
        actor_id=current_user.id,
        actor_role=current_user.role,
        action_type="COMPLAINT_CREATED",
        details={
            "language": lang,
            "has_audio": payload.has_audio,
            "pii_items_detected": len(pii_audit),
            "ward": payload.ward
        },
        new_state="SUBMITTED"
    )
    
    return complaint

@router.get("", response_model=List[ComplaintOut])
def list_complaints(
    status_filter: Optional[str] = Query(None, alias="status"),
    department_filter: Optional[str] = Query(None, alias="department"),
    ward_filter: Optional[str] = Query(None, alias="ward"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ComplaintRecord)
    
    # Citizen can only view their own complaints; Officers & Admins view all
    if current_user.role == "citizen":
        query = query.filter(ComplaintRecord.citizen_id == current_user.id)
        
    if status_filter:
        query = query.filter(ComplaintRecord.status == status_filter)
    if department_filter:
        query = query.filter(ComplaintRecord.department == department_filter)
    if ward_filter:
        query = query.filter(ComplaintRecord.ward == ward_filter)
        
    complaints = query.order_by(ComplaintRecord.created_at.desc()).offset(offset).limit(limit).all()
    
    # Mask raw_content for users without officer/admin clearance
    for c in complaints:
        if current_user.role not in ["officer", "admin"] and c.citizen_id != current_user.id:
            c.raw_content = None
            
    return complaints

@router.get("/{id}", response_model=ComplaintOut)
def get_complaint(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    complaint = db.query(ComplaintRecord).filter(ComplaintRecord.id == id).first()
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
        
    # Authorization check
    if current_user.role == "citizen" and complaint.citizen_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this complaint")
        
    if current_user.role not in ["officer", "admin"]:
        complaint.raw_content = None
        
    return complaint

@router.post("/{id}/evidence", response_model=EvidenceItemOut, status_code=status.HTTP_201_CREATED)
def upload_evidence(
    id: str,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    complaint = db.query(ComplaintRecord).filter(ComplaintRecord.id == id).first()
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
        
    if current_user.role == "citizen" and complaint.citizen_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        
    ext = file.filename.split(".")[-1].lower() if file.filename else ""
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension '.{ext}' not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}"
        )
        
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, f"{id}_{file.filename}")
    
    hasher = hashlib.sha256()
    size = 0
    with open(file_path, "wb") as buffer:
        chunk = file.file.read(1024 * 1024)
        while chunk:
            size += len(chunk)
            if size > settings.MAX_UPLOAD_SIZE_BYTES:
                os.remove(file_path)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File exceeds 10MB limit")
            hasher.update(chunk)
            buffer.write(chunk)
            chunk = file.file.read(1024 * 1024)
            
    sha256_hash = hasher.hexdigest()
    
    # Check if this is an audio file and transcribe
    if ext in ["webm", "wav", "mp3", "ogg"]:
        transcription_text = AudioAdapter.transcribe(file_path, language=complaint.original_language)
        complaint.transcription = transcription_text
        complaint.has_audio = True
        complaint.audio_storage_path = file_path
        
    evidence = EvidenceItem(
        complaint_id=complaint.id,
        file_name=file.filename or "evidence",
        file_type=file.content_type or f"application/{ext}",
        file_size_bytes=size,
        storage_path=file_path,
        sha256_hash=sha256_hash,
        description=description,
        uploaded_by_role=current_user.role
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    
    record_audit(
        db=db,
        case_id=complaint.id,
        actor_id=current_user.id,
        actor_role=current_user.role,
        action_type="EVIDENCE_ATTACHED",
        details={"file_name": file.filename, "size_bytes": size, "sha256": sha256_hash}
    )
    
    return evidence

@router.post("/{id}/triage", response_model=RoutingRecommendationOut)
def triage_complaint(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    complaint = db.query(ComplaintRecord).filter(ComplaintRecord.id == id).first()
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
        
    # Remove existing recommendation if any
    if complaint.recommendation:
        db.delete(complaint.recommendation)
        db.commit()
        
    recommendation = triage_agent.evaluate_complaint(db, complaint)
    db.add(recommendation)
    
    prev_state = complaint.status
    complaint.status = "TRIAGED_PENDING_APPROVAL"
    complaint.priority = recommendation.priority_score
    complaint.category = recommendation.suggested_category
    complaint.department = recommendation.suggested_department
    db.commit()
    db.refresh(recommendation)
    
    record_audit(
        db=db,
        case_id=complaint.id,
        actor_id=current_user.id,
        actor_role=current_user.role,
        action_type="TRIAGE_RECOMMENDED",
        details={
            "suggested_department": recommendation.suggested_department,
            "suggested_priority": recommendation.priority_score,
            "confidence": recommendation.confidence,
            "citations_count": len(recommendation.citations),
            "approval_required": True
        },
        previous_state=prev_state,
        new_state="TRIAGED_PENDING_APPROVAL"
    )
    
    return recommendation

@router.post("/{id}/approve-routing", response_model=ComplaintOut)
def approve_routing(
    id: str,
    approval: RoutingApprovalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_officer)
):
    complaint = db.query(ComplaintRecord).filter(ComplaintRecord.id == id).first()
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
        
    rec = complaint.recommendation
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot approve routing: complaint has not been triaged yet."
        )
        
    prev_state = complaint.status
    is_overridden = bool(
        (approval.approved_department and approval.approved_department != rec.suggested_department) or
        (approval.approved_priority and approval.approved_priority != rec.priority_score)
    )
    
    rec.is_approved = True
    rec.is_overridden = is_overridden
    rec.override_reason = approval.override_reason
    rec.approved_by_officer_id = current_user.id
    rec.approved_at = datetime.now(timezone.utc)
    
    if approval.approved_department:
        complaint.department = approval.approved_department
    if approval.approved_priority:
        complaint.priority = approval.approved_priority
    if approval.officer_notes:
        complaint.officer_notes = approval.officer_notes
        
    complaint.status = "ROUTED_ASSIGNED"
    complaint.assigned_officer_id = current_user.id
    db.commit()
    db.refresh(complaint)
    
    record_audit(
        db=db,
        case_id=complaint.id,
        actor_id=current_user.id,
        actor_role=current_user.role,
        action_type="ROUTING_OVERRIDDEN" if is_overridden else "ROUTING_APPROVED",
        details={
            "final_department": complaint.department,
            "final_priority": complaint.priority,
            "is_overridden": is_overridden,
            "override_reason": approval.override_reason
        },
        previous_state=prev_state,
        new_state="ROUTED_ASSIGNED"
    )
    
    return complaint

@router.post("/{id}/resolution-check", response_model=ResolutionAssessmentOut)
def check_resolution(
    id: str,
    submission: ResolutionSubmissionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_officer)
):
    complaint = db.query(ComplaintRecord).filter(ComplaintRecord.id == id).first()
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
        
    if complaint.resolution_assessment:
        db.delete(complaint.resolution_assessment)
        db.commit()
        
    complaint.resolution_summary = submission.action_taken_summary
    complaint.officer_notes = submission.completion_notes
    
    assessment = resolution_checker.evaluate_resolution(
        db=db,
        complaint=complaint,
        action_summary=submission.action_taken_summary,
        officer_notes=submission.completion_notes
    )
    db.add(assessment)
    
    prev_state = complaint.status
    if assessment.evaluation_verdict == "likely_resolved":
        complaint.status = "VERIFIED_RESOLVED"
    else:
        complaint.status = "RESOLVED_PENDING_VERIFICATION"
        
    db.commit()
    db.refresh(assessment)
    
    record_audit(
        db=db,
        case_id=complaint.id,
        actor_id=current_user.id,
        actor_role=current_user.role,
        action_type="RESOLUTION_EVALUATED",
        details={
            "verdict": assessment.evaluation_verdict,
            "confidence": assessment.confidence,
            "deterministic_checks_passed": assessment.deterministic_checks_passed,
            "contradiction_detected": assessment.contradiction_detected
        },
        previous_state=prev_state,
        new_state=complaint.status
    )
    
    return assessment
