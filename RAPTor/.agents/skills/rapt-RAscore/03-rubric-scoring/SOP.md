# 03 Rubric Scoring SOP

**目的**：用 LLM 依 RAscore v0.1 rubric 對 A1-G2 逐準則評分，並用 deterministic script 計算總分。

---

## 步驟 3.1：載入評分規則

LOAD：

- REF [rapt-RAscore::references/rascore-rubric-v01.md]
- REF [rapt-RAscore::references/rascore-llm-judge-prompt.md]
- REF [rapt-RAscore::references/rascore-finding-taxonomy.md]

READ：

- `${paths.reports_dir}/rascore-precheck.json`
- discovery docs
- high-level Gherkin
- DBML
- glossary（若存在）
- traceability（若存在）
- verify report（若存在）

---

## 步驟 3.2：LLM 逐準則評分

對 A1-G2 每條產生：

```json
{
  "score": 0,
  "confidence": "low",
  "review_mode": "llm-assisted",
  "reason": "扣分或給分理由，必須引用 evidence。",
  "evidence": [
    {"artifact": "docs/04-features/order.feature", "location": "Scenario: ...", "note": "..."}
  ],
  "findings": [
    {
      "severity": "high",
      "category": "cross-spec-gap",
      "issue": "...",
      "recommendation": "...",
      "owner_skill": "rapt-modeling"
    }
  ]
}
```

限制：

- 分數只能是 `0`、`1`、`2`、`3`。
- 不要求也不輸出 chain-of-thought；只輸出可稽核的理由、證據與扣分依據。
- 不得用總分掩蓋否決條件。
- 若證據不足，給低信心並列為 finding，不要假裝確定。

---

## 步驟 3.3：寫入 draft JSON

CREATE / UPDATE `${paths.reports_dir}/rascore-scorecard.draft.json`。

draft 必須包含全部 23 個 criteria：

```json
{
  "project": "project-name",
  "rascore_version": "0.1",
  "criteria": {
    "A1": {"score": 2, "confidence": "medium", "reason": "...", "evidence": [], "findings": []},
    "A2": {"score": 2, "confidence": "medium", "reason": "...", "evidence": [], "findings": []}
  }
}
```

---

## 步驟 3.4：計算總分

```
RUN: python {skill_dir}/scripts/rascore_calculate.py \
       --scorecard-draft {paths.reports_dir}/rascore-scorecard.draft.json \
       --output {paths.reports_dir}/rascore-scorecard.yml
```

script 負責：

- 驗證 23 個準則齊全。
- 驗證分數範圍。
- 套用權重。
- 套用否決條件。
- 判定 advisory 等級。

