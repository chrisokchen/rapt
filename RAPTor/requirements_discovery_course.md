# 需求發掘與分析旅程：從混沌到秩序

**時間**: 150 分鐘 (2.5 小時)  
**目標**: 掌握從模糊的業務需求到精確的 DBML/haPDL 規格的完整方法論。  
**核心策略**: "Learn by Doing" (做中學) - 透過實際案例與工作坊，體驗完整的需求發掘流程。  
**前置知識**: 已了解 WA-RAPTor 的工具鏈（haPDL → PDL → App）。

---

## 課程大綱 (Agenda)

1.  **開場與動機 (Introduction)** - 10 mins
    *   銜接上次課程：從「工具鏈」到「思考鏈」
    *   核心問題：如何產出高品質的規格？
2.  **Module 1: 業務探索 - Event Storming 工作坊 (Business Discovery)** - 50 mins
    *   理論：為什麼需要 Event Storming？
    *   實戰：「線上訂餐系統」案例的 Event Storming
    *   產出：領域事件全景圖
3.  **Module 2: 領域建模 - 從事件到 DBML (Domain Modeling)** - 40 mins
    *   從 Event Storming 萃取實體
    *   定義實體關係與約束
    *   撰寫第一版 DBML
4.  **Module 3: 需求澄清 - 結構化提問法 (Requirements Clarification)** - 25 mins
    *   掃描規格的模糊點
    *   結構化提問範例
    *   更新 DBML 與業務規則
5.  **Module 4: 規格制定 - 從意圖到規格 (Specification Formulation)** - 20 mins
    *   撰寫 High-level Gherkin
    *   撰寫 haPDL（極簡版）
    *   連結到 WA-RAPTor 工具鏈
6.  **結語與實務建議** - 5 mins

---

## 詳細腳本 (Script)

### 0. 開場與動機 (10 mins)

#### 銜接上次課程
*   **回顧**: 「上次課程中，我們看到了 WA-RAPTor 的『魔術』——只要有 haPDL 和 DBML，就能自動生成前端、API、測試。」
*   **提問**: 「但是，**haPDL 和 DBML 是從哪裡來的**？它們不會憑空出現。今天我們要解決這個問題。」

#### 核心問題
*   **展示一個糟糕的規格**:
    ```yaml
    # 糟糕的 haPDL 範例
    page: user-page
    fields: [name, email, status]  # 沒有型別、沒有驗證規則
    ```
*   **展示一個好的規格**:
    ```yaml
    # 良好的 haPDL 範例 (參考 user-list.hapdl.yaml)
    page: user-list
    entity: User
    filters: [name~, email@, status=]
    columns: [id, name!, email, status:badge, created_at|date]
    ```
*   **差異**: 「好的規格是『精確』、『可推導』、『有脈絡』的。要達到這個水準，我們需要一套**系統化的思考流程**。」

#### 今日目標
*   「今天我們要走過完整的七階段流程，從『客戶說他想要一個訂餐系統』，一路走到『產出高品質的 DBML 與 haPDL』。」
*   「這個流程叫做『需求發掘與分析流程』，它是 WA-RAPTor 的**上游**。」

---

### Module 1: 業務探索 - Event Storming 工作坊 (50 mins)

**目標**: 透過協作式工作坊，快速探索業務流程與領域知識。

#### 1.1 理論基礎 (10 mins)

**什麼是 Event Storming？**
*   **定義**: 一種視覺化的協作技術，用便利貼在牆上（或數位白板上）快速建模業務流程。
*   **發明者**: Alberto Brandolini (DDD 社群)。
*   **核心理念**: 「與其讓專家口述、分析師抄寫，不如讓大家一起貼便利貼，直接視覺化業務流程。」

**為什麼需要 Event Storming？**
1.  **打破資訊不對稱**: 業務專家、開發者、設計師都在同一個房間（或視訊會議），面對同一張圖。
2.  **快速**: 2-3 小時就能產出一個複雜系統的全景圖。
3.  **發現隱藏的假設**: 「訂單送出後會發生什麼？」這種問題在口述時容易被忽略，但在 Event Storming 中會被強制攤開。

**Event Storming 的語言（便利貼顏色）**:
*   **橘色 (Domain Event)**: 業務事件，過去式。例如：「訂單已建立」、「付款已完成」。
*   **藍色 (Command)**: 觸發事件的命令/動作。例如：「提交訂單」、「確認付款」。
*   **黃色 (Actor)**: 執行命令的角色。例如：「顧客」、「廚師」、「外送員」。
*   **黃色大 (Aggregate)**: 處理命令並產生事件的業務概念。例如：「訂單」、「菜單」。
*   **紫色 (Policy/Rule)**: 自動化規則。例如：「當付款完成，自動通知廚房」。
*   **粉紅色 (Hotspot)**: 問題點、待澄清的地方。例如：「如果顧客取消訂單，已備料的成本誰負擔？」

#### 1.2 實戰演練：「線上訂餐系統」(30 mins)

**情境設定**:
*   **業務願景**: 「我們要做一個線上訂餐平台，讓顧客可以瀏覽菜單、下單、付款，然後由餐廳接單、備餐、外送。」
*   **參與角色**: PO (產品負責人)、BA (業務分析師)、架構師、前端開發者。

**Step 1: 混亂探索 (10 mins)**
*   **指令**: 「請大家把腦中『線上訂餐』這件事會發生的所有事件（橘色便利貼）都貼出來，不用管順序。」
*   **範例事件**:
    *   訂單已建立
    *   付款已完成
    *   餐廳已接單
    *   餐點已備好
    *   外送員已取餐
    *   餐點已送達
    *   顧客已評價
    *   訂單已取消
    *   退款已完成

**Step 2: 時間線排序 (5 mins)**
*   **指令**: 「把這些事件按照時間順序排列。」
*   **結果**: 一條從左到右的時間線，展示完整的業務流程。

**Step 3: 識別命令與角色 (10 mins)**
*   **指令**: 「為每個事件加上『誰』(黃色) 做了『什麼』(藍色)，才觸發這個事件？」
*   **範例**:
    ```
    [顧客] --[提交訂單]--> [訂單已建立]
    [顧客] --[確認付款]--> [付款已完成]
    [餐廳] --[接受訂單]--> [餐廳已接單]
    ```

**Step 4: 識別聚合 (5 mins)**
*   **指令**: 「哪些業務概念負責處理這些命令？用黃色大便利貼標出來。」
*   **範例聚合**:
    *   **Order (訂單)**: 處理「提交訂單」、「取消訂單」。
    *   **Payment (付款)**: 處理「確認付款」、「退款」。
    *   **Delivery (外送)**: 處理「指派外送員」、「確認送達」。

**Step 5: 標記 Hotspot (待澄清問題)**
*   **範例問題**:
    *   ❓ 「訂單建立後多久內，顧客可以取消？」
    *   ❓ 「如果外送員遲到，有自動補償機制嗎？」
    *   ❓ 「餐廳可以拒絕訂單嗎？在什麼情況下？」

#### 1.3 產出物展示 (10 mins)
*   **展示完整的 Event Storming 圖**（投影在螢幕上或分享 Miro/Mural 連結）。
*   **小結**:
    *   「我們在 30 分鐘內，視覺化了整個訂餐系統的業務流程。」
    *   「橘色事件是『發生了什麼』，藍色命令是『使用者做了什麼』，黃色大聚合是『核心業務概念』。」
    *   「接下來，我們要把這些便利貼『翻譯』成 DBML。」

---

### Module 2: 領域建模 - 從事件到 DBML (40 mins)

**目標**: 將 Event Storming 的視覺化產出，轉換為結構化的 DBML 資料模型。

#### 2.1 轉換規則 (10 mins)

**從 Event Storming 到 DBML 的對應**:

| Event Storming 元素 | DBML 元素 | 範例 |
|:---|:---|:---|
| **聚合 (黃色大)** | **Table** | `Order` → `Table Order` |
| **事件 (橘色)** | **狀態欄位** | 「訂單已建立」 → `status = 'created'` |
| **命令 (藍色)** | **操作/方法** (註記在 Note 中) | 「提交訂單」 → `Note: 'createOrder()'` |
| **角色 (黃色)** | **外鍵關聯** | 「顧客」 → `customer_id` |
| **屬性 (隱含)** | **Column** | 訂單的「總金額」 → `total decimal` |

**實體識別原則**:
1.  **聚合 = 實體**: Event Storming 中的黃色大便利貼，幾乎直接對應到 DBML 的 Table。
2.  **事件 = 狀態**: 如果一個實體有多個事件（例如：「訂單已建立」、「訂單已完成」），通常代表它有一個 `status` 欄位。
3.  **命令 = 操作**: 命令不會直接變成欄位，但可以寫在 Table 的 `Note` 中，說明這個實體支援哪些操作。

#### 2.2 實戰演練：撰寫 DBML (25 mins)

**Step 1: 識別核心實體 (5 mins)**

從 Event Storming 圖中，我們識別出以下聚合：
*   **Order (訂單)**
*   **OrderItem (訂單項目)**
*   **Customer (顧客)**
*   **Restaurant (餐廳)**
*   **Menu (菜單)**
*   **MenuItem (菜單項目)**
*   **Payment (付款)**
*   **Delivery (外送)**

**Step 2: 定義實體屬性 (10 mins)**

以 **Order** 為例：

```dbml
Table Order {
  order_id varchar(36) [pk, not null, note: '訂單唯一識別碼 (UUID)']
  customer_id varchar(36) [not null, note: '顧客識別碼']
  restaurant_id varchar(36) [not null, note: '餐廳識別碼']
  total decimal(10,2) [not null, note: '訂單總金額']
  status varchar(20) [not null, default: 'pending', note: '訂單狀態: pending/confirmed/preparing/ready/delivering/completed/cancelled']
  delivery_address text [not null, note: '外送地址']
  created_at timestamp [not null, default: `now()`]
  updated_at timestamp [not null, default: `now()`]

  Note: '''
  訂單聚合根
  操作: createOrder(), cancelOrder(), confirmOrder()
  事件: OrderCreated, OrderConfirmed, OrderCancelled, OrderCompleted
  '''
}
```

**關鍵點**:
*   **狀態列舉**: `status` 欄位涵蓋了所有可能的訂單狀態（對應 Event Storming 中的橘色事件）。
*   **不變條件**: `total >= 0`（可以寫在 Note 中）。
*   **外鍵**: `customer_id` 和 `restaurant_id` 對應到黃色便利貼的角色。

**Step 3: 定義實體關係 (10 mins)**

```dbml
Ref: Order.customer_id > Customer.customer_id [note: '一個顧客可以有多個訂單']
Ref: Order.restaurant_id > Restaurant.restaurant_id [note: '一個餐廳可以接收多個訂單']
Ref: OrderItem.order_id > Order.order_id [note: '一個訂單包含多個訂單項目']
Ref: OrderItem.menu_item_id > MenuItem.menu_item_id [note: '訂單項目引用菜單項目']
Ref: Payment.order_id > Order.order_id [note: '一個訂單對應一筆付款']
Ref: Delivery.order_id > Order.order_id [note: '一個訂單對應一次外送']
```

**關鍵點**:
*   **一對多 vs. 多對多**: 訂單與訂單項目是「一對多」，訂單項目與菜單項目是「多對一」。
*   **聚合邊界**: `Order` 是聚合根，`OrderItem` 是聚合內部的實體。外部不能直接操作 `OrderItem`，必須透過 `Order`。

#### 2.3 產出物展示 (5 mins)
*   **展示完整的 DBML 檔案** (`1-DBML.dbml`)。
*   **小結**:
    *   「我們已經把 Event Storming 的便利貼，轉換成結構化的資料模型。」
    *   「這個 DBML 就是 WA-RAPTor 的『字典』，所有後續的 haPDL、TypeSpec 都會參考它。」

---

### Module 3: 需求澄清 - 結構化提問法 (25 mins)

**目標**: 系統化識別規格中的模糊點，透過結構化提問獲得明確答案。

#### 3.1 為什麼需要需求澄清？(5 mins)

**常見問題**:
*   **模糊的約束**: 「訂單總金額可以是零嗎？」（例如全額折扣）
*   **邊界條件不清**: 「訂單建立後多久內可以取消？」
*   **狀態轉換規則**: 「訂單可以從 `delivering` 直接變成 `cancelled` 嗎？」

**不澄清的後果**:
*   開發者根據假設實作 → 上線後發現不符合業務規則 → 重工。
*   測試案例不完整 → Bug 漏網 → 客戶抱怨。

#### 3.2 結構化提問法 (15 mins)

**掃描清單** (參考 `0_reqDevProcess/01-整體流程架構.md` 的 Phase 3):

**A. 資料模型檢查**
```
- [ ] 數值屬性的範圍限制是否明確？
      例如：Order.total 的最小值是 0 還是 0.01？
- [ ] 字串屬性的長度限制是否明確？
      例如：Customer.name 最多幾個字元？
- [ ] 狀態轉換規則是否完整？
      例如：Order.status 從 'pending' 可以直接變成 'cancelled' 嗎？
```

**範例澄清問題**:

**問題 1**: 「訂單總金額可以是零嗎？」

| 選項 | 描述 |
|:---|:---|
| A | 允許為零（例如全額折扣訂單） |
| B | 不允許為零，最小值為 0.01 |
| C | 視訂單類型而定 |

**假設答案**: B (不允許為零)

**更新 DBML**:
```dbml
total decimal(10,2) [not null, note: '訂單總金額，必須 >= 0.01']
```

---

**問題 2**: 「訂單建立後多久內可以取消？」

| 選項 | 描述 |
|:---|:---|
| A | 只要訂單狀態是 'pending'，隨時可以取消 |
| B | 建立後 15 分鐘內可以取消 |
| C | 一旦餐廳接單 (confirmed)，就不能取消 |

**假設答案**: C (餐廳接單後不可取消)

**更新業務規則**:
```markdown
## Rule: 訂單取消規則
- 如果 `status = 'pending'`，顧客可以取消訂單。
- 如果 `status = 'confirmed'` 或之後，不可取消。
```

#### 3.3 產出物展示 (5 mins)
*   **展示澄清問題列表** (`.clarify/` 目錄)。
*   **展示更新後的 DBML**。
*   **小結**:
    *   「需求澄清不是『一次性』的工作，而是持續的對話。」
    *   「每次澄清，我們都讓規格更加『精確』。」

---

### Module 4: 規格制定 - 從意圖到規格 (20 mins)

**目標**: 將澄清後的需求，轉換為 Gherkin 與 haPDL。

#### 4.1 撰寫 High-level Gherkin (10 mins)

**從業務規則到 Gherkin**:

以「訂單取消規則」為例：

```gherkin
# 2-HighLevel-Gherkin.feature

Feature: 訂單管理
  身為顧客
  我想要能夠取消訂單
  以便在改變心意時不被扣款

  Background:
    Given 系統中存在以下訂單:
      | order_id | status    | created_at         |
      | ORD-001  | pending   | 2024-01-15 10:00  |
      | ORD-002  | confirmed | 2024-01-15 09:00  |

  Rule: 只有 pending 狀態的訂單可以取消

    Example: 成功取消 pending 訂單
      Given 訂單 "ORD-001" 的狀態為 "pending"
      When 顧客嘗試取消訂單 "ORD-001"
      Then 訂單應該成功取消
      And 訂單狀態應變更為 "cancelled"

    Example: 無法取消已確認的訂單
      Given 訂單 "ORD-002" 的狀態為 "confirmed"
      When 顧客嘗試取消訂單 "ORD-002"
      Then 應該顯示錯誤訊息 "訂單已被餐廳接受，無法取消"
      And 訂單狀態應保持為 "confirmed"
```

**關鍵點**:
*   **Rule**: 一條業務規則對應一個 `Rule` 區塊。
*   **Example**: 每個 Rule 至少有一個正向範例和一個反向範例。

#### 4.2 撰寫 haPDL (10 mins)

**從 DBML 與業務需求到 haPDL**:

```yaml
# 4-haPDL.yaml

page: order-list
type: list
title: 我的訂單
entity: Order

view:
  filters:
    - status=              # 自動推導：status 是 enum，生成下拉選單
    - created_at|daterange # 日期範圍篩選

  columns:
    - order_id
    - restaurant.name      # 自動推導：join Restaurant table
    - total|currency       # 貨幣格式化
    - status:badge         # 徽章顯示（pending=藍, confirmed=綠）
    - created_at|datetime

actions:
  standard: [view, cancel]  # 取消按鈕只在 status=pending 時顯示

  custom:
    - name: cancel
      label: 取消訂單
      condition: status == 'pending'  # 客製化條件
      confirm: 確定要取消訂單嗎？
```

**關鍵點**:
*   **符號魔法**: `status=`、`total|currency`、`status:badge` 都是簡寫。
*   **自動推導**: haPDL 會去查 DBML，知道 `status` 是 enum，`restaurant_id` 是外鍵。
*   **條件邏輯**: `cancel` 按鈕只在符合條件時顯示。

---

### Module 5: 驗證、生成與迭代 (簡述) (10 mins)

**Phase 5: 驗證確認**
*   執行自動化工具，檢查 DBML、Gherkin、haPDL 的一致性。
*   例如：haPDL 中引用的 `Order.status`，是否在 DBML 中定義？

**Phase 6: 原型生成**
*   執行 WA-RAPTor Generator:
    ```
    DBML + haPDL → PDL → Vue 前端程式碼
    DBML + haAPI → TypeSpec → OpenAPI
    ```
*   產出互動式原型，展示給客戶看。

**Phase 7: 迭代精煉**
*   客戶測試原型，提出反饋。
*   更新 DBML/haPDL，重新生成。
*   重複直到滿意。

**小結**:
*   「Phase 1-4 是『人類的思考』，Phase 5-7 是『機器的工作』。」
*   「WA-RAPTor 的價值在於：一旦規格寫好，剩下的事情都能自動化。」

---

### 6. 結語與實務建議 (5 mins)

#### 回顧七階段
*   **Phase 1-2**: 用 Event Storming 和領域建模，把混沌變成秩序。
*   **Phase 3**: 用結構化提問，把模糊變成精確。
*   **Phase 4**: 用 Gherkin 和 haPDL，把需求變成規格。
*   **Phase 5-7**: 交給 WA-RAPTor，把規格變成程式碼。

#### 實務建議

**1. 不是每個專案都需要完整流程**
*   **小專案**: 跳過 Event Storming，直接寫 DBML。
*   **大專案**: 一定要做 Event Storming，避免「盲人摸象」。

**2. Event Storming 的成功關鍵**
*   **參與者多樣性**: 一定要有業務專家、開發者、設計師。
*   **時間控制**: 不要超過 3 小時，保持專注。
*   **視覺化工具**: 實體便利貼 > 數位白板 > 文件。

**3. DBML 是基石**
*   **投資時間在 DBML 上**: DBML 寫得好，後續的 haPDL、TypeSpec 都會自動變好。
*   **持續更新**: DBML 不是一次性產物，是「活文件」。

**4. 需求澄清是持續的**
*   **建立問題庫**: 把每次澄清的問題與答案記錄下來，形成團隊知識庫。
*   **自動化掃描**: 使用工具（或 AI）自動掃描 DBML/haPDL 的模糊點。

#### Call to Action
*   「回去後，找一個小專案，試著跑一次 Event Storming → DBML → haPDL 的流程。」
*   「把 `0_reqDevProcess/templates/` 中的模板下載下來，當作起點。」

---

## 延伸閱讀

*   [需求發掘與分析流程完整文件](0_reqDevProcess/README.md)
*   [整體流程架構詳解](0_reqDevProcess/01-整體流程架構.md)
*   [Event Storming 官方網站](https://www.eventstorming.com/)
*   [DBML 語法指南](https://www.dbml.org/)
*   [Specification by Example (Book)](https://gojko.net/books/specification-by-example/)

---

## 附錄：課程準備清單

### 講師準備
- [ ] 準備「線上訂餐系統」的 Event Storming 示範圖（Miro/Mural）
- [ ] 準備完整的 DBML 範例檔案
- [ ] 準備澄清問題範例（至少 5 個）
- [ ] 準備 haPDL 範例檔案

### 學員準備
- [ ] 攜帶筆記型電腦（選擇性：如果要實際撰寫 DBML）
- [ ] 閱讀 `0_reqDevProcess/README.md`（課前預習）
- [ ] 準備一個自己團隊的小案例（課後練習用）

### 工具準備
- [ ] 數位白板工具 (Miro/Mural/FigJam)，或實體便利貼與白板
- [ ] DBML 編輯器（VS Code + DBML extension）
- [ ] WA-RAPTor Generator（用於示範 Phase 6）
