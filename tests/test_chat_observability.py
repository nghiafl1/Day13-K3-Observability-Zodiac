from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from app import logging_config
from app.main import app


def test_chat_response_log_exposes_quality_for_dashboard(
    monkeypatch, tmp_path: Path
) -> None:
    log_path = tmp_path / "logs.jsonl"
    monkeypatch.setattr(logging_config, "LOG_PATH", log_path)

    with TestClient(app) as client:
        response = client.post(
            "/chat",
            json={
                "user_id": "student-01",
                "session_id": "session-01",
                "feature": "qa",
                "message": "Explain observability",
            },
        )

    assert response.status_code == 200
    events = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
    response_event = next(event for event in events if event["event"] == "response_sent")
    assert response_event["quality_score"] == response.json()["quality_score"]


def test_chat_logs_checkpoint_one_context_and_redacts_pii(
    monkeypatch, tmp_path: Path
) -> None:
    log_path = tmp_path / "logs.jsonl"
    monkeypatch.setattr(logging_config, "LOG_PATH", log_path)

    with TestClient(app) as client:
        response = client.post(
            "/chat",
            headers={"x-request-id": "req-1a2b3c4d"},
            json={
                "user_id": "student-01",
                "session_id": "session-01",
                "feature": "qa",
                "message": "Contact me at student@example.com or 090 123 4567",
            },
        )

    assert response.status_code == 200
    api_events = [
        json.loads(line)
        for line in log_path.read_text(encoding="utf-8").splitlines()
        if json.loads(line).get("service") == "api"
    ]
    assert api_events
    for event in api_events:
        assert event["correlation_id"] == "req-1a2b3c4d"
        assert {"user_id_hash", "session_id", "feature", "model", "env"}.issubset(event)
        serialized = json.dumps(event, ensure_ascii=False)
        assert "student@example.com" not in serialized
        assert "090 123 4567" not in serialized
