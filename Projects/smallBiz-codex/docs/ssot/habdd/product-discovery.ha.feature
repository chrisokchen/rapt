# source: docs/discovery/02-user-journeys.md#一般網購消費者的主要旅程從瀏覽到售後
# stories: US-003, US-004
Feature: 商品探索與購物意向保存
  In order to 快速找到商品並保留購買意向
  As a 一般網購消費者
  I want to 瀏覽商品、理解價格並保存想買的商品

  Background:
    Given 我以一般網購消費者身分使用商店
    And 商店已有可販售商品

  # scenario_id: SCN-DISC-001
  # entities: 商品, 分類, SKU
  Scenario: 取得可販售商品資訊
    Given 商品已上架且仍有可販售庫存
    When 消費者瀏覽商品
    Then 消費者取得商品名稱、分類、售價、原價與庫存狀態
    And 消費者能判斷商品是否符合購買需求

  # scenario_id: SCN-DISC-002
  # entities: 商品, 願望清單
  Scenario: 收藏尚未立即購買的商品
    Given 消費者看到感興趣的可販售商品
    When 消費者收藏商品
    Then 商品被保存到消費者的願望清單
    And 消費者日後可找回該商品

  # scenario_id: SCN-DISC-003
  # entities: 購物車, SKU
  Scenario: 保留購物車內容
    Given 消費者已將商品加入購物車
    When 消費者稍後回到商店
    Then 購物車保留先前加入的商品與數量
    And 消費者可繼續準備結帳

  # scenario_id: SCN-DISC-004
  # entities: 商品, SKU
  Scenario: 商品售完時不可加入購物車
    Given 商品目前沒有可販售庫存
    When 消費者嘗試加入購物車
    Then 購物車不新增該商品
    And 消費者得知商品目前無法購買
