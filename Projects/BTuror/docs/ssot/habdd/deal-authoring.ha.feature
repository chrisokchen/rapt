# language: zh-TW
# source: docs/discovery/02-user-journeys.md#domain-expert-annotator; docs/discovery/03-event-timeline.md#1,2,3; docs/ssot/habdd/story-index.md#US-011,US-012
# feature-id: F-007
Feature: 牌例與本體標注
  In order to 讓診斷引擎可運作並使資料可重現與可演化
  As a 橋藝專家標注者
  I want to 標注 curated 牌例並發布版本化的本體與規則

  Background:
    Given 我已登入為橋藝專家標注者
    And 系統已備妥可標注的牌例工作區

  # scenario_id: SCN-F007-001
  # entities: 牌例
  Scenario: 成功匯入並標注 curated 牌例
    Given 一副待標注的 Entry Management 牌例
    When 標注者完成該牌例的局面標注
    Then 系統儲存含關鍵時刻、所需技能、可接受路線與常見錯誤的標注
    And 該牌例成為可供練習與診斷的牌例

  # scenario_id: SCN-F007-002
  # entities: 牌例
  Scenario: 拒絕缺漏關鍵欄位的標注
    Given 標注者提交的局面標注缺少關鍵時刻或所需技能
    When 系統檢核該標注
    Then 系統不接受該標注
    And 系統指出缺漏的關鍵欄位

  # scenario_id: SCN-F007-003
  # entities: 本體, 規則集
  Scenario: 發布版本化的本體與規則集
    Given 標注者已完成一組本體與診斷規則的修訂
    When 標注者發布該修訂
    Then 系統以新版本號記錄該本體與規則集
    And 既有牌例標注標明其依據的版本
