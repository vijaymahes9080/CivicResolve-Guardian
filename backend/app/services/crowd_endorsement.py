"""
CivicResolve Guardian - Crowd Endorsement & Upvoting (+1 Me Too) Engine
Permits verified ward residents to endorse existing public grievances,
preventing duplicate ticket inflation while escalating priority based on community demand.
"""

from typing import Dict, Any, Set


class CrowdEndorsementManager:
    """Manages community upvoting and dynamic priority escalation."""

    def __init__(self):
        # complaint_id -> set of hashed citizen IDs
        self._endorsements: Dict[str, Set[str]] = {}

    def endorse_complaint(self, complaint_id: str, citizen_id_hash: str) -> Dict[str, Any]:
        if complaint_id not in self._endorsements:
            self._endorsements[complaint_id] = set()

        already_voted = citizen_id_hash in self._endorsements[complaint_id]
        if not already_voted:
            self._endorsements[complaint_id].add(citizen_id_hash)

        total_votes = len(self._endorsements[complaint_id])
        escalation = self.calculate_priority_boost(total_votes)

        return {
            "complaint_id": complaint_id,
            "total_endorsements": total_votes,
            "already_voted": already_voted,
            "dynamic_priority_boost": escalation["boosted_priority"],
            "sla_hours_reduction": escalation["sla_reduction_hours"],
            "community_urgency_tier": escalation["tier"],
        }

    def get_endorsement_count(self, complaint_id: str) -> int:
        return len(self._endorsements.get(complaint_id, set()))

    @staticmethod
    def calculate_priority_boost(endorsement_count: int) -> Dict[str, Any]:
        if endorsement_count >= 20:
            return {"boosted_priority": "CRITICAL", "sla_reduction_hours": 18, "tier": "MAJOR_COMMUNITY_CRISIS"}
        elif endorsement_count >= 10:
            return {"boosted_priority": "HIGH", "sla_reduction_hours": 12, "tier": "HIGH_NEIGHBORHOOD_IMPACT"}
        elif endorsement_count >= 5:
            return {"boosted_priority": "MEDIUM", "sla_reduction_hours": 6, "tier": "MODERATE_INTEREST"}
        else:
            return {"boosted_priority": "STANDARD", "sla_reduction_hours": 0, "tier": "INDIVIDUAL_SUBMISSION"}
