# RAPTor Kickoff Plan — Bridge Cognitive Tutor

> initialized_at: 2026-06-16
> arguments_schema_version: 2

## Project 設定

| 欄位 | 值 |
|---|---|
| `project.name` | Bridge Cognitive Tutor |
| `project.description` | AI 驅動、可診斷、可解釋的橋牌認知學習系統；MVP 聚焦 Entry Management Tutor（橋引管理教練）。 |
| `project.language` | zh-hant |
| `project.mode` | greenfield |
| `paths.docs_dir` | docs/ |

## arguments.yml 預覽

```yaml
arguments_schema_version: 2

project:
  name: Bridge Cognitive Tutor
  description: AI 驅動、可診斷、可解釋的橋牌認知學習系統；MVP 聚焦 Entry Management Tutor（橋引管理教練）。
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

## v2 docs layout 預覽

```text
docs/
  discovery/            # Phase 1 業務探索摘要
  reports/              # verify / RAscore 等報告
  ssot/                 # Single Source of Truth（人工權威來源）
    dbml/               # annotated DBML 資料模型
    habdd/              # 高階 Gherkin feature
    haarm/              # haARM 存取控制
    haapi/              # haAPI 後端意圖
    hapdl/              # haPDL 前端意圖
  generate/             # 衍生產物（status: deferred，暫不生成）
    pdl/
    isabdd/
    openapi/
    lofi/
    designbrief/
.clarify/               # 釐清 session 暫存
.raptor/                # RAPTor 控制檔（arguments / session / traceability / impact-matrix）
```

## `generated.status: deferred` 的意義

- 目前**不生成** PDL、isaBDD、OpenAPI、Lo-Fi、Design Brief 等 downstream / preview 產物。
- 各 preview skill 會回報「需後續 generate」，但不會寫入 `docs/generate/**`。
- 待 SSoT 經 `/rapt-verify` 驗證穩定後，再視需要逐一執行 preview skill。

## 下一步

執行 `/rapt-discovery`，匯入 `raw-input/` 內既有材料（PRD、grill 討論、審查意見）作為原始需求 source。
