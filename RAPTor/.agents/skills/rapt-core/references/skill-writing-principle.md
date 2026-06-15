# RAPTor Skill Writing Principle

本文件提供所有 `rapt-*` skill 改版時的共用撰寫規則。

## Frontmatter

每個 `SKILL.md` 應在 frontmatter 中標示：

```yaml
---
name: rapt-example
description: "..."
skill-type: planner | worker | verifier | utility | preview
---
```

## 必備段落

每個 skill 至少包含下列段落：

1. `## TRIGGER`
2. `## SKIP`
3. `## PRINCIPLE`
4. `## Artifact Output Contract`
5. `## Inputs`
6. `## Workflow`
7. `## Exit Report`

## Long Process Discipline

- 超過 5 個步驟的工作，必須先建立可更新的 TODO/checklist。
- 每完成一個 phase gate，先輸出 findings 分流：`NEED_TO_FIX`、`NEED_TO_CLARIFY`、`NOTE_ONLY`。
- 若即將進入長時間批次處理，先保存當前 target、inputs、已完成項目與下一步。
- 使用者要求「照計畫執行」時，不停在建議；除非觸及 destructive action 或需要業務決策。

## Verb Discipline

- `READ`：只讀取 artifact。
- `DERIVE`：根據已讀內容推導中間結果。
- `ASSERT`：檢查必要條件，不修改檔案。
- `EMIT`：輸出給使用者或報告，不代表寫檔。
- `CREATE`：建立新 artifact。
- `UPDATE`：修改既有 artifact。
- `DENY`：明確禁止寫入。
- `ASK`：要求使用者決策，不自行假設。
- `DELEGATE`：Planner 將 payload 交給 Worker。

## Worker Failure Contract

Worker 無法完成時，不可沉默失敗，也不可自行擴張修改範圍。必須回傳：

```yaml
worker_result:
  status: failed
  failure_kind: invalid_payload | missing_evidence | contract_violation | dsl_lint_failed | unsupported_case
  target_path: docs/ssot/habdd/user.ha.feature
  message: 缺少 source_evidence，無法安全產生 DSL。
  required_action: 請 Planner 補上 discovery 或 clarify decision 來源。
```
