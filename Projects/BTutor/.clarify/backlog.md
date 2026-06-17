# Clarify Backlog

> 最後掃描：2026-06-16
> OPEN 項目：0；已解 9（CON 1 / GAP 6 / ASM 2，全數 RESOLVED via CLR-260616-01）

## CON（衝突，需裁決）

| ID | 位置 | 衝突描述 | 衝突雙方 | 狀態 |
|----|------|---------|---------|------|
| CiC-CON-001 | docs/discovery/00-source-inventory.md#sources | MVP 首要交付介面：Coach Dashboard 先行 vs Student UI 先行 | Gemini roadmap（Dashboard 最後）vs Sonnet（Dashboard 先行）；PRD 並列 | RESOLVED (Q1：Coach Dashboard 先行) |

## GAP（資訊缺失，需人工回答）

| ID | 位置 | 描述 | 影響 | 狀態 |
|----|------|------|------|------|
| CiC-GAP-006 | docs/ssot/dbml/(mastery) | Probabilistic student model 選型未定 | StudentSkillState 更新邏輯、冷啟動、資料需求 | RESOLVED (Q3：CDM DINA/DINO) |
| CiC-GAP-003 | docs/discovery/02-user-journeys.md#intermediate-player | 牌例指派方式未定 | PlaySession 建立流程、haAPI/haPDL、Assignment | RESOLVED (Q2：自選+教練派題；adaptive deferred) |
| CiC-GAP-007 | docs/discovery/04-vision-kpi-scope.md#in-scope | 首批 curated deal 數量與標注流程未定 | MVP 內容備齊、ontology 驗證、時程 | RESOLVED (Q4：10–20 副 LLM+審核) |
| CiC-GAP-BHV-001 | docs/ssot/habdd/story-index.md#cross-cutting | Dashboard 篩選排序承接方式未定 | F-006 scenario、haPDL 清單頁 | RESOLVED (Q6：MVP 納入 SCN-F006-005) |
| CiC-GAP-MOD-001 | docs/ssot/haarm/bridge-cognitive-tutor.haarm.yaml#researcher | researcher 遙測匿名化政策未定 | haAPI 查詢去識別化、PII | RESOLVED (Q7：去識別化 CON-PRIV-001) |
| CiC-GAP-005 | docs/discovery/04-vision-kpi-scope.md#kpi | KPI baseline/target 未量化 | 驗收標準、mastery 權重 | RESOLVED (Q5：pilot 後再定量) |

## ASM（假設，需確認）

| ID | 位置 | 假設內容 | 請確認 | 狀態 |
|----|------|---------|-------|------|
| CiC-ASM-002 | docs/discovery/01-stakeholders.md#parent-school | parent-school / researcher 為 MVP 邊緣角色 | parent-school 是否納入 MVP actor | RESOLVED (Q8：parent-school 納入 MVP) |

## BDY（超界）

| ID | 位置 | 描述 | 建議轉送 |
|----|------|------|---------|
| （無） | | | |

## 已解決

| ID | 位置 | 描述 | 解決方式 |
|----|------|------|---------|
| CiC-ASM-004 | docs/discovery/03-event-timeline.md#events | `system` actor 需細分為服務 actor | rapt-modeling 已建立 diagnosis-engine/student-model/explanation-layer/pattern-miner 四個 service actor |

## 結構掃描發現（A1-A6 / B1-B5 / C1-C3）

| 規則 | 位置 | 問題 | 嚴重度 |
|------|------|------|-------|
| A1-A6 | docs/ssot/dbml/schema.dbml | 無發現（所有 Table 有 PK+label、ref_code 有 seeds、sensitive 已標、Ref 完整） | — |
| B1-B5 | docs/ssot/habdd/*.ha.feature | 無發現（source/GWT/story 對應/無技術語彙/When 單一動作皆符合） | — |
| C1-C3 | docs/ssot/haarm/bridge-cognitive-tutor.haarm.yaml | C3：parent-school 無對應 role（已由 CiC-ASM-002 涵蓋）；C1/C2 無發現 | WARNING |

## RAscore Findings

| Finding | Criterion | CiC 類型 | 位置 | 問題 | 建議 |
|---------|-----------|----------|------|------|------|
| （無 — Phase 5 RAscore 尚未執行） | | | | | |
