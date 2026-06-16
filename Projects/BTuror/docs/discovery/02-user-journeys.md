# User Journeys

> 來源：BTutor_PRD.md §5（MVP 核心功能）、§21（MVP 架構）、BridgeTuror-grill.md Q13 / Q14 / Q24–Q31、0517-BTutor_discuss_*（roadmap / dogfooding）
> 範圍：僅描述業務流程，不涉及技術實作（API / 點擊 / 表單）。actor.id 對應 01-stakeholders.md。

## intermediate-player 的主要旅程：一副 Entry Management 練習

1. **進入練習**
   - 觸發：玩家自選或被教練指派一副 curated Entry Management 牌例
   - 動作：開始一副練習 session
   - 預期結果：載入牌例與其 Situation 標注，建立一筆練習紀錄

2. **逐墩打牌（產生 Action Trace）**
   - 觸發：輪到玩家做出牌決策
   - 動作：在合法牌中選牌；過程可能猶豫、改變主意、悔牌
   - 預期結果：系統記錄 selected_card / legal_cards / think_time / undo（認知負載與猶豫結構的訊號）

3. **遇到困難時請求提示**
   - 觸發：玩家卡關或不確定
   - 動作：呼叫漸進式提示（Level 1 方向 → Level 4 完整教學）
   - 預期結果：系統給出對應層級提示，並記錄 hint escalation（assistance dependency 訊號）

4. **關鍵時刻的輕量 reasoning 蒐集**
   - 觸發：系統偵測到長考 / 關鍵錯誤 / 呼叫高階提示（觸發式，避免心流中斷）
   - 動作：玩家從 reasoning tags（counting / entry preservation / planning / probability / danger hand）擇一或補一句
   - 預期結果：取得可解釋的 cognitive intent 訊號

5. **賽後認知診斷與教學（Post-Mortem）**
   - 觸發：整副牌結束
   - 動作：玩家檢視診斷結果與教學說明
   - 預期結果：取得 evidence-based diagnosis（hypothesis / confidence / evidence / rule refs）、misconception 分析、LLM 依程度調整語氣的教學、與建議的下一步訓練

6. **看見成長（Mastery Journey）**
   - 觸發：診斷完成後更新學生模型
   - 動作：玩家檢視各 sub-skill 的 mastery（recognition / execution / transfer / retention）與錯誤模式時間軸
   - 預期結果：感受到「我在變強」而非「在農經驗值」；mastery 為多維 partial、probabilistic 狀態

## human-coach 的主要旅程：學生認知檢視與派題

1. **檢視認知分析**
   - 觸發：教練想了解學生 / 全班近況
   - 動作：開啟 Coach Dashboard
   - 預期結果：看到 misconception trends、mastery evolution、transfer failures、hint dependency、cognitive progress

2. **診斷 review（人機協作）**
   - 觸發：教練對某次 AI 診斷有疑慮
   - 動作：回溯該次診斷的 evidence log
   - 預期結果：可判讀系統為何判定某 cognitive failure，必要時標記 AI 診斷與教練意見的分歧（高價值 dataset）

3. **派發針對性訓練**
   - 觸發：發現學生在某 sub-skill / misconception 卡住
   - 動作：指派對應 cognitive vertical 的牌例或 Situation Family
   - 預期結果：學生收到針對弱點的訓練，教練省下找題與判斷弱點的時間

## junior-learner 的主要旅程：MiniBridge 基礎認知練習

1. **以淺層 ontology 練習**
   - 觸發：學習者開始一副簡化牌例
   - 動作：在 Level 0–1 認知層級打牌（注意 / 保留 entries）
   - 預期結果：以兒童可懂的語氣給回饋（如「橋斷掉北邊大牌就拿不到了喔～」），培養 planning / counting / 專注習慣

## domain-expert-annotator 的主要旅程：curated deal 標注

1. **標注局面**
   - 觸發：新增一副 curated Entry Management 牌例
   - 動作：撰寫 / 審核 Situation DSL（features / critical_moments / skills / acceptable_lines / common_mistakes），可由 LLM 草擬後人工審核
   - 預期結果：牌例具備可驅動「診斷 → 出題 → hint → mastery update → dashboard」的標注，並登錄 DSL / ontology 版本

<!-- CiC GAP #003 RESOLVED -->
**類型**：GAP（已解決，CLR-260616-01#Q2）
**位置**：docs/discovery/02-user-journeys.md#intermediate-player
**描述**：牌例如何指派給玩家。
**決策**：**MVP 支援玩家自選 + 教練派題**（PlaySession 自選 + Assignment）；**adaptive sequencing 延後（deferred-mvp-out）**。
**影響**：PlaySession 建立流程、Assignment、haAPI / haPDL
<!-- /CiC -->
