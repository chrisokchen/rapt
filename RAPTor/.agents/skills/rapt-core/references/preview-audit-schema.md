# Preview Audit Schema

Preview skill 只產生 generated artifact，但必須同步輸出 audit，說明它看到的 SSoT 缺口與轉換假設。

## Output Files

| Skill | Generated Output | Audit Output |
|---|---|---|
| `rapt-openapi` | `docs/generate/openapi/openapi.yaml` | `docs/generate/openapi/openapi-audit.yml` |
| `rapt-lofi` | `docs/generate/lofi/index.html` | `docs/generate/lofi/scope-audit.yml` |
| `rapt-design-brief` | `docs/generate/designbrief/design-brief.md` | `docs/generate/designbrief/style-profile.yml` |

## Audit Shape

```yaml
audit:
  id: PREVIEW-20260611-001
  skill: rapt-openapi
  generated_at: "2026-06-11T16:00:00+08:00"
  source_artifacts:
    - docs/ssot/haapi/user.haapi.yaml
  output_artifact: docs/generate/openapi/openapi.yaml
  status: ok | partial | blocked
  assumptions:
    - 使用 schema_version 3.3 預設 mapping。
  findings:
    - id: PREVIEW-FIND-001
      route: NEED_TO_FIX | NEED_TO_CLARIFY | NOTE_ONLY
      can_fix: false
      artifact: docs/ssot/haapi/user.haapi.yaml
      location: exposes.operations.approve
      summary: operation 缺少 response example，OpenAPI 使用 generic response。
```

## Rules

- Preview audit 不直接修改 SSoT。
- audit finding 若影響下游開發，應交給 `rapt-verify` 或 `rapt-reconcile`。
- 若 source SSoT 缺失導致 generated output 不可信，`status` 必須是 `partial` 或 `blocked`。
