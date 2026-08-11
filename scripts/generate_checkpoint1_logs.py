"""Generate clean, reproducible evidence logs for Checkpoint 1."""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Support both `python scripts/generate_checkpoint1_logs.py` and module execution.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app


REQUESTS = (
    {
        "request_id": "req-a1b2c3d4",
        "user_id": "u_cp1_01",
        "session_id": "s_cp1_01",
        "feature": "qa",
        "message": "Please send the answer to learner@example.com or 090 123 4567.",
    },
    {
        "request_id": "req-e5f6a7b8",
        "user_id": "u_cp1_02",
        "session_id": "s_cp1_02",
        "feature": "summary",
        "message": "Summarize observability. Test card: 4111 1111 1111 1111.",
    },
)


def main() -> None:
    with TestClient(app) as client:
        for payload in REQUESTS:
            response = client.post(
                "/chat",
                headers={"x-request-id": payload["request_id"]},
                json={key: value for key, value in payload.items() if key != "request_id"},
            )
            response.raise_for_status()
            assert response.json()["correlation_id"] == payload["request_id"]
    print(f"Generated {len(REQUESTS)} Checkpoint 1 requests in data/logs.jsonl")


if __name__ == "__main__":
    main()
