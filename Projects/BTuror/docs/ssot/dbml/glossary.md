# 統一語言詞彙表（Ubiquitous Language Glossary）

> 專案：Bridge Cognitive Tutor
> 最後更新：2026-06-16
> 術語數量：24（業務實體 22 + 關鍵屬性術語）

## 業務實體術語

| 術語（繁中）| 英文 | 定義 | 使用位置 |
|-----------|------|------|---------|
| 使用者帳號 | UserAccount | 系統的登入身分（學生 / 教練 / 標注者 / 研究者） | DBML / haARM |
| 學生檔案 | StudentProfile | 學習者的認知檔案，含認知層級 | Feature / DBML |
| 教練學生關係 | CoachStudentLink | 教練與其指導學生的關聯 | DBML / haARM |
| 監護關係 | GuardianStudentLink | 家長 / 學校與學習者的監護關聯（CLR-260616-01#Q8） | DBML / haARM |
| 牌例 | CuratedDeal | 人工 curated 的橋引管理練習牌局 | Feature / DBML |
| 局面標注 | SituationAnnotation | 牌例的 Situation DSL 標注 | Feature / DBML |
| 本體版本 | OntologyVersion | 版本化的認知本體 | Feature / DBML |
| 認知技能 | CognitiveSkill | 認知本體中的可觀測技能節點 | Feature / DBML |
| 規則集 | RuleSet | 版本化的診斷規則集合 | Feature / DBML |
| 診斷規則 | DiagnosisRule | 將證據映射到錯誤分類的規則 | DBML |
| 本體演化提案 | OntologyProposal | AI 提出、人工核可的本體變更 | Feature / DBML |
| 練習 | PlaySession | 學生對一副牌例的練習 session | Feature / DBML |
| 出牌紀錄 | ActionTrace | 逐墩出牌的認知軌跡 | Feature / DBML |
| 提示紀錄 | HintEvent | 漸進式提示事件 | Feature / DBML |
| 推理標記 | ReasoningTag | 觸發式蒐集的推理標籤 | Feature / DBML |
| 診斷 | Diagnosis | 基於證據的認知診斷假設 | Feature / DBML |
| 診斷證據 | DiagnosisEvidence | 支撐診斷的可審計證據明細 | Feature / DBML |
| 賽後教學 | CoachingFeedback | LLM 產生的賽後教學說明與建議 | Feature / DBML |
| 教練覆核 | CoachReview | 教練對 AI 診斷的覆核與分歧標記 | Feature / DBML |
| 認知精熟度 | StudentSkillState | 學生對某技能的多維 partial mastery | Feature / DBML |
| 訓練指派 | Assignment | 教練派發的針對性訓練 | Feature / DBML |
| 學習事件 | LearningEvent | event-sourced 學習事件流 | Feature / DBML |
| 重播 | ReplayRun | 指定版本下的可重現重播 | Feature / DBML |

## Canonical Mapping

| term | canonical_english | dbml_table | dbml_columns | gherkin_synonyms | legacy_aliases | notes |
|---|---|---|---|---|---|---|
| 練習 | PlaySession | PlaySession | sessionId,studentId,dealId,status |  |  |  |
| 牌例 | CuratedDeal | CuratedDeal | dealId,title,declarer | 牌局 |  |  |
| 局面標注 | SituationAnnotation | SituationAnnotation | annotationId,situationType,dslBody | Situation DSL |  |  |
| 出牌紀錄 | ActionTrace | ActionTrace | actionId,selectedCard,legalCards | 認知軌跡 |  |  |
| 提示紀錄 | HintEvent | HintEvent | hintId,hintLevel |  |  |  |
| 推理標記 | ReasoningTag | ReasoningTag | reasoningId,tagCode |  |  |  |
| 診斷 | Diagnosis | Diagnosis | diagnosisId,hypothesis,confidence |  |  |  |
| 證據日誌 | DiagnosisEvidence | DiagnosisEvidence | evidenceId,evidenceText,ruleId | 診斷證據 |  | Gherkin「證據日誌」對應 DiagnosisEvidence 集合 |
| 教學說明 | CoachingFeedback | CoachingFeedback | feedbackId,explanationText | 賽後教學 |  |  |
| 訓練建議 | CoachingFeedback | CoachingFeedback | suggestedSkillId |  |  | 「訓練建議」為 CoachingFeedback 的建議技能 |
| 精熟度 | StudentSkillState | StudentSkillState | recognitionMastery,executionMastery,transferMastery,retentionMastery |  |  | 多維 partial mastery |
| 遷移 | StudentSkillState | StudentSkillState | transferMastery |  |  | 遷移為精熟度的一個面向 |
| 保留 | StudentSkillState | StudentSkillState | retentionMastery |  |  | 保留為精熟度的一個面向 |
| 錯誤模式 | Diagnosis | Diagnosis | mistakeCategory,cognitiveOrigin |  |  | 錯誤模式時間軸由歷次 Diagnosis 聚合 |
| 指派 | Assignment | Assignment | assignmentId,targetSkillId |  |  |  |
| 本體 | OntologyVersion | OntologyVersion | ontologyVersion,status |  |  |  |
| 規則集 | RuleSet | RuleSet | ruleSetVersion,status |  |  |  |
| 本體演化提案 | OntologyProposal | OntologyProposal | proposalId,status |  |  |  |
| 重播 | ReplayRun | ReplayRun | replayId,replayType,scope |  |  |  |
| 診斷分歧 | CoachReview | CoachReview | reviewId,agreement |  |  | Gherkin「標記分歧」對應 CoachReview.agreement=D |
| 局面標注完整性 | SituationAnnotation | SituationAnnotation | isComplete |  |  | 對應 CON-ANNO-001 |
| 可接受路線 | SituationAnnotation | SituationAnnotation | dslBody |  |  | acceptable_lines 內嵌於 dslBody（半結構化） |

## 欄位/屬性術語

| 術語 | 英文 | 定義 |
|------|------|------|
| 認知層級 | cognitiveLevel | 分層認知本體的層級（MiniBridge → 高階） |
| 提示層級 | hintLevel | 漸進式提示的 0–4 級 |
| 認知成因 | cognitiveOrigin | 錯誤的認知來源（辨識 / 執行 / 過載 / 迷思） |
| 信心值 | confidence | 診斷或精熟估計的機率信心 |
| 風格差異 | isStylistic | 安全替代路線而非錯誤的標記 |

## 已棄用術語

| 棄用詞 | 替換為 | 原因 |
|--------|-------|------|
| 用戶 | 學生 / 使用者 | 統一以「學生」（學習者）或「使用者帳號」（身分）表達，避免混用 |
| 牌局 | 牌例 | curated 練習素材統一稱「牌例」（CuratedDeal） |
