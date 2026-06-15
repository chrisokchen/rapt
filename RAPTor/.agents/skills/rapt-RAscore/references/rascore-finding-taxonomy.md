# RAscore Finding Taxonomy

findings 必須具體、可定位、可交辦。禁止只寫「品質不足」「需改善」。

| 類別 | 說明 | 常見準則 | 建議 owner_skill |
|---|---|---|---|
| `coverage-loss` | 來源需求流失或未覆蓋 | A1/A2/E1 | `rapt-clarify` |
| `scope-creep` | 無來源新增或腦補 | A3/E2 | `manual-review` |
| `gherkin-quality` | 抽象層級、原子性、GWT、可驗證性問題 | B1-B5/F1 | `rapt-behavior` |
| `dbml-quality` | 實體、關聯、約束、命名問題 | C1-C4 | `rapt-modeling` |
| `cross-spec-gap` | Gherkin 與 DBML 無法互證 | D1-D4 | `rapt-reconcile` |
| `traceability-gap` | 前向或後向追溯斷鏈 | E1-E3 | `rapt-reconcile` |
| `readiness-gap` | 不足以支援測試或後續 DSL | F1-F2 | `rapt-reconcile` |
| `process-gap` | 流程不可重現或評審不可校準 | G1-G2 | `manual-review` |

severity 建議：

- `critical`：觸發否決條件或導致 SSOT 不可信。
- `high`：會造成後續 DSL / 測試 / codegen 明顯錯誤。
- `medium`：局部缺口，需要修正但不破壞整體。
- `low`：命名、格式、信心不足或可延後處理。

