import pytest

def test_create_complaint_with_pii_redaction(client, citizen_token):
    headers = {"Authorization": f"Bearer {citizen_token}"}
    payload = {
        "content": "Drinking water contamination at Door No. 12, 5th Cross. Contact Ramesh at 9840123456.",
        "ward": "Ward 12",
        "zone": "Zone 4"
    }
    response = client.post("/api/v1/complaints", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "SUBMITTED"
    assert "[PHONE_REDACTED]" in data["redacted_content"]
    assert "9840123456" not in data["redacted_content"]
    assert "[DOOR_ADDRESS_REDACTED]" in data["redacted_content"]
    assert data["ward"] == "Ward 12"

def test_triage_and_routing_approval_flow(client, citizen_token, officer_token):
    # 1. Citizen creates complaint
    c_headers = {"Authorization": f"Bearer {citizen_token}"}
    create_resp = client.post(
        "/api/v1/complaints",
        json={"content": "Dangerous live electric wire hanging near school gate.", "ward": "Ward 12"},
        headers=c_headers
    )
    assert create_resp.status_code == 201
    case_id = create_resp.json()["id"]

    # 2. Run Triage
    triage_resp = client.post(f"/api/v1/complaints/{case_id}/triage", headers=c_headers)
    assert triage_resp.status_code == 200
    triage_data = triage_resp.json()
    assert triage_data["suggested_department"] == "Electrical & Street Lighting"
    assert triage_data["priority_score"] == "CRITICAL"
    assert triage_data["approval_required"] is True

    # 3. Officer approves routing
    o_headers = {"Authorization": f"Bearer {officer_token}"}
    approval_resp = client.post(
        f"/api/v1/complaints/{case_id}/approve-routing",
        json={"officer_notes": "Immediate safety team dispatched."},
        headers=o_headers
    )
    assert approval_resp.status_code == 200
    assert approval_resp.json()["status"] == "ROUTED_ASSIGNED"

    # 4. Check Audit Trail
    audit_resp = client.get(f"/api/v1/audit/{case_id}", headers=o_headers)
    assert audit_resp.status_code == 200
    events = audit_resp.json()
    action_types = [e["action_type"] for e in events]
    assert "COMPLAINT_CREATED" in action_types
    assert "TRIAGE_RECOMMENDED" in action_types
    assert "ROUTING_APPROVED" in action_types
