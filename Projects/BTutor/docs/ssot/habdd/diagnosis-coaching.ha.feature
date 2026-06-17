# language: zh-TW
# source: docs/discovery/02-user-journeys.md#intermediate-player-step5; docs/discovery/03-event-timeline.md#9,10,12; docs/ssot/habdd/story-index.md#US-005
# feature-id: F-004
Feature: 認知診斷與賽後教學
  In order to 理解玩家在哪個認知環節失敗並給出可解釋教學
  As a 中級卡關玩家
  I want to 在牌局結束後取得基於證據的診斷與教學

  Background:
    Given 我已登入為中級卡關玩家
    And 我已完成一副橋引管理練習

  # scenario_id: SCN-F004-001
  # entities: 診斷, 證據日誌
  Scenario: 產生基於證據的診斷
    Given 該副練習已收集到出牌軌跡、提示與推理標記
    When 系統執行認知診斷
    Then 系統產生一筆含假設、信心值與支持證據的診斷
    And 診斷引用其依據的規則

  # scenario_id: SCN-F004-002
  # entities: 證據日誌, 診斷
  Scenario: 寫入可審計證據日誌
    Given 系統已產生一筆診斷
    When 系統封存該次診斷
    Then 系統寫入可回溯的證據日誌，含證據、規則與學生模型變化量

  # scenario_id: SCN-F004-003
  # entities: 診斷
  Scenario: 安全的替代路線不判為錯誤
    Given 玩家選擇了一條非最佳但安全的合法路線
    When 系統評估該次決策
    Then 系統將其標記為風格差異而非錯誤
    And 賽後教學說明其與最佳路線的取捨

  # scenario_id: SCN-F004-004
  Scenario: 低信心診斷不過度宣稱
    Given 系統對某次失敗的成因證據不足
    When 系統產生診斷
    Then 系統以較低信心值呈現該假設
    And 賽後教學以試探語氣陳述而非斷定成因

  # scenario_id: SCN-F004-005
  Scenario: 依玩家層級調整教學語氣
    Given 玩家的程度層級已知
    When 系統產生賽後教學說明
    Then 系統依該層級調整用語密度與語氣
    And 教學內容的診斷結論維持一致

  # scenario_id: SCN-F004-006
  Scenario: 提供下一步訓練建議
    Given 診斷指出特定的認知缺口
    When 系統完成賽後教學
    Then 系統建議對應該缺口的下一步訓練
