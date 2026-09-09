# ADR 0004: Model Context Protocol (MCP) Deny-by-Default Authorization

## Status
Accepted

## Context
When external agents or IDE clients interface with CivicResolve Guardian via MCP (Model Context Protocol), exposing broad database read/write permissions creates severe security risks, including cross-case data leakage and privilege escalation.

## Decision
We enforce a **Deny-by-Default MCP Architecture**:
1. **Tool Allowlist**: The MCP server exposes strictly 6 predefined tools:
   - `search_policy`
   - `get_case_summary`
   - `suggest_routing`
   - `list_missing_evidence`
   - `draft_citizen_update`
   - `request_human_approval`
2. **Role & Tenant Enforcement**: Every tool execution must supply a valid caller token and verify that the caller is authorized to view the requested `case_id`.
3. **Payload Sanitization**: Case summaries returned via MCP automatically apply PII redactions so external LLM contexts never receive unmasked citizen data.
4. **Audit Signing**: Every MCP tool execution generates an immutable `AuditEvent` with actor role `mcp_tool`.

## Consequences
- **Pros**: Secure external agent integration, airtight boundaries against prompt injection or unauthorized case manipulation.
- **Cons**: Requires explicit schema definitions and role-context injection on all MCP tool endpoints.
