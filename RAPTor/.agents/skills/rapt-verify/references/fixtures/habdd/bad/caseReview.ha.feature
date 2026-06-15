Feature: 案件覆核 API 測試
  Scenario: 直接呼叫核准 API
    Given 使用者點擊 #approve-button
    When POST /api/cases/123/approve
    Then response status should be 200
