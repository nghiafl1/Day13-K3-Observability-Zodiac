# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: Zodiac
- Repository URL: https://github.com/nghiafl1/Day13-K3-Observability-Zodiac
- Commit SHA cuối:
- Thành viên và vai trò: Nguyễn Huy Nghĩa (2A202601943) — phụ trách Checkpoint 2.

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100 (xem `submission/evidence/checkpoint1-validator.txt`; tái tạo bằng `python scripts/generate_checkpoint1_logs.py`)
- Tổng số traces: tối thiểu 20 traces đã gửi lên Langfuse
- Số PII leak còn lại: 0
- Dashboard: `http://127.0.0.1:8000/dashboard`
- `validate_dashboard.py`: HỢP LỆ: 6/6 panel

## 3. Logging và tracing

- Evidence correlation ID: `data/logs.jsonl`
- Evidence PII redaction: `data/logs.jsonl`
- Evidence trace waterfall: `submission/evidence/trace-baseline-v1.png`
- Trace đã xác minh: `d97b598b925b4639b59253c88d41e206`
- Metadata: `prompt_name=day13-chat`, `prompt_label=production`, `prompt_version=1`, `prompt_source=langfuse`.

## 4. Prompt versioning

- Prompt name: `day13-chat`
- Version/label baseline: v1 / `baseline`, `production`
- Version/label candidate: v2 / `candidate`
- Trace ID baseline v1: `d97b598b925b4639b59253c88d41e206`
- Trace ID candidate v2: `a9eaea7db4ca1f5504a8225de0e0f088`
- Trace ID production v2 trước rollback: `03449f05113c31dbb82cb1680e0829f9`
- Trace ID production v1 sau rollback: `46530b7612ac337fa54df14014f401f6`
- Bằng chứng đổi label/rollback: `submission/evidence/prompt-rollback.png`

## 5. Điều tra challenge (CP3)

- Challenge ID: `day13-k3-observability-v1`
- Incident chính thức: `rag_slow`; feature bị ảnh hưởng: `refund`.
- Triệu chứng từ metrics: 5 request thành công, nhưng `latency_p50=3579 ms`, `latency_p95=4685 ms` và `latency_p99=4685 ms`. P95 vượt ngưỡng challenge `2000 ms`; không có error (`error_breakdown={}`, `error_rate_pct=0.0`). Xem `submission/evidence/challenge-metrics.txt`.
- Trace/waterfall: Langfuse đã được flush sau khi chạy. Trace ID `e8daea2a1f5cf3fe1385b67fe765d521` (session `k3-challenge-s02`, `correlation_id=req-b1569811`) cho thấy span `run` mất `4.69 s`; metadata có prompt name/label/version và correlation ID. Ảnh: `submission/evidence/challenge-trace-waterfall.png`.
- Log/correlation evidence: `req-b1569811` (session `k3-challenge-s02`) có cặp `request_received` → `response_sent` với `latency_ms=4685`; bốn request còn lại có latency 3522–3741 ms. Tất cả đều có `feature=refund`, `session_id`, `user_id_hash`, `model`, `env` và `correlation_id`. Xem `submission/evidence/challenge-log-correlation.txt`.
- Root cause: `app/mock_rag.py`, hàm `retrieve()`, chủ động gọi `time.sleep(2.5)` khi `STATE["rag_slow"]` bật. Dấu hiệu này phù hợp với P95 tăng cao trong khi error rate vẫn 0%.
- Fix action: đặt timeout và retry/backoff có giới hạn cho retrieval; dùng fallback cached answer khi vector retrieval chậm.
- Preventive measure: alert khi retrieval latency/P95 vượt SLO, theo dõi span retrieval trên Langfuse, canary load test cho feature `refund` trước release.
- Evidence lệnh chạy và tắt incident: `submission/evidence/challenge-run.txt`.

## 6. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: `HỢP LỆ: 6/6 panel`
- Evidence dashboard: `submission/evidence/dashboard.png`
- Evidence validator: `submission/evidence/dashboard-validator.png`
- SLO: latency P95 ≤ 3000 ms, error rate ≤ 2%, daily cost ≤ 2.5 USD, quality average ≥ 0.75.
- Alert rules và runbook: `config/alert_rules.yaml`, `docs/alerts.md`

## 7. Đóng góp cá nhân

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| Phạm Thế Dũng (2A202601985) | CP1: correlation ID, log enrichment và PII scrubbing. | `be391d6`, `f0b1104` | Structured JSON logs, request context và che PII trước khi ghi log. |
| Nguyễn Huy Nghĩa (2A202601943) | CP2: Langfuse trace/prompt workflow, dashboard, SLO, alert rules và runbook. | `70bd7a2` | Liên kết traces, prompt versioning, dashboard và SLO/alert có thể vận hành. |
| Phạm Văn Lưu (2A202601857) | CP3: chạy official challenge, điều tra Metrics → Traces → Logs, lưu evidence, đề xuất fix/preventive measure; bổ sung tiêu chí còn thiếu cho rubric. | `e46c34b`, `f2d0234`, `32fd7d5` | Dùng P95 để nhận biết latency incident, dùng trace khoanh vùng và correlation ID/log để chứng minh root cause. |
