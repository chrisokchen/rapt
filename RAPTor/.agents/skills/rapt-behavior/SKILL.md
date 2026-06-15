---
name: rapt-behavior
description: "RAPTor Phase 1.5 高階 Gherkin 生成。從 discovery 產出中萃取使用者故事，並生成業務語言的高階 Gherkin feature files（SSoT）。Use when: 完成 /rapt-discovery 後、/rapt-behavior、需要建立 BDD Feature 規格。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: planner
---

# RAPTor Behavior — Phase 1.5 高階 Gherkin

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::ssot-definition.md]
- LOAD REF [rapt-core::cic-note-policy.md]
- LOAD REF [rapt-core::phase-gates.md]
- LOAD REF [rapt-core::traceability-schema.md]

## TRIGGER

- ??????? `rapt-behavior` ??? RAPTor phase?
- ???? artifact ?????? phase ???????????????

## SKIP

- `.raptor/arguments.yml` ???????? `/rapt-kickoff`?
- ?????? worker ? DSL ????????? `rapt-form-*` skill?
- ??????? skill ? Artifact Output Contract?


## PRINCIPLE: CWD 為產出錨點
## PRINCIPLE: Artifact Output Contract（只寫 `${paths.high_gherkin_dir}/**`）
## PRINCIPLE: STRICT SOP
## PRINCIPLE: 長流程待辦（Tier 0 / Tier 1）

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| CREATE / UPDATE | `${paths.high_gherkin_dir}/*.feature` | 高階 Gherkin feature files（SSoT）|
| CREATE / UPDATE | `${paths.high_gherkin_dir}/story-index.md` | Feature 索引與摘要 |
| CREATE / UPDATE | `${paths.traceability_file}` | 僅限 L1/L2 traceability 草稿 |
| UPDATE | `.raptor/session.md` | 更新 Phase 1.5 進度 |
| **DENY** | DBML / haARM / haAPI / haPDL | 不觸碰規格 artifact |
| **DENY** | `generated/` | 不建立 generated artifacts |
| **DENY** | Low-level Gherkin（含 selector / API URL）| 只寫高階業務語言 |

---

## SOP

### 步驟 0：READ arguments.yml + Phase 1 artifacts

```
READ: .raptor/arguments.yml
ASSERT: 存在，否則 EMIT 錯誤「請先執行 /rapt-kickoff」並停止
READ: ${paths.business_discovery_dir}/ — 所有 Phase 1 文件
ASSERT: Phase 1 discovery 存在（至少找到 01-stakeholders.md）
  若不存在 → EMIT 警告「建議先完成 /rapt-discovery」，ASK 是否繼續
```

### 步驟 1：EXECUTE `01-story-extraction/SOP.md`

從 discovery artifact 萃取使用者故事（User Story）。

### 步驟 2：EXECUTE `02-high-level-gherkin/SOP.md`

將 User Story 轉換為高階 Gherkin feature 格式。

LOAD REF [rapt-behavior::rules/high-level-gherkin-rules.md]
LOAD REF [rapt-behavior::rules/cross-cutting-scenario-checklist.md]
LOAD REF [rapt-behavior::rules/test-readiness-gherkin-rules.md]

### 步驟 3：UPDATE traceability L1/L2 草稿

依 `rapt-core::traceability-schema.md` 更新 `${paths.traceability_file}`：

- L1 Requirement Coverage：story/source → feature/scenario。
- L2 Scenario Data Mapping 草稿：scenario_id、feature、scenario、entities、source。
- 不填入沒有證據的 DBML table / field；精確化由 `rapt-modeling`、`rapt-intent` 或 `rapt-reconcile` 完成。

### 步驟 4：VALIDATE Phase 1.5 閘門

LOAD REF [rapt-core::phase-gates.md §Phase 1.5]

逐一檢查閘門條件。  
未通過的項目：記 CiC `GAP`。

### 步驟 5：EMIT 完成通知

```
✅ Phase 1.5 High-Level Gherkin 完成！

產出：
- ${high_gherkin_dir}/*.feature（{N} 個）
- ${high_gherkin_dir}/story-index.md

品質閘門：PASS / PARTIAL

建議下一步：執行 /rapt-modeling 建立資料模型
```
