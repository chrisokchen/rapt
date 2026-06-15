# RAscore Action Map

RAscore findings 是 advisory-only，但每筆 finding 必須能導向明確下一步。

## Action Types

| recommended_action_type | route | owner_skill | 說明 |
|---|---|---|---|
| `traceability_mapping` | NEED_TO_FIX | `rapt-reconcile` | 補齊 story/scenario/API/PDL trace |
| `dsl_lint_fix` | NEED_TO_FIX | 對應 `rapt-form-*` | 修正 DSL 格式或命名 |
| `source_evidence_gap` | NEED_TO_CLARIFY | `rapt-clarify` | 缺少來源或 evidence |
| `business_rule_conflict` | NEED_TO_CLARIFY | `rapt-clarify` | 業務規則互相矛盾 |
| `skill_gap` | NOTE_ONLY | skills backlog | 重複 finding 顯示 skill 規則不足 |
| `manual_review` | NEED_TO_CLARIFY | domain owner | 無法安全自動判斷 |

## Required Fields

```json
{
  "id": "RA-FIND-001",
  "severity": "high",
  "category": "traceability",
  "artifact": "docs/ssot/habdd/case-review.ha.feature",
  "location": "Scenario: 主管核准待覆核案件",
  "issue": "Scenario 缺少 haAPI mapping",
  "recommendation": "補上 traceability mapping",
  "owner_skill": "rapt-reconcile",
  "recommended_action_type": "traceability_mapping",
  "route": "NEED_TO_FIX",
  "can_fix": true
}
```

## Rules

- `recommended_action_type` 必須能映射到 `route`。
- 若無法判斷 `can_fix`，預設 `can_fix: false` 並 route 到 `NEED_TO_CLARIFY`。
- `skill_gap` 不直接修專案 artifact，應記入 skill improvement backlog。
