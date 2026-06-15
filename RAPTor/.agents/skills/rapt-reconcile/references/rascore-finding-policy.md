# RAscore Finding Policy

本文件定義 `rapt-reconcile` 如何處理 `rapt-RAscore` 產出的 findings。

## 輸入優先序

1. `${paths.reports_dir}/rascore-findings.json`
2. `${paths.reports_dir}/rascore-findings.md`
3. `${paths.reports_dir}/rascore-scorecard.yml`

JSON 是主要機器讀取格式；Markdown 是 fallback。

## 分類

| 類型 | 定義 | 處理 |
|---|---|---|
| `can-fix` | 有精確來源可機械修復 | 加入 fix plan |
| `need-human` | 需要業務裁決 | 建立 CiC 或委派 `rapt-clarify` |
| `delegate-skill` | 需由 behavior/modeling/intent 重跑或補產物 | 記錄下一步 |
| `skill-gap` | finding 顯示 skill 規則不足 | 記入 skill 改寫 backlog |

## Category 對應

| RAscore category | 預設處理 |
|---|---|
| `cross-spec-gap` | glossary / L2 足夠時 can-fix，否則 need-human 或 delegate modeling |
| `traceability-gap` | 缺引用可 can-fix；source 狀態衝突需 clarify |
| `gherkin-quality` | 替代策略需 clarify；規則性缺口 delegate behavior |
| `dbml-quality` | 值域/constraint 多為 clarify + modeling |
| `coverage-loss` | 先 clarify 是否 in MVP，再 delegate behavior |
| `scope-creep` | clarify |
| `readiness-gap` | delegate verify / intent / behavior |
| `process-gap` | verify missing 提示；編碼問題交 core/manual |

## Can-Fix 前提

- 有明確 source_evidence、decision log、glossary mapping 或 DBML 精確名稱。
- 不涉及新增業務規則。
- 不涉及新增 table / column / Scenario。

## Deny

- 不自動裁決「阻擋或警示」。
- 不自動決定 scope。
- 不用低信心 mapping 補精確 table / field。
