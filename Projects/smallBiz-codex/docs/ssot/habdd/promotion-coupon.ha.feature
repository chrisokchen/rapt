# source: docs/discovery/02-user-journeys.md#平台營運--行銷人員的主要旅程協助商家做促銷
# stories: US-014
Feature: 促銷活動與優惠券
  In order to 推動銷售並控制優惠風險
  As a 平台營運 / 行銷人員
  I want to 支援標準促銷工具、優惠券限制與折扣風險控管

  Background:
    Given 我已登入為平台營運 / 行銷人員
    And 商家準備進行促銷活動

  # scenario_id: SCN-PROMO-001
  # entities: 促銷活動, 商品, 分類
  Scenario Outline: 建立有檔期的促銷活動
    Given 商家已選定促銷適用範圍
    When 平台營運 / 行銷人員建立「<促銷類型>」促銷活動
    Then 促銷活動具有起訖時間與適用範圍
    And 活動在有效期間內影響符合條件的商品

    Examples:
      | 促銷類型 |
      | 百分比折扣 |
      | 固定金額折抵 |
      | 買 X 送 Y |

  # scenario_id: SCN-PROMO-002
  # entities: 優惠券, 會員等級
  Scenario: 建立有限制條件的優惠券
    Given 商家要發放優惠券
    When 平台營運 / 行銷人員設定優惠券限制
    Then 優惠券具有唯一代碼、最低消費、使用上限、有效期間與會員等級資格
    And 商家可降低優惠券被濫用的風險

  # scenario_id: SCN-PROMO-003
  # entities: 優惠券, 訂單
  Scenario: 一筆訂單最多使用一張優惠券
    Given 訂單已套用一張優惠券
    When 消費者再套用另一張優惠券
    Then 訂單保留既有優惠券
    And 新優惠券未納入該筆訂單金額

  # scenario_id: SCN-PROMO-004
  # entities: 促銷活動, 優惠券, 會員折扣, 點數
  Scenario: 折扣疊加規則已依釐清決策裁決
    Given 訂單同時符合活動價、優惠券、會員折扣與點數折抵
    When 系統需要計算最終折扣
    Then 此情境遵循 DEC-CLR-002 的折扣疊加規則
    And 後續規格必須以點數最後折抵為準
  # clarification_decision: DEC-CLR-002
  # source: .clarify/decisions/batch-CLR-260613-001.md#q2-cic-gap-002折扣疊加與計算順序
  # scenario_id: SCN-PROMO-005
  # entities: 促銷活動, 優惠券, 會員折扣, 點數, 訂單
  Scenario: 依決策計算可疊加折扣
    Given 訂單同時符合活動價、優惠券、會員折扣與點數折抵條件
    When 系統計算訂單折扣
    Then 活動價可與優惠券或會員折扣擇一疊加
    And 優惠券與會員折扣互斥
    And 點數折抵最後計算
