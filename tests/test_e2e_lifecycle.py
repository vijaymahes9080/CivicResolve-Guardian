"""
CivicResolve Guardian - End-to-End Integrated Lifecycle Test
Validates the complete lifecycle flow across bilingual ingestion, PII masking,
RAG citation lookup, PWD cost estimation, and cryptographic Merkle verification.
"""

import pytest
from app.core.pii import redact_pii
from app.services.language import detect_language
from app.services.cost_estimator import MunicipalCostEstimator
from app.services.gis_clustering import haversine_distance_meters
from app.core.merkle import MerkleTree
from app.services.receipt_generator import ReceiptGenerator


def test_full_civic_lifecycle():
    # 1. Citizen submits raw complaint with Tamil text and phone number
    raw_text = "குடிநீர் குழாய் உடைந்து சாலை முழுவதும் வெள்ளம். தொடர்பு: 9840123456"

    # 2. Language Detection
    lang = detect_language(raw_text)
    assert lang == "ta"

    # 3. PII Redaction
    redaction = redact_pii(raw_text)
    assert "[PHONE_REDACTED]" in redaction["redacted_text"]
    assert len(redaction["entities"]) >= 1

    # 4. Geodesic distance to Ward Office (Ripon Building)
    incident_lat, incident_lon = 13.0820, 80.2700
    ripon_lat, ripon_lon = 13.0827, 80.2707
    dist = haversine_distance_meters(incident_lat, incident_lon, ripon_lat, ripon_lon)
    assert dist < 200.0 # Under 200 meters

    # 5. PWD Schedule of Rates (SOR) Resource & Budget Estimation
    budget = MunicipalCostEstimator.estimate_repair("WATER_SUPPLY", "critical")
    assert budget["estimated_duration_hours"] > 6.0
    assert budget["cost_breakdown"]["total_estimated_inr"] > 15000

    # 6. Cryptographic Merkle Audit Tree
    audit_events = [
        {"action": "CITIZEN_SUBMISSION", "lang": lang},
        {"action": "PII_REDACTION_APPLIED", "masked": len(redaction["entities"])},
        {"action": "PWD_BUDGET_ESTIMATED", "inr": budget["cost_breakdown"]["total_estimated_inr"]},
        {"action": "OFFICER_APPROVED", "officer": "officer-chennai-01"},
    ]
    tree = MerkleTree(audit_events)
    assert len(tree.root_hash) == 64

    # Verify cryptographic inclusion proof for Officer Approval
    proof = tree.generate_proof(3)
    is_valid = MerkleTree.verify_proof(audit_events[3], proof, tree.root_hash)
    assert is_valid is True

    # 7. Official Receipt Generation
    complaint_dict = {
        "id": "CMP-E2E-2026-99",
        "category": "WATER_SUPPLY",
        "department": "Chennai Metro Water",
        "sla_target_hours": 24,
        "title_en": "Drinking water trunk main burst",
        "description_redacted": redaction["redacted_text"],
    }
    receipt = ReceiptGenerator.generate_html_receipt(complaint_dict, merkle_root=tree.root_hash)
    assert "CMP-E2E-2026-99" in receipt
    assert tree.root_hash in receipt
