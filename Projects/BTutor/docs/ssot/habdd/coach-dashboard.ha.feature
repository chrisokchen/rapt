# language: zh-TW
# source: docs/discovery/02-user-journeys.md#human-coach; docs/discovery/03-event-timeline.md#15,16; docs/ssot/habdd/story-index.md#US-007,US-008,US-009
# feature-id: F-006
Feature: 教練儀表板與派題
  In order to 省下判斷弱點的時間並專注高層教學
  As a 人類教練
  I want to 檢視學生認知分析並派發針對性訓練

  Background:
    Given 我已登入為人類教練
    And 我負責的學生已累積練習與診斷資料

  # scenario_id: SCN-F006-001
  # entities: 精熟度, 診斷
  Scenario: 檢視學生認知分析
    Given 某學生已有多副練習的診斷紀錄
    When 教練開啟該學生的認知分析
    Then 教練看到誤解趨勢、精熟演化、遷移失敗與提示依賴度

  # scenario_id: SCN-F006-002
  # entities: 證據日誌, 診斷
  Scenario: 回溯診斷的證據日誌
    Given 教練對某次 AI 診斷有疑慮
    When 教練檢視該次診斷的證據日誌
    Then 教練看到系統判定該認知失敗的完整證據與規則依據

  # scenario_id: SCN-F006-003
  # entities: 診斷
  Scenario: 標記 AI 與教練診斷分歧
    Given 教練檢視了某次診斷的證據日誌
    When 教練標記其與 AI 診斷意見不一致
    Then 系統記錄此分歧供後續本體檢討

  # scenario_id: SCN-F006-004
  # entities: 指派, 練習
  Scenario: 派發針對性訓練
    Given 教練在分析中發現學生卡在某認知缺口
    When 教練指派對應該缺口的牌例給該學生
    Then 該學生收到該指派
    And 該指派與目標認知缺口關聯記錄

  # scenario_id: SCN-F006-005
  # entities: 精熟度
  # source: CLR-260616-01#Q6
  Scenario: 依學生與技能篩選認知分析
    Given 教練負責的學生已累積多筆診斷
    When 教練以特定學生與特定認知技能篩選分析
    Then 系統僅呈現符合該篩選條件的誤解趨勢與精熟資料
