"""
CivicResolve Guardian - Prometheus Metrics & Telemetry Collector
Instruments request counters, RAG retrieval latencies, PII redaction frequencies,
and live operational cockpit telemetry in standard Prometheus text format.
"""

from typing import Dict, Any


class MetricsRegistry:
    """In-memory telemetry collector for Prometheus scraping."""

    def __init__(self):
        self.request_counts: Dict[str, int] = {}
        self.pii_redactions_total: int = 0
        self.rag_queries_total: int = 0
        self.triage_approvals_total: int = 0
        self.active_websocket_clients: int = 0

    def inc_request(self, endpoint: str, status_code: int = 200):
        key = f'{endpoint}:{status_code}'
        self.request_counts[key] = self.request_counts.get(key, 0) + 1

    def inc_pii_redaction(self, count: int = 1):
        self.pii_redactions_total += count

    def inc_rag_query(self):
        self.rag_queries_total += 1

    def inc_approval(self):
        self.triage_approvals_total += 1

    def generate_prometheus_text(self) -> str:
        lines = [
            "# HELP civicresolve_requests_total Total HTTP requests handled",
            "# TYPE civicresolve_requests_total counter",
        ]
        for key, count in self.request_counts.items():
            endpoint, status = key.split(":")
            lines.append(f'civicresolve_requests_total{{endpoint="{endpoint}",status="{status}"}} {count}')

        lines.extend([
            "# HELP civicresolve_pii_redactions_total Total PII fields masked in vault",
            "# TYPE civicresolve_pii_redactions_total counter",
            f"civicresolve_pii_redactions_total {self.pii_redactions_total}",
            "# HELP civicresolve_rag_queries_total Total policy RAG retrieval queries",
            "# TYPE civicresolve_rag_queries_total counter",
            f"civicresolve_rag_queries_total {self.rag_queries_total}",
            "# HELP civicresolve_triage_approvals_total Officer triage approvals signed",
            "# TYPE civicresolve_triage_approvals_total counter",
            f"civicresolve_triage_approvals_total {self.triage_approvals_total}",
            "# HELP civicresolve_active_websocket_clients Live officer war-room connections",
            "# TYPE civicresolve_active_websocket_clients gauge",
            f"civicresolve_active_websocket_clients {self.active_websocket_clients}",
        ])
        return "\n".join(lines) + "\n"


telemetry_registry = MetricsRegistry()
