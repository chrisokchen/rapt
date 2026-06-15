# 跨 DSL 引用規則 v3.3

本文件定義 DBML → haARM → haAPI → haPDL 之間的引用方向與最低一致性檢查規則（v3.3.0）。

---

## 引用關係圖

```
DBML (資料 SSoT)
  ↓ entity name (case-sensitive)       haARM (存取控制 SSoT)
  ↓                                        ↓ role.id / permission.id
haAPI (後端意圖 SSoT)  ←←←←←←←←←←←←←←←←←←←
  ↓ api: id
haPDL (前端意圖 SSoT)  ←←←←←←←←←←←←←←←←←←← haARM (role.id / permission.id)

高階 Gherkin (行為 SSoT) → 引用 haAPI operation names / haPDL page actions (非技術性)
```

---

## 跨 DSL 引用點一覽表

| 引用方向 | 欄位路徑 | 目標 | 大小寫規則 | 違反後果 |
|---------|---------|------|----------|---------|
| haARM `resource.id` → DBML | DBML `Table <Name>` | 資源對應實體 | case-insensitive | rapt-verify FAIL |
| haARM `resource.fields[]` → DBML | DBML Column 名稱 | 欄位級權限 | 完全一致 | rapt-verify FAIL |
| haAPI `entity:` → DBML | DBML `Table <Name>` | API 對應實體 | **case-sensitive** | rapt-verify FAIL |
| haAPI `access.endpoints.*.required_roles[]` → haARM | haARM `roles[].id` | 端點角色 | 完全一致 | rapt-verify FAIL |
| haAPI `access.endpoints.*.required_permissions[].id` → haARM | haARM `permissions[].id` | 端點權限 | 完全一致 | rapt-verify FAIL |
| haAPI `access.operations.*.required_roles[]` → haARM | haARM `roles[].id` | 操作角色 | 完全一致 | rapt-verify FAIL |
| haAPI `access.conditions[].haarm_constraint` → haARM | haARM `constraints[].id` | 條件 opaque ref | 完全一致 | rapt-verify WARN |
| haPDL `api:` → haAPI | haAPI `api:` 頂層 id | 頁面綁定 API | 完全一致 | rapt-verify FAIL |
| haPDL `entity:` → DBML | DBML `Table <Name>` | 頁面推斷型別 | **case-sensitive** | rapt-verify FAIL |
| haPDL `auth.roles[]` → haARM | haARM `roles[].id` | 頁面角色控制 | 完全一致 | rapt-verify FAIL |
| haPDL `security.permission_refs.*[].id` → haARM | haARM `permissions[].id` | 頁面細粒度權限 | 完全一致 | rapt-verify FAIL |
| 高階 Gherkin `Background: Given I am a <role>` → haARM | haARM `roles[].name` 或 `roles[].id` | 行為場景角色 | case-insensitive | rapt-verify WARN |

---

## 棄用欄位警告（v3.3 → v3.4 移除）

| DSL | 棄用欄位 | 替換欄位 | 嚴重度 |
|-----|---------|---------|-------|
| haAPI | `access.permissions:` (v3.1 dead-letter) | `access.endpoints.*.required_permissions[].id` | ERROR（v3.4 移除）|
| haPDL | `security.permissions:` (v3.1 legacy) | `security.permission_refs.*[].id` | ERROR（v3.4 移除）|

**【強制】** rapt-form-haapi 和 rapt-form-hapdl 產出的 artifact 中，**禁止出現** `access.permissions:` 和 `security.permissions:`。

---

## 最低一致性檢查清單（rapt-verify 執行）

```
□ 每個 haAPI entity: 對應的 DBML Table 存在
□ 每個 haPDL entity: 對應的 DBML Table 存在
□ 每個 haPDL api: 對應的 haAPI api: id 存在
□ haAPI required_roles[] 每個 id 在 haARM roles[] 存在
□ haAPI required_permissions[].id 每個在 haARM permissions[] 存在
□ haPDL auth.roles[] 每個 id 在 haARM roles[] 存在
□ haPDL security.permission_refs.*[].id 每個在 haARM permissions[] 存在
□ haARM resource.id 能對應到 DBML Table（case-insensitive）
□ 無 access.permissions: 或 security.permissions: legacy 欄位
```

---

## haARM Backfill 規則

當 rapt-intent 或 rapt-form-haapi/hapdl 需要使用尚未存在於 haARM 的 role/permission 時：

1. **機械性缺失**（僅缺 id，語意已知）→ DELEGATE to `rapt-reconcile`（backfill mode）
2. **語意不明**（不知道應給哪個 role 哪些 permission）→ CREATE CiC `GAP` 便條，DELEGATE to `rapt-clarify`
3. **任何情況** → `rapt-intent` 本身**禁止直接修改 haARM**
