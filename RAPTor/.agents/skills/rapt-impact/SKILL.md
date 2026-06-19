---
name: rapt-impact
description: "RAPTor 新功能與變更的事前影響分析。讀取 what-if 提案、行內需求或指定 SSoT 路徑，唯讀遍歷 DBML、haBDD、haARM、haAPI、haPDL 與 traceability，產出受影響 artifact、既有行為回歸風險、價值對齊、驗證計畫，以及 accept/defer/reject/needs_clarification 建議。Use when: /rapt-impact、brownfield 新功能加入前評估、scope-creep 裁決、clarify 選項可能改變 scope，或需要回答變更會牽動哪些規格。Advisory-only，不修改 SSoT 或 impact-matrix。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: utility
---

# RAPTor Impact — 變更事前影響分析

先遵守 rapt-core：

- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::ssot-definition.md]
- LOAD REF [rapt-core::dsl-cross-reference-v33.md]
- LOAD REF [rapt-core::traceability-schema.md]
- LOAD REF [rapt-core::impact-matrix-schema.md]
- LOAD REF [rapt-core::finding-taxonomy.md]
- LOAD REF [rapt-core::cic-note-policy.md]
- LOAD REF [rapt-core::clarify-payload-schema.md]
- LOAD REF [rapt-modeling::rules/compatibility-modeling-rules.md]

## PRINCIPLE

- **Artifact Output Contract**：只建立 impact report 並更新 session 摘要。
- **STRICT SOP**：依序執行四個 sub-SOP，不跳步。
- **Advisory-only**：輸出是決策建議，不是 phase gate 或自動裁決。
- **Evidence-or-CiC**：每個影響項目必須有 evidence；只有推斷時標 `confidence: low` 並提出 CiC。
- **No-SSoT-mutation**：不修改任何 SSoT、generated artifact、arguments 或 impact-matrix。
- **Maturity-adaptive**：L2/L3 不完整時降級分析，不得假裝具備 deterministic evidence。

## TRIGGER

- 使用者執行 `/rapt-impact` 或明確指定本 skill。
- 評估新增功能、需求變更、資料模型調整、API/UI/權限改動會影響哪些既有規格。
- `rapt-RAscore` 或 `rapt-verify` 發現 `scope-creep`，需要決定是否納入。
- `rapt-clarify` 的候選決策可能造成 scope add、scope extension 或 scope change。
- brownfield / existing 專案帶著新提案重新進入 RAPTor 流程。

## SKIP

- greenfield 且尚無任何 DBML 或 haBDD：EMIT 無既有系統可分析，建議 `/rapt-discovery`。
- 只需驗證或修復既有規格：改用 `/rapt-verify` 或 `/rapt-reconcile`。
- 問題只存在於 generated artifact 且不涉及規格語意：交給對應 generator/preview skill。
- `.raptor/arguments.yml` 不存在：停止並建議 `/rapt-kickoff`。

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|---|---|---|
| READ | `${paths.whatif_dir}/**` | 提案輸入；fallback 為 `whatif/` |
| READ | `${paths.ssot_dir}/**` | DBML、haBDD、haARM、haAPI、haPDL |
| READ | `${paths.traceability_file}` | L1/L2/L3 與 decision traceability |
| READ | `${paths.impact_matrix_file}` | 僅作既有變更傳播 context |
| READ | `${paths.discovery_dir}/04-vision-kpi-scope.md` | KPI 與 In/Out/Deferred 邊界 |
| EXECUTE（可選） | `rapt-impact::scripts/extract_impact_graph.py` | 建立 deterministic edge-list |
| CREATE / UPDATE | `${paths.impact_dir}/impact-graph-YYYYMMDD.json` | extractor 中間產物（同日快取、可稽核、跨 skill 複用） |
| CREATE / UPDATE | `${paths.impact_dir}/IA-YYYYMMDD-NNN.md` | 人類可讀報告 |
| CREATE / UPDATE | `${paths.impact_dir}/IA-YYYYMMDD-NNN.yml` | 機器可讀報告 |
| UPDATE | `.raptor/session.md` | 追加一筆 impact 摘要 |
| **DENY** | `${paths.ssot_dir}/**` | 不修改 SSoT |
| **DENY** | `${paths.impact_matrix_file}` | 只輸出 `proposed_impact_entries` |
| **DENY** | `${generated.generated_dir}/**` | 不產生或修改 generated artifact |
| **DENY** | `.raptor/arguments.yml` | 不修改路徑或專案設定 |

路徑相容 fallback：

- `${paths.whatif_dir}` 缺少時使用 `whatif/`。
- `${paths.impact_dir}` 缺少時使用 `${paths.reports_dir}/impact/`。
- `project.mode` 可接受 `brownfield` 或既有 schema 的 `existing`；其他值不得自行改寫。

## INPUT

依優先序綁定一種提案來源：

1. 使用者指定的 `${paths.whatif_dir}/<file>` 或提案路徑。
2. 使用者本次行內自然語言描述。
3. 使用者指定的既有 SSoT 檔案，分析其潛在改動傳播。

另讀取 arguments、SSoT、traceability、scope/KPI、glossary、constraints，以及存在時的 impact-matrix、verify report 與 RAscore findings。

## SOP

### 步驟 0：建立執行清單

以內部 TODO 追蹤下列四項，完成一項才標記一項：

1. 綁定環境與提案。
2. 建立證據圖譜。
3. 分析 scope、影響、風險與價值。
4. 渲染報告、更新 session 並交接。

### 步驟 1：EXECUTE `01-bind-and-ingest/SOP.md`

解析 arguments、確認前置條件、標準化提案，建立 entity/action 種子與輸入索引。

### 步驟 2：EXECUTE `02-build-impact-graph/SOP.md`

優先執行 `scripts/extract_impact_graph.py`；腳本不可用時直接讀 SSoT 建圖。所有邊必須附 evidence 與 confidence。

### 步驟 3：EXECUTE `03-assess-and-decide/SOP.md`

遍歷受影響集合，評估既有 scenario 回歸、scope、價值、成本與風險，產生唯一 recommendation。

### 步驟 4：EXECUTE `04-report-and-handoff/SOP.md`

LOAD REF：

- [rapt-impact::references/impact-analysis-rules.md]
- [rapt-impact::references/impact-report-schema.md]

建立成對的 `.md`/`.yml` 報告，只在報告內提出 CiC 與 impact entries，更新 session，輸出下一步。

## Failure Contract

- 找不到 arguments：不建立報告，建議 `/rapt-kickoff`。
- 找不到 DBML 與 haBDD：不建立假影響清單，建議 `/rapt-discovery`。
- 提案無法萃取 entity/action：仍建立報告，分類 `unclear`，建議 `needs_clarification`。
- deterministic 證據不足：繼續分析，但降低 maturity/confidence，所有低信心項目提出 GAP/ASM。
- 報告 schema 驗證失敗：不得宣告完成；修正 `.yml` 與 `.md` 一致性後再 EMIT。

