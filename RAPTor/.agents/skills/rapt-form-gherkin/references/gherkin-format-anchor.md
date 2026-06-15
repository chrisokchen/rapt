# Gherkin Format Anchor

> **重要聲明**：DSLspec v3.3 takes precedence over this anchor's examples.  
> 本文件只作為「快速格式參考」；若本文件與 `RAPTor/DSLspec/` 有任何衝突，以 DSLspec 為準。

本文件是 `rapt-form-gherkin` 的格式錨點。高階 Gherkin 沒有專屬 DSLspec，但有以下共識格式。

---

## 高階 Gherkin 檔案結構

```gherkin
# source: <source_evidence 引用>
# feature-id: F-{NNN}
Feature: <業務能力名稱>
  In order to <業務價值（為什麼）>
  As a <主要角色>
  I want to <核心能力（做什麼）>

  Background:
    Given 我已登入為 <role>
    And <系統前提狀態>

  # --- Scenario 分組標題（可選）---

  Scenario: <正向場景名稱>
    Given <前置業務狀態>
    When <使用者的一個業務動作>
    Then <業務結果1>
    And <業務結果2（可選）>

  Scenario: <例外場景名稱>
    Given <前置業務狀態>
    When <觸發例外的業務動作>
    Then <例外的業務結果>

  Scenario Outline: <可參數化場景>
    Given <含 <param> 的前置狀態>
    When <含 <param> 的業務動作>
    Then <含 <result> 的業務結果>
    Examples:
      | param | result |
      | ...   | ...    |
```

---

## 格式規則

| 項目 | 規則 |
|------|------|
| 縮排 | 2 spaces |
| 語言宣告 | 若用中文：開頭加 `# language: zh-TW`（可選）|
| Feature 標題 | 使用業務能力的**名詞**，不用動詞 |
| Scenario 標題 | 用**句子**描述場景，含正向/例外/邊界 |
| When 步驟 | 只有一個業務動作；多動作拆多 Scenario |
| 業務術語 | 一致引用 Stakeholder / Event Timeline 定義 |
| source comment | 每個 Feature 必須有 `# source: <ref>` |

---

## 與 Low-level Gherkin 的邊界

| 項目 | 高階 Gherkin（本 anchor）| Low-level Gherkin（deferred）|
|------|------------------------|-----------------------------|
| 目的 | 業務規格 SSoT | E2E 測試執行 |
| 語言 | 業務語言 | 技術語言 |
| 含 selector | ❌ 禁止 | ✅ 必要 |
| 含 API URL | ❌ 禁止 | ✅ 必要 |
| 含 HTTP method | ❌ 禁止 | ✅ 必要 |
| 由誰產生 | rapt-form-gherkin | Wave 7（deferred）|

---

## 常用 step 語句模板

```gherkin
# Given（前置狀態）
Given 我已登入為 <角色>
Given <業務物件> 狀態為「<狀態>」
Given <業務前提條件>

# When（業務動作）
When <角色> 提交 <業務物件>
When <角色> 批准 <業務請求>
When <角色> 取消 <業務操作>
When 系統自動觸發 <業務事件>

# Then（業務結果）
Then <業務物件> 狀態變為「<狀態>」
Then <角色> 收到 <業務通知>
Then 系統記錄 <業務事件>
Then <業務規則> 被執行
```
