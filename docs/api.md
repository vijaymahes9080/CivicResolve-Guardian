# REST API Reference: CivicResolve Guardian

Base URL: `http://localhost:8000/api/v1`

---

## Authentication Endpoints

### 1. Register User
`POST /auth/register`
```json
{
  "email": "citizen@civicresolve.gov.in",
  "password": "Citizen@2026!",
  "full_name": "Vijay Mahes",
  "role": "citizen",
  "phone_number": "+91 9840123456",
  "preferred_language": "en"
}
```

### 2. Login
`POST /auth/login`
```json
{
  "email": "officer@civicresolve.gov.in",
  "password": "Officer@2026!"
}
```
**Response**:
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "user": { "id": "...", "role": "officer", "full_name": "..." }
}
```

---

## Grievance Endpoints

### 3. File Grievance
`POST /complaints`  
**Headers**: `Authorization: Bearer <token>`
```json
{
  "content": "Drinking water contamination at Door No. 12, 4th Cross. Contact 9840123456.",
  "language": "en",
  "ward": "Ward 12",
  "zone": "Zone 4 (Central)"
}
```

### 4. Run Bounded Triage
`POST /complaints/{id}/triage`  
**Response**:
```json
{
  "complaint_id": "...",
  "suggested_category": "Drinking Water & Sewerage Network",
  "suggested_department": "Water Supply & Sewerage Board",
  "priority_score": "CRITICAL",
  "confidence": 0.88,
  "reasons": ["Classified under Water Supply & Sewerage Board"],
  "citations": [
    {
      "policy_id": "POL-WATER-001",
      "section_id": "1.1",
      "title": "Section 1.1: Drinking Water Contamination",
      "relevance_score": 0.92
    }
  ],
  "approval_required": true
}
```

### 5. Officer Approve Routing
`POST /complaints/{id}/approve-routing`  
**Headers**: `Authorization: Bearer <officer_token>`
```json
{
  "approved_department": "Water Supply & Sewerage Board",
  "approved_priority": "CRITICAL",
  "officer_notes": "Emergency repair vehicle dispatched."
}
```

### 6. Verify Resolution Quality
`POST /complaints/{id}/resolution-check`  
**Headers**: `Authorization: Bearer <officer_token>`
```json
{
  "action_taken_summary": "Replaced burst pipe valve and verified water pressure. No sewage leak.",
  "completion_notes": "Site verified by Junior Engineer."
}
```

### 7. Search Policies & Bylaws
`GET /policies/search?query=drinking+water+leak&department=WATER`
