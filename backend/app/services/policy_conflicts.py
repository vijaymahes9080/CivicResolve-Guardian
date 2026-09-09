"""
CivicResolve Guardian - Municipal Policy Conflict & Jurisdiction Overlap Detector
Identifies jurisdictional deadlocks between municipal departments
(e.g., Metro Water underground pipe excavation vs PWD / Corporation road cutting moratoriums).
"""

from typing import List, Dict, Any


CONFLICT_RULES = [
    {
        "departments": {"WATER_SUPPLY", "ROAD_TRANSPORT"},
        "trigger_terms": ["road cut", "trench", "excavation", "pipeline repair", "digging"],
        "conflict_type": "EXCAVATION_RESTORATION_DEADLOCK",
        "description": "Conflict between Metro Water underground pipeline excavation and Highway road surface restoration charter.",
        "resolution_protocol": "Joint Inspection & Unified Road Restoration NOC mandated. Water board deposits road restoration fee prior to backfilling.",
        "arbitration_authority": "Chief Engineer (General) & Zonal Joint Commissioner",
    },
    {
        "departments": {"STREET_LIGHTING", "ROAD_TRANSPORT"},
        "trigger_terms": ["median", "pole relocation", "widening", "junction improvement"],
        "conflict_type": "POLE_RELOCATION_VS_WIDENING",
        "description": "Street lighting poles obstruct road widening project.",
        "resolution_protocol": "Electrical wing coordinates with PWD for concurrent underground cable ducting and mast relocation.",
        "arbitration_authority": "Superintending Engineer (Electrical & Roads)",
    },
    {
        "departments": {"SOLID_WASTE", "PUBLIC_HEALTH"},
        "trigger_terms": ["dumping ground", "biomedical", "hazard", "leachate", "stagnant water"],
        "conflict_type": "HEALTH_HAZARD_WASTE_DISPUTE",
        "description": "Unattended municipal solid waste heap transforming into an active vector breeding and epidemic hazard.",
        "resolution_protocol": "Emergency dual-dispatch: Solid waste clears within 6 hours, followed immediately by health department larvicide fumigation.",
        "arbitration_authority": "City Health Officer & Chief Engineer (SWM)",
    },
]


class PolicyConflictDetector:
    """Detects and resolves inter-departmental jurisdiction collisions."""

    @classmethod
    def analyze_complaint_conflict(cls, text: str, primary_category: str) -> Dict[str, Any]:
        text_lower = text.lower()
        detected_conflicts: List[Dict[str, Any]] = []

        for rule in CONFLICT_RULES:
            if primary_category.upper() in rule["departments"]:
                matching_terms = [term for term in rule["trigger_terms"] if term in text_lower]
                if matching_terms:
                    # Found an inter-departmental jurisdiction overlap
                    secondary_dept = list(rule["departments"] - {primary_category.upper()})[0]
                    detected_conflicts.append({
                        "conflict_type": rule["conflict_type"],
                        "primary_department": primary_category.upper(),
                        "secondary_department": secondary_dept,
                        "matched_triggers": matching_terms,
                        "description": rule["description"],
                        "resolution_protocol": rule["resolution_protocol"],
                        "arbitration_authority": rule["arbitration_authority"],
                    })

        has_conflict = len(detected_conflicts) > 0

        return {
            "has_jurisdiction_conflict": has_conflict,
            "total_conflicts": len(detected_conflicts),
            "conflicts": detected_conflicts,
            "requires_joint_noc": has_conflict,
            "coordinating_officer_required": has_conflict,
        }
