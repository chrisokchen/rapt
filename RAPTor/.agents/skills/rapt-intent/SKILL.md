---
name: rapt-intent
description: "RAPTor Phase 4 意圖規格制定。從 DBML + haARM + Gherkin 切分 API 意圖（haAPI）和頁面意圖（haPDL），生成意圖層 SSoT。Use when: 完成 /rapt-clarify 後、/rapt-intent、需要生成 haAPI/haPDL 規格。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: planner
---

# RAPTor Intent — Phase 4 意圖規格制定

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::ssot-definition.md]
- LOAD REF [rapt-core::dsl-cross-reference-v33.md]
- LOAD REF [rapt-core::planner-worker-contract.md]
- LOAD REF [rapt-core::cic-note-policy.md]
- LOAD REF [rapt-core::phase-gates.md]
- LOAD REF [rapt-core::traceability-schema.md]

## TRIGGER

- ??????? `rapt-intent` ??? RAPTor phase?
- ???? artifact ?????? phase ???????????????

## SKIP

- `.raptor/arguments.yml` ???????? `/rapt-kickoff`?
- ?????? worker ? DSL ????????? `rapt-form-*` skill?
- ??????? skill ? Artifact Output Contract?


## PRINCIPLE: CWD 為產出錨點
## PRINCIPLE: Artifact Output Contract（只寫 backend_intent_dir / frontend_intent_dir + traceability）
## PRINCIPLE: STRICT SOP
## PRINCIPLE: 長流程待辦（Tier 0 / Tier 1）

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| CREATE / UPDATE | `${paths.backend_intent_dir}/*.haapi.yaml` | haAPI（SSoT）|
| CREATE / UPDATE | `${paths.frontend_intent_dir}/*.hapdl.yaml` | haPDL（SSoT）|
| CREATE / UPDATE | `${paths.traceability_file}` | 可追蹤性矩陣 |
| UPDATE | `.raptor/session.md` | 更新 Phase 4 進度 |
| **DENY** | haARM 直接修改 | 需透過 rapt-reconcile 或 rapt-clarify |
| **DENY** | DBML / Gherkin | 只讀不寫 |
| **DENY** | `generated/` | 不建立 generated artifacts |

---

## SOP

### 步驟 0：READ arguments.yml + Phase 2/3 artifacts

```
READ: .raptor/arguments.yml
ASSERT: .raptor/session.md Phase 3 閘門已通過（或 EMIT 警告）
READ: ${paths.data_model_dir}/*.dbml
READ: ${paths.data_model_dir}/glossary.md
READ: ${paths.data_model_dir}/seeds.md（若存在）
READ: ${paths.data_model_dir}/constraints.md（若存在）
READ: ${paths.access_control_dir}/*.haarm.yaml
READ: ${paths.high_gherkin_dir}/*.feature
READ: ${paths.traceability_file}（若存在）
```

### 步驟 1：EXECUTE `01-api-intent-slicing/SOP.md`

從 DBML + haARM + Gherkin 切分 API 意圖。

### 步驟 2：EXECUTE `02-page-intent-slicing/SOP.md`

從 API intent + Gherkin 切分頁面意圖。

### 步驟 3：EXECUTE `03-haapi-render/SOP.md`

LOAD REF [rapt-intent::rules/haapi-v33-rules.md]  
生成 haAPI，DELEGATE to `rapt-form-haapi`。

### 步驟 4：EXECUTE `04-hapdl-render/SOP.md`

LOAD REF [rapt-intent::rules/hapdl-v33-rules.md]  
生成 haPDL，DELEGATE to `rapt-form-hapdl`。

### 步驟 5：UPDATE traceability L2/L3

依 `rapt-core::traceability-schema.md`：

- 用 glossary canonical mapping 將 Gherkin `# entities:` 精確化到 DBML table。
- 用 haAPI / haPDL 的 source_evidence 補全 L3 Intent Mapping。
- 可由 haAPI operation 的 entity / fields / constraints 補 L2 read_tables、write_tables、fields、constraints。
- 證據不足時保留低信心，不得硬猜。

### 步驟 6：VALIDATE Phase 4 閘門

LOAD REF [rapt-core::phase-gates.md §Phase 4]

### 步驟 7：EMIT 完成通知

```
✅ Phase 4 Spec Formulation 完成！

產出：
- ${backend_intent_dir}*.haapi.yaml（{N} 個）
- ${frontend_intent_dir}*.hapdl.yaml（{M} 個）
- ${traceability_file}（初稿）

品質閘門：PASS / PARTIAL

建議下一步：執行 /rapt-verify 進行規格驗證
```
