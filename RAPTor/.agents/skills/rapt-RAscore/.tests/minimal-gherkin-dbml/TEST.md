# minimal-gherkin-dbml

目的：驗證 `rapt-RAscore` 可以讀取最小 RAPTor artifact，產出 precheck evidence，並用 scorecard draft 計算 advisory scorecard。

## 驗收

1. `rascore_precheck.py` 可產生 `rascore-precheck.json`。
2. precheck 可偵測 Gherkin UI 操作詞。
3. precheck 可列出 DBML table 與 orphan table 初篩。
4. `rascore_calculate.py` 可將 23 準則 draft 轉成 `rascore-scorecard.yml`。
5. 若 draft 觸發 `D2 = 0`，輸出 veto 且 advisory grade 最高為 C。

