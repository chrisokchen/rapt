# language: zh-TW
# source: docs/discovery/01-stakeholders.md#parent-school; .clarify/decisions/batch-CLR-260616-01.md#Q8; docs/ssot/habdd/story-index.md#US-015
# feature-id: F-009
Feature: 家長認知進展檢視
  In order to 了解孩子的專注、規劃與推理能力成長
  As a 家長
  I want to 檢視我所監護學習者的認知進展

  Background:
    Given 我已登入為家長
    And 我與某學習者存在監護關係

  # scenario_id: SCN-F009-001
  # entities: 精熟度, 監護關係
  Scenario: 檢視監護學習者的認知進展
    Given 我監護的學習者已累積練習與精熟紀錄
    When 家長檢視該學習者的認知進展
    Then 系統呈現該學習者各認知面向的精熟度與成長趨勢

  # scenario_id: SCN-F009-002
  # entities: 精熟度, 監護關係
  Scenario: 不得檢視非監護學習者的資料
    Given 某學習者與該家長不存在監護關係
    When 家長嘗試檢視該學習者的認知進展
    Then 系統不提供該學習者的資料
