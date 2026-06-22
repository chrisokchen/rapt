---
name: rapt-RAscore
description: "RAPTor RAscore 需求分析品質評分。讀取 discovery、Gherkin、DBML、glossary、traceability 與 verify report，以 LLM-assisted rubric 產生 advisory-only RAscore、veto、scorecard 與 findings。Use when: /rapt-RAscore、需要評估 Gherkin + DBML 是否可作為 SSoT、Phase 2 後品質評分。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: utility
---

# RAPTor RAscore — 需求分析品質評分

先遵守 rapt-core：

- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::ssot-definition.md]
- LOAD REF [rapt-core::phase-gates.md]
- LOAD REF [rapt-core::cic-note-policy.md]
- LOAD REF [rapt-core::traceability-schema.md]
- LOAD REF [rapt-core::rascore-feedback-policy.md]
- LOAD REF [rapt-core::encoding-policy.md]

## TRIGGER

- 任一 rapt-* skill 執行前需要載入共用 reference 規範時。
- 需要查閱跨 skill 共用的 utility 定義或 schema 時。

## SKIP

- 不直接接手任何會寫入 SSoT artifact 的階段工作。
- 應改用對應的 planner、worker、verifier 或 preview skill。


## PRINCIPLE: Artifact Output Contract（只寫 RAscore reports）
## PRINCIPLE: STRICT SOP
## PRINCIPLE: Advisory-only（不是 phase gate）

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|---|---|---|
| CREATE / UPDATE | `${paths.reports_dir}/rascore-precheck.json` | 靜態預檢 evidence |
| CREATE / UPDATE | `${paths.reports_dir}/rascore-scorecard.draft.json` | LLM 逐準則評分草稿 |
| CREATE / UPDATE | `${paths.reports_dir}/rascore-scorecard.yml` | deterministic scorecard |
| CREATE / UPDATE | `${paths.reports_dir}/rascore-report.md` | 人類可讀總報告 |
| CREATE / UPDATE | `${paths.reports_dir}/rascore-findings.md` | Markdown findings |
| CREATE / UPDATE | `${paths.reports_dir}/rascore-findings.json` | 機器可讀 findings，供 rapt-reconcile 使用 |
| UPDATE | `.raptor/session.md` | 追加 RAscore 摘要 |
| **DENY** | DBML / Gherkin / haARM / haAPI / haPDL | 不修改 SSoT artifact |
| **DENY** | `generated/` | 不產生 downstream artifacts |
| **DENY** | `.raptor/arguments.yml` | 不修改 arguments schema |

---

## SOP

### 步驟 0：READ arguments.yml

```text
READ: .raptor/arguments.yml
ASSERT: 存在，否則 EMIT 錯誤「請先執行 /rapt-kickoff」並停止
ASSERT: 本 skill 為 advisory-only，不阻擋 phase gate
```

### 步驟 1：EXECUTE `01-bind-inputs/SOP.md`

綁定 discovery、Gherkin、DBML、glossary、traceability 與 verify report。

### 步驟 2：EXECUTE `02-static-precheck/SOP.md`

執行 `scripts/rascore_precheck.py`，產生：

- Gherkin 結構 evidence
- DBML 結構 evidence
- glossary-aware mapping evidence
- traceability L2 coverage evidence
- seed / constraint 支撐 evidence（若可掃描）

### 步驟 3：EXECUTE `03-rubric-scoring/SOP.md`

LOAD：

- REF [rapt-RAscore::references/rascore-rubric-v01.md]
- REF [rapt-RAscore::references/rascore-llm-judge-prompt.md]
- REF [rapt-RAscore::references/rascore-finding-taxonomy.md]
- REF [rapt-RAscore::references/rascore-action-map.md]

用 LLM-assisted rubric 對 A1-G2 逐準則評分，寫入 `${paths.reports_dir}/rascore-scorecard.draft.json`。

再執行 `scripts/rascore_calculate.py` 產生 `${paths.reports_dir}/rascore-scorecard.yml`。

### 步驟 4：EXECUTE `04-report-rendering/SOP.md`

優先執行 `scripts/rascore_render.py`：

```text
RUN: python {skill_dir}/scripts/rascore_render.py \
  --scorecard ${paths.reports_dir}/rascore-scorecard.yml \
  --draft ${paths.reports_dir}/rascore-scorecard.draft.json \
  --precheck ${paths.reports_dir}/rascore-precheck.json \
  --report ${paths.reports_dir}/rascore-report.md \
  --findings-md ${paths.reports_dir}/rascore-findings.md \
  --findings-json ${paths.reports_dir}/rascore-findings.json
```

若 render script 不可用，依 `references/rascore-report-schema.md` 手動渲染，但必須維持欄位一致。

### 步驟 5：EMIT 完成摘要

```text
RAscore 完成（advisory-only）
分數：{score.total} / 100（{score.grade}）
Veto：{triggered / 未觸發}

主要 findings：
1. {finding}
2. {finding}
3. {finding}

輸出：
- ${paths.reports_dir}/rascore-report.md
- ${paths.reports_dir}/rascore-scorecard.yml
- ${paths.reports_dir}/rascore-findings.md
- ${paths.reports_dir}/rascore-findings.json
```
