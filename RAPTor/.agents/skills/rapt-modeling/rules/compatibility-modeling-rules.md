# Compatibility Modeling Rules

本規則用於 existing-system 或 legacy naming 情境，避免為了相容既有系統而讓模型品質不可審查。

## Compatibility Decisions

若保留反正規化、逗號串列、legacy table name、混合命名風格，必須在 `glossary.md` 或 data model 文件中建立 compatibility decision。

```markdown
## Compatibility Decisions

| item | decision | risk | compensating_rule | source |
|---|---|---|---|---|
| InfoUser.ugrpId | 保留逗號串列 | DBML 無法保證 FK | CON-AUTH-002: haAPI 建立/更新時驗證每個群組存在 | CLR-... |
```

## MUST

- 反正規化欄位必須有 risk 與 compensating rule。
- legacy 名稱必須在 glossary canonical mapping 中有 alias。
- 不可為了美化命名而破壞 source 可追溯性。
- 若相容設計會影響 referential integrity，必須在 `constraints.md` 建立補償規則。
