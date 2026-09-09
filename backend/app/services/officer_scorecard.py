"""
CivicResolve Guardian - Officer Performance & SLA Velocity Scorecard
Computes departmental accountability rankings, resolution veracity adherence %,
and identifies governance bottlenecks or premature closure tendencies across municipal zones.
"""

from typing import List, Dict, Any


class OfficerScorecardEngine:
    """Computes municipal officer productivity, integrity, and SLA compliance metrics."""

    @classmethod
    def evaluate_officer(
        cls,
        officer_id: str,
        department: str,
        cases: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        if not cases:
            return {
                "officer_id": officer_id,
                "department": department,
                "total_cases": 0,
                "sla_compliance_pct": 100.0,
                "veracity_score_pct": 100.0,
                "performance_grade": "NOT_ENOUGH_DATA",
            }

        total = len(cases)
        on_time_count = sum(1 for c in cases if c.get("closed_within_sla", True))
        passed_veracity_count = sum(1 for c in cases if c.get("resolution_veracity_passed", True))
        reopened_disputes = sum(1 for c in cases if c.get("disputed_by_citizen", False))

        sla_compliance_pct = round((on_time_count / total) * 100.0, 1)
        # Veracity penalty for disputed or fraudulent closures
        veracity_score_pct = round(((passed_veracity_count - (reopened_disputes * 1.5)) / total) * 100.0, 1)
        veracity_score_pct = max(0.0, min(100.0, veracity_score_pct))

        composite_score = round((sla_compliance_pct * 0.45) + (veracity_score_pct * 0.55), 1)

        if composite_score >= 90.0:
            grade = "A+ (EXEMPLARY_SERVICE)"
        elif composite_score >= 80.0:
            grade = "A (COMMENDABLE)"
        elif composite_score >= 65.0:
            grade = "B (STANDARD_COMPLIANT)"
        elif composite_score >= 50.0:
            grade = "C (NEEDS_OVERSIGHT)"
        else:
            grade = "F (CRITICAL_AUDIT_RECOMMENDED)"

        return {
            "officer_id": officer_id,
            "department": department,
            "total_cases_handled": total,
            "sla_compliance_pct": sla_compliance_pct,
            "veracity_score_pct": veracity_score_pct,
            "reopened_disputes": reopened_disputes,
            "composite_score": composite_score,
            "performance_grade": grade,
            "is_audit_flagged": grade.startswith("F") or veracity_score_pct < 60.0,
        }
