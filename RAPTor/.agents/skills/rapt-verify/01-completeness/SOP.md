# 01 Completeness Check SOP

**目的**：驗證所有 SSoT artifacts 已存在且不為空。

---

## 步驟

### 1.1 CHECK 五類 SSoT 檔案

```
ASSERT: ${paths.data_model_dir}/*.dbml 至少一個檔案存在
ASSERT: ${paths.access_control_dir}/*.haarm.yaml 至少一個檔案存在
ASSERT: ${paths.high_gherkin_dir}/*.feature 至少一個檔案存在
ASSERT: ${paths.backend_intent_dir}/*.haapi.yaml 至少一個檔案存在
ASSERT: ${paths.frontend_intent_dir}/*.hapdl.yaml 至少一個檔案存在
```

### 1.2 CHECK 支援文件

```
CHECK: ${disc_dir}/01-stakeholders.md
CHECK: ${paths.high_gherkin_dir}/story-index.md
CHECK: ${paths.data_model_dir}/glossary.md
CHECK: ${paths.data_model_dir}/seeds.md（若 DBML 存在 ref_code / 狀態 / bitmask）
CHECK: ${paths.data_model_dir}/constraints.md（若 Gherkin / DBML 存在高風險狀態、權限、刪除限制）
CHECK: ${paths.traceability_file}
```

### 1.3 CHECK 每個 SSoT 檔案不為空（> 5 行）

### 1.4 OUTPUT completeness_result

```yaml
completeness:
  status: PASS | FAIL
  missing_files: []
  empty_files: []
  warnings: []
```
