# RAPTor Finding Taxonomy

本文件定義 `rapt-verify`、`rapt-reconcile`、`rapt-RAscore` 與各 Planner skill 共同使用的問題分類。所有 finding 必須能被分流到「可修、需問、僅記錄」三類之一，避免 phase gate 結束時留下無法執行的模糊描述。

## Finding YAML Shape

```yaml
findings:
  - id: FIND-YYYYMMDD-001
    severity: blocker | high | medium | low | info
    category: missing_source | contradiction | trace_gap | dsl_invalid | generated_drift | policy_violation | naming_drift | evidence_weak
    route: NEED_TO_FIX | NEED_TO_CLARIFY | NOTE_ONLY
    can_fix: true
    owner_skill: rapt-modeling
    artifact: docs/ssot/dbml/schema.dbml
    location: Table User
    summary: 使用者角色欄位缺少 haARM 對應權限來源
    evidence:
      - docs/discovery/02-story-index.md#US-004
    suggested_action: 補上 role/permission 對應，或建立 clarify 問題確認角色邊界。
```

## Route Rules

| route | 使用時機 | 下一步 |
|---|---|---|
| `NEED_TO_FIX` | 已有足夠 evidence，且修正落在 Artifact Output Contract 允許範圍 | 交給 `rapt-reconcile` 或原 owner skill 修正 |
| `NEED_TO_CLARIFY` | 缺少業務決策、來源互相矛盾、或修正會改變需求語意 | 交給 `rapt-clarify` 產生 question pack |
| `NOTE_ONLY` | 不阻擋後續流程，但值得列入報告或 RAscore | 留在 report，不觸發修復 |

## Required Behavior

- 每筆 finding 都必須有 `route` 與 `can_fix`。
- `can_fix: true` 只能搭配明確 artifact、location、evidence 與 suggested_action。
- `policy_violation` 預設視為 `NEED_TO_FIX`；若涉及需求取捨，改為 `NEED_TO_CLARIFY`。
- `generated_drift` 不可直接修改 SSoT，除非 finding 同時指出 SSoT 本身也有錯。
