# 問題格式規範（Question Format）

本文件定義 `rapt-clarify-loop` 向使用者呈現問題時的統一格式。

---

## 問題呈現格式

當 `rapt-clarify-loop` 執行 `ASK` 時，以以下格式呈現問題集：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 RAPTor 釐清 Session [{batch_id}]
共 {N} 個問題，請逐一回答
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【Q{序號}/{total}】{問題標題} [{CiC-id}]

類型：{GAP | ASM | CON | BDY}
📍 來源：{location}

{問題描述}

⚠️ 影響：{impact}

選項（可直接回答字母，或自由輸入）：
  A) {option_A}
  B) {option_B}（建議）
  C) {option_C}

若選擇維持假設，請回「OK」或「保留 ASM」

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

（問題 2、3...依序列出）
```

---

## 不同類型問題的呈現差異

### GAP（資訊缺失）

```
【Q1/3】訂單折扣計算層級 [CiC-240601-001]

類型：GAP（缺少必要資訊，無法繼續設計）
📍 來源：schema.dbml#Order

「折扣率」是作用在訂單整體，還是每個商品明細上？

⚠️ 影響：會影響 Order 和 OrderItem 的 DBML 欄位設計

選項：
  A) 訂單整體折扣（Order.discountRate）
  B) 商品明細折扣（OrderItem.discountRate）
  C) 兩層都有（Order 和 OrderItem 各有折扣率）
```

### ASM（假設確認）

```
【Q2/3】退款申請的 Stakeholder 對應 [CiC-240601-002]

類型：ASM（已做假設，請確認）
📍 來源：01-stakeholders.md

目前假設「退款審核員」是一個獨立的系統角色（非客服人員）。

⚠️ 影響：haARM role 設計

請確認：
  A) 正確，退款審核員是獨立角色
  B) 不對，退款由客服人員處理（不需獨立角色）
  C) 補充：{請說明實際情況}

（若無意見，回「OK」維持現有假設）
```

### CON（衝突裁決）

```
【Q3/3】訂單狀態欄位名稱衝突 [CiC-240601-003]

類型：CON（兩份文件有衝突）
📍 來源：schema.dbml vs order-checkout.feature

衝突：
  - DBML 中：Order.status（nchar(1)，ref_code: OrderStatus）
  - Gherkin 中：Scenario 提到「訂單狀態為「pending」」（英文 lowercase）

⚠️ 影響：ref_code 的值集合設計和 Gherkin 術語一致性

請裁決：
  A) 以 DBML 為準（值集合用大寫代碼，Gherkin 術語用中文）
  B) 以 Gherkin 為準（值集合用英文 lowercase）
  C) 兩者都更新，使用新的一致標準：{請說明}
```

---

## 回答記錄格式

使用者回答後，`rapt-clarify-loop` 記錄：

```markdown
### Q1 [CiC-240601-001] 回答：B

> 回答時間：2024-06-01 14:30
> 原始回答：「B，商品明細層級折扣，但要保留未來支援訂單整體折扣的可能性」
> 決策摘要：OrderItem.discountRate（decimal(5,4)）；Order 層不加折扣欄位，保留擴展彈性
> 待套用：rapt-clarify/04-decision-apply
```
