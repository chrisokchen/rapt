# 01 Bind Inputs SOP

**目的**：明確綁定 RAscore 評分所需輸入，避免 evaluator 自行猜路徑。

---

## 步驟 1.1：讀取 arguments

```
READ: .raptor/arguments.yml
LOAD REF [rapt-core::paths-and-arguments.md]
```

使用既有 paths，不修改 `.raptor/arguments.yml`：

- `${paths.business_discovery_dir}`
- `${paths.high_gherkin_dir}`
- `${paths.data_model_dir}`
- `${paths.traceability_file}`
- `${paths.reports_dir}`

---

## 步驟 1.2：綁定必要輸入

READ：

- `${paths.business_discovery_dir}/**/*.md`
- `${paths.high_gherkin_dir}/*.feature`
- `${paths.data_model_dir}/*.dbml`

ASSERT：

- 若找不到任何 discovery 文件：繼續，但 A/E 維度最高信心只能 `low`，並記 warning。
- 若找不到任何 `.feature`：EMIT 錯誤並停止，因為 B/D/F 無法評分。
- 若找不到任何 `.dbml`：EMIT 錯誤並停止，因為 C/D 無法評分。

---

## 步驟 1.3：綁定可選輸入

READ if exists：

- `${paths.data_model_dir}/glossary.md`
- `${paths.data_model_dir}/seeds.md`
- `${paths.data_model_dir}/constraints.md`
- `${paths.traceability_file}`
- `${paths.reports_dir}/verify-report.md`

缺少可選輸入時不要停止，但要降低相關準則信心：

- 無 glossary：D1 / B5 / C4 confidence 降為 `medium` 或 `low`。
- 無 seeds 且 DBML 有 ref_code / 狀態 / bitmask：C3 / D4 confidence 降為 `medium` 或 `low`。
- 無 constraints 且有權限、狀態轉換、引用刪除限制：D4 / F1 confidence 降為 `medium` 或 `low`。
- 無 traceability：E1 / E2 confidence 降為 `low`。
- 無 verify report：F/G 只能依 Gherkin + DBML 與流程 artifact 評估。
  同時 EMIT 建議：「若要提高 RAscore D/E/F/G 的 evidence 信心，請先執行 /rapt-verify 再重跑 /rapt-RAscore。」

---

## 步驟 1.4：建立輸入索引

在後續 SOP 的工作記憶中建立：

```yaml
rascore_inputs:
  discovery_docs: []
  feature_files: []
  dbml_files: []
  glossary_file: null
  seeds_file: null
  constraints_file: null
  traceability_file: null
  verify_report_file: null
  reports_dir: ${paths.reports_dir}
  missing_inputs: []
```
