# RAPTor Session

> arguments.yml: initialized
> arguments_schema_version: 2
> initialized_at: 2026-06-16

## Phase Status

| Phase | Status | Next |
|---|---|---|
| 1. Discovery | done | /rapt-behavior |
| 1.5 Behavior | done | /rapt-modeling |
| 2. Modeling | done | /rapt-clarify |
| 3. Clarification | done | /rapt-intent |
| 4. Intent | done | /rapt-verify |
| 5. Verification | done (PASS) | /rapt-RAscore（可選）|
| 6. Reconcile | done | — |
| Preview | deferred | /rapt-openapi, /rapt-lofi, /rapt-design-brief |

## Phase 1 Discovery（完成於 2026-06-16）

產出（`docs/discovery/`）：
- `00-source-inventory.md`（4 sources：PRD + grill + 2 審查）
- `01-stakeholders.md`（6 角色）
- `02-user-journeys.md`（4 旅程）
- `03-event-timeline.md`（19 events / 7 BC 候選）
- `04-vision-kpi-scope.md`（vision + 6 KPI + scope）

閘門：**PASS**（6/6 條件通過）

待處理 CiC（留給 /rapt-clarify）：
| # | 類型 | 位置 | 摘要 |
|---|---|---|---|
| 001 | CON | source-inventory | Coach Dashboard vs Student UI 建置順序 |
| 002 | ASM | stakeholders | parent-school / researcher 是否納入 MVP actor |
| 003 | GAP | user-journeys | 牌例指派方式（自選 / 派題 / adaptive） |
| 004 | ASM | event-timeline | `system` actor 需細分為服務 actor |
| 005 | GAP | vision-kpi-scope | KPI baseline / target 未量化 |
| 006 | GAP | vision-kpi-scope | Probabilistic student model（CDM vs BKT）未定 |
| 007 | GAP | vision-kpi-scope | 首批 curated deal 數量 / 標注負責人未定 |

## Phase 1.5 Behavior（完成於 2026-06-16）

產出（`docs/ssot/habdd/`）：
- `story-index.md`（14 stories + 4 OOS + Cross-Cutting Matrix）
- 8 個 `.ha.feature`：deal-practice(F-001)、graduated-hint(F-002)、reasoning-capture(F-003)、diagnosis-coaching(F-004)、mastery-tracking(F-005)、coach-dashboard(F-006)、deal-authoring(F-007)、replay-governance(F-008)
- `.raptor/traceability.md`（L1 全覆蓋、L2 草稿 33 scenarios）

閘門：**PASS**（9/9 條件通過）

待處理 CiC（累計）：
| # | 類型 | 位置 | 摘要 |
|---|---|---|---|
| BHV-001 | GAP | habdd/story-index | Coach Dashboard 篩選/排序承接方式未定 |

## Phase 2 Domain Modeling（完成於 2026-06-16）

產出：
- `docs/ssot/dbml/schema.dbml`（22 tables / 6 TableGroup contexts / 35 Refs）
- `docs/ssot/dbml/seeds.md`（21 個 ref_code 值集）
- `docs/ssot/dbml/constraints.md`（16 constraints + 4 compatibility decisions）
- `docs/ssot/dbml/glossary.md`（24 術語 + Canonical Mapping）
- `docs/ssot/haarm/bridge-cognitive-tutor.haarm.yaml`（9 actors / 10 roles / 22 resources / 51 permissions）

閘門：**PASS**（11/11 條件通過；無 AP-01~AP-05 反模式）

CiC 異動：
| # | 類型 | 位置 | 狀態 |
|---|---|---|---|
| MOD-001 | GAP | haarm#researcher | 新增：研究者 scope:all 遙測匿名化政策未定 |
| ASM-004 | ASM | haarm | **已解**：`system` 細分為 4 個 service actor |
| GAP-006 | GAP | (mastery) | 部分處理：mastery 以 4 維固定欄位建模（相容 CDM partial mastery），模型選型仍待 clarify |

## Phase 3 Clarification（完成於 2026-06-16）

Batch CLR-260616-01（8 問，全數回答並 APPLIED）：
| Q | CiC | 決策 |
|---|---|---|
| Q1 | CON-001 | Coach Dashboard 為 MVP 首要交付介面 |
| Q2 | GAP-003 | 自選 + 教練派題；adaptive 延後 |
| Q3 | GAP-006 | student model 採 CDM（DINA/DINO） |
| Q4 | GAP-007 | 首批 10–20 副，LLM 草擬 + 專家審核 |
| Q5 | GAP-005 | KPI target 於 pilot 後再定量 |
| Q6 | BHV-001 | Dashboard 納入基本篩選（SCN-F006-005） |
| Q7 | MOD-001 | researcher 僅存取去識別化遙測 |
| Q8 | ASM-002 | **parent-school 納入 MVP** |

SSoT 異動：
- DBML：+GuardianStudentLink（23 tables）
- haARM：+parent-school actor/role、+guardian_student_link resource、+3 permissions、researcher 去識別化註記
- habdd：+F-009 parent-view、F-006 +SCN-F006-005（篩選）；story-index 15 stories
- seeds：UserType +家長(P)；constraints：+CON-MASTERY-002 / CON-PRIV-001 / CON-GUARD-001
- traceability：Decision Traceability（9 筆）+ Deferred Register

閘門：**PASS**（6/6；backlog 0 OPEN，全部 CiC RESOLVED）

## Phase 4 Intent（完成於 2026-06-16）

產出：
- `docs/ssot/haapi/`：10 個 .haapi.yaml（curated-deal, situation-annotation, cognitive-skill, play-session, diagnosis, coaching-feedback, student-skill-state, assignment, ontology-proposal, replay-run）
- `docs/ssot/hapdl/`：13 個 .hapdl.yaml（含 MVP 首要 coach-dashboard，及 parent-progress、play-session-play、diagnosis-detail 等）
- traceability：L3 Intent Mapping（34 scenario）+ L2 write_tables 精確化

覆蓋說明：child/telemetry 實體以 operation/nested 承接 —
- ActionTrace/HintEvent/ReasoningTag → play-session operations（play_card/request_hint/tag_reasoning）
- DiagnosisEvidence/CoachingFeedback → diagnosis / coaching-feedback read
- UserAccount/StudentProfile/*Link/OntologyVersion/RuleSet/DiagnosisRule/LearningEvent → identity/reference/event-store（MVP 無獨立 CRUD 意圖或由 service 寫入）

閘門：**PARTIAL**（4/5 PASS；無 legacy 欄位、L2/L3 完整、entity 對應 DBML、主要 table 有 haAPI/haPDL）
- ⚠ 待 backfill：**CiC-BDY-INT-001**（haAPI situation-annotation 引用 `situation_annotation_read`，haARM 缺此 permission，需 rapt-reconcile backfill）

CiC（累計待處理）：
| # | 類型 | 位置 | 摘要 |
|---|---|---|---|
| BDY-INT-001 | BDY | haapi/situation-annotation | 機械性：haARM 缺 situation_annotation_read，待 reconcile 補 |

## Phase 5 Verification（完成於 2026-06-16）

報告：`docs/reports/verify-report.md` + `.yml`
- 完整性：**PASS**　覆蓋率：**PASS**（must/should/overall 100%）
- 一致性：**FAIL**（dsl-lint：1 XREF-003，缺 situation_annotation_read；無結構錯誤、無 legacy 欄位）
- 可追蹤性：**PARTIAL**（L1 PASS、L3 35/38 顯式、部分 L2 low-confidence）
- RAscore Readiness：**PASS**（glossary/seeds/constraints 全綠）

整體：**FAIL**（1 blocker → NEED_TO_FIX）
| Finding | route | owner |
|---|---|---|
| FIND-20260616-001 | NEED_TO_FIX | rapt-reconcile（backfill situation_annotation_read）|
| FIND-20260616-002/003 | NOTE_ONLY | rapt-intent（L2/L3 精確化，可選）|

## Reconcile Log — RECON-20260616-001（2026-06-16）

### 已修復（can-fix，全機械性）
- [FIND-001] haARM backfill permission `situation_annotation_read`（annotator role）→ 解 CiC-BDY-INT-001
  - changed: bridge-cognitive-tutor.haarm.yaml#permissions + roles.annotator
  - basis: 鏡像既有 situation_annotation_create/update；dsl-cross-reference backfill mode
- [FIND-002] traceability L3 補 4 列（SCN-F002-003/004, SCN-F003-002/003 → play-session ops）
- [FIND-003] traceability L2 讀取型 scenario 精確化 read_tables（F005-002/F006-001/F006-002，low→medium）

### 委派釐清（need-human）
- （無）

### 驗證
- post-fix `dsl-lint.py --levels all` → **[] 0 findings, exit 0**
- snapshot：`.raptor/reconcile/archive/RECON-20260616-001/`
- session record：`.raptor/reconcile/sessions/RECON-20260616-001.yml`
- impact-matrix：IMPACT-20260616-001（applied）

### CiC 狀態
- **BDY-INT-001 已解**（backlog 全清空）

> 預期重跑 /rapt-verify：consistency PASS、整體 PASS、Phase 5 閘門通過。

## Phase 5 Verification 重跑（VERIFY-20260616-002，2026-06-16）

reconcile 後重跑，結果：**PASS（整體）** ✅
- 完整性 PASS / 一致性 **PASS**（dsl-lint 0 findings）/ 可追蹤性 PASS（L3 38/38）/ 覆蓋率 PASS（100%）
- Phase 5 閘門：**通過**（0 FAIL、can_continue: true）
- 剩 1 NOTE_ONLY（部分讀取型 L2 low-confidence，不阻擋）
- 報告：docs/reports/verify-report.md + .yml（取代 VERIFY-...-001）

RAPTor 主線（Phase 1 → 5）完成。後續可選：/rapt-RAscore（品質評分）、Preview 工具（openapi/lofi/design-brief，generated 仍 deferred）。

## RAscore

- Report: docs/reports/rascore-report.md
- Scorecard: docs/reports/rascore-scorecard.yml
- Findings JSON: docs/reports/rascore-findings.json
- Score: **95.13 / 100（Grade A）**
- Veto: 未觸發
- Advisory only: true
- 維度：A 3.0｜B 2.8｜C 3.0｜D 2.75｜E 3.0｜F 2.5｜G 2.5
- 3 個 low findings（皆 NOTE_ONLY，advisory）：RA-B4-001（部分 create 缺負向 scenario）、RA-D3-001（9 個 infra/L3-only table 非直接 # entities）、RA-F1-001（少數質性 Then）
