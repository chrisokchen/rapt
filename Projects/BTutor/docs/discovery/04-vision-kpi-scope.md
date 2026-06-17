# Vision, KPI & Scope

> 來源：BTutor_PRD.md §2 / §4 / §5 / §6 / §18 / §19 / §20、BridgeTuror-grill.md Q1 / Q8 / Q11 / Q24、0517-BTutor_discuss_Gemini.md（風險與 roadmap）、0517-BTutor_discuss_vscSonnet.md（技術建議）

## Vision

> 本系統讓**中級卡關玩家與青少年橋牌學習者及其教練**，能夠透過**可診斷、可解釋、可追蹤認知演化**的橋牌認知學習系統，理解「玩家如何思考、在哪個認知環節失敗」，從而形成**可遷移的橋牌認知（transferable bridge cognition）**，而非死背牌例或 pattern matching。

核心理念：**AI 不替玩家思考，AI 幫助理解玩家如何思考**；診斷 truth 來自 Rule Engine + Student Model + Evidence Trace，LLM 只負責解釋（不判案，只寫判決書）。最終定位為 **Bridge Cognitive Operating System**，而非題庫 / chatbot / DDS UI。

## KPI — 成功指標

> 採 Cognitive Mastery Metrics 與「錯誤模式是否改變」，明確排除 solve rate / streaks / raw DDS accuracy 作為主要指標（PRD §18 Non-Goals）。

| # | 指標 | 量測方式 | 基準值 | 目標值 |
|---|------|---------|-------|-------|
| 1 | Transfer success（遷移成功率） | 同一 cognitive structure 之變形 family 局面的正確率 | 待業主設定 | 待業主設定 |
| 2 | Misconception reduction（同類錯誤遞減） | 同一 cognitive failure（如 entry mismanagement）的再犯率隨時間下降幅度 | 待業主設定 | 待業主設定 |
| 3 | Hint independence（提示獨立性） | 達成正解所需的最低 hint level 隨時間下降 | 待業主設定 | 待業主設定 |
| 4 | Planning sophistication（規劃成熟度） | 提早 planning 行為比例、規劃 horizon 提升 | 待業主設定 | 待業主設定 |
| 5 | Retention stability（保留穩定度） | 隔週 / 隔期重測同 skill 的 mastery 維持率 | 待業主設定 | 待業主設定 |
| 6 | Diagnosis auditability（診斷可審計率） | 具完整 evidence log（hypothesis/confidence/evidence/rule_ids）的診斷比例 | 0%（新系統） | 100%（所有診斷皆 evidence-based） |

## 範圍邊界

### In-Scope（MVP 本系統負責）
- **單一認知 vertical**：Declarer Play 之 **Entry Management Tutor**（entry recognition / preservation / sequencing / unblock / communication planning / delayed cashing）
- **Curated Deal Practice**：人工 curated Entry Management 牌例
- **Bridge Situation DSL**：第一版僅支援 Entry Management 的 **Annotation + Diagnosis（A+C）**；含 ontology / DSL / rule / mastery model 的 versioning
- **Telemetry（四訊號）**：action trace（selected_card / legal_cards / think_time_ms / undo_count）、timing、hint escalation、reasoning tags
- **Evidence-based Diagnosis**：Rule-based + Probabilistic Student Model 產生 hypothesis / confidence / evidence / rule refs，並寫入可審計 Evidence Log
- **Graduated Hint System**：Level 0–4，escalation 作為 cognition signal
- **Mistake Taxonomy**：planning / entry mismanagement / counting / inference / probability miscalibration / tempo / practical overoptimization；允許多條 acceptable lines（非 binary 正解）
- **Multi-dimensional Mastery Tracking**：recognition / execution / transfer / retention（partial、probabilistic）
- **Post-Mortem Coaching**：認知診斷 + 解釋 + misconception 分析 + 下一步訓練建議
- **Coach Dashboard**：misconception trends / mastery evolution / transfer failures / hint dependency；含依學生 / 技能的基本篩選（CLR-260616-01#Q6）。MVP 首要交付介面（CLR-260616-01#Q1）
- **家長認知進展檢視**（唯讀）：家長 / 學校檢視所監護學習者的精熟與成長（GuardianStudentLink，CLR-260616-01#Q8）
- **Reproducible Replay**：Event-Sourced；用途 Debug / Research / Student History；MVP replay 單位＝deal session
- **LLM Explanation Layer**：依年齡 / mastery / frustration / fatigue / coach preference 調整語氣，僅 narration

### Out-of-Scope（明確排除）
- bidding tutor（叫牌）、defense tutor（防禦）— 避免 partnership ambiguity 與 convention chaos
- multiplayer / realtime partner / partnership modeling（多人協作）
- free-form AI chat（自由對話）— 避免 parsing 地獄與 UX 摩擦
- autonomous ontology evolution（全自動本體演化）— 僅做 AI 提案 + 人類核可
- eye tracking / biometric telemetry / mouse path telemetry / free-form chain-of-thought
- fully automatic deal generation（全自動生牌）
- deep embeddings-first architecture（embedding 優先架構）

### Deferred（未來版本）
- **Situation Family Generator / constraint-based generation**：DSL 的 Generation（B）能力與 infinite curriculum（長期大 moat）
- **Latent embedding sidecar**：顯式 ontology 之外的隱向量模型（Hybrid 第二層）
- **Adaptive sequencing / weakness-targeting assignment**：依 mastery 自適應出題
- **Ontology Governance Workflow 全自動化**：pattern mining → proposal → replay 評估之自動化（MVP 僅人工核可）
- **Gamification（badge / streak / leaderboard）**：MVP 僅 Mastery Progress Bar + Error Pattern Timeline
- **Junior / Student 完整 UI**：MVP 以 Coach Dashboard 為先（家長唯讀進展檢視已納入 in-scope，見上）
- **Adaptive sequencing / weakness-targeting 自動派題**：MVP 僅自選 + 教練派題，自適應排序延後（CLR-260616-01#Q2）

### 外部依賴
- **DDS（Double Dummy Solver）**：建議 Bo Haglund DDS library（C++，Python binding）做合法性 / 路線驗證
- **LLM API**：建議 Claude API（Haiku / Sonnet）作 explanation layer，成本可控
- **BridgeRuleEngine**：獨立的合法出牌 / trick winner / revoke 判定元件

<!-- CiC GAP #005 RESOLVED -->
**類型**：GAP（已解決，CLR-260616-01#Q5）
**位置**：docs/discovery/04-vision-kpi-scope.md#kpi
**描述**：KPI baseline / target 未量化。
**決策**：**pilot 後再定量**（deferred-needs-decision）；MVP 先以方向性指標（趨勢改善）為準。KPI #1–#5 的 baseline/target 維持「待業主設定（pilot 後）」。
**影響**：成功驗收標準、mastery update 權重
<!-- /CiC -->

<!-- CiC GAP #006 RESOLVED -->
**類型**：GAP（已解決，CLR-260616-01#Q3）
**位置**：docs/discovery/04-vision-kpi-scope.md#in-scope
**描述**：Probabilistic Student Model 的具體模型未定。
**決策**：**採 CDM（DINA/DINO）**，支援 partial mastery；StudentSkillState 4 維欄位表 P(屬性精熟)，由 student-model 服務更新（constraints.md CON-MASTERY-002）。
**影響**：StudentSkillState 更新規則、冷啟動策略
<!-- /CiC -->

<!-- CiC GAP #007 RESOLVED -->
**類型**：GAP（已解決，CLR-260616-01#Q4）
**位置**：docs/discovery/04-vision-kpi-scope.md#in-scope
**描述**：第一批 curated deal 的數量與標注負責人未定。
**決策**：**首批 10–20 副，LLM 草擬 Situation DSL + 專家人工審核**（打破產能瓶頸）。
**影響**：MVP 內容備齊度、ontology 驗證可行性
<!-- /CiC -->
