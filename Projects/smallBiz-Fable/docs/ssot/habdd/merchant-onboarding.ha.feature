# language: zh-TW
# source: docs/discovery/02-user-journeys.md#merchant的主要旅程1
# stories: US-009, US-017
# feature-id: F-007
Feature: 商家開店與帳號管理
  In order to 以月租方式快速擁有自己的線上商店
  As a 商家
  I want to 註冊開店並由平台管理營運資格

  # scenario_id: SCN-ONBOARD-001
  # entities: 商家, 店面
  Scenario: 商家註冊開店申請
    Given 申請者尚未擁有商家帳號
    When 申請者提交商家註冊
    Then 系統建立待開通的商家帳號

  # scenario_id: SCN-ONBOARD-002
  # entities: 商家, 店面
  # 決策 CLR-260613-02#Q1：MVP 平台後台僅開通/停權，審核為人工單一步驟
  Scenario: 平台開通商家店面
    Given 商家帳號處於待開通狀態
    When 平台管理員開通該商家
    Then 商家店面進入營運狀態
    And 商家可開始上架商品

  # scenario_id: SCN-ONBOARD-003
  # entities: 商家, 店面
  Scenario: 平台停權違規商家
    Given 商家店面處於營運狀態
    When 平台管理員停權該商家
    Then 商家店面暫停營運
    And 該店商品於前台不再顯示
