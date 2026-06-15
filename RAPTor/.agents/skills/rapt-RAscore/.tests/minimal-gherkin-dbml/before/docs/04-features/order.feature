Feature: 訂單管理

  Scenario: 客戶取消未付款訂單
    Given 客戶已有一筆未付款訂單
    When 客戶取消訂單
    Then 訂單狀態應為已取消

  Scenario: 客戶按下取消按鈕
    Given 客戶在訂單頁面
    When 客戶點擊取消按鈕
    Then 系統顯示成功訊息

