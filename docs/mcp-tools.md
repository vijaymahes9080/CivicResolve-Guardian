# Model Context Protocol (MCP) Tool Reference

CivicResolve Guardian implements the Model Context Protocol (MCP 2.x) to securely expose 6 bounded, strictly permissioned tools for AI agent and IDE integration.

---

## Tool Contracts

### 1. `search_policy`
- **Description**: Search indexed municipal bylaws and SLA charters for matching regulations.
- **Parameters**:
  - `query` (string, min 3 chars)
  - `department` (optional string)
- **Role Requirement**: Public / Any

### 2. `get_case_summary`
- **Description**: Retrieves sanitized case metadata and status. PII is scrubbed.
- **Parameters**:
  - `case_id` (string, UUID)
  - `caller_role` (string, default: "officer")
- **Role Requirement**: `officer` or `admin`

### 3. `suggest_routing`
- **Description**: Runs deterministic triage agent and returns department, category, priority, and citations.
- **Parameters**:
  - `case_id` (string, UUID)
  - `caller_role` (string, default: "officer")
- **Role Requirement**: `officer` or `admin`

### 4. `list_missing_evidence`
- **Description**: Analyzes complaint text to detect missing landmarks or photos.
- **Parameters**:
  - `case_id` (string, UUID)
  - `caller_role` (string, default: "officer")
- **Role Requirement**: `officer` or `admin`

### 5. `draft_citizen_update`
- **Description**: Generates a polite, grounded citizen update message in English or Tamil.
- **Parameters**:
  - `case_id` (string, UUID)
  - `caller_role` (string, default: "officer")
- **Role Requirement**: `officer` or `admin`

### 6. `request_human_approval`
- **Description**: Stages an official routing request for human officer review. Does not mutate status autonomously.
- **Parameters**:
  - `case_id` (string, UUID)
  - `proposed_department` (string)
  - `proposed_priority` (string)
  - `officer_notes` (optional string)
  - `caller_role` (string, default: "officer")
- **Role Requirement**: `officer` or `admin`
