# haPDL 速查卡 v3.3

> 1 頁 A4 列印；完整規格見 [`haPDLdoc.md`](haPDLdoc.md)；跨 DSL 整合見 [`CROSS-DSL-GUIDE.md`](CROSS-DSL-GUIDE.md)

## 1. 最小檔案結構

```yaml
page: <kebab-case-id>
type: list|form|detail|dashboard|wizard
title: <人類可讀名稱>
entity: <DBML Table>         # 推斷型別/標籤
api: <haAPI api: id>         # 跨 DSL 引用點，須匹配 haAPI
schema_version: "3.3.0"

view:
  filters: [...]    # list 用
  columns: [...]    # list 用
  fields: [...]     # form 用
  features: { pagination, sortable, searchable }

actions:
  standard: [create, edit, delete, export]   # sugar 自動展開
  operations: [export]                       # 引用 haAPI operation
  custom: []
  placement: { header, row, batch }

auth:
  roles: [...]      # 引用 haARM role.id

security:
  permission_refs: { view, create, edit, delete }   # v3.3 雙軌
  datasource_scope: all|own|department|team         # v3.3 對齊 haARM scope
```

## 2. 五種頁面類型（type）

| type | 用途 | 典型欄位 |
|------|------|---------|
| `list` | 表格瀏覽 | filters / columns / pagination / actions |
| `form` | 建立/編輯 | fields / validation / layout |
| `detail` | 唯讀檢視 | sections / relations |
| `dashboard` | 儀表板 | widgets / charts / KPIs |
| `wizard` | 多步驟流程 | steps / progress / navigation |

## 3. 欄位符號（最精簡寫法）

| 符號 | 語義 | 範例 → 展開 |
|------|------|------------|
| `!` | 重要 / required | `name!` → `required=true (form), emphasis=true (list)` |
| `?` | optional | `description?` → `optional=true` |
| `#` | readonly | `id#` |
| `*` | sensitive | `password*` → 自動遮罩 |
| `@` | email 格式 | `email@` |
| `[]` | array / multi-select | `tags[]` |
| `:type` | 顯示型別 | `status:badge`、`avatar:image` |
| `\|format` | formatter | `created_at\|date` |
| `~` | 模糊搜尋 | `name~` (filter) |
| `=` | 精確匹配 | `status=` (filter) |
| `^` | 可排序 | `created_at^` (columns) |

## 4. v3.3 雙軌權限結構

```yaml
auth:
  roles: [htsd, sysadm, audit]           # 粗粒度（引用 haARM role.id）

security:
  permission_refs:                       # 細粒度（引用 haARM permission.id）
    view:   [{id: infouser_read}]
    create: [{id: infouser_create}]
    edit:   [{id: infouser_update}]
    delete: [{id: infouser_delete}]
  datasource_scope: department           # SQL 過濾語意（codegen 翻譯為 WHERE）
```

> **棄用警告**：`security.permissions:` （v3.1 legacy）將於 v3.4 移除。

## 5. Convention 三層 defaults

```
明示寫的 fields/columns/actions  >  template extends  >  standard 展開
   >  type 預設  >  DBML 推斷（label/group/sensitive）  >  系統 fallback
```

`type: list` 預設 → `haPDL2PDL/src/defaults/list.defaults.yaml`
`type: form` 預設 → `haPDL2PDL/src/defaults/form.defaults.yaml`
全 type 共用 → `haPDL2PDL/src/defaults/global.defaults.yaml`

> **Q6 一致性**：與 haARM `profile_overrides` 同樣採「scalar deep merge + 陣列完全覆寫」。

## 6. actions.standard 自動展開（type: form）

```yaml
actions:
  standard: [create]      # → 自動展開為 submit + cancel + reset 三按鈕
  standard: [update]      # → submit + cancel + delete + reset
```

詳細展開規則見 `haPDL/haPDL-page-type-defaults-v3.2.1.md` §九。

## 7. 跨 DSL 引用點

| 從 | 到 | 用途 |
|----|----|------|
| haPDL `api:` | haAPI `api:` 頂層 | 頁面綁定 API（Rule 5）|
| haPDL `auth.roles[]` | haARM `roles[].id` | 頁面角色（Rule 6）|
| haPDL `security.permission_refs.*[].id` | haARM `permissions[].id` | 細粒度權限 |
| haPDL `entity:` | DBML `Table <Name>` | 推斷型別（透過 haAPI 中介）|

## 8. 反模式（§20.5）

| 編號 | 反模式 | 修正 |
|------|--------|------|
| AP-01 | 新規格用 `security.permissions:` | 改用 `security.permission_refs.{view\|create\|edit\|delete}[].id` |
| AP-02 | deptId 過濾寫在 `datasource.query` | 用 `security.datasource_scope: department` |
| AP-03 | `actions.standard: [create]` 與自訂同名 action 衝突 | 重命名 custom action |
| AP-04 | 顯示型別硬編在 columns | 用 DBML 一級標註（label/group/sensitive），haPDL 只覆寫例外 |
| AP-05 | `auth.roles:` 寫 haARM 未定義的 role | 提交前跑 `validate_cross_dsl.py` |

## 9. 常用 CLI

```bash
# haPDL → PDL 轉換
hapdl convert <file>.hapdl.yaml --dbml schema.dbml -o output.pdl.yaml

# 驗證
hapdl validate <file>.hapdl.yaml
hapdl-lint <file>.hapdl.yaml

# 跨 DSL 引用驗證
python benchmarks/validate_cross_dsl.py <anchor>
```

## 10. 最精簡 list 頁範例

```yaml
page: user-list
type: list
title: 使用者管理
entity: InfoUser
api: info-user

view:
  filters: [name~, email@, status=]
  columns: [id, name!, email, status:badge, created_at|date]
  features: { pagination: 20, sortable: [name, created_at] }

actions:
  standard: [create, edit, delete, export]

auth: { roles: [admin, manager] }
```

---
**版本**：v3.3.0｜**對齊**：四 DSL v3.3｜**最後更新**：2026-05-14
