import pytest
from app.services.notifications import NotificationDispatcher

def test_notification_dispatcher_sms_english():
    res = NotificationDispatcher.dispatch_alert(
        channel="SMS",
        recipient="9840123456",
        template_key="COMPLAINT_RECEIVED",
        lang="en",
        context={"id": "CMP-101", "category": "Water Leakage", "link": "https://civicresolve.gov.in/track/CMP-101"},
    )
    assert res["status"] == "DELIVERED_SIMULATED"
    assert "CMP-101" in res["message_body"]
    assert res["recipient_masked"] == "984******56"
    assert res["channel"] == "SMS"

def test_notification_dispatcher_whatsapp_tamil():
    res = NotificationDispatcher.dispatch_alert(
        channel="WHATSAPP",
        recipient="+919876543210",
        template_key="OFFICER_APPROVED",
        lang="ta",
        context={"id": "CMP-202", "dept": "குடிநீர் வழங்கல்", "sla": 24},
    )
    assert "ஒப்புதல்" in res["message_body"]
    assert res["language"] == "ta"
    assert res["channel"] == "WHATSAPP"
