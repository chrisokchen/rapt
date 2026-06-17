# language: zh-TW
# source: docs/discovery/02-user-journeys.md#intermediate-player; docs/ssot/habdd/story-index.md#US-001,US-002
# feature-id: F-001
Feature: 橋引管理練習
  In order to 在可診斷的場景中練習橋引管理並留下認知軌跡
  As a 中級卡關玩家
  I want to 開始一副 curated 牌例並逐墩打牌

  Background:
    Given 我已登入為中級卡關玩家
    And 系統已備妥已標注的 Entry Management curated 牌例

  # scenario_id: SCN-F001-001
  # entities: 練習, 牌例
  Scenario: 成功開始一副橋引管理練習
    Given 一副已標注的 Entry Management 牌例可供練習
    When 玩家開始該牌例的練習
    Then 系統建立一筆新的練習
    And 玩家看到該牌局的起始局面

  # scenario_id: SCN-F001-002
  # entities: 出牌紀錄, 練習
  Scenario: 出牌被記錄為認知軌跡
    Given 玩家正在進行一副練習且輪到其決策
    When 玩家從合法牌中選出一張牌
    Then 系統記錄該次出牌、當時的合法牌、思考時間與悔牌次數
    And 該墩進入下一個決策點

  # scenario_id: SCN-F001-003
  # entities: 出牌紀錄
  Scenario: 悔牌與重新決策被記錄
    Given 玩家已暫定一張出牌
    When 玩家收回該決策並改選另一張牌
    Then 系統將此次計畫變更記錄為認知軌跡的一部分

  # scenario_id: SCN-F001-004
  # entities: 出牌紀錄
  Scenario: 拒絕非法出牌
    Given 玩家正在進行一副練習且輪到其決策
    When 玩家嘗試打出一張不合規則的牌
    Then 系統不接受該次出牌
    And 系統提示玩家僅能從合法牌中選擇

  # scenario_id: SCN-F001-005
  # entities: 練習
  Scenario: 青少年以淺層認知層級練習
    Given 青少年學習者已登入且選擇 MiniBridge 練習
    When 學習者開始一副以淺層 ontology 標注的牌例
    Then 系統以適齡的認知層級載入該牌局
    And 系統僅追蹤基礎打牌認知訊號
