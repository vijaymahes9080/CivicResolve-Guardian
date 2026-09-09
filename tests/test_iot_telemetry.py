import pytest
from app.api.iot_telemetry import IoTTriageConverter

def test_iot_flood_sensor_breach():
    event = IoTTriageConverter.process_sensor_event(
        device_id="FLOOD-GAUGE-VELACHERY-01",
        sensor_type="FLOOD_LEVEL_CM",
        reading_value=92.5,
        ward_id="WARD-178",
        lat=12.9815,
        lon=80.2180,
    )
    assert event["triggered"] is True
    assert event["status"] == "ESCALATION_TICKET_GENERATED"
    ticket = event["generated_ticket"]
    assert ticket["category"] == "WATER_SUPPLY"
    assert ticket["priority"] == "critical"
    assert ticket["ward_id"] == "WARD-178"
    assert "VELACHERY" in ticket["origin"]

def test_iot_sensor_normal_reading():
    event = IoTTriageConverter.process_sensor_event(
        device_id="BIN-LIDAR-09",
        sensor_type="BIN_FILL_PCT",
        reading_value=45.0, # under 90% threshold
        ward_id="WARD-110",
        lat=13.08,
        lon=80.27,
    )
    assert event["triggered"] is False
    assert event["status"] == "NORMAL"
