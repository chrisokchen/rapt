# haPDL 正式鍵名裁決（Canonical Keys）v3.3

> 本文件為 `dsl-lint` L2 schema、L3 lint、以及三支 preview 腳本欄位審計的**唯一鍵名來源**。
> 裁決依據：`DSLspec/haPDL-specification-v3.3.md` §3.1/§8、`DSLspec/haPDL-QUICK-REFERENCE.md`、`rapt-form-hapdl/references/hapdl-format-anchor.md`、`rapt-intent/rules/hapdl-v33-rules.md`、`rapt-core/references/dsl-cross-reference-v33.md`。
> 裁決日期：2026-06-06。

---

## 裁決摘要

format-anchor、quick-reference、rules、cross-reference **四份文件對鍵名完全一致**；唯一偏離者是 preview 腳本（`hapdl2lofi.py` / `hapdl2brief.py` 使用 `page_id`/`auth_roles`/`primary_actor` 等規格不存在的鍵）。**故以四份文件的一致詞彙為正式鍵名，腳本為待修正的 outlier。**

---

## 正式鍵名表

### 頂層（required）

| 鍵 | 型別 | 說明 |
|----|------|------|
| `page` | string (kebab-case) | 頁面識別碼。**非** `page_id`、**非** `pages[].id` |
| `type` | enum: `list` \| `form` \| `detail` \| `dashboard` \| `wizard` | 頁面類型 |
| `title` | string | 人類可讀標題 |
| `entity` | string (case-sensitive) | 對應 DBML Table Name |
| `api` | string | 對應 haAPI 頂層 `api:` logical id |
| `schema_version` | string | 接受 `3.3` 或 `3.3.x` |

### 頂層（forbidden）

| 鍵 | 原因 |
|----|------|
| `meta` | 多頁打包包裝，禁止（一檔一頁） |
| `pages` | 多頁打包包裝，禁止 |
| `page_id` | 腳本 outlier，正式鍵為 `page` |

### view（list/detail 用）

| 鍵 | 說明 |
|----|------|
| `view.filters[]` | `{field, label, type, ref_code?}` |
| `view.columns[]` | `{field, label, link?, format?, ref_code?, sortable?}` |
| `view.fields[]` | form 也可用 `form.fields`（見下） |
| `view.features` | `{pagination, sortable, searchable}` |

> ❌ 禁止 outlier 鍵：`layout`、`filter_bar`、`activity_cards`（TEST 自創）。一律改 `view.*`。

### form（form 用）

| 鍵 | 說明 |
|----|------|
| `form.mode` | `create` \| `edit` |
| `form.fields[]` | `{field, label, type, required?, readonly?, ref_code?}` |

### actions

| 鍵 | 說明 |
|----|------|
| `actions.standard[]` | sugar，CRUD 動作 |
| `actions.operations[]` | 引用 haAPI operation 名 |
| `actions.custom[]` | 自訂動作 |
| `actions.placement` | `{header, row, batch}` |
| `actions.submit` / `actions.cancel` | form 頁專用 |

### 權限（雙軌）

| 鍵 | 角色 | 跨 DSL 目標 |
|----|------|-------------|
| `auth.roles[]` | 粗粒度 | haARM `roles[].id`（**非** `auth_roles`、**非** `primary_actor`） |
| `security.permission_refs.{action}[].id` | 細粒度 | haARM `permissions[].id`；action ∈ `{view, create, edit, update, delete, submit}` |
| `security.datasource_scope` | 資料範圍 | `own` \| `department` \| `team` \| `all` |

### 權限（forbidden）

| 鍵 | 原因 |
|----|------|
| `security.permissions` | v3.1 legacy，禁止（改 `permission_refs`） |

### 其他可選頂層（spec §3.1）
`extends`、`mixins`、`version`、`state`、`error_handling`、`async`、`accessibility`、`testing`、`advanced`、`source_evidence`。`security` 亦可含 §8 的 `field_level` / `data_isolation` / `audit` 等子塊（與 `permission_refs` 並存）。

---

## 腳本 outlier 對照（Phase 5 欄位審計依據）

| 腳本現用鍵（錯） | 正式鍵 | 出現位置 |
|-----------------|--------|---------|
| `page.get("page_id")` | `page` | hapdl2lofi.py / hapdl2brief.py |
| `page.get("auth_roles")` | `auth.roles` | 同上 |
| `page.get("primary_actor")` | （無正式對應；改由 `auth.roles` 推導 actor label 或移除） | 同上 |
| `layout` / `filter_bar` / `activity_cards`（TEST 生成） | `view.filters` / `view.columns` | TEST 檔案（將重生成） |

---

## 附帶 spec 文件待補（不阻塞）
`haPDL-specification-v3.3.md` §3.1 的頂層 skeleton 未列 `auth:`，但 quick-ref/anchor/rules/cross-ref 均使用 `auth.roles`。建議在 §3.1 skeleton 補一行 `auth: { roles: [...] }` 以消除文件間落差（屬文件補強，非結構變更）。
