# 01 Gap Scan SOP

**目的**：掃描所有 SSoT artifact 中的 CiC 便條（GAP/ASM/BDY/CON），以及執行結構性掃描規則（A1-A6、B1-B5、C1-C3），建立完整的 backlog。

---

## 前提

LOAD REF [rapt-clarify::rules/data-model-scan-a1-a6.md]  
LOAD REF [rapt-clarify::rules/feature-model-scan-b1-b5.md]  
LOAD REF [rapt-clarify::rules/access-control-scan.md]
LOAD REF [rapt-clarify::rules/rascore-finding-scan.md]

---

## 步驟

### 1.1 SCAN CiC 便條

SEARCH 以下路徑中的 `<!-- CiC` 標記：

```
${paths.data_model_dir}/**
${paths.access_control_dir}/**
${paths.high_gherkin_dir}/**
${paths.business_discovery_dir}/**
```

對每個找到的 CiC 便條，記錄：

```
- id: CiC-{YYMMDD}-{seq}
- type: GAP | ASM | BDY | CON
- location: <檔案路徑>#<行號或節標題>
- description: <便條描述>
- impact: <影響的下游 artifact>
- status: OPEN
```

### 1.2 EXECUTE Structural Scan

執行結構性掃描（不依賴 CiC 便條，主動找問題）：

**資料模型掃描**（LOAD REF `rules/data-model-scan-a1-a6.md`）：
- A1：DBML Table 有無 PK
- A2：DBML Column 有無 label
- A3：status 欄位有無 ref_code
- A4：外鍵有無 Ref 宣告
- A5：sensitive 欄位是否標注
- A6：group 是否重複定義（DBML + haPDL）

**行為模型掃描**（LOAD REF `rules/feature-model-scan-b1-b5.md`）：
- B1：Feature 有無 source_evidence
- B2：Scenario 有無完整 G-W-T
- B3：Story 有無對應 Feature
- B4：Feature 有無技術語彙
- B5：Scenario 中 When 有無多個動作

**存取控制掃描**（LOAD REF `rules/access-control-scan.md`）：
- C1：haARM resource 有無對應 DBML Table
- C2：end-user role 有無 scope: all（AP-04）
- C3：haARM role 有無對應所有 Stakeholder actor

### 1.3 SCAN RAscore findings

若存在，READ：

```
${paths.reports_dir}/rascore-findings.json
${paths.reports_dir}/rascore-findings.md
${paths.reports_dir}/rascore-scorecard.yml
```

依 `rules/rascore-finding-scan.md` 將 findings 轉成 backlog：

- coverage-loss / deferred → GAP
- scope-creep → BDY 或 CON
- dbml-quality 值域 / constraint → GAP
- gherkin-quality 替代結果 → CON
- traceability source 不同步 → ASM

每個 RAscore backlog item 必須保留 `finding_id`、`criterion`、`artifact`、`location`、`recommendation`。

### 1.4 WRITE `${clarify_dir}backlog.md`

```markdown
# Clarify Backlog

> 最後掃描：{date}
> OPEN 項目：{N}

## GAP（資訊缺失，需人工回答）

| ID | 位置 | 描述 | 影響 |
|----|------|------|------|
| CiC-{id} | ... | ... | ... |

## ASM（假設，需確認）

| ID | 位置 | 假設內容 | 請確認 |
|----|------|---------|-------|

## BDY（超界，需轉 reconcile/clarify）

| ID | 位置 | 描述 | 建議轉送 |
|----|------|------|---------|

## CON（衝突，需裁決）

| ID | 位置 | 衝突描述 | 衝突雙方 |
|----|------|---------|---------|

## 結構掃描發現（A1-A6 / B1-B5 / C1-C3）

| 規則 | 位置 | 問題 | 嚴重度 |
|------|------|------|-------|

## RAscore Findings

| Finding | Criterion | CiC 類型 | 位置 | 問題 | 建議 |
|---------|-----------|----------|------|------|------|
```
