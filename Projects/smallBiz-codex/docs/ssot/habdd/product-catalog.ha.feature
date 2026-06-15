# source: docs/discovery/02-user-journeys.md#中小零售店老闆--商家的主要旅程建立並營運線上商店
# stories: US-001, US-002
Feature: 商品與銷售單位管理
  In order to 讓實體商品能轉為可販售的線上商品
  As a 中小零售店老闆 / 商家
  I want to 建立商品、SKU、分類與販售狀態

  Background:
    Given 我已登入為中小零售店老闆 / 商家
    And 商家正在經營自己的線上商店

  # scenario_id: SCN-CATALOG-001
  # entities: 商品, SKU, 分類
  Scenario: 建立多規格商品
    Given 商家準備販售一項有多種規格的商品
    When 商家建立商品與每個可銷售規格
    Then 商品包含可辨識的 SKU、售價與分類
    And 商品維持「草稿」狀態

  # scenario_id: SCN-CATALOG-002
  # entities: 商品, SKU
  Scenario: 上架已完成設定的商品
    Given 商品已有名稱、分類、圖片、SKU、售價與庫存
    When 商家上架商品
    Then 商品成為可販售商品
    And 消費者可取得商品資訊與庫存狀態

  # scenario_id: SCN-CATALOG-003
  # entities: 商品, SKU
  Scenario: 缺少可銷售規格時維持草稿
    Given 商品尚未建立任何可銷售規格
    When 商家要求上架商品
    Then 商品維持「草稿」狀態
    And 商家取得缺少銷售規格的說明

  # scenario_id: SCN-CATALOG-004
  # entities: 商品
  Scenario: 下架不再販售的商品
    Given 商品目前為可販售商品
    When 商家下架商品
    Then 商品不再接受新的購買
    And 歷史訂單保留商品快照
