# Constraint Modeling Rules

本規則定義 `${paths.data_model_dir}/constraints.md` 的用途與格式。

## constraints.md

用於承載 DBML 欄位型別或 `seeds.md` 無法完整表示的業務規則。

```markdown
# Domain Constraints

| constraint_id | type | owner_table | owner_field | rule | source | related_scenarios | enforcement |
|---|---|---|---|---|---|---|---|
| CON-AUTH-001 | bitmask | uGrpAP | rights | 修改權限不可在無檢視權限時成立 | docs/04-features/... | SCN-AUTH-004 | haAPI |
```

## 應建立 constraint 的情境

- 權限位元組合規則。
- 狀態轉換規則。
- 被引用資料不可刪除。
- 唯一性與跨欄位限制。
- 頻率限制。
- 服務層補償檢查。

## 規則

- `constraint_id` 必須穩定，可被 traceability、haAPI、RAscore 引用。
- 若規則尚未確認，建立 CiC，不得假設。
- `enforcement` 可為 `haAPI`、`haARM`、`manual`、`generated-test`、`unknown`。
