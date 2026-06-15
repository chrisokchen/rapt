# 04 haPDL Render SOP

**目的**：依 Page Intent Map，組裝 haPDL payload 並 DELEGATE to `rapt-form-hapdl` 生成最終 haPDL 檔案。

---

## 步驟

### 4.1 LOAD hapdl-v33-rules

LOAD REF [rapt-intent::rules/hapdl-v33-rules.md]

### 4.2 BUILD haPDL payload

對每個 page_intent：

```yaml
# 組裝 payload（傳給 rapt-form-hapdl）
payload:
  schema_version: "3.3"
  page_intent: <page_intent_map 中的對應項目>
  haapi_ref: "${paths.backend_intent_dir}/{api_id}.haapi.yaml"
  dbml_ref: <DBML 資料來源路徑>
  haarm_ref: <haARM 資料來源路徑>
  output_file: "${paths.frontend_intent_dir}/{page_id}.hapdl.yaml"
  source_evidence:
    - "${paths.backend_intent_dir}/{api_id}.haapi.yaml"   # haAPI
    - "features/{feature_file}#Scenario:{scenario_name}"  # Gherkin
    - "access-control/{haarm_file}#permission:{perm_id}"  # haARM
```

### 4.3 VALIDATE payload 完整性

ASSERT：
- `entity:` 值 case-sensitive 對應 DBML Table Name ✓
- `api:` 值對應 haAPI 的 `api:` 頂層 id ✓
- **DENY `security.permissions:`**（deprecated）
- `security.permission_refs` 使用 `{id: xxx}` 格式 ✓
- 引用的 permission.id 存在於 haARM ✓
- `source_evidence` 非空 ✓

### 4.4 DELEGATE to rapt-form-hapdl

DELEGATE: `rapt-form-hapdl` with payload

### 4.5 VERIFY 生成結果

READ 生成的 .hapdl.yaml，確認：
- 檔案存在且不為空
- `schema_version: "3.3"`
- `entity:` 與 DBML Table Name 完全一致
- `api:` 值能對應實際 haAPI 檔案
- 無 `security.permissions:` 欄位
