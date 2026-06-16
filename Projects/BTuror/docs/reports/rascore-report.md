# RAPTor RAscore 評分報告

專案：Bridge Cognitive Tutor
評分模式：LLM-assisted advisory-only

## 總覽

| 項目 | 結果 |
|---|---:|
| RAscore | 95.13 / 100 |
| Raw Grade | A |
| Advisory Grade | A |
| Advisory-only | true |
| Veto | 未觸發 |

## 維度分數

| 維度 | 名稱 | 平均分 | 加權分 |
|---|---|---:|---:|
| A | 需求覆蓋與保真度 | 3.0 / 3 | 20.0 |
| B | Gherkin 行為規格品質 | 2.8 / 3 | 16.8 |
| C | DBML 領域模型品質 | 3.0 / 3 | 14.0 |
| D | Gherkin ↔ DBML 跨規格一致性 | 2.75 / 3 | 22.0 |
| E | 追溯性與決策記錄 | 3.0 / 3 | 14.0 |
| F | 可驗證與生成準備度 | 2.5 / 3 | 5.83 |
| G | 流程穩定性 | 2.5 / 3 | 2.5 |

## Top Findings

1. [RA-B4-001] 部分資料變更 feature（play-session/assignment/graduated-hint）缺個別負向/失敗 scenario。
2. [RA-D3-001] 9 個 DBML table 未直接出現在任何 scenario # entities（identity/infra 或僅由 L3 intent 承接）。
3. [RA-F1-001] 少數 Then 以教學語氣/語用描述，缺可機械斷言的觀察點。

## Precheck 摘要

- glossary mappings: 50
- scenario table candidates: 32
- orphan tables after glossary: 9
- L2 traceability ratio: 1.0

## 建議行動

1. 將 high / medium findings 交由 `rapt-reconcile` 分類。
2. 對 need-human 項目執行 `/rapt-clarify`。
3. 修正後執行 `/rapt-verify`，再重跑 `/rapt-RAscore`。

完整 findings：`.raptor/reports/rascore-findings.md`
機器可讀 findings：`.raptor/reports/rascore-findings.json`
