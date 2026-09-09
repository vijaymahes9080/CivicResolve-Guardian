import pytest
from app.services.image_forensics import ImageForensicsAnalyzer

def test_image_forensics_valid_geotag():
    dummy_bytes = b"GIF89a" + b"\x00" * 1024
    exif = {
        "latitude": 13.0827,
        "longitude": 80.2707,
        "software": "Apple iPhone 14",
    }
    result = ImageForensicsAnalyzer.analyze_evidence(
        image_bytes=dummy_bytes,
        claimed_lat=13.0830,
        claimed_lon=80.2710,
        category="ROAD_TRANSPORT",
        exif_metadata=exif,
    )
    assert result["is_valid"] is True
    assert result["geotag_verified"] is True
    assert result["veracity_score"] >= 0.85
    assert result["recommendation"] == "ACCEPT"

def test_image_forensics_geotag_mismatch():
    dummy_bytes = b"BM" + b"\xFF" * 1024
    exif = {
        "latitude": 12.9716, # Bangalore coordinates
        "longitude": 77.5946,
    }
    # Claimed location is Chennai
    result = ImageForensicsAnalyzer.analyze_evidence(
        image_bytes=dummy_bytes,
        claimed_lat=13.0827,
        claimed_lon=80.2707,
        category="WATER_SUPPLY",
        exif_metadata=exif,
    )
    assert any("GEOTAG_MISMATCH" in f for f in result["flags"])
    assert result["geotag_verified"] is False
    assert result["veracity_score"] < 0.70

def test_image_forensics_photoshop_detection():
    dummy_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 500
    exif = {
        "software": "Adobe Photoshop 2024",
    }
    result = ImageForensicsAnalyzer.analyze_evidence(
        image_bytes=dummy_bytes,
        claimed_lat=13.0,
        claimed_lon=80.0,
        category="SOLID_WASTE",
        exif_metadata=exif,
    )
    assert any("SYNTHETIC_OR_EDITED" in f for f in result["flags"])
    assert result["recommendation"] == "FLAG_FOR_OFFICER_REVIEW"
