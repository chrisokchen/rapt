# Traceability

> 專案：Bridge Cognitive Tutor（MVP：Entry Management Tutor）
> 最後更新：2026-06-16（rapt-behavior 建立 L1、草擬 L2）
> 說明：L2 的 read/write_tables / fields 待 rapt-modeling、rapt-intent 精確化；本階段僅以業務語言標 entities。

## L1 Requirement Coverage

| req_or_story | source | feature | scenario_count | status | notes |
|---|---|---|---:|---|---|
| US-001 | docs/discovery/02-user-journeys.md#intermediate-player | deal-practice.ha.feature | 1 | covered | SCN-F001-001 |
| US-002 | docs/discovery/02-user-journeys.md#intermediate-player | deal-practice.ha.feature | 3 | covered | SCN-F001-002/003/004 |
| US-003 | docs/discovery/02-user-journeys.md#intermediate-player | graduated-hint.ha.feature | 4 | covered |  |
| US-004 | docs/discovery/02-user-journeys.md#intermediate-player | reasoning-capture.ha.feature | 3 | covered |  |
| US-005 | docs/discovery/02-user-journeys.md#intermediate-player | diagnosis-coaching.ha.feature | 6 | covered |  |
| US-006 | docs/discovery/02-user-journeys.md#intermediate-player | mastery-tracking.ha.feature | 5 | covered |  |
| US-007 | docs/discovery/02-user-journeys.md#human-coach | coach-dashboard.ha.feature | 1 | covered | SCN-F006-001 |
| US-008 | docs/discovery/02-user-journeys.md#human-coach | coach-dashboard.ha.feature | 2 | covered | SCN-F006-002/003 |
| US-009 | docs/discovery/02-user-journeys.md#human-coach | coach-dashboard.ha.feature | 1 | covered | SCN-F006-004 |
| US-010 | docs/discovery/02-user-journeys.md#junior-learner | deal-practice.ha.feature | 1 | partial | SCN-F001-005；適齡教學語氣涵蓋於 SCN-F004-005 |
| US-011 | docs/discovery/02-user-journeys.md#domain-expert-annotator | deal-authoring.ha.feature | 2 | covered | SCN-F007-001/002 |
| US-012 | docs/discovery/03-event-timeline.md#3 | deal-authoring.ha.feature | 1 | covered | SCN-F007-003 |
| US-013 | docs/discovery/03-event-timeline.md#17 | replay-governance.ha.feature | 3 | covered | SCN-F008-001/002/003 |
| US-014 | docs/discovery/03-event-timeline.md#18,19 | replay-governance.ha.feature | 2 | covered | SCN-F008-004/005 |
| US-015 | docs/discovery/01-stakeholders.md#parent-school; CLR-260616-01#Q8 | parent-view.ha.feature | 2 | covered | SCN-F009-001/002 |
| US-OOS-1 叫牌教練 | docs/discovery/04-vision-kpi-scope.md#out-of-scope | — | 0 | out-of-scope | MVP 僅 Declarer/Entry Management |
| US-OOS-2 防禦教練 | docs/discovery/04-vision-kpi-scope.md#out-of-scope | — | 0 | out-of-scope |  |
| US-OOS-3 多人協作 | docs/discovery/04-vision-kpi-scope.md#out-of-scope | — | 0 | out-of-scope |  |
| US-OOS-4 自由對話 | docs/discovery/04-vision-kpi-scope.md#out-of-scope | — | 0 | out-of-scope |  |
| CC-dashboard-filter | docs/ssot/habdd/story-index.md#cross-cutting | coach-dashboard.ha.feature | 0 | open-cic | CiC-BHV-001：dashboard 篩選/排序未定 |

## L2 Scenario Data Mapping

| scenario_id | feature | scenario | entities | glossary_terms | read_tables | write_tables | fields | constraints | confidence | source |
|---|---|---|---|---|---|---|---|---|---|---|
| SCN-F001-001 | deal-practice.ha.feature | 成功開始一副橋引管理練習 | 練習, 牌例 | 練習, 牌例 | CuratedDeal | PlaySession |  | CON-SESS-001 | medium | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F001-002 | deal-practice.ha.feature | 出牌被記錄為認知軌跡 | 出牌紀錄, 練習 | 出牌紀錄 | PlaySession | ActionTrace | ActionTrace.selectedCard,legalCards | CON-PLAY-001 | medium | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F001-003 | deal-practice.ha.feature | 悔牌與重新決策被記錄 | 出牌紀錄 | 出牌紀錄 |  |  |  |  | low | docs/ssot/habdd/deal-practice.ha.feature |
| SCN-F001-004 | deal-practice.ha.feature | 拒絕非法出牌 | 出牌紀錄 | 出牌紀錄 |  |  |  |  | low | docs/ssot/habdd/deal-practice.ha.feature |
| SCN-F001-005 | deal-practice.ha.feature | 青少年以淺層認知層級練習 | 練習 | 練習 |  |  |  |  | low | docs/ssot/habdd/deal-practice.ha.feature |
| SCN-F002-001 | graduated-hint.ha.feature | 請求第一級方向性提示 | 提示紀錄, 練習 | 提示紀錄 |  |  |  |  | low | docs/ssot/habdd/graduated-hint.ha.feature |
| SCN-F002-002 | graduated-hint.ha.feature | 提示逐級升級 | 提示紀錄 | 提示紀錄 |  |  |  |  | low | docs/ssot/habdd/graduated-hint.ha.feature |
| SCN-F002-003 | graduated-hint.ha.feature | 提示依賴度成為認知訊號 | 提示紀錄 | 提示紀錄 |  |  |  |  | low | docs/ssot/habdd/graduated-hint.ha.feature |
| SCN-F002-004 | graduated-hint.ha.feature | 無提示自行完成決策 | 提示紀錄 | 提示紀錄 |  |  |  |  | low | docs/ssot/habdd/graduated-hint.ha.feature |
| SCN-F003-001 | reasoning-capture.ha.feature | 長考時觸發推理標記蒐集 | 推理標記 | 推理標記 |  |  |  |  | low | docs/ssot/habdd/reasoning-capture.ha.feature |
| SCN-F003-002 | reasoning-capture.ha.feature | 關鍵錯誤後觸發推理標記蒐集 | 推理標記 | 推理標記 |  |  |  |  | low | docs/ssot/habdd/reasoning-capture.ha.feature |
| SCN-F003-003 | reasoning-capture.ha.feature | 玩家略過推理標記以維持心流 | 推理標記 | 推理標記 |  |  |  |  | low | docs/ssot/habdd/reasoning-capture.ha.feature |
| SCN-F004-001 | diagnosis-coaching.ha.feature | 產生基於證據的診斷 | 診斷, 證據日誌 | 診斷, 證據日誌 | PlaySession,ActionTrace | Diagnosis | Diagnosis.hypothesis,confidence | CON-DIAG-001 | medium | docs/ssot/haapi/diagnosis.haapi.yaml |
| SCN-F004-002 | diagnosis-coaching.ha.feature | 寫入可審計證據日誌 | 證據日誌, 診斷 | 證據日誌 | Diagnosis | DiagnosisEvidence | DiagnosisEvidence.ruleId,masteryDelta | CON-DIAG-001 | medium | docs/ssot/haapi/diagnosis.haapi.yaml |
| SCN-F004-003 | diagnosis-coaching.ha.feature | 安全的替代路線不判為錯誤 | 診斷 | 診斷, 可接受路線 |  |  |  |  | low | docs/ssot/habdd/diagnosis-coaching.ha.feature |
| SCN-F004-004 | diagnosis-coaching.ha.feature | 低信心診斷不過度宣稱 | 診斷 | 診斷 |  |  |  |  | low | docs/ssot/habdd/diagnosis-coaching.ha.feature |
| SCN-F004-005 | diagnosis-coaching.ha.feature | 依玩家層級調整教學語氣 | 教學說明 | 教學說明 |  |  |  |  | low | docs/ssot/habdd/diagnosis-coaching.ha.feature |
| SCN-F004-006 | diagnosis-coaching.ha.feature | 提供下一步訓練建議 | 訓練建議 | 訓練建議 |  |  |  |  | low | docs/ssot/habdd/diagnosis-coaching.ha.feature |
| SCN-F005-001 | mastery-tracking.ha.feature | 診斷後更新多維精熟度 | 精熟度, 診斷 | 精熟度 | Diagnosis | StudentSkillState | StudentSkillState.recognitionMastery,executionMastery,transferMastery,retentionMastery | CON-MASTERY-001,CON-MASTERY-002 | medium | docs/ssot/haapi/student-skill-state.haapi.yaml |
| SCN-F005-002 | mastery-tracking.ha.feature | 呈現部分精熟狀態 | 精熟度 | 精熟度 | StudentSkillState |  | StudentSkillState.recognitionMastery,executionMastery | CON-MASTERY-001 | medium | docs/ssot/haapi/student-skill-state.haapi.yaml |
| SCN-F005-003 | mastery-tracking.ha.feature | 以變形局面驗證遷移 | 精熟度, 練習 | 精熟度, 遷移 |  |  |  |  | low | docs/ssot/habdd/mastery-tracking.ha.feature |
| SCN-F005-004 | mastery-tracking.ha.feature | 隔期重測更新保留度 | 精熟度 | 精熟度, 保留 |  |  |  |  | low | docs/ssot/habdd/mastery-tracking.ha.feature |
| SCN-F005-005 | mastery-tracking.ha.feature | 檢視錯誤模式時間軸 | 精熟度 | 錯誤模式 |  |  |  |  | low | docs/ssot/habdd/mastery-tracking.ha.feature |
| SCN-F006-001 | coach-dashboard.ha.feature | 檢視學生認知分析 | 精熟度, 診斷 | 精熟度, 診斷 | StudentSkillState,Diagnosis |  |  |  | medium | docs/ssot/haapi/student-skill-state.haapi.yaml |
| SCN-F006-002 | coach-dashboard.ha.feature | 回溯診斷的證據日誌 | 證據日誌, 診斷 | 證據日誌 | Diagnosis,DiagnosisEvidence |  |  | CON-DIAG-001 | medium | docs/ssot/haapi/diagnosis.haapi.yaml |
| SCN-F006-003 | coach-dashboard.ha.feature | 標記 AI 與教練診斷分歧 | 診斷 | 診斷分歧 |  |  |  |  | low | docs/ssot/habdd/coach-dashboard.ha.feature |
| SCN-F006-004 | coach-dashboard.ha.feature | 派發針對性訓練 | 指派, 練習 | 指派 | CoachStudentLink | Assignment |  | CON-ASSIGN-001 | medium | docs/ssot/habdd/coach-dashboard.ha.feature |
| SCN-F006-005 | coach-dashboard.ha.feature | 依學生與技能篩選認知分析 | 精熟度 | 精熟度 | StudentSkillState,CognitiveSkill |  |  |  | medium | CLR-260616-01#Q6 |
| SCN-F007-001 | deal-authoring.ha.feature | 成功匯入並標注 curated 牌例 | 牌例 | 牌例, 局面標注 | CuratedDeal | SituationAnnotation | SituationAnnotation.dslBody,isComplete | CON-ANNO-001 | medium | docs/ssot/haapi/situation-annotation.haapi.yaml |
| SCN-F007-002 | deal-authoring.ha.feature | 拒絕缺漏關鍵欄位的標注 | 牌例 | 局面標注 |  |  |  |  | low | docs/ssot/habdd/deal-authoring.ha.feature |
| SCN-F007-003 | deal-authoring.ha.feature | 發布版本化的本體與規則集 | 本體, 規則集 | 本體, 規則集 |  |  |  |  | low | docs/ssot/habdd/deal-authoring.ha.feature |
| SCN-F008-001 | replay-governance.ha.feature | 除錯重播確認診斷依據 | 重播, 證據日誌 | 重播 |  |  |  |  | low | docs/ssot/habdd/replay-governance.ha.feature |
| SCN-F008-002 | replay-governance.ha.feature | 研究重播比較不同規則版本 | 重播, 規則集 | 重播, 規則集 |  |  |  |  | low | docs/ssot/habdd/replay-governance.ha.feature |
| SCN-F008-003 | replay-governance.ha.feature | 學生歷程重播重算精熟曲線 | 重播, 精熟度 | 重播, 精熟度 |  |  |  |  | low | docs/ssot/habdd/replay-governance.ha.feature |
| SCN-F008-004 | replay-governance.ha.feature | 本體變更需具治理權限者核可 | 本體, 本體演化提案 | 本體演化提案 |  |  |  |  | low | docs/ssot/habdd/replay-governance.ha.feature |
| SCN-F008-005 | replay-governance.ha.feature | 核可後套用本體演化提案 | 本體演化提案, 本體 | 本體演化提案 |  |  |  |  | low | docs/ssot/habdd/replay-governance.ha.feature |
| SCN-F009-001 | parent-view.ha.feature | 檢視監護學習者的認知進展 | 精熟度, 監護關係 | 精熟度, 監護關係 | StudentSkillState,GuardianStudentLink |  |  | CON-GUARD-001 | medium | CLR-260616-01#Q8 |
| SCN-F009-002 | parent-view.ha.feature | 不得檢視非監護學習者的資料 | 精熟度, 監護關係 | 監護關係 | GuardianStudentLink |  |  | CON-GUARD-001 | medium | CLR-260616-01#Q8 |

## L3 Intent Mapping

> 由 rapt-intent 維護（Phase 4，2026-06-16）。

| scenario_id | haapi_operation | hapdl_page | haarm_permissions | source |
|---|---|---|---|---|
| SCN-F001-001 | play-session.create | play-session-play | play_session_create | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F001-002 | play-session.play_card | play-session-play | action_trace_create | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F001-003 | play-session.play_card | play-session-play | action_trace_create | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F001-004 | play-session.play_card | play-session-play | action_trace_create | docs/ssot/haapi/play-session.haapi.yaml (CON-PLAY-001) |
| SCN-F001-005 | play-session.create | play-session-play | play_session_create | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F002-001 | play-session.request_hint | play-session-play | hint_event_create | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F002-002 | play-session.request_hint | play-session-play | hint_event_create | docs/ssot/haapi/play-session.haapi.yaml (CON-HINT-001) |
| SCN-F002-003 | play-session.request_hint | play-session-play | hint_event_create | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F002-004 | play-session.play_card | play-session-play | action_trace_create | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F003-001 | play-session.tag_reasoning | play-session-play | reasoning_tag_create | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F003-002 | play-session.tag_reasoning | play-session-play | reasoning_tag_create | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F003-003 | play-session.tag_reasoning | play-session-play | reasoning_tag_create | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F003-002 | play-session.tag_reasoning | play-session-play | reasoning_tag_create | docs/ssot/haapi/play-session.haapi.yaml |
| SCN-F004-001 | play-session.diagnose / diagnosis.read | diagnosis-detail | diagnosis_create / diagnosis_read_own | docs/ssot/haapi/diagnosis.haapi.yaml (CON-DIAG-001) |
| SCN-F004-002 | diagnosis.read | diagnosis-detail | diagnosis_evidence_read_own | docs/ssot/haapi/diagnosis.haapi.yaml |
| SCN-F004-003 | diagnosis.read | diagnosis-detail | diagnosis_read_own | docs/ssot/haapi/diagnosis.haapi.yaml (CON-DIAG-003) |
| SCN-F004-004 | diagnosis.read | diagnosis-detail | diagnosis_read_own | docs/ssot/haapi/diagnosis.haapi.yaml (CON-DIAG-002) |
| SCN-F004-005 | coaching-feedback.read | diagnosis-detail | coaching_feedback_read_own | docs/ssot/haapi/coaching-feedback.haapi.yaml |
| SCN-F004-006 | coaching-feedback.read | diagnosis-detail | coaching_feedback_read_own | docs/ssot/haapi/coaching-feedback.haapi.yaml |
| SCN-F005-001 | student-skill-state.read | student-mastery-detail | student_skill_state_read_own | docs/ssot/haapi/student-skill-state.haapi.yaml |
| SCN-F005-002 | student-skill-state.read | student-mastery-detail | student_skill_state_read_own | docs/ssot/haapi/student-skill-state.haapi.yaml |
| SCN-F005-003 | student-skill-state.read | student-mastery-detail | student_skill_state_read_own | docs/ssot/haapi/student-skill-state.haapi.yaml |
| SCN-F005-004 | student-skill-state.read | student-mastery-detail | student_skill_state_read_own | docs/ssot/haapi/student-skill-state.haapi.yaml |
| SCN-F005-005 | diagnosis.list | student-mastery-detail | diagnosis_read_own | docs/ssot/haapi/diagnosis.haapi.yaml |
| SCN-F006-001 | student-skill-state.list | coach-dashboard | student_skill_state_read_team | docs/ssot/haapi/student-skill-state.haapi.yaml |
| SCN-F006-002 | diagnosis.read | coach-dashboard | diagnosis_evidence_read_team | docs/ssot/haapi/diagnosis.haapi.yaml |
| SCN-F006-003 | diagnosis.review | coach-dashboard | coach_review_create | docs/ssot/haapi/diagnosis.haapi.yaml |
| SCN-F006-004 | assignment.create | assignment-form | assignment_create | docs/ssot/haapi/assignment.haapi.yaml |
| SCN-F006-005 | student-skill-state.list | coach-dashboard | student_skill_state_read_team | docs/ssot/haapi/student-skill-state.haapi.yaml |
| SCN-F007-001 | situation-annotation.create | situation-annotation-form | situation_annotation_create | docs/ssot/haapi/situation-annotation.haapi.yaml |
| SCN-F007-002 | situation-annotation.create | situation-annotation-form | situation_annotation_create | docs/ssot/haapi/situation-annotation.haapi.yaml (CON-ANNO-001) |
| SCN-F007-003 | cognitive-skill.create / ontology publish | cognitive-skill-list | ontology_version_publish / cognitive_skill_create | docs/ssot/haapi/cognitive-skill.haapi.yaml (CON-GOV-002) |
| SCN-F008-001 | replay-run.create | replay-run-list | replay_run_create | docs/ssot/haapi/replay-run.haapi.yaml |
| SCN-F008-002 | replay-run.create | replay-run-list | replay_run_create | docs/ssot/haapi/replay-run.haapi.yaml |
| SCN-F008-003 | replay-run.create | replay-run-list | replay_run_create | docs/ssot/haapi/replay-run.haapi.yaml |
| SCN-F008-004 | ontology-proposal.approve | ontology-proposal-list | ontology_proposal_review | docs/ssot/haapi/ontology-proposal.haapi.yaml (CON-GOV-001) |
| SCN-F008-005 | ontology-proposal.approve | ontology-proposal-list | ontology_proposal_review | docs/ssot/haapi/ontology-proposal.haapi.yaml |
| SCN-F009-001 | student-skill-state.read | parent-progress | student_skill_state_read_ward | docs/ssot/haapi/student-skill-state.haapi.yaml (CON-GUARD-001) |
| SCN-F009-002 | student-skill-state.read | parent-progress | student_skill_state_read_ward | docs/ssot/haapi/student-skill-state.haapi.yaml (CON-GUARD-001) |

> 註：F-007 局面標注另由 situation-annotation API 承接；ontology/rule 版本發布對應 OntologyVersion（haARM ontology_version_publish）。

## Decision Traceability

| decision_id | cic_id | status | affected_artifacts | summary |
|---|---|---|---|---|
| CLR-260616-01#Q1 | CiC-CON-001 | applied | docs/discovery/00-source-inventory.md; docs/discovery/04-vision-kpi-scope.md | Coach Dashboard 為 MVP 首要交付介面 |
| CLR-260616-01#Q2 | CiC-GAP-003 | applied | docs/discovery/02-user-journeys.md; docs/discovery/04-vision-kpi-scope.md | 牌例自選 + 教練派題；adaptive sequencing 延後（deferred-mvp-out） |
| CLR-260616-01#Q3 | CiC-GAP-006 | applied | docs/ssot/dbml/constraints.md; docs/discovery/04-vision-kpi-scope.md | student model 採 CDM（DINA/DINO）；CON-MASTERY-002 |
| CLR-260616-01#Q4 | CiC-GAP-007 | applied | docs/discovery/04-vision-kpi-scope.md | 首批 10–20 副，LLM 草擬 + 專家審核 |
| CLR-260616-01#Q5 | CiC-GAP-005 | applied | docs/discovery/04-vision-kpi-scope.md | KPI target 於 pilot 後再定量（deferred-needs-decision） |
| CLR-260616-01#Q6 | CiC-GAP-BHV-001 | applied | docs/ssot/habdd/coach-dashboard.ha.feature; docs/ssot/habdd/story-index.md | Coach Dashboard 納入依學生/技能基本篩選（SCN-F006-005） |
| CLR-260616-01#Q7 | CiC-GAP-MOD-001 | applied | docs/ssot/dbml/constraints.md; docs/ssot/haarm/bridge-cognitive-tutor.haarm.yaml | researcher 僅存取去識別化遙測；CON-PRIV-001 |
| CLR-260616-01#Q8 | CiC-ASM-002 | applied | docs/ssot/dbml/schema.dbml; docs/ssot/haarm/bridge-cognitive-tutor.haarm.yaml; docs/ssot/habdd/parent-view.ha.feature | parent-school 納入 MVP：GuardianStudentLink + parent-school role + F-009 + CON-GUARD-001 |
| (modeling) | CiC-ASM-004 | applied | docs/ssot/haarm/bridge-cognitive-tutor.haarm.yaml | `system` 細分為 4 個 service actor |

## Deferred Register

| item | status | decision_ref | notes |
|---|---|---|---|
| Adaptive sequencing / 自動派題 | deferred-mvp-out | CLR-260616-01#Q2 | MVP 僅自選 + 教練派題 |
| KPI baseline/target 量化 | deferred-needs-decision | CLR-260616-01#Q5 | pilot 後再定 |
| Situation Family Generator / 自動生牌 | deferred-mvp-out | docs/discovery/04-vision-kpi-scope.md#deferred | 長期 moat，DSL Generation 延後 |
| Latent embedding sidecar | deferred-mvp-out | docs/discovery/04-vision-kpi-scope.md#deferred | Hybrid 第二層 |
| Gamification（badge/streak） | deferred-mvp-out | docs/discovery/04-vision-kpi-scope.md#deferred | MVP 僅 Progress Bar + Error Timeline |
