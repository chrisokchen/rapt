# haBDD Pattern Rules

haBDD 是高階業務行為 SSoT，檔名建議使用 `*.ha.feature`，內容保持 business-readable，不包含 selector、HTTP method、API path、test id 或其他 implementation literal。

## Required Header

```gherkin
# source: docs/discovery/02-story-index.md#US-001
# feature-id: F-001
Feature: <業務能力名稱>
```

## Scenario Rules

- 每個 Scenario 應有一個清楚的 `When` business action。
- `Given` 描述業務前置狀態，不描述 UI 操作或資料庫 setup。
- `Then` 描述業務結果、狀態、通知、稽核紀錄或使用者可觀察結果。
- `Scenario Outline` 只用於業務參數組合，不用來列 UI selector 或 API payload。

## Forbidden Literals

以下內容屬於 generated isaBDD/e2e，不可放入 haBDD：

- CSS selector：`#submit`、`.button-primary`
- test id：`data-testid`
- URL 或 API path：`https://...`、`/api/...`
- HTTP method：`GET`、`POST`、`PUT`、`PATCH`、`DELETE`

## Good

```gherkin
# source: docs/discovery/02-story-index.md#US-001
# feature-id: F-001
Feature: 案件覆核
  Scenario: 主管核准待覆核案件
    Given 待覆核案件已由承辦人送出
    When 審核主管核准案件
    Then 案件狀態應變更為已核准
```

## Bad

```gherkin
Feature: 案件覆核 API 測試
  Scenario: 直接呼叫核准 API
    Given 使用者點擊 #approve-button
    When POST /api/cases/123/approve
    Then response status should be 200
```
