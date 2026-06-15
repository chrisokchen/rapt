# source: docs/discovery/04-vision-kpi-scope.md#範圍邊界
# stories: US-017
Feature: 資料與權限邊界
  In order to 保護商家資料與消費者訂單隱私
  As a 平台管理員
  I want to 確保不同角色只能處理自己被授權的資料

  Background:
    Given 平台已有商家、消費者與平台管理角色
    And 平台需要隔離不同商家的資料

  # scenario_id: SCN-AUTH-001
  # entities: 商家, 商品, 訂單
  Scenario: 商家只能管理自己的商店資料
    Given 商家甲與商家乙各自擁有商品與訂單
    When 商家甲要求管理商店資料
    Then 商家甲只取得自己商店的商品與訂單
    And 商家乙的資料不包含在結果中

  # scenario_id: SCN-AUTH-002
  # entities: 消費者, 訂單
  Scenario: 消費者只能查看自己的訂單
    Given 消費者甲與消費者乙各自擁有訂單
    When 消費者甲查看訂單
    Then 消費者甲只取得自己的訂單
    And 消費者乙的訂單不包含在結果中

  # scenario_id: SCN-AUTH-003
  # entities: 平台管理員, 商家
  Scenario: 平台管理員管理平台層級資料
    Given 平台管理員負責維護平台營運
    When 平台管理員查看平台層級資料
    Then 平台管理員取得跨商家的營運管理資訊
    And 平台管理員行為保留可追蹤紀錄
