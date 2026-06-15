# haAPI 格式錨點（Format Anchor）

> ⚠️ **唯一裁決者：`RAPTor/DSLspec/haAPI-specification_v3.3.md` §2.2（exposes）+ §2.3.1（Access v2）**。本文件為快速參考摘要，與 DSLspec 有任何差異時一律以 DSLspec 為準。
> 結構受 `dsl-lint.py`（L2/L3）強制檢查；違規一律 ERROR。

---

## 核心分層（務必理解）

| 區塊 | 負責 | 形狀 |
|------|------|------|
| `exposes` | **能力宣告**：哪些端點存在、path、method | `standard` 陣列 + `operations` 陣列 |
| `access` | **授權**：每個操作的 roles / permissions | `endpoints` **dict** + `operations` **dict**（key=操作名） |

**path / method 只在 `exposes`，`access` 內不得出現 path/methods。**

---

## 最小合法 haAPI 範例（v3.3）

```yaml
api: order
schema_version: "3.3"
entity: Order          # case-sensitive，對應 DBML Table Name
title: 訂單管理 API
description: 訂單的 CRUD + 業務操作

# ── 能力宣告：端點與 path/method 的 SSoT ──
exposes:
  standard: [list, read, create, update]   # 路徑由慣例推導（見下）
  list:
    filters:
      - {field: customerId, operators: [eq]}
      - {field: status, operators: [eq]}
    sorting: {fields: [createdAt], default: createdAt:desc}
    pagination: {style: offset, default_size: 20}
  operations:
    - name: apply_refund
      method: POST
      path: /{id}/apply-refund             # 相對路徑，附加於 base

# ── 授權：dict（key=操作名），只談 roles/permissions ──
access:
  authentication: {type: bearer, required: true}
  endpoints:
    list:
      required_roles: [staff, admin]
      required_permissions:
        - id: order_read
    read:
      required_roles: [staff, admin]
      required_permissions:
        - id: order_read
    create:
      required_roles: [customer, staff]
      required_permissions:
        - id: order_create
    update:
      required_roles: [staff, admin]
      required_permissions:
        - id: order_update
  operations:
    apply_refund:
      required_roles: [customer]
      required_permissions:
        - id: order_refund

source_evidence:
  - "features/order-management.feature#Scenario:瀏覽訂單列表"
  - "schema/shop.dbml#Table:Order"
  - "access-control/shop.haarm.yaml#roles"
```

---

## 路徑推導規約（base = api，不做複數轉換）

下游（haapi2openapi）依此確定性推導 OpenAPI path，**不需在 haAPI 寫 path**：

```
base = api 值（已是 kebab-case；若缺則用 entity 轉 kebab，皆不加複數）
```

| exposes 來源 | path | method |
|-------------|------|--------|
| `standard: list`   | `/{base}`           | GET |
| `standard: create` | `/{base}`           | POST |
| `standard: read`   | `/{base}/{id}`      | GET |
| `standard: update` | `/{base}/{id}`      | PUT |
| `standard: patch`  | `/{base}/{id}`      | PATCH |
| `standard: delete` | `/{base}/{id}`      | DELETE |
| `operations: - <name>`（字串） | `/{base}/{id}/<name>` | POST |
| `operations: - {name, method, path}` | `/{base}` + 相對 `path` | 取 `method` |

> 例：`api: order` → list = `GET /order`、read = `GET /order/{id}`、apply_refund = `POST /order/{id}/apply-refund`。

---

## 禁止格式（dsl-lint 會直接報 ERROR）

```yaml
# ❌ HAAPI-SCHEMA-001：access.endpoints/operations 寫成 array 並夾帶 path/methods
access:
  endpoints:
    - path: /orders        # 禁止！
      methods: [GET, POST]

# ❌ HAAPI-SCHEMA-002：自創頂層 endpoints
endpoints:                 # 禁止！

# ❌ HAAPI-SCHEMA-004：deprecated access.permissions
access:
  permissions: [order_read]   # 禁止！
```

---

## entity: 案例對應表

| DBML Table | haAPI entity: |
|-----------|---------------|
| Order | Order |
| OrderItem | OrderItem |
| CustomerProfile | CustomerProfile |

**規則**：完全照抄 DBML Table Name，不修改大小寫，不加 plural。
