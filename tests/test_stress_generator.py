import pytest
from backend.scripts.generate_stress_data import generate_synthetic_record, generate_batch

def test_generate_synthetic_record():
    rec = generate_synthetic_record(42)
    assert rec["id"] == "STRESS-000042"
    assert rec["category"] in ["WATER_SUPPLY", "ROAD_TRANSPORT", "SOLID_WASTE", "STREET_LIGHTING", "PUBLIC_HEALTH"]
    assert 12.90 <= rec["latitude"] <= 13.20
    assert 80.10 <= rec["longitude"] <= 80.35
    assert rec["language"] in ["en", "ta"]

def test_generate_batch_scale():
    batch = generate_batch(200)
    assert len(batch) == 200
    wards = set(b["ward_id"] for b in batch)
    assert len(wards) > 10
