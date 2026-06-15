# RAPTor Kickoff Plan

## Project

- name: SmallBiz 電商平台
- description: 月租制、開箱即用的 B2C 電商平台，讓中小商家能管理商品、庫存、訂單、會員、促銷、金流、物流與基本報表。
- language: zh-hant
- mode: greenfield

## Arguments Preview

```yaml
arguments_schema_version: 2

project:
  name: SmallBiz 電商平台
  description: 月租制、開箱即用的 B2C 電商平台，讓中小商家能管理商品、庫存、訂單、會員、促銷、金流、物流與基本報表。
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
```

## v2 Docs Layout

| Key | Path | Purpose |
|---|---|---|
| `paths.discovery_dir` | `docs/discovery/` | 業務探索輸出 |
| `paths.reports_dir` | `docs/reports/` | 驗證與分析報告 |
| `paths.ssot_dir` | `docs/ssot/` | SSoT 根目錄 |
| `paths.data_model_dir` | `docs/ssot/dbml/` | annotated DBML |
| `paths.high_gherkin_dir` | `docs/ssot/habdd/` | 高階 Gherkin |
| `paths.access_control_dir` | `docs/ssot/haarm/` | haARM 存取控制 |
| `paths.backend_intent_dir` | `docs/ssot/haapi/` | haAPI 後端意圖 |
| `paths.frontend_intent_dir` | `docs/ssot/hapdl/` | haPDL 前端意圖 |
| `paths.clarify_dir` | `.clarify/` | 釐清工作區 |
| `paths.traceability_file` | `.raptor/traceability.md` | 追蹤矩陣 |
| `paths.impact_matrix_file` | `.raptor/impact-matrix.yml` | 影響矩陣 |

## Generated Artifacts

`generated.status` is `deferred`. Preview or generated artifacts are reserved for later RAPTor phases and will use:

| Key | Path |
|---|---|
| `generated.generated_dir` | `docs/generate/` |
| `generated.pdl_dir` | `docs/generate/pdl/` |
| `generated.low_gherkin_dir` | `docs/generate/isabdd/` |
| `generated.openapi_dir` | `docs/generate/openapi/` |
| `generated.lofi_dir` | `docs/generate/lofi/` |
| `generated.designbrief_dir` | `docs/generate/designbrief/` |

## Policy

- `arguments_schema_version: 2`
- `policy.write_mode: deny-by-default`
- `generated.status: deferred`
- Kickoff only writes `.raptor/**`; SSoT and generated artifacts are created by later phases.

## Next Step

Run `/rapt-discovery` to process `raw-input/` into business discovery artifacts.
