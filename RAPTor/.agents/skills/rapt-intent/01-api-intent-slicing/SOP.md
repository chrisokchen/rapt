# 01 API Intent Slicing SOP

**目的**：從 DBML Entity + haARM + Gherkin Feature 切分 API 意圖，為每個主要 Entity 確定需要哪些 haAPI 檔案。

---

## 步驟

### 1.1 DERIVE API Intent 清單

對每個 DBML Table（含 Aggregate Root）：

```
API Intent = 一個 Entity 需要的 API 能力集合
對每個 Table DERIVE：
  - api_id: <kebab-case of Table Name>  ← 對應 haAPI api: 頂層
  - entity: <DBML Table Name>           ← case-sensitive
  - standard_operations: [list, create, read, update, delete]（依業務需求選取）
  - custom_operations: []               ← Gherkin 中超出 CRUD 的業務動作
  - access_roles: [<從 haARM 取得的 roles>]
  - list_capabilities: { filters, sorting, pagination, search }
```

**Gherkin → custom_operations 對應**：  
掃描 Gherkin Feature/Scenario 中的業務動作，若超出 list/read/create/update/delete：

```
範例：
  "客戶申請退款" → operation: applyRefund
  "管理員審核退款" → operation: approveRefund
  "匯出訂單報表" → operation: exportOrders
```

### 1.2 VALIDATE haARM 引用

對每個 API Intent 中的 access_roles 和 permissions：
- ASSERT 每個 role.id 存在於 haARM
- ASSERT 每個 permission.id 存在於 haARM
- 若不存在：記 CiC `BDY`，DELEGATE to `rapt-reconcile`（機械性補 id）

### 1.3 EMIT API Intent 清單

EMIT 將要生成的 haAPI 清單（不寫入）：

```
計畫生成 haAPI：
  - order.haapi.yaml (entity: Order, ops: [list,create,read,update] + applyRefund)
  - order-item.haapi.yaml (entity: OrderItem, ops: [list,create,update,delete])
  ...
```

---

## 輸出（傳遞給步驟 3）

一份 api_intent_map：

```yaml
api_intents:
  - api_id: order
    entity: Order                    # case-sensitive
    title: 訂單管理
    standard: [list, create, read, update]
    operations:
      - name: applyRefund
        actor: customer
        source: features/refund.feature#Scenario:客戶申請退款
    access:
      roles: [customer, staff, admin]
      source: access-control/shop.haarm.yaml#roles
    list:
      filters: [customerId, status, createdAt]
      sorting: [createdAt]
      pagination: offset
```
