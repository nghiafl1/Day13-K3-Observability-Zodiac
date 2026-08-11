from app.dashboard import dashboard_values


def test_dashboard_calculates_all_six_panel_values() -> None:
    records = [
        {"event": "request_received"},
        {"event": "response_sent", "latency_ms": 200, "cost_usd": 0.01, "tokens_in": 10, "tokens_out": 20, "quality_score": 0.9},
        {"event": "request_failed", "error_type": "RuntimeError"},
    ]
    values = dashboard_values(records)
    assert set(values) == {"latency", "traffic", "errors", "cost", "tokens", "quality"}
    assert "P95" in values["latency"]
    assert "100.0%" in values["errors"]
    assert values["quality"] == "0.90"
