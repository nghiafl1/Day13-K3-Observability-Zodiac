# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: K3
- Repository URL:
- Commit SHA cuối:
- Thành viên và vai trò:

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100
- Tổng số traces: tối thiểu 20 traces đã gửi lên Langfuse
- Số PII leak còn lại: 0
- Dashboard: `http://127.0.0.1:8000/dashboard`
- `validate_dashboard.py`: HỢP LỆ: 6/6 panel

## 3. Logging và tracing

- Evidence correlation ID: `data/logs.jsonl`
- Evidence PII redaction: `data/logs.jsonl`
- Evidence trace waterfall: `submission/evidence/trace-baseline-v1.png`
- Trace đã xác minh: `d97b598b925b4639b59253c88d41e206`
- Metadata trace xác minh: `prompt_name=day13-chat`, `prompt_label=production`, `prompt_version=1`, `prompt_source=langfuse`.

## 4. Prompt versioning

- Prompt name: `day13-chat`
- Version/label baseline: v1 / `baseline`, `production`
- Version/label candidate: v2 / `candidate`
- Trace ID baseline v1: `d97b598b925b4639b59253c88d41e206`
- Trace ID candidate v2: `a9eaea7db4ca1f5504a8225de0e0f088`
- Trace ID production v2 trước rollback: `03449f05113c31dbb82cb1680e0829f9`
- Trace ID production v1 sau rollback: `46530b7612ac337fa54df14014f401f6`
- Bằng chứng đổi label/rollback: `submission/evidence/prompt-rollback.png`

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: `HỢP LỆ: 6/6 panel`
- Evidence dashboard: `submission/evidence/dashboard.png`
- Evidence validator: `submission/evidence/dashboard-validator.txt`
- SLO: latency P95 ≤ 3000 ms, error rate ≤ 2%, daily cost ≤ 2.5 USD, quality average ≥ 0.75.
- Alert rules và runbook: `config/alert_rules.yaml`, `docs/alerts.md`

## 6. Đóng góp cá nhân

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| Phạm Thế Dũng (2A202601985) | Checkpoint 1: correlation ID, log enrichment và PII scrubbing; Checkpoint 2: dashboard, SLO, alert/runbook và prompt version workflow. | `COMMIT_SHA_CP1` | Logging có cấu trúc, tracing, prompt versioning, dashboard SLO và incident evidence. |
