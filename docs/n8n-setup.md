# n8n Setup & Deployment Guide

## 1. Prerequisites
- Docker & Docker Compose or Node.js 18+
- Active CivicResolve Guardian backend running at `http://localhost:8000`

## 2. Launching n8n with Docker
```bash
docker run -d --name civicresolve-n8n \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=Admin@2026! \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n:latest
```

## 3. Importing the Workflow
1. Navigate to `http://localhost:5678` in your browser.
2. Log in with `admin` / `Admin@2026!`.
3. Select **Workflows** > **Import from File**.
4. Upload `n8n/civicresolve_triage_workflow.json`.
5. Toggle the workflow to **Active**.

## 4. Triggering via cURL
```bash
curl -X POST http://localhost:5678/webhook/civicresolve-complaint-submitted \
  -H "Content-Type: application/json" \
  -d '{"complaint_id": "REPLACE_WITH_UUID", "token": "REPLACE_WITH_JWT"}'
```
