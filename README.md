# CivicResolve Guardian 🏛️🛡️

> **Multilingual, Evidence-Grounded Public Grievance Triage, Routing & Resolution Quality Platform**
> *Supporting English & Tamil (தமிழ்) | Human-in-the-Loop Municipal Governance*

[![CI](https://github.com/vijaymahes9080/CivicResolve-Guardian/actions/workflows/ci.yml/badge.svg)](https://github.com/vijaymahes9080/CivicResolve-Guardian/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React 18](https://img.shields.io/badge/React-18-cyan.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)

---

## 🌟 Mission & Key Capabilities

Public grievance portals worldwide suffer from three systemic crises:
1. **Administrative Gridlock**: Grievances bounce aimlessly between departments due to manual guesswork.
2. **Citizen Privacy Exposure**: Citizen mobile numbers, residential addresses, and personal identities are leaked in public tracking feeds.
3. **Superficial "Ghost" Closures**: Cases are marked "Resolved" without verifiable evidence, photographic proof, or actual redress.

**CivicResolve Guardian** addresses these crises through a robust, production-ready system:
- **Multilingual Ingestion (English & Tamil தமிழ்)**: Native support for Tamil script and transliteration with voice/audio grievance intake.
- **Dual-Storage Privacy Vault**: Real-time automated PII redaction (phones, Aadhaar/IDs, door addresses, names) ensuring public and AI layers remain leak-free.
- **Grounded Policy RAG**: Recommendations are anchored in municipal bylaws and citizen charters with verified citations—returning "Insufficient Evidence" rather than hallucinating.
- **Bounded Triage State Machine**: Suggests departments, priority levels, and missing evidence with deterministic guardrails—**no autonomous action without explicit officer approval**.
- **Resolution Quality Checker**: Evaluates whether officer resolution claims are genuine, evidence-backed, date-consistent, and non-contradictory.
- **Permissioned MCP Server**: Exposes 6 strictly audited tools for external agentic integration under deny-by-default access control.
- **Automated n8n Workflows**: Full lifecycle management with reminders, SLA escalation, and dead-letter error handling.

---

## 🏗️ Architecture Overview

```
                          [ Citizens (English / தமிழ்) ]
                                |               |
                             (Text)          (Audio)
                                |               |
                                v               v
                    +---------------------------------------+
                    |  Language Detector & Whisper Adapter  |
                    +---------------------------------------+
                                        |
                                        v
                    +---------------------------------------+
                    |       Dual-Storage Privacy Gate       |
                    |   (Raw Vault vs. Redacted Public DB)  |
                    +---------------------------------------+
                                        | (Redacted Payload)
                                        v
                    +---------------------------------------+
                    |     FastAPI Core & Security Gateway    |
                    |       (JWT, RBAC, Rate Limiting)       |
                    +---------------------------------------+
                           /            |            \
                          v             v             v
            +----------------+  +----------------+  +----------------+
            |  Grounded RAG  |  | Bounded Triage |  |   Resolution   |
            |  Policy Engine |  |  State Machine |  | Quality Auditor|
            +----------------+  +----------------+  +----------------+
                          \             |             /
                           v            v            v
                    +---------------------------------------+
                    |   Officer Dashboard & Human Approval  |
                    |      (Queue, Citations, Audit Log)    |
                    +---------------------------------------+
                                        |
                    +---------------------------------------+
                    |   MCP Server (6 Tools) & n8n Engine   |
                    +---------------------------------------+
```

---

## 🚀 Quickstart & Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- Git

### 1. Clone & Setup Environment
```bash
git clone https://github.com/vijaymahes9080/CivicResolve-Guardian.git
cd CivicResolve-Guardian
cp .env.example .env
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py       # Seeds municipal bylaws, demo users, sample complaints
uvicorn app.main:app --reload --port 8000
```
Backend runs at `http://localhost:8000` (Swagger UI at `/docs`).

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

---

## 🔑 Demo Credentials (Local Use Only)

| Role | Username / Email | Password | Access Rights |
|---|---|---|---|
| **Admin** | `admin@civicresolve.gov.in` | `Admin@2026!` | Full administrative, audit, and policy management |
| **Officer (GRO)** | `officer@civicresolve.gov.in` | `Officer@2026!` | Triage queue, approval drawer, resolution submission |
| **Citizen (English)** | `citizen@civicresolve.gov.in` | `Citizen@2026!` | Grievance submission, evidence upload, case tracking |
| **Citizen (Tamil)** | `selvi@civicresolve.gov.in` | `Citizen@2026!` | தமிழ் grievance submission, tracking |

---

## 🎬 5-Minute Interactive Demo Flow

1. **Submit Grievance (Citizen Portal)**:
   - Switch language to **தமிழ்** or **English**.
   - Type a complaint containing a phone number and address:
     > *"Severe drinking water contamination on 4th Cross Street, Ward 12. Brown foul-smelling water since 3 days. Contact me at 9840123456."*
   - Notice the live PII preview scrubbing the mobile number to `[PHONE_REDACTED]`.
   - Submit the grievance.
2. **Review AI Triage & Grounded Citations (Officer Dashboard)**:
   - Log in as `officer@civicresolve.gov.in`.
   - Open the new case in the **Triage Queue**.
   - View the AI recommendation: Department: `Water Supply & Sewerage Board`, Priority: `HIGH`.
   - Inspect the **Policy Citations Panel**: Links directly to Section 4.2 of the *Municipal Water Supply Charter* (SLA: 24 hours for contamination).
3. **Approve Routing (Human-in-the-Loop)**:
   - Confirm the recommendation in the **Approval Drawer** with one click.
   - Observe the state transition to `ROUTED_ASSIGNED` and inspect the immutable cryptographic audit event.
4. **Resolution Quality Verification**:
   - Submit an officer resolution report.
   - Run the **Resolution Quality Auditor** to verify evidence attachment and detect any contradictions before final closure.

---

## 🛡️ Security, Privacy & Ethics

- **Zero Fabricated Policies**: The RAG engine is strictly grounded in synthetic municipal bylaws. If no regulation matches, it returns `insufficient_evidence`.
- **Dual-Storage Isolation**: Citizens' raw identity data is quarantined in the Restricted Vault. Public and AI layers strictly consume scrubbed data.
- **No Unsafe Autonomous Escalation**: AI models recommend; only human officers execute official assignments and closures.
- **Prompt Injection Immunity**: Complaint text is sanitized and passed through typed parameter boundaries.

---

## 🐳 Docker Deployment

```bash
docker-compose up -d --build
```
Services deployed:
- **Backend API**: `http://localhost:8000`
- **Frontend App**: `http://localhost:5173`
- **PostgreSQL Database**: `localhost:5432`
- **Redis Cache / Broker**: `localhost:6379`
- **n8n Automation Engine**: `http://localhost:5678`

---

## 📜 Documentation Index

- [Architecture & Data Flows](file:///d:/current%20project/zz/docs/architecture.md)
- [Product Requirements Document (PRD)](file:///d:/current%20project/zz/docs/prd.md)
- [REST API Reference](file:///d:/current%20project/zz/docs/api.md)
- [Security Controls & Headers](file:///d:/current%20project/zz/docs/security.md)
- [STRIDE Threat Model](file:///d:/current%20project/zz/docs/threat-model.md)
- [Evaluation & Benchmark Report](file:///d:/current%20project/zz/docs/evaluation.md)
- [n8n Workflow Setup](file:///d:/current%20project/zz/docs/n8n-setup.md)
- [MCP Tool Contracts](file:///d:/current%20project/zz/docs/mcp-tools.md)
- [WCAG Accessibility Guidelines](file:///d:/current%20project/zz/docs/accessibility.md)
- [Data Privacy & Dual-Storage Architecture](file:///d:/current%20project/zz/docs/privacy.md)
- [Interactive Demo Walkthrough](file:///d:/current%20project/zz/docs/demo-script.md)
- [Project Roadmap](file:///d:/current%20project/zz/docs/roadmap.md)
