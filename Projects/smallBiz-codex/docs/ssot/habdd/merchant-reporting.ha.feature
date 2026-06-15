# source: docs/discovery/02-user-journeys.md#中小零售店老闆--商家的主要旅程建立並營運線上商店
# stories: US-016
Feature: 商家營運報表
  In order to 用資料支援補貨與營運判斷
  As a 中小零售店老闆 / 商家
  I want to 查看銷售概況與商品排行

  Background:
    Given 我已登入為中小零售店老闆 / 商家
    And 商家已有訂單與商品銷售資料

  # scenario_id: SCN-REPORT-001
  # entities: 報表, 訂單, 銷售摘要
  Scenario: 查看指定期間的銷售概況
    Given 商家選定一段報表期間
    When 商家查看銷售概況
    Then 商家取得該期間的訂單數、營業額與客單價
    And 商家可用報表判斷營運表現

  # scenario_id: SCN-REPORT-002
  # entities: 報表, 商品
  Scenario: 查看商品銷售排行
    Given 商家選定一段報表期間
    When 商家查看商品排行
    Then 商家取得暢銷商品與滯銷商品清單
    And 商家可用排行安排補貨與促銷

  # scenario_id: SCN-REPORT-003
  # entities: 報表, 商家
  Scenario: 無銷售資料時呈現空報表
    Given 商家在指定期間沒有任何訂單
    When 商家查看銷售概況
    Then 商家取得零銷售的報表結果
    And 報表不產生誤導性的銷售數字
