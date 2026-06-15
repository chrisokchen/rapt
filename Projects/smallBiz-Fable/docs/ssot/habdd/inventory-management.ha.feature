# language: zh-TW
# source: docs/discovery/02-user-journeys.md#merchant的主要旅程1
# stories: US-011
# feature-id: F-009
Feature: 庫存管理
  In order to 賣一個扣一個、不再讓客人付款後才知道缺貨
  As a 商家
  I want to 以 SKU 為單位管理即時庫存

  Background:
    Given 我已登入為商家

  # scenario_id: SCN-STOCK-001
  # entities: 庫存, SKU
  Scenario: 設定 SKU 庫存量
    Given 商品的 SKU 已建立
    When 商家將該 SKU 庫存設定為 50 件
    Then 該 SKU 的可售庫存為 50 件

  # scenario_id: SCN-STOCK-002
  # entities: 庫存, 訂單
  Scenario: 訂單成立時自動扣減庫存
    Given 某 SKU 的庫存為 5 件
    When 含該 SKU 2 件的訂單成立
    Then 該 SKU 的庫存變為 3 件

  # scenario_id: SCN-STOCK-003
  # entities: 庫存, 通知
  Scenario: 低於水位時通知補貨
    Given 商家將某 SKU 的補貨水位設定為 10 件
    And 該 SKU 目前庫存為 11 件
    When 銷售使該 SKU 庫存降至 9 件
    Then 商家收到補貨提醒通知

  # scenario_id: SCN-STOCK-004
  # entities: 庫存, 訂單
  # 決策 CLR-260613-01#Q1：下單預留+逾時釋放落實防超賣，可售=quantity-reservedQuantity（CON-STK-001/003）
  Scenario: 最後一件商品不被超賣
    Given 某 SKU 庫存僅剩 1 件
    And 兩位消費者的購物車都包含該 SKU
    When 兩位消費者先後提交訂單
    Then 只有先提交者的訂單成立
    And 後提交者收到庫存不足的提示
