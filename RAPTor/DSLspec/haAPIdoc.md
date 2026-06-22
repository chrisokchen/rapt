# haAPI 完整參考手冊

**haAPI — High-level Abstract API Definition Language**

| 項目 | 說明 |
|------|------|
| 版本 | **v3.3.0 (Release Candidate, 2026-05-13)** |
| 對齊規格 | haARM v3.3、haPDL v3.3、Annotated DBML v3.3、TypeSpec v0.50+ |
| 檔案格式 | YAML（`.haapi.yaml`） |
| 所屬框架 | WA-RAPTor（Web-based Application Requirements Analysis and Prototyping Tool） |
| 文件日期 | 2026-05-13 |
| 前版 | v3.2（見 `archive/haAPI-specification_v3.2.md`） |

---

## 目錄

0. [版本沿革](#0-版本沿革)
1. [設計理念與定位](#1-設計理念與定位)
2. [EBNF 文法定義](#2-ebnf-文法定義)
3. [JSON Schema 定義](#3-json-schema-定義)
4. [語義規則表](#4-語義規則表)
5. [語法與語義說明](#5-語法與語義說明)
6. [Z3 約束驗證](#6-z3-約束驗證)
7. [完整範例](#7-完整範例)
8. [驗證規則總覽](#8-驗證規則總覽)
9. [跨規格映射](#9-跨規格映射)
10. [工具鏈與最佳實踐](#10-工具鏈與最佳實踐)
11. [附錄：遷移指南](#11-附錄遷移指南)

---

## 0. 版本沿革

### 0.1 跨 DSL 版本歷程（v1.0 → v3.3）

| 版本 | 日期 | 主要變更 |
|------|------|---------|
| v1.0 | 2026-04 早期 | 初版規格分散建立（haARM v1、haAPI v1.0、haPDL v1.0、DBML v1.1） |
| v2.0 | 2026-04 中 | haARM：新增 `resources` 區段、`scope`、`$self`、`context:`、`TimeWindowCondition` |
| v3.0 | 2026-04 末 | haAPI 新增 `proxy`/`ext.*`/`logic`、三層級聯 resilience；haPDL 新增 State/Error/Async/A11y/Security/Testability/樣板與混入 |
| v3.1 | 2026-05 初 | haPDL：Scope Declaration、`security.permission_refs`、`datasource_scope` 雛形 |
| v3.2 | 2026-05-11 | haAPI Access v2 雙軌（`endpoints`/`operations`）、PDL `permission_refs` 落地、DBML 四個自訂標註 |
| **v3.3** | **2026-05-13** | (a) haARM 跳版 v3.3，新增 `starts_with`/`ends_with` 運算子；(b) Convention over Configuration 三段式（預設 → 慣例 Profile → 明示覆寫）；(c) DBML 移除「是否需要？」探索性標題、四標註升為一級語法；(d) 四 DSL 統一 12 章骨架；(e) 新增 `CROSS-DSL-GUIDE.md` 整合入口 |

### 0.2 v3.3 四 DSL 版本互鎖表

| DSL | 主檔（SSoT） | 規格檔 | 版本 | 對齊狀態 |
|-----|-------------|--------|------|---------|
| haAPI | `haAPIdoc.md` | `haAPI-specification_v3.3.md` | **v3.3.0** | Access v2 雙軌引用 haARM `permission.id`/`role.id` |
| haPDL | `haPDLdoc.md` | `haPDL-specification-v3.3.md` + `pdl-syntax-v3.3.md` | **v3.3.0** | `auth.roles[]` / `security.permission_refs` 對齊 haARM |
| haARM | `haARMdoc.md` | `haARM-Specification_v3.3.md` | **v3.3.0** | 新增 `starts_with`，引入 profile / auto_infer |
| DBML | `annotated_DBML-v3.3.md` | — | **v3.3.0** | 收編 4 個一級標註；與 haARM `resource.id` ↔ table 對齊 |

> **維護規則**：跨 DSL 版本升級時先寫入本 §0.1，再到各 *doc.md sync；不在各檔自行加非同步版本。Freeze 視窗起於 **2026-05-19**（凍結 EBNF/JSON Schema/欄位語意；文字、範例、速查卡不受限）。詳見 `ccwLog/0513-specsAlign_plan.md` §0 與 `ccwLog/0513-PQ_discuss.md` Q12。

### 0.3 章節骨架對照表（v3.3 統一 12 章）

> 本檔現行章節以「現狀」呈現，M2/M3/M1 將分批搬入下列 v3.3 標準位置。對照表會在 freeze 視窗結束後（>2026-05-26）正式完成重排。

| v3.3 標準章 | 標題 | 本檔現行位置 | 完工里程碑 |
|:----------:|------|------------|:---------:|
| 0 | 版本沿革 | §0（本章，已就位） | ✅ M0.4 |
| 1 | 設計理念與定位 | §1（含新加 §1.5 SSoT 宣告） | ✅ M0.4 |
| 2 | 適用情境 | 散見於 §1.4「職責分離三檔案」 | ⏳ M0.3 後續 polish |
| 3 | EBNF 文法定義 | §2 | M0.3 重排 |
| 4 | JSON Schema 定義 | §3 | M0.3 重排 |
| 5 | 語義規則表 | §4 + §5 | M0.3 重排 |
| 6 | Convention over Configuration | （新增章，placeholder 見文末附錄） | ⏳ M2 |
| 7 | 跨規格整合 | §9 跨規格映射（重命名 + 補 hycms-ht002 範例） | ⏳ M3 |
| 8 | 完整範例 | §7 | M0.3 重排 |
| 9 | 驗證規則（含 §9.5 Anti-Pattern） | §8 + 新 §9.5 | ⏳ M1（§9.5）+ M0.3 重排 |
| 10 | 工具支援與 Lint | §10 + §6 Z3 驗證（併入） | M0.3 重排 |
| 11 | 遷移指引 | §11 | M0.3 重排 |

---

## 1. 設計理念與定位

### 1.1 核心理念

haAPI 是一套**意圖導向**的 API 定義語言，專注於描述「業務能力」而非「技術實現」。在 WA-RAPTor 七規格檔案體系中，haAPI 位於**意圖層**第 3 號規格。

```
業務需求 → haAPI（What） → TypeSpec（How） → OpenAPI / 程式碼
```

### 1.2 與現有工具的關係

| 工具 | 層級 | 關注點 | 產出物 |
|------|------|--------|--------|
| **haAPI** | 意圖層 | 業務能力、領域操作 | API 意圖規格 |
| **TypeSpec** | 規格層 | 型別、路由、協定 | API 技術規格 |
| **OpenAPI** | 文檔層 | 端點、參數、範例 | API 文檔 |
| **程式碼** | 實作層 | 邏輯、效能、安全 | 可執行程式 |

### 1.3 設計原則

| # | 原則 | 說明 |
|---|------|------|
| 1 | **領域驅動** | 基於 DBML 定義的領域模型 |
| 2 | **慣例優於配置** | 自動推斷 RESTful 最佳實踐 |
| 3 | **前後端一致** | 與 HaPDL 頁面規格對應 |
| 4 | **漸進式細化** | 從簡單 CRUD 到複雜業務邏輯 |
| 5 | **可生成性** | 能自動轉換為 TypeSpec/OpenAPI |
| 6 | **職責分離** | 意圖歸 haAPI、基礎設施歸 infra config、行為預設歸 codegen.config |

### 1.4 職責分離三檔案

| 檔案 | 負責什麼（What） | 不負責什麼（Not） |
|------|------------------|-------------------|
| `*.haapi.yaml` | 「我需要呼叫 smtp 的 send_email」 | smtp 的連線位址、帳密、protocol |
| `integrations.config.yaml` | smtp 用 SendGrid、端點在哪、用什麼認證 | 哪支 API 會用到 smtp |
| `codegen.config.yaml` | 全域 resilience 預設（timeout/retry） | 個別服務的基礎設施細節 |

### 1.5 SSoT 主手冊宣告

**本文件為 haAPI 的 SSoT 主手冊**，PM/SA 與下游 codegen 對 haAPI 語法的單一可信來源。

- 技術參考：`haAPI-specification_v3.3.md`（EBNF 與 JSON Schema 完整版）
- 驗證實作：`haAPI-Z3-Constraint-Validation.md`（Z3 表達式與證明）
- 跨 DSL 整合：`CROSS-DSL-GUIDE.md`（v3.3 待建，詳見 M3）

三者描述衝突時**以本檔為準**；補充檔需於下次版本同步至本檔對應章節。

---

## 2. EBNF 文法定義

以下為 haAPI 的完整上下文無關文法（Context-Free Grammar），涵蓋 8 個主要區段，嵌套結構 5-6 層深度。

```ebnf
(* ============================================================ *)
(* haAPI 文法定義 — v3.2                                         *)
(* ============================================================ *)

HaAPIDocument ::= MetadataSection
                  APIDefinitionSection
                  (IntegrationsSection)?
                  (ExposesSection)?
                  (AccessSection)?
                  (ConsumersSection)?
                  (AdvancedSection)?

(* ===== 元資料區段 ===== *)
MetadataSection ::= NEWLINE? Metadata? NEWLINE?

Metadata ::= 'metadata' ':' NEWLINE?
             INDENT MetadataFields DEDENT

MetadataFields ::= MetadataField
                 | MetadataField MetadataFields

MetadataField ::= 'version' ':' Version NEWLINE
                | 'title' ':' String NEWLINE
                | 'description' ':' String NEWLINE
                | 'namespace' ':' NamespaceId NEWLINE

Version ::= DigitSequence '.' DigitSequence ('.' DigitSequence)?

NamespaceId ::= Identifier ('.' Identifier)*

(* ===== API 定義區段 ===== *)
APIDefinitionSection ::= '- api' ':' APIId NEWLINE
                         INDENT APIFields DEDENT

APIFields ::= APIField
            | APIField APIFields

APIField ::= 'title' ':' String NEWLINE
           | 'version' ':' Version NEWLINE
           | 'entity' ':' EntityRef NEWLINE
           | 'description' ':' String NEWLINE
           | 'tags' ':' TagList NEWLINE
           | 'deprecated' ':' Boolean NEWLINE
           | 'integrations' ':' NEWLINE INDENT IntegrationDeclaration+ DEDENT
           | 'exposes' ':' NEWLINE INDENT ExposesDefinition DEDENT
           | 'access' ':' NEWLINE INDENT AccessDefinition DEDENT
           | 'consumers' ':' NEWLINE INDENT ConsumerDefinition DEDENT
           | 'advanced' ':' NEWLINE INDENT AdvancedDefinition DEDENT

TagList ::= '[' Tag (',' Tag)* ']'

Tag ::= String | Identifier

EntityRef ::= Identifier

(* ===== 外部服務整合區段 ===== *)
IntegrationsSection ::= 'integrations' ':' NEWLINE
                        INDENT Integration+ DEDENT

Integration ::= '- name' ':' IntegrationId NEWLINE
                INDENT IntegrationFields DEDENT

IntegrationFields ::= IntegrationField
                    | IntegrationField IntegrationFields

IntegrationField ::= 'service' ':' String NEWLINE
                   | 'capabilities' ':' CapabilityList NEWLINE
                   | 'resilience' ':' ResilienceConfig NEWLINE
                   | 'timeout' ':' TimeValue NEWLINE
                   | 'retry' ':' RetryConfig NEWLINE

CapabilityList ::= '[' CapabilityRef (',' CapabilityRef)* ']'

CapabilityRef ::= Identifier

(* ===== 業務能力公開區段 ===== *)
ExposesDefinition ::= StandardCapabilities
                    | ListDefinition
                    | OperationsDefinition
                    | ExposesField ExposesDefinition

StandardCapabilities ::= 'standard' ':' StandardActionList

StandardActionList ::= '[' StandardAction (',' StandardAction)* ']'
                     | StandardActionKeyword

StandardActionKeyword ::= 'crud' | 'all'

StandardAction ::= 'list' | 'create' | 'read' | 'update'
                 | 'patch' | 'delete' | 'exists'

ListDefinition ::= 'list' ':' NEWLINE
                   INDENT ListFields DEDENT

ListFields ::= ListField
             | ListField ListFields

ListField ::= 'filters' ':' NEWLINE INDENT FilterConfig+ DEDENT
            | 'sorting' ':' NEWLINE INDENT SortingConfig DEDENT
            | 'pagination' ':' NEWLINE INDENT PaginationConfig DEDENT
            | 'search' ':' NEWLINE INDENT SearchConfig DEDENT
            | 'aggregations' ':' AggregationList NEWLINE
            | 'includes' ':' IncludeList NEWLINE

FilterConfig ::= '- field' ':' FieldName NEWLINE
                 INDENT FilterFields DEDENT

FilterFields ::= FilterField
               | FilterField FilterFields

FilterField ::= 'operators' ':' OperatorList NEWLINE
              | 'nullable' ':' Boolean NEWLINE

OperatorList ::= '[' Operator (',' Operator)* ']'

Operator ::= 'eq' | 'ne' | 'gt' | 'gte' | 'lt' | 'lte'
           | 'in' | 'nin' | 'contains' | 'starts_with'
           | 'ends_with' | 'between' | 'match'

SortingConfig ::= 'fields' ':' FieldList NEWLINE
                  'default' ':' SortOrder NEWLINE

FieldList ::= '[' FieldName (',' FieldName)* ']'

SortOrder ::= FieldName ':' Direction

Direction ::= 'asc' | 'desc'

PaginationConfig ::= 'style' ':' PaginationStyle NEWLINE
                     'default_size' ':' Integer NEWLINE
                     'max_size' ':' Integer NEWLINE

PaginationStyle ::= 'offset' | 'cursor' | 'page'

SearchConfig ::= 'fields' ':' FieldList NEWLINE
                 'type' ':' SearchType NEWLINE

SearchType ::= 'fulltext' | 'simple'

AggregationList ::= '[' AggregationRef (',' AggregationRef)* ']'

AggregationRef ::= Identifier

IncludeList ::= '[' FieldName (',' FieldName)* ']'

(* ===== 自訂操作區段 ===== *)
OperationsDefinition ::= 'operations' ':' NEWLINE
                         (INDENT Operation+ DEDENT)?

Operation ::= '- name' ':' OperationId NEWLINE
              INDENT OperationFields DEDENT

OperationFields ::= OperationField
                  | OperationField OperationFields

OperationField ::= 'description' ':' String NEWLINE
                 | 'method' ':' HTTPMethod NEWLINE
                 | 'path' ':' PathTemplate NEWLINE
                 | 'batch' ':' Boolean NEWLINE
                 | 'async' ':' Boolean NEWLINE
                 | 'params' ':' ParamList NEWLINE
                 | 'formats' ':' FormatList NEWLINE
                 | 'cache' ':' Integer NEWLINE
                 | 'workflow' ':' Boolean NEWLINE
                 | 'require_reason' ':' Boolean NEWLINE
                 | 'proxy' ':' NEWLINE INDENT ProxyConfig DEDENT
                 | 'sql_hint' ':' String NEWLINE
                 | 'logic' ':' NEWLINE INDENT LogicDefinition DEDENT

HTTPMethod ::= 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' | 'HEAD'

PathTemplate ::= String

ParamList ::= '[' Param (',' Param)* ']'

Param ::= ParamName ':' ParamType

ParamName ::= Identifier

ParamType ::= Identifier

FormatList ::= '[' Format (',' Format)* ']'

Format ::= Identifier

ProxyConfig ::= 'target' ':' ProxyTarget NEWLINE
                ('enrich' ':' Object NEWLINE)?
                ('pick' ':' FieldList NEWLINE)?

ProxyTarget ::= 'ext' '.' Identifier '.' Identifier

LogicDefinition ::= 'steps' ':' NEWLINE INDENT LogicStep+ DEDENT
                    'returns' ':' Object NEWLINE
                    ('mode' ':' LogicMode NEWLINE)?

LogicStep ::= '- action' ':' ActionType NEWLINE
              INDENT LogicStepFields DEDENT

ActionType ::= 'query' | 'update' | 'insert' | 'upsert' | 'validate'
             | 'foreach' | 'create_job' | 'parse_file' | 'update_job'
             | ExternalAction

ExternalAction ::= 'ext' '.' Identifier '.' Identifier

LogicStepFields ::= LogicStepField
                  | LogicStepField LogicStepFields

LogicStepField ::= 'sql' ':' String NEWLINE
                 | 'rule' ':' String NEWLINE
                 | 'input' ':' Object NEWLINE
                 | 'result' ':' Identifier NEWLINE
                 | 'on_fail' ':' NEWLINE INDENT ErrorHandling DEDENT
                 | 'on_empty' ':' NEWLINE INDENT ErrorHandling DEDENT
                 | 'items' ':' Identifier NEWLINE
                 | 'steps' ':' NEWLINE INDENT LogicStep+ DEDENT
                 | 'resilience' ':' NEWLINE INDENT ResilienceConfig DEDENT

ErrorHandling ::= 'status' ':' Integer NEWLINE
                  'message' ':' String NEWLINE
                  ('side_effect' ':' NEWLINE INDENT SideEffect DEDENT)?

SideEffect ::= 'sql' ':' String NEWLINE

LogicMode ::= 'sync' | 'async_job'

(* ===== 存取控制區段 ===== *)
AccessSection ::= 'access' ':' NEWLINE
                  (INDENT AccessDefinition DEDENT)?

AccessDefinition ::= AccessRule
                   | AccessRule AccessDefinition

AccessRule ::= '- operation' ':' OperationId NEWLINE
               INDENT AccessFields DEDENT

AccessFields ::= AccessField
               | AccessField AccessFields

AccessField ::= 'requires_roles' ':' RoleList NEWLINE
              | 'requires_permissions' ':' PermissionList NEWLINE
              | 'requires_authentication' ':' Boolean NEWLINE
              | 'rate_limit' ':' RateLimitConfig NEWLINE

RoleList ::= '[' Role (',' Role)* ']'

Role ::= String

PermissionList ::= '[' Permission (',' Permission)* ']'

Permission ::= String

RateLimitConfig ::= 'requests' ':' Integer 'per' TimeUnit

TimeUnit ::= 'second' | 'minute' | 'hour' | 'day'

(* ===== 消費者定義區段 ===== *)
ConsumersSection ::= 'consumers' ':' NEWLINE
                     (INDENT ConsumerDefinition DEDENT)?

ConsumerDefinition ::= Consumer
                     | Consumer ConsumerDefinition

Consumer ::= '- page' ':' PageRef NEWLINE
             INDENT ConsumerFields DEDENT

PageRef ::= Identifier

ConsumerFields ::= ConsumerField
                 | ConsumerField ConsumerFields

ConsumerField ::= 'uses' ':' OperationRefList NEWLINE
                | 'binds' ':' BindingMap NEWLINE

OperationRefList ::= '[' OperationRef (',' OperationRef)* ']'

OperationRef ::= Identifier

BindingMap ::= Object

(* ===== 進階配置區段 ===== *)
AdvancedSection ::= 'advanced' ':' NEWLINE
                    (INDENT AdvancedDefinition DEDENT)?

AdvancedDefinition ::= AdvancedField
                     | AdvancedField AdvancedDefinition

AdvancedField ::= 'resilience' ':' NEWLINE INDENT ResilienceConfig DEDENT
                | 'caching' ':' NEWLINE INDENT CachingConfig DEDENT
                | 'external_resilience' ':' NEWLINE INDENT ExternalResilienceConfig DEDENT
                | 'rate_limiting' ':' NEWLINE INDENT RateLimitConfig DEDENT
                | 'monitoring' ':' NEWLINE INDENT MonitoringConfig DEDENT

ResilienceConfig ::= 'timeout' ':' TimeValue NEWLINE
                     'retry' ':' NEWLINE INDENT RetryConfig DEDENT
                     'fallback' ':' NEWLINE INDENT FallbackConfig DEDENT

TimeValue ::= Integer TimeUnit

RetryConfig ::= 'max_attempts' ':' Integer NEWLINE
                'backoff' ':' BackoffStrategy NEWLINE

BackoffStrategy ::= 'fixed' | 'exponential' | 'linear'

FallbackConfig ::= 'enabled' ':' Boolean NEWLINE
                   'strategy' ':' FallbackStrategy NEWLINE

FallbackStrategy ::= 'return_cached' | 'return_default' | 'fail_fast'

ExternalResilienceConfig ::= 'default_timeout' ':' TimeValue NEWLINE
                              'default_retry' ':' NEWLINE INDENT RetryConfig DEDENT

CachingConfig ::= 'enabled' ':' Boolean NEWLINE
                  'ttl' ':' TimeValue NEWLINE
                  'key_generation' ':' CacheKeyStrategy NEWLINE

CacheKeyStrategy ::= 'auto' | 'custom'

MonitoringConfig ::= 'enabled' ':' Boolean NEWLINE
                     'metrics' ':' MetricsList NEWLINE

MetricsList ::= '[' Metric (',' Metric)* ']'

Metric ::= Identifier

(* ===== 基本符號 ===== *)
Identifier     ::= Letter (Letter | Digit | '_')*
APIId          ::= Identifier
IntegrationId  ::= Identifier
OperationId    ::= Identifier
FieldName      ::= Identifier ('.' Identifier)*
String         ::= '"' StringContent '"'
StringContent  ::= (Character - '"')*
Character      ::= ? 任何字符 ?
Number         ::= DigitSequence ('.' DigitSequence)?
Integer        ::= DigitSequence
Boolean        ::= 'true' | 'false'
DigitSequence  ::= Digit+
Digit          ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
Letter         ::= 'a' | 'b' | ... | 'z' | 'A' | 'B' | ... | 'Z'
Object         ::= '{' KeyValuePair (',' KeyValuePair)* '}'
KeyValuePair   ::= String ':' Value
Value          ::= String | Number | Boolean | Array | Object
Array          ::= '[' Value (',' Value)* ']'
NEWLINE        ::= ? 換行符號 ?
INDENT         ::= ? 增加縮排 ?
DEDENT         ::= ? 減少縮排 ?
```

---

## 3. JSON Schema 定義

以下為 haAPI v3.2 的完整 JSON Schema，包含 25+ 核心定義。

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://wa-raptor.example.com/haapi/schema.json",
  "title": "haAPI Schema",
  "description": "Schema for High-level Abstract API Definition Language v3.2",
  "type": "object",
  "required": ["metadata", "apis"],
  "additionalProperties": false,
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["version"],
      "additionalProperties": false,
      "properties": {
        "version": {
          "type": "string",
          "pattern": "^3\\.2(\\.\\d+)?$",
          "description": "haAPI 規格版本"
        },
        "title": {
          "type": "string",
          "description": "API 集合標題"
        },
        "description": {
          "type": "string",
          "description": "API 集合描述"
        },
        "namespace": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*(\\.[a-zA-Z_][a-zA-Z0-9_]*)*$",
          "description": "命名空間"
        }
      }
    },
    "apis": {
      "type": "array",
      "items": { "$ref": "#/definitions/API" },
      "minItems": 1,
      "description": "API 定義清單"
    },
    "integrations": {
      "type": "array",
      "items": { "$ref": "#/definitions/Integration" },
      "description": "外部服務整合宣告"
    }
  },
  "definitions": {
    "API": {
      "type": "object",
      "required": ["api", "title", "entity"],
      "additionalProperties": false,
      "properties": {
        "api": {
          "type": "string",
          "pattern": "^[a-z0-9]([a-z0-9-]*[a-z0-9])?$",
          "description": "API 識別碼（kebab-case）"
        },
        "title": {
          "type": "string",
          "minLength": 1,
          "description": "API 標題"
        },
        "version": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+(\\.\\d+)?$",
          "description": "API 版本（SemVer）"
        },
        "entity": {
          "type": "string",
          "pattern": "^[A-Za-z_][a-zA-Z0-9_]*$",
          "description": "主要實體（引用 DBML）"
        },
        "description": {
          "type": "string",
          "description": "API 說明"
        },
        "tags": {
          "type": "array",
          "items": { "type": "string" },
          "description": "分類標籤"
        },
        "deprecated": {
          "type": "boolean",
          "default": false,
          "description": "是否已棄用"
        },
        "integrations": {
          "type": "array",
          "items": { "$ref": "#/definitions/Integration" },
          "description": "服務整合"
        },
        "exposes": {
          "$ref": "#/definitions/Exposes",
          "description": "公開的業務能力"
        },
        "access": {
          "$ref": "#/definitions/Access",
          "description": "存取控制"
        },
        "consumers": {
          "type": "array",
          "items": { "$ref": "#/definitions/Consumer" },
          "description": "消費者清單"
        },
        "advanced": {
          "$ref": "#/definitions/Advanced",
          "description": "進階配置"
        }
      }
    },
    "Integration": {
      "type": "object",
      "required": ["name"],
      "additionalProperties": false,
      "properties": {
        "name": {
          "type": "string",
          "description": "整合名稱"
        },
        "service": {
          "type": "string",
          "description": "服務名稱"
        },
        "capabilities": {
          "type": "array",
          "items": { "type": "string" },
          "description": "能力清單"
        },
        "resilience": {
          "$ref": "#/definitions/Resilience"
        },
        "timeout": {
          "type": "string",
          "pattern": "^\\d+(ms|s|m)$",
          "description": "超時設定"
        },
        "retry": {
          "$ref": "#/definitions/Retry"
        }
      }
    },
    "Exposes": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "standard": {
          "oneOf": [
            {
              "type": "array",
              "items": {
                "type": "string",
                "enum": ["list", "create", "read", "update", "patch", "delete", "exists"]
              }
            },
            {
              "type": "string",
              "enum": ["crud", "all"]
            }
          ],
          "description": "標準 CRUD 操作"
        },
        "list": {
          "$ref": "#/definitions/ListCapability"
        },
        "operations": {
          "type": "array",
          "items": { "$ref": "#/definitions/Operation" },
          "description": "自訂業務操作"
        }
      }
    },
    "ListCapability": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "filters": {
          "type": "array",
          "items": { "$ref": "#/definitions/Filter" },
          "description": "篩選能力"
        },
        "sorting": {
          "$ref": "#/definitions/Sorting"
        },
        "pagination": {
          "$ref": "#/definitions/Pagination"
        },
        "search": {
          "$ref": "#/definitions/Search"
        },
        "aggregations": {
          "type": "array",
          "items": { "type": "string" },
          "description": "聚合能力"
        },
        "includes": {
          "type": "array",
          "items": { "type": "string" },
          "description": "關聯包含"
        }
      }
    },
    "Filter": {
      "type": "object",
      "required": ["field"],
      "additionalProperties": false,
      "properties": {
        "field": {
          "type": "string",
          "description": "欄位名稱"
        },
        "operators": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["eq", "ne", "gt", "gte", "lt", "lte", "in", "nin",
                     "contains", "starts_with", "ends_with", "between", "match"]
          },
          "description": "支援的操作符"
        },
        "nullable": {
          "type": "boolean",
          "description": "是否可為空"
        }
      }
    },
    "Sorting": {
      "type": "object",
      "required": ["fields"],
      "additionalProperties": false,
      "properties": {
        "fields": {
          "type": "array",
          "items": { "type": "string" },
          "description": "可排序欄位"
        },
        "default": {
          "type": "string",
          "pattern": "^\\w+:(asc|desc)$",
          "description": "預設排序"
        }
      }
    },
    "Pagination": {
      "type": "object",
      "required": ["style", "default_size", "max_size"],
      "additionalProperties": false,
      "properties": {
        "style": {
          "type": "string",
          "enum": ["offset", "cursor", "page"],
          "description": "分頁方式"
        },
        "default_size": {
          "type": "integer",
          "minimum": 1,
          "description": "預設頁面大小"
        },
        "max_size": {
          "type": "integer",
          "minimum": 1,
          "description": "最大頁面大小"
        }
      }
    },
    "Search": {
      "type": "object",
      "required": ["fields", "type"],
      "additionalProperties": false,
      "properties": {
        "fields": {
          "type": "array",
          "items": { "type": "string" },
          "description": "搜尋欄位"
        },
        "type": {
          "type": "string",
          "enum": ["fulltext", "simple"],
          "description": "搜尋類型"
        }
      }
    },
    "Operation": {
      "type": "object",
      "required": ["name"],
      "additionalProperties": false,
      "properties": {
        "name": {
          "type": "string",
          "pattern": "^[a-z_][a-z0-9_]*$",
          "description": "操作名稱（snake_case）"
        },
        "description": { "type": "string" },
        "method": {
          "type": "string",
          "enum": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD"],
          "description": "HTTP 方法"
        },
        "path": { "type": "string", "description": "路徑範本" },
        "batch": { "type": "boolean", "description": "是否批次操作" },
        "async": { "type": "boolean", "description": "是否非同步" },
        "params": {
          "type": "array",
          "items": { "type": "object", "additionalProperties": { "type": "string" } },
          "description": "參數清單"
        },
        "formats": {
          "type": "array",
          "items": { "type": "string" },
          "description": "支援格式"
        },
        "cache": { "type": "integer", "minimum": 0, "description": "快取秒數" },
        "workflow": { "type": "boolean", "description": "工作流操作" },
        "require_reason": { "type": "boolean", "description": "需要原因" },
        "proxy": { "$ref": "#/definitions/Proxy" },
        "sql_hint": { "type": "string", "description": "SQL 提示" },
        "logic": { "$ref": "#/definitions/Logic" }
      }
    },
    "Proxy": {
      "type": "object",
      "required": ["target"],
      "additionalProperties": false,
      "properties": {
        "target": {
          "type": "string",
          "pattern": "^ext\\.[a-z_]+\\.[a-z_]+$",
          "description": "轉發目標（ext.<service>.<method>）"
        },
        "enrich": { "type": "object", "description": "補入參數" },
        "pick": {
          "type": "array",
          "items": { "type": "string" },
          "description": "擷取欄位"
        }
      }
    },
    "Logic": {
      "type": "object",
      "required": ["steps", "returns"],
      "additionalProperties": false,
      "properties": {
        "steps": {
          "type": "array",
          "items": { "$ref": "#/definitions/LogicStep" },
          "description": "邏輯步驟"
        },
        "returns": { "type": "object", "description": "回傳值" },
        "mode": {
          "type": "string",
          "enum": ["sync", "async_job"],
          "description": "執行模式"
        }
      }
    },
    "LogicStep": {
      "type": "object",
      "required": ["action"],
      "additionalProperties": false,
      "properties": {
        "action": { "type": "string", "description": "步驟動作" },
        "sql": { "type": "string", "description": "SQL 語句" },
        "rule": { "type": "string", "description": "驗證規則" },
        "input": { "type": "object", "description": "輸入值" },
        "result": { "type": "string", "description": "結果變數" },
        "on_fail": { "$ref": "#/definitions/ErrorHandling" },
        "on_empty": { "$ref": "#/definitions/ErrorHandling" },
        "items": { "type": "string", "description": "迴圈項目" },
        "steps": {
          "type": "array",
          "items": { "$ref": "#/definitions/LogicStep" },
          "description": "子步驟"
        },
        "resilience": { "$ref": "#/definitions/Resilience" }
      }
    },
    "ErrorHandling": {
      "type": "object",
      "required": ["status", "message"],
      "additionalProperties": false,
      "properties": {
        "status": { "type": "integer", "description": "HTTP 狀態碼" },
        "message": { "type": "string", "description": "錯誤訊息" },
        "side_effect": {
          "type": "object",
          "additionalProperties": { "type": "string" },
          "description": "副作用"
        }
      }
    },
    "Access": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "rules": {
          "type": "array",
          "items": { "$ref": "#/definitions/AccessRule" },
          "description": "存取規則"
        }
      }
    },
    "AccessRule": {
      "type": "object",
      "required": ["operation"],
      "additionalProperties": false,
      "properties": {
        "operation": { "type": "string", "description": "操作名稱" },
        "requires_roles": {
          "type": "array",
          "items": { "type": "string" },
          "description": "所需角色"
        },
        "requires_permissions": {
          "type": "array",
          "items": { "type": "string" },
          "description": "所需權限"
        },
        "requires_authentication": { "type": "boolean", "description": "需要認證" },
        "rate_limit": { "$ref": "#/definitions/RateLimit" }
      }
    },
    "RateLimit": {
      "type": "object",
      "required": ["requests", "per"],
      "additionalProperties": false,
      "properties": {
        "requests": { "type": "integer", "minimum": 1, "description": "請求數" },
        "per": {
          "type": "string",
          "enum": ["second", "minute", "hour", "day"],
          "description": "時間單位"
        }
      }
    },
    "Consumer": {
      "type": "object",
      "required": ["page"],
      "additionalProperties": false,
      "properties": {
        "page": { "type": "string", "description": "頁面 ID" },
        "uses": {
          "type": "array",
          "items": { "type": "string" },
          "description": "使用的操作"
        },
        "binds": { "type": "object", "description": "綁定映射" }
      }
    },
    "Advanced": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "resilience": { "$ref": "#/definitions/Resilience" },
        "caching": { "$ref": "#/definitions/Caching" },
        "external_resilience": { "$ref": "#/definitions/Resilience" },
        "rate_limiting": { "$ref": "#/definitions/RateLimit" },
        "monitoring": { "$ref": "#/definitions/Monitoring" }
      }
    },
    "Resilience": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "timeout": {
          "type": "string",
          "pattern": "^\\d+(ms|s|m)$",
          "description": "超時設定"
        },
        "retry": { "$ref": "#/definitions/Retry" },
        "fallback": { "$ref": "#/definitions/Fallback" }
      }
    },
    "Retry": {
      "type": "object",
      "required": ["max_attempts", "backoff"],
      "additionalProperties": false,
      "properties": {
        "max_attempts": { "type": "integer", "minimum": 1, "description": "最大嘗試次數" },
        "backoff": {
          "type": "string",
          "enum": ["fixed", "exponential", "linear"],
          "description": "退避策略"
        }
      }
    },
    "Fallback": {
      "type": "object",
      "required": ["enabled", "strategy"],
      "additionalProperties": false,
      "properties": {
        "enabled": { "type": "boolean", "description": "是否啟用" },
        "strategy": {
          "type": "string",
          "enum": ["return_cached", "return_default", "fail_fast"],
          "description": "降級策略"
        }
      }
    },
    "Caching": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "enabled": { "type": "boolean", "description": "是否啟用" },
        "ttl": {
          "type": "string",
          "pattern": "^\\d+(ms|s|m|h)$",
          "description": "存活時間"
        },
        "key_generation": {
          "type": "string",
          "enum": ["auto", "custom"],
          "description": "快取鑰匙生成策略"
        }
      }
    },
    "Monitoring": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "enabled": { "type": "boolean", "description": "是否啟用" },
        "metrics": {
          "type": "array",
          "items": { "type": "string" },
          "description": "度量清單"
        }
      }
    }
  }
}
```

---

## 4. 語義規則表

### 4.1 API 定義語義（API Definition）

| 字段 | 類型 | 必需 | 有效值 | 命名慣例 | 說明 |
|------|------|:----:|--------|----------|------|
| `api` | String | Y | kebab-case | `user-management` | API 識別碼 |
| `title` | String | Y | 任意字串 | — | API 顯示名稱 |
| `version` | String | — | X.Y.Z | `1.0.0` | 語義版本號 |
| `entity` | String | Y | PascalCase | `User` | DBML 主要實體引用 |
| `description` | String | — | 任意字串 | — | API 用途說明 |
| `tags` | Array | — | `[tag1, tag2]` | — | 分類標籤 |
| `deprecated` | Boolean | — | `true` / `false` | — | 棄用標記（預設 `false`） |

### 4.2 業務能力定義語義（Exposes）

| 區塊 | 說明 | 必需 | 內容 |
|------|------|:----:|------|
| `standard` | 標準 CRUD | — | 陣列 `[list, create, ...]` 或簡寫 `crud` / `all` |
| `list` | 列表查詢能力 | — | filters, sorting, pagination, search, aggregations, includes |
| `operations` | 自訂業務操作 | — | 完整操作定義陣列 |

#### 4.2.1 標準操作與 HTTP 對應

| 操作 | HTTP 方法 | 路徑 | 說明 |
|------|----------|------|------|
| `list` | GET | `/entities` | 列表查詢（支援篩選、排序、分頁） |
| `create` | POST | `/entities` | 建立記錄 |
| `read` | GET | `/entities/{id}` | 讀取單筆記錄 |
| `update` | PUT | `/entities/{id}` | 完整更新（覆蓋所有欄位） |
| `patch` | PATCH | `/entities/{id}` | 部分更新（僅更新指定欄位） |
| `delete` | DELETE | `/entities/{id}` | 刪除記錄 |
| `exists` | HEAD | `/entities/{id}` | 存在性檢查（無回應主體） |

> **簡寫**：`standard: crud` 等同 `[create, read, update, delete]`；`standard: all` 等同所有 7 種標準操作。

### 4.3 查詢能力語義（List Capability）

| 字段 | 類型 | 說明 | 預設值 |
|------|------|------|--------|
| `filters` | Array\<Filter\> | 篩選欄位配置 | — |
| `sorting` | Object | 排序配置（fields + default） | — |
| `pagination` | Object | 分頁配置（style + size） | offset, 20, 100 |
| `search` | Object | 全文搜尋配置 | — |
| `aggregations` | Array\<String\> | 聚合操作名稱 | — |
| `includes` | Array\<String\> | 關聯資料載入 | — |

#### 4.3.1 篩選操作符（Filter Operators）

| 操作符 | 用途 | 適用類型 | 查詢範例 |
|--------|------|----------|----------|
| `eq` | 等於 | all | `status[eq]=active` |
| `ne` | 不等於 | all | `status[ne]=deleted` |
| `gt` | 大於 | number, date | `amount[gt]=1000` |
| `gte` | 大於等於 | number, date | `created_at[gte]=2026-01-01` |
| `lt` | 小於 | number, date | `price[lt]=100` |
| `lte` | 小於等於 | number, date | `age[lte]=18` |
| `in` | 在集合中 | all | `status[in]=active,pending` |
| `nin` | 不在集合中 | all | `role[nin]=guest,banned` |
| `contains` | 包含子字串 | string | `name[contains]=john` |
| `starts_with` | 以...開始 | string | `email[starts_with]=admin` |
| `ends_with` | 以...結尾 | string | `domain[ends_with]=.com` |
| `between` | 區間（含兩端） | number, date | `price[between]=100,1000` |
| `match` | 正則表達式 | string | `code[match]=^[A-Z]{3}` |

> **Operator 預設規則**：`operators` 清單的 **第一個元素即為該欄位的預設 operator**。呼叫 List API 時若未指定 operator，後端一律套用此預設。規格作者透過調整清單順序來決定預設行為。
>
> 範例：
> ```yaml
> filters:
>   - field: userId
>     operators: [contains, eq, starts_with]   # 第一個 = contains = 預設
> ```
> 上例中 `GET /api/info-user?userId=john` 未指定 operator，後端套用預設 `contains`，
> 產生 `WHERE userId LIKE '%john%'` 形式的 SQL。
> 若改為 `operators: [eq, contains, starts_with]`，同一請求則為 `WHERE userId = 'john'`。

#### 4.3.2 分頁樣式（Pagination Style）

| 樣式 | 說明 | 適用場景 |
|------|------|----------|
| `offset` | 偏移量分頁（skip/take） | 一般列表、已知總筆數 |
| `cursor` | 游標分頁（next/prev token） | 大量資料、即時串流 |
| `page` | 頁碼分頁（page/page_size） | 傳統分頁 UI |

#### 4.3.3 搜尋類型（Search Type）

| 類型 | 說明 | 實作方式 |
|------|------|----------|
| `fulltext` | 全文搜尋 | 資料庫全文索引（CONTAINS/MATCH、分詞、詞幹） |
| `simple` | 簡單匹配 | 字串匹配（LIKE '%xxx%'），不需全文索引 |

### 4.4 自訂操作語義（Operations）

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| `name` | String | Y | 操作識別碼（snake_case） |
| `description` | String | — | 操作說明 |
| `method` | String | — | HTTP 方法（預設 `POST`） |
| `path` | String | — | 相對路徑（kebab-case） |
| `batch` | Boolean | — | 批次操作 |
| `async` | Boolean | — | 非同步處理 |
| `params` | Array | — | 參數清單 |
| `formats` | Array | — | 支援格式（csv, excel, pdf） |
| `cache` | Integer | — | 快取秒數 |
| `workflow` | Boolean | — | 工作流程操作 |
| `require_reason` | Boolean | — | 需要操作原因欄位 |
| `proxy` | Object | — | 代理配置（見 4.4.1） |
| `sql_hint` | String | — | SQL 提示（見 4.4.2） |
| `logic` | Object | — | 邏輯步驟（見 4.4.3） |

> **互斥規則**：`proxy`、`sql_hint`、`logic` 三者只能選其一。

#### 4.4.1 Proxy 語義（純代理操作）

看到 `proxy` 就表示此 operation 沒有本地業務邏輯，CodeGen 只需產生轉發程式碼。

| 屬性 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| `target` | String | Y | 轉發目標，`ext.<service>.<method>` 語法 |
| `enrich` | Object | — | 自動補入的額外請求參數 |
| `pick` | Array | — | 從外部回應中只擷取的欄位列表 |

```yaml
# 範例
proxy:
  target: ext.captcha.validate
  enrich: { complexity: high, ttl: 300 }
  pick: [id, score, success]
```

#### 4.4.2 sql_hint 語義（單行 SQL 提示）

適用於單一 SQL 即可完成的簡單操作。使用 `@paramName` 作為參數佔位符。

```yaml
sql_hint: "UPDATE Product SET status='ACTIVE', activatedAt=GETDATE() WHERE productId=@productId"
```

#### 4.4.3 Logic 語義（多步驟邏輯）

適用於多步驟、有分支、需要跨表操作的複雜操作。

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| `steps` | Array\<LogicStep\> | Y | 邏輯步驟序列 |
| `returns` | Object | Y | 自訂回傳結構 |
| `mode` | String | — | 執行模式：`sync`（預設）/ `async_job` |

#### 4.4.4 Action Types（邏輯步驟動作類型）

| Action | 說明 | 必要屬性 | 選用屬性 |
|--------|------|----------|----------|
| `query` | SELECT 查詢 | `sql`, `result` | `on_empty` |
| `update` | UPDATE 語句 | `sql` | `on_fail` |
| `insert` | INSERT 語句 | `sql` | `on_fail` |
| `upsert` | MERGE/UPSERT | `sql` | `on_fail` |
| `validate` | 條件驗證 | `rule`, `on_fail` | — |
| `ext.<service>.<method>` | 呼叫外部服務 | `input` | `result`, `on_fail`, `resilience` |
| `foreach` | 迴圈處理 | `items`, `steps` | — |
| `create_job` | 建立非同步任務 | `returns` | — |
| `parse_file` | 解析上傳檔案 | `format`, `result` | — |
| `update_job` | 更新任務狀態 | `status`, `returns` | — |

#### 4.4.5 ext.* 命名空間語法

外部服務呼叫使用三段式格式：`ext.<service>.<method>`

```yaml
# 範例
- action: ext.captcha.validate       # 驗證碼驗證
- action: ext.smtp.send_email        # 寄送郵件
- action: ext.stripe.create_charge   # 建立支付
- action: ext.llm.invoke             # 呼叫 LLM
```

**命名空間規則**：
- `ext` 前綴表示外部服務呼叫
- `<service>` 必須在 `integrations` 中有宣告
- `<method>` 必須在該 service 的 `capabilities` 中列出

**Step 欄位慣例**：
- `input`：step 級傳入值（區分於 operation-level 的 `params`）
- `result`：step 級回傳值（統一命名，不混用 `output`）
- `resilience`：選擇性，僅在需要覆蓋預設值時使用
- `on_fail`：錯誤處理

#### 4.4.6 錯誤處理語義

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| `on_empty` | Object | — | 查詢無結果時觸發（僅適用 `query`） |
| `on_fail` | Object | — | 操作失敗時觸發 |
| `status` | Integer | Y | HTTP 狀態碼（200-599） |
| `message` | String | Y | 錯誤訊息 |
| `side_effect` | Object | — | 失敗時的副作用（如記錄日誌） |

```yaml
# 範例
on_fail:
  status: 403
  message: "此帳號已被停用"
  side_effect:
    sql: |
      INSERT INTO ApiLog (action, userId, message)
      VALUES ('login_failed', @userId, '帳號已停用')
```

#### 4.4.7 實作複雜度選擇指引

| 複雜度 | 用什麼 | 範例 |
|--------|--------|------|
| 單一 SQL | `sql_hint: "..."` | activate, deactivate |
| 多步驟、線性流 | `logic.steps: [...]` | assign_groups, change_password |
| 有分支/失敗處理 | `steps` + `on_fail` | login |
| 非同步/批次 | `logic.mode: async_job` + `foreach` | bulk_import |
| 外部整合 | `action: ext.<service>.<method>` | captcha 驗證, email 寄送 |
| 純代理轉發 | `proxy: { target: ext.*.* }` | captcha 代理, 檔案上傳代理 |

> 標準 CRUD 操作（list, create, read, update, delete）不需要 `sql_hint` 或 `logic`，CodeGen 引擎會從 DBML 模型自動推導。

### 4.5 外部服務整合語義（Integrations）

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| `name` | String | Y | 整合識別碼 |
| `service` | String | — | 外部服務名稱 |
| `capabilities` | Array | — | 能力清單（method 列表） |
| `timeout` | String | — | 超時設定（如 `30s`） |
| `retry` | Object | — | 重試配置 |
| `resilience` | Object | — | 彈性配置 |

**作用**：
1. CodeGen 根據 `integrations` 自動產生 client stub 和 DI 配置
2. Linter 驗證 `ext.<service>.<method>` 引用合法性
3. 支援 IDE auto-complete
4. 支援架構圖自動生成（外部依賴可視化）

### 4.6 存取控制語義（Access）

| 字段 | 類型 | 說明 |
|------|------|------|
| `requires_roles` | Array\<String\> | 所需角色清單（OR 關係：擁有其中一個即可） |
| `requires_permissions` | Array\<String\> | 所需權限清單（AND 關係：需全部擁有） |
| `requires_authentication` | Boolean | 是否需要認證 |
| `rate_limit` | Object | 速率限制 |

**預設行為**：
- 未指定任何 access rule 時：公開 API
- 指定 `requires_roles`：需要對應角色之一
- 指定 `requires_permissions`：需要全部對應權限

### 4.7 進階配置語義（Advanced）

| 字段 | 類型 | 說明 | 層級 |
|------|------|------|------|
| `resilience` | Object | 內部服務彈性配置 | API 級 |
| `external_resilience` | Object | 外部服務彈性配置（覆蓋專案預設） | API 級 |
| `caching` | Object | 快取策略 | API 級 |
| `rate_limiting` | Object | 速率限制 | API 級 |
| `monitoring` | Object | 監控配置 | API 級 |

#### 4.7.1 三層級聯 Resilience 預設機制

外部服務呼叫的韌性屬性採用**級聯預設值 (Cascading Defaults)** 機制：

```
Step-level (最高優先) → API-level (advanced) → Project-level (codegen.config) → 框架內建預設
```

| 層級 | 配置位置 | 說明 |
|------|----------|------|
| **第一層**（專案級） | `codegen.config.yaml` | 全域預設，含實作細節（backoff 策略等） |
| **第二層**（API 級） | `advanced.external_resilience` | 覆蓋此 API 所有 ext.* 呼叫的預設 |
| **第三層**（Step 級） | `logic.steps[].resilience` | 僅用於例外情況 |

| 核心原則 | 說明 |
|----------|------|
| **沒寫就繼承** | Step 沒寫 → 用 API 的 → 用 codegen.config → 用框架內建值 |
| **寫了就覆蓋** | 任何一層明確指定的值覆蓋上一層（部分覆蓋，非全量取代） |
| **意圖歸 haAPI** | haAPI 只寫「我要什麼」：timeout 多久、重試幾次 |
| **實作歸 config** | codegen.config 負責「怎麼做」：backoff 策略、觸發狀態碼 |

### 4.8 消費者語義（Consumers）

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| `page` | String | Y | HaPDL 頁面 ID |
| `uses` | Array | — | 該頁面使用的操作清單 |
| `binds` | Object | — | 頁面與 API 的綁定映射 |

### 4.9 命名慣例總表

| 元素 | 慣例 | 範例 |
|------|------|------|
| `api` | kebab-case | `user-management` |
| `entity` | PascalCase | `User`, `UserRole` |
| `operations` (name) | snake_case | `reset_password`, `bulk_import` |
| `paths` | kebab-case | `/reset-password`, `/bulk-import` |
| `parameters` | snake_case | `user_id`, `created_at` |
| `models` (生成物) | PascalCase | `CreateUserRequest` |
| `ext.*` 命名空間 | `ext.<service>.<method>` | `ext.smtp.send_email` |

---

## 5. 語法與語義說明

### 5.1 文件基本結構

一份 haAPI 文件的基本結構如下：

```yaml
# API 識別與元資料
api: <api-identifier>           # kebab-case 格式（必要）
title: <api-title>              # API 顯示名稱（必要）
entity: <EntityName>            # 主要領域實體，來自 DBML（必要）
version: <version>              # 版本號（選用）
description: <description>      # API 用途說明（選用）
tags: [tag1, tag2]             # 分類標籤（選用）
deprecated: false               # 是否已棄用（選用）

# 外部服務依賴宣告
integrations:
  <integration-declarations>

# 業務能力定義
exposes:
  <capability-definitions>

# 關聯欄位自動填充（可選，v3.3+ codegen 支援）
# TODO: 此語法已由 whyAPI codegen 實作，待正式納入 haAPI spec
# 參考：ccwLog/0522-whyAPI_fixLog.md ERR-W09-CODEGEN
derived_fields:
  <derived-field-definitions>

# 存取控制
access:
  <access-controls>

# 前端關聯
consumers:
  <consumer-definitions>

# 進階配置
advanced:
  <advanced-settings>
```

### 5.2 漸進式複雜度

haAPI 支持從最簡到完整的三種寫法：

#### 最簡版本（Minimal）

```yaml
api: user-api
entity: User
exposes:
  standard: crud
access:
  roles:
    admin: all
    user: [list, read]
```

自動推斷：標題 "User API"、路徑 `/users`、標準 CRUD 端點、預設分頁與排序。

#### 標準版本（Standard）

```yaml
api: user-api
title: 使用者管理 API
entity: User
version: 1.0

exposes:
  standard: [list, create, read, update, delete]
  list:
    filters:
      - field: name
        operators: [contains, starts_with]
      - field: status
        operators: [eq, in]
    sorting:
      fields: [name, created_at]
      default: created_at:desc
    pagination:
      style: offset
      default_size: 20
      max_size: 100
  operations:
    - activate
    - deactivate
    - reset_password

access:
  roles:
    admin: all
    manager: [list, read, update]
    user: [list, read]

consumers:
  pages: [user-list, user-detail, user-edit]
```

#### 完整版本（Full）

包含自訂操作、複雜邏輯、外部服務整合、進階配置等所有區段（見[第 7 節完整範例](#7-完整範例)）。

### 5.3 查詢能力詳細語法

#### 篩選條件（Filters）

```yaml
list:
  filters:
    - field: status
      operators: [eq, ne, in]         # 支援的操作符清單

    - field: created_at
      operators: [gt, gte, lt, lte, between]

    - field: name
      operators: [contains, starts_with, ends_with]
      nullable: true                    # 允許 null 值篩選
      # 預設 operator = operators[0] = contains（不需另外宣告）
```

#### 排序（Sorting）

```yaml
list:
  sorting:
    fields: [id, name, created_at, updated_at]    # 可排序欄位
    default: created_at:desc                        # 預設排序
```

#### 分頁（Pagination）

```yaml
list:
  pagination:
    style: offset          # offset | cursor | page
    default_size: 20       # 預設每頁筆數
    max_size: 100          # 最大每頁筆數
```

#### 搜尋（Search）

```yaml
list:
  search:
    fields: [name, email, description]    # 搜尋欄位
    type: fulltext                         # fulltext | simple
```

#### 聚合（Aggregations）

```yaml
list:
  aggregations:
    - count_by_status         # group_by 類型
    - avg_price_by_category   # avg 類型
    - sum_amount              # sum 類型
```

#### 關聯載入（Includes）

```yaml
list:
  includes:
    - department      # 預設不載入
    - roles           # 可配合 default: true 預設載入
    - manager
```

### 5.4 自訂操作詳細語法

#### 簡單操作（使用預設慣例）

```yaml
operations:
  - activate              # POST /entities/{id}/activate
  - deactivate           # POST /entities/{id}/deactivate
  - archive              # POST /entities/{id}/archive
```

#### 詳細操作定義

```yaml
operations:
  - name: transfer_ownership
    description: 轉移擁有權
    method: POST
    path: /{id}/transfer
    params:
      - new_owner_id: user_id
      - reason: string?         # ? 表示選擇性參數
```

#### Proxy 操作（純代理）

```yaml
operations:
  - name: verify_captcha
    method: POST
    path: /verify-captcha
    proxy:
      target: ext.captcha.validate
      enrich: { complexity: high }
      pick: [id, score, success]
```

#### sql_hint 操作（單一 SQL）

```yaml
operations:
  - name: activate
    method: POST
    path: /{id}/activate
    sql_hint: "UPDATE InfoUser SET userType='A' WHERE userId=@userId"
```

#### Logic 操作（多步驟邏輯）

```yaml
operations:
  - name: change_password
    method: POST
    path: /{id}/change-password
    params:
      - old_password: string
      - new_password: string
    logic:
      steps:
        - action: query
          sql: "SELECT password FROM InfoUser WHERE userId = @userId"
          result: currentUser

        - action: validate
          rule: "decrypt(currentUser.password, 'Rijndael') == old_password"
          on_fail:
            status: 401
            message: "舊密碼不正確"

        - action: update
          sql: |
            UPDATE InfoUser
            SET password = encrypt(@new_password, 'Rijndael'),
                modify_time = GETDATE()
            WHERE userId = @userId

        - action: insert
          sql: |
            INSERT INTO userPWlog (userId, changeTime, password)
            VALUES (@userId, GETDATE(), encrypt(@new_password, 'Rijndael'))

      returns: { success: true, message: "密碼變更成功" }
```

#### 迴圈處理（foreach）

```yaml
- action: foreach
  items: rows               # 來自前一步驟的 result
  steps:
    - action: validate
      rule: "row.field matches '^[A-Z]+$'"
    - action: upsert
      sql: "MERGE INTO ... "
      on_fail:
        action: log_error
        continue: true       # 失敗後繼續處理下一筆
```

#### 回傳結構（returns）

```yaml
logic:
  steps: [...]
  returns:                   # 自訂回傳結構
    token: "@newToken"
    user:
      userId: "user.userId"
      userName: "user.userName"
  # 或簡單回傳
  returns: { success: true, message: "操作完成" }
  # 或回傳實體（預設）
  returns: InfoUser
```

### 5.5 外部服務整合語法

#### 宣告（Integrations）

```yaml
integrations:
  - name: captcha
    capabilities: [generate, validate]

  - name: smtp
    capabilities: [send_email]

  - name: llm
    capabilities: [invoke]
    timeout: 60s
```

#### 使用（ext.* 呼叫）

```yaml
logic:
  steps:
    - action: ext.captcha.validate
      input: { id: "@captcha_id", code: "@captcha_code" }
      result: captcha_result
      on_fail: { status: 403, message: "驗證碼錯誤" }

    - action: ext.smtp.send_email
      input: { to: "@user.email", template: "welcome" }
      result: email_sent

    - action: ext.llm.invoke
      input: { prompt: "@generated_prompt", max_tokens: 500 }
      result: ai_response
      resilience: { timeout: 60s }    # step 級覆蓋（例外情況）
```

### 5.5.5 關聯欄位自動填充（derived_fields）

> **⚠️ 待正式納入 spec（v3.3+）**：此語法已由 whyAPI codegen 完整實作（見 `ccwLog/0522-whyAPI_fixLog.md` FIX-W09-CODEGEN），尚未編入正式 spec。

#### 使用場景

當資料庫有**反正規化的衍生欄位**（例如 `ugrpName` 由 `ugrpId` 查詢關聯表填入），且前端只傳來來源欄位時，codegen 應自動在 INSERT/UPDATE 前補查目標欄位值。

#### 語法

```yaml
# 頂層宣告，與 exposes: 同層
derived_fields:
  - field: ugrpName           # 目標欄位（DB NOT NULL，需自動填充）
    derived_from: ugrpId      # 來源欄位（前端提供 List<String>）
    lookup:
      table: ugrp             # 關聯表
      key: ugrpId             # lookup 表的 key 欄位（對應 derived_from）
      value: ugrpName         # lookup 表的 value 欄位（對應 field）
```

#### 語義

- CodeGen 在 INSERT 和 UPDATE 方法中，若來源欄位（`derived_from`）有值且目標欄位（`field`）為 null，自動執行 lookup 查詢並填充目標欄位
- 來源欄位為 `List<String>` 時，生成 `IN (?,?,?)` 查詢，結果以逗號 join
- 來源欄位為 `String` 時，生成 `= ?` 查詢

#### 範例（InfoUser）

```yaml
api: info-user
entity: InfoUser

derived_fields:
  - field: ugrpName
    derived_from: ugrpId
    lookup:
      table: ugrp
      key: ugrpId
      value: ugrpName

exposes:
  standard: [list, create, read, update, delete]
```

codegen 產生的 Java 片段：
```java
// INSERT/UPDATE 前自動執行
if (in.ugrpId != null && !in.ugrpId.isEmpty() && in.ugrpName == null) {
    // SELECT ugrpName FROM ugrp WHERE ugrpId IN (?,?,...)
    in.ugrpName = String.join(",", resultList);
}
```

### 5.6 存取控制語法

#### 結構化模式（Structured Access Rules）

```yaml
access:
  rules:
    - operation: list
      requires_authentication: false     # 公開操作

    - operation: create
      requires_roles: [admin, merchant]
      rate_limit:
        requests: 100
        per: hour

    - operation: delete
      requires_roles: [admin]
      requires_permissions: [entity:delete]
      rate_limit:
        requests: 10
        per: day
```

### 5.7 符號簡寫系統

haAPI 支持一套符號簡寫，用於快速定義能力特徵：

| 符號 | 說明 | 範例 |
|------|------|------|
| `~` | 模糊搜尋 | `name~` |
| `@` | Email 格式驗證 | `email@` |
| `=` | 精確匹配 | `status=` |
| `>` | 大於 | `amount>` |
| `<` | 小於 | `amount<` |
| `[]` | 陣列包含 | `tags[]` |
| `><` | 範圍（between） | `created_at><` |
| `!` (sorting) | 預設排序欄位 | `created_at!` |
| `?` (includes) | 選擇性包含 | `department?` |
| `!` (includes) | 總是包含 | `roles!` |

```yaml
# 簡寫版
exposes:
  list:
    filters:
      - name~
      - email@
      - status=
      - created_at><
    sorting:
      - name
      - created_at!
    includes:
      - department?
      - roles!
```

### 5.8 路由慣例

```
標準操作:
  list:       GET    /entities
  create:     POST   /entities
  read:       GET    /entities/{id}
  update:     PUT    /entities/{id}
  patch:      PATCH  /entities/{id}
  delete:     DELETE /entities/{id}

自訂操作:
  動詞型:     POST /entities/{id}/activate
  資源型:     GET  /entities/{id}/metrics
  批次操作:   POST /entities/bulk-{action}
  匯入匯出:  POST /entities/import
              GET  /entities/export
```

---

## 6. Z3 約束驗證

haAPI 使用 Z3 SAT Solver 驗證定義的邏輯正確性，包含 6 種約束類型。

### 6.1 Z3 概念映射

| haAPI 概念 | Z3 表示 | 說明 |
|-----------|--------|------|
| API | 邏輯模組 | API 的完整邏輯規格 |
| Operation | 謂詞 | 操作的執行邏輯 |
| LogicStep | 函數 | 步驟的條件與結果 |
| Integration | 符號 | 外部服務的約束 |
| Access.Role | 集合 | 角色權限集合 |
| Parameter | 變數 | 參數值 |

### 6.2 約束類型 1：外部服務依賴約束

若操作使用外部服務呼叫，該服務必須在 integrations 中聲明。

```python
# Z3 邏輯式
ForAll([operation, step],
  Implies(
    usesExternalService(step, "stripe", "create_charge"),
    serviceDeclared(operation.api, "stripe", "create_charge")
  )
)
```

**驗證邏輯**：
- 若步驟呼叫 `ext.stripe.create_charge`，stripe 必須在 integrations 中聲明
- `create_charge` 必須在 stripe 的 capabilities 中列出
- 所有引用的外部服務都必須宣告

### 6.3 約束類型 2：邏輯步驟資料流約束

步驟引用的變數必須在前面的步驟中定義。

```python
# Z3 邏輯式
ForAll([steps, i, j],
  Implies(
    And(i < j, usesVariable(steps[j], var)),
    Or([isDefinedBy(steps[k], var) for k in range(i)])
  )
)
```

**驗證邏輯**：
- 無前向引用（步驟不能引用後續步驟的結果）
- 所有使用的變數都在前面定義過
- `result` 變數無重複定義

### 6.4 約束類型 3：操作存取控制約束

```python
# 操作需要認證
ForAll([user, operation],
  Implies(
    requiresAuthentication(operation),
    isAuthenticated(user)
  )
)

# 操作需要特定角色（OR 關係）
ForAll([user, operation],
  Implies(
    canExecute(user, operation),
    Or([hasRole(user, role) for role in operation.required_roles])
  )
)

# 操作需要特定權限（AND 關係）
ForAll([user, operation],
  Implies(
    canExecute(user, operation),
    And([hasPermission(user, perm) for perm in operation.required_permissions])
  )
)
```

**驗證邏輯**：
- 認證需求一致性
- 角色與權限不相互矛盾
- 公開 API 無矛盾的認證要求

### 6.5 約束類型 4：錯誤處理完整性約束

可能失敗的步驟必須有錯誤處理。

```python
ForAll([step],
  Implies(
    canFail(step),
    hasErrorHandler(step)
  )
)
```

**可能失敗的動作**：

| Action | 可能失敗 | 需要的處理 |
|--------|:--------:|-----------|
| `query` | Y | `on_empty` 或 `on_fail` |
| `validate` | Y | `on_fail` |
| `ext.*` | Y | `on_fail` |
| `update` | Y | `on_fail` |
| `insert` | Y | `on_fail` |
| `foreach` | — | 子步驟各自處理 |

### 6.6 約束類型 5：速率限制約束

```python
# 操作級限制不能超過 API 級限制
ForAll([api, operation],
  Implies(
    hasRateLimit(api) And hasRateLimit(operation),
    operation.rate_limit <= api.rate_limit
  )
)
```

**驗證邏輯**：
- 操作級速率限制 <= API 級速率限制
- 時間單位一致
- 限制值為正整數

### 6.7 約束類型 6：外部服務彈性配置約束

```python
ForAll([step, integration],
  Implies(
    callsIntegration(step, integration),
    And(
      step.timeout >= integration.timeout,
      step.retry.max_attempts <= integration.max_attempts * 2
    )
  )
)
```

**驗證邏輯**：
- 步驟超時 >= 整合定義的最小超時
- 重試次數合理（1-10 次）
- 退避策略有效（fixed / exponential / linear）
- 配置層級一致

---

## 7. 完整範例

### 7.1 電商系統 API 定義

```yaml
metadata:
  version: 3.2
  title: E-Commerce API Suite
  namespace: com.example.ecommerce.api
  description: 完整的電商 API 定義

integrations:
  - name: email_service
    service: smtp
    capabilities: [send_email, send_batch, schedule_email]
    timeout: 30s
    retry:
      max_attempts: 3
      backoff: exponential

  - name: payment_gateway
    service: stripe
    capabilities: [create_charge, refund, create_subscription]
    timeout: 15s
    resilience:
      timeout: 20s
      retry:
        max_attempts: 2
        backoff: exponential

  - name: llm_service
    service: openai
    capabilities: [invoke, embed, moderate]
    timeout: 60s

apis:
  # ==================== 商品 API ====================
  - api: product-api
    title: 商品管理 API
    version: 1.0.0
    entity: Product
    tags: [products, catalog]

    integrations:
      - name: llm_service
        service: openai
        capabilities: [invoke]

    exposes:
      standard: [list, create, read, update, delete]

      list:
        filters:
          - field: category
            operators: [eq, in]
          - field: price
            operators: [gt, lt, between]
          - field: name
            operators: [contains, starts_with]

        sorting:
          fields: [name, price, created_at, popularity]
          default: created_at:desc

        pagination:
          style: offset
          default_size: 20
          max_size: 100

        search:
          fields: [name, description, tags]
          type: fulltext

        aggregations:
          - count_by_category
          - avg_price_by_category

        includes:
          - category
          - reviews
          - inventory

      operations:
        # 批量匯入（async + foreach + logic）
        - name: bulk_import
          description: 批量匯入商品
          method: POST
          path: /import
          batch: true
          async: true
          params:
            - file: file
          logic:
            steps:
              - action: parse_file
                format: xlsx
                result: products

              - action: foreach
                items: products
                steps:
                  - action: validate
                    rule: "product.price > 0 && product.name != ''"
                    on_fail:
                      status: 400
                      message: "Invalid product data"

                  - action: insert
                    sql: |
                      INSERT INTO Product (name, price, category)
                      VALUES (@name, @price, @category)

              - action: create_job
                returns:
                  success: true
                  imported_count: "{{count}}"

        # LLM 推薦（ext.* + cache + logic）
        - name: calculate_recommendation
          description: 計算推薦商品
          method: GET
          path: /{id}/recommendations
          async: true
          cache: 3600
          logic:
            steps:
              - action: query
                sql: "SELECT * FROM Product WHERE id = @productId"
                result: product
                on_empty:
                  status: 404
                  message: "Product not found"

              - action: ext.llm.invoke
                input:
                  prompt: "Based on {{product.name}}, recommend 5 similar products"
                  max_tokens: 200
                result: recommendation

              - action: update
                sql: |
                  INSERT INTO ProductRecommendation (productId, recommendations, createdAt)
                  VALUES (@productId, @recommendation, GETDATE())

            returns:
              recommendations: "{{recommendation}}"

        # 上架（sql_hint）
        - name: activate
          description: 上架商品
          method: POST
          path: /{id}/activate
          sql_hint: "UPDATE Product SET status='ACTIVE', activatedAt=GETDATE() WHERE productId=@productId"

        # 下架（sql_hint）
        - name: archive
          description: 下架商品
          method: POST
          path: /{id}/archive
          sql_hint: "UPDATE Product SET status='ARCHIVED', archivedAt=GETDATE() WHERE productId=@productId"

        # 同步庫存（proxy）
        - name: sync_inventory
          description: 同步庫存到倉庫系統
          method: POST
          path: /{id}/sync-inventory
          proxy:
            target: ext.warehouse.update_inventory
            enrich: { sync_time: "{{now}}" }
            pick: [id, quantity, location]

    access:
      rules:
        - operation: list
          requires_authentication: false

        - operation: create
          requires_roles: [admin, merchant]
          rate_limit:
            requests: 100
            per: hour

        - operation: delete
          requires_roles: [admin]
          rate_limit:
            requests: 10
            per: day

    consumers:
      - page: product-list
        uses: [list, read]
        binds:
          filters: [category, price, search]
          actions: [create, delete]

      - page: product-detail
        uses: [read, update]

    advanced:
      resilience:
        timeout: 30s
        retry:
          max_attempts: 3
          backoff: exponential
        fallback:
          enabled: true
          strategy: return_cached

      caching:
        enabled: true
        ttl: 5m
        key_generation: auto

      external_resilience:
        timeout: 30s
        retry:
          max_attempts: 2
          backoff: exponential

      rate_limiting:
        requests: 1000
        per: hour

      monitoring:
        enabled: true
        metrics: [response_time, error_rate, cache_hit_ratio]

  # ==================== 訂單 API ====================
  - api: order-api
    title: 訂單管理 API
    version: 1.0.0
    entity: Order
    tags: [orders, transactions]

    integrations:
      - name: payment_gateway
        service: stripe
        capabilities: [create_charge, refund]
      - name: email_service
        service: smtp
        capabilities: [send_email]

    exposes:
      standard: [list, create, read, update]

      operations:
        - name: complete_order
          description: 完成訂單
          method: POST
          path: /{id}/complete
          workflow: true
          require_reason: true
          params:
            - reason: string
          logic:
            steps:
              - action: query
                sql: "SELECT * FROM Order WHERE orderId = @orderId"
                result: order
                on_empty:
                  status: 404
                  message: "Order not found"

              - action: validate
                rule: "order.status == 'PENDING'"
                on_fail:
                  status: 400
                  message: "Only pending orders can be completed"

              - action: ext.stripe.create_charge
                input:
                  amount: "{{order.amount}}"
                  currency: "{{order.currency}}"
                result: payment

              - action: validate
                rule: "payment.success == true"
                on_fail:
                  status: 402
                  message: "Payment failed"

              - action: update
                sql: |
                  UPDATE Order 
                  SET status='COMPLETED', completedAt=GETDATE()
                  WHERE orderId=@orderId

              - action: ext.smtp.send_email
                input:
                  to: "{{order.customer.email}}"
                  template: "order_confirmation"
                result: email_sent

            returns:
              success: true
              order_id: "{{order.orderId}}"
              payment_id: "{{payment.id}}"

    access:
      rules:
        - operation: list
          requires_roles: [user]

        - operation: create
          requires_authentication: true

        - operation: complete_order
          requires_roles: [admin, staff]
          rate_limit:
            requests: 50
            per: hour

    consumers:
      - page: order-list
        uses: [list, read]

      - page: order-detail
        uses: [read, update, complete_order]
```

### 7.2 使用者管理 API 定義

```yaml
api: user-management
title: 使用者管理 API
entity: User
version: 2.0
description: 組織使用者帳號管理，提供完整的 CRUD 操作與進階管理功能

integrations:
  - name: captcha
    capabilities: [generate, validate]
  - name: smtp
    capabilities: [send_email]

exposes:
  standard: [list, create, read, update, delete]

  list:
    filters:
      - field: name
        operators: [contains, starts_with]
      - field: email
        operators: [eq, contains]
      - field: department_id
        operators: [eq, in]
      - field: status
        operators: [eq, ne, in]
      - field: created_at
        operators: [gt, gte, lt, lte, between]

    sorting:
      fields: [id, name, email, created_at, last_login]
      default: created_at:desc

    pagination:
      style: offset
      default_size: 20
      max_size: 100

    search:
      fields: [name, email, bio]
      type: fulltext

    includes:
      - department
      - roles
      - manager

    aggregations:
      - count_by_status
      - count_by_department
      - avg_age

  operations:
    - name: activate
      description: 啟用使用者帳號
      method: POST
      path: /{id}/activate

    - name: deactivate
      description: 停用使用者帳號
      method: POST
      path: /{id}/deactivate
      params:
        - reason: string
        - effective_date: date?

    - name: reset_password
      description: 重設密碼
      method: POST
      path: /{id}/reset-password
      params:
        - temporary_password: string?
        - send_email: boolean
      logic:
        steps:
          - action: ext.smtp.send_email
            input: { to: "@user.email", template: "password_reset" }
            result: email_sent
            on_fail: { status: 502, message: "寄送重設密碼信件失敗" }

    - name: assign_roles
      description: 指派角色
      method: POST
      path: /{id}/roles
      params:
        - role_ids: string[]

    - name: revoke_roles
      description: 撤銷角色
      method: DELETE
      path: /{id}/roles
      params:
        - role_ids: string[]

    # Proxy 操作
    - name: get_captcha
      description: 取得驗證碼
      method: GET
      path: /captcha
      proxy:
        target: ext.captcha.generate
        pick: [id, image_data]

    - name: verify_captcha
      description: 驗證驗證碼
      method: POST
      path: /verify-captcha
      proxy:
        target: ext.captcha.validate
        pick: [success, score]

    - name: bulk_import
      description: 批次匯入使用者
      method: POST
      path: /import
      batch: true
      async: true
      params:
        - file: binary
        - format: enum[csv, excel]
        - dry_run: boolean

    - name: export
      description: 匯出使用者資料
      method: GET
      path: /export
      params:
        - format: enum[csv, excel, pdf]
        - fields: string[]?

access:
  rules:
    - operation: list
      requires_roles: [admin, manager, user]

    - operation: create
      requires_roles: [admin, manager]
      rate_limit:
        requests: 100
        per: hour

    - operation: delete
      requires_roles: [admin]

    - operation: bulk_import
      requires_roles: [admin]
      rate_limit:
        requests: 10
        per: day

consumers:
  - page: user-list
    uses: [list, create, export]

  - page: user-detail
    uses: [read, update, delete, activate, deactivate]

  - page: user-edit
    uses: [read, update, reset_password]

advanced:
  external_resilience:
    timeout: 15s
    retry:
      max_attempts: 3
      backoff: exponential
```

---

## 8. 驗證規則總覽

haAPI 定義需通過五層驗證：

### 8.1 第一層：語法驗證

| # | 規則 | 說明 |
|---|------|------|
| 1 | 所有必需字段存在 | `api`, `title`, `entity` 為必要 |
| 2 | API ID 遵循 kebab-case | `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$` |
| 3 | 操作 ID 遵循 snake_case | `^[a-z_][a-z0-9_]*$` |
| 4 | 版本號遵循 SemVer | `X.Y.Z` 格式 |
| 5 | YAML 語法正確 | 結構、縮排、型別 |
| 6 | HTTP 方法有效 | GET, POST, PUT, PATCH, DELETE, HEAD |
| 7 | 操作符有效 | 13 種定義的操作符之一 |

### 8.2 第二層：引用驗證

| # | 規則 | 說明 |
|---|------|------|
| 1 | `entity` 引用有效的 DBML 實體 | 跨檔案引用檢查 |
| 2 | `ext.*` 引用的 service 在 integrations 中聲明 | 外部服務宣告檢查 |
| 3 | `ext.*` 引用的 method 在 capabilities 中列出 | 能力清單檢查 |
| 4 | 消費者引用的頁面存在 | HaPDL 對齊檢查 |
| 5 | 操作引用一致 | access rules 引用的操作必須存在 |

### 8.3 第三層：語義驗證

| # | 規則 | 說明 |
|---|------|------|
| 1 | `proxy` / `sql_hint` / `logic` 只能選一個 | 互斥規則 |
| 2 | 外部服務呼叫使用 `ext.*` 語法 | 命名空間規則 |
| 3 | 步驟中的 `result` 變數無重複 | 唯一性規則 |
| 4 | 邏輯步驟順序合理 | 資料流方向性 |
| 5 | `on_empty` 只用於 `query` 步驟 | 語義匹配 |

### 8.4 第四層：跨規格驗證

| # | 規則 | 說明 |
|---|------|------|
| 1 | haAPI 操作與 HaPDL 動作對齊 | 前後端一致性 |
| 2 | 安全配置與 HaPDL 權限一致 | 角色/權限一致性 |
| 3 | 消費者綁定有效 | 頁面與操作的映射 |

### 8.5 第五層：邏輯驗證（Z3）

| # | 約束類型 | 說明 |
|---|----------|------|
| 1 | 外部服務依賴約束 | ext.* 引用解析 |
| 2 | 邏輯步驟資料流約束 | 無前向引用 |
| 3 | 存取控制約束 | 角色/權限一致性 |
| 4 | 錯誤處理完整性 | 可失敗步驟都有處理 |
| 5 | 速率限制約束 | 操作級 <= API 級 |
| 6 | 彈性配置約束 | 層級配置合理性 |

### 8.5 常見誤用與反模式（Anti-Pattern, v3.3 新增）

> Q14 決議：Anti-Pattern 整合進驗證規則章節，lint 訊息可直接引用本節編號。

| 編號 | 反模式 | 為何錯 | 正確寫法 |
|------|--------|--------|---------|
| **AP-01** | 在新規格用 `access.permissions` 結構 | 已於 v3.2 標為 dead-letter；codegen 在 v3.4 移除支援 | 改用 v3.2 引入的 `access.endpoints.{op}` + `access.operations.{op}`（雙軌結構，§2.3.1） |
| **AP-02** | 把 `rate_limit` 寫在 permission 區段 | rate_limit 是 endpoint 屬性而非權限屬性，混在 permission 內會在 codegen 階段被忽略 | 放在 `access.endpoints.{op}.rate_limit`（dead-letter 遷移對照表，§2.3.2） |
| **AP-03** | 同一 op 同時寫 `required_roles` 與 `required_permissions` 但無 AND/OR 註記 | 雙軌結構預設 AND 語意；PM 若預期 OR（其一即可）會造成過度限制 | 顯式宣告 `mode: AND` 或 `mode: OR`；預設 AND 時加註解說明 |
| **AP-04** | 在 `access.endpoints.{op}.conditions[]` 內聯邏輯字串 | 與 haARM 雙重事實源；haARM constraint 變更時 haAPI 內聯邏輯不會同步 | 用 `conditions[].haarm_constraint: <constraint_id>` opaque ref，由 haARM 持有事實 |
| **AP-05** | 把 resilience（timeout/retry/circuit_breaker）寫在每支 endpoint | 全域預設可在 `codegen.config.yaml` 一處設；逐 endpoint 寫造成維護地獄 | 用四層級聯（step → API → project → 框架），僅在覆寫時寫；見 §4.7.1 三層級聯預設機制 |

> **lint 觸發規則**：`haapi-lint` 在 v3.3 起檢查 AP-01～AP-05；違反 AP-01/AP-02/AP-04 為 **error**，AP-03/AP-05 為 **warning**。

---

## 9. 跨規格映射

### 9.1 haAPI <-> HaPDL

| haAPI | HaPDL | 說明 |
|-------|-------|------|
| `operations` | `actions.operations` | 操作名稱引用 |
| `access.requires_roles` | `security.field_level.visible_to_roles` | 角色需求 |
| `consumers.page` | 頁面 ID | 消費頁面映射 |

### 9.2 haAPI <-> Annotated DBML

| haAPI | DBML | 說明 |
|-------|------|------|
| `entity` | table name | 主要實體 |
| `list.filters[].field` | column name | 篩選欄位 |
| `list.search.fields` | 全文索引欄位 | 搜尋欄位 |

### 9.3 haAPI -> TypeSpec/OpenAPI

| haAPI | 生成物 | 說明 |
|-------|--------|------|
| `standard` | CRUD endpoints | 標準端點 |
| `operations` | custom endpoints | 自訂端點 |
| `access` | `@authorize` decorators | 授權規則 |
| `logic` | implementation steps | 業務邏輯 |
| `list.filters` | query parameters | 查詢參數 |
| `list.pagination` | pagination models | 分頁模型 |

### 9.4 轉換流程

```
DBML (Domain Model)
    |
haAPI (API Intent)
    |
TypeSpec (API Specification)
    |
    +-- OpenAPI (API Documentation)
    +-- Client SDK (客戶端)
    +-- Server Stub (伺服器骨架)
```

---

## 10. 工具鏈與最佳實踐

### 10.1 專案目錄結構

```
project/
+-- codegen.config.yaml              # 全域行為預設
+-- integrations.config.yaml         # 外部服務基礎設施設定
+-- models/
|   +-- schema.dbml                  # 領域模型
+-- api/
|   +-- user-management.haapi.yaml   # API 意圖定義
|   +-- order-management.haapi.yaml
+-- generated/                       # CodeGen 產出物
    +-- user-management.tsp
```

### 10.2 檔案命名

```
<api-identifier>.haapi.yaml

範例：
  product-api.haapi.yaml
  order-api.haapi.yaml
  user-management.haapi.yaml
```

### 10.3 CLI 工具

```bash
# 驗證 haAPI 規格
haapi validate user-management.haapi.yaml

# 檢查外部服務依賴完整性
haapi check-integrations \
    --api user-management.haapi.yaml \
    --config integrations.config.yaml

# 生成 TypeSpec
haapi generate \
    --input user-management.haapi.yaml \
    --dbml schema.dbml \
    --output generated/user-management.tsp

# 生成 OpenAPI
tsp compile generated/user-management.tsp \
    --emit @typespec/openapi3

# 檢查前後端同步
haapi sync-check \
    --api user-management.haapi.yaml \
    --pages user-list.hapdl.yaml
```

### 10.4 命名慣例

| 元素 | 慣例 | 正確範例 | 錯誤範例 |
|------|------|----------|----------|
| API ID | kebab-case | `user-management` | `userManagement` |
| Entity | PascalCase | `User` | `user` |
| Operation name | snake_case | `reset_password` | `resetPassword` |
| Path | kebab-case | `/reset-password` | `/reset_password` |
| Parameter | snake_case | `user_id` | `userId` |
| ext.* namespace | `ext.<svc>.<method>` | `ext.smtp.send_email` | `ext.Smtp.SendEmail` |

### 10.5 外部服務整合最佳實踐

1. **integrations 只宣告名稱和能力**，不放基礎設施細節（provider, api_key 等歸 infra config）
2. **resilience 大多數情況不需要寫**，讓 codegen.config 預設處理；只在有特殊需求時覆蓋
3. **純代理用 proxy，有邏輯用 logic.steps**
4. **所有可失敗步驟都需要錯誤處理**（on_fail / on_empty）

### 10.6 錯誤處理原則

```yaml
# 使用標準 HTTP 狀態碼
2xx: 成功
4xx: 客戶端錯誤
5xx: 伺服器錯誤

# 提供結構化錯誤訊息（problem+json 格式）
error_response:
  type: "https://example.com/errors/validation"
  title: "Validation Error"
  status: 400
  detail: "The request contains invalid fields"
  errors:
    - field: "email"
      message: "Invalid email format"
```

---

## 11. 附錄：遷移指南

### 11.1 v1.1 -> v1.2/v3.2 遷移清單

| 變更項目 | v1.1 | v1.2 (v3.2) | 向後相容 |
|----------|------|-------------|----------|
| 外部呼叫 action | `action: external` + `service` + `method` | `action: ext.<service>.<method>` | 否 |
| 外部呼叫傳入值 | `params: { ... }` (step 級) | `input: { ... }` | 否 |
| 外部呼叫回傳值 | `result` | `result`（不變） | 是 |
| 純代理操作 | 需完整 `logic.steps` | `proxy: { target, enrich, pick }` | 新增語法 |
| 外部服務宣告 | 無 | `integrations: [...]` | 新增區塊 |
| 韌性設定 | 無標準機制 | 三層級聯（step -> advanced -> codegen.config） | 新增機制 |
| 其他 action | `query`, `validate`, `foreach` 等 | 不變 | 是 |

### 11.2 遷移範例

```yaml
# v1.1（已棄用）
- action: external
  service: smtp
  method: send_email
  params: { to: "@user.email", subject: "Welcome" }
  result: email_sent

# v1.2 / v3.2（現行）
- action: ext.smtp.send_email
  input: { to: "@user.email", subject: "Welcome" }
  result: email_sent
```

### 11.3 版本歷程

| 版本 | 說明 |
|------|------|
| v1.1 | 初始版本，基本 CRUD + custom operations |
| v1.2 | ext.* 命名空間、proxy 原語、integrations 宣告、三層級聯 Resilience |
| v3.2 | 版本號對齊 haARM/HaPDL v3.2（功能同 v1.2） |

---

**文檔版本**：1.0
**對應規範**：haAPI v3.3、haARM v3.3、haPDL v3.3、Annotated DBML v3.3
**發佈日期**：2026-05-14（v3.3 RC）
**資料來源**：`8specDSLs/haAPI-specification_v3.3.md`、`8specDSLs/archive/haAPI-Structured-Specification-v3_2.md`（v3.2 落檔保存）、`8specDSLs/haAPI-Z3-Constraint-Validation.md`

---

## 附錄 A: §6 Convention over Configuration（v3.3 新增；M3 重排時升為正式 §6）

> v3.3 統一章節骨架中 §6 為 Convention over Configuration（見 §0.3）。本附錄是 haAPI 的 §6 內容；待 freeze 視窗結束（>2026-05-26）後由 M3 polish 升至正式編號。

### A.6.1 三段式優先序

```
   隱含預設值                慣例 Profile               明示覆寫
   (built-in defaults)  →   (named profile)        →   (explicit fields)
   ────────────────────     ──────────────────         ──────────────────
   standard: crud 自動展開    standard: [create]         exposes 全列
   entity 推 5 端點          整合 profile（如 saga）     operations 完全自訂
   路徑慣例（/api/<entity>）   resilience profile          per-step timeout 覆寫
```

### A.6.2 haAPI 預設值來源（兩處）

haAPI 沒有獨立的 defaults 檔案，預設值散佈在：

#### 1. 規格文件智慧推斷 — `haAPI-specification_v3.3.md`

| 預設規則 | 章節 | 範例 |
|---------|------|------|
| `standard: crud` → 5 端點 | §3（智慧推斷）| `POST/GET/GET-list/PATCH/DELETE` |
| entity 名 → 路徑/title/分頁自動推斷 | §4.2（路由慣例映射表） | `entity: Order` → `path: /api/orders, title: 訂單管理` |
| 操作命名慣例（`POST /users` → `createUser`） | §4.2.1 | 端點 → operation 名稱自動對應 |
| pagination 預設樣式 | §4.3.2 | `style: page-size`（傳統 page=1&size=20） |

#### 2. 外部設定 — `codegen.config.yaml` 四層級聯

```yaml
# codegen.config.yaml（專案根目錄）
defaults:
  resilience:
    timeout: 30s
    retry: { max_attempts: 3, backoff: exponential }
    circuit_breaker: { failure_threshold: 5, reset_after: 60s }
```

級聯優先序（高 → 低）：

```
step.resilience           （個別步驟覆寫）
  > API.resilience        （單 API 預設）
  > project.resilience    （project-level codegen.config.yaml）
  > framework defaults    （Resilience4j / Spring Retry 內建）
```

詳見 §4.7.1「三層級聯 Resilience 預設機制」。

### A.6.3 慣例 Profile 實例

| 觸發方式 | 範例檔 | 自動展開 |
|---------|--------|---------|
| `standard: crud` | `benchmarks/haAPI/simple-crud.haapi.yaml` | 5 端點 + 標準路徑 + 預設 access |
| `standard: [create, update]` | `benchmarks/haAPI/info-user.haapi.yaml` | 局部 sugar：僅展開列出的兩個操作 |
| `proxy:` 純代理 | §2.2.3 範例 | 一行展開為 forward + retry + error map |

### A.6.4 何時不該套 Convention

| 情境 | 替代方案 |
|------|---------|
| 非 RESTful 操作（如 Webhook、SSE） | 直接寫 `operations[]`，省略 `standard` |
| 整合非標準外部服務 | `integrations.config.yaml` 內顯式宣告 |
| 業務流程橫跨多 entity（saga） | 用 `logic[]` 多步驟，不套 standard CRUD |

### A.6.5 三欄對照範例（同一情境的三種寫法）

| 寫法 | 行數 | 適用對象 |
|------|------|---------|
| **最精簡**（純 standard）| 8 行 | PM：套用 80% 標準場景 |
| **慣例展開後**（standard + 局部 operations）| 25 行 | SA：覆寫 1-2 個特殊操作 |
| **明示覆寫**（完全自訂 operations[]）| 80+ 行 | 客製化專家：完全控制每個端點 |

詳見 §7 與 `benchmarks/haAPI/hycms-ht002.haapi.yaml`（M3 已落地）。

---

## 附錄 B: §7 跨規格整合（v3.3 新增；M3 已落地）

> v3.3 統一章節骨架 §7 = 跨規格整合（見 §0.3）。完整跨 DSL 導覽請見 [`CROSS-DSL-GUIDE.md`](CROSS-DSL-GUIDE.md)；本節僅列 haAPI 端的引用界面與 hycms-ht002 範例對應。

### B.7.1 haAPI 端的跨 DSL 引用點

| 引用點 | haAPI 欄位 | 對應目標 | 驗證規則 |
|--------|----------|---------|---------|
| Entity | `entity:` 頂層 | DBML `Table <Name>` | `validate_cross_dsl.py` Rule 2 |
| 端點權限 | `access.endpoints.{op}.required_permissions[].id` | haARM `permissions[].id` | Rule 3 |
| 端點角色 | `access.endpoints.{op}.required_roles[]` | haARM `roles[].id` | Rule 4 |
| 端點條件 | `access.endpoints.{op}.conditions[].haarm_constraint` | haARM `constraints[].id` | （v3.3 opaque ref，未自動驗證） |
| API 綁定 | `api:` 頂層 | haPDL `api:` | Rule 5 |

### B.7.2 hycms-ht002 範例對應

`benchmarks/haAPI/hycms-ht002.haapi.yaml` 體現端對端引用：

```yaml
api: hycms-ht002                    # ← 對應 haPDL page 的 api: 欄位
entity: InfoUser                    # ← 對應 DBML Table InfoUser

access:
  roles: [htsd, sysadm, audit]      # ← 對應 haARM roles[].id（平面化供 validator）
  permissions:                      # ← 對應 haARM permissions[].id（平面化）
    - infouser_read
    - infouser_create
    ...

  endpoints:                        # v3.3 Access v2 雙軌（細粒度）
    read:
      required_roles: [htsd, sysadm, audit]
      required_permissions:
        - id: infouser_read
```

跑 `python benchmarks/validate_cross_dsl.py hycms-ht002` 驗證引用一致性。

### B.7.3 與 `CROSS-DSL-GUIDE.md` 的關係

本節是 haAPI 視角的引用清單；CROSS-DSL-GUIDE.md 是四 DSL 平面的完整對應表（含版本互鎖、Anti-Pattern、同步機制）。**新增跨 DSL anchor 時須先讀 CROSS-DSL-GUIDE §3.2 流程**。

---
