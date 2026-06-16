# Event Timeline

> 來源：BTutor_PRD.md §5 / §14 / §15 / §21、BridgeTuror-grill.md Q22（Evidence Log）/ Q25（telemetry schema）/ Q30–Q32（replay / governance）
> 方法：Event Storming 輕量版。僅做業務層分析，不寫資料庫 Table / API / UI。actor 引用 01-stakeholders.md。

## Domain Events（時序排列）

| # | 事件 | Actor | 前置條件 | 後置狀態 |
|---|------|-------|---------|---------|
| 1 | 牌例已匯入 | domain-expert-annotator | 取得 curated deal | 牌例進入待標注 |
| 2 | 局面已標注（Situation DSL） | domain-expert-annotator | 牌例已匯入、ontology 版本就緒 | 牌例具可驅動診斷的 Situation 標注 |
| 3 | 認知本體 / 規則已發布（versioned） | domain-expert-annotator | ontology / rule / DSL 草稿完成 | 該版本 ontology / rule set 生效 |
| 4 | 練習已開始 | intermediate-player / junior-learner | 牌例已標注、玩家獲指派或自選 | 建立練習 session，載入局面 |
| 5 | 出牌已記錄 | intermediate-player | 練習進行中、輪到玩家 | 記下 selected_card / legal_cards / think_time / undo |
| 6 | 提示已升級 | intermediate-player | 玩家請求提示 | 給出對應 Level（0–4）提示，記 hint escalation |
| 7 | 推理標籤已標記 | intermediate-player | 觸發式（長考 / 關鍵錯誤 / 高階提示） | 取得 reasoning tag 訊號 |
| 8 | 關鍵錯誤已偵測 | system（rule engine） | 出牌偏離 acceptable_lines 之 critical_moment | 標記候選 mistake（含 taxonomy / severity） |
| 9 | 診斷假設已產生 | system（rule + probabilistic） | 蒐集足夠 evidence | 產出 hypothesis / confidence / evidence / rule_ids |
| 10 | 證據日誌已寫入 | system | 診斷假設已產生 | 可回溯、可審計的 evidence log 落地 |
| 11 | 學生 mastery 已更新 | system（student model） | 證據日誌已寫入 | 多維 partial mastery（recognition/execution/transfer/retention）更新 |
| 12 | 賽後教學已產生 | system（LLM explanation layer） | 證據日誌已寫入、pedagogy strategy 決定 | 依程度語氣的解釋 / Socratic / 下一步建議（LLM 只 narration） |
| 13 | 練習已完成 | intermediate-player / junior-learner | 整副牌結束 | session 結束，事件流封存 |
| 14 | 遷移已驗證 | system | 完成同 family 變形局面 | 更新 transfer mastery，判別記憶 vs 真學會 |
| 15 | 教練已檢視儀表板 | human-coach | 存在學生練習與診斷資料 | 取得 misconception / mastery / transfer / hint 分析 |
| 16 | 訓練已派發 | human-coach | 檢視分析後 | 學生收到針對性牌例 / Situation Family |
| 17 | 學習軌跡已重播 | researcher / domain-expert-annotator / system | 事件流與某 ontology/rule 版本 | 在指定版本下重新判讀（Debug / Research / Student History） |
| 18 | 本體演化提案已提出 | system（pattern mining） | 累積 telemetry，發現共現 / 依賴 | 產生 ontology patch 提案 |
| 19 | 本體演化已核可 | human-coach / domain-expert-annotator | 提案經 evidence + replay 評估 | 核可後成為新版本（AI suggests, human governs） |

## Commands

| Command | 觸發的 Event |
|---------|------------|
| 匯入牌例 | 牌例已匯入（#1） |
| 標注局面 | 局面已標注（#2） |
| 發布 ontology / rule 版本 | 認知本體 / 規則已發布（#3） |
| 開始練習 | 練習已開始（#4） |
| 出牌 | 出牌已記錄（#5）→（可能）關鍵錯誤已偵測（#8） |
| 請求提示 | 提示已升級（#6） |
| 標記推理 | 推理標籤已標記（#7） |
| 執行診斷 | 診斷假設已產生（#9）→ 證據日誌已寫入（#10）→ 學生 mastery 已更新（#11） |
| 產生賽後教學 | 賽後教學已產生（#12） |
| 完成練習 | 練習已完成（#13） |
| 出 transfer 變形題 | 遷移已驗證（#14） |
| 檢視儀表板 | 教練已檢視儀表板（#15） |
| 派發訓練 | 訓練已派發（#16） |
| 重播 session | 學習軌跡已重播（#17） |
| 提交 ontology 提案 | 本體演化提案已提出（#18） |
| 核可 ontology 提案 | 本體演化已核可（#19） |

## 初步 Bounded Context 分群（草圖）

> 注意：初步分群，非最終 Bounded Context（Phase 2 才確立）。

### Deal & Situation Authoring（牌例與局面標注）
- Events: [#1 牌例已匯入, #2 局面已標注, #3 本體/規則已發布]
- 可能的 Aggregate: [CuratedDeal, SituationAnnotation / SituationIR, CognitiveOntology, RuleSet]

### Play & Telemetry（打牌與遙測）
- Events: [#4 練習已開始, #5 出牌已記錄, #6 提示已升級, #7 推理標籤已標記, #13 練習已完成]
- 可能的 Aggregate: [PlaySession, ActionTrace, HintEvent, ReasoningTag]

### Diagnosis（診斷）
- Events: [#8 關鍵錯誤已偵測, #9 診斷假設已產生, #10 證據日誌已寫入]
- 可能的 Aggregate: [Mistake/ErrorTaxonomy, DiagnosisHypothesis, EvidenceLog]

### Student Model & Mastery（學生模型）
- Events: [#11 學生 mastery 已更新, #14 遷移已驗證]
- 可能的 Aggregate: [StudentSkillState, MasteryTrajectory]

### Tutoring & Explanation（教學與解釋）
- Events: [#12 賽後教學已產生]（含 graduated hint 策略、pedagogy strategy、LLM realization）
- 可能的 Aggregate: [PedagogicalStrategy, TutorExplanation]

### Coach Analytics（教練分析）
- Events: [#15 教練已檢視儀表板, #16 訓練已派發]
- 可能的 Aggregate: [CoachDashboardView, Assignment]

### Replay & Ontology Governance（重播與治理）
- Events: [#17 學習軌跡已重播, #18 本體演化提案已提出, #19 本體演化已核可]
- 可能的 Aggregate: [EventLog, ReplayRun, OntologyProposal, GovernanceReview]

<!-- CiC ASM #004 -->
**類型**：ASM
**位置**：docs/discovery/03-event-timeline.md#events
**描述**：事件 #8–#12、#17–#19 的 actor 標為 `system`（rule engine / student model / LLM / pattern mining）。01-stakeholders.md 的 actor 為人類角色；此處 `system` 屬內部服務 actor，假設後續 haARM 以 service actor 表示，非人類角色。
**影響**：haARM actor 分類（user vs service）、事件擁有權歸屬
**推薦**：rapt-modeling 時將 `system` 細分為具體服務 actor（DiagnosisEngine / StudentModel / ExplanationLayer / PatternMiner）
<!-- /CiC -->
