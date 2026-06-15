# Paths & Arguments 規則

所有 `rapt-*` skill 的路徑唯一來源是 `.raptor/arguments.yml`。skill 不得 hardcode 產物路徑；若 arguments 缺少新鍵，才可使用本文件定義的相容 fallback。

## 解析優先序

1. 使用者本次明確指定的 target 或 output path。
2. `.raptor/arguments.yml` 的 `paths.*`、`generated.*`、`anchors.*`。
3. 本文件定義的 v2 預設路徑。
4. v1 legacy fallback，只能為了讀取既有專案使用，不可作為新專案預設。

## Schema Version

```yaml
arguments_schema_version: 2
```

- v2 新專案必須寫入 `arguments_schema_version: 2`。
- 未宣告版本者視為 v1 legacy，可讀取但應提示執行 layout migration。
- 工具可用 `rapt-core/scripts/resolve_args.py --strict-v2` 要求 v2。

## v2 `.raptor/arguments.yml`

```yaml
arguments_schema_version: 2

project:
  name: <string>
  description: <string>
  language: zh-hant
  mode: greenfield | existing | single-package

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

## v1 Legacy Fallback

| v2 key | v2 default | v1 fallback |
|---|---|---|
| `paths.discovery_dir` | `docs/discovery/` | `paths.business_discovery_dir` 或 `docs/01-discovery/` |
| `paths.data_model_dir` | `docs/ssot/dbml/` | `docs/02-data-model/` |
| `paths.access_control_dir` | `docs/ssot/haarm/` | `docs/03-access-control/` |
| `paths.high_gherkin_dir` | `docs/ssot/habdd/` | `docs/04-features/` |
| `paths.backend_intent_dir` | `docs/ssot/haapi/` | `docs/05-backend-intent/` |
| `paths.frontend_intent_dir` | `docs/ssot/hapdl/` | `docs/06-frontend-intent/` |
| `generated.openapi_dir` | `docs/generate/openapi/` | `docs/06-openapi/` |
| `generated.lofi_dir` | `docs/generate/lofi/` | `docs/07-lofi-preview/` |
| `generated.designbrief_dir` | `docs/generate/designbrief/` | `docs/08-design-brief/` |

## Path Binding Rules

- 相對路徑一律以專案 CWD 為基準。
- Planner 讀取 arguments 後，應把解析後的 path 放進 payload；Worker 不自行猜路徑。
- Worker 只可寫入 payload 明確授權的 target path。
- Preview skill 只可寫入 `generated.*` 對應目錄，不可修改 `docs/ssot/**`。
- `generated.status: deferred` 時，不產生 PDL、isaBDD、TypeSpec 等 downstream artifact；只能報告需要後續 generate。

## `.raptor/` Files

```text
.raptor/
  arguments.yml
  session.md
  traceability.md
  impact-matrix.yml
  reports/
```

## Tooling

```powershell
python RAPTor/.agents/skills/rapt-core/scripts/resolve_args.py --key paths.data_model_dir
python RAPTor/.agents/skills/rapt-core/scripts/migrate_docs_layout.py --root .
```
