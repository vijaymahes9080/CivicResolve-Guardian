import pytest
from app.services.whistleblower import WhistleblowerVault

def test_whistleblower_submission():
    text = "Contractor dumping untreated chemical sludge into Velachery lake at 2 AM"
    res = WhistleblowerVault.create_whistleblower_submission(text, "WARD-178")
    assert res["is_whistleblower"] is True
    assert res["case_access_key"].startswith("CRG-ANON-")
    assert len(res["nullifier_hash"]) == 64
    assert res["ward_id"] == "WARD-178"
    assert res["pii_purged"] is True

def test_whistleblower_nullifier_verification():
    secret = "f8a9b2c3d4e5f607"
    ward_id = "WARD-100"
    nullifier = WhistleblowerVault.create_whistleblower_submission("Secret info", ward_id)["nullifier_hash"]
    # Corrupt or wrong secret fails
    assert WhistleblowerVault.verify_nullifier("wrong_secret", ward_id, nullifier) is False
