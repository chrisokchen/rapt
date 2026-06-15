# RAPTor Kickoff Plan — smallBiz

> 建立日期：2026-06-12
> CWD：projects/smallBiz-Fable/
> arguments_schema_version: 2

## 1. Project 設定（使用者已確認）

| 欄位 | 值 |
|---|---|
| project.name | smallBiz |
| project.description | 月租制、開箱即用的 B2C 電商平台，讓台灣中小零售商家自有線上商店、自管商品訂單與會員資料。 |
| project.language | zh-hant |
| project.mode | greenfield |
| paths.docs_dir | docs/ |

需求來源材料（已存在，僅 READ）：

- `raw-input/1-initPlan.md` — SmallBiz 電商平台開發構想書（v0.3 草稿）
- `raw-input/2-meetUsers.md` — 使用者訪談紀錄
- `raw-input/3-draftSpec.md` — 規格草稿

## 2. 即將寫入的 arguments.yml（YAML preview）

```yaml
arguments_schema_version: 2

project:
  name: smallBiz
  description: 月租制、開箱即用的 B2C 電商平台，讓台灣中小零售商家自有線上商店、自管商品訂單與會員資料。
  language: zh-hant
  mode: greenfield

paths:
  docs_dir: docs/
  discovery_dir: docs/discovery/
  reports_dir: docs/reports/
  clarify_dir: .clarify/
  traceability_file: .raptor/traceability.md
  impact_matrix_file: .raptor/impact-matrix.yml

  ssot_dir: docs/ssot/
  data_model_dir: docs/ssot/dbml/
  high_gherkin_dir: docs/ssot/habdd/
  access_control_dir: docs/ssot/haarm/
  backend_intent_dir: docs/ssot/haapi/
  frontend_intent_dir: docs/ssot/hapdl/

generated:
  status: deferred
  generated_dir: docs/generate/
  pdl_dir: docs/generate/pdl/
  low_gherkin_dir: docs/generate/isabdd/
  openapi_dir: docs/generate/openapi/
  lofi_dir: docs/generate/lofi/
  designbrief_dir: docs/generate/designbrief/

dsl_versions:
  dbml: "3.3.0"
  habdd: "3.3.0"
  haarm: "3.3.0"
  haapi: "3.3.0"
  hapdl: "3.3.0"

anchors:
  dslspec_root: RAPTor/DSLspec
  req_process_root: RAPTor/0_reqDevProcess
  templates_root: RAPTor/0_reqDevProcess/templates
  prompts_root: RAPTor/0_prompts

policy:
  write_mode: deny-by-default
  clarify_batch_size: 5
  cic_notes_enabled: true
```

## 3. v2 docs layout 預覽

```text
docs/
  discovery/        # Phase 1 原始需求整理與發現
  reports/          # 驗證/審查報告
  ssot/             # 唯一事實來源（SSoT）
    dbml/           # 資料模型（DBML 3.3.0）
    habdd/          # 高階行為 Gherkin（haBDD 3.3.0）
    haarm/          # 存取控制（haARM 3.3.0）
    haapi/          # 後端意圖（haAPI 3.3.0）
    hapdl/          # 前端意圖（haPDL 3.3.0）
  generate/         # 衍生產物（status: deferred，暫不產生）
    pdl/  isabdd/  openapi/  lofi/  designbrief/
.clarify/           # 澄清問答批次
.raptor/            # arguments.yml / session.md / traceability.md / impact-matrix.yml
```

## 4. `generated.status: deferred` 的意義

- SSoT phase（Discovery → Reconcile）期間，**不**產生 PDL、isaBDD、OpenAPI、lofi、design brief 等 downstream artifact。
- Preview skill（/rapt-openapi、/rapt-lofi、/rapt-design-brief）僅在使用者明確啟用 generate 後才寫入 `docs/generate/**`。
- 此欄位為 kickoff 後不可變欄位，變更需使用者明確授權。

## 5. 下一步

執行 `/rapt-discovery`，匯入 `raw-input/` 三份原始需求材料，產出 discovery artifact 至 `docs/discovery/`。
