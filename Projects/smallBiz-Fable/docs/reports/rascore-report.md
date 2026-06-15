# RAPTor RAscore 評分報告

專案：smallBiz
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

1. [RA-F1-001] 會員等級門檻金額未定，tier 場景無法量化斷言
2. [RA-B5-001] feature 內 entities 偶用『物流單』『SKU』等同義詞
3. [RA-D3-001] AuditLog/Invoice/Payment/Refund 等支援實體無直接行為場景

## Precheck 摘要

- glossary mappings: 66
- scenario table candidates: 62
- orphan tables after glossary: 9
- L2 traceability ratio: 0.9552

## 建議行動

1. 將 high / medium findings 交由 `rapt-reconcile` 分類。
2. 對 need-human 項目執行 `/rapt-clarify`。
3. 修正後執行 `/rapt-verify`，再重跑 `/rapt-RAscore`。

完整 findings：`.raptor/reports/rascore-findings.md`
機器可讀 findings：`.raptor/reports/rascore-findings.json`
