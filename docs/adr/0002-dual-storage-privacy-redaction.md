# ADR 0002: Dual-Storage Privacy Vault & PII Redaction

## Status
Accepted

## Context
Citizens filing grievances routinely provide sensitive Personally Identifiable Information (PII), such as personal mobile numbers, Aadhaar/voter identity numbers, home door numbers, and family names. If raw grievance data is ingested directly into vector databases, public audit dashboards, or shared with third-party LLMs, citizen privacy is fundamentally compromised.

## Decision
We enforce an architectural **Dual-Storage Privacy Pipeline**:
1. **Restricted Vault**: Stores the immutable raw complaint text, citizen contact phone/email, and original audio recordings. Access is strictly gated to verified officers assigned to the case.
2. **Redacted Processing Store**: A sanitized version where:
   - Indian 10-digit mobile numbers are replaced with `[PHONE_REDACTED]`.
   - 12-digit Aadhaar / identity tokens are masked to `[AADHAAR_REDACTED]`.
   - Specific house/door addresses are generalized to `[ADDRESS_REDACTED]`.
   - Personal names in complaint bodies are replaced with `[NAME_REDACTED]`.
3. **AI Layer Isolation**: RAG embeddings, triage classifiers, vector searches, and public audit feeds strictly consume the redacted representation.

## Consequences
- **Pros**: Complies with personal data protection regulations, eliminates PII leakage into vector indexes and model context windows, prevents accidental public exposure in transparency portals.
- **Cons**: Requires dual-column database storage and disciplined access control checks in API endpoints.
