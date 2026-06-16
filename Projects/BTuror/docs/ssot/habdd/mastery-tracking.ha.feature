# language: zh-TW
# source: docs/discovery/02-user-journeys.md#intermediate-player-step6; docs/discovery/03-event-timeline.md#11,14; docs/ssot/habdd/story-index.md#US-006
# feature-id: F-005
Feature: 認知精熟追蹤
  In order to 追蹤可遷移的橋牌認知成長而非答對率
  As a 中級卡關玩家
  I want to 檢視我的多維精熟度與錯誤模式變化

  Background:
    Given 我已登入為中級卡關玩家
    And 我已累積至少一副練習的診斷紀錄

  # scenario_id: SCN-F005-001
  # entities: 精熟度, 診斷
  Scenario: 診斷後更新多維精熟度
    Given 系統已產生一筆新的診斷
    When 系統更新學生模型
    Then 系統以機率方式更新辨識、執行、遷移、保留四個面向的精熟度

  # scenario_id: SCN-F005-002
  # entities: 精熟度
  Scenario: 呈現部分精熟狀態
    Given 玩家能辨識危險手但在複雜局面執行不穩
    When 玩家檢視某技能的精熟度
    Then 系統顯示辨識面向高、執行面向偏低的部分精熟狀態

  # scenario_id: SCN-F005-003
  # entities: 精熟度, 練習
  Scenario: 以變形局面驗證遷移
    Given 玩家已在原始局面達成正解
    When 玩家在相同認知結構但不同表面牌型的局面再次練習
    Then 系統依其表現更新遷移面向的精熟度

  # scenario_id: SCN-F005-004
  # entities: 精熟度
  Scenario: 隔期重測更新保留度
    Given 玩家曾在某技能達到穩定表現
    When 玩家於一段時間後重測同一技能
    Then 系統依其表現更新保留面向的精熟度

  # scenario_id: SCN-F005-005
  Scenario: 檢視錯誤模式時間軸
    Given 玩家已累積多副練習的診斷
    When 玩家檢視其錯誤模式時間軸
    Then 系統呈現同類認知錯誤隨時間的變化
