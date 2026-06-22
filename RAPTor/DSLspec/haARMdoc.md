# haARM 完整參考手冊

**haARM — ha Actor-Role Modeling Language**

| 項目 | 說明 |
|------|------|
| 版本 | **v3.3.0 (Release Candidate, 2026-05-13)** |
| 對齊規格 | haAPI v3.3、haPDL v3.3、Annotated DBML v3.3、Gherkin BDD |
| 檔案格式 | YAML（`.haarm.yaml`） |
| 所屬框架 | WA-RAPTor（Web-based Application Requirements Analysis and Prototyping Tool） |
| 文件日期 | 2026-05-13 |
| 前版 | v2（見 `archive/haARM-Specification_v2.md`） |

---

## 目錄

0. [版本沿革](#0-版本沿革)
1. [設計理念與定位](#1-設計理念與定位)
2. [EBNF 文法定義（簡化版）](#2-ebnf-文法定義簡化版)
3. [BNF 正式文法規格（完整版）](#3-bnf-正式文法規格完整版)
4. [JSON Schema 定義](#4-json-schema-定義)
5. [語義規則表](#5-語義規則表)
6. [語法與語義說明](#6-語法與語義說明)
7. [Z3 約束驗證](#7-z3-約束驗證)
8. [完整範例](#8-完整範例)
9. [驗證規則總覽](#9-驗證規則總覽)
10. [跨規格映射](#10-跨規格映射)
11. [工具鏈與最佳實踐](#11-工具鏈與最佳實踐)
12. [附錄：遷移指南與擴展點](#12-附錄遷移指南與擴展點)

---

## 0. 版本沿革

### 0.1 跨 DSL 版本歷程（v1.0 → v3.3）

| 版本 | 日期 | 主要變更 |
|------|------|---------|
| v1.0 | 2026-04 早期 | 初版規格分散建立（haARM v1、haAPI v1.0、haPDL v1.0、DBML v1.1） |
| v2.0 | 2026-04 中 | haARM：新增 `resources` 區段、Permission `scope`、`$self`、`context:`、`TimeWindowCondition`、結構化 `Constraint.rule` |
| v3.0 | 2026-04 末 | haAPI 新增 `proxy`/`ext.*`/`logic`；haPDL 新增 State/Error/Async/A11y/Security/Testability |
| v3.1 | 2026-05 初 | haPDL：Scope Declaration、`security.permission_refs`、`datasource_scope` 雛形 |
| v3.2 | 2026-05-11 | haAPI Access v2 雙軌、PDL `permission_refs` 落地、DBML 四個自訂標註 |
| **v3.3** | **2026-05-13** | (a) haARM 跳版 v3.3，新增 `starts_with`/`ends_with` 運算子；(b) Convention over Configuration 三段式（預設 → 慣例 Profile → 明示覆寫）；(c) 一級欄位 `actor.enabled` / `role.implicit` / `resource.allowed_actions` / `permission.legacy_bit`；(d) `dynamic_grants` 文件化（預設 disabled，v3.4 落地）；(e) 四 DSL 統一 12 章骨架 |

### 0.2 v3.3 四 DSL 版本互鎖表

| DSL | 主檔（SSoT） | 規格檔 | 版本 | 對齊狀態 |
|-----|-------------|--------|------|---------|
| haAPI | `haAPIdoc.md` | `haAPI-specification_v3.3.md` | **v3.3.0** | Access v2 雙軌引用 haARM `permission.id`/`role.id` |
| haPDL | `haPDLdoc.md` | `haPDL-specification-v3.3.md` + `pdl-syntax-v3.3.md` | **v3.3.0** | `auth.roles[]` / `security.permission_refs` 對齊 haARM |
| haARM | `haARMdoc.md` | `haARM-Specification_v3.3.md` | **v3.3.0** | 新增 `starts_with`，引入 profile / auto_infer |
| DBML | `annotated_DBML-v3.3.md` | — | **v3.3.0** | 收編 4 個一級標註；與 haARM `resource.id` ↔ table 對齊 |

> **維護規則**：跨 DSL 版本升級時先寫入本 §0.1，再到各 *doc.md sync；不在各檔自行加非同步版本。Freeze 視窗起於 **2026-05-19**（凍結 EBNF/JSON Schema/欄位語意；文字、範例、速查卡不受限）。詳見 `ccwLog/0513-specsAlign_plan.md` §0 與 `ccwLog/0513-PQ_discuss.md` Q12。

### 0.3 章節骨架對照表（v3.3 統一 12 章）

> 本檔現行章節以「現狀」呈現，M1/M2/M3 將分批搬入下列 v3.3 標準位置。對照表會在 freeze 視窗結束後（>2026-05-26）正式完成重排。

| v3.3 標準章 | 標題 | 本檔現行位置 | 完工里程碑 |
|:----------:|------|------------|:---------:|
| 0 | 版本沿革 | §0（本章，已就位） | ✅ M0.4 |
| 1 | 設計理念與定位 | §1（§1.6 SSoT 宣告已加；§1.5 五大組成區塊會併入 §5） | ✅ M0.4 |
| 2 | 適用情境 | 散見於 §1 | ⏳ M0.3 後續 polish |
| 3 | EBNF 文法定義 | §2 + §3 BNF | M0.3 重排（M1 新增 `starts_with`/`ends_with`） |
| 4 | JSON Schema 定義 | §4 | M0.3 重排（M1 擴 enum + 一級欄位） |
| 5 | 語義規則表 | §5 + §6 + 現 §1.5「五大組成區塊」 | M0.3 重排 |
| 6 | Convention over Configuration | （新增章；M2 寫入 profile / auto_infer / `.haarm.config.yaml`） | ⏳ M2 |
| 7 | 跨規格整合 | §10 跨規格映射（補 hycms-ht002 範例） | ⏳ M3 |
| 8 | 完整範例 | §8 | M0.3 重排 |
| 9 | 驗證規則（含 §9.5 Anti-Pattern） | §9 + 新 §9.5（AP-01～AP-05） | ⏳ M1（§9.5）+ M0.3 重排 |
| 10 | 工具支援與 Lint | §11 + §7 Z3 驗證（併入） | M0.3 重排 |
| 11 | 遷移指引 | §12（含新加 v2→v3.3 遷移表） | M0.3 重排（M1 補表） |

---

## 1. 設計理念與定位

### 1.1 核心理念

haARM 是一套**宣告式**的 Actor-Role 建模語言，專注於描述「誰可以做什麼」的業務授權模型。在 WA-RAPTor 八規格檔案體系中，haARM 位於**治理層**第 8 號規格，作為角色基礎存取控制（RBAC）的中樞規格。

```
業務需求 → haARM（Who + What） → RBAC Engine / Gherkin BDD Tests
```

### 1.2 與現有工具的關係

| 工具 | 層級 | 關注點 | 產出物 |
|------|------|--------|--------|
| **haARM** | 治理層 | 角色、權限、約束 | RBAC 授權模型 |
| **haAPI** | 意圖層 | 業務能力、API 操作 | API 意圖規格 |
| **HaPDL** | 描述層 | 頁面結構、互動行為 | 頁面描述規格 |
| **DBML** | 模型層 | 領域實體、資料關係 | 資料庫 Schema |
| **Gherkin** | 驗證層 | 行為驗證、場景測試 | BDD 測試案例 |

### 1.3 設計原則

| # | 原則 | 說明 |
|---|------|------|
| 1 | **領域驅動** | 基於業務角色與資源的領域模型 |
| 2 | **宣告式** | 聲明權限而非編寫授權代碼 |
| 3 | **層級繼承** | 支援角色繼承與權限級聯 |
| 4 | **約束可驗證** | 所有治理約束可透過 Z3 SMT 求解器形式化驗證 |
| 5 | **漸進式宣告** | 五大區塊皆為 optional，可隨需求演進逐步補充 |
| 6 | **交叉引用一致** | 所有 `ref` 欄位遵循統一的命名空間引用語法 |
| 7 | **跨規格對齊** | 與 haPDL、haAPI、DBML、Gherkin 建立明確引用鏈路 |

### 1.4 在 WA-RAPTor 體系中的定位

```
┌─────────────────────────────────────────────────────────────┐
│                    WA-RAPTor DSL 生態系                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  haPDL ──── Feature/Story 定義 ──────┐                      │
│    │         (US-101, US-201...)      │                      │
│    │                                  ▼                      │
│    │              ┌──────────────────────────┐               │
│    └─── ref ────▶ │        haARM             │               │
│                   │  Actor-Role Modeling     │               │
│    ┌─── ref ────▶ │  (角色權限中樞)          │               │
│    │              └──┬────────┬────────┬─────┘               │
│    │                 │        │        │                      │
│  haAPI ◀── endpoint-ref      │     constraint                │
│    │    (GET /users...)       │     transform                │
│    │                         │        │                      │
│    │                    ap-mapping     │                      │
│    │                         │        │                      │
│    ▼                         ▼        ▼                      │
│  TypeSpec               DBML      Gherkin ──▶ BDD Tests     │
│    │                  (RBAC       (權限驗證                   │
│    ▼                   Tables)     Scenarios)                │
│  OpenAPI                  │                                  │
│                           ▼                                  │
│                    Database Schema                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.5 haARM 五大組成區塊

| 區塊 | 英文名稱 | 功能 | 必需 |
|------|----------|------|:----:|
| 元資料 | Metadata | 文檔標識、版本、命名空間 | ✓ |
| 演員定義 | Actors | 定義系統中的參與者（人、系統、服務） | ✗ |
| 權限詞彙表 | Permissions | 定義可執行的操作動作與範圍 | ✗ |
| 參與矩陣 | Participation-Matrix | 角色與 UserStory 的權限映射 | ✗ |
| 功能對應 | AP-Mapping | UserStory 到 API 端點與資料表的對應 | ✗ |
| 治理約束 | Constraints | SoD、互斥、強制指派、基數、時間等約束規則 | ✗ |

### 1.6 SSoT 主手冊宣告

**本文件為 haARM 的 SSoT 主手冊**，PM/SA 與下游 codegen 對 haARM 語法的單一可信來源。

- 技術參考：`haARM-Specification_v3.3.md`（EBNF 與 JSON Schema 完整版）、`haARM-BNF-Grammar.md`（BNF 完整文法）
- 驗證實作：`haARM-Z3-Constraint-Validation.md`（Z3 表達式與證明）
- 跨 DSL 整合：`CROSS-DSL-GUIDE.md`（v3.3 待建，詳見 M3）

三者描述衝突時**以本檔為準**；補充檔需於下次版本同步至本檔對應章節。

> M0.3 重排時會把現行 §1.5「haARM 五大組成區塊」併入 §5 語義規則表，§1.6 改回 §1.5。

---

## 2. EBNF 文法定義（簡化版）

以下為 haARM 的簡化 EBNF 文法，涵蓋 6 個主要區段。此版本適用於快速理解整體語法結構。

```ebnf
(* ============================================================ *)
(* haARM 文法定義 — v3.2 簡化版                                    *)
(* ============================================================ *)

HaARMDocument ::= MetadataSection
                  ActorsSection
                  RolesSection
                  PermissionsSection
                  AccessControlSection
                  (ConstraintsSection)?

(* ===== 元資料區段 ===== *)
MetadataSection ::= 'metadata' ':' NEWLINE
                    INDENT MetadataFields DEDENT

MetadataFields ::= MetadataField
                 | MetadataField MetadataFields

MetadataField ::= 'title' ':' String NEWLINE
                | 'version' ':' Version NEWLINE
                | 'description' ':' String NEWLINE
                | 'namespace' ':' NamespaceId NEWLINE

Version ::= DigitSequence '.' DigitSequence ('.' DigitSequence)?

NamespaceId ::= Identifier ('.' Identifier)*

(* ===== 演員區段 ===== *)
ActorsSection ::= 'actors' ':' NEWLINE
                  (INDENT ActorDefinition+ DEDENT)?

ActorDefinition ::= '- id' ':' ActorId NEWLINE
                    INDENT ActorFields DEDENT

ActorFields ::= ActorField
              | ActorField ActorFields

ActorField ::= 'name' ':' String NEWLINE
             | 'type' ':' ActorType NEWLINE
             | 'description' ':' String NEWLINE
             | 'properties' ':' NEWLINE INDENT PropertyMap DEDENT

ActorType ::= 'user' | 'system' | 'service' | 'external'

PropertyMap ::= Property
              | Property PropertyMap

Property ::= Identifier ':' (String | Number | Boolean) NEWLINE

(* ===== 角色區段 ===== *)
RolesSection ::= 'roles' ':' NEWLINE
                 (INDENT RoleDefinition+ DEDENT)?

RoleDefinition ::= '- id' ':' RoleId NEWLINE
                   INDENT RoleFields DEDENT

RoleFields ::= RoleField
             | RoleField RoleFields

RoleField ::= 'name' ':' String NEWLINE
            | 'description' ':' String NEWLINE
            | 'parent_roles' ':' RoleRefList NEWLINE
            | 'permissions' ':' PermissionRefList NEWLINE

RoleRefList ::= '[' RoleRef (',' RoleRef)* ']'

RoleRef ::= '@' RoleId | RoleId

(* ===== 權限區段 ===== *)
PermissionsSection ::= 'permissions' ':' NEWLINE
                       (INDENT PermissionDefinition+ DEDENT)?

PermissionDefinition ::= '- id' ':' PermissionId NEWLINE
                         INDENT PermissionFields DEDENT

PermissionFields ::= PermissionField
                   | PermissionField PermissionFields

PermissionField ::= 'resource' ':' ResourceRef NEWLINE
                  | 'action' ':' ActionType NEWLINE
                  | 'conditions' ':' ConditionList NEWLINE
                  | 'description' ':' String NEWLINE

ResourceRef ::= Identifier ('.' Identifier)* | '*'

ActionType ::= 'read' | 'write' | 'create' | 'update' | 'delete'
             | 'execute' | 'admin' | CustomAction

CustomAction ::= Identifier

ConditionList ::= '[' Condition (',' Condition)* ']'
                | Condition

Condition ::= FieldName Operator FieldValue

FieldName ::= Identifier ('.' Identifier)*

Operator ::= '==' | '!=' | '<' | '>' | '<=' | '>=' | 'in' | 'contains'

FieldValue ::= String | Number | Boolean | Array

Array ::= '[' Value (',' Value)* ']'

(* ===== 存取控制區段 ===== *)
AccessControlSection ::= 'access_control' ':' NEWLINE
                         (INDENT AccessRule+ DEDENT)?

AccessRule ::= '- id' ':' RuleId NEWLINE
               INDENT RuleFields DEDENT

RuleFields ::= RuleField
             | RuleField RuleFields

RuleField ::= 'actor' ':' ActorRef NEWLINE
            | 'roles' ':' RoleRefList NEWLINE
            | 'permissions' ':' PermissionRefList NEWLINE
            | 'effect' ':' Effect NEWLINE
            | 'conditions' ':' ConditionList NEWLINE
            | 'priority' ':' Integer NEWLINE

ActorRef ::= '@' ActorId | ActorId

Effect ::= 'allow' | 'deny'

PermissionRefList ::= '[' PermissionRef (',' PermissionRef)* ']'

PermissionRef ::= '@' PermissionId | PermissionId

(* ===== 約束條件區段 ===== *)
ConstraintsSection ::= 'constraints' ':' NEWLINE
                       (INDENT Constraint+ DEDENT)?

Constraint ::= '- id' ':' ConstraintId NEWLINE
               INDENT ConstraintFields DEDENT

ConstraintFields ::= ConstraintField
                   | ConstraintField ConstraintFields

ConstraintField ::= 'type' ':' ConstraintType NEWLINE
                  | 'expression' ':' Expression NEWLINE
                  | 'severity' ':' Severity NEWLINE

ConstraintType ::= 'mutual_exclusion' | 'dependency' | 'cardinality' | 'custom'

Expression ::= String (* Z3 或邏輯表達式 *)

Severity ::= 'error' | 'warning'

(* ===== 基本符號 ===== *)
Identifier     ::= Letter (Letter | Digit | '_')*
ActorId        ::= Identifier
RoleId         ::= Identifier
PermissionId   ::= Identifier
ResourceId     ::= Identifier
RuleId         ::= Identifier
ConstraintId   ::= Identifier
String         ::= '"' StringContent '"'
StringContent  ::= (Character - '"')*
Character      ::= ? 任何字符 ?
Number         ::= DigitSequence ('.' DigitSequence)?
Integer        ::= DigitSequence
Boolean        ::= 'true' | 'false'
DigitSequence  ::= Digit+
Digit          ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
Letter         ::= 'a' | 'b' | ... | 'z' | 'A' | 'B' | ... | 'Z'
NEWLINE        ::= ? 換行符號 ?
INDENT         ::= ? 增加縮排 ?
DEDENT         ::= ? 減少縮排 ?
```

---

## 3. BNF 正式文法規格（完整版）

以下為 haARM 的完整正式 BNF 文法，包含五大區塊（Actors、Permissions、Participation-Matrix、AP-Mapping、Constraints）的完整語法，以及交叉引用語法和擴展點定義。

### 3.1 頂層結構

```bnf
<haarm-spec>        ::= <metadata>
                        <actors-section>?
                        <permissions-section>?
                        <participation-section>?
                        <ap-mapping-section>?
                        <constraints-section>?

<metadata>          ::= "haarm:" NEWLINE
                        INDENT "version:" <semver> NEWLINE
                        INDENT "spec-id:" <identifier> NEWLINE
                        INDENT "title:" <quoted-string> NEWLINE
                        INDENT "description:" <quoted-string>? NEWLINE
                        INDENT "domain:" <identifier> NEWLINE
                        INDENT "refs:" <external-refs>? NEWLINE
                        INDENT "last-updated:" <iso-date> NEWLINE

<semver>            ::= DIGIT+ "." DIGIT+ "." DIGIT+

<external-refs>     ::= NEWLINE (INDENT INDENT "- " <namespace-ref>)+

<namespace-ref>     ::= <namespace> "::" <identifier>

<namespace>         ::= "haPDL" | "haAPI" | "DBML" | "Gherkin" | "haARM"
```

### 3.2 Actors 區塊

```bnf
<actors-section>    ::= "actors:" NEWLINE
                        (INDENT <actor-def>)+

<actor-def>         ::= "- id:" <actor-id> NEWLINE
                        INDENT "name:" <quoted-string> NEWLINE
                        INDENT "alias:" <identifier>? NEWLINE
                        INDENT "description:" <quoted-string>? NEWLINE
                        INDENT "type:" <actor-type>? NEWLINE
                        INDENT "inherits:" <actor-id-or-list>? NEWLINE
                        INDENT "group:" <group-id-or-list>? NEWLINE
                        INDENT "tags:" <tag-list>? NEWLINE

<actor-id>          ::= "A" DIGIT DIGIT (DIGIT)*
                      | <identifier>

<actor-type>        ::= "human" | "system" | "external" | "composite"

<actor-id-or-list>  ::= <actor-id>
                      | "[" <actor-id> ("," <actor-id>)* "]"

<group-id-or-list>  ::= <group-id>
                      | "[" <group-id> ("," <group-id>)* "]"

<group-id>          ::= <identifier>

<tag-list>          ::= "[" <identifier> ("," <identifier>)* "]"
```

#### 3.2.1 Actor 繼承語意規則

```
RULE inherit-permissions:
  IF actor A inherits actor B
  THEN A.effective_permissions ⊇ B.effective_permissions
  
RULE inherit-transitivity:
  IF A inherits B AND B inherits C
  THEN A.effective_permissions ⊇ C.effective_permissions

RULE no-circular-inheritance:
  FOR ALL actor chains: A₁ inherits A₂ inherits ... Aₙ
  REQUIRE A₁ ≠ Aₙ
```

### 3.3 Permissions 區塊

```bnf
<permissions-section>  ::= "permissions:" NEWLINE
                           INDENT "vocabulary:" NEWLINE
                           (INDENT INDENT "- " <permission-action>)+ NEWLINE
                           INDENT "aliases:" NEWLINE
                           (INDENT INDENT <alias-def>)*
                           INDENT "scopes:" NEWLINE
                           (INDENT INDENT <scope-def>)*

<permission-action>    ::= <upper-camel-identifier>

<alias-def>            ::= <identifier> ":" 
                           "[" <permission-action> ("," <permission-action>)* "]"

<scope-def>            ::= "- name:" <identifier> NEWLINE
                           INDENT "description:" <quoted-string>? NEWLINE
                           INDENT "applies-to:" <scope-target>

<scope-target>         ::= "all" | "own" | "group" | "department" | <identifier>
```

#### 3.3.1 內建權限動作（Built-in Actions）

以下權限動作為 haARM 內建，無需在 vocabulary 中重複宣告：

| Action | 語意 |
|--------|------|
| Create | 建立新資源 |
| Read | 查詢/檢視資源 |
| Update | 修改既有資源 |
| Delete | 刪除資源 |
| Execute | 執行操作/流程 |
| Approve | 審核/核准 |
| Export | 匯出資料 |
| Import | 匯入資料 |
| Configure | 系統設定 |
| Delegate | 委派權限予其他角色 |

#### 3.3.2 內建別名（Built-in Aliases）

| Alias | 展開 |
|-------|------|
| CRUD | [Create, Read, Update, Delete] |
| ReadOnly | [Read] |
| ReadWrite | [Read, Create, Update] |
| FullAccess | [Create, Read, Update, Delete, Approve, Export, Configure] |

### 3.4 Participation-Matrix 區塊

```bnf
<participation-section>  ::= "participation-matrix:" NEWLINE
                             (INDENT <participation-entry>)+

<participation-entry>    ::= "- actor:" <actor-id> NEWLINE
                             INDENT "stories:" NEWLINE
                             (INDENT INDENT <story-participation>)+

<story-participation>    ::= "- ref:" <story-ref> NEWLINE
                             INDENT "permissions:" <permission-list> NEWLINE
                             INDENT "scope:" <scope-target>? NEWLINE
                             INDENT "context:" <quoted-string>? NEWLINE
                             INDENT "conditions:" <condition-list>? NEWLINE
                             INDENT "effective-from:" <iso-date>? NEWLINE
                             INDENT "effective-until:" <iso-date>? NEWLINE

<story-ref>              ::= "US-" DIGIT DIGIT DIGIT (DIGIT)*
                           | <namespace-ref>

<permission-list>        ::= "[" <permission-ref> ("," <permission-ref>)* "]"

<permission-ref>         ::= <permission-action> | <identifier>  
                             /* identifier 可引用 alias */

<condition-list>         ::= NEWLINE (INDENT "- " <condition-expr>)+

<condition-expr>         ::= "when:" <quoted-string>
                           | "unless:" <quoted-string>
                           | "requires-approval-from:" <actor-id>
                           | "time-window:" <time-range>

<time-range>             ::= <time> "-" <time>
                           | "business-hours"
                           | "always"
```

#### 3.4.1 權限解析優先序

```
RULE permission-resolution:
  1. 明確宣告的 permissions (highest priority)
  2. 繼承自 parent actor 的 permissions
  3. 來自 group 的 permissions
  4. 遇衝突時：deny > allow (安全優先)
  
RULE scope-narrowing:
  IF child declares scope = "own"
  AND parent declares scope = "all"
  THEN effective scope = "own"  /* 子角色不能擴大範圍 */
```

### 3.5 AP-Mapping 區塊

```bnf
<ap-mapping-section>   ::= "ap-mapping:" NEWLINE
                           (INDENT <story-ap-entry>)+

<story-ap-entry>       ::= "- story:" <story-ref> NEWLINE
                           INDENT "apcat:" <apcat-id> NEWLINE
                           INDENT "entities:" NEWLINE
                           (INDENT INDENT <ap-entity>)+

<ap-entity>            ::= "- id:" <ap-id> NEWLINE
                           INDENT "name:" <quoted-string> NEWLINE
                           INDENT "endpoint-ref:" <endpoint-ref>? NEWLINE
                           INDENT "dbml-ref:" <dbml-ref>? NEWLINE
                           INDENT "required-permissions:" <permission-list>? NEWLINE

<apcat-id>             ::= <upper-camel-identifier>

<ap-id>                ::= "AP-" DIGIT DIGIT DIGIT (DIGIT)*

<endpoint-ref>         ::= "haAPI::" <http-method> " " <url-path>

<http-method>          ::= "GET" | "POST" | "PUT" | "PATCH" | "DELETE"

<url-path>             ::= "/" <path-segment> ("/" <path-segment>)*

<path-segment>         ::= <identifier>
                         | "{" <identifier> "}"    /* path parameter */

<dbml-ref>             ::= "DBML::" <identifier> ("." <identifier>)?
```

#### 3.5.1 AP-Entity 與 Permission 一致性規則

```
RULE ap-permission-consistency:
  FOR ALL ap-entity E in story S:
    E.required-permissions ⊆ 
      UNION { P.permissions | P ∈ participation-matrix WHERE P.ref = S }

RULE ap-endpoint-coverage:
  FOR ALL ap-entity E with endpoint-ref:
    EXISTS haAPI endpoint matching E.endpoint-ref
```

### 3.6 Constraints 區塊

```bnf
<constraints-section>     ::= "constraints:" NEWLINE
                              (INDENT <constraint-category>)+

<constraint-category>     ::= <sod-constraints>
                            | <mutex-constraints>
                            | <mandatory-constraints>
                            | <cardinality-constraints>
                            | <temporal-constraints>
                            | <custom-constraints>

(* --- Separation of Duty --- *)
<sod-constraints>         ::= "separation-of-duty:" NEWLINE
                              (INDENT <sod-rule>)+

<sod-rule>                ::= "- name:" <quoted-string> NEWLINE
                              INDENT "actors:" <actor-id-pair> NEWLINE
                              INDENT "conflicting-permissions:" 
                                     <permission-pair> NEWLINE
                              INDENT "on-stories:" <story-ref-list> NEWLINE
                              INDENT "rationale:" <quoted-string> NEWLINE
                              INDENT "severity:" <severity-level>? NEWLINE

<actor-id-pair>           ::= "[" <actor-id> "," <actor-id> "]"
                            | "SAME-ACTOR"

<permission-pair>         ::= "[" <permission-ref> "," <permission-ref> "]"

<story-ref-list>          ::= "[" <story-ref> ("," <story-ref>)* "]"
                            | "ANY"

<severity-level>          ::= "error" | "warning" | "info"

(* --- Mutual Exclusion --- *)
<mutex-constraints>       ::= "mutual-exclusion:" NEWLINE
                              (INDENT <mutex-rule>)+

<mutex-rule>              ::= "- name:" <quoted-string> NEWLINE
                              INDENT "exclusive-actors:" 
                                     <actor-id-list> NEWLINE
                              INDENT "rationale:" <quoted-string> NEWLINE
                              INDENT "severity:" <severity-level>? NEWLINE

<actor-id-list>           ::= "[" <actor-id> ("," <actor-id>)+ "]"

(* --- Mandatory Assignment --- *)
<mandatory-constraints>   ::= "mandatory-assignment:" NEWLINE
                              (INDENT <mandatory-rule>)+

<mandatory-rule>          ::= "- name:" <quoted-string> NEWLINE
                              INDENT "target:" <mandatory-target> NEWLINE
                              INDENT "rule:" <quoted-string> NEWLINE
                              INDENT "rationale:" <quoted-string> NEWLINE

<mandatory-target>        ::= "story" | "actor" | "apcat" | "ap-entity"

(* --- Cardinality --- *)
<cardinality-constraints> ::= "cardinality:" NEWLINE
                              (INDENT <cardinality-rule>)+

<cardinality-rule>        ::= "- name:" <quoted-string> NEWLINE
                              INDENT "subject:" <cardinality-subject> NEWLINE
                              INDENT "min:" DIGIT+? NEWLINE
                              INDENT "max:" (DIGIT+ | "unbounded")? NEWLINE
                              INDENT "rationale:" <quoted-string> NEWLINE

<cardinality-subject>     ::= "actors-per-story"
                            | "stories-per-actor"
                            | "permissions-per-actor"
                            | "groups-per-actor"

(* --- Temporal --- *)
<temporal-constraints>    ::= "temporal:" NEWLINE
                              (INDENT <temporal-rule>)+

<temporal-rule>           ::= "- name:" <quoted-string> NEWLINE
                              INDENT "type:" <temporal-type> NEWLINE
                              INDENT "actors:" <actor-id-list> NEWLINE
                              INDENT "time-window:" <time-range> NEWLINE
                              INDENT "rationale:" <quoted-string> NEWLINE

<temporal-type>           ::= "restricted-hours" | "temporary-elevation"
                            | "scheduled-rotation"

(* --- Custom (Z3-compatible) --- *)
<custom-constraints>      ::= "custom:" NEWLINE
                              (INDENT <custom-rule>)+

<custom-rule>             ::= "- name:" <quoted-string> NEWLINE
                              INDENT "z3-expr:" <z3-expression> NEWLINE
                              INDENT "rationale:" <quoted-string> NEWLINE
                              INDENT "severity:" <severity-level>? NEWLINE

<z3-expression>           ::= <quoted-string>
                              /* Z3 SMT-LIB compatible expression */
```

#### 3.6.1 約束語義型別摘要

| 約束類型 | 用途 | Z3 對應 |
|----------|------|---------|
| separation-of-duty | 同一人不可同時持有衝突權限 | `Not(And(...))` |
| mutual-exclusion | 兩角色不可由同一人擔任 | `Distinct(...)` |
| mandatory-assignment | 確保關鍵資源有人負責 | `AtLeast(...,1)` |
| cardinality | 數量上下界約束 | `And(>=min, <=max)` |
| temporal | 時間窗口限制 | `Implies(time_in_window, ...)` |
| custom | 任意 Z3 SMT 公式 | 直接嵌入 |

### 3.7 共用終端符號

```bnf
<identifier>             ::= LETTER (LETTER | DIGIT | "_" | "-")*

<upper-camel-identifier> ::= UPPER_LETTER (LETTER | DIGIT)*

<quoted-string>          ::= '"' (CHAR - '"')* '"'
                           | "'" (CHAR - "'")* "'"
                           | (CHAR - NEWLINE)+    /* YAML unquoted */

<iso-date>               ::= DIGIT{4} "-" DIGIT{2} "-" DIGIT{2}

<time>                   ::= DIGIT{2} ":" DIGIT{2}

LETTER                   ::= [a-zA-Z] | CJK_CHAR
UPPER_LETTER             ::= [A-Z]
DIGIT                    ::= [0-9]
CHAR                     ::= /* any Unicode character */
CJK_CHAR                 ::= /* CJK Unified Ideographs range */
NEWLINE                  ::= "\n" | "\r\n"
INDENT                   ::= "  "    /* 2 spaces per level */
```

### 3.8 交叉引用語法

haARM 使用統一的命名空間引用語法與其他 WA-RAPTor DSL 互參：

```bnf
<cross-ref>     ::= <namespace> "::" <ref-path>

<ref-path>      ::= <identifier> ("." <identifier>)*
                  | <http-method> " " <url-path>   /* haAPI 專用 */
                  | <identifier> "." <identifier>   /* DBML 專用 */
```

#### 引用範例

| 引用語法 | 語意 |
|----------|------|
| `haPDL::US-101` | 引用 haPDL 中的 UserStory US-101 |
| `haAPI::GET /users` | 引用 haAPI 中的端點 |
| `haAPI::POST /users/{id}/approve` | 引用含路徑參數的端點 |
| `DBML::users.role_id` | 引用 DBML 中的資料表欄位 |
| `Gherkin::permission-check` | 引用 Gherkin 中的場景標籤 |
| `haARM::A01` | 自引用其他角色（用於約束定義） |

### 3.9 文法擴展點

haARM 文法預留以下擴展機制，供未來版本使用：

```bnf
<extension-block>  ::= "x-" <identifier> ":" NEWLINE
                       (INDENT <any-yaml-content>)+
```

預期的擴展方向包括：

- `x-audit-trail`: 角色變更稽核軌跡
- `x-delegation-chain`: 權限委派鏈
- `x-data-classification`: 資料分級與角色存取等級對應
- `x-multi-tenancy`: 多租戶隔離角色模型

---

## 4. JSON Schema 定義

以下為 haARM v3.2 的完整 JSON Schema，包含 6 個核心定義。

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://wa-raptor.example.com/haarm/schema.json",
  "title": "haARM Schema",
  "description": "Schema for ha Actor-Role Modeling Language v3.2",
  "type": "object",
  "required": ["metadata", "actors", "roles", "permissions", "access_control"],
  "additionalProperties": false,
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["title", "version"],
      "additionalProperties": false,
      "properties": {
        "title": {
          "type": "string",
          "minLength": 1,
          "description": "haARM 文檔標題"
        },
        "version": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+(\\.\\d+)?$",
          "description": "版本號 (e.g., 1.0.0)"
        },
        "description": {
          "type": "string",
          "description": "文檔描述"
        },
        "namespace": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*(\\.[a-zA-Z_][a-zA-Z0-9_]*)*$",
          "description": "命名空間 (e.g., com.example.auth)"
        }
      }
    },
    "actors": {
      "type": "array",
      "items": { "$ref": "#/definitions/Actor" },
      "description": "演員定義清單"
    },
    "roles": {
      "type": "array",
      "items": { "$ref": "#/definitions/Role" },
      "description": "角色定義清單"
    },
    "permissions": {
      "type": "array",
      "items": { "$ref": "#/definitions/Permission" },
      "description": "權限定義清單"
    },
    "access_control": {
      "type": "array",
      "items": { "$ref": "#/definitions/AccessRule" },
      "description": "存取控制規則清單"
    },
    "constraints": {
      "type": "array",
      "items": { "$ref": "#/definitions/Constraint" },
      "description": "治理約束條件"
    }
  },
  "definitions": {
    "Actor": {
      "type": "object",
      "required": ["id", "name", "type"],
      "additionalProperties": false,
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
          "description": "演員唯一識別碼"
        },
        "name": {
          "type": "string",
          "minLength": 1,
          "description": "演員名稱"
        },
        "type": {
          "type": "string",
          "enum": ["user", "system", "service", "external"],
          "description": "演員類型"
        },
        "description": {
          "type": "string",
          "description": "演員描述"
        },
        "properties": {
          "type": "object",
          "additionalProperties": {
            "oneOf": [
              { "type": "string" },
              { "type": "number" },
              { "type": "boolean" }
            ]
          },
          "description": "自訂屬性鍵值對"
        }
      }
    },
    "Role": {
      "type": "object",
      "required": ["id", "name"],
      "additionalProperties": false,
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
          "description": "角色唯一識別碼"
        },
        "name": {
          "type": "string",
          "minLength": 1,
          "description": "角色名稱"
        },
        "description": {
          "type": "string",
          "description": "角色描述"
        },
        "parent_roles": {
          "type": "array",
          "items": { "type": "string" },
          "description": "父角色 ID 清單（支持層級繼承）"
        },
        "permissions": {
          "type": "array",
          "items": { "type": "string" },
          "description": "權限 ID 清單"
        }
      }
    },
    "Permission": {
      "type": "object",
      "required": ["id", "resource", "action"],
      "additionalProperties": false,
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
          "description": "權限唯一識別碼"
        },
        "resource": {
          "type": "string",
          "description": "資源識別碼 (e.g., users.profile, orders.*, admin.*)"
        },
        "action": {
          "type": "string",
          "enum": ["read", "write", "create", "update", "delete", "execute", "admin"],
          "description": "操作類型"
        },
        "conditions": {
          "type": "array",
          "items": { "$ref": "#/definitions/Condition" },
          "description": "條件約束"
        },
        "description": {
          "type": "string",
          "description": "權限描述"
        }
      }
    },
    "Condition": {
      "type": "object",
      "required": ["field", "operator", "value"],
      "additionalProperties": false,
      "properties": {
        "field": {
          "type": "string",
          "description": "欄位名稱 (e.g., user.department, request.time)"
        },
        "operator": {
          "type": "string",
          "enum": ["==", "!=", "<", ">", "<=", ">=", "in", "contains"],
          "description": "比較運算子"
        },
        "value": {
          "oneOf": [
            { "type": "string" },
            { "type": "number" },
            { "type": "boolean" },
            { 
              "type": "array",
              "items": {
                "oneOf": [
                  { "type": "string" },
                  { "type": "number" }
                ]
              }
            }
          ],
          "description": "比較值"
        }
      }
    },
    "AccessRule": {
      "type": "object",
      "required": ["id", "effect"],
      "additionalProperties": false,
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
          "description": "規則唯一識別碼"
        },
        "actor": {
          "type": "string",
          "description": "演員 ID"
        },
        "roles": {
          "type": "array",
          "items": { "type": "string" },
          "description": "角色 ID 清單"
        },
        "permissions": {
          "type": "array",
          "items": { "type": "string" },
          "description": "權限 ID 清單"
        },
        "effect": {
          "type": "string",
          "enum": ["allow", "deny"],
          "description": "規則效果"
        },
        "conditions": {
          "type": "array",
          "items": { "$ref": "#/definitions/Condition" },
          "description": "額外條件"
        },
        "priority": {
          "type": "integer",
          "minimum": 0,
          "description": "規則優先級（數字越小優先級越高）"
        }
      }
    },
    "Constraint": {
      "type": "object",
      "required": ["id", "type", "expression"],
      "additionalProperties": false,
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
          "description": "約束識別碼"
        },
        "type": {
          "type": "string",
          "enum": ["mutual_exclusion", "dependency", "cardinality", "custom"],
          "description": "約束類型"
        },
        "expression": {
          "type": "string",
          "description": "約束表達式（Z3 邏輯語法）"
        },
        "severity": {
          "type": "string",
          "enum": ["error", "warning"],
          "description": "違反約束的嚴重程度"
        }
      }
    }
  }
}
```

---

## 5. 語義規則表

### 5.1 文件結構層級

| 層級 | 元素 | 必需 | 類型 | 說明 |
|------|------|:----:|------|------|
| 0 | 根文檔 | ✓ | Object | haARM 根層級 |
| 1 | metadata | ✓ | Object | 文檔元資料 |
| 1 | actors | ✓ | Array | 演員清單 |
| 1 | roles | ✓ | Array | 角色清單 |
| 1 | permissions | ✓ | Array | 權限清單 |
| 1 | access_control | ✓ | Array | 存取規則清單 |
| 1 | constraints | ✗ | Array | 治理約束（可選） |

### 5.2 Metadata（元資料）欄位

| 欄位 | 類型 | 必需 | 格式 | 說明 |
|------|------|:----:|------|------|
| title | String | ✓ | - | 文檔標題，至少 1 個字符 |
| version | String | ✓ | `\d+\.\d+(\.\d+)?` | 版本號，符合 SemVer |
| description | String | ✗ | - | 文檔描述 |
| namespace | String | ✗ | `^[a-zA-Z_]...` | 命名空間，點號分隔 |

### 5.3 Actor（演員）欄位

| 欄位 | 類型 | 必需 | 有效值 | 說明 |
|------|------|:----:|--------|------|
| id | String | ✓ | `[a-zA-Z_][a-zA-Z0-9_]*` | 演員唯一識別碼 |
| name | String | ✓ | - | 演員可讀名稱 |
| type | String | ✓ | user, system, service, external | 演員類型 |
| description | String | ✗ | - | 演員描述 |
| properties | Object | ✗ | 鍵值對 | 自訂屬性（可選） |

**有效的 Actor Type：**

| Type | 說明 | 使用場景 |
|------|------|----------|
| `user` | 真實用戶 | 一般使用者、管理員 |
| `system` | 系統內部演員 | 排程器、背景服務 |
| `service` | 微服務或服務帳戶 | API Gateway、微服務 |
| `external` | 外部系統或第三方 | 第三方整合、合作夥伴 |

**完整 BNF 版本額外支援：**

| Type | 說明 | 使用場景 |
|------|------|----------|
| `human` | 同 `user`（完整版語法） | 一般人類使用者 |
| `composite` | 複合角色 | 由多個子角色組合而成 |

### 5.4 Role（角色）欄位

| 欄位 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| id | String | ✓ | 角色唯一識別碼 |
| name | String | ✓ | 角色可讀名稱 |
| description | String | ✗ | 角色描述 |
| parent_roles | Array | ✗ | 父角色 ID 清單（支持層級繼承） |
| permissions | Array | ✗ | 權限 ID 清單 |

**角色繼承規則：**
- 子角色繼承父角色的所有權限
- 支持多重繼承（多個 parent_roles）
- 循環繼承會被約束檢測拒絕
- 子角色的有效範圍（scope）不可超越父角色

### 5.5 Permission（權限）欄位

| 欄位 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| id | String | ✓ | 權限唯一識別碼 |
| resource | String | ✓ | 資源識別碼（支持萬用字符） |
| action | String | ✓ | 操作類型 |
| conditions | Array | ✗ | 條件約束清單 |
| description | String | ✗ | 權限描述 |

**有效的 Action 類型：**

| Action | 說明 | HTTP 對應 |
|--------|------|-----------|
| `read` | 讀取資源 | GET |
| `write` | 寫入資源 | POST/PUT |
| `create` | 建立新資源 | POST |
| `update` | 更新資源 | PUT/PATCH |
| `delete` | 刪除資源 | DELETE |
| `execute` | 執行操作/函數 | POST |
| `admin` | 管理資源 | 所有方法 |

**資源識別碼格式：**

| 格式 | 說明 | 範例 |
|------|------|------|
| `entity.field` | 具體資源 | `users.profile` |
| `entity.*` | 萬用符 | `orders.*`（orders 下所有子資源） |
| `*` | 所有資源 | 超級管理員使用 |

### 5.6 AccessControl（存取規則）欄位

| 欄位 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| id | String | ✓ | 規則唯一識別碼 |
| actor | String | ✗ | 演員 ID（二選一：actor 或 roles） |
| roles | Array | ✗ | 角色 ID 清單（二選一：actor 或 roles） |
| permissions | Array | ✗ | 權限 ID 清單 |
| effect | String | ✓ | allow 或 deny |
| conditions | Array | ✗ | 額外條件約束 |
| priority | Integer | ✗ | 優先級（0 最高，預設 100） |

**優先級規則：**
1. `deny` 規則預設優先於 `allow` 規則
2. 相同 effect 時，priority 數字越小優先級越高
3. 預設 priority 為 100

### 5.7 Condition（條件）欄位

| 欄位 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| field | String | ✓ | 欄位路徑（點號分隔） |
| operator | String | ✓ | 比較運算子 |
| value | Mixed | ✓ | 比較值 |

**有效的運算子與使用場景：**

| 運算子 | 語意 | value 類型 | 範例 |
|--------|------|-----------|------|
| `==` | 等於 | String, Number, Boolean | `value: "admin"` |
| `!=` | 不等於 | String, Number, Boolean | `value: "inactive"` |
| `<` | 小於 | Number | `value: 1000` |
| `>` | 大於 | Number | `value: 0` |
| `<=` | 小於等於 | Number | `value: 100` |
| `>=` | 大於等於 | Number | `value: 9` |
| `in` | 值在陣列中 | Array | `value: ["HR", "Sales"]` |
| `contains` | 字符串包含 | String | `value: "@example.com"` |

### 5.8 Constraint（約束）欄位

| 欄位 | 類型 | 必需 | 有效值 | 說明 |
|------|------|:----:|--------|------|
| id | String | ✓ | - | 約束唯一識別碼 |
| type | String | ✓ | mutual_exclusion, dependency, cardinality, custom | 約束類型 |
| expression | String | ✓ | Z3 邏輯表達式 | 約束表達式 |
| severity | String | ✗ | error, warning | 違反嚴重程度 |

**約束類型詳細說明：**

| 類型 | 說明 | 使用場景 | 違反後果 |
|------|------|----------|----------|
| mutual_exclusion | 互斥約束 | 兩個角色不能同時指派給同一演員 | 禁止角色指派 |
| dependency | 依賴約束 | 一個角色依賴另一個角色的存在 | 禁止單獨指派 |
| cardinality | 基數約束 | 限制角色或權限的數量上下界 | 禁止超出範圍 |
| custom | 自訂約束 | 使用 Z3 邏輯語法的自訂表達式 | 依 severity 決定 |

---

## 6. 語法與語義說明

### 6.1 演員（Actor）定義

演員是 haARM 中的基本實體，代表系統中可被授權的參與者。

**基本範例：**
```yaml
actors:
  - id: admin_user
    name: System Administrator
    type: user
    description: 系統管理員
    properties:
      department: IT
      email: admin@example.com

  - id: api_gateway
    name: API Gateway Service
    type: service
```

**完整 BNF 版範例（含繼承與群組）：**
```yaml
actors:
  - id: A00
    name: 基礎使用者
    alias: BaseUser
    description: "所有角色的根角色"
    type: human
    tags: [abstract, base]

  - id: A01
    name: 系統管理員
    alias: SysAdmin
    type: human
    inherits: A00
    group: AdminGroup
    tags: [privileged, admin]
```

### 6.2 角色（Role）定義與繼承

角色是權限的容器，支持層級繼承。

```yaml
roles:
  - id: admin
    name: Administrator
    description: 系統管理員，擁有最高權限
    permissions:
      - user_read
      - user_write
      - user_delete
  
  - id: order_manager
    name: Order Manager
    parent_roles: [admin]
    description: 訂單管理員，繼承管理員的權限
    permissions:
      - order_read
      - order_update
```

### 6.3 權限（Permission）定義

權限定義了「對什麼資源可以做什麼動作」的原子授權單元。

**基本權限：**
```yaml
permissions:
  - id: user_read
    resource: users.profile
    action: read
    description: 讀取用戶信息
```

**帶條件的權限：**
```yaml
permissions:
  - id: order_update_with_condition
    resource: orders.details
    action: update
    conditions:
      - field: user.department
        operator: "=="
        value: sales
      - field: order.status
        operator: in
        value: ["pending", "processing"]
    description: 銷售部門才能更新待處理訂單
```

### 6.4 存取控制規則（AccessControl）

存取規則將演員/角色與權限綁定，並指定效果（允許/拒絕）。

```yaml
access_control:
  - id: admin_all_access
    actor: admin_user
    permissions:
      - user_read
      - user_write
      - user_delete
    effect: allow
    priority: 10
  
  - id: sales_order_deny
    roles: [sales_associate]
    permissions:
      - order_delete
    effect: deny
    conditions:
      - field: order.amount
        operator: ">"
        value: 10000
    priority: 5
```

### 6.5 約束（Constraint）定義

約束定義了 RBAC 系統的治理規則，可透過 Z3 SMT 求解器進行形式化驗證。

**互斥約束：**
```yaml
constraints:
  - id: auditor_accountant_mutual_exclusion
    type: mutual_exclusion
    expression: "Not(hasRole(actor, 'auditor') And hasRole(actor, 'accountant'))"
    severity: error
```

**依賴約束：**
```yaml
  - id: manager_requirement
    type: dependency
    expression: "hasRole(actor, 'team_lead') Implies hasRole(actor, 'manager')"
    severity: error
```

**基數約束：**
```yaml
  - id: max_admin_count
    type: cardinality
    expression: "Cardinality({actor | hasRole(actor, 'admin')}) <= 5"
    severity: warning
```

### 6.6 權限詞彙表（Permissions Vocabulary）

完整 BNF 版本支援更豐富的權限定義：

```yaml
permissions:
  vocabulary:
    - Create
    - Read
    - Update
    - Delete
    - Submit
    - Approve
    - Reject
    - Publish
    - Unpublish
    - Archive
    - Export
    - Configure
    - AssignRole
    - ViewAuditLog

  aliases:
    CRUD: [Create, Read, Update, Delete]
    ReadOnly: [Read]
    ContentLifecycle: [Create, Read, Update, Submit]
    ReviewActions: [Read, Approve, Reject]
    PublishControl: [Publish, Unpublish, Archive]
    FullAccess: [Create, Read, Update, Delete, Approve, Export, Configure]

  scopes:
    - name: own
      description: "僅限自己建立的資源"
      applies-to: own
    - name: group
      description: "同群組成員建立的資源"
      applies-to: group
    - name: department
      description: "同部門的資源"
      applies-to: department
    - name: all
      description: "全系統資源"
      applies-to: all
```

### 6.7 參與矩陣（Participation-Matrix）

```yaml
participation-matrix:
  - actor: A01
    stories:
      - ref: US-101
        permissions: [CRUD, AssignRole]
        scope: all
        context: "管理所有使用者帳號"
      - ref: US-102
        permissions: [Configure]
        scope: all
        context: "設定系統參數"
        conditions:
          - unless: "目標為生產環境變更"

  - actor: A03
    stories:
      - ref: US-201
        permissions: [ContentLifecycle]
        scope: own
        context: "建立新文章、編修自己的草稿、提交審核"
      - ref: US-202
        permissions: [Read, Update]
        scope: group
        context: "協作編輯同組成員的草稿"
        conditions:
          - when: "目標文章狀態為 draft"
```

### 6.8 功能對應（AP-Mapping）

```yaml
ap-mapping:
  - story: US-101
    apcat: UserMgmt
    entities:
      - id: AP-001
        name: 使用者清單查詢
        endpoint-ref: haAPI::GET /users
        dbml-ref: DBML::users
        required-permissions: [Read]
      - id: AP-002
        name: 使用者帳號建立
        endpoint-ref: haAPI::POST /users
        dbml-ref: DBML::users
        required-permissions: [Create]
```

---

## 7. Z3 約束驗證

### 7.1 基本概念映射

| haARM 概念 | Z3 表示 | 說明 |
|-----------|--------|------|
| Actor | 集合元素 | 如 `actor_john` |
| Role | 邏輯謂詞 | 如 `hasRole(actor, role_id)` |
| Permission | 邏輯謂詞 | 如 `hasPermission(actor, perm_id)` |
| Condition | 一階邏輯 | 如 `user.dept == "HR"` |

### 7.2 約束類型與 Z3 表達式

#### 7.2.1 互斥約束 (Mutual Exclusion)

**haARM YAML：**
```yaml
constraints:
  - id: auditor_accountant_exclusion
    type: mutual_exclusion
    expression: "Not(hasRole(actor, 'auditor') And hasRole(actor, 'accountant'))"
    severity: error
```

**Z3 邏輯式：**
```python
# 對所有演員
ForAll([actor], 
  Not(And(hasRole(actor, auditor), 
          hasRole(actor, accountant)))
)
```

#### 7.2.2 依賴約束 (Dependency)

**haARM YAML：**
```yaml
constraints:
  - id: team_lead_requires_manager
    type: dependency
    expression: "ForAll([actor], Implies(hasRole(actor, 'team_lead'), hasRole(actor, 'manager')))"
    severity: error
```

**Z3 邏輯式：**
```python
ForAll([actor],
  Implies(hasRole(actor, team_lead),
          hasRole(actor, manager))
)
```

#### 7.2.3 基數約束 (Cardinality)

**haARM YAML：**
```yaml
constraints:
  - id: max_admins
    type: cardinality
    expression: "Cardinality({actor | hasRole(actor, 'admin')}) <= 5"
    severity: error
```

**Z3 邏輯式：**
```python
PK_Cardinality(
  [actor for actor in all_actors if hasRole(actor, admin)],
  le,  # 小於等於
  5
)
```

#### 7.2.4 自訂約束 (Custom)

**haARM YAML：**
```yaml
constraints:
  - id: complex_business_logic
    type: custom
    expression: |
      ForAll([actor],
        (hasRole(actor, 'finance') And actor.dept == 'accounting')
        Implies hasPermission(actor, 'financial_report_read')
      )
    severity: error
```

### 7.3 Python Z3 驗證器核心實現

#### 7.3.1 資料結構

```python
from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Union
from z3 import *

@dataclass
class Actor:
    id: str
    name: str
    type: str  # user, system, service, external
    properties: Dict[str, Union[str, int, bool]] = None

@dataclass
class Role:
    id: str
    name: str
    parent_roles: List[str] = None
    permissions: List[str] = None

@dataclass
class Permission:
    id: str
    resource: str
    action: str
    conditions: List['Condition'] = None

@dataclass
class Condition:
    field: str
    operator: str  # ==, !=, <, >, <=, >=, in, contains
    value: Union[str, int, bool, List]

@dataclass
class AccessRule:
    id: str
    actor: Optional[str] = None
    roles: Optional[List[str]] = None
    permissions: Optional[List[str]] = None
    effect: str = 'allow'
    conditions: Optional[List[Condition]] = None
    priority: int = 100

@dataclass
class Constraint:
    id: str
    type: str  # mutual_exclusion, dependency, cardinality, custom
    expression: str
    severity: str = 'error'

@dataclass
class HaARMDocument:
    title: str
    version: str
    namespace: str
    actors: Dict[str, Actor]
    roles: Dict[str, Role]
    permissions: Dict[str, Permission]
    access_control: List[AccessRule]
    constraints: List[Constraint]
```

#### 7.3.2 驗證器類別

```python
class HaARMZ3Validator:
    """haARM Z3 約束驗證器"""
    
    def __init__(self, document: HaARMDocument):
        self.doc = document
        self.z3_solver = Solver()
        self.role_predicates: Dict[str, FuncDeclRef] = {}
        self.permission_predicates: Dict[str, FuncDeclRef] = {}
        self.actor_symbols: Dict[str, ExprRef] = {}
        self.setup_z3_environment()
    
    def setup_z3_environment(self):
        """初始化 Z3 環境"""
        for actor_id in self.doc.actors.keys():
            self.actor_symbols[actor_id] = Const(
                f"actor_{actor_id}", DeclareSort("Actor")
            )
        
        for role_id in self.doc.roles.keys():
            self.role_predicates[role_id] = Function(
                f"hasRole_{role_id}", DeclareSort("Actor"), BoolSort()
            )
        
        for perm_id in self.doc.permissions.keys():
            self.permission_predicates[perm_id] = Function(
                f"hasPermission_{perm_id}", DeclareSort("Actor"), BoolSort()
            )
    
    def validate_all(self) -> Dict[str, bool]:
        """驗證所有約束"""
        results = {}
        for constraint in self.doc.constraints:
            if constraint.type == 'mutual_exclusion':
                results[constraint.id] = self.validate_mutual_exclusion(constraint)
            elif constraint.type == 'dependency':
                results[constraint.id] = self.validate_dependency(constraint)
            elif constraint.type == 'cardinality':
                results[constraint.id] = self.validate_cardinality(constraint)
            elif constraint.type == 'custom':
                results[constraint.id] = self._validate_custom(constraint)
        return results
    
    def check_reachability(self, actor_id: str, role_id: str) -> bool:
        """
        檢查可達性：某個演員是否能夠合法地擁有某個角色
        （考慮所有約束）
        """
        solver = Solver()
        solver.add(self.z3_solver.assertions())
        target = self.role_predicates[role_id](self.actor_symbols[actor_id])
        solver.add(target)
        return solver.check() == sat
    
    def find_conflicts(self) -> List[Dict]:
        """找出所有衝突的約束組合"""
        conflicts = []
        constraints = self.doc.constraints
        for i in range(len(constraints)):
            for j in range(i + 1, len(constraints)):
                c1, c2 = constraints[i], constraints[j]
                solver = Solver()
                expr1 = self._parse_constraint_expression(c1.expression)
                expr2 = self._parse_constraint_expression(c2.expression)
                solver.add(expr1)
                solver.add(expr2)
                if solver.check() == unsat:
                    conflicts.append({
                        'constraint1': c1.id,
                        'constraint2': c2.id,
                        'reason': 'Constraints are mutually exclusive'
                    })
        return conflicts
```

#### 7.3.3 使用範例

```python
# 載入 haARM 文檔
with open('ecommerce.haarm.yaml', 'r') as f:
    import yaml
    data = yaml.safe_load(f)

# 建立驗證器
validator = HaARMZ3Validator(doc)

# 驗證所有約束
results = validator.validate_all()
print("約束驗證結果：")
for constraint_id, is_valid in results.items():
    status = "✓ 通過" if is_valid else "✗ 失敗"
    print(f"  {constraint_id}: {status}")

# 可達性檢查
can_reach = validator.check_reachability('john', 'admin')
print(f"john 能否擁有 admin 角色？{can_reach}")

# 衝突偵測
conflicts = validator.find_conflicts()
if conflicts:
    print("發現約束衝突：")
    for conflict in conflicts:
        print(f"  {conflict['constraint1']} <-> {conflict['constraint2']}")
```

### 7.4 Z3 表達式語法參考

#### 邏輯運算子

```python
And(expr1, expr2, ...)      # 邏輯與
Or(expr1, expr2, ...)       # 邏輯或
Not(expr)                    # 邏輯非
Implies(expr1, expr2)        # 蘊含 (expr1 => expr2)
Iff(expr1, expr2)           # 雙向蘊含 (expr1 <=> expr2)
```

#### 量化

```python
ForAll([x, y], expr)        # ∀x,y. expr
Exists([x, y], expr)        # ∃x,y. expr
```

#### 比較

```python
Eq(expr1, expr2)            # ==
Ne(expr1, expr2)            # !=
expr1 < expr2               # <
expr1 > expr2               # >
expr1 <= expr2              # <=
expr1 >= expr2              # >=
```

#### 字符串

```python
Concat(str1, str2)          # 字符串連接
Contains(str1, str2)        # str1 包含 str2
Length(str)                  # 字符串長度
```

### 7.5 整合工作流

```
haARM YAML 文檔
    ↓
YAML 解析 → Python 物件
    ↓
JSON Schema 驗證 (語法層)
    ↓
HaARMZ3Validator 驗證 (語義層)
    ↓
Z3 求解器檢查 (邏輯層)
    ↓
產生驗證報告
```

---

## 8. 完整範例

### 8.1 基礎範例：E-Commerce RBAC

```yaml
metadata:
  title: E-Commerce Platform RBAC
  version: 1.0.0
  namespace: com.example.ecommerce.auth
  description: E-Commerce 平臺的角色存取控制模型

actors:
  - id: customer
    name: Customer User
    type: user
    description: 普通客戶
  
  - id: admin_user
    name: Administrator
    type: user
    description: 系統管理員
  
  - id: api_service
    name: Order Service
    type: service
    description: 訂單微服務

roles:
  - id: customer_role
    name: Customer
    permissions:
      - order_view_own
      - cart_manage
  
  - id: merchant
    name: Merchant
    parent_roles: [customer_role]
    permissions:
      - product_create
      - product_update
      - order_view_merchant
  
  - id: admin
    name: Administrator
    permissions:
      - user_read
      - user_write
      - user_delete
      - order_read
      - order_delete
      - audit_log_read

permissions:
  - id: order_view_own
    resource: orders.own
    action: read
    description: 客戶可查看自己的訂單
  
  - id: order_view_merchant
    resource: orders.merchant
    action: read
    conditions:
      - field: user.role
        operator: "=="
        value: merchant
    description: 商家可查看自己的訂單
  
  - id: product_create
    resource: products
    action: create
    description: 建立新產品
  
  - id: product_update
    resource: products
    action: update
    description: 更新產品
  
  - id: cart_manage
    resource: cart
    action: write
    description: 管理購物車
  
  - id: user_read
    resource: users
    action: read
    description: 讀取用戶信息
  
  - id: user_write
    resource: users
    action: write
    description: 寫入用戶信息
  
  - id: user_delete
    resource: users
    action: delete
    description: 刪除用戶
  
  - id: order_read
    resource: orders
    action: read
    description: 讀取訂單
  
  - id: order_delete
    resource: orders
    action: delete
    description: 刪除訂單
  
  - id: audit_log_read
    resource: audit_logs
    action: read
    description: 讀取稽核日誌

access_control:
  - id: customer_access
    roles: [customer_role]
    permissions:
      - order_view_own
      - cart_manage
    effect: allow
    priority: 100
  
  - id: merchant_access
    roles: [merchant]
    permissions:
      - product_create
      - product_update
      - order_view_merchant
    effect: allow
    priority: 50
  
  - id: admin_access
    roles: [admin]
    permissions:
      - user_read
      - user_write
      - user_delete
      - order_read
      - order_delete
    effect: allow
    priority: 10
  
  - id: deny_customer_delete
    roles: [customer_role]
    permissions:
      - user_delete
    effect: deny
    priority: 5

constraints:
  - id: merchant_admin_exclusion
    type: mutual_exclusion
    expression: "Not(hasRole(actor, 'merchant') And hasRole(actor, 'admin'))"
    severity: error
  
  - id: max_admin_count
    type: cardinality
    expression: "Cardinality({actor | hasRole(actor, 'admin')}) <= 3"
    severity: warning
```

### 8.2 進階範例：智慧內容管理平台（CMS）

以下為一個完整的 CMS 系統 haARM 規格，展示所有五個區塊的用法。

```yaml
haarm:
  version: 0.1.0
  spec-id: CMS-RBAC-2026
  title: "智慧內容管理平台 — 角色權限模型"
  description: "定義 CMS 平台中六個核心角色的權限分派、
                UserStory 參與關係與功能實體對應"
  domain: ContentManagement
  refs:
    - haPDL::CMS-FeatureModel-v2
    - haAPI::CMS-API-Spec-v1
    - DBML::CMS-Schema-v3
  last-updated: 2026-04-02

actors:
  - id: A00
    name: 基礎使用者
    alias: BaseUser
    description: "所有角色的根角色，提供最基本的系統存取能力"
    type: human
    tags: [abstract, base]

  - id: A01
    name: 系統管理員
    alias: SysAdmin
    type: human
    inherits: A00
    group: AdminGroup
    tags: [privileged, admin]

  - id: A02
    name: 使用者管理員
    alias: UserAdmin
    type: human
    inherits: A00
    group: AdminGroup
    tags: [admin]

  - id: A03
    name: 內容編輯者
    alias: ContentEditor
    type: human
    inherits: A00
    group: EditorialGroup
    tags: [content, editorial]

  - id: A04
    name: 內容審核者
    alias: ContentReviewer
    type: human
    inherits: A00
    group: EditorialGroup
    tags: [content, review]

  - id: A05
    name: 稽核員
    alias: Auditor
    type: human
    inherits: A00
    group: ComplianceGroup
    tags: [compliance, readonly]

  - id: A90
    name: 自動發布排程器
    alias: AutoPublisher
    type: system
    inherits: A00
    tags: [system, automated]

permissions:
  vocabulary:
    - Create
    - Read
    - Update
    - Delete
    - Submit
    - Approve
    - Reject
    - Publish
    - Unpublish
    - Archive
    - Export
    - Configure
    - AssignRole
    - ViewAuditLog

  aliases:
    CRUD: [Create, Read, Update, Delete]
    ReadOnly: [Read]
    ContentLifecycle: [Create, Read, Update, Submit]
    ReviewActions: [Read, Approve, Reject]
    PublishControl: [Publish, Unpublish, Archive]

  scopes:
    - name: own
      description: "僅限自己建立的資源"
      applies-to: own
    - name: group
      description: "同群組成員建立的資源"
      applies-to: group
    - name: all
      description: "全系統資源"
      applies-to: all

participation-matrix:
  - actor: A01
    stories:
      - ref: US-101
        permissions: [CRUD, AssignRole]
        scope: all
        context: "管理所有使用者帳號"
      - ref: US-102
        permissions: [Configure]
        scope: all
        context: "設定系統參數"

  - actor: A03
    stories:
      - ref: US-201
        permissions: [ContentLifecycle]
        scope: own
        context: "建立、編修與提交內容"
      - ref: US-202
        permissions: [Read, Update]
        scope: group
        context: "協作編輯草稿"
        conditions:
          - when: "目標文章狀態為 draft"

  - actor: A04
    stories:
      - ref: US-301
        permissions: [ReviewActions]
        scope: all
        context: "審閱所有待審內容"
      - ref: US-302
        permissions: [PublishControl]
        scope: all
        context: "將已核准內容發布上線"
        conditions:
          - when: "內容狀態為 approved"

  - actor: A05
    stories:
      - ref: US-401
        permissions: [Read, ViewAuditLog, Export]
        scope: all
        context: "檢視完整系統操作紀錄"

  - actor: A90
    stories:
      - ref: US-501
        permissions: [Publish]
        scope: all
        context: "依排程自動發布已核准內容"
        conditions:
          - when: "內容狀態為 approved 且已到達排程時間"
          - requires-approval-from: A04

ap-mapping:
  - story: US-101
    apcat: UserMgmt
    entities:
      - id: AP-001
        name: 使用者清單查詢
        endpoint-ref: haAPI::GET /users
        dbml-ref: DBML::users
        required-permissions: [Read]
      - id: AP-002
        name: 使用者帳號建立
        endpoint-ref: haAPI::POST /users
        dbml-ref: DBML::users
        required-permissions: [Create]

  - story: US-301
    apcat: ReviewMgmt
    entities:
      - id: AP-040
        name: 待審內容清單
        endpoint-ref: haAPI::GET /reviews/pending
        dbml-ref: DBML::articles
        required-permissions: [Read]
      - id: AP-041
        name: 核准內容
        endpoint-ref: haAPI::POST /articles/{id}/approve
        dbml-ref: DBML::review_logs
        required-permissions: [Approve]

constraints:
  separation-of-duty:
    - name: "內容建立與審核職責分離"
      actors: SAME-ACTOR
      conflicting-permissions: [Submit, Approve]
      on-stories: [US-201, US-301]
      rationale: "同一人不可同時擔任內容提交者與審核者"
      severity: error

    - name: "使用者管理與稽核職責分離"
      actors: SAME-ACTOR
      conflicting-permissions: [AssignRole, ViewAuditLog]
      on-stories: [US-104, US-401]
      rationale: "角色指派者不可同時擔任稽核員"
      severity: error

  mutual-exclusion:
    - name: "系統管理員與稽核員互斥"
      exclusive-actors: [A01, A05]
      rationale: "最高權限管理者與獨立稽核者必須由不同人擔任"
      severity: error

    - name: "內容編輯者與審核者互斥"
      exclusive-actors: [A03, A04]
      rationale: "編輯者與審核者不可為同一人（四眼原則）"
      severity: error

  mandatory-assignment:
    - name: "每個 UserStory 至少一個角色"
      target: story
      rule: "FORALL story S: COUNT(actors in S) >= 1"
      rationale: "確保所有需求都有明確的責任歸屬"

  cardinality:
    - name: "每個 UserStory 的角色數上限"
      subject: actors-per-story
      min: 1
      max: 5
      rationale: "避免過多角色參與導致權責不清"

  temporal:
    - name: "系統設定僅限上班時間"
      type: restricted-hours
      actors: [A01]
      time-window: 09:00-18:00
      rationale: "系統設定變更僅限上班時間"

  custom:
    - name: "系統角色不可持有管理權限"
      z3-expr: "ForAll([a], Implies(
                  actor_type(a) == 'system',
                  Not(Or(has_permission(a, 'Configure'),
                         has_permission(a, 'AssignRole'),
                         has_permission(a, 'Delete')))
                ))"
      rationale: "自動化系統角色僅限執行層操作"
      severity: error
```

### 8.3 角色權限矩陣（Permission Heatmap）

```
                    US-101  US-102  US-201  US-202  US-301  US-302  US-401  US-501
A01 SysAdmin        CRUD+    Cfg      -       -       R       -       -       -
A02 UserAdmin       CRU       -       -       -       -       -       -       -
A03 ContentEditor    -        -      Life    R+U      -       -       -       -
A04 ContentReviewer  -        -       R       -      Rev     Pub      -       -
A05 Auditor          -        -       -       -       R       -     Audit     -
A90 AutoPublisher    -        -       -       -       -       -       -      Pub

Legend: CRUD+ = CRUD+AssignRole, Cfg = Configure, Life = ContentLifecycle,
        Rev = ReviewActions, Pub = PublishControl, Audit = Read+ViewAuditLog+Export,
        R = ReadOnly, R+U = Read+Update, CRU = Create+Read+Update
```

### 8.4 約束驗證摘要

| # | 約束名稱 | 類型 | 嚴重度 | 驗證結果 |
|---|----------|------|--------|----------|
| C1 | 內容建立與審核職責分離 | SoD | error | ✅ PASS |
| C2 | 使用者管理與稽核職責分離 | SoD | error | ✅ PASS |
| C3 | 系統管理員與稽核員互斥 | Mutex | error | ✅ PASS |
| C4 | 內容編輯者與審核者互斥 | Mutex | error | ✅ PASS |
| C5 | 每個 UserStory 至少一個角色 | Mandatory | — | ✅ PASS |
| C6 | 系統角色不可持有管理權限 | Custom | error | ✅ PASS |

---

## 9. 驗證規則總覽

haARM 採用 4 層驗證架構：

### 第 1 層：語法驗證

- 所有必需字段必須存在
- 識別碼必須符合 `[a-zA-Z_][a-zA-Z0-9_]*` 模式
- 版本號必須符合 `\d+\.\d+(\.\d+)?` 模式
- 命名空間必須是點號分隔的識別碼
- YAML 格式合法

### 第 2 層：引用驗證

- 所有 actor 引用必須指向存在的 actor ID
- 所有 role 引用必須指向存在的 role ID
- 所有 permission 引用必須指向存在的 permission ID
- 角色繼承不能形成循環
- parent_roles 中的所有 ID 必須已定義

### 第 3 層：語義驗證（Z3 約束）

- 互斥約束不能被任何訪問規則同時滿足
- 依賴約束必須在頒配權限時檢查
- 基數約束不能被超過
- 自訂 Z3 表達式必須可求解

### 第 4 層：衝突檢測

- 同一演員的 `allow` 和 `deny` 規則優先級衝突檢查
- 依賴關係中的循環檢測
- 資源路徑衝突檢測
- 約束之間的互斥性檢測

### 驗證檢查清單

- [ ] 所有演員都存在且 ID 唯一
- [ ] 所有角色都存在且無循環繼承
- [ ] 所有權限都存在且資源有效
- [ ] 互斥約束已驗證
- [ ] 依賴約束已驗證
- [ ] 基數約束已驗證
- [ ] 自訂約束已驗證
- [ ] 沒有約束衝突
- [ ] 存取規則優先級合理
- [ ] 條件表達式合法
- [ ] 所有交叉引用（haAPI、DBML、haPDL）有效

### 9.5 常見誤用與反模式（Anti-Pattern, v3.3 新增）

> Q14 決議：Anti-Pattern 不獨立成章，整合進 §9（驗證規則）作為一體兩面。lint 訊息可直接引用本節編號（如 `error AP-01`）。

| 編號 | 反模式 | 為何錯 | 正確寫法 |
|------|--------|--------|---------|
| **AP-01** | 把 `contains` 當前綴比對<br>`deptId contains $self.department_id` | `contains` 自 v3.3 起正名為**中綴比對**（`LIKE '%substr%'`），會匹配 `ZA01B`、`XA01YB` 等非預期值；hyCMS 部門子樹隔離需要嚴格前綴 | 用 `starts_with`（見 §3.8.1）：<br>`deptId starts_with $self.department_id` |
| **AP-02** | `profile_overrides.<action>` 沒寫 `conditions:` 鍵 | Q6 合併語意：scalar 欄位 deep merge，但**conditions 是完全覆寫**——沒寫 key 表示「繼承 profile 原值」。PM 想「改 scope 只改 scope」時容易誤以為 conditions 也被清空 | 想繼承：省略 conditions 鍵<br>想清空：明示 `conditions: []`（lint 會在合併後 conditions 為空時 error） |
| **AP-03** | 同 namespace 兩個 `implicit: true` role | 隱式角色行為未定義：是 OR 聯集還是優先序？runtime 行為依 codegen 實作而異 | 同 namespace 至多一個 implicit role；多重隱式語意請用 `parent_roles` 階層繼承（lint 對此發出 warning，Q8） |
| **AP-04** | `scope: all` 套在 end-user 角色 | 等於把該 role 升為「跨部門全域可見」，違反最小權限原則；hyCMS 升級時常見錯誤 | 用 `scope: own` / `scope: department` / `scope: team`；無範圍限制必有業務理由並 code review |
| **AP-05** | 用 `enabled: false` 當 runtime 拒登手段 | Q7 決議：`enabled: false` 是**規格層遮罩**（lint 警告引用），不保證 runtime 攔截；真正的拒登在 codegen 端 | 規格層停用：`enabled: false`<br>Runtime 拒登：由 codegen 在 auth middleware 落實（不在 haARM 範圍） |

> **lint 觸發規則**：`haarm-lint` 在 v3.3 起檢查 AP-01～AP-05；違反 AP-01/AP-02 為 **error**，AP-03/AP-04 為 **warning**，AP-05 為 **hint**。

---

## 10. 跨規格映射

### 10.1 haARM ↔ haAPI 映射

| haARM 概念 | haAPI 對應 | 映射方式 |
|-----------|-----------|----------|
| Actor | — | haAPI 不直接定義角色 |
| Permission (action) | exposes.standard / operations | 權限動作對應 API 操作 |
| AccessRule (roles) | access.requires_roles | 角色清單直接對應 |
| Condition | access.conditions | 條件表達式對應 |

### 10.2 haARM ↔ HaPDL 映射

| haARM 概念 | HaPDL 對應 | 映射方式 |
|-----------|-----------|----------|
| Actor (roles) | security.action_level.requires_roles | 角色清單對應 |
| Permission | security.field_level.visible_to_roles | 欄位級權限 |
| AccessRule | security.data_isolation | 資料隔離規則 |

### 10.3 haARM ↔ DBML 映射

| haARM 概念 | DBML 對應 | 自動生成 |
|-----------|----------|----------|
| Actor | roles 表 | ✓ |
| Permission | permissions 表 | ✓ |
| Role-Permission | role_permissions 表 | ✓ |
| AccessRule | access_rules 表 | ✓ |
| Constraint | constraint_rules 表 | ✓ |

### 10.4 haARM → Gherkin 自動轉換

haARM 的約束定義可自動轉換為 Gherkin BDD 測試場景：

```gherkin
# 自動產生自 haARM constraint: 內容建立與審核職責分離

Feature: 內容建立與審核職責分離驗證

  @permission-check @sod @severity-error
  Scenario: 內容編輯者不可核准自己提交的內容
    Given 使用者角色為 "ContentEditor"
    And 使用者已對文章 "ART-001" 執行 "Submit"
    When 使用者嘗試對同一文章執行 "Approve"
    Then 系統應拒絕存取
    And 回傳錯誤訊息包含 "職責分離違規"

  @permission-check @mutex @severity-error
  Scenario: 同一帳號不可同時持有編輯者與審核者角色
    Given 使用者已被指派角色 "ContentEditor"
    When 管理員嘗試為該使用者加指角色 "ContentReviewer"
    Then 系統應拒絕角色指派
    And 回傳錯誤訊息包含 "互斥角色衝突"
```

### 10.5 haARM → DBML RBAC 資料表自動生成

```dbml
// 自動產生自 haARM actors + permissions 定義

Table roles {
  id varchar [pk, note: "對應 haARM actor id"]
  name varchar [not null]
  alias varchar [unique]
  description text
  type varchar [note: "human | system | external | composite"]
  inherits_from varchar [ref: > roles.id]
  group_name varchar
  is_active boolean [default: true]
  created_at timestamp [default: `now()`]
}

Table permissions {
  id int [pk, increment]
  action varchar [not null, note: "對應 haARM vocabulary"]
  description text
}

Table role_permissions {
  id int [pk, increment]
  role_id varchar [ref: > roles.id]
  story_ref varchar [note: "對應 haPDL UserStory ID"]
  permission_id int [ref: > permissions.id]
  scope varchar [note: "own | group | department | all"]
  context text
  effective_from date
  effective_until date

  indexes {
    (role_id, story_ref, permission_id) [unique]
  }
}

Table constraint_rules {
  id int [pk, increment]
  name varchar [not null]
  type varchar [note: "sod | mutex | mandatory | cardinality | temporal | custom"]
  severity varchar [default: "error"]
  rule_expression text
  rationale text
  is_active boolean [default: true]
}

Table mutual_exclusions {
  id int [pk, increment]
  constraint_id int [ref: > constraint_rules.id]
  actor_id_1 varchar [ref: > roles.id]
  actor_id_2 varchar [ref: > roles.id]
}
```

---

## 11. 工具鏈與最佳實踐

### 11.1 工具鏈

```
haARM YAML
  ↓ (驗證)
JSON Schema + Z3 Solver
  ↓ (編譯)
RBAC Engine Code
  ├─ TypeScript: role.checker.ts
  ├─ Python: rbac_validator.py
  └─ SQL: permission_tables.sql
```

### 11.2 工具支援

| 工具 | 功能 | 狀態 |
|------|------|------|
| **VSCode 擴展** | 語法著色、自動補全、即時驗證 | 規劃中 |
| **CLI 工具** | `haarm validate`、`haarm to-gherkin`、`haarm to-dbml` | 規劃中 |
| **Z3 整合** | 約束滿足性檢查 | ✓ 可用 |
| **JSON Schema** | 語法驗證 | ✓ 可用 |

### 11.3 最佳實踐

#### 檔案命名

```
<name>.haarm.yaml
```

範例：
```
rbac.haarm.yaml
ecommerce-auth.haarm.yaml
cms-permissions.haarm.yaml
```

#### 設計原則

1. **最小權限原則**：只授予必要的最小權限
2. **職責分離**：關鍵操作至少需要兩人參與
3. **角色層級化**：使用繼承減少重複定義
4. **約束先行**：先定義治理約束，再定義權限規則
5. **條件細化**：使用 conditions 實現精確的授權控制

#### 版本控制

- 遵循**語義化版本** (SemVer) 規範
- MAJOR.MINOR.PATCH 格式
- 向後兼容性檢查

### 11.4 性能考慮

- **大規模約束**：使用增量求解
- **複雜表達式**：預編譯為 Z3 AST
- **快取結果**：對相同約束組合進行快取
- **並行驗證**：獨立的約束可並行驗證

---

## 12. 附錄：遷移指南與擴展點

### 12.1 從簡化版遷移到完整 BNF 版

| 簡化版概念 | 完整 BNF 版對應 | 遷移步驟 |
|-----------|----------------|----------|
| actors.type: user | actors.type: human | 更新 type 名稱 |
| roles + permissions | permissions.vocabulary + aliases | 改用詞彙表 + 別名系統 |
| access_control | participation-matrix | 按 UserStory 重新組織 |
| — | ap-mapping | 新增 API 端點與 DBML 對應 |
| constraints (flat) | constraints (categorized) | 按類型分類 |

### 12.2 Lark Parser Grammar（實作參考）

以下為 Lark parser 格式的實作文法骨架，可直接用於 Python 解析器開發：

```lark
start: metadata section*

metadata: "haarm:" NEWLINE properties

section: actors_section
       | permissions_section
       | participation_section
       | ap_mapping_section
       | constraints_section

actors_section: "actors:" NEWLINE actor_def+
actor_def: "- id:" ACTOR_ID NEWLINE actor_props
actor_props: (actor_prop NEWLINE)*
actor_prop: "name:" STRING
          | "alias:" IDENTIFIER
          | "description:" STRING
          | "type:" ACTOR_TYPE
          | "inherits:" actor_id_or_list
          | "group:" group_id_or_list
          | "tags:" tag_list

permissions_section: "permissions:" NEWLINE vocab aliases? scopes?
vocab: "vocabulary:" NEWLINE ("- " PERMISSION_ACTION NEWLINE)+
aliases: "aliases:" NEWLINE alias_def+
alias_def: IDENTIFIER ":" permission_list NEWLINE
scopes: "scopes:" NEWLINE scope_def+

participation_section: "participation-matrix:" NEWLINE participation_entry+
participation_entry: "- actor:" ACTOR_ID NEWLINE "stories:" NEWLINE story_part+
story_part: "- ref:" STORY_REF NEWLINE story_part_props

ap_mapping_section: "ap-mapping:" NEWLINE story_ap_entry+
story_ap_entry: "- story:" STORY_REF NEWLINE "apcat:" IDENTIFIER NEWLINE "entities:" NEWLINE ap_entity+

constraints_section: "constraints:" NEWLINE constraint_category+
constraint_category: sod_constraints
                   | mutex_constraints
                   | mandatory_constraints
                   | cardinality_constraints
                   | temporal_constraints
                   | custom_constraints

// --- Terminal Rules ---
ACTOR_ID: /A\d{2,}/
AP_ID: /AP-\d{3,}/
STORY_REF: /US-\d{3,}/
ACTOR_TYPE: "human" | "system" | "external" | "composite"
SCOPE_TARGET: "all" | "own" | "group" | "department"
SEVERITY: "error" | "warning" | "info"
PERMISSION_ACTION: /[A-Z][a-zA-Z]*/
IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_-]*/
ENDPOINT_REF: /haAPI::(GET|POST|PUT|PATCH|DELETE) \/[a-zA-Z0-9\/_{}.-]+/
DBML_REF: /DBML::[a-zA-Z_][a-zA-Z0-9_.]+/
STRING: /[^\n]+/

%import common.NEWLINE
%import common.WS_INLINE
%ignore WS_INLINE
```

### 12.3 Z3 安裝

```bash
# Python 安裝
pip install z3-solver

# 驗證安裝
python -c "from z3 import *; print('Z3 installed successfully')"
```

---

**文檔版本**：v3.3.0 (Release Candidate, 2026-05-14)
**撰寫日期**：2026-04-12（初版）；2026-05-14（v3.3 升版）
**所屬框架**：WA-RAPTor
**維護者**：WA-RAPTor 規範工作組

---

## 附錄 B: §7 跨規格整合（v3.3 新增；M3 已落地）

> v3.3 統一章節骨架 §7 = 跨規格整合（見 §0.3）。完整跨 DSL 導覽請見 [`CROSS-DSL-GUIDE.md`](CROSS-DSL-GUIDE.md)；本節僅列 haARM 端的引用界面與 hycms-ht002 範例對應。

### B.7.1 haARM 是橫切面 DSL

haARM 與其他三個 DSL 都互相引用：

| 來自 | 引用 haARM 哪個欄位 | 用途 |
|------|-------------------|------|
| DBML（被動）| `resource.id` ↔ Table 名稱、`resource.fields[]` ↔ Column 名稱 | RBAC 資源/欄位對應 |
| haAPI | `permissions[].id`、`roles[].id`、`constraints[].id` | API 端點權限 |
| haPDL | `roles[].id`、`permissions[].id` | 頁面層級權限/角色判定 |
| Gherkin | `actors[].id` + `roles[].id` | BDD 場景的 Given 步驟 |

### B.7.2 haARM 端的跨 DSL 引用點

| 引用點 | haARM 結構 | 被誰引用 | 驗證規則 |
|--------|----------|---------|---------|
| Resource ↔ DBML Table | `resources[].id`（case-insensitive 匹配 DBML Table）| 隱式被 DBML 對齊 | `validate_cross_dsl.py` Rule 1 |
| Resource fields | `resources[].fields[]` | DBML Column 名稱 | Rule 1 |
| Permission ID | `permissions[].id` | haAPI `access.endpoints.{op}.required_permissions[].id`、haPDL `security.permission_refs.*[].id` | Rule 3 |
| Role ID | `roles[].id` | haAPI `access.endpoints.{op}.required_roles[]`、haPDL `auth.roles[]` | Rules 4, 6 |
| Constraint ID | `constraints[].id` | haAPI `access.endpoints.{op}.conditions[].haarm_constraint` | （v3.3 opaque ref，M4 lint 補上） |

### B.7.3 hycms-ht002 範例對應

`benchmarks/haARM/hycms-ht002.haarm.yaml`：

```yaml
resources:
  - id: infouser                       # ← case-insensitive 匹配 DBML Table InfoUser
    fields: [userId, deptId, email, ...]  # ← 必須是 DBML 欄位
    profile: dept_isolated_crud        # v3.3 §3.10 Profile 系統

roles:
  - id: htsd                            # ← 被 haAPI/haPDL 引用
    profile: dept_viewer

permissions:
  - id: infouser_read                   # ← 被 haAPI access.endpoints 引用
    ...
    conditions:
      - field: deptId
        operator: starts_with           # v3.3 §3.8.1 新運算子
        value: "$self.department_id"

constraints:
  - id: audit_sysadm_exclusion          # ← 可被 haAPI haarm_constraint 引用
    type: mutual_exclusion
    rule: { not_both: [audit, sysadm] }
```

跑 `python benchmarks/validate_cross_dsl.py hycms-ht002` 驗證引用一致性。

### B.7.4 與 `CROSS-DSL-GUIDE.md` 的關係

本節是 haARM 視角的引用清單；CROSS-DSL-GUIDE.md 是四 DSL 平面的完整對應表（含版本互鎖、Anti-Pattern、同步機制）。**新增跨 DSL anchor 時須先讀 CROSS-DSL-GUIDE §3.2 流程**。

---
