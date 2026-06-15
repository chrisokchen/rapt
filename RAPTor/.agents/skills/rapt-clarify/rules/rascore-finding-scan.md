# RAscore Finding Scan

本規則定義 `rapt-clarify` 如何將 RAscore findings 轉成可回答的 clarification backlog。

## 讀取

若存在，讀取：

- `${paths.reports_dir}/rascore-findings.json`
- `${paths.reports_dir}/rascore-findings.md`
- `${paths.reports_dir}/rascore-scorecard.yml`

## 轉換規則

| finding 類型 | CiC 類型 | 問題 |
|---|---|---|
| coverage-loss / deferred | GAP | 是否納入 MVP？若不納入，deferral 依據是什麼？ |
| scope-creep | BDY / CON | 後續決策是否正式改變 scope？ |
| dbml-quality 值域/constraint | GAP | 代碼值、狀態、bitmask、限制規則為何？ |
| gherkin-quality 替代結果 | CON | 選阻擋還是警示？拒絕刪除還是要求先清除？ |
| traceability source 不同步 | ASM | 是否可依 decision log 回寫 RESOLVED？ |

## Deferred 狀態

每個 deferred 項目只能是：

- `deferred-mvp-out`
- `deferred-needs-decision`
- `accepted-risk`

禁止「討論過但無記錄」。
