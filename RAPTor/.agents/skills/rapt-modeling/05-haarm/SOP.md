# 05 haARM SOP

**目的**：從 Stakeholders 和 DBML 建立 haARM（Access Control SSoT v3.3），DELEGATE to `rapt-form-haarm` 渲染輸出。

---

## 前提

LOAD REF [rapt-modeling::rules/haarm-v33-rules.md]  
LOAD REF [rapt-core::dsl-cross-reference-v33.md §haARM Backfill 規則]

---

## 步驟

### 5.1 DERIVE Actors

從 `${disc_dir}01-stakeholders.md` DERIVE haARM actors：

```yaml
actors:
  - id: <stakeholder.id（lowercase-hyphen）>
    name: <stakeholder.name>
    type: <stakeholder.type：user|service|system|external>
    enabled: true           # 預設；若 stakeholder 明確停用才設 false
```

### 5.2 DERIVE Roles

從 Gherkin Background 和 Discovery roles DERIVE：

```yaml
roles:
  - id: <lowercase-hyphen>
    name: <中文名稱>
    permissions: [<permission id 列表，後續步驟填入>]
    profile: <可選：若適用內建 profile>
    implicit: false         # 只有最基礎公開角色才設 true，且最多 1 個
```

**規則**：end-user role 不得有 `scope: all`（AP-04）。

### 5.3 DERIVE Resources

對每個 DBML Table，DERIVE haARM resource：

```yaml
resources:
  - id: <snake_case of Table Name>        # case-insensitive 對應 DBML Table
    name: <中文業務名稱>
    type: entity
    fields: [<需要欄位級權限的 Column 名稱>]
    profile: <選用內建 profile，如 dept_isolated_crud>
    profile_overrides:                     # 僅在需要覆寫 profile 時
      <action>:
        scope: <覆寫 scope>
        conditions: []                     # 明示清空（AP-02 要求）
    auto_infer: false                      # 預設 false，不自動推斷
```

五個內建 Profile 選擇：
- `public_read_only`：無 deptId 的查表類
- `dept_isolated_crud`：標準後台（有 deptId）
- `owner_only_crud`：個人資料
- `admin_full`：系統管理類
- `read_only_dept`：報表查詢

### 5.4 DERIVE Permissions

若不用 profile，或需要 profile 以外的細粒度權限，手動定義：

```yaml
permissions:
  - id: <resource_id>_<action>           # 命名慣例：resource_action
    resource: <resource.id>
    action: list|read|create|update|delete|export|...
    scope: all|own|department|team|department_subtree
    conditions:
      - field: <dbml_column>
        operator: eq|starts_with|ends_with|contains|in
        value: "$self.<field>"
    fields: [<欄位級限制，可選>]
```

### 5.5 VALIDATE 反規則

LOAD REF [rapt-modeling::rules/haarm-v33-rules.md]

檢查 AP-01 ~ AP-05：
- AP-01：`contains` 用對（中綴）不誤當前綴（要用 starts_with）
- AP-02：`profile_overrides` 需明示 `conditions:` 鍵
- AP-03：同 namespace 最多 1 個 `implicit: true` role
- AP-04：end-user role 不用 `scope: all`
- AP-05：`enabled: false` 只做規格遮罩，不當 runtime 拒登

### 5.6 DELEGATE `rapt-form-haarm` 渲染

```yaml
payload:
  target_path: "${access_control_dir}{project_name}.haarm.yaml"
  source_evidence:
    - type: discovery
      ref: "${disc_dir}01-stakeholders.md"
    - type: modeling
      ref: "02-annotated-dbml/schema.dbml"
  content:
    metadata: { title, version: "3.3.0", namespace: <project_name> }
    actors: [...]
    roles: [...]
    resources: [...]
    permissions: [...]
    constraints: []
  dsl_version: "3.3.0"
  write_mode: create
```

---

## haARM Backfill 注意

若後續 `rapt-intent` 需要 haARM 中不存在的 role/permission：  
→ 由 `rapt-reconcile`（機械性）或 `rapt-clarify`（語意性）處理，  
→ **不在本步驟預先猜測**。
