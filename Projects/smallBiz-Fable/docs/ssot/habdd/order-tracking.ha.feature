# language: zh-TW
# source: docs/discovery/02-user-journeys.md#consumer的主要旅程1
# stories: US-006
# feature-id: F-006
Feature: 訂單追蹤與通知
  In order to 全程掌握訂單進度而不需電話詢問
  As a 消費者
  I want to 查詢訂單狀態並在狀態變更時收到通知

  Background:
    Given 我已登入為消費者

  # scenario_id: SCN-TRACK-001
  # entities: 訂單, 通知
  Scenario: 訂單狀態變更時收到通知
    Given 消費者有一筆「已付款」訂單
    When 系統自動觸發訂單狀態變更通知
    Then 消費者透過綁定的通知通道收到狀態變更訊息

  # scenario_id: SCN-TRACK-002
  Scenario: 查詢訂單物流進度
    Given 訂單已出貨且具有物流單號
    When 消費者查詢該訂單的物流進度
    Then 顯示物流業者回報的目前配送狀態

  # scenario_id: SCN-TRACK-003
  # entities: 訂單, 會員
  Scenario: 無法查詢他人的訂單
    Given 存在一筆屬於其他會員的訂單
    When 消費者查詢非本人的訂單
    Then 查詢被拒絕
    And 系統不顯示任何該訂單的內容
