# source: docs/discovery/03-event-timeline.md#訂單與履約
# stories: US-010, US-011, US-018
Feature: 訂單履約與狀態通知
  In order to 減少漏單並讓消費者掌握配送進度
  As a 中小零售店老闆 / 商家
  I want to 管理訂單狀態、出貨與通知

  Background:
    Given 我已登入為中小零售店老闆 / 商家
    And 商家已有消費者提交的訂單

  # scenario_id: SCN-ORDER-001
  # entities: 訂單, 訂單狀態
  Scenario: 依狀態查看待處理訂單
    Given 商家有多筆不同狀態的訂單
    When 商家依訂單狀態查看訂單
    Then 商家取得符合該狀態的訂單清單
    And 商家可判斷下一批待處理訂單

  # scenario_id: SCN-ORDER-002
  # entities: 訂單, 出貨, 物流
  Scenario: 標記訂單出貨
    Given 訂單狀態為「已確認」
    When 商家標記訂單出貨
    Then 訂單狀態成為「已出貨」
    And 訂單包含可追蹤的物流資訊

  # scenario_id: SCN-ORDER-003
  # entities: 訂單, 物流
  Scenario: 消費者追蹤配送進度
    Given 訂單已有物流資訊
    When 消費者查看訂單進度
    Then 消費者取得目前訂單狀態與配送狀態
    And 消費者能判斷商品是否已送達

  # scenario_id: SCN-ORDER-004
  # entities: 訂單, 通知
  Scenario Outline: 訂單狀態變更時通知消費者
    Given 消費者有一筆訂單
    When 訂單狀態成為「<狀態>」
    Then 消費者收到對應狀態通知
    And 訂單保留通知已送出的紀錄

    Examples:
      | 狀態 |
      | 已確認 |
      | 已出貨 |
      | 配送中 |

  # scenario_id: SCN-ORDER-005
  # entities: 訂單, 退款, 庫存
  Scenario: 付款逾時與取消規則已依釐清決策裁決
    Given 訂單狀態為「待付款」
    When 系統需要判定訂單是否逾時
    Then 此情境遵循 DEC-CLR-004 的訂單保留規則
    And 後續規格必須以 30 分鐘未付款自動取消為準
  # clarification_decision: DEC-CLR-004
  # source: .clarify/decisions/batch-CLR-260613-001.md#q4-cic-gap-004付款逾時取消與退款
  # scenario_id: SCN-ORDER-006
  # entities: 訂單, 退款, 庫存
  Scenario: 依決策處理付款逾時與出貨前取消
    Given 消費者建立訂單後尚未付款
    When 訂單超過 30 分鐘仍未付款
    Then 系統自動取消訂單
    And 系統釋放該訂單的預留庫存
    Given 訂單已付款但尚未出貨
    When 消費者取消訂單
    Then 系統建立原路退款流程
