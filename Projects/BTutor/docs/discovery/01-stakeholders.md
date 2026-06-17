# Stakeholders

> 來源：BTutor_PRD.md §7（目標使用者）、§8、BridgeTuror-grill.md Q18 / Q23、0517-BTutor_discuss_Gemini.md（To-B 策略）、0517-BTutor_discuss_vscSonnet.md（Coach dogfooding、Annotation 作者）

## 角色列表

| id | 名稱 | 類型 | 系統中的角色 |
|----|------|------|------------|
| intermediate-player | 中級卡關玩家 | user | **主要使用者**。概念懂但實戰不穩，接受診斷、提示與賽後教學 |
| junior-learner | 青少年 / MiniBridge 學習者 | user | **次要使用者**。培養 planning / counting / 專注力等 declarer 認知基礎 |
| human-coach | 人類教練 | user | **主要 feedback 對象**。透過 Coach Dashboard 檢視認知分析、派題、診斷誤判 review |
| domain-expert-annotator | 橋藝專家 / 標注者 | user | 標注 curated deal 的 Situation DSL、維護 Cognitive Ontology、審核 ontology 演化提案（MVP 階段常即業主本人） |
| researcher | 研究者 | external | 使用匿名化 longitudinal cognition telemetry 做學習分析 / 研究（次要、MVP 邊緣） |
| parent-school | 家長 / 學校 | external | MiniBridge 情境下檢視專注力 / 規劃 / 推理進展報告（MVP 不聚焦） |

## 各角色詳細描述

### intermediate-player — 中級卡關玩家
- **類型**：user（主要）
- **系統角色**：練習 curated deal、產生 action trace、接受 graduated hint 與 evidence-based diagnosis、賽後 post-mortem coaching、追蹤多維 mastery
- **主要關切**：把「上課都懂」轉成「實戰會打」、理解自己為什麼錯、看到自己在變強
- **痛點**：概念知道很多但執行不穩、planning 弱、transfer 能力不足、容易「上課都懂、打牌不會」（cognition transfer failure）

### junior-learner — 青少年 / MiniBridge 學習者
- **類型**：user（次要）
- **系統角色**：以較淺的 Layered Cognitive Ontology（Level 0–1）練習 declarer 基礎認知
- **主要關切**：建立正確的 planning / counting / 專注習慣，而非背 convention
- **痛點**：缺乏系統化、可診斷的打牌認知訓練；叫牌噪音干擾純打牌認知養成（MiniBridge 去除叫牌正好適合）

### human-coach — 人類教練
- **類型**：user（主要 feedback 對象）
- **系統角色**：檢視 misconception trends / mastery evolution / transfer failures / hint dependency；派發針對性訓練；review AI 診斷
- **主要關切**：省下找題、判斷弱點、追進度的時間，專注高層策略 / 心理 / partnership / motivation
- **痛點**：真人教練成本高，大量時間耗在低層分析而非高價值教學；缺乏全班認知 overload / misconception 聚類的可視化

### domain-expert-annotator — 橋藝專家 / 標注者
- **類型**：user
- **系統角色**：人工標注 curated deal 的 Situation DSL（situation_type / features / critical_moments / skills / acceptable_lines / common_mistakes），定義並維護 Cognitive Ontology 與 Diagnosis Rules
- **主要關切**：以可控、可審核方式建立高品質 ontology 種子；用 LLM 草擬 DSL 再人工審核以打破產能瓶頸
- **痛點**：人工標注成本極高（Gemini / Sonnet 共同警示），是 MVP 最大工程瓶頸之一

### researcher — 研究者
- **類型**：external（次要）
- **系統角色**：取用匿名 cognition telemetry、diagnosis evidence graph、mastery trajectories 做學習科學研究
- **主要關切**：資料可重現（reproducible replay）、ontology / rule 版本可比較
- **痛點**：一般 edtech 缺乏 research-grade 可重現的縱貫認知資料

### parent-school — 家長 / 學校
- **類型**：external（MVP 不聚焦）
- **系統角色**：MiniBridge 情境下接收學習者的認知能力報告
- **主要關切**：孩子的專注力、規劃力、推理力成長
- **痛點**：缺乏可解釋的能力面向報告

<!-- CiC ASM #002 RESOLVED -->
**類型**：ASM（已確認，CLR-260616-01#Q8）
**位置**：docs/discovery/01-stakeholders.md#parent-school
**描述**：parent-school / researcher 是否納入 MVP actor。
**決策**：**parent-school 納入 MVP** — 新增 GuardianStudentLink、parent-school actor/role 與 F-009 parent-view；researcher 維持 MVP 內（去識別化存取，見 GAP-MOD-001）。
**影響**：haARM actor / role 範圍、Coach Dashboard / 家長視圖
<!-- /CiC -->
