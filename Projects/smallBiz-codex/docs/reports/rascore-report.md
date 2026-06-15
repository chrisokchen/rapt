# RAPTor RAscore 評分報告

專案：SmallBiz 電商管理
評分模式：LLM-assisted advisory-only

## 總覽

| 項目 | 結果 |
|---|---:|
| RAscore | 87.69 / 100 |
| Raw Grade | A |
| Advisory Grade | A |
| Advisory-only | true |
| Veto | 未觸發 |

## 維度分數

| 維度 | 名稱 | 平均分 | 加權分 |
|---|---|---:|---:|
| A | 需求覆蓋與保真度 | 2.67 / 3 | 17.78 |
| B | Gherkin 行為規格品質 | 2.8 / 3 | 16.8 |
| C | DBML 領域模型品質 | 2.75 / 3 | 12.83 |
| D | Gherkin ↔ DBML 跨規格一致性 | 2.5 / 3 | 20.0 |
| E | 追溯性與決策記錄 | 2.67 / 3 | 12.44 |
| F | 可驗證與生成準備度 | 2.5 / 3 | 5.83 |
| G | 流程穩定性 | 2.0 / 3 | 2.0 |

## Top Findings

1. [RA-B5-001] 9 個 scenario 的 L2 mapping 仍為 low confidence，業務詞與資料詞對應尚未完全穩定。
2. [RA-D2-001] 許多舊有 scenario 的 read_tables、write_tables、fields 仍空白，從 scenario 到 DBML 的欄位級可驗證性不足。
3. [RA-A3-001] 部分能力已接近完整產品範圍，尚未在 RAscore 階段重新確認 MVP 優先級。
4. [RA-C4-001] 部分複合規則尚以 constraints 補充，欄位級計算來源與稽核欄位仍可更明確。
5. [RA-E3-001] RAscore precheck 與 verify 的 scenario count 口徑不同，可能造成報告解讀混淆。

## Precheck 摘要

- glossary mappings: 59
- scenario table candidates: 48
- orphan tables after glossary: 7
- L2 traceability ratio: 0.875
- verify 正式口徑：45 個 scenario，L2/L3 traceability 全數通過

## 建議行動

1. 優先處理 2 個 medium findings，補強 L2 mapping 的 table/field evidence。
2. 將 4 個 low findings 納入後續 modeling / process backlog。
3. 修正後可重跑 `/rapt-verify` 與 `/rapt-RAscore` 比較分數變化。

完整 findings：`docs/reports/rascore-findings.md`
機器可讀 findings：`docs/reports/rascore-findings.json`
