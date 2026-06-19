# 01 Bind and Ingest SOP

**目的**：綁定唯讀輸入、確認 brownfield 分析前提，並把提案標準化為可追蹤的分析種子。

## 步驟 1.1：解析 arguments

READ `.raptor/arguments.yml` 與 `.raptor/session.md`。

ASSERT：

- arguments 必須存在。
- 相對路徑以專案 CWD 為基準。
- `paths.whatif_dir` 缺少時只在本次記憶中 fallback 為 `whatif/`。
- `paths.impact_dir` 缺少時只在本次記憶中 fallback 為 `${paths.reports_dir}/impact/`。
- 不得修改 arguments 以補路徑。

將 `project.mode: existing` 視為 brownfield 相容值；若為 `greenfield`，仍檢查既有 SSoT，只有 SSoT 為空時才 SKIP。

## 步驟 1.2：綁定提案

依序選擇第一個有效來源：

1. 使用者明確指定的 what-if 檔案或路徑。
2. 使用者本次行內描述。
3. 使用者指定的 SSoT 檔案。

READ 檔案時保留：

- `source_ref`
- 檔案行號或 Markdown section
- 原始標題
- 變更動機、預期使用者、預期結果

若同時有多個來源，以使用者明確指定者為主，其餘列為 supporting context，不自行合併成額外需求。

## 步驟 1.3：綁定既有系統證據

READ if exists：

- `${paths.data_model_dir}/**/*.dbml`
- `${paths.high_gherkin_dir}/**/*.feature`
- `${paths.access_control_dir}/**/*.{yaml,yml}`
- `${paths.backend_intent_dir}/**/*.{yaml,yml}`
- `${paths.frontend_intent_dir}/**/*.{yaml,yml}`
- `${paths.traceability_file}`
- `${paths.impact_matrix_file}`
- `${paths.discovery_dir}/04-vision-kpi-scope.md`
- `${paths.data_model_dir}/glossary.md`
- `${paths.data_model_dir}/constraints.md`
- `${paths.reports_dir}/verify-report.yml`
- `${paths.reports_dir}/rascore-findings.json`

ASSERT 至少存在 DBML 或 haBDD。兩者都不存在時停止，且不產生推測性報告。

## 步驟 1.4：標準化提案

DERIVE：

```yaml
proposal_input:
  title: <短標題>
  source_ref: <path、inline:user-request 或 artifact path>
  mode: brownfield | existing | greenfield-with-ssot
  summary: <一段可驗證摘要>
  business_entities: []
  actions: []
  actors: []
  expected_outcomes: []
  explicit_constraints: []
  ambiguities: []
```

規則：

- entity 先用提案原詞，再用 glossary canonical/legacy alias 對應。
- action 使用動詞原形或既有 DSL operation 名稱。
- 不把推測寫成明示需求。
- 找不到 entity 但有 action 時保留 action，classification 先設 `unclear`。
- entity/action 都找不到時建立 GAP clarify payload，後續直接走報告步驟。

## 步驟 1.5：建立輸入索引

DERIVE：

```yaml
impact_inputs:
  proposal: {}
  dbml_files: []
  habdd_files: []
  haarm_files: []
  haapi_files: []
  hapdl_files: []
  traceability_file: null
  impact_matrix_file: null
  scope_file: null
  glossary_file: null
  constraints_file: null
  verify_report_file: null
  rascore_findings_file: null
  impact_dir: null
  missing_optional_inputs: []
```

EMIT 一行前置摘要：提案來源、專案 mode、可用 DSL 類型、缺少的選配證據。

