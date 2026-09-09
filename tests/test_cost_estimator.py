import pytest
from app.services.cost_estimator import MunicipalCostEstimator

def test_cost_estimator_water_supply():
    est = MunicipalCostEstimator.estimate_repair("WATER_SUPPLY", "high")
    assert est["category"] == "WATER_SUPPLY"
    assert est["priority"] == "high"
    assert "Super Sucker Jetting Machine" in est["equipment_assigned"]
    assert est["estimated_duration_hours"] > 6.0
    assert est["cost_breakdown"]["total_estimated_inr"] > 10000
    assert "INR" in est["cost_breakdown"]["currency"]

def test_cost_estimator_critical_escalation():
    est = MunicipalCostEstimator.estimate_repair("ROAD_TRANSPORT", "critical")
    assert est["priority"] == "critical"
    assert est["financial_approval_authority"] == "Assistant Executive Engineer (AEE)"
    assert est["cost_breakdown"]["total_estimated_inr"] > 25000
