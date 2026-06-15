# haPDL 格式錨點（Format Anchor）

> ⚠️ **唯一裁決者：`RAPTor/DSLspec/haPDL-specification-v3.3.md` §3.1 + `rapt-core::hapdl-canonical-keys.md`**。本文件為摘要，差異時以 DSLspec 為準。
> 結構受 `dsl-lint.py` 強制檢查；**一檔一頁、頂層必須是 `page`**。

---

## 最小合法 haPDL 範例（v3.3）— List 頁面

```yaml
page: order-list
schema_version: "3.3"
type: list
entity: Order          # case-sensitive，對應 DBML Table Name
api: order             # 對應 haAPI api: order 的 logical id
title: 訂單列表

view:
  filters:
    - {field: customerId, label: 客戶編號, type: eq}
    - {field: status, label: 狀態, type: eq, ref_code: OrderStatus}
    - {field: createdAt, label: 建立日期, type: range}
  columns:
    - {field: orderId, label: 訂單編號, link: true}
    - {field: customerId, label: 客戶編號}
    - {field: status, label: 狀態, format: badge, ref_code: OrderStatus}
    - {field: totalAmount, label: 總金額, format: currency}
    - {field: createdAt, label: 建立日期, format: date, sortable: true}
  actions:
    standard: [create]
    placement:
      header: [create]

security:
  permission_refs:
    view:
      - {id: order_read}
    create:
      - {id: order_create}
  datasource_scope: department

source_evidence:
  - "backend-intent/order.haapi.yaml"
  - "features/order-management.feature#Scenario:瀏覽訂單列表"
  - "access-control/shop.haarm.yaml#permission:order_read"
```

---

## 最小合法 haPDL 範例（v3.3）— Form 頁面

```yaml
page: order-form
schema_version: "3.3"
type: form
entity: Order
api: order
title: 建立訂單

form:
  mode: create         # create | edit
  fields:
    - {field: customerId, label: 客戶編號, type: select, required: true}
    - {field: status, label: 狀態, type: select, ref_code: OrderStatus}
    - {field: totalAmount, label: 總金額, type: number, readonly: true}
  actions:
    submit: createOrder
    cancel: order-list

security:
  permission_refs:
    submit:
      - {id: order_create}
  datasource_scope: own

source_evidence:
  - "backend-intent/order.haapi.yaml#operation:createOrder"
  - "features/order-management.feature#Scenario:建立訂單"
```

---

## 禁止格式（dsl-lint 會直接報 ERROR）

```yaml
# ❌ HAPDL-SCHEMA-001：meta / pages 多頁打包（違反一檔一頁）
meta:                 # 絕對禁止
  module: order
pages:                # 絕對禁止
  - id: order-list

# ❌ HAPDL-SCHEMA-002：用 page_id 取代 page
page_id: order-list   # 絕對禁止（正式鍵為 page）

# ❌ HAPDL-LINT-003：deprecated security.permissions
security:
  permissions:        # 絕對禁止
    - order_read
```

---

## api: 對應關係

| haAPI api: | haPDL api: |
|------------|-----------|
| order | order |
| order-item | order-item |

**規則**：`api:` 使用 haAPI 的 logical id（`api:` 頂層值），不使用 URL 路徑。

---

## datasource_scope 語意

| 值 | 適用情境 |
|----|---------|
| `own` | 使用者只能看自己的資料（如客戶看自己訂單）|
| `department` | 可看部門內資料（如客服看所轄區訂單）|
| `all` | 全系統（僅 admin / system role）|
