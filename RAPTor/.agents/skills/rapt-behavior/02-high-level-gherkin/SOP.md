# 02 High-Level Gherkin SOP

**目的**：將 User Story 轉換為高階 Gherkin feature files（SSoT），一個 Feature = 一個 `.feature` 檔案。

---

## 前提

LOAD REF [rapt-behavior::rules/high-level-gherkin-rules.md]
LOAD REF [rapt-behavior::rules/cross-cutting-scenario-checklist.md]
LOAD REF [rapt-behavior::rules/test-readiness-gherkin-rules.md]

---

## 步驟

### 2.1 GROUP stories into Features

對 `story-index.md` 中的 must-have / should-have stories，依業務能力分群：

```
分群原則：
  - 同一業務能力的多個故事 → 同一個 Feature
  - 跨能力的故事 → 不同 Feature
  - 一個 Feature 建議有 3-8 個 Scenario
```

### 2.2 DERIVE Feature 內容

對每個 Feature 群組，DERIVE：

```gherkin
# source: <discovery/story refs>
# stories: US-001, US-004
Feature: <業務能力名稱（中英文皆可）>
  In order to <業務價值>
  As a <primary actor>
  I want to <核心能力>

  Background:
    Given 我已登入為 <role>          # 引用 haARM role（未來對應）
    And 系統處於 <前提狀態>

  # scenario_id: SCN-<FEATURE>-001
  # entities: <業務實體1>, <業務實體2>
  Scenario: <具體業務場景>
    Given <前置業務狀態>
    When <使用者做了什麼業務動作>
    Then <預期的業務結果>
    And <其他業務結果>

  Scenario Outline: <可參數化的場景>
    Given ...
    When ...
    Then ...
    Examples:
      | 參數1 | 參數2 |
      | ...   | ...   |
```

### 2.3 VALIDATE 反規則

LOAD REF [rapt-behavior::rules/high-level-gherkin-rules.md]

對每個 Scenario 執行反規則檢查：
- 無 click / button / page / URL / HTTP / selector / form submit
- 無技術系統名稱（MySQL / Redis / JWT）
- 每個 Scenario 有 Given-When-Then 完整三段
- When 只有一個動作（不堆疊）
- Then 只有一個可觀察業務結果集合，不含「阻擋或警示」「拒絕或要求先清除」等替代策略
- 資料依賴 Scenario 有本地 Given，不只依賴 Background
- 資料變更 / 授權 / 狀態轉換 Scenario 有 `# entities:` comment
- 建立 / 修改 / 刪除 / 匯入 / 批次操作有至少一個負向 Scenario，或在 story-index matrix 標註不適用 / deferred

違反者：修正後繼續；無法修正者記 CiC `BDY`。

### 2.4 VALIDATE Cross-Cutting Capability Matrix

對 `story-index.md` 的 Cross-Cutting Capability Matrix：

- `handling=scenario` 必須能連到 feature/scenario。
- `handling=deferred` 必須有 decision_ref 或 OPEN CiC。
- `handling=open-cic` 必須建立 CiC。
- 不允許 scope 明列能力但 matrix 無列。

### 2.5 DELEGATE `rapt-form-gherkin` 渲染每個 Feature 檔案

對每個 Feature，DELEGATE to `rapt-form-gherkin`：

```yaml
payload:
  target_path: "${high_gherkin_dir}/{feature-slug}.feature"
  source_evidence:
    - type: discovery
      ref: "${disc_dir}02-user-journeys.md#{相關步驟}"
    - type: story
      ref: "story-index.md#US-{id}"
  content:
    feature_name: <名稱>
    in_order_to: <業務價值>
    as_a: <actor>
    i_want_to: <核心能力>
    background: <前提>
    scenarios: [<list of derived scenarios with scenario_id and entities>]
  dsl_version: "3.3.0"
  write_mode: create
```

### 2.6 UPDATE `story-index.md`

為每個 User Story 補上 Feature 連結。

### 2.7 UPDATE `${paths.traceability_file}` L1/L2 草稿

依 `rapt-core::traceability-schema.md` 寫入或更新：

- L1 Requirement Coverage：story → feature / scenario。
- L2 Scenario Data Mapping 草稿：scenario_id、feature、scenario、entities、source。

不得填入沒有證據的 DBML table / field。

---

## 輸出完成條件

```
□ 每個 must-have story 對應至少一個 Scenario
□ 每個 Feature 有 ≥1 個 Scenario
□ story-index.md Feature 連結欄位已填
□ Cross-Cutting Capability Matrix 已填
□ 無技術語彙（通過 rules 檢查）
□ Then 無替代策略
□ 資料變更 / 授權 / 狀態轉換 Scenario 有 # entities:
□ traceability.md L1/L2 草稿已更新
□ 每個 Feature 有 source_evidence
```
