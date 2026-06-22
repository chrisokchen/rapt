# PDL (Page Description Language) 語法規格 v3.3

**版本**: v3.3.0 (Release Candidate, 2026-05-13)
**最後更新**: 2026-05-13
**前版**: v3.2（見 `archive/pdl-syntax-v3.2.md`）
**基於**: pdl-syntax.md v1.0 + haPDL-specification-v3.0.md 新增功能 + 跨規格對齊 v3.1 + haAPI v3.2 對齊 + haARM v3.3 雙軌引用

---

## 版本沿革

| 版本 | 日期 | 重點變更 |
|------|------|----------|
| 1.0 | 2025-10-31 | 初始版本：頁面結構、資料來源、欄位、動作、權限、佈局 |
| 3.0 | 2026-03-31 | **重大升級**：對齊 haPDL v3.0，新增狀態管理、錯誤處理、非同步行為、無障礙、安全性、複雜表單、檔案處理、測試性 |
| 3.1 | 2026-03-31 | **跨規格對齊**：haAPI 綁定（api_ref）、operations 映射、DBML 標註整合（label/ref_code/sensitive/group）、? 符號消歧、Resolution Order、field_restrictions 推導、async_ui 展開、events 預留 |
| 3.2 | 2026-04-02 | **haAPI v3.2 對齊**：proxy 操作展開規則、Resolution Order 新增 Resilience、error_handling 支援外部服務錯誤、`input`/`result` 術語對照、版本引用更新 |

### v3.1 跨規格對齊變更摘要 ⭐ NEW

- 🔗 **haAPI 綁定**：datasource 新增 `api_ref`，actions 新增 operations 映射展開規則
- 🏷️ **DBML 標註整合**：label → 欄位標籤、ref_code → options、sensitive → masking、group → sections
- ❓ **`?` 符號消歧**：附錄 E 明確定義 filter / column / form 三種上下文
- 🔒 **field_restrictions 推導**：從 haAPI access.permissions 推導欄位級讀寫權限
- ⚡ **async_ui 展開**：haAPI async 操作對應的前端 UX 配置
- 📋 **Resolution Order 參考**：屬性查找優先順序（DBML → haAPI → haPDL → Convention → Default）
- 📡 **events 預留**：P2 事件訂閱區塊草案

### v3.2 haAPI v3.2 對齊變更摘要 ⭐ NEW

- 🔀 **proxy 操作展開**：haAPI `proxy` 型操作的 PDL action 展開規則
- 🔄 **Resilience 級聯**：Resolution Order 新增 Resilience 屬性（haAPI 專屬三層級聯）
- ⚠️ **外部服務錯誤**：error_handling 支援 `ext.*` 呼叫的 `on_fail` 錯誤處理
- 📖 **術語對照**：haAPI v3.2 `input`/`result` 與 PDL `params`/`response` 對照

### v3.0 新增區塊總覽

- 🔄 **狀態管理** (`state`)：local/shared/cascading/persistence/computed/watchers
- ⚠️ **錯誤處理** (`error_handling`)：validation/api/network/business/boundary
- ⚡ **非同步行為** (`async`)：fetching/mutations/loading/request_control/caching
- ♿ **無障礙存取** (`accessibility`)：semantics/aria/keyboard/screen_reader/visual/compliance
- 🔒 **安全性** (`security`)：field_level/data_isolation/sensitive_operations/input_protection/audit
- 📝 **複雜表單** (`complex_form`)：dynamic_sections/repeatable/cross_field_validation/form_state
- 📁 **檔案處理** (`file_handling`)：upload/preview/management
- 🧪 **測試性** (`testing`)：selectors/mock_data/gherkin_integration
- 🆕 **新頁面類型**：kanban、calendar

---

## 目錄

1. [概述](#概述)
2. [核心概念](#核心概念)
3. [文件結構](#文件結構)
4. [頁面類型](#頁面類型)
5. [資料來源](#資料來源)
6. [欄位定義](#欄位定義)
7. [驗證規則](#驗證規則)
8. [動作與效果](#動作與效果)
9. [權限控制](#權限控制)
10. [佈局與樣式](#佈局與樣式)
11. [狀態管理](#狀態管理) ⭐ NEW
12. [錯誤處理](#錯誤處理) ⭐ NEW
13. [非同步行為](#非同步行為) ⭐ NEW
14. [無障礙存取](#無障礙存取) ⭐ NEW
15. [安全性](#安全性) ⭐ NEW
16. [複雜表單](#複雜表單) ⭐ NEW
17. [檔案處理](#檔案處理) ⭐ NEW
18. [測試性](#測試性) ⭐ NEW
19. [TypeScript 型別定義](#typescript-型別定義)
20. [完整範例](#完整範例)

---

## 概述

**PDL (Page Description Language)** 是一種宣告式的領域特定語言，用於定義 Web 應用程式的頁面結構、行為和互動。PDL 是 haPDL 轉換後的**目標格式**（展開格式），包含所有明確配置而無符號縮寫。

### 設計理念

1. **宣告式而非命令式** - 描述「是什麼」而非「怎麼做」
2. **規格即程式碼** - 從規格自動產生 UI 元件、API 規格、測試
3. **分離關注點** - 資料、UI、邏輯、權限各自獨立定義
4. **可組合與可擴展** - 支援元件重用與自訂擴展
5. **行為完整性** ⭐ NEW - 完整描述動態互動、狀態管理與錯誤處理

### 支援的格式

- **YAML** - 主要格式，適合人類閱讀與編寫
- **JSON** - 程式化處理與工具整合
- **TypeScript** - 型別定義與程式碼產生

---

## 核心概念

### 1. 頁面 (Page)

頁面是 PDL 的基本單位，定義了 UI 的結構與行為。

```yaml
page:
  id: string                # 唯一識別碼
  type: page_type          # 頁面類型
  title: string            # 頁面標題
  route: string            # URL 路由
  schema_version: "3.0"    # PDL 規格版本 ⭐ NEW
  mixins: [...]            # 混入功能 ⭐ NEW
  auth: {...}              # 權限控制
  datasource: {...}        # 資料來源
  layout: {...}            # 佈局配置
  actions: [...]           # 使用者動作
  state: {...}             # 狀態管理 ⭐ NEW
  error_handling: {...}    # 錯誤處理 ⭐ NEW
  async: {...}             # 非同步行為 ⭐ NEW
  accessibility: {...}     # 無障礙存取 ⭐ NEW
  security: {...}          # 安全性 ⭐ NEW
  testing: {...}           # 測試性 ⭐ NEW
```

### 2. 資料流 (Data Flow)

PDL 支援四種資料來源，按優先順序：

1. **route** - URL 路徑參數
2. **store** - 全域狀態
3. **api** - API 端點
4. **user-input** - 使用者輸入

### 3. 效果鏈 (Effect Chain)

動作觸發效果，效果可嵌套形成鏈：

```
使用者動作 → 驗證 → API 呼叫 → 成功/失敗效果 → 後續動作
```

### 4. 權限模型 (Permission Model)

採用 **RBAC (Role-Based Access Control)**：
- 頁面級權限
- 動作級權限
- 欄位級權限

### 5. 狀態模型 (State Model) ⭐ NEW

支援多層級狀態管理：
- **local** - 頁面內部狀態
- **shared** - 跨頁面共享狀態（session / user / workflow / global）
- **cascading** - 欄位連動
- **computed** - 計算屬性
- **persistence** - 狀態持久化

---

## 文件結構

### 完整應用結構

```yaml
version: 3                    # PDL 版本 (升級為 3)

app:                          # 應用程式資訊
  name: string
  version: string
  schema_version: "3.0"       # ⭐ NEW
  config: {...}

models: {...}                 # 資料模型定義

pages: {...}                  # 頁面定義

navigation: {...}             # 導航選單

permissions: {...}            # 角色權限

theme: {...}                  # 全域樣式

# ⭐ NEW: 應用級配置
global_error_handling: {...}  # 全域錯誤處理
global_accessibility: {...}   # 全域無障礙設定
global_security: {...}        # 全域安全性設定
```

### 單一頁面檔案結構

```yaml
version: 3
page:
  id: string
  type: list|form|detail|grid|dashboard|modal|master-detail|explorer|wizard|search|report|kanban|calendar
  title: string
  route: string
  schema_version: "3.0"        # ⭐ NEW
  mixins: [...]                # ⭐ NEW
  auth:
    roles: [...]
  datasource: {...}
  header: {...}
  filters: [...]               # 僅 list 類型
  table: {...}                 # 僅 list 類型
  form: {...}                  # 僅 form 類型
  layout: {...}                # detail/dashboard/master-detail 類型
  actions: {...}
  hooks: {...}

  # ===== v3.0 新增頂層區塊 =====
  state: {...}                 # ⭐ NEW: 狀態管理
  error_handling: {...}        # ⭐ NEW: 錯誤處理
  async: {...}                 # ⭐ NEW: 非同步行為
  accessibility: {...}         # ⭐ NEW: 無障礙存取
  security: {...}              # ⭐ NEW: 安全性
  file_handling: {...}         # ⭐ NEW: 檔案處理
  testing: {...}               # ⭐ NEW: 測試性
```

---

## 頁面類型

PDL v3.0 支援十三種頁面類型。

### 1. 列表頁 (list)

**用途**: 顯示多筆資料，支援搜尋、篩選、分頁、排序

```yaml
page:
  type: list
  datasource:
    entity: EntityName
    query:
      endpoint: GET /resources
      params: [...]

  header:
    actions:
      - id: create
        label: "新增"
        route: /resource/new

  filters:
    - id: keyword
      label: "搜尋"
      input: text
    - id: status
      label: "狀態"
      input: select
      options: ["active", "inactive"]
    # ⭐ NEW: 區間篩選
    - id: created_at
      label: "建立時間"
      input: daterange
      operator: between
    # ⭐ NEW: 可空值篩選
    - id: assigned_to
      label: "負責人"
      input: select
      nullable: true
      null_label: "未指派"

  table:
    selectable: true
    columns:
      - key: id
        label: "ID"
        width: 80
        sortable: true
      - key: name
        label: "名稱"
        type: text
        sortable: true          # ⭐ 對應 haPDL fieldName^
        groupable: true         # ⭐ NEW: 對應 haPDL fieldName&
      - key: status
        label: "狀態"
        type: badge
        map:
          active: "success"
          inactive: "neutral"
      # ⭐ NEW: 新增顯示類型
      - key: location
        label: "位置"
        type: map               # 地圖座標
      - key: diff
        label: "變更"
        type: change-track      # 變更追蹤
      - key: config
        label: "設定"
        type: json-tree         # JSON 樹狀檢視
      - key: notes
        label: "備註"
        type: markdown-rendered # Markdown 渲染
      - key: actions
        label: ""
        type: row-actions
        actions: [...]

  bulk_actions: [...]
  pagination:
    enabled: true
    page_size: 20
```

#### 欄位類型 (v3.0 完整清單)

| 類型 | 說明 | 範例 |
|------|------|------|
| `text` | 純文字 | 名稱、描述 |
| `number` | 數字 | ID、數量 |
| `currency` | 貨幣 | 價格、金額 |
| `date` | 日期 | 建立日期 |
| `datetime` | 日期時間 | 更新時間 |
| `badge` | 徽章 | 狀態標籤 |
| `tag` | 標籤 | 分類標籤 |
| `avatar` | 頭像 | 使用者頭像 |
| `image` | 圖片 | 產品圖片 |
| `link` | 連結 | 外部網址 |
| `action_group` | 操作按鈕群組 | 編輯/刪除 |
| `row-actions` | 行操作 | 同上 |
| `toggle` | 開關狀態 | 是否啟用 |
| `bar` | 進度條 | 完成度 |
| `stars` | 星級評分 | 評分 |
| `chips` | 標籤群組 | 多標籤 |
| `truncate` | 截斷文字 | 長文字 |
| `map` | 地圖座標 ⭐ NEW | GPS 位置 |
| `swatch` | 色彩顯示 ⭐ NEW | 色碼 |
| `attachment` | 檔案附件 ⭐ NEW | 附件清單 |
| `avatar-name` | 頭像+名稱 ⭐ NEW | 使用者欄位 |
| `change-track` | 變更追蹤 ⭐ NEW | 修改紀錄 |
| `json-tree` | JSON 樹狀 ⭐ NEW | 結構化資料 |
| `markdown-rendered` | Markdown 渲染 ⭐ NEW | 內容欄位 |
| `code-highlight` | 程式碼高亮 ⭐ NEW | 程式碼片段 |

#### 格式化 (v3.0 完整清單)

| 格式 | 說明 | 範例 |
|------|------|------|
| `date` | 日期 (YYYY-MM-DD) | `2026-03-31` |
| `datetime` | 日期時間 | `2026-03-31 14:30` |
| `time` | 時間 (HH:mm) | `14:30` |
| `number(n)` | 數字（n位小數） | `1,234.56` |
| `percent` | 百分比 | `85.5%` |
| `bytes` | 檔案大小 | `1.2 MB` |
| `relative` | 相對時間 ⭐ NEW | `3 天後` |
| `humanize` | 人性化時間 | `2 小時前` |
| `compact` | 緊湊數字 ⭐ NEW | `1.2K` |
| `currency(CODE)` | 指定幣別 ⭐ NEW | `NT$ 1,234` |
| `uppercase` | 大寫 ⭐ NEW | `ABC` |
| `lowercase` | 小寫 ⭐ NEW | `abc` |
| `capitalize` | 首字大寫 ⭐ NEW | `Hello` |
| `mask(pattern)` | 遮罩格式 ⭐ NEW | `09**-***-789` |

#### 條件樣式

```yaml
columns:
  - key: stock
    label: "庫存"
    type: number
    conditional_style:
      - condition: "value < 10"
        style:
          color: red
          font_weight: bold
          background_color: "#ffe6e6"
      - condition: "value >= 100"
        style:
          color: green
```

---

### 2. 表單頁 (form)

**用途**: 新增或編輯資料

```yaml
page:
  type: form
  mode: auto  # auto | create | edit

  datasource:
    entity: EntityName
    query:  { endpoint: GET /resources/:id }
    submit: { endpoint: POST /resources }
    update: { endpoint: PUT /resources/:id }

  form:
    layout: vertical  # vertical | horizontal | tabs

    sections:
      - title: "基本資訊"
        collapsible: false
        fields:
          - field: name
            label: "名稱"
            input: text
            required: true
            placeholder: "請輸入名稱"

          - field: category
            label: "分類"
            input: select
            required: true
            options: "@lookup(Category,id,name)"

    tabs:
      - id: base
        title: "基本資訊"
        fields: [...]

    validation: [...]

  actions:
    primary: [...]
    secondary: [...]
    danger: [...]

  hooks:
    beforeSubmit: [...]
    afterSubmit: [...]
    onError: [...]
```

#### 輸入類型 (v3.0 完整清單)

| 類型 | 說明 | 屬性 |
|------|------|------|
| `text` | 單行文字 | `placeholder`, `maxLength` |
| `textarea` | 多行文字 | `rows`, `placeholder` |
| `number` | 數字 | `min`, `max`, `step` |
| `email` | 電子郵件 | `placeholder` |
| `password` | 密碼 | `placeholder` |
| `tel` | 電話號碼 | `placeholder` |
| `url` | 網址 | `placeholder` |
| `select` | 下拉選單 | `options`, `multiple` |
| `radio` | 單選按鈕 | `options` |
| `checkbox` | 多選框 | `options` |
| `switch` | 開關 | `default` |
| `date` | 日期選擇器 | `min`, `max` |
| `datetime` | 日期時間 | `min`, `max` |
| `time` | 時間選擇器 | `min`, `max`, `step` |
| `daterange` | 日期範圍 | - |
| `upload` | 檔案上傳 | `accept`, `maxSize`, `multiple` |
| `image` | 圖片上傳 | `accept`, `maxSize` |
| `rich_editor` | 富文本編輯器 | `height` |
| `markdown` | Markdown 編輯器 | `height` |
| `code` | 程式碼編輯器 | `language`, `height` |
| `color` | 顏色選擇器 | - |
| `slider` | 滑桿 | `min`, `max`, `step` |
| `rating` | 評分 | `max`, `allowHalf` |
| `tag_input` | 標籤輸入 | `maxTags` |
| `tree_select` | 樹形選擇 | `options`, `multiple` |
| `cascader` | 級聯選擇 | `options` |
| `transfer` | 穿梭框 | `options` |
| `autocomplete` | 自動完成 ⭐ NEW | `source`, `debounce` |
| `json_editor` | JSON 編輯器 ⭐ NEW | `schema`, `height` |

---

### 3. 詳情頁 (detail)

（同 v1.0，無變更）

---

### 4. 儀表板頁 (dashboard)

（同 v1.0，無變更）

---

### 5. 網格頁 (grid)

（同 v1.0，無變更）

---

### 6. 彈窗頁 (modal)

（同 v1.0，無變更）

---

### 7. Master-Details 頁 (master-detail)

（同 v1.0，無變更）

---

### 8. Explorer 頁 (explorer)

**用途**: 樹狀導覽 + 內容面板

```yaml
page:
  type: explorer
  datasource:
    tree:
      entity: Category
      query: { endpoint: GET /categories/tree }
    content:
      entity: Product
      query: { endpoint: GET /products?category={selectedNode.id} }

  layout:
    split:
      direction: horizontal
      sizes: [25, 75]
    tree:
      searchable: true
      selectable: single
      expandable: true
      lazy_load: true
    content:
      type: list    # list | detail | custom
      # content 區域使用標準 list/detail 配置
```

---

### 9. 看板頁 (kanban) ⭐ NEW

**用途**: 拖放式狀態管理（如 Trello 風格）

```yaml
page:
  type: kanban

  datasource:
    entity: Task
    query: { endpoint: GET /tasks }
    update: { endpoint: PATCH /tasks/:id }

  kanban:
    # 看板欄位（每個狀態一欄）
    group_by: status
    columns:
      - id: todo
        label: "待辦"
        color: "#e0e0e0"
        wip_limit: 10            # 在製品數量限制
      - id: in_progress
        label: "進行中"
        color: "#2196f3"
        wip_limit: 5
      - id: review
        label: "審核中"
        color: "#ff9800"
        wip_limit: 3
      - id: done
        label: "完成"
        color: "#4caf50"

    # 卡片配置
    card:
      title_field: title
      description_field: description
      assignee_field: assigned_to
      priority_field: priority
      due_date_field: due_date
      tags_field: labels
      cover_image_field: cover

      # 卡片樣式
      priority_colors:
        urgent: "#f44336"
        high: "#ff9800"
        normal: "#2196f3"
        low: "#9e9e9e"

    # 拖放設定
    drag_drop:
      enabled: true
      cross_column: true
      within_column: true        # 欄內排序
      confirm_transitions:       # 某些轉換需確認
        - from: in_progress
          to: done
          confirm: "確定任務已完成？"
      blocked_transitions:       # 禁止的轉換
        - from: done
          to: todo

    # 泳道（選用）
    swimlanes:
      enabled: false
      group_by: assignee

    # 篩選
    filters:
      - id: assignee
        label: "負責人"
        input: select
      - id: priority
        label: "優先級"
        input: select

  actions:
    - id: add_task
      label: "新增任務"
      route: /tasks/new
    - id: archive_done
      label: "封存已完成"
      call: "POST /tasks/archive"
      confirm: true
```

---

### 10. 日曆頁 (calendar) ⭐ NEW

**用途**: 時間軸檢視與事件管理

```yaml
page:
  type: calendar

  datasource:
    entity: Event
    query: { endpoint: GET /events }
    submit: { endpoint: POST /events }
    update: { endpoint: PUT /events/:id }
    delete: { endpoint: DELETE /events/:id }

  calendar:
    # 檢視模式
    views: [month, week, day, agenda]
    default_view: month

    # 事件欄位映射
    event:
      title_field: title
      start_field: start_time
      end_field: end_time
      all_day_field: is_all_day
      color_field: category
      description_field: description
      location_field: location
      recurrence_field: recurrence_rule

    # 事件顏色映射
    color_map:
      meeting: "#2196f3"
      deadline: "#f44336"
      reminder: "#ff9800"
      holiday: "#4caf50"

    # 互動
    interactions:
      click_event: detail_modal   # detail_modal | detail_page | inline_edit
      drag_resize: true           # 拖放調整時間
      drag_move: true             # 拖放移動日期
      click_empty: create_modal   # 點擊空白建立事件
      double_click: edit

    # 顯示設定
    display:
      week_starts_on: monday
      working_hours: {start: "09:00", end: "18:00"}
      show_weekends: true
      time_slot_interval: 30     # 分鐘
      max_events_per_day: 5      # 超過則顯示「+N 更多」
      show_current_time: true

    # 重複事件
    recurrence:
      enabled: true
      patterns: [daily, weekly, monthly, yearly, custom]
      max_occurrences: 365

  filters:
    - id: category
      label: "類別"
      input: checkbox
      options: [meeting, deadline, reminder, holiday]
    - id: date_range
      label: "日期範圍"
      input: daterange
```

---

### 11. Wizard 頁 (wizard)

（同 v1.0 概念，此處補充完整語法）

```yaml
page:
  type: wizard
  
  wizard:
    steps:
      - id: basic_info
        title: "基本資訊"
        description: "填寫基本資料"
        fields: [...]
        validation: [...]
        
      - id: details
        title: "詳細設定"
        fields: [...]
        skip_if: "mode == 'simple'"
        
      - id: confirm
        title: "確認送出"
        type: summary
        show_all_fields: true
        editable: true
    
    # 步驟導覽
    navigation:
      show_steps: true
      allow_skip: false
      allow_back: true
      linear: true              # 必須按順序
      
    # 進度指示器
    progress:
      type: steps               # steps | progress_bar | dots
      show_percentage: false
```

---

## 資料來源

（v3.1 新增 `api_ref` 欄位，其餘同 v1.0）

### datasource 配置

```yaml
datasource:
  entity: EntityName
  api_ref: resource-management    # ⭐ v3.1: 引用 haAPI 定義名稱（可追溯，對應 haAPI v3.2）
  query:
    endpoint: GET /resources
    params:
      - name: search
        from: filter.keyword
      - name: page
        from: pager.page
      - name: size
        from: pager.size
    cache:
      enabled: true
      ttl: 300
    on_error: show_toast
  submit:
    endpoint: POST /resources
  update:
    endpoint: PUT /resources/:id
```

### 參數來源

```yaml
params:
  - { name: category, from: filter.category }   # 篩選器
  - { name: id, from: route.id }                 # 路由
  - { name: token, from: query.token }           # 查詢字串
  - { name: user_id, from: store.currentUser.id }# 全域狀態
  - { name: name, from: form.name }              # 表單
  - { name: type, value: "product" }             # 固定值
```

### 資料轉換

```yaml
datasource:
  query:
    endpoint: GET /resources
    transform:
      - field: price
        type: number
        factor: 100
      - field: created_at
        type: date
        format: "YYYY-MM-DD HH:mm:ss"
      - field: status
        type: map
        mapping: { 1: "active", 0: "inactive" }
      - field: full_name
        type: computed
        expression: "firstName + ' ' + lastName"
```

---

## 欄位定義

### 欄位基本結構

```yaml
fields:
  - field: field_name
    label: "顯示標籤"
    input: text
    type: text
    required: true
    readonly: false
    disabled: false
    placeholder: "提示文字"
    help: "說明文字"
    default: "預設值"
    sortable: true              # ⭐ NEW: 可排序
    groupable: true             # ⭐ NEW: 可群組
    validation: [...]
    visible_if: "expression"
    permissions: [...]
    # ⭐ NEW: 連動相關
    cascading_source: true      # 此欄位為連動來源
    cascading_target: "field"   # 此欄位的連動對象
```

### 欄位標籤解析優先順序 ⭐ v3.1

當轉換器產生欄位 `label` 時，按以下優先順序解析：

1. **DBML `label:` 標註**：若 DBML 欄位已標註 `label:`，直接使用
2. **haPDL 明確指定**：若 haPDL 中以 `"label"` 覆寫
3. **Convention 推斷**：查 `translations` 字典（如 `created_at` → `"建立時間"`）
4. **Capitalize**：`snake_case` → 首字母大寫 + 空格（如 `user_name` → `"User Name"`）

### ref_code 動態列舉展開 ⭐ v3.1

當 DBML 欄位標註 `ref_code:` 時，轉換器自動展開為 `select` + 動態來源：

```yaml
# DBML: userType nchar(1) [not null, ref_code: 'UserType', label: '使用者類別']
# 轉換器自動產出：
fields:
  - field: userType
    label: "使用者類別"       # 來自 DBML label:
    input: select               # 來自 ref_code 推斷
    options:
      source: "/api/code-mains?codeId=UserType"   # 來自 ref_code 展開
      value_field: mcode
      label_field: mcodeName
    required: true              # 來自 DBML [not null]
```

### 欄位組

```yaml
form:
  sections:
    - title: "地址資訊"
      fields:
        - field: address_line1
          label: "地址行 1"
        - field_group:
            layout: inline
            fields:
              - { field: city, label: "城市", width: "33%" }
              - { field: state, label: "省份", width: "33%" }
              - { field: zipcode, label: "郵遞區號", width: "34%" }
```

---

## 驗證規則

### validation 語法

（同 v1.0 基礎驗證，以下新增 v3.0 功能）

```yaml
validation:
  # ===== v1.0 基礎驗證 =====
  - { field: name, rule: required, message: "此欄位為必填" }
  - { field: name, rule: max_length, value: 100, message: "不超過 100 個字元" }
  - { field: email, rule: email, message: "請輸入有效的電子郵件" }
  - { field: age, rule: range, min: 18, max: 100, message: "年齡必須在 18-100 之間" }
  - { field: sku, rule: pattern, value: "^[A-Z0-9-]+$", message: "格式不正確" }
  - { field: username, rule: unique, api: "GET /check-username", message: "已被使用" }
  - { rule: custom, expr: "startDate < endDate", message: "結束日期必須晚於開始日期" }

  # ===== v3.0 跨欄位驗證 ===== ⭐ NEW
  cross_field:
    - fields: [start_date, end_date]
      rule: "end_date > start_date"
      message: "結束日期必須晚於開始日期"
    - fields: [password, confirm_password]
      rule: "password === confirm_password"
      message: "兩次輸入的密碼不一致"

  # ===== v3.0 條件驗證 ===== ⭐ NEW
  conditional:
    - field: tax_id
      rule: "isValidTaxId(tax_id)"
      when: "customer_type === 'business'"
      message: "請輸入有效的統一編號"

  # ===== v3.0 非同步驗證 ===== ⭐ NEW
  async:
    - field: email
      rule: "api:/validate/email-unique?email={email}"
      debounce: 500
      message: "此 Email 已被使用"

  # ===== v3.0 群組驗證 ===== ⭐ NEW
  group:
    - group: shipping_address
      rule: "isCompleteAddress(shipping_address)"
      when: "delivery_method === 'shipping'"
      message: "請填寫完整的收件地址"
```

### 內建驗證類型

| 類型 | 說明 | 參數 |
|------|------|------|
| `required` | 必填 | - |
| `email` | Email 格式 | - |
| `phone` | 手機號碼 | - |
| `url` | 網址格式 | - |
| `pattern` | 正規表達式 | `value` |
| `min_length` | 最小長度 | `value` |
| `max_length` | 最大長度 | `value` |
| `min` | 最小值 | `value` |
| `max` | 最大值 | `value` |
| `range` | 數值範圍 | `min`, `max` |
| `unique` | 唯一性檢查 | `api`, `params` |
| `custom` | 自訂驗證 | `validator` 或 `expr` |
| `capacityCheck` | 容量檢查 | `expr` |

---

## 動作與效果

（v3.1 新增 haAPI operations 映射、async_ui 展開規則）

### UserAction 結構

```yaml
actions:
  - id: action_id
    label: "動作標籤"
    icon: "icon-name"
    style: primary
    permissions: [...]
    visible_if: "expression"
    disabled_if: "expression"
    route: "/target/path"
    call: "POST /api/endpoint"
    submit: true
    confirm: true
    confirm_title: "確認操作"
    confirm_message: "確定要執行此操作嗎？"
    on_success: effect_type
    on_error: effect_type
```

### haAPI operations 映射展開 ⭐ v3.1

haPDL 的 `actions.operations` 由轉換器展開為完整的 PDL action 配置：

```yaml
# haPDL 輸入：
# actions:
#   operations: [activate, deactivate]

# 轉換器從 haAPI 解析後產出 PDL：
actions:
  - id: activate
    label: "啟用"                  # 來自 haAPI operation.label
    icon: "check-circle"          # 來自 haAPI 或 Convention
    style: success
    call: "PUT /api/users/:id/activate"  # 來自 haAPI exposes
    permissions: [admin, manager]        # 來自 haAPI access.permissions
    confirm: true
    confirm_message: "確定要啟用此使用者嗎？"
    on_success: { type: toast, message: "已啟用", variant: success }

  - id: deactivate
    label: "停用"
    icon: "x-circle"
    style: warning
    call: "PUT /api/users/:id/deactivate"
    permissions: [admin]
    confirm: true
```

### proxy 操作展開規則 ⭐ v3.2

haAPI v3.2 新增了 `proxy` 型操作（純代理轉發，無本地業務邏輯）。proxy 操作對前端完全透明，展開為標準 PDL action：

```yaml
# haAPI v3.2 定義：
# operations:
#   - name: get_captcha
#     method: GET
#     path: /captcha
#     proxy:
#       target: ext.captcha.generate
#       pick: [id, image_data]
#
#   - name: verify_captcha
#     method: POST
#     path: /verify-captcha
#     proxy:
#       target: ext.captcha.validate
#       pick: [success, score]

# PDL 展開結果（與一般操作相同，proxy 對前端透明）：
actions:
  - id: get_captcha
    label: "取得驗證碼"
    call: "GET /api/users/captcha"        # 從 haAPI path 推導
    proxy: true                            # 標記為代理操作（供前端效能提示）
    response_fields: [id, image_data]      # 從 haAPI proxy.pick 推導

  - id: verify_captcha
    label: "驗證驗證碼"
    call: "POST /api/users/verify-captcha"
    proxy: true
    response_fields: [success, score]
```

**展開規則**：
- `proxy.target` 不展開到 PDL（屬於後端實作細節）
- `proxy.pick` → PDL `response_fields`（告知前端預期的回應結構）
- `proxy.enrich` 不展開到 PDL（後端自動補入的參數，前端不需要知道）
- PDL 可選擇性加入 `proxy: true` 標記，讓前端知道此呼叫是輕量轉發（可做快取/效能優化）

> **術語對照** ⭐ v3.2：haAPI v3.2 在 step 級使用 `input`（傳入值）和 `result`（回傳值）。PDL 展開時，`input` 對應 action 的 `params`/`body`，`result` 對應 `response`。此命名差異反映意圖層（haAPI）與實作層（PDL）的不同抽象級別。

### async_ui 展開規則 ⭐ v3.1

當 haAPI 操作標記 `async: true` 時，haPDL 的 `async_ui` 展開為 PDL 的非同步動作配置：

```yaml
# haPDL 輸入：
# actions:
#   custom:
#     - name: bulk_import
#       operation: bulk_import
#       async_ui:
#         submit_feedback: toast
#         progress: polling
#         completion: notification

# PDL 展開結果：
actions:
  - id: bulk_import
    label: "批次匯入"
    call: "POST /api/users/bulk-import"
    async: true
    async_config:
      submit_feedback:
        type: toast
        message: "已提交批次匯入任務"
      progress:
        type: polling
        endpoint: "GET /api/jobs/{jobId}/status"
        interval: 3000
        display: progress_bar
      completion:
        type: notification
        message: "批次匯入完成，共處理 {total} 筆"
        action: { type: navigate, target: "/import-results/{jobId}" }
```

### 效果鏈

```yaml
effects:
  - type: validate
    target: all-fields
    onSuccess:
      - type: api-call
        target: "POST /resources"
        onSuccess:
          - { type: show-modal, target: success-message }
          - { type: navigate, target: "/resources" }
        onError:
          - { type: show-modal, target: error-message }
```

### Hooks

```yaml
hooks:
  beforeLoad: [...]
  afterLoad: [...]
  beforeSubmit: [...]
  afterSubmit:
    - { type: toast, message: "已儲存", variant: success }
    - { type: redirect, to: "/resources" }
  onError: [...]
```

---

## 權限控制

（v3.1 新增 field_restrictions 推導規則；v3.2 + 2026-05-11 對齊 haARM v2 雙軌結構）

### 基本權限配置（v3.1 — auth-only mode，已對齊 haARM v2）

```yaml
auth:
  # 引用 .haarm.yaml roles[].id（粗粒度，OR 語意）
  roles: [admin, manager, user]
  page_permissions:
    view: [admin, manager, user]
    create: [admin, manager]
    edit: [admin, manager]
    delete: [admin]
```

### 雙軌權限配置（v3.2 + 2026-05-11，對齊 haARM v2）⭐ NEW

> **背景**：v3.1 的 `security.permissions: { view: [admin, manager] }` 雖名為 permission，內容其實是 role 字串。為與 haARM v2 對齊並支援 ABAC（含 scope / conditions），自 PDL v3.2 起拆為兩軌：
> - `auth.roles[]` ─ 粗粒度 RBAC（OR 語意），引用 haARM `role.id`
> - `security.permission_refs.{view|create|edit|delete}[]` ─ 細粒度 ABAC（AND 語意），引用 haARM `permission.id`
> - `security.datasource_scope` ─ 資料範圍提示，runtime-decidable，與 haAPI `scope` 對應

```yaml
auth:
  roles: [admin, manager, self]              # 引用 haARM role.id

security:
  permission_refs:                            # 引用 haARM permission.id（不展開 scope/conditions）
    view:
      - id: user_list
    create:
      - id: user_create
    edit:
      - id: user_update_own                  # 條件式 permission，conditions 保留於 haARM
    delete:
      - id: user_delete

  datasource_scope: own                       # all | own | department | team（與 haAPI scope 對應）

  # field_level 仍可使用 v3.1 結構（masking / access_control 等）
  field_level:
    masking:
      - { field: telephone, type: phone }
```

**渲染規則（Pdl2whyVue）：**

按鈕、列、路由的 v-if 表達式由 `auth.roles[]` 與 `security.permission_refs.{op}[]` 兩段組合：

```ejs
v-if="
  ( <%- gate.edit.roles.length %> === 0 || hasRole([<%- gate.edit.roles.map(r=>`'${r}'`).join(',') %>]) )
  && ( <%- gate.edit.permissions.length %> === 0 || hasPermission([<%- gate.edit.permissions.map(p=>`'${p}'`).join(',') %>]) )
"
```

**Deprecation Timeline：**

| 版本 | 舊（`security.permissions: { view: [admin,...] }`） | 新（`auth.roles` + `security.permission_refs`） |
|------|-------|-------|
| PDL v3.2 (current) | ✅ parser 接受 + emit deprecation warning | ✅ 接受 |
| PDL v3.3 | ⚠️ warning（lint 級） | ✅ 必用 |
| PDL v3.4 | ❌ 不接受 | ✅ 必用 |

### field_restrictions 推導（從 haAPI）⭐ v3.1

haAPI 的 `access.permissions.field_restrictions` 會被轉換器推導為 PDL 的 `security.field_level.access_control`：

```yaml
# haAPI 定義：
# access:
#   permissions:
#     update:
#       roles: [admin, manager, self]
#       field_restrictions:
#         admin: none
#         manager: [salary, ssn]
#         self: [name, email]

# PDL 展開結果：
security:
  field_level:
    access_control:
      salary:
        read: [admin, manager, self]
        write: [admin]              # manager 排除
      ssn:
        read: [admin, manager, self]
        write: [admin]              # manager 排除
      name:
        read: [admin, manager, self]
        write: [admin, manager, self]  # self 可編輯
      email:
        read: [admin, manager, self]
        write: [admin, manager, self]  # self 可編輯
```

推導邏輯：
- `field_restrictions.{role}: none` → 該角色可寫入所有欄位
- `field_restrictions.{role}: [field_list]` → 標記為**禁止寫入**的欄位（仍可讀取）
- haAPI `require_mfa: true` → PDL `security.sensitive_operations.require_mfa`

---

## 佈局與樣式

（同 v1.0，無變更）

---

## 狀態管理 ⭐ NEW

### state 配置

haPDL 的 `state` 區塊展開為以下 PDL 結構：

```yaml
state:
  local:
    - name: isEditing
      type: boolean
      default: false

    - name: selectedItems
      type: "array<string>"
      default: []
      max_length: 100

    - name: filterCriteria
      type: object
      schema:
        keyword: string
        status: "enum[active, inactive, all]"
        dateRange: DateRange
      default:
        status: all

    # 衍生狀態
    - name: hasSelection
      derived: "selectedItems.length > 0"

    # UI 狀態
    - name: expandedRows
      type: "set<string>"
      scope: ui

  shared:
    - name: currentWorkspace
      type: Workspace
      scope: session
      description: "當前工作區"

    - name: userPreferences
      type: UserPreferences
      scope: user
      sync: true

    - name: orderDraft
      type: Order
      scope: workflow
      workflow_id: create-order
      ttl: 3600

  cascading:
    # 基本連動
    - trigger: city
      target: district
      source: "api:/regions?city_id={city.id}"
      loading_text: "載入區域中..."
      error_text: "無法載入區域資料"
      clear_on_change: true

    # 多層連動
    - trigger: category
      targets:
        - field: subcategory
          source: "api:/subcategories?parent={category.id}"
          clear_on_change: true
        - field: product
          source: "api:/products?subcategory={subcategory.id}"
          depends_on: subcategory
          clear_on_change: true

    # 計算連動
    - triggers: [quantity, unit_price]
      target: subtotal
      compute: "quantity * unit_price"
      immediate: true

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

    # 驗證連動
    - trigger: start_date
      target: end_date
      validation:
        rule: "end_date > start_date"
        message: "結束日期必須晚於開始日期"

  persistence:
    filters:
      storage: sessionStorage
      key: "{page}-filters"
      include: [status, dateRange, keyword]
      ttl: 86400
    pagination:
      storage: localStorage
      key: "user-pagination-prefs"
    sorting:
      storage: sessionStorage
    expanded:
      storage: sessionStorage
      key: "{page}-expanded"
    custom:
      - state: selectedView
        storage: localStorage
      - state: draftData
        storage: indexedDB
        encrypt: true
        compress: true

  computed:
    - name: totalAmount
      expression: "items.reduce((sum, item) => sum + item.subtotal, 0)"
      dependencies: [items]

    - name: formattedTotal
      expression: "formatCurrency(totalAmount, 'TWD')"
      dependencies: [totalAmount]

    # 非同步計算
    - name: shippingFee
      async: true
      expression: "api:/shipping/calculate?total={totalAmount}&zip={zipCode}"
      dependencies: [totalAmount, zipCode]
      debounce: 500
      cache: true

  watchers:
    - watch: status
      handler: onStatusChange
      immediate: false

    - watch: formData
      handler: onFormDataChange
      deep: true

    - watch: searchKeyword
      handler: performSearch
      debounce: 300

    - watch: scrollPosition
      handler: loadMoreItems
      throttle: 100
```

---

## 錯誤處理 ⭐ NEW

### error_handling 配置

haPDL 的 `error_handling` 區塊展開為以下 PDL 結構：

```yaml
error_handling:
  source: user-management.haapi.yaml   # ⭐ v3.1: 引用 haAPI 錯誤模型（自動生成 status_handlers）
  validation:
    display:
      mode: inline              # inline | summary | toast | modal
      position: below           # above | below | right
      scroll_to_first: true
      highlight_field: true
      highlight_style: border   # border | background | icon
    timing:
      on_blur: true
      on_change: false
      on_submit: true
      debounce: 300
    messages:
      required: "{field} 為必填欄位"
      email: "請輸入有效的電子郵件地址"
      min: "{field} 不得小於 {min}"
      max: "{field} 不得大於 {max}"
      minLength: "{field} 至少需要 {minLength} 個字元"
      maxLength: "{field} 不得超過 {maxLength} 個字元"
      pattern: "{field} 格式不正確"
      unique: "{field} 已存在"
      custom: "{message}"
    summary:
      enabled: true
      position: top
      title: "請修正以下錯誤："
      max_display: 5
      show_count: true

  api:
    status_handlers:
      400: { type: validation, action: map_to_fields, fallback_message: "請求資料格式錯誤" }
      401: { type: authentication, action: redirect, target: "/login", preserve_return_url: true }
      403: { type: authorization, action: display, display_mode: modal, message: "您沒有權限" }
      404: { type: not_found, action: display, display_mode: inline, show_back_button: true }
      409:
        type: conflict
        action: display
        display_mode: modal
        message: "資料已被修改，請重新載入"
        actions:
          - { label: "重新載入", action: reload }
          - { label: "保留我的變更", action: force_save }
      422: { type: validation, action: map_to_fields, field_mapping: { source: "errors", field_key: "field", message_key: "message" } }
      429: { type: rate_limit, action: display, display_mode: toast, retry_after: true }
      500: { type: server_error, action: display, display_mode: modal, show_error_id: true }
      503: { type: maintenance, action: display, display_mode: fullscreen, show_status_page: true }

    # 外部服務錯誤處理 ⭐ v3.2
    # 當 haAPI ext.* step 的 on_fail 觸發時，轉換器自動產生對應的 status_handler
    # 例如 haAPI 定義：
    #   - action: ext.smtp.send_email
    #     on_fail: { status: 502, message: "寄信失敗" }
    # 會自動合併到 502 處理器中：
    external_service_errors:
      enabled: true                       # 啟用外部服務錯誤的特殊處理
      default_handler:
        type: external_service_error
        action: display
        display_mode: toast
        message: "外部服務暫時無法使用"
        retry_available: true             # 若 haAPI 有 resilience retry 設定
      # 可按服務覆蓋（從 haAPI integrations + on_fail 推導）：
      by_service:
        smtp:
          message: "郵件服務暫時無法使用，請稍後再試"
          retry_available: true
        captcha:
          message: "驗證碼服務無法連線"
          retry_available: false           # captcha 通常不適合自動重試

    reporting:
      enabled: true
      endpoint: "/api/error-reports"
      include: [error_id, timestamp, user_id, page_url, action]
      exclude: [password, token, credit_card]

  network:
    timeout:
      duration: 30000
      message: "連線逾時"
      action: retry_prompt
    retry:
      enabled: true
      max_attempts: 3
      strategy: exponential
      base_delay: 1000
      max_delay: 30000
      jitter: true
      retryable_methods: [GET, PUT, DELETE]
      retryable_status: [408, 429, 500, 502, 503, 504]
    offline:
      detection: { method: navigator }
      mode: queue
      indicator:
        enabled: true
        position: top
        message: "目前處於離線狀態"
        show_queue_count: true
      queue:
        storage: indexedDB
        max_size: 100
        max_age: 86400
      cache:
        enabled: true
        strategy: stale-while-revalidate
        ttl: 3600
      recovery:
        auto_sync: true
        sync_order: fifo
        conflict_resolution: server_wins
        notify_on_complete: true

  business:
    errors:
      INSUFFICIENT_STOCK:
        message: "庫存不足，目前剩餘 {available} 件"
        display: inline
        field: quantity
        severity: warning
        actions:
          - { label: "調整數量", action: set_max_available }
      DUPLICATE_ORDER:
        message: "偵測到重複訂單，是否繼續？"
        display: modal
        severity: warning
        actions:
          - { label: "檢視既有訂單", action: navigate, target: "/orders/{existing_order_id}" }
          - { label: "仍要建立", action: continue, confirm: true }
    severity_styles:
      info: { icon: info-circle, color: blue, duration: 3000 }
      warning: { icon: alert-triangle, color: orange, duration: 5000 }
      error: { icon: x-circle, color: red, duration: null }
      critical: { icon: alert-octagon, color: red, blocking: true }

  boundary:
    page:
      enabled: true
      fallback: { type: error_page, title: "頁面載入失敗", actions: [{label: "重新載入", action: reload}] }
      tracking: { enabled: true, service: sentry, sample_rate: 1.0 }
    section:
      enabled: true
      fallback: { type: inline_error, show_retry: true }
    component:
      enabled: true
      fallback: { type: placeholder, show_error_icon: true }
```

---

## 非同步行為 ⭐ NEW

### async 配置

```yaml
async:
  fetching:
    default:
      strategy: cache-first     # cache-first | network-first | stale-while-revalidate
      stale_time: 30000
      cache_time: 300000
    on_mount:
      parallel: true
      timeout: 10000
      retry: 2
    background_refresh:
      enabled: true
      interval: 60000
      when_visible: true
      when_focused: true
    prefetch:
      enabled: true
      triggers:
        - { on: hover_link, delay: 200 }
        - { on: near_viewport, threshold: "200px" }

  mutations:
    optimistic:
      enabled: true
      rules:
        - action: toggle_status
          optimistic: true
          rollback_on_error: true
        - action: delete
          optimistic: true
          undo: { enabled: true, duration: 5000, message: "已刪除 {name}", action_label: "復原" }
    queue:
      enabled: true
      strategy: sequential
      batch: { enabled: true, max_size: 10, max_wait: 2000 }
    conflict:
      detection: version
      version_field: _version
      resolution: { mode: prompt, merge_strategy: field_level }

  loading:
    global:
      enabled: true
      delay: 200
      minimum: 500
    zones:
      page: { type: skeleton, count: 5 }
      table: { type: skeleton, rows: 10 }
      form: { type: overlay, opacity: 0.5, spinner: true }
      button: { type: spinner, disable: true, text: "處理中..." }
      inline: { type: spinner, size: small }
    indicators:
      spinner: { type: circular, size: medium, color: primary }
      skeleton: { animation: wave, color: "#e0e0e0", highlight: "#f5f5f5" }
      progress: { type: linear, indeterminate: true, color: primary }

  request_control:
    debounce: { search: 300, filter: 500, auto_save: 2000 }
    throttle: { scroll: 100, resize: 200 }
    cancellation:
      on_unmount: true
      on_navigation: true
      on_new_request: true
    concurrency: { max_parallel: 6, queue_overflow: wait }
    deduplication: { enabled: true, window: 1000 }

  caching:
    layers:
      - { type: memory, max_size: 100, ttl: 60000 }
      - { type: sessionStorage, max_size: "5MB", ttl: 3600000 }
      - { type: indexedDB, max_size: "50MB", ttl: 86400000 }
    rules:
      - { pattern: "/api/*/list", strategy: stale-while-revalidate, stale_time: 30000 }
      - { pattern: "/api/*/:id", strategy: cache-first, ttl: 60000 }
      - { pattern: "/api/options/*", strategy: cache-first, ttl: 3600000 }
    invalidation:
      manual:
        - { trigger: "mutation:create", invalidate: ["list", "count"] }
        - { trigger: "mutation:update", invalidate: ["detail:{id}", "list"] }
        - { trigger: "mutation:delete", invalidate: ["list", "count"] }
      auto: { on_focus: false, on_reconnect: true }
```

---

## 無障礙存取 ⭐ NEW

### accessibility 配置

```yaml
accessibility:
  semantics:
    page:
      main_landmark: true
      navigation_landmark: true
      search_landmark: true
    headings:
      page_title: h1
      section_title: h2
      subsection_title: h3
      auto_increment: true
    table: { caption: true, scope: true }
    form: { fieldset_grouping: true, legend: true, label_association: true }

  aria:
    auto_labels:
      enabled: true
      regions:
        table: "資料列表"
        filters: "篩選條件"
        pagination: "分頁導覽"
        form: "資料表單"
        actions: "操作按鈕"
      states:
        loading: "載入中"
        empty: "無資料"
        error: "發生錯誤"
    live_regions:
      - { id: notification-area, aria-live: polite, aria-atomic: true }
      - { id: error-summary, aria-live: assertive, aria-atomic: true }

  keyboard:
    enabled: true
    focus:
      visible: true
      trap_in_modal: true
      restore_on_close: true
      skip_links: true
    focus_indicator:
      style: outline
      color: "#005fcc"
      width: 2px
      offset: 2px
    shortcuts:
      global:
        - { key: "/", action: focus_search, description: "聚焦搜尋框" }
        - { key: "?", action: show_shortcuts, description: "顯示快捷鍵" }
        - { key: "Escape", action: close_modal, description: "關閉對話框" }
      list:
        - { key: "ctrl+n", action: create, description: "新增" }
        - { key: "j", action: next_row, description: "下一列" }
        - { key: "k", action: prev_row, description: "上一列" }
      form:
        - { key: "ctrl+s", action: save, description: "儲存" }
        - { key: "ctrl+Enter", action: submit, description: "送出表單" }
      table_navigation:
        enabled: true
        arrow_keys: true
        home_end: true
        page_up_down: true
    hints:
      enabled: true
      show_on: hold_alt
      position: tooltip

  screen_reader:
    announcements:
      data_loaded: "已載入 {count} 筆 {entity} 資料"
      data_loading: "正在載入資料"
      data_empty: "沒有符合條件的資料"
      action_complete: "{action} 成功"
      action_failed: "{action} 失敗：{error}"
      filter_applied: "已套用篩選，顯示 {count} 筆資料"
      sorted: "已依 {field} {direction}排序"
      page_changed: "第 {page} 頁，共 {total} 頁"
      validation_error: "表單驗證失敗，{count} 個錯誤"
    priority: { error: assertive, success: polite, info: polite }
    timing: { delay: 100, debounce: 500 }

  visual:
    high_contrast: { enabled: true, auto_detect: true, toggle_shortcut: "ctrl+alt+h" }
    text_scaling: { enabled: true, min_scale: 1.0, max_scale: 2.0, respect_browser: true }
    reduced_motion: { enabled: true, auto_detect: true }
    color:
      non_color_indicators: true
      colorblind_friendly: true
      contrast_ratio: { text: 4.5, large_text: 3.0, ui_components: 3.0 }
    error_indicators: { icon: true, border: true, text: true, color_only: false }

  compliance:
    level: AA
    standard: WCAG21
    additional: [Section508]
    validation: { enabled: true, on_build: true, fail_on_error: true }
```

---

## 安全性 ⭐ NEW

### security 配置

> ⭐ v3.1 新增：`sensitive` 映射鏈說明。DBML `sensitive: true` 與 haPDL `fieldName*` 符號聯集判定，
> 任一來源標記即自動納入 `security.field_level.masking`。合併規則：
>
> ```
> sensitive 判定 = DBML sensitive: true  ∪  haPDL fieldName* 符號
>                  ↓
>                  PDL security.field_level.masking 自動包含此欄位
> ```
>
> - DBML 標了 `sensitive: true`，haPDL 未標 `*` → **仍自動遮罩**
> - DBML 未標，haPDL 標了 `*` → **仍自動遮罩**
> - 兩者都標了 → **合併，以 haPDL 的遮罩模式為準**

```yaml
security:
  field_level:
    masking:
      - field: phone
        pattern: "###-###-{last4}"
        unmask_permission: [admin, owner]
        unmask_action: click
        log_unmask: true
      - field: email
        pattern: "{first2}***@{domain}"
        unmask_permission: [admin]
      - field: credit_card
        pattern: "****-****-****-{last4}"
        unmask_permission: []
    encryption:
      - { field: ssn, algorithm: AES-256-GCM, key_source: vault }
    access_control:
      - { field: internal_notes, read: [internal_staff], write: [manager, admin] }
      - { field: cost_price, read: [finance, admin], write: [finance_manager] }

  data_isolation:
    mode: tenant
    scope_field: organization_id
    rules:
      tenant: { field: tenant_id, auto_filter: true, auto_set: true, immutable: true }
      department: { field: department_id, hierarchy: true }
      owner: { field: created_by, share: { enabled: true, field: shared_with, max_shares: 10 } }
    exceptions:
      - { role: super_admin, bypass: all, audit: true }

  sensitive_operations:
    require_mfa:
      - { action: delete_user, mfa_type: [totp, sms] }
      - { action: export_all, mfa_type: [totp], cooldown: 3600 }
    require_confirmation:
      - { action: delete, type: dialog, message: "確定要刪除 {name} 嗎？" }
      - { action: bulk_delete, type: dialog, require_input: true, input_match: "DELETE" }
    require_approval:
      - { action: large_order, condition: "amount > 100000", approvers: [manager, finance], approval_type: any }
    rate_limits:
      - { action: login_attempt, limit: 5, window: 300, lockout: 900 }
      - { action: api_call, limit: 100, window: 60, by: user }

  input_protection:
    xss: { enabled: true, mode: strict, sanitize_html: true, allowed_tags: [b, i, u, a, p, br] }
    sql_injection: { enabled: true, parameterized_only: true }
    csrf: { enabled: true, token_field: _csrf_token, header_name: X-CSRF-Token }
    file_upload:
      allowed_types:
        - { mime: "image/*", extensions: [jpg, jpeg, png, gif, webp] }
        - { mime: "application/pdf", extensions: [pdf] }
      blocked_types:
        - { extensions: [exe, bat, cmd, sh, php, js] }
      scanning: { enabled: true, service: clamav }
      max_size: 10MB
    max_lengths: { default: 1000, text_area: 10000, search: 200, email: 254, url: 2048 }

  audit:
    enabled: true
    level: detailed
    operations:
      - { type: create, entities: all, fields: all }
      - { type: update, entities: all, fields: changed }
      - { type: delete, entities: all, fields: all }
      - { type: login, success: true, failure: true }
    record: [timestamp, user_id, user_name, ip_address, action, entity, entity_id, changes, request_id]
    sensitive_handling: { mode: hash, fields: [password, credit_card, ssn] }
    storage: { type: separate_db, retention: 2555, encryption: true }
    alerts:
      - { condition: "failed_login_count > 5", channel: [email, slack], severity: warning }
      - { condition: "bulk_delete_count > 100", channel: [email, slack, pager], severity: critical }
```

---

## 複雜表單 ⭐ NEW

### dynamic_sections 配置

```yaml
form:
  dynamic_sections:
    - section: business_info
      visible_when: "customer_type == 'business'"
      fields:
        - { field: company_name, label: "公司名稱", input: text, required: true }
        - { field: tax_id, label: "統一編號", input: text, required: true }
    - section: individual_info
      visible_when: "customer_type == 'individual'"
      fields:
        - { field: id_number, label: "身分證字號", input: text }
        - { field: birth_date, label: "出生日期", input: date }
    - section: shipping_info
      visible_when: "delivery_method == 'shipping'"
      required_when: "delivery_method == 'shipping'"
      fields:
        - { field: shipping_address, label: "收件地址", input: text, required: true }
        - { field: recipient_name, label: "收件人", input: text, required: true }

  conditional_fields:
    - { field: other_reason, visible_when: "reason == 'other'", required_when: "reason == 'other'" }
```

### repeatable 配置

```yaml
form:
  repeatable:
    - name: contacts
      label: "聯絡人"
      min: 1
      max: 5
      default_count: 1
      fields:
        - { name: name, type: text, required: true, placeholder: "姓名" }
        - { name: phone, type: tel, required: true, placeholder: "電話" }
        - { name: email, type: email, required: false }
        - { name: is_primary, type: radio_in_group, label: "主要聯絡人" }
      ui:
        layout: card
        add_label: "新增聯絡人"
        remove_label: "移除"
        sortable: true
      validation:
        - rule: "items.filter(c => c.is_primary).length === 1"
          message: "請指定一位主要聯絡人"

    - name: order_items
      label: "訂單項目"
      min: 1
      max: 50
      fields:
        - { name: product, type: autocomplete, source: "api:/products", required: true, width: "30%" }
        - { name: quantity, type: number, required: true, min: 1, width: "15%" }
        - { name: unit_price, type: currency, readonly: true, width: "20%" }
        - { name: discount, type: percent, default: 0, max: 50, width: "15%" }
        - { name: subtotal, type: currency, computed: "quantity * unit_price * (1 - discount / 100)", readonly: true, width: "20%" }
      ui:
        layout: table
        add_label: "新增項目"
        show_row_number: true
      summary:
        - { field: subtotal, aggregation: sum, label: "小計" }
        - { field: quantity, aggregation: sum, label: "總數量" }
```

### form_state 配置

```yaml
form:
  state:
    dirty_check:
      enabled: true
      prompt_on_leave: true
      message: "您有未儲存的變更，確定要離開嗎？"
      exclude_fields: [_csrf_token]
    auto_save:
      enabled: true
      delay: 5000
      storage: localStorage
      key: "draft-{page}-{id}"
      max_age: 86400
      exclude_fields: [password, credit_card]
      notify: true
    draft_recovery:
      enabled: true
      prompt: true
      message: "偵測到未完成的草稿，是否恢復？"
    step_memory:
      enabled: true
      persist: sessionStorage
    reset:
      confirm: true
      message: "確定要清除所有輸入嗎？"
      preserve: [entity_id]
```

---

## 檔案處理 ⭐ NEW

### file_handling 配置

```yaml
file_handling:
  upload:
    mode: single                # single | multiple | directory
    accept: [".pdf", ".docx", "image/*"]
    max_size: 10MB
    max_files: 20
    max_total_size: 100MB
    chunked:
      enabled: true
      chunk_size: 2MB
      parallel: 3
      retry: 3
      resume: true
    preprocessing:
      images:
        resize: { enabled: true, max_width: 1920, max_height: 1080, quality: 0.85 }
        compress: { enabled: true, max_size: 1MB }
        format_convert: { heic_to: jpg }
      documents:
        virus_scan: true
    progress:
      display: individual       # individual | combined | both
      show_speed: true
      show_remaining: true
    drag_drop:
      enabled: true
      zone_selector: ".upload-zone"
      highlight_class: "drag-over"
    queue:
      enabled: true
      auto_start: true
      max_concurrent: 3
      retry_failed: true

  preview:
    images: { enabled: true, thumbnail_size: "100x100", lightbox: true, zoom: true, rotate: true }
    documents:
      pdf: { enabled: true, renderer: pdfjs, max_pages: 50 }
      office: { enabled: true, service: office_online }
      text: { enabled: true, max_size: 1MB, syntax_highlight: true }
    videos: { enabled: true, thumbnail: true, player: native, autoplay: false }
    audio: { enabled: true, player: native, waveform: true }

  management:
    metadata:
      show: [name, size, type, created_at, uploaded_by]
      editable: [name, description, tags]
    operations:
      download: { enabled: true, direct: false, log: true }
      rename: { enabled: true, validation: "^[a-zA-Z0-9_.-]+$" }
      delete: { enabled: true, confirm: true, soft_delete: true }
      share: { enabled: true, expiry_options: [1h, 24h, 7d, 30d, never], password_protect: true }
    versioning:
      enabled: true
      max_versions: 10
      auto_version: true
      diff_view: true
```

---

## 測試性 ⭐ NEW

### testing 配置

（haPDL v3.0 規格中此區塊尚在規劃，以下為 PDL 層的預留結構）

```yaml
testing:
  # 選擇器策略
  selectors:
    strategy: data-testid       # data-testid | id | class | role
    prefix: ""
    auto_generate: true         # 自動為所有互動元素產生 data-testid
    naming:
      page: "{page-id}"
      field: "{page-id}-{field-name}"
      action: "{page-id}-{action-id}"
      table_row: "{page-id}-row-{index}"
      table_cell: "{page-id}-row-{index}-{column}"

  # Mock 資料
  mock_data:
    enabled: true
    generator: faker             # faker | custom
    seed: 12345                  # 固定種子確保可重現
    rules:
      - field_pattern: "*_name"
        generator: "faker.name"
      - field_pattern: "*_email"
        generator: "faker.email"
      - field_pattern: "*_at"
        generator: "faker.date.recent"
      - field_pattern: "status"
        generator: "faker.random.arrayElement"
        params: ["active", "inactive", "pending"]
    fixtures:
      - entity: User
        file: "fixtures/users.json"
        count: 50

  # Gherkin 整合
  gherkin:
    auto_generate: true          # 自動從 PDL 產生 Gherkin 場景
    output_dir: "features/"
    language: zh-TW
    templates:
      list_page:
        - "Given 我在 {title} 頁面"
        - "When 我輸入篩選條件"
        - "Then 列表應顯示符合條件的資料"
      form_page:
        - "Given 我在 {title} 表單"
        - "When 我填寫所有必填欄位並送出"
        - "Then 應顯示成功訊息"

  # E2E 測試提示
  e2e:
    framework: playwright        # playwright | cypress | selenium
    base_url: "http://localhost:3000"
    screenshots:
      on_failure: true
      full_page: false
    video:
      enabled: false
```

---

## TypeScript 型別定義

### 核心介面 (v3.0 擴展)

```typescript
/** 頁面狀態定義 (v3.0) */
export interface PageState {
  id: string
  name: string
  description?: string
  schemaVersion?: '3.0'                   // ⭐ NEW
  mixins?: string[]                       // ⭐ NEW
  data: DataRequirement[]
  actions: UserAction[]
  validations?: ValidationRule[]
  transitions: Transition[]
  layout?: LayoutHint
  state?: StateConfig                     // ⭐ NEW
  errorHandling?: ErrorHandlingConfig     // ⭐ NEW
  async?: AsyncConfig                     // ⭐ NEW
  accessibility?: AccessibilityConfig     // ⭐ NEW
  security?: SecurityConfig               // ⭐ NEW
  fileHandling?: FileHandlingConfig       // ⭐ NEW
  testing?: TestingConfig                 // ⭐ NEW
}

/** 資料需求定義 */
export interface DataRequirement {
  source: 'api' | 'store' | 'route' | 'user-input'
  name: string
  type: string
  endpoint?: string
  required?: boolean
  defaultValue?: any
  transform?: string
}

/** 使用者動作定義 */
export interface UserAction {
  id: string
  label: string
  type: 'button' | 'link' | 'form-submit' | 'gesture'
  permissions?: string[]
  conditions?: Condition[]
  effects: Effect[]
}

/** 動作效果 */
export interface Effect {
  type: 'navigate' | 'api-call' | 'update-store' | 'show-modal' | 'validate'
  target?: string
  payload?: any
  onSuccess?: Effect[]
  onError?: Effect[]
}

/** 狀態轉換 */
export interface Transition {
  from: string
  to: string
  trigger: string
  guards?: Condition[]
}

/** 條件定義 */
export interface Condition {
  type: 'data' | 'permission' | 'time' | 'custom'
  expression: string
  errorMessage?: string
}

/** 驗證規則 (v3.0 擴展) */
export interface ValidationRule {
  field: string
  rules: Array<{
    type: 'required' | 'pattern' | 'range' | 'custom' | 'unique' | 'capacityCheck'
    value?: any
    message: string
  }>
}

/** 跨欄位驗證 ⭐ NEW */
export interface CrossFieldValidation {
  fields: string[]
  rule: string
  message: string
  when?: string
}

/** 版面配置提示 (v3.0 擴展) */
export interface LayoutHint {
  type: 'list' | 'grid' | 'form' | 'dashboard' | 'detail' | 'kanban' | 'calendar'
  responsive?: boolean
  sections?: Array<{
    id: string
    title?: string
    columns?: number
    fields: string[]
  }>
}

// ===== v3.0 新增介面 =====

/** 狀態管理配置 ⭐ NEW */
export interface StateConfig {
  local?: LocalState[]
  shared?: SharedState[]
  cascading?: CascadingRule[]
  persistence?: PersistenceConfig
  computed?: ComputedProperty[]
  watchers?: Watcher[]
}

export interface LocalState {
  name: string
  type: string
  default?: any
  derived?: string
  scope?: 'data' | 'ui'
}

export interface SharedState {
  name: string
  type: string
  scope: 'session' | 'user' | 'workflow' | 'global'
  sync?: boolean
  ttl?: number
}

export interface CascadingRule {
  trigger: string | string[]
  target?: string
  targets?: Array<{ field: string; source: string; depends_on?: string; clear_on_change?: boolean }>
  source?: string
  compute?: string
  conditions?: Array<{ when: string; required?: boolean; visible?: boolean }>
  validation?: { rule: string; message: string }
  clear_on_change?: boolean
  immediate?: boolean
}

export interface ComputedProperty {
  name: string
  expression: string
  dependencies: string[]
  async?: boolean
  debounce?: number
  cache?: boolean
}

export interface Watcher {
  watch: string | string[]
  handler: string
  deep?: boolean
  immediate?: boolean
  condition?: string
  debounce?: number
  throttle?: number
}

/** 錯誤處理配置 ⭐ NEW */
export interface ErrorHandlingConfig {
  validation?: ValidationErrorConfig
  api?: ApiErrorConfig
  network?: NetworkErrorConfig
  business?: BusinessErrorConfig
  boundary?: ErrorBoundaryConfig
}

/** 非同步行為配置 ⭐ NEW */
export interface AsyncConfig {
  fetching?: FetchingConfig
  mutations?: MutationConfig
  loading?: LoadingConfig
  requestControl?: RequestControlConfig
  caching?: CachingConfig
}

/** 無障礙存取配置 ⭐ NEW */
export interface AccessibilityConfig {
  semantics?: SemanticsConfig
  aria?: AriaConfig
  keyboard?: KeyboardConfig
  screenReader?: ScreenReaderConfig
  visual?: VisualConfig
  compliance?: ComplianceConfig
}

/** 安全性配置 ⭐ NEW */
export interface SecurityConfig {
  fieldLevel?: FieldLevelSecurityConfig
  dataIsolation?: DataIsolationConfig
  sensitiveOperations?: SensitiveOpsConfig
  inputProtection?: InputProtectionConfig
  audit?: AuditConfig
}

/** 檔案處理配置 ⭐ NEW */
export interface FileHandlingConfig {
  upload?: UploadConfig
  preview?: PreviewConfig
  management?: FileManagementConfig
}

/** 測試性配置 ⭐ NEW */
export interface TestingConfig {
  selectors?: SelectorConfig
  mockData?: MockDataConfig
  gherkin?: GherkinConfig
  e2e?: E2EConfig
}

/** 使用者流程 */
export interface UserFlow {
  id: string
  name: string
  description: string
  actors: Actor[]
  pages: PageState[]
  globalData?: DataRequirement[]
  errorHandling?: ErrorHandlingConfig    // ⭐ NEW: 流程級錯誤處理
}

/** 角色定義 */
export interface Actor {
  id: string
  name: string
  permissions: string[]
}
```

---

## 完整範例

### 範例 1: v3.0 列表頁（包含新功能）

```yaml
version: 3
page:
  id: user-list
  type: list
  title: "使用者管理"
  route: "/users"
  schema_version: "3.0"
  auth:
    roles: [admin, manager]

  datasource:
    entity: User
    query:
      endpoint: GET /api/users
      params:
        - { name: q, from: filter.keyword }
        - { name: status, from: filter.status }
        - { name: page, from: pager.page }

  filters:
    - { id: keyword, label: "搜尋", input: text, placeholder: "名稱或 Email" }
    - { id: status, label: "狀態", input: select, options: [active, inactive, pending] }
    - { id: created_at, label: "建立時間", input: daterange, operator: between }

  table:
    selectable: true
    columns:
      - { key: id, label: "ID", width: 80, sortable: true }
      - { key: name, label: "名稱", sortable: true, groupable: true }
      - { key: email, label: "Email" }
      - { key: status, label: "狀態", type: badge, width: 100, map: { active: success, inactive: neutral, pending: warning } }
      - { key: created_at, label: "建立時間", type: datetime, format: relative, width: 160, sortable: true }
      - key: actions
        type: row-actions
        actions:
          - { id: view, label: "檢視", route: "/users/:id" }
          - { id: edit, label: "編輯", route: "/users/:id/edit" }
          - { id: delete, label: "刪除", call: "DELETE /api/users/:id", confirm: true }

  pagination: { enabled: true, page_size: 20 }

  # ===== v3.0 新增 =====
  state:
    local:
      - { name: selectedRows, type: "array<string>", default: [] }
    persistence:
      filters: { storage: sessionStorage, key: "user-list-filters" }

  async:
    fetching:
      default: { strategy: stale-while-revalidate, stale_time: 30000 }
      background_refresh: { enabled: true, interval: 60000 }
    loading:
      zones:
        table: { type: skeleton, rows: 10 }

  error_handling:
    api:
      status_handlers:
        401: { type: authentication, action: redirect, target: "/login" }
        500: { type: server_error, action: display, display_mode: toast }

  accessibility:
    keyboard:
      enabled: true
      shortcuts:
        list:
          - { key: "ctrl+n", action: create, description: "新增" }
    screen_reader:
      announcements:
        data_loaded: "已載入 {count} 筆使用者資料"

  security:
    field_level:
      masking:
        - { field: email, pattern: "{first2}***@{domain}", unmask_permission: [admin] }
    audit:
      enabled: true
      operations:
        - { type: read, condition: "is_export" }
```

---

## 附錄

### A. 命名慣例

- **欄位名稱**: `snake_case` (例如: `user_name`, `created_at`)
- **動作 ID**: `kebab-case` (例如: `create-user`, `delete-item`)
- **頁面 ID**: `kebab-case` (例如: `product-list`, `user-detail`)
- **路由**: `kebab-case` (例如: `/products/:id/edit`)

### B. 表達式語法

```
# 比較運算子
==, !=, <, >, <=, >=

# 邏輯運算子
&&, ||, !

# 欄位引用
row.field_name          # 列表行資料
form.field_name         # 表單資料
route.param_name        # 路由參數
store.path.to.value     # 全域狀態
user.role               # 當前使用者

# 函式
@lookup(Entity,id,name) # 查詢資料
@now()                  # 當前時間
@user()                 # 當前使用者
```

### C. 內建圖示

PDL 支援常用圖示名稱 (基於 Feather Icons):

```
plus, minus, edit, trash, eye, download, upload, search, filter
check, x, alert-triangle, alert-circle, info
arrow-left, arrow-right, chevron-left, chevron-right
file, folder, image, file-text
settings, user, users, calendar, clock, mail, phone
```

### D. 顏色值

```
# 語意顏色
primary, secondary, success, warning, danger, info, neutral, gray, muted

# 具體顏色
red, orange, yellow, green, blue, purple, pink

# 自訂
#1890ff, rgb(24, 144, 255), rgba(24, 144, 255, 0.5)
```

### E. haPDL 符號 → PDL 展開對照表 ⭐ NEW

| haPDL 符號 | PDL 展開結果 |
|-----------|-------------|
| `name!` | `{ field: name, required: true }` |
| `name?` (form) | `{ field: name, required: false }` |
| `name?` (filter) | `{ id: name, nullable: true, null_label: "未指定" }` ⭐ v3.1 消歧 |
| `name?` (column) | `{ key: name, hideable: true }` ⭐ v3.1 消歧 |
| `name#` | `{ field: name, readonly: true }` |
| `name*` | `{ field: name, input: password, sensitive: true }` → 同時納入 `security.field_level.masking` |
| `name@` | `{ field: name, input: email, validation: [{rule: email}] }` |
| `name[]` | `{ field: name, input: select, multiple: true }` |
| `name{}` | `{ field: name, input: json_editor }` |
| `name~` (filter) | `{ id: name, operator: contains }` |
| `name~` (form) | `{ field: name, cascading_source: true }` (連動來源) ⭐ v3.1 消歧 |
| `name<~` | `{ field: name, cascading_target: "source_field" }` (連動目標) |
| `name=` | `{ id: name, operator: equals }` |
| `name>` | `{ id: name, operator: greater_than }` |
| `name<` | `{ id: name, operator: less_than }` |
| `name><` | `{ id: name, operator: between, input: daterange }` ⭐ NEW |
| `name^` | `{ key: name, sortable: true }` ⭐ NEW |
| `name&` | `{ key: name, groupable: true }` ⭐ NEW |
| `name:badge` | `{ key: name, type: badge }` |
| `name:image` | `{ key: name, type: image }` |
| `name:map` | `{ key: name, type: map }` ⭐ NEW |
| `name\|date` | `{ key: name, type: datetime, format: date }` |
| `name\|relative` | `{ key: name, type: datetime, format: relative }` ⭐ NEW |
| `name\|compact` | `{ key: name, type: number, format: compact }` ⭐ NEW |
| `name\|mask(...)` | `{ key: name, format: mask, mask_pattern: "..." }` ⭐ NEW |

> **`?` 符號消歧規則**（v3.1）：轉換器根據上下文自動判定 `?` 的語意。
> `view.filters` 中 → nullable；`view.columns` 中 → hideable；`form.fields` 中 → optional。

> **DBML `group:` → PDL `section`** 術語對應（v3.1）：DBML 的 `group:` 標註表示「領域結構分組」，
> 轉換器自動展開為 PDL 的 `form.sections`（「UI 表單分區」）。

### F. events 事件訂閱（P2 預留）⭐ v3.1

> ⚠️ **此區塊為 P2 預留設計**，尚未納入正式語法。待 WebSocket / SSE 整合方案確定後再正式定義。

```yaml
# PDL events 區塊（草案）
events:
  subscribe:
    - event: user.created          # 來自 haAPI consumers.events
      action: refresh_list         # 前端行為：重新整理列表
      transport: websocket         # 傳輸方式
    - event: user.updated
      action: update_item          # 前端行為：更新單筆資料
      transport: sse
```

### G. Resolution Order 參考 ⭐ v3.1 · 更新 v3.2

當多個來源同時提供同一屬性時，按以下優先順序解析（左高右低）：

```
① DBML 明確標註 → ② haAPI 定義 → ③ haPDL 符號/配置 → ④ Convention 推斷 → ⑤ 預設值
```

完整查找矩陣請參考 `haPDL-specification-v3.2.md` 附錄 C。

> ⭐ **v3.2 新增**：Resilience（timeout/retry）屬性為 haAPI 專屬，採三層級聯解析（Step → API `advanced.external_resilience` → `codegen.config.yaml` → 框架內建預設），haPDL/PDL 不直接參與。

---

## 參考資料

- **haPDL-specification-v3.2.md** - haPDL v3.2 完整語法規格（haAPI v3.2 對齊版）
- **haAPI-specification_v3.2.md** - haAPI v3.2 高階 API 規格（ext.* 命名空間、proxy、integrations、resilience 級聯）
- **annotated_DBML-v3.2.md** - Annotated DBML v3.2 標註規格
- **pdl-syntax.md** - PDL v1.0 語法規格（本文件前身）
- **QUICK-REFERENCE.md** - 快速參考指南
- **DSL-DESIGN-GUIDE.md** - 設計指南
- **IMPLEMENTATION-GUIDE.md** - 實作指南

---

**文件維護者**: WA-RAPTor 團隊
**最後更新**: 2026-04-02
**版本**: 3.2

---

## TODO（待辦事項）

### [2026-04-23] `validation` 規則需支援條件式豁免（選填欄位空值跳過）

**來源**：`ccwLog/0423-UiTest_UserEdit-password.md`（密碼選填欄位驗證豁免問題）

**議題**：
目前 PDL 的 `validation` 陣列規則（`minLength`、`pattern`、`match` 等）無條件觸發，當欄位設 `required: false` + `validation.minLength: 12` 時，語義相互矛盾：允許空值，但空值必然違反 `minLength`。PDL schema 未提供 `condition` / `skipIfEmpty` 屬性表達「僅在有值時驗證」。

**行動項**：
- [ ] 在 `validation` 陣列每條規則新增可選屬性 `condition: not_empty`（或 `skipIfEmpty: true`），範例：
  ```yaml
  validation:
    - rule: minLength
      value: 12
      condition: not_empty  # 僅在有值時驗證
    - rule: pattern
      value: '^(?=.*[0-9]).{12,}$'
      condition: not_empty
  ```
- [ ] 定義語義：`condition: not_empty` ⇔ 空字串/undefined/null 時短路通過（不觸發錯誤訊息）
- [ ] 可選：若 `required: false` 則預設套用 `condition: not_empty`（隱式豁免）；`required: true` 則顯式寫 `condition: always`
- [ ] 更新 PDL schema（JSON Schema + Zod 驗證）
- [ ] 更新 Pdl2whyVue 的 field-mapper 讀取 `condition` 屬性生成對應 Vuetify rule（目前已用 `f.required` 做隱式豁免，等 schema 擴充後改為顯式）
- [ ] 與 haPDL `*?` + validation、haAPI `field_overrides.skip_if_empty` 命名對齊

**優先度**：P1（PDL 是下游 codegen 直接讀取的規格，語義必須明確）
