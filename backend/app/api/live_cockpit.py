"""
CivicResolve Guardian - Real-Time Live Triage Cockpit WebSocket Feed
Manages active WebSocket connections for municipal war-room dashboards,
streaming live complaint arrivals, SLA countdown alerts, and officer collaborative triage.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

router = APIRouter(prefix="/ws", tags=["WebSocket Cockpit"])


class CockpitConnectionManager:
    """Manages active WebSocket connections for municipal operational control centers."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.zone_subscriptions: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, zone: str = "ALL"):
        await websocket.accept()
        self.active_connections.append(websocket)
        if zone not in self.zone_subscriptions:
            self.zone_subscriptions[zone] = []
        self.zone_subscriptions[zone].append(websocket)

    def disconnect(self, websocket: WebSocket, zone: str = "ALL"):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if zone in self.zone_subscriptions and websocket in self.zone_subscriptions[zone]:
            self.zone_subscriptions[zone].remove(websocket)

    async def broadcast_event(self, event_type: str, payload: Dict[str, Any], target_zone: str = "ALL"):
        """Broadcasts structured event JSON to listening dashboards."""
        msg = json.dumps({"event_type": event_type, "data": payload})
        targets = self.active_connections if target_zone == "ALL" else self.zone_subscriptions.get(target_zone, [])
        for conn in list(targets):
            try:
                await conn.send_text(msg)
            except Exception:
                pass


cockpit_manager = CockpitConnectionManager()


@router.websocket("/live-triage")
async def live_triage_feed(websocket: WebSocket, zone: str = "ALL"):
    await cockpit_manager.connect(websocket, zone)
    try:
        while True:
            # Keep-alive receive loop
            data = await websocket.receive_text()
            # Echo heartbeat ping/pong
            if data == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        cockpit_manager.disconnect(websocket, zone)
