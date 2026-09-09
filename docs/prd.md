# Product Requirements Document (PRD): CivicResolve Guardian

## 1. Executive Summary & Vision
**CivicResolve Guardian** is an enterprise-grade, evidence-grounded civic grievance triage and resolution verification platform designed for municipal corporations and state government administrations (with first-class Tamil & English support). It solves three critical systemic failures in modern public grievance systems:
1. **Misrouting and Administrative Delays**: Grievances bounce between civic departments (e.g., Road Works vs. Underground Drainage) due to subjective manual triage.
2. **Citizen Privacy Violations**: Public grievance portals often expose citizen phone numbers, home addresses, and identity records in open audit trails.
3. **Ghost / Superficial Resolutions**: Officers frequently mark grievances "Resolved" without attaching verifiable proof or genuinely addressing the underlying civic failure.

CivicResolve Guardian introduces **deterministic guardrails, dual-storage privacy vaults, policy-grounded RAG citations**, and an **automated resolution quality auditor** to make every civic resolution verifiable, transparent, and legally accountable.

---

## 2. Target Users & Personas

| Persona | Role | Primary Needs | Key Pain Points Addressed |
|---|---|---|---|
| **Citizen (பொதுமக்கள்)** | Grievance Submitter | File complaints in Tamil/English via text or voice; track status reliably; safeguard personal data. | Complex forms, language barriers, fear of personal phone/address exposure, unresolved ghost closures. |
| **Grievance Redressal Officer (GRO)** | Case Reviewer & Router | Review AI triage suggestions with policy citations; approve or override routing; dispatch field workers. | Overwhelming case backlogs, unclear jurisdictional bylaws, pressure to close cases prematurely. |
| **Municipal Commissioner / Admin** | Quality & SLA Overseer | Monitor department SLAs, identify repeat problem areas, audit resolution veracity. | Inaccurate resolution reporting, lack of objective resolution quality metrics. |

---

## 3. Core Functional Requirements

### 3.1 Multilingual Grievance Intake & Privacy Vault
- **FR-1.1**: Support direct text submission in English and Tamil (தமிழ் script and transliterated Tamil).
- **FR-1.2**: Support optional voice/audio submission (WebM, WAV, MP3) with consent-based storage and Whisper-compatible transcription.
- **FR-1.3**: Automatic dual-storage pipeline:
  - **Vault (Restricted Access)**: Original citizen input, contact details, audio records.
  - **Redacted Store (Public / AI Processing)**: All 10-digit Indian phone numbers, Aadhaar/ID numbers, specific door addresses, and person names scrubbed using deterministic regular expressions and Presidio-compatible entity markers.
- **FR-1.4**: Evidence attachment validator enforcing mime types (JPEG, PNG, PDF) and max 10MB per file with SHA-256 integrity hashing.

### 3.2 Policy Knowledge Base & Grounded Retrieval (RAG)
- **FR-2.1**: Ingest municipal bylaws, citizen charters, and SLA circulars for:
  - Water Supply & Sewerage
  - Solid Waste Management & Sanitation
  - Roads & Potholes
  - Street Lighting & Electrical Safety
  - Public Health & Vector Control
- **FR-2.2**: Chunking documents with stable IDs (`DOC-{dept}-{id}-C{idx}`) preserving section titles, jurisdiction, and official SLA targets.
- **FR-2.3**: Grounded citations: All triage recommendations MUST link to exact policy sections. If retrieval similarity is below threshold (0.50), the system must explicitly declare `insufficient_evidence` rather than speculating.

### 3.3 Bounded Triage State Machine
- **FR-3.1**: Predict category and responsible municipal department with confidence score (0.0 - 1.0).
- **FR-3.2**: Calculate deterministic priority (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) based on life safety risks, school/hospital proximity, and policy SLA.
- **FR-3.3**: Duplicate detection: Search active open complaints in the same ward/locality within 14 days and flag high-similarity cases (>0.75).
- **FR-3.4**: Missing evidence detection: Flag missing landmarks, missing photos for road/structural complaints, or absent timestamps.
- **FR-3.5**: Mandatory Human-in-the-Loop Gating: **AI cannot change official routing or status autonomously**. All assignments require explicit officer confirmation or override.

### 3.4 Resolution Quality Checker
- **FR-4.1**: Multi-factor evaluation of officer closure reports:
  - Required fields present (action taken summary, worker details).
  - Photographic or documentary resolution evidence attached.
  - Timestamp consistency (closure date cannot precede submission date).
  - Issue coverage (does the resolution note address the specific complaint defect?).
- **FR-4.2**: Structured evaluation output: `likely_resolved`, `weak_resolution`, `insufficient_evidence`, `contradiction_detected`.
- **FR-4.3**: Contradiction detection: Flags cases where citizen marks "Issue Persists" or resolution notes contradict original location/issue.

### 3.5 Permissioned Model Context Protocol (MCP) Server
- **FR-5.1**: Provide a secure MCP server exposing strictly 6 tools:
  1. `search_policy`
  2. `get_case_summary`
  3. `suggest_routing`
  4. `list_missing_evidence`
  5. `draft_citizen_update`
  6. `request_human_approval`
- **FR-5.2**: Enforce RBAC per tool, log every invocation in the audit trail, and redact PII before returning payloads.

### 3.6 Automation Workflow (n8n)
- **FR-6.1**: Modular n8n workflow triggered upon grievance submission.
- **FR-6.2**: Automated triage invocation and officer notification dispatch.
- **FR-6.3**: SLA timer management with overdue escalation notices and dead-letter error handling.

---

## 4. Non-Functional Requirements
- **NFR-1 Latency**: Triage and citation retrieval must complete within < 1.5 seconds on a standard consumer laptop.
- **NFR-2 Security**: Strict defense against prompt injection in complaint bodies, indirect prompt injection from uploaded files, broken object-level authorization (BOLA), and SSRF.
- **NFR-3 Accessibility**: Frontend built to WCAG 2.1 AA standards with visible focus states, ARIA landmarks, keyboard navigability, and high contrast.
- **NFR-4 Auditability**: Every state change, routing approval, and tool call produces an immutable `AuditEvent` signed with a cryptographic checksum.
