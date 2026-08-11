# Alert runbook

## Alert 1 — High API latency

- Severity: warning
- SLI/SLO: latency P95 ≤ 3000 ms.
- Condition: P95 exceeds 3000 ms for 10 minutes.
- User impact: slow answers and possible client timeouts.
- First checks: identify the affected window in the dashboard; open a slow trace; find its matching correlation ID in logs.
- Temporary mitigation: disable the suspected incident or reduce concurrency while investigating.
- Owner: Observability team.

## Alert 2 — Elevated API error rate

- Severity: critical
- SLI/SLO: error rate ≤ 2%.
- Condition: error rate exceeds 2% for 5 minutes.
- User impact: requests fail before receiving an answer.
- First checks: inspect error breakdown; open the failing trace; compare with `request_failed` logs.
- Temporary mitigation: roll back the failing configuration or disable the unhealthy dependency.
- Owner: API team.

## Alert 3 — Quality proxy degradation

- Severity: warning
- SLI/SLO: mean quality score ≥ 0.75.
- Condition: mean quality score is below 0.75 for 15 minutes.
- User impact: answers are returned but are less useful.
- First checks: compare prompt label/version; inspect a low-quality trace; compare retrieved docs with the matching log.
- Temporary mitigation: roll back the `production` label to the baseline prompt version.
- Owner: AI team.
