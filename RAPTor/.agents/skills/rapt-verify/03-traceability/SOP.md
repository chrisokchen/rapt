# 03 Traceability Check SOP

**目的**：驗證 traceability L1/L2/L3 是否足以支援需求覆蓋、Scenario → DBML、Scenario → intent 的追蹤。

---

## 步驟

### 3.1 BUILD Gherkin scenario index

READ 所有 `${paths.high_gherkin_dir}/*.feature`：
```
scenario_index = [{feature_file, scenario_id, scenario_name, entities, tags}]
```

解析：
- `# scenario_id:`
- `# entities:`
- Scenario 名稱

### 3.2 BUILD haAPI operation index

READ 所有 `${paths.backend_intent_dir}/*.haapi.yaml`：
```
operation_index = [{api_id, operation_id, source_evidence[]}]
```

### 3.3 BUILD haPDL page index

READ 所有 `${paths.frontend_intent_dir}/*.hapdl.yaml`：
```
page_index = [{page_id, source_evidence[]}]
```

### 3.4 MATCH Gherkin → haAPI / haPDL

對每個 scenario：
- SEARCH operation_index 中 source_evidence 含此 scenario 引用
- SEARCH page_index 中 source_evidence 含此 scenario 引用
- 若兩者都找不到：標記 UNTRACED

### 3.5 VALIDATE L2 Scenario Data Mapping

READ `${paths.traceability_file}`，依 `rapt-core::traceability-schema.md` 驗證：

- 每個 Scenario 有 L2 row，或有 deferred / out-of-scope 註記。
- L2 `entities` 能對應 Gherkin `# entities:`。
- L2 `read_tables` / `write_tables` 若非空，必須能精確對上 DBML Table。
- L2 `constraints` 若非空，必須能對上 `${paths.data_model_dir}/constraints.md` 的 `constraint_id`。
- `confidence=low` 的 row 不算完整覆蓋，但可作 warning。

### 3.6 VALIDATE glossary / seed / constraint coverage

- Gherkin entities 應能透過 `glossary.md` Canonical Mapping 對到 DBML table。
- 每個 DBML `ref_code:` 應能對到 `seeds.md`。
- 高風險狀態 / 權限 / 刪除限制應能對到 `constraints.md`，或有 OPEN CiC。

### 3.7 OUTPUT traceability_result

```yaml
traceability:
  status: PASS | PARTIAL | FAIL
  l1_requirement_coverage:
    status: PASS | PARTIAL | FAIL
  l2_scenario_data_mapping:
    status: PASS | PARTIAL | FAIL
    total_scenarios: N
    mapped: M
    low_confidence: K
    missing:
      - feature: order-checkout.feature
        scenario: 客戶結帳時應用折扣碼
        issue: 無 L2 Scenario Data Mapping
  l3_intent_mapping:
    status: PASS | PARTIAL | FAIL
    total_scenarios: N
    traced: M
    untraced:
      - feature: order-checkout.feature
        scenario: 客戶結帳時應用折扣碼
        issue: 無對應 haAPI operation 或 haPDL page
  rascore_readiness:
    glossary_dbml_mapping: PASS | PARTIAL | FAIL
    ref_code_seed_coverage: PASS | PARTIAL | FAIL
    constraint_coverage: PASS | PARTIAL | FAIL
```
