# haARM v3.3 Rules

> **版本**：v3.3.0  
> **完整規格**：`RAPTor/DSLspec/haARM-QUICK-REFERENCE.md`、`RAPTor/DSLspec/haARMdoc.md`  
> DSLspec v3.3 takes precedence over this file's examples.

---

## 強制規則（MUST）

### R-ARM-01：v3.3 新運算子正確使用（AP-01）

```yaml
# ✅ 正確：前綴用 starts_with
conditions:
  - field: deptId
    operator: starts_with
    value: "$self.department_id"

# ❌ 錯誤 AP-01：前綴誤用 contains
conditions:
  - field: deptId
    operator: contains     # WRONG: contains 是中綴（LIKE '%x%'）
    value: "$self.department_id"
```

| 運算子 | 正確用途 | SQL 等價 |
|--------|---------|---------|
| `starts_with` | 前綴比對（部門子樹）| `LIKE 'prefix%'` |
| `ends_with` | 後綴比對 | `LIKE '%suffix'` |
| `contains` | 中綴比對（關鍵字搜尋）| `LIKE '%substr%'` |

### R-ARM-02：profile_overrides 必須明示 conditions 鍵（AP-02）

```yaml
# ✅ 正確：明示 conditions: [] 清空
resources:
  - id: documents
    profile: dept_isolated_crud
    profile_overrides:
      delete:
        scope: all
        conditions: []       # 明示清空（不是省略！）

# ❌ 錯誤 AP-02：想清空但省略 conditions 鍵
resources:
  - id: documents
    profile: dept_isolated_crud
    profile_overrides:
      delete:
        scope: all
        # conditions 鍵不存在 → 繼承 profile 的 conditions（非預期）
```

### R-ARM-03：implicit role 最多一個（AP-03）

```yaml
# ✅ 正確：只有一個 implicit: true
roles:
  - id: public
    implicit: true           # 所有 actor 自動具備
  - id: customer
    implicit: false          # 預設可省略
```

### R-ARM-04：end-user role 不用 scope: all（AP-04）

```yaml
# ✅ 正確：end-user 用 own / department / team + conditions
permissions:
  - id: order_read_own
    resource: order
    action: read
    scope: own               # end-user 只能看自己的訂單
    conditions:
      - field: customerId
        operator: eq
        value: "$self.user_id"

# ❌ 錯誤 AP-04：end-user role 用 scope: all
permissions:
  - id: order_read_all
    resource: order
    action: read
    scope: all               # 客戶角色不能看所有人的訂單！
```

### R-ARM-05：enabled: false 只做規格遮罩（AP-05）

```yaml
# ✅ 正確：規格層停用 actor，codegen 端拒絕登入
actors:
  - id: legacy_api
    type: external
    enabled: false           # 表示此 actor 已不在規格中使用

# ❌ 錯誤 AP-05：把 enabled: false 當 runtime 黑名單
# enabled: false 不等於「拒絕此使用者登入」
# runtime 拒登需要 codegen 端實作
```

---

## 五個內建 Resource Profile（v3.3 §3.10）

| Profile ID | 適用情境 | 自動展開的 permissions |
|-----------|---------|---------------------|
| `public_read_only` | 無 deptId 的公開查表 | read (scope: all) |
| `dept_isolated_crud` | 標準後台（有 deptId）| CRUD×4 + own×2 |
| `owner_only_crud` | 個人資料（profile/settings）| CRUD×4 (scope: own) |
| `admin_full` | 系統管理類 | CRUD + admin (scope: all) |
| `read_only_dept` | 報表查詢 | read (scope: department_subtree) |

---

## 跨 DSL 引用要求

```
haARM role.id    ← 必須被 haAPI required_roles[] 和 haPDL auth.roles[] 引用
haARM permission.id ← 必須被 haAPI required_permissions[].id 和 haPDL security.permission_refs.*[].id 引用
haARM resource.id → 必須能對應 DBML Table（case-insensitive）
haARM resource.fields[] → 必須能對應 DBML Column 名稱
haARM constraint.id ← 被 haAPI conditions[].haarm_constraint 引用（opaque ref，WARN 級）
```

---

## auto_infer 規則

- `auto_infer` 預設 **`false`**。
- 需要在 `.haarm.config.yaml` 顯式設定 `auto_infer: true` 才啟用。
- **在本 skill 產出中不使用 auto_infer**（避免不可預測的推斷結果）。
