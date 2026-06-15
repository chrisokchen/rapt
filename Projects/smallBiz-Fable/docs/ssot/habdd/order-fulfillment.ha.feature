# language: zh-TW
# source: docs/discovery/02-user-journeys.md#merchant的主要旅程2
# stories: US-012
# feature-id: F-010
Feature: 商家訂單處理
  In order to 一個畫面看完所有訂單、不漏單不重複出貨
  As a 商家
  I want to 篩選訂單、確認並標記出貨

  Background:
    Given 我已登入為商家
    And 商家店面處於營運狀態

  # scenario_id: SCN-FULFILL-001
  Scenario: 依狀態篩選訂單
    Given 店內有「待付款」「已付款」「已出貨」等多筆不同狀態的訂單
    When 商家依「已付款」狀態篩選訂單
    Then 僅顯示狀態為「已付款」的訂單

  # scenario_id: SCN-FULFILL-002
  # entities: 訂單
  # 決策 CLR-260613-03#ASM#008（確認）：「已付款 → 已確認」為商家手動動作（CON-ORD-001）
  Scenario: 商家確認已付款訂單
    Given 訂單狀態為「已付款」
    When 商家確認該訂單
    Then 訂單狀態變為「已確認」

  # scenario_id: SCN-FULFILL-003
  # entities: 訂單, 物流單
  Scenario: 標記出貨並填入物流單號
    Given 訂單狀態為「已確認」
    When 商家標記出貨並填入物流單號
    Then 訂單狀態變為「已出貨」
    And 消費者收到出貨通知

  # scenario_id: SCN-FULFILL-004
  # entities: 訂單, 商家
  Scenario: 無法查看其他商家的訂單
    Given 存在一筆屬於其他商家店面的訂單
    When 商家查詢非本店的訂單
    Then 查詢被拒絕
    And 系統不顯示任何該訂單的內容
