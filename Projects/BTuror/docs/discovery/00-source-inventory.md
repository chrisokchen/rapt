# Source Inventory

> 建立時間：2026-06-16
> 來源數量：4
> 專案：Bridge Cognitive Tutor（MVP：Entry Management Tutor）

## 輸入文件清單

| # | 來源 | 類型 | 核心內容摘要 |
|---|------|------|------------|
| 1 | `raw-input/BTutor_PRD.md` | proposal（PRD v0.1, 2026-05-18） | 產品需求文件。定義願景、問題、MVP 範圍（Declarer Play / Entry Management）、核心 8 大功能、Cognitive Ontology、Situation DSL、Diagnosis、Telemetry、Replay、Coach Dashboard、Success Metrics、長期 moat。 |
| 2 | `raw-input/BridgeTuror-grill.md` | meeting_notes（34 題 `/grill-me` 壓測對話） | 系統設計推演紀錄。逐題逼出 skill unit（cognitive model）、hybrid diagnosis（Rule+Probabilistic+LLM）、Situation IR/DSL、MVP 切刀、telemetry 粒度、mastery 多維表示、mistake taxonomy、transfer validation、replay、ontology governance、長期資產。 |
| 3 | `raw-input/0517-BTutor_discuss_Gemini.md` | meeting_notes（架構審查，Gemini） | 第三方審查。肯定 Deterministic/LLM 切分、Entry Management MVP、Event Sourcing；警示 DSL 編寫成本、Reasoning Tag UX 摩擦、冷啟動、acceptable lines；建議 To-B（教練 co-pilot）、MiniBridge 切入、Paper/CLI→Telemetry→LLM→Dashboard roadmap。 |
| 4 | `raw-input/0517-BTutor_discuss_vscSonnet.md` | meeting_notes（架構審查，Claude Sonnet 4.6） | 第三方審查。肯定 cognitive model 為 skill unit、hybrid diagnosis、Situation IR moat；補強建議：盡早標注 Situation Annotation、Probabilistic model 用 CDM（DINA/DINO）、Ontology 拆 observable indicators、Coach Dashboard 先行、獨立 BridgeRuleEngine（Bo Haglund DDS）、Gamification 延後；建議技術棧 Python/FastAPI/PostgreSQL/Vue + Claude API。 |

## 萃取的關鍵業務概念

1. **Cognitive Diagnosis（認知診斷）**：系統核心不是判定對錯，而是診斷「玩家如何思考、在哪個認知環節失敗」。最小診斷單位是 cognitive model（認知能力），非知識點或答案。
2. **Hybrid Diagnosis Architecture（混合診斷架構）**：Rule Engine 決定 truth（不可妥協）＋ Probabilistic Student Model 管理 uncertainty ＋ LLM 只負責 narration。核心邊界：「LLM 不判案，只寫判決書」。
3. **Bridge Situation DSL / Situation IR（局面中介表示）**：全系統的 cognition intermediate representation 與真正 moat。MVP 先支援 Entry Management 的 Annotation + Diagnosis（A+C），Generation 延後。
4. **Cognitive Ontology（認知本體）**：Entry Management 聚焦 entry recognition / preservation / sequencing / unblock / communication planning / delayed cashing，拆解到可觀測 behavior indicators，分層（Junior → Expert），可演化（AI 提案、人類審核）。
5. **Telemetry & Action Trace（認知遙測）**：MVP 只收四訊號 — action trace（selected_card / legal_cards / think_time_ms / undo_count）、timing、hint escalation、reasoning tags；高訊號密度、不過度工程化。
6. **Evidence-based & Auditable Diagnosis（可審計診斷）**：每次診斷保留 evidence log（hypothesis / confidence / evidence / rule_ids / student_model_delta），可回溯、可給教練 review。
7. **Probabilistic Student Model & Multi-dimensional Mastery（多維 partial mastery）**：mastery 非 binary，拆 recognition / execution / transfer / retention（＋ explanation / low-hint independence），probabilistic evolving state。
8. **Graduated Hint System（漸進式提示）**：Level 0–4，hint escalation 本身即為 cognition signal，用以控制 productive struggle、避免 over-coaching。
9. **Transfer Validation & Situation Family（遷移驗證）**：以「相同底層 cognition、不同表面牌型」測 transfer，防止 pattern memorization / hint farming 作弊；Situation Family Generator 為長期大 moat（MVP 延後生成）。
10. **Reproducible Replay & Versioning（可重現重播）**：Event-Sourced 架構，所有核心 object（ontology / DSL / rule set / mastery model）versioned；replay 用於 Debug / Research / Student History（MVP 單位＝deal session）。
11. **Dual-Layer Tutoring & Coach-centric（學生層＋教練層）**：feedback recipient 為學生本人＋人類教練（A+B），定位 Human Coach Augmentation / B2B2C；Coach Dashboard 建議先於 Student UI（開發者本人即 pilot 教練）。
12. **Long-term Moat（長期護城河）**：Cognitive Ontology + Longitudinal Telemetry + Diagnosis Evidence Graph + Mastery Evolution Trajectories — 最終定位為 Bridge Cognitive Operating System，而非題庫 / chatbot / DDS UI。

<!-- CiC CON #001 RESOLVED -->
**類型**：CON（已裁決，CLR-260616-01#Q1）
**位置**：docs/discovery/00-source-inventory.md#sources
**描述**：Coach Dashboard vs Student UI 何者先做。
**決策**：**Coach Dashboard 先行**（業主本人即 pilot 教練，資料視覺化即可驗證 diagnosis quality）。
**影響**：MVP 實作優先序、haPDL 頁面切分順序
<!-- /CiC -->
