from app import metrics
from app.metrics import percentile


def test_percentile_basic() -> None:
    assert percentile([100, 200, 300, 400], 50) >= 100


def test_snapshot_includes_error_rate_pct(monkeypatch) -> None:
    monkeypatch.setattr(metrics, "TRAFFIC", 4)
    monkeypatch.setattr(metrics, "ERRORS", metrics.Counter({"RuntimeError": 1}))
    assert metrics.snapshot()["error_rate_pct"] == 20.0
