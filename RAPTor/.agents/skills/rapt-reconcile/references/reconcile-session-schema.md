# rapt-reconcile Session Schema

`rapt-reconcile` 每次修復都必須建立 session record，並在修改前保存 snapshot。這能讓修復可追溯，也能清楚描述哪些 finding 被修、哪些被轉交 clarify。

## Output Paths

```text
.raptor/reconcile/sessions/RECON-YYYYMMDD-NNN.yml
.raptor/reconcile/archive/RECON-YYYYMMDD-NNN/<artifact-relative-path>
```

## Session YAML

```yaml
session:
  id: RECON-20260611-001
  started_at: "2026-06-11T15:45:00+08:00"
  source_reports:
    - docs/reports/verify-report.yml
  status: completed | partial | blocked

findings:
  NEED_TO_FIX:
    - FIND-20260611-001
  NEED_TO_CLARIFY:
    - FIND-20260611-002
  NOTE_ONLY:
    - FIND-20260611-003

changes:
  - finding_id: FIND-20260611-001
    artifact: docs/ssot/haapi/order.haapi.yaml
    action: update
    snapshot: .raptor/reconcile/archive/RECON-20260611-001/docs/ssot/haapi/order.haapi.yaml
    summary: 修正 permission id 對齊 haARM。

impact_matrix_updates:
  - id: IMPACT-20260611-001
    status: applied

clarify_payloads:
  - .clarify/batches/CLR-BATCH-20260611-001.yml
```

## Rules

- 修改任何 SSoT 前，先將原檔複製到 archive。
- 每個 applied finding 必須列入 `changes`。
- 每個需使用者決策的 finding 必須列入 `clarify_payloads` 或 `NEED_TO_CLARIFY`。
- 若修復會影響下游 artifact，必須 upsert `.raptor/impact-matrix.yml`。
- session 結束時更新 `.raptor/session.md` 的 reconcile 摘要。
