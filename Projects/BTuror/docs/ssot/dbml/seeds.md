# Seeds and Value Sets

> 專案：Bridge Cognitive Tutor
> 最後更新：2026-06-16
> 說明：規格層值域 SSoT。每個 DBML `ref_code:` 在此有對應 section。資料庫 seed script 為 generated（方向 seeds.md → generated）。

## UserType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| UserAccount | userType | S | 學生 | 學習者（中級玩家 / 青少年） | docs/discovery/01-stakeholders.md | true |
| UserAccount | userType | C | 教練 | 人類教練 | docs/discovery/01-stakeholders.md | true |
| UserAccount | userType | A | 標注者 | 橋藝專家 / 標注者 | docs/discovery/01-stakeholders.md | true |
| UserAccount | userType | R | 研究者 | 取用匿名遙測的研究者 | docs/discovery/01-stakeholders.md | true |
| UserAccount | userType | P | 家長 | 家長 / 學校監護人（CLR-260616-01#Q8） | .clarify/decisions/batch-CLR-260616-01.md#Q8 | true |

## CognitiveLevel

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| StudentProfile | cognitiveLevel | 0 | MiniBridge | 青少年 / 純打牌基礎認知 | docs/discovery/04-vision-kpi-scope.md; grill Q18 | true |
| StudentProfile | cognitiveLevel | 1 | 基礎莊家 | 基礎 declarer 認知 | grill Q18 | true |
| StudentProfile | cognitiveLevel | 2 | 中級規劃 | 中級 planning 認知 | grill Q18 | true |
| StudentProfile | cognitiveLevel | 3 | 高階實戰 | 高階 practical 認知 | grill Q18 | true |

> 註：CognitiveSkill.cognitiveLevel 共用同一值域（Layered Cognitive Ontology）。

## Seat

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| CuratedDeal | declarer | N | 北 | North | 橋牌通用 | true |
| CuratedDeal | declarer | E | 東 | East | 橋牌通用 | true |
| CuratedDeal | declarer | S | 南 | South | 橋牌通用 | true |
| CuratedDeal | declarer | W | 西 | West | 橋牌通用 | true |

> 註：ActionTrace.seat 共用同一值域。

## ScoringContext

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| CuratedDeal | scoringContext | I | IMP | IMP 賽制 | BTutor_PRD.md §12 | true |
| CuratedDeal | scoringContext | M | MP | Matchpoint 賽制 | BTutor_PRD.md §12 | true |
| CuratedDeal | scoringContext | B | BAM | Board-a-Match 賽制 | BTutor_PRD.md §12 | true |

## SituationType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| SituationAnnotation | situationType | EM | 橋引管理 | Entry Management（MVP 唯一支援） | BTutor_PRD.md §11; grill Q29 | true |

> 註：MVP 第一版 DSL 僅支援 Entry Management；未來擴充其他 situation type（見 discovery 04 §Deferred）。

## PublishStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| OntologyVersion / RuleSet | status | D | 草稿 | Draft，尚未生效 | grill Q30 | true |
| OntologyVersion / RuleSet | status | P | 已發布 | Published，版本生效且不可變 | grill Q30 | true |
| OntologyVersion / RuleSet | status | X | 已淘汰 | 已被新版本取代 | grill Q30 | true |

## SessionStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| PlaySession | status | I | 進行中 | in_progress | docs/ssot/habdd/deal-practice.ha.feature | true |
| PlaySession | status | C | 已完成 | completed | docs/ssot/habdd/deal-practice.ha.feature | true |
| PlaySession | status | A | 已中止 | abandoned | docs/ssot/habdd/deal-practice.ha.feature | true |

## HintLevel

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| HintEvent | hintLevel | 0 | 無提示 | Level 0 — 無提示 | BTutor_PRD.md §5.4; grill Q14 | true |
| HintEvent | hintLevel | 1 | 方向性提示 | Level 1 — Directional cue | BTutor_PRD.md §5.4 | true |
| HintEvent | hintLevel | 2 | 局部提示 | Level 2 — Localized cue | BTutor_PRD.md §5.4 | true |
| HintEvent | hintLevel | 3 | 部分揭示 | Level 3 — Partial reveal | BTutor_PRD.md §5.4 | true |
| HintEvent | hintLevel | 4 | 完整教學 | Level 4 — Full explanation | BTutor_PRD.md §5.4 | true |

## ReasoningTag

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| ReasoningTag | tagCode | CT | 計數 | counting | BTutor_PRD.md §5.3 | true |
| ReasoningTag | tagCode | EP | 橋引保留 | entry preservation | BTutor_PRD.md §5.3 | true |
| ReasoningTag | tagCode | PL | 規劃 | planning | BTutor_PRD.md §5.3 | true |
| ReasoningTag | tagCode | PR | 機率 | probability | BTutor_PRD.md §5.3 | true |
| ReasoningTag | tagCode | DH | 危險手 | danger hand | BTutor_PRD.md §5.3 | true |

## ReasoningTrigger

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| ReasoningTag | triggerType | H | 長考 | hesitation 觸發 | 0517-BTutor_discuss_Gemini.md §風險2 | true |
| ReasoningTag | triggerType | M | 關鍵錯誤 | critical mistake 觸發 | 0517-BTutor_discuss_Gemini.md §風險2 | true |
| ReasoningTag | triggerType | E | 高階提示 | hint escalation 觸發 | 0517-BTutor_discuss_Gemini.md §風險2 | true |

## MistakeCategory

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Diagnosis / DiagnosisRule | mistakeCategory | PF | 規劃失誤 | planning failure | BTutor_PRD.md §13 | true |
| Diagnosis / DiagnosisRule | mistakeCategory | EM | 橋引誤用 | entry mismanagement | BTutor_PRD.md §13 | true |
| Diagnosis / DiagnosisRule | mistakeCategory | CF | 計數失誤 | counting failure | BTutor_PRD.md §13 | true |
| Diagnosis / DiagnosisRule | mistakeCategory | IF | 推論失誤 | inference failure | BTutor_PRD.md §13 | true |
| Diagnosis / DiagnosisRule | mistakeCategory | PM | 機率誤判 | probability miscalibration | BTutor_PRD.md §13 | true |
| Diagnosis / DiagnosisRule | mistakeCategory | TE | 節奏失誤 | tempo error | BTutor_PRD.md §13 | true |
| Diagnosis / DiagnosisRule | mistakeCategory | PO | 過度最佳化 | practical overoptimization | BTutor_PRD.md §13 | true |

## MistakeSeverity

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Diagnosis | severity | N | 輕微 | minor | grill Q17 | true |
| Diagnosis | severity | J | 重大 | major | grill Q17 | true |
| Diagnosis | severity | C | 災難性 | catastrophic | grill Q17 | true |

## CognitiveOrigin

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Diagnosis | cognitiveOrigin | R | 辨識 | recognition | grill Q17 | true |
| Diagnosis | cognitiveOrigin | E | 執行 | execution | grill Q17 | true |
| Diagnosis | cognitiveOrigin | O | 認知過載 | overload | grill Q17 | true |
| Diagnosis | cognitiveOrigin | M | 迷思 | misconception | grill Q17 | true |

## Recoverability

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Diagnosis | recoverability | R | 可回復 | recoverable | grill Q17 | true |
| Diagnosis | recoverability | I | 不可逆 | irreversible | grill Q17 | true |

## MasteryTrend

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| StudentSkillState | trend | U | 進步中 | improving | grill Q15 | true |
| StudentSkillState | trend | S | 持平 | stable | grill Q15 | true |
| StudentSkillState | trend | D | 退步中 | declining | grill Q15 | true |

## ReviewAgreement

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| CoachReview | agreement | A | 同意 | agree | docs/ssot/habdd/coach-dashboard.ha.feature | true |
| CoachReview | agreement | D | 分歧 | disagree | docs/ssot/habdd/coach-dashboard.ha.feature | true |

## ProposalStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| OntologyProposal | status | P | 待核可 | proposed | docs/ssot/habdd/replay-governance.ha.feature | true |
| OntologyProposal | status | A | 已核可 | approved | docs/ssot/habdd/replay-governance.ha.feature | true |
| OntologyProposal | status | R | 已駁回 | rejected | docs/ssot/habdd/replay-governance.ha.feature | true |

## AssignmentStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Assignment | status | A | 已指派 | assigned | docs/ssot/habdd/coach-dashboard.ha.feature | true |
| Assignment | status | I | 進行中 | in_progress | docs/ssot/habdd/coach-dashboard.ha.feature | true |
| Assignment | status | C | 已完成 | completed | docs/ssot/habdd/coach-dashboard.ha.feature | true |

## LearningEventType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| LearningEvent | eventType | P | 出牌事件 | PlayEvent | docs/discovery/03-event-timeline.md; grill Q31 | true |
| LearningEvent | eventType | H | 提示事件 | HintEvent | grill Q31 | true |
| LearningEvent | eventType | R | 推理事件 | ReasoningEvent | grill Q31 | true |
| LearningEvent | eventType | D | 診斷事件 | DiagnosisEvent | grill Q31 | true |
| LearningEvent | eventType | M | 精熟更新事件 | MasteryUpdateEvent | grill Q31 | true |

## ReplayScope

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| ReplayRun | scope | S | 單副練習 | deal session（MVP 預設單位） | grill Q31 | true |
| ReplayRun | scope | T | 學生歷程 | student learning journey | grill Q31 | true |

## ReplayType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| ReplayRun | replayType | D | 除錯重播 | Debug Replay | grill Q31 | true |
| ReplayRun | replayType | R | 研究重播 | Research Replay | grill Q31 | true |
| ReplayRun | replayType | S | 學生歷程重播 | Student History Replay | grill Q31 | true |
