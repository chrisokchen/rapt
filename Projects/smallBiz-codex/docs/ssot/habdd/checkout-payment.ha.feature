# source: docs/discovery/02-user-journeys.md#一般網購消費者的主要旅程從瀏覽到售後
# stories: US-007, US-008, US-009
Feature: 結帳與付款
  In order to 讓消費者以清楚金額完成購買
  As a 一般網購消費者
  I want to 提交訂單、選擇付款方式並取得付款結果

  Background:
    Given 我以一般網購消費者身分使用商店
    And 購物車中有至少一個可販售商品

  # scenario_id: SCN-CHECKOUT-001
  # entities: 購物車, 訂單, 收件資訊
  Scenario: 以必要資訊提交訂單
    Given 消費者已確認購物車商品與收件資訊
    When 消費者提交訂單
    Then 系統建立一筆具有唯一編號的訂單
    And 訂單狀態成為「待付款」

  # scenario_id: SCN-CHECKOUT-002
  # entities: 訂單, 付款
  Scenario Outline: 使用支援的付款方式完成付款
    Given 訂單狀態為「待付款」
    When 消費者以「<付款方式>」完成付款
    Then 訂單狀態成為「已付款」
    And 消費者取得付款完成通知

    Examples:
      | 付款方式 |
      | 信用卡 |
      | PayPal |
      | 銀行轉帳 |

  # scenario_id: SCN-CHECKOUT-003
  # entities: 訂單, 優惠, 運費, 稅金
  Scenario: 顯示可追溯的訂單金額
    Given 購物車商品、優惠資格、運費門檻與稅金規則皆已確定
    When 系統計算訂單金額
    Then 訂單呈現商品小計、優惠、運費、稅金與應付總額
    And 商家與消費者看到一致的訂單金額

  # scenario_id: SCN-CHECKOUT-004
  # entities: 訂單, 優惠
  Scenario: 優惠不符合資格時維持原訂單金額
    Given 消費者的訂單不符合優惠使用資格
    When 消費者套用優惠
    Then 訂單金額維持未套用該優惠的結果
    And 消費者得知優惠未被採用的原因

  # scenario_id: SCN-CHECKOUT-005
  # entities: 訂單, 稅金
  Scenario: 稅基規則已依釐清決策裁決
    Given 訂單同時包含商品金額、優惠與運費
    When 系統需要計算營業稅
    Then 此情境遵循 DEC-CLR-005 的稅基規則
    And 後續規格必須以折扣與點數折抵後的商品金額為稅基
  # clarification_decision: DEC-CLR-005
  # source: .clarify/decisions/batch-CLR-260613-001.md#q5-cic-gap-0055-營業稅稅基
  # scenario_id: SCN-CHECKOUT-006
  # entities: 訂單, 稅金, 優惠, 運費
  Scenario: 依決策計算 5% 營業稅
    Given 訂單包含商品小計、活動折扣、優惠券、會員折扣、點數折抵與運費
    When 系統計算訂單稅金
    Then 稅基為商品小計扣除活動、優惠券、會員折扣與點數折抵後的商品金額
    And 稅基不包含運費
    And 營業稅率為 5%
