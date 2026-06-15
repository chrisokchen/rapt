# Phase Gates — 各 Phase 品質閘門

本文件定義 RAPTor 七個 Phase 的完成條件（品質閘門）。當某 Phase 的閘門條件**全部通過**，才允許進入下一 Phase。

---

## Phase 1：Business Discovery（rapt-discovery）

**閘門條件（全部通過才可進 Phase 1.5）**

```
□ 至少一份 discovery 文件已讀取並摘要
□ Stakeholder list 存在（至少 2 個角色）
□ Event timeline / 業務流程草圖 存在
□ Vision statement 存在（1-2 句）
□ 至少 2 個 KPI / 成功指標
□ 範圍邊界明確（in-scope / out-of-scope）
```

---

## Phase 1.5：High-Level Gherkin（rapt-behavior）

**閘門條件（全部通過才可進 Phase 2）**

```
□ 至少 1 個 .feature 檔案存在
□ 每個 Feature 有 ≥1 個 Scenario
□ 無技術語彙（click / button / URL / HTTP / selector）
□ 每個 Feature 有 source_evidence 指向 Phase 1 的 discovery doc
□ story-index.md 存在，包含所有 Feature 的摘要
□ 若 scope 明列共通管理能力，story-index.md 必須標註 Scenario / deferred / out-of-scope 承接方式
□ Then 不含替代策略（例如「阻擋或警示」「拒絕或要求先清除」）
□ traceability.md L1/L2 草稿存在
□ 每個資料變更 / 授權 / 狀態轉換 Scenario 至少有 # entities: 標註
```

---

## Phase 2：Domain Modeling（rapt-modeling）

**閘門條件（全部通過才可進 Phase 3）**

```
□ schema.dbml 存在，包含所有核心 Table
□ 每個 Table 的 PK 欄位有 label:
□ 每個 sensitive 欄位有 sensitive: true
□ haARM .haarm.yaml 存在，resource 數量 ≥ Table 數量的 50%
□ haARM roles 包含所有 Stakeholder 角色
□ DBML ref_code: 欄位有 seeds.md 值域或 OPEN CiC
□ 高風險狀態 / 權限 / 刪除限制有 constraints.md constraint_id 或 OPEN CiC
□ compatibility decision 有 compensating rule
□ Ubiquitous language glossary 存在（≥5 個術語）
□ glossary.md 符合 canonical mapping schema
□ 無 AP-01~AP-05 反模式（dbml-v33 / haarm-v33 rules）
```

---

## Phase 3：Clarification（rapt-clarify）

**閘門條件（全部通過才可進 Phase 4）**

```
□ .clarify/backlog.md 中無 OPEN 的 GAP 或 CON
□ 所有 ASM 均已確認（CONFIRMED 或 REJECTED）
□ Decision log 存在（至少對應所有 GAP 的決策）
□ SSoT 已按 decision log 更新（04-decision-apply 完成）
□ 已 RESOLVED 的 CiC 在 source/discovery 原文件中標記 RESOLVED + 決策引用
□ deferred 項目有 deferred-mvp-out / deferred-needs-decision / accepted-risk 三者之一的明確狀態
```

---

## Phase 4：Spec Formulation（rapt-intent）

**閘門條件（全部通過才可進 Phase 5）**

```
□ 每個主要 SSoT Table 有對應的 .haapi.yaml
□ 每個主要 .haapi.yaml 有對應的 .hapdl.yaml（至少 list + form）
□ 無 legacy 欄位：access.permissions:、security.permissions:
□ traceability.md L2/L3 完整到 Scenario-level
□ haARM backfill 完成（無 OPEN BDY CiC 關於 missing role/permission）
```

---

## Phase 5：Validation（rapt-verify）

**閘門條件（全部通過才可進 Phase 6）**

```
□ rapt-verify 報告存在（{reports_dir}/verify-report.md）
□ 0 個 FAIL 項目（跨 DSL 引用一致性）
□ WARN 項目已評估（記錄為 accepted / to-fix）
□ 高階 Gherkin → haAPI 覆蓋率 ≥ 80%
□ 所有 haAPI entity 可對應 DBML Table
□ 所有 haPDL api: 可對應 haAPI api:
□ verify-report.md 產出 RAscore Readiness section
```

---

## Phase 6：Prototype（超出本 v1 skill 範圍）

> Wave 7 延後實作。本版 skill 不執行此 Phase。

---

## Phase 7：Iteration

> 迭代回 Phase 3 或 Phase 1.5，依 rapt-verify 報告的問題類型決定。

---

## 閘門失敗的處理

| 失敗情境 | 處理 |
|---------|------|
| 資料不足 | 記 CiC `GAP`，DELEGATE to rapt-clarify |
| 跨 DSL 不一致 | DELEGATE to rapt-reconcile |
| 格式反模式 | DELEGATE to 對應 rapt-form-* Worker 修正 |
| 範圍超出 | EMIT 警告，請使用者決策 |
