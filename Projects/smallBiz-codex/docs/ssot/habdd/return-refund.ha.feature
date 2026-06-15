# source: docs/discovery/02-user-journeys.md#一般網購消費者的主要旅程從瀏覽到售後
# stories: US-015
Feature: 退貨與退款
  In order to 讓售後流程簡單且可追蹤
  As a 一般網購消費者
  I want to 申請退貨並取得審核、取件與退款進度

  Background:
    Given 我以一般網購消費者身分使用商店
    And 我有一筆已送達訂單

  # scenario_id: SCN-RETURN-001
  # entities: 訂單, 退貨申請
  Scenario: 消費者申請退貨
    Given 訂單符合目前已知的退貨申請條件
    When 消費者申請退貨
    Then 系統建立一筆退貨申請
    And 退貨申請狀態成為「待審核」

  # scenario_id: SCN-RETURN-002
  # entities: 退貨申請, 物流, 退款
  Scenario: 商家核准退貨後安排取件
    Given 退貨申請狀態為「待審核」
    When 商家核准退貨申請
    Then 退貨申請狀態成為「已核准」
    And 消費者取得退貨取件安排

  # scenario_id: SCN-RETURN-003
  # entities: 退貨申請, 退款, 訂單
  Scenario: 退回商品確認後完成退款
    Given 退貨商品已被商家確認收回
    When 系統完成退款
    Then 訂單狀態成為「已退款」
    And 消費者取得退款完成通知

  # scenario_id: SCN-RETURN-004
  # entities: 退貨申請, 訂單
  Scenario: 退貨政策已依釐清決策裁決
    Given 消費者要退回特價商品或已拆封商品
    When 系統需要判定退貨資格
    Then 此情境遵循 DEC-CLR-006 的退貨政策
    And 後續規格必須以到貨後 7 天內可退與原路退款為準
  # clarification_decision: DEC-CLR-006
  # source: .clarify/decisions/batch-CLR-260613-002.md#q6-cic-gap-006退貨期限不可退範圍與退款路徑
  # scenario_id: SCN-RETURN-005
  # entities: 退貨申請, 訂單, 退款
  Scenario: 依決策審核退貨期限與退款路徑
    Given 消費者在到貨後 7 天內申請退貨
    When 商品不是已拆封商品、個人化商品或耗材
    Then 系統允許建立退貨申請
    And 商家核准後退款必須原路退回
    Given 消費者申請退貨的商品已拆封、個人化或屬於耗材
    When 系統檢查退貨資格
    Then 系統拒絕退貨申請
