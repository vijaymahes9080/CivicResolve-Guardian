# n8n Automated Triage, Reminder & Escalation Workflow

This directory contains the production-ready n8n workflow for **CivicResolve Guardian**:
[`civicresolve_triage_workflow.json`](file:///d:/current%20project/zz/n8n/civicresolve_triage_workflow.json)

---

## 🎯 Workflow Overview

1. **Intake Webhook**: Listens on `POST /webhook/civicresolve-complaint-submitted` with payload:
   ```json
   {
     "complaint_id": "9e9a9d9f-3805-4ff9-ac3d-521bc8be6fe2",
     "token": "JWT_AUTH_TOKEN_HERE"
   }
   ```
2. **Fetch Case Details**: Authenticates with FastAPI backend to retrieve the complaint.
3. **Trigger Triage Engine**: Invokes `POST /api/v1/complaints/{id}/triage` to generate grounded routing and policy citations.
4. **Priority Branching**:
   - If **CRITICAL**: Dispatches simulated urgent SMS/Radio dispatch alert.
   - If **HIGH/MEDIUM/LOW**: Posts standard officer review queue notification.
5. **SLA Window & Reminder**: Simulates SLA timer (configurable 24h default).
6. **Overdue Escalation**: If case status remains `TRIAGED_PENDING_APPROVAL` after the SLA window, triggers an **L2 Municipal Commissioner Escalation Alert**.
7. **Dead-Letter Handler**: Catches failed HTTP calls for inspection.

---

## 📥 Import Instructions

1. Start n8n (either via Docker `docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n` or local CLI `npx n8n`).
2. Open n8n web console at `http://localhost:5678`.
3. Click **Workflows** > **Import from File**.
4. Select `civicresolve_triage_workflow.json`.
5. Click **Publish / Active** toggle.

---

## 🧪 Testing the Webhook

Run the following cURL command or PowerShell invoke:

```bash
curl -X POST http://localhost:5678/webhook-test/civicresolve-complaint-submitted \
  -H "Content-Type: application/json" \
  -d '{"complaint_id": "REPLACE_WITH_CASE_ID", "token": "REPLACE_WITH_OFFICER_OR_CITIZEN_TOKEN"}'
```
