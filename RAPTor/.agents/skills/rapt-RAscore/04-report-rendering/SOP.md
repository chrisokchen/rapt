# 04 Report Rendering SOP

**目的**：把 scorecard 轉成團隊可讀、可追蹤、可行動的 Markdown 報告。

---

## 步驟 4.1：載入格式

LOAD REF [rapt-RAscore::references/rascore-report-schema.md]

READ：

- `${paths.reports_dir}/rascore-scorecard.yml`
- `${paths.reports_dir}/rascore-scorecard.draft.json`
- `${paths.reports_dir}/rascore-precheck.json`

---

## 步驟 4.2：優先使用 render script

若 `scripts/rascore_render.py` 可用，執行：

```text
RUN: python {skill_dir}/scripts/rascore_render.py \
  --scorecard ${paths.reports_dir}/rascore-scorecard.yml \
  --draft ${paths.reports_dir}/rascore-scorecard.draft.json \
  --precheck ${paths.reports_dir}/rascore-precheck.json \
  --report ${paths.reports_dir}/rascore-report.md \
  --findings-md ${paths.reports_dir}/rascore-findings.md \
  --findings-json ${paths.reports_dir}/rascore-findings.json
```

若 script 失敗，才依本 SOP 手動渲染。

---

## 步驟 4.3：寫總報告

CREATE / UPDATE `${paths.reports_dir}/rascore-report.md`，包含：

- 總分、等級、advisory-only 狀態。
- 七維度平均分與加權分。
- 否決條件是否觸發。
- 前 5 個重要缺口。
- Specification Quality Report。
- Cross-Spec Consistency Report。
- Traceability Report。
- 建議行動。

---

## 步驟 4.4：寫 findings 報告

CREATE / UPDATE `${paths.reports_dir}/rascore-findings.md`。
CREATE / UPDATE `${paths.reports_dir}/rascore-findings.json`。

findings 必須依 severity 排序，且每項包含：

- criterion
- category
- severity
- artifact / location
- issue
- recommendation
- owner_skill
- recommended_action_type（JSON 必填，Markdown 可省略）

owner_skill 建議值：

- `rapt-clarify`
- `rapt-behavior`
- `rapt-modeling`
- `rapt-reconcile`
- `manual-review`

---

## 步驟 4.5：更新 session

UPDATE `.raptor/session.md`，只追加摘要，不覆寫既有內容：

```markdown
## RAscore

- Report: .raptor/reports/rascore-report.md
- Scorecard: .raptor/reports/rascore-scorecard.yml
- Findings JSON: .raptor/reports/rascore-findings.json
- Score: {total} ({grade})
- Advisory only: true
```
