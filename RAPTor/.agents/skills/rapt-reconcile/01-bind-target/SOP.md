# 01 Bind Target SOP

**目的**：從 rapt-verify 報告與 RAscore findings 中提取所有需修復的項目並綁定到具體檔案位置。

---

## 步驟

### 1.1 READ reports

READ if exists `${paths.reports_dir}/verify-report.md`，提取：
- Completeness FAIL 項目
- Cross-DSL ERROR 和 WARNING 項目
- Traceability FAIL 項目
- Coverage FAIL 項目（無法自動修復，僅記錄）

READ if exists：

- `${paths.reports_dir}/rascore-findings.json`
- `${paths.reports_dir}/rascore-findings.md`
- `${paths.reports_dir}/rascore-scorecard.yml`

JSON 優先；Markdown 作 fallback。

若 verify report 不存在但 RAscore findings 存在，不停止，將 `verify_missing=true` 寫入 binding metadata。

### 1.2 RESOLVE verify finding 到具體路徑

```
問題：R-API-06 order.haapi.yaml#list.filters filter `createdat` 大小寫不符
綁定：${paths.backend_intent_dir}/order.haapi.yaml
位置：list.filters[field==createdat]
修復值：createdAt（從 DBML 讀取的精確值）
```

### 1.3 RESOLVE RAscore finding 到具體路徑

對每個 RAscore finding 綁定：

```yaml
- id: RA-D1-001
  source: rascore
  criterion: D1
  category: cross-spec-gap
  artifact: .raptor/reports/rascore-precheck.json
  location: cross_spec
  owner_skill: rapt-reconcile
  issue: 機械比對無法從繁中 Gherkin 直接匹配英文 DBML 名稱
  candidate_targets:
    - .raptor/traceability.md
    - docs/02-data-model/glossary.md
```

### 1.4 OUTPUT binding_list

```yaml
findings:
  - id: F001
    source: verify
    rule: R-API-06
    file: backend-intent/order.haapi.yaml
    location: list.filters[0].field
    current: createdat
    correct: createdAt
    source: schema/shop.dbml#Table:Order#column:createdAt
  - id: F002
    source: verify
    rule: traceability
    feature: order-checkout.feature
    scenario: 客戶使用折扣碼結帳
    missing: haAPI source_evidence
  - id: RA-D1-001
    source: rascore
    criterion: D1
    category: cross-spec-gap
    artifact: .raptor/reports/rascore-precheck.json
    location: cross_spec
    owner_skill: rapt-reconcile
```
