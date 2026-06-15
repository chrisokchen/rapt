# language: zh-TW
# source: docs/discovery/02-user-journeys.md#consumer的主要旅程1
# stories: US-007
# feature-id: F-012
Feature: 忠誠點數
  In order to 累積回購誘因並折抵消費
  As a 消費者
  I want to 在消費後獲得點數並於結帳時折抵

  Background:
    Given 我已登入為消費者

  # scenario_id: SCN-POINT-001
  # entities: 點數, 訂單
  # 決策 CLR-260613-01#Q4：回饋以折後實付金額計算（CON-PNT-004）
  Scenario: 訂單完成後獲得消費點數
    Given 會員完成一筆 1,000 元的訂單
    When 系統發放消費點數
    Then 會員獲得 10 點（每滿 100 元 1 點）
    And 點數餘額相應增加

  # scenario_id: SCN-POINT-002
  # entities: 點數, 訂單
  # 決策 CLR-260613-01#Q4：單筆折抵上限 50%、點數效期 1 年（CON-PNT-003/005）
  Scenario: 結帳時折抵點數
    Given 會員點數餘額為 50 點
    When 會員在結帳時折抵 30 點
    Then 訂單金額減少 30 元（1 點折 1 元）
    And 會員點數餘額變為 20 點

  # scenario_id: SCN-POINT-003
  # entities: 點數
  Scenario: 折抵超過餘額的點數被拒絕
    Given 會員點數餘額為 10 點
    When 會員在結帳時折抵 30 點
    Then 折抵不成立
    And 訂單金額維持不變
