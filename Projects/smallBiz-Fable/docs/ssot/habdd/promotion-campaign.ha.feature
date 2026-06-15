# language: zh-TW
# source: docs/discovery/02-user-journeys.md#促銷活動操作
# stories: US-015
# feature-id: F-013
Feature: 促銷活動
  In order to 讓檔期活動自動上下架、不靠人工切換
  As a 商家
  I want to 建立有檔期的促銷活動

  Background:
    Given 我已登入為商家
    And 商家店面處於營運狀態

  # scenario_id: SCN-PROMO-001
  # entities: 促銷活動
  Scenario: 建立有檔期的促銷活動
    Given 商家已決定活動類型與檔期起迄時間
    When 商家建立該促銷活動
    Then 促銷活動以「排程中」狀態儲存

  # scenario_id: SCN-PROMO-002
  # entities: 促銷活動
  Scenario: 檔期開始時活動自動生效
    Given 促銷活動處於「排程中」且檔期開始時間已到
    When 系統自動觸發活動生效
    Then 活動優惠於前台生效

  # scenario_id: SCN-PROMO-003
  # entities: 促銷活動
  Scenario: 檔期結束時活動自動失效
    Given 促銷活動正在生效中且檔期結束時間已到
    When 系統自動觸發活動失效
    Then 活動優惠於前台停止套用
    And 商品恢復以原售價販售

  # scenario_id: SCN-PROMO-004
  # entities: 促銷活動, 訂單
  # 決策 CLR-260613-01#Q2：疊加順序 活動→券→點數（CON-ORD-008）；本 scenario 驗證單一活動效果
  Scenario Outline: 依活動類型套用優惠
    Given 商家的「<活動類型>」促銷活動正在生效中
    When 消費者購買活動範圍內的商品
    Then 訂單金額依「<優惠效果>」計算

    Examples:
      | 活動類型     | 優惠效果               |
      | 百分比折扣   | 商品售價乘以折扣比例     |
      | 滿額折現     | 達門檻後減去固定金額     |
      | 買X送Y      | 加贈指定的贈送商品       |
