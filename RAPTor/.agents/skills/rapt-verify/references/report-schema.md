# rapt-verify Report Schema

`rapt-verify` 必須同時輸出 human-readable markdown 與 machine-readable YAML。Markdown 給人閱讀；YAML 給 `rapt-reconcile`、`rapt-clarify`、`rapt-RAscore` 與自動化工具使用。

## Output Paths

| Path | Purpose |
|---|---|
| `${paths.reports_dir}/verify-report.md` | 人讀摘要 |
| `${paths.reports_dir}/verify-report.yml` | 機器可讀 findings 與 phase gate |

## YAML Shape

```yaml
report:
  id: VERIFY-20260611-001
  project: sample-project
  generated_at: "2026-06-11T15:30:00+08:00"
  status: PASS | PARTIAL | FAIL
  schema_version: 2

summary:
  completeness: PASS | PARTIAL | FAIL
  consistency: PASS | PARTIAL | FAIL
  traceability: PASS | PARTIAL | FAIL
  coverage: PASS | PARTIAL | FAIL
  error_count: 0
  warning_count: 0

findings:
  - id: FIND-20260611-001
    severity: blocker | high | medium | low | info
    category: missing_source | contradiction | trace_gap | dsl_invalid | generated_drift | policy_violation | naming_drift | evidence_weak
    route: NEED_TO_FIX | NEED_TO_CLARIFY | NOTE_ONLY
    can_fix: true
    owner_skill: rapt-intent
    artifact: docs/ssot/haapi/order.haapi.yaml
    location: access.endpoints.list.required_permissions
    summary: haAPI permission id 不存在於 haARM。
    evidence:
      - docs/ssot/haarm/access.haarm.yaml#permissions
    suggested_action: 修正 permission id，或由 rapt-reconcile 建立明確 backfill plan。

phase_gate:
  can_continue: false
  blockers:
    - FIND-20260611-001
  next:
    NEED_TO_FIX:
      - FIND-20260611-001
    NEED_TO_CLARIFY: []
    NOTE_ONLY: []
```

## Markdown Sections

Markdown 報告必須包含：

1. Status Summary
2. Phase Gate
3. NEED_TO_FIX
4. NEED_TO_CLARIFY
5. NOTE_ONLY
6. RAscore Readiness
7. Next Actions

## Finding Rules

- 每筆 finding 必須符合 `rapt-core::finding-taxonomy.md`。
- `route` 與 `can_fix` 為必填。
- `NEED_TO_FIX` 表示已有足夠 evidence，可由 reconcile 或 owner skill 修復。
- `NEED_TO_CLARIFY` 表示需要使用者或 domain owner 決策，不得由工具假設。
- `NOTE_ONLY` 不阻擋流程，但保留在 report。

## Status Rules

| Status | Meaning |
|---|---|
| `PASS` | 無 blocker/high/medium finding，或只剩 NOTE_ONLY |
| `PARTIAL` | 有 warning 或 medium finding，但不阻擋下一 phase |
| `FAIL` | 有 blocker/high finding，或 phase gate 不允許繼續 |
