# language: zh-TW
# source: docs/discovery/02-user-journeys.md#促銷活動操作
# stories: US-016
# feature-id: F-014
Feature: 優惠券
  In order to 行銷拉新而不被無門檻券外流薅羊毛
  As a 商家
  I want to 發行有門檻、張數上限與效期的優惠券

  # scenario_id: SCN-COUPON-001
  # entities: 優惠券
  Scenario: 發行優惠券
    Given 商家已設定折扣方式、最低消費門檻、總使用張數上限與有效期間
    When 商家發行該優惠券
    Then 優惠券具有唯一代碼並可供消費者使用

  # scenario_id: SCN-COUPON-002
  # entities: 優惠券, 訂單
  Scenario: 達門檻訂單成功套用優惠券
    Given 訂單金額達到優惠券的最低消費門檻
    When 消費者套用該優惠券
    Then 訂單金額依券面折扣方式減少

  # scenario_id: SCN-COUPON-003
  # entities: 優惠券, 訂單
  Scenario: 未達最低消費門檻無法套用
    Given 訂單金額未達優惠券的最低消費門檻
    When 消費者套用該優惠券
    Then 套用不成立
    And 訂單金額維持不變

  # scenario_id: SCN-COUPON-004
  # entities: 優惠券, 訂單
  Scenario: 一筆訂單最多使用一張優惠券
    Given 訂單已套用一張優惠券
    When 消費者套用第二張優惠券
    Then 第二張優惠券套用不成立

  # scenario_id: SCN-COUPON-005
  # entities: 優惠券
  Scenario: 總使用張數達上限後無法套用
    Given 優惠券的總使用張數已達上限
    When 消費者套用該優惠券
    Then 套用不成立
    And 消費者收到優惠券已被領完的提示

  # scenario_id: SCN-COUPON-006
  # entities: 優惠券, 會員
  # 決策 CLR-260613-01#Q4：會員四級確立（CON-MBR-003）；等級升降級見 member-tier.ha.feature（門檻金額 deferred-needs-decision）
  Scenario: 等級限定券拒絕不符資格的會員
    Given 優惠券限定特定會員等級才能使用
    And 消費者的會員等級不符合限定
    When 消費者套用該優惠券
    Then 套用不成立
    And 消費者收到不符使用資格的提示
