# source: docs/discovery/03-event-timeline.md#庫存
# stories: US-005, US-006
Feature: 庫存控制
  In order to 避免超賣並提升庫存準確度
  As a 中小零售店老闆 / 商家
  I want to 以 SKU 維護庫存並在訂單流程中扣減庫存

  Background:
    Given 我已登入為中小零售店老闆 / 商家
    And 商家已有可販售 SKU

  # scenario_id: SCN-INV-001
  # entities: SKU, 庫存水位
  Scenario: 設定 SKU 庫存與補貨水位
    Given 商家準備販售一個 SKU
    When 商家設定庫存數量與低庫存水位
    Then SKU 具有可販售庫存與補貨門檻
    And 商家可用庫存狀態安排補貨

  # scenario_id: SCN-INV-002
  # entities: SKU, 庫存異動, 訂單
  Scenario: 訂單成立後扣減庫存
    Given 消費者提交的訂單包含一個有庫存的 SKU
    When 系統依訂單規則扣減庫存
    Then SKU 可販售庫存減少訂購數量
    And 訂單保留扣減後的庫存結果

  # scenario_id: SCN-INV-003
  # entities: SKU, 庫存水位
  Scenario: 庫存低於水位時提醒商家
    Given SKU 庫存已低於商家設定的補貨水位
    When 系統檢查庫存狀態
    Then 商家取得該 SKU 需要補貨的通知
    And 商品仍呈現目前可販售狀態

  # scenario_id: SCN-INV-004
  # entities: SKU, 訂單
  Scenario: 庫存不足時不建立可履約訂單
    Given 消費者的購買數量大於 SKU 可販售庫存
    When 消費者提交訂單
    Then 訂單未進入可履約狀態
    And SKU 可販售庫存維持不變

  # scenario_id: SCN-INV-005
  # entities: SKU, 訂單
  Scenario: 庫存預留規則已依釐清決策裁決
    Given 多位消費者同時購買同一個低庫存 SKU
    When 系統需要判定庫存歸屬
    Then 此情境遵循 DEC-CLR-001 的庫存預留規則
    And 後續規格必須以 30 分鐘逾時取消與預留釋放為準
  # clarification_decision: DEC-CLR-001
  # source: .clarify/decisions/batch-CLR-260613-001.md#q1-cic-gap-001庫存扣減與預留策略
  # scenario_id: SCN-INV-006
  # entities: SKU, 庫存預留, 訂單
  Scenario: 依決策建立庫存預留並於付款完成扣減
    Given 消費者提交包含庫存商品的訂單
    When 訂單成立但尚未付款
    Then 系統建立庫存預留並鎖定可販售庫存
    And 付款完成時正式扣減庫存
    And 未付款訂單逾時取消時釋放預留庫存
