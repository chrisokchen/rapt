# language: zh-TW
# source: docs/discovery/02-user-journeys.md#merchant的主要旅程1
# stories: US-010
# feature-id: F-008
Feature: 商品管理
  In order to 不需技術知識就能把店內商品搬上線
  As a 商家
  I want to 建立商品、設定規格組合並控制上下架

  Background:
    Given 我已登入為商家
    And 商家店面處於營運狀態

  # scenario_id: SCN-PRODUCT-001
  # entities: 商品
  Scenario: 建立商品並儲存為草稿
    Given 商家備妥商品名稱、描述、分類、品牌與圖片
    When 商家建立該商品
    Then 商品以「草稿」狀態儲存
    And 商品不在前台顯示

  # scenario_id: SCN-PRODUCT-002
  # entities: 商品, SKU
  Scenario: 設定規格組合與 SKU
    Given 商品已建立且有「顏色 × 容量」兩種規格
    When 商家為商品建立規格組合
    Then 每個規格組合具有唯一的 SKU 代碼
    And 每個 SKU 具有獨立售價

  # scenario_id: SCN-PRODUCT-003
  # entities: SKU
  Scenario: 售價為零的 SKU 設定被拒絕
    Given 商品的某規格組合正在設定售價
    When 商家將該 SKU 售價設定為 0 元
    Then 該售價設定不被接受
    And 商家收到售價必須大於 0 的提示

  # scenario_id: SCN-PRODUCT-004
  # entities: 商品
  Scenario: 上架商品
    Given 商品資料完整且至少有一個有效 SKU
    When 商家上架該商品
    Then 商品於前台可被消費者瀏覽

  # scenario_id: SCN-PRODUCT-005
  # entities: 商品, 訂單
  Scenario: 下架商品不影響既有訂單
    Given 商品已上架且曾被消費者下單購買
    When 商家下架該商品
    Then 商品於前台不再顯示
    And 既有訂單的商品快照內容維持不變
