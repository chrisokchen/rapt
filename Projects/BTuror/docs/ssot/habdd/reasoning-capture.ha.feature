# language: zh-TW
# source: docs/discovery/02-user-journeys.md#intermediate-player-step4; docs/ssot/habdd/story-index.md#US-004
# feature-id: F-003
Feature: 推理標記蒐集
  In order to 取得可解釋的 cognitive intent 訊號而不中斷心流
  As a 中級卡關玩家
  I want to 在關鍵時刻標記我的推理

  Background:
    Given 我已登入為中級卡關玩家
    And 我正在進行一副橋引管理練習

  # scenario_id: SCN-F003-001
  # entities: 推理標記
  Scenario: 長考時觸發推理標記蒐集
    Given 系統偵測到玩家在某決策點出現長考
    When 玩家從推理標籤中選擇其考量
    Then 系統記錄該推理標記與所屬墩次

  # scenario_id: SCN-F003-002
  # entities: 推理標記
  Scenario: 關鍵錯誤後觸發推理標記蒐集
    Given 系統在玩家出牌後偵測到關鍵錯誤
    When 玩家標記其當下的推理考量
    Then 系統記錄該推理標記作為診斷輔助訊號

  # scenario_id: SCN-F003-003
  Scenario: 玩家略過推理標記以維持心流
    Given 系統在觸發點邀請玩家標記推理
    When 玩家略過此次標記
    Then 系統不中斷練習並繼續下一個決策
