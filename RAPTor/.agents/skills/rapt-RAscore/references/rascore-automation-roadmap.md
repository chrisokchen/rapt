# RAscore Automation Roadmap

## Phase 0：LLM-assisted 評分 MVP

- LLM 依 rubric 逐準則評分。
- script 只做 precheck evidence 與 deterministic 計算。
- advisory-only，不阻擋 phase gate。

## Phase 1：半自動靜態檢查

- Gherkin 語法與 GWT 缺漏。
- Scenario 長度。
- UI / 技術細節洩漏詞。
- DBML Table / Enum / Ref / PK 初篩。
- traceability 檔案存在性與粗略引用掃描。

## Phase 2：Gherkin ↔ DBML 概念對齊

- Gherkin AST 抽取候選名詞、狀態詞、行為動詞。
- DBML parser 抽取 table、column、enum、ref。
- glossary、字串相似度與 embedding 建立 mapping。
- mapping 分為 `ACCEPT`、`REVIEW`、`UNMATCHED`。

## Phase 3：接入後續生成準備度

- 讀取 `rapt-verify` report。
- 評估 haAPI / haPDL / haARM readiness。
- 評估 test generation readiness。
- 評估 change resilience。

