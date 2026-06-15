# 02 Annotated DBML SOP

**目的**：將 entity_map 轉換為 annotated DBML（v3.3），DELEGATE to `rapt-form-dbml` 渲染輸出。

---

## 前提

LOAD REF [rapt-modeling::rules/dbml-v33-annotation-rules.md]
LOAD REF [rapt-modeling::rules/ref-code-and-seed-rules.md]
LOAD REF [rapt-modeling::rules/constraint-modeling-rules.md]
LOAD REF [rapt-modeling::rules/compatibility-modeling-rules.md]

---

## 步驟

### 2.1 DERIVE DBML Table 設計

對每個 Entity（含 Aggregate Root），DERIVE：

```
Table 名稱：PascalCase（與 entity_map.name 一致）
欄位設計：
  - 每個欄位決定 sql_type（nvarchar / int / datetime2 / decimal 等）
  - 每個欄位的 label:（繁中 UI 顯示名稱）
  - 是否 sensitive: true（密碼/電話/email/身分證等）
  - 是否 ref_code:（動態列舉的下拉，引用 CodeMain key）
  - 是否 group:（邏輯分組，如 basic / contact / system）
  - PK、not null、unique、default 等標準屬性
  - 外鍵 Ref: 宣告（用 ref: > 而非 ref_code）
  - ref_code 欄位必須規劃 seeds.md 值域或建立 CiC
  - bitmask / 狀態 / 刪除限制必須規劃 constraints.md 或建立 CiC
  - 反正規化或 legacy 相容欄位必須規劃 compatibility decision 與 compensating rule
Note:（Table 業務說明）
```

### 2.2 VALIDATE 反規則

LOAD REF [rapt-modeling::rules/dbml-v33-annotation-rules.md]

逐一檢查 AP-01 ~ AP-05：
- AP-01：無 `note: 'label:...|group:...'` 嵌入格式
- AP-02：同欄位不同時有 ref_code 和 ref
- AP-03：無顯式 `sensitive: false`
- AP-04：無重複的 group（只寫一次，DBML 或 haPDL 二擇一）
- AP-05：無 UI 偏好（color/icon）在 DBML 中
- R-DBML-07：每個 `ref_code:` 有 `seeds.md` 對應值域或 OPEN CiC
- R-DBML-08：bitmask / 狀態欄位有 `seeds.md` 或 `constraints.md` 支撐
- R-DBML-09：反正規化 / 逗號串列欄位有 compatibility decision 與 compensating rule
- R-DBML-10：legacy 命名在 glossary canonical mapping 中有 alias

### 2.3 DELEGATE `rapt-form-dbml` 渲染

對每個 Table，DELEGATE to `rapt-form-dbml`：

```yaml
payload:
  target_path: "${data_model_dir}schema.dbml"
  source_evidence:
    - type: modeling
      ref: "01-entity-and-aggregate/entity_map#Order"
    - type: discovery
      ref: "${disc_dir}03-event-timeline.md"
  content:
    tables: [<list of table definitions>]
    refs: [<list of Ref declarations>]
  dsl_version: "3.3.0"
  write_mode: create
```

---

## 設計決策原則

| 欄位類型 | 建議 SQL 型別 |
|---------|------------|
| 主鍵（業務 ID）| `nvarchar(60)` 或 `nvarchar(20)` |
| 名稱 / 標題 | `nvarchar(100)` |
| 狀態碼（1碼）| `nchar(1)` |
| 備註 / 描述 | `nvarchar(500)` 或 `nvarchar(max)` |
| 金額 | `decimal(18,2)` |
| 整數計數 | `int` |
| 時間戳記 | `datetime2(0)` |
| 密碼 | `nvarchar(150)` + `sensitive: true` |

若有欄位無法從 source 判斷型別：記 CiC `ASM`。

---

## 支援 artifact

### seeds.md

對所有 `ref_code:`、狀態集合、位元旗標建立規格層值域 SSoT。

```markdown
# Seeds and Value Sets

## AccountStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| InfoUser | accountStatus | A | 啟用 | 帳號可登入與操作 | docs/01-discovery/... | true |
```

### constraints.md

對 DBML 欄位無法完整表示的業務規則建立 constraint catalog。

```markdown
# Domain Constraints

| constraint_id | type | owner_table | owner_field | rule | source | related_scenarios | enforcement |
|---|---|---|---|---|---|---|---|
| CON-AUTH-001 | bitmask | uGrpAP | rights | 修改權限不可在無檢視權限時成立 | docs/04-features/... | SCN-AUTH-004 | haAPI |
```
