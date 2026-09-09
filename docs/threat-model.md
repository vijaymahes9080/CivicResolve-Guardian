# STRIDE Threat Model: CivicResolve Guardian

## 1. Threat Matrix & Mitigations

| Category | Threat Description | Attack Vector | System Defense & Mitigation | Status |
|---|---|---|---|---|
| **Spoofing** | Adversary attempts to file or approve complaints as a Municipal Officer. | Forged JWT token or session hijacking. | Cryptographic HMAC-SHA256 JWT tokens with role claims verified by database query on every protected endpoint. | **Mitigated** |
| **Tampering** | Rogue actor alters case status or deletes audit logs. | Direct API mutation or SQL injection. | SQLAlchemy ORM parameterized queries; immutable append-only `AuditEvent` log signed with HMAC-SHA256 checksum. | **Mitigated** |
| **Repudiation** | Officer denies approving or closing a complaint prematurely. | Unrecorded state changes. | Every state change produces an immutable audit record capturing actor ID, timestamp, prior state, new state, and cryptographic signature. | **Mitigated** |
| **Information Disclosure** | Citizen phone numbers, addresses, and identity numbers exposed in public audit logs. | Data scraping or public API endpoints. | Dual-Storage Privacy Vault: PII redacted deterministically at intake; public API endpoints only expose scrubbed representation. | **Mitigated** |
| **Denial of Service** | Flooding API with large text or malicious audio files. | Rapid complaint submissions or oversized audio payloads. | SlowAPI rate limiting (100 req/min); strict 10MB file limit with streaming hash verification. | **Mitigated** |
| **Elevation of Privilege** | Citizen attempts to call officer routing approval or MCP tools. | API parameter tampering or role escalation headers. | RBAC middleware (`require_role(["officer", "admin"])`) rejecting unauthorized callers with HTTP 403 Forbidden. | **Mitigated** |
| **Prompt Injection** | Citizen complaint instructs LLM to override routing or approve cash compensation. | Adversarial prompt text embedded in complaint body. | Bounded State Machine: AI models cannot alter case status autonomously (`approval_required=true` enforced). | **Mitigated** |

---

## 2. Indirect Document Injection Defense
When citizen uploads evidence (PDF/Images), documents are checked for MIME type integrity and stored outside the web root. RAG search queries only execute against verified administrative bylaws, never citizen-uploaded text.
