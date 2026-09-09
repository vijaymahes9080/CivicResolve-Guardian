"""
CivicResolve Guardian - IoT Sensor & Drone Telemetry Ingestion Pipeline
Ingests real-time civic sensor streams (flood ultrasonic gauges, smart bin fill level,
lux street lighting sensors, and air quality telemetry), converting critical thresholds into automated tickets.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone


class IoTTriageConverter:
    """Converts raw IoT telemetry alarm payloads into grounded civic grievance records."""

    THRESHOLDS = {
        "FLOOD_LEVEL_CM": {"critical": 85.0, "category": "WATER_SUPPLY", "title_en": "Automated Sensor: Stormwater Drain Overflow Alert"},
        "BIN_FILL_PCT": {"critical": 90.0, "category": "SOLID_WASTE", "title_en": "Automated Sensor: Public Bin Capacity Exceeded (>90%)"},
        "LIGHT_LUX_LEVEL": {"critical": 5.0, "category": "STREET_LIGHTING", "title_en": "Automated Sensor: Grid Light Luminaire Power Failure"},
        "AIR_PM25": {"critical": 250.0, "category": "PUBLIC_HEALTH", "title_en": "Automated Sensor: Hazardous PM2.5 Ambient Air Spike"},
    }

    @classmethod
    def process_sensor_event(
        cls,
        device_id: str,
        sensor_type: str,
        reading_value: float,
        ward_id: str,
        lat: float,
        lon: float,
        battery_pct: Optional[float] = 95.0,
    ) -> Dict[str, Any]:
        cfg = cls.THRESHOLDS.get(sensor_type.upper())
        if not cfg:
            return {"triggered": False, "reason": f"Unknown sensor type {sensor_type}"}

        is_breached = False
        if sensor_type == "LIGHT_LUX_LEVEL":
            is_breached = reading_value < cfg["critical"]
        else:
            is_breached = reading_value >= cfg["critical"]

        if not is_breached:
            return {
                "triggered": False,
                "device_id": device_id,
                "status": "NORMAL",
                "reading_value": reading_value,
            }

        ticket_payload = {
            "title_en": cfg["title_en"],
            "title_ta": "தானியங்கி உணரி எச்சரிக்கை: நகராட்சி அவசர பராமரிப்பு தேவை",
            "description_en": (
                f"Automated IoT device alert from {device_id} in {ward_id}. "
                f"Sensor '{sensor_type}' recorded value {reading_value}, exceeding safety threshold {cfg['critical']}. "
                f"Telemetry timestamp: {datetime.now(timezone.utc).isoformat()}."
            ),
            "description_ta": f"உணரி {device_id} பதிவு செய்த மதிப்பு {reading_value}. உடனடி நடவடிக்கை தேவை.",
            "category": cfg["category"],
            "priority": "critical" if reading_value >= cfg["critical"] * 1.05 else "high",
            "ward_id": ward_id,
            "latitude": lat,
            "longitude": lon,
            "origin": f"IOT_TELEMETRY_{device_id}",
            "device_battery_pct": battery_pct,
            "requires_human_approval": True,
        }

        return {
            "triggered": True,
            "status": "ESCALATION_TICKET_GENERATED",
            "device_id": device_id,
            "reading_value": reading_value,
            "generated_ticket": ticket_payload,
        }
