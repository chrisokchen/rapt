# language: zh-TW
# source: docs/discovery/02-user-journeys.md#consumer的主要旅程1
# stories: US-004
# feature-id: F-004
Feature: 結帳與訂單成立
  In order to 以最少步驟完成購買且金額自動算對
  As a 消費者
  I want to 提交訂單並讓系統計算折扣、運費與稅金

  Background:
    Given 我已登入為消費者

  # scenario_id: SCN-CHECKOUT-001
  # entities: 訂單, 商品快照, 庫存
  # 決策 CLR-260613-01#Q1：下單即預留、付款轉正式扣減、逾時釋放（CON-STK-003）
  Scenario: 成功提交訂單
    Given 購物車中有上架且庫存充足的商品
    And 消費者已選擇收件資訊與付款方式
    When 消費者提交訂單
    Then 系統建立一筆「待付款」訂單並給予唯一訂單編號
    And 訂單記錄當下的商品名稱、SKU 與單價快照
    And 對應 SKU 的庫存被扣減

  # scenario_id: SCN-CHECKOUT-002
  # entities: 訂單
  Scenario Outline: 依滿額門檻計算運費
    Given 購物車商品小計為 <商品小計> 元
    When 消費者提交訂單
    Then 訂單運費為 <運費> 元

    Examples:
      | 商品小計 | 運費 |
      | 1200    | 0    |
      | 1000    | 0    |
      | 800     | 100  |

  # scenario_id: SCN-CHECKOUT-003
  # entities: 訂單, 發票
  # 決策 CLR-260613-01#Q2：稅基=折後商品額、不含運（CON-ORD-006）；順序 活動→券→點數→運費→稅（CON-ORD-008）
  Scenario: 訂單金額自動含稅
    Given 消費者已確認購物車內容與優惠
    When 消費者提交訂單
    Then 訂單總額包含自動計算的 5% 營業稅

  # scenario_id: SCN-CHECKOUT-004
  # entities: 訂單, 庫存
  Scenario: 庫存不足時訂單不成立
    Given 購物車中某 SKU 的庫存為 0
    When 消費者提交訂單
    Then 訂單不成立
    And 消費者收到該商品庫存不足的提示
