# 03 Ubiquitous Language SOP

**目的**：建立並維護統一語言（Ubiquitous Language）詞彙表，確保系統術語在 Discovery、Gherkin、DBML、haARM、haAPI、haPDL 間完全一致。

---

## 步驟

### 3.1 COLLECT Terms

從以下 source COLLECT 所有業務術語：

- `${disc_dir}01-stakeholders.md` → actor 名稱
- `${disc_dir}03-event-timeline.md` → Domain Event 名詞
- `${high_gherkin_dir}/*.feature` → Feature/Scenario 名詞
- DBML entity_map → Table/Column 名稱

### 3.2 DERIVE 術語定義

對每個術語：

```
- term: <術語（繁中）>
- english: <英文（PascalCase for Entity, camelCase for field）>
- definition: <業務定義（1-2 句話）>
- usage_examples: [<在哪裡使用>]
- synonyms: [<同義詞，應避免混用>]
- anti_patterns: [<避免使用的錯誤表達>]
- dbml_table: <對應 DBML table，若無則空白>
- dbml_columns: [<對應 DBML columns>]
- legacy_aliases: [<既有系統或舊命名>]
```

若同義詞並存（如「用戶」vs「客戶」），選一個為標準，其餘標為 deprecated。

### 3.3 WRITE `${data_model_dir}glossary.md`

```markdown
# 統一語言詞彙表（Ubiquitous Language Glossary）

> 最後更新：{date}
> 術語數量：{N}

## 業務實體術語

| 術語（繁中）| 英文 | 定義 | 使用位置 |
|-----------|------|------|---------|
| 訂單 | Order | 客戶確認的購買請求 | Feature / DBML / haAPI |
| ...  | ...  | ...  | ...     |

## Canonical Mapping

| term | canonical_english | dbml_table | dbml_columns | gherkin_synonyms | legacy_aliases | notes |
|---|---|---|---|---|---|---|
| 訂單 | Order | Order | orderId,status | 購買請求 | legacy_order |  |

## 欄位/屬性術語

| 術語 | 英文 | 定義 |
|------|------|------|

## 已棄用術語

| 棄用詞 | 替換為 | 原因 |
|--------|-------|------|
```

---

## 術語一致性規則

1. **DBML Table 名稱**必須對應 glossary 中的 English term（PascalCase）
2. **haARM resource.id**用 snake_case 版本的 English term
3. **haAPI entity**用 DBML Table Name（case-sensitive）
4. **高階 Gherkin**用中文術語（與 glossary term 一致）
5. **混用同義詞**是 AP-G08 反模式（rapt-verify 會警告）
6. **legacy 命名**必須出現在 `legacy_aliases`
7. **L2 traceability** 的 `entities` 必須能透過 Canonical Mapping 對應到 DBML table，否則標低信心或建立 CiC
