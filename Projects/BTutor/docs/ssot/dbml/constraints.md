# Domain Constraints

> 專案：Bridge Cognitive Tutor
> 最後更新：2026-06-16
> 說明：承載 DBML 型別與 seeds.md 無法完整表達的業務規則。constraint_id 穩定，供 traceability / haAPI / RAscore 引用。

| constraint_id | type | owner_table | owner_field | rule | source | related_scenarios | enforcement |
|---|---|---|---|---|---|---|---|
| CON-PLAY-001 | referential | ActionTrace | selectedCard | selectedCard 必須屬於同列 legalCards 集合；非法出牌不予接受 | docs/ssot/habdd/deal-practice.ha.feature | SCN-F001-004 | haAPI |
| CON-SESS-001 | state-transition | PlaySession | status | 狀態僅可由 I（進行中）轉為 C（已完成）或 A（已中止）；終態不可回轉 | docs/ssot/habdd/deal-practice.ha.feature | SCN-F001-001 | haAPI |
| CON-HINT-001 | monotonic | HintEvent | hintLevel | 同一墩的提示層級只能逐級升級，不可下降 | docs/ssot/habdd/graduated-hint.ha.feature | SCN-F002-002 | haAPI |
| CON-DIAG-001 | cardinality | Diagnosis | diagnosisId | 每筆 Diagnosis 至少對應一筆 DiagnosisEvidence（evidence-based、可審計） | docs/ssot/habdd/diagnosis-coaching.ha.feature | SCN-F004-001, SCN-F004-002 | haAPI |
| CON-DIAG-002 | threshold | Diagnosis | confidence | confidence 低於門檻時不得以斷定語氣陳述成因；CoachingFeedback 須以試探語氣呈現 | docs/ssot/habdd/diagnosis-coaching.ha.feature | SCN-F004-004 | haAPI |
| CON-DIAG-003 | business-rule | Diagnosis | isStylistic | 落在 SituationAnnotation.acceptableLines 內的安全替代路線須標 isStylistic=1，不得判為 mistake | docs/ssot/habdd/diagnosis-coaching.ha.feature | SCN-F004-003 | haAPI |
| CON-DIAG-004 | range | Diagnosis | confidence | confidence ∈ [0,1] | grill Q22 | SCN-F004-001 | haAPI |
| CON-MASTERY-001 | range | StudentSkillState | recognitionMastery,executionMastery,transferMastery,retentionMastery,confidence | 各精熟度與信心值 ∈ [0,1]；允許 partial mastery | docs/ssot/habdd/mastery-tracking.ha.feature | SCN-F005-001, SCN-F005-002 | haAPI |
| CON-EVENT-001 | append-only | LearningEvent | eventId | 學習事件流為 append-only，不可更新或刪除（event sourcing，state=replay(events)） | grill Q31; docs/discovery/03-event-timeline.md | SCN-F008-001 | haAPI |
| CON-EVENT-002 | version-stamp | LearningEvent | ontologyVersion,ruleSetVersion | 每筆事件須記錄當時的 ontology 與 rule 版本，供日後以不同版本重播 | grill Q30 | SCN-F008-002, SCN-F008-003 | haAPI |
| CON-GOV-001 | authorization | OntologyProposal | status | 提案僅可由具治理權限者核可（P→A）或駁回（P→R）；不具權限者不可套用 | docs/ssot/habdd/replay-governance.ha.feature | SCN-F008-004, SCN-F008-005 | haARM |
| CON-GOV-002 | immutability | OntologyVersion | status | 版本一經發布（P）即不可變；演化須建立新版本而非修改既有版本 | grill Q30 | SCN-F007-003, SCN-F008-005 | haAPI |
| CON-AUTH-001 | uniqueness | CognitiveSkill | ontologyVersion,skillCode | 同一本體版本內 skillCode 唯一 | grill Q15,Q16 | SCN-F005-001 | haAPI |
| CON-ASSIGN-001 | referential | Assignment | coachId,studentId | 指派僅可建立於存在 CoachStudentLink 的教練—學生關係 | docs/ssot/habdd/coach-dashboard.ha.feature | SCN-F006-004 | haAPI |
| CON-REVIEW-001 | authorization | CoachReview | coachId | 教練僅可覆核其指導之學生的診斷（依 CoachStudentLink） | docs/ssot/habdd/coach-dashboard.ha.feature | SCN-F006-002, SCN-F006-003 | haARM |
| CON-ANNO-001 | completeness | SituationAnnotation | isComplete | isComplete=1 須含關鍵時刻、所需技能、可接受路線、常見錯誤；缺漏不予接受 | docs/ssot/habdd/deal-authoring.ha.feature | SCN-F007-002 | haAPI |
| CON-MASTERY-002 | model | StudentSkillState | recognitionMastery,executionMastery,transferMastery,retentionMastery | mastery 採 CDM（DINA/DINO）估計：各面向值表 P(該屬性精熟)，由 student-model 服務更新（CLR-260616-01#Q3） | .clarify/decisions/batch-CLR-260616-01.md#Q3 | manual |
| CON-PRIV-001 | privacy | LearningEvent,Diagnosis,StudentSkillState | (all) | researcher 角色僅可存取去識別化（de-identified）後的遙測；haAPI 查詢層須移除 PII 與可識別關聯（CLR-260616-01#Q7） | .clarify/decisions/batch-CLR-260616-01.md#Q7 | haAPI |
| CON-GUARD-001 | authorization | GuardianStudentLink | guardianId | 家長僅可檢視其監護學習者（依 GuardianStudentLink）的精熟 / 進展，不得存取他人資料（CLR-260616-01#Q8） | .clarify/decisions/batch-CLR-260616-01.md#Q8 | haARM |

## Compatibility Decisions

> 本專案為 greenfield，無 legacy schema；以下為「半結構化 / 反正規化」設計決策，依 R-DBML-09 須有 risk 與補償規則。

| item | decision | risk | compensating_rule | source |
|---|---|---|---|---|
| SituationAnnotation.dslBody | 以 nvarchar(max) 儲存 Situation DSL 內文（半結構化） | DB 無法強制 DSL 結構，可能存入不合規 DSL | CON-ANNO-001：haAPI 寫入前依 Situation DSL schema 驗證必要區段 | grill Q28; 0517-BTutor_discuss_vscSonnet.md（JSONB） |
| ActionTrace.legalCards | 以 nvarchar(max) JSON 陣列儲存合法牌集合（反正規化） | DB 無法保證每張牌合法且唯一 | CON-PLAY-001：haAPI 驗證為合法牌碼陣列且 selectedCard ∈ legalCards | 0517-BTutor_discuss_vscSonnet.md（BridgeRuleEngine） |
| LearningEvent.payload | 以 nvarchar(max) JSON 儲存事件內容（多型 event） | DB 無法強制各 eventType 的 payload 結構 | CON-EVENT-001/002：haAPI 依 eventType 驗證 payload 結構並戳記版本 | grill Q31 |
| Diagnosis / StudentSkillState 多維 mastery | 以固定欄位（recognition/execution/transfer/retention）表示而非動態 dimension 表 | 新增 mastery 面向須改 schema | 以 OntologyVersion 控管；面向擴充走版本演化（CON-GOV-002） | grill Q15,Q20 |
