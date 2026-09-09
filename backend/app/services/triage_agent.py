import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.complaint import ComplaintRecord
from app.models.triage import RoutingRecommendation
from app.services.rag import rag_engine
from app.services.language import LanguageDetector
from app.core.config import settings
from app.core.logging import logger

class BoundedTriageAgent:
    """
    Deterministic Bounded Triage State Machine.
    Produces safe, policy-grounded recommendations without allowing
    unconstrained or unsafe autonomous actions.
    """
    
    DEPARTMENTS = {
        "WATER": "Water Supply & Sewerage Board",
        "WASTE": "Solid Waste Management",
        "ROAD": "Roads & Bridges",
        "LIGHT": "Electrical & Street Lighting",
        "HEALTH": "Public Health & Sanitation"
    }

    # Department category rule mapping
    RULE_PATTERNS = {
        "WATER": [
            r'\b(?:water|pipe|pipeline|leak|leakage|burst|drinking|tanker|tap|sewage|sewer|manhole|kudineer|thanni|kaalvai)\b',
            r'குடிநீர்|குழாய்|கழிவுநீர்|தண்ணீர்|சாக்கடை'
        ],
        "WASTE": [
            r'\b(?:garbage|trash|waste|rubbish|dump|dumping|bin|debris|litter|kuppai|sanitary)\b',
            r'குப்பை|கழிவு|சாக்கடை|தூய்மை'
        ],
        "ROAD": [
            r'\b(?:road|pothole|crater|tar|bitumen|footpath|pavement|bridge|divider|saalai|kuzhi)\b',
            r'சாலை|பள்ளம்|ரோடு|நடைபாதை'
        ],
        "LIGHT": [
            r'\b(?:street\s*light|lamp|pole|darkness|dark\s*stretch|wire|live\s*wire|voltage|electric|shock|vilakku)\b',
            r'தெரு\s*விளக்கு|மின்சாரம்|மின்\s*கம்பி'
        ],
        "HEALTH": [
            r'\b(?:mosquito|dengue|malaria|stagnant|fogging|larvae|food\s*stall|unhygienic|infection|fever)\b',
            r'கொசு|டெங்கு|காய்ச்சல்|சுகாதாரம்'
        ]
    }

    CRITICAL_TRIGGERS = [
        r'\b(?:contamination|poison|live\s*(?:electric\s*)?wire|hanging\s*(?:electric\s*)?wire|electric\s*shock|open\s*manhole|death|fatal|collapsed|dengue\s*outbreak|fire|cylinder)\b',
        r'விஷம்|உயிர்\s*ஆபத்து|மின்\s*தாக்கம்|விபத்து|உடைந்த'
    ]

    HIGH_TRIGGERS = [
        r'\b(?:burst|overflowing|flooding|urgent|school|hospital|major\s*traffic|arterial|3\s*days|four\s*days)\b',
        r'பள்ளி|மருத்துவமனை|வெள்ளம்|அவசரம்'
    ]

    @classmethod
    def evaluate_complaint(cls, db: Session, complaint: ComplaintRecord) -> RoutingRecommendation:
        text = complaint.redacted_content.lower()
        lang = complaint.original_language or LanguageDetector.detect(complaint.redacted_content)
        
        # 1. Department & Category Classification
        dept_scores = {k: 0 for k in cls.DEPARTMENTS}
        for dept_key, patterns in cls.RULE_PATTERNS.items():
            for pat in patterns:
                matches = len(re.findall(pat, text, re.IGNORECASE))
                dept_scores[dept_key] += matches * 2

        # RAG Search for Policy Grounding
        citations = rag_engine.search_policy(db, query=complaint.redacted_content, top_k=2)
        for cit in citations:
            pid = cit["policy_id"].upper()
            for dept_key in cls.DEPARTMENTS:
                if dept_key in pid:
                    dept_scores[dept_key] += 3

        best_dept_key = max(dept_scores, key=dept_scores.get)
        if dept_scores[best_dept_key] == 0:
            suggested_department = "General Public Grievance Cell"
            suggested_category = "General Municipal Inquiries"
            confidence = 0.40
        else:
            suggested_department = cls.DEPARTMENTS[best_dept_key]
            category_names = {
                "WATER": "Drinking Water & Sewerage Network",
                "WASTE": "Solid Waste Clearance & Sanitation",
                "ROAD": "Road Surface & Infrastructure Repair",
                "LIGHT": "Street Lighting & Electrical Safety",
                "HEALTH": "Vector Control & Disease Prevention"
            }
            suggested_category = category_names.get(best_dept_key, "General Infrastructure")
            confidence = min(0.95, round(0.55 + (dept_scores[best_dept_key] * 0.08), 2))

        # 2. Priority Scoring
        priority = "MEDIUM"
        is_critical = any(re.search(pat, text, re.IGNORECASE) for pat in cls.CRITICAL_TRIGGERS)
        is_high = any(re.search(pat, text, re.IGNORECASE) for pat in cls.HIGH_TRIGGERS)
        
        if is_critical:
            priority = "CRITICAL"
        elif is_high or dept_scores[best_dept_key] >= 6:
            priority = "HIGH"
        elif dept_scores[best_dept_key] <= 1:
            priority = "LOW"

        # 3. Duplicate Detection within Ward
        duplicate_candidates = []
        if complaint.ward:
            other_complaints = db.query(ComplaintRecord).filter(
                ComplaintRecord.id != complaint.id,
                ComplaintRecord.ward == complaint.ward,
                ComplaintRecord.status.in_(["SUBMITTED", "TRIAGED_PENDING_APPROVAL", "ROUTED_ASSIGNED", "IN_PROGRESS"])
            ).all()
            
            q_words = set(re.findall(r'\b\w{4,}\b', text))
            for other in other_complaints:
                o_words = set(re.findall(r'\b\w{4,}\b', other.redacted_content.lower()))
                if q_words and o_words:
                    sim = len(q_words.intersection(o_words)) / len(q_words.union(o_words))
                    if sim >= settings.DUPLICATE_SIMILARITY_THRESHOLD:
                        duplicate_candidates.append({
                            "complaint_id": other.id,
                            "similarity_score": round(sim, 2),
                            "status": other.status
                        })

        # 4. Missing Evidence Checks
        missing_evidence = []
        has_landmark = bool(re.search(r'\b(?:near|opposite|behind|street|road|ward|cross|junction|அருகில்|எதிரில்|தெரு)\b', text, re.IGNORECASE))
        if not has_landmark:
            missing_evidence.append("Specific geographic landmark or street junction name")
            
        evidence_count = len(complaint.evidence_items)
        if best_dept_key in ["ROAD", "WATER", "LIGHT"] and evidence_count == 0:
            missing_evidence.append("Photographic evidence of the defect or hazardous site")

        # 5. Policy Reasons
        reasons = [
            f"Classified under '{suggested_department}' based on key defect indicators.",
            f"Assigned priority '{priority}' evaluating public safety hazards and civic SLA requirements."
        ]
        if duplicate_candidates:
            reasons.append(f"Identified {len(duplicate_candidates)} possible duplicate grievance(s) active in Ward {complaint.ward}.")
        if not citations:
            reasons.append("Notice: No direct municipal policy citation met threshold; manual officer verification required.")

        # 6. Draft Polite Citizen Update
        if lang == "ta":
            draft_resp = (
                f"வணக்கம். உங்கள் புகார் '{suggested_department}' துறைக்கு "
                f"பரிந்துரைக்கப்பட்டுள்ளது. எங்கள் அதிகாரி விரைவில் இதை சரிபார்த்து நடவடிக்கை எடுப்பார். "
                f"முன்னுரிமை: {priority}."
            )
        else:
            draft_resp = (
                f"Dear Citizen, your grievance has been triaged for '{suggested_department}' "
                f"with priority '{priority}'. An authorized officer will verify the routing and initiate field action."
            )

        recommendation = RoutingRecommendation(
            complaint_id=complaint.id,
            suggested_category=suggested_category,
            suggested_department=suggested_department,
            priority_score=priority,
            confidence=confidence,
            reasons=reasons,
            citations=citations,
            duplicate_candidates=duplicate_candidates,
            missing_evidence=missing_evidence,
            draft_citizen_response=draft_resp,
            approval_required=True
        )
        
        return recommendation

triage_agent = BoundedTriageAgent()
