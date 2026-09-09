import pytest
from app.services.receipt_generator import ReceiptGenerator

def test_generate_html_receipt():
    data = {
        "id": "CMP-CH-00123",
        "status": "officer_approved",
        "category": "WATER_SUPPLY",
        "department": "Chennai Metro Water",
        "sla_target_hours": 24,
        "title_en": "Broken drinking water main pipe",
        "description_redacted": "Contaminated water leaking into residential compound",
    }
    html = ReceiptGenerator.generate_html_receipt(data, merkle_root="abc123merkle456")
    assert "CMP-CH-00123" in html
    assert "GREATER CHENNAI CORPORATION" in html
    assert "புகார் எண்" in html
    assert "abc123merkle456" in html
    assert "24 Hours" in html
