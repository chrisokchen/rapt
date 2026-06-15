---
name: rapt-modeling
description: "RAPTor Phase 2 領域建模。從 discovery + Gherkin 產出建立 annotated DBML（資料模型 SSoT）與 haARM（存取控制 SSoT）。Use when: 完成 /rapt-behavior 後、/rapt-modeling、需要建立資料模型或 RBAC 規格。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: planner
---

# RAPTor Modeling — Phase 2 領域建模

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::ssot-definition.md]
- LOAD REF [rapt-core::dsl-cross-reference-v33.md]
- LOAD REF [rapt-core::cic-note-policy.md]
- LOAD REF [rapt-core::phase-gates.md]
- LOAD REF [rapt-core::traceability-schema.md]

## TRIGGER

- ??????? `rapt-modeling` ??? RAPTor phase?
- ???? artifact ?????? phase ???????????????

## SKIP

- `.raptor/arguments.yml` ???????? `/rapt-kickoff`?
- ?????? worker ? DSL ????????? `rapt-form-*` skill?
- ??????? skill ? Artifact Output Contract?


## PRINCIPLE: CWD 為產出錨點
## PRINCIPLE: Artifact Output Contract（只寫 `${paths.data_model_dir}/**` 和 `${paths.access_control_dir}/**`）
## PRINCIPLE: STRICT SOP
## PRINCIPLE: 長流程待辦（Tier 0 / Tier 1）

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| CREATE / UPDATE | `${paths.data_model_dir}/*.dbml` | Annotated DBML（SSoT）|
| CREATE / UPDATE | `${paths.data_model_dir}/glossary.md` | 統一語言詞彙表 |
| CREATE / UPDATE | `${paths.data_model_dir}/seeds.md` | 代碼值域 / 狀態集合 / 位元旗標定義 |
| CREATE / UPDATE | `${paths.data_model_dir}/constraints.md` | 業務約束 / 狀態轉換 / 服務層補償規則 |
| CREATE / UPDATE | `${paths.access_control_dir}/*.haarm.yaml` | haARM（SSoT）|
| UPDATE | `.raptor/session.md` | 更新 Phase 2 進度 |
| **DENY** | Gherkin / haAPI / haPDL | 不觸碰意圖層 artifact |
| **DENY** | `generated/` | 不建立 generated artifacts |

---

## SOP

### 步驟 0：READ arguments.yml + Phase 1.5 artifacts

```
READ: .raptor/arguments.yml
ASSERT: 存在，否則 EMIT 錯誤「請先執行 /rapt-kickoff」並停止
READ: ${paths.high_gherkin_dir}/*.feature
READ: ${paths.business_discovery_dir}/
ASSERT: 至少一個 .feature 檔案存在（或 EMIT 警告，ASK 是否繼續）
```

### 步驟 1：EXECUTE `01-entity-and-aggregate/SOP.md`

識別實體、Aggregate 與邊界。

### 步驟 2：EXECUTE `02-annotated-dbml/SOP.md`

LOAD REF [rapt-modeling::rules/dbml-v33-annotation-rules.md]  
LOAD REF [rapt-modeling::rules/ref-code-and-seed-rules.md]  
LOAD REF [rapt-modeling::rules/constraint-modeling-rules.md]  
LOAD REF [rapt-modeling::rules/compatibility-modeling-rules.md]  
生成 annotated DBML，DELEGATE to `rapt-form-dbml`。

### 步驟 3：WRITE seeds / constraints support artifacts

依 DBML 與 Gherkin 中的狀態、代碼、位元旗標、引用限制，建立：

- `${paths.data_model_dir}/seeds.md`
- `${paths.data_model_dir}/constraints.md`

若值域或限制規則無法確認，建立 CiC，不得只寫自然語言 Note。

### 步驟 4：EXECUTE `03-ubiquitous-language/SOP.md`

建立統一語言詞彙表。

### 步驟 5：EXECUTE `04-bounded-context/SOP.md`

確立 Bounded Context 邊界（與 DBML 對齊）。

### 步驟 6：EXECUTE `05-haarm/SOP.md`

LOAD REF [rapt-modeling::rules/haarm-v33-rules.md]  
生成 haARM，DELEGATE to `rapt-form-haarm`。

### 步驟 7：VALIDATE Phase 2 閘門

LOAD REF [rapt-core::phase-gates.md §Phase 2]

### 步驟 8：EMIT 完成通知

```
✅ Phase 2 Domain Modeling 完成！

產出：
- ${data_model_dir}schema.dbml
- ${data_model_dir}glossary.md
- ${data_model_dir}seeds.md
- ${data_model_dir}constraints.md
- ${access_control_dir}{project_name}.haarm.yaml

品質閘門：PASS / PARTIAL

建議下一步：執行 /rapt-clarify 解決所有 CiC 便條
```
