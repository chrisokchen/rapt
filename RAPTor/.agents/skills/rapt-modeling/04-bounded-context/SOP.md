# 04 Bounded Context SOP

**目的**：確立 Bounded Context 邊界（與 DBML Aggregate 對齊），定義 Context Map 以描述 Context 間的關係。

---

## 步驟

### 4.1 DERIVE Bounded Context 邊界

基於 `01-entity-and-aggregate` 的 entity_map 和初步分群，正式劃定 Bounded Context：

```
Bounded Context = 一組有統一語言的業務能力邊界
  - 每個 Context 有一個名稱（領域術語）
  - 每個 Context 包含若干 Aggregate
  - Context 邊界 = 術語意義改變的地方
```

### 4.2 DERIVE Context Map

```
Context Map 關係類型：
  - Shared Kernel：共用 Aggregate（如共用 User）
  - Customer-Supplier：一方依賴另一方的 API
  - Conformist：下游照單全收上游模型
  - Anti-Corruption Layer：下游有轉換層
  - Open Host Service：提供公開 API（通常是 haAPI 的邊界）
```

### 4.3 EMIT Context 分析摘要

EMIT Context Map 草圖（不寫入 DBML，只做文件記錄）：

```markdown
## Bounded Contexts

### {Context A}
  包含：[Aggregate1, Aggregate2]
  關係：Customer of {Context B}

### {Context B}
  包含：[Aggregate3]
  關係：Supplier to {Context A}
```

### 4.4 UPDATE schema.dbml 加入 Context 分組（可選）

若 DBML 工具支援，用 Table Group 標注 Context 歸屬：

```dbml
TableGroup OrderContext {
  Order
  OrderItem
}

TableGroup CatalogContext {
  Product
  Category
}
```

**注意**：TableGroup 是可選的視覺化輔助，不影響 haARM/haAPI 設計。

---

## 邊界規則

- **Context 邊界不等於 DB Schema 邊界**（monolith 中所有 Table 可在同一個 DB）
- **Context 邊界影響 haAPI 設計**：跨 Context 的讀取通過 haAPI 端點，不直接 JOIN
- 若有明顯的 Context 衝突：記 CiC `CON`
