# Ref Code and Seed Rules

本規則定義 DBML `ref_code:`、狀態集合、代碼值與權限位元的規格層 SSoT。

## seeds.md

`rapt-modeling` 必須在 `${paths.data_model_dir}/seeds.md` 維護可機械解析的值域。

```markdown
# Seeds and Value Sets

## AccountStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| InfoUser | accountStatus | A | 啟用 | 帳號可登入與操作 | docs/01-discovery/... | true |
```

## MUST

- 每個 DBML `ref_code:` 都必須在 `seeds.md` 有對應 section，或有 OPEN CiC。
- bitmask 欄位必須列出 bit / label / meaning。
- 狀態碼必須列出 value / label / meaning。
- 未確認值域不可只寫 Note，必須建立 CiC。

## SSoT 方向

`seeds.md` 是規格層值域 SSoT。未來資料庫 seed script 是 generated artifact，方向只能是 `seeds.md -> generated`。
