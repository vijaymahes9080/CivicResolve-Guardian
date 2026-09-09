import pytest
from app.services.officer_scorecard import OfficerScorecardEngine

def test_officer_scorecard_exemplary():
    cases = [
        {"closed_within_sla": True, "resolution_veracity_passed": True, "disputed_by_citizen": False},
        {"closed_within_sla": True, "resolution_veracity_passed": True, "disputed_by_citizen": False},
        {"closed_within_sla": True, "resolution_veracity_passed": True, "disputed_by_citizen": False},
        {"closed_within_sla": False, "resolution_veracity_passed": True, "disputed_by_citizen": False},
    ]
    card = OfficerScorecardEngine.evaluate_officer("OFFICER-CHENNAI-01", "ROAD_TRANSPORT", cases)
    assert card["total_cases_handled"] == 4
    assert card["sla_compliance_pct"] == 75.0
    assert card["veracity_score_pct"] == 100.0
    assert "A" in card["performance_grade"]
    assert card["is_audit_flagged"] is False

def test_officer_scorecard_audit_flagged():
    cases = [
        {"closed_within_sla": False, "resolution_veracity_passed": False, "disputed_by_citizen": True},
        {"closed_within_sla": False, "resolution_veracity_passed": False, "disputed_by_citizen": True},
        {"closed_within_sla": True, "resolution_veracity_passed": True, "disputed_by_citizen": False},
    ]
    card = OfficerScorecardEngine.evaluate_officer("OFFICER-LAX-09", "SOLID_WASTE", cases)
    assert card["is_audit_flagged"] is True
    assert "F" in card["performance_grade"] or "C" in card["performance_grade"]
