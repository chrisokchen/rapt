# language: zh-TW
# source: docs/discovery/02-user-journeys.md#consumer的主要旅程1
# stories: US-001
# feature-id: F-001
Feature: 會員帳號
  In order to 取得會員身分以便購物、累點與查詢訂單
  As a 消費者
  I want to 註冊會員帳號並管理我的基本資料

  # scenario_id: SCN-MEMBER-001
  # entities: 會員
  Scenario: 以 Email 成功註冊會員
    Given 該 Email 尚未被任何會員使用
    When 消費者以 Email 提交會員註冊
    Then 系統建立待驗證的會員帳號
    And 系統發送信箱驗證信給消費者

  # scenario_id: SCN-MEMBER-002
  # entities: 會員
  Scenario: 完成信箱驗證後會員生效
    Given 消費者已註冊且帳號處於待驗證狀態
    When 消費者完成信箱驗證
    Then 會員帳號生效並可開始購物

  # scenario_id: SCN-MEMBER-003
  # entities: 會員
  Scenario: 重複 Email 註冊被拒絕
    Given 該 Email 已被其他會員註冊
    When 消費者以相同 Email 提交會員註冊
    Then 註冊不成立
    And 消費者收到 Email 已被使用的提示

  # scenario_id: SCN-MEMBER-004
  # entities: 會員, 收件地址
  Scenario: 儲存常用收件地址
    Given 會員帳號已生效
    When 會員儲存一筆常用收件地址
    Then 該地址出現在會員的常用地址清單
    And 結帳時可直接選用該地址
