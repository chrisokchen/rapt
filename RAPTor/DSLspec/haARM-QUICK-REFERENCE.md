# haARM 速查卡 v3.3

> 1 頁 A4 列印；完整規格見 [`haARMdoc.md`](haARMdoc.md)；跨 DSL 整合見 [`CROSS-DSL-GUIDE.md`](CROSS-DSL-GUIDE.md)

## 1. 最小檔案結構

```yaml
metadata: { title, version: "3.3.0", namespace }
actors:        # 演員（人 / 系統 / 服務）
  - id: <lowercase>; name; type: user|service|system|external; enabled?: bool  # v3.3 enabled
roles:         # 角色（被 haAPI/haPDL 引用）
  - id; name; permissions: [...]; profile?; implicit?: bool                    # v3.3 profile/implicit
resources:     # 資源（對應 DBML Table）
  - id; name; type: entity|action|view; fields: [...]
    profile?; allowed_actions?; profile_overrides?; auto_infer?                # v3.3 全新
permissions:   # 權限
  - id; resource; action; scope; conditions?; fields?; legacy_bit?             # v3.3 legacy_bit
access_control: []  # v3.3 §3.7.1 隱式 allow，多數可省略
constraints: []     # SoD / 互斥 / 基數
```

## 2. v3.3 新運算子（§3.8.1）

| operator | 語義 | SQL 等價 |
|----------|------|---------|
| `starts_with` | **前綴**比對 | `LIKE 'prefix%'` |
| `ends_with` | 後綴比對 | `LIKE '%suffix'` |
| `contains` | **中綴**比對（v3.3 正名）| `LIKE '%substr%'` |
| `==` `!=` `<` `>` `<=` `>=` `in` | 既有運算子 | — |

```yaml
conditions:
  - field: deptId
    operator: starts_with        # ← 部門子樹隔離
    value: "$self.department_id"
```

## 3. v3.3 五個內建 Resource Profile（§3.10，Q4）

| profile id | 適用 | 自動展開 |
|-----------|------|---------|
| `public_read_only` | 無 deptId 查表類 | `read` (scope: all) |
| `dept_isolated_crud` | 標準後台（有 deptId）| CRUD × 4 + own × 2 |
| `owner_only_crud` | 個人資料 | CRUD × 4 (scope: own) |
| `admin_full` | 系統管理類 | CRUD + admin (scope: all) |
| `read_only_dept` | 報表查詢 | `read` (scope: department_subtree) |

```yaml
resources:
  - id: documents
    profile: dept_isolated_crud          # 一行展開 6 個 permission
    profile_overrides:                   # Q6：scalar deep merge，conditions 完全覆寫
      delete:
        scope: all
        conditions: []                   # 明示清空（防止 §9.5 AP-02）
```

## 4. 預設 / 慣例 / 明示覆寫（三段式優先序）

```
明示 permissions/conditions  >  profile_overrides  >  profile  >  欄位推斷  >  系統預設
```

`auto_infer` 預設 `false`（Q5）；要啟用須在 `.haarm.config.yaml` 顯式打開。

## 5. v3.3 一級欄位（M1.2）

| 欄位 | 屬於 | 預設 | 用途 |
|------|------|------|------|
| `actor.enabled` | Actor | `true` | 規格層遮罩（Q7）；runtime 拒登由 codegen 端 |
| `role.implicit` | Role | `false` | 所有 actor 自動具備（hyCMS isPublic 對應） |
| `resource.allowed_actions` | Resource | （省略=不限）| UI / lint action 白名單（hyCMS apmask 對應） |
| `permission.legacy_bit` | Permission | （省略）| hyCMS bitmask 遷移期對照 |

## 6. 跨 DSL 引用點（須通過 `validate_cross_dsl.py`）

| 從 | 到 | 必須 |
|----|----|----|
| haARM `resource.id` | DBML `Table <Name>` | case-insensitive 匹配 |
| haARM `resource.fields[]` | DBML Column | 名稱完全一致 |
| haARM `permission.id` ← | haAPI `required_permissions[].id` + haPDL `permission_refs.*[].id` | 引用前 ID 必須存在 |
| haARM `role.id` ← | haAPI `required_roles[]` + haPDL `auth.roles[]` | 同上 |

## 7. 反模式（lint 自動偵測，§9.5）

| 編號 | 反模式 | 修正 |
|------|--------|------|
| AP-01 | `contains` 當前綴比對 | 用 `starts_with` |
| AP-02 | `profile_overrides` 沒寫 `conditions:` 鍵 | 想繼承=省略；想清空=明示 `[]` |
| AP-03 | 同 namespace 多個 `implicit: true` role | 至多 1 個，或用 `parent_roles` 階層 |
| AP-04 | end-user 角色套 `scope: all` | 改用 own/department/team 並加 conditions |
| AP-05 | `enabled: false` 當 runtime 拒登 | 規格層遮罩 + codegen 端拒登 |

## 8. 常用 CLI

```bash
# 跨 DSL 引用驗證（M3 已可用）
python benchmarks/validate_cross_dsl.py <anchor>

# Schema 驗證（M1 驗收用）
node benchmarks/haARM/validate-v33-schema.mjs

# Profile 展開（M4 規劃中）
haarm-lint --explain-profile <resource-id>

# 推斷鏈追蹤（M4 規劃中）
haarm-lint --trace <resource-id> <role-id> <attr>
```

## 9. 最精簡 vs 完整明示寫法（§3.10 對照）

| 寫法 | 行數 | 適用 |
|------|------|------|
| 最精簡（profile + auto_infer）| ~15 行 | PM：套標準場景 |
| 慣例展開後（profile + overrides）| ~30 行 | SA：覆寫特殊 action |
| 完整明示（v2 寫法保留）| ~120 行 | 客製化專家 |

三種寫法可在同一份 YAML 共存。

---
**版本**：v3.3.0｜**對齊**：四 DSL v3.3｜**最後更新**：2026-05-14
