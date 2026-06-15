# source: docs/discovery/02-story-index.md#US-001
# feature-id: F-001
Feature: 案件覆核
  In order to 確保案件決策有雙人覆核
  As a 審核主管
  I want to 檢視待覆核案件並記錄覆核結果

  Scenario: 主管核准待覆核案件
    Given 待覆核案件已由承辦人送出
    When 審核主管核准案件
    Then 案件狀態應變更為已核准
    And 系統應留下覆核紀錄
