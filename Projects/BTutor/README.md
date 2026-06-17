# Bridge Cognitive Tutor（BTutor）

> AI 驅動、**可診斷、可解釋、可追蹤認知演化**的橋牌認知學習系統。
> MVP 聚焦單一認知 vertical：**Declarer Play 之 Entry Management Tutor（橋引管理教練）**。

本目錄是 BTutor 的**需求分析與規格（SSoT）工作區**，採用 [RAPTor](#raptor-工作流) 需求開發流程產出。
這裡**不含應用程式原始碼**；交付物是一套可作為下游 codegen 權威來源的規格文件。

---

## 願景

讓**中級卡關玩家、青少年橋牌學習者及其教練**，透過可診斷、可解釋的橋牌認知系統，理解「玩家**如何思考**、在**哪個認知環節失敗**」，從而形成**可遷移的橋牌認知（transferable bridge cognition）**，而非死背牌例或 pattern matching。

核心理念：**AI 不替玩家思考，AI 幫助理解玩家如何思考**。
診斷 truth 來自 **Rule Engine + Student Model + Evidence Trace**；LLM 只負責解釋——**不判案，只寫判決書**。
最終定位為 **Bridge Cognitive Operating System**，而非題庫 / chatbot / DDS UI。

---

## 範圍（MVP）

### In-Scope
- **Entry Management Tutor**：entry recognition / preservation / sequencing / unblock / communication planning / delayed cashing
- **Curated Deal Practice**：人工 curated 牌例（首批 10–20 副，LLM 草擬 DSL ＋ 專家審核）
- **Bridge Situation DSL**：第一版支援 Entry Management 的 **Annotation + Diagnosis（A+C）**，含 ontology / rule / mastery model 的 versioning
- **Telemetry（四訊號）**：action trace、timing、hint escalation、reasoning tags
- **Evidence-based Diagnosis**：Rule-based ＋ Probabilistic Student Model（**CDM / DINA-DINO**），產出 hypothesis / confidence / evidence / rule refs 並寫入**可審計 Evidence Log**
- **Graduated Hint System**：Level 0–4，escalation 作為 cognition signal
- **Multi-dimensional Mastery Tracking**：recognition / execution / transfer / retention（partial、probabilistic）
- **Post-Mortem Coaching** 與 **Coach Dashboard**（MVP 首要交付介面）
- **家長認知進展檢視**（唯讀）、**Reproducible Replay**（event-sourced）、**LLM Explanation Layer**

### Out-of-Scope
叫牌 / 防禦教練、多人即時協作、自由對話 AI chat、全自動本體演化、生物特徵遙測、全自動生牌、embedding 優先架構。

### Deferred（未來版本）
Situation Family Generator、latent embedding sidecar、adaptive sequencing、ontology governance 全自動化、gamification。

完整定義見 [`docs/discovery/04-vision-kpi-scope.md`](docs/discovery/04-vision-kpi-scope.md)。

---

## KPI

採 **Cognitive Mastery Metrics**，明確排除 solve rate / streaks / raw DDS accuracy 作為主要指標：

| # | 指標 | 量測方式 |
|---|------|---------|
| 1 | Transfer success | 同一 cognitive structure 變形 family 的正確率 |
| 2 | Misconception reduction | 同類 cognitive failure 再犯率下降幅度 |
| 3 | Hint independence | 達成正解所需最低 hint level 隨時間下降 |
| 4 | Planning sophistication | 提早 planning 行為比例、規劃 horizon |
| 5 | Retention stability | 隔週 / 隔期重測 mastery 維持率 |
| 6 | Diagnosis auditability | 具完整 evidence log 的診斷比例（目標 100%） |

> baseline / target 為 **pilot 後再定量**；MVP 以方向性（趨勢改善）為準。

---

## 目錄結構

```text
BTutor/
├── raw-input/            原始需求材料（PRD、grill 討論、AI 審查意見）
├── docs/
│   ├── discovery/        Phase 1 業務探索摘要（stakeholders / journeys / events / vision）
│   ├── ssot/             Single Source of Truth（人工權威來源）
│   │   ├── dbml/         annotated DBML 資料模型（23 tables）＋ glossary / constraints / seeds
│   │   ├── habdd/        高階 Gherkin feature（9 features / 15 user stories）
│   │   ├── haarm/        haARM 存取控制（RBAC）
│   │   ├── haapi/        haAPI 後端意圖（10 檔）
│   │   └── hapdl/        haPDL 前端意圖（13 檔）
│   ├── generate/         衍生 / preview 產物（openapi / lofi / designbrief；status: deferred）
│   └── reports/          verify / RAscore 等品質報告
├── .raptor/              RAPTor 控制檔（arguments / session / traceability / impact-matrix）
└── .clarify/             釐清 session 暫存與決策紀錄
```

---

## RAPTor 工作流

本專案以 RAPTor skill family 逐階段產出規格，各階段以前一階段為輸入：

| Phase | Skill | 產物 |
|---|---|---|
| 1 — 探索 | `/rapt-discovery` | `docs/discovery/` |
| 1.5 — 行為 | `/rapt-behavior` | `docs/ssot/habdd/` 高階 Gherkin |
| 2 — 建模 | `/rapt-modeling` | `docs/ssot/dbml/`、`docs/ssot/haarm/` |
| 3 — 釐清 | `/rapt-clarify` | `.clarify/` 決策，套回 SSoT（CiC 便條） |
| 4 — 意圖 | `/rapt-intent` | `docs/ssot/haapi/`、`docs/ssot/hapdl/` |
| 5 — 驗證 | `/rapt-verify` | `docs/reports/verify-report.*` |
| — 評分 | `/rapt-RAscore` | `docs/reports/rascore-*` |
| — 預覽 | `/rapt-openapi` `/rapt-lofi` `/rapt-design-brief` | `docs/generate/`（deferred） |

路徑與版本設定的 SSoT 為 [`.raptor/arguments.yml`](.raptor/arguments.yml)；DSL 版本統一為 `3.3.0`。
`generated.status: deferred` — 目前不生成 downstream / preview 產物，待 SSoT 穩定後再逐一啟用。

---

## 現況

| 項目 | 狀態 |
|---|---|
| Verify（Phase 5） | **PASS** ✅ — 完整性 / 一致性 / 可追蹤性 / 覆蓋率四項全綠，0 error |
| 覆蓋率 | must-have 100% / should-have 100% / overall 100% |
| RAscore（advisory） | **95.13 / 100，Grade A**，veto 未觸發 |

詳見 [`docs/reports/verify-report.md`](docs/reports/verify-report.md) 與 [`docs/reports/rascore-report.md`](docs/reports/rascore-report.md)。

規格層 SSoT 已驗證一致，可作為下游 codegen 的權威來源。

---

## 外部依賴（實作階段）

- **DDS（Double Dummy Solver）** — 建議 Bo Haglund DDS library，做合法性 / 路線驗證
- **LLM API** — 建議 Claude API（Haiku / Sonnet）作 explanation layer
- **BridgeRuleEngine** — 獨立的合法出牌 / trick winner / revoke 判定元件
