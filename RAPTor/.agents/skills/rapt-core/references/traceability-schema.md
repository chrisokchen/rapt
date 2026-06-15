# Traceability Schema

本文件定義 `.raptor/traceability.md` 的標準結構。所有會讀寫 traceability 的 skill 必須遵守本 schema。

## 原則

- Traceability 是跨 artifact 的可稽核索引，不是自由摘要。
- 高階 Gherkin 可先用業務語言標註 entity；DBML table / field 必須由 glossary、DBML 或 intent 階段精確化。
- 不得用猜測填入精確 table / field。證據不足時保留空白並標低信心或建立 CiC。

## L1 Requirement Coverage

由 `rapt-behavior` 初始化，描述需求 / story 到 Feature / Scenario 的覆蓋。

```markdown
## L1 Requirement Coverage

| req_or_story | source | feature | scenario_count | status | notes |
|---|---|---|---:|---|---|
| US-001 | docs/01-discovery/... | user-management.feature | 3 | covered |  |
```

`status` 建議值：

- `covered`
- `partial`
- `deferred`
- `out-of-scope`
- `open-cic`

## L2 Scenario Data Mapping

由 `rapt-behavior` 草擬，`rapt-modeling`、`rapt-intent` 或 `rapt-reconcile` 精確化。

```markdown
## L2 Scenario Data Mapping

| scenario_id | feature | scenario | entities | glossary_terms | read_tables | write_tables | fields | constraints | confidence | source |
|---|---|---|---|---|---|---|---|---|---|---|
| SCN-USER-001 | user-management.feature | 成功建立使用者並指派權限群組 | 使用者, 權限群組 | 使用者, 權限群組 | ugrp | InfoUser | InfoUser.userId, InfoUser.ugrpId | CON-AUTH-002 | medium | docs/04-features/user-management.feature |
```

欄位規則：

| 欄位 | 必要性 | 說明 |
|---|---|---|
| `scenario_id` | should | 穩定 ID；若 legacy feature 尚無 ID，可暫用 feature + scenario name。 |
| `feature` | must | Feature 檔名。 |
| `scenario` | must | Scenario 名稱。 |
| `entities` | should | Gherkin `# entities:` 的業務語言 entity。 |
| `glossary_terms` | should | 對應 `glossary.md` 的 term。 |
| `read_tables` | should | DBML 精確 table name；不足時留空。 |
| `write_tables` | should | DBML 精確 table name；不足時留空。 |
| `fields` | optional | 高風險資料異動或測試生成需要時填入。 |
| `constraints` | optional | 對應 `constraints.md` 的 `constraint_id`。 |
| `confidence` | must | `high` / `medium` / `low`。 |
| `source` | must | 可定位 artifact。 |

## L3 Intent Mapping

由 `rapt-intent` 維護，描述 Scenario 到 haAPI / haPDL / haARM 的對應。

```markdown
## L3 Intent Mapping

| scenario_id | haapi_operation | hapdl_page | haarm_permissions | source |
|---|---|---|---|---|
| SCN-USER-001 | user.create | user-form | user:create | docs/05-backend-intent/user.haapi.yaml |
```

## Decision Traceability

由 `rapt-clarify` 或 `rapt-reconcile` 維護，描述 CiC / decision 對 artifact 的影響。

```markdown
## Decision Traceability

| decision_id | cic_id | status | affected_artifacts | summary |
|---|---|---|---|---|
| CLR-260609-01#Q2 | CiC-260609-002 | applied | docs/01-discovery/04-vision-kpi-scope.md | 最小認證範圍納入 MVP |
```

## Skill 責任

| skill | 責任 |
|---|---|
| `rapt-behavior` | 建立 L1，草擬 L2 的 scenario、entities、source。 |
| `rapt-modeling` | 建立 glossary、seeds、constraints，支援 L2 精確化。 |
| `rapt-intent` | 補全 L2 的 table / field，建立 L3。 |
| `rapt-verify` | 驗證 L1/L2/L3 覆蓋率與 DBML 精確對應。 |
| `rapt-reconcile` | 在有精確 evidence 時修補 L2 / decision traceability。 |
| `rapt-clarify` | 將決策狀態與 affected artifacts 寫入 Decision Traceability。 |
