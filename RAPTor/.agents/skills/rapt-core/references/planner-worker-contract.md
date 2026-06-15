# Planner / Worker 合約

RAPTor skill 家族分為兩類角色：**Planner**（決策與協調）與 **Worker**（純渲染）。本文件定義兩者的職責邊界與 payload 合約。

---

## 角色定義

### Planner Skills（規劃者）

> `rapt-discovery`, `rapt-behavior`, `rapt-modeling`, `rapt-clarify`, `rapt-intent`, `rapt-verify`, `rapt-reconcile`, `rapt-kickoff`

Planner skills 的職責：
- 執行多步驟 SOP，協調多個 sub-SOP
- 分析輸入 artifact，做推斷與決策
- 組裝完整的 **payload**，再 DELEGATE 給 Worker
- 可 ASK 使用者，可記 CiC 便條

### Worker Skills（渲染者）

> `rapt-form-dbml`, `rapt-form-haarm`, `rapt-form-gherkin`, `rapt-form-haapi`, `rapt-form-hapdl`

Worker skills 的職責：
- **僅**依照 Planner 提供的 payload 渲染輸出
- 格式化輸出（套用 DSLspec 格式規則）
- **不推斷、不填補、不擴展** payload 以外的內容

---

## Payload 合約

### Planner → Worker DELEGATE 時必須提供

```yaml
payload:
  target_path: <絕對或相對路徑>        # Worker 唯一可寫入的路徑
  source_evidence:                     # 必填，可追溯性錨點
    - type: discovery | gherkin | modeling | clarify_decision
      ref: <引用的文件或節點>
      excerpt: <原始文字摘錄（可選）>
  content:                             # 完整內容物料（不含格式）
    # ... 依各 Worker spec 定義
  dsl_version: "3.3.0"                 # 必填，防止版本偏移
  write_mode: create | update | append # 預設 create
```

### Worker 的絕對禁止事項

| 禁止 | 原因 |
|------|------|
| 推斷 payload 未提供的欄位值 | Worker 不持有業務語意，推斷必然不準確 |
| 在 target_path 以外寫入任何路徑 | 超出合約範圍 |
| 新增 payload 未明示的 entity / resource / role | 同上 |
| 呼叫 `ASK` 向使用者澄清 | 語意問題應由 Planner 在 DELEGATE 前解決 |
| 修改 haARM（除非明確為 `rapt-form-haarm`）| 跨切面 SSoT 只能由 Planner 授權 Worker 更新 |
| 使用棄用欄位（`access.permissions`、`security.permissions`）| 見 dsl-cross-reference-v33.md |

---

## source_evidence 規則

- `source_evidence` 是 **必填**（mandatory），不得省略。
- Planner 在組裝 payload 前，必須能明確指出每個輸出元素的來源（discovery doc / feature / decision log）。
- 若某欄位值**無法追溯到任何 source**，Planner 應先記 CiC `GAP`，**不得** hardcode 填入。

---

## 例外：`rapt-clarify/04-decision-apply`

- `04-decision-apply` 是 Planner sub-SOP 中唯一**可以回寫 SSoT**（DBML / haARM / Gherkin）的步驟。
- 但仍需：（1）Decision log 中有明確決策紀錄，（2）`target_path` 明確，（3）`source_evidence` 指向 decision log。
- **禁止**在 `01-03` 步驟中回寫任何 SSoT。
