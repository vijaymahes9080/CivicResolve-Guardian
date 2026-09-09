# Data Privacy & Dual-Storage Architecture

## 1. The Citizen Privacy Problem
Public grievance dashboards frequently suffer from inadvertent PII disclosure:
- Citizen phone numbers posted on public tracking boards.
- Residential street addresses and names visible to anyone with a case ID.
- Citizen identities scraped by telemarketers.

## 2. The CivicResolve Dual-Storage Solution

```
Citizen Raw Input (Text / Voice)
       │
       ▼
[ PII Redaction Filter ]
  ├─ Phone numbers  ──> [PHONE_REDACTED]
  ├─ Aadhaar/IDs    ──> [AADHAAR_REDACTED]
  ├─ Door numbers   ──> [DOOR_ADDRESS_REDACTED]
  └─ Personal names ──> [NAME_REDACTED]
       │
       ├─────────────────────────────────┐
       ▼                                 ▼
[ Restricted Vault ]           [ Public & AI Store ]
- Encrypted raw text           - Sanitized text
- Audio recording              - RAG embeddings
- Caller contact details       - Public tracking
- Accessible ONLY by           - MCP agent payloads
  assigned officers            - Audit transparency
```

## 3. Data Retention & Consent
- Citizen voice recordings are only retained if the citizen provides affirmative consent (`audio_consent_stored=true`).
- Citizens can request grievance record anonymization upon final verification.
