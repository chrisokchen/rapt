# language: zh-TW
# source: docs/discovery/02-user-journeys.md#merchant的主要旅程2
# stories: US-014
# feature-id: F-015
Feature: 商家報表
  In order to 看得懂銷售狀況、進貨有依據
  As a 商家
  I want to 查看極簡的銷售概況與商品排行

  Background:
    Given 我已登入為商家
    And 店內有交易資料

  # scenario_id: SCN-REPORT-001
  Scenario: 查看期間銷售概況
    Given 商家選定一個查詢期間
    When 商家查看銷售概況
    Then 顯示該期間的訂單數、營業額與客單價

  # scenario_id: SCN-REPORT-002
  Scenario: 查看商品排行
    Given 商家選定一個查詢期間
    When 商家查看商品排行
    Then 顯示該期間的暢銷商品與滯銷商品清單
