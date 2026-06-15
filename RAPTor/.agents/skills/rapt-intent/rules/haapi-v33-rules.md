# haAPI v3.3 規則

本文件定義 `rapt-intent`（和 `rapt-form-haapi`）在生成 haAPI 時必須遵守的規則。
> 唯一裁決者：`DSLspec/haAPI-specification_v3.3.md` §2.2 / §2.3.1。結構由 `dsl-lint.py` 強制檢查。

---

## Access v2 雙軌格式（強制）— `access` 是 **dict**，不是 array

`access.endpoints` / `access.operations` 以**操作名為 key**（dict），value 只放授權（roles/permissions）。
**path / method 屬於 `exposes`，不寫在 `access`。**

```yaml
# ✅ 正確：dict（key=操作名），只談授權
exposes:
  standard: [list, read]                  # path/method 由 exposes + 慣例推導
  operations:
    - name: apply_refund
      method: POST
      path: /{id}/apply-refund

access:
  endpoints:
    list:                                 # ← key=操作名
      required_roles: [staff, admin]
      required_permissions:
        - id: order_read                  # ← {id: ...}，非裸字串
    read:
      required_roles: [staff, admin]
      required_permissions:
        - id: order_read
  operations:
    apply_refund:
      required_roles: [customer]
      required_permissions:
        - id: order_refund

# ❌ 禁止：array 形式並夾帶 path/methods（HAAPI-SCHEMA-001）
access:
  endpoints:
    - path: /orders                       # FORBIDDEN
      methods: [GET, POST]

# ❌ 禁止：自創頂層 endpoints（HAAPI-SCHEMA-002）
endpoints: [...]                          # FORBIDDEN

# ❌ 禁止：legacy access.permissions（HAAPI-SCHEMA-004）
access:
  permissions: [order_read]               # FORBIDDEN
```

---

## 規則表

| ID | 規則 | 嚴重度 | 反例 |
|----|------|-------|------|
| R-API-01 | `entity:` 值必須 case-sensitive 對應 DBML Table Name | ERROR | `entity: order`（Table 是 `Order`）|
| R-API-02 | `access.permissions:` 已 deprecated，禁止使用 | ERROR | `access.permissions: [order_read]` |
| R-API-03 | `access.operations.<op>.required_roles` 中的每個 role 必須在 haARM 存在 | ERROR | role `analyst` 未在 haARM 定義 |
| R-API-04 | `access.operations.<op>.required_permissions[].id` 中的每個 permission 必須在 haARM 存在 | ERROR | permission `order_export` 未在 haARM 定義 |
| R-API-05 | `schema_version` 必須是 `"3.3"`（接受 `3.3.x`）| ERROR | `schema_version: "3.2"` |
| R-API-06 | `exposes.list.filters` 欄位名稱必須 case-sensitive 對應 DBML column | WARNING | filter `customerid`（column 是 `customerId`）|
| R-API-07 | 自訂 operation 必須有 `source_evidence`（Gherkin 引用）| WARNING | operation `applyRefund` 無 Gherkin 來源 |
| R-API-08 | `access.endpoints` / `access.operations` 必須是 **dict**（key=操作名）；禁止 array、禁止頂層 `endpoints:` | ERROR | `access.endpoints: [{path: ...}]` 或頂層 `endpoints:` |

---

## AP（反模式）

| AP | 描述 | ✅ 改用 |
|----|------|---------|
| AP-API-01 | 在 haAPI 中定義 haARM 尚未有的 role | 先透過 rapt-reconcile 在 haARM 中建立 role |
| AP-API-02 | `entity:` 使用 plural 形式 | 對應 DBML Table（通常 singular）|
| AP-API-03 | 直接修改 haARM 來補上缺少的 permission | DELEGATE to rapt-reconcile |

---

## list.columns 符號速查

```
{field}     普通欄位
{field}#    主鍵（顯示 link）
{field}|currency   格式化（金額）
{field}|date       格式化（日期）
{field}^    可排序
{field}=    可篩選
{field}:badge      以 badge 顯示
```
