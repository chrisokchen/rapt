# haPDL → PDL 轉換器規格書 (haPDL2PDL Translator Specification) v3.3

**版本**: v3.3.0 (Release Candidate, 2026-05-13)
**前版**: v3.2.1（見 `archive/haPDL2PDLspec-v3.2.md`）
**整合來源**: Gemini 版、Opus 版、antiOpus 版
**適用範圍**: haPDL v3.3 → PDL v3.3
**參照規格**:
- `haPDL-specification-v3.2.md` (haPDL 主規格)
- `haPDL-page-type-defaults-v3.2.1.md` (Defaults 規格)
- `pdl-syntax-v3.2.md` (PDL 目標格式)
- `whyVueArch.md` (whyVue 目標框架參考；本規格不涉及框架細節)

---

## 目錄

1. [系統架構與定位](#1-系統架構與定位)
2. [輸入與輸出](#2-輸入與輸出)
3. [轉換管線 — 六階段處理](#3-轉換管線--六階段處理)
4. [錯誤與警告代碼表](#4-錯誤與警告代碼表)
5. [特殊頁面處理策略](#5-特殊頁面處理策略)
6. [Deep Merge 語意規格](#6-deep-merge-語意規格)
7. [Entity 名稱轉換規則](#7-entity-名稱轉換規則)
8. [內部資料結構定義](#8-內部資料結構定義)
9. [端到端轉換範例](#9-端到端轉換範例)
10. [測試與驗收策略](#10-測試與驗收策略)

---

## 1. 系統架構與定位

### 1.1 定位

`haPDL2PDL` 是整個編譯管線的**前端（Frontend）**。唯一職責是**語意展開（Rehydrate）**：讀取高抽象度、依賴推斷機制的 haPDL 檔案，結合外部 SSOT（DBML、haAPI），將其全面補完，輸出**毫無歧義、不包含任何語法糖或隱式推斷**的 PDL 結構。

後續的 `PDL2Vue`、`PDL2React` 等後端轉換器只需讀取 PDL，做純粹的「結構 → 模板」映射，無需處理任何業務規則推導。

### 1.2 架構圖

```
┌──────────────┐     ┌──────────┐     ┌──────────┐
│ .hapdl.yaml  │     │ erm.dbml │     │ .haapi.  │
│ (來源頁面)   │     │ (DBML)   │     │  yaml    │
└──────┬───────┘     └────┬─────┘     └────┬─────┘
       │                  │                 │
       ▼                  ▼                 ▼
  ┌─────────────────────────────────────────────┐
  │           haPDL2PDL Translator              │
  │                                             │
  │   Phase 1: Context Init（上下文初始化）      │
  │   Phase 2: Defaults Merging（預設值合併）    │
  │   Phase 3: Sugar Expansion（語法糖展開）     │
  │   Phase 4: DBML Hydration（DBML 推導）      │
  │   Phase 5: haAPI Hydration（haAPI 推導）     │
  │   Phase 6: User Override & Export（覆寫輸出）│
  │                                             │
  └──────────────────┬──────────────────────────┘
                     │
                     ▼
              ┌──────────────┐
              │  .pdl.yaml   │
              │ (PDL 輸出)   │
              └──────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   [PDL2Vue]    [PDL2React]  [PDL2Xxx]
```

---

## 2. 輸入與輸出

### 2.1 輸入

| 輸入 | 格式 | 必要性 | 說明 |
|------|------|--------|------|
| 來源頁面 | `[page].hapdl.yaml` | **必要** | haPDL v3.2.1 格式 |
| 資料模型 | `erm.dbml` | **必要** | Annotated DBML，含 `label` / `sensitive` / `group` / `ref_code` 標註 |
| API 規格 | `[api-name].haapi.yaml` | **條件必要** | haPDL 有 `api:` 綁定時必須提供 |
| Defaults 規則 | 內建 | 內建 | `haPDL-page-type-defaults-v3.2.1` 編譯進轉換器，不需外部檔案 |

### 2.2 輸出

| 輸出 | 格式 | 說明 |
|------|------|------|
| 展開頁面 | `[page].pdl.yaml` | 嚴格符合 `pdl-syntax-v3.2.md` 結構 |
| 錯誤報告 | stderr / JSON | 帶有來源行號的結構化錯誤訊息 |

### 2.3 CLI 介面

```bash
hapdl convert <file.hapdl.yaml> \
  --dbml <erm.dbml> \
  --haapi-dir <haapi-directory> \
  -o <output.pdl.yaml> \
  [--verbose]    # 輸出每個 Phase 的中間狀態
  [--dry-run]    # 只驗證，不輸出檔案
  [--strict]     # 將 WARN 提升為 ERROR
```

---

## 3. 轉換管線 — 六階段處理

### 覆寫優先級公式

```
最終 PDL = haPDL_明確配置 ⊕ haAPI_推導 ⊕ DBML_推導 ⊕ Convention_展開 ⊕ Page_Type_Defaults ⊕ Global_Defaults
```

> `⊕` = deep merge（左方優先覆寫右方）。即 haPDL 使用者的明確配置擁有**最高覆寫權**。

等效表達：`PDL = (((Convention_Defaults ⊕ DBML) ⊕ haAPI) ⊕ haPDL_User_Config)`

---

### Phase 1: Context Init（上下文初始化）

**輸入**: `.hapdl.yaml` 原始 YAML  
**輸出**: `TranslatorContext` 物件 + PDL 空殼

#### 步驟

**1. 解析 haPDL 頂層欄位**

```yaml
# 從 haPDL 讀取
page: apcat-add        → ctx.page_id = "apcat-add"
type: form             → ctx.page_type = "form"
title: 新增AP分類      → ctx.title = "新增AP分類"
entity: Apcat          → ctx.entity = "Apcat"
api: apcat             → ctx.api_name = "apcat"
schema_version: "3.2.1" → ctx.schema_version = "3.2.1"
```

**2. 載入 DBML Entity**

- 搜尋 `erm.dbml` 中 `Table Apcat { ... }` 定義
- 解析所有欄位定義（name, type, constraints, notes/annotations）
- 解析 Enum 定義（如有 FK 引用）
- 結果存入 `ctx.dbml_context: Map<field_name, DBMLField>`
- 失敗 → `CTX-ERR-001`

**3. 載入 haAPI 規格**（若有 `api:` 綁定）

- 搜尋 `apcat.haapi.yaml`
- 載入 `exposes`/`standard`（CRUD endpoints）
- 載入 `operations`（業務操作 endpoints）
- 載入 `access.permissions`
- 載入 `advanced.validation`（欄位驗證規則）
- 載入 `search.fields`（若有）
- 結果存入 `ctx.haapi_context: HaAPISpec`
- 失敗 → `CTX-ERR-002`

**4. 建立 PDL 空殼**

```yaml
version: 3
page:
  id: "apcat-add"
  type: form
  title: "新增AP分類"
  route: "/apcat/add"           # Convention: /{entity-kebab}/{page-suffix}
  schema_version: "3.2"
  datasource:
    entity: Apcat
    api_ref: apcat              # 從 haPDL api: 映射
```

> **Route Convention**: `page: apcat-add` → suffix = `add` → route = `/{entity-kebab}/add` = `/apcat/add`。
> 若 page id 含複合後綴（如 `user-update`），按 entity 推導：`/{entity-kebab}/update`。
> 特殊頁面（如 `login`）若 page id 不含 entity 字串，route = `/{page-id}`。

---

### Phase 2: Defaults Merging（預設值合併）

**輸入**: `TranslatorContext` + PDL 空殼  
**輸出**: PDL 骨架（含所有預設值）

#### 步驟

**1. 注入 Global Defaults**（所有頁面類型共用）

```yaml
accessibility:
  keyboard:
    enabled: true
testing:
  selectors:
    strategy: data-testid
    auto_generate: true
  mock_data:
    enabled: true
```

**2. 依 `page_type` 注入 Page Type Defaults**

| `page_type` | 載入的 Defaults | 關鍵內容 |
|-------------|----------------|---------|
| `list` | `list_defaults` | pagination (20, [10,20,50,100]), searchable, exportable, selection, state.persistence, async.loading (skeleton, delay=200, minimum=500), error_handling.api (400/409/500) |
| `form` | `form_defaults` | error_handling.validation (inline, below, scroll_to_first, highlight, on_blur, on_submit), error_handling.api (400/409/500), async.submit (button_spinner, disable_form, redirect=`/{entity-kebab}/list`) |
| `detail` | `detail_defaults` | （未來定義） |
| `hybrid` | **無** type-specific defaults | 全部明確配置 |
| 其他 | 僅 Global Defaults | — |

> 完整定義見 `haPDL-page-type-defaults-v3.2.1.md`。

**3. Accessibility aria Convention 推斷**

若 haPDL 未明確定義 `accessibility.aria`，自動產生：

| type | page_label | 第二 label |
|------|-----------|-----------|
| list | `"{title}列表"` | `table_label: "{title}資料列表"` |
| form | `"{title}表單"` | `form_label: "{title}資料填寫"` |
| detail | `"{title}詳情"` | `content_label: "{title}資料內容"` |

例：`title: 新增AP分類, type: form` → `page_label: "新增AP分類表單"`, `form_label: "新增AP分類資料填寫"`

**4. Template 變數替換**

在 Defaults 中的模板變數進行替換：

| 變數 | 來源 | 範例 |
|------|------|------|
| `{page}` | `page_id` | `apcat-add` |
| `{title}` | `title` | `新增AP分類` |
| `{entity}` | `entity_name` | `Apcat` |
| `{entity-kebab}` | CamelCase → kebab（見 §7） | `apcat` |
| `{operation}` | 由 standard/operations 推斷 | `新增` / `編輯` |

例：`state.persistence.filters.key: "{page}-filters"` → `"apcat-add-filters"`

---

### Phase 3: Sugar Expansion（語法糖展開）

**輸入**: PDL 骨架 + haPDL 中的符號化欄位與 actions  
**輸出**: PDL 中的完整欄位物件陣列 + 展開的 actions

#### 3.1 欄位符號解析

掃描 haPDL 的 `view.fields`、`view.columns`、`view.filters`，將符號化字串解析為欄位物件。

**解析策略**：從欄位名稱末尾向前掃描符號，先提取 `:type` 和 `|format`（含括號），再提取尾部修飾符號。

##### 完整符號表

| 符號 | filters | columns | fields (form) |
|------|---------|---------|---------------|
| `!` | — | `emphasis: true` | `required: true` |
| `?` | `nullable: true, null_label: "未指定"` | `hideable: true` | `required: false`（顯式選填） |
| `#` | — | — | `readonly: true` |
| `*` | — | — | `input: password, sensitive: true` → 加入 `security.field_level.masking` |
| `@` | — | — | `input: email` + email 驗證規則 |
| `[]` | `operator: in, input: multiselect` | — | `input: select, multiple: true` |
| `{}` | — | — | `input: json_editor` |
| `~` | `operator: contains` | — | `cascading_source: true` |
| `<~` | — | — | `cascading_target: "{source_field}"` |
| `=` | `operator: equals` | — | — |
| `>` | `operator: greater_than` | — | — |
| `<` | `operator: less_than` | — | — |
| `><` | `operator: between, input: daterange` | — | — |
| `^` | — | `sortable: true` | — |
| `&` | — | `groupable: true` | — |
| `:type` | — | `type: {type}` | — |
| `\|format` | — | 依 format 設定顯示格式 | — |

##### 多符號組合範例

符號可以組合使用：

```
password*!    → field: password, input: password, sensitive: true, required: true
userId!^      → key: userId, emphasis: true, sortable: true        (columns 上下文)
email@!       → field: email, input: email, required: true, validation: [{rule: email}]
lastVisit|datetime^  → key: lastVisit, format: datetime, sortable: true
xsNewWindow:badge    → key: xsNewWindow, type: badge
ugrpId[]!     → field: ugrpId, input: select, multiple: true, required: true
```

##### `keyword` 虛擬 filter 展開

`keyword` 是保留名稱，不對應實體欄位：

```yaml
# haPDL 輸入
filters:
  - keyword~

# Phase 3 中間結果
filters:
  - id: keyword
    label: "搜尋"
    input: text
    operator: contains
    placeholder: "請輸入關鍵字"
    _pending_search_fields: true   # 標記：等待 Phase 5 haAPI 補全
```

補全邏輯（Phase 5 執行）：
1. 若 haAPI 存在 `search.fields: [f1, f2, ...]` → 設定 `search_fields: [f1, f2, ...]`
2. 若 haAPI 無 `search.fields` → 掃描 DBML 中 entity 的所有 text 型別欄位作為 `search_fields`
3. 清除 `_pending_search_fields` 標記

#### 3.2 actions.standard 展開

##### list 頁面

`standard: [create, edit, delete, export]` 展開為：

```yaml
actions:
  - id: create
    label: "新增"
    icon: plus
    route: /{entity-kebab}/add
    placement: header
  - id: edit
    label: "編輯"
    icon: pencil
    route: /{entity-kebab}/edit/{id}
    placement: row
  - id: delete
    label: "刪除"
    icon: trash
    variant: danger
    confirm: "確定要刪除嗎？"
    placement: row
  - id: export
    label: "匯出"
    icon: download
    placement: header
```

##### form 頁面

`standard: [create]` 展開為三按鈕組：

```yaml
actions:
  primary:
    - id: save
      label: "新增儲存"
      type: submit
      variant: primary
      effects:
        - type: api-call
          target: submit              # 對應 async.mutations.submit
  secondary:
    - id: reset
      label: "清除重填"
      type: reset
      variant: secondary
      effects:
        - type: update-store
          target: form
          payload: reset
    - id: cancel
      label: "返回"
      type: navigate
      route: /{entity-kebab}/list     # Convention 推斷
```

`standard: [update]` 展開為：

| 按鈕 | label | type | variant |
|------|-------|------|---------|
| save | "儲存" | submit | primary |
| reset | "還原" | reset | secondary |
| cancel | "返回" | navigate | — |

##### 物件格式的 standard（直接透傳）

若 `actions.standard` 不是簡單陣列而是**物件陣列**（如 login 頁面），直接透傳為 PDL actions，**不做 Convention 展開**：

```yaml
# haPDL — 物件格式
actions:
  standard:
    - name: login
      label: 登入
      type: submit
      variant: primary

# → PDL 直接透傳
```

同理，若 `actions.standard` 是含 `enabled`/`label`/`route` 等屬性的物件（如 apList），也視為使用者明確配置，展開後以使用者值覆寫 Convention：

```yaml
# haPDL — 物件格式帶屬性
actions:
  standard:
    create:
      enabled: true
      label: 新增AP
      route: /ap/add

# → 展開 create action，但 label/route 使用使用者指定值
```

##### actions.custom 覆寫 standard

若 `actions.custom` 中定義了與 standard 同名的按鈕（如自訂 `cancel.route`），custom 優先覆寫 standard 的 Convention 推斷值。

#### 3.3 actions.operations 展開

將 haPDL `operations: [op1, op2]` 映射到 haAPI 操作定義：

```
operations: [batch-update-group]
  → 從 haapi_context 查找 operation 定義
  → 提取 endpoint, method
  → 寫入 PDL actions 對應項目（或供 Phase 5 端點推導使用）
```

#### 3.4 placement 展開

若 haPDL 定義了 `actions.placement`：

```yaml
placement:
  header: [create, export]     → PDL header.actions
  row: [edit, delete]          → PDL table.columns[type=row-actions].actions
  batch: [delete]              → PDL bulk_actions
```

---

### Phase 4: DBML Hydration（DBML 推導）

**輸入**: 欄位物件陣列 + DBML Entity 定義  
**輸出**: 欄位物件，補充 DBML 來源的屬性

#### 對每個欄位執行：

**1. 類型推導**（`input` 未被 Phase 3 指定時）

| DBML 類型 | PDL input (form) | PDL column type (list) | 附加屬性 |
|----------|-------------------|----------------------|---------|
| `nvarchar(N)` / `varchar(N)` | `text` | `text` | `maxLength: N` |
| `int` / `bigint` | `number` | `number` | `step: 1` |
| `decimal(P,S)` / `numeric` | `number` | `number` | `step: 10^-S` |
| `bit` / `boolean` | `switch` | `toggle` | — |
| `datetime` / `datetime2` | `datetime` | `datetime` | — |
| `date` | `date` | `date` | — |
| `text` / `ntext` | `textarea` | `text` | — |
| `tinyint` | `number` | `number` | Convention: `min: 0, max: 255` |

> Phase 3 已設定的 `input`（如 `*` → `password`、`@` → `email`）不被覆寫。

**2. 約束推導**

| DBML 約束 | PDL 屬性 | 覆寫規則 |
|-----------|---------|---------|
| `[not null]` | `required: true` | 除非 Phase 3 因 `?` 已設為 false |
| `[pk]` | `required: true, unique: true` | — |
| `[unique]` | `unique: true` | — |
| `[default: X]` | `default: X` | — |
| `nvarchar(N)` | `maxLength: N` | — |

**3. Annotated DBML 標註推導** (v3.1)

| DBML Note 語法 | PDL 屬性 |
|---------------|---------|
| `[note: 'label:AP分類編號']` | `label: "AP分類編號"` |
| `[note: 'sensitive:true']` | 加入 `security.field_level.masking` |
| `[note: 'ref_code:StatusCode']` | `options: { source: "@lookup(StatusCode, code, label)" }` |
| `[note: 'group:基本資訊']` | 加入 `form.sections[基本資訊].fields[]` |

**4. Enum / FK 解析**

- DBML `Enum` 定義 → PDL `options` 下拉選項
- FK 引用（`ref: > OtherTable.id`）→ 推斷為 `select` 類型，用引用表的 label 欄位作為 `options.label_field`

**5. sensitive 合併規則** (v3.1)

```
PDL masking = DBML(sensitive: true) ∪ haPDL(fieldName*)
```

即使 haPDL 中未使用 `*` 符號，若 DBML 標記 `sensitive: true`，仍自動啟用 masking。

**6. 欄位未找到處理**

若 haPDL 引用的欄位名在 DBML Entity 中不存在 → `DBML-ERR-001`（如 `password2` 是虛擬欄位，不在 DBML 中，應標記為 virtual 並跳過 DBML 推導）。

---

### Phase 5: haAPI Hydration（haAPI 推導）

**輸入**: PDL 中間結果 + haAPI 規格  
**輸出**: PDL 中間結果，補充 haAPI 來源的屬性

#### 5.1 Validation 推導

讀取 haAPI 的 `advanced.validation.rules`，對每個欄位覆寫/補充 validation：

```yaml
# haAPI 定義
advanced:
  validation:
    rules:
      - field: apcatId
        pattern: "^[A-Z0-9]{1,10}$"
        unique: true
        max_length: 10

# → 合併至 PDL 欄位驗證
form.fields[apcatId].validation:
  - rule: pattern
    value: "^[A-Z0-9]{1,10}$"
  - rule: unique
    value: true
```

**SSOT 衝突解決規則**：

| 屬性 | 解決策略 | 錯誤條件 |
|------|---------|---------|
| `maxLength` | 取 `min(DBML, haAPI)` — 較嚴格者 | 若 haPDL > DBML → `SSOT-ERR-001` |
| `pattern` | haAPI 優先（通常更精確）| 若 haPDL 比 haAPI 更寬鬆 → `LINT-WARN-001` |
| `required` | 任一來源為 true 即為 true | 不可放寬 |
| `min` / `max` | haAPI 優先，haPDL 可進一步收緊 | — |

#### 5.2 Permissions 推導

讀取 haAPI `access.permissions`，映射至 PDL：

| PDL 操作 | haAPI 操作 | 說明 |
|---------|-----------|------|
| `view` | `list` + `read`（取聯集） | 查看權限 |
| `create` | `create` | 新增權限 |
| `edit` | `update` | 編輯權限 |
| `delete` | `delete` | 刪除權限 |

```yaml
# haAPI
access:
  permissions:
    create:
      roles: [admin]
    list:
      roles: [admin, manager, user]

# → PDL
security:
  permissions:
    create: [admin]
  auth:
    roles: [admin]              # 取頁面主操作（form-add → create）
```

**安全檢查**：haPDL 的 permissions 只能**收緊**（取子集），不能放寬 haAPI 限制 → 否則 `SEC-ERR-001`。

**欄位級權限推導**：若 haAPI 有欄位級 access control → 映射到 PDL `security.field_level.readonly` 或 `hidden`。

#### 5.3 async.submit 端點推導（Form 頁面）

**適用條件**：`page_type == form` 且 haPDL **未**明確定義 `async.submit.endpoint`

推導鏈：

```
haPDL.actions.operations: [create]
  → haAPI.exposes.standard 或 haAPI.standard
  → 找到 create 對應 POST /api/{entity-kebab}
  → 寫入 PDL
```

```yaml
# PDL 結果
datasource:
  submit:
    endpoint: "POST /api/apcat"

async:
  mutations:
    submit:
      endpoint: "POST /api/apcat"
      loading: { ... }           # 來自 form_defaults
      on_success: { ... }
      on_error: { ... }
```

**跳過推導的判定條件**（見 §5 特殊頁面）：
1. `async.submit.endpoint` 在 haPDL 中有明確值
2. `actions.operations` 中的值不在 haAPI `standard` 清單中
3. haPDL 中有非標準 action（如 `store_session`）

#### 5.4 keyword search.fields 補全

```yaml
# haAPI
search:
  fields: [apcatId, apcatCname, apcatEname]

# → 補全 Phase 3 的 _pending_search_fields
filters[keyword]:
  search_fields: [apcatId, apcatCname, apcatEname]
  _pending_search_fields: null    # 標記清除
```

若 haAPI 無 `search.fields`，fallback 至 DBML 中 entity 的所有 text 型別欄位。

#### 5.5 error_handling.api.source 推導

```
haPDL: api: apcat
→ PDL: error_handling.api.source: apcat
```

haPDL 的 `api:` 綁定自動成為 error_handling 的上下文，無需重複指定。

#### 5.6 async_ui 展開 (v3.1)

若 haAPI 操作標記為 `async: true`（長時間操作），展開前端 UX 配置：

```yaml
async:
  operations:
    - operation: generate-report
      indicator: progress_bar
      polling:
        interval: 2000
        endpoint: /api/{entity-kebab}/jobs/{jobId}
      on_complete:
        message: "報表生成完成"
        action: download
```

---

### Phase 6: User Override & Export（使用者覆寫與輸出）

**輸入**: PDL 中間結果 + haPDL 中的明確配置  
**輸出**: 最終 PDL

#### 6.1 Deep Merge

將 haPDL 中**所有明確定義的屬性**執行 deep merge（語意見 §6）。

**核心**：haPDL 明確配置擁有**最高優先級**。如果使用者在 haPDL 中寫了 `async.submit.endpoint: /api/user/login`，Phase 5 的自動推導結果必須被覆寫。

覆寫範例（以 userAdd 為例）：
- `error_handling.validation.rules[password].minLength: 12` → 覆寫
- `error_handling.api.status_handlers.409.message: "使用者帳號已存在"` → 覆寫
- `async.submit.on_success.message: "新增使用者成功"` → 覆寫
- `async.submit.on_error.action: stay` → 覆寫
- `accessibility.keyboard.tab_order: [...]` → 覆寫
- `security.field_level.masking: [...]` → 覆寫

#### 6.2 路由推斷驗證

確保所有 `route` 欄位已具象化：

| 來源 | 推斷規則 |
|------|---------|
| `page.route` | `/{entity-kebab}/{page-suffix}` |
| `actions.create.route` | `/{entity-kebab}/add` |
| `actions.edit.route` | `/{entity-kebab}/edit/{id}` |
| `actions.cancel.route` | `/{entity-kebab}/list` |
| `async.submit.on_success.redirect` | `/{entity-kebab}/list` |

**例外**：如 `codeAdd` 的 `cancel.route` 含查詢參數 `?metaId={metaId}`，由 haPDL 明確配置覆寫 Convention。

#### 6.3 Schema Validation

對最終 PDL 執行 `pdl-syntax-v3.2.md` 驗證：

| 驗證項目 | 條件 |
|---------|------|
| `page.id` | 必填，kebab-case 格式 |
| `page.type` | 必填，符合 PDL 13 種頁面類型之一 |
| `page.title` | 必填 |
| `datasource.entity` | 必填 |
| form 頁面 | `form.fields` 至少一個欄位 |
| list 頁面 | `table.columns` 至少一個欄位 |
| form 頁面 | `datasource.submit` 或 `async.mutations.submit` 的 endpoint 已存在 |

#### 6.4 輸出

序列化 PDL 物件為 YAML，寫入 `[page].pdl.yaml`。

---

## 4. 錯誤與警告代碼表

### 錯誤代碼命名規則

| 前綴 | 類別 | 說明 |
|------|------|------|
| `CTX-ERR` | 上下文 | Phase 1 輸入載入失敗 |
| `SSOT-ERR` | SSOT 衝突 | 跨規格一致性違規 |
| `SEC-ERR` | 安全 | 權限放寬（安全漏洞） |
| `CONV-ERR` | 推導失敗 | Convention 推導無法完成 |
| `SUGAR-ERR` | 語法 | 符號解析失敗 |
| `DBML-ERR` | DBML | DBML 查找失敗 |
| `LINT-WARN` | Lint | 最佳實踐建議 |
| `MERGE-WARN` | 合併 | 冗餘配置偵測 |

### 完整代碼表

| 代碼 | 嚴重性 | Phase | 說明 |
|------|--------|-------|------|
| `CTX-ERR-001` | **FATAL** | 1 | Entity 在 DBML 中找不到 |
| `CTX-ERR-002` | **FATAL** | 1 | haAPI 檔案找不到（有 `api:` 綁定時） |
| `CTX-WARN-001` | WARN | 1 | `schema_version` 與轉換器版本不匹配 |
| `SUGAR-ERR-001` | ERROR | 3 | 無法解析的欄位符號組合（如 `name!?` — required 與 optional 衝突） |
| `DBML-ERR-001` | ERROR | 4 | haPDL 引用的欄位名在 DBML Entity 中不存在（且非 virtual 欄位） |
| `SSOT-ERR-001` | ERROR | 5/6 | haPDL `maxLength` 超過 DBML 定義（不允許放寬） |
| `SEC-ERR-001` | ERROR | 5/6 | haPDL `permissions` 放寬了 haAPI 限制（權限提升） |
| `CONV-ERR-001` | ERROR | 5 | form 頁面無 `operations` 且無明確 `async.submit.endpoint`（無法推導端點） |
| `LINT-WARN-001` | WARN | 5 | haPDL `pattern` 比 haAPI 更寬鬆 |
| `LINT-WARN-002` | WARN | 3-5 | Convention 推斷失敗（如欄位在 DBML 無 label 標註），需明確指定 |
| `LINT-WARN-003` | WARN | — | list 頁面未定義 filters（best practice） |
| `LINT-WARN-004` | INFO | — | form 頁面的 validation rules 完全依賴 DBML 推斷（建議明確定義關鍵規則） |
| `MERGE-WARN-001` | WARN | 6 | haPDL 明確配置與推導結果完全相同（冗餘配置，可省略） |

---

## 5. 特殊頁面處理策略

### 5.1 辨識規則

轉換器透過以下條件辨識「不適用標準 Convention 推斷」的頁面：

| 辨識條件 | 處理方式 |
|---------|---------|
| haPDL 已明確定義 `async.submit.endpoint` | Phase 5.3 **跳過**端點推導 |
| `actions.standard` 為物件陣列格式（非 `[create, edit, ...]`） | Phase 3.2 **直接透傳**，不做 Convention 展開 |
| `page_type: hybrid` | Phase 2 **無** type-specific defaults |
| `security.public: true` | Phase 5.2 **跳過** permissions 推導 |
| `actions.operations` 中的值不在 haAPI `standard` 清單中 | Phase 5.3 **跳過**端點推導 |
| haPDL 中有 `async.submit.action: store_session` 或其他非標準 action | Phase 5.3 **跳過**端點推導 |

### 5.2 Benchmark 特殊頁面 Phase 行為矩陣

| 頁面 | Phase 2 | Phase 3 | Phase 5.3 | 保留 async.submit 原因 |
|------|---------|---------|-----------|----------------------|
| **login** | form_defaults (部分) | standard 透傳（物件格式） | **跳過** | `store_session` + `store_fields` 是登入專屬；endpoint `/api/user/login` 非標準 CRUD |
| **reset_password** | form_defaults (部分) | 正常展開 | **跳過** | token param + redirect 到 `/login` 而非 `/{entity-kebab}/list` |
| **userUpdate** | form_defaults | 正常展開 | **跳過** | endpoint 含 `{session.user_id}`；operation `update-self` 非標準 `update` |
| **codeList** | list_defaults | 正常展開 | 正常 | 雙 API 綁定（tree: code-meta-def, content: code-main），需保留 source 消歧 |
| **ugrpAp** | **無** (hybrid) | 透傳 | **跳過** | 自計算 payload（權限矩陣 bitwise OR）；endpoint 含兩參數 `{ugrpId}/{apCat}` |

---

## 6. Deep Merge 語意規格

### 合併規則

| 值類型 | 策略 | 說明 |
|-------|------|------|
| **物件屬性** | 遞迴合併 | 逐 key 深層覆寫 |
| **陣列屬性** | **完全替換** | 不做 append 或 union |
| **純量屬性** | 直接覆寫 | — |
| **null / 未定義** | 不覆寫 | 保留既有值 |

### 範例

```python
defaults = {
  "features": {
    "pagination": {
      "pageSize": 20,
      "pageSizes": [10, 20, 50, 100]   # 陣列
    },
    "searchable": True
  }
}

override = {
  "features": {
    "pagination": {
      "pageSize": 10,                   # 純量覆寫
      "pageSizes": [10, 20]             # 陣列完全替換
    }
    # searchable 未指定 → 保留 True
  }
}

result = deep_merge(defaults, override)
# {
#   "features": {
#     "pagination": { "pageSize": 10, "pageSizes": [10, 20] },
#     "searchable": True
#   }
# }
```

### 為何陣列不做 merge

陣列元素缺乏 key，無法判斷「哪個元素對應哪個」。若使用 append 或 union：
- `pageSizes: [10, 20]` + `[10, 20, 50, 100]` → `[10, 20, 10, 20, 50, 100]`？
- `status_handlers` 中的 409 要取哪個？

因此統一採「完全替換」策略，語意清晰。

---

## 7. Entity 名稱轉換規則

| 輸入 | 轉換函式 | 輸出 | 用途 |
|------|---------|------|------|
| `InfoUser` | `to_kebab()` | `info-user` | route、API endpoint |
| `Apcat` | `to_kebab()` | `apcat` | route |
| `uGrpAP` | `to_kebab()` | `u-grp-ap` | route |
| `InfoUser` | `to_snake()` | `info_user` | 變數名（PDL2Vue 使用） |

### 實作

```python
import re

def to_kebab(name: str) -> str:
    """CamelCase/mixedCase → kebab-case"""
    # 1. 在大寫字母前插入分隔
    s = re.sub(r'([A-Z]+)', r'-\1', name)
    # 2. 轉小寫並清理
    return re.sub(r'-+', '-', s).lower().strip('-')

def to_snake(name: str) -> str:
    """CamelCase/mixedCase → snake_case"""
    return to_kebab(name).replace('-', '_')

def extract_page_suffix(page_id: str, entity_kebab: str) -> str:
    """從 page_id 提取操作後綴"""
    # apcat-add → add
    # user-list → list
    # login → login（無 entity 前綴時，整個 page_id 作為後綴）
    if page_id.startswith(entity_kebab + '-'):
        return page_id[len(entity_kebab) + 1:]
    return page_id
```

### 邊界情況

| Entity | Page ID | Suffix | Route |
|--------|---------|--------|-------|
| `Apcat` | `apcat-add` | `add` | `/apcat/add` |
| `InfoUser` | `user-add` | `add` | `/info-user/add` |
| `InfoUser` | `login` | `login` | `/login` (特殊頁面) |
| `uGrpAP` | `ugrp-ap` | 整體 | `/ugrp-ap` (特殊頁面) |

---

## 8. 內部資料結構定義

### Python Dataclass

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class TranslatorContext:
    """Phase 1 產出：轉換上下文"""
    page_id: str
    page_type: str           # list | form | detail | hybrid | ...
    title: str
    entity_name: str
    entity_kebab: str        # CamelCase → kebab-case
    api_name: Optional[str]
    schema_version: str

    dbml_context: Dict[str, 'DBMLField'] = field(default_factory=dict)
    haapi_context: Optional['HaAPISpec'] = None
    hapdl_raw: Dict = field(default_factory=dict)  # 原始 haPDL YAML dict

@dataclass
class DBMLField:
    """DBML 欄位定義"""
    name: str
    type: str               # nvarchar(20), int, boolean, ...
    constraints: List[str]  # not null, pk, unique, ...
    default: Optional[str] = None
    notes: Dict[str, str] = field(default_factory=dict)  # label, ref_code, sensitive, group
    enum_values: Optional[List[str]] = None
    fk_ref: Optional[str] = None    # OtherTable.field

@dataclass
class HaAPISpec:
    """haAPI 規格"""
    name: str
    standard: Dict[str, 'APIOperation'] = field(default_factory=dict)   # create, read, update, delete
    operations: Dict[str, 'APIOperation'] = field(default_factory=dict) # 業務操作
    access_permissions: Dict[str, List[str]] = field(default_factory=dict)
    search_fields: Optional[List[str]] = None
    validation_rules: List[Dict] = field(default_factory=list)

@dataclass
class APIOperation:
    """API 操作定義"""
    name: str
    path: str               # /api/info-user
    method: str             # GET, POST, PUT, PATCH, DELETE
    input_schema: Optional[Dict] = None   # request body schema
    is_async: bool = False
```

### PDL 中間物件

轉換過程中，PDL 以 Python dict 表示，最終序列化為 YAML。每個 Phase 在同一個 dict 上原地修改（in-place mutation）。

---

## 9. 端到端轉換範例

### 9.1 範例 A：apcatAdd（標準 form-add 頁面）

#### 輸入：`apcatAdd.hapdl.yaml`

```yaml
page: apcat-add
type: form
title: 新增AP分類
entity: Apcat
api: apcat
schema_version: "3.2.1"

view:
  fields:
    - apcatId!
    - apcatCname!
    - apcatEname?
    - apseq?
  defaults:
    apseq: 1

actions:
  standard: [create]
  operations: [create]

error_handling:
  validation:
    rules:
      - field: apcatId
        constraints:
          - pattern: "^[A-Z0-9]{1,10}$"
            message: "AP分類編號只能包含大寫英數字"
      - field: apseq
        constraints:
          - min: 1
  api:
    status_handlers:
      409: { type: conflict, action: display, display_mode: toast }
  business:
    errors:
      DUPLICATE_APCAT_ID:
        message: "此AP分類編號已存在，請使用其他編號"
        display: toast
        severity: error
        field: apcatId

async:
  submit:
    on_success:
      message: "新增AP分類成功"

security:
  permissions:
    create: [admin]
```

#### 各 Phase 處理要點

| Phase | 關鍵操作 |
|-------|---------|
| 1 | 載入 Apcat DBML + apcat.haapi.yaml；建 PDL 空殼 route=/apcat/add |
| 2 | 注入 form_defaults（validation display/timing, async.submit loading/redirect, error_handling.api 400/500）；aria: "新增AP分類表單" |
| 3 | `apcatId!` → required:true；`apcatEname?` → required:false；`apseq?` → required:false；standard:[create] → save/reset/cancel 三按鈕 |
| 4 | DBML: apcatId nvarchar(10) → maxLength:10, input:text；apcatCname nvarchar(20)；apcatEname nvarchar(30)；apseq tinyint → min:0, max:255 |
| 5 | haAPI: create → POST /api/apcat；permissions create:[admin]；validation apcatId pattern + unique |
| 6 | 覆寫：apseq.min:1（haPDL 收緊了 Phase 4 的 min:0）、409 message、business errors、on_success message |

#### 輸出：`apcatAdd.pdl.yaml`（部分節錄）

```yaml
version: 3
page:
  id: apcat-add
  type: form
  title: "新增AP分類"
  route: /apcat/add
  schema_version: "3.2"
  auth:
    roles: [admin]

  datasource:
    entity: Apcat
    api_ref: apcat
    submit:
      endpoint: "POST /api/apcat"

  form:
    layout: vertical
    fields:
      - field: apcatId
        label: "AP分類編號"
        input: text
        required: true
        maxLength: 10
        unique: true
        validation:
          - rule: pattern
            value: "^[A-Z0-9]{1,10}$"
            message: "AP分類編號只能包含大寫英數字"

      - field: apcatCname
        label: "AP分類中文名稱"
        input: text
        required: true
        maxLength: 20

      - field: apcatEname
        label: "AP分類英文名稱"
        input: text
        required: false
        maxLength: 30

      - field: apseq
        label: "顯示順序"
        input: number
        required: false
        default: 1
        min: 1
        max: 255

  actions:
    primary:
      - id: save
        label: "新增儲存"
        type: submit
        variant: primary
    secondary:
      - id: reset
        label: "清除重填"
        type: reset
        variant: secondary
      - id: cancel
        label: "返回"
        type: navigate
        route: /apcat/list

  error_handling:
    validation:
      display: { mode: inline, position: below, scroll_to_first: true, highlight_field: true }
      timing: { on_blur: true, on_submit: true }
    api:
      source: apcat
      status_handlers:
        400: { type: validation, action: map_to_fields }
        409: { type: conflict, action: display, display_mode: toast }
        500: { type: server_error, action: display, display_mode: modal }
    business:
      errors:
        DUPLICATE_APCAT_ID:
          message: "此AP分類編號已存在，請使用其他編號"
          display: toast
          severity: error
          field: apcatId

  async:
    mutations:
      submit:
        endpoint: "POST /api/apcat"
        loading: { indicator: button_spinner, disable_form: true }
        on_success:
          message: "新增AP分類成功"
          action: navigate
          target: /apcat/list
        on_error:
          message: "新增AP分類失敗: {error}"

  accessibility:
    aria: { page_label: "新增AP分類表單", form_label: "新增AP分類資料填寫" }
    keyboard: { enabled: true }

  security:
    permissions: { create: [admin] }
    field_level: {}

  testing:
    selectors: { strategy: data-testid, auto_generate: true }
    mock_data: { enabled: true }
```

---

### 9.2 範例 B：userList（標準 list 頁面）

#### 輸入：`userList.hapdl.yaml`（關鍵片段）

```yaml
page: user-list
type: list
title: 使用者管理
entity: InfoUser
api: info-user

view:
  filters:
    - userId~
    - userName~
    - ugrpId[]
    - deptId=
  columns:
    - userId!^
    - userName^
    - deptName
    - lastVisit|datetime^
    - visitCount^
  features:
    pagination:
      pageSize: 10            # 覆寫 list_defaults 的 20
```

#### 各 Phase 處理要點

| Phase | 關鍵操作 |
|-------|---------|
| 1 | 載入 InfoUser DBML + info-user.haapi.yaml；route=/info-user/list |
| 2 | 注入 list_defaults (pagination[20], searchable, skeleton, persistence) + aria "使用者管理列表"/"使用者管理資料列表" |
| 3 | `userId~` → {id:userId, operator:contains}；`ugrpId[]` → {id:ugrpId, operator:in, input:multiselect}；`userId!^` → {key:userId, emphasis:true, sortable:true}；`lastVisit\|datetime^` → {key:lastVisit, format:datetime, sortable:true} |
| 4 | DBML: userId varchar(20)、lastVisit datetime 等 → 補充 label |
| 5 | haAPI: permissions、search.fields |
| 6 | 覆寫 pageSize:10、security.permissions（manager edit）、401/403 handler |

---

### 9.3 範例 C：login（特殊頁面）

#### 各 Phase 行為差異

| Phase | 與標準 form 的差異 |
|-------|------------------|
| 2 | form_defaults 注入，但 `on_blur: false` 將在 Phase 6 覆寫 |
| 3 | `actions.standard` 是物件格式 → **透傳** login 按鈕，不展開 save/reset/cancel |
| 5 | `async.submit.endpoint` 在 haPDL 已明確為 `/api/user/login` → **跳過**端點推導 |
| 6 | 保留 `store_session`、`store_fields`、`brute_force`、`captcha` 等 login 專屬配置 |

---

## 10. 測試與驗收策略

### 10.1 三層測試架構

```
┌─────────────────────────────────┐
│  Layer 3: 端到端 Benchmark      │  20 個 .hapdl.yaml → 比對 .pdl.yaml
├─────────────────────────────────┤
│  Layer 2: Linter 整合           │  每個錯誤代碼一個觸發用例
├─────────────────────────────────┤
│  Layer 1: Phase 單元測試        │  每個 Phase 獨立可測
└─────────────────────────────────┘
```

### 10.2 Phase 單元測試範例

```python
# Phase 3 — 符號解析
def test_phase3_field_symbols():
    assert parse_field("password*!", context="fields") == {
        "field": "password", "required": True, "sensitive": True, "input": "password"
    }
    assert parse_field("userId!^", context="columns") == {
        "key": "userId", "emphasis": True, "sortable": True
    }
    assert parse_field("lastVisit|datetime^", context="columns") == {
        "key": "lastVisit", "format": "datetime", "sortable": True
    }

# Phase 4 — DBML 推導
def test_phase4_dbml_type_inference():
    dbml_field = DBMLField(name="email", type="varchar(100)", constraints=["not null"])
    result = infer_from_dbml(dbml_field)
    assert result["input"] == "text"
    assert result["maxLength"] == 100
    assert result["required"] == True

# Phase 6 — Deep Merge
def test_phase6_deep_merge_array_replace():
    defaults = {"features": {"pagination": {"pageSizes": [10, 20, 50, 100]}}}
    override = {"features": {"pagination": {"pageSizes": [10, 20]}}}
    result = deep_merge(defaults, override)
    assert result["features"]["pagination"]["pageSizes"] == [10, 20]

# Linter — SSOT 衝突
def test_ssot_err001_maxlength_widening():
    with pytest.raises(SSOTConflictError, match="SSOT-ERR-001"):
        validate_constraints(dbml_max=20, hapdl_max=50)

# Linter — 安全
def test_sec_err001_permission_escalation():
    with pytest.raises(SecurityError, match="SEC-ERR-001"):
        validate_permissions(
            haapi_roles=["admin"],
            hapdl_roles=["admin", "manager"]  # 放寬 → 報錯
        )
```

### 10.3 Benchmark 端到端測試

以 `benchmarks/haPDL-v3.2/` 下的 20 個 `.hapdl.yaml` 作為黃金測試集：

| 類別 | 頁面數 | 驗收重點 |
|------|--------|---------|
| 標準 list | 4 | filters/columns 符號展開、list_defaults、pagination 覆寫、sorting |
| 標準 form (add) | 5 | fields 符號展開、form_defaults、actions.standard 展開、DBML 型別推斷、haAPI 端點推導 |
| 標準 form (edit) | 6 | 同 add + 載入資料端點、update 按鈕組、delete 操作 |
| 特殊頁面 | 5 | 明確配置的穿越保留、Convention 跳過、async.submit 透傳 |

```bash
# 端到端測試腳本
for f in benchmarks/haPDL-v3.2/*.hapdl.yaml; do
    hapdl convert "$f" --dbml erm.dbml --haapi-dir haapi/ \
        -o "output/$(basename $f .hapdl.yaml).pdl.yaml"
    diff "expected/$(basename $f .hapdl.yaml).pdl.yaml" \
         "output/$(basename $f .hapdl.yaml).pdl.yaml"
done
```

### 10.4 Linter 整合測試

針對 §4 錯誤代碼表的每個代碼，準備一個**故意觸發**的測試用例：

| 代碼 | 測試檔案 | 觸發方式 |
|------|---------|---------|
| `CTX-ERR-001` | `test-missing-entity.hapdl.yaml` | `entity: NonExistent` |
| `CTX-ERR-002` | `test-missing-haapi.hapdl.yaml` | `api: non-exist-api` |
| `SSOT-ERR-001` | `test-maxlength-wider.hapdl.yaml` | `maxLength: 999`（DBML 為 20） |
| `SEC-ERR-001` | `test-permission-escalation.hapdl.yaml` | 添加 haAPI 未允許的 role |
| `CONV-ERR-001` | `test-no-endpoint.hapdl.yaml` | form 無 operations 且無 endpoint |
| `SUGAR-ERR-001` | `test-conflicting-symbols.hapdl.yaml` | `name!?`（required + optional 衝突） |

---

## 附錄 A：三版規格來源對照

本文整合自三份獨立分析的規格書，以下為各章節的主要採納來源：

| 章節 | 主要來源 | 採納理由 |
|------|---------|---------|
| §1 架構圖 | antiOpus | 最清晰的管線可視化 |
| §2 CLI 介面 | Opus | 唯一定義了 --verbose/--dry-run 旗標 |
| §3 Phase 1-2 | 三版共識 | 三版對 Phase 1-2 描述一致 |
| §3 Phase 3 符號表 | antiOpus + Opus | antiOpus 的 `{}` / `<~` 符號最完整，Opus 的組合範例最清晰 |
| §3 Phase 3 actions | antiOpus | 引入 effects chain 概念（`type: api-call` / `navigate`）對齊 PDL effect chain |
| §3 keyword 展開 | antiOpus | `_pending_search_fields` 標記機制最適合跨 Phase 延遲處理 |
| §3 物件格式 standard | Opus + antiOpus | 兩者互補：Opus 定義了透傳規則，antiOpus 提供了物件格式帶屬性的處理 |
| §4 Phase 4 | 三版共識 | DBML 推導邏輯三版一致；antiOpus 的 Annotated DBML note 語法最詳細 |
| §4 Phase 5 | 三版共識 | Opus 的衝突解決策略表最明確 |
| §4 Phase 6 | Opus + antiOpus | Opus 的路由推斷驗證最完整；antiOpus 的 schema validation 清單更嚴謹 |
| §4 錯誤代碼 | antiOpus | 結構化命名（CTX/SSOT/SEC/CONV/SUGAR/MERGE 前綴）最佳 |
| §5 特殊頁面 | Opus + antiOpus | Opus 的 Phase 行為矩陣 + antiOpus 的 3 條辨識規則 |
| §6 Deep Merge | Opus | 唯一明確定義「陣列完全替換」語意並給出理由 |
| §7 名稱轉換 | Opus + antiOpus | Opus 的 Python 實作 + antiOpus 的 extract_page_suffix 邏輯 |
| §8 資料結構 | Opus | 唯一提供 Python dataclass 定義 |
| §9 範例 A (apcatAdd) | antiOpus | 完整 PDL 輸出含 business errors |
| §9 範例 B (userList) | 新增 | 補充 list 頁面範例（三版均只有 form 範例） |
| §9 範例 C (login) | 三版共識 | 特殊頁面差異說明 |
| §10 測試 | Opus + antiOpus | Opus 的三層架構 + antiOpus 的 Linter 觸發用例表 |

---

**文件維護者**：WA-RAPTor 團隊  
**版本**：v3.2.1 (Consolidated)  
**參照主規格**：`haPDL-specification-v3.2.md`、`pdl-syntax-v3.2.md`、`haPDL-page-type-defaults-v3.2.1.md`
