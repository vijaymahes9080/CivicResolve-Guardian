import pytest
from app.core.pii import pii_engine

def test_english_phone_and_aadhaar_redaction():
    raw_text = "My name is Ramesh. Call me at 9840123456 or alternate +91 9789012345. My Aadhaar is 2345 6789 0123."
    redacted, audit = pii_engine.redact(raw_text)
    
    assert "[PHONE_REDACTED]" in redacted
    assert "9840123456" not in redacted
    assert "9789012345" not in redacted
    assert "[AADHAAR_REDACTED]" in redacted
    assert "2345 6789 0123" not in redacted
    assert "[NAME_REDACTED]" in redacted
    assert len(audit) >= 3

def test_tamil_phone_and_door_address_redaction():
    raw_text = "கதவு எண் 14/A, பாரதி தெரு. குடிநீர் வரவில்லை. தொடர்பு எண் 9840199999."
    redacted, audit = pii_engine.redact(raw_text)
    
    assert "[PHONE_REDACTED]" in redacted
    assert "9840199999" not in redacted
    assert "[DOOR_ADDRESS_REDACTED]" in redacted
    assert "14/A" not in redacted
    assert "பாரதி தெரு" in redacted  # General street should be preserved

def test_email_redaction():
    raw_text = "Please update me at citizen.help@gmail.com regarding the open drain."
    redacted, audit = pii_engine.redact(raw_text)
    
    assert "[EMAIL_REDACTED]" in redacted
    assert "citizen.help@gmail.com" not in redacted
