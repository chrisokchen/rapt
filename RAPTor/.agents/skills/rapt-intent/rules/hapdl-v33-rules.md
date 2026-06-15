# haPDL v3.3 規則

本文件定義 `rapt-intent`（和 `rapt-form-hapdl`）在生成 haPDL 時必須遵守的規則。
> 唯一裁決者：`DSLspec/haPDL-specification-v3.3.md` §3.1 + `rapt-core::hapdl-canonical-keys.md`。結構由 `dsl-lint.py` 強制檢查。

---

## 一檔一頁（強制）— 頂層必須是 `page`

```yaml
# ✅ 正確：一個檔案一個頁面，頂層即 page 宣告
page: order-list
type: list
entity: Order
api: order
title: 訂單列表

# ❌ 禁止：meta / pages 多頁打包（HAPDL-SCHEMA-001）
meta:                    # FORBIDDEN
  module: order
pages:                   # FORBIDDEN
  - id: order-list

# ❌ 禁止：用 page_id 取代 page（HAPDL-SCHEMA-002）
page_id: order-list      # FORBIDDEN（正式鍵為 page）
```

---

## security.permission_refs 格式（強制）

haPDL v3.3 的 security 欄位：

```yaml
# ✅ 正確：permission_refs 格式
security:
  permission_refs:
    view:
      - {id: order_read}
    create:
      - {id: order_create}
    update:
      - {id: order_update}
  datasource_scope: own   # own | department | all

# ❌ 禁止：legacy security.permissions（已 deprecated）
security:
  permissions:          # FORBIDDEN
    - order_read
```

---

## api: 引用規則（強制）

haPDL 中的 `api:` 欄位必須對應 haAPI 的 `api:` 頂層 id：

```yaml
# ✅ 正確
api: order   # 對應 order.haapi.yaml 中的 api: order

# ❌ 錯誤
api: orders  # haAPI 中的 api: 是 order，不是 orders
api: /api/v1/orders  # 不使用 URL 路徑
```

---

## 規則表

| ID | 規則 | 嚴重度 | 反例 |
|----|------|-------|------|
| R-PDL-01 | `entity:` 值必須 case-sensitive 對應 DBML Table Name | ERROR | `entity: order`（Table 是 `Order`）|
| R-PDL-02 | `security.permissions:` 已 deprecated，禁止使用 | ERROR | `security.permissions: [order_read]` |
| R-PDL-03 | `api:` 值必須對應實際 haAPI 的 `api:` id | ERROR | `api: order-management`（haAPI 是 `order`）|
| R-PDL-04 | `security.permission_refs.{action}[].id` 必須在 haARM 存在 | ERROR | permission `order_approve` 未在 haARM 定義 |
| R-PDL-05 | `schema_version` 必須是 `"3.3"` | ERROR | `schema_version: "3.2"` |
| R-PDL-06 | end-user role 的 `datasource_scope` 不得為 `all` | ERROR | customer 頁面設定 `datasource_scope: all` |
| R-PDL-07 | 表單欄位必須有中文 `label:` | WARNING | `- field: status`（無 label）|
| R-PDL-08 | 一檔一頁：頂層 key 必須是 `page`；禁止 `meta`/`pages`/`page_id` 包裝 | ERROR | `meta:` + `pages:` 打包多頁於單檔 |

---

## AP（反模式）

| AP | 描述 | ✅ 改用 |
|----|------|---------|
| AP-PDL-01 | 在 haPDL 中直接寫入業務邏輯（if/else）| 業務邏輯屬 haAPI 層，haPDL 只描述顯示意圖 |
| AP-PDL-02 | `entity:` 使用 plural | 對應 DBML Table（通常 singular）|
| AP-PDL-03 | `api:` 填入完整 URL 路徑 | 使用 haAPI 的 logical id |

---

## datasource_scope 語意

| 值 | 意思 |
|----|------|
| `own` | 只能看自己的資料 |
| `department` | 可以看同部門/組織的資料 |
| `all` | 可以看全系統的資料（僅 admin/system）|
