# haARM v3.3 語法規範文檔

> **版本**: v3.3.0 (Release Candidate, 2026-05-13)
> **前版**: v2（見 `archive/haARM-Specification_v2.md`）
> **v3.3 重點**: (1) 新增 `starts_with` / `ends_with` 運算子，正名 `contains` 為中綴比對；(2) 引入 Convention over Configuration 三段式（M1 schema、M2 sugar 規則）；(3) Actor.enabled / Role.implicit / Resource.allowed_actions / Permission.legacy_bit 一級欄位；(4) dynamic_grants 文件化（預設 disabled，v3.4 落地）
> **SSoT 主手冊**: `haARMdoc.md`（本檔為技術參考；正式範例與整合說明請見主手冊）

## 概述

haARM（ha Actor-Role Modeling Language）是 WA-RAPTor 框架的**橫切面 DSL**，專注於角色基礎存取控制（RBAC）建模，並預留屬性基礎（ABAC）與關係基礎（ReBAC）的擴展空間。

### 定位

haARM 不是管線中的第八個階段，而是橫跨 Intent 與 Implementation 兩層的**共用定義**，被多個規格引用：

```
Intent Layer（意圖層）          Implementation Layer（實作層）
─────────────────────          ──────────────────────────────
1. DBML（領域模型）              5. TypeSpec/OpenAPI
2. High-level Gherkin            6. PDL（頁面實作規格）
3. haAPI（高階 API）             7. Low-level Gherkin
4. haPDL（高階頁面）

        ╔══════════════════════════════════════╗
        ║  haARM（橫切面：角色/權限/存取控制）      ║
        ║  被 #2, #3, #4, #6, #7 引用              ║
        ╚══════════════════════════════════════╝
```

**跨 DSL 銜接點：**

| haARM 元素 | 引用方 | 對應欄位 |
|-----------|--------|---------|
| `role.id` | haPDL | `auth.roles[]` |
| `permission.id` | haAPI | 端點的 `@useAuth` 權限宣告 |
| `actor.id` + `role.id` | Gherkin | `Given 用戶為 <actor> 且具角色 <role>` |
| `resource.id` | DBML / haAPI | entity 名稱 / 端點資源路徑 |

### v2 變更摘要

| 變更項目 | v1 | v2 |
|---------|----|----|
| 新增 `resources` 區段 | permission 直接寫 resource 字串 | 獨立定義 resource，permission 引用 resource ID |
| Permission action | JSON Schema enum 限定 7 種 | 改為 pattern，支援 CustomAction |
| AccessRule actor/roles | 都是 optional，無約束 | 加入 `oneOf`，至少填一個 |
| Constraint | 僅 Z3 語法字串 | 新增結構化替代語法，Z3 為進階選項 |
| Condition 擴展 | 僅靜態 field/operator/value | 新增 `context:` 前綴支援動態屬性、`$self` 關係引用、時間窗口語意 |
| 定位說明 | 稱為「第八個 DSL」 | 明確為橫切面規格 |

---

## 1. EBNF 文法定義

```ebnf
(* haARM v2 文法定義 *)

HaARMDocument ::= MetadataSection
                  ActorsSection
                  RolesSection
                  ResourcesSection
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
             | 'enabled' ':' Boolean NEWLINE  (* v3.3：規格層遮罩；預設 true *)

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
            | 'implicit' ':' Boolean NEWLINE  (* v3.3：隱式角色，所有 actor 自動具備；預設 false *)

RoleRefList ::= '[' RoleRef (',' RoleRef)* ']'

RoleRef ::= '@' RoleId | RoleId

(* ===== 資源區段（v2 新增）===== *)
ResourcesSection ::= 'resources' ':' NEWLINE
                     (INDENT ResourceDefinition+ DEDENT)?

ResourceDefinition ::= '- id' ':' ResourceId NEWLINE
                       INDENT ResourceFields DEDENT

ResourceFields ::= ResourceField
                 | ResourceField ResourceFields

ResourceField ::= 'name' ':' String NEWLINE
                | 'type' ':' ResourceType NEWLINE
                | 'parent' ':' ResourceRef NEWLINE
                | 'description' ':' String NEWLINE
                | 'fields' ':' ResourceFieldList NEWLINE
                | 'allowed_actions' ':' ActionList NEWLINE  (* v3.3：UI/lint 用 action 白名單；省略=不限 *)

ActionList ::= '[' ActionType (',' ActionType)* ']'

ResourceType ::= 'entity' | 'collection' | 'action' | 'view'

ResourceRef ::= '@' ResourceId | ResourceId

ResourceFieldList ::= '[' String (',' String)* ']'

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
                  | 'scope' ':' ScopeType NEWLINE
                  | 'legacy_bit' ':' Integer NEWLINE  (* v3.3：hyCMS bitmask 遷移期對照值；不影響語義 *)

ActionType ::= 'read' | 'write' | 'create' | 'update' | 'delete'
             | 'execute' | 'admin' | CustomAction

CustomAction ::= Identifier

(* v2: 新增 scope 用於關係型權限 *)
ScopeType ::= 'all' | 'own' | 'department' | 'team' | CustomScope

CustomScope ::= Identifier

(* ===== 條件定義（v2 擴展）===== *)
ConditionList ::= '[' Condition (',' Condition)* ']'
                | Condition

Condition ::= FieldCondition | TimeWindowCondition

FieldCondition ::= FieldName Operator FieldValue

(* v2: 支援動態屬性，以 context: 前綴區分 runtime 值 *)
FieldName ::= StaticField | DynamicField

StaticField ::= Identifier ('.' Identifier)*

DynamicField ::= 'context' ':' Identifier ('.' Identifier)*

(* v2: $self 引用當前 actor 的屬性，用於關係型權限 *)
FieldValue ::= String | Number | Boolean | Array | SelfRef

SelfRef ::= '$self' '.' Identifier ('.' Identifier)*

Array ::= '[' Value (',' Value)* ']'

(* v2: 時間窗口條件，語意明確 *)
TimeWindowCondition ::= 'time_window' ':' NEWLINE
                        INDENT TimeWindowFields DEDENT

TimeWindowFields ::= TimeWindowField
                   | TimeWindowField TimeWindowFields

TimeWindowField ::= 'start' ':' TimeValue NEWLINE
                  | 'end' ':' TimeValue NEWLINE
                  | 'timezone' ':' String NEWLINE
                  | 'days' ':' DayList NEWLINE

TimeValue ::= String (* HH:MM 格式 *)

DayList ::= '[' DayName (',' DayName)* ']'

DayName ::= 'mon' | 'tue' | 'wed' | 'thu' | 'fri' | 'sat' | 'sun'

Operator ::= '==' | '!=' | '<' | '>' | '<=' | '>=' | 'in'
           | 'contains' | 'starts_with' | 'ends_with'  (* v3.3：新增前綴/後綴比對 *)

(* ===== 存取控制區段 ===== *)
AccessControlSection ::= 'access_control' ':' NEWLINE
                         (INDENT AccessRule+ DEDENT)?

(* v2: actor 或 roles 至少須填一個 *)
AccessRule ::= '- id' ':' RuleId NEWLINE
               INDENT (ActorAccessFields | RolesAccessFields) DEDENT

ActorAccessFields ::= 'actor' ':' ActorRef NEWLINE
                      CommonRuleFields

RolesAccessFields ::= 'roles' ':' RoleRefList NEWLINE
                      CommonRuleFields

CommonRuleFields ::= RuleField
                   | RuleField CommonRuleFields

RuleField ::= 'permissions' ':' PermissionRefList NEWLINE
            | 'effect' ':' Effect NEWLINE
            | 'conditions' ':' ConditionList NEWLINE
            | 'priority' ':' Integer NEWLINE

ActorRef ::= '@' ActorId | ActorId

Effect ::= 'allow' | 'deny'

PermissionRefList ::= '[' PermissionRef (',' PermissionRef)* ']'

PermissionRef ::= '@' PermissionId | PermissionId

(* ===== 約束條件區段（v2 擴展）===== *)
ConstraintsSection ::= 'constraints' ':' NEWLINE
                       (INDENT Constraint+ DEDENT)?

Constraint ::= '- id' ':' ConstraintId NEWLINE
               INDENT ConstraintFields DEDENT

ConstraintFields ::= ConstraintField
                   | ConstraintField ConstraintFields

(* v2: 支援結構化語法或 Z3 表達式 *)
ConstraintField ::= 'type' ':' ConstraintType NEWLINE
                  | 'rule' ':' StructuredRule NEWLINE
                  | 'expression' ':' Expression NEWLINE
                  | 'severity' ':' Severity NEWLINE
                  | 'description' ':' String NEWLINE

ConstraintType ::= 'mutual_exclusion' | 'dependency' | 'cardinality' | 'custom'

(* v2 新增：結構化約束語法，替代 Z3 *)
StructuredRule ::= MutualExclusionRule | DependencyRule | CardinalityRule

MutualExclusionRule ::= 'not_both' ':' '[' RoleRef ',' RoleRef ']'

DependencyRule ::= 'requires' ':' '{' RoleRef ':' RoleRef '}'

CardinalityRule ::= 'max_holders' ':' '{' RoleRef ':' Integer '}'

(* Z3 表達式作為進階選項 *)
Expression ::= String

Severity ::= 'error' | 'warning'

(* ===== 基本符號 ===== *)
Identifier ::= Letter (Letter | Digit | '_')*

ActorId ::= Identifier
RoleId ::= Identifier
PermissionId ::= Identifier
ResourceId ::= Identifier
RuleId ::= Identifier
ConstraintId ::= Identifier

String ::= '"' StringContent '"'
StringContent ::= (Character - '"')*
Character ::= ? 任何字符 ?
Number ::= DigitSequence ('.' DigitSequence)?
Integer ::= DigitSequence
Boolean ::= 'true' | 'false'
DigitSequence ::= Digit+
Digit ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
Letter ::= 'a' | 'b' | ... | 'z' | 'A' | 'B' | ... | 'Z'

NEWLINE ::= ? 換行符號 ?
INDENT ::= ? 增加縮排 ?
DEDENT ::= ? 減少縮排 ?
```

---

## 2. JSON Schema 定義

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://wa-raptor.example.com/haarm/v2/schema.json",
  "title": "haARM v2 Schema",
  "description": "Schema for ha Actor-Role Modeling Language v2",
  "type": "object",
  "required": ["metadata", "actors", "roles", "resources", "permissions", "access_control"],
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
    "resources": {
      "type": "array",
      "items": { "$ref": "#/definitions/Resource" },
      "description": "資源定義清單（v2 新增）"
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
        },
        "enabled": {
          "type": "boolean",
          "default": true,
          "description": "v3.3：規格層遮罩。false 時所有引用此 actor 的規則被 lint 警告/拒絕；runtime 拒登在 codegen 端落實（Q7 決議）"
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
        },
        "implicit": {
          "type": "boolean",
          "default": false,
          "description": "v3.3：true 時所有 actor 自動具備此角色（hyCMS isPublic 對應）。同 namespace 若出現 ≥2 個 implicit role，lint 發出警告（Q8 決議）"
        }
      }
    },
    "Resource": {
      "type": "object",
      "required": ["id", "name", "type"],
      "additionalProperties": false,
      "description": "資源定義（v2 新增）",
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_.]*$",
          "description": "資源唯一識別碼，支援點號階層（e.g., orders.details）"
        },
        "name": {
          "type": "string",
          "minLength": 1,
          "description": "資源可讀名稱"
        },
        "type": {
          "type": "string",
          "enum": ["entity", "collection", "action", "view"],
          "description": "資源類型"
        },
        "parent": {
          "type": "string",
          "description": "父資源 ID（建立階層結構）"
        },
        "description": {
          "type": "string",
          "description": "資源描述"
        },
        "fields": {
          "type": "array",
          "items": { "type": "string" },
          "description": "資源包含的欄位清單（可用於 field-level 權限控制）"
        },
        "allowed_actions": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$"
          },
          "description": "v3.3：UI 與 lint 用的 action 白名單（對映 hyCMS AP.apmask）。省略=該 resource 上所有出現過的 action；明示則限制可用 action 範圍"
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
          "description": "資源 ID 引用（應對應 resources 區段中定義的 ID，或使用 * 萬用符）"
        },
        "action": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
          "description": "操作類型（內建：read, write, create, update, delete, execute, admin；亦可自訂）"
        },
        "scope": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
          "description": "權限作用範圍（v2 新增：all=全部, own=僅自己的, department=同部門, team=同團隊；亦可自訂）",
          "default": "all"
        },
        "conditions": {
          "type": "array",
          "items": { "$ref": "#/definitions/Condition" },
          "description": "條件約束"
        },
        "description": {
          "type": "string",
          "description": "權限描述"
        },
        "legacy_bit": {
          "type": "integer",
          "minimum": 1,
          "description": "v3.3：hyCMS bitmask 遷移期對照值（如 4=create、8=update）。純文件性註記，不影響 runtime 語義；遷移完成後可移除"
        }
      }
    },
    "Condition": {
      "oneOf": [
        { "$ref": "#/definitions/FieldCondition" },
        { "$ref": "#/definitions/TimeWindowCondition" }
      ]
    },
    "FieldCondition": {
      "type": "object",
      "required": ["field", "operator", "value"],
      "additionalProperties": false,
      "properties": {
        "field": {
          "type": "string",
          "description": "欄位名稱。靜態欄位直接寫路徑（e.g., user.department）；動態屬性加 context: 前綴（e.g., context:current_time）"
        },
        "operator": {
          "type": "string",
          "enum": ["==", "!=", "<", ">", "<=", ">=", "in", "contains", "starts_with", "ends_with"],
          "description": "比較運算子。v3.3 新增 `starts_with`（前綴，等價 SQL `LIKE 'prefix%'`）與 `ends_with`（後綴，等價 SQL `LIKE '%suffix'`）。`contains` 自 v3.3 起正名為中綴比對（`LIKE '%substr%'`）"
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
          "description": "比較值。可使用 $self.field 引用當前 actor 的屬性（e.g., $self.department 表示「與自己同部門」）"
        }
      }
    },
    "TimeWindowCondition": {
      "type": "object",
      "required": ["time_window"],
      "additionalProperties": false,
      "description": "時間窗口條件（v2 新增）",
      "properties": {
        "time_window": {
          "type": "object",
          "required": ["start", "end"],
          "additionalProperties": false,
          "properties": {
            "start": {
              "type": "string",
              "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
              "description": "開始時間 (HH:MM)"
            },
            "end": {
              "type": "string",
              "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
              "description": "結束時間 (HH:MM)"
            },
            "timezone": {
              "type": "string",
              "description": "時區 (e.g., Asia/Taipei)",
              "default": "UTC"
            },
            "days": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
              },
              "description": "適用的星期幾"
            }
          }
        }
      }
    },
    "AccessRule": {
      "type": "object",
      "required": ["id", "effect"],
      "additionalProperties": false,
      "oneOf": [
        { "required": ["id", "effect", "actor"] },
        { "required": ["id", "effect", "roles"] }
      ],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*$",
          "description": "規則唯一識別碼"
        },
        "actor": {
          "type": "string",
          "description": "演員 ID（與 roles 二選一，至少填一個）"
        },
        "roles": {
          "type": "array",
          "items": { "type": "string" },
          "description": "角色 ID 清單（與 actor 二選一，至少填一個）"
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
      "required": ["id", "type"],
      "additionalProperties": false,
      "description": "v2：rule（結構化）或 expression（Z3）至少填一個",
      "oneOf": [
        { "required": ["id", "type", "rule"] },
        { "required": ["id", "type", "expression"] }
      ],
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
        "rule": {
          "$ref": "#/definitions/StructuredRule",
          "description": "結構化約束語法（v2 新增，推薦使用）"
        },
        "expression": {
          "type": "string",
          "description": "Z3 邏輯表達式（進階選項，用於 custom 類型或複雜邏輯）"
        },
        "severity": {
          "type": "string",
          "enum": ["error", "warning"],
          "description": "違反約束的嚴重程度"
        },
        "description": {
          "type": "string",
          "description": "約束描述"
        }
      }
    },
    "StructuredRule": {
      "type": "object",
      "description": "結構化約束定義（v2 新增）",
      "oneOf": [
        {
          "required": ["not_both"],
          "additionalProperties": false,
          "properties": {
            "not_both": {
              "type": "array",
              "items": { "type": "string" },
              "minItems": 2,
              "maxItems": 2,
              "description": "互斥的兩個角色 ID"
            }
          }
        },
        {
          "required": ["requires"],
          "additionalProperties": false,
          "properties": {
            "requires": {
              "type": "object",
              "additionalProperties": { "type": "string" },
              "description": "依賴關係：key 角色依賴 value 角色（e.g., { team_lead: manager }）"
            }
          }
        },
        {
          "required": ["max_holders"],
          "additionalProperties": false,
          "properties": {
            "max_holders": {
              "type": "object",
              "additionalProperties": { "type": "integer", "minimum": 1 },
              "description": "基數限制：key 角色最多 value 人持有（e.g., { admin: 5 }）"
            }
          }
        }
      ]
    }
  }
}
```

---

## 3. 語法元素詳細說明表

### 3.1 文件結構層級

| 層級 | 元素 | 必需 | 類型 | 說明 |
|------|------|:----:|------|------|
| 0 | 根文檔 | - | Object | haARM 根層級 |
| 1 | metadata | Y | Object | 文檔元資料 |
| 1 | actors | Y | Array | 演員清單 |
| 1 | roles | Y | Array | 角色清單 |
| 1 | **resources** | **Y** | **Array** | **資源清單（v2 新增）** |
| 1 | permissions | Y | Array | 權限清單 |
| 1 | access_control | Y | Array | 存取規則清單 |
| 1 | constraints | N | Array | 治理約束（可選） |

### 3.2 Metadata（元資料）字段

| 字段 | 類型 | 必需 | 格式 | 說明 |
|------|------|:----:|------|------|
| title | String | Y | - | 文檔標題，至少 1 個字符 |
| version | String | Y | `\d+\.\d+(\.\d+)?` | 版本號，符合 SemVer |
| description | String | N | - | 文檔描述 |
| namespace | String | N | `^[a-zA-Z_]...` | 命名空間，點號分隔 |

**範例：**
```yaml
metadata:
  title: E-Commerce RBAC
  version: 2.0.0
  namespace: com.example.ecommerce.auth
  description: E-Commerce Platform 的角色存取控制模型
```

### 3.3 Actor（演員）定義

| 字段 | 類型 | 必需 | 有效值 | 說明 |
|------|------|:----:|--------|------|
| id | String | Y | `[a-zA-Z_][a-zA-Z0-9_]*` | 演員唯一識別碼 |
| name | String | Y | - | 演員可讀名稱 |
| type | String | Y | user, system, service, external | 演員類型 |
| description | String | N | - | 演員描述 |
| properties | Object | N | 鍵值對 | 自訂屬性（可選） |
| **enabled** | **Boolean** | **N** | **true / false** | **v3.3：規格層遮罩（Q7）。預設 `true`；`false` 時引用此 actor 的規則被 lint 警告，runtime 拒登由 codegen 端落實。對映 hyCMS `ugrpId='Disable'`。<br/>**PM 何時填**：明確要把某 actor「停用但保留歷史」時填 `enabled: false`（如離職員工帳號）；新增 actor 預設可省略。 |

**有效的 Actor Type：**
- `user` - 真實用戶
- `system` - 系統內部演員
- `service` - 微服務或服務帳戶
- `external` - 外部系統或第三方

**範例：**
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

### 3.4 Role（角色）定義

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| id | String | Y | 角色唯一識別碼 |
| name | String | Y | 角色可讀名稱 |
| description | String | N | 角色描述 |
| parent_roles | Array | N | 父角色 ID 清單（支持層級繼承） |
| permissions | Array | N | 權限 ID 清單 |
| **implicit** | **Boolean** | **N** | **v3.3：預設 `false`；`true` 時所有 actor 自動具備此角色（對映 hyCMS `ugrp.isPublic='Y'`）。同 namespace 若出現 ≥2 個 implicit role，lint 發出警告（Q8）。<br/>**PM 何時填**：當「全公司任何登入者都該有這個 role 的權限」時填 `implicit: true`（例：所有員工都可讀公告板）；極少使用，多數 role 應顯式指派給特定 actor。 |

**支持角色繼承層級：**
- 子角色可繼承父角色的所有權限
- 支持多重繼承
- 循環繼承會被約束檢測拒絕

**範例：**
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

### 3.5 Resource（資源）定義（v2 新增）

| 字段 | 類型 | 必需 | 有效值 | 說明 |
|------|------|:----:|--------|------|
| id | String | Y | `[a-zA-Z_][a-zA-Z0-9_.]*` | 資源唯一識別碼（支援點號階層） |
| name | String | Y | - | 資源可讀名稱 |
| type | String | Y | entity, collection, action, view | 資源類型 |
| parent | String | N | 資源 ID | 父資源（建立階層） |
| description | String | N | - | 資源描述 |
| fields | Array | N | 字串清單 | 資源欄位（用於 field-level 權限控制） |
| **allowed_actions** | **Array<String>** | **N** | **action 名稱清單** | **v3.3：UI 與 lint 用的 action 白名單（對映 hyCMS `AP.apmask`）。省略=該 resource 上所有出現過的 action 都被允許；明示則限制可用 action 範圍。<br/>**PM 何時填**：當 resource 在不同頁面只應顯示部分動作按鈕時填（例：稽核員頁面只能 `[read, export]`）；UI 不需遮罩可省略。 |

**資源類型說明：**

| 類型 | 說明 | 範例 |
|------|------|------|
| `entity` | 領域實體，對應 DBML 中的 table | users, orders |
| `collection` | 實體的子集合或聚合 | orders.items, users.addresses |
| `action` | 可執行操作（非 CRUD） | reports.generate, system.backup |
| `view` | 唯讀視圖或儀表板 | dashboard.sales, reports.monthly |

**範例：**
```yaml
resources:
  - id: users
    name: 用戶
    type: entity
    description: 用戶主檔
    fields: [id, name, email, department, role]

  - id: users.profile
    name: 用戶個人資料
    type: collection
    parent: users
    description: 用戶個人資料子集

  - id: orders
    name: 訂單
    type: entity
    fields: [id, customer_id, amount, status, created_by]

  - id: orders.details
    name: 訂單明細
    type: collection
    parent: orders

  - id: reports.generate
    name: 產生報表
    type: action
    description: 觸發報表產生流程
```

**設計理由：**
- v1 中 permission 直接寫 resource 字串（如 `users.profile`），無法驗證 typo
- v2 將 resource 獨立定義，permission 的 `resource` 欄位改為引用 resource ID
- Lint 工具可檢查 permission 引用的 resource 是否存在
- `fields` 欄位預留 field-level 權限控制的擴展空間

### 3.6 Permission（權限）定義

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| id | String | Y | 權限唯一識別碼 |
| resource | String | Y | 資源 ID 引用（對應 resources 區段）或 `*` |
| action | String | Y | 操作類型（內建或自訂） |
| **scope** | **String** | **N** | **權限作用範圍（v2 新增，預設 all）** |
| **fields** | **Array<String>** | **N** | **此 permission 准許操作的欄位白名單（2026-05-11 dead-letter 遷移擴充；預設為 resource.fields 全集）** |
| conditions | Array | N | 條件約束清單 |
| description | String | N | 權限描述 |
| **legacy_bit** | **Integer** | **N** | **v3.3：hyCMS bitmask 遷移期對照值（如 4=create、8=update）。純文件性註記，不影響 runtime 語義；遷移完成後可移除。<br/>**PM 何時填**：正在從 hyCMS 移植權限資料、需要保留與舊 `uGrpAP.rights` smallint 的對照關係時填；新專案或已脫離 bitmask 的場景省略。 |

**內建 Action 類型：**
- `read` - 讀取資源
- `write` - 寫入資源
- `create` - 建立新資源
- `update` - 更新資源
- `delete` - 刪除資源
- `execute` - 執行操作/函數
- `admin` - 管理資源

> **v2 變更**：action 不再限於 enum，可使用自訂動作名稱（如 `approve`、`export`、`archive`），只要符合 `[a-zA-Z_][a-zA-Z0-9_]*` 模式即可。

**Scope 類型（v2 新增）：**

| scope | 說明 | 等效的 runtime 檢查 |
|-------|------|-------------------|
| `all` | 可存取所有該資源的紀錄（預設） | 無額外過濾 |
| `own` | 僅可存取自己建立/擁有的紀錄 | `WHERE created_by = current_user` |
| `department` | 僅可存取同部門的紀錄 | `WHERE department = current_user.department` |
| `team` | 僅可存取同團隊的紀錄 | `WHERE team_id = current_user.team_id` |
| 自訂 | 自訂範圍名稱 | 由實作端定義 |

**範例：**
```yaml
permissions:
  - id: user_read
    resource: users.profile
    action: read
    description: 讀取用戶資料

  # v2: 自訂 action + scope
  - id: order_approve
    resource: orders
    action: approve
    scope: department
    description: 核准同部門的訂單

  # v2: 使用 $self 引用做關係型權限
  - id: order_update_own
    resource: orders.details
    action: update
    scope: own
    conditions:
      - field: order.created_by
        operator: "=="
        value: "$self.id"
    description: 僅能更新自己建立的訂單

  # v2: 使用 time_window 做時間控制
  - id: order_delete_business_hours
    resource: orders
    action: delete
    conditions:
      - time_window:
          start: "09:00"
          end: "18:00"
          timezone: "Asia/Taipei"
          days: [mon, tue, wed, thu, fri]
    description: 僅限營業時間內刪除訂單

  # v2: 使用 context: 前綴做動態屬性
  - id: sensitive_data_read
    resource: users
    action: read
    conditions:
      - field: "context:request.ip_range"
        operator: in
        value: ["10.0.0.0/8", "172.16.0.0/12"]
    description: 僅限內網存取敏感資料
```

### 3.7 AccessControl（存取規則）定義

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| id | String | Y | 規則唯一識別碼 |
| actor | String | **至少一個** | 演員 ID |
| roles | Array | **至少一個** | 角色 ID 清單 |
| permissions | Array | N | 權限 ID 清單 |
| effect | String | Y | allow 或 deny |
| conditions | Array | N | 額外條件約束 |
| priority | Integer | N | 優先級（0 最高） |

> **v2 變更**：`actor` 與 `roles` 至少須填一個（JSON Schema 使用 `oneOf` 約束）。v1 中兩者都是 optional，可能產生無主體的空規則。

**優先級規則：**
- `deny` 規則預設優先於 `allow` 規則
- 相同 effect 時，priority 數字越小優先級越高
- 預設 priority 為 100

**範例：**
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

#### 3.7.1 v3.3：隱式 access_control（Convention over Configuration）

> v3.3 對 PM/SA 進一步減負：若 `role.permissions[]` 列了 permission 但**沒有對應的 access_control 規則**，自動視為一條隱式 allow 規則。

**規則**：

```yaml
roles:
  - id: dept_viewer
    permissions: [user_read, doc_read]   # ← 寫這一次就夠

# 不需要再寫：
# access_control:
#   - id: dept_viewer_allow
#     roles: [dept_viewer]
#     permissions: [user_read, doc_read]
#     effect: allow
#     priority: 100
```

**隱式規則等價於**：

```yaml
- id: <role_id>_implicit_allow      # 自動命名
  roles: [<role_id>]
  permissions: [...]                # 取 role.permissions[] 全集
  effect: allow
  priority: 100                     # v3.3 預設值
```

**何時需要顯式 access_control？**

| 需求 | 必須顯式寫 |
|------|----------|
| `effect: deny` | 是（隱式只生 allow） |
| 額外 `conditions[]`（如 IP 限制） | 是 |
| 非預設 priority（如 priority: 5 蓋過繼承的 deny） | 是 |
| 跨 actor 直接授權（actor 而非 role） | 是 |
| 一條 access_rule 同時授予多個 role | 是 |

**Lint 行為**：

- role 列了 permission 但無對應 access_control → 不報錯（v3.3 起為合法寫法）
- 顯式寫的 access_control 永遠覆蓋隱式（顯式優先；priority 數字較小者贏）
- `haarm-lint --explain-access <role-id>` 印出所有隱式 + 顯式規則的合併結果

**遷移路徑**：v2 規格中既有 `access_control[]` 完全相容；既有專案不必改。新規格可省略隱式可推導的部分。

---

### 3.8 Condition（條件）定義（v2 擴展）

v2 的 Condition 支援兩種形式：

#### 3.8.1 FieldCondition（欄位條件）

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| field | String | Y | 欄位路徑（點號分隔） |
| operator | String | Y | 比較運算子 |
| value | Mixed | Y | 比較值 |

**v2 擴展 — field 前綴：**

| 前綴 | 說明 | 範例 |
|------|------|------|
| （無前綴） | 靜態欄位，對應實體屬性 | `user.department`、`order.status` |
| `context:` | 動態屬性，需 runtime 解析 | `context:request.ip_range`、`context:current_time` |

**v2 擴展 — value 的 `$self` 引用：**

| 語法 | 說明 | 用途 |
|------|------|------|
| `$self.id` | 當前 actor 的 ID | 資料擁有者檢查 |
| `$self.department` | 當前 actor 的部門 | 同部門過濾 |
| `$self.<property>` | 當前 actor 的任意屬性 | 關係型權限 |

**範例：**
```yaml
conditions:
  # 靜態條件（與 v1 相同）
  - field: user.department
    operator: "=="
    value: HR

  # v2: 關係型 — 只能存取自己部門的資料
  - field: record.department
    operator: "=="
    value: "$self.department"

  # v2: 關係型 — 只能管理自己建立的訂單
  - field: order.created_by
    operator: "=="
    value: "$self.id"

  # v2: 動態屬性 — 基於請求來源的 IP 範圍
  - field: "context:request.ip_range"
    operator: in
    value: ["10.0.0.0/8"]

  # v3.3: 前綴比對（部門子樹隔離，取代 v2 約定俗成的 contains）
  - field: deptId
    operator: starts_with
    value: "$self.department_id"

  # v3.3: 後綴比對（上屬部門查詢）
  - field: deptId
    operator: ends_with
    value: "$self.department_id"
```

##### v3.3 運算子語義對照表

| operator | 語義 | SQL 等價式 | value 允許 | 引入版本 |
|----------|------|-----------|-----------|:-------:|
| `==` / `!=` | 相等 / 不等 | `=` / `<>` | 字面值 / `$self.<prop>` | v1 |
| `<` / `>` / `<=` / `>=` | 大小比較 | `< > <= >=` | 數字 / 日期字串 | v1 |
| `in` | 包含於集合 | `IN (...)` | 陣列 | v1 |
| `contains` | **中綴比對**（v3.3 正名） | `LIKE '%substr%'` | 字面字串 / `$self.<prop>` | v1（v3.3 正名） |
| **`starts_with`** | **前綴比對** | `LIKE 'prefix%'` | 字面字串 / `$self.<prop>` | **v3.3 新增** |
| **`ends_with`** | **後綴比對** | `LIKE '%suffix'` | 字面字串 / `$self.<prop>` | **v3.3 新增** |

> **`contains` 語義正名（v3.3）**：
> v2 規格中 `contains` 的方向性未明確；`benchmarks/haARM/0511-dataRights.md` 約定俗成將其視為「前綴比對」（如 `deptId contains $self.department_id` 用於 hyCMS 部門子樹隔離）。**這在 v3.3 起為反模式（見 §9.5 AP-01）**。
> - 部門子樹隔離：請改用 `starts_with`（`deptId starts_with $self.department_id`）
> - 上屬部門查詢：請改用 `ends_with`（`deptId ends_with $self.department_id`）
> - 真正的「子字串包含」：保留 `contains`（如 `description contains 'urgent'`）
>
> **value 規則（Q3 決議）**：`starts_with` / `ends_with` 的 `value` 同時接受字面字串與 `$self.<prop>` 動態引用，與既有 `contains` 一致。

#### 3.8.2 TimeWindowCondition（時間窗口條件，v2 新增）

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| time_window.start | String | Y | 開始時間（HH:MM） |
| time_window.end | String | Y | 結束時間（HH:MM） |
| time_window.timezone | String | N | 時區（預設 UTC） |
| time_window.days | Array | N | 適用星期（mon-sun） |

**設計理由：** v1 中時間控制只能用 `field: request.time, operator: >=, value: 9` 表示，語意不明確且無法表達跨日、時區、星期等複合條件。v2 提供專用的 `time_window` 結構。

**範例：**
```yaml
conditions:
  - time_window:
      start: "09:00"
      end: "18:00"
      timezone: "Asia/Taipei"
      days: [mon, tue, wed, thu, fri]
```

### 3.9 Constraint（約束）定義（v2 擴展）

| 字段 | 類型 | 必需 | 說明 |
|------|------|:----:|------|
| id | String | Y | 約束唯一識別碼 |
| type | String | Y | 約束類型 |
| **rule** | **Object** | **至少一個** | **結構化約束語法（v2 新增，推薦）** |
| expression | String | **至少一個** | Z3 邏輯表達式（進階選項） |
| severity | String | N | 違反嚴重程度 |
| **description** | **String** | **N** | **約束描述（v2 新增）** |

> **v2 變更**：`rule`（結構化）與 `expression`（Z3）至少填一個。推薦使用 `rule`，Z3 `expression` 保留給 `custom` 類型或結構化語法無法表達的複雜邏輯。

**結構化約束語法（v2 新增）：**

| type | rule 格式 | 說明 |
|------|----------|------|
| `mutual_exclusion` | `not_both: [role_a, role_b]` | 兩個角色不能同時指派 |
| `dependency` | `requires: { role_a: role_b }` | role_a 必須先有 role_b |
| `cardinality` | `max_holders: { role_a: N }` | role_a 最多 N 人持有 |
| `custom` | （僅用 expression） | 複雜邏輯用 Z3 表達式 |

**範例（v2 結構化語法 vs v1 Z3 語法）：**
```yaml
constraints:
  # v2 結構化語法（推薦）
  - id: auditor_accountant_exclusion
    type: mutual_exclusion
    rule:
      not_both: [auditor, accountant]
    severity: error
    description: 稽核員與會計不能為同一人（SOX 合規）

  - id: team_lead_requires_manager
    type: dependency
    rule:
      requires:
        team_lead: manager
    severity: error
    description: 團隊領導必須先具備管理者角色

  - id: max_admin_count
    type: cardinality
    rule:
      max_holders:
        admin: 5
    severity: warning
    description: 管理員最多 5 人

  # 複雜邏輯仍可用 Z3（進階）
  - id: complex_governance_rule
    type: custom
    expression: "Implies(hasRole(actor, 'approver'), Not(hasPermission(actor, 'submit')))"
    severity: error
    description: 核准者不能同時擁有提交權限（Maker-Checker）
```

---

### 3.10 Profile 系統（v3.3 新增 — Convention over Configuration 第一段：「慣例 Profile」）

> **設計動機**：v2 規格要求 PM/SA 為每個 resource 手寫 CRUD × 4～6 個 permission 與 access_control 規則，典型企業後台 30~50 個 AP 會膨脹到 3000~5000 行 YAML。Profile 是「預先寫好的常見組合」，讓常見場景一行解決。
>
> **三段式優先序**：預設（無寫=隱含 all/`type: entity` 推 CRUD）→ **慣例 Profile**（本節）→ 明示覆寫（§3.10.3）。

#### 3.10.1 Resource Profile

`resource.profile:` 欄位讓 Resource 一行宣告其「權限模式」，背後自動展開為 N 個 permission。

**v3.3 內建 5 個 Resource profile（Q4 決議）**：

| profile id | 適用場景 | 自動產生的 permissions |
|-----------|---------|---------------------|
| `public_read_only` | 無 deptId 的查表類（如 APcat、CodeMain） | `<r>_read` (scope: all) |
| `dept_isolated_crud` | 有 deptId 的標準後台功能（如 HT002 使用者管理） | CRUD × 4（scope: department_subtree + `deptId starts_with $self.department_id`）+ own × 2（`*_read_self`、`*_update_self`） |
| `owner_only_crud` | 個人資料、購物車 | CRUD × 4（scope: own，搭配 `created_by == $self.id`） |
| `admin_full` | 系統管理類（後台、稽核日誌） | CRUD + `admin`（scope: all） |
| `read_only_dept` | 報表查詢（只讀但要過濾部門） | `<r>_read`（scope: department_subtree） |

> **為何只有 5 個？** Q4 決議「內建越少越好」。Q3 已允許 `$self.<prop>` 動態表達式，混合場景（如 owner+dept 同時生效）優先用 §3.11 欄位推斷而非加 profile 變體。詳見 §3.10.4「何時不該套 Profile」。

**範例**：

```yaml
resources:
  - id: HT002
    name: "使用者管理"
    type: entity
    fields: [userId, userName, email, deptId, ugrpId, inUse]
    profile: dept_isolated_crud   # ← 一行解決，等價於展開後的 6 個 permission
```

**展開後等價於**（runtime / lint `--explain-profile HT002` 印出，不必寫進 YAML）：

```yaml
permissions:
  - id: HT002_read         # ← <resource>_<action> 自動命名（§3.13）
    resource: HT002
    action: read
    scope: department_subtree
    conditions:
      - field: deptId
        operator: starts_with        # v3.3：精確前綴比對
        value: "$self.department_id"
  - id: HT002_create
    resource: HT002
    action: create
    scope: department_subtree
  - id: HT002_update
    resource: HT002
    action: update
    scope: department_subtree
    conditions:
      - field: deptId
        operator: starts_with
        value: "$self.department_id"
  - id: HT002_delete
    resource: HT002
    action: delete
    scope: department_subtree
    conditions:
      - field: deptId
        operator: starts_with
        value: "$self.department_id"
  - id: HT002_read_self    # ← 自己資料免檢查（自動加 _self 後綴）
    resource: HT002
    action: read
    scope: own
    conditions:
      - field: userId
        operator: "=="
        value: "$self.user_id"
  - id: HT002_update_self
    resource: HT002
    action: update
    scope: own
    conditions:
      - field: userId
        operator: "=="
        value: "$self.user_id"
```

#### 3.10.2 Role Profile

`role.profile:` 欄位讓 Role 一行宣告對「該 namespace 所有 profile=X 的 resource 都套 Y 等級」。

**v3.3 內建對映 Role profile**：

| role profile id | 對 Resource 的權限對應 |
|----------------|---------------------|
| `super_admin` | 所有 resource 自動 grant CRUD + admin（scope: all） |
| `dept_owner` | profile=`dept_isolated_crud` 的所有 resource 自動 grant CRUD |
| `dept_viewer` | profile=`dept_isolated_crud`/`read_only_dept` 的所有 resource 自動 grant read |
| `admin_full` | profile=`admin_full` 的所有 resource 自動 grant CRUD + admin |
| `read_only_dept_role` | profile=`read_only_dept` 的所有 resource 自動 grant read |

**範例**：

```yaml
roles:
  - id: HTSD
    name: "HT 系統部門"
    profile: dept_viewer       # ← 對所有 dept_isolated_crud / read_only_dept resource 自動 grant read

  - id: SysAdm
    name: "系統管理員"
    profile: super_admin       # ← 對所有 resource 自動 grant CRUD + admin
```

等價於自動產生 access_control 規則，把該 role 對應的所有 resource 全 hook 上去。runtime / lint `--explain-profile <role-id>` 可印出展開結果。

#### 3.10.3 Profile 覆寫機制（profile_overrides，Q6 合併語意）

避免 profile 變成黑盒，允許 PM/SA 看到展開結果並**局部覆寫**單一 action。

**Q6 決議合併語意（混合策略）**：

| 欄位類型 | 合併規則 | 範例 |
|---------|---------|------|
| scalar（`scope`、`effect`） | **Deep merge**：有寫即取代，無寫即繼承 profile 展開值 | `scope: all` 覆寫，但 `effect` 繼承 |
| object | Deep merge：嵌套物件遞迴合併 | `metadata.foo` 覆寫，`metadata.bar` 繼承 |
| **list（`conditions`、`fields`）** | **完全覆寫**：有 key 就整個 list 取代（沿用 `haPDL/haPDL-page-type-defaults-v3.2.1.md` §九） | 省略 conditions=繼承；寫 `conditions: []` = 明示清空 |

**為何 list 採完全覆寫？** Q6 codegen owner 評估：array deep merge 的「sentinel 區分」（`[]` vs 省略）會把實作成本從 2.5 天推到 5.5~7 天，且 PM/SA 心智負擔倍增。完全覆寫對映 haPDL 既有決策，merge 邏輯複雜度近似方案 A（全取代）。

**範例**：

```yaml
resources:
  - id: HT002
    profile: dept_isolated_crud
    profile_overrides:
      delete:
        scope: all              # ← scalar：覆寫 scope（其他欄位繼承 profile）
        conditions: []          # ← list：明示清空（admin 可全域刪，不受部門限制）
      print:                    # ← 新增 profile 沒有的 action
        scope: department_subtree
```

**強制透明機制（Q6 lint 規則）**：

- `haarm-lint --explain-profile <resource>` 必須能印出最終展開結果（YAML）
- CI 在 PR 偵測到 `profile_overrides` 變更時，自動跑 `--explain-profile` 並把展開結果附在 review
- **合併後 `conditions == []` 但 YAML 中無明示 `conditions: []` 鍵 → lint error**（防止靜默漏權，對應 §9.5 AP-02）
- `profile_overrides` 內出現 profile 不認識的 action（如 `print`）→ 自動視為新增 action，lint info 訊息

#### 3.10.4 何時不該套 Profile

Profile 不是萬靈丹。下列情境用 §3.11 欄位推斷或完全明示更合適：

| 情境 | 不該用 Profile 的理由 | 替代方案 |
|------|-------------------|---------|
| 同時要 owner 又要 dept（混合 scope） | 內建 5 個 profile 沒有 owner+dept 變體（Q4 決議） | 用 §3.11 欄位推斷（偵測 `deptId` + `created_by` 自動套兩條 condition） |
| 跨 resource 的非標準 SoD 規則 | profile 範圍是單一 resource | 寫 `constraints[]`（§3.9 mutual_exclusion） |
| 該專案有超過 10 個 resource 都不套標準 profile | profile 沒帶來簡化 | 在 `.haarm.config.yaml` 設 `defaults.resource_profile: null` 並全部明示 |
| permission 數量本來就只有 1～2 個（如純查詢頁） | profile 展開反而增加噪音 | 直接寫 permissions[]，省略 profile |

---

### 3.11 Field-Presence Inference（欄位推斷，v3.3 新增）

> **設計動機**：即使有 profile，PM/SA 仍要記得標 `profile: dept_isolated_crud`。若 resource 的欄位本身已暗示權限模式（如有 `deptId` 即為部門隔離），編譯器應該自動推斷。
>
> **三段式優先序**：**預設（本節：欄位推斷）** → 慣例 Profile（§3.10）→ 明示覆寫。
>
> **Q5 決議：預設 `auto_infer: false`**——v3.3 開放此機制但**不自動生效**，避免「隱式生效」嚇到 SA。必須在 `.haarm.config.yaml`（§3.12）顯式啟用。

#### 3.11.1 內建推斷規則

| 偵測欄位 | 自動套用的 condition | 對應 hyCMS 行為 |
|---------|-------------------|--------------|
| `deptId` | `field: deptId, operator: starts_with, value: $self.department_id` | 部門前綴樹隔離（v3.3 用精確 `starts_with`，取代 v2 約定俗成的 `contains`） |
| `created_by` 或 `owner_id` | `field: <欄位>, operator: ==, value: $self.id` | 自己建立的資料免檢查 |
| `is_public` 或 `isPublic` | `field: <欄位>, operator: ==, value: true`（OR 條件，與其他 condition 並列） | hyCMS isPublic 群組 |
| `status` 含 `archived`/`deleted` 值 | （無強制預設；lint 提示「可加 `status != 'archived'`」） | 通用軟刪除模式 |

#### 3.11.2 推斷與 profile/明示的優先序

當同一 resource 同時有「欄位推斷套用」與「profile 套用」時：

```
明示 permissions/conditions  >  profile（含 profile_overrides）  >  欄位推斷
（最高優先）                      （次高）                          （兜底）
```

例：
- 若 resource 有 `deptId` 又有 `profile: dept_isolated_crud`，profile 已涵蓋 deptId condition，**欄位推斷不重複套**
- 若 resource 有 `deptId` 但沒 profile，欄位推斷自動加 `starts_with $self.department_id`
- 若 PM 顯式寫了 condition（如 `operator: in`），**完全採用 PM 的寫法，不推斷**

#### 3.11.3 逃生口

```yaml
resources:
  - id: HT002
    fields: [..., deptId, ...]
    auto_infer: false   # ← 此 resource 關閉欄位推斷，退回完全明示模式
```

或在 `.haarm.config.yaml` 全域關閉（§3.12）。

#### 3.11.4 lint 反向追蹤（trace）

當 SA 質疑「為什麼這個使用者看得到那筆資料」，須能用 lint trace 反向印出推斷鏈：

```bash
haarm-lint --trace HT002 HTSD A01B
# 印出：
# Resource HT002: profile=dept_isolated_crud
# Role HTSD: profile=dept_viewer
# 套用規則：HT002_read (scope: department_subtree)
# Condition: deptId starts_with "A01B"  ← 來自 profile dept_isolated_crud 展開
# 適用 actor: HTSD（$self.department_id = "A01B"）
# 結果：A01B、A01B01、A01B02、A01BX 等部門子樹資料可見
```

> **沒有 trace 工具的 convention 是技術債**（沿用 `ccwLog/0512-hyCmcAcs_discuss_Opus.md` 第六節論點 3）。

---

### 3.12 Project-level 配置（`.haarm.config.yaml`，v3.3 新增）

> **設計動機**：避免每個 `.haarm.yaml` 重複寫相同的「全域預設」。仿 `tsconfig.json`、`.prettierrc`、`codegen.config.yaml` 的設計。

#### 3.12.1 檔案位置與命名

```
<project-root>/
├── .haarm.config.yaml         # ← project-level 全域配置（本節）
├── *.haarm.yaml               # 各 namespace 的 haARM 規格
├── benchmarks/
└── ...
```

#### 3.12.2 完整欄位規格

```yaml
# .haarm.config.yaml
version: "1.0"                    # 本配置檔自身的版本

defaults:
  # 全專案預設 Resource profile（無寫 profile 的 resource 都套這個；null 表示無預設）
  resource_profile: dept_isolated_crud

  # 全專案預設 Role profile
  role_profile: null              # null = 無預設

  # 預設欄位名（§3.11 推斷用）
  owner_field: created_by         # 或 created_by / owner_id 等
  dept_field: deptId              # 或 department_id / dept_code 等

  # 全專案 actor 預設帶哪些 properties（要求 .haarm.yaml 的 actor 都帶這些 key）
  actor_properties:
    - id
    - department_id
    - user_id

  # 內網限制等全專案套用的 conditions（自動 AND 進每條 permission）
  global_conditions:
    - field: "context:request.ip_range"
      operator: in
      value: ["10.0.0.0/8"]

  # v3.3：deptId 推斷預設使用 starts_with 而非 contains
  # （Q3 + Q5：為遷移期相容性留旋鈕；新專案應保持 true）
  starts_with_for_dept: true

  # auto_infer 開關（§3.11；Q5 預設關）
  auto_infer:
    enabled: false                # 必須顯式設 true 才啟用欄位推斷
    dept_isolation: true          # 若 enabled=true，個別子項可關
    owner_check: true
    public_flag: false            # is_public 推斷預設關（多數專案無此欄位）
```

#### 3.12.3 優先序（含 `.haarm.config.yaml`）

```
.haarm.yaml 明示 permissions/conditions
   > resource.profile_overrides
   > resource.profile（或 role.profile）
   > resource.auto_infer 個別開關
   > .haarm.config.yaml defaults
   > haARM 內建預設（v3.3 內建 5 profile、5 推斷規則）
```

#### 3.12.4 與既有 codegen.config.yaml 的分工

| 配置檔 | 內容 |
|--------|------|
| `.haarm.config.yaml` | **規格層** convention（profile 預設、欄位推斷、global conditions） |
| `codegen.config.yaml` | **codegen 層** convention（resilience timeout/retry、整合服務端點、Java package 路徑） |

兩者互不重疊。haARM 規格的解讀只看前者；後者只影響產出物（如 Spring Boot 程式碼）。

---

### 3.13 Permission ID 自動命名慣例（v3.3 新增）

> **設計動機**：仿 haAPI 的「`POST /users` 自動推導為 `createUser`」慣例。Profile 與欄位推斷會產生大量 permission，逐個取 ID 是噪音。

#### 3.13.1 命名規則

```
<resource_id>_<action>(_<scope_suffix>)
```

- `<resource_id>` 取 resource id 全字（保留底線，不轉駝峰）
- `<action>` 取 permission action（如 `read`、`create`、`update`、`delete`、`admin`、`approve`）
- `<scope_suffix>`：
  - `scope: own` → 後綴 `_self`（如 `HT002_read_self`）
  - `scope: department` / `department_subtree` → 後綴 `_dept`（避免與 default 衝突；profile 展開時可省略）
  - `scope: team` → 後綴 `_team`
  - `scope: all`（預設）→ 無後綴
  - 自訂 scope → 後綴為該 scope 的 snake_case id

#### 3.13.2 範例

| permission 來源 | 自動 ID |
|---------------|--------|
| resource=`HT002`, action=`read`, scope=`all` | `HT002_read` |
| resource=`HT002`, action=`update`, scope=`own` | `HT002_update_self` |
| resource=`HT002`, action=`read`, scope=`department_subtree` | `HT002_read`（profile 展開時省略 dept 後綴，因為 dept 是該 profile 的預設） |
| resource=`orders`, action=`approve`, scope=`team` | `orders_approve_team` |

#### 3.13.3 衝突處理

- 同 namespace 兩個 permission 自動 ID 撞名 → **lint error**，強制 PM 顯式寫 `id:` 區分
- 顯式 `id:` 永遠優先於自動命名（不會被覆蓋）

#### 3.13.4 何時不該倚賴自動命名

- 跨 namespace 的權限引用：仍應顯式寫 ID 以利搜尋
- 對外公開的 permission（如 OAuth scope）：使用穩定的人工命名
- 遷移期同時保留 hyCMS legacy_bit：建議顯式寫 ID 帶 bit 對照（如 `HT002_create_bit4`）

---

### 3.14 dynamic_grants（v3.3 RC, predefault disabled, v3.4 正式落地）

> **狀態**：v3.3 文件化、**預設 disabled**；schema 接受但 runtime 應忽略；v3.4 完成 ReBAC 實作後解除（Q13 決議）。

#### 設計動機

對映 hyCMS `ctUgrpSet/2/3` 三張內容節點審稿表（見 `ccwLog/0512-hyCmcAcs_discuss_Opus.md` G4）。haARM v2 之前的權限模型是 **type-level**（resource 的型別層級），無法為「每個目錄節點實例 × 每個群組」獨立指派權限。`dynamic_grants` 將 haARM 擴展為 **ReBAC（Relationship-Based Access Control）**，允許 permission 標記為「實例綁定」，由實作端提供一個 grant table 來查 `(actor, resource_instance) → 允許/拒絕`。

#### 語法（v3.3 RC）

```yaml
metadata:
  dynamic_grants:
    enabled: false   # v3.3 必填且 必須 false；v3.4 起可為 true
    table_name: cms_node_grants    # 實作端的 grant table 名稱（runtime 查詢用）

permissions:
  - id: cms_node_submit
    resource: content_nodes
    action: submit
    dynamic_grant: true   # ← 此 permission 為「實例綁定」，runtime 必查 grant table
```

#### 介面契約（給 v3.4 codegen 實作者）

Grant table 預期形狀（runtime 查詢 API）：

| 欄位 | 型別 | 說明 |
|------|------|------|
| `actor_id` | string | 演員 ID |
| `resource_instance_id` | string | resource 實例的主鍵（如目錄節點 ID） |
| `permission_id` | string | haARM permission ID |
| `granted_at` | timestamp | 授權時間（稽核用） |
| `granted_by` | string | 授權者 actor ID |

Runtime 判定流程：
1. 先按 v3.3 既有 access_control 規則計算 type-level 允許/拒絕
2. 若 type-level 允許且 permission.dynamic_grant=true，**再查 grant table**；查無則拒絕
3. 若 type-level 已拒絕，直接拒絕（不查 grant table）

#### 為何 v3.3 不直接落地？

- ReBAC 的稽核、撤銷、繼承語義需獨立 RFC（v3.4 處理）
- v3.3 範圍蔓延風險太高（Q13 決議：v3.3 RC 僅文件化）
- 既有專案可先用 `permission.legacy_bit` + 自訂 access_rule 過渡

#### v3.3 lint 規則

- 若 `metadata.dynamic_grants.enabled: true`，lint 報 error：「dynamic_grants 在 v3.3 預設 disabled，請等候 v3.4」
- 若 permission 有 `dynamic_grant: true` 但 `metadata.dynamic_grants` 未宣告，lint 報 warning

---

## 4. 完整範例：E-Commerce 系統（v2）

```yaml
metadata:
  title: E-Commerce Platform RBAC
  version: 2.0.0
  namespace: com.example.ecommerce.auth
  description: E-Commerce 平臺的角色存取控制模型（v2）

actors:
  - id: customer
    name: Customer User
    type: user
    description: 普通客戶
    properties:
      registration_type: self_service

  - id: admin_user
    name: Administrator
    type: user
    description: 系統管理員
    properties:
      department: IT

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
      - order_read_all
      - order_delete
      - audit_log_read

# v2 新增：資源定義
resources:
  - id: users
    name: 用戶
    type: entity
    fields: [id, name, email, department, role]

  - id: users.profile
    name: 用戶個人資料
    type: collection
    parent: users

  - id: orders
    name: 訂單
    type: entity
    fields: [id, customer_id, merchant_id, amount, status, created_by]

  - id: orders.own
    name: 自己的訂單
    type: collection
    parent: orders

  - id: orders.merchant
    name: 商家訂單
    type: collection
    parent: orders

  - id: products
    name: 產品
    type: entity
    fields: [id, name, price, merchant_id, status]

  - id: cart
    name: 購物車
    type: entity

  - id: audit_log
    name: 稽核日誌
    type: view

permissions:
  - id: order_view_own
    resource: orders.own
    action: read
    scope: own
    description: 客戶可查看自己的訂單

  - id: order_view_merchant
    resource: orders.merchant
    action: read
    scope: own
    conditions:
      - field: order.merchant_id
        operator: "=="
        value: "$self.id"
    description: 商家可查看自己店的訂單

  - id: order_read_all
    resource: orders
    action: read
    scope: all
    description: 管理員可查看所有訂單

  - id: order_delete
    resource: orders
    action: delete
    conditions:
      - time_window:
          start: "09:00"
          end: "18:00"
          timezone: "Asia/Taipei"
          days: [mon, tue, wed, thu, fri]
    description: 僅限營業時間內刪除訂單

  - id: cart_manage
    resource: cart
    action: write
    scope: own
    description: 管理自己的購物車

  - id: product_create
    resource: products
    action: create
    description: 建立新產品

  - id: product_update
    resource: products
    action: update
    scope: own
    conditions:
      - field: product.merchant_id
        operator: "=="
        value: "$self.id"
    description: 商家只能更新自己的產品

  - id: user_read
    resource: users
    action: read
    description: 讀取用戶資料

  - id: user_write
    resource: users
    action: write
    description: 修改用戶資料

  - id: user_delete
    resource: users
    action: delete
    description: 刪除用戶

  - id: audit_log_read
    resource: audit_log
    action: read
    description: 檢視稽核日誌

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
      - order_read_all
      - order_delete
      - audit_log_read
    effect: allow
    priority: 10

  - id: deny_customer_delete
    roles: [customer_role]
    permissions:
      - user_delete
    effect: deny
    priority: 5

constraints:
  # v2: 結構化語法
  - id: merchant_admin_exclusion
    type: mutual_exclusion
    rule:
      not_both: [merchant, admin]
    severity: error
    description: 商家與管理員角色互斥

  - id: max_admin_count
    type: cardinality
    rule:
      max_holders:
        admin: 3
    severity: warning
    description: 管理員最多 3 人
```

---

## 5. 驗證規則

### 5.1 語法驗證

- 所有必需字段必須存在
- 識別碼必須符合 `[a-zA-Z_][a-zA-Z0-9_]*` 模式
- 版本號必須符合 `\d+\.\d+(\.\d+)?` 模式
- 命名空間必須是點號分隔的識別碼
- **v2**：AccessRule 的 `actor` 與 `roles` 至少填一個
- **v2**：Constraint 的 `rule` 與 `expression` 至少填一個
- **v2**：Permission 的 `action` 符合 `[a-zA-Z_][a-zA-Z0-9_]*` 模式（不限於內建類型）
- **v2**：TimeWindowCondition 的 start/end 符合 `HH:MM` 格式

### 5.2 引用驗證

- 所有 actor 引用必須指向存在的 actor ID
- 所有 role 引用必須指向存在的 role ID
- 所有 permission 引用必須指向存在的 permission ID
- **v2**：所有 permission 的 `resource` 引用必須指向存在的 resource ID（或為 `*`）
- **v2**：resource 的 `parent` 引用必須指向存在的 resource ID
- 角色繼承不能形成循環

### 5.3 語義驗證

- 互斥約束不能被任何訪問規則同時滿足
- 依賴約束必須在頒配權限時檢查
- 基數約束不能被超過
- **v2**：使用結構化 `rule` 的約束可直接做靜態分析，不需要 Z3 solver
- **v2**：含 `$self` 引用的 condition，對應 actor 必須定義相應的 property

### 5.4 衝突檢測

- 同一演員的 `allow` 和 `deny` 規則優先級衝突檢查
- 依賴關係中的循環檢測
- 資源路徑衝突檢測
- **v2**：resource 階層中 parent 循環檢測
- **v2**：`$self` 引用的屬性是否存在於 actor 的 properties 中

---

## 6. 檔案格式

### 檔案命名
```
<name>.haarm.yaml
```

### 範例
```
rbac.haarm.yaml
ecommerce-auth.haarm.yaml
system-permissions.haarm.yaml
```

---

## 7. 版本控制

- 遵循 **語義化版本** (SemVer) 規範
- MAJOR.MINOR.PATCH 格式
- 向後兼容性檢查

### v1 → v2 遷移指引

| v1 語法 | v2 對應 | 是否 breaking |
|---------|---------|:------------:|
| permission.resource 直接寫字串 | 改為引用 resources 區段的 ID | Y（需新增 resources 區段） |
| permission.action enum | 仍可使用內建值，另支援自訂 | N（向後相容） |
| AccessRule 無 actor/roles 約束 | 至少填一個 | Y（原先可能有空規則） |
| constraint 僅 expression | 可用 rule 或 expression | N（向後相容） |
| 無 scope | 新增 scope，預設 all | N（向後相容） |
| 無 time_window | 新增 TimeWindowCondition | N（向後相容） |
| 無 $self 引用 | 新增 $self.property 語法 | N（向後相容） |
| 無 context: 前綴 | 新增 context:field 語法 | N（向後相容） |

---

## 8. 工具支援

- **VSCode 擴展**：語法著色、自動補全、即時驗證
- **CLI 工具**：驗證、轉換、生成文檔
- **haarm-lint**：語法驗證 + 引用完整性檢查 + 跨 DSL 引用檢查
- **Z3 整合**（進階）：約束滿足性檢查（僅 `expression` 模式需要）
