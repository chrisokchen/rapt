# 03 haAPI Render SOP

**目的**：依 API Intent Map，組裝 haAPI payload 並 DELEGATE to `rapt-form-haapi` 生成最終 haAPI 檔案。

---

## 步驟

### 3.1 LOAD haapi-v33-rules

LOAD REF [rapt-intent::rules/haapi-v33-rules.md]

### 3.2 BUILD haAPI payload

對每個 api_intent：

```yaml
# 組裝 payload（傳給 rapt-form-haapi）
payload:
  schema_version: "3.3"
  api_intent: <api_intent_map 中的對應項目>
  haarm_ref: <haARM 資料來源路徑>
  dbml_ref: <DBML 資料來源路徑>
  output_file: "${paths.backend_intent_dir}/{api_id}.haapi.yaml"
  source_evidence:
    - "features/{feature_file}#Scenario:{scenario_name}"  # Gherkin
    - "schema/{dbml_file}#Table:{table_name}"             # DBML
    - "access-control/{haarm_file}#roles"                  # haARM
```

### 3.3 VALIDATE payload 完整性

ASSERT：
- `entity:` 值 case-sensitive 對應 DBML Table Name ✓
- `access.endpoints` / `access.operations` 結構使用 v2 雙軌格式 ✓
- **DENY `access.permissions:`**（deprecated）
- 所有引用的 `role.id` 存在於 haARM ✓
- `source_evidence` 非空 ✓

### 3.4 DELEGATE to rapt-form-haapi

DELEGATE: `rapt-form-haapi` with payload

### 3.5 VERIFY 生成結果

READ 生成的 .haapi.yaml，確認：
- 檔案存在且不為空
- `schema_version: "3.3"`
- `entity:` 與 DBML Table Name 完全一致
- 無 `access.permissions:` 欄位
