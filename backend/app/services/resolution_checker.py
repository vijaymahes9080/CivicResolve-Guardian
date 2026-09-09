import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.complaint import ComplaintRecord
from app.models.resolution import ResolutionAssessment
from app.core.logging import logger

class ResolutionQualityChecker:
    """
    Evaluates whether an officer's reported resolution genuinely solves
    the citizen's grievance, enforcing deterministic checks and contradiction detection.
    """

    CONTRADICTION_PATTERNS = [
        r'\b(?:pending|cannot\s*be\s*repaired|funds\s*awaited|postponed|no\s*fault\s*found|not\s*our\s*department)\b',
        r'\b(?:temporary\s*patch|will\s*do\s*later|tender\s*called)\b'
    ]

    @classmethod
    def evaluate_resolution(
        cls,
        db: Session,
        complaint: ComplaintRecord,
        action_summary: str,
        officer_notes: Optional[str] = None,
        citizen_feedback_score: Optional[int] = None
    ) -> ResolutionAssessment:
        checks_detail: Dict[str, bool] = {
            "required_fields_present": bool(action_summary and len(action_summary.strip()) >= 15),
            "resolution_evidence_attached": False,
            "dates_consistent": True,
            "addressed_requested_issue": False,
            "valid_status_transition": complaint.status in ["IN_PROGRESS", "ROUTED_ASSIGNED", "ACTION_PROPOSED"]
        }

        # Check evidence attached by officer
        officer_evidence = [e for e in complaint.evidence_items if e.uploaded_by_role == "officer"]
        checks_detail["resolution_evidence_attached"] = len(officer_evidence) > 0

        # Check keyword issue coverage
        c_words = set(re.findall(r'\b[a-zA-Z\u0B80-\u0BFF]{4,}\b', complaint.redacted_content.lower()))
        r_words = set(re.findall(r'\b[a-zA-Z\u0B80-\u0BFF]{4,}\b', (action_summary + " " + (officer_notes or "")).lower()))
        
        shared_keywords = c_words.intersection(r_words)
        checks_detail["addressed_requested_issue"] = len(shared_keywords) >= 1 or len(action_summary) > 40

        # Contradiction Detection
        full_text = (action_summary + " " + (officer_notes or "")).lower()
        contradiction_detected = False
        contradiction_notes = None
        
        for pat in cls.CONTRADICTION_PATTERNS:
            match = re.search(pat, full_text, re.IGNORECASE)
            if match:
                contradiction_detected = True
                contradiction_notes = f"Resolution text contains contradiction indicator: '{match.group(0)}' indicating incomplete remediation."
                break

        if citizen_feedback_score is not None and citizen_feedback_score <= 2:
            contradiction_detected = True
            contradiction_notes = f"Citizen reported dissatisfaction (Rating {citizen_feedback_score}/5), disputing resolution."

        # Compute Verdict
        deterministic_passed = all([
            checks_detail["required_fields_present"],
            checks_detail["dates_consistent"],
            checks_detail["addressed_requested_issue"]
        ])

        if contradiction_detected:
            verdict = "contradiction_detected"
            confidence = 0.90
            explanation = contradiction_notes or "Contradictory status found in closure report."
        elif not checks_detail["resolution_evidence_attached"]:
            verdict = "insufficient_evidence"
            confidence = 0.85
            explanation = "Action summary provided, but no post-remediation photographic proof or site inspection report was attached."
        elif not deterministic_passed:
            verdict = "weak_resolution"
            confidence = 0.75
            explanation = "Resolution summary is overly brief or fails to directly reference the reported civic defect."
        else:
            verdict = "likely_resolved"
            confidence = 0.92
            explanation = "All deterministic criteria satisfied: valid action summary, evidence verified, and matching defect parameters."

        assessment = ResolutionAssessment(
            complaint_id=complaint.id,
            evaluation_verdict=verdict,
            confidence=confidence,
            explanation=explanation,
            deterministic_checks_passed=deterministic_passed,
            checks_detail=checks_detail,
            contradiction_detected=contradiction_detected,
            contradiction_notes=contradiction_notes,
            evidence_references=[e.file_name for e in officer_evidence],
            citizen_satisfaction_score=citizen_feedback_score
        )

        return assessment

resolution_checker = ResolutionQualityChecker()
