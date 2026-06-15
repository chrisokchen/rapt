# rapt-kickoff Arguments Schema

本文件定義 `.raptor/arguments.yml` v2 schema。`rapt-kickoff` 建立新專案時必須輸出 v2；既有 v1 專案可由 `rapt-core/scripts/migrate_docs_layout.py` 規劃遷移。

## Schema

```yaml
arguments_schema_version: 2

project:
  name: <string>
  description: <string>
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

## Immutable After Kickoff

以下欄位建立後不可由一般 skill 自動修改，除非使用者明確授權：

- `project.name`
- `arguments_schema_version`
- `dsl_versions.*`
- `generated.status`
- `anchors.*`

## File First Rule

`rapt-kickoff` 必須先產出 `.raptor/KICKOFF_PLAN.md`，讓使用者可確認即將建立的 paths、policy、generated status，再建立 `.raptor/arguments.yml`。

## Other Skills Read Rule

每個 skill 的 Step 0 應包含：

```text
READ: .raptor/arguments.yml
ASSERT: arguments_schema_version == 2，或啟用 v1 legacy fallback 並提出 migration note
DERIVE: 所需 paths/generated/anchors
```

若 `.raptor/arguments.yml` 不存在，應提示先執行 `/rapt-kickoff`，不可自行建立替代設定檔。
