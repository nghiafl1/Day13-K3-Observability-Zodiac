# Alert runbook

## high_latency_p95

- Severity/owner: warning, Observability team.
- Trigger: P95 request latency exceeds 3000 ms for 10 minutes.
- Investigate: identify the affected dashboard window, open a slow Langfuse trace and waterfall, then search the matching `correlation_id` in `data/logs.jsonl`.
- Mitigate: disable the suspected incident, reduce concurrency, or use a cached/fallback response.
- Prevent recurrence: set a retrieval timeout and alert on dependency/span latency before end-to-end P95 is breached.

## elevated_error_rate

- Severity/owner: critical, API team.
- Trigger: error rate exceeds 2% for 5 minutes.
- Investigate: inspect `error_breakdown`, open a failing trace, and compare it with the `request_failed` log for the same correlation ID.
- Mitigate: roll back the failing configuration or disable the unhealthy dependency.
- Prevent recurrence: add dependency health checks, bounded retries, and an error-budget alert.

## cost_budget_exceeded

- Severity/owner: warning, AI team.
- Trigger: total daily cost exceeds 2.50 USD.
- Investigate: group traces by model, feature, prompt label/version, token usage and cost.
- Mitigate: throttle high-cost traffic, cap output tokens, or roll back an expensive prompt/model change.
- Prevent recurrence: enforce per-request token limits and alert before 80% of the daily budget.

## quality_proxy_degradation

- Severity/owner: warning, AI team.
- Trigger: mean quality score is below 0.75 for 15 minutes.
- Investigate: compare prompt label/version, inspect low-quality traces, and compare retrieved documents with matching logs.
- Mitigate: roll `production` back to the baseline prompt version.
- Prevent recurrence: canary prompt versions and gate promotion on the quality proxy.
