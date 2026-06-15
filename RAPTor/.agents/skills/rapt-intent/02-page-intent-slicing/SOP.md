# 02 Page Intent Slicing SOP

**目的**：從 API Intent + Gherkin Feature 切分頁面意圖（haPDL），為每個主要業務功能確定需要哪些頁面。

---

## 步驟

### 2.1 DERIVE Page Intent 清單

對每個 API Intent，DERIVE 對應的頁面：

```
標準頁面模式（依 haAPI 操作推斷）：
  standard: [list] → type: list 頁面
  standard: [create] → type: form（create 模式）
  standard: [update] → type: form（edit 模式）
  standard: [read] → type: detail 頁面
  custom operation（如 dashboard/report）→ type: dashboard

特殊頁面（從 Gherkin 識別）：
  多步驟業務流程 → type: wizard
```

對每個 Page DERIVE：

```
- page_id: <kebab-case>
- type: list | form | detail | dashboard | wizard
- entity: <DBML Table Name>  ← case-sensitive
- api: <haAPI api: id>       ← 對應 api_intent_map 的 api_id
- title: <業務顯示名稱>
- primary_actor: <主要使用此頁面的角色>
- key_fields: [<業務上重要的欄位（中文名稱）>]
- actions: [<頁面上的業務動作>]
- auth_roles: [<從 haARM 取得>]
```

### 2.2 IDENTIFY field layout

對每個 Page 的 key_fields，從 DBML 推導顯示方式：

```
DBML label: → haPDL 欄位顯示名稱
DBML sensitive: true → haPDL * 符號（遮罩）
DBML ref_code: → haPDL :select 下拉
DBML group: → haPDL 欄位分組
```

### 2.3 EMIT Page Intent 清單

EMIT 將要生成的 haPDL 清單（不寫入）：

```
計畫生成 haPDL：
  - order-list.hapdl.yaml (type: list, entity: Order)
  - order-form.hapdl.yaml (type: form, entity: Order)
  - refund-wizard.hapdl.yaml (type: wizard, entity: Refund)
  ...
```

---

## 輸出（傳遞給步驟 4）

一份 page_intent_map：

```yaml
page_intents:
  - page_id: order-list
    type: list
    entity: Order                    # case-sensitive
    api: order                       # 對應 haAPI api: order
    title: 訂單列表
    auth_roles: [staff, admin]
    view:
      filters: [customerId=, status=, createdAt^]
      columns: [orderId#, customerId, status:badge, totalAmount|currency, createdAt|date^]
    actions:
      standard: [create, export]
      placement: { header: [create, export] }
    security:
      permission_refs:
        view: [{id: order_read}]
        create: [{id: order_create}]
      datasource_scope: department
    source: features/order-management.feature
```
