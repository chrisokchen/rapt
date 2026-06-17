# language: zh-TW
# source: docs/discovery/03-event-timeline.md#17,18,19; docs/discovery/04-vision-kpi-scope.md#in-scope; docs/ssot/habdd/story-index.md#US-013,US-014
# feature-id: F-008
Feature: 可重現重播與本體治理
  In order to 在認知理解演化時仍能重新判讀舊資料並避免本體漂移
  As a 橋藝專家標注者
  I want to 重播學習軌跡並以人工核可治理本體演化

  Background:
    Given 我已登入為具治理權限的標注者
    And 系統已封存學習事件流且本體與規則皆已版本化

  # scenario_id: SCN-F008-001
  # entities: 重播, 證據日誌
  Scenario: 除錯重播確認診斷依據
    Given 某副練習的事件流已封存
    When 標注者以原始版本重播該練習
    Then 系統重現當時的診斷與其證據，供確認規則為何如此判定

  # scenario_id: SCN-F008-002
  # entities: 重播, 規則集
  Scenario: 研究重播比較不同規則版本
    Given 同一批學習軌跡已封存
    When 標注者以另一個規則集版本重播該批軌跡
    Then 系統產出兩版本下的診斷差異供比較

  # scenario_id: SCN-F008-003
  # entities: 重播, 精熟度
  Scenario: 學生歷程重播重算精熟曲線
    Given 本體已改版
    When 標注者以新版本重播某學生的學習歷程
    Then 系統重新計算該學生的精熟度軌跡

  # scenario_id: SCN-F008-004
  # entities: 本體, 本體演化提案
  Scenario: 本體變更需具治理權限者核可
    Given 系統依遙測共現提出一則本體演化提案
    When 不具治理權限者嘗試套用該提案
    Then 系統不套用該提案
    And 系統要求由具治理權限者核可後方可生效

  # scenario_id: SCN-F008-005
  # entities: 本體演化提案, 本體
  Scenario: 核可後套用本體演化提案
    Given 一則本體演化提案已附證據並通過重播評估
    When 具治理權限者核可該提案
    Then 系統以新版本套用該本體變更
