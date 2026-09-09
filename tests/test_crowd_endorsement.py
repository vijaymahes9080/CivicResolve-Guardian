import pytest
from app.services.crowd_endorsement import CrowdEndorsementManager

def test_crowd_endorsement_lifecycle():
    mgr = CrowdEndorsementManager()

    # Citizen 1 endorses
    res1 = mgr.endorse_complaint("CMP-ROAD-99", "citizen_hash_1")
    assert res1["total_endorsements"] == 1
    assert res1["already_voted"] is False
    assert res1["dynamic_priority_boost"] == "STANDARD"

    # Citizen 1 attempts duplicate endorsement
    res_dup = mgr.endorse_complaint("CMP-ROAD-99", "citizen_hash_1")
    assert res_dup["already_voted"] is True
    assert res_dup["total_endorsements"] == 1

    # Simulate 10 community members endorsing
    for i in range(2, 12):
        mgr.endorse_complaint("CMP-ROAD-99", f"citizen_hash_{i}")

    assert mgr.get_endorsement_count("CMP-ROAD-99") == 11
    boost = mgr.calculate_priority_boost(11)
    assert boost["boosted_priority"] == "HIGH"
    assert boost["sla_reduction_hours"] == 12
