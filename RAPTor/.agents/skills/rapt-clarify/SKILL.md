---
name: rapt-clarify
description: "RAPTor Phase 3 釐清流程。掃描所有 SSoT 中的 CiC 便條（GAP/ASM/BDY/CON），打包成問題集，與使用者進行釐清 session，並將決策套用回 SSoT。Use when: 完成 /rapt-modeling 後、/rapt-clarify、有 CiC 便條需要處理、SSoT 中有疑問需要確認。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: planner
---

# RAPTor Clarify — Phase 3 釐清流程

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::cic-note-policy.md]
- LOAD REF [rapt-core::phase-gates.md]
- LOAD REF [rapt-core::rascore-feedback-policy.md]

## TRIGGER

- ??????? `rapt-clarify` ??? RAPTor phase?
- ???? artifact ?????? phase ???????????????

## SKIP

- `.raptor/arguments.yml` ???????? `/rapt-kickoff`?
- ?????? worker ? DSL ????????? `rapt-form-*` skill?
- ??????? skill ? Artifact Output Contract?


## PRINCIPLE: CWD 為產出錨點
## PRINCIPLE: Artifact Output Contract
## PRINCIPLE: STRICT SOP
## PRINCIPLE: 長流程待辦（Tier 0 / Tier 1）

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| CREATE / UPDATE | `${paths.clarify_dir}backlog.md` | CiC 問題 backlog |
| CREATE / UPDATE | `${paths.clarify_dir}decisions/` | 決策記錄（每個 session 一個檔案）|
| UPDATE（僅 04-decision-apply）| DBML / haARM / Gherkin | 依 decision log 回寫 SSoT |
| UPDATE（僅 04-decision-apply）| `${paths.business_discovery_dir}/**` | 僅限 CiC 狀態、decision reference、scope 同步段 |
| UPDATE（僅 04-decision-apply）| `${paths.data_model_dir}/seeds.md` | 依決策回寫值域 / 狀態 / 位元旗標 |
| UPDATE（僅 04-decision-apply）| `${paths.data_model_dir}/constraints.md` | 依決策回寫業務約束 |
| UPDATE（僅 04-decision-apply）| `${paths.traceability_file}` | 依決策回寫 deferred / decision traceability |
| UPDATE | `.raptor/session.md` | 更新 Phase 3 進度 |
| **DENY**（01-03 步驟）| 任何 SSoT artifact | 只有 04 才可回寫 |
| **DENY** | haAPI / haPDL | 不觸碰意圖層 |

---

## SOP

### 步驟 0：READ arguments.yml

```
READ: .raptor/arguments.yml
ASSERT: 存在，否則 EMIT 錯誤並停止
```

### 步驟 1：EXECUTE `01-gap-scan/SOP.md`

掃描所有 SSoT artifact 中的 CiC 便條，建立 backlog。

若存在 RAscore findings，依 `rapt-clarify::rules/rascore-finding-scan.md` 一併轉成 backlog。

### 步驟 2：EXECUTE `02-question-packaging/SOP.md`

將 backlog 打包成有優先序的問題集。

RAscore 來源問題使用 `rapt-clarify::templates/rascore-question-pack.md`。

### 步驟 3：EXECUTE `03-clarification-session/SOP.md`

與使用者進行 ASK session，記錄決策。

### 步驟 4：EXECUTE `04-decision-apply/SOP.md`

將決策套用回 SSoT。

### 步驟 5：VALIDATE Phase 3 閘門

LOAD REF [rapt-core::phase-gates.md §Phase 3]

### 步驟 6：EMIT 完成通知

```
✅ Phase 3 Clarification 完成！

處理的 CiC：
- GAP：{X} 個（已解決）
- ASM：{Y} 個（已確認）
- BDY：{Z} 個（已轉 reconcile）
- CON：{W} 個（已裁決）

品質閘門：PASS / PARTIAL

建議下一步：執行 /rapt-intent 生成意圖層規格
```
