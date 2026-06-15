# 01 Entity & Aggregate SOP

**目的**：從 Gherkin Feature 和 Discovery artifacts 識別核心業務實體（Entity）、Aggregate、Value Object，為 DBML 建模奠定基礎。

---

## 步驟

### 1.1 DERIVE Entity Candidates

從以下 source DERIVE 實體候選人：

```
來源：
  - ${high_gherkin_dir}/*.feature → Feature/Scenario 中的業務名詞
  - ${disc_dir}03-event-timeline.md → Domain Event 中的業務物件
  - ${disc_dir}01-stakeholders.md → Actor 相關的業務物件
```

對每個候選實體記錄：

```
- name: <PascalCase，對應未來 DBML Table Name>
- description: <一行業務描述>
- key_properties: [<核心屬性（業務語言）>]
- identified_from: <source 引用>
```

### 1.2 CLASSIFY Entity / Aggregate / Value Object

```
Entity = 有身份（ID）的業務物件，生命週期獨立
Aggregate = 一組強相關 Entity 的邊界（Aggregate Root 是 Entity）
Value Object = 無身份，由值定義（地址、金額等）
```

### 1.3 DERIVE Aggregate 邊界

對每個 Aggregate，確定：
- Aggregate Root（對外的唯一入口）
- 包含的 Entity / Value Object
- 跨 Aggregate 的引用方式（只用 ID，不直接嵌入）

### 1.4 EMIT Entity 分析摘要

EMIT 實體列表供確認（不 ASK，只 EMIT）：

```
已識別的實體（{N} 個）：
  Aggregates: [...]
  Entities: [...]
  Value Objects: [...]

若有明顯缺漏或重複，請告知後執行 /rapt-clarify
```

---

## 輸出（傳遞給步驟 2）

一份結構化的 entity_map：

```yaml
entities:
  - name: Order             # PascalCase
    type: aggregate_root
    description: 客戶訂單
    key_properties: [orderId, customerId, status, totalAmount]
    source: features/order-checkout.feature#Scenario:成功提交訂單
  - name: OrderItem
    type: entity
    parent_aggregate: Order
    description: 訂單明細
    key_properties: [itemId, productId, quantity, unitPrice]
    source: features/order-checkout.feature
```
