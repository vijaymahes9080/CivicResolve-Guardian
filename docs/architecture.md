# System Architecture: CivicResolve Guardian

## 1. Overview
**CivicResolve Guardian** coordinates citizen touchpoints, bounded AI triage agents, grounded policy RAG retrieval, human officer approval gates, and automated resolution verification into an auditable, high-assurance civic governance platform.

---

## 2. Component Topology

```mermaid
flowchart TB
    subgraph Citizens["Citizen Touchpoints"]
        WebCitizen["Citizen Web App\n(Tamil / English)"]
        AudioInput["Voice / Audio Ingestion\n(Whisper Adapter)"]
    end

    subgraph PrivacyGate["Privacy & Ingestion Boundary"]
        LangDetect["Language Detector\n(Tamil / English)"]
        PIIRedactor["PII Redaction Engine\n(Presidio / Regex Engine)"]
        Vault["Encrypted Raw Storage\n(Restricted Access)"]
    end

    subgraph ControlPlane["CivicResolve Guardian Core (FastAPI)"]
        APIGateway["REST API & RBAC Gate\n(JWT, Rate Limiting)"]
        RAGEngine["Policy RAG & Citation Engine\n(Synthesized Bylaws & SLA Charters)"]
        TriageStateMachine["Bounded Triage Agent\n(Deterministic Rules + Scoring)"]
        ResolutionAuditor["Resolution Quality Checker\n(Deterministic + LLM Evaluation)"]
        AuditLog["Immutable Audit Event Store"]
    end

    subgraph Officers["Officer & Administration Plane"]
        OfficerDashboard["Officer Review Dashboard\n(Queue, Citations, Approvals)"]
        ApprovalDrawer["Human-in-the-Loop Gating"]
    end

    subgraph Automation["External Automation & MCP Plane"]
        MCPServer["Permissioned MCP Server\n(6 Guarded Tools)"]
        N8NWorkflow["n8n Community Workflow\n(Intake, Reminders, Escalations)"]
    end

    WebCitizen --> PrivacyGate
    AudioInput --> PrivacyGate
    PrivacyGate --> Vault
    PrivacyGate -->|Redacted Payload| APIGateway
    APIGateway --> TriageStateMachine
    TriageStateMachine --> RAGEngine
    TriageStateMachine --> OfficerDashboard
    OfficerDashboard --> ApprovalDrawer
    ApprovalDrawer --> APIGateway
    APIGateway --> ResolutionAuditor
    APIGateway --> AuditLog
    MCPServer <--> APIGateway
    N8NWorkflow <--> APIGateway
```

---

## 3. Data Flow Stages

1. **Ingestion & Privacy Sanitization**:
   - Citizen provides textual or voice grievance in Tamil (தமிழ்) or English.
   - PII Detection Engine scrubs phone numbers, Aadhaar/IDs, person names, and door numbers.
   - Original unredacted text is stored in the **Restricted Vault**. Redacted representation is stored in the public/AI processing database.
2. **Grounded Policy Retrieval (RAG)**:
   - Evaluates grievance text against 5 indexed municipal bylaws.
   - Requires similarity score >= 0.50. If no policy passes threshold, declares `insufficient_evidence`.
3. **Bounded Triage State Machine**:
   - Classifies department and priority with deterministic rule anchors.
   - Computes duplicate similarity against open cases in the same ward.
   - Flags missing evidence items.
   - Enforces `approval_required: true`.
4. **Human-in-the-Loop Officer Approval**:
   - Officer reviews recommendations side-by-side with citations.
   - Approves routing or provides explicit override reason.
   - Case transitions to `ROUTED_ASSIGNED`.
5. **Resolution Veracity Verification**:
   - Officer submits action summary and completion photo.
   - Resolution Quality Auditor verifies deterministic constraints and runs contradiction detection.
   - Verdict rendered: `likely_resolved`, `weak_resolution`, `insufficient_evidence`, or `contradiction_detected`.
