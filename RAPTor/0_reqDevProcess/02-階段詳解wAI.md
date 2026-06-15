# LLM 協助需求發掘流程：各階段詳細分析

> 本文件分析七階段需求發掘流程中，LLM 可以在哪些部分提供有效協助，並說明具體的做法與預期成果。

## 📋 目錄
- [總體原則](#總體原則)
- [Phase 1: 業務探索](#phase-1-業務探索)
- [Phase 2: 領域建模](#phase-2-領域建模)
- [Phase 3: 需求澄清](#phase-3-需求澄清)
- [Phase 4: 規格制定](#phase-4-規格制定)
- [Phase 5: 驗證確認](#phase-5-驗證確認)
- [Phase 6: 原型生成](#phase-6-原型生成)
- [Phase 7: 迭代精煉](#phase-7-迭代精煉)
- [LLM 協助效益評估](#llm-協助效益評估)
- [注意事項與限制](#注意事項與限制)

---

## 總體原則

### LLM 最適合協助的任務特徵

```
✅ 高度適合 LLM
- 結構化文本的生成與轉換
- 從範例中學習並產生類似內容
- 識別模式與提出建議
- 格式驗證與一致性檢查
- 多文件間的交叉引用分析

⚠️ 需要人工監督
- 業務邏輯的正確性判斷
- 領域知識的深度理解
- 利害關係人意圖的詮釋
- 優先級與決策判斷

❌ 不適合 LLM
- 利害關係人的直接訪談
- 複雜業務決策的最終拍板
- 完全自動化的規格生成（需要人工驗證）
```

### 協助模式分類

| 模式 | 說明 | 典型應用 |
|------|------|---------|
| **輔助生成** | LLM 生成初稿，人工審查與修正 | 撰寫 BDD Feature、API 規格 |
| **智能轉換** | LLM 將一種格式轉換為另一種 | Event → Entity、Feature → API |
| **自動檢查** | LLM 檢查規格的完整性與一致性 | 語法檢查、缺口分析 |
| **結構化提問** | LLM 生成澄清問題清單 | 識別模糊點、邊界條件 |
| **範例擴充** | LLM 根據規則生成測試案例 | BDD Example 生成 |
| **文件生成** | LLM 從規格生成說明文件 | 技術文件、API 文件 |

---

## Phase 1: 業務探索

### 1.1 訪談準備與記錄整理

#### 適合度：★★★★☆ (高)

**LLM 協助內容**：

**1. 生成訪談大綱**

```
給 AI 什麼：
- 專案背景簡介
- 訪談對象角色（PO、業務使用者、領域專家等）
- 訪談目標（理解業務流程、識別痛點、確認功能需求等）

要 AI 做什麼：
- 根據角色與目標生成結構化訪談大綱
- 包含開場、主要問題、追問問題、結尾
- 針對不同角色客製化問題

請 AI 生成什麼：
- 訪談問題清單（開放式與封閉式問題）
- 問題的優先級排序
- 預期收集的資訊類型
```

**範例提示詞**：

```
你是需求分析專家。請為以下情境生成訪談大綱：

專案背景：
我們正在開發一個電商訂單管理系統，要替換現有的 Excel 流程。

訪談對象：
- 角色：訂單管理專員
- 年資：5 年
- 日常工作：處理客戶訂單、追蹤出貨、處理退換貨

訪談目標：
1. 理解目前的訂單處理流程
2. 識別現有流程的痛點
3. 收集對新系統的期望

請生成：
1. 訪談大綱（包含 10-15 個主要問題）
2. 每個問題的追問方向
3. 需要特別注意的資訊點
```

**2. 訪談記錄的結構化整理**

```
給 AI 什麼：
- 訪談逐字稿或錄音轉文字結果
- 訪談大綱（用於對照）

要 AI 做什麼：
- 萃取關鍵資訊（痛點、需求、業務規則）
- 識別業務流程步驟
- 標記模糊或矛盾之處

請 AI 生成什麼：
- 結構化訪談摘要
- 痛點清單（依影響程度排序）
- 初步業務流程描述
- 待澄清問題清單
```

**範例提示詞**：

```
請分析以下訪談記錄，萃取關鍵資訊：

[訪談逐字稿]
訪談者：請描述您目前如何處理客戶訂單？
受訪者：我們收到訂單後，會先在 Excel 登記，然後手動檢查庫存...（省略）

請生成：
1. 當前流程摘要（步驟化）
2. 識別的痛點清單（標註影響程度：高/中/低）
3. 提到的業務規則
4. 模糊或不清楚的部分（需要追問）
```

### 1.2 User Journey Map 生成

#### 適合度：★★★☆☆ (中)

**LLM 協助內容**：

**生成 User Journey Map 初稿**

```
給 AI 什麼：
- Persona 描述（角色、目標、行為特徵）
- 訪談記錄中的使用場景描述
- 業務流程步驟

要 AI 做什麼：
- 識別旅程的主要階段 (Stages)
- 推測各階段的使用者行動 (Actions)
- 推測使用者的想法與情緒變化
- 識別可能的痛點 (Pain Points)

請 AI 生成什麼：
- User Journey Map (Markdown 表格格式)
- 包含：Stages、Actions、Thoughts、Emotions、Pain Points、Opportunities
```

**範例提示詞**：

```
請根據以下資訊生成 User Journey Map：

Persona: 訂單管理專員 Amy
- 目標：快速且準確地處理客戶訂單
- 特徵：熟悉 Excel，不熟悉複雜系統

業務流程：
1. 接收客戶訂單（Email 或電話）
2. 在 Excel 登記訂單資訊
3. 檢查庫存是否足夠
4. 確認訂單並通知客戶
5. 轉交倉庫出貨
6. 追蹤出貨狀態

請生成 User Journey Map，包含以下欄位：
- Stage（階段名稱）
- Actions（使用者行動）
- Thoughts（使用者想法）
- Emotions（情緒評分 -5 到 +5）
- Pain Points（痛點）
- Opportunities（改善機會）

以 Markdown 表格格式輸出。
```

**注意**：LLM 生成的情緒評分與痛點是「推測」，需要與實際使用者驗證。

### 1.3 Event Storming 輔助

#### 適合度：★★☆☆☆ (低-中)

**限制**：Event Storming 是高度互動的協作工作坊，LLM 無法直接參與。但可在**準備**與**後處理**階段協助。

**LLM 協助內容**：

**1. 事前準備：生成領域事件候選清單**

```
給 AI 什麼：
- 業務流程描述
- 訪談記錄中提到的業務活動

要 AI 做什麼：
- 識別可能的領域事件（過去式）
- 分類事件類型（核心流程、例外處理、通知等）

請 AI 生成什麼：
- 領域事件候選清單
- 每個事件的簡短描述
```

**範例提示詞**：

```
請從以下業務流程中識別領域事件（Domain Events）：

流程描述：
1. 客戶提交訂單
2. 系統檢查庫存
3. 庫存足夠時，建立訂單記錄
4. 庫存不足時，通知客戶
5. 訂單確認後，發送確認信
6. 倉庫揀貨出貨
7. 客戶收到商品

請生成：
- 領域事件清單（使用過去式，如「訂單已建立」）
- 事件的觸發條件
- 事件的參與角色
```

**2. 事後整理：數位化 Event Storming 輸出**

```
給 AI 什麼：
- Event Storming 照片或便利貼內容
- 工作坊記錄

要 AI 做什麼：
- 整理事件、命令、聚合、角色
- 建立事件的時間線
- 識別限界上下文邊界

請 AI 生成什麼：
- 結構化的 Event Storming 摘要
- Mermaid 圖表（事件流程）
- 聚合與限界上下文清單
```

### 1.4 業務願景文件撰寫

#### 適合度：★★★★☆ (高)

```
給 AI 什麼：
- 訪談摘要
- 專案背景資料
- 業務目標與 KPI

要 AI 做什麼：
- 撰寫業務願景文件初稿
- 結構化呈現：願景、目標、價值主張、關鍵成功因素

請 AI 生成什麼：
- 業務願景文件（Markdown 格式）
- 包含：Executive Summary、Vision、Goals、Success Criteria
```

**範例提示詞**：

```
請撰寫業務願景文件：

背景：
我們是一家中型電商公司，目前使用 Excel 處理訂單，流程效率低且容易出錯。

訪談摘要：
- 每日處理 50-100 筆訂單
- 人工庫存檢查耗時，常導致超賣
- 訂單狀態追蹤困難，客戶常來電詢問

專案目標：
1. 減少訂單處理時間 50%
2. 降低超賣錯誤率至 0.5% 以下
3. 提升客戶滿意度至 90%

請生成：
- 業務願景文件（包含 Vision、Goals、Value Proposition、Success Criteria）
- 使用清晰且具說服力的語言
- Markdown 格式
```

---

## Phase 2: 領域建模

### 2.1 從 Event Storming 萃取實體

#### 適合度：★★★★★ (極高)

這是 LLM 最擅長的任務之一：結構化轉換。

**LLM 協助內容**：

**從領域事件自動萃取實體與屬性**

```
給 AI 什麼：
- Event Storming 的事件清單
- 命令清單
- 聚合清單

要 AI 做什麼：
- 識別核心實體（從聚合推導）
- 為每個實體定義初步屬性
- 識別實體間的關係

請 AI 生成什麼：
- DBML 格式的實體定義
- 包含：Table、欄位、型別、關係、說明
```

**範例提示詞**：

```
請從以下 Event Storming 輸出中萃取領域實體並生成 DBML：

領域事件：
- 訂單已建立
- 訂單項目已加入
- 庫存已扣減
- 訂單已確認
- 訂單已取消

聚合：
- 訂單 (Order)
- 商品 (Product)
- 客戶 (Customer)

命令：
- 建立訂單
- 加入訂單項目
- 確認訂單
- 取消訂單

請生成：
1. DBML 格式的實體定義
2. 包含合理的屬性（id、名稱、狀態、時間戳等）
3. 定義實體間的關係（Ref）
4. 為每個 Table 和欄位加上說明（note）
```

**預期輸出**：

```dbml
Table Order {
  order_id varchar(36) [pk, note: '訂單唯一識別碼']
  customer_id varchar(36) [not null, ref: > Customer.customer_id, note: '客戶識別碼']
  total decimal(10,2) [not null, note: '訂單總金額']
  status varchar(20) [not null, note: '訂單狀態: pending/confirmed/cancelled']
  created_at timestamp [not null, default: `now()`]
  updated_at timestamp [not null, default: `now()`]

  Note: '''
  訂單聚合根
  不變條件: total = sum(OrderItem.subtotal)
  '''
}

Table Customer {
  customer_id varchar(36) [pk]
  name varchar(100) [not null]
  email varchar(255) [unique, not null]
  created_at timestamp [not null, default: `now()`]
}

Table OrderItem {
  order_item_id varchar(36) [pk]
  order_id varchar(36) [not null, ref: > Order.order_id]
  product_id varchar(36) [not null, ref: > Product.product_id]
  quantity int [not null, note: '數量，必須 >= 1']
  price decimal(10,2) [not null]
  subtotal decimal(10,2) [not null]
}
```

### 2.2 通用語言詞彙表生成

#### 適合度：★★★★☆ (高)

```
給 AI 什麼：
- DBML 實體定義
- Event Storming 輸出
- 訪談記錄中的業務術語

要 AI 做什麼：
- 識別核心業務術語
- 為每個術語提供明確定義
- 列出可能的別名或同義詞

請 AI 生成什麼：
- 通用語言詞彙表（Markdown 表格）
- 包含：術語、定義、別名、範例
```

**範例提示詞**：

```
請從以下資訊中建立通用語言詞彙表：

DBML 實體：Order, Customer, Product, OrderItem, Cart

Event Storming 術語：
- 訂單已建立、庫存已扣減、訂單已確認

訪談記錄片段：
- "客戶下單後，我們會建立訂購單..."
- "如果庫存不足，訂單會標記為待補貨..."

請生成 Markdown 表格，包含：
| 術語 | 定義 | 別名 | 範例 |

注意：
- 使用業務語言而非技術術語
- 確保定義清晰且無歧義
- 列出所有可能造成混淆的別名
```

### 2.3 限界上下文識別

#### 適合度：★★★☆☆ (中)

```
給 AI 什麼：
- 完整的 DBML 實體模型
- Event Storming 的聚合清單
- 業務流程描述

要 AI 做什麼：
- 識別高內聚的實體群組
- 建議限界上下文劃分
- 說明劃分理由

請 AI 生成什麼：
- 限界上下文清單
- 每個上下文包含的實體
- 上下文間的依賴關係
- Mermaid 圖表
```

**範例提示詞**：

```
請分析以下實體模型，建議限界上下文 (Bounded Context) 劃分：

實體：
- Order, OrderItem
- Product, Category, ProductVariant
- Customer, Address, PaymentMethod
- Inventory, Stock, Warehouse
- Shipment, Carrier, TrackingInfo

請生成：
1. 建議的限界上下文清單（如 Sales Context, Catalog Context 等）
2. 每個上下文包含的實體
3. 上下文間的依賴關係
4. 劃分理由（基於業務內聚性）
5. Mermaid 圖表展示上下文關係
```

### 2.5 角色/權限建模 (haARM) — AI 輔助

#### 適合度：★★★★☆ (高)

LLM 可從 Event Storming 的角色欄位和 DBML 實體自動生成 haARM 初稿。

**LLM 協助內容**：

**從 Event Storming 角色與 DBML 實體生成 haARM**

```
給 AI 什麼：
- Event Storming 的「相關角色」欄位
- DBML 實體清單
- 業務規則中涉及權限的部分

要 AI 做什麼：
- 提取並分類 actors（user/system/service/external）
- 將 actors 歸納為 roles，建立繼承關係
- 從 DBML entity 建立 resources（1:1 映射）
- 為每個 resource 推導 CRUD+ 權限
- 識別互斥/依賴約束

請 AI 生成什麼：
- haARM v2 格式的 .haarm.yaml
```

**範例提示詞**：

```
根據以下 Event Storming 識別的角色和 DBML 實體，
請建立 haARM v2 的 actors、roles、resources、permissions 定義。

Event Storming 相關角色：
- 客戶、商家、系統管理員、API 閘道服務

DBML 實體：
- users, orders, products, cart, audit_log

業務規則：
- 客戶只能查看自己的訂單
- 商家只能管理自己的產品
- 管理員不能同時是商家
- 訂單刪除僅限營業時間

請生成完整的 .haarm.yaml，包含 constraints 區段。
```

**人工審查重點**：
- 權限是否過寬（如一個角色擁有所有 CRUD）
- 是否遺漏互斥約束（如 Maker-Checker）
- resource 與 DBML entity 是否對齊
- scope 設定是否正確（all vs own vs department）

---

## Phase 3: 需求澄清

### 3.1 自動化規格掃描

#### 適合度：★★★★★ (極高)

這是 LLM 極度擅長的任務：自動化檢查與缺口分析。

**LLM 協助內容**：

**1. 資料模型完整性掃描**

```
給 AI 什麼：
- DBML 實體模型
- 檢查清單（A1-A6: 實體完整性、屬性定義、邊界條件等）

要 AI 做什麼：
- 逐項檢查 DBML 是否符合完整性要求
- 識別缺失的約束條件
- 識別模糊的屬性定義

請 AI 生成什麼：
- 掃描報告（檢查項通過/失敗）
- 發現的問題清單
- 待澄清的問題（結構化格式）
```

**範例提示詞**：

```
請檢查以下 DBML 模型的完整性：

[DBML 內容]

檢查清單：
A1. 實體完整性
- 所有核心業務概念是否都已建模？
- 實體命名是否清晰且無歧義？

A2. 屬性定義
- 每個屬性是否都有明確的資料型別？
- 每個屬性是否都有充足的定義說明？

A3. 屬性值邊界條件
- 數值屬性的範圍限制是否明確？
- 最小值/最大值是否已定義？

A4. 跨屬性不變條件
- 屬性間的計算關係是否明確？

A5. 關係與唯一性
- 實體間的關聯關係是否完整？
- 主鍵與唯一性規則是否明確？

A6. 生命週期與狀態
- 具有狀態的實體是否定義了所有可能狀態？
- 狀態轉換規則是否完整？

請生成：
1. 檢查報告（每項檢查的通過/失敗狀態）
2. 發現的問題清單（具體指出哪個實體/屬性有問題）
3. 待澄清問題（使用結構化格式，包含問題、影響範圍、優先級）
```

**2. 生成結構化澄清問題**

```
給 AI 什麼：
- 掃描發現的問題
- 問題模板格式

要 AI 做什麼：
- 將問題轉換為結構化的澄清問題
- 提供多選項答案
- 評估影響範圍與優先級

請 AI 生成什麼：
- 結構化的澄清問題檔案（Markdown）
- 包含：問題、定位、多選題、影響範圍、優先級
```

**範例提示詞**：

```
請根據以下掃描結果，生成結構化的澄清問題：

發現問題：
- Order.total 屬性缺少最小值約束（不確定是否允許為零）
- Order.status 的所有可能值未明確列出
- OrderItem.quantity 與 Product.stock 的關係未明確（是否允許超賣）

問題模板格式：
# 澄清問題
[問題描述]

# 定位
[ERM 或 Feature 定位]

# 多選題
| 選項 | 描述 |

# 影響範圍
[列出受影響的元件]

# 優先級
[High/Medium/Low + 理由]

請為每個問題生成一個 Markdown 檔案。
```

**預期輸出範例**：

```markdown
# 澄清問題

訂單金額是否允許為零？

# 定位

ERM: Order.total 屬性

# 多選題

| 選項 | 描述 |
|------|------|
| A | 允許為零（例如全額折扣訂單） |
| B | 不允許為零，最小值為 0.01 |
| C | 視訂單類型而定（某些類型允許） |
| Short | 提供其他答案（<=5 字） |

# 影響範圍

- Order 實體的 total 屬性約束
- 建立訂單的前置條件驗證
- 訂單列表的篩選邏輯
- 付款流程（零元訂單可能跳過付款）

# 優先級

High
- 阻礙核心訂單建立功能的規格定義
- 影響資料庫約束與 API 驗證邏輯
```

### 3.2 邊界條件識別

#### 適合度：★★★★★ (極高)

```
給 AI 什麼：
- BDD Feature 的 Rule（業務規則）
- DBML 實體的約束條件

要 AI 做什麼：
- 識別所有可能的邊界條件
- 生成邊界值測試案例建議

請 AI 生成什麼：
- 邊界條件清單
- 建議的測試 Example（Gherkin 格式）
```

**範例提示詞**：

```
請識別以下業務規則的邊界條件並生成測試案例：

Rule: 訂單商品數量不可超過庫存

相關約束：
- OrderItem.quantity: int, >= 1
- Product.stock: int, >= 0

請生成：
1. 邊界條件清單（最小值、最大值、臨界點）
2. 建議的 BDD Example（Gherkin 格式）
3. 涵蓋：正常情況、邊界值、錯誤情況
```

**預期輸出**：

```gherkin
# 邊界條件清單
1. quantity = 1, stock = 0 (錯誤：庫存不足)
2. quantity = 1, stock = 1 (成功：剛好相等)
3. quantity = 1, stock = 2 (成功：庫存充足)
4. quantity = 10, stock = 10 (成功：剛好相等)
5. quantity = 11, stock = 10 (錯誤：超過庫存)
6. quantity = 0 (錯誤：不符合最小值約束)
7. quantity = -1 (錯誤：負數)

# 建議的 BDD Examples

Example: 庫存為零時應拒絕訂購
  Given 商品 "PROD-001" 的庫存為 0
  And 客戶的購物車包含:
    | product_id | quantity |
    | PROD-001   | 1        |
  When 客戶提交訂單
  Then 應該顯示錯誤訊息 "商品庫存不足"

Example: 數量剛好等於庫存應成功
  Given 商品 "PROD-001" 的庫存為 10
  And 客戶的購物車包含:
    | product_id | quantity |
    | PROD-001   | 10       |
  When 客戶提交訂單
  Then 應該成功建立訂單
  And 商品 "PROD-001" 的庫存應為 0

Example: 數量超過庫存應拒絕
  Given 商品 "PROD-001" 的庫存為 10
  And 客戶的購物車包含:
    | product_id | quantity |
    | PROD-001   | 11       |
  When 客戶提交訂單
  Then 應該顯示錯誤訊息包含 "庫存不足"
```

---

## Phase 4: 規格制定

### 4.1 撰寫 BDD Feature 文件

#### 適合度：★★★★★ (極高)

這是 LLM 最強項之一。

**LLM 協助內容**：

**1. 從需求描述生成 BDD Feature**

```
給 AI 什麼：
- 業務需求描述（自然語言）
- User Journey 的某個階段
- 相關的業務規則

要 AI 做什麼：
- 撰寫 BDD Feature（Gherkin 格式）
- 識別並拆解 Rule
- 為每個 Rule 生成 Example

請 AI 生成什麼：
- 完整的 .feature 檔案
- 包含：Feature、Background、Rule、Example
- 使用 Given-When-Then 結構
- 使用 Data Table 提供具體資料
```

**範例提示詞**：

```
請撰寫 BDD Feature 文件：

需求描述：
客戶可以建立新訂單。訂單必須至少包含一件商品，且商品數量不可超過庫存。訂單建立後，系統應扣減庫存並發送確認信給客戶。

業務規則：
1. 訂單必須至少包含一件商品
2. 訂單商品數量不可超過庫存
3. 訂單總金額 = sum(訂單項目.小計)
4. 訂單建立後應扣減庫存
5. 訂單建立後應發送確認信

相關實體：
- Order: order_id, customer_id, total, status
- OrderItem: order_item_id, order_id, product_id, quantity, price, subtotal
- Product: product_id, name, price, stock

請生成：
- 完整的 BDD Feature 文件（Gherkin 格式）
- 使用 Rule + Example 結構（不要用 Scenario）
- 每個 Rule 至少 2 個 Example（成功 + 失敗或邊界情況）
- 使用 Data Table 提供測試資料
- 包含 Background 減少重複
```

**2. 從現有 Example 擴展更多測試案例**

```
給 AI 什麼：
- 現有的 BDD Feature 文件
- 要求增加測試涵蓋率（邊界條件、錯誤處理）

要 AI 做什麼：
- 分析現有 Example 的涵蓋度
- 識別缺失的測試場景
- 生成補充的 Example

請 AI 生成什麼：
- 新的 Example（Gherkin 格式）
- 說明每個 Example 的測試目的
```

### 4.2 定義 API 規格 (TypeSpec)

#### 適合度：★★★★★ (極高)

**LLM 協助內容**：

**從 BDD Feature 自動生成 API 規格**

```
給 AI 什麼：
- BDD Feature 文件
- DBML 實體模型

要 AI 做什麼：
- 識別需要的 API 端點
- 定義請求與回應模型
- 定義驗證規則
- 定義錯誤回應

請 AI 生成什麼：
- TypeSpec 格式的 API 規格
- 包含：model、enum、interface、驗證規則、錯誤處理
```

**範例提示詞**：

```
請從以下 BDD Feature 生成 TypeSpec API 規格：

[BDD Feature 內容]

DBML 實體：
[DBML 內容]

請生成：
1. TypeSpec 檔案（完整且可編譯）
2. 定義所有需要的 model（對應 DBML 實體）
3. 定義 enum（如 OrderStatus）
4. 定義 API 端點（對應 BDD 的 When 步驟）
5. 包含驗證規則（@minValue、@maxValue 等）
6. 定義所有可能的錯誤回應（400, 404, 409 等）
7. 為所有 model 與 interface 加上 JSDoc 註解
```

### 4.3 設計 UI 規格 (YAML DSL)

#### 適合度：★★★★☆ (高)

```
給 AI 什麼：
- BDD Feature 文件
- API 規格（TypeSpec）
- 頁面類型（form、list、detail 等）

要 AI 做什麼：
- 設計頁面結構（layout、sections、components）
- 定義資料綁定（datasource）
- 定義使用者動作（actions）
- 定義驗證規則（validation）
- 定義效果鏈（effects）

請 AI 生成什麼：
- YAML 格式的頁面規格
- 符合 WA-RAPTor 的 Page DSL 格式
```

**範例提示詞**：

```
請從以下資訊生成 UI 頁面規格（YAML DSL）：

BDD Feature: 建立訂單
[Feature 內容]

API 端點：
- GET /cart - 取得購物車
- POST /orders - 建立訂單

頁面類型：form

請生成：
- YAML 格式的頁面規格
- 包含：page、datasource、layout、actions、validation、hooks
- 使用 WA-RAPTor 的 Page DSL 格式
- 定義完整的效果鏈（validation → api-call → navigate）
- 包含錯誤處理（onError）
```

### 4.4 建立可追溯矩陣

#### 適合度：★★★★☆ (高)

```
給 AI 什麼：
- User Journey Maps
- Event Storming 輸出
- BDD Features
- API 規格
- UI 規格
- DBML 模型

要 AI 做什麼：
- 建立需求與規格的對應關係
- 識別未涵蓋的需求
- 識別未追溯的規格

請 AI 生成什麼：
- 可追溯矩陣（Markdown 表格）
- 包含：Journey → Feature、Feature → API、Feature → UI、Event → Entity
```

**範例提示詞**：

```
請建立可追溯矩陣：

User Journey Stages:
[Journey 內容]

Event Storming Events:
[Events 內容]

BDD Features:
[Features 清單]

API Endpoints:
[API 清單]

UI Pages:
[Pages 清單]

DBML Tables:
[Tables 清單]

請生成 Markdown 格式的可追溯矩陣，包含：
1. User Journey → Features
2. Event Storming → Entities
3. Features → API Endpoints
4. Features → UI Pages
5. BDD Examples → Test Cases

識別並標記：
- 未涵蓋的 Journey Stages（缺少對應 Feature）
- 未追溯的 API 端點（缺少對應 Feature）
```

---

## Phase 5: 驗證確認

### 5.1 完整性檢查

#### 適合度：★★★★★ (極高)

```
給 AI 什麼：
- 所有規格文件（BDD、DBML、TypeSpec、YAML）
- 完整性檢查清單

要 AI 做什麼：
- 逐項檢查規格完整性
- 識別缺失的元件
- 識別不完整的定義

請 AI 生成什麼：
- 完整性檢查報告
- 包含：通過/失敗狀態、問題清單、修正建議
```

**範例提示詞**：

```
請檢查以下規格的完整性：

BDD Features: [檔案清單]
API Spec: [TypeSpec 內容]
Data Model: [DBML 內容]
UI Pages: [YAML 清單]

完整性檢查清單：
1. BDD Features
   - 每個 Feature 都有明確的業務價值描述？
   - 每個 Feature 至少有一個 Rule？
   - 每個 Rule 至少有一個 Example？
   - 所有 Example 都使用 Given-When-Then 結構？

2. API 規格
   - 所有 API 端點都有定義？
   - 所有請求/回應模型都已定義？
   - 所有錯誤情況都有對應的錯誤回應？
   - 所有驗證規則都已定義？

3. 資料模型
   - 所有實體都已定義？
   - 所有屬性都有型別與約束？
   - 所有關係都已建立？
   - 所有不變條件都已記錄？

4. UI 規格
   - 所有頁面都有對應的 YAML 檔案？
   - 所有互動都有定義的 actions？
   - 所有資料綁定都已定義？
   - 所有驗證規則都已定義？

請生成：
- 檢查報告（每項的通過/失敗狀態）
- 發現的問題清單（具體指出缺失內容）
- 修正建議（優先級排序）
```

### 5.2 一致性驗證

#### 適合度：★★★★★ (極高)

```
給 AI 什麼：
- 所有規格文件
- 通用語言詞彙表

要 AI 做什麼：
- 檢查術語一致性
- 檢查資料一致性（欄位名稱、型別）
- 檢查行為一致性（BDD 與 API 的對應）

請 AI 生成什麼：
- 一致性驗證報告
- 不一致之處清單
- 修正建議
```

**範例提示詞**：

```
請檢查以下規格的一致性：

BDD Feature: [內容]
TypeSpec API: [內容]
DBML: [內容]
YAML UI: [內容]
通用語言詞彙表: [內容]

檢查項目：
1. 術語一致性
   - 相同概念在所有規格中使用相同術語？
   - 無同義詞混用情況？

2. 資料一致性
   - BDD Example 中的資料符合 DBML 約束？
   - API 規格的欄位與 DBML 實體對應？
   - UI 規格的欄位與 API 規格對應？

3. 行為一致性
   - API 端點的行為與 BDD Feature 一致？
   - UI 頁面的行為與 BDD Example 一致？
   - 錯誤處理在各層級保持一致？

請生成：
- 一致性驗證報告
- 不一致之處清單（具體指出位置）
- 修正建議（標註影響範圍）
```

### 5.3 涵蓋率分析

#### 適合度：★★★★☆ (高)

```
給 AI 什麼：
- User Journey Maps
- BDD Features
- API 規格
- UI 規格

要 AI 做什麼：
- 計算業務需求涵蓋率
- 計算規則涵蓋率（有 Example 的比例）
- 計算 API 涵蓋率（CRUD 完整性）
- 計算 UI 涵蓋率

請 AI 生成什麼：
- 涵蓋率報告（量化指標）
- 未涵蓋的需求清單
- 改善建議
```

---

## Phase 6: 原型生成

### 6.1 Mock API 生成

#### 適合度：★★★★★ (極高)

```
給 AI 什麼：
- TypeSpec API 規格

要 AI 做什麼：
- 生成 Express.js Mock Server 程式碼
- 實作所有 API 端點
- 使用 Faker.js 生成真實感測試資料
- 實作基本的驗證邏輯

請 AI 生成什麼：
- 完整的 Mock Server 程式碼（TypeScript）
- 包含：路由定義、請求處理、資料生成、錯誤處理
```

**範例提示詞**：

```
請從以下 TypeSpec 規格生成 Express.js Mock Server：

[TypeSpec 內容]

要求：
1. 使用 TypeScript
2. 使用 Express.js 框架
3. 使用 @faker-js/faker 生成測試資料
4. 實作所有端點（GET、POST、PUT、DELETE）
5. 實作基本的驗證邏輯（對應 TypeSpec 的 @minValue 等）
6. 實作錯誤回應（400、404、409 等）
7. 程式碼應可直接執行（包含必要的 import）

請生成：
- server.ts（主程式）
- 必要的型別定義
- README.md（說明如何啟動）
```

### 6.2 UI 原型生成

#### 適合度：★★★★☆ (高)

```
給 AI 什麼：
- YAML UI 規格

要 AI 做什麼：
- 生成 React 元件程式碼
- 實作資料綁定
- 實作使用者互動（actions、effects）
- 實作驗證邏輯

請 AI 生成什麼：
- React 元件程式碼（TypeScript + TSX）
- 包含：useState、useEffect、事件處理、API 呼叫
```

**範例提示詞**：

```
請從以下 YAML UI 規格生成 React 元件：

[YAML 內容]

技術要求：
1. 使用 TypeScript
2. 使用 React Hooks（useState、useEffect）
3. 使用 TanStack React Query 處理 API 呼叫
4. 使用 Zod 進行驗證
5. 使用 Ant Design 元件庫

請生成：
- OrderCreationPage.tsx（主元件）
- 型別定義
- 驗證 Schema（Zod）
- README.md（說明如何使用）
```

### 6.3 測試案例生成

#### 適合度：★★★★★ (極高)

```
給 AI 什麼：
- BDD Feature 文件（Gherkin）

要 AI 做什麼：
- 生成 Playwright E2E 測試程式碼
- 實作所有 Example
- 包含資料準備、動作執行、結果驗證

請 AI 生成什麼：
- Playwright 測試程式碼（TypeScript）
- 包含：test、expect、page 操作
```

**範例提示詞**：

```
請從以下 BDD Feature 生成 Playwright E2E 測試：

[Gherkin Feature 內容]

技術要求：
1. 使用 Playwright + TypeScript
2. 使用 @cucumber/cucumber 整合 Gherkin
3. 實作所有 Step Definitions
4. 包含必要的 fixtures（資料準備）
5. 使用 Page Object Model 模式

請生成：
- steps/orderCreation.steps.ts（Step Definitions）
- pages/OrderCreationPage.ts（Page Object）
- fixtures/testData.ts（測試資料）
```

### 6.4 技術文件生成

#### 適合度：★★★★★ (極高)

```
給 AI 什麼：
- TypeSpec API 規格
- BDD Features
- DBML 模型

要 AI 做什麼：
- 生成 API 文件（Markdown）
- 生成資料模型文件
- 生成使用者指南

請 AI 生成什麼：
- 完整的技術文件（Markdown）
- 包含：API 端點說明、請求/回應範例、錯誤碼說明
```

**範例提示詞**：

```
請從以下 TypeSpec 規格生成 API 文件：

[TypeSpec 內容]

要求：
1. Markdown 格式
2. 包含所有 API 端點
3. 每個端點包含：描述、URL、HTTP Method、請求參數、回應範例、錯誤碼
4. 使用表格呈現參數列表
5. 使用程式碼區塊呈現 JSON 範例
6. 包含目錄與錨點連結

請生成：
- API-Documentation.md
```

---

## Phase 7: 迭代精煉

### 7.1 反饋分析與分類

#### 適合度：★★★★☆ (高)

```
給 AI 什麼：
- 使用者測試反饋（文字、表單回覆）
- 原有的規格文件

要 AI 做什麼：
- 分析反饋內容
- 分類問題類型（需求、規格、原型）
- 評估優先級與影響範圍

請 AI 生成什麼：
- 反饋分析報告
- 問題分類清單
- 修正建議（優先級排序）
```

**範例提示詞**：

```
請分析以下使用者測試反饋：

反饋 1: "建立訂單後沒有顯示成功訊息，不確定是否成功"
反饋 2: "當庫存不足時，錯誤訊息太技術性，看不懂"
反饋 3: "希望可以一次選擇多個商品加入購物車"
反饋 4: "訂單列表沒有篩選功能，找不到歷史訂單"

請生成：
1. 問題分類
   - 需求層面（缺失功能）
   - 規格層面（規格不清楚）
   - 原型層面（UI/UX 問題）

2. 每個問題的：
   - 問題描述
   - 問題類型
   - 影響範圍（哪些規格需要更新）
   - 優先級（High/Medium/Low + 理由）
   - 修正建議

3. 總結報告
   - 高優先級問題數量
   - 建議的修正順序
```

### 7.2 規格更新建議

#### 適合度：★★★★☆ (高)

```
給 AI 什麼：
- 反饋分析結果
- 需要修正的問題
- 原有的規格文件

要 AI 做什麼：
- 提出規格更新方案
- 生成更新後的規格片段
- 評估影響範圍

請 AI 生成什麼：
- 規格更新建議文件
- 包含：問題、建議方案、更新後的規格、影響範圍
```

**範例提示詞**：

```
請根據以下反饋提出規格更新建議：

問題：建立訂單後沒有顯示成功訊息

當前規格：
[YAML UI 規格片段]

請生成：
1. 問題分析
   - 當前規格的缺失
   - 使用者期望的行為

2. 更新方案
   - 方案 A: [描述]
   - 方案 B: [描述]
   - 推薦方案: [哪一個] + [理由]

3. 更新後的規格
   - 顯示需要修改的 YAML 片段
   - 使用 diff 格式標示變更

4. 影響範圍
   - 需要更新的規格檔案
   - 需要重新生成的程式碼
   - 需要更新的測試案例
```

---

## LLM 協助效益評估

### 各階段效益總結

| 階段 | LLM 適合度 | 主要協助內容 | 預估時間節省 | 人工監督需求 |
|------|-----------|-------------|------------|------------|
| **Phase 1: 業務探索** | ★★★☆☆ | 訪談大綱生成、記錄整理、Journey Map 初稿 | 30-40% | 高（需驗證業務正確性） |
| **Phase 2: 領域建模** | ★★★★★ | Event → Entity 轉換、DBML 生成、詞彙表生成 | 60-70% | 中（需驗證領域邏輯） |
| **Phase 3: 需求澄清** | ★★★★★ | 自動掃描、問題生成、邊界條件識別 | 70-80% | 低（主要檢查完整性） |
| **Phase 4: 規格制定** | ★★★★★ | BDD Feature、API 規格、UI 規格、可追溯矩陣 | 60-70% | 中（需驗證規格正確性） |
| **Phase 5: 驗證確認** | ★★★★★ | 完整性檢查、一致性驗證、涵蓋率分析 | 80-90% | 低（自動化檢查） |
| **Phase 6: 原型生成** | ★★★★★ | Mock API、UI 原型、測試案例、文件 | 70-80% | 中（需驗證可執行性） |
| **Phase 7: 迭代精煉** | ★★★★☆ | 反饋分析、問題分類、更新建議 | 50-60% | 高（需人工決策） |

### 整體效益分析

**時間節省**：
- 規格撰寫階段（Phase 3-4）：節省 60-70% 的時間
- 驗證檢查階段（Phase 5）：節省 80-90% 的時間
- 程式碼生成階段（Phase 6）：節省 70-80% 的時間
- **整體預估**：節省 50-60% 的需求分析與規格制定時間

**品質提升**：
- 規格完整性：自動掃描可識別 80-90% 的缺失
- 規格一致性：自動檢查可發現 90-95% 的不一致
- 測試涵蓋率：自動生成可涵蓋 70-80% 的邊界條件

**風險降低**：
- 減少人為遺漏：自動化檢查減少 70-80% 的遺漏錯誤
- 早期發現問題：Phase 3 的自動掃描可提前發現 80% 的規格問題
- 規格與程式碼一致：自動生成確保 95% 以上的一致性

---

## 注意事項與限制

### 1. LLM 的限制

```
❌ LLM 無法做到的事：
1. 理解隱含的業務邏輯（需要人工補充）
2. 做出業務決策（需要 PO/BA 判斷）
3. 評估方案的商業價值（需要業務專家）
4. 理解特定領域的深度知識（需要領域專家）
5. 完全自動化的規格生成（必須人工驗證）
```

### 2. 人工監督的重要性

**高監督需求的環節**：
- Phase 1: 業務探索（訪談詮釋、需求理解）
- Phase 7: 迭代精煉（反饋判斷、決策制定）

**中監督需求的環節**：
- Phase 2: 領域建模（領域邏輯驗證）
- Phase 4: 規格制定（規格正確性驗證）
- Phase 6: 原型生成（程式碼可執行性驗證）

**低監督需求的環節**：
- Phase 3: 需求澄清（自動掃描、問題生成）
- Phase 5: 驗證確認（自動化檢查）

### 3. 最佳實踐

**1. 迭代式協作**
```
不要：一次性讓 LLM 生成完整規格
要：分階段、小步驟地使用 LLM，每步驗證
```

**2. 提供充足上下文**
```
不要：只給 LLM 簡短的需求描述
要：提供完整的背景、相關規格、範例
```

**3. 明確的輸出格式**
```
不要：讓 LLM 自由發揮輸出格式
要：提供明確的格式範本與範例
```

**4. 持續驗證與修正**
```
不要：盲目相信 LLM 的輸出
要：每個輸出都經過人工審查與驗證
```

**5. 建立範例庫**
```
不要：每次都重新描述要求
要：建立高品質的提示詞與範例庫，重複使用
```

### 4. 團隊技能要求

**使用 LLM 協助需求分析的團隊需要**：
- 熟悉 BDD、DBML、TypeSpec 等規格語言
- 理解提示工程 (Prompt Engineering) 基礎
- 具備規格驗證與審查能力
- 了解 LLM 的能力邊界與限制

### 5. 工具整合建議

**建議的工具鏈**：
```
1. LLM 平台
   - Claude (Sonnet/Opus) - 長文本理解與生成
   - GPT-4 - 通用任務

2. 規格編輯
   - VS Code + 外掛（Gherkin、DBML、TypeSpec）

3. 自動化流程
   - 腳本化的 LLM 呼叫（使用 API）
   - Git Hooks 整合（自動檢查）
   - CI/CD 整合（自動驗證）

4. 版本控制
   - Git（追蹤提示詞與生成結果）
   - 標記 LLM 生成的內容（需人工驗證）
```

---

## 總結

### LLM 在需求發掘流程中的核心價值

1. **加速規格撰寫**：BDD、API、UI 規格的初稿生成
2. **提升規格品質**：自動化完整性與一致性檢查
3. **降低遺漏風險**：系統化掃描與邊界條件識別
4. **促進規格轉換**：Event → Entity、Feature → API 等轉換
5. **加速原型生成**：Mock API、測試案例、文件的自動生成

### 成功使用 LLM 的關鍵

1. **明確的輸入輸出**：清晰定義給 AI 什麼、要 AI 做什麼、生成什麼
2. **充足的上下文**：提供完整的背景、範例、格式要求
3. **持續的驗證**：每個輸出都需人工審查與修正
4. **迭代式協作**：小步驟前進，逐步完善
5. **建立知識庫**：累積高品質的提示詞與範例

### 未來展望

隨著 LLM 能力的提升，未來可能實現：
- 更高程度的自動化（80-90% 的規格自動生成）
- 多模態理解（從 UI 設計稿直接生成規格）
- 主動式需求探索（LLM 主動提問以完善需求）
- 即時驗證與修正（生成即驗證，自動修正錯誤）

但**人類的判斷與決策**仍是不可或缺的核心環節。

---

**版權聲明**：本文件屬於 WA-RAPTor 專案，採用 MIT 授權。
