from __future__ import annotations

import html
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean
from typing import Any

from fastapi.responses import HTMLResponse

from .metrics import percentile

LOG_PATH = Path("data/logs.jsonl")
WINDOW_MINUTES = 60
REFRESH_SECONDS = 30


def _records(path: Path = LOG_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    result = []
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=WINDOW_MINUTES)
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
            timestamp = datetime.fromisoformat(record["ts"].replace("Z", "+00:00"))
        except (KeyError, ValueError, json.JSONDecodeError):
            continue
        if timestamp >= cutoff:
            result.append(record)
    return result


def dashboard_values(records: list[dict[str, Any]]) -> dict[str, str]:
    requests = [item for item in records if item.get("event") == "request_received"]
    responses = [item for item in records if item.get("event") == "response_sent"]
    failures = [item for item in records if item.get("event") == "request_failed"]
    latencies = [item["latency_ms"] for item in responses if isinstance(item.get("latency_ms"), int)]
    costs = [item["cost_usd"] for item in responses if isinstance(item.get("cost_usd"), (int, float))]
    tokens_in = [item["tokens_in"] for item in responses if isinstance(item.get("tokens_in"), int)]
    tokens_out = [item["tokens_out"] for item in responses if isinstance(item.get("tokens_out"), int)]
    quality = [item["quality_score"] for item in responses if isinstance(item.get("quality_score"), (int, float))]
    breakdown: dict[str, int] = {}
    for item in failures:
        kind = str(item.get("error_type", "unknown"))
        breakdown[kind] = breakdown.get(kind, 0) + 1
    error_rate = (len(failures) / len(requests) * 100) if requests else 0.0
    return {
        "latency": f"P50 {percentile(latencies, 50):.0f} · P95 {percentile(latencies, 95):.0f} · P99 {percentile(latencies, 99):.0f} ms",
        "traffic": f"{len(requests)} requests · {len(requests) / WINDOW_MINUTES:.2f} req/min",
        "errors": f"{error_rate:.1f}% · {html.escape(str(breakdown or 'no errors'))}",
        "cost": f"${sum(costs):.4f} total",
        "tokens": f"{sum(tokens_in):,} input · {sum(tokens_out):,} output",
        "quality": f"{mean(quality):.2f}" if quality else "No response data",
    }


def render_dashboard() -> HTMLResponse:
    values = dashboard_values(_records())
    cards = [
        ("Latency percentiles", values["latency"], "P95 ≤ 3000 ms"),
        ("Request traffic", values["traffic"], "≥ 1 request/min"),
        ("Error rate & breakdown", values["errors"], "≤ 2%"),
        ("Cost over time", values["cost"], "≤ $2.50 / window"),
        ("Input & output tokens", values["tokens"], "≤ 50,000 tokens"),
        ("Quality proxy", values["quality"], "Average ≥ 0.75"),
    ]
    card_html = "".join(f"<section><h2>{title}</h2><p>{value}</p><small>SLO: {threshold}</small></section>" for title, value, threshold in cards)
    return HTMLResponse(f"""<!doctype html><html><head><meta charset='utf-8'><meta http-equiv='refresh' content='{REFRESH_SECONDS}'><title>Day 13 AI Observability</title><style>body{{font-family:system-ui;background:#0b1020;color:#f1f5f9;margin:0;padding:32px}}header{{display:flex;justify-content:space-between;align-items:end}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:24px}}section{{background:#17203a;border:1px solid #334155;border-radius:12px;padding:20px}}h1,h2,p{{margin:0}}h2{{font-size:1rem;color:#93c5fd}}p{{font-size:1.3rem;margin:14px 0}}small{{color:#a7f3d0}}</style></head><body><header><div><h1>Day 13 AI Observability</h1><p>Window: last {WINDOW_MINUTES} minutes · refresh: {REFRESH_SECONDS}s</p></div><small>Source: data/logs.jsonl</small></header><main class='grid'>{card_html}</main></body></html>""")
