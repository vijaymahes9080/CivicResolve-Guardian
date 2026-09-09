import pytest
from app.services.gis_clustering import haversine_distance_meters, detect_spatial_clusters

def test_haversine_distance():
    # Chennai Ripon Building to Central Station ~ 1.1 km
    lat1, lon1 = 13.0827, 80.2707
    lat2, lon2 = 13.0837, 80.2755
    dist = haversine_distance_meters(lat1, lon1, lat2, lon2)
    assert 400 < dist < 800

def test_detect_spatial_clusters():
    # 3 water complaints near T. Nagar (within 150m) and 1 distant complaint in Anna Nagar
    complaints = [
        {"id": "CMP-1", "category": "WATER_SUPPLY", "lat": 13.0418, "lon": 80.2337},
        {"id": "CMP-2", "category": "WATER_SUPPLY", "lat": 13.0422, "lon": 80.2340},
        {"id": "CMP-3", "category": "WATER_SUPPLY", "lat": 13.0415, "lon": 80.2335},
        {"id": "CMP-4", "category": "WATER_SUPPLY", "lat": 13.0850, "lon": 80.2100}, # Far away
        {"id": "CMP-5", "category": "ROAD_TRANSPORT", "lat": 13.0418, "lon": 80.2337}, # Different category
    ]

    clusters = detect_spatial_clusters(complaints, epsilon_meters=300.0, min_samples=2)
    assert len(clusters) == 1
    c = clusters[0]
    assert c["category"] == "WATER_SUPPLY"
    assert c["incident_count"] == 3
    assert set(c["complaint_ids"]) == {"CMP-1", "CMP-2", "CMP-3"}
    assert c["radius_meters"] < 200
    assert "WATER_SUPPLY" in c["cluster_id"]
