import pytest
from app.services.policy_conflicts import PolicyConflictDetector

def test_policy_conflict_excavation_deadlock():
    text = "Water pipeline burst requires immediate excavation and road cut on 100 feet road"
    result = PolicyConflictDetector.analyze_complaint_conflict(text, "WATER_SUPPLY")
    assert result["has_jurisdiction_conflict"] is True
    assert result["requires_joint_noc"] is True
    conflict = result["conflicts"][0]
    assert conflict["conflict_type"] == "EXCAVATION_RESTORATION_DEADLOCK"
    assert conflict["secondary_department"] == "ROAD_TRANSPORT"
    assert "road cut" in conflict["matched_triggers"]

def test_policy_conflict_none():
    text = "Street light bulb is fused"
    result = PolicyConflictDetector.analyze_complaint_conflict(text, "STREET_LIGHTING")
    assert result["has_jurisdiction_conflict"] is False
    assert len(result["conflicts"]) == 0
