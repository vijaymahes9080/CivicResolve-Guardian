import pytest
from app.services.bot_simulator import WhatsAppChatbotSession

def test_whatsapp_bot_flow_english():
    session = WhatsAppChatbotSession("9840123456", lang="en")
    # Step 1: Greeting
    r1 = session.process_message("Hi")
    assert "Welcome to Greater Chennai Corporation" in r1["reply"]
    assert r1["state"] == "AWAIT_DESCRIPTION"

    # Step 2: Description with phone PII
    r2 = session.process_message("Drainage water overflowing near my house. Call 9876543210")
    assert "Ward Number" in r2["reply"]
    assert r2["state"] == "AWAIT_WARD"
    assert "[PHONE_REDACTED]" in session.collected_data["description"]

    # Step 3: Ward
    r3 = session.process_message("Ward 174, Adyar")
    assert r3["completed"] is True
    assert "WA-" in r3["ticket_id"]
    assert "Ticket: #" in r3["reply"]

def test_whatsapp_bot_flow_tamil():
    session = WhatsAppChatbotSession("9840123456", lang="ta")
    r1 = session.process_message("வணக்கம்")
    assert "குறைதீர்ப்பு" in r1["reply"]

    r2 = session.process_message("தெருவிளக்கு எரியவில்லை")
    assert "வார்டு எண்" in r2["reply"]

    r3 = session.process_message("வார்டு 115")
    assert r3["completed"] is True
    assert "நன்றி!" in r3["reply"]
