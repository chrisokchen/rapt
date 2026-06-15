# 02 Question Packaging SOP

**目的**：將 backlog 中的 CiC 項目打包成有優先序、可批次回答的問題集，符合 `clarify_batch_size` 上限。

---

## 步驟

LOAD REF [rapt-clarify::templates/rascore-question-pack.md]

### 2.1 READ backlog

```
READ: ${clarify_dir}backlog.md
DERIVE: OPEN 項目列表（狀態為 OPEN 的所有 CiC）
```

若 OPEN 項目來源為 RAscore finding，保留：

- finding_id
- criterion
- category
- artifact / location
- recommendation

### 2.2 PRIORITIZE

```
優先序：
  1. CON（衝突，影響最廣）
  2. GAP（缺失，下游無法繼續）
  3. BDY（超界，但可先記錄）
  4. ASM（假設，可後確認）

同優先序內，依影響 artifact 的數量排序（影響越多越優先）。
```

### 2.3 PACKAGE into Batches

依 `policy.clarify_batch_size`（預設 5）分批：

```
每批最多 {clarify_batch_size} 個問題
每個問題包含：
  - ID
  - 問題描述（清楚，無術語堆砌）
  - 影響範圍（如果不回答，哪些 artifact 無法完成）
  - 建議選項（A / B / C，如有的話）
  - 預設假設（若有 ASM 的話）
  - RAscore finding context（若來源為 RAscore）
```

**問題打包格式**（交由 `rapt-clarify-loop` 使用）：

```yaml
batch_id: CLR-{YYMMDD}-{seq}
questions:
  - id: CiC-001
    type: GAP
    question: "訂單的折扣計算是訂單級別還是商品級別？"
    impact: "影響 Order.discountRate 欄位設計和 haARM 的計算邏輯"
    options:
      A: "訂單級別（整筆訂單一個折扣率）"
      B: "商品級別（每個 OrderItem 有獨立折扣率）"
      C: "兩者都有（訂單和商品各有折扣率）"
    recommendation: "B（商品級別，彈性更高）"
    assumption: "若無回答，暫以 B 為 ASM"
```

RAscore 來源問題使用 `templates/rascore-question-pack.md`，並至少提供：

```yaml
rascore_context:
  finding_id: RA-D4-001
  criterion: D4
  category: cross-spec-gap
  artifact: docs/02-data-model/schema.dbml
  location: rights / permissionMask
  recommendation: 釐清權限位元命名與限制規則
```

### 2.4 WRITE `${clarify_dir}decisions/batch-{CLR-id}.md`

```markdown
# Clarify Batch {CLR-id}

> 建立時間：{date}
> 狀態：PENDING

## 問題清單

### Q1 [{CiC-id}]：{問題}

**影響**：{impact}

**選項**：
- A：{option_A}
- B：{option_B}（建議）
- C：{option_C}

---

（以下問題依序...）

## 回答記錄

> 等待使用者回答...
```
