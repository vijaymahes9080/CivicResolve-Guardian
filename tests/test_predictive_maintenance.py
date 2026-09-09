import pytest
from app.services.predictive_maintenance import PredictiveMaintenanceForecaster

def test_predictive_maintenance_monsoon_risk():
    complaints = [
        {"category": "ROAD_TRANSPORT"},
        {"category": "ROAD_TRANSPORT"},
        {"category": "ROAD_TRANSPORT"},
        {"category": "WATER_SUPPLY"},
    ]
    report = PredictiveMaintenanceForecaster.forecast_ward_risk("WARD-115", complaints, season="MONSOON")
    assert report["ward_id"] == "WARD-115"
    assert report["ward_status"] in ["RED_ALERT", "AMBER_WATCH"]
    top = report["assessments"][0]
    assert top["category"] == "ROAD_TRANSPORT"
    assert top["seasonal_multiplier"] == 2.5
    assert top["risk_score_pct"] > 70.0
    assert "cold-mix" in top["preventative_action"]

def test_predictive_maintenance_normal_season():
    complaints = [{"category": "STREET_LIGHTING"}]
    report = PredictiveMaintenanceForecaster.forecast_ward_risk("WARD-042", complaints, season="STANDARD")
    assert report["ward_status"] == "GREEN_NORMAL"
    assert report["assessments"][0]["risk_score_pct"] < 30.0
