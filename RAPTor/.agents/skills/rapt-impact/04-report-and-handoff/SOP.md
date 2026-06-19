# 04 Report and Handoff SOP

**目的**：建立可稽核、可重入且不污染 SSoT 的影響分析報告。

LOAD REF：

- [rapt-impact::references/impact-report-schema.md]
- [rapt-impact::references/impact-analysis-rules.md]
- [rapt-core::clarify-payload-schema.md]
- [rapt-core::impact-matrix-schema.md]

## 步驟 4.1：配置報告 ID

格式：`IA-YYYYMMDD-NNN`。

規則：

- 掃描 `${paths.impact_dir}` 的同日報告，取下一個序號。
- 若同一 `source_ref` 已有未封存報告，優先更新同一 ID，並將 `revision` 遞增。
- 不得僅因重跑就建立重複報告。
- Markdown 與 YAML 必須使用同一 ID。

## 步驟 4.2：建立 machine-readable YAML

依 `impact-report-schema.md` 寫入 `${paths.impact_dir}/{id}.yml`。

ASSERT：

- `classification.type`、`recommendation.decision` 與 confidence 為合法 enum。
- 每個 affected/update 與 regression risk 都有 evidence 或 low-confidence CiC。
- `proposed_impact_entries` 沒有被寫入 `${paths.impact_matrix_file}`。
- `proposed_cic` 使用 GAP/ASM/BDY/CON。
- verification plan 指定 owner skill 與驗證目標。

## 步驟 4.3：建立 human-readable Markdown

依固定順序寫 `${paths.impact_dir}/{id}.md`：

1. Proposal Summary
2. Evidence Maturity
3. Scope Classification
4. Impact Graph Trace
5. Affected Artifacts
6. Existing Behavior / Regression Risks
7. Data / API / UI / Permission Impact
8. Value Alignment
9. Cost / Risk Summary
10. Verification Plan
11. Decision Recommendation
12. Confidence & Missing Evidence
13. Proposed CiC & Proposed Impact Entries

將 `scope_change`、blocker/high regression 與 low maturity 放在摘要區醒目呈現。

## 步驟 4.4：建立 proposed handoff，不直接套用

- `needs_clarification`：建立符合 clarify payload schema 的 questions，handoff `/rapt-clarify`。
- `accept`：列出 `/rapt-behavior → /rapt-modeling → /rapt-intent → /rapt-verify`；依受影響面增列 `/rapt-openapi`、`/rapt-lofi`。
- `defer`：提出 BDY CiC，交 clarify 將提案納入 Deferred。
- `reject`：提出 BDY/CON CiC，交 clarify 記錄 Out 或拒絕理由。

任何 handoff 都不得在本步修改 scope、SSoT 或 impact-matrix。

## 步驟 4.5：更新 session

只追加一筆摘要，包含：

- report ID 與 source_ref
- classification、recommendation、overall confidence
- affected 計數與最高 regression severity
- 下一個 owner skill
- `advisory-only: true`

不得把完整報告複製進 session。

## 步驟 4.6：EMIT 完成摘要

```text
Impact Analysis 完成（{id}）

提案：{title}（{classification}, confidence: {confidence}）
證據成熟度：{maturity}
受影響：DBML {count}、haBDD {count}、haAPI {count}、haPDL {count}、haARM {count}
最高回歸風險：{severity}
價值對齊：{kpi_refs or 未找到 KPI}（fit: {fit}）
建議：{decision} — {reason}

報告：
- {id}.md
- {id}.yml

下一步：{handoff}
```

