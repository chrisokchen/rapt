# haAPI 速查卡 v3.3

> 1 頁 A4 列印；完整規格見 [`haAPIdoc.md`](haAPIdoc.md)；跨 DSL 整合見 [`CROSS-DSL-GUIDE.md`](CROSS-DSL-GUIDE.md)

## 1. 最小檔案結構

```yaml
api: <kebab-case-id>           # 被 haPDL api: 引用
title: <人類可讀名稱>
entity: <DBML Table Name>      # case-sensitive，須匹配 DBML
version: "3.3.0"

exposes:
  standard: [list, create, read, update, delete]   # 一行展開 5 端點
  standard_overrides: {}                            # 覆寫個別欄位
  list: { filters, sorting, pagination, search }    # 列表能力
  operations: []                                    # 非標準業務操作

access:
  authentication: { type: bearer, required: true }
  roles: [...]                  # 平面化（validate_cross_dsl.py 讀這個）
  permissions: [...]            # 平面化
  endpoints: { list/read/create/update/delete: ... }   # v3.2+ Access v2 雙軌
  operations: { ... }
```

## 2. Convention：standard 自動展開

| 觸發 | 展開 |
|------|------|
| `standard: crud` | 5 端點（POST/GET-list/GET/PATCH/DELETE）|
| `standard: [create, update]` | 局部 sugar，僅 2 端點 |
| `entity: Order` | 自動推 `/api/orders`、`title: 訂單管理`、pagination 預設 |
| `POST /users` | 自動推 operation `createUser` |

## 3. v3.3 Access v2 雙軌結構（§2.3.1）

```yaml
access:
  endpoints:
    read:
      required_roles: [htsd, sysadm]          # ← 引用 haARM role.id
      required_permissions:
        - id: infouser_read                   # ← 引用 haARM permission.id
      scope: department                       # ← 對齊 haARM scope
      conditions:
        - haarm_constraint: user_self_access  # ← 引用 haARM constraint.id（opaque ref）
      rate_limit: 100/hour

  operations:
    export:
      required_roles: [sysadm]
      required_permissions: [{id: infouser_export}]
```

> **棄用警告**：`access.permissions:` （v3.1 dead-letter）將於 v3.4 移除；改用上面雙軌。

## 4. Resilience 四層級聯（§4.7.1）

```
step.resilience  >  API.resilience  >  project codegen.config.yaml  >  framework 預設
```

```yaml
# codegen.config.yaml（專案根目錄）
defaults:
  resilience:
    timeout: 30s
    retry: { max_attempts: 3, backoff: exponential }
    circuit_breaker: { failure_threshold: 5, reset_after: 60s }
```

## 5. 列表查詢能力（list）

```yaml
list:
  filters:
    - field: userId; operators: [eq, contains, starts_with]
    - field: deptId; operators: [eq, starts_with]    # v3.3 對齊 haARM 新運算子
  sorting:
    fields: [userId, userName]; default: userId:asc
  pagination:
    style: offset|cursor|page-size; default_size: 20; max_size: 100
  search:
    fields: [...]; type: simple|fulltext; min_length: 2
  includes:
    - field: department; type: object; default: false
```

## 6. 跨 DSL 引用點

| 從 | 到 | 用途 |
|----|----|------|
| haAPI `entity:` | DBML `Table <Name>` | 對應實體（Rule 2）|
| haAPI `access.required_permissions[].id` | haARM `permissions[].id` | 端點權限（Rule 3）|
| haAPI `access.required_roles[]` | haARM `roles[].id` | 端點角色（Rule 4）|
| haAPI `access.conditions[].haarm_constraint` | haARM `constraints[].id` | 條件 opaque ref |
| haPDL `api:` | haAPI `api:` 頂層 | 頁面綁定 API（Rule 5）|

## 7. 反模式（§8.5）

| 編號 | 反模式 | 修正 |
|------|--------|------|
| AP-01 | 在新規格用 `access.permissions:` | 改用 `access.endpoints` + `access.operations` 雙軌 |
| AP-02 | 把 `rate_limit` 寫在 permission | 改放在 `endpoint.rate_limit` |
| AP-03 | 同 op 雙軌但無 AND/OR 註記 | 顯式宣告 `mode: AND` 或 `OR` |
| AP-04 | `conditions[]` 內聯邏輯字串 | 用 `haarm_constraint: <id>` opaque ref |
| AP-05 | resilience 逐 endpoint 寫 | 用四層級聯，僅覆寫時寫 |

## 8. 三層職責分離（§1.4）

| 檔案 | 負責 |
|------|------|
| `*.haapi.yaml` | 業務能力意圖（「我需要呼叫 smtp 的 send_email」）|
| `integrations.config.yaml` | 外部服務細節（端點、認證、protocol）|
| `codegen.config.yaml` | 全域 resilience 預設（timeout/retry）|

## 9. 常用 CLI（M4 規劃中）

```bash
haapi-lint <file>.haapi.yaml          # 語法 + 引用完整性
haapi-lint --validate-cross-dsl <anchor>   # 跨 DSL 引用驗證
python benchmarks/validate_cross_dsl.py <anchor>   # 已可用
```

## 10. 最精簡 vs 完整寫法

| 寫法 | 行數 | 適用 |
|------|------|------|
| 最精簡（standard: crud）| ~8 行 | PM：80% 標準場景 |
| 慣例展開後（standard + overrides）| ~25 行 | SA：覆寫 1-2 端點 |
| 完整明示（operations 全列）| ~80+ 行 | 客製化專家 |

---
**版本**：v3.3.0｜**對齊**：四 DSL v3.3｜**最後更新**：2026-05-14
