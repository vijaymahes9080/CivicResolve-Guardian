import pytest
from app.core.telemetry import MetricsRegistry

def test_metrics_registry():
    registry = MetricsRegistry()
    registry.inc_request("/api/v1/complaints", 201)
    registry.inc_request("/api/v1/complaints", 201)
    registry.inc_pii_redaction(3)
    registry.inc_rag_query()
    registry.inc_approval()
    registry.active_websocket_clients = 5

    output = registry.generate_prometheus_text()
    assert 'civicresolve_requests_total{endpoint="/api/v1/complaints",status="201"} 2' in output
    assert "civicresolve_pii_redactions_total 3" in output
    assert "civicresolve_rag_queries_total 1" in output
    assert "civicresolve_active_websocket_clients 5" in output
