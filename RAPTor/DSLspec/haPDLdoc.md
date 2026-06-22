# haPDL 完整手冊

**haPDL (High-level Abstract Page Description Language) v3.3**

> WA-RAPTor 框架的高階頁面描述 DSL，專注於頁面結構、狀態管理、互動行為建模。

**版本**：**v3.3.0 (Release Candidate, 2026-05-13)**
**基準時間**：2026-05-13
**對齊規格**：haAPI v3.3、haARM v3.3、Annotated DBML v3.3、PDL v3.3
**前版**：v3.2.1（見 `archive/haPDL-specification-v3.2.md`）

---

## 目錄

0. [版本沿革（跨 DSL）](#0-版本沿革跨-dsl)
1. [概述與設計理念](#1-概述與設計理念)
2. [版本沿革（haPDL 專屬）](#2-版本沿革haPDL-專屬)
3. [適用情境](#3-適用情境)
4. [EBNF 文法定義](#4-ebnf-文法定義)
5. [JSON Schema 定義](#5-json-schema-定義)
6. [語義規則表](#6-語義規則表)
7. [基礎語法規格](#7-基礎語法規格)
8. [狀態管理系統](#8-狀態管理系統)
9. [錯誤處理框架](#9-錯誤處理框架)
10. [非同步行為規範](#10-非同步行為規範)
11. [無障礙存取規範](#11-無障礙存取規範)
12. [安全性規格](#12-安全性規格)
13. [測試性規格](#13-測試性規格)
14. [複雜表單支援](#14-複雜表單支援)
15. [檔案處理規格](#15-檔案處理規格)
16. [進階配置](#16-進階配置)
17. [樣板與混入](#17-樣板與混入)
18. [跨規格整合](#18-跨規格整合)
19. [完整範例](#19-完整範例)
20. [驗證規則檢查清單](#20-驗證規則檢查清單)
21. [檔案格式與工具支援](#21-檔案格式與工具支援)
22. [附錄](#附錄)

---

## 0. 版本沿革（跨 DSL）

### 0.1 跨 DSL 版本歷程（v1.0 → v3.3）

| 版本 | 日期 | 主要變更 |
|------|------|---------|
| v1.0 | 2026-04 早期 | 初版規格分散建立（haARM v1、haAPI v1.0、haPDL v1.0、DBML v1.1） |
| v2.0 | 2026-04 中 | haARM：新增 `resources` 區段、`scope`、`$self`、`context:`、`TimeWindowCondition` |
| v3.0 | 2026-04 末 | haAPI 新增 `proxy`/`ext.*`/`logic`；haPDL 新增 State/Error/Async/A11y/Security/Testability/樣板與混入 |
| v3.1 | 2026-05 初 | haPDL：Scope Declaration、`security.permission_refs`、`datasource_scope` 雛形 |
| v3.2 | 2026-05-11 | haAPI Access v2 雙軌、PDL `permission_refs` 落地、DBML 四個自訂標註 |
| **v3.3** | **2026-05-13** | (a) haARM 跳版 v3.3，新增 `starts_with`/`ends_with`；(b) Convention over Configuration 三段式；(c) DBML 移除「是否需要？」探索性標題、四標註升一級語法；(d) 四 DSL 統一 12 章骨架；(e) 新增 `CROSS-DSL-GUIDE.md` |

### 0.2 v3.3 四 DSL 版本互鎖表

| DSL | 主檔（SSoT） | 規格檔 | 版本 | 對齊狀態 |
|-----|-------------|--------|------|---------|
| haAPI | `haAPIdoc.md` | `haAPI-specification_v3.3.md` | **v3.3.0** | Access v2 雙軌引用 haARM `permission.id`/`role.id` |
| haPDL | `haPDLdoc.md` | `haPDL-specification-v3.3.md` + `pdl-syntax-v3.3.md` | **v3.3.0** | `auth.roles[]` / `security.permission_refs` 對齊 haARM |
| haARM | `haARMdoc.md` | `haARM-Specification_v3.3.md` | **v3.3.0** | 新增 `starts_with`，引入 profile / auto_infer |
| DBML | `annotated_DBML-v3.3.md` | — | **v3.3.0** | 收編 4 個一級標註；與 haARM `resource.id` ↔ table 對齊 |

> **維護規則**：跨 DSL 版本升級時先寫入本 §0.1，再到各 *doc.md sync；不在各檔自行加非同步版本。Freeze 視窗起於 **2026-05-19**（凍結 EBNF/JSON Schema/欄位語意；文字、範例、速查卡不受限）。詳見 `ccwLog/0513-specsAlign_plan.md` §0 與 `ccwLog/0513-PQ_discuss.md` Q12。
>
> §2「版本沿革（haPDL 專屬）」記錄 haPDL 內部的演進，與本 §0 互補；M0.3 會合併重複項。

### 0.3 章節骨架對照表（v3.3 統一 12 章）

> haPDLdoc 現行 22 章是四份 *doc.md 中最複雜者。M0.3 採「保留現狀 + 對照表標記」策略；實際重排排在 freeze 視窗結束後（>2026-05-26），由 M2/M3 一併完成。

| v3.3 標準章 | 標題 | 本檔現行位置（合併源） | 完工里程碑 |
|:----------:|------|---------------------|:---------:|
| 0 | 版本沿革 | §0（跨 DSL）+ §2（haPDL 專屬，將併入 §0.4） | ✅ M0.4 |
| 1 | 設計理念與定位 | §1（已加 §1.5 SSoT 宣告） | ✅ M0.4 |
| 2 | 適用情境 | §3 | M0.3 重排 |
| 3 | EBNF 文法定義 | §4 | M0.3 重排 |
| 4 | JSON Schema 定義 | §5 | M0.3 重排 |
| 5 | 語義規則表 | §6 + §7 基礎語法 + §8 狀態 + §9 錯誤 + §10 非同步 + §11 A11y + §12 安全性 + §13 測試性 + §14 複雜表單 + §15 檔案處理 + §16 進階配置 + §17 樣板與混入 | M0.3 重排（內容多，分子章節） |
| 6 | Convention over Configuration | （新增章；M2 寫入三層 defaults 來源） | ⏳ M2 |
| 7 | 跨規格整合 | §18 + 補 hycms-ht002 範例 | ⏳ M3 |
| 8 | 完整範例 | §19 | M0.3 重排 |
| 9 | 驗證規則（含 §9.5 Anti-Pattern） | §20 + 新 §9.5 | ⏳ M1（§9.5）+ M0.3 重排 |
| 10 | 工具支援與 Lint | §21 | M0.3 重排 |
| 11 | 遷移指引 | §22 / 附錄 | M0.3 重排 |

---

## 1. 概述與設計理念

haPDL 是一套高階抽象的頁面描述語言，專為已建立領域模型的團隊設計，讓使用者能夠以**宣告意圖**的方式定義頁面及其互動行為，而無需關注實作細節。

### 1.1 核心原則

| # | 原則 | 說明 |
|---|------|------|
| 1 | **意圖優於實作** | 描述「要什麼」而非「怎麼做」 |
| 2 | **慣例優於配置** | 利用合理的預設值減少配置 |
| 3 | **漸進式細化** | 從簡單開始，需要時才增加複雜度 |
| 4 | **領域驅動** | 基於 DBML 定義的領域模型自動推斷 |
| 5 | **可讀性優先** | 語法接近自然語言，非技術人員也能理解 |
| 6 | **行為完整性** | 不僅描述靜態結構，更完整描述動態互動 (v3.0+) |
| 7 | **跨規格對齊** | 與 haAPI、Annotated DBML 建立明確引用鏈路 (v3.1+) |

### 1.2 架構層次

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

### 1.3 Scope Declaration（職責邊界）

haPDL 關注「使用者在頁面上能做什麼」（前端意圖）。後端的實作邏輯屬於 haAPI → TypeSpec/CodeGen 管線，haPDL 不涉及。

```
haPDL → 知道「activate 按鈕會呼叫 activate 操作」
haAPI → 知道「activate 操作的實作是 UPDATE InfoUser SET userType='A'」
haAPI → 知道「reset_password 操作會呼叫 ext.smtp.send_email」
haAPI → 知道「verify_captcha 是 proxy 到 ext.captcha.validate」
PDL   → 知道「activate 按鈕的完整 UI 配置（icon、variant、確認對話框）」
```

haPDL 透過 `api:` 欄位引用 haAPI 定義名稱，透過 `actions.operations` 引用 haAPI 操作名稱，但不涉及其實作細節。haAPI 的 `ext.*` 命名空間、`proxy` 原語、`integrations` 宣告和 `resilience` 級聯機制皆屬於 haAPI 內部細節，haPDL 僅透過操作名稱引用，不區分操作的底層類型。

### 1.4 在 WA-RAPTor 體系中的定位

```
Gherkin BDD 規格 ─┐
haARM 角色/權限 ──┤→ 語意模型 (IML) → 多目標產生
DBML 領域模型 ───┘
  ├→ haPDL（高階頁面描述）→ PDL（詳細頁面配置）→ UI 元件 (React/Vue)
  ├→ haAPI（高階 API）→ TypeSpec/OpenAPI → 後端程式碼
  ├→ 驗證規則 (Zod)
  └→ 測試套件 (Playwright/Cucumber)
```

### 1.5 SSoT 主手冊宣告

**本文件為 haPDL 的 SSoT 主手冊**，PM/SA 與下游 codegen（Pdl2whyVue / haPDL2PDL）對 haPDL 語法的單一可信來源。

- 技術參考：`haPDL-specification-v3.3.md`（EBNF 與 JSON Schema 完整版）、`pdl-syntax-v3.3.md`（投影層語法）、`haPDL2PDLspec-v3.3.md`（轉換器規格）
- 驗證實作：`HaPDL-Z3-Constraint-Validation.md`（Z3 表達式與證明）
- Convention 來源：`haPDL2PDL/src/defaults/*.yaml` + `haPDL/haPDL-page-type-defaults-v3.2.1.md`（M2.6 待 sync 至 v3.3）+ `phase2-defaults.ts` / `phase3-sugar.ts`
- 跨 DSL 整合：`CROSS-DSL-GUIDE.md`（v3.3 待建，詳見 M3）

三者描述衝突時**以本檔為準**；補充檔需於下次版本同步至本檔對應章節。

---

## 2. 版本沿革（haPDL 專屬）

| 版本 | 日期 | 重點變更 |
|------|------|----------|
| 1.0 | 2025-01 | 初始版本，基礎頁面描述 |
| 2.0 | 2025-03 | 新增 Master-Detail、Explorer 頁面類型 |
| 3.0 | 2025-12 | **重大升級**：從「頁面描述語言」進化為「互動行為描述語言」 |
| 3.1 | 2026-03-31 | **跨規格對齊**：haAPI 綁定、DBML 整合、`?` 消歧、Resolution Order、Scope Declaration |
| 3.2 | 2026-04-02 | **haAPI v3.2 對齊**：Scope Declaration 補充 `ext.*`/`proxy`/`integrations` 邊界、Resolution Order 新增 Resilience 屬性 |
| 3.2.1 | 2026-04-07 | **Convention 強化**：Page Type Defaults、`keyword` 保留名稱、testing 完整定義、form actions 展開規則、accessibility Convention 推斷 |

### v3.0 新增特性總覽

- **狀態管理系統**：跨頁面狀態、元件連動、狀態持久化
- **錯誤處理框架**：分層錯誤策略、使用者反饋、離線支援
- **非同步行為規範**：樂觀更新、Loading 狀態、請求控制
- **無障礙存取 (a11y)**：ARIA 標籤、鍵盤導覽、螢幕閱讀器支援
- **複雜表單支援**：動態區塊、可重複欄位、跨欄位驗證
- **完整檔案處理**：分塊上傳、預覽、處理管線
- **安全性規格**：欄位遮罩、資料隔離、敏感操作保護
- **測試性支援**：選擇器策略、Mock 資料、Gherkin 整合

---

## 3. 適用情境

### 最適合場景

- 企業後台管理系統（大量 CRUD 頁面）
- 已完成領域建模（Event Storming + DBML）的專案
- 需要快速原型開發和迭代
- 跨職能團隊協作（PM、BA、開發者共同參與）
- 標準化的業務流程系統
- 需要完整無障礙支援的政府/公共服務系統
- 需要離線能力的現場作業系統

### 不適合場景

- 高度客製化的使用者介面
- 遊戲或創意互動應用
- 沒有明確領域模型的專案
- 需要複雜動畫或視覺效果的頁面

---

## 4. EBNF 文法定義

### 4.1 頂層結構

```ebnf
(* HaPDL 文法定義 *)

HaPDLDocument ::= MetadataSection
                  PageDefinitionSection
                  (TemplateDefinitionSection)?
                  (MixinDefinitionSection)?
```

### 4.2 元資料區段

```ebnf
MetadataSection ::= 'metadata' ':' NEWLINE
                    INDENT MetadataFields DEDENT

MetadataFields ::= MetadataField
                 | MetadataField MetadataFields

MetadataField ::= 'schema_version' ':' Version NEWLINE
                | 'title' ':' String NEWLINE
                | 'version' ':' Version NEWLINE
                | 'description' ':' String NEWLINE
                | 'namespace' ':' NamespaceId NEWLINE
```

### 4.3 頁面定義區段

```ebnf
PageDefinitionSection ::= 'pages' ':' NEWLINE
                          (INDENT PageDefinition+ DEDENT)?

PageDefinition ::= '- page' ':' PageId NEWLINE
                   INDENT PageFields DEDENT

PageFields ::= PageField
             | PageField PageFields

PageField ::= 'type' ':' PageType NEWLINE
            | 'title' ':' String NEWLINE
            | 'entity' ':' EntityRef NEWLINE
            | 'api' ':' ApiRef NEWLINE
            | 'extends' ':' TemplateRef NEWLINE
            | 'mixins' ':' MixinRefList NEWLINE
            | 'view' ':' NEWLINE INDENT ViewDefinition DEDENT
            | 'state' ':' NEWLINE INDENT StateDefinition DEDENT
            | 'actions' ':' NEWLINE INDENT ActionsDefinition DEDENT
            | 'error_handling' ':' NEWLINE INDENT ErrorHandlingDefinition DEDENT
            | 'async' ':' NEWLINE INDENT AsyncDefinition DEDENT
            | 'security' ':' NEWLINE INDENT SecurityDefinition DEDENT
            | 'accessibility' ':' NEWLINE INDENT AccessibilityDefinition DEDENT
            | 'testing' ':' NEWLINE INDENT TestingDefinition DEDENT
            | 'advanced' ':' NEWLINE INDENT AdvancedDefinition DEDENT

PageType ::= 'list' | 'form' | 'detail' | 'master-detail' | 'explorer'
           | 'dashboard' | 'wizard' | 'search' | 'report' | 'hybrid'
           | 'kanban' | 'calendar' | CustomPageType
```

### 4.4 視圖定義

```ebnf
ViewDefinition ::= FiltersDefinition
                 | ColumnsDefinition
                 | FieldsDefinition
                 | LayoutDefinition
                 | ViewField ViewDefinition

FiltersDefinition ::= 'filters' ':' NEWLINE
                      INDENT FilterItem+ DEDENT

FilterItem ::= '- ' FieldRef FilterModifier
             | '- keyword' FilterModifier

FilterModifier ::= '~' | '=' | '>' | '<' | '><' | '[]' | '@' | '?' | ''

ColumnsDefinition ::= 'columns' ':' NEWLINE
                      INDENT ColumnItem+ DEDENT

ColumnItem ::= '- ' FieldRef ColumnModifier (DisplayType)? (Format)?

ColumnModifier ::= '!' | '?' | '^' | '&' | ''

DisplayType ::= ':badge' | ':image' | ':currency' | ':bar' | ':stars'
              | ':toggle' | ':chips' | ':truncate' | ':map' | ':swatch'
              | ':attachment' | ':avatar-name' | ':change-track' | ':tree'
              | ':rendered' | ':highlight' | CustomDisplayType

Format ::= '|date' | '|datetime' | '|time' | '|relative' | '|humanize'
         | '|number' '(' Integer ')' | '|percent' | '|bytes' | '|compact'
         | '|currency' '(' CurrencyCode ')' | '|uppercase' | '|lowercase'
         | '|capitalize' | '|mask' '(' MaskPattern ')' | CustomFormat

FieldsDefinition ::= 'fields' ':' NEWLINE
                     INDENT FieldItem+ DEDENT

FieldItem ::= '- ' FieldRef FieldModifier

FieldModifier ::= '!' | '?' | '#' | '*' | '@' | '[]' | '{}' | '~' | '<~' | ''

LayoutDefinition ::= 'layout' ':' LayoutType

LayoutType ::= 'single-column' | 'two-column' | 'three-column' | 'grid'
```

### 4.5 狀態定義

```ebnf
StateDefinition ::= LocalStateDefinition
                  | SharedStateDefinition
                  | CascadingDefinition
                  | PersistenceDefinition
                  | ComputedDefinition
                  | WatcherDefinition
                  | StateField StateDefinition

LocalStateDefinition ::= 'local' ':' NEWLINE
                         INDENT StateVariable+ DEDENT

StateVariable ::= '- name' ':' StateVarId NEWLINE
                  INDENT StateVarFields DEDENT

StateVarFields ::= StateVarField
                 | StateVarField StateVarFields

StateVarField ::= 'type' ':' StateType NEWLINE
                | 'default' ':' Value NEWLINE
                | 'max_length' ':' Integer NEWLINE
                | 'min_value' ':' Number NEWLINE
                | 'max_value' ':' Number NEWLINE
                | 'derived' ':' Expression NEWLINE
                | 'scope' ':' ('ui' | 'data') NEWLINE
                | 'description' ':' String NEWLINE

StateType ::= 'boolean' | 'string' | 'number' | 'integer'
            | 'array' ('<' SimpleType '>')? | 'object'
            | 'set' ('<' SimpleType '>')?
            | 'enum' '[' EnumValue (',' EnumValue)* ']'
            | EntityRef
```

### 4.6 動作定義

```ebnf
ActionsDefinition ::= StandardActionsDefinition
                    | OperationsDefinition
                    | CustomActionDefinition
                    | ActionField ActionsDefinition

StandardActionsDefinition ::= 'standard' ':' ActionList

ActionList ::= '[' ActionName (',' ActionName)* ']'

ActionName ::= 'create' | 'read' | 'update' | 'delete'

OperationsDefinition ::= 'operations' ':' ApiOperationRefList

ApiOperationRefList ::= '[' ApiOperationRef (',' ApiOperationRef)* ']'

CustomActionDefinition ::= 'custom' ':' NEWLINE
                           INDENT CustomAction+ DEDENT

CustomAction ::= '- name' ':' ActionId NEWLINE
                 INDENT CustomActionFields DEDENT

CustomActionFields ::= CustomActionField
                     | CustomActionField CustomActionFields

CustomActionField ::= 'operation' ':' ApiOperationName NEWLINE
                    | 'label' ':' String NEWLINE
                    | 'type' ':' ('submit' | 'button' | 'navigate' | 'reset') NEWLINE
                    | 'variant' ':' String NEWLINE
                    | 'icon' ':' IconId NEWLINE
                    | 'params' ':' ParamMap NEWLINE
                    | 'async_ui' ':' NEWLINE INDENT AsyncUIConfig DEDENT
                    | 'error_handling' ':' NEWLINE INDENT ActionErrorHandling DEDENT
                    | 'confirmation' ':' NEWLINE INDENT ConfirmationDialog DEDENT
                    | 'conditions' ':' ConditionList NEWLINE
```

### 4.7 錯誤處理定義

```ebnf
ErrorHandlingDefinition ::= DefaultErrorStrategy
                          | PageLevelErrorHandling
                          | ErrorField ErrorHandlingDefinition

DefaultErrorStrategy ::= 'default_strategy' ':' ErrorStrategy

ErrorStrategy ::= 'retry' | 'fallback' | 'dismiss' | 'custom'

PageLevelErrorHandling ::= 'handlers' ':' NEWLINE
                           INDENT ErrorHandler+ DEDENT

ErrorHandler ::= '- id' ':' ErrorHandlerId NEWLINE
                 INDENT ErrorHandlerFields DEDENT

ErrorHandlerFields ::= ErrorHandlerField
                     | ErrorHandlerField ErrorHandlerFields

ErrorHandlerField ::= 'error_code' ':' (Integer | ErrorPattern) NEWLINE
                    | 'error_type' ':' ErrorType NEWLINE
                    | 'strategy' ':' ErrorStrategy NEWLINE
                    | 'message' ':' String NEWLINE
                    | 'user_message' ':' String NEWLINE
                    | 'retry_count' ':' Integer NEWLINE
                    | 'fallback_value' ':' Value NEWLINE

ErrorType ::= 'validation' | 'network' | 'authorization' | 'not_found'
            | 'conflict' | 'timeout' | 'custom'
```

### 4.8 非同步定義

```ebnf
AsyncDefinition ::= AsyncUIDefinition
                  | OptimisticUpdateDefinition
                  | RequestControlDefinition
                  | AsyncField AsyncDefinition

AsyncUIDefinition ::= 'ui' ':' NEWLINE
                      INDENT AsyncUIField+ DEDENT

AsyncUIField ::= 'loading_indicator' ':' String NEWLINE
               | 'loading_message' ':' String NEWLINE
               | 'skeleton_screen' ':' Boolean NEWLINE
               | 'progress_bar' ':' Boolean NEWLINE

OptimisticUpdateDefinition ::= 'optimistic_update' ':' NEWLINE
                                INDENT OptimisticField+ DEDENT

OptimisticField ::= 'enabled' ':' Boolean NEWLINE
                  | 'fallback_on_error' ':' Boolean NEWLINE

RequestControlDefinition ::= 'request_control' ':' NEWLINE
                             INDENT RequestControlField+ DEDENT

RequestControlField ::= 'debounce_ms' ':' Integer NEWLINE
                      | 'throttle_ms' ':' Integer NEWLINE
                      | 'abort_on_navigation' ':' Boolean NEWLINE
```

### 4.9 安全性定義

```ebnf
SecurityDefinition ::= FieldLevelSecurity
                     | ActionLevelSecurity
                     | DataIsolationSecurity
                     | SecurityField SecurityDefinition

FieldLevelSecurity ::= 'field_level' ':' NEWLINE
                       INDENT FieldSecurityRule+ DEDENT

FieldSecurityRule ::= '- id' ':' FieldId NEWLINE
                      INDENT FieldSecurityFields DEDENT

FieldSecurityField ::= 'masking' ':' Boolean NEWLINE
                     | 'mask_type' ':' MaskType NEWLINE
                     | 'visible_to_roles' ':' RoleRefList NEWLINE
                     | 'editable_by_roles' ':' RoleRefList NEWLINE

MaskType ::= 'full' | 'partial' | 'none' | 'custom'

ActionLevelSecurity ::= 'action_level' ':' NEWLINE
                        INDENT ActionSecurityRule+ DEDENT

ActionSecurityRule ::= '- id' ':' ActionId NEWLINE
                       INDENT ActionSecurityFields DEDENT

ActionSecurityField ::= 'requires_roles' ':' RoleRefList NEWLINE
                      | 'requires_mfa' ':' Boolean NEWLINE
                      | 'requires_confirmation' ':' Boolean NEWLINE
                      | 'sensitive_operation' ':' Boolean NEWLINE

DataIsolationSecurity ::= 'data_isolation' ':' NEWLINE
                          INDENT DataIsolationField+ DEDENT

DataIsolationField ::= 'tenant_isolation' ':' Boolean NEWLINE
                     | 'user_isolation' ':' Boolean NEWLINE
                     | 'row_level_security' ':' Boolean NEWLINE
```

### 4.10 無障礙存取定義

```ebnf
AccessibilityDefinition ::= AriaConfiguration
                          | KeyboardNavigationConfig
                          | ScreenReaderConfig
                          | A11yField AccessibilityDefinition

AriaConfiguration ::= 'aria' ':' NEWLINE
                      INDENT AriaRule+ DEDENT

AriaRule ::= '- id' ':' FieldId NEWLINE
             INDENT AriaFields DEDENT

AriaField ::= 'label' ':' String NEWLINE
            | 'description' ':' String NEWLINE
            | 'role' ':' AriaRole NEWLINE
            | 'live' ':' AriaLive NEWLINE

AriaLive ::= 'off' | 'polite' | 'assertive'

KeyboardNavigationConfig ::= 'keyboard' ':' NEWLINE
                             INDENT KeyboardField+ DEDENT

KeyboardField ::= 'tab_order' ':' Integer NEWLINE
                | 'focus_trap' ':' Boolean NEWLINE
                | 'keyboard_shortcuts' ':' ShortcutList NEWLINE

ScreenReaderConfig ::= 'screen_reader' ':' NEWLINE
                       INDENT ScreenReaderField+ DEDENT

ScreenReaderField ::= 'skip_to_content' ':' Boolean NEWLINE
                    | 'announce_changes' ':' Boolean NEWLINE
                    | 'context_help' ':' String NEWLINE
```

### 4.11 測試性定義

```ebnf
TestingDefinition ::= SelectorStrategyDefinition
                    | MockDataDefinition
                    | GherkinIntegrationDefinition
                    | TestingField TestingDefinition

SelectorStrategyDefinition ::= 'selectors' ':' NEWLINE
                               INDENT SelectorRule+ DEDENT

SelectorRule ::= '- id' ':' ComponentId NEWLINE
                 INDENT SelectorFields DEDENT

SelectorField ::= 'data_testid' ':' String NEWLINE
                | 'aria_label' ':' String NEWLINE
                | 'css_selector' ':' String NEWLINE
                | 'xpath' ':' String NEWLINE

MockDataDefinition ::= 'mock_data' ':' NEWLINE
                       INDENT MockDataField+ DEDENT

MockDataField ::= 'fixture_file' ':' FilePath NEWLINE
                | 'default_dataset' ':' DatasetId NEWLINE

GherkinIntegrationDefinition ::= 'gherkin' ':' NEWLINE
                                 INDENT GherkinField+ DEDENT

GherkinField ::= 'feature_file' ':' FilePath NEWLINE
               | 'step_definitions' ':' FilePath NEWLINE
```

### 4.12 進階配置

```ebnf
AdvancedDefinition ::= PerformanceConfig
                     | CachingConfig
                     | PluginConfig
                     | AdvancedField AdvancedDefinition

PerformanceConfig ::= 'performance' ':' NEWLINE
                      INDENT PerformanceField+ DEDENT

PerformanceField ::= 'lazy_load' ':' Boolean NEWLINE
                   | 'virtualization' ':' Boolean NEWLINE
                   | 'batch_size' ':' Integer NEWLINE

CachingConfig ::= 'caching' ':' NEWLINE
                  INDENT CachingField+ DEDENT

CachingField ::= 'enabled' ':' Boolean NEWLINE
               | 'ttl_seconds' ':' Integer NEWLINE
               | 'cache_key' ':' String NEWLINE

PluginConfig ::= 'plugins' ':' PluginRefList
```

### 4.13 樣板與混入定義

```ebnf
TemplateDefinitionSection ::= 'templates' ':' NEWLINE
                              (INDENT TemplateDefinition+ DEDENT)?

TemplateDefinition ::= '- name' ':' TemplateId NEWLINE
                       INDENT TemplateFields DEDENT

TemplateField ::= 'page_type' ':' PageType NEWLINE
                | 'description' ':' String NEWLINE
                | 'default_view' ':' NEWLINE INDENT ViewDefinition DEDENT
                | 'default_actions' ':' NEWLINE INDENT ActionsDefinition DEDENT

MixinDefinitionSection ::= 'mixins' ':' NEWLINE
                           (INDENT MixinDefinition+ DEDENT)?

MixinDefinition ::= '- name' ':' MixinId NEWLINE
                    INDENT MixinFields DEDENT

MixinField ::= 'description' ':' String NEWLINE
             | 'provides' ':' NEWLINE INDENT (StateDefinition | ActionsDefinition) DEDENT
```

### 4.14 基本符號

```ebnf
Identifier ::= Letter (Letter | Digit | '_')*

PageId ::= Identifier
FieldRef ::= Identifier ('.' Identifier)*
FieldId ::= Identifier
EntityRef ::= Identifier
ApiRef ::= Identifier
ApiOperationName ::= Identifier
TemplateRef ::= Identifier
MixinRef ::= Identifier
StateVarId ::= Identifier
ActionId ::= Identifier
TemplateId ::= Identifier
MixinId ::= Identifier
ErrorHandlerId ::= Identifier
ComponentId ::= Identifier
DatasetId ::= Identifier

MixinRefList ::= '[' MixinRef (',' MixinRef)* ']'
RoleRefList ::= '[' String (',' String)* ']'
PluginRefList ::= '[' String (',' String)* ']'
ConditionList ::= '[' Condition (',' Condition)* ']'
ShortcutList ::= '[' KeyboardShortcut (',' KeyboardShortcut)* ']'

Condition ::= FieldName Operator FieldValue
FieldName ::= Identifier ('.' Identifier)*
Operator ::= '==' | '!=' | '<' | '>' | '<=' | '>=' | 'in' | 'contains' | 'matches'
FieldValue ::= String | Number | Boolean | Array

String ::= '"' StringContent '"'
Number ::= DigitSequence ('.' DigitSequence)?
Integer ::= DigitSequence
Boolean ::= 'true' | 'false'
Value ::= String | Number | Boolean | Array | Object
Array ::= '[' Value (',' Value)* ']'
Object ::= '{' KeyValuePair (',' KeyValuePair)* '}'
KeyValuePair ::= String ':' Value
ParamMap ::= Object
Expression ::= String  (* JavaScript 表達式 *)
Version ::= DigitSequence '.' DigitSequence ('.' DigitSequence)?
NamespaceId ::= Identifier ('.' Identifier)*
FilePath ::= String
CurrencyCode ::= 'TWD' | 'USD' | 'EUR' | 'JPY' | ...
SimpleType ::= 'string' | 'number' | 'boolean' | 'integer'
EnumValue ::= Identifier
KeyboardShortcut ::= String
AriaRole ::= String
IconId ::= String
MaskPattern ::= String
CustomPageType ::= Identifier
CustomDisplayType ::= Identifier
CustomFormat ::= Identifier
ErrorPattern ::= Identifier

NEWLINE ::= (* 換行符號 *)
INDENT ::= (* 增加縮排 *)
DEDENT ::= (* 減少縮排 *)
```

---

## 5. JSON Schema 定義

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://wa-raptor.example.com/hapdl/schema.json",
  "title": "HaPDL Schema",
  "description": "Schema for High-level Abstract Page Description Language v3.2",
  "type": "object",
  "required": ["metadata", "pages"],
  "additionalProperties": false,
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["schema_version"],
      "additionalProperties": false,
      "properties": {
        "schema_version": {
          "type": "string",
          "pattern": "^3\\.2(\\.\\d+)?$",
          "description": "HaPDL 規格版本（必須為 3.2.x）"
        },
        "title": {
          "type": "string",
          "minLength": 1,
          "description": "頁面集合標題"
        },
        "version": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+(\\.\\d+)?$",
          "description": "文檔版本"
        },
        "description": {
          "type": "string",
          "description": "文檔描述"
        },
        "namespace": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*(\\.[a-zA-Z_][a-zA-Z0-9_]*)*$",
          "description": "命名空間"
        }
      }
    },
    "pages": {
      "type": "array",
      "items": { "$ref": "#/definitions/Page" },
      "minItems": 1,
      "description": "頁面定義清單"
    },
    "templates": {
      "type": "array",
      "items": { "$ref": "#/definitions/Template" },
      "description": "可重用的頁面樣板"
    },
    "mixins": {
      "type": "array",
      "items": { "$ref": "#/definitions/Mixin" },
      "description": "可混入的功能模組"
    }
  },
  "definitions": {
    "Page": {
      "type": "object",
      "required": ["page", "type", "entity"],
      "additionalProperties": false,
      "properties": {
        "page": {
          "type": "string",
          "pattern": "^[a-z0-9]([a-z0-9-]*[a-z0-9])?$",
          "description": "頁面唯一識別碼（kebab-case）"
        },
        "type": {
          "type": "string",
          "enum": [
            "list", "form", "detail", "master-detail", "explorer",
            "dashboard", "wizard", "search", "report", "hybrid",
            "kanban", "calendar"
          ],
          "description": "頁面類型"
        },
        "title": { "type": "string", "minLength": 1, "description": "頁面標題" },
        "entity": {
          "type": "string",
          "pattern": "^[A-Za-z_][a-zA-Z0-9_]*$",
          "description": "主要實體名稱（來自 DBML）"
        },
        "api": {
          "type": "string",
          "pattern": "^[a-z0-9]([a-z0-9-]*[a-z0-9])?$",
          "description": "綁定的 haAPI 定義名稱"
        },
        "extends": { "type": "string", "description": "繼承的樣板識別碼" },
        "mixins": {
          "type": "array",
          "items": { "type": "string" },
          "description": "混入的功能模組 ID"
        },
        "view": { "$ref": "#/definitions/View" },
        "state": { "$ref": "#/definitions/State" },
        "actions": { "$ref": "#/definitions/Actions" },
        "error_handling": { "$ref": "#/definitions/ErrorHandling" },
        "async": { "$ref": "#/definitions/Async" },
        "security": { "$ref": "#/definitions/Security" },
        "accessibility": { "$ref": "#/definitions/Accessibility" },
        "testing": { "$ref": "#/definitions/Testing" },
        "advanced": { "$ref": "#/definitions/Advanced" }
      }
    },
    "View": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "filters": {
          "type": "array",
          "items": { "$ref": "#/definitions/FilterItem" },
          "description": "篩選欄位定義"
        },
        "columns": {
          "type": "array",
          "items": { "$ref": "#/definitions/ColumnItem" },
          "description": "顯示欄位定義"
        },
        "fields": {
          "type": "array",
          "items": { "$ref": "#/definitions/FieldItem" },
          "description": "表單欄位定義"
        },
        "layout": {
          "type": "string",
          "enum": ["single-column", "two-column", "three-column", "grid"],
          "description": "佈局方式"
        }
      }
    },
    "FilterItem": {
      "type": "object",
      "required": ["name"],
      "additionalProperties": false,
      "properties": {
        "name": { "type": "string", "description": "欄位名稱或 'keyword'" },
        "operator": {
          "type": "string",
          "enum": ["~", "=", ">", "<", "><", "[]", "@", "?", ""],
          "description": "篩選操作符"
        },
        "type": { "type": "string", "description": "推斷的資料類型" },
        "label": { "type": "string", "description": "自訂標籤" },
        "null_label": { "type": "string", "description": "可空值篩選標籤" }
      }
    },
    "ColumnItem": {
      "type": "object",
      "required": ["name"],
      "additionalProperties": false,
      "properties": {
        "name": { "type": "string", "description": "欄位名稱" },
        "modifier": {
          "type": "string",
          "enum": ["!", "?", "^", "&", ""],
          "description": "欄位修飾符"
        },
        "type": { "type": "string", "description": "顯示類型" },
        "format": { "type": "string", "description": "格式化方式" },
        "label": { "type": "string", "description": "自訂欄位標籤" },
        "width": { "type": "string", "description": "欄寬（CSS 值）" },
        "sortable": { "type": "boolean", "description": "是否可排序" },
        "groupable": { "type": "boolean", "description": "是否可群組" },
        "hideable": { "type": "boolean", "description": "是否可隱藏" }
      }
    },
    "FieldItem": {
      "type": "object",
      "required": ["name"],
      "additionalProperties": false,
      "properties": {
        "name": { "type": "string", "description": "欄位名稱" },
        "modifier": {
          "type": "string",
          "enum": ["!", "?", "#", "*", "@", "[]", "{}", "~", "<~", ""],
          "description": "欄位修飾符"
        },
        "type": { "type": "string", "description": "輸入類型" },
        "required": { "type": "boolean", "description": "是否必填" },
        "readonly": { "type": "boolean", "description": "是否唯讀" },
        "sensitive": { "type": "boolean", "description": "是否敏感（遮罩）" },
        "label": { "type": "string", "description": "自訂標籤" },
        "placeholder": { "type": "string", "description": "佔位符" },
        "validation": { "type": "object", "description": "驗證規則" },
        "cascade_source": { "type": "string", "description": "連動來源欄位" },
        "cascade_target": {
          "type": "array",
          "items": { "type": "string" },
          "description": "連動目標欄位"
        }
      }
    },
    "State": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "local": {
          "type": "array",
          "items": { "$ref": "#/definitions/StateVariable" },
          "description": "頁面內部狀態"
        },
        "shared": {
          "type": "array",
          "items": { "$ref": "#/definitions/SharedState" },
          "description": "跨頁面共享狀態"
        },
        "cascading": {
          "type": "array",
          "items": { "$ref": "#/definitions/CascadingConfig" },
          "description": "欄位連動配置"
        },
        "persistence": {
          "type": "array",
          "items": { "$ref": "#/definitions/PersistenceConfig" },
          "description": "狀態持久化配置"
        },
        "computed": {
          "type": "array",
          "items": { "$ref": "#/definitions/ComputedProperty" },
          "description": "計算屬性"
        },
        "watchers": {
          "type": "array",
          "items": { "$ref": "#/definitions/Watcher" },
          "description": "狀態監聽器"
        }
      }
    },
    "StateVariable": {
      "type": "object",
      "required": ["name", "type"],
      "additionalProperties": false,
      "properties": {
        "name": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
          "description": "狀態變數名稱"
        },
        "type": { "type": "string", "description": "資料類型" },
        "default": {},
        "description": { "type": "string" },
        "max_length": { "type": "integer" },
        "min_value": { "type": "number" },
        "max_value": { "type": "number" },
        "derived": { "type": "string", "description": "衍生表達式" },
        "scope": {
          "type": "string",
          "enum": ["ui", "data"],
          "description": "狀態範圍"
        }
      }
    },
    "SharedState": {
      "type": "object",
      "required": ["name", "type"],
      "additionalProperties": false,
      "properties": {
        "name": { "type": "string", "description": "共享狀態名稱" },
        "type": { "type": "string", "description": "資料類型" },
        "scope": {
          "type": "string",
          "enum": ["session", "user", "workspace"],
          "description": "共享範圍"
        },
        "ttl_seconds": { "type": "integer", "description": "生存時間（秒）" }
      }
    },
    "CascadingConfig": {
      "type": "object",
      "required": ["source", "targets"],
      "additionalProperties": false,
      "properties": {
        "source": { "type": "string", "description": "來源欄位" },
        "targets": {
          "type": "array",
          "items": { "type": "string" },
          "description": "目標欄位"
        },
        "strategy": {
          "type": "string",
          "enum": ["clear", "filter", "reload"],
          "description": "連動策略"
        },
        "api_operation": { "type": "string", "description": "用於重新載入的 API 操作" }
      }
    },
    "PersistenceConfig": {
      "type": "object",
      "required": ["state_var"],
      "additionalProperties": false,
      "properties": {
        "state_var": { "type": "string", "description": "狀態變數名稱" },
        "storage": {
          "type": "string",
          "enum": ["local", "session"],
          "description": "儲存位置"
        },
        "key": { "type": "string", "description": "儲存鑰匙" }
      }
    },
    "ComputedProperty": {
      "type": "object",
      "required": ["name", "expression"],
      "additionalProperties": false,
      "properties": {
        "name": { "type": "string", "description": "計算屬性名稱" },
        "expression": { "type": "string", "description": "計算表達式" },
        "dependencies": {
          "type": "array",
          "items": { "type": "string" },
          "description": "依賴的狀態變數"
        }
      }
    },
    "Watcher": {
      "type": "object",
      "required": ["target", "handler"],
      "additionalProperties": false,
      "properties": {
        "target": { "type": "string", "description": "監聽目標" },
        "handler": { "type": "string", "description": "處理函數" },
        "deep": { "type": "boolean", "description": "深度監聽" },
        "immediate": { "type": "boolean", "description": "立即觸發" }
      }
    },
    "Actions": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "standard": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["create", "read", "update", "delete"]
          },
          "description": "標準 CRUD 動作"
        },
        "operations": {
          "type": "array",
          "items": { "type": "string" },
          "description": "haAPI 操作引用"
        },
        "custom": {
          "type": "array",
          "items": { "$ref": "#/definitions/CustomAction" },
          "description": "自訂動作"
        }
      }
    },
    "CustomAction": {
      "type": "object",
      "required": ["name", "type"],
      "additionalProperties": false,
      "properties": {
        "name": { "type": "string", "description": "動作名稱" },
        "operation": { "type": "string", "description": "引用的 haAPI 操作" },
        "type": {
          "type": "string",
          "enum": ["submit", "button", "navigate", "reset"],
          "description": "動作類型"
        },
        "label": { "type": "string", "description": "按鈕標籤" },
        "icon": { "type": "string", "description": "圖示" },
        "variant": { "type": "string", "description": "視覺變體" },
        "params": { "type": "object", "description": "額外參數" },
        "async_ui": { "type": "object", "description": "非同步 UI 配置" },
        "error_handling": { "type": "object", "description": "錯誤處理配置" },
        "confirmation": { "type": "object", "description": "確認對話框配置" },
        "conditions": { "type": "array", "description": "顯示條件" }
      }
    },
    "ErrorHandling": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "default_strategy": {
          "type": "string",
          "enum": ["retry", "fallback", "dismiss", "custom"],
          "description": "預設錯誤策略"
        },
        "handlers": {
          "type": "array",
          "items": { "$ref": "#/definitions/ErrorHandler" },
          "description": "自訂錯誤處理器"
        }
      }
    },
    "ErrorHandler": {
      "type": "object",
      "required": ["id"],
      "additionalProperties": false,
      "properties": {
        "id": { "type": "string", "description": "錯誤處理器識別碼" },
        "error_code": {
          "oneOf": [{ "type": "integer" }, { "type": "string" }],
          "description": "HTTP 狀態碼或錯誤模式"
        },
        "error_type": {
          "type": "string",
          "enum": ["validation", "network", "authorization", "not_found", "conflict", "timeout", "custom"],
          "description": "錯誤類型"
        },
        "strategy": { "type": "string", "description": "處理策略" },
        "message": { "type": "string", "description": "日誌訊息" },
        "user_message": { "type": "string", "description": "使用者看到的訊息" },
        "retry_count": { "type": "integer", "description": "重試次數" },
        "fallback_value": {},
        "offline_mode": { "type": "boolean", "description": "離線支援" }
      }
    },
    "Async": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "ui": { "type": "object", "description": "非同步 UI 配置" },
        "optimistic_update": { "type": "object", "description": "樂觀更新配置" },
        "request_control": { "type": "object", "description": "請求控制配置" }
      }
    },
    "Security": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "field_level": {
          "type": "array",
          "items": { "$ref": "#/definitions/FieldSecurity" },
          "description": "欄位級安全"
        },
        "action_level": {
          "type": "array",
          "items": { "$ref": "#/definitions/ActionSecurity" },
          "description": "動作級安全"
        },
        "data_isolation": { "type": "object", "description": "資料隔離" }
      }
    },
    "FieldSecurity": {
      "type": "object",
      "required": ["id"],
      "additionalProperties": false,
      "properties": {
        "id": { "type": "string", "description": "欄位名稱" },
        "masking": { "type": "boolean", "description": "是否遮罩" },
        "mask_type": {
          "type": "string",
          "enum": ["full", "partial", "none"],
          "description": "遮罩類型"
        },
        "visible_to_roles": {
          "type": "array",
          "items": { "type": "string" },
          "description": "可見角色"
        },
        "editable_by_roles": {
          "type": "array",
          "items": { "type": "string" },
          "description": "可編輯角色"
        }
      }
    },
    "ActionSecurity": {
      "type": "object",
      "required": ["id"],
      "additionalProperties": false,
      "properties": {
        "id": { "type": "string", "description": "動作名稱" },
        "requires_roles": {
          "type": "array",
          "items": { "type": "string" },
          "description": "所需角色"
        },
        "requires_mfa": { "type": "boolean", "description": "需要多因素認證" },
        "requires_confirmation": { "type": "boolean", "description": "需要確認" },
        "sensitive_operation": { "type": "boolean", "description": "是否敏感操作" }
      }
    },
    "Accessibility": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "aria": {
          "type": "array",
          "items": { "$ref": "#/definitions/AriaConfig" },
          "description": "ARIA 配置"
        },
        "keyboard": { "type": "object", "description": "鍵盤導覽配置" },
        "screen_reader": { "type": "object", "description": "螢幕閱讀器配置" }
      }
    },
    "AriaConfig": {
      "type": "object",
      "required": ["id"],
      "additionalProperties": false,
      "properties": {
        "id": { "type": "string", "description": "元件識別碼" },
        "label": { "type": "string", "description": "ARIA 標籤" },
        "description": { "type": "string", "description": "ARIA 描述" },
        "role": { "type": "string", "description": "ARIA 角色" },
        "live": {
          "type": "string",
          "enum": ["off", "polite", "assertive"],
          "description": "ARIA live 屬性"
        }
      }
    },
    "Testing": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "selectors": {
          "type": "array",
          "items": { "$ref": "#/definitions/SelectorConfig" },
          "description": "測試選擇器"
        },
        "mock_data": { "type": "object", "description": "Mock 資料配置" },
        "gherkin": { "type": "object", "description": "Gherkin 整合配置" }
      }
    },
    "SelectorConfig": {
      "type": "object",
      "required": ["id"],
      "additionalProperties": false,
      "properties": {
        "id": { "type": "string", "description": "組件識別碼" },
        "data_testid": { "type": "string", "description": "data-testid 屬性" },
        "aria_label": { "type": "string", "description": "ARIA 標籤" },
        "css_selector": { "type": "string", "description": "CSS 選擇器" },
        "xpath": { "type": "string", "description": "XPath 表達式" }
      }
    },
    "Advanced": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "performance": { "type": "object", "description": "性能優化" },
        "caching": { "type": "object", "description": "快取策略" },
        "plugins": {
          "type": "array",
          "items": { "type": "string" },
          "description": "插件引用"
        }
      }
    },
    "Template": {
      "type": "object",
      "required": ["name", "page_type"],
      "additionalProperties": false,
      "properties": {
        "name": { "type": "string", "description": "樣板名稱" },
        "page_type": { "type": "string", "description": "頁面類型" },
        "description": { "type": "string", "description": "樣板描述" },
        "default_view": { "$ref": "#/definitions/View" },
        "default_actions": { "$ref": "#/definitions/Actions" }
      }
    },
    "Mixin": {
      "type": "object",
      "required": ["name"],
      "additionalProperties": false,
      "properties": {
        "name": { "type": "string", "description": "混入名稱" },
        "description": { "type": "string", "description": "功能描述" },
        "provides": { "type": "object", "description": "提供的功能（state/actions/etc）" }
      }
    }
  }
}
```

---

## 6. 語義規則表

### 6.1 頁面定義（Page Definition）

| 字段 | 類型 | 必需 | 有效值 | 說明 |
|------|------|:----:|--------|------|
| page | String | Y | kebab-case | 頁面唯一識別碼 |
| type | String | Y | 見 6.2 PageType | 頁面類型 |
| title | String | Y | — | 顯示標題 |
| entity | String | Y | EntityName | DBML 實體名稱 |
| api | String | — | haapi-name | 綁定的 haAPI 定義名稱 (v3.1+) |
| extends | String | — | template-name | 繼承的樣板 |
| mixins | Array | — | [mixin-ids] | 混入的功能模組 |
| view | View | — | — | 視圖定義 |
| state | State | — | — | 狀態管理 |
| actions | Actions | — | — | 動作定義 |
| error_handling | ErrorHandling | — | — | 錯誤處理 |
| async | Async | — | — | 非同步行為 |
| security | Security | — | — | 安全性 |
| accessibility | Accessibility | — | — | 無障礙存取 |
| testing | Testing | — | — | 測試性 |
| advanced | Advanced | — | — | 進階配置 |

### 6.2 頁面類型說明

| 類型 | 用途 | 特徵 | 預設動作 |
|------|------|------|----------|
| **list** | 列表頁 | 多筆資料展示 + 篩選 + 分頁 | create, read, update, delete |
| **form** | 表單頁 | 資料新增/編輯 | create/update |
| **detail** | 詳情頁 | 單筆資料檢視 | read, update |
| **master-detail** | 主從頁 | 主記錄 + 明細列表 | CRUD x 2 |
| **explorer** | 樹狀導覽 | 階層樹 + 內容面板 | read, expand |
| **dashboard** | 儀表板 | 統計圖表 + 指標 | read |
| **wizard** | 精靈頁 | 多步驟流程 | create, validate |
| **search** | 搜尋頁 | 進階搜尋條件 | read |
| **report** | 報表頁 | 資料分析 + 匯出 | read, export |
| **hybrid** | 混合頁 | 多種功能組合 | custom |
| **kanban** | 看板頁 | 拖放式狀態管理 (v3.0+) | update (drag) |
| **calendar** | 日曆頁 | 時間軸檢視 (v3.0+) | create, update |

### 6.3 欄位修飾符

#### 6.3.1 篩選欄位修飾符 (filters)

| 修飾符 | 名稱 | 效果 | 適用類型 | 範例 |
|--------|------|------|----------|------|
| `~` | 模糊搜尋 | 使用 LIKE/contains | text, varchar | `username~` |
| `=` | 精確匹配 | 使用 = | all | `status=` |
| `>` | 大於 | > 比較 | number, date | `price>` |
| `<` | 小於 | < 比較 | number, date | `score<` |
| `><` | 區間篩選 | 雙邊界 (v3.0+) | number, date | `amount><` |
| `[]` | 多選篩選 | IN 操作 | enum, ref | `status[]` |
| `@` | 特殊格式 | email/url 驗證 | text | `email@` |
| `?` | 可空值篩選 | IS NULL 篩選 (v3.0+) | nullable | `nickname?` |

#### 6.3.2 顯示欄位修飾符 (columns)

| 修飾符 | 效果 | 範例 |
|--------|------|------|
| `!` | 粗體強調 | `status!` |
| `?` | 可隱藏（hideable） | `description?` |
| `^` | 可排序 (v3.0+) | `created_at^` |
| `&` | 可群組 (v3.0+) | `category&` |

#### 6.3.3 表單欄位修飾符 (fields)

| 修飾符 | 效果 | 範例 |
|--------|------|------|
| `!` | 必填 (required) | `email!` |
| `?` | 選填 (optional) | `nickname?` |
| `#` | 唯讀 (readonly) | `id#` |
| `*` | 敏感/遮罩 (mask) | `password*` |
| `@` | Email 格式 (validation) | `contact@` |
| `[]` | 多選 (select-multiple) | `tags[]` |
| `{}` | JSON 物件 (json-editor) | `metadata{}` |
| `~` | 連動來源 (cascading source) (v3.0+) | `country~` |
| `<~` | 連動目標 (cascading target) (v3.0+) | `city<~` |

> **`?` 符號語意消歧** (v3.1)：`?` 的意義取決於所在區塊：
> - `view.filters` 中：**可空值篩選**，展開為 `nullable: true` + `null_label`
> - `view.columns` 中：**可藏欄位**，展開為 `hideable: true`
> - `view.fields` 中：**選填欄位**，展開為 `required: false`

### 6.4 顯示類型 (:type)

| 類型 | 搭配欄位 | 渲染方式 | 範例 |
|------|----------|----------|------|
| `badge` | status, priority | 彩色徽章 | `status:badge` |
| `image` | avatar, image | 圖片預覽 | `avatar:image` |
| `currency` | price, amount | 貨幣符號 | `price:currency` |
| `bar` | progress, percentage | 進度條 | `progress:bar` |
| `stars` | rating | 星級評分 | `rating:stars` |
| `toggle` | active, enabled | 開關狀態 | `active:toggle` |
| `chips` | tags, categories | 標籤群組 | `tags:chips` |
| `truncate(n)` | long text | 截斷文字 | `description:truncate(100)` |
| `map` | coordinates | 地圖座標 (v3.0+) | `location:map` |
| `swatch` | color | 色彩選擇器 (v3.0+) | `color:swatch` |
| `attachment` | file | 檔案附件 (v3.0+) | `document:attachment` |
| `avatar-name` | user | 使用者頭像+名稱 (v3.0+) | `creator:avatar-name` |
| `change-track` | delta | 變更追蹤 (v3.0+) | `diff:change-track` |
| `tree` | json | JSON 樹狀檢視 (v3.0+) | `config:tree` |
| `rendered` | markdown | Markdown 渲染 (v3.0+) | `description:rendered` |
| `highlight` | code | 程式碼高亮 (v3.0+) | `script:highlight` |

### 6.5 格式化 (|format)

| 格式 | 類型 | 效果 | 範例輸出 |
|------|------|------|----------|
| `date` | datetime | YYYY-MM-DD | `2026-04-02` |
| `datetime` | datetime | YYYY-MM-DD HH:mm:ss | `2026-04-02 14:30:00` |
| `time` | datetime | HH:mm | `14:30` |
| `relative` | datetime | 相對時間 (v3.0+) | `3 天後` |
| `humanize` | datetime | 人性化時間 | `2 小時前` |
| `number(n)` | numeric | 小數位數 | `123.45` |
| `percent` | numeric | 百分比 | `85%` |
| `bytes` | numeric | 檔案大小 | `1.2 MB` |
| `compact` | numeric | 緊湊數字 (v3.0+) | `1.2K` |
| `currency(code)` | numeric | 指定幣別 (v3.0+) | `TWD 1,000` |
| `uppercase` | text | 大寫 (v3.0+) | `ABC` |
| `lowercase` | text | 小寫 (v3.0+) | `abc` |
| `capitalize` | text | 首字大寫 (v3.0+) | `Hello` |
| `mask(pattern)` | text | 遮罩格式 (v3.0+) | `XXX-XXX-1234` |

### 6.6 狀態定義（State Definition）

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| **local** | Array&lt;StateVariable&gt; | — | 頁面內部狀態 |
| **shared** | Array&lt;SharedState&gt; | — | 跨頁面共享狀態 |
| **cascading** | Array&lt;CascadingConfig&gt; | — | 欄位連動配置 |
| **persistence** | Array&lt;PersistenceConfig&gt; | — | 狀態持久化 |
| **computed** | Array&lt;ComputedProperty&gt; | — | 計算屬性 |
| **watchers** | Array&lt;Watcher&gt; | — | 狀態監聽 |

#### StateVariable 子字段

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| name | String | Y | 變數名稱（camelCase） |
| type | String | Y | boolean, string, number, array, object, enum, EntityRef |
| default | Value | — | 預設值 |
| max_length | Integer | — | 陣列最大長度 |
| min_value | Number | — | 最小值 |
| max_value | Number | — | 最大值 |
| derived | Expression | — | JavaScript 衍生表達式 |
| scope | String | — | `ui` 或 `data` |

#### SharedState 子字段

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| name | String | Y | 共享狀態名稱 |
| type | String | Y | 資料類型 |
| scope | String | Y | `session` / `user` / `workspace` |
| ttl_seconds | Integer | — | 生存時間（秒） |

#### CascadingConfig 子字段

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| source | String | Y | 來源欄位 |
| targets | Array | Y | 目標欄位陣列 |
| strategy | String | Y | `clear` / `filter` / `reload` |
| api_operation | String | — | 用於重新載入的操作 |

#### ComputedProperty 子字段

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| name | String | Y | 計算屬性名稱 |
| expression | String | Y | 計算表達式 |
| dependencies | Array | — | 依賴的狀態變數 |

#### Watcher 子字段

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| target | String | Y | 監聽目標 |
| handler | String | Y | 處理函數 |
| deep | Boolean | — | 深度監聽 |
| immediate | Boolean | — | 立即觸發 |

### 6.7 動作定義（Actions Definition）

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| standard | Array | — | `['create', 'read', 'update', 'delete']` |
| operations | Array | — | haAPI 操作名稱清單 (v3.1+) |
| custom | Array&lt;CustomAction&gt; | — | 自訂動作 |

#### 標準動作在 form 頁面的展開規則 (v3.2.1)

**standard: [create] 自動展開：**

| 按鈕 | type | variant | label |
|------|------|---------|-------|
| save | submit | primary | "新增儲存" |
| reset | reset | secondary | "清除重填" |
| cancel | navigate | — | "返回" |

**standard: [update] 自動展開：**

| 按鈕 | type | variant | label |
|------|------|---------|-------|
| save | submit | primary | "儲存" |
| reset | reset | secondary | "還原" |
| cancel | navigate | — | "返回" |

- `cancel.route` 由 Convention 從 entity 推斷：`/{entity-kebab}/list`
- `variant` 屬於 PDL 層，haPDL 中無需指定
- 如需覆寫個別按鈕，使用 `actions.custom` 區塊

#### CustomAction 子字段

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| name | String | Y | 動作識別碼 |
| operation | String | — | 引用的 haAPI 操作名稱 (v3.1+) |
| type | String | Y | `submit` / `button` / `navigate` / `reset` |
| label | String | — | 按鈕顯示文字 |
| icon | String | — | 圖示標識符 |
| variant | String | — | UI 樣式變體 |
| params | Object | — | 額外參數映射 |
| async_ui | Object | — | 非同步 UI 配置 |
| error_handling | Object | — | 錯誤處理配置 |
| confirmation | Object | — | 確認對話框 |
| conditions | Array | — | 顯示條件陣列 |

### 6.8 錯誤處理（Error Handling）

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| default_strategy | String | — | `retry` / `fallback` / `dismiss` / `custom` |
| handlers | Array&lt;ErrorHandler&gt; | — | 自訂處理器 |

#### ErrorHandler 子字段

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| id | String | Y | 處理器識別碼 |
| error_code | Int/String | — | HTTP 狀態碼或錯誤模式 |
| error_type | String | — | `validation` / `network` / `authorization` / `not_found` / `conflict` / `timeout` / `custom` |
| strategy | String | Y | 錯誤處理策略 |
| message | String | — | 日誌訊息 |
| user_message | String | — | 使用者看到的訊息 |
| retry_count | Integer | — | 重試次數（預設 3） |
| fallback_value | Value | — | 降級值 |
| offline_mode | Boolean | — | 離線支援 |

### 6.9 非同步行為（Async）

#### AsyncUI 子字段

| 字段 | 類型 | 有效值 | 說明 |
|------|------|--------|------|
| loading_indicator | String | `spinner` / `skeleton` / `bar` | 載入指示器類型 |
| loading_message | String | — | 載入提示訊息 |
| skeleton_screen | Boolean | true / false | 骨架屏支援 |
| progress_bar | Boolean | true / false | 進度條顯示 |

#### OptimisticUpdate 子字段

| 字段 | 類型 | 說明 |
|------|------|------|
| enabled | Boolean | 是否啟用樂觀更新 |
| fallback_on_error | Boolean | 錯誤時回滾 |

#### RequestControl 子字段

| 字段 | 類型 | 說明 |
|------|------|------|
| debounce_ms | Integer | 防抖延遲（毫秒） |
| throttle_ms | Integer | 節流延遲（毫秒） |
| abort_on_navigation | Boolean | 導覽時中止請求 |

### 6.10 安全性（Security）

#### FieldSecurity 子字段

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| id | String | Y | 欄位名稱 |
| masking | Boolean | — | 是否遮罩 |
| mask_type | String | — | `full` / `partial` / `none` / `custom` |
| visible_to_roles | Array | — | 可見角色清單 |
| editable_by_roles | Array | — | 可編輯角色清單 |

> **敏感欄位合併規則** (v3.1)：DBML `sensitive: true` 或 haPDL `fieldName*` → 自動遮罩。haPDL `*` 可覆寫 DBML 定義。

#### ActionSecurity 子字段

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| id | String | Y | 動作名稱 |
| requires_roles | Array | — | 所需角色清單 |
| requires_mfa | Boolean | — | 需要多因素認證 |
| requires_confirmation | Boolean | — | 需要確認對話框 |
| sensitive_operation | Boolean | — | 敏感操作標記 |

#### DataIsolation 子字段

| 字段 | 類型 | 說明 |
|------|------|------|
| tenant_isolation | Boolean | 多租戶隔離 |
| user_isolation | Boolean | 使用者級隔離 |
| row_level_security | Boolean | 行級安全 |

### 6.11 無障礙存取（Accessibility）

#### ARIA 配置

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| id | String | Y | 元件識別碼 |
| label | String | — | ARIA label |
| description | String | — | ARIA description |
| role | String | — | ARIA role |
| live | String | — | `off` / `polite` / `assertive` |

> **accessibility 預設推斷** (v3.2.1)：`accessibility.aria` 的 label 可由 `title` + `type` 自動推斷。例如 list 頁面自動產生 "{title}列表"。`keyboard.enabled` 預設為 `true`。

#### 鍵盤導覽

| 字段 | 類型 | 說明 |
|------|------|------|
| tab_order | Integer | 聚焦順序 |
| focus_trap | Boolean | 模態框焦點困陷 |
| keyboard_shortcuts | Array | 快捷鍵映射 |

#### 螢幕閱讀器

| 字段 | 類型 | 說明 |
|------|------|------|
| skip_to_content | Boolean | 跳至內容連結 |
| announce_changes | Boolean | 宣告動態變更 |
| context_help | String | 內容幫助文字 |

### 6.12 測試性（Testing）

#### 選擇器策略

| 字段 | 類型 | 優先級 | 說明 |
|------|------|--------|------|
| data_testid | String | 1 (最高) | data-testid 屬性 |
| aria_label | String | 2 | ARIA 標籤 |
| css_selector | String | 3 | CSS 選擇器 |
| xpath | String | 4 (最低) | XPath 表達式 |

#### Mock 資料

| 字段 | 類型 | 說明 |
|------|------|------|
| fixture_file | String | Fixture 檔案路徑 |
| default_dataset | String | 預設資料集識別碼 |

#### Gherkin 整合

| 字段 | 類型 | 說明 |
|------|------|------|
| feature_file | String | .feature 檔案路徑 |
| step_definitions | String | Step 定義檔案路徑 |

---

## 7. 基礎語法規格

### 7.1 頁面基本結構

```yaml
# ===== 頁面識別 =====
page: <page-identifier>        # kebab-case 格式
type: <page-type>              # 頁面類型
title: <page-title>            # 顯示標題
entity: <EntityName>           # 主要實體（來自 DBML）
api: <haapi-name>              # haAPI 定義名稱（可選）

# ===== 擴展與版本 =====
extends: <template-name>       # 繼承模板（可選）
mixins: [<mixin-names>]        # 混入功能（可選）
version: <version-number>      # 版本號（可選）
schema_version: "3.2"          # haPDL 規格版本

# ===== 各維度定義 =====
view:                          # 視圖定義
  <view-configurations>
state:                         # 狀態管理
  <state-configurations>
actions:                       # 動作定義
  <action-configurations>
error_handling:                # 錯誤處理
  <error-configurations>
async:                         # 非同步行為
  <async-configurations>
accessibility:                 # 無障礙存取
  <a11y-configurations>
security:                      # 安全性
  <security-configurations>
testing:                       # 測試性
  <testing-configurations>
advanced:                      # 進階配置
  <advanced-settings>
```

> **Defaults vs extends/mixins** (v3.2.1)：Page Type Defaults 是轉換器內建的慣例預設值，無需宣告。`extends` 用於跨頁面的自訂模板繼承。`mixins` 用於可重用的功能片段混入。

### 7.2 簡潔欄位語法

```yaml
view:
  # ===== 篩選欄位 =====
  filters:
    - fieldName         # 基本篩選
    - fieldName~        # 模糊搜尋
    - fieldName=        # 精確匹配
    - fieldName>        # 大於
    - fieldName<        # 小於
    - fieldName><       # 區間篩選
    - fieldName[]       # 多選篩選
    - fieldName@        # 特殊格式
    - fieldName?        # 可空值篩選
    - keyword~          # 全文搜尋（保留名稱）

  # ===== 顯示欄位 =====
  columns:
    - fieldName         # 基本顯示
    - fieldName!        # 強調
    - fieldName?        # 可隱藏
    - fieldName:type    # 指定顯示類型
    - fieldName|format  # 指定格式化
    - fieldName^        # 可排序
    - fieldName&        # 可群組

  # ===== 表單欄位 =====
  fields:
    - fieldName         # 基本輸入
    - fieldName!        # 必填
    - fieldName?        # 選填
    - fieldName#        # 唯讀
    - fieldName*        # 敏感
    - fieldName@        # Email
    - fieldName[]       # 多選
    - fieldName{}       # JSON
    - fieldName~        # 連動來源
    - fieldName<~       # 連動目標
```

> **`keyword` 保留名稱** (v3.2.1)：`keyword` 是保留的虛擬 filter 名稱，代表「全文搜尋框」。它不對應 entity 的實體欄位，透過 `api:` 綁定查找 haAPI 的 `search.fields` 取得搜尋目標欄位。若未綁定 haAPI，Convention 預設搜尋 entity 中所有 text 類型欄位。

> **sensitive 合併規則** (v3.1)：敏感欄位判定 = DBML `sensitive: true` ∪ haPDL `fieldName*` 符號。即使 haPDL 中未使用 `*` 符號，若 DBML 對應欄位有 `sensitive: true`，轉換器仍應在 PDL 輸出中自動啟用遮罩。

---

## 8. 狀態管理系統

### 8.1 概觀

```yaml
state:
  local:       # 頁面內部狀態
  shared:      # 跨頁面共享狀態
  cascading:   # 欄位連動
  persistence: # 狀態持久化
  computed:    # 計算屬性
  watchers:    # 狀態監聽
```

### 8.2 頁面內部狀態

```yaml
state:
  local:
    - name: isEditing
      type: boolean
      default: false

    - name: selectedItems
      type: array<string>
      default: []
      max_length: 100

    - name: hasSelection
      derived: "selectedItems.length > 0"

    - name: expandedRows
      type: set<string>
      scope: ui  # 不影響資料層
```

### 8.3 跨頁面共享狀態

```yaml
state:
  shared:
    - name: currentWorkspace
      type: Workspace
      scope: session
      description: "當前工作區，跨頁面共享"

    - name: userPreferences
      type: UserPreferences
      scope: user
      sync: true  # 跨分頁同步

    - name: orderDraft
      type: Order
      scope: workflow
      workflow_id: create-order
      ttl: 3600
```

### 8.4 欄位連動（Cascading）

```yaml
state:
  cascading:
    # 基本連動
    - trigger: city
      target: district
      source: "api:/regions?city_id={city.id}"
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
```

### 8.5 狀態持久化

```yaml
state:
  persistence:
    filters:
      storage: sessionStorage
      key: "{page}-filters"
      include: [status, dateRange, keyword]
      ttl: 86400

    pagination:
      storage: localStorage
      key: "user-pagination-prefs"
```

### 8.6 計算屬性

```yaml
state:
  computed:
    - name: totalAmount
      expression: "items.reduce((sum, item) => sum + item.subtotal, 0)"
      dependencies: [items]

    - name: shippingFee
      async: true
      expression: "api:/shipping/calculate?total={totalAmount}&zip={zipCode}"
      dependencies: [totalAmount, zipCode]
      debounce: 500
```

### 8.7 狀態監聽器

```yaml
state:
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
```

---

## 9. 錯誤處理框架

### 9.1 驗證錯誤

```yaml
error_handling:
  validation:
    display:
      mode: inline          # inline | summary | toast | modal
      scroll_to_first: true
      highlight_field: true
    timing:
      on_blur: true
      on_submit: true
      debounce: 300
    messages:
      required: "{field} 為必填欄位"
      email: "請輸入有效的電子郵件地址"
```

### 9.2 API 錯誤

```yaml
error_handling:
  api:
    status_handlers:
      401:
        action: redirect
        target: "/login"
        message: "登入已過期"
      403:
        action: display
        display_mode: modal
        message: "您沒有權限執行此操作"
      409:
        action: display
        display_mode: modal
        message: "資料已被其他人修改"
        actions:
          - label: "重新載入"
            action: reload
          - label: "保留我的變更"
            action: force_save
      500:
        action: display
        message: "伺服器發生錯誤"
        show_error_id: true
```

### 9.3 網路錯誤

```yaml
error_handling:
  network:
    retry:
      max_attempts: 3
      strategy: exponential
      base_delay: 1000
    offline:
      mode: queue
      indicator:
        enabled: true
        message: "目前處於離線狀態"
      recovery:
        auto_sync: true
        conflict_resolution: server_wins
```

### 9.4 業務錯誤

```yaml
error_handling:
  business:
    errors:
      INSUFFICIENT_STOCK:
        message: "庫存不足，目前剩餘 {available} 件"
        display: inline
        severity: warning
      DUPLICATE_ORDER:
        message: "偵測到重複訂單，是否繼續？"
        display: modal
        severity: warning
```

### 9.5 錯誤邊界

```yaml
error_handling:
  boundary:
    page:
      enabled: true
      fallback:
        type: error_page
        title: "頁面載入失敗"
        actions:
          - label: "重新載入"
            action: reload
    section:
      enabled: true
      fallback:
        type: inline_error
        show_retry: true
```

---

## 10. 非同步行為規範

### 10.1 資料獲取

```yaml
async:
  fetching:
    default:
      strategy: cache-first    # cache-first | network-first | stale-while-revalidate
      stale_time: 30000
    background_refresh:
      enabled: true
      interval: 60000
      when_visible: true
    prefetch:
      enabled: true
      triggers:
        - on: hover_link
          delay: 200
```

### 10.2 資料變更（Mutations）

```yaml
async:
  mutations:
    optimistic:
      enabled: true
      rules:
        - action: toggle_status
          optimistic: true
          rollback_on_error: true
        - action: delete
          optimistic: true
          undo:
            enabled: true
            duration: 5000
            message: "已刪除 {name}"
    conflict:
      detection: version
      resolution:
        mode: prompt
```

### 10.3 表單提交 (v3.2.1)

```yaml
async:
  submit:
    loading:
      indicator: button_spinner    # button_spinner | overlay | none
      disable_form: true
    on_success:
      message: "{operation}{title}成功"
      redirect: "/{entity-kebab}/list"  # Convention 推斷
      action: redirect
    on_error:
      message: "{operation}{title}失敗: {error}"
```

> 不得在 `async.submit` 中硬編碼 `endpoint` 或 `method`，由 `actions.operations` + `api:` 自動解析。

### 10.4 Loading 狀態

```yaml
async:
  loading:
    global:
      delay: 200              # 延遲顯示避免閃爍
      minimum: 500            # 最少顯示時間
    zones:
      table:
        type: skeleton
        rows: 10
      button:
        type: spinner
        disable: true
        text: "處理中..."
```

### 10.5 請求控制

```yaml
async:
  request_control:
    debounce:
      search: 300
      auto_save: 2000
    throttle:
      scroll: 100
    cancellation:
      on_unmount: true
      on_new_request: true
    concurrency:
      max_parallel: 6
```

---

## 11. 無障礙存取規範

### 11.1 語意標籤

```yaml
accessibility:
  semantics:
    page:
      main_landmark: true
      navigation_landmark: true
    headings:
      page_title: h1
      section_title: h2
      auto_increment: true
    form:
      fieldset_grouping: true
      label_association: true
```

### 11.2 ARIA 標籤

```yaml
accessibility:
  aria:
    auto_labels:
      enabled: true
      regions:
        table: "資料列表"
        filters: "篩選條件"
        form: "資料表單"
    live_regions:
      - id: notification-area
        aria-live: polite
      - id: error-summary
        aria-live: assertive
```

### 11.3 鍵盤導覽

```yaml
accessibility:
  keyboard:
    enabled: true
    focus:
      visible: true
      trap_in_modal: true
      skip_links: true
    shortcuts:
      global:
        - key: "/"
          action: focus_search
        - key: "Escape"
          action: close_modal
      list:
        - key: "ctrl+n"
          action: create
        - key: "j"
          action: next_row
      form:
        - key: "ctrl+s"
          action: save
        - key: "ctrl+Enter"
          action: submit
```

### 11.4 螢幕閱讀器

```yaml
accessibility:
  screen_reader:
    announcements:
      data_loaded: "已載入 {count} 筆 {entity} 資料"
      action_complete: "{action} 成功"
      filter_applied: "已套用篩選，顯示 {count} 筆資料"
      validation_error: "表單驗證失敗，{count} 個錯誤"
    priority:
      error: assertive
      success: polite
```

### 11.5 合規等級

```yaml
accessibility:
  compliance:
    level: AA                 # A | AA | AAA
    standard: WCAG21
    validation:
      enabled: true
      on_build: true
      fail_on_error: true
```

---

## 12. 安全性規格

### 12.1 欄位級安全

```yaml
security:
  field_level:
    masking:
      - field: phone
        pattern: "###-###-{last4}"
        unmask_permission: [admin, owner]
        log_unmask: true
      - field: credit_card
        pattern: "****-****-****-{last4}"
        unmask_permission: []        # 永不顯示完整
    encryption:
      - field: ssn
        algorithm: AES-256-GCM
        key_source: vault
    access_control:
      - field: internal_notes
        read: [internal_staff]
        write: [manager, admin]
```

### 12.2 資料隔離

```yaml
security:
  data_isolation:
    mode: tenant
    rules:
      tenant:
        field: tenant_id
        auto_filter: true
        auto_set: true
        immutable: true
      owner:
        field: created_by
        share:
          enabled: true
          max_shares: 10
    exceptions:
      - role: super_admin
        bypass: all
        audit: true
```

### 12.3 敏感操作保護

```yaml
security:
  sensitive_operations:
    require_mfa:
      - action: delete_user
        mfa_type: [totp, sms]
    require_confirmation:
      - action: bulk_delete
        type: dialog
        message: "確定要刪除選取的 {count} 筆資料嗎？"
        input_match: "DELETE"
    require_approval:
      - action: large_order
        condition: "amount > 100000"
        approvers: [manager, finance]
        approval_type: any
    rate_limits:
      - action: login_attempt
        limit: 5
        window: 300
        lockout: 900
```

### 12.4 輸入防護

```yaml
security:
  input_protection:
    xss:
      enabled: true
      mode: strict
      sanitize_html: true
    csrf:
      enabled: true
      token_field: _csrf_token
    file_upload:
      allowed_types:
        - mime: "image/*"
          extensions: [jpg, jpeg, png, gif, webp]
      blocked_types:
        - extensions: [exe, bat, cmd, sh, php, js]
      scanning:
        enabled: true
      max_size: 10MB
```

### 12.5 稽核日誌

```yaml
security:
  audit:
    enabled: true
    level: detailed
    operations:
      - type: create
        entities: all
      - type: update
        fields: changed
      - type: delete
        entities: all
    sensitive_handling:
      mode: hash
      fields: [password, credit_card, ssn]
    storage:
      retention: 2555         # 7 年
      encryption: true
```

---

## 13. 測試性規格

### 13.1 簡化配置 (v3.2.1)

大多數頁面不需寫此區塊，全局預設：`strategy=data-testid`、`mock.enabled=true`。

```yaml
testing:
  selectors:
    strategy: data-testid     # data-testid | id | class | role

  mock:
    enabled: true
    fixtures:
      - entity: EntityName
        file: "path/to/fixture.json"

  notes: |
    自由文字說明
```

### 13.2 完整配置

```yaml
testing:
  selectors:
    - id: product_table
      data_testid: product-table
      aria_label: 商品清單
    - id: delete_button
      data_testid: product-delete-btn
      css_selector: "[data-action='delete']"

  mock_data:
    fixture_file: fixtures/products.json
    default_dataset: sample_products

  gherkin:
    feature_file: features/product_management.feature
    step_definitions: step_definitions/product_steps.js
```

---

## 14. 複雜表單支援

### 14.1 動態區塊

```yaml
view:
  form:
    dynamic_sections:
      - section: business_info
        visible_when: "customer_type == 'business'"
        fields:
          - company_name!
          - tax_id!

    conditional_fields:
      - field: other_reason
        visible_when: "reason == 'other'"
        required_when: "reason == 'other'"
```

### 14.2 可重複欄位群組

```yaml
view:
  form:
    repeatable:
      - name: contacts
        label: "聯絡人"
        min: 1
        max: 5
        fields:
          - name: name
            type: text
            required: true
          - name: phone
            type: tel
            required: true
        ui:
          layout: card          # card | table | inline
          sortable: true
        validation:
          - rule: "items.filter(c => c.is_primary).length === 1"
            message: "請指定一位主要聯絡人"
```

### 14.3 跨欄位驗證

```yaml
view:
  form:
    validations:
      cross_field:
        - fields: [start_date, end_date]
          rule: "end_date > start_date"
          message: "結束日期必須晚於開始日期"

      async:
        - field: email
          rule: "api:/validate/email-unique?email={email}"
          debounce: 500
          message: "此 Email 已被使用"
```

### 14.4 表單狀態管理

```yaml
view:
  form:
    state:
      dirty_check:
        enabled: true
        prompt_on_leave: true
        message: "您有未儲存的變更，確定要離開嗎？"

      auto_save:
        enabled: true
        delay: 5000
        storage: localStorage

      draft_recovery:
        enabled: true
        prompt: true
```

---

## 15. 檔案處理規格

### 15.1 檔案上傳

```yaml
file_handling:
  upload:
    mode: multiple
    accept: [".pdf", ".docx", "image/*"]
    max_size: 10MB
    chunked:
      enabled: true
      chunk_size: 2MB
      resume: true
    drag_drop:
      enabled: true
```

### 15.2 檔案預覽

```yaml
file_handling:
  preview:
    images:
      enabled: true
      lightbox: true
      zoom: true
    documents:
      pdf:
        renderer: pdfjs
```

### 15.3 檔案管理

```yaml
file_handling:
  management:
    versioning:
      enabled: true
      max_versions: 10
    operations:
      download: true
      rename: true
      delete:
        confirm: true
        soft_delete: true
```

---

## 16. 進階配置

```yaml
advanced:
  performance:
    lazy_load: true
    virtualization: true
    batch_size: 50

  caching:
    enabled: true
    ttl_seconds: 300
    cache_key: "products:{category}:{page}"

  plugins: [plugin-a, plugin-b]
```

---

## 17. 樣板與混入

### 17.1 樣板定義

```yaml
templates:
  - name: crud-list-template
    page_type: list
    description: "標準 CRUD 列表頁樣板"
    default_view:
      layout: single-column
    default_actions:
      standard: [create, read, update, delete]
```

### 17.2 混入定義

```yaml
mixins:
  - name: soft-delete-mixin
    description: "軟刪除功能混入"
    provides:
      actions:
        custom:
          - name: soft_delete
            type: button
            label: "移至回收站"
            confirmation:
              title: "確認移至回收站？"
```

### 17.3 使用方式

```yaml
pages:
  - page: user-list
    type: list
    entity: User
    extends: crud-list-template
    mixins: [soft-delete-mixin]
```

---

## 18. 跨規格整合

### 18.1 HaPDL <-> haAPI 映射

| HaPDL | haAPI | 說明 |
|-------|-------|------|
| `api:` | definition name | 頁面綁定的 API |
| `actions.operations:` | operation names | 操作引用 |
| `actions.custom[].operation:` | operation name | 自訂動作操作 |
| 不涉及 | `sql_hint` | haPDL 不關心 SQL 實作 |
| 不涉及 | `logic` steps | 後端業務邏輯 |
| 不涉及 | `ext.*` | 外部服務呼叫 |
| 不涉及 | `proxy` | 代理轉發 |

### 18.2 HaPDL <-> Annotated DBML 映射

| HaPDL | DBML | 合併規則 |
|-------|------|----------|
| `fieldName*` | `sensitive: true` | 聯集（兩者之一啟用遮罩） |
| `fieldName!` | `not_null: true` | 聯集 |
| `fieldName?` (form) | `nullable: true` | 參考性 |
| — | `ref_code:` | 推斷外鍵關係 → select 輸入 |
| — | `label:` | 推斷欄位標籤 |
| — | `group:` | 推斷表單分組 |

### 18.3 HaPDL <-> PDL 映射

| HaPDL | PDL | 說明 |
|-------|-----|------|
| 高階聲明 | 詳細配置 | HaPDL 是 PDL 的抽象層 |
| `actions.custom[].async_ui` | `action.async.ui` | UI 配置映射 |
| `security.field_level[].masking` | `field.security.masking` | 安全配置映射 |

### 18.4 haAPI 綁定語法

```yaml
actions:
  standard: [create, edit, delete]          # 對應 haAPI standard CRUD
  operations: [activate, deactivate]        # 引用 haAPI operations 名稱
  custom:
    - name: bulk_import
      operation: bulk_import                # haAPI 標記 async: true
      async_ui:
        submit_feedback: toast
        progress: polling
        completion: notification
```

轉換器會自動從 haAPI 定義解析出端點、HTTP 方法、角色權限，產出完整的 PDL action 配置。

#### async_ui（非同步操作 UI）

| 屬性 | 說明 | 預設值 |
|------|------|--------|
| `submit_feedback` | 提交後回饋方式：`toast` / `modal` / `inline` | `toast` |
| `progress` | 進度追蹤方式：`polling` / `websocket` / `none` | `polling` |
| `completion` | 完成通知方式：`notification` / `toast` / `redirect` | `notification` |

### 18.5 DBML 整合規則

#### label: 標籤推斷

標籤解析優先順序：

1. DBML `label:` 屬性
2. haPDL 明確指定
3. Convention 推斷（translations 字典）
4. Capitalize

#### ref_code: 動態列舉

當 DBML 欄位有 `ref_code:` 屬性時，轉換器自動推斷為 select 輸入並設定動態來源。

#### sensitive: 敏感欄位

```
sensitive 判定 = DBML sensitive: true  ∪  haPDL fieldName* 符號
                 ↓
                 PDL security.field_level.masking 自動包含此欄位
```

#### group: 表單分組

DBML `group:` 用於自動產生 PDL 表單 `sections`。若 haPDL 未指定 sections，轉換器從 DBML `group:` 自動產生。

### 18.6 Resolution Order（查找優先順序）

```
① DBML 明確標註 → ② haAPI 定義 → ③ haPDL 符號/配置 → ④ Convention 推斷 → ⑤ 預設值
```

#### 完整查找矩陣

| 屬性 | DBML | haAPI | haPDL | Convention | 預設值 |
|------|:----:|:-----:|:-----:|:----------:|:------:|
| **欄位標籤** | `label:` | — | — | `translations{}` | Capitalize |
| **輸入型別** | — | — | 符號 `@[]{}` | `dbml_type→input` | text |
| **顯示型別** | — | — | 符號 `:badge` | `dbml_type→display` | text |
| **必填** | `[not null]` | — | 符號 `!` | — | false |
| **敏感** | `sensitive:` | `data_masking` | 符號 `*` | 名稱推斷 | false |
| **列舉來源** | `ref_code:` | `enum` in filters | — | — | — |
| **分組** | `group:` | — | section 配置 | — | 無分組 |
| **API 端點** | — | `exposes` | `api:` 引用 | CamelCase→kebab | — |
| **權限** | — | `access.permissions` | `auth.roles` | — | 無限制 |
| **驗證規則** | `[not null]`/`nvarchar(N)` | `validation.rules` | 明確覆寫 | 型別推斷 | 無驗證 |

#### Validation Rules 推斷鏈 (v3.2.1)

| 規則 | DBML | haAPI | haPDL 覆寫 | Convention |
|------|------|-------|-----------|-----------|
| required | `[not null]`, `[pk]` | — | `!` 符號 | — |
| maxLength | `nvarchar(N)` → N | `max_length` | 明確指定 | — |
| unique | `[pk]`, `[unique]` | `unique: true` | — | — |
| min/max | — | — | 明確指定 | tinyint→0-255 |
| pattern | — | `pattern` | 明確指定 | — |

**覆寫規則**：haPDL 可收緊但不應放寬 haAPI 的驗證規則。

#### Permissions 推斷規則 (v3.2.1)

| haPDL 操作 | haAPI 操作 |
|-----------|-----------|
| view | list + read |
| create | create |
| edit | update |
| delete | delete |

**覆寫規則**：haPDL 只能收緊（取子集），不能放寬 haAPI 的權限。

---

## 19. 完整範例

### 電商後台管理系統

```yaml
metadata:
  schema_version: "3.2"
  title: 電商後台管理系統
  version: 1.0.0
  namespace: com.example.ecommerce.admin
  description: 完整的電商平臺管理介面

pages:
  # ===== 商品列表頁 =====
  - page: product-list
    type: list
    title: 商品列表
    entity: Product
    api: product-api

    view:
      filters:
        - keyword~
        - category[]
        - status=
        - price><
        - created_at>

      columns:
        - product_id#
        - name!
        - image:image
        - price|currency(TWD)
        - stock|number(0)
        - status:badge
        - created_at|datetime^

    state:
      local:
        - name: selectedIds
          type: array<string>
          default: []
      cascading:
        - source: category
          targets: [subcategory]
          strategy: reload
          api_operation: get_subcategories
      computed:
        - name: selectedCount
          expression: "selectedIds.length"
          dependencies: [selectedIds]

    actions:
      standard: [create, update, delete]
      operations: [bulk_publish, bulk_archive, bulk_price_adjust]
      custom:
        - name: publish_bulk
          operation: bulk_publish
          type: button
          label: 批量發佈
          icon: send
          confirmation:
            title: 確認批量發佈？
            message: "將發佈 {selectedCount} 個商品"
          async_ui:
            loading_indicator: spinner
            loading_message: 正在發佈...
        - name: export_csv
          type: button
          label: 匯出 CSV
          icon: download
          params:
            format: csv
          async_ui:
            progress_bar: true

    error_handling:
      default_strategy: retry
      handlers:
        - id: network_error
          error_type: network
          strategy: retry
          retry_count: 3
          user_message: 網路連線中斷，正在重試...

    async:
      ui:
        loading_indicator: skeleton
        skeleton_screen: true
      optimistic_update:
        enabled: true
        fallback_on_error: true
      request_control:
        debounce_ms: 300
        abort_on_navigation: true

    security:
      field_level:
        - id: price
          visible_to_roles: [admin, finance]
          editable_by_roles: [admin]
      action_level:
        - id: delete
          requires_roles: [admin]
          requires_confirmation: true
          sensitive_operation: true
      data_isolation:
        tenant_isolation: true

    accessibility:
      aria:
        - id: product_table
          label: 商品清單表格
          role: table
          live: polite
      keyboard:
        tab_order: 1
        keyboard_shortcuts:
          - key: "Ctrl+S"
            action: save
          - key: "Delete"
            action: delete_selected
      screen_reader:
        skip_to_content: true
        announce_changes: true

    testing:
      selectors:
        - id: product_table
          data_testid: product-table
          aria_label: 商品清單
        - id: delete_button
          data_testid: product-delete-btn
      mock_data:
        fixture_file: fixtures/products.json
        default_dataset: sample_products

    advanced:
      performance:
        lazy_load: true
        virtualization: true
        batch_size: 50
      caching:
        enabled: true
        ttl_seconds: 300

  # ===== 商品編輯頁 =====
  - page: product-form
    type: form
    title: 商品編輯
    entity: Product
    api: product-api

    view:
      layout: two-column
      fields:
        - name!
        - sku!
        - category!
        - subcategory<~
        - description
        - price!
        - stock!
        - image:image
        - status=
        - is_featured?
        - metadata{}
        - tags[]

    state:
      local:
        - name: isEditing
          type: boolean
          default: false
      persistence:
        - state_var: formData
          storage: session
          key: "product_form_draft"

    actions:
      standard: [create, update]
      custom:
        - name: save_draft
          operation: save_draft
          type: button
          label: 儲存草稿
          variant: secondary
        - name: preview
          type: button
          label: 預覽
          icon: eye

    security:
      action_level:
        - id: publish
          requires_roles: [admin, editor]
          requires_confirmation: true

    accessibility:
      aria:
        - id: product_form
          label: 商品編輯表單
          role: form
      keyboard:
        tab_order: 1
        keyboard_shortcuts:
          - key: "Ctrl+Enter"
            action: submit

    testing:
      selectors:
        - id: form
          data_testid: product-form
        - id: submit_button
          data_testid: submit-btn
      gherkin:
        feature_file: features/product_management.feature
        step_definitions: step_definitions/product_steps.js
```

---

## 20. 驗證規則檢查清單

### 20.1 語法驗證

- [ ] 所有必需字段存在（page, type, entity）
- [ ] 頁面 ID 遵循 kebab-case 格式
- [ ] 版本號遵循 `\d+\.\d+(\.\d+)?` 模式
- [ ] 命名空間為點號分隔的識別碼
- [ ] YAML 語法正確

### 20.2 引用驗證

- [ ] entity 引用有效的 DBML 實體
- [ ] api 引用有效的 haAPI 定義 (v3.1+)
- [ ] operations 引用有效的 haAPI 操作名稱 (v3.1+)
- [ ] extends 引用存在的樣板
- [ ] mixins 引用存在的混入模組
- [ ] 所有字段引用指向存在的欄位

### 20.3 語義驗證

- [ ] 修飾符匹配字段類型
- [ ] 篩選欄位符號有效
- [ ] 顯示類型與格式化兼容
- [ ] 狀態變數名稱唯一
- [ ] 動作名稱唯一
- [ ] 錯誤處理器 ID 唯一

### 20.4 欄位級驗證

- [ ] 敏感欄位標記完整 (v3.1+)
- [ ] 連動欄位配對正確
- [ ] 計算屬性依賴有效
- [ ] 條件表達式合法

### 20.5 跨規格驗證

- [ ] haAPI 綁定有效 (v3.1+)
- [ ] 操作名稱與 haAPI 對齊 (v3.1+)
- [ ] DBML 敏感標註推斷正確 (v3.1+)
- [ ] Scope Declaration 遵守 (v3.1+)
- [ ] 權限不放寬 haAPI 定義 (v3.2.1)

### 20.5 常見誤用與反模式（Anti-Pattern, v3.3 新增）

> Q14 決議：Anti-Pattern 整合進驗證規則章節，lint 訊息可直接引用本節編號。

| 編號 | 反模式 | 為何錯 | 正確寫法 |
|------|--------|--------|---------|
| **AP-01** | 在新規格用 `security.permissions` 結構 | v3.1 legacy；v3.4 將移除（見 `pdl-syntax-v3.3.md` 雙軌權限配置） | 改用 `security.permission_refs.{view\|create\|edit\|delete}[].id`，引用 haARM `permission.id` |
| **AP-02** | 把 deptId 過濾邏輯寫在 `datasource.query` | 與 haARM 雙重事實源；haARM 的 scope 語義無法投影過來 | 用 `security.datasource_scope: department`，由 codegen 在 service 層執行 `WHERE deptId starts_with $self.department_id`（M2 後落地） |
| **AP-03** | `actions.standard: [create]` 同時定義同名 `actions.custom.create` | 兩者展開規則不同（standard 走 sugar 展開，custom 走明示），重名會在 phase3-sugar.ts 觸發 conflict | 重命名 custom action（如 `create_with_template`）或移除 standard 同名項 |
| **AP-04** | 把欄位顯示型別硬編在 `columns:` | DBML 已有 `label:`/`group:`/`sensitive:` 一級語法（Q9）；硬編造成下游分散維護 | 在 DBML 一處宣告，haPDL 只在需要覆寫時寫（與 Q6 合併語意一致） |
| **AP-05** | `auth.roles: [unknown_role]` 引用不存在的 haARM role.id | 跨 DSL 引用斷裂；M4 lint 升級後會 error | 確認 role.id 在 haARM `.haarm.yaml` 已宣告；用 `validate_cross_dsl.py` 驗證 |

> **lint 觸發規則**：`hapdl-lint` 在 v3.3 起檢查 AP-01～AP-05；違反 AP-01/AP-05 為 **error**，AP-02/AP-03/AP-04 為 **warning**。

---

## 21. 檔案格式與工具支援

### 21.1 檔案命名

```
<page-identifier>.hapdl.yaml
```

範例：

```
user-list.hapdl.yaml
product-form.hapdl.yaml
dashboard-analytics.hapdl.yaml
```

### 21.2 工具支援

- **VSCode 擴展**：YAML 語法著色、自動補全、即時驗證
- **CLI 工具**：
  - 驗證：`hapdl validate <file>`
  - 轉換：`hapdl to-pdl <file>` → PDL
  - 生成文檔：`hapdl docs <file>`
  - 檢查：`hapdl lint <file>`
- **JSON Schema 驗證**：使用第 5 節的 JSON Schema
- **haAPI 交叉驗證**：檢查 API 綁定有效性

### 21.3 整合工作流

```
HaPDL YAML 文檔
    ↓
YAML 解析 → Python/JavaScript 物件
    ↓
JSON Schema 驗證（語法層）
    ↓
語義驗證（引用、類型、跨規格）
    ↓
haAPI 交叉驗證
    ↓
DBML 敏感性推斷
    ↓
轉換為 PDL（詳細配置）
    ↓
生成前端程式碼（Vue/React）
```

### 21.4 版本控制

- 遵循**語義化版本** (SemVer) 規範
- MAJOR.MINOR.PATCH 格式
- 向後兼容性檢查
- v3.2 為當前標準版本

---

## 附錄

### 附錄 A：保留名稱與關鍵字

#### 保留的虛擬欄位

| 名稱 | 用途 | 說明 |
|------|------|------|
| `keyword` | 篩選 | 全文搜尋框（無對應實體欄位） |
| `keyword~` | 篩選 | 模糊搜尋（預設） |
| `keyword=` | 篩選 | 精確匹配 |

#### 保留的狀態變數名

- `isLoading` — 載入狀態
- `error` — 錯誤訊息
- `selectedItems` — 選中項目

### 附錄 B：常見模式

#### Pattern: 主從列表

```yaml
pages:
  - page: order-list
    type: master-detail
    title: 訂單列表
    view:
      filters:
        - order_id=
        - status[]
        - created_at><
      columns:
        - order_id^
        - customer_name
        - total|currency(TWD)
        - status:badge
      detail_columns:
        - item_id
        - product_name
        - quantity|number(0)
        - unit_price|currency(TWD)
```

#### Pattern: 連動欄位

```yaml
view:
  fields:
    - country~
    - province<~

state:
  cascading:
    - source: country
      targets: [province, city]
      strategy: reload
      api_operation: get_provinces
```

#### Pattern: 敏感資料

```yaml
view:
  fields:
    - ssn*
    - password*

security:
  field_level:
    - id: ssn
      masking: true
      mask_type: full
      visible_to_roles: [admin, auditor]
```

### 附錄 C：HaPDL 定義統計

| 維度 | 定義數量 |
|------|----------|
| Page（核心） | 1 |
| View（Filter/Column/Field） | 3 |
| State（Local/Shared/Cascading/Persistence/Computed/Watcher） | 6 |
| Actions（Standard/Custom） | 2 |
| Error（Strategy/Handler） | 2 |
| Async（UI/OptimisticUpdate/RequestControl） | 3 |
| Security（Field/Action/DataIsolation） | 3 |
| Accessibility（ARIA/Keyboard/ScreenReader） | 3 |
| Testing（Selector/MockData/Gherkin） | 3 |
| Template + Mixin | 2 |
| **合計** | **28 個定義** |

### 附錄 D：events 訂閱（P2 預留）

> 此區塊為 P2 預留設計，尚未納入正式語法。待 WebSocket / SSE 整合方案確定後再正式定義。

```yaml
# 未來 haPDL 語法（草案）
events:
  subscribe:
    - event: user.created
      action: refresh_list
    - event: user.updated
      action: update_item
```

---

**文件維護者**：WA-RAPTor 團隊  
**最後更新**：2026-05-14（v3.3 RC）
**版本**：v3.3.0
**來源文件**：`8specDSLs/haPDL-specification-v3.3.md`、`8specDSLs/pdl-syntax-v3.3.md`、`8specDSLs/archive/HaPDL-Structured-Specification-v3_2.md`（v3.2 落檔保存）

---

## 附錄 A: §6 Convention over Configuration（v3.3 新增；M3 重排時升為正式 §6）

> v3.3 統一章節骨架中 §6 為 Convention over Configuration（見 §0.3）。本附錄是 haPDL 的 §6 內容；待 freeze 視窗結束（>2026-05-26）後由 M3 polish 升至正式編號。

### A.6.1 三段式優先序

```
   隱含預設值                慣例 Profile               明示覆寫
   (built-in defaults)  →   (named profile)        →   (explicit fields)
   ────────────────────     ──────────────────         ──────────────────
   type: form 推欄位         standard: [create]         actions 全列
   DBML → 自動標籤           type: list 預設 columns    columns 完全自訂
   標準動作圖示/變體          template extends           fields 明示 input type
```

### A.6.2 haPDL Convention 來源（三層）

#### 1. YAML 設定檔 — `haPDL2PDL/src/defaults/`

| 檔案 | 範圍 | 範例內容 |
|------|------|---------|
| `global.defaults.yaml` | 全 type 共用 | 預設 pagination=20、selectable=multiple |
| `list.defaults.yaml` | `type: list` 專用 | 預設 columns、actions、features |
| `form.defaults.yaml` | `type: form` 專用 | 預設 layout、validation 規則 |

#### 2. 設計規格文件 — `haPDL/haPDL-page-type-defaults-v3.2.1.md`

> **注意**：此檔仍標 v3.2.1，M2.6 已記錄需在後續 polish 同步至 v3.3。當前以 v3.2.1 內容為準，差異僅在版本標頭。

定義：
- 合併策略：scalar deep merge、**陣列完全覆寫**（與 §3.10.3 一致；Q6 統一決策）
- 推斷規則：DBML 欄位型別 → form input 型別
- 覆寫語義：何時 haPDL 蓋過 DBML、何時 PDL 蓋過 haPDL

#### 3. 程式碼邏輯 — `haPDL2PDL/src/`

| 檔案 | 作用 |
|------|------|
| `phase2-defaults.ts` | 合併 defaults + 推斷 aria-* 屬性 |
| `phase3-sugar.ts` | 符號展開（`!` `?` `#` `*` `@`）+ `standard: [create]` → 三按鈕 |
| `convention.py`（haPDL converter） | DBML 欄位 → label/group 推斷（v3.3 已對齊 DBML 一級標註） |

### A.6.3 慣例 Profile 實例

| 觸發方式 | 範例檔 | 自動展開 |
|---------|--------|---------|
| `type: list` | `benchmarks/haPDL-v3.2/apcatList.hapdl.yaml` | 表格 + filter + pagination + standard actions |
| `type: form` + `standard: [create]` | `benchmarks/haPDL-v3.2/apcatAdd.hapdl.yaml` | submit/cancel/reset 三按鈕 + 對應路由 |
| `extends:` 樣板繼承 | §17 樣板與混入 | 共用佈局/欄位/驗證 |

### A.6.4 三段式優先序的合併語意

```
明示寫的 fields/columns/actions   （最高）
  > template extends （樣板繼承的合併結果）
  > standard 展開（如 [create] → 三按鈕）
  > type 預設（type: form 推 fields）
  > DBML 推斷（type/label/group）
  > 系統 fallback（capitalize、generic input）
```

**Q6 一致性**：與 haARM `profile_overrides` 同樣採「scalar deep merge + 陣列完全覆寫」。

### A.6.5 何時不該套 Convention

| 情境 | 替代方案 |
|------|---------|
| 多 entity 聚合頁（如 dashboard）| 用 `type: dashboard`，明示 widgets，不靠 DBML 推斷 |
| 非標準互動（drag-drop、即時編輯）| 寫 `advanced.custom_components`，不套 type 預設 |
| BDD-driven 已有 step 對應 | 從 Gherkin 反向生成 haPDL，convention 僅補空缺 |

### A.6.6 與 haARM 的 Convention 對齊

`security.permission_refs` 與 `auth.roles[]` 在 v3.3 與 haARM 雙軌引用（見 §1.5 SSoT 宣告）。haPDL 不重複定義權限預設，由 haARM 的 profile/auto_infer 統一決定。

---

## 附錄 B: §7 跨規格整合（v3.3 新增；M3 已落地）

> v3.3 統一章節骨架 §7 = 跨規格整合（見 §0.3）。完整跨 DSL 導覽請見 [`CROSS-DSL-GUIDE.md`](CROSS-DSL-GUIDE.md)；本節僅列 haPDL 端的引用界面與 hycms-ht002 範例對應。

### B.7.1 haPDL 端的跨 DSL 引用點

| 引用點 | haPDL 欄位 | 對應目標 | 驗證規則 |
|--------|----------|---------|---------|
| API 綁定 | `api:` 頁面層級 | haAPI `api:` 頂層 | `validate_cross_dsl.py` Rule 5 |
| 頁面角色 | `auth.roles[]` | haARM `roles[].id` | Rule 6 |
| Permission 雙軌（v3.3） | `security.permission_refs.{view\|create\|edit\|delete}[].id` | haARM `permissions[].id` | （Rule 3/4 在 haAPI 側驗，haPDL 側 M4 lint 補上） |
| Datasource Scope | `security.datasource_scope` | haARM permission.scope（語義對齊，非 ID 引用） | codegen 對 SQL 過濾翻譯 |
| Entity（推斷用） | `entity:` 頁面層級 | DBML `Table <Name>`（透過 haAPI 中介）| 經 haAPI 間接驗證 |

### B.7.2 hycms-ht002 範例對應

`benchmarks/haPDL-v3.2/hycms-ht002.hapdl.yaml`：

```yaml
page: hycms-ht002-list
type: list
entity: InfoUser
api: hycms-ht002                       # ← 對應 haAPI api: 欄位

auth:
  roles: [htsd, sysadm, audit]         # ← 對應 haARM roles[].id

security:
  permission_refs:                     # v3.3 雙軌：精細權限 ↓ 引用 haARM permission.id
    view:   [{id: infouser_read}]
    create: [{id: infouser_create}]
    edit:   [{id: infouser_update}]
    delete: [{id: infouser_delete}]
  datasource_scope: department          # 對應 haARM scope: department
```

跑 `python benchmarks/validate_cross_dsl.py hycms-ht002` 驗證引用一致性。

### B.7.3 與 `CROSS-DSL-GUIDE.md` 的關係

本節是 haPDL 視角的引用清單；CROSS-DSL-GUIDE.md 是四 DSL 平面的完整對應表（含版本互鎖、Anti-Pattern、同步機制）。**新增跨 DSL anchor 時須先讀 CROSS-DSL-GUIDE §3.2 流程**。

---
