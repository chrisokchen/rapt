# haPDL (High-level Abstract Page Description Language) 語法規格 v3.3

> **版本**: v3.3.0 (Release Candidate, 2026-05-13)
> **前版**: v3.2（見 `archive/haPDL-specification-v3.2.md`）
> **v3.3 重點**: (1) 跟隨 haARM v3.3 升版互鎖；(2) Convention 來源三層（`haPDL2PDL/src/defaults/*.yaml` + `haPDL/haPDL-page-type-defaults-v3.2.1.md` + `phase2-defaults.ts`/`phase3-sugar.ts`）；(3) 與 haARM `permission.id` / `role.id` 引用對齊
> **SSoT 主手冊**: `haPDLdoc.md`

## 版本沿革

| 版本 | 日期 | 重點變更 |
|------|------|----------|
| 1.0 | 2025-01 | 初始版本，基礎頁面描述 |
| 2.0 | 2025-03 | 新增 Master-Detail、Explorer 頁面類型 |
| 3.0 | 2025-12 | **重大升級**：從「頁面描述語言」進化為「互動行為描述語言」 |
| 3.1 | 2026-03-31 | **跨規格對齊**：新增 haAPI 綁定（`api:`、`actions.operations`）、DBML 標註整合（`label:`/`ref_code:`/`sensitive:`/`group:`）、`?` 符號消歧、Resolution Order 附錄、Scope Declaration |
| 3.2 | 2026-04-02 | **haAPI v3.2 對齊**：Scope Declaration 補充 `ext.*`/`proxy`/`integrations` 邊界、Resolution Order 新增 Resilience 屬性、版本引用更新 |
| 3.2.1 | 2026-04-07 | **Convention 強化**：新增 Page Type Defaults 機制（獨立檔案 `haPDL-page-type-defaults-v3.2.1.md`）、`keyword` 保留名稱、`testing` 完整定義章節、form actions 展開規則、accessibility Convention 推斷、validation/permissions SSOT 推斷規則 |

### v3.0 新增特性總覽

- 🔄 **狀態管理系統**：跨頁面狀態、元件連動、狀態持久化
- ⚠️ **錯誤處理框架**：分層錯誤策略、使用者反饋、離線支援
- ⚡ **非同步行為規範**：樂觀更新、Loading 狀態、請求控制
- ♿ **無障礙存取 (a11y)**：ARIA 標籤、鍵盤導覽、幕閱讀器支援
- 📝 **複雜表單支援**：動態區塊、可重複欄位、跨欄位驗證
- 📁 **完整檔案處理**：分塊上傳、預覽、處理管線
- 🔒 **安全性規格**：欄位遮罩、資料隔離、敏感操作保護
- 🧪 **測試性支援**：選擇器策略、Mock 資料、Gherkin 整合

### v3.1 對齊更新摘要

- 🔗 **haAPI 綁定**：頁面頂層新增 `api:` 欄位，`actions` 新增 `operations` 語法
- 📦 **Annotated DBML 整合**：文件化 `label:`/`ref_code:`/`sensitive:`/`group:` 推斷規則
- ❓ **`?` 符號消歧**：明確定義 filter/column/form 三種上下文語意
- 🔒 **sensitive 合併規則**：DBML `sensitive:` ∪ haPDL `*` = PDL masking
- 🧭 **Resolution Order 附錄**：正式定義多來源屬性查找優先順序
- 🏷️ **Scope Declaration**：明確劃定 haPDL 與 haAPI 的職責邊界

---

## 一、設計理念

haPDL 是一套高階抽象的頁面描述語言，專為已建立領域模型的團隊設計，讓使用者能夠以**宣告意圖**的方式定義頁面及其互動行為，而無需關注實作細節。

### 核心原則

1. **意圖優於實作** - 描述「要什麼」而非「怎麼做」
2. **慣例優於配置** - 利用合理的預設值減少配置
3. **漸進式細化** - 從簡單開始，需要時才增加複雜度
4. **領域驅動** - 基於 DBML 定義的領域模型自動推斷
5. **可讀性優先** - 語法接近自然語言，非技術人員也能理解
6. **行為完整性** ⭐ NEW - 不僅描述靜態結構，更完整描述動態互動
7. **跨規格對齊** ⭐ v3.1 - 與 haAPI、Annotated DBML 建立明確引用鏈路

### Scope Declaration（職責邊界）⭐ v3.1 · 更新 v3.2

haPDL 關注「使用者在頁面上能做什麼」（前端意圖）。後端的實作邏輯（haAPI 的 `sql_hint`、`logic` steps、`ext.*` 外部服務呼叫、`proxy` 轉發）屬於 haAPI → TypeSpec/CodeGen 管線，haPDL 不涉及。

```
haPDL → 知道「activate 按鈕會呼叫 activate 操作」
haAPI → 知道「activate 操作的實作是 UPDATE InfoUser SET userType='A'」
haAPI → 知道「reset_password 操作會呼叫 ext.smtp.send_email」       ← v3.2
haAPI → 知道「verify_captcha 是 proxy 到 ext.captcha.validate」      ← v3.2
PDL   → 知道「activate 按鈕的完整 UI 配置（icon、variant、確認對話框）」
```

haPDL 透過 `api:` 欄位引用 haAPI 定義名稱，透過 `actions.operations` 引用 haAPI 操作名稱，但不涉及其實作細節。

> haAPI v3.2 的 `ext.*` 命名空間、`proxy` 原語、`integrations` 宣告和 `resilience` 級聯機制皆屬於 haAPI → TypeSpec/CodeGen 管線的內部細節。haPDL 僅透過 `actions.operations` 引用操作名稱，**不區分該操作是 DB 操作、外部服務呼叫、還是 proxy 轉發**。haAPI 的 `integrations` 宣告（外部服務依賴）屬於 API/基礎設施層面，haPDL 不直接引用。外部服務呼叫的 UI 影響（loading 狀態、失敗處理）透過操作級的 `async_ui` 和 `error_handling` 間接處理。

### v3.0 設計哲學

```
┌─────────────────────────────────────────────────────────────┐
│                    haPDL 3.0 架構層次                        │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: 測試與品質     testing, accessibility, security   │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: 互動行為       state, async, error_handling       │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: 動作與流程     actions, hooks, workflows          │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: 頁面結構       page, view, layout                 │
├─────────────────────────────────────────────────────────────┤
│  Layer 0: 領域基礎       entity (DBML), relations           │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、適用情境

### 最適合場景
- ✅ 企業後台管理系統（大量 CRUD 頁面）
- ✅ 已完成領域建模（Event Storming + DBML）的專案
- ✅ 需要快速原型開發和迭代
- ✅ 跨職能團隊協作（PM、BA、開發者共同參與）
- ✅ 標準化的業務流程系統
- ✅ 需要完整無障礙支援的政府/公共服務系統 ⭐ NEW
- ✅ 需要離線能力的現場作業系統 ⭐ NEW

### 不適合場景
- ❌ 高度客製化的使用者介面
- ❌ 遊戲或創意互動應用
- ❌ 沒有明確領域模型的專案
- ❌ 需要複雜動畫或視覺效果的頁面

---

## 三、基礎語法規格

### 3.1 頁面基本結構

```yaml
# ===== 頁面識別 =====
page: <page-identifier>        # kebab-case 格式
type: <page-type>              # 頁面類型
title: <page-title>            # 顯示標題
entity: <EntityName>           # 主要實體（來自 DBML）
api: <haapi-name>              # haAPI 定義名稱（可選）⭐ v3.1

# ===== 擴展與版本 =====
extends: <template-name>       # 繼承模板（可選）
mixins: [<mixin-names>]        # 混入功能（可選）⭐ NEW
version: <version-number>      # 版本號（可選）
schema_version: "3.0"          # haPDL 規格版本 ⭐ NEW

# ===== 視圖定義 =====
view:
  <view-configurations>

# ===== 狀態管理 ===== ⭐ NEW
state:
  <state-configurations>

# ===== 動作定義 =====
actions:
  standard: [create, edit, delete]     # 標準 CRUD（對應 haAPI standard）
  operations: [<haapi-op-names>]       # 業務操作（引用 haAPI operations）⭐ v3.1
  custom:                              # 自訂動作
    - name: <action-name>
      operation: <haapi-op-name>       # 引用 haAPI operation ⭐ v3.1
      params: {...}                    # 額外參數

# ===== 錯誤處理 ===== ⭐ NEW
error_handling:
  <error-configurations>

# ===== 非同步行為 ===== ⭐ NEW
async:
  <async-configurations>

# ===== 無障礙存取 ===== ⭐ NEW
accessibility:
  <a11y-configurations>

# ===== 安全性 ===== ⭐ NEW
security:
  <security-configurations>

# ===== 測試性 ===== ⭐ NEW
testing:
  <testing-configurations>

# ===== 進階配置 =====
advanced:
  <advanced-settings>
```

> **Defaults vs extends/mixins** ⭐ v3.2.1
> **Page Type Defaults**（規格規節：`haPDL-page-type-defaults-v3.2.1.md`）是轉換器內建的慣例預設値，**無需宣告**。
> `extends` 用於跨頁面的自訂模板繼承（未來擴充）。
> `mixins` 用於可重用的功能片段混入（未來擴充）。

### actions.standard 在 form 頁面的展開規則 ⭐ v3.2.1

form 頁面的 `standard: [create]` 或 `standard: [update]` 由 Convention 自動展開為三個按鈕：

| standard 値 | 展開按鈕 | type | variant | label 模板 |
|------------|---------|------|---------|-----------|
| `create` | save | submit | primary | "新增儲存" |
| | reset | reset | secondary | "清除重填" |
| | cancel | navigate | — | "返回" |
| `update` | save | submit | primary | "儲存" |
| | reset | reset | secondary | "還原" |
| | cancel | navigate | — | "返回" |

- `cancel.route` 由 Convention 從 entity 推斷：`/{entity-kebab}/list`
- `variant` 屬於 PDL 層，haPDL 中無需指定
- 如需覆寫個別按鈕，使用 `actions.custom` 區塊

### 3.2 頁面類型 (type)

```yaml
# 基礎類型（最常用）
type: list          # 列表頁 - 顯示多筆資料
type: form          # 表單頁 - 新增/編輯資料
type: detail        # 詳情頁 - 檢視單筆資料
type: master-detail # 主從頁 - 主記錄 + 明細列表
type: explorer      # 樹狀導覽頁 - 階層樹 + 內容面板

# 進階類型
type: dashboard     # 儀表板 - 統計圖表
type: wizard        # 精靈頁 - 多步驟流程
type: search        # 搜尋頁 - 進階搜尋
type: report        # 報表頁 - 資料分析
type: hybrid        # 混合頁 - 組合多種功能
type: kanban        # 看板頁 - 拖放式狀態管理 ⭐ NEW
type: calendar      # 日曆頁 - 時間軸檢視 ⭐ NEW
```

### 3.3 簡潔欄位語法

```yaml
view:
  # ===== 篩選欄位符號 =====
  filters:
    - fieldName         # 基本篩選
    - fieldName~        # 模糊搜尋 (contains)
    - fieldName=        # 精確匹配 (equals)
    - fieldName>        # 範圍篩選 (greater than)
    - fieldName<        # 範圍篩選 (less than)
    - fieldName><       # 區間篩選 (between) ⭐ NEW
    - fieldName[]       # 多選篩選 (in)
    - fieldName@        # 特殊格式 (email/url)
    - fieldName?        # 可空值篩選 (nullable) ⭐ NEW

  > **`keyword` 保留名稱** ⭐ v3.2.1
  > `keyword` 是保留的虛擬 filter 名稱，代表「全文搜尋框」。
  > 它不對應 entity 的實體欄位，而是透過 `api:` 綁定查找 haAPI 的
  > `search.fields` 來取得搜尋目標欄位。
  > 若未綁定 haAPI 或 haAPI 未定義 `search.fields`，
  > Convention 預設搜尋 entity 中所有 text 類型欄位。
  > `keyword~` 用於模糊搜尋（最常用），`keyword=` 用於精確匹配。

  > **`?` 符號語意消歧** ⭐ v3.1
  > `?` 的意義取決於所在區塊：
  > - `view.filters` 中：**可空值篩選**，展開為 `nullable: true` + `null_label`
  > - `view.columns` 中：**可藏欄位**，展開為 `hideable: true`
  > - `form.fields` 中：**選填欄位**，展開為 `required: false`
    
  # ===== 顯示欄位符號 =====
  columns:
    - fieldName         # 基本顯示
    - fieldName!        # 重要欄位（粗體/強調）
    - fieldName?        # 選擇性顯示（可隱藏）
    - fieldName:type    # 指定顯示類型
    - fieldName|format  # 指定格式化方式
    - fieldName^        # 可排序欄位 ⭐ NEW
    - fieldName&        # 可群組欄位 ⭐ NEW
    
  # ===== 表單欄位符號 =====
  fields:
    - fieldName         # 基本輸入
    - fieldName!        # 必填欄位
    - fieldName?        # 選填欄位
    - fieldName#        # 唯讀欄位
    - fieldName*        # 密碼/敏感資料

  > **sensitive 合併規則** ⭐ v3.1
  > 敏感欄位判定 = DBML `sensitive: true` ∪ haPDL `fieldName*` 符號。
  > 即使 haPDL 中未使用 `*` 符號，若 DBML 對應欄位有 `sensitive: true`，
  > 轉換器仍應在 PDL 輸出中自動啟用 `security.field_level.masking`。
  > haPDL `*` 符號是「覆寫」機制，用於 DBML 未標記但頁面需要遮罩的情況。

    - fieldName@        # Email 格式
    - fieldName[]       # 多選欄位
    - fieldName{}       # JSON/物件欄位
    - fieldName~        # 連動欄位來源 ⭐ NEW
    - fieldName<~       # 連動欄位目標 ⭐ NEW
```

### 3.4 顯示類型 (:type)

```yaml
columns:
  # 基礎類型
  - status:badge       # 徽章顯示
  - avatar:image       # 圖片顯示
  - price:currency     # 貨幣格式
  - progress:bar       # 進度條
  - rating:stars       # 星級評分
  - active:toggle      # 開關狀態
  - tags:chips         # 標籤群組
  - description:truncate(100)  # 截斷文字
  
  # 進階類型 ⭐ NEW
  - location:map       # 地圖座標
  - color:swatch       # 色彩選擇器
  - file:attachment    # 檔案附件
  - user:avatar-name   # 使用者頭像+名稱
  - diff:change-track  # 變更追蹤
  - json:tree          # JSON 樹狀檢視
  - markdown:rendered  # Markdown 渲染
  - code:highlight     # 程式碼高亮
```

### 3.5 格式化 (|format)

```yaml
columns:
  # 日期時間格式
  - created_at|date           # 日期格式 (YYYY-MM-DD)
  - updated_at|datetime       # 日期時間格式
  - scheduled|time            # 時間格式 (HH:mm)
  - deadline|relative         # 相對時間 (3 天後) ⭐ NEW
  - duration|humanize         # 人性化時間 (2 小時前)
  
  # 數值格式
  - amount|number(2)          # 數字格式（2位小數）
  - percentage|percent        # 百分比格式
  - fileSize|bytes            # 檔案大小格式
  - count|compact             # 緊湊數字 (1.2K) ⭐ NEW
  - price|currency(TWD)       # 指定幣別 ⭐ NEW
  
  # 文字格式 ⭐ NEW
  - name|uppercase            # 大寫
  - code|lowercase            # 小寫
  - title|capitalize          # 首字大寫
  - phone|mask(###-###-####)  # 遮罩格式
```

---

## 四、狀態管理系統 ⭐ NEW

### 4.1 狀態管理概觀

```yaml
state:
  # ===== 頁面內部狀態 =====
  local:
    <local-state-definitions>
  
  # ===== 跨頁面共享狀態 =====
  shared:
    <shared-state-definitions>
  
  # ===== 欄位連動 =====
  cascading:
    <cascading-definitions>
  
  # ===== 狀態持久化 =====
  persistence:
    <persistence-definitions>
  
  # ===== 計算屬性 =====
  computed:
    <computed-definitions>
  
  # ===== 狀態監聽 =====
  watchers:
    <watcher-definitions>
```

### 4.2 頁面內部狀態

```yaml
state:
  local:
    # 簡單狀態
    - name: isEditing
      type: boolean
      default: false
    
    # 帶驗證的狀態
    - name: selectedItems
      type: array<string>
      default: []
      max_length: 100
    
    # 複雜物件狀態
    - name: filterCriteria
      type: object
      schema:
        keyword: string
        status: enum[active, inactive, all]
        dateRange: DateRange
      default:
        status: all
    
    # 衍生狀態（從其他狀態計算）
    - name: hasSelection
      derived: "selectedItems.length > 0"
    
    # UI 狀態
    - name: expandedRows
      type: set<string>
      scope: ui  # 不影響資料層
```

### 4.3 跨頁面共享狀態

```yaml
state:
  shared:
    # 會話級共享（關閉瀏覽器即消失）
    - name: currentWorkspace
      type: Workspace
      scope: session
      description: "當前工作區，跨頁面共享"
    
    # 使用者級共享（持久化到 localStorage）
    - name: userPreferences
      type: UserPreferences
      scope: user
      sync: true  # 跨分頁同步
    
    # 流程級共享（特定工作流程內共享）
    - name: orderDraft
      type: Order
      scope: workflow
      workflow_id: create-order
      ttl: 3600  # 1小時後過期
    
    # 全域狀態（整個應用共享）
    - name: notifications
      type: array<Notification>
      scope: global
      max_length: 50
```

### 4.4 欄位連動（Cascading）

```yaml
state:
  cascading:
    # 基本連動：選擇縣市 → 載入區域
    - trigger: city
      target: district
      source: "api:/regions?city_id={city.id}"
      loading_text: "載入區域中..."
      error_text: "無法載入區域資料"
      clear_on_change: true  # 上層變更時清空
    
    # 多層連動：類別 → 子類別 → 品項
    - trigger: category
      targets:
        - field: subcategory
          source: "api:/subcategories?parent={category.id}"
          clear_on_change: true
        - field: product
          source: "api:/products?subcategory={subcategory.id}"
          depends_on: subcategory  # 等待 subcategory 載入完成
          clear_on_change: true
    
    # 條件連動
    - trigger: customer_type
      target: tax_id
      conditions:
        - when: "customer_type == 'business'"
          required: true
          visible: true
        - when: "customer_type == 'individual'"
          required: false
          visible: false
    
    # 計算連動：數量 × 單價 = 小計
    - triggers: [quantity, unit_price]
      target: subtotal
      compute: "quantity * unit_price"
      immediate: true  # 立即計算，不等待 blur
    
    # 驗證連動：結束日期必須晚於開始日期
    - trigger: start_date
      target: end_date
      validation:
        rule: "end_date > start_date"
        message: "結束日期必須晚於開始日期"
```

### 4.5 狀態持久化

```yaml
state:
  persistence:
    # 篩選條件持久化
    filters:
      storage: sessionStorage
      key: "{page}-filters"
      include: [status, dateRange, keyword]
      exclude: [temporaryFlag]
      ttl: 86400  # 24小時
    
    # 分頁設定持久化
    pagination:
      storage: localStorage
      key: "user-pagination-prefs"
      
    # 排序設定持久化
    sorting:
      storage: sessionStorage
      
    # 展開狀態持久化
    expanded:
      storage: sessionStorage
      key: "{page}-expanded"
    
    # 自訂持久化
    custom:
      - state: selectedView
        storage: localStorage
        encrypt: false
      - state: draftData
        storage: indexedDB
        encrypt: true
        compress: true
```

### 4.6 計算屬性

```yaml
state:
  computed:
    # 簡單計算
    - name: totalAmount
      expression: "items.reduce((sum, item) => sum + item.subtotal, 0)"
      dependencies: [items]
    
    # 帶格式化的計算
    - name: formattedTotal
      expression: "formatCurrency(totalAmount, 'TWD')"
      dependencies: [totalAmount]
    
    # 條件計算
    - name: discountedTotal
      expression: |
        if (coupon && coupon.type === 'percentage') {
          return totalAmount * (1 - coupon.value / 100);
        } else if (coupon && coupon.type === 'fixed') {
          return Math.max(0, totalAmount - coupon.value);
        }
        return totalAmount;
      dependencies: [totalAmount, coupon]
    
    # 非同步計算
    - name: shippingFee
      async: true
      expression: "api:/shipping/calculate?total={totalAmount}&zip={zipCode}"
      dependencies: [totalAmount, zipCode]
      debounce: 500
      cache: true
```

### 4.7 狀態監聽器

```yaml
state:
  watchers:
    # 基本監聽
    - watch: status
      handler: onStatusChange
      immediate: false
    
    # 深度監聽
    - watch: formData
      handler: onFormDataChange
      deep: true
      
    # 多狀態監聽
    - watch: [quantity, unitPrice]
      handler: recalculateSubtotal
    
    # 帶條件的監聽
    - watch: selectedItems
      handler: updateBatchActions
      condition: "selectedItems.length > 0"
    
    # 防抖監聽
    - watch: searchKeyword
      handler: performSearch
      debounce: 300
    
    # 節流監聯
    - watch: scrollPosition
      handler: loadMoreItems
      throttle: 100
```

---

## 五、錯誤處理框架 ⭐ NEW

### 5.1 錯誤處理概觀

```yaml
error_handling:
  # ===== 驗證錯誤 =====
  validation:
    <validation-error-config>
  
  # ===== API 錯誤 =====
  api:
    <api-error-config>
  
  # ===== 網路錯誤 =====
  network:
    <network-error-config>
  
  # ===== 業務錯誤 =====
  business:
    <business-error-config>
  
  # ===== 全域錯誤邊界 =====
  boundary:
    <error-boundary-config>
```

### 5.2 驗證錯誤處理

```yaml
error_handling:
  validation:
    # 顯示策略
    display:
      mode: inline          # inline | summary | toast | modal
      position: below       # above | below | right
      scroll_to_first: true
      highlight_field: true
      highlight_style: border  # border | background | icon
    
    # 驗證時機
    timing:
      on_blur: true         # 離開欄位時驗證
      on_change: false      # 輸入時即時驗證（預設關閉避免干擾）
      on_submit: true       # 送出時驗證
      debounce: 300         # 防抖延遲（毫秒）
    
    # 錯誤訊息
    messages:
      required: "{field} 為必填欄位"
      email: "請輸入有效的電子郵件地址"
      min: "{field} 不得小於 {min}"
      max: "{field} 不得大於 {max}"
      minLength: "{field} 至少需要 {minLength} 個字元"
      maxLength: "{field} 不得超過 {maxLength} 個字元"
      pattern: "{field} 格式不正確"
      unique: "{field} 已存在，請使用其他值"
      custom: "{message}"
    
    # 錯誤摘要
    summary:
      enabled: true
      position: top         # top | bottom
      title: "請修正以下錯誤："
      max_display: 5        # 最多顯示幾個錯誤
      show_count: true      # 顯示總錯誤數
```

### 5.3 API 錯誤處理

```yaml
error_handling:
  api:
    # HTTP 狀態碼對應處理
    status_handlers:
      400:
        type: validation
        action: map_to_fields    # 將錯誤對應到表單欄位
        fallback_message: "請求資料格式錯誤"
        
      401:
        type: authentication
        action: redirect
        target: "/login"
        message: "登入已過期，請重新登入"
        preserve_return_url: true
        
      403:
        type: authorization
        action: display
        display_mode: modal
        message: "您沒有權限執行此操作"
        show_request_access: true  # 顯示申請權限按鈕
        
      404:
        type: not_found
        action: display
        display_mode: inline
        message: "找不到請求的資源"
        show_back_button: true
        
      409:
        type: conflict
        action: display
        display_mode: modal
        message: "資料已被其他人修改，請重新載入"
        actions:
          - label: "重新載入"
            action: reload
          - label: "保留我的變更"
            action: force_save
            
      422:
        type: validation
        action: map_to_fields
        field_mapping:
          source: "errors"        # API 回應中的錯誤欄位路徑
          field_key: "field"
          message_key: "message"
        
      429:
        type: rate_limit
        action: display
        display_mode: toast
        message: "請求過於頻繁，請稍後再試"
        retry_after: true         # 顯示重試倒數
        
      500:
        type: server_error
        action: display
        display_mode: modal
        message: "伺服器發生錯誤，請稍後再試"
        show_error_id: true       # 顯示錯誤 ID 供回報
        actions:
          - label: "重試"
            action: retry
          - label: "回報問題"
            action: report
            
      502:
        type: gateway_error
        action: display
        display_mode: toast
        message: "服務暫時無法使用"
        auto_retry: true
        retry_delay: 5000
        
      503:
        type: maintenance
        action: display
        display_mode: fullscreen
        message: "系統維護中，請稍後再試"
        show_status_page: true
    
    # 錯誤回報
    reporting:
      enabled: true
      endpoint: "/api/error-reports"
      include:
        - error_id
        - timestamp
        - user_id
        - page_url
        - action
        - request_payload
        - response_body
      exclude:
        - password
        - token
        - credit_card
```

### 5.4 網路錯誤處理

```yaml
error_handling:
  network:
    # 連線逾時
    timeout:
      duration: 30000           # 30 秒
      message: "連線逾時，請檢查網路狀態"
      action: retry_prompt
    
    # 重試策略
    retry:
      enabled: true
      max_attempts: 3
      strategy: exponential     # linear | exponential | fibonacci
      base_delay: 1000          # 基礎延遲（毫秒）
      max_delay: 30000          # 最大延遲
      jitter: true              # 加入隨機抖動避免同時重試
      retryable_methods: [GET, PUT, DELETE]  # 可重試的 HTTP 方法
      retryable_status: [408, 429, 500, 502, 503, 504]
    
    # 離線處理
    offline:
      detection:
        method: navigator       # navigator | heartbeat | both
        heartbeat_url: "/api/health"
        heartbeat_interval: 30000
      
      mode: queue              # queue | cache | reject
      
      # 離線時的 UI 提示
      indicator:
        enabled: true
        position: top
        message: "目前處於離線狀態"
        show_queue_count: true
      
      # 離線佇列
      queue:
        storage: indexedDB
        max_size: 100
        max_age: 86400         # 24小時後過期
        priority_field: priority
        dedup: true            # 去重複
        
      # 離線快取
      cache:
        enabled: true
        strategy: stale-while-revalidate
        ttl: 3600
        max_size: 50MB
      
      # 上線恢復
      recovery:
        auto_sync: true
        sync_order: fifo       # fifo | lifo | priority
        conflict_resolution: server_wins  # server_wins | client_wins | manual
        notify_on_complete: true
```

### 5.5 業務錯誤處理

```yaml
error_handling:
  business:
    # 預定義業務錯誤
    errors:
      INSUFFICIENT_STOCK:
        message: "庫存不足，目前剩餘 {available} 件"
        display: inline
        field: quantity
        severity: warning
        actions:
          - label: "調整數量"
            action: set_max_available
          
      DUPLICATE_ORDER:
        message: "偵測到重複訂單，是否繼續？"
        display: modal
        severity: warning
        actions:
          - label: "檢視既有訂單"
            action: navigate
            target: "/orders/{existing_order_id}"
          - label: "仍要建立"
            action: continue
            confirm: true
            
      CREDIT_LIMIT_EXCEEDED:
        message: "已超過信用額度，請聯繫業務人員"
        display: modal
        severity: error
        blocking: true
        actions:
          - label: "聯繫業務"
            action: contact
            channel: email
          - label: "申請提高額度"
            action: navigate
            target: "/credit-request"
            
      PENDING_APPROVAL:
        message: "此操作需要主管核准"
        display: toast
        severity: info
        auto_action:
          type: submit_for_approval
          notify: [manager]
    
    # 錯誤嚴重程度對應的顯示樣式
    severity_styles:
      info:
        icon: info-circle
        color: blue
        duration: 3000
      warning:
        icon: alert-triangle
        color: orange
        duration: 5000
      error:
        icon: x-circle
        color: red
        duration: null        # 不自動消失
      critical:
        icon: alert-octagon
        color: red
        blocking: true        # 阻擋後續操作
```

### 5.6 錯誤邊界

```yaml
error_handling:
  boundary:
    # 頁面級錯誤邊界
    page:
      enabled: true
      fallback:
        type: error_page
        title: "頁面載入失敗"
        message: "很抱歉，頁面發生錯誤"
        actions:
          - label: "重新載入"
            action: reload
          - label: "返回首頁"
            action: navigate
            target: "/"
      
      # 錯誤追蹤
      tracking:
        enabled: true
        service: sentry        # sentry | datadog | custom
        sample_rate: 1.0
        
    # 區塊級錯誤邊界
    section:
      enabled: true
      fallback:
        type: inline_error
        message: "此區塊載入失敗"
        show_retry: true
      
    # 元件級錯誤邊界
    component:
      enabled: true
      fallback:
        type: placeholder
        show_error_icon: true
```

---

## 六、非同步行為規範 ⭐ NEW

### 6.1 非同步行為概觀

```yaml
async:
  # ===== 資料獲取 =====
  fetching:
    <fetching-config>
  
  # ===== 資料變更 =====
  mutations:
    <mutations-config>
  
  # ===== Loading 狀態 =====
  loading:
    <loading-config>
  
  # ===== 請求控制 =====
  request_control:
    <request-control-config>
  
  # ===== 快取策略 =====
  caching:
    <caching-config>
```

### 6.2 資料獲取

```yaml
async:
  fetching:
    # 預設策略
    default:
      strategy: cache-first    # cache-first | network-first | stale-while-revalidate
      stale_time: 30000        # 30 秒內視為新鮮
      cache_time: 300000       # 5 分鐘後從快取移除
      
    # 頁面載入
    on_mount:
      parallel: true           # 平行載入多個資源
      timeout: 10000
      retry: 2
      
    # 背景更新
    background_refresh:
      enabled: true
      interval: 60000          # 每分鐘
      when_visible: true       # 僅在頁面可見時
      when_focused: true       # 僅在視窗聚焦時
      
    # 相依資料載入
    dependencies:
      # 先載入 A，再用 A 的結果載入 B
      - name: orderDetails
        depends_on: orderId
        fetch_on: orderId_change
        
    # 預載入
    prefetch:
      enabled: true
      triggers:
        - on: hover_link
          delay: 200
        - on: near_viewport
          threshold: 200px
```

### 6.3 資料變更（Mutations）

```yaml
async:
  mutations:
    # 樂觀更新
    optimistic:
      enabled: true
      
      # 樂觀更新設定
      rules:
        - action: toggle_status
          optimistic: true
          rollback_on_error: true
          rollback_delay: 0
          
        - action: update_quantity
          optimistic: true
          transform: |
            (current, payload) => ({
              ...current,
              quantity: payload.quantity,
              subtotal: payload.quantity * current.unitPrice
            })
          
        - action: delete
          optimistic: true
          undo:
            enabled: true
            duration: 5000
            message: "已刪除 {name}"
            action_label: "復原"
    
    # 變更佇列
    queue:
      enabled: true
      strategy: sequential     # sequential | parallel | debounce
      debounce_delay: 1000
      batch:
        enabled: true
        max_size: 10
        max_wait: 2000
    
    # 衝突處理
    conflict:
      detection: version       # version | timestamp | hash
      version_field: _version
      resolution:
        mode: prompt           # prompt | server_wins | client_wins | merge
        merge_strategy: field_level
```

### 6.3.1 表單提交（Submit）⭐ v3.2.1

form 頁面專用的提交行為配置。`endpoint` 和 `method` 由 `actions.operations`
+ haAPI 綁定自動推斷，此處將定義 UX 行為。

```yaml
async:
  submit:
    loading:
      indicator: button_spinner | overlay | none   # 預設: button_spinner
      disable_form: true | false                   # 預設: true
    on_success:
      message: "模板字串"            # 預設: "{operation}{title}成功"
      redirect: "/path"             # 預設: Convention 推斷 /{entity-kebab}/list
      action: redirect | stay | close_modal   # 預設: redirect
    on_error:
      message: "模板字串"            # 預設: "{operation}{title}失敗: {error}"
```

> **注意**：不得在 `async.submit` 中硬編碼 `endpoint` 或 `method`。
> 這些由 `actions.operations` + `api:` haAPI 綁定自動解析。
> `async.submit` 的預設値從 `form_defaults` 給入，天游大多數 form 頁面可完全匆略此區塊。

### 6.4 Loading 狀態

```yaml
async:
  loading:
    # 全域 Loading
    global:
      enabled: true
      delay: 200              # 延遲顯示，避免閃爍
      minimum: 500            # 最少顯示時間，避免閃爍
      
    # 按區域的 Loading
    zones:
      page:
        type: skeleton
        count: 5              # Skeleton 數量
        
      table:
        type: skeleton
        rows: 10
        
      form:
        type: overlay
        opacity: 0.5
        spinner: true
        
      button:
        type: spinner
        disable: true
        text: "處理中..."
        
      inline:
        type: spinner
        size: small
    
    # Loading 指示器樣式
    indicators:
      spinner:
        type: circular        # circular | linear | dots
        size: medium
        color: primary
        
      skeleton:
        animation: wave       # wave | pulse | none
        color: "#e0e0e0"
        highlight: "#f5f5f5"
        
      progress:
        type: linear
        indeterminate: true
        color: primary
        
      overlay:
        background: "rgba(255, 255, 255, 0.8)"
        blur: 2px
```

### 6.5 請求控制

```yaml
async:
  request_control:
    # 防抖（Debounce）
    debounce:
      search: 300
      filter: 500
      auto_save: 2000
      
    # 節流（Throttle）
    throttle:
      scroll: 100
      resize: 200
      mousemove: 50
      
    # 取消策略
    cancellation:
      on_unmount: true        # 頁面離開時取消
      on_navigation: true     # 導航時取消
      on_new_request: true    # 新請求時取消舊請求
      
    # 並發控制
    concurrency:
      max_parallel: 6         # 最大並行請求數
      queue_overflow: wait    # wait | reject | drop_oldest
      
    # 請求去重
    deduplication:
      enabled: true
      window: 1000            # 1秒內相同請求視為重複
      key_generator: default  # 預設使用 URL + 參數
```

### 6.6 快取策略

```yaml
async:
  caching:
    # 快取層級
    layers:
      - type: memory
        max_size: 100
        ttl: 60000
        
      - type: sessionStorage
        max_size: 5MB
        ttl: 3600000
        
      - type: indexedDB
        max_size: 50MB
        ttl: 86400000
    
    # 快取規則
    rules:
      # 列表資料
      - pattern: "/api/*/list"
        strategy: stale-while-revalidate
        stale_time: 30000
        
      # 單筆資料
      - pattern: "/api/*/:id"
        strategy: cache-first
        ttl: 60000
        
      # 下拉選項
      - pattern: "/api/options/*"
        strategy: cache-first
        ttl: 3600000
        
      # 使用者資料
      - pattern: "/api/users/me"
        strategy: network-first
        ttl: 0
    
    # 快取失效
    invalidation:
      # 手動失效
      manual:
        - trigger: "mutation:create"
          invalidate: ["list", "count"]
        - trigger: "mutation:update"
          invalidate: ["detail:{id}", "list"]
        - trigger: "mutation:delete"
          invalidate: ["list", "count"]
      
      # 自動失效
      auto:
        on_focus: false       # 視窗聚焦時
        on_reconnect: true    # 網路恢復時
        interval: null        # 定時失效

---

## 七、無障礙存取規範 (Accessibility) ⭐ NEW

### 7.1 無障礙概觀

```yaml
accessibility:
  # ===== 語意標籤 =====
  semantics:
    <semantics-config>
  
  # ===== ARIA 標籤 =====
  aria:
    <aria-config>
  
  # ===== 鍵盤導覽 =====
  keyboard:
    <keyboard-config>
  
  # ===== 螢幕閱讀器 =====
  screen_reader:
    <screen-reader-config>
  
  # ===== 視覺輔助 =====
  visual:
    <visual-config>
  
  # ===== 合規等級 =====
  compliance:
    <compliance-config>
```

### 7.2 語意標籤

```yaml
accessibility:
  semantics:
    # 頁面結構
    page:
      main_landmark: true       # <main> 標籤
      navigation_landmark: true # <nav> 標籤
      search_landmark: true     # search role
      
    # 標題層級
    headings:
      page_title: h1
      section_title: h2
      subsection_title: h3
      auto_increment: true      # 自動遞增標題層級
      
    # 表格語意
    table:
      caption: true             # 表格標題
      scope: true               # th scope 屬性
      summary: false            # 已棄用，使用 caption
      
    # 表單語意
    form:
      fieldset_grouping: true   # 使用 fieldset 群組
      legend: true              # fieldset legend
      label_association: true   # label for 關聯
```

### 7.3 ARIA 標籤

```yaml
accessibility:
  aria:
    # 自動生成的 ARIA 標籤
    auto_labels:
      enabled: true
      
      # 區域標籤
      regions:
        table: "資料列表"
        filters: "篩選條件"
        pagination: "分頁導覽"
        form: "資料表單"
        actions: "操作按鈕"
        
      # 狀態標籤
      states:
        loading: "載入中"
        empty: "無資料"
        error: "發生錯誤"
        
    # 自訂 ARIA 標籤
    custom:
      - selector: ".data-table"
        aria-label: "{title}，共 {count} 筆資料"
        
      - selector: ".filter-panel"
        aria-label: "篩選 {entity} 資料"
        
      - selector: ".action-button"
        aria-describedby: "action-help"
    
    # 動態 ARIA 更新
    live_regions:
      - id: notification-area
        aria-live: polite
        aria-atomic: true
        
      - id: error-summary
        aria-live: assertive
        aria-atomic: true
        
      - id: row-count
        aria-live: polite
        aria-atomic: false
```

### 7.4 鍵盤導覽

```yaml
accessibility:
  keyboard:
    # 啟用鍵盤導覽
    enabled: true
    
    # 焦點管理
    focus:
      visible: true             # 顯示焦點指示器
      trap_in_modal: true       # Modal 內焦點陷阱
      restore_on_close: true    # 關閉 Modal 後恢復焦點
      skip_links: true          # 跳轉連結
      
    # 焦點指示器樣式
    focus_indicator:
      style: outline            # outline | ring | background
      color: "#005fcc"
      width: 2px
      offset: 2px
      
    # 標準快捷鍵
    shortcuts:
      # 全域快捷鍵
      global:
        - key: "/"
          action: focus_search
          description: "聚焦搜尋框"
          
        - key: "?"
          action: show_shortcuts
          description: "顯示快捷鍵說明"
          
        - key: "Escape"
          action: close_modal
          description: "關閉對話框"
          
      # 列表頁快捷鍵
      list:
        - key: "ctrl+n"
          action: create
          description: "新增資料"
          
        - key: "ctrl+f"
          action: focus_filter
          description: "聚焦篩選"
          
        - key: "ctrl+e"
          action: export
          description: "匯出資料"
          
        - key: "j"
          action: next_row
          description: "下一列"
          
        - key: "k"
          action: prev_row
          description: "上一列"
          
        - key: "Enter"
          action: view_selected
          description: "檢視選取項目"
          
        - key: "Delete"
          action: delete_selected
          description: "刪除選取項目"
          require_selection: true
          
      # 表單頁快捷鍵
      form:
        - key: "ctrl+s"
          action: save
          description: "儲存"
          
        - key: "ctrl+Enter"
          action: submit
          description: "送出表單"
          
        - key: "Escape"
          action: cancel
          description: "取消"
          
      # 表格內導覽
      table_navigation:
        enabled: true
        arrow_keys: true        # 方向鍵導覽
        home_end: true          # Home/End 跳至首尾
        page_up_down: true      # PageUp/Down 翻頁
    
    # 快捷鍵提示
    hints:
      enabled: true
      show_on: "hold_alt"       # 按住 Alt 顯示提示
      position: tooltip
```

### 7.5 螢幕閱讀器支援

```yaml
accessibility:
  screen_reader:
    # 公告設定
    announcements:
      # 資料載入公告
      data_loaded: "已載入 {count} 筆 {entity} 資料"
      data_loading: "正在載入資料"
      data_empty: "沒有符合條件的資料"
      
      # 操作完成公告
      action_complete: "{action} 成功"
      action_failed: "{action} 失敗：{error}"
      
      # 篩選公告
      filter_applied: "已套用篩選，顯示 {count} 筆資料"
      filter_cleared: "已清除所有篩選"
      
      # 選取公告
      item_selected: "已選取 {name}"
      item_deselected: "已取消選取 {name}"
      selection_count: "已選取 {count} 項"
      
      # 排序公告
      sorted: "已依 {field} {direction}排序"
      
      # 分頁公告
      page_changed: "第 {page} 頁，共 {total} 頁"
      
      # 表單公告
      validation_error: "表單驗證失敗，{count} 個錯誤"
      field_error: "{field} {error}"
      
    # 公告優先級
    priority:
      error: assertive
      success: polite
      info: polite
      
    # 公告時機
    timing:
      delay: 100              # 避免過於頻繁
      debounce: 500           # 合併快速連續的公告
```

### 7.6 視覺輔助

```yaml
accessibility:
  visual:
    # 高對比模式
    high_contrast:
      enabled: true
      auto_detect: true       # 自動偵測系統設定
      toggle_shortcut: "ctrl+alt+h"
      
    # 文字縮放
    text_scaling:
      enabled: true
      min_scale: 1.0
      max_scale: 2.0
      respect_browser: true   # 尊重瀏覽器縮放設定
      
    # 減少動態效果
    reduced_motion:
      enabled: true
      auto_detect: true       # 自動偵測 prefers-reduced-motion
      toggle_shortcut: "ctrl+alt+m"
      
    # 色彩輔助
    color:
      # 不僅依賴顏色傳達資訊
      non_color_indicators: true
      # 色盲友善
      colorblind_friendly: true
      # 對比度
      contrast_ratio:
        text: 4.5             # WCAG AA
        large_text: 3.0
        ui_components: 3.0
        
    # 錯誤指示
    error_indicators:
      icon: true              # 圖示指示
      border: true            # 邊框指示
      text: true              # 文字說明
      color_only: false       # 不僅用顏色
```

### 7.7 合規等級

```yaml
accessibility:
  compliance:
    # 目標合規等級
    level: AA                 # A | AA | AAA
    standard: WCAG21          # WCAG20 | WCAG21 | WCAG22
    
    # 額外合規要求
    additional:
      - Section508            # 美國 508 條款
      - EN301549              # 歐盟無障礙標準
      
    # 驗證設定
    validation:
      enabled: true
      on_build: true          # 建置時驗證
      fail_on_error: true     # 有錯誤時中斷建置
      
    # 排除項目（需說明原因）
    exclusions:
      - selector: ".legacy-widget"
        reason: "第三方元件，待替換"
        ticket: "A11Y-123"

---

> **accessibility 預設推斷** ⭐ v3.2.1
>
> `accessibility.aria` 的 label 可由 `title` + `type` 自動推斷：
>
> | type | page_label | 第二 label |
> |------|-----------|-----------|
> | list | "{title}列表" | table_label: "{title}資料列表" |
> | form | "{title}表單" | form_label: "{title}資料填寫" |
> | detail | "{title}詳情" | content_label: "{title}資料內容" |
>
> `keyboard.enabled` 預設為 `true`。僅在 label 不符合模板時才需明確配置。

## 八、安全性規格 ⭐ NEW

### 8.1 安全性概觀

```yaml
security:
  # ===== 欄位級安全 =====
  field_level:
    <field-security-config>
  
  # ===== 資料隔離 =====
  data_isolation:
    <data-isolation-config>
  
  # ===== 敏感操作保護 =====
  sensitive_operations:
    <sensitive-ops-config>
  
  # ===== 輸入防護 =====
  input_protection:
    <input-protection-config>
  
  # ===== 稽核日誌 =====
  audit:
    <audit-config>
```

### 8.2 欄位級安全

```yaml
security:
  field_level:
    # 欄位遮罩
    masking:
      - field: phone
        pattern: "###-###-{last4}"
        unmask_permission: [admin, owner]
        unmask_action: click        # click | hover | button
        log_unmask: true
        
      - field: email
        pattern: "{first2}***@{domain}"
        unmask_permission: [admin]
        
      - field: id_number
        pattern: "{first3}****{last3}"
        unmask_permission: [admin]
        require_reason: true        # 需要輸入查看原因
        
      - field: credit_card
        pattern: "****-****-****-{last4}"
        unmask_permission: []       # 永不顯示完整
        
      - field: salary
        pattern: "******"
        unmask_permission: [hr_admin, owner]
        audit_level: high
    
    # 欄位加密
    encryption:
      - field: ssn
        algorithm: AES-256-GCM
        key_source: vault
        
      - field: medical_record
        algorithm: AES-256-GCM
        key_source: per_user        # 每個使用者獨立金鑰
    
    # 欄位存取控制
    access_control:
      - field: internal_notes
        read: [internal_staff]
        write: [manager, admin]
        
      - field: cost_price
        read: [finance, admin]
        write: [finance_manager]
```

### 8.3 資料隔離

```yaml
security:
  data_isolation:
    # 隔離模式
    mode: tenant              # tenant | department | team | owner
    
    # 隔離欄位
    scope_field: organization_id
    
    # 隔離規則
    rules:
      # 租戶隔離
      tenant:
        field: tenant_id
        auto_filter: true       # 自動加入查詢條件
        auto_set: true          # 新增時自動設定
        immutable: true         # 不可修改
        
      # 部門隔離
      department:
        field: department_id
        hierarchy: true         # 支援層級（上級可看下級）
        cross_access:
          - role: admin
            access: all
          - role: hr
            access: all_read
            
      # 擁有者隔離
      owner:
        field: created_by
        share:
          enabled: true
          field: shared_with
          max_shares: 10
    
    # 例外規則
    exceptions:
      - role: super_admin
        bypass: all
        audit: true
        
      - entity: PublicAnnouncement
        bypass: tenant
        
    # 隔離驗證
    validation:
      on_read: true
      on_write: true
      on_delete: true
      fail_silently: false      # 違規時是否顯示錯誤
```

### 8.4 敏感操作保護

```yaml
security:
  sensitive_operations:
    # 需要 MFA 的操作
    require_mfa:
      - action: delete_user
        mfa_type: [totp, sms]
        
      - action: export_all
        mfa_type: [totp]
        cooldown: 3600          # 1小時內免再驗證
        
      - action: change_permission
        mfa_type: [totp, email]
        
      - action: access_sensitive_data
        mfa_type: [totp]
        session_duration: 300   # 5分鐘後需重新驗證
    
    # 需要確認的操作
    require_confirmation:
      - action: delete
        type: dialog
        message: "確定要刪除 {name} 嗎？此操作無法復原。"
        require_input: false
        
      - action: bulk_delete
        type: dialog
        message: "確定要刪除選取的 {count} 筆資料嗎？"
        require_input: true
        input_match: "DELETE"   # 需輸入指定文字
        
      - action: publish
        type: dialog
        message: "發布後將對所有使用者可見，確定要發布嗎？"
        show_preview: true
    
    # 需要核准的操作
    require_approval:
      - action: large_order
        condition: "amount > 100000"
        approvers: [manager, finance]
        approval_type: any      # any | all | majority
        timeout: 86400          # 24小時
        
      - action: data_export
        condition: "record_count > 1000"
        approvers: [data_owner, compliance]
        approval_type: all
        
    # 操作限制
    rate_limits:
      - action: login_attempt
        limit: 5
        window: 300             # 5分鐘內
        lockout: 900            # 鎖定15分鐘
        
      - action: password_reset
        limit: 3
        window: 3600
        
      - action: api_call
        limit: 100
        window: 60
        by: user
```

### 8.5 輸入防護

```yaml
security:
  input_protection:
    # XSS 防護
    xss:
      enabled: true
      mode: strict            # strict | moderate | permissive
      sanitize_html: true
      allowed_tags: [b, i, u, a, p, br, ul, ol, li]
      allowed_attributes:
        a: [href, title]
      strip_dangerous: true
      
    # SQL 注入防護
    sql_injection:
      enabled: true
      parameterized_only: true
      block_suspicious: true
      
    # CSRF 防護
    csrf:
      enabled: true
      token_field: _csrf_token
      cookie_name: csrf_token
      header_name: X-CSRF-Token
      
    # 檔案上傳防護
    file_upload:
      # 允許的類型
      allowed_types:
        - mime: "image/*"
          extensions: [jpg, jpeg, png, gif, webp]
        - mime: "application/pdf"
          extensions: [pdf]
        - mime: "application/vnd.openxmlformats-officedocument.*"
          extensions: [docx, xlsx, pptx]
          
      # 禁止的類型
      blocked_types:
        - mime: "application/x-executable"
        - extensions: [exe, bat, cmd, sh, php, js]
        
      # 檔案掃描
      scanning:
        enabled: true
        service: clamav
        on_upload: true
        quarantine: true
        
      # 大小限制
      max_size: 10MB
      max_total_size: 100MB   # 單次上傳總大小
      
    # 輸入長度限制
    max_lengths:
      default: 1000
      text_area: 10000
      search: 200
      email: 254
      url: 2048
```

### 8.6 稽核日誌

```yaml
security:
  audit:
    # 啟用稽核
    enabled: true
    
    # 稽核等級
    level: detailed           # minimal | standard | detailed
    
    # 需稽核的操作
    operations:
      - type: create
        entities: all
        fields: all
        
      - type: update
        entities: all
        fields: changed        # all | changed | sensitive
        
      - type: delete
        entities: all
        fields: all
        soft_delete_info: true
        
      - type: read
        entities: [sensitive_entity]
        condition: "is_bulk_read || is_export"
        
      - type: login
        success: true
        failure: true
        
      - type: permission_change
        before_after: true
    
    # 稽核欄位
    record:
      - timestamp
      - user_id
      - user_name
      - ip_address
      - user_agent
      - action
      - entity
      - entity_id
      - changes
      - request_id
      - session_id
      
    # 敏感資料處理
    sensitive_handling:
      mode: hash              # hash | mask | omit
      fields: [password, credit_card, ssn]
      
    # 儲存設定
    storage:
      type: separate_db       # same_db | separate_db | external
      retention: 2555         # 7年
      encryption: true
      
    # 告警設定
    alerts:
      - condition: "failed_login_count > 5"
        channel: [email, slack]
        severity: warning
        
      - condition: "bulk_delete_count > 100"
        channel: [email, slack, pager]
        severity: critical

---

## 八の五、haPDL 測試性規格 ⭐ v3.2.1

haPDL 的 `testing:` 區塊定義轉換器層的測試配置，轉換後展開為 PDL 的 `testing.mock_data` 區塊。

```yaml
testing:
  selectors:
    strategy: data-testid | id | class | role   # 預設: data-testid

  mock:
    enabled: true | false                        # 預設: true
    fixtures:                                    # 可選，指定固定測試資料
      - entity: EntityName
        file: "path/to/fixture.json"

  notes: |                                       # 可選，測試備註
    自由文字說明
```

**語意說明**：
- `selectors.strategy`: 轉換器產生 PDL 元素選取器時的首選策略。預設 `data-testid` 最佳實踐適用性。
- `mock.enabled`: 啟用後轉換器自動產生 PDL 的 `mock_data` 區塊。`true` 為所有頁面的 global_defaults。
- `mock.fixtures`: 指定固定測試夫資料檔，覆寫自動產生的 mock_data。
- [參照相對應] PDL `testing.mock_data` 區塊定義詳見 `pdl-syntax-v3.2.md` §testing。

大多數頁面不需寫此區塊，全局預設從 `global_defaults` 給入：`strategy=data-testid`、`mock.enabled=true`。

## 九、複雜表單支援 ⭐ NEW

### 9.1 動態區塊

```yaml
view:
  form:
    dynamic_sections:
      # 條件顯示區塊
      - section: business_info
        visible_when: "customer_type == 'business'"
        fields:
          - company_name!
          - tax_id!
          - company_address
          
      - section: individual_info
        visible_when: "customer_type == 'individual'"
        fields:
          - id_number
          - birth_date
          
      # 條件必填
      - section: shipping_info
        visible_when: "delivery_method == 'shipping'"
        required_when: "delivery_method == 'shipping'"
        fields:
          - shipping_address!
          - recipient_name!
          - recipient_phone!
          
      # 多條件組合
      - section: international_shipping
        visible_when: |
          delivery_method == 'shipping' && 
          shipping_address.country != 'TW'
        fields:
          - customs_declaration!
          - tariff_code
          
    # 欄位級條件
    conditional_fields:
      - field: other_reason
        visible_when: "reason == 'other'"
        required_when: "reason == 'other'"
        
      - field: discount_code
        visible_when: "has_discount == true"
        validation_when: "has_discount == true"
```

### 9.2 可重複欄位群組

```yaml
view:
  form:
    repeatable:
      # 聯絡人列表
      - name: contacts
        label: "聯絡人"
        min: 1
        max: 5
        default_count: 1
        
        fields:
          - name: name
            type: text
            required: true
            placeholder: "姓名"
            
          - name: phone
            type: tel
            required: true
            placeholder: "電話"
            
          - name: email
            type: email
            required: false
            placeholder: "Email"
            
          - name: is_primary
            type: radio_in_group  # 群組內單選
            label: "主要聯絡人"
            
        # UI 配置
        ui:
          layout: card          # card | table | inline
          add_label: "新增聯絡人"
          remove_label: "移除"
          sortable: true        # 可拖曳排序
          collapse: false       # 可收合
          
        # 驗證
        validation:
          - rule: "items.filter(c => c.is_primary).length === 1"
            message: "請指定一位主要聯絡人"
            
      # 訂單項目（表格形式）
      - name: order_items
        label: "訂單項目"
        min: 1
        max: 50
        
        fields:
          - name: product
            type: autocomplete
            source: "api:/products"
            required: true
            width: 30%
            
          - name: quantity
            type: number
            required: true
            min: 1
            width: 15%
            
          - name: unit_price
            type: currency
            readonly: true      # 從產品帶入
            width: 20%
            
          - name: discount
            type: percent
            default: 0
            max: 50
            width: 15%
            
          - name: subtotal
            type: currency
            computed: "quantity * unit_price * (1 - discount / 100)"
            readonly: true
            width: 20%
            
        ui:
          layout: table
          add_label: "新增項目"
          show_row_number: true
          
        # 群組計算
        summary:
          - field: subtotal
            aggregation: sum
            label: "小計"
          - field: quantity
            aggregation: sum
            label: "總數量"
```

### 9.3 跨欄位驗證

```yaml
view:
  form:
    validations:
      # 跨欄位比較
      cross_field:
        - fields: [start_date, end_date]
          rule: "end_date > start_date"
          message: "結束日期必須晚於開始日期"
          
        - fields: [password, confirm_password]
          rule: "password === confirm_password"
          message: "兩次輸入的密碼不一致"
          
        - fields: [min_price, max_price]
          rule: "max_price >= min_price"
          message: "最高價不得低於最低價"
          
      # 條件驗證
      conditional:
        - field: tax_id
          rule: "isValidTaxId(tax_id)"
          when: "customer_type === 'business'"
          message: "請輸入有效的統一編號"
          
        - field: id_number
          rule: "isValidIdNumber(id_number)"
          when: "customer_type === 'individual' && nationality === 'TW'"
          message: "請輸入有效的身分證字號"
          
      # 群組驗證
      group:
        - group: shipping_address
          rule: "isCompleteAddress(shipping_address)"
          when: "delivery_method === 'shipping'"
          message: "請填寫完整的收件地址"
          
      # 非同步驗證
      async:
        - field: email
          rule: "api:/validate/email-unique?email={email}"
          debounce: 500
          message: "此 Email 已被使用"
          
        - field: coupon_code
          rule: "api:/validate/coupon?code={coupon_code}&total={total}"
          message: "優惠碼無效或已過期"
          
      # 自訂驗證函數
      custom:
        - name: isValidTaxId
          description: "驗證統一編號"
          implementation: |
            (value) => {
              if (!value || value.length !== 8) return false;
              // 統一編號驗證邏輯
              const weights = [1, 2, 1, 2, 1, 2, 4, 1];
              let sum = 0;
              for (let i = 0; i < 8; i++) {
                let product = parseInt(value[i]) * weights[i];
                sum += Math.floor(product / 10) + (product % 10);
              }
              return sum % 10 === 0 || (value[6] === '7' && (sum + 1) % 10 === 0);
            }
```

### 9.4 表單狀態管理

```yaml
view:
  form:
    state:
      # 髒資料檢查
      dirty_check:
        enabled: true
        prompt_on_leave: true
        message: "您有未儲存的變更，確定要離開嗎？"
        exclude_fields: [_csrf_token, _timestamp]
        
      # 自動儲存
      auto_save:
        enabled: true
        delay: 5000           # 5秒無操作後儲存
        storage: localStorage # localStorage | server
        key: "draft-{page}-{id}"
        max_age: 86400        # 24小時
        exclude_fields: [password, credit_card]
        notify: true          # 顯示「已自動儲存」提示
        
      # 草稿恢復
      draft_recovery:
        enabled: true
        prompt: true          # 詢問是否恢復
        message: "偵測到未完成的草稿，是否恢復？"
        
      # 步驟記憶（Wizard 表單）
      step_memory:
        enabled: true
        persist: sessionStorage
        
      # 表單重設
      reset:
        confirm: true
        message: "確定要清除所有輸入嗎？"
        preserve: [entity_id]  # 保留的欄位
```

---

## 十、檔案處理規格 ⭐ NEW

### 10.1 檔案上傳

```yaml
file_handling:
  upload:
    # 基本設定
    mode: single            # single | multiple | directory
    accept: [".pdf", ".docx", "image/*"]
    max_size: 10MB
    max_files: 20
    max_total_size: 100MB
    
    # 分塊上傳
    chunked:
      enabled: true
      chunk_size: 2MB
      parallel: 3           # 並行上傳數
      retry: 3
      resume: true          # 支援斷點續傳
      
    # 上傳前處理
    preprocessing:
      images:
        resize:
          enabled: true
          max_width: 1920
          max_height: 1080
          quality: 0.85
        compress:
          enabled: true
          max_size: 1MB
        format_convert:
          heic_to: jpg
          
      documents:
        virus_scan: true
        
    # 上傳進度
    progress:
      display: individual   # individual | combined | both
      show_speed: true
      show_remaining: true
      
    # 拖放區
    drag_drop:
      enabled: true
      zone_selector: ".upload-zone"
      highlight_class: "drag-over"
      accept_directories: false
      
    # 上傳佇列
    queue:
      enabled: true
      auto_start: true
      max_concurrent: 3
      retry_failed: true
```

### 10.2 檔案預覽

```yaml
file_handling:
  preview:
    # 圖片預覽
    images:
      enabled: true
      thumbnail_size: 100x100
      lightbox: true
      zoom: true
      rotate: true
      
    # 文件預覽
    documents:
      pdf:
        enabled: true
        renderer: pdfjs
        max_pages: 50
      office:
        enabled: true
        service: office_online  # office_online | google_docs | custom
      text:
        enabled: true
        max_size: 1MB
        syntax_highlight: true
        
    # 影片預覽
    videos:
      enabled: true
      thumbnail: true
      player: native        # native | videojs | plyr
      autoplay: false
      max_duration: 3600    # 1小時
      
    # 音訊預覽
    audio:
      enabled: true
      player: native
      waveform: true
```

### 10.3 檔案管理

```yaml
file_handling:
  management:
    # 檔案資訊
    metadata:
      show: [name, size, type, created_at, uploaded_by]
      editable: [name, description, tags]
      
    # 檔案操作
    operations:
      download:
        enabled: true
        direct: false       # 是否直接下載（vs 透過 API）
        log: true
        
      rename:
        enabled: true
        validation: "^[a-zA-Z0-9_.-]+$"
        
      delete:
        enabled: true
        confirm: true
        soft_delete: true
        
      move:
        enabled: true
        target_folders: true
        
      copy:
        enabled: true
        
      share:
        enabled: true
        expiry_options: [1h, 24h, 7d, 30d, never]
        password_protect: true
        
    # 版本控制
    versioning:
      enabled: true
      max_versions: 10
      auto_version: true
      diff_view: true
```

---

## 附錄 A：haAPI 綁定與操作映射 ⭐ v3.1 · 更新 v3.2

### A.1 頁面級 API 綁定

透過頁面頂層 `api:` 欄位建立 haPDL 頁面與 haAPI 定義的雙向追溯鏈：

```yaml
page: user-list
type: list
entity: InfoUser
api: user-management    # 指向 haAPI 定義名稱

page: user-detail
type: detail
entity: InfoUser
api: user-management    # 同一 haAPI 可被多個頁面引用
```

此欄位對應 haAPI 端的 `consumers.pages` 聲明。Linter 可檢驗雙向一致性。

### A.2 actions.operations 語法

`actions.operations` 引用 haAPI 的業務操作名稱（不硬編碼 URL）：

```yaml
actions:
  standard: [create, edit, delete]          # 對應 haAPI standard CRUD
  operations: [activate, deactivate]        # 引用 haAPI operations 名稱

  custom:
    - name: export
      operation: export                     # 引用 haAPI operation
      params:
        format: csv
    - name: bulk_import
      operation: bulk_import                # haAPI 標記 async: true
      async_ui:                             # 非同步操作 UI 行為
        submit_feedback: toast              # 提交後顯示 toast（非阻塞）
        progress: polling                   # 輪詢進度
        completion: notification            # 完成後推播通知
```

轉換器會自動從 haAPI 定義解析出端點、HTTP 方法、角色權限，產出完整的 PDL action 配置。

> ⭐ **v3.2 補充**：haAPI v3.2 新增了 `proxy` 型操作（如 `get_captcha`、`verify_captcha`），這些操作對 haPDL 完全透明 — haPDL 只需在 `operations` 中引用操作名稱，不需要知道它是 proxy 轉發還是有本地邏輯的操作。轉換器會統一處理 PDL 展開。

### A.3 async_ui（非同步操作 UI）

當 haAPI 操作標記 `async: true` 時，haPDL 可透過 `async_ui` 定義前端非同步 UX：

| 屬性 | 說明 | 預設值 |
|------|------|--------|
| `submit_feedback` | 提交後回饋方式：`toast` / `modal` / `inline` | `toast` |
| `progress` | 進度追蹤方式：`polling` / `websocket` / `none` | `polling` |
| `completion` | 完成通知方式：`notification` / `toast` / `redirect` | `notification` |

注意：此處的 `async_ui` 關注**前端 UX**（提交回饋、進度顯示），與 §6 `async` 區塊的**資料獲取策略**（cache-first、樂觀更新）是不同層次。

### A.4 events 訂閱（P2 預留）

> ⚠️ **此區塊為 P2 預留設計**，尚未納入正式語法。待 WebSocket / SSE 整合方案確定後再正式定義。

haAPI 的 `consumers.events` 定義了後端事件（如 `user.created`），haPDL 需要前端事件訂閱機制來觸發即時更新：

```yaml
# 未來 haPDL 語法（草案）
events:
  subscribe:
    - event: user.created      # 來自 haAPI consumers.events
      action: refresh_list     # 前端行為：重新整理列表
    - event: user.updated
      action: update_item      # 前端行為：更新單筆資料
```

對應的 PDL 展開需定義 WebSocket/SSE 連線配置與事件處理策略。

---

## 附錄 B：Annotated DBML 整合規則 ⭐ v3.1

### B.1 label: 標籤推斷

當 DBML 欄位有 `label:` 屬性時，haPDL 轉換器**優先使用此標籤**作為欄位顯示名稱，不走推斷邏輯。

```yaml
# DBML 定義
# order_number varchar(50) [label: '訂單編號']

# haPDL 中直接寫欄位名（不需額外指定標籤）
columns:
  - order_number     # 轉換器自動套用 DBML label → '訂單編號'

# 標籤解析優先順序
# ① DBML label: → ② haPDL 明確指定 → ③ Convention 推斷（translations 字典）→ ④ Capitalize
```

### B.2 ref_code: 動態列舉

當 DBML 欄位有 `ref_code:` 屬性時，轉換器自動推斷為 select 輸入並設定動態來源：

```yaml
# DBML 定義
# userType nchar(1) [not null, ref_code: 'UserType', label: '使用者類別']

# haPDL 中不需額外指定（自動推斷）
columns:
  - userType        # 偵測到 ref_code → 自動用 select + 動態來源

# 轉換器產出的 PDL
# form:
#   fields:
#     - field: userType
#       label: '使用者類別'
#       input: select
#       options:
#         source: '/api/code-mains?codeId=UserType'
#         value_field: mcode
#         label_field: mcodeName
```

### B.3 sensitive: 敏感欄位

DBML `sensitive: true` 與 haPDL `fieldName*` 符號聯合判定：

```
sensitive 判定 = DBML sensitive: true  ∪  haPDL fieldName* 符號
                 ↓
                 PDL security.field_level.masking 自動包含此欄位
```

- DBML 標了 `sensitive: true`，haPDL 未標 `*` → **仍自動遮罩**
- DBML 未標，haPDL 標了 `*` → **仍自動遮罩**
- 兩者都標了 → **合併，以 haPDL 的遮罩模式為準**（haPDL 可覆寫 DBML 預設行為）

### B.4 group: 表單分組

DBML `group:` 用於自動產生 PDL 表單 `sections`：

```yaml
# DBML 定義
# order_number varchar(50) [group: 'basic', label: '訂單編號']
# order_date date [group: 'dates', label: '訂單日期']

# haPDL 中可以覆寫分組（頁面級）
view:
  form:
    sections:
      - id: basic
        fields: [order_number, customer_name, status]
      - id: dates
        fields: [order_date, delivery_date]

# 若 haPDL 未指定 sections，轉換器從 DBML group: 自動產生：
# sections:
#   - id: basic
#     title: '基本資訊'   ← group 名稱 → Convention 推斷中文標題
#     fields: [order_number, ...]
#   - id: dates
#     title: '日期資訊'
#     fields: [order_date, ...]
```

> **術語對應**：DBML `group:` = PDL `section`。兩者描述同一概念但層次不同 — DBML 是「領域結構分組」，PDL 是「UI 表單分區」。

---

## 附錄 C：Resolution Order（查找優先順序）⭐ v3.1 · 更新 v3.2

當多個來源同時提供同一屬性時，按以下優先順序解析（左高右低）：

```
① DBML 明確標註 → ② haAPI 定義 → ③ haPDL 符號/配置 → ④ Convention 推斷 → ⑤ 預設值
```

### 完整查找矩陣

| 屬性 | ① DBML 標註 | ② haAPI 定義 | ③ haPDL 配置 | ④ Convention | ⑤ 預設值 |
|------|:---:|:---:|:---:|:---:|:---:|
| **欄位標籤** | `label:` | — | — | `translations{}` | `Capitalize` |
| **輸入型別** | — | — | 符號 `@[]{}` | `dbml_type→input` | `text` |
| **顯示型別** | — | — | 符號 `:badge` | `dbml_type→display` | `text` |
| **必填** | `[not null]` | — | 符號 `!` | — | `false` |
| **敏感** | `sensitive:` | `data_masking` | 符號 `*` | 名稱推斷 | `false` |
| **列舉來源** | `ref_code:` | `enum` in filters | — | — | — |
| **分組** | `group:` | — | section 配置 | — | 無分組 |
| **API 端點** | — | `exposes` | `api:` 引用 | CamelCase→kebab | — |
| **權限** | — | `access.permissions` | `auth.roles` | — | 無限制 |
| **MFA 需求** | — | `require_mfa` | — | — | `false` |
| **Resilience (timeout/retry)** | — | `ext.*` step / `advanced.external_resilience` / `codegen.config` | — | — | 框架內建値 |
| **搜尋目標欄位** | — | `search.fields` | `keyword~` 觸發 | — | entity 全部 text 欄位 |
| **驗證規則** | `[not null]`/`nvarchar(N)` | `validation.rules` | 明確覆寫 | 型別推斷 | 無驗證 |
| **前端權限** | — | `access.permissions` | 收緧子集 | — | 無限制 |

### 特殊合併規則

- **sensitive**：DBML ∪ haPDL（聯集，任一來源標記即生效）
- **權限**：haAPI `field_restrictions` 推導至 PDL `security.field_level.access_control`
- **MFA**：haAPI `require_mfa` 推導至 PDL `security.sensitive_operations.require_mfa`
- **Resilience** ⭐ v3.2：haAPI 專屬，採三層級聯（Step-level → API-level `advanced.external_resilience` → Project-level `codegen.config.yaml` → 框架內建預設）。haPDL/PDL 不直接參與此解析鏈。
- **搜尋目標欄位** ⭐ v3.2.1：`keyword~` / `keyword=` 觸發查找 haAPI `search.fields`；無 haAPI 時 Convention 搜尋 entity 內所有 text 欄位
- **驗證規則** ⭐ v3.2.1：见下方 「Validation Rules 推斷鏈」
- **前端權限** ⭐ v3.2.1：见下方 「Permissions 推斷規則」

### Validation Rules 推斷鏈 ⭐ v3.2.1

form 頁面的 `error_handling.validation.rules` 依以下優先順序自動推斷：

| 規則 | ① DBML | ② haAPI | ③ haPDL 覆寫 | ④ Convention |
|------|--------|---------|-------------|-------------|
| required | `[not null]`, `[pk]` | — | `!` 符號 | — |
| maxLength | `nvarchar(N)` → N | `max_length` | 明確指定 | — |
| unique | `[pk]`, `[unique]` | `unique: true` | — | — |
| min/max | — | — | 明確指定 | tinyint→0-255, int→-2³¹~2³¹ |
| pattern | — | `pattern` | 明確指定（⚠️ 應嚴於 haAPI） | — |

**覆寫規則**：
- haPDL 可收緧但不應放寬 haAPI 的驗證規則
- 若 haPDL pattern 比 haAPI 寬鬆，Linter 應發出 warning
- `validation.rules` 中只需寫與推斷結果不同的部分

### Permissions 推斷規則 ⭐ v3.2.1

`security.permissions` 預設從 haAPI 的 `access.permissions` 自動推斷。

推斷映射：

| haPDL 操作 | haAPI 操作 |
|-----------|-----------|
| view | list + read |
| create | create |
| edit | update |
| delete | delete |

**覆寫規則**：
- haPDL 只能收緧（取子集），不能放寬 haAPI 的權限
- 若 haPDL permissions 包含 haAPI 不允許的 role，Linter 應發出 error
- 省略 `security.permissions` 時，完全没用 haAPI 定義

---

**文件維護者**: WA-RAPTor 團隊
**最後更新**: 2026-04-07
**版本**: 3.2.1
**參照文件**: `haPDL-page-type-defaults-v3.2.1.md`（Page Type Defaults 獨立規格）

---

## TODO（待辦事項）

### [2026-04-23] `*?` 符號（sensitive + optional）+ validation 組合的「空值豁免」語義

**來源**：`ccwLog/0423-UiTest_UserEdit-password.md`（密碼選填欄位驗證豁免問題）

**議題**：
haPDL 的 `password*?` 正確表達「敏感 + 選填」，但規格未明文定義：當選填欄位（`?`）同時存在於 `error_handling.validation.rules` 中（如 `minLength`、`pattern`）時，驗證應在「有值時」才觸發，空值時應被豁免。目前 haPDL → PDL 轉換器未自動補此條件，導致下游 Pdl2whyVue 生成的 Vue 元件對選填欄位的空值仍觸發錯誤。

**行動項**：
- [ ] 在 §符號系統（`*`、`?`、`!`、`@`）章節補充「`?` + validation 的語義規則」：`?` 欄位在 `validation.rules` 中的規則，僅在欄位有值時觸發
- [ ] 新增「optional + rule」的 worked example，明確輸出 PDL 應帶 `skip_if_empty: true` 或 `condition: not_empty`
- [ ] 在 Cross-cutting 規則矩陣（附錄 C）註明此語義，並與 `haAPI.field_overrides.skip_if_empty`、`PDL.validation.condition` 命名對齊
- [ ] 更新 haPDL2PDL 轉換器（`8codeGens/haPDL2PDLspec-v3.2.md`）相應補規則

**優先度**：P1（haPDL 是上游意圖層，應先定義語義，下游才能正確生成）
