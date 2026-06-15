# RAscore Feedback Policy

RAscore 是 advisory-only 品質評分，不是自動修復器，也不是 phase gate。

## Feedback Loop

```text
rapt-verify
  -> rapt-RAscore
  -> rascore-findings.json / rascore-findings.md
  -> rapt-reconcile
       - can-fix
       - need-human
       - delegate-skill
       - skill-gap
  -> rapt-clarify / rapt-behavior / rapt-modeling / rapt-intent
  -> rapt-verify
  -> rapt-RAscore
```

## 分類原則

| 類型 | 定義 | 處理 |
|---|---|---|
| `can-fix` | 有精確來源可機械修復 | `rapt-reconcile` 可修 |
| `need-human` | 需要業務、範圍、策略或值域裁決 | `rapt-clarify` |
| `delegate-skill` | 需要由某個生成 skill 重跑或補產物 | 建議交對應 skill |
| `skill-gap` | 重複 findings 顯示 skill 規則不足 | 回補 skill SOP / rules |

## 禁止

- 不得讓 RAscore 直接修改 Gherkin、DBML、haAPI、haPDL、haARM 或 generated artifact。
- 不得讓 reconcile 自動裁決業務語意。
- 不得用低信心映射填入精確 traceability。

## RAscore Findings 處理

RAscore findings 應優先輸出 JSON 結構供 `rapt-reconcile` 讀取；Markdown 只作人類報告。
