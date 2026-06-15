# language: zh-TW
# source: docs/discovery/02-user-journeys.md#consumer的主要旅程1
# stories: US-005
# feature-id: F-005
Feature: 付款與發票
  In order to 安全付款並取得發票
  As a 消費者
  I want to 以慣用的付款方式完成訂單付款

  # scenario_id: SCN-PAY-001
  # entities: 訂單, 付款
  Scenario: 信用卡付款成功
    Given 訂單處於「待付款」狀態
    When 消費者透過金流服務完成信用卡付款
    Then 訂單狀態變為「已付款」
    And 消費者收到付款成功通知

  # scenario_id: SCN-PAY-002
  # entities: 訂單, 付款
  Scenario: 付款失敗時訂單保留待付款
    Given 訂單處於「待付款」狀態
    When 付款因故失敗
    Then 訂單保持「待付款」狀態
    And 系統通知消費者可重新付款

  # scenario_id: SCN-PAY-003
  # entities: 訂單, 付款
  Scenario: 銀行轉帳以後五碼對帳
    Given 消費者選擇銀行轉帳並已回報匯款帳號後五碼
    When 商家完成對帳確認
    Then 訂單狀態變為「已付款」
    And 消費者收到付款確認通知

  # scenario_id: SCN-PAY-004
  # entities: 訂單, 庫存
  # 決策 CLR-260613-01#Q1：付款期限 72 小時，逾時自動取消並釋放預留（CON-ORD-002）
  Scenario: 逾時未付款訂單自動取消
    Given 訂單處於「待付款」狀態
    When 超過付款期限系統自動取消訂單
    Then 訂單狀態變為「已取消」
    And 該訂單先前扣減的庫存被回補

  # scenario_id: SCN-PAY-005
  # entities: 訂單, 發票
  Scenario: 付款完成後開立發票
    Given 訂單已付款
    When 系統自動觸發發票開立
    Then 消費者取得該訂單的電子發票
    And 發票含 5% 營業稅額
