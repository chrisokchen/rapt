# source: docs/discovery/04-vision-kpi-scope.md#範圍邊界
# stories: US-012, US-013
Feature: 會員與忠誠點數
  In order to 累積回頭客並支援分級行銷
  As a 一般網購消費者
  I want to 註冊會員、累積點數並取得會員權益

  Background:
    Given 商店支援會員與點數制度
    And 消費者可用 Email 成為會員

  # scenario_id: SCN-MEMBER-001
  # entities: 會員, Email
  Scenario: 使用 Email 註冊會員
    Given 消費者尚未以該 Email 成為會員
    When 消費者註冊會員
    Then 系統建立一筆待驗證會員資料
    And 該 Email 不能被重複註冊

  # scenario_id: SCN-MEMBER-002
  # entities: 會員, 點數, 訂單
  Scenario: 依消費金額累積點數
    Given 會員完成一筆可回饋點數的訂單
    When 系統結算會員點數
    Then 會員點數依「消費 100 元得 1 點」增加
    And 點數異動可被會員與商家追蹤

  # scenario_id: SCN-MEMBER-003
  # entities: 會員, 點數, 訂單
  Scenario: 使用點數折抵訂單
    Given 會員擁有可使用點數
    When 會員在訂單中使用點數折抵
    Then 訂單金額依「1 點折抵 1 元」減少
    And 會員可使用點數同步減少

  # scenario_id: SCN-MEMBER-004
  # entities: 會員, 會員等級, 優惠券
  Scenario: 會員等級符合專屬優惠資格
    Given 會員已有一個會員等級
    When 系統判定會員是否符合專屬優惠資格
    Then 符合資格的會員可使用該等級優惠
    And 不符合資格的會員不取得該優惠資格

  # scenario_id: SCN-MEMBER-005
  # entities: 會員, 會員等級, 點數
  Scenario: 會員分級與點數生命週期已依釐清決策裁決
    Given 平台需要判定會員等級與點數效期
    When 系統需要套用會員規則
    Then 此情境遵循 DEC-CLR-003 的會員忠誠規則
    And 後續規格必須以 MVP 手動維護會員分級為準
  # clarification_decision: DEC-CLR-003
  # source: .clarify/decisions/batch-CLR-260613-001.md#q3-cic-gap-003會員分級與點數生命週期
  # scenario_id: SCN-MEMBER-006
  # entities: 會員, 會員等級, 點數
  Scenario: MVP 啟用點數並手動維護會員分級
    Given 消費者完成可累積點數的訂單
    When 系統處理會員忠誠規則
    Then 系統累積可折抵訂單的點數
    And 會員分級由商家或平台手動維護
    And 自動升降級排程延後到後續版本
