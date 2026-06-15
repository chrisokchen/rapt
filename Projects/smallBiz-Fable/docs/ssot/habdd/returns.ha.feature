# language: zh-TW
# source: docs/discovery/02-user-journeys.md#consumer的主要旅程2
# stories: US-008, US-013
# feature-id: F-011
Feature: 退換貨
  In order to 讓退貨有規則可循且不需紙本流程
  As a 消費者
  I want to 在線上申請退貨並追蹤退款

  # scenario_id: SCN-RETURN-001
  # entities: 退貨申請, 訂單
  # 決策 CLR-260613-01#Q3：退貨期限 7 天（自到貨日起算，CON-RTN-001）
  Scenario: 線上申請退貨
    Given 訂單已送達且仍在退貨期限內
    When 消費者對該訂單申請退貨
    Then 系統建立待審核的退貨申請
    And 全程不需要紙本表單

  # scenario_id: SCN-RETURN-002
  # entities: 退貨申請, 物流單
  Scenario: 商家核准退貨並安排取件
    Given 退貨申請處於待審核狀態
    When 商家核准該退貨申請
    Then 系統安排物流上門取件
    And 消費者收到取件安排通知

  # scenario_id: SCN-RETURN-003
  # entities: 退貨申請
  Scenario: 商家拒絕退貨申請
    Given 退貨申請處於待審核狀態
    When 商家拒絕該退貨申請
    Then 退貨申請狀態變為「已拒絕」
    And 消費者收到含拒絕原因的通知

  # scenario_id: SCN-RETURN-004
  # entities: 訂單, 退款
  # 決策 CLR-260613-01#Q3：退款一律原路退回
  Scenario: 確認退回商品後退款
    Given 退貨商品已退回且商家確認無誤
    When 系統執行退款
    Then 訂單狀態變為「已退款」
    And 消費者收到退款完成通知

  # scenario_id: SCN-RETURN-005
  # entities: 退貨申請
  Scenario: 超過退貨期限的申請不成立
    Given 訂單已超過退貨期限
    When 消費者對該訂單申請退貨
    Then 退貨申請不成立
    And 消費者收到已超過期限的提示
