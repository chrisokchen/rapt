# User Story Index

> 最後更新：2026-06-16
> 專案：Bridge Cognitive Tutor（MVP：Entry Management Tutor）
> 總計：15 個故事（must-have: 7, should-have: 7, nice-to-have: 1）＋ 4 個 out-of-scope
> 來源：docs/discovery/02-user-journeys.md、03-event-timeline.md、04-vision-kpi-scope.md

## Must-Have

| 故事 ID | Actor | 目標 | 業務價值 | Feature 連結 |
|--------|-------|------|---------|------------|
| US-001 | 中級卡關玩家 | 開始一副 curated Entry Management 牌例練習 | 取得可診斷的練習場景 | F-001 deal-practice.ha.feature |
| US-002 | 中級卡關玩家 | 逐墩打牌並被記錄 action trace | 形成認知診斷的 ground truth | F-001 deal-practice.ha.feature |
| US-003 | 中級卡關玩家 | 卡關時請求漸進式提示 | 在 productive struggle 下獲得最小協助 | F-002 graduated-hint.ha.feature |
| US-005 | 中級卡關玩家 | 賽後取得 evidence-based 診斷與教學 | 理解「為什麼錯」而非只知道對錯 | F-004 diagnosis-coaching.ha.feature |
| US-006 | 中級卡關玩家 | 追蹤多維 mastery 與錯誤模式變化 | 感受到認知成長 | F-005 mastery-tracking.ha.feature |
| US-007 | 人類教練 | 在儀表板檢視學生認知分析 | 省下判斷弱點時間，專注高層教學 | F-006 coach-dashboard.ha.feature |
| US-011 | 橋藝專家 / 標注者 | 以 Situation DSL 標注 curated deal | 讓診斷引擎可運作、驗證 ontology | F-007 deal-authoring.ha.feature |

## Should-Have

| 故事 ID | Actor | 目標 | 業務價值 | Feature 連結 |
|--------|-------|------|---------|------------|
| US-004 | 中級卡關玩家 | 在關鍵時刻標記 reasoning tag | 提供可解釋的 cognitive intent 訊號 | F-003 reasoning-capture.ha.feature |
| US-008 | 人類教練 | 回溯某次診斷的證據日誌並標記分歧 | 建立 AI/教練分歧的高價值 dataset | F-006 coach-dashboard.ha.feature |
| US-009 | 人類教練 | 依弱點派發針對性訓練 | 讓學生練到對的認知缺口 | F-006 coach-dashboard.ha.feature |
| US-010 | 青少年 / MiniBridge 學習者 | 以淺層 ontology 與適齡語氣練習 | 培養 declarer 認知基礎 | F-001 / F-004（適齡情境） |
| US-012 | 橋藝專家 / 標注者 | 發布 versioned 本體 / 規則集 | 確保資料可重現、可演化 | F-007 deal-authoring.ha.feature |
| US-013 | 研究者 / 標注者 | 在指定 ontology/rule 版本下重播學習軌跡 | 支援 Debug / Research / Student-History 判讀 | F-008 replay-governance.ha.feature |
| US-015 | 家長 / 學校 | 檢視所監護學習者的認知進展 | 了解孩子的專注 / 規劃 / 推理成長（CLR-260616-01#Q8） | F-009 parent-view.ha.feature |

## Nice-to-Have

| 故事 ID | Actor | 目標 | 業務價值 | Feature 連結 |
|--------|-------|------|---------|------------|
| US-014 | 人類教練 / 標注者 | 審核 AI 提出的本體演化提案 | AI suggests, human governs，防止 ontology drift | F-008 replay-governance.ha.feature |

## Out-of-Scope

| 故事 ID | 目標 | 原因 |
|--------|------|------|
| US-OOS-1 | 叫牌教練（bidding tutor） | MVP 僅 Declarer Play / Entry Management（discovery 04 §Out-of-Scope） |
| US-OOS-2 | 防禦教練（defense tutor） | 同上；避免 hidden-information 複雜度 |
| US-OOS-3 | 多人 / 即時夥伴協作 | MVP 單人練習；避免 partnership ambiguity |
| US-OOS-4 | 自由對話 AI chat | 避免 parsing 地獄與 UX 摩擦（discovery 04 §Out-of-Scope） |

> 註：「全自動生牌 / Situation Family Generator」「latent embedding sidecar」「adaptive sequencing」屬 **Deferred**（非 out-of-scope），見 discovery 04 §Deferred；本階段不展開為 Scenario。

## Cross-Cutting Capability Matrix

| module | capability | handling | feature/scenario | decision_ref | notes |
|---|---|---|---|---|---|
| 牌例標注 | 匯入 | scenario | F-007#成功匯入並標注 curated 牌例 |  | 對應 event #1 牌例已匯入 |
| 牌例標注 | 批次處理 | out-of-scope |  |  | MVP 未列批次匯入 |
| 練習 | 錯誤格式 | scenario | F-001#拒絕非法出牌 |  | 合法出牌驗證 |
| 全域 | 授權不足 | scenario | F-008#本體變更需具治理權限者核可 |  | 治理權限分離 |
| 診斷 / 重播 | 稽核記錄 | scenario | F-004#寫入可審計證據日誌；F-008（event-sourced replay） |  | Evidence Log + Event Sourcing |
| 教練分析 | 篩選 | scenario | F-006#依學生與技能篩選認知分析 | CLR-260616-01#Q6 | MVP 納入基本篩選 |
| 教練分析 | 排序 | scenario | F-006#依學生與技能篩選認知分析 | CLR-260616-01#Q6 | 與篩選同 Scenario 承接 |
| 教練分析 | 匯出 | out-of-scope |  |  | MVP dashboard 僅核心視覺化，未列匯出 |
| 教練分析 | 分頁 | out-of-scope |  |  | MVP 未列清單分頁 |
| 遙測 | 清理 / 保留政策 | out-of-scope |  |  | 縱貫遙測為核心資產，MVP 無清理政策 |
| 全域 | 部分成功 / 部分失敗 | out-of-scope |  |  | 單副練習操作視為原子 |

<!-- CiC GAP #BHV-001 RESOLVED -->
**類型**：GAP（已解決，CLR-260616-01#Q6）
**位置**：docs/ssot/habdd/story-index.md#cross-cutting-capability-matrix
**決策**：MVP 納入基本篩選（依學生 / 技能）；承接於 F-006 SCN-F006-005。
**影響**：F-006 coach-dashboard、haPDL 清單頁意圖
<!-- /CiC -->
