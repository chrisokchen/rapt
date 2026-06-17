# language: zh-TW
# source: docs/discovery/02-user-journeys.md#intermediate-player-step3; docs/ssot/habdd/story-index.md#US-003
# feature-id: F-002
Feature: 漸進式提示
  In order to 在不破壞 productive struggle 的前提下獲得最小協助
  As a 中級卡關玩家
  I want to 按需求逐級請求提示

  Background:
    Given 我已登入為中級卡關玩家
    And 我正在進行一副橋引管理練習

  # scenario_id: SCN-F002-001
  # entities: 提示紀錄, 練習
  Scenario: 請求第一級方向性提示
    Given 玩家在某個決策點感到不確定
    When 玩家請求提示
    Then 系統提供第一級的方向性提示
    And 系統記錄該次提示的層級

  # scenario_id: SCN-F002-002
  # entities: 提示紀錄
  Scenario: 提示逐級升級
    Given 玩家已取得第一級提示但仍無法決定
    When 玩家再次請求提示
    Then 系統提供下一個更高層級的提示
    And 系統記錄提示已升級

  # scenario_id: SCN-F002-003
  # entities: 提示紀錄
  Scenario: 提示依賴度成為認知訊號
    Given 玩家在本墩已升級提示至完整教學層級
    When 該墩決策完成
    Then 系統將本次達成正解所需的最高提示層級記錄為認知訊號

  # scenario_id: SCN-F002-004
  Scenario: 無提示自行完成決策
    Given 玩家在某個決策點未請求任何提示
    When 玩家完成該墩決策
    Then 系統記錄該決策為零提示完成
