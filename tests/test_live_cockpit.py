import pytest
from app.api.live_cockpit import CockpitConnectionManager

@pytest.mark.asyncio
async def test_cockpit_manager_connection():
    class DummyWebSocket:
        def __init__(self):
            self.accepted = False
            self.sent_messages = []

        async def accept(self):
            self.accepted = True

        async def send_text(self, text: str):
            self.sent_messages.append(text)

    mgr = CockpitConnectionManager()
    ws = DummyWebSocket()

    await mgr.connect(ws, zone="ZONE-05")
    assert ws.accepted is True
    assert ws in mgr.active_connections
    assert ws in mgr.zone_subscriptions["ZONE-05"]

    # Broadcast event
    await mgr.broadcast_event("NEW_CRITICAL_COMPLAINT", {"id": "CMP-999"}, target_zone="ZONE-05")
    assert len(ws.sent_messages) == 1
    assert "CMP-999" in ws.sent_messages[0]

    mgr.disconnect(ws, zone="ZONE-05")
    assert ws not in mgr.active_connections
